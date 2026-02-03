"""Normalizer - Converts ZeusRequest to NormalizedProblem."""

import json
from src.models.schemas import ZeusRequest, NormalizedProblem
from src.llm.openrouter import OpenRouterClient
from src.prompts.design_brief import DesignBriefPrompts
from src.prompts.solution_designer import SolutionDesignerPrompts


class Normalizer:
    """Normalizes input requests into structured problems."""

    def __init__(self, llm_client: OpenRouterClient):
        """Initialize normalizer with LLM client."""
        self.llm = llm_client

    async def normalize(self, request: ZeusRequest) -> tuple[NormalizedProblem, dict[str, int]]:
        """Normalize a request into a structured problem.

        Args:
            request: The Zeus request to normalize.

        Returns:
            Tuple of (NormalizedProblem, usage_stats).
        """
        # Select prompts based on mode
        prompts = DesignBriefPrompts if request.mode == "brief" else SolutionDesignerPrompts

        # Format context
        context_str = self._format_context(request.context)
        constraints_str = "\n".join(f"- {c}" for c in request.constraints) if request.constraints else "None specified"

        # Build the normalization prompt
        prompt = prompts.NORMALIZE.format(
            prompt=request.prompt,
            constraints=constraints_str,
            context=context_str,
        )

        # Call LLM for structured extraction
        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=prompts.SYSTEM,
            temperature=0.3,  # Lower temperature for extraction
        )

        # Build NormalizedProblem, ensuring constraints are never dropped
        normalized = NormalizedProblem(
            problem_statement=response.get("problem_statement", request.prompt),
            constraints=self._merge_constraints(request.constraints, response.get("constraints", [])),
            output_spec=response.get("output_spec", self._default_output_spec(request.mode)),
            context=response.get("context", {}),
        )

        return normalized, usage

    def _format_context(self, context: str | dict | None) -> str:
        """Format context for the prompt."""
        if context is None:
            return "None provided"
        if isinstance(context, str):
            return context
        return json.dumps(context, indent=2)

    def _merge_constraints(self, original: list[str], extracted: list[str]) -> list[str]:
        """Merge constraints, ensuring originals are never dropped.

        Args:
            original: User-provided constraints (must all be preserved).
            extracted: LLM-extracted constraints.

        Returns:
            Merged list with all original constraints present.
        """
        # Start with all original constraints
        merged = list(original)

        # Add any extracted constraints not already present
        original_lower = {c.lower() for c in original}
        for constraint in extracted:
            if constraint.lower() not in original_lower:
                merged.append(constraint)

        return merged

    def _default_output_spec(self, mode: str) -> str:
        """Get default output specification based on mode."""
        if mode == "brief":
            return "A structured Design Brief with clear problem statement, requirements, constraints, and success criteria"
        return "A comprehensive Target Solution with architecture, components, interfaces, and implementation guidance"
