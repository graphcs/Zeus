"""Constraint Checker - V3 Deterministic and Semantic Verification."""

import re
import logging
from src.models.schemas import (
    ConstraintCheckResult,
    VerificationReport,
)
from src.llm.openrouter import OpenRouterClient
from src.prompts.constraint_verification import ConstraintVerificationPrompts

logger = logging.getLogger(__name__)


class ConstraintChecker:
    """Verifies content against constraints using deterministic and LLM checks."""

    def __init__(self, client: OpenRouterClient):
        self.client = client

    @staticmethod
    def _check_deterministic(content: str, constraint: str) -> ConstraintCheckResult | None:
        """Attempt rule-based constraint verification before falling back to LLM.

        Patterns detected:
        1. Section presence: "must include/contain/have ... section"
        2. Word/length limits: "under/less than/fewer than N words"
        3. Keyword presence: "must mention/address/cover X"

        Returns:
            ConstraintCheckResult if deterministic check succeeds, None to fall through to LLM.
        """
        c_lower = constraint.lower().strip()

        # Pattern 1: Section presence — "must include/contain/have ... section"
        section_match = re.search(
            r"must\s+(?:include|contain|have)\s+(?:a\s+)?(.+?)\s+section",
            c_lower,
        )
        if section_match:
            section_name = section_match.group(1).strip()
            # Search for heading containing the section name
            headings = re.findall(r"^#{1,3}\s+(.+)", content, re.MULTILINE | re.IGNORECASE)
            found = any(section_name in h.lower() for h in headings)
            return ConstraintCheckResult(
                constraint=constraint,
                status="pass" if found else "fail",
                evidence=f"Section '{section_name}' {'found' if found else 'not found'} in headings",
            )

        # Pattern 2: Word count — "under/less than/fewer than N words"
        word_limit_match = re.search(
            r"(?:under|less than|fewer than|at most|max(?:imum)?)\s+(\d+)\s+words",
            c_lower,
        )
        if word_limit_match:
            limit = int(word_limit_match.group(1))
            word_count = len(content.split())
            passed = word_count < limit
            return ConstraintCheckResult(
                constraint=constraint,
                status="pass" if passed else "fail",
                evidence=f"Word count: {word_count} (limit: {limit})",
            )

        # Pattern 3: Keyword presence — "must mention/address/cover X"
        keyword_match = re.search(
            r"must\s+(?:mention|address|cover)\s+(.+)",
            c_lower,
        )
        if keyword_match:
            keyword = keyword_match.group(1).strip().rstrip(".")
            found = keyword in content.lower()
            return ConstraintCheckResult(
                constraint=constraint,
                status="pass" if found else "fail",
                evidence=f"Keyword '{keyword}' {'found' if found else 'not found'} in content",
            )

        # No deterministic pattern matched
        return None

    async def verify_constraints(self, content: str, constraints: list[str]) -> tuple[VerificationReport | None, dict[str, int]]:
        """Verify constraints against content.

        Tries deterministic checks first, then falls back to LLM for remaining constraints.

        Args:
            content: The generated solution/brief content.
            constraints: List of constraint strings.

        Returns:
            Tuple of (VerificationReport or None, usage_stats).
        """
        empty_usage = {"tokens_in": 0, "tokens_out": 0}

        if not constraints:
            return None, empty_usage

        # First pass: deterministic checks
        deterministic_results: list[ConstraintCheckResult] = []
        remaining_constraints: list[str] = []

        for constraint in constraints:
            result = self._check_deterministic(content, constraint)
            if result is not None:
                deterministic_results.append(result)
            else:
                remaining_constraints.append(constraint)

        # Second pass: LLM for remaining constraints
        llm_results: list[ConstraintCheckResult] = []
        usage = empty_usage

        if remaining_constraints:
            try:
                constraints_text = "\n".join(f"- {c}" for c in remaining_constraints)
                prompt = ConstraintVerificationPrompts.VERIFY_CONSTRAINTS.format(
                    content=content,
                    constraints_list=constraints_text
                )

                data, usage = await self.client.generate_json(
                    system=ConstraintVerificationPrompts.SYSTEM,
                    prompt=prompt,
                    temperature=0.0
                )

                checks_data = data.get("checks", [])

                for c_data in checks_data:
                    status = c_data.get("status", "unverified")
                    if status not in ["pass", "fail", "unverified"]:
                        status = "unverified"

                    llm_results.append(ConstraintCheckResult(
                        constraint=c_data.get("constraint", "Unknown constraint"),
                        status=status,
                        evidence=c_data.get("evidence", "")
                    ))

            except Exception as e:
                logger.error(f"Constraint verification (LLM) failed: {e}")
                # Mark remaining as unverified
                for c in remaining_constraints:
                    llm_results.append(ConstraintCheckResult(
                        constraint=c,
                        status="unverified",
                        evidence=f"LLM verification failed: {e}",
                    ))

        # Merge results
        all_checks = deterministic_results + llm_results
        verified_count = sum(1 for c in all_checks if c.status in ("pass", "fail"))
        total = len(constraints)
        coverage = verified_count / total if total > 0 else 0.0

        return VerificationReport(
            checks=all_checks,
            coverage_score=coverage
        ), usage
