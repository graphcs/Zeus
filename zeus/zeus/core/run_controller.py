"""Run Controller - Orchestrates the full Zeus pipeline."""

import asyncio
from typing import Callable
from zeus.models.schemas import (
    ZeusRequest,
    ZeusResponse,
    RunRecord,
    BudgetUsed,
)
from zeus.llm.openrouter import OpenRouterClient, OpenRouterError
from zeus.core.normalizer import Normalizer
from zeus.core.planner import Planner
from zeus.core.generator import Generator
from zeus.core.critic import Critic
from zeus.core.assembler import Assembler
from zeus.core.persistence import Persistence
from zeus.prompts.design_brief import DesignBriefPrompts
from zeus.prompts.solution_designer import SolutionDesignerPrompts


class RunController:
    """Orchestrates the Zeus pipeline.

    Pipeline: Normalize → Plan → Generate → Critique → [Revise → Critique] → Assemble

    Invariants enforced:
    - Critique runs on every generation
    - Every run has a run_id and persisted RunRecord
    - Max 1 revision loop enforced
    - Graceful degradation on LLM failures
    """

    MAX_REVISIONS = 1

    def __init__(
        self,
        llm_client: OpenRouterClient,
        persistence: Persistence | None = None,
        on_progress: Callable[[str], None] | None = None,
    ):
        """Initialize run controller.

        Args:
            llm_client: The LLM client to use.
            persistence: Optional persistence layer. Creates default if not provided.
            on_progress: Optional callback for progress updates.
        """
        self.llm = llm_client
        self.persistence = persistence or Persistence()
        self.on_progress = on_progress or (lambda msg: None)

        # Initialize pipeline components
        self.normalizer = Normalizer(llm_client)
        self.planner = Planner(llm_client)
        self.generator = Generator(llm_client)
        self.critic = Critic(llm_client)
        self.assembler = Assembler()

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

        try:
            # Phase 1: Normalize
            self.on_progress("Normalizing input...")
            record.normalized_problem, usage = await self.normalizer.normalize(request)
            self._update_budget(record, usage)

            # Phase 2: Plan
            self.on_progress("Creating generation plan...")
            record.plan, usage = await self.planner.plan(record.normalized_problem, request.mode)
            self._update_budget(record, usage)

            # Phase 3: Generate v1
            self.on_progress("Generating initial candidate...")
            record.candidate_v1, usage = await self.generator.generate(
                record.normalized_problem,
                record.plan,
                request.mode,
            )
            self._update_budget(record, usage)

            # Phase 4: Critique v1 (INVARIANT: critique runs on every generation)
            self.on_progress("Running multi-view critique...")
            record.critique_v1, usage = await self.critic.critique(
                record.candidate_v1,
                record.normalized_problem,
                request.mode,
            )
            self._update_budget(record, usage)

            # Phase 5: Revision loop (if needed and allowed)
            if record.needs_revision() and record.can_revise():
                self.on_progress("Addressing blocker issues...")
                record.budget_used.revisions += 1

                # Generate v2
                record.candidate_v2, usage = await self.generator.revise(
                    record.candidate_v1,
                    record.critique_v1,
                    record.normalized_problem,
                    request.mode,
                )
                self._update_budget(record, usage)

                # Critique v2 (INVARIANT: critique runs on every generation)
                self.on_progress("Re-evaluating revised candidate...")
                record.critique_v2, usage = await self.critic.critique(
                    record.candidate_v2,
                    record.normalized_problem,
                    request.mode,
                )
                self._update_budget(record, usage)

            # Phase 6: Assemble final output
            self.on_progress("Assembling final output...")
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
    api_key: str | None = None,
    model: str | None = None,
    on_progress: Callable[[str], None] | None = None,
) -> ZeusResponse:
    """Convenience function to run Zeus.

    Args:
        prompt: The input prompt.
        mode: "brief" or "solution".
        constraints: Optional list of constraints.
        context: Optional context.
        api_key: Optional API key (uses env var if not provided).
        model: Optional model override.
        on_progress: Optional progress callback.

    Returns:
        The ZeusResponse.
    """
    request = ZeusRequest(
        prompt=prompt,
        mode=mode,
        constraints=constraints or [],
        context=context,
    )

    client_kwargs = {}
    if api_key:
        client_kwargs["api_key"] = api_key
    if model:
        client_kwargs["model"] = model

    async with OpenRouterClient(**client_kwargs) as client:
        controller = RunController(client, on_progress=on_progress)
        return await controller.run(request)
