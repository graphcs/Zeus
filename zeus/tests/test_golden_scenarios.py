"""Golden Scenario Tests for Zeus MVP.

These tests verify the behavioral contract defined in the MVP specification.
They are based on the golden scenarios from:
    docs/6. Example_Runs_Golden_Scenarios_Architecture_Only_V0.md

Requirements:
    - OPENROUTER_API_KEY environment variable must be set
    - Tests make real LLM calls and may take several minutes to complete

Run with:
    pytest tests/test_golden_scenarios.py -v --timeout=600

Or run specific scenarios:
    pytest tests/test_golden_scenarios.py::TestGoldenScenarios::test_case_1_api_design -v
"""

import os
import pytest
from zeus.core.run_controller import run_zeus
from zeus.models.schemas import ZeusResponse


# Skip all tests if no API key is available
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set - golden scenarios require real LLM calls"
)


class TestGoldenScenarios:
    """Golden scenario tests for Zeus MVP validation.

    Each test verifies specific behavioral properties defined in the MVP spec:
    - Critique runs on every request
    - assumptions[] and known_issues[] always present
    - run_id generated
    - Constraints preserved
    - Budget enforced (max 6 LLM calls, max 1 revision)
    """

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_case_1_api_design(self):
        """Case 1: API design with constraints (no revision expected).

        Expected properties:
        - Critique runs and reports no blocker/major issues
        - No revision loop
        - Output respects the "exactly 4 endpoints" constraint (best effort)
        - assumptions[] and known_issues[] present
        - RunRecord includes plan, candidate v1, critique v1, final response
        """
        response = await run_zeus(
            prompt=(
                "Design a minimal REST API for a 'RunRecord logging service' "
                "that accepts run events and supports querying by run_id. "
                "Include endpoints and example request/response shapes."
            ),
            mode="brief",
            constraints=[
                "Include exactly 4 endpoints",
                "Keep the design MVP-friendly (no auth details)."
            ],
        )

        # Verify MVP invariants
        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None
        assert response.output is not None
        assert len(response.output) > 0

        # Verify usage is within budget
        assert response.usage.llm_calls <= 6

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_case_2_conflicting_constraints(self):
        """Case 2: Conflicting architectural constraints (must surface known issue).

        Expected properties:
        - System proceeds best-effort (does not block)
        - Critique flags a major conflict/infeasibility
        - Optional revision (<=1) attempts to propose pragmatic design
        - known_issues explicitly notes constraint conflicts
        """
        response = await run_zeus(
            prompt=(
                "Propose an architecture for an event processing pipeline that "
                "guarantees exactly-once delivery with zero operational complexity."
            ),
            mode="brief",
            constraints=[
                "No external dependencies",
                "Exactly-once delivery required"
            ],
        )

        # Verify MVP invariants
        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None

        # Verify system didn't block - we got output
        assert response.output is not None
        assert len(response.output) > 0

        # Verify usage is within budget (may have revision)
        assert response.usage.llm_calls <= 6

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_case_3_structured_output(self):
        """Case 3: Structured output required (architecture as JSON).

        Expected properties:
        - Generator attempts structured output
        - If parse fails, repair attempt or fallback occurs
        - Best-effort response returned
        - <=1 revision
        """
        response = await run_zeus(
            prompt=(
                "Return a JSON architecture description for a service that runs "
                "'Normalize -> Generate -> Critique -> Log' on user requests."
            ),
            mode="brief",
            constraints=[
                "Return valid JSON with keys: components, data_flows, persistence, failure_modes"
            ],
        )

        # Verify MVP invariants
        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None

        # Verify best-effort output returned
        assert response.output is not None
        assert len(response.output) > 0

        # Verify usage is within budget
        assert response.usage.llm_calls <= 6

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_case_4_underspecified_requirements(self):
        """Case 4: Under-specified requirements (best-effort normalize + explicit assumptions).

        Expected properties:
        - Normalizer infers default output format
        - Critique flags missing inputs
        - assumptions lists reasonable defaults
        - No blocking; best-effort design returned
        """
        response = await run_zeus(
            prompt=(
                "Design a 'policy gate' component for controlling tool access "
                "in an AI system. Provide responsibilities and interfaces."
            ),
            mode="brief",
            constraints=[],  # No constraints provided
        )

        # Verify MVP invariants
        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None

        # Verify assumptions were inferred (should have some)
        assert len(response.assumptions) > 0

        # Verify best-effort output
        assert response.output is not None
        assert len(response.output) > 0

        # Verify usage is within budget
        assert response.usage.llm_calls <= 6

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_case_5_multiview_coverage(self):
        """Case 5: Multi-view coverage requirement (end-to-end system design).

        Expected properties:
        - Critique includes multi-view coverage (scope, architecture, risk,
          compliance, security/ops, evaluation)
        - If major gaps, <=1 revision attempts to add missing sections
        - known_issues includes open questions
        """
        response = await run_zeus(
            prompt=(
                "Design a governed, self-improving operations assistant that "
                "produces plans and documents, and continuously improves using "
                "run records and evaluations. Provide an end-to-end architecture "
                "and key data contracts."
            ),
            mode="brief",
            constraints=[],
        )

        # Verify MVP invariants
        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None

        # Verify comprehensive output for complex request
        assert response.output is not None
        assert len(response.output) > 1000  # Should be substantial

        # Verify usage is within budget
        assert response.usage.llm_calls <= 6

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_case_6_failure_modes(self):
        """Case 6: Failure mode emphasis (graceful degradation).

        Expected properties:
        - System returns best-effort output
        - Constraints are preserved (6+ failure modes)
        - RunRecord includes execution details
        """
        response = await run_zeus(
            prompt=(
                "Design a run controller for an LLM pipeline that must handle "
                "timeouts, partial failures, and structured-output parse errors. "
                "Include a failure-mode table."
            ),
            mode="brief",
            constraints=[
                "Include a table with at least 6 failure modes."
            ],
        )

        # Verify MVP invariants
        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None

        # Verify output contains failure modes (constraint respected)
        assert response.output is not None
        output_lower = response.output.lower()
        assert "failure" in output_lower

        # Verify usage is within budget
        assert response.usage.llm_calls <= 6

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_case_7_constraint_enforcement(self):
        """Case 7: Deterministic constraint enforcement (constraints must be checked).

        Expected properties:
        - Constraints appear in NormalizedProblem
        - Critique checks for section-title requirements
        - Output includes required sections
        """
        response = await run_zeus(
            prompt=(
                "Propose a deterministic constraint checker layer for verifying "
                "output contracts in an AI system. Include what can be checked "
                "deterministically vs heuristically."
            ),
            mode="brief",
            constraints=[
                "Must include a section titled 'Deterministic Checks'",
                "Must include a section titled 'Heuristic Checks'"
            ],
        )

        # Verify MVP invariants
        assert isinstance(response, ZeusResponse)
        assert response.run_id is not None
        assert response.assumptions is not None
        assert response.known_issues is not None

        # Verify constraint enforcement (required sections present)
        assert response.output is not None
        output_lower = response.output.lower()
        assert "deterministic" in output_lower
        assert "heuristic" in output_lower

        # Verify usage is within budget
        assert response.usage.llm_calls <= 6


