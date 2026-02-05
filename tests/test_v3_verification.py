#!/usr/bin/env python3
"""Test V3 Verification, Completeness, and Structuring Logic.

Run with: python3 tests/test_v3_verification.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to ensure src can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.constraint_checker import ConstraintChecker
from src.core.evaluator import CompletenessChecker, BRIEF_REQUIRED_SECTIONS, SOLUTION_REQUIRED_SECTIONS
from src.core.comparator import Comparator
from src.models.schemas import (
    ConstraintCheckResult,
    VerificationReport,
    StructuredKnownIssue,
    RunRecord,
    ZeusResponse,
    EvaluationSummary,
)

# ============================================================================
# Deterministic Constraint Checker Tests
# ============================================================================

def test_deterministic_section_check():
    """Constraint 'must include Risk section', content has ## Risk → pass."""
    print("Testing deterministic section check (present)...", end=" ")
    content = "# Overview\nSome text\n## Risk\nRisk details here\n## Scope\nScope details"
    constraint = "Must include Risk section"
    result = ConstraintChecker._check_deterministic(content, constraint)

    assert result is not None
    assert result.status == "pass"
    assert "found" in result.evidence
    print("OK")


def test_deterministic_section_missing():
    """Constraint 'must include Risk section', content lacks it → fail."""
    print("Testing deterministic section check (missing)...", end=" ")
    content = "# Overview\nSome text\n## Scope\nScope details"
    constraint = "Must include Risk section"
    result = ConstraintChecker._check_deterministic(content, constraint)

    assert result is not None
    assert result.status == "fail"
    assert "not found" in result.evidence
    print("OK")


def test_deterministic_keyword_check():
    """Constraint 'must address scalability' → pass when keyword present."""
    print("Testing deterministic keyword check (present)...", end=" ")
    content = "This design addresses scalability through horizontal sharding."
    constraint = "must address scalability"
    result = ConstraintChecker._check_deterministic(content, constraint)

    assert result is not None
    assert result.status == "pass"
    print("OK")


def test_deterministic_keyword_missing():
    """Constraint 'must mention caching' → fail when keyword absent."""
    print("Testing deterministic keyword check (missing)...", end=" ")
    content = "This design uses a simple database layer."
    constraint = "must mention caching"
    result = ConstraintChecker._check_deterministic(content, constraint)

    assert result is not None
    assert result.status == "fail"
    print("OK")


def test_deterministic_word_count_pass():
    """Constraint 'must be under 100 words' → pass with short content."""
    print("Testing deterministic word count (pass)...", end=" ")
    content = "This is a short document with only a few words."
    constraint = "must be under 100 words"
    result = ConstraintChecker._check_deterministic(content, constraint)

    assert result is not None
    assert result.status == "pass"
    assert "Word count" in result.evidence
    print("OK")


def test_deterministic_word_count_fail():
    """Constraint 'must be under 10 words' → fail with longer content."""
    print("Testing deterministic word count (fail)...", end=" ")
    content = "This is a document that has way more than ten words in it for sure."
    constraint = "must be under 10 words"
    result = ConstraintChecker._check_deterministic(content, constraint)

    assert result is not None
    assert result.status == "fail"
    print("OK")


def test_semantic_constraint_passthrough():
    """Constraint 'must be async-first' → returns None (falls through to LLM)."""
    print("Testing semantic constraint passthrough...", end=" ")
    content = "Some content about architecture."
    constraint = "must be async-first"
    result = ConstraintChecker._check_deterministic(content, constraint)

    assert result is None
    print("OK")


# ============================================================================
# Completeness Checker Tests
# ============================================================================

def test_brief_completeness_full():
    """Content with all 10 brief sections → score 1.0."""
    print("Testing brief completeness (full)...", end=" ")
    sections = BRIEF_REQUIRED_SECTIONS
    content = "\n".join(f"## {s.title()}\nContent for {s}." for s in sections)
    score, missing = CompletenessChecker.check(content, "brief")

    assert score == 1.0, f"Expected 1.0, got {score}"
    assert missing == [], f"Expected no missing, got {missing}"
    print("OK")


def test_brief_completeness_partial():
    """Content missing 3 sections → correct score and missing list."""
    print("Testing brief completeness (partial)...", end=" ")
    # Use all sections except the last 3
    present = BRIEF_REQUIRED_SECTIONS[:-3]
    dropped = BRIEF_REQUIRED_SECTIONS[-3:]
    content = "\n".join(f"## {s.title()}\nContent for {s}." for s in present)
    score, missing = CompletenessChecker.check(content, "brief")

    expected_score = len(present) / len(BRIEF_REQUIRED_SECTIONS)
    assert abs(score - expected_score) < 0.01, f"Expected {expected_score}, got {score}"
    assert len(missing) == 3, f"Expected 3 missing, got {len(missing)}"
    for d in dropped:
        assert d in missing, f"Expected '{d}' in missing list"
    print("OK")


