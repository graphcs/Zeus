"""Tests for Assembler V1 evaluation signals."""

import pytest
from zeus.models.schemas import (
    ZeusRequest,
    Candidate,
    CritiqueIssue,
    Critique,
    RunRecord,
    Tradeoff,
)
from zeus.core.assembler import Assembler


class TestConfidenceScoring:
    """Tests for confidence calculation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.assembler = Assembler()

    def test_no_critique_returns_medium(self):
        """Test that no critique returns medium confidence."""
        confidence = self.assembler._calculate_confidence(None)
        assert confidence == "medium"

    def test_blocker_returns_low(self):
        """Test that any blocker returns low confidence."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="blocker", description="Critical issue"),
            ]
        )
        confidence = self.assembler._calculate_confidence(critique)
        assert confidence == "low"

    def test_two_majors_returns_low(self):
        """Test that 2+ majors returns low confidence."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="major", description="Issue 1"),
                CritiqueIssue(role="architecture", severity="major", description="Issue 2"),
            ]
        )
        confidence = self.assembler._calculate_confidence(critique)
        assert confidence == "low"

    def test_one_major_returns_medium(self):
        """Test that 1 major returns medium confidence."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="major", description="Issue"),
            ]
        )
        confidence = self.assembler._calculate_confidence(critique)
        assert confidence == "medium"

    def test_three_minors_returns_medium(self):
        """Test that 3+ minors returns medium confidence."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="minor", description="Issue 1"),
                CritiqueIssue(role="architecture", severity="minor", description="Issue 2"),
                CritiqueIssue(role="risk", severity="minor", description="Issue 3"),
            ]
        )
        confidence = self.assembler._calculate_confidence(critique)
        assert confidence == "medium"

    def test_few_minors_returns_high(self):
        """Test that few minors returns high confidence."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="minor", description="Issue 1"),
                CritiqueIssue(role="architecture", severity="minor", description="Issue 2"),
            ]
        )
        confidence = self.assembler._calculate_confidence(critique)
        assert confidence == "high"

    def test_no_issues_returns_high(self):
        """Test that no issues returns high confidence."""
        critique = Critique(issues=[])
        confidence = self.assembler._calculate_confidence(critique)
        assert confidence == "high"


class TestCoverageCalculation:
    """Tests for coverage calculation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.assembler = Assembler()

    def test_no_critique_returns_zero(self):
        """Test that no critique returns zero coverage."""
        score, covered, missing = self.assembler._calculate_coverage(None)
        assert score == 0.0
        assert covered == []
        assert len(missing) == 6

    def test_full_coverage(self):
        """Test full perspective coverage."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="minor", description="Scope ok"),
                CritiqueIssue(role="architecture", severity="minor", description="Arch ok"),
                CritiqueIssue(role="risk", severity="minor", description="Risk ok"),
                CritiqueIssue(role="security", severity="minor", description="Security ok"),
                CritiqueIssue(role="compliance", severity="minor", description="Compliance ok"),
                CritiqueIssue(role="evaluation", severity="minor", description="Eval ok"),
            ]
        )
        score, covered, missing = self.assembler._calculate_coverage(critique)
        assert score == 1.0
        assert len(covered) == 6
        assert len(missing) == 0

    def test_partial_coverage(self):
        """Test partial perspective coverage."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="minor", description="Scope ok"),
                CritiqueIssue(role="architecture", severity="minor", description="Arch ok"),
                CritiqueIssue(role="risk", severity="minor", description="Risk ok"),
            ]
        )
        score, covered, missing = self.assembler._calculate_coverage(critique)
        assert score == 0.5  # 3/6
        assert len(covered) == 3
        assert len(missing) == 3

    def test_perspective_alias_normalization(self):
        """Test that perspective aliases are normalized."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="completeness", severity="minor", description="Maps to scope"),
                CritiqueIssue(role="structural", severity="minor", description="Maps to architecture"),
            ]
        )
        score, covered, missing = self.assembler._calculate_coverage(critique)
        assert "scope" in covered  # completeness -> scope
        assert "architecture" in covered  # structural -> architecture