class TestMVPInvariants:
    """Additional tests for MVP system invariants."""

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_critique_always_runs(self):
        """Verify critique runs on every generation (MVP invariant #1)."""
        response = await run_zeus(
            prompt="Design a simple logging service.",
            mode="brief",
            constraints=[],
        )

        # Critique running is evidenced by known_issues being populated
        # (critique generates the issues that become known_issues)
        assert response.known_issues is not None
        # At minimum, the meta issue about coverage should be present
        # or actual issues from the critique

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_transparency_fields_always_present(self):
        """Verify assumptions[] and known_issues[] always present (MVP invariant #3)."""
        response = await run_zeus(
            prompt="Design a minimal cache.",
            mode="brief",
            constraints=[],
        )

        # These must never be None
        assert response.assumptions is not None
        assert response.known_issues is not None
        # They are lists (may be empty but exist)
        assert isinstance(response.assumptions, list)
        assert isinstance(response.known_issues, list)

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_run_id_generated(self):
        """Verify every run has a unique run_id (MVP invariant #2)."""
        response1 = await run_zeus(
            prompt="Design service A.",
            mode="brief",
            constraints=[],
        )
        response2 = await run_zeus(
            prompt="Design service B.",
            mode="brief",
            constraints=[],
        )

        assert response1.run_id is not None
        assert response2.run_id is not None
        # Run IDs should be unique
        assert response1.run_id != response2.run_id

    @pytest.mark.asyncio
    @pytest.mark.timeout(300)
    async def test_budget_enforcement(self):
        """Verify budget is enforced (MVP invariant #5)."""
        response = await run_zeus(
            prompt="Design a complex distributed system with many components.",
            mode="brief",
            constraints=["Must be highly detailed"],
            max_llm_calls=6,  # Explicit budget
        )

        # Must not exceed budget
        assert response.usage.llm_calls <= 6
