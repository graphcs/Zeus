#!/usr/bin/env python3
"""Test V2 Regression Logic.

Run with: python3 tests/test_v2_regression.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to ensure src can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.comparator import Comparator
from src.models.schemas import RunRecord, ZeusResponse, EvaluationSummary

def create_mock_record(run_id, cov, issues, blockers, majors, constraints=0):
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
                issues_by_category={}
            ).model_dump()
        )
    )

def test_regression_same_stats():
    """Test regression with identical stats (should be not worse)."""
    print("Testing regression with same stats...", end=" ")
    base = create_mock_record("base", 0.8, 5, 0, 1)
    curr = create_mock_record("curr", 0.8, 5, 0, 1)
    
    delta = Comparator.compare(curr, base)
    
    assert delta is not None
    assert delta.is_worse is False
    assert delta.coverage_delta == 0.0
    assert delta.issues_delta == 0
    assert delta.constraints_delta == 0
    assert delta.baseline_run_id == "base"
    print("OK")

def test_regression_worse_blocker():
    """Test regression when a blocker is introduced."""
    print("Testing regression with new blocker...", end=" ")
    base = create_mock_record("base", 0.8, 5, 0, 1)
    curr = create_mock_record("curr", 0.8, 6, 1, 1) # Added 1 blocker
    
    delta = Comparator.compare(curr, base)
    
    assert delta.is_worse is True
    assert delta.blocker_delta == 1
    print("OK")

def test_regression_worse_coverage():
    """Test regression when coverage drops significantly."""
    print("Testing regression with worse coverage...", end=" ")
    base = create_mock_record("base", 0.8, 5, 0, 1)
    curr = create_mock_record("curr", 0.6, 5, 0, 1) # Drop 0.2
    
    delta = Comparator.compare(curr, base)
    
    assert delta.is_worse is True
    assert delta.coverage_delta < -0.15
    print("OK")

def test_improvement():
    """Test improvement (stats get better)."""
    print("Testing improvement...", end=" ")
    base = create_mock_record("base", 0.8, 5, 1, 1, constraints=3)
    curr = create_mock_record("curr", 0.9, 3, 0, 0, constraints=1) # Less issues, more coverage
    
    delta = Comparator.compare(curr, base)
    
    assert delta.is_worse is False
    assert delta.coverage_delta >= 0.09  # float precision
    assert delta.issues_delta == -2
    assert delta.constraints_delta == -2
    assert delta.blocker_delta == -1
    print("OK")

if __name__ == "__main__":
    try:
        test_regression_same_stats()
        test_regression_worse_blocker()
        test_regression_worse_coverage()
        test_improvement()
        print("\n✅ All V2 Regression tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
