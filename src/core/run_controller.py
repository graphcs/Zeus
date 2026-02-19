"""Run Controller - Orchestrates the 7-phase Zeus pipeline."""

import asyncio
import logging
import time
from typing import Callable

logger = logging.getLogger(__name__)
from src.models.schemas import (
    ZeusRequest,
    ZeusResponse,
    RunRecord,
    BudgetUsed,
    BudgetConfig,
    InventorConfig,
    CrossCritique,
    SelfEvaluationScorecard,
)
from src.llm.openrouter import OpenRouterClient, OpenRouterError, OpenRouterTimeoutError
from src.core.normalizer import Normalizer
from src.core.inventor import Inventor
from src.core.synthesizer import Synthesizer
from src.core.library_loader import LibraryLoader
from src.core.library_critic import LibraryCritic
from src.core.refiner import Refiner
from src.core.assembler import Assembler
from src.core.persistence import Persistence
from src.prompts.intake import IntakePrompts
from src.prompts.inventor import InventorPrompts
from src.prompts.synthesis import SynthesisPrompts
from src.prompts.library_critique import LibraryCritiquePrompts
from src.prompts.refinement import RefinementPrompts
from src.prompts.assembly import AssemblyPrompts


class BudgetExceededError(Exception):
    """Raised when LLM call budget is exhausted."""
    pass


