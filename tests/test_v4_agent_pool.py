"""Tests for V4 Agent Pool — Blackboard, SpecialistReviewer, Synthesizer.

Run with: pytest tests/test_v4_agent_pool.py -v
"""

import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.core.blackboard import Blackboard, BlackboardIssue, IssueStatus
from src.core.specialist_reviewer import SpecialistReviewer, SPECIALIST_PRIORITY
from src.models.schemas import (
    Candidate,
    Critique,
    CritiqueIssue,
    NormalizedProblem,
    SpecialistReview,
    SynthesisResult,
    AgentPoolResult,
)


# ============================================================================
# Helpers
# ============================================================================

def _make_candidate(content: str = "# Test Candidate\nSome content.") -> Candidate:
    return Candidate(
        content=content,
        assumptions=["Assumption 1"],
        uncertainty_flags=["Flag 1"],
    )


def _make_issue(
    role: str = "risk",
    severity: str = "major",
    description: str = "A test issue",
) -> CritiqueIssue:
    return CritiqueIssue(
        role=role,
        severity=severity,
        description=description,
    )


def _make_critique(*issues: CritiqueIssue) -> Critique:
    return Critique(
        issues=list(issues),
        constraint_violations=[],
        missing_perspectives=[],
    )


def _make_problem() -> NormalizedProblem:
    return NormalizedProblem(
        problem_statement="Design a cache system",
        constraints=["Must be thread-safe"],
        output_spec="Markdown architecture document",
    )


# ============================================================================
# Blackboard Tests
# ============================================================================

class TestBlackboard:
    """Tests for the V4 Blackboard shared state."""

    def test_blackboard_creation(self):
        """Blackboard initialises with candidate and empty issues."""
        board = Blackboard(candidate=_make_candidate())
        assert board.candidate is not None
        assert board.issues == []
        assert board.open_issues == []
        assert board.has_budget is True

    def test_add_issues_from_critique(self):
        """Issues imported from a Critique appear on the board."""
        board = Blackboard(candidate=_make_candidate())
        critique = _make_critique(
            _make_issue(severity="blocker"),
            _make_issue(severity="minor"),
        )
        board.add_issues_from_critique(critique, source="test_critic")

        assert len(board.issues) == 2
        assert len(board.open_issues) == 2
        assert len(board.open_blockers) == 1

    def test_mark_resolved(self):
        """Resolved issues are no longer in open_issues."""
        board = Blackboard(candidate=_make_candidate())
        critique = _make_critique(
            _make_issue(severity="blocker", description="Issue A"),
            _make_issue(severity="major", description="Issue B"),
        )
        board.add_issues_from_critique(critique)

        board.mark_resolved([0], specialist="risk_specialist", note="Fixed")

        assert len(board.open_issues) == 1
        assert board.issues[0].status == IssueStatus.RESOLVED
        assert board.issues[0].resolved_by == "risk_specialist"

    def test_budget_tracking(self):
        """Budget decrements correctly and has_budget flips when exhausted."""
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=2)

        assert board.has_budget is True
        board.use_specialist_call()
        assert board.has_budget is True
        board.use_specialist_call()
        assert board.has_budget is False

    def test_event_log_records_mutations(self):
        """Every mutation appends to the event log."""
        board = Blackboard(candidate=_make_candidate())
        critique = _make_critique(_make_issue())
        board.add_issues_from_critique(critique)
        board.use_specialist_call()
        board.mark_resolved([0], specialist="test", note="fixed")
        board.update_candidate(_make_candidate("# Updated"), "synthesizer")

        assert len(board.event_log) == 4

    def test_summary_snapshot(self):
        """Summary produces correct counts."""
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=3)
        critique = _make_critique(
            _make_issue(severity="blocker"),
            _make_issue(severity="major"),
            _make_issue(severity="minor"),
        )
        board.add_issues_from_critique(critique)
        board.mark_resolved([0], specialist="risk", note="fixed blocker")
        board.issues[2].defer("Not critical")
        board.use_specialist_call()

        summary = board.summary()
        assert summary["total_issues"] == 3
        assert summary["resolved"] == 1
        assert summary["deferred"] == 1
        assert summary["open"] == 1
        assert summary["specialist_calls_used"] == 1
        assert "risk" in summary["resolved_by_specialist"]

    def test_add_specialist_issues(self):
        """Specialist-discovered issues are added to the board."""
        board = Blackboard(candidate=_make_candidate())
        new_issues = [_make_issue(role="security", description="New sec issue")]
        board.add_specialist_issues(new_issues, specialist="security_ops")

        assert len(board.issues) == 1
        assert board.issues[0].issue.role == "security"

    def test_open_majors(self):
        """open_majors returns only unresolved major issues."""
        board = Blackboard(candidate=_make_candidate())
        critique = _make_critique(
            _make_issue(severity="blocker"),
            _make_issue(severity="major"),
            _make_issue(severity="minor"),
        )
        board.add_issues_from_critique(critique)

        assert len(board.open_majors) == 1
        assert board.open_majors[0].issue.severity == "major"


# ============================================================================
# Specialist Selection Tests
# ============================================================================

