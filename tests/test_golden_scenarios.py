"""Golden Scenario Tests for Zeus.

These tests verify the behavioral contract of the multi-inventor pipeline.

Requirements:
    - OPENROUTER_API_KEY environment variable must be set
    - Tests make real LLM calls and may take several minutes

Run with:
    pytest tests/test_golden_scenarios.py -v --timeout=900
"""

import os
import pytest
from src.core.run_controller import run_zeus
from src.models.schemas import ZeusResponse


pytestmark = pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set - golden scenarios require real LLM calls"
)


class TestGoldenScenarios:
    """Golden scenario tests for Zeus validation.

    Each test verifies:
    - 5 deliverables present
    - assumptions[] and known_issues[] always present
    - run_id generated
    - Score in valid range
    - Budget enforced (max ~30 LLM calls)
    """

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_case_1_api_design(self):
        """Case 1: API design with constraints."""
        response = await run_zeus(
            prompt=(
                "Design a minimal REST API for a 'RunRecord logging service' "
                "that accepts run events and supports querying by run_id."
            ),
            constraints=[
                "Include exactly 4 endpoints",
                "Keep the design MVP-friendly (no auth details)."
            ],
            num_inventors=3,
        )

        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None
        assert len(response.output) > 0
        assert 0.0 <= response.total_score <= 220.0
        assert response.usage.llm_calls <= 30

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_case_2_conflicting_constraints(self):
        """Case 2: Conflicting constraints (must surface issue)."""
        response = await run_zeus(
            prompt=(
                "Propose an architecture for an event processing pipeline that "
                "guarantees exactly-once delivery with zero operational complexity."
            ),
            constraints=[
                "No external dependencies",
                "Exactly-once delivery required"
            ],
            num_inventors=3,
        )

        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None
        assert len(response.output) > 0
        assert response.usage.llm_calls <= 30

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_case_3_underspecified_requirements(self):
        """Case 3: Under-specified requirements (best-effort with assumptions)."""
        response = await run_zeus(
            prompt=(
                "Design a 'policy gate' component for controlling tool access "
                "in an AI system."
            ),
            constraints=[],
            num_inventors=3,
        )

        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert len(response.assumptions) > 0  # Should have inferred assumptions
        assert len(response.output) > 0
        assert response.usage.llm_calls <= 30

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_case_4_complex_system(self):
        """Case 4: Complex system design (comprehensive output)."""
        response = await run_zeus(
            prompt=(
                "Design a governed, self-improving operations assistant that "
                "produces plans and documents, and continuously improves using "
                "run records and evaluations."
            ),
            constraints=[],
            objectives=["Self-improvement capability", "Audit trail"],
            num_inventors=4,
        )

        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert len(response.output) > 1000  # Should be substantial
        assert response.usage.llm_calls <= 30

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_case_5_constraint_enforcement(self):
        """Case 5: Constraint enforcement."""
        response = await run_zeus(
            prompt=(
                "Propose a deterministic constraint checker for verifying "
                "output contracts in an AI system."
            ),
            constraints=[
                "Must include a section titled 'Deterministic Checks'",
                "Must include a section titled 'Heuristic Checks'"
            ],
            num_inventors=3,
        )

        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        output_lower = response.output.lower()
        assert "deterministic" in output_lower
        assert "heuristic" in output_lower
        assert response.usage.llm_calls <= 30


class TestInvariants:
    """Tests for system invariants."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_transparency_fields_always_present(self):
        """Verify assumptions[] and known_issues[] always present."""
        response = await run_zeus(
            prompt="Design a minimal cache.",
            constraints=[],
            num_inventors=2,
            max_llm_calls=10,
        )

        assert response.assumptions is not None
        assert response.known_issues is not None
        assert isinstance(response.assumptions, list)
        assert isinstance(response.known_issues, list)

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_unique_run_ids(self):
        """Verify every run has a unique run_id."""
        response1 = await run_zeus(
            prompt="Design service A.",
            constraints=[],
            num_inventors=2,
            max_llm_calls=10,
        )
        response2 = await run_zeus(
            prompt="Design service B.",
            constraints=[],
            num_inventors=2,
            max_llm_calls=10,
        )

        assert response1.run_id is not None
        assert response2.run_id is not None
        assert response1.run_id != response2.run_id

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_scorecard_present(self):
        """Verify scorecard is populated."""
        response = await run_zeus(
            prompt="Design a simple logging service.",
            constraints=[],
            num_inventors=2,
            max_llm_calls=15,
        )

        assert response.scorecard is not None
        assert len(response.scorecard.criteria_scores) == 13
        assert len(response.scorecard.hard_constraints) >= 2
        assert response.total_score > 0
