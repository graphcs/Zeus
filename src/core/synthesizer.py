"""Synthesizer - V4 Merges specialist feedback into an improved candidate.

The synthesizer takes the current candidate from the blackboard,
all specialist fix suggestions, and the open-issues list, then
produces a single revised candidate that incorporates the best
fixes while preserving design coherence.
"""

import logging
from src.llm.openrouter import OpenRouterClient
from src.models.schemas import (
    Candidate,
    NormalizedProblem,
    SpecialistReview,
    SynthesisResult,
)
from src.core.blackboard import Blackboard
from src.prompts.synthesizer import SynthesizerPrompts

logger = logging.getLogger(__name__)


def _format_specialist_reviews(reviews: list[SpecialistReview]) -> str:
    """Format specialist reviews for the synthesis prompt.

    Args:
        reviews: List of specialist reviews to format.

    Returns:
        Human-readable summary of all specialist feedback.
    """
    if not reviews:
        return "No specialist reviews available."

    parts: list[str] = []
    for review in reviews:
        lines = [f"### Specialist: {review.specialist}"]

        if review.new_issues:
            lines.append("**New Issues:**")
            for issue in review.new_issues:
                lines.append(
                    f"- [{issue.severity.upper()}] ({issue.role}) {issue.description}"
                )
                if issue.suggested_fix:
                    lines.append(f"  → Fix: {issue.suggested_fix}")

        if review.fix_suggestions:
            lines.append(f"\n**Fix Suggestions:** {review.fix_suggestions}")

        if review.resolution_notes:
            lines.append(f"**Resolution Notes:** {review.resolution_notes}")

        parts.append("\n".join(lines))

    return "\n\n---\n\n".join(parts)


def _format_open_issues(board: Blackboard) -> str:
    """Format open issues for the synthesis prompt.

    Args:
        board: The current blackboard.

    Returns:
        Indexed list of open issues.
    """
    open_issues = board.open_issues
    if not open_issues:
        return "No open issues."

    lines: list[str] = []
    for idx, bi in enumerate(open_issues):
        issue = bi.issue
        lines.append(
            f"[{idx}] [{issue.severity.upper()}] ({issue.role}) "
            f"{issue.description}"
        )
    return "\n".join(lines)


class Synthesizer:
    """Merges specialist reviews into a single improved candidate.

    The synthesizer is invoked after all specialist reviews complete.
    It reads the blackboard, considers all fix suggestions, and produces
    a revised candidate that addresses open issues without regressions.
    """

    def __init__(self, llm_client: OpenRouterClient):
        """Initialize synthesizer with LLM client.

        Args:
            llm_client: The LLM client for generation.
        """
        self.llm = llm_client

    async def synthesize(
        self,
        board: Blackboard,
        problem: NormalizedProblem,
        reviews: list[SpecialistReview],
    ) -> tuple[SynthesisResult, dict[str, int]]:
        """Synthesize specialist feedback into an improved candidate.

        Args:
            board: The shared blackboard with current candidate and issues.
            problem: The normalized problem for context.
            reviews: All specialist reviews to incorporate.

        Returns:
            Tuple of (SynthesisResult, usage_stats).
        """
        constraints_str = (
            "\n".join(f"- {c}" for c in problem.constraints)
            if problem.constraints
            else "None"
        )

        prompt = SynthesizerPrompts.SYNTHESIZE.format(
            problem_statement=problem.problem_statement,
            constraints=constraints_str,
            content=board.candidate.content,
            specialist_reviews=_format_specialist_reviews(reviews),
            open_issues=_format_open_issues(board),
        )

        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=SynthesizerPrompts.SYSTEM,
            temperature=0.5,
            max_tokens=8192,
        )

        # Build revised candidate
        revised_candidate = Candidate(
            content=response.get("content", board.candidate.content),
            assumptions=response.get("assumptions", board.candidate.assumptions),
            uncertainty_flags=response.get(
                "uncertainty_flags", board.candidate.uncertainty_flags
            ),
            reasoning_trace=response.get(
                "reasoning_trace", board.candidate.reasoning_trace
            ),
            comparison_analysis=response.get(
                "comparison_analysis", board.candidate.comparison_analysis
            ),
        )

        # Validate resolved indices
        open_count = len(board.open_issues)
        raw_indices = response.get("resolved_issue_indices", [])
        resolved_indices = [
            idx for idx in raw_indices
            if isinstance(idx, int) and 0 <= idx < open_count
        ]

        result = SynthesisResult(
            revised_candidate=revised_candidate,
            resolved_issue_indices=resolved_indices,
            resolution_notes=response.get("resolution_notes", ""),
        )

        return result, usage
