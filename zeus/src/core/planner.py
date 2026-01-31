"""Planner - Creates linear plans for generation tasks."""

import json
from src.models.schemas import NormalizedProblem, Plan, PlanStep
from src.llm.openrouter import OpenRouterClient
from src.prompts.design_brief import DesignBriefPrompts
from src.prompts.solution_designer import SolutionDesignerPrompts


class Planner:
    """Creates linear plans for generation tasks."""

    def __init__(self, llm_client: OpenRouterClient):
        """Initialize planner with LLM client."""
        self.llm = llm_client

    async def plan(
        self,
        problem: NormalizedProblem,
        mode: str,
    ) -> tuple[Plan, dict[str, int]]:
        """Create a plan for generating output.

        Args:
            problem: The normalized problem.
            mode: "brief" or "solution".

        Returns:
            Tuple of (Plan, usage_stats).
        """
        prompts = DesignBriefPrompts if mode == "brief" else SolutionDesignerPrompts

        constraints_str = "\n".join(f"- {c}" for c in problem.constraints) if problem.constraints else "None"
        context_str = json.dumps(problem.context, indent=2) if problem.context else "None"

        prompt = prompts.PLAN.format(
            problem_statement=problem.problem_statement,
            constraints=constraints_str,
            output_spec=problem.output_spec,
            context=context_str,
        )

        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=prompts.SYSTEM,
            temperature=0.5,
        )

        # Parse steps
        steps = []
        for step_data in response.get("steps", []):
            steps.append(PlanStep(
                step_number=step_data.get("step_number", len(steps) + 1),
                description=step_data.get("description", ""),
                focus_area=step_data.get("focus_area", ""),
            ))

        # If no steps were returned, create default steps
        if not steps:
            steps = self._default_plan(mode)

        return Plan(steps=steps), usage

    def _default_plan(self, mode: str) -> list[PlanStep]:
        """Generate default plan steps if LLM fails."""
        if mode == "brief":
            return [
                PlanStep(step_number=1, description="Analyze the problem statement", focus_area="problem_analysis"),
                PlanStep(step_number=2, description="Identify key requirements", focus_area="requirements"),
                PlanStep(step_number=3, description="Define scope boundaries", focus_area="scope"),
                PlanStep(step_number=4, description="Establish success criteria", focus_area="success_criteria"),
                PlanStep(step_number=5, description="Document constraints", focus_area="constraints"),
                PlanStep(step_number=6, description="List assumptions", focus_area="assumptions"),
            ]
        else:
            return [
                PlanStep(step_number=1, description="Analyze requirements from brief", focus_area="requirements"),
                PlanStep(step_number=2, description="Design system architecture", focus_area="architecture"),
                PlanStep(step_number=3, description="Define components and interfaces", focus_area="components"),
                PlanStep(step_number=4, description="Specify data models", focus_area="data_model"),
                PlanStep(step_number=5, description="Address security concerns", focus_area="security"),
                PlanStep(step_number=6, description="Assess risks and mitigations", focus_area="risk"),
                PlanStep(step_number=7, description="Define testing strategy", focus_area="testing"),
            ]