class TestSpecialistSelection:
    """Tests for specialist selection logic."""

    def test_select_with_blockers_runs_all(self):
        """When blockers exist, all specialists should be candidates."""
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=3)
        critique = _make_critique(_make_issue(severity="blocker"))
        board.add_issues_from_critique(critique)

        selected = SpecialistReviewer.select_specialists(board)
        assert len(selected) == 3
        assert selected == SPECIALIST_PRIORITY

    def test_select_respects_budget(self):
        """Selection is capped by remaining budget."""
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=1)
        critique = _make_critique(_make_issue(severity="blocker"))
        board.add_issues_from_critique(critique)

        selected = SpecialistReviewer.select_specialists(board)
        assert len(selected) == 1

    def test_select_no_budget_returns_empty(self):
        """No remaining budget → no specialists selected."""
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=0)
        critique = _make_critique(_make_issue(severity="blocker"))
        board.add_issues_from_critique(critique)

        selected = SpecialistReviewer.select_specialists(board)
        assert selected == []

    def test_select_by_domain(self):
        """Specialists are selected based on open issue domains."""
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=3)
        critique = _make_critique(
            _make_issue(role="risk", severity="major"),
        )
        board.add_issues_from_critique(critique)

        selected = SpecialistReviewer.select_specialists(board)
        assert "risk_compliance" in selected

    def test_select_fallback_with_unmatched_issues(self):
        """If no domain matches but issues exist, pick top-priority specialist."""
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=3)
        critique = _make_critique(
            _make_issue(role="unrecognized_domain", severity="major"),
        )
        board.add_issues_from_critique(critique)

        selected = SpecialistReviewer.select_specialists(board)
        assert len(selected) >= 1
        assert selected[0] == SPECIALIST_PRIORITY[0]


# ============================================================================
# Schema Tests
# ============================================================================

class TestV4Schemas:
    """Tests for V4 Pydantic models."""

    def test_specialist_review_creation(self):
        """SpecialistReview can be created with valid data."""
        review = SpecialistReview(
            specialist="risk_compliance",
            new_issues=[_make_issue()],
            resolved_issue_indices=[0, 1],
            resolution_notes="Fixed risk issues",
            fix_suggestions="Add monitoring",
        )
        assert review.specialist == "risk_compliance"
        assert len(review.new_issues) == 1
        assert len(review.resolved_issue_indices) == 2

    def test_synthesis_result_creation(self):
        """SynthesisResult can be created with a revised candidate."""
        result = SynthesisResult(
            revised_candidate=_make_candidate("# Revised content"),
            resolved_issue_indices=[0, 1, 2],
            resolution_notes="Addressed all blockers",
        )
        assert result.revised_candidate.content == "# Revised content"
        assert len(result.resolved_issue_indices) == 3

    def test_agent_pool_result_creation(self):
        """AgentPoolResult aggregates specialist reviews and synthesis."""
        review = SpecialistReview(
            specialist="security_ops",
            new_issues=[],
        )
        synthesis = SynthesisResult(
            revised_candidate=_make_candidate(),
            resolved_issue_indices=[],
        )
        result = AgentPoolResult(
            specialist_reviews=[review],
            synthesis=synthesis,
            blackboard_summary={"total_issues": 5, "resolved": 3},
            specialists_run=["security_ops"],
        )
        assert len(result.specialist_reviews) == 1
        assert result.synthesis is not None
        assert result.blackboard_summary["total_issues"] == 5

    def test_agent_pool_result_serialisation(self):
        """AgentPoolResult round-trips through JSON serialisation."""
        result = AgentPoolResult(
            specialist_reviews=[
                SpecialistReview(specialist="risk_compliance", new_issues=[]),
            ],
            specialists_run=["risk_compliance"],
            blackboard_summary={"open": 0},
        )
        data = result.model_dump()
        restored = AgentPoolResult.model_validate(data)
        assert restored.specialists_run == ["risk_compliance"]


# ============================================================================
# Integration-level: Blackboard → Selection → Parse flow
# ============================================================================

class TestBlackboardWorkflow:
    """End-to-end workflow tests without LLM calls."""

    def test_full_blackboard_lifecycle(self):
        """Simulate: critique → select specialists → add findings → resolve → synthesize."""
        # Step 1: Initialise board
        board = Blackboard(candidate=_make_candidate(), max_specialist_calls=3)

        # Step 2: Load initial critique
        initial_critique = _make_critique(
            _make_issue(role="risk", severity="blocker", description="No failover"),
            _make_issue(role="security", severity="major", description="No auth"),
            _make_issue(role="evaluation", severity="minor", description="Vague metrics"),
        )
        board.add_issues_from_critique(initial_critique, source="v1_critic")
        assert len(board.open_issues) == 3

        # Step 3: Select specialists
        selected = SpecialistReviewer.select_specialists(board)
        assert len(selected) == 3  # All run because blocker exists

        # Step 4: Simulate risk specialist findings
        board.use_specialist_call()
        board.add_specialist_issues(
            [_make_issue(role="compliance", severity="minor", description="Audit gap")],
            specialist="risk_compliance",
        )
        board.mark_resolved([0], specialist="risk_compliance", note="Added failover section")

        # Step 5: Simulate security specialist
        board.use_specialist_call()
        board.mark_resolved([1], specialist="security_ops", note="Added auth layer")

        # Step 6: Simulate evaluation specialist
        board.use_specialist_call()
        board.mark_resolved([2], specialist="evaluation_regression", note="Added metrics")

        assert not board.has_budget  # All calls used

        # Step 7: Simulate synthesis
        revised = _make_candidate("# Improved Candidate\nWith failover, auth, and metrics.")
        board.update_candidate(revised, source="synthesizer")

        # Verify final state
        summary = board.summary()
        assert summary["resolved"] == 3
        assert summary["open"] == 1  # The audit gap added by specialist
        assert summary["specialist_calls_used"] == 3
        assert board.candidate.content.startswith("# Improved Candidate")
