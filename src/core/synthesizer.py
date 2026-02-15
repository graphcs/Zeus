"""Synthesizer - Phase 3: Convergent Synthesis."""

import logging
from src.models.schemas import (
    ProblemBrief, InventorSolution, CrossCritique,
    SynthesisResult, Provenance, ResolvedConflict,
)
from src.llm.openrouter import OpenRouterClient
from src.prompts.synthesis import SynthesisPrompts
from src.core.library_loader import LibraryLoader

logger = logging.getLogger(__name__)


class Synthesizer:
    """Combines inventor solutions into a unified draft."""

    def __init__(self, llm_client: OpenRouterClient, library_loader: LibraryLoader):
        self.llm = llm_client
        self.library_loader = library_loader

    async def synthesize(
        self,
        problem_brief: ProblemBrief,
        solutions: list[InventorSolution],
        cross_critiques: list[CrossCritique] | None = None,
    ) -> tuple[SynthesisResult, dict[str, int]]:
        """Synthesize multiple inventor solutions into a unified draft.

        Args:
            problem_brief: The problem brief.
            solutions: Inventor solutions to synthesize.
            cross_critiques: Optional cross-critiques from Phase 2.

        Returns:
            Tuple of (SynthesisResult, usage_stats).
        """
        logger.info(f"Synthesizing {len(solutions)} inventor solutions" +
                     (f" with {len(cross_critiques)} cross-critiques" if cross_critiques else ""))

        # Summarize each solution to manage context window
        solutions_text = self._format_solutions(solutions)
        logger.info(f"Formatted solutions text: {len(solutions_text)} chars")

        # Format cross-critiques if available
        cross_critiques_section = ""
        if cross_critiques:
            cross_critiques_section = "CROSS-CRITIQUES:\n" + self._format_cross_critiques(cross_critiques)

        # Build library context (synthesizer gets ALL libraries)
        all_libs = self.library_loader.get_all()
        library_context = ""
        if all_libs:
            logger.info(f"Loading {len(all_libs)} libraries for synthesis: {list(all_libs.keys())}")
            parts = ["ALL REFERENCE LIBRARIES:"]
            for name, content in all_libs.items():
                truncated = content[:15000] if len(content) > 15000 else content
                parts.append(f"\n--- {name.upper()} ---\n{truncated}")
            library_context = "\n".join(parts)

        objectives_str = "\n".join(f"- {o}" for o in problem_brief.objectives) if problem_brief.objectives else "None"
        constraints_str = "\n".join(f"- {c}" for c in problem_brief.constraints) if problem_brief.constraints else "None"

        prompt = SynthesisPrompts.SYNTHESIZE.format(
            num_solutions=len(solutions),
            problem_brief=problem_brief.problem_statement,
            objectives=objectives_str,
            constraints=constraints_str,
            eval_criteria=problem_brief.eval_criteria or "Not provided",
            library_context=library_context,
            solutions=solutions_text,
            cross_critiques_section=cross_critiques_section,
        )

        logger.info(f"Calling LLM for synthesis (prompt {len(prompt)} chars)...")
        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=SynthesisPrompts.SYSTEM,
            temperature=0.5,
            max_tokens=16384,
        )
        logger.info(f"Synthesis LLM response received")

        # Parse provenance
        provenance = []
        for p in response.get("provenance", []):
            provenance.append(Provenance(
                element=p.get("element", ""),
                source_inventor=p.get("source_inventor", "unknown"),
                modified=p.get("modified", False),
                reason=p.get("reason", ""),
            ))

        # Parse resolved conflicts
        conflicts = []
        for c in response.get("resolved_conflicts", []):
            conflicts.append(ResolvedConflict(
                conflict=c.get("conflict", ""),
                resolution=c.get("resolution", ""),
                rationale=c.get("rationale", ""),
            ))

        result = SynthesisResult(
            unified_draft=response.get("unified_draft", ""),
            version=1,
            provenance=provenance,
            resolved_conflicts=conflicts,
            open_issues=response.get("open_issues", []),
        )

        logger.info(f"Synthesis result: draft {len(result.unified_draft)} chars, "
                     f"{len(provenance)} provenance entries, "
                     f"{len(conflicts)} resolved conflicts, "
                     f"{len(result.open_issues)} open issues")
        return result, usage

    def _format_solutions(self, solutions: list[InventorSolution]) -> str:
        """Format inventor solutions for the synthesis prompt."""
        parts = []
        for sol in solutions:
            # Summarize long solutions to key elements
            content = sol.content
            if len(content) > 20000:
                content = content[:20000] + "\n\n[... truncated for synthesis ...]"

            parts.append(
                f"\n{'='*60}\n"
                f"INVENTOR {sol.inventor_id} ({sol.inventor_type}):\n"
                f"Libraries used: {', '.join(sol.libraries_used) if sol.libraries_used else 'none'}\n"
                f"Key reasoning: {sol.reasoning_trace[:500] if sol.reasoning_trace else 'not provided'}\n\n"
                f"{content}\n"
            )
        return "\n".join(parts)

    def _format_cross_critiques(self, critiques: list[CrossCritique]) -> str:
        """Format cross-critiques for the synthesis prompt."""
        parts = []
        for cc in critiques:
            parts.append(
                f"\nInventor {cc.critic_id} → Inventor {cc.target_id}:\n"
                f"  Disagreements: {'; '.join(cc.disagreements) if cc.disagreements else 'none'}\n"
                f"  Missed: {'; '.join(cc.missed_elements) if cc.missed_elements else 'none'}\n"
                f"  Strengths: {'; '.join(cc.strengths) if cc.strengths else 'none'}"
            )
        return "\n".join(parts)