class TestIssueCounts:
    """Tests for issue count calculation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.assembler = Assembler()

    def test_no_critique_returns_zeros(self):
        """Test that no critique returns zero counts."""
        counts = self.assembler._calculate_issue_counts(None)
        assert counts == {"blockers": 0, "majors": 0, "minors": 0}

    def test_counts_by_severity(self):
        """Test counting issues by severity."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="blocker", description="Blocker 1"),
                CritiqueIssue(role="arch", severity="blocker", description="Blocker 2"),
                CritiqueIssue(role="risk", severity="major", description="Major 1"),
                CritiqueIssue(role="security", severity="minor", description="Minor 1"),
                CritiqueIssue(role="eval", severity="minor", description="Minor 2"),
            ]
        )
        counts = self.assembler._calculate_issue_counts(critique)
        assert counts == {"blockers": 2, "majors": 1, "minors": 2}


class TestIssuesByCategory:
    """Tests for issue grouping by category."""

    def setup_method(self):
        """Set up test fixtures."""
        self.assembler = Assembler()

    def test_no_critique_returns_empty(self):
        """Test that no critique returns empty dict."""
        grouped = self.assembler._group_issues_by_category(None)
        assert grouped == {}

    def test_groups_by_category(self):
        """Test grouping issues by category."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="major", category="completeness", description="Missing section"),
                CritiqueIssue(role="scope", severity="minor", category="completeness", description="Vague wording"),
                CritiqueIssue(role="arch", severity="major", category="maintainability", description="Tight coupling"),
            ]
        )
        grouped = self.assembler._group_issues_by_category(critique)

        assert "completeness" in grouped
        assert len(grouped["completeness"]) == 2
        assert "maintainability" in grouped
        assert len(grouped["maintainability"]) == 1

    def test_excludes_blockers(self):
        """Test that blockers are excluded from grouping."""
        critique = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="blocker", category="correctness", description="Critical error"),
                CritiqueIssue(role="scope", severity="minor", category="clarity", description="Minor issue"),
            ]
        )
        grouped = self.assembler._group_issues_by_category(critique)

        # Blocker should not appear
        assert "correctness" not in grouped
        # Minor should appear
        assert "clarity" in grouped


class TestAssemblerIntegration:
    """Integration tests for Assembler."""

    def setup_method(self):
        """Set up test fixtures."""
        self.assembler = Assembler()

    def test_assemble_includes_v1_fields(self):
        """Test that assembled response includes V1 fields."""
        record = RunRecord(
            mode="brief",
            request=ZeusRequest(prompt="Test", mode="brief"),
        )
        record.candidate_v1 = Candidate(
            content="# Test Brief",
            assumptions=["Assumption 1"],
            tradeoffs=[
                Tradeoff(
                    chose="Option A",
                    over="Option B",
                    rationale="Better fit",
                    impact="medium",
                )
            ],
        )
        record.critique_v1 = Critique(
            issues=[
                CritiqueIssue(role="scope", severity="minor", description="Ok"),
                CritiqueIssue(role="architecture", severity="minor", description="Ok"),
            ]
        )

        response = self.assembler.assemble(record)

        # Check V1 fields are populated
        assert response.confidence in ("low", "medium", "high")
        assert 0.0 <= response.coverage_score <= 1.0
        assert isinstance(response.covered_perspectives, list)
        assert isinstance(response.missing_perspectives, list)
        assert len(response.tradeoffs) == 1
        assert response.tradeoffs[0].chose == "Option A"

        # Check issue counts and category grouping
        assert isinstance(response.issue_counts, dict)
        assert "blockers" in response.issue_counts
        assert "majors" in response.issue_counts
        assert "minors" in response.issue_counts
        assert isinstance(response.issues_by_category, dict)

    def test_assemble_error_case_has_v1_fields(self):
        """Test that error response still has V1 fields."""
        record = RunRecord(
            mode="brief",
            request=ZeusRequest(prompt="Test", mode="brief"),
        )
        record.errors.append("Generation failed")

        response = self.assembler.assemble(record)

        # Even error response should have V1 fields
        assert response.confidence == "low"
        assert response.coverage_score == 0.0
        assert response.tradeoffs == []
        assert response.issue_counts == {"blockers": 0, "majors": 0, "minors": 0}
        assert response.issues_by_category == {}
