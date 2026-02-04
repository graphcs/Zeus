"""Constraint Checker - V3 Deterministic and Semantic Verification."""

import json
import logging
from src.models.schemas import (
    ConstraintCheckResult,
    VerificationReport,
)
from src.llm.openrouter import OpenRouterClient
from src.prompts.constraint_verification import ConstraintVerificationPrompts

logger = logging.getLogger(__name__)

class ConstraintChecker:
    """Verifies content against constraints using LLM and deterministic checks."""

    def __init__(self, client: OpenRouterClient):
        self.client = client

    async def verify_constraints(self, content: str, constraints: list[str]) -> tuple[VerificationReport | None, dict[str, int]]:
        """Verify constraints against content.
        
        Args:
            content: The generated solution/brief content.
            constraints: List of constraint strings. 
            
        Returns:
            Tuple of (VerificationReport or None, usage_stats).
        """
        empty_usage = {"tokens_in": 0, "tokens_out": 0}

        if not constraints:
            return None, empty_usage

        try:
            # Prepare prompt
            constraints_text = "\n".join(f"- {c}" for c in constraints)
            prompt = ConstraintVerificationPrompts.VERIFY_CONSTRAINTS.format(
                content=content,
                constraints_list=constraints_text
            )

            # NOTE: generate returns (content, usage)
            data, usage = await self.client.generate_json(
                system=ConstraintVerificationPrompts.SYSTEM,
                prompt=prompt,
                temperature=0.0 # Deterministic
            )

            # Parse results
            checks_data = data.get("checks", [])
            
            checks = []
            for c_data in checks_data:
                # Validate against schema
                # Ensure status is valid
                status = c_data.get("status", "unverified")
                if status not in ["pass", "fail", "unverified"]:
                    status = "unverified"
                
                checks.append(ConstraintCheckResult(
                    constraint=c_data.get("constraint", "Unknown constraint"),
                    status=status,
                    evidence=c_data.get("evidence", "")
                ))
            
            # Compute coverage score
            verified_count = sum(1 for c in checks if c.status in ("pass", "fail"))
            total = len(constraints)
            coverage = verified_count / total if total > 0 else 0.0

            return VerificationReport(
                checks=checks,
                coverage_score=coverage
            ), usage

        except Exception as e:
            logger.error(f"Constraint verification failed: {e}")
            return None, empty_usage
