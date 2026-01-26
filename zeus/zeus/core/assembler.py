"""Assembler - Final output assembly."""

from zeus.models.schemas import (
    Candidate,
    Critique,
    ZeusResponse,
    RunRecord,
    UsageStats,
    REQUIRED_PERSPECTIVES,
    PERSPECTIVE_ALIASES,
    CONFIDENCE_LEVELS,
)

# Pricing per 1M tokens (USD) - Claude Sonnet 4 via OpenRouter
MODEL_PRICING = {
    "anthropic/claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "anthropic/claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "default": {"input": 3.00, "output": 15.00},
}


class Assembler:
    """Assembles final output from candidates and critiques."""

    def _calculate_usage(self, record: RunRecord) -> UsageStats:
        """Calculate usage statistics including cost.

        Args:
            record: The run record with budget usage.

        Returns:
            UsageStats with token counts and estimated cost.
        """
        budget = record.budget_used
        tokens_in = budget.tokens_in
        tokens_out = budget.tokens_out
        total_tokens = tokens_in + tokens_out

        # Get pricing for the model
        pricing = MODEL_PRICING.get(record.model_version, MODEL_PRICING["default"])

        # Calculate cost: (tokens / 1M) * price_per_1M
        cost_in = (tokens_in / 1_000_000) * pricing["input"]
        cost_out = (tokens_out / 1_000_000) * pricing["output"]
        cost_usd = round(cost_in + cost_out, 6)

        return UsageStats(
            llm_calls=budget.llm_calls,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            total_tokens=total_tokens,
            cost_usd=cost_usd,
        )

    def _calculate_confidence(self, critique: Critique | None) -> CONFIDENCE_LEVELS:
        """Calculate confidence level based on critique severity.

        Rules:
        - Any blocker → low
        - 2+ major issues → low
        - 1 major OR 3+ minor → medium
        - Otherwise → high

        Args:
            critique: The critique to evaluate.

        Returns:
            Confidence level: "low", "medium", or "high".
        """
        if critique is None:
            return "medium"  # No critique = uncertain

        blockers = sum(1 for i in critique.issues if i.severity == "blocker")
        majors = sum(1 for i in critique.issues if i.severity == "major")
        minors = sum(1 for i in critique.issues if i.severity == "minor")

        if blockers > 0 or majors >= 2:
            return "low"
        elif majors == 1 or minors >= 3:
            return "medium"
        else:
            return "high"

    def _normalize_perspective(self, role: str) -> str:
        """Normalize a critique role to a standard perspective.

        Args:
            role: The role string from critique issue.

        Returns:
            Normalized perspective name.
        """
        role_lower = role.lower().strip()

        # Check if it's already a required perspective
        if role_lower in REQUIRED_PERSPECTIVES:
            return role_lower

        # Check aliases
        return PERSPECTIVE_ALIASES.get(role_lower, role_lower)

    def _calculate_coverage(self, critique: Critique | None) -> tuple[float, list[str], list[str]]:
        """Calculate perspective coverage from critique.

        Args:
            critique: The critique to evaluate.

        Returns:
            Tuple of (coverage_score, covered_perspectives, missing_perspectives).
        """
        if critique is None:
            return 0.0, [], list(REQUIRED_PERSPECTIVES)

        covered = set()
        for issue in critique.issues:
            perspective = self._normalize_perspective(issue.role)
            if perspective in REQUIRED_PERSPECTIVES:
                covered.add(perspective)

        missing = REQUIRED_PERSPECTIVES - covered
        coverage_score = len(covered) / len(REQUIRED_PERSPECTIVES)

        return coverage_score, sorted(covered), sorted(missing)

    def _calculate_issue_counts(self, critique: Critique | None) -> dict[str, int]:
        """Calculate issue counts by severity.

        Args:
            critique: The critique to evaluate.

        Returns:
            Dict with blockers, majors, minors counts.
        """
        if critique is None:
            return {"blockers": 0, "majors": 0, "minors": 0}

        blockers = sum(1 for i in critique.issues if i.severity == "blocker")
        majors = sum(1 for i in critique.issues if i.severity == "major")
        minors = sum(1 for i in critique.issues if i.severity == "minor")

        return {"blockers": blockers, "majors": majors, "minors": minors}

    def _group_issues_by_category(self, critique: Critique | None) -> dict[str, list[str]]:
        """Group critique issues by category.

        Args:
            critique: The critique to evaluate.

        Returns:
            Dict mapping category to list of issue descriptions.
        """
        if critique is None:
            return {}

        grouped: dict[str, list[str]] = {}
        for issue in critique.issues:
            if issue.severity in ("major", "minor"):  # Exclude blockers (should be fixed)
                category = getattr(issue, 'category', 'completeness')
                severity = issue.severity.upper()
                desc = f"[{severity}] {issue.description}"
                if category not in grouped:
                    grouped[category] = []
                grouped[category].append(desc)

        return grouped

    def assemble(self, record: RunRecord) -> ZeusResponse:
        """Assemble the final response from a run record.

        Args:
            record: The complete run record.

        Returns:
            The final ZeusResponse.

        Invariants enforced:
        - assumptions[] is always present (may be empty)
        - known_issues[] is always present (may be empty)
        """
        # Use the latest candidate (v2 if exists, else v1)
        final_candidate = record.candidate_v2 or record.candidate_v1

        # Calculate usage stats
        usage = self._calculate_usage(record)

        # Get final critique for V1 metrics
        final_critique = record.critique_v2 or record.critique_v1

        # Calculate V1 evaluation signals
        confidence = self._calculate_confidence(final_critique)
        coverage_score, covered_perspectives, missing_perspectives = self._calculate_coverage(final_critique)
        issue_counts = self._calculate_issue_counts(final_critique)
        issues_by_category = self._group_issues_by_category(final_critique)

        if final_candidate is None:
            # Graceful degradation - no candidate generated
            return ZeusResponse(
                output=self._error_output(record),
                assumptions=["Generation failed - no assumptions available"],
                known_issues=record.errors or ["Generation failed"],
                run_id=record.run_id,
                usage=usage,
                confidence="low",
                coverage_score=coverage_score,
                covered_perspectives=covered_perspectives,
                missing_perspectives=missing_perspectives,
                tradeoffs=[],
                issue_counts=issue_counts,
                issues_by_category=issues_by_category,
            )

        # Collect known issues from critique
        known_issues = self._collect_known_issues(record)

        # Ensure assumptions and known_issues are always present
        assumptions = final_candidate.assumptions or []
        if not assumptions:
            assumptions = ["No explicit assumptions documented"]

        if not known_issues:
            known_issues = ["No known issues identified"]

        # Get tradeoffs from candidate
        tradeoffs = final_candidate.tradeoffs or []

        return ZeusResponse(
            output=self._format_output(final_candidate, record),
            assumptions=assumptions,
            known_issues=known_issues,
            run_id=record.run_id,
            usage=usage,
            confidence=confidence,
            coverage_score=coverage_score,
            covered_perspectives=covered_perspectives,
            missing_perspectives=missing_perspectives,
            tradeoffs=tradeoffs,
            issue_counts=issue_counts,
            issues_by_category=issues_by_category,
        )

    def _format_output(self, candidate: Candidate, record: RunRecord) -> str:
        """Format the final output with metadata."""
        output_parts = [candidate.content]

        # Add uncertainty flags if present
        if candidate.uncertainty_flags:
            output_parts.append("\n---\n")
            output_parts.append("## ⚠️ Areas of Uncertainty\n")
            for flag in candidate.uncertainty_flags:
                output_parts.append(f"- {flag}\n")

        return "".join(output_parts)

    def _collect_known_issues(self, record: RunRecord) -> list[str]:
        """Collect known issues from critiques."""
        issues = []

        # Get the final critique (v2 if exists, else v1)
        final_critique = record.critique_v2 or record.critique_v1

        if final_critique:
            # Include unresolved major/minor issues (blockers should be fixed)
            for issue in final_critique.issues:
                if issue.severity in ("major", "minor"):
                    category = getattr(issue, 'category', 'completeness')
                    issues.append(f"[{issue.severity.upper()}/{category}] {issue.role}: {issue.description}")

            # Include any remaining constraint violations
            for violation in final_critique.constraint_violations:
                issues.append(f"[CONSTRAINT] {violation}")

            # Include missing perspectives as potential gaps
            for perspective in final_critique.missing_perspectives:
                issues.append(f"[GAP] Missing perspective: {perspective}")

        # Include any errors from the run
        issues.extend(record.errors)

        return issues

    def _error_output(self, record: RunRecord) -> str:
        """Generate error output when generation fails."""
        mode_name = "Design Brief" if record.mode == "brief" else "Target Solution"

        output = f"""# {mode_name} Generation Failed

Unfortunately, Zeus was unable to generate a complete {mode_name.lower()}.

## Original Request
{record.request.prompt}

## Errors Encountered
"""
        for error in record.errors:
            output += f"- {error}\n"

        output += """
## Recommendations
- Check your API key and network connection
- Try simplifying your request
- Review the constraints for conflicts
"""
        return output