class RunController:
    """Orchestrates the 7-phase Zeus pipeline.

    Pipeline:
        Phase 0: Intake → ProblemBrief
        Phase 1: Divergent Generation → InventorSolutions (parallel)
        Phase 2: Cross-Pollination → CrossCritiques (optional, parallel)
        Phase 3: Convergent Synthesis → SynthesisResult
        Phase 4: Library-Informed Critique → LibraryCritiqueResult (parallel)
        Phase 5: Iterative Refinement → final_draft (bounded loop)
        Phase 6: Output Assembly → ZeusResponse (5 deliverables)

    Invariants:
        1. Every synthesis draft gets library-informed critique
        2. Every run gets a unique run_id and persisted RunRecord
        3. assumptions[] and known_issues[] always present in output
        4. Constraints never silently dropped
        5. Budget enforcement with configurable caps
        6. Failures yield best-effort output with logged errors
        7. Each phase module independently replaceable
        8. Model + prompt versions recorded in RunRecord
        9. RunRecords are append-only
    """

    DEFAULT_BUDGET = BudgetConfig()

    def __init__(
        self,
        llm_client: OpenRouterClient,
        persistence: Persistence | None = None,
        on_progress: Callable[[str], None] | None = None,
        budget_config: BudgetConfig | None = None,
        library_paths: list[str] | None = None,
    ):
        self.llm = llm_client
        self.persistence = persistence or Persistence()
        self.on_progress = on_progress or (lambda msg: None)
        self.budget_config = budget_config or self.DEFAULT_BUDGET

        # Initialize library loader
        self.library_loader = LibraryLoader(user_paths=library_paths)

        # Initialize pipeline components
        self.normalizer = Normalizer(llm_client)
        self.inventor = Inventor(llm_client, self.library_loader)
        self.synthesizer = Synthesizer(llm_client, self.library_loader)
        self.library_critic = LibraryCritic(llm_client, self.library_loader)
        self.refiner = Refiner(llm_client, self.library_loader)
        self.assembler = Assembler(llm_client)

    async def run(self, request: ZeusRequest) -> ZeusResponse:
        """Execute the full 7-phase pipeline.

        Args:
            request: The Zeus request to process.

        Returns:
            The final ZeusResponse.
        """
        # Load user-specified library paths
        if request.library_paths:
            self.library_loader = LibraryLoader(user_paths=request.library_paths)
            self.inventor = Inventor(self.llm, self.library_loader)
            self.synthesizer = Synthesizer(self.llm, self.library_loader)
            self.library_critic = LibraryCritic(self.llm, self.library_loader)
            self.refiner = Refiner(self.llm, self.library_loader)

        record = RunRecord(
            request=request,
            model_version=self.llm.model,
            prompt_versions=self._get_prompt_versions(),
        )

        start_time = time.monotonic()

        try:
            await self._execute_pipeline(request, record)

        except BudgetExceededError as e:
            logger.error(f"Budget exceeded: {e}")
            record.errors.append(f"Budget exceeded: {str(e)}")

        except OpenRouterTimeoutError as e:
            elapsed = time.monotonic() - start_time
            msg = f"LLM call timeout: {str(e)} (run elapsed: {elapsed:.1f}s)"
            logger.error(msg)
            record.errors.append(msg)

        except OpenRouterError as e:
            logger.error(f"LLM error: {e}")
            record.errors.append(f"LLM error: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            record.errors.append(f"Unexpected error: {str(e)}")

        finally:
            # Assemble best-effort output if not already assembled
            if record.final_response is None:
                logger.info("Attempting best-effort assembly after pipeline error...")
                try:
                    self.on_progress("Assembling output...")
                    response, assembly_usage = await self.assembler.assemble(record)
                    self._update_budget(record, assembly_usage)
                    record.final_response = response
                except Exception as e:
                    logger.error(f"Assembly also failed: {e}")
                    record.errors.append(f"Assembly failed: {str(e)}")
                    record.final_response = self.assembler._error_response(record)

            # INVARIANT: Every run has a persisted RunRecord
            if record.errors:
                logger.error(f"Run completed with {len(record.errors)} error(s):")
                for err in record.errors:
                    logger.error(f"  • {err}")
            self.on_progress("Saving run record...")
            self.persistence.save(record)
            logger.info(f"Run record saved: {record.run_id}")

        return record.final_response

    async def _execute_pipeline(self, request: ZeusRequest, record: RunRecord) -> None:
        """Execute all 7 phases of the pipeline."""

        # ── Phase 0: Intake ────────────────────────────────────
        self.on_progress("Phase 0: Normalizing input...")
        logger.info("Phase 0: Intake — normalizing request into ProblemBrief")
        self._check_budget(record, "intake")
        record.problem_brief, usage = await self.normalizer.normalize(request)
        self._update_budget(record, usage)
        logger.info(
            f"Phase 0 complete — classified as '{record.problem_brief.classification.problem_type}', "
            f"{len(record.problem_brief.constraints)} constraints, "
            f"{len(record.problem_brief.objectives)} objectives  "
            f"[budget: {record.budget_used.llm_calls} calls]"
        )

        # ── Phase 1: Divergent Generation ─────────────────────
        self.on_progress("Phase 1: Running parallel inventors...")
        configs = self._build_inventor_configs(request, record)
        record.inventor_configs = configs
        logger.info(
            f"Phase 1: Launching {len(configs)} parallel inventors: "
            f"{', '.join(f'{c.inventor_id}({c.inventor_type})' for c in configs)}"
        )

        self._check_budget(record, "inventors")
        solutions, inv_usage = await self.inventor.generate_solutions(
            record.problem_brief, configs
        )
        record.inventor_solutions = solutions
        self._update_budget_aggregate(record, inv_usage)

        # Need at least 1 valid solution to continue
        valid_solutions = [s for s in solutions if not s.content.startswith("[Inventor")]
        logger.info(
            f"Phase 1 complete — {len(valid_solutions)}/{len(solutions)} valid solutions  "
            f"[budget: {record.budget_used.llm_calls} calls]"
        )
        if not valid_solutions:
            logger.error("All inventors failed — no valid solutions produced")
            record.errors.append("All inventors failed — no valid solutions produced")
            return

        # ── Phase 2: Cross-Pollination (optional) ─────────────
        if request.enable_cross_pollination and len(valid_solutions) >= 2:
            remaining = self.budget_config.max_llm_calls - record.budget_used.llm_calls
            cross_poll_budget = min(remaining // 2, len(valid_solutions) * 2)
            if cross_poll_budget >= 2:
                self.on_progress("Phase 2: Cross-pollination...")
                logger.info(f"Phase 2: Cross-pollination with {len(valid_solutions)} solutions")
                cross_critiques, cp_usage = await self._run_cross_pollination(
                    valid_solutions, record
                )
                record.cross_critiques = cross_critiques
                self._update_budget_aggregate(record, cp_usage)
                logger.info(
                    f"Phase 2 complete — {len(cross_critiques)} critiques  "
                    f"[budget: {record.budget_used.llm_calls} calls]"
                )
        else:
            logger.info("Phase 2: Skipped (cross-pollination disabled or <2 solutions)")

        # ── Phase 3: Convergent Synthesis ──────────────────────
        self.on_progress("Phase 3: Synthesizing solutions...")
        logger.info("Phase 3: Synthesizing inventor solutions into unified draft")
        self._check_budget(record, "synthesis")
        synthesis_result, syn_usage = await self.synthesizer.synthesize(
            record.problem_brief,
            record.inventor_solutions,
            record.cross_critiques if record.cross_critiques else None,
        )
        record.synthesis_result = synthesis_result
        self._update_budget(record, syn_usage)

        if not synthesis_result.unified_draft:
            logger.error("Synthesis produced empty draft")
            record.errors.append("Synthesis produced empty draft")
            return
        logger.info(
            f"Phase 3 complete — draft length {len(synthesis_result.unified_draft)} chars, "
            f"{len(synthesis_result.open_issues)} open issues  "
            f"[budget: {record.budget_used.llm_calls} calls]"
        )

        # ── Phase 4: Library-Informed Critique ─────────────────
        self.on_progress("Phase 4: Running library critics...")
        remaining = self.budget_config.max_llm_calls - record.budget_used.llm_calls
        logger.info(f"Phase 4: Running 6 parallel library critics (budget remaining: {remaining} calls)")
        if remaining >= 1:
            critique_result, crit_usage = await self.library_critic.critique(
                synthesis_result.unified_draft,
                record.problem_brief.eval_criteria,
            )
            record.library_critique = critique_result
            self._update_budget_aggregate(record, crit_usage)
            logger.info(
                f"Phase 4 complete — {critique_result.blocker_count} blockers, "
                f"{critique_result.major_count} major, {critique_result.minor_count} minor issues  "
                f"[budget: {record.budget_used.llm_calls} calls]"
            )

        # ── Phase 5: Iterative Refinement ──────────────────────
        remaining = self.budget_config.max_llm_calls - record.budget_used.llm_calls
        if record.library_critique and remaining >= 2:
            blockers = record.library_critique.blocker_count
            majors = record.library_critique.major_count
            if blockers > 0 or majors > 0:
                self.on_progress("Phase 5: Refining draft...")
                logger.info(
                    f"Phase 5: Refining draft — {blockers} blockers, {majors} major issues "
                    f"(max {self.budget_config.max_revisions} revisions, {remaining} calls left)"
                )
                final_draft, history, ref_usage = await self.refiner.refine(
                    synthesis_result.unified_draft,
                    record.library_critique,
                    record.problem_brief,
                    max_revisions=self.budget_config.max_revisions,
                    budget_remaining=remaining,
                )
                record.final_draft = final_draft
                record.refinement_history = history
                self._update_budget_aggregate(record, ref_usage)
                logger.info(
                    f"Phase 5 complete — {len(history)} revision(s)  "
                    f"[budget: {record.budget_used.llm_calls} calls]"
                )
            else:
                logger.info("Phase 5: Skipped — no blocker/major issues found")
                record.final_draft = synthesis_result.unified_draft
        else:
            logger.info("Phase 5: Skipped — no critique or budget exhausted")
            record.final_draft = synthesis_result.unified_draft

        # ── Phase 6: Output Assembly ───────────────────────────
        self.on_progress("Phase 6: Assembling deliverables...")
        logger.info("Phase 6: Assembling 5 deliverables + evaluation scorecard")
        response, asm_usage = await self.assembler.assemble(record)
        self._update_budget(record, asm_usage)
        record.final_response = response
        logger.info(
            f"Phase 6 complete — score {response.total_score:.1f}/{response.max_score:.0f} "
            f"({response.score_percentage:.1f}%)  "
            f"[total budget: {record.budget_used.llm_calls} calls, "
            f"{record.budget_used.tokens_in + record.budget_used.tokens_out} tokens]"
        )

    async def _run_cross_pollination(
        self, solutions, record
    ) -> tuple[list[CrossCritique], dict[str, int]]:
        """Run cross-pollination: each inventor critiques one other."""
        total_usage = {"tokens_in": 0, "tokens_out": 0, "llm_calls": 0}
        critiques = []

        # Each inventor critiques the next (circular)
        tasks = []
        for i, sol in enumerate(solutions):
            target_idx = (i + 1) % len(solutions)
            target = solutions[target_idx]

            # Summarize own solution
            own_summary = sol.content[:2000] if sol.content else "No solution"
            target_content = target.content[:5000] if target.content else "No solution"

            prompt = InventorPrompts.CROSS_CRITIQUE.format(
                critic_id=sol.inventor_id,
                critic_type=sol.inventor_type,
                own_solution_summary=own_summary,
                target_id=target.inventor_id,
                target_solution=target_content,
                problem_brief=record.problem_brief.problem_statement,
            )

            tasks.append(self._run_single_cross_critique(
                prompt, sol.inventor_id, target.inventor_id
            ))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                continue
            critique, usage = result
            critiques.append(critique)
            total_usage["tokens_in"] += usage.get("tokens_in", 0)
            total_usage["tokens_out"] += usage.get("tokens_out", 0)
            total_usage["llm_calls"] += 1

        return critiques, total_usage

    async def _run_single_cross_critique(
        self, prompt: str, critic_id: str, target_id: str
    ) -> tuple[CrossCritique, dict[str, int]]:
        """Run a single cross-critique."""
        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=InventorPrompts.SYSTEM,
            temperature=0.5,
        )

        critique = CrossCritique(
            critic_id=critic_id,
            target_id=target_id,
            disagreements=response.get("disagreements", []),
            missed_elements=response.get("missed_elements", []),
            strengths=response.get("strengths", []),
        )

        return critique, usage

    def _build_inventor_configs(self, request: ZeusRequest, record: RunRecord) -> list[InventorConfig]:
        """Build inventor configurations based on problem classification."""
        num_inventors = request.num_inventors
        classification = record.problem_brief.classification if record.problem_brief else None

        configs = []

        # Standard inventor lineup (A through E)
        inventor_defs = [
            ("A", "foundational"),
            ("B", "competitive"),
            ("C", "comprehensive"),
            ("D", "tabula_rasa"),
            ("E", "domain_specific"),
        ]

        for i, (inv_id, inv_type) in enumerate(inventor_defs[:num_inventors]):
            type_info = InventorPrompts.INVENTOR_TYPES.get(inv_type, {})
            libraries = list(type_info.get("libraries", []))

            # Domain-specific inventor gets libraries based on classification
            if inv_type == "domain_specific" and classification:
                libraries = list(classification.recommended_library_emphasis)
                if not libraries:
                    libraries = ["first_principles", "technologies"]

            configs.append(InventorConfig(
                inventor_id=inv_id,
                inventor_type=inv_type,
                library_assignments=libraries,
                emphasis=type_info.get("emphasis", ""),
            ))

        return configs

    def _check_budget(self, record: RunRecord, phase: str) -> None:
        """Check if budget allows another LLM call."""
        if record.budget_used.llm_calls >= self.budget_config.max_llm_calls:
            raise BudgetExceededError(
                f"LLM call budget exhausted at phase '{phase}'. "
                f"Used {record.budget_used.llm_calls}/{self.budget_config.max_llm_calls} calls."
            )

    def _update_budget(self, record: RunRecord, usage: dict[str, int]) -> None:
        """Update budget from a single-call usage dict."""
        record.budget_used.llm_calls += usage.get("llm_calls", 1)
        record.budget_used.tokens_in += usage.get("tokens_in", 0)
        record.budget_used.tokens_out += usage.get("tokens_out", 0)

    def _update_budget_aggregate(self, record: RunRecord, usage: dict[str, int]) -> None:
        """Update budget from an aggregated usage dict (multiple calls)."""
        record.budget_used.llm_calls += usage.get("llm_calls", 0)
        record.budget_used.tokens_in += usage.get("tokens_in", 0)
        record.budget_used.tokens_out += usage.get("tokens_out", 0)

    def _get_prompt_versions(self) -> dict:
        """Get prompt version info for traceability."""
        versions = {}
        versions.update(IntakePrompts.get_version_info())
        versions.update(InventorPrompts.get_version_info())
        versions.update(SynthesisPrompts.get_version_info())
        versions.update(LibraryCritiquePrompts.get_version_info())
        versions.update(RefinementPrompts.get_version_info())
        versions.update(AssemblyPrompts.get_version_info())
        return versions


async def run_zeus(
    prompt: str,
    constraints: list[str] | None = None,
    objectives: list[str] | None = None,
    context: str | dict | None = None,
    library_paths: list[str] | None = None,
    output_spec_path: str | None = None,
    eval_criteria_path: str | None = None,
    enable_cross_pollination: bool = False,
    num_inventors: int = 4,
    api_key: str | None = None,
    model: str | None = None,
    on_progress: Callable[[str], None] | None = None,
    max_llm_calls: int | None = None,
    max_revisions: int | None = None,
    per_call_timeout: float | None = None,
) -> ZeusResponse:
    """Convenience function to run Zeus.

    Args:
        prompt: The input prompt / problem statement.
        constraints: Optional list of constraints.
        objectives: Optional list of objectives.
        context: Optional context.
        library_paths: Optional paths to library files.
        output_spec_path: Optional path to output specification file.
        eval_criteria_path: Optional path to evaluation criteria file.
        enable_cross_pollination: Enable Phase 2 cross-pollination.
        num_inventors: Number of parallel inventors (default 4).
        api_key: Optional API key (uses env var if not provided).
        model: Optional model override.
        on_progress: Optional progress callback.
        max_llm_calls: Optional hard cap on LLM calls.
        max_revisions: Optional max refinement iterations.
        per_call_timeout: Optional timeout per LLM call in seconds.

    Returns:
        The ZeusResponse with 5 deliverables and evaluation scorecard.
    """
    request = ZeusRequest(
        prompt=prompt,
        constraints=constraints or [],
        objectives=objectives or [],
        context=context,
        library_paths=library_paths or [],
        output_spec_path=output_spec_path,
        eval_criteria_path=eval_criteria_path,
        enable_cross_pollination=enable_cross_pollination,
        num_inventors=num_inventors,
    )

    budget_kwargs = {}
    if max_llm_calls is not None:
        budget_kwargs["max_llm_calls"] = max_llm_calls
    if max_revisions is not None:
        budget_kwargs["max_revisions"] = max_revisions
    if per_call_timeout is not None:
        budget_kwargs["per_call_timeout"] = per_call_timeout

    budget_config = BudgetConfig(**budget_kwargs) if budget_kwargs else BudgetConfig()

    client_kwargs = {}
    if api_key:
        client_kwargs["api_key"] = api_key
    if model:
        client_kwargs["model"] = model
    if budget_config.per_call_timeout:
        client_kwargs["timeout"] = budget_config.per_call_timeout

    async with OpenRouterClient(**client_kwargs) as client:
        controller = RunController(
            client,
            on_progress=on_progress,
            budget_config=budget_config,
            library_paths=library_paths,
        )
        return await controller.run(request)