def test_solution_completeness():
    """Content with all solution sections → score 1.0."""
    print("Testing solution completeness (full)...", end=" ")
    sections = SOLUTION_REQUIRED_SECTIONS
    content = "\n".join(f"## {s.title()}\nContent for {s}." for s in sections)
    score, missing = CompletenessChecker.check(content, "solution")

    assert score == 1.0, f"Expected 1.0, got {score}"
    assert missing == [], f"Expected no missing, got {missing}"
    print("OK")


# ============================================================================
# Schema Tests
# ============================================================================

def test_structured_issue_schema():
    """StructuredKnownIssue creation with all fields."""
    print("Testing StructuredKnownIssue schema...", end=" ")
    issue = StructuredKnownIssue(
        issue="Database may hit connection limit under load",
        impact="Service degradation during peak traffic",
        mitigation="Implement connection pooling with max 50 connections",
        verification_step="Load test with 100 concurrent users",
    )
    assert issue.issue == "Database may hit connection limit under load"
    assert issue.impact == "Service degradation during peak traffic"
    assert issue.mitigation == "Implement connection pooling with max 50 connections"
    assert issue.verification_step == "Load test with 100 concurrent users"
    print("OK")


def test_verification_report_schema():
    """VerificationReport with checks and score."""
    print("Testing VerificationReport schema...", end=" ")
    checks = [
        ConstraintCheckResult(constraint="must use REST", status="pass", evidence="REST endpoints found"),
        ConstraintCheckResult(constraint="must support pagination", status="fail", evidence="No pagination found"),
        ConstraintCheckResult(constraint="should be fast", status="unverified", evidence=None),
    ]
    report = VerificationReport(checks=checks, coverage_score=2 / 3)

    assert len(report.checks) == 3
    assert report.checks[0].status == "pass"
    assert report.checks[1].status == "fail"
    assert report.checks[2].status == "unverified"
    assert abs(report.coverage_score - 2 / 3) < 0.01
    print("OK")


# ============================================================================
# Regression with Completeness Tests
# ============================================================================

def _create_mock_record(run_id, cov, issues, blockers, majors, completeness=0.8, constraints=0):
    """Helper to create a mock run record with evaluation stats."""
    return RunRecord(
        mode="brief",
        request={"prompt": "test", "mode": "brief"},
        run_id=run_id,
        timestamp=datetime.utcnow().isoformat(),
        final_response=ZeusResponse(
            output="test",
            run_id=run_id,
            evaluation_summary=EvaluationSummary(
                confidence="medium",
                coverage_score=cov,
                total_issues=issues,
                blockers=blockers,
                majors=majors,
                minors=issues - blockers - majors,
                constraint_violations=constraints,
                missing_perspectives=[],
                covered_perspectives=[],
                issues_by_category={},
                completeness_score=completeness,
                missing_sections=[],
            ).model_dump()
        )
    )


def test_regression_completeness_drop():
    """Completeness drops significantly → is_worse."""
    print("Testing regression with completeness drop...", end=" ")
    base = _create_mock_record("base", 0.8, 5, 0, 1, completeness=0.9)
    curr = _create_mock_record("curr", 0.8, 5, 0, 1, completeness=0.5)  # Drop 0.4

    delta = Comparator.compare(curr, base)

    assert delta is not None
    assert delta.is_worse is True
    assert delta.completeness_delta < -0.2
    print("OK")


def test_regression_completeness_stable():
    """Completeness stays same → not worse (all else equal)."""
    print("Testing regression with stable completeness...", end=" ")
    base = _create_mock_record("base", 0.8, 5, 0, 1, completeness=0.8)
    curr = _create_mock_record("curr", 0.8, 5, 0, 1, completeness=0.8)

    delta = Comparator.compare(curr, base)

    assert delta is not None
    assert delta.is_worse is False
    assert delta.completeness_delta == 0.0
    print("OK")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    try:
        # Deterministic constraint checker tests
        test_deterministic_section_check()
        test_deterministic_section_missing()
        test_deterministic_keyword_check()
        test_deterministic_keyword_missing()
        test_deterministic_word_count_pass()
        test_deterministic_word_count_fail()
        test_semantic_constraint_passthrough()

        # Completeness checker tests
        test_brief_completeness_full()
        test_brief_completeness_partial()
        test_solution_completeness()

        # Schema tests
        test_structured_issue_schema()
        test_verification_report_schema()

        # Regression with completeness tests
        test_regression_completeness_drop()
        test_regression_completeness_stable()

        print("\n✅ All V3 Verification tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
