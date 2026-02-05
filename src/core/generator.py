"""Generator - LLM-based generation of candidates."""

import json
import re
from src.models.schemas import NormalizedProblem, Plan, Candidate, Critique
from src.llm.openrouter import OpenRouterClient
from src.prompts.design_brief import DesignBriefPrompts
from src.prompts.solution_designer import SolutionDesignerPrompts


class Generator:
    """Generates design brief or solution candidates using LLM."""

    def __init__(self, llm_client: OpenRouterClient):
        """Initialize generator with LLM client."""
        self.llm = llm_client

    async def generate(
        self,
        problem: NormalizedProblem,
        plan: Plan,
        mode: str,
    ) -> tuple[Candidate, dict[str, int]]:
        """Generate a candidate design brief or solution.

        Args:
            problem: The normalized problem.
            plan: The generation plan.
            mode: "brief" or "solution".

        Returns:
            Tuple of (Candidate, usage_stats).
        """
        prompts = DesignBriefPrompts if mode == "brief" else SolutionDesignerPrompts

        # Format inputs
        constraints_str = "\n".join(f"- {c}" for c in problem.constraints) if problem.constraints else "None"
        context_str = json.dumps(problem.context, indent=2) if problem.context else "None"
        plan_str = self._format_plan(plan)
        
        human_suggestions_str = "\n".join(f"- {h}" for h in problem.human_suggestions) if problem.human_suggestions else "None"
        prior_solutions_str = "\n".join(f"- {p}" for p in problem.prior_solutions) if problem.prior_solutions else "None"

        prompt = prompts.GENERATE.format(
            problem_statement=problem.problem_statement,
            constraints=constraints_str,
            output_spec=problem.output_spec,
            context=context_str,
            human_suggestions=human_suggestions_str,
            prior_solutions=prior_solutions_str,
            plan=plan_str,
        )

        if mode == "solution":
            # Two-step generation for Solution mode to ensure robustness
            
            # Step 1: Content
            content_prompt = prompt + "\n\nCRITICAL INSTRUCTION: Output ONLY the Markdown content for the solution. Do not include JSON metadata."
            content_response, usage_1 = await self.llm.generate(
                prompt=content_prompt,
                system=prompts.SYSTEM,
                temperature=0.7,
                max_tokens=8192,
            )
            
            # Step 2: Metadata Extraction
            extract_prompt = f"""Analyze the Solution content above and extract the following metadata in JSON format:
{{
    "assumptions": ["List of assumptions made"],
    "uncertainty_flags": ["Areas of uncertainty or decisions deferred"],
    "reasoning_trace": "Compressed explanation of key decisions and rationale",
    "comparison_analysis": "Explicit delta highlighting improvements or regressions to prior solutions or alternatives"
}}

SOLUTION CONTENT:
{content_response[:20000]}  # Truncated if too long
"""
            metadata_response, usage_2 = await self.llm.generate_json(
                prompt=extract_prompt,
                system="You are a data extractor.",
                temperature=0.3,
            )

            response = {
                "content": content_response,
                **metadata_response
            }
            
            # Combine usage
            usage = {
                "tokens_in": usage_1.get("tokens_in", 0) + usage_2.get("tokens_in", 0),
                "tokens_out": usage_1.get("tokens_out", 0) + usage_2.get("tokens_out", 0),
            }

        else:
            response, usage = await self.llm.generate_json(
                prompt=prompt,
                system=prompts.SYSTEM,
                temperature=0.7,
                max_tokens=8192,  # Larger output for comprehensive content
            )

        candidate = Candidate(
            content=response.get("content", ""),
            assumptions=response.get("assumptions", []),
            uncertainty_flags=response.get("uncertainty_flags", []),
            reasoning_trace=response.get("reasoning_trace", ""),
            comparison_analysis=response.get("comparison_analysis", ""),
        )


        return candidate, usage

    async def revise(
        self,
        candidate: Candidate,
        critique: Critique,
        problem: NormalizedProblem,
        mode: str,
    ) -> tuple[Candidate, dict[str, int]]:
        """Revise a candidate based on critique feedback.

        Args:
            candidate: The original candidate.
            critique: The critique to address.
            problem: The normalized problem.
            mode: "brief" or "solution".

        Returns:
            Tuple of (revised Candidate, usage_stats).
        """
        prompts = DesignBriefPrompts if mode == "brief" else SolutionDesignerPrompts

        constraints_str = "\n".join(f"- {c}" for c in problem.constraints) if problem.constraints else "None"
        context_str = json.dumps(problem.context, indent=2) if problem.context else "None"
        critique_str = self._format_critique(critique)

        human_suggestions_str = "\n".join(f"- {h}" for h in problem.human_suggestions) if problem.human_suggestions else "None"
        prior_solutions_str = "\n".join(f"- {p}" for p in problem.prior_solutions) if problem.prior_solutions else "None"

        prompt = prompts.REVISE.format(
            content=candidate.content,
            critique=critique_str,
            constraints=constraints_str,
            context=context_str,
            human_suggestions=human_suggestions_str,
            prior_solutions=prior_solutions_str,
        )

        if mode == "solution":
             # Two-step generation for Solution mode to ensure robustness
            
            # Step 1: Content (Revised)
            content_prompt = prompt + "\n\nCRITICAL INSTRUCTION: Output ONLY the revised Markdown content for the solution. Do not include JSON metadata."
            content_response, usage_1 = await self.llm.generate(
                prompt=content_prompt,
                system=prompts.SYSTEM,
                temperature=0.7,
                max_tokens=8192,
            )
            
            # Step 2: Metadata Extraction (Revised)
            extract_prompt = f"""Analyze the Revised Solution content above and extract the following metadata in JSON format.
Ensure you update the reasoning trace and comparison analysis based on the revision.

{{
    "assumptions": ["Updated list of assumptions"],
    "uncertainty_flags": ["Updated areas of uncertainty"],
    "reasoning_trace": "Updated compressed explanation of key decisions and rationale",
    "comparison_analysis": "Updated explicit delta highlighting improvements or regressions"
}}

REVISED SOLUTION CONTENT:
{content_response[:20000]}
"""
            metadata_response, usage_2 = await self.llm.generate_json(
                prompt=extract_prompt,
                system="You are a data extractor.",
                temperature=0.3,
            )

            response = {
                "content": content_response,
                **metadata_response
            }
            
            # Combine usage
            usage = {
                "tokens_in": usage_1.get("tokens_in", 0) + usage_2.get("tokens_in", 0),
                "tokens_out": usage_1.get("tokens_out", 0) + usage_2.get("tokens_out", 0),
            }
        else:
            response, usage = await self.llm.generate_json(
                prompt=prompt,
                system=prompts.SYSTEM,
                temperature=0.7,
                max_tokens=8192,
            )

        revised = Candidate(
            content=response.get("content", candidate.content),
            assumptions=response.get("assumptions", candidate.assumptions),
            uncertainty_flags=response.get("uncertainty_flags", candidate.uncertainty_flags),
            reasoning_trace=response.get("reasoning_trace", candidate.reasoning_trace),
            comparison_analysis=response.get("comparison_analysis", candidate.comparison_analysis),
        )

        return revised, usage

    def _format_plan(self, plan: Plan) -> str:
        """Format plan for prompt."""
        if not plan.steps:
            return "No specific plan - generate comprehensive output"

        lines = []
        for step in plan.steps:
            lines.append(f"{step.step_number}. {step.description} (Focus: {step.focus_area})")
        return "\n".join(lines)

    def _format_critique(self, critique: Critique) -> str:
        """Format critique for revision prompt."""
        lines = ["## Issues to Address"]

        for issue in critique.issues:
            severity_marker = {"blocker": "🚫", "major": "⚠️", "minor": "ℹ️"}.get(issue.severity, "•")
            lines.append(f"\n### {severity_marker} [{issue.severity.upper()}] {issue.role}")
            lines.append(f"**Issue:** {issue.description}")
            if issue.suggested_fix:
                lines.append(f"**Suggested Fix:** {issue.suggested_fix}")

        if critique.constraint_violations:
            lines.append("\n## Constraint Violations")
            for violation in critique.constraint_violations:
                lines.append(f"- {violation}")

        if critique.missing_perspectives:
            lines.append("\n## Missing Perspectives")
            for perspective in critique.missing_perspectives:
                lines.append(f"- {perspective}")

        return "\n".join(lines)
