"""Specialist Reviewer - V4 Domain-specific deep-dive agents.

Each specialist focuses on one domain and performs a deeper analysis
than the generalist multi-view critique. Specialists operate on the
shared blackboard state and can discover new issues or mark existing
ones as resolved.

Specialists:
- risk_compliance: Operational risk and constraint compliance
- evaluation_regression: Testability, metrics, and regression safety
- security_ops: Security posture and operational readiness
"""

import json
import logging
from typing import Literal

from src.llm.openrouter import OpenRouterClient
from src.models.schemas import CritiqueIssue, NormalizedProblem, SpecialistReview
from src.core.blackboard import Blackboard
from src.prompts.specialist_reviewer import SpecialistReviewerPrompts

logger = logging.getLogger(__name__)

# Type alias for supported specialist names
SpecialistName = Literal["risk_compliance", "evaluation_regression", "security_ops"]

# Maps specialist names to their prompt attributes
_SPECIALIST_CONFIG: dict[SpecialistName, dict[str, str]] = {
    "risk_compliance": {
        "system_attr": "RISK_COMPLIANCE_SYSTEM",
        "review_attr": "RISK_COMPLIANCE_REVIEW",
    },
    "evaluation_regression": {
        "system_attr": "EVALUATION_REGRESSION_SYSTEM",
        "review_attr": "EVALUATION_REGRESSION_REVIEW",
    },
    "security_ops": {
        "system_attr": "SECURITY_OPS_SYSTEM",
        "review_attr": "SECURITY_OPS_REVIEW",
    },
}

# Priority order: which specialists are most critical to run first
SPECIALIST_PRIORITY: list[SpecialistName] = [
    "risk_compliance",
    "security_ops",
    "evaluation_regression",
]


def _format_open_issues(board: Blackboard) -> str:
    """Format open blackboard issues as a numbered list for prompts.

    Args:
        board: The current blackboard.

    Returns:
        Formatted string with indexed issues.
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


class SpecialistReviewer:
    """Runs domain-specific specialist reviews against the blackboard.

    Usage:
        reviewer = SpecialistReviewer(llm_client)
        review = await reviewer.review(
            specialist="risk_compliance",
            board=board,
            problem=normalized_problem,
        )
    """

    VALID_SEVERITIES = frozenset({"blocker", "major", "minor"})
    VALID_CATEGORIES = frozenset({
        "correctness", "completeness", "constraint_violation",
        "clarity", "uncertainty", "safety", "feasibility", "general",
    })

    def __init__(self, llm_client: OpenRouterClient):
        """Initialize specialist reviewer with LLM client.

        Args:
            llm_client: The LLM client for API calls.
        """
        self.llm = llm_client

    async def review(
        self,
        specialist: SpecialistName,
        board: Blackboard,
        problem: NormalizedProblem,
    ) -> tuple[SpecialistReview, dict[str, int]]:
        """Run a single specialist review.

        Args:
            specialist: Which specialist to invoke.
            board: The shared blackboard state.
            problem: The normalized problem for context.

        Returns:
            Tuple of (SpecialistReview, usage_stats).

        Raises:
            ValueError: If specialist name is not recognized.
        """
        if specialist not in _SPECIALIST_CONFIG:
            raise ValueError(
                f"Unknown specialist '{specialist}'. "
                f"Valid: {list(_SPECIALIST_CONFIG.keys())}"
            )

        config = _SPECIALIST_CONFIG[specialist]
        system_prompt = getattr(SpecialistReviewerPrompts, config["system_attr"])
        review_template = getattr(SpecialistReviewerPrompts, config["review_attr"])

        # Format prompt inputs
        constraints_str = (
            "\n".join(f"- {c}" for c in problem.constraints)
            if problem.constraints
            else "None"
        )
        open_issues_str = _format_open_issues(board)

        prompt = review_template.format(
            problem_statement=problem.problem_statement,
            constraints=constraints_str,
            content=board.candidate.content,
            open_issues=open_issues_str,
        )

        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=system_prompt,
            temperature=0.4,  # Lower temp for analytical precision
        )

        review = self._parse_review(specialist, response, board)
        return review, usage

    def _parse_review(
        self,
        specialist: SpecialistName,
        response: dict,
        board: Blackboard,
    ) -> SpecialistReview:
        """Parse the LLM response into a SpecialistReview.

        Args:
            specialist: The specialist name.
            response: Parsed JSON from the LLM.
            board: The blackboard (for validating resolved indices).

        Returns:
            Validated SpecialistReview.
        """
        # Parse new issues
        new_issues: list[CritiqueIssue] = []
        for issue_data in response.get("new_issues", []):
            severity = issue_data.get("severity", "minor")
            if severity not in self.VALID_SEVERITIES:
                severity = "minor"

            category = issue_data.get("category", "general")
            if category not in self.VALID_CATEGORIES:
                category = "general"

            new_issues.append(CritiqueIssue(
                role=issue_data.get("role", specialist),
                severity=severity,
                category=category,
                description=issue_data.get("description", ""),
                suggested_fix=issue_data.get("suggested_fix"),
            ))

        # Validate resolved indices against actual open issues
        open_count = len(board.open_issues)
        raw_indices = response.get("resolved_issue_indices", [])
        resolved_indices = [
            idx for idx in raw_indices
            if isinstance(idx, int) and 0 <= idx < open_count
        ]

        return SpecialistReview(
            specialist=specialist,
            new_issues=new_issues,
            resolved_issue_indices=resolved_indices,
            resolution_notes=response.get("resolution_notes", ""),
            fix_suggestions=response.get("fix_suggestions", ""),
        )

    @staticmethod
    def select_specialists(board: Blackboard) -> list[SpecialistName]:
        """Select which specialists to run based on open issues and budget.

        The selection is priority-ordered and budget-aware. If there are
        open blocker issues, all specialists are candidates. Otherwise,
        specialists are selected based on which domains have open issues.

        Args:
            board: The current blackboard state.

        Returns:
            Ordered list of specialists to run (may be shorter than full list
            if budget is limited).
        """
        if not board.has_budget:
            return []

        remaining = board.max_specialist_calls - board.specialist_calls_used

        # If there are open blockers, prioritise all specialists
        if board.open_blockers:
            return SPECIALIST_PRIORITY[:remaining]

        # Otherwise pick specialists whose domains have open issues
        domain_roles: dict[SpecialistName, set[str]] = {
            "risk_compliance": {"risk", "compliance"},
            "security_ops": {"security", "operations", "security_ops"},
            "evaluation_regression": {"evaluation", "measurability", "testing"},
        }

        selected: list[SpecialistName] = []
        open_roles = {bi.issue.role.lower() for bi in board.open_issues}

        for spec in SPECIALIST_PRIORITY:
            if len(selected) >= remaining:
                break
            # Check if any open issue touches this specialist's domain
            if domain_roles[spec] & open_roles:
                selected.append(spec)

        # If nothing matched but we still have issues, run the top-priority specialist
        if not selected and board.open_issues and remaining > 0:
            selected.append(SPECIALIST_PRIORITY[0])

        return selected
