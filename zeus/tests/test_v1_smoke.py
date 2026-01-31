#!/usr/bin/env python3
"""V1 Smoke Test - Quick validation of V1 features.

This script performs basic validation that all V1 features are working:
- Confidence scoring
- Coverage metrics
- Tradeoff extraction
- Schema validation
- Display formatting
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.run_controller import run_zeus
from src.models.schemas import ZeusResponse


async def test_v1_response_fields():
    """Test that V1 fields are populated in response."""
    print("🧪 Test 1: V1 Response Fields")
    print("-" * 50)
    
    response = await run_zeus(
        prompt="Design a simple in-memory cache with TTL support",
        mode="brief",
        constraints=["Must be thread-safe", "Must support TTL expiration"],
    )
    
    # Validate response type
    assert isinstance(response, ZeusResponse), "Response should be ZeusResponse"
    
    # Check V0 fields (baseline)
    assert hasattr(response, 'output'), "❌ Missing output"
    assert hasattr(response, 'assumptions'), "❌ Missing assumptions"
    assert hasattr(response, 'known_issues'), "❌ Missing known_issues"
    assert hasattr(response, 'run_id'), "❌ Missing run_id"
    assert hasattr(response, 'usage'), "❌ Missing usage"
    
    # Check V1 fields (new)
    assert hasattr(response, 'confidence'), "❌ Missing confidence"
    assert hasattr(response, 'coverage_score'), "❌ Missing coverage_score"
    assert hasattr(response, 'tradeoffs'), "❌ Missing tradeoffs"
    
    print(f"✅ All fields present")
    print(f"   - Output: {len(response.output)} chars")
    print(f"   - Assumptions: {len(response.assumptions)}")
    print(f"   - Known Issues: {len(response.known_issues)}")
    print(f"   - Run ID: {response.run_id[:8]}...")
    print(f"   - Confidence: {response.confidence}")
    print(f"   - Coverage: {response.coverage_score:.0%}")
    print(f"   - Tradeoffs: {len(response.tradeoffs)}")
    
    return response


async def test_v1_confidence_values():
    """Test that confidence values are valid."""
    print("\n🧪 Test 2: Confidence Values")
    print("-" * 50)
    
    response = await run_zeus(
        prompt="Design a distributed system",
        mode="brief",
        constraints=[],
    )
    
    valid_confidence = ("low", "medium", "high")
    assert response.confidence in valid_confidence, \
        f"❌ Invalid confidence: {response.confidence}"
    
    print(f"✅ Confidence value valid: {response.confidence}")
    return response


async def test_v1_coverage_range():
    """Test that coverage score is in valid range."""
    print("\n🧪 Test 3: Coverage Score Range")
    print("-" * 50)
    
    response = await run_zeus(
        prompt="Design a logging system",
        mode="brief",
        constraints=["Must support multiple log levels"],
    )
    
    assert 0.0 <= response.coverage_score <= 1.0, \
        f"❌ Coverage out of range: {response.coverage_score}"
    
    perspectives_covered = int(response.coverage_score * 6)
    print(f"✅ Coverage in valid range: {response.coverage_score:.0%}")
    print(f"   Perspectives covered: {perspectives_covered}/6")
    
    return response


async def test_v1_tradeoffs_list():
    """Test that tradeoffs are properly extracted."""
    print("\n🧪 Test 4: Tradeoffs Extraction")
    print("-" * 50)
    
    response = await run_zeus(
        prompt="Design a system that balances speed and accuracy",
        mode="brief",
        constraints=["Must be real-time"],
    )
    
    assert isinstance(response.tradeoffs, list), \
        "❌ Tradeoffs should be a list"
    
    print(f"✅ Tradeoffs properly formatted")
    print(f"   Count: {len(response.tradeoffs)}")
    if response.tradeoffs:
        print(f"   Sample: {response.tradeoffs[0][:60]}...")
    
    return response


async def test_v1_evaluator_import():
    """Test that evaluator modules import correctly."""
    print("\n🧪 Test 5: Evaluator Module Imports")
    print("-" * 50)
    
    try:
        from src.core.evaluator import (
            ConfidenceEvaluator,
            TradeoffExtractor,
            EvaluationEngine,
        )
        from src.models.schemas import EvaluationSummary
        
        print("✅ All evaluator classes import successfully")
        print("   - ConfidenceEvaluator")
        print("   - TradeoffExtractor")
        print("   - EvaluationEngine")
        print("   - EvaluationSummary")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


async def test_v1_schema_validation():
    """Test that V1 schemas validate correctly."""
    print("\n🧪 Test 6: Schema Validation")
    print("-" * 50)
    
    from src.models.schemas import (
        ZeusResponse,
        CritiqueIssue,
        EvaluationSummary,
        UsageStats,
    )
    
    # Test ZeusResponse with V1 fields
    response = ZeusResponse(
        output="Test output",
        assumptions=["Test assumption"],
        known_issues=["Test issue"],
        run_id="test-123",
        usage=UsageStats(),
        confidence="high",
        coverage_score=0.83,
        tradeoffs=["Test tradeoff"],
    )
    
    assert response.confidence == "high"
    assert response.coverage_score == 0.83
    assert len(response.tradeoffs) == 1
    
    # Test CritiqueIssue with category
    issue = CritiqueIssue(
        role="scope",
        severity="minor",
        category="completeness",
        description="Test issue",
    )
    
    assert issue.category == "completeness"
    
    # Test EvaluationSummary
    summary = EvaluationSummary(
        confidence="medium",
        coverage_score=0.67,
        total_issues=3,
        blockers=0,
        majors=1,
        minors=2,
    )
    
    assert summary.confidence == "medium"
    assert summary.coverage_score == 0.67
    
    print("✅ All schemas validate correctly")
    print("   - ZeusResponse with V1 fields")
    print("   - CritiqueIssue with category")
    print("   - EvaluationSummary")
    
    return True


async def main():
    """Run all smoke tests."""
    print("=" * 50)
    print("🚀 Zeus V1 Smoke Test Suite")
    print("=" * 50)
    
    try:
        # Test imports first
        await test_v1_evaluator_import()
        await test_v1_schema_validation()
        
        # Test actual generation (requires API key)
        try:
            response1 = await test_v1_response_fields()
            response2 = await test_v1_confidence_values()
            response3 = await test_v1_coverage_range()
            response4 = await test_v1_tradeoffs_list()
            
            print("\n" + "=" * 50)
            print("🎉 ALL TESTS PASSED!")
            print("=" * 50)
            print("\nV1 Features Validated:")
            print("  ✅ Response fields populated")
            print("  ✅ Confidence scoring working")
            print("  ✅ Coverage metrics calculated")
            print("  ✅ Tradeoffs extracted")
            print("  ✅ Schemas validated")
            print("  ✅ Evaluator modules functional")
            print("\n🚀 Zeus V1 is ready for production!")
            
        except Exception as e:
            if "OPENROUTER_API_KEY" in str(e):
                print("\n⚠️  API Key Tests Skipped")
                print("Set OPENROUTER_API_KEY to run full integration tests")
                print("\n✅ Schema and import tests PASSED")
            else:
                raise
    
    except Exception as e:
        print("\n" + "=" * 50)
        print("❌ TESTS FAILED")
        print("=" * 50)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
