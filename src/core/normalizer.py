"""Normalizer - Phase 0: Intake & Problem Understanding."""

import json
import logging
from pathlib import Path
from src.models.schemas import ZeusRequest, ProblemBrief, ProblemClassification
from src.llm.openrouter import OpenRouterClient
from src.prompts.intake import IntakePrompts

logger = logging.getLogger(__name__)


class Normalizer:
    """Normalizes input requests into structured ProblemBriefs."""

    def __init__(self, llm_client: OpenRouterClient):
        self.llm = llm_client

    async def normalize(self, request: ZeusRequest) -> tuple[ProblemBrief, dict[str, int]]:
        """Normalize a request into a ProblemBrief.

        Args:
            request: The Zeus request to normalize.

        Returns:
            Tuple of (ProblemBrief, usage_stats).
        """
        logger.info(f"Normalizing request: prompt {len(request.prompt)} chars, "
                     f"{len(request.constraints)} constraints, {len(request.objectives)} objectives")

        context_str = self._format_context(request.context)
        constraints_str = "\n".join(f"- {c}" for c in request.constraints) if request.constraints else "None specified"
        objectives_str = "\n".join(f"- {o}" for o in request.objectives) if request.objectives else "None specified"

        # Load output spec and eval criteria if paths provided
        output_spec = self._load_file(request.output_spec_path) if request.output_spec_path else "Not provided"
        eval_criteria = self._load_file(request.eval_criteria_path) if request.eval_criteria_path else "Not provided"
        if request.output_spec_path:
            logger.info(f"Output spec loaded: {len(output_spec)} chars from {request.output_spec_path}")
        if request.eval_criteria_path:
            logger.info(f"Eval criteria loaded: {len(eval_criteria)} chars from {request.eval_criteria_path}")

        logger.info("Calling LLM for intake normalization...")
        prompt = IntakePrompts.NORMALIZE.format(
            prompt=request.prompt,
            objectives=objectives_str,
            constraints=constraints_str,
            context=context_str,
            output_spec=output_spec,
            eval_criteria=eval_criteria,
        )

        response, usage = await self.llm.generate_json(
            prompt=prompt,
            system=IntakePrompts.SYSTEM,
            temperature=0.3,
        )
        logger.info("Intake LLM response received — parsing ProblemBrief")

        # Parse classification
        classification_data = response.get("classification", {})
        classification = ProblemClassification(
            problem_type=classification_data.get("problem_type", "general"),
            uncertainty_level=classification_data.get("uncertainty_level", "medium"),
            key_domains=classification_data.get("key_domains", []),
            recommended_library_emphasis=classification_data.get("recommended_library_emphasis", []),
        )

        # Build ProblemBrief, ensuring constraints are never dropped
        brief = ProblemBrief(
            problem_statement=response.get("problem_statement", request.prompt),
            objectives=self._merge_lists(request.objectives, response.get("objectives", [])),
            constraints=self._merge_constraints(request.constraints, response.get("constraints", [])),
            classification=classification,
            implicit_assumptions=response.get("implicit_assumptions", []),
            ambiguities=response.get("ambiguities", []),
            output_spec=output_spec if output_spec != "Not provided" else "",
            eval_criteria=eval_criteria if eval_criteria != "Not provided" else "",
            context=response.get("context", {}),
        )

        logger.info(f"ProblemBrief: type='{classification.problem_type}', "
                     f"uncertainty='{classification.uncertainty_level}', "
                     f"domains={classification.key_domains}, "
                     f"{len(brief.constraints)} constraints, {len(brief.objectives)} objectives, "
                     f"{len(brief.implicit_assumptions)} assumptions, {len(brief.ambiguities)} ambiguities")
        return brief, usage

    def _format_context(self, context: str | dict | None) -> str:
        if context is None:
            return "None provided"
        if isinstance(context, str):
            return context
        return json.dumps(context, indent=2)

    def _merge_constraints(self, original: list[str], extracted: list[str]) -> list[str]:
        """Merge constraints, ensuring originals are never dropped."""
        merged = list(original)
        original_lower = {c.lower() for c in original}
        for constraint in extracted:
            if constraint.lower() not in original_lower:
                merged.append(constraint)
        return merged

    def _merge_lists(self, original: list[str], extracted: list[str]) -> list[str]:
        """Merge lists, preserving originals."""
        merged = list(original)
        original_lower = {o.lower() for o in original}
        for item in extracted:
            if item.lower() not in original_lower:
                merged.append(item)
        return merged

    def _load_file(self, path: str | None) -> str:
        """Load file content from path."""
        if not path:
            return ""
        p = Path(path)
        if p.exists():
            try:
                return p.read_text(encoding="utf-8")
            except Exception:
                return ""
        return ""
