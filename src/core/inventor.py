"""Inventor - Phase 1: Divergent Generation with parallel inventors."""

import asyncio
import json
import logging
from src.models.schemas import ProblemBrief, InventorConfig, InventorSolution
from src.llm.openrouter import OpenRouterClient, OpenRouterError
from src.prompts.inventor import InventorPrompts
from src.core.library_loader import LibraryLoader

logger = logging.getLogger(__name__)


class Inventor:
    """Runs parallel divergent generation across multiple inventor configurations."""

    def __init__(self, llm_client: OpenRouterClient, library_loader: LibraryLoader):
        self.llm = llm_client
        self.library_loader = library_loader

    async def generate_solutions(
        self,
        problem_brief: ProblemBrief,
        configs: list[InventorConfig],
    ) -> tuple[list[InventorSolution], dict[str, int]]:
        """Run all inventors in parallel.

        Args:
            problem_brief: The normalized problem brief.
            configs: Inventor configurations.

        Returns:
            Tuple of (list of solutions, aggregated usage stats).
        """
        logger.info(f"Launching {len(configs)} inventors in parallel")
        for cfg in configs:
            logger.info(f"  Inventor {cfg.inventor_id} ({cfg.inventor_type}) — libs: {cfg.library_assignments}")

        tasks = [
            self._run_single_inventor(problem_brief, config)
            for config in configs
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        solutions = []
        total_usage = {"tokens_in": 0, "tokens_out": 0, "llm_calls": 0}

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"Inventor {configs[i].inventor_id} failed: {result}")
                solutions.append(InventorSolution(
                    inventor_id=configs[i].inventor_id,
                    inventor_type=configs[i].inventor_type,
                    content=f"[Inventor {configs[i].inventor_id} failed: {str(result)}]",
                    assumptions=[f"Inventor {configs[i].inventor_id} failed to generate"],
                ))
            else:
                solution, usage = result
                solutions.append(solution)
                total_usage["tokens_in"] += usage.get("tokens_in", 0)
                total_usage["tokens_out"] += usage.get("tokens_out", 0)
                total_usage["llm_calls"] += 1
                logger.info(
                    f"Inventor {solution.inventor_id} ({solution.inventor_type}) done — "
                    f"{len(solution.content)} chars, {len(solution.assumptions)} assumptions"
                )

        logger.info(f"All inventors complete — {total_usage['llm_calls']} succeeded, "
                     f"{len(configs) - total_usage['llm_calls']} failed")
        return solutions, total_usage

    async def _run_single_inventor(
        self,
        problem_brief: ProblemBrief,
        config: InventorConfig,
    ) -> tuple[InventorSolution, dict[str, int]]:
        """Run a single inventor."""
        logger.info(f"Inventor {config.inventor_id} ({config.inventor_type}): building library context...")
        library_context = self._build_library_context(config)
        logger.info(f"Inventor {config.inventor_id}: library context {len(library_context)} chars, calling LLM...")

        objectives_str = "\n".join(f"- {o}" for o in problem_brief.objectives) if problem_brief.objectives else "None specified"
        constraints_str = "\n".join(f"- {c}" for c in problem_brief.constraints) if problem_brief.constraints else "None specified"

        prompt = InventorPrompts.GENERATE.format(
            inventor_id=config.inventor_id,
            inventor_type=config.inventor_type,
            problem_brief=problem_brief.problem_statement,
            objectives=objectives_str,
            constraints=constraints_str,
            library_context=library_context,
            output_spec=problem_brief.output_spec or "Produce a comprehensive solution document",
            eval_criteria=problem_brief.eval_criteria or "Not provided",
            emphasis=config.emphasis,
        )

        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=InventorPrompts.SYSTEM,
            temperature=0.7,
            max_tokens=16384,
        )

        solution = InventorSolution(
            inventor_id=config.inventor_id,
            inventor_type=config.inventor_type,
            content=response.get("content", ""),
            assumptions=response.get("assumptions", []),
            reasoning_trace=response.get("reasoning_trace", ""),
            libraries_used=response.get("libraries_used", config.library_assignments),
        )

        return solution, usage

    def _build_library_context(self, config: InventorConfig) -> str:
        """Build library context string for an inventor."""
        if config.inventor_type == "tabula_rasa":
            return "LIBRARIES: None provided. Reason from your own knowledge only."

        if config.inventor_type == "comprehensive":
            # Load ALL libraries
            all_libs = self.library_loader.get_all()
            if not all_libs:
                return "LIBRARIES: No libraries available."
            parts = ["REFERENCE LIBRARIES:"]
            for name, content in all_libs.items():
                # Truncate very large libraries to avoid context overflow
                truncated = content[:30000] if len(content) > 30000 else content
                parts.append(f"\n--- {name.upper()} ---\n{truncated}")
            return "\n".join(parts)

        # Load assigned libraries
        if not config.library_assignments:
            return "LIBRARIES: None assigned."

        libs = self.library_loader.load_multiple(config.library_assignments)
        loaded = {k: v for k, v in libs.items() if v}

        if not loaded:
            return "LIBRARIES: Assigned libraries not available."

        parts = ["REFERENCE LIBRARIES:"]
        for name, content in loaded.items():
            truncated = content[:30000] if len(content) > 30000 else content
            parts.append(f"\n--- {name.upper()} ---\n{truncated}")
        return "\n".join(parts)
