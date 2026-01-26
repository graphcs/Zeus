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
