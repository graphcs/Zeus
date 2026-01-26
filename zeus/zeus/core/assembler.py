"""Assembler - Final output assembly."""

from zeus.models.schemas import (
    Candidate,
    Critique,
    ZeusResponse,
    RunRecord,
    UsageStats,
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

        if final_candidate is None:
            # Graceful degradation - no candidate generated
            return ZeusResponse(
                output=self._error_output(record),
                assumptions=["Generation failed - no assumptions available"],
                known_issues=record.errors or ["Generation failed"],
                run_id=record.run_id,
                usage=usage,
            )

        # Collect known issues from critique
        known_issues = self._collect_known_issues(record)

        # Ensure assumptions and known_issues are always present
        assumptions = final_candidate.assumptions or []
        if not assumptions:
            assumptions = ["No explicit assumptions documented"]

        if not known_issues:
            known_issues = ["No known issues identified"]

        return ZeusResponse(
            output=self._format_output(final_candidate, record),
            assumptions=assumptions,
            known_issues=known_issues,
            run_id=record.run_id,
            usage=usage,
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
                    issues.append(f"[{issue.severity.upper()}] {issue.role}: {issue.description}")

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
