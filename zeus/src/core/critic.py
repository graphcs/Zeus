"""Critic - Multi-view critique of candidates."""

import json
from src.models.schemas import NormalizedProblem, Candidate, Critique, CritiqueIssue
from src.llm.openrouter import OpenRouterClient
from src.prompts.design_brief import DesignBriefPrompts
from src.prompts.solution_designer import SolutionDesignerPrompts


# Required perspectives for critique coverage (MVP spec)
REQUIRED_PERSPECTIVES = frozenset({
    "scope",        # Requirements/scope coverage
    "architecture", # Technical architecture review
    "risk",         # Risk assessment
    "security",     # Security/ops considerations
    "compliance",   # Compliance with constraints
    "evaluation",   # Evaluation/experimentation readiness
})

# Mapping of alternative names to canonical perspective names
PERSPECTIVE_ALIASES = {
    # Scope aliases
    "requirements": "scope",
    "completeness": "scope",
    "scope_definition": "scope",
    # Architecture aliases
    "technical": "architecture",
    "design": "architecture",
    "feasibility": "architecture",
    # Risk aliases
    "risks": "risk",
    "risk_assessment": "risk",
    # Security aliases
    "security_ops": "security",
    "ops": "security",
    "operations": "security",
    # Compliance aliases
    "constraints": "compliance",
    "constraint_compliance": "compliance",
    # Evaluation aliases
    "measurability": "evaluation",
    "testing": "evaluation",
    "success_criteria": "evaluation",
    "experimentation": "evaluation",
}


class Critic:
    """Provides multi-view critique of candidates."""

    def __init__(self, llm_client: OpenRouterClient):
        """Initialize critic with LLM client."""
        self.llm = llm_client

    async def critique(
        self,
        candidate: Candidate,
        problem: NormalizedProblem,
        mode: str,
    ) -> tuple[Critique, dict[str, int]]:
        """Critique a candidate from multiple perspectives.

        Args:
            candidate: The candidate to critique.
            problem: The normalized problem for context.
            mode: "brief" or "solution".

        Returns:
            Tuple of (Critique, usage_stats).
        """
        prompts = DesignBriefPrompts if mode == "brief" else SolutionDesignerPrompts

        constraints_str = "\n".join(f"- {c}" for c in problem.constraints) if problem.constraints else "None"
        context_str = json.dumps(problem.context, indent=2) if problem.context else "None"

        prompt = prompts.CRITIQUE.format(
            problem_statement=problem.problem_statement,
            constraints=constraints_str,
            context=context_str,
            content=candidate.content,
        )

        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=prompts.SYSTEM,
            temperature=0.5,  # Moderate temperature for balanced critique
        )

        # Parse issues
        issues = []
        for issue_data in response.get("issues", []):
            severity = issue_data.get("severity", "minor")
            if severity not in ("blocker", "major", "minor"):
                severity = "minor"
            
            # Parse category (V1 feature)
            category = issue_data.get("category", "general")
            if category not in ("correctness", "completeness", "constraint_violation", 
                               "clarity", "uncertainty", "safety", "feasibility", "general"):
                category = "general"

            issues.append(CritiqueIssue(
                role=issue_data.get("role", "general"),
                severity=severity,
                category=category,
                description=issue_data.get("description", ""),
                suggested_fix=issue_data.get("suggested_fix"),
            ))

        # Get missing perspectives from response
        llm_missing = response.get("missing_perspectives", [])

        # Validate perspective coverage and compute actual missing perspectives
        _, missing = self._validate_perspective_coverage(issues)

        # Merge LLM-reported missing with our validation
        all_missing = list(set(llm_missing) | missing)

        critique = Critique(
            issues=issues,
            constraint_violations=response.get("constraint_violations", []),
            missing_perspectives=all_missing,
        )

        # Invariant: Add constraint violations as blocker issues if not already captured
        self._ensure_constraint_violations_as_issues(critique)

        # Add minor issue if coverage is incomplete
        if missing:
            critique.issues.append(CritiqueIssue(
                role="meta",
                severity="minor",
                description=f"Critique coverage incomplete. Missing perspectives: {', '.join(sorted(missing))}",
                suggested_fix="Consider adding analysis from these viewpoints in future iterations",
            ))

        return critique, usage

    def _normalize_perspective(self, role: str) -> str | None:
        """Normalize a role/perspective name to canonical form.

        Args:
            role: The role name from critique issue.

        Returns:
            Canonical perspective name or None if not recognized.
        """
        role_lower = role.lower().strip().replace(" ", "_").replace("-", "_")

        # Direct match
        if role_lower in REQUIRED_PERSPECTIVES:
            return role_lower

        # Alias match
        if role_lower in PERSPECTIVE_ALIASES:
            return PERSPECTIVE_ALIASES[role_lower]

        # Partial match - check if any required perspective is contained in the role
        for perspective in REQUIRED_PERSPECTIVES:
            if perspective in role_lower or role_lower in perspective:
                return perspective

        return None

    def _validate_perspective_coverage(
        self, issues: list[CritiqueIssue]
    ) -> tuple[set[str], set[str]]:
        """Validate that critique covers required perspectives.

        Args:
            issues: List of critique issues.

        Returns:
            Tuple of (covered_perspectives, missing_perspectives).
        """
        covered = set()

        for issue in issues:
            normalized = self._normalize_perspective(issue.role)
            if normalized:
                covered.add(normalized)

        missing = REQUIRED_PERSPECTIVES - covered

        return covered, missing

    def get_coverage_score(self, critique: Critique) -> float:
        """Calculate perspective coverage score.

        Args:
            critique: The critique to evaluate.

        Returns:
            Coverage score from 0.0 to 1.0.
        """
        covered, _ = self._validate_perspective_coverage(critique.issues)
        return len(covered) / len(REQUIRED_PERSPECTIVES)

    def _ensure_constraint_violations_as_issues(self, critique: Critique) -> None:
        """Ensure constraint violations are represented as blocker issues."""
        if not critique.constraint_violations:
            return

        # Check if violations are already in issues
        existing_descriptions = {issue.description.lower() for issue in critique.issues}

        for violation in critique.constraint_violations:
            if violation.lower() not in existing_descriptions:
                critique.issues.append(CritiqueIssue(
                    role="compliance",
                    severity="blocker",
                    description=f"Constraint violation: {violation}",
                    suggested_fix="Ensure this constraint is addressed in the output",
                ))

    def summarize(self, critique: Critique) -> dict:
        """Summarize critique for logging/display.

        Args:
            critique: The critique to summarize.

        Returns:
            Summary dict with counts by severity and coverage.
        """
        blockers = sum(1 for i in critique.issues if i.severity == "blocker")
        majors = sum(1 for i in critique.issues if i.severity == "major")
        minors = sum(1 for i in critique.issues if i.severity == "minor")

        # Calculate coverage
        covered, missing = self._validate_perspective_coverage(critique.issues)
        coverage_score = len(covered) / len(REQUIRED_PERSPECTIVES)

        return {
            "total_issues": len(critique.issues),
            "blockers": blockers,
            "majors": majors,
            "minors": minors,
            "constraint_violations": len(critique.constraint_violations),
            "missing_perspectives": list(missing),
            "covered_perspectives": list(covered),
            "coverage_score": round(coverage_score, 2),
            "needs_revision": blockers > 0,
        }
