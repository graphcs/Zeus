"""Run Controller - Orchestrates the full Zeus pipeline."""

import asyncio
import time
from typing import Callable
from src.models.schemas import (
    ZeusRequest,
    ZeusResponse,
    RunRecord,
    BudgetUsed,
    BudgetConfig,
)
from src.llm.openrouter import OpenRouterClient, OpenRouterError, OpenRouterTimeoutError
from src.core.normalizer import Normalizer
from src.core.planner import Planner
from src.core.generator import Generator
from src.core.critic import Critic
from src.core.assembler import Assembler
from src.core.constraint_checker import ConstraintChecker
from src.core.issue_structurer import IssueStructurer
from src.core.persistence import Persistence
from src.core.comparator import Comparator
from src.prompts.design_brief import DesignBriefPrompts
from src.prompts.solution_designer import SolutionDesignerPrompts


class BudgetExceededError(Exception):
    """Raised when LLM call budget is exhausted."""
    pass


class RunTimeoutError(Exception):
    """Raised when total run timeout is exceeded."""
    pass


class RunController:
    """Orchestrates the Zeus pipeline.

    Pipeline: Normalize → Plan → Generate → Critique → [Revise → Critique] → Assemble

    Invariants enforced:
    - Critique runs on every generation
    - Every run has a run_id and persisted RunRecord
    - Max 1 revision loop enforced
    - Call budget enforced (hard cap on LLM calls)
    - Graceful degradation on LLM failures
    """

    DEFAULT_BUDGET = BudgetConfig()

    def __init__(
        self,
        llm_client: OpenRouterClient,
        persistence: Persistence | None = None,
        on_progress: Callable[[str], None] | None = None,
        budget_config: BudgetConfig | None = None,
    ):
        """Initialize run controller.

        Args:
            llm_client: The LLM client to use.
            persistence: Optional persistence layer. Creates default if not provided.
            on_progress: Optional callback for progress updates.
            budget_config: Optional budget configuration. Uses defaults if not provided.
        """
        self.llm = llm_client
        self.persistence = persistence or Persistence()
        self.on_progress = on_progress or (lambda msg: None)
        self.budget_config = budget_config or self.DEFAULT_BUDGET

        # Initialize pipeline components
        self.normalizer = Normalizer(llm_client)
        self.planner = Planner(llm_client)
        self.generator = Generator(llm_client)
        self.critic = Critic(llm_client)
        self.assembler = Assembler()
        self.constraint_checker = ConstraintChecker(llm_client)
        self.issue_structurer = IssueStructurer(llm_client)

    async def run(self, request: ZeusRequest) -> ZeusResponse:
        """Execute the full Zeus pipeline.

        Args:
            request: The Zeus request to process.

        Returns:
            The final ZeusResponse.
        """
        # Initialize run record
        record = RunRecord(
            mode=request.mode,
            request=request,
            model_version=self.llm.model,
            prompt_versions=self._get_prompt_versions(request.mode),
        )

        start_time = time.monotonic()

        try:
            # Wrap entire pipeline in total run timeout
            async with asyncio.timeout(self.budget_config.total_run_timeout):
                await self._execute_pipeline(request, record)

            # Assembler must be called on success path too
            record.final_response = self.assembler.assemble(record)
            
            # V2: Regression Analysis against baseline
            # Try to match a baseline by mode (e.g., 'baseline_brief', 'baseline_solution')
            baseline_name = f"baseline_{request.mode}"
            baseline = self.persistence.get_baseline(baseline_name)
            
            if baseline:
                self.on_progress(f"Running regression analysis against {baseline_name}...")
                regression = Comparator.compare(record, baseline)
                if regression:
                    record.final_response.regression_analysis = regression

        except TimeoutError:
            # Total run timeout exceeded
            elapsed = time.monotonic() - start_time
            record.errors.append(
                f"Run timeout: exceeded {self.budget_config.total_run_timeout}s limit "
                f"(elapsed: {elapsed:.1f}s)"
            )
            record.final_response = self.assembler.assemble(record)

        except BudgetExceededError as e:
            # Budget exhausted - assemble best-effort response
            record.errors.append(f"Budget exceeded: {str(e)}")
            record.final_response = self.assembler.assemble(record)

        except OpenRouterTimeoutError as e:
            # Per-call timeout - log and assemble best-effort
            elapsed = time.monotonic() - start_time
            record.errors.append(
                f"LLM call timeout: {str(e)} (run elapsed: {elapsed:.1f}s)"
            )
            record.final_response = self.assembler.assemble(record)

        except OpenRouterError as e:
            # Graceful degradation on LLM failures
            record.errors.append(f"LLM error: {str(e)}")
            record.final_response = self.assembler.assemble(record)

        except Exception as e:
            # Catch-all for unexpected errors
            record.errors.append(f"Unexpected error: {str(e)}")
            record.final_response = self.assembler.assemble(record)

        finally:
            # INVARIANT: Every run has a persisted RunRecord
            self.on_progress("Saving run record...")
            self.persistence.save(record)

        return record.final_response

    async def _execute_pipeline(self, request: ZeusRequest, record: RunRecord) -> None:
        """Execute the pipeline phases.

        Args:
            request: The Zeus request to process.
            record: The run record to update.
        """
        # Phase 1: Normalize
        self.on_progress("Normalizing input...")
        self._check_budget(record, "normalize")
        record.normalized_problem, usage = await self.normalizer.normalize(request)
        self._update_budget(record, usage)

        # Phase 2: Plan
        self.on_progress("Creating generation plan...")
        self._check_budget(record, "plan")
        record.plan, usage = await self.planner.plan(record.normalized_problem, request.mode)
        self._update_budget(record, usage)

        # Phase 3: Generate v1
        self.on_progress("Generating initial candidate...")
        self._check_budget(record, "generate_v1")
        record.candidate_v1, usage = await self.generator.generate(
            record.normalized_problem,
            record.plan,
            request.mode,
            on_progress=self.on_progress,
        )
        self._update_budget(record, usage)

        # Phase 4: Critique v1 (INVARIANT: critique runs on every generation)
        self.on_progress("Running multi-view critique...")
        self._check_budget(record, "critique_v1")
        record.critique_v1, usage = await self.critic.critique(
            record.candidate_v1,
            record.normalized_problem,
            request.mode,
        )
        self._update_budget(record, usage)

        # Phase 5: Revision loop (if needed, allowed, and within budget)
        if record.needs_revision() and record.can_revise():
            # Check if we have budget for both revise and critique
            remaining_calls = self.budget_config.max_llm_calls - record.budget_used.llm_calls
            if remaining_calls >= 2:
                self.on_progress("Addressing blocker issues...")
                record.budget_used.revisions += 1

                # Generate v2
                self._check_budget(record, "revise")
                record.candidate_v2, usage = await self.generator.revise(
                    record.candidate_v1,
                    record.critique_v1,
                    record.normalized_problem,
                    request.mode,
                    on_progress=self.on_progress,
                )
                self._update_budget(record, usage)

                # Critique v2 (INVARIANT: critique runs on every generation)
                self.on_progress("Re-evaluating revised candidate...")
                self._check_budget(record, "critique_v2")
                record.critique_v2, usage = await self.critic.critique(
                    record.candidate_v2,
                    record.normalized_problem,
                    request.mode,
                )
                self._update_budget(record, usage)
            else:
                # Not enough budget for revision loop
                record.errors.append(
                    f"Skipped revision: insufficient budget ({remaining_calls} calls remaining, need 2)"
                )

        # Phase 5.5: V3 Verification & Structuring
        final_candidate = record.candidate_v2 or record.candidate_v1
        final_critique = record.critique_v2 or record.critique_v1
        
        # Constraint Verification (V3)
        if final_candidate and record.normalized_problem and record.normalized_problem.constraints:
            remaining_calls = self.budget_config.max_llm_calls - record.budget_used.llm_calls
            if remaining_calls > 0:
                self.on_progress("Verifying constraints (V3)...")
                try:
                    self._check_budget(record, "verify_constraints")
                    report, usage = await self.constraint_checker.verify_constraints(
                        final_candidate.content,
                        record.normalized_problem.constraints
                    )
                    record.verification_report = report
                    self._update_budget(record, usage)
                except BudgetExceededError:
                    record.errors.append("Skipped constraint verification: budget exceeded")

        # Issue Structuring (V3)
        if final_critique and final_critique.issues:
             # Prepare raw issues list from critique
             raw_issues = [
                 f"{issue.role.upper()} ({issue.severity}): {issue.description}"
                 for issue in final_critique.issues
             ]
             # Also include uncertainty flags from candidate?
             if final_candidate and final_candidate.uncertainty_flags:
                 raw_issues.extend([f"UNCERTAINTY: {flag}" for flag in final_candidate.uncertainty_flags])
             
             remaining_calls = self.budget_config.max_llm_calls - record.budget_used.llm_calls
             if remaining_calls > 0 and raw_issues:
                 self.on_progress("Structuring identified issues (V3)...")
                 try:
                     self._check_budget(record, "structure_issues")
                     structured, usage = await self.issue_structurer.structure_issues(raw_issues)
                     record.structured_issues = structured
                     self._update_budget(record, usage)
                 except BudgetExceededError:
                     record.errors.append("Skipped issue structuring: budget exceeded")


    def _check_budget(self, record: RunRecord, phase: str) -> None:
        """Check if budget allows another LLM call.

        Args:
            record: The run record with current budget usage.
            phase: Name of the phase requesting the call (for error messages).

        Raises:
            BudgetExceededError: If the call budget is exhausted.
        """
        if record.budget_used.llm_calls >= self.budget_config.max_llm_calls:
            raise BudgetExceededError(
                f"LLM call budget exhausted at phase '{phase}'. "
                f"Used {record.budget_used.llm_calls}/{self.budget_config.max_llm_calls} calls."
            )

    def _update_budget(self, record: RunRecord, usage: dict[str, int]) -> None:
        """Update budget tracking from usage stats."""
        record.budget_used.llm_calls += 1
        record.budget_used.tokens_in += usage.get("tokens_in", 0)
        record.budget_used.tokens_out += usage.get("tokens_out", 0)

    def _get_prompt_versions(self, mode: str) -> dict:
        """Get prompt version info for traceability."""
        if mode == "brief":
            return DesignBriefPrompts.get_version_info()
        return SolutionDesignerPrompts.get_version_info()


