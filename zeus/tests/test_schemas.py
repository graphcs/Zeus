"""Tests for Zeus data schemas."""

import pytest
from zeus.models.schemas import (
    ZeusRequest,
    ZeusResponse,
    NormalizedProblem,
    Candidate,
    CritiqueIssue,
    Critique,
    Plan,
    PlanStep,
    RunRecord,
    BudgetUsed,
    Tradeoff,
    REQUIRED_PERSPECTIVES,
)


class TestZeusRequest:
    """Tests for ZeusRequest model."""

    def test_minimal_request(self):
        """Test creating a request with minimal fields."""
        request = ZeusRequest(prompt="Build something", mode="brief")
        assert request.prompt == "Build something"
        assert request.mode == "brief"
        assert request.constraints == []
        assert request.context is None

    def test_full_request(self):
        """Test creating a request with all fields."""
        request = ZeusRequest(
            prompt="Build a task manager",
            mode="solution",
            constraints=["Must be async", "No external deps"],
            context={"existing_system": "Legacy API"},
        )
        assert request.mode == "solution"
        assert len(request.constraints) == 2
        assert request.context["existing_system"] == "Legacy API"

    def test_invalid_mode(self):
        """Test that invalid mode raises error."""
        with pytest.raises(ValueError):
            ZeusRequest(prompt="Test", mode="invalid")


class TestNormalizedProblem:
    """Tests for NormalizedProblem model."""

    def test_create_normalized_problem(self):
        """Test creating a normalized problem."""
        problem = NormalizedProblem(
            problem_statement="Build a task manager",
            constraints=["Must be async"],
            output_spec="Design brief with requirements",
            context={"domain": "productivity"},
        )
        assert problem.problem_statement == "Build a task manager"
        assert "Must be async" in problem.constraints


class TestCandidate:
    """Tests for Candidate model."""

    def test_create_candidate(self):
        """Test creating a candidate."""
        candidate = Candidate(
            content="# Design Brief\n\nThis is the content.",
            assumptions=["Assume Python 3.11+"],
            uncertainty_flags=["Database choice unclear"],
        )
        assert "Design Brief" in candidate.content
        assert len(candidate.assumptions) == 1
        assert len(candidate.uncertainty_flags) == 1


class TestCritique:
    """Tests for Critique model."""

    def test_create_critique(self):
        """Test creating a critique."""
        critique = Critique(
            issues=[
                CritiqueIssue(
                    role="completeness",
                    severity="blocker",
                    description="Missing requirements section",
                    suggested_fix="Add requirements section",
                ),
                CritiqueIssue(
                    role="clarity",
                    severity="minor",
                    description="Some terms undefined",
                ),
            ],
            constraint_violations=["Async constraint not addressed"],
            missing_perspectives=["Security"],
        )
        assert len(critique.issues) == 2
        assert critique.issues[0].severity == "blocker"
        assert len(critique.constraint_violations) == 1


class TestRunRecord:
    """Tests for RunRecord model."""

    def test_has_blockers(self):
        """Test blocker detection."""
        record = RunRecord(
            mode="brief",
            request=ZeusRequest(prompt="Test", mode="brief"),
        )

        # No critique yet
        assert not record.has_blockers(None)

        # Critique with blocker
        critique_with_blocker = Critique(
            issues=[CritiqueIssue(
                role="test",
                severity="blocker",
                description="Test blocker",
            )]
        )
        assert record.has_blockers(critique_with_blocker)

        # Critique without blocker
        critique_minor = Critique(
            issues=[CritiqueIssue(
                role="test",
                severity="minor",
                description="Test minor",
            )]
        )
        assert not record.has_blockers(critique_minor)

    def test_needs_revision(self):
        """Test revision logic."""
        record = RunRecord(
            mode="brief",
            request=ZeusRequest(prompt="Test", mode="brief"),
        )

        # No critique, no revision needed
        assert not record.needs_revision()

        # Add blocker critique
        record.critique_v1 = Critique(
            issues=[CritiqueIssue(
                role="test",
                severity="blocker",
                description="Needs fix",
            )]
        )
        assert record.needs_revision()

        # After revision, no longer needs it
        record.candidate_v2 = Candidate(content="Revised content")
        assert not record.needs_revision()

    def test_can_revise(self):
        """Test revision budget."""
        record = RunRecord(
            mode="brief",
            request=ZeusRequest(prompt="Test", mode="brief"),
        )

        assert record.can_revise()
        record.budget_used.revisions = 1
        assert not record.can_revise()


class TestZeusResponse:
    """Tests for ZeusResponse model."""

    def test_response_invariants(self):
        """Test that response always has required fields."""
        response = ZeusResponse(
            output="# Output",
            assumptions=[],  # Empty but present
            known_issues=[],  # Empty but present
            run_id="test-123",
        )
        assert response.assumptions is not None
        assert response.known_issues is not None
        assert response.run_id == "test-123"

    def test_v1_evaluation_signals(self):
        """Test V1 evaluation signal fields."""
        response = ZeusResponse(
            output="# Output",
            run_id="test-123",
            confidence="high",
            coverage_score=0.83,
            covered_perspectives=["scope", "architecture", "risk", "security", "evaluation"],
            missing_perspectives=["compliance"],
            tradeoffs=[
                Tradeoff(
                    chose="SQLite",
                    over="PostgreSQL",
                    rationale="Simpler deployment",
                    impact="medium",
                )
            ],
        )
        assert response.confidence == "high"
        assert response.coverage_score == 0.83
        assert len(response.covered_perspectives) == 5
        assert "compliance" in response.missing_perspectives
        assert len(response.tradeoffs) == 1


class TestTradeoff:
    """Tests for Tradeoff model."""

    def test_create_tradeoff(self):
        """Test creating a tradeoff."""
        tradeoff = Tradeoff(
            chose="REST API",
            over="GraphQL",
            rationale="Team familiarity",
            impact="high",
        )
        assert tradeoff.chose == "REST API"
        assert tradeoff.over == "GraphQL"
        assert tradeoff.impact == "high"

    def test_tradeoff_defaults(self):
        """Test tradeoff default values."""
        tradeoff = Tradeoff(
            chose="Option A",
            over="Option B",
            rationale="Reason",
        )
        assert tradeoff.impact == "medium"  # Default


class TestCritiqueIssueCategory:
    """Tests for CritiqueIssue category field."""

    def test_issue_with_category(self):
        """Test creating an issue with category."""
        issue = CritiqueIssue(
            role="architecture",
            severity="major",
            category="maintainability",
            description="Tight coupling between components",
        )
        assert issue.category == "maintainability"

    def test_issue_default_category(self):
        """Test default category value."""
        issue = CritiqueIssue(
            role="scope",
            severity="minor",
            description="Minor scope gap",
        )
        assert issue.category == "completeness"  # Default


class TestRequiredPerspectives:
    """Tests for required perspectives constant."""

    def test_required_perspectives_count(self):
        """Test that we have 6 required perspectives."""
        assert len(REQUIRED_PERSPECTIVES) == 6

    def test_required_perspectives_content(self):
        """Test required perspective names."""
        expected = {"scope", "architecture", "risk", "security", "compliance", "evaluation"}
        assert REQUIRED_PERSPECTIVES == expected
