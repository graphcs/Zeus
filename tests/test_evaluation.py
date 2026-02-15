"""Tests for the 13-criteria evaluation framework."""

import pytest
from src.core.evaluator import Evaluator, CRITERIA_DEFINITIONS, MAX_SCORE
from src.models.schemas import CriterionScore, HardConstraintResult, SelfEvaluationScorecard


class TestEvaluator:
    """Tests for the Evaluator class."""

    def setup_method(self):
        self.evaluator = Evaluator()

    def test_max_score_constant(self):
        """Verify max score calculation: (7*5*5.0) + (3*5*2.0) + (3*5*1.0) = 220."""
        assert MAX_SCORE == 220.0

    def test_criteria_count(self):
        """Verify we have exactly 13 criteria."""
        assert len(CRITERIA_DEFINITIONS) == 13

    def test_must_criteria_count(self):
        """Verify we have exactly 7 MUST criteria."""
        must_count = sum(1 for _, _, _, _, is_must in CRITERIA_DEFINITIONS if is_must)
        assert must_count == 7

    def test_perfect_score(self):
        """Test scorecard with all 5s."""
        raw_scores = []
        for section, name, objective, weight, _ in CRITERIA_DEFINITIONS:
            raw_scores.append({
                "section": section,
                "name": name,
                "objective": objective,
                "raw_score": 5,
                "weight": weight,
            })

        hard_constraints = [
            {"constraint_id": "C1", "name": "Team Scale", "passed": True},
            {"constraint_id": "C2", "name": "Digital and Remote", "passed": True},
        ]

        scorecard = self.evaluator.build_scorecard({
            "criteria_scores": raw_scores,
            "hard_constraints": hard_constraints,
        })

        assert scorecard.total_score == 220.0
        assert scorecard.score_percentage == 100.0
        assert not scorecard.disqualified
        assert scorecard.disqualification_reasons == []

    def test_minimum_passing_score(self):
        """Test scorecard where all MUST criteria are exactly 3."""
        raw_scores = []
        for section, name, objective, weight, _ in CRITERIA_DEFINITIONS:
            raw_scores.append({
                "section": section,
                "name": name,
                "objective": objective,
                "raw_score": 3,
                "weight": weight,
            })

        scorecard = self.evaluator.build_scorecard({
            "criteria_scores": raw_scores,
            "hard_constraints": [
                {"constraint_id": "C1", "name": "Team Scale", "passed": True},
                {"constraint_id": "C2", "name": "Digital and Remote", "passed": True},
            ],
        })

        expected_score = sum(3 * w for _, _, _, w, _ in CRITERIA_DEFINITIONS)
        assert scorecard.total_score == expected_score
        assert not scorecard.disqualified

    def test_disqualification_must_below_3(self):
        """Test that a MUST criterion < 3 disqualifies."""
        raw_scores = []
        for section, name, objective, weight, is_must in CRITERIA_DEFINITIONS:
            score = 2 if section == "1.1" else 4  # Capital Preservation gets 2
            raw_scores.append({
                "section": section,
                "name": name,
                "objective": objective,
                "raw_score": score,
                "weight": weight,
            })

        scorecard = self.evaluator.build_scorecard({
            "criteria_scores": raw_scores,
            "hard_constraints": [
                {"constraint_id": "C1", "name": "Team Scale", "passed": True},
                {"constraint_id": "C2", "name": "Digital and Remote", "passed": True},
            ],
        })

        assert scorecard.disqualified is True
        assert len(scorecard.disqualification_reasons) == 1
        assert "Capital Preservation" in scorecard.disqualification_reasons[0]

    def test_disqualification_hard_constraint_fail(self):
        """Test that a HARD constraint failure disqualifies."""
        raw_scores = []
        for section, name, objective, weight, _ in CRITERIA_DEFINITIONS:
            raw_scores.append({
                "section": section,
                "name": name,
                "objective": objective,
                "raw_score": 4,
                "weight": weight,
            })

        scorecard = self.evaluator.build_scorecard({
            "criteria_scores": raw_scores,
            "hard_constraints": [
                {"constraint_id": "C1", "name": "Team Scale", "passed": False, "notes": "Requires 50+ people"},
                {"constraint_id": "C2", "name": "Digital and Remote", "passed": True},
            ],
        })

        assert scorecard.disqualified is True
        assert any("Team Scale" in r for r in scorecard.disqualification_reasons)

    def test_score_clamping(self):
        """Test that scores are clamped to 1-5."""
        raw_scores = [{
            "section": "1.1",
            "name": "Capital Preservation",
            "objective": "1 (MUST)",
            "raw_score": 10,  # Over max
            "weight": 5.0,
        }]

        scorecard = self.evaluator.build_scorecard({"criteria_scores": raw_scores})
        # Find the 1.1 score
        score_1_1 = next(s for s in scorecard.criteria_scores if s.section == "1.1")
        assert score_1_1.raw_score == 5  # Clamped to max

    def test_missing_criteria_defaults(self):
        """Test that missing criteria get default score of 3."""
        scorecard = self.evaluator.build_scorecard({"criteria_scores": []})
        assert len(scorecard.criteria_scores) == 13  # All filled in
        for score in scorecard.criteria_scores:
            assert score.raw_score == 3

    def test_missing_hard_constraints_default_pass(self):
        """Test that missing HARD constraints default to PASS."""
        scorecard = self.evaluator.build_scorecard({"hard_constraints": []})
        assert len(scorecard.hard_constraints) == 2
        for hc in scorecard.hard_constraints:
            assert hc.passed is True

    def test_identified_weaknesses(self):
        """Test weakness identification from low scores."""
        raw_scores = []
        for section, name, objective, weight, _ in CRITERIA_DEFINITIONS:
            score = 2 if section in ("3.1", "4.3") else 4
            raw_scores.append({
                "section": section,
                "name": name,
                "objective": objective,
                "raw_score": score,
                "weight": weight,
            })

        scorecard = self.evaluator.build_scorecard({"criteria_scores": raw_scores})
        assert len(scorecard.identified_weaknesses) > 0
        weakness_text = " ".join(scorecard.identified_weaknesses)
        assert "Simplicity" in weakness_text or "Crypto-Native" in weakness_text

    def test_weight_math(self):
        """Verify weight calculations are correct."""
        raw_scores = [{
            "section": "1.1",
            "name": "Capital Preservation",
            "objective": "1 (MUST)",
            "raw_score": 4,
            "weight": 5.0,
        }]

        scorecard = self.evaluator.build_scorecard({"criteria_scores": raw_scores})
        score_1_1 = next(s for s in scorecard.criteria_scores if s.section == "1.1")
        assert score_1_1.weighted_score == 20.0  # 4 * 5.0

    def test_empty_evaluation_data(self):
        """Test with completely empty evaluation data."""
        scorecard = self.evaluator.build_scorecard({})
        assert scorecard.total_score > 0  # Default scores of 3
        assert not scorecard.disqualified  # All defaults pass minimum
