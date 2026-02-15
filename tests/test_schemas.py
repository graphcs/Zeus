"""Tests for Zeus data schemas."""

import pytest
from src.models.schemas import (
    ZeusRequest,
    ZeusResponse,
    ProblemClassification,
    ProblemBrief,
    InventorConfig,
    InventorSolution,
    CrossCritique,
    Provenance,
    ResolvedConflict,
    SynthesisResult,
    LibraryCritiqueIssue,
    LibraryCritiqueFinding,
    LibraryCritiqueResult,
    RefinementIteration,
    CriterionScore,
    HardConstraintResult,
    SelfEvaluationScorecard,
    RunRecord,
    BudgetUsed,
    BudgetConfig,
    UsageStats,
)


class TestZeusRequest:
    """Tests for ZeusRequest model."""

    def test_minimal_request(self):
        request = ZeusRequest(prompt="Build something")
        assert request.prompt == "Build something"
        assert request.constraints == []
        assert request.objectives == []
        assert request.context is None
        assert request.library_paths == []
        assert request.num_inventors == 4
        assert request.enable_cross_pollination is False

    def test_full_request(self):
        request = ZeusRequest(
            prompt="Build a task manager",
            constraints=["Must be async", "No external deps"],
            objectives=["High performance", "Low latency"],
            context={"existing_system": "Legacy API"},
            library_paths=["/path/to/lib1.md"],
            output_spec_path="/path/to/spec.md",
            eval_criteria_path="/path/to/eval.md",
            enable_cross_pollination=True,
            num_inventors=5,
        )
        assert len(request.constraints) == 2
        assert len(request.objectives) == 2
        assert request.context["existing_system"] == "Legacy API"
        assert request.enable_cross_pollination is True
        assert request.num_inventors == 5

    def test_num_inventors_bounds(self):
        with pytest.raises(ValueError):
            ZeusRequest(prompt="Test", num_inventors=0)
        with pytest.raises(ValueError):
            ZeusRequest(prompt="Test", num_inventors=11)


class TestProblemBrief:
    def test_create_problem_brief(self):
        brief = ProblemBrief(
            problem_statement="Build a task manager",
            constraints=["Must be async"],
            objectives=["High performance"],
            classification=ProblemClassification(
                problem_type="system_architecture",
                uncertainty_level="medium",
                key_domains=["distributed systems"],
            ),
            implicit_assumptions=["Python 3.11+"],
        )
        assert brief.problem_statement == "Build a task manager"
        assert "Must be async" in brief.constraints
        assert brief.classification.problem_type == "system_architecture"


class TestInventorModels:
    def test_inventor_config(self):
        config = InventorConfig(
            inventor_id="A",
            inventor_type="foundational",
            library_assignments=["first_principles", "mental_models"],
            emphasis="Focus on durable principles",
        )
        assert config.inventor_id == "A"
        assert len(config.library_assignments) == 2

    def test_inventor_solution(self):
        sol = InventorSolution(
            inventor_id="A",
            inventor_type="foundational",
            content="# Solution\nDetails here",
            assumptions=["Assume Python 3.11+"],
            reasoning_trace="Started with first principles...",
            libraries_used=["first_principles"],
        )
        assert sol.inventor_id == "A"
        assert len(sol.assumptions) == 1


class TestSynthesisModels:
    def test_provenance(self):
        p = Provenance(
            element="Risk control module",
            source_inventor="A",
            modified=True,
            reason="Enhanced with competitive insights from B",
        )
        assert p.modified is True

    def test_synthesis_result(self):
        result = SynthesisResult(
            unified_draft="# Unified Solution",
            version=1,
            provenance=[Provenance(element="Core", source_inventor="A")],
            resolved_conflicts=[ResolvedConflict(
                conflict="A vs B on architecture",
                resolution="Used A's approach",
                rationale="More scalable",
            )],
        )
        assert result.version == 1
        assert len(result.provenance) == 1
        assert len(result.resolved_conflicts) == 1


class TestCritiqueModels:
    def test_library_critique_issue(self):
        issue = LibraryCritiqueIssue(
            severity="blocker",
            description="Missing risk controls",
            suggested_fix="Add position sizing limits",
        )
        assert issue.severity == "blocker"

    def test_library_critique_result(self):
        result = LibraryCritiqueResult(
            findings=[LibraryCritiqueFinding(
                library_name="first_principles",
                violations=["No first principle for X"],
                embodied=["Y principle well applied"],
                coverage_pct=75.0,
            )],
            all_issues=[LibraryCritiqueIssue(severity="major", description="Test")],
            blocker_count=0,
            major_count=1,
            minor_count=0,
        )
        assert result.major_count == 1
        assert result.findings[0].coverage_pct == 75.0


