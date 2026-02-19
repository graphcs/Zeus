"""Assembler - Phase 6: Output Assembly with 5 deliverables."""

import logging
from src.models.schemas import (
    ZeusResponse,
    RunRecord,
    UsageStats,
    SelfEvaluationScorecard,
)
from src.llm.openrouter import OpenRouterClient
from src.prompts.assembly import AssemblyPrompts
from src.core.evaluator import Evaluator

logger = logging.getLogger(__name__)

# Pricing per 1M tokens (USD)
MODEL_PRICING = {
    "anthropic/claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "anthropic/claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "default": {"input": 3.00, "output": 15.00},
}


class Assembler:
    """Assembles the 5 deliverables and evaluation scorecard."""

    def __init__(self, llm_client: OpenRouterClient):
        self.llm = llm_client
        self.evaluator = Evaluator()

    async def assemble(self, record: RunRecord) -> tuple[ZeusResponse, dict[str, int]]:
        """Assemble final response from a run record.

        Args:
            record: The complete run record with all phase outputs.

        Returns:
            Tuple of (ZeusResponse, usage_stats).
        """
        logger.info("Assembling 5 deliverables from run record")
        # Build inputs for the assembly prompt
        solution = record.final_draft or ""
        if not solution and record.synthesis_result:
            solution = record.synthesis_result.unified_draft
        logger.info(f"Final draft: {len(solution)} chars")

        problem_brief = record.problem_brief
        if not problem_brief:
            logger.error("No problem brief — returning error response")
            return self._error_response(record), {"tokens_in": 0, "tokens_out": 0, "llm_calls": 0}

        objectives_str = "\n".join(f"- {o}" for o in problem_brief.objectives) if problem_brief.objectives else "None"
        constraints_str = "\n".join(f"- {c}" for c in problem_brief.constraints) if problem_brief.constraints else "None"

        # Format provenance data
        provenance_str = self._format_provenance(record)

        # Format alternative approaches from inventor solutions
        alternatives_str = self._format_alternatives(record)

        # Format refinement history
        refinement_str = self._format_refinement_history(record)

        # Collect all assumptions
        assumptions_str = self._collect_assumptions(record)

        prompt = AssemblyPrompts.ASSEMBLE.format(
            solution=solution,
            problem_brief=problem_brief.problem_statement,
            objectives=objectives_str,
            constraints=constraints_str,
            output_spec=problem_brief.output_spec or "Not provided",
            eval_criteria=problem_brief.eval_criteria or "Not provided",
            provenance=provenance_str,
            alternatives=alternatives_str,
            refinement_history=refinement_str,
            assumptions=assumptions_str,
        )

        logger.info(f"Calling LLM for assembly (prompt {len(prompt)} chars)...")
        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=AssemblyPrompts.SYSTEM,
            temperature=0.3,
            max_tokens=16384,
        )
        logger.info("Assembly LLM response received — parsing deliverables")

        # Parse the 5 deliverables
        executive_summary = response.get("executive_summary", "")
        solution_design_document = response.get("solution_design_document", "")
        foundation_documentation = response.get("foundation_documentation", "")
        self_eval_scorecard_md = response.get("self_evaluation_scorecard", "")
        run_log = response.get("run_log", "")

        logger.info(f"Deliverables: exec_summary={len(executive_summary)} chars, "
                     f"solution_doc={len(solution_design_document)} chars, "
                     f"foundation={len(foundation_documentation)} chars, "
                     f"scorecard={len(self_eval_scorecard_md)} chars, "
                     f"run_log={len(run_log)} chars")

        # Build evaluation scorecard
        evaluation_data = response.get("evaluation", {})
        scorecard = self.evaluator.build_scorecard(evaluation_data)
        logger.info(f"Evaluation: {scorecard.total_score:.1f}/{scorecard.max_score:.0f} "
                     f"({scorecard.score_percentage:.1f}%), "
                     f"disqualified={scorecard.disqualified}")

        # Store scorecard on record
        record.self_evaluation = scorecard

        # Combine all deliverables into single output
        output = self._combine_deliverables(
            executive_summary,
            solution_design_document,
            foundation_documentation,
            self_eval_scorecard_md,
            run_log,
        )

        # Collect known issues
        known_issues = self._collect_known_issues(record)
        if not known_issues:
            known_issues = ["No known issues identified"]

        # Collect assumptions
        all_assumptions = self._collect_all_assumptions(record)
        if not all_assumptions:
            all_assumptions = ["No explicit assumptions documented"]

        # Calculate usage stats
        usage_stats = self._calculate_usage(record, usage)

        # Build provenance list
        provenance_list = []
        if record.synthesis_result:
            provenance_list = record.synthesis_result.provenance

        # Build alternative approaches
        alternative_approaches = []
        for sol in record.inventor_solutions:
            if sol.content and not sol.content.startswith("[Inventor"):
                summary = sol.content[:200] + "..." if len(sol.content) > 200 else sol.content
                alternative_approaches.append(
                    f"Inventor {sol.inventor_id} ({sol.inventor_type}): {summary}"
                )

        zeus_response = ZeusResponse(
            output=output,
            assumptions=all_assumptions,
            known_issues=known_issues,
            run_id=record.run_id,
            usage=usage_stats,
            executive_summary=executive_summary,
            solution_design_document=solution_design_document,
            foundation_documentation=foundation_documentation,
            self_evaluation_scorecard=self_eval_scorecard_md,
            run_log=run_log,
            total_score=scorecard.total_score,
            max_score=scorecard.max_score,
            score_percentage=scorecard.score_percentage,
            disqualified=scorecard.disqualified,
            scorecard=scorecard,
            provenance=provenance_list,
            alternative_approaches=alternative_approaches,
        )

        return zeus_response, {"tokens_in": usage.get("tokens_in", 0), "tokens_out": usage.get("tokens_out", 0), "llm_calls": 1}

    def _format_provenance(self, record: RunRecord) -> str:
        """Format provenance data from synthesis."""
        if not record.synthesis_result or not record.synthesis_result.provenance:
            return "No provenance data available."
        lines = []
        for p in record.synthesis_result.provenance:
            modified = " (modified)" if p.modified else ""
            lines.append(f"- {p.element}: from Inventor {p.source_inventor}{modified} — {p.reason}")
        return "\n".join(lines)

    def _format_alternatives(self, record: RunRecord) -> str:
        """Format alternative approaches from inventor solutions."""
        if not record.inventor_solutions:
            return "No alternative approaches."
        parts = []
        for sol in record.inventor_solutions:
            reasoning = sol.reasoning_trace[:500] if sol.reasoning_trace else "No reasoning trace"
            parts.append(
                f"Inventor {sol.inventor_id} ({sol.inventor_type}):\n"
                f"  Libraries: {', '.join(sol.libraries_used) if sol.libraries_used else 'none'}\n"
                f"  Reasoning: {reasoning}"
            )
        return "\n\n".join(parts)

    def _format_refinement_history(self, record: RunRecord) -> str:
        """Format refinement iteration history."""
        if not record.refinement_history:
            return "No refinement iterations."
        lines = []
        for ri in record.refinement_history:
            lines.append(
                f"Iteration {ri.iteration}: {ri.issues_addressed} issues addressed, "
                f"{ri.blockers_remaining} blockers remaining, {ri.majors_remaining} majors remaining"
            )
        return "\n".join(lines)

    def _collect_assumptions(self, record: RunRecord) -> str:
        """Collect all assumptions for assembly prompt."""
        assumptions = []
        if record.problem_brief and record.problem_brief.implicit_assumptions:
            assumptions.extend(record.problem_brief.implicit_assumptions)
        for sol in record.inventor_solutions:
            assumptions.extend(sol.assumptions)
        if not assumptions:
            return "No assumptions collected."
        return "\n".join(f"- {a}" for a in assumptions)

    def _collect_all_assumptions(self, record: RunRecord) -> list[str]:
        """Collect all assumptions as a list for the response."""
        assumptions = []
        if record.problem_brief and record.problem_brief.implicit_assumptions:
            assumptions.extend(record.problem_brief.implicit_assumptions)
        for sol in record.inventor_solutions:
            assumptions.extend(sol.assumptions)
        return assumptions

    def _collect_known_issues(self, record: RunRecord) -> list[str]:
        """Collect known issues from critique and errors."""
        issues = []

        if record.library_critique:
            for issue in record.library_critique.all_issues:
                if issue.severity in ("major", "minor"):
                    issues.append(f"[{issue.severity.upper()}] {issue.description}")

        if record.synthesis_result and record.synthesis_result.open_issues:
            for oi in record.synthesis_result.open_issues:
                issues.append(f"[OPEN] {oi}")

        issues.extend(record.errors)
        return issues

    def _combine_deliverables(
        self,
        executive_summary: str,
        solution_design_document: str,
        foundation_documentation: str,
        self_eval_scorecard: str,
        run_log: str,
    ) -> str:
        """Combine all 5 deliverables into a single output document."""
        parts = [
            "# Deliverable 1: Executive Summary\n",
            executive_summary,
            "\n\n---\n\n",
            "# Deliverable 2: Solution Design Document\n",
            solution_design_document,
            "\n\n---\n\n",
            "# Deliverable 3: Foundation Documentation\n",
            foundation_documentation,
            "\n\n---\n\n",
            "# Deliverable 4: Self-Evaluation Scorecard\n",
            self_eval_scorecard,
            "\n\n---\n\n",
            "# Deliverable 5: Run Log\n",
            run_log,
        ]
        return "".join(parts)

    def _calculate_usage(self, record: RunRecord, assembly_usage: dict) -> UsageStats:
        """Calculate total usage statistics including cost."""
        budget = record.budget_used
        tokens_in = budget.tokens_in + assembly_usage.get("tokens_in", 0)
        tokens_out = budget.tokens_out + assembly_usage.get("tokens_out", 0)
        llm_calls = budget.llm_calls + 1
        total_tokens = tokens_in + tokens_out

        pricing = MODEL_PRICING.get(record.model_version, MODEL_PRICING["default"])
        cost_in = (tokens_in / 1_000_000) * pricing["input"]
        cost_out = (tokens_out / 1_000_000) * pricing["output"]
        cost_usd = round(cost_in + cost_out, 6)

        return UsageStats(
            llm_calls=llm_calls,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            total_tokens=total_tokens,
            cost_usd=cost_usd,
        )

    def _error_response(self, record: RunRecord) -> ZeusResponse:
        """Generate error response when assembly fails."""
        output = f"""# Solution Generation Failed

Unfortunately, Zeus was unable to generate a complete solution.

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
        return ZeusResponse(
            output=output,
            assumptions=["Generation failed — no assumptions available"],
            known_issues=record.errors or ["Generation failed"],
            run_id=record.run_id,
            total_score=0.0,
            score_percentage=0.0,
            disqualified=True,
            scorecard=SelfEvaluationScorecard(
                disqualified=True,
                disqualification_reasons=["Generation failed"],
            ),
        )
