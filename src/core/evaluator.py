"""Evaluator - 13-Criteria Evaluation Framework (/220 max)."""

from src.models.schemas import (
    CriterionScore,
    HardConstraintResult,
    SelfEvaluationScorecard,
)


# Full criteria definition: section, name, objective, weight, is_must
CRITERIA_DEFINITIONS = [
    ("1.1", "Capital Preservation", "1 (MUST)", 5.0, True),
    ("1.2", "Return Competitiveness", "2 (MUST)", 5.0, True),
    ("1.3", "Human Cognitive Efficiency", "7 (MUST)", 5.0, True),
    ("2.1", "First Principles Foundation", "3 (MUST)", 5.0, True),
    ("2.2", "Secrets & Differentiated Innovation", "4 (MUST)", 5.0, True),
    ("2.3", "Focused Mastery", "5 (MUST)", 5.0, True),
    ("2.4", "Adaptability", "6 (MUST)", 5.0, True),
    ("3.1", "Simplicity", "8 (COULD)", 2.0, False),
    ("3.2", "Human Input Capacity", "9 (COULD)", 2.0, False),
    ("3.3", "Transparency", "10 (COULD)", 2.0, False),
    ("4.3", "Crypto-Native", "C3 (SOFT)", 1.0, False),
    ("4.4", "Regulatory Environment", "C4 (SOFT)", 1.0, False),
    ("4.5", "Capital Requirements", "C5 (SOFT)", 1.0, False),
]

HARD_CONSTRAINTS = [
    ("C1", "Team Scale"),
    ("C2", "Digital and Remote"),
]

MAX_SCORE = 220.0  # (7 * 5 * 5.0) + (3 * 5 * 2.0) + (3 * 5 * 1.0) = 175 + 30 + 15


class Evaluator:
    """Builds a SelfEvaluationScorecard from LLM evaluation output.

    The LLM (via the assembly prompt) scores each criterion 1-5.
    This class validates, computes weighted scores, checks disqualification,
    and produces the final SelfEvaluationScorecard.
    """

    def build_scorecard(self, evaluation_data: dict) -> SelfEvaluationScorecard:
        """Build a scorecard from raw evaluation data returned by the LLM.

        Args:
            evaluation_data: Dict with 'criteria_scores', 'hard_constraints',
                             and optionally 'identified_weaknesses'.

        Returns:
            A fully computed SelfEvaluationScorecard.
        """
        criteria_scores = self._parse_criteria_scores(
            evaluation_data.get("criteria_scores", [])
        )
        hard_constraints = self._parse_hard_constraints(
            evaluation_data.get("hard_constraints", [])
        )

        # Compute totals
        total_score = sum(cs.weighted_score for cs in criteria_scores)
        score_percentage = (total_score / MAX_SCORE * 100) if MAX_SCORE > 0 else 0.0

        # Disqualification check
        disqualified, disqualification_reasons = self._check_disqualification(
            criteria_scores, hard_constraints
        )

        # Identify weaknesses (lowest scoring criteria)
        identified_weaknesses = evaluation_data.get("identified_weaknesses", [])
        if not identified_weaknesses:
            identified_weaknesses = self._identify_weaknesses(criteria_scores)

        return SelfEvaluationScorecard(
            criteria_scores=criteria_scores,
            hard_constraints=hard_constraints,
            total_score=round(total_score, 1),
            max_score=MAX_SCORE,
            score_percentage=round(score_percentage, 1),
            disqualified=disqualified,
            disqualification_reasons=disqualification_reasons,
            identified_weaknesses=identified_weaknesses,
        )

    def _parse_criteria_scores(self, raw_scores: list[dict]) -> list[CriterionScore]:
        """Parse and validate criteria scores from LLM output."""
        scores = []
        scores_by_section = {}

        for raw in raw_scores:
            section = raw.get("section", "")
            raw_score = raw.get("raw_score", 3)

            # Clamp to valid range
            raw_score = max(1, min(5, int(raw_score)))

            weight = float(raw.get("weight", 1.0))
            weighted_score = raw_score * weight

            score = CriterionScore(
                section=section,
                name=raw.get("name", ""),
                objective=raw.get("objective", ""),
                raw_score=raw_score,
                weight=weight,
                weighted_score=round(weighted_score, 1),
                justification=raw.get("justification", ""),
            )
            scores.append(score)
            scores_by_section[section] = score

        # Fill in any missing criteria with default score of 3
        for section, name, objective, weight, _ in CRITERIA_DEFINITIONS:
            if section not in scores_by_section:
                raw_score = 3
                scores.append(CriterionScore(
                    section=section,
                    name=name,
                    objective=objective,
                    raw_score=raw_score,
                    weight=weight,
                    weighted_score=round(raw_score * weight, 1),
                    justification="Score not provided; defaulted to 3.",
                ))

        return scores

    def _parse_hard_constraints(self, raw_constraints: list[dict]) -> list[HardConstraintResult]:
        """Parse HARD constraint results."""
        results = []
        seen_ids = set()

        for raw in raw_constraints:
            constraint_id = raw.get("constraint_id", "")
            results.append(HardConstraintResult(
                constraint_id=constraint_id,
                name=raw.get("name", ""),
                passed=raw.get("passed", True),
                notes=raw.get("notes", ""),
            ))
            seen_ids.add(constraint_id)

        # Fill in missing HARD constraints as passed (optimistic default)
        for cid, name in HARD_CONSTRAINTS:
            if cid not in seen_ids:
                results.append(HardConstraintResult(
                    constraint_id=cid,
                    name=name,
                    passed=True,
                    notes="Not explicitly assessed; defaulted to PASS.",
                ))

        return results

    def _check_disqualification(
        self,
        criteria_scores: list[CriterionScore],
        hard_constraints: list[HardConstraintResult],
    ) -> tuple[bool, list[str]]:
        """Check disqualification rules.

        Rules:
        - Any MUST criterion scoring < 3 is disqualifying.
        - Any HARD constraint failure is disqualifying.
        """
        reasons = []

        # Check MUST criteria
        must_sections = {section for section, _, _, _, is_must in CRITERIA_DEFINITIONS if is_must}
        for score in criteria_scores:
            if score.section in must_sections and score.raw_score < 3:
                reasons.append(
                    f"MUST criterion '{score.name}' ({score.section}) scored {score.raw_score}/5 (minimum 3 required)"
                )

        # Check HARD constraints
        for hc in hard_constraints:
            if not hc.passed:
                reasons.append(
                    f"HARD constraint '{hc.name}' ({hc.constraint_id}) FAILED"
                )

        return len(reasons) > 0, reasons

    def _identify_weaknesses(self, criteria_scores: list[CriterionScore]) -> list[str]:
        """Identify the lowest-scoring criteria as weaknesses."""
        if not criteria_scores:
            return []

        sorted_scores = sorted(criteria_scores, key=lambda s: s.raw_score)
        weaknesses = []
        for score in sorted_scores[:3]:
            if score.raw_score <= 3:
                weaknesses.append(
                    f"{score.name} ({score.section}): scored {score.raw_score}/5"
                )

        return weaknesses