class TestEvaluationModels:
    def test_criterion_score(self):
        score = CriterionScore(
            section="1.1",
            name="Capital Preservation",
            objective="1 (MUST)",
            raw_score=4,
            weight=5.0,
            weighted_score=20.0,
            justification="Strong risk controls",
        )
        assert score.weighted_score == 20.0

    def test_criterion_score_bounds(self):
        with pytest.raises(ValueError):
            CriterionScore(section="1.1", name="Test", objective="1", raw_score=0, weight=5.0)
        with pytest.raises(ValueError):
            CriterionScore(section="1.1", name="Test", objective="1", raw_score=6, weight=5.0)

    def test_hard_constraint_result(self):
        hc = HardConstraintResult(
            constraint_id="C1",
            name="Team Scale",
            passed=True,
            notes="5-person team sufficient",
        )
        assert hc.passed is True

    def test_scorecard_basics(self):
        scorecard = SelfEvaluationScorecard(
            criteria_scores=[
                CriterionScore(section="1.1", name="Test", objective="1 (MUST)", raw_score=4, weight=5.0, weighted_score=20.0),
            ],
            hard_constraints=[
                HardConstraintResult(constraint_id="C1", name="Team Scale", passed=True),
            ],
            total_score=20.0,
            max_score=220.0,
            score_percentage=9.1,
            disqualified=False,
        )
        assert scorecard.total_score == 20.0
        assert not scorecard.disqualified

    def test_scorecard_disqualification(self):
        scorecard = SelfEvaluationScorecard(
            disqualified=True,
            disqualification_reasons=["MUST criterion scored < 3"],
        )
        assert scorecard.disqualified is True
        assert len(scorecard.disqualification_reasons) == 1


class TestZeusResponse:
    def test_response_invariants(self):
        response = ZeusResponse(
            output="# Output",
            assumptions=[],
            known_issues=[],
            run_id="test-123",
        )
        assert response.assumptions is not None
        assert response.known_issues is not None
        assert response.run_id == "test-123"
        assert response.total_score == 0.0
        assert response.max_score == 220.0

    def test_response_with_deliverables(self):
        response = ZeusResponse(
            output="# Full output",
            assumptions=["Assume X"],
            known_issues=["Issue Y"],
            run_id="test-456",
            executive_summary="# Executive Summary",
            solution_design_document="# Solution Design",
            foundation_documentation="# Foundation",
            self_evaluation_scorecard="# Scorecard",
            run_log="# Run Log",
            total_score=165.0,
            score_percentage=75.0,
            disqualified=False,
        )
        assert response.executive_summary == "# Executive Summary"
        assert response.total_score == 165.0
        assert not response.disqualified


class TestRunRecord:
    def test_create_run_record(self):
        record = RunRecord(
            request=ZeusRequest(prompt="Test"),
        )
        assert record.run_id is not None
        assert record.timestamp is not None
        assert record.problem_brief is None
        assert record.inventor_solutions == []
        assert record.errors == []

    def test_run_record_with_phases(self):
        record = RunRecord(
            request=ZeusRequest(prompt="Test"),
            problem_brief=ProblemBrief(problem_statement="Test problem"),
            inventor_solutions=[
                InventorSolution(inventor_id="A", content="Solution A"),
                InventorSolution(inventor_id="B", content="Solution B"),
            ],
            synthesis_result=SynthesisResult(unified_draft="# Unified"),
        )
        assert record.problem_brief is not None
        assert len(record.inventor_solutions) == 2
        assert record.synthesis_result.unified_draft == "# Unified"


class TestBudgetConfig:
    def test_default_budget(self):
        config = BudgetConfig()
        assert config.max_llm_calls == 30
        assert config.target_llm_calls == 20
        assert config.max_revisions == 3
        assert config.per_call_timeout == 120.0
        assert config.total_run_timeout == 900.0

    def test_custom_budget(self):
        config = BudgetConfig(max_llm_calls=10, max_revisions=1)
        assert config.max_llm_calls == 10
        assert config.max_revisions == 1
