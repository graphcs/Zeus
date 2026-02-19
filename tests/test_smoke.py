"""Smoke Test - Quick validation that the pipeline works end-to-end.

Requires OPENROUTER_API_KEY to run actual LLM calls.

Run with:
    pytest tests/test_smoke.py -v
"""

import os
import pytest
from src.core.run_controller import run_zeus
from src.models.schemas import ZeusResponse


pytestmark = pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set - smoke tests require real LLM calls"
)


class TestSmoke:
    """Smoke tests for the Zeus multi-inventor pipeline."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_basic_solve(self):
        """Test a basic solve produces 5 deliverables and valid score."""
        response = await run_zeus(
            prompt="Design a simple in-memory cache with TTL support",
            constraints=["Must be thread-safe", "Must support TTL expiration"],
            num_inventors=2,  # Fewer inventors for speed
            max_llm_calls=15,
        )

        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.output is not None
        assert len(response.output) > 0

        # 5 deliverables present
        assert response.executive_summary is not None
        assert response.solution_design_document is not None
        assert response.foundation_documentation is not None
        assert response.self_evaluation_scorecard is not None
        assert response.run_log is not None

        # Score in valid range
        assert 0.0 <= response.total_score <= 220.0
        assert 0.0 <= response.score_percentage <= 100.0

        # Invariants
        assert response.assumptions is not None
        assert response.known_issues is not None
        assert isinstance(response.assumptions, list)
        assert isinstance(response.known_issues, list)

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_with_objectives(self):
        """Test solving with objectives provided."""
        response = await run_zeus(
            prompt="Design a REST API for a task management system",
            constraints=["Must use async"],
            objectives=["High availability", "Low latency"],
            num_inventors=2,
            max_llm_calls=15,
        )

        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert len(response.output) > 0
        assert response.total_score >= 0.0

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_budget_enforcement(self):
        """Verify budget is enforced."""
        response = await run_zeus(
            prompt="Design a complex distributed system.",
            constraints=["Must be detailed"],
            num_inventors=2,
            max_llm_calls=10,
        )

        assert response.usage.llm_calls <= 10