async def run_zeus(
    prompt: str,
    mode: str,
    constraints: list[str] | None = None,
    context: str | dict | None = None,
    human_suggestions: list[str] | None = None,
    prior_solutions: list[str] | None = None,
    api_key: str | None = None,
    model: str | None = None,
    on_progress: Callable[[str], None] | None = None,
    max_llm_calls: int | None = None,
    per_call_timeout: float | None = None,
    total_run_timeout: float | None = None,
) -> ZeusResponse:
    """Convenience function to run Zeus.

    Args:
        prompt: The input prompt.
        mode: "brief" or "solution".
        constraints: Optional list of constraints.
        context: Optional context.
        human_suggestions: Optional list of human suggestions.
        prior_solutions: Optional list of prior solution contents.
        api_key: Optional API key (uses env var if not provided).
        model: Optional model override.
        on_progress: Optional progress callback.
        max_llm_calls: Optional hard cap on LLM calls (default: 6).
        per_call_timeout: Optional timeout per LLM call in seconds (default: 60).
        total_run_timeout: Optional total run timeout in seconds (default: 300).

    Returns:
        The ZeusResponse.
    """
    request = ZeusRequest(
        prompt=prompt,
        mode=mode,
        constraints=constraints or [],
        context=context,
        human_suggestions=human_suggestions or [],
        prior_solutions=prior_solutions or [],
    )

    # Build budget config with any overrides
    budget_kwargs = {}
    if max_llm_calls is not None:
        budget_kwargs["max_llm_calls"] = max_llm_calls
    if per_call_timeout is not None:
        budget_kwargs["per_call_timeout"] = per_call_timeout
    if total_run_timeout is not None:
        budget_kwargs["total_run_timeout"] = total_run_timeout

    budget_config = BudgetConfig(**budget_kwargs) if budget_kwargs else BudgetConfig()

    # Build client kwargs
    client_kwargs = {}
    if api_key:
        client_kwargs["api_key"] = api_key
    if model:
        client_kwargs["model"] = model
    # Pass per-call timeout to the client
    if budget_config.per_call_timeout:
        client_kwargs["timeout"] = budget_config.per_call_timeout

    async with OpenRouterClient(**client_kwargs) as client:
        controller = RunController(client, on_progress=on_progress, budget_config=budget_config)
        return await controller.run(request)
