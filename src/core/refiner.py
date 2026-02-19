"""Refiner - Phase 5: Iterative Refinement."""

import logging
from src.models.schemas import (
    ProblemBrief, LibraryCritiqueResult, LibraryCritiqueIssue,
    RefinementIteration,
)
from src.llm.openrouter import OpenRouterClient
from src.prompts.refinement import RefinementPrompts
from src.core.library_loader import LibraryLoader
from src.core.library_critic import LibraryCritic

logger = logging.getLogger(__name__)


class Refiner:
    """Iteratively refines the unified draft based on critique findings."""

    def __init__(self, llm_client: OpenRouterClient, library_loader: LibraryLoader):
        self.llm = llm_client
        self.library_loader = library_loader
        self.library_critic = LibraryCritic(llm_client, library_loader)

    async def refine(
        self,
        draft: str,
        critique_result: LibraryCritiqueResult,
        problem_brief: ProblemBrief,
        max_revisions: int = 3,
        budget_remaining: int = 10,
    ) -> tuple[str, list[RefinementIteration], dict[str, int]]:
        """Iteratively refine the draft.

        Args:
            draft: Current unified draft.
            critique_result: Initial critique findings.
            problem_brief: The problem brief.
            max_revisions: Maximum revision iterations.
            budget_remaining: Remaining LLM call budget.

        Returns:
            Tuple of (final_draft, refinement_history, aggregated_usage).
        """
        current_draft = draft
        history = []
        total_usage = {"tokens_in": 0, "tokens_out": 0, "llm_calls": 0}
        current_critique = critique_result

        logger.info(f"Starting refinement loop — max {max_revisions} revisions, {budget_remaining} calls left")

        for iteration in range(1, max_revisions + 1):
            blockers = [i for i in current_critique.all_issues if i.severity == "blocker"]
            majors = [i for i in current_critique.all_issues if i.severity == "major"]

            if not blockers and not majors:
                logger.info(f"Iteration {iteration}: no blockers/majors — stopping refinement")
                break

            if budget_remaining < 2:
                logger.info(f"Iteration {iteration}: budget exhausted ({budget_remaining} calls) — stopping")
                break

            logger.info(f"Iteration {iteration}/{max_revisions}: fixing {len(blockers)} blockers + "
                         f"{len(majors)} majors ({budget_remaining} calls left)")

            issues_str = self._format_issues(blockers + majors)
            constraints_str = "\n".join(f"- {c}" for c in problem_brief.constraints) if problem_brief.constraints else "None"
            library_context = self._build_library_context()

            prompt = RefinementPrompts.REFINE.format(
                version=iteration,
                draft=current_draft,
                issues=issues_str,
                problem_brief=problem_brief.problem_statement,
                constraints=constraints_str,
                library_context=library_context,
            )

            logger.info(f"Iteration {iteration}: calling LLM for refinement...")
            response, usage = await self.llm.generate_json(
                prompt=prompt,
                system=RefinementPrompts.SYSTEM,
                temperature=0.5,
                max_tokens=16384,
            )

            total_usage["tokens_in"] += usage.get("tokens_in", 0)
            total_usage["tokens_out"] += usage.get("tokens_out", 0)
            total_usage["llm_calls"] += 1
            budget_remaining -= 1

            current_draft = response.get("refined_draft", current_draft)
            addressed = len(response.get("issues_addressed", []))
            logger.info(f"Iteration {iteration}: refined draft {len(current_draft)} chars, "
                         f"{addressed} issues addressed")

            # Re-critique if budget allows
            if budget_remaining >= 1:
                logger.info(f"Iteration {iteration}: re-critiquing refined draft...")
                current_critique, critique_usage = await self.library_critic.critique(
                    current_draft,
                    problem_brief.eval_criteria,
                )
                total_usage["tokens_in"] += critique_usage.get("tokens_in", 0)
                total_usage["tokens_out"] += critique_usage.get("tokens_out", 0)
                total_usage["llm_calls"] += critique_usage.get("llm_calls", 0)
                budget_remaining -= critique_usage.get("llm_calls", 1)

                new_blockers = current_critique.blocker_count
                new_majors = current_critique.major_count
                logger.info(f"Iteration {iteration}: re-critique found {new_blockers} blockers, {new_majors} majors")
            else:
                new_blockers = 0
                new_majors = 0

            history.append(RefinementIteration(
                iteration=iteration,
                issues_addressed=addressed,
                blockers_remaining=new_blockers,
                majors_remaining=new_majors,
            ))

        logger.info(f"Refinement done — {len(history)} iterations, final draft {len(current_draft)} chars")
        return current_draft, history, total_usage

    def _format_issues(self, issues: list[LibraryCritiqueIssue]) -> str:
        """Format issues for the refinement prompt."""
        lines = []
        for i, issue in enumerate(issues, 1):
            marker = "BLOCKER" if issue.severity == "blocker" else "MAJOR"
            lines.append(f"{i}. [{marker}] {issue.description}")
            if issue.suggested_fix:
                lines.append(f"   Suggested fix: {issue.suggested_fix}")
        return "\n".join(lines) if lines else "No significant issues to address."

    def _build_library_context(self) -> str:
        """Build library context for refinement."""
        all_libs = self.library_loader.get_all()
        if not all_libs:
            return ""
        parts = ["AVAILABLE LIBRARIES FOR REFERENCE:"]
        for name, content in all_libs.items():
            truncated = content[:10000] if len(content) > 10000 else content
            parts.append(f"\n--- {name.upper()} ---\n{truncated}")
        return "\n".join(parts)
