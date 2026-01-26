"""Critic - Multi-view critique of candidates."""

import json
from zeus.models.schemas import NormalizedProblem, Candidate, Critique, CritiqueIssue
from zeus.llm.openrouter import OpenRouterClient
from zeus.prompts.design_brief import DesignBriefPrompts
from zeus.prompts.solution_designer import SolutionDesignerPrompts


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

            issues.append(CritiqueIssue(
                role=issue_data.get("role", "general"),
                severity=severity,
                description=issue_data.get("description", ""),
                suggested_fix=issue_data.get("suggested_fix"),
            ))

        critique = Critique(
            issues=issues,
            constraint_violations=response.get("constraint_violations", []),
            missing_perspectives=response.get("missing_perspectives", []),
        )

        # Invariant: Add constraint violations as blocker issues if not already captured
        self._ensure_constraint_violations_as_issues(critique)

        return critique, usage

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
            Summary dict with counts by severity.
        """
        blockers = sum(1 for i in critique.issues if i.severity == "blocker")
        majors = sum(1 for i in critique.issues if i.severity == "major")
        minors = sum(1 for i in critique.issues if i.severity == "minor")

        return {
            "total_issues": len(critique.issues),
            "blockers": blockers,
            "majors": majors,
            "minors": minors,
            "constraint_violations": len(critique.constraint_violations),
            "missing_perspectives": len(critique.missing_perspectives),
            "needs_revision": blockers > 0,
        }
