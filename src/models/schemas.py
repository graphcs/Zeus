"""Data contracts for Zeus - Multi-Inventor Design System."""

import os
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
import uuid


def _env_int(key: str, default: int) -> int:
    val = os.getenv(key)
    return int(val) if val else default


def _env_float(key: str, default: float) -> float:
    val = os.getenv(key)
    return float(val) if val else default


# ============================================================================
# Input Models
# ============================================================================

class ZeusRequest(BaseModel):
    """Input request to Zeus."""
    prompt: str = Field(..., description="Raw problem statement or idea")
    constraints: list[str] = Field(default_factory=list, description="User-specified constraints")
    objectives: list[str] = Field(default_factory=list, description="User-specified objectives")
    context: str | dict | None = Field(default=None, description="Additional context")
    library_paths: list[str] = Field(default_factory=list, description="Paths to library files")
    output_spec_path: str | None = Field(default=None, description="Path to output specification")
    eval_criteria_path: str | None = Field(default=None, description="Path to evaluation criteria")
    enable_cross_pollination: bool = Field(default=False, description="Enable Phase 2 cross-pollination")
    num_inventors: int = Field(default=4, ge=1, le=10, description="Number of inventors to run")


# ============================================================================
# Phase 0: Intake Models
# ============================================================================

class ProblemClassification(BaseModel):
    """Classification of the problem type to inform inventor configuration."""
    problem_type: str = Field(default="general", description="e.g. strategy_design, system_architecture, process_design")
    uncertainty_level: Literal["low", "medium", "high"] = Field(default="medium")
    key_domains: list[str] = Field(default_factory=list, description="Key domains relevant to the problem")
    recommended_library_emphasis: list[str] = Field(default_factory=list, description="Libraries to emphasize")


class ProblemBrief(BaseModel):
    """Normalized problem statement that all inventors receive."""
    problem_statement: str = Field(..., description="Clear, normalized problem statement")
    objectives: list[str] = Field(default_factory=list, description="All objectives")
    constraints: list[str] = Field(default_factory=list, description="All constraints (never dropped)")
    classification: ProblemClassification = Field(default_factory=ProblemClassification)
    implicit_assumptions: list[str] = Field(default_factory=list, description="Assumptions surfaced during intake")
    ambiguities: list[str] = Field(default_factory=list, description="Ambiguities identified")
    output_spec: str = Field(default="", description="Output specification content")
    eval_criteria: str = Field(default="", description="Evaluation criteria content")
    context: dict = Field(default_factory=dict, description="Parsed context")


# ============================================================================
# Phase 1: Inventor Models
# ============================================================================

class InventorConfig(BaseModel):
    """Configuration for a single inventor."""
    inventor_id: str = Field(..., description="Unique inventor identifier (e.g. 'A', 'B')")
    inventor_type: str = Field(..., description="foundational, competitive, comprehensive, tabula_rasa, domain_specific")
    library_assignments: list[str] = Field(default_factory=list, description="Libraries assigned to this inventor")
    emphasis: str = Field(default="", description="Emphasis directive for this inventor")
    model_override: str | None = Field(default=None, description="Optional model override")


class InventorSolution(BaseModel):
    """Output from a single inventor."""
    inventor_id: str = Field(..., description="Which inventor produced this")
    inventor_type: str = Field(default="", description="Type of inventor")
    content: str = Field(default="", description="Full solution content")
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made")
    reasoning_trace: str = Field(default="", description="Key reasoning and decisions")
    libraries_used: list[str] = Field(default_factory=list, description="Libraries actually used")


# ============================================================================
# Phase 2: Cross-Pollination Models
# ============================================================================

class CrossCritique(BaseModel):
    """A critique from one inventor of another's solution."""
    critic_id: str = Field(..., description="Inventor providing the critique")
    target_id: str = Field(..., description="Inventor being critiqued")
    disagreements: list[str] = Field(default_factory=list, description="Points of disagreement")
    missed_elements: list[str] = Field(default_factory=list, description="Elements the target missed")
    strengths: list[str] = Field(default_factory=list, description="Strengths of the target solution")


# ============================================================================
# Phase 3: Synthesis Models
# ============================================================================

class Provenance(BaseModel):
    """Tracks where a solution element came from."""
    element: str = Field(..., description="Description of the solution element")
    source_inventor: str = Field(..., description="Which inventor it came from")
    modified: bool = Field(default=False, description="Whether it was modified during synthesis")
    reason: str = Field(default="", description="Reason for inclusion/modification")


class ResolvedConflict(BaseModel):
    """A conflict between inventors that was resolved during synthesis."""
    conflict: str = Field(..., description="Description of the conflict")
    resolution: str = Field(..., description="How it was resolved")
    rationale: str = Field(default="", description="Why this resolution was chosen")


class SynthesisResult(BaseModel):
    """Output from the convergent synthesis phase."""
    unified_draft: str = Field(default="", description="The synthesized solution content")
    version: int = Field(default=1, description="Draft version number")
    provenance: list[Provenance] = Field(default_factory=list, description="Element provenance tracking")
    resolved_conflicts: list[ResolvedConflict] = Field(default_factory=list, description="Conflicts resolved")
    open_issues: list[str] = Field(default_factory=list, description="Remaining open issues")


# ============================================================================
# Phase 4: Library Critique Models
# ============================================================================

class LibraryCritiqueIssue(BaseModel):
    """A single issue found by a library critic."""
    severity: Literal["blocker", "major", "minor"] = Field(..., description="Issue severity")
    description: str = Field(..., description="Issue description")
    suggested_fix: str | None = Field(default=None, description="Suggested fix")


class LibraryCritiqueFinding(BaseModel):
    """Findings from a single library critic."""
    library_name: str = Field(..., description="Which library was used as lens")
    violations: list[str] = Field(default_factory=list, description="Principles/elements violated")
    embodied: list[str] = Field(default_factory=list, description="Principles/elements embodied")
    missing: list[str] = Field(default_factory=list, description="Principles/elements missing")
    coverage_pct: float = Field(default=0.0, ge=0.0, le=100.0, description="Coverage percentage")
    issues: list[LibraryCritiqueIssue] = Field(default_factory=list, description="Issues found")


class LibraryCritiqueResult(BaseModel):
    """Combined output from all library critics."""
    findings: list[LibraryCritiqueFinding] = Field(default_factory=list, description="Per-library findings")
    all_issues: list[LibraryCritiqueIssue] = Field(default_factory=list, description="All issues merged")
    blocker_count: int = Field(default=0)
    major_count: int = Field(default=0)
    minor_count: int = Field(default=0)


# ============================================================================
# Phase 5: Refinement Models
# ============================================================================

class RefinementIteration(BaseModel):
    """Record of a single refinement iteration."""
    iteration: int = Field(..., description="Iteration number")
    issues_addressed: int = Field(default=0, description="Number of issues addressed")
    blockers_remaining: int = Field(default=0, description="Blockers remaining after this iteration")
    majors_remaining: int = Field(default=0, description="Majors remaining")


# ============================================================================
# Evaluation Models (13 criteria, /220 max)
# ============================================================================

class CriterionScore(BaseModel):
    """Score for a single evaluation criterion."""
    section: str = Field(..., description="Section number e.g. '1.1'")
    name: str = Field(..., description="Criterion name e.g. 'Capital Preservation'")
    objective: str = Field(..., description="Objective reference e.g. '1 (MUST)'")
    raw_score: int = Field(..., ge=1, le=5, description="Raw score 1-5")
    weight: float = Field(..., description="Weight multiplier")
    weighted_score: float = Field(default=0.0, description="raw_score * weight")
    justification: str = Field(default="", description="Scoring justification")


class HardConstraintResult(BaseModel):
    """Result for a HARD constraint check."""
    constraint_id: str = Field(..., description="e.g. 'C1'")
    name: str = Field(..., description="Constraint name")
    passed: bool = Field(..., description="Whether the constraint passed")
    notes: str = Field(default="", description="Assessment notes")


class SelfEvaluationScorecard(BaseModel):
    """Full self-evaluation scorecard per Evaluation_Criteria_v3."""
    criteria_scores: list[CriterionScore] = Field(default_factory=list, description="All 13 criterion scores")
    hard_constraints: list[HardConstraintResult] = Field(default_factory=list, description="HARD constraint results")
    total_score: float = Field(default=0.0, description="Sum of weighted scores")
    max_score: float = Field(default=220.0, description="Maximum possible score")
    score_percentage: float = Field(default=0.0, description="total_score / max_score * 100")
    disqualified: bool = Field(default=False, description="Whether solution is disqualified")
    disqualification_reasons: list[str] = Field(default_factory=list, description="Reasons for disqualification")
    identified_weaknesses: list[str] = Field(default_factory=list, description="Lowest-scoring areas")


# ============================================================================
# Output Models
# ============================================================================

class UsageStats(BaseModel):
    """Token usage and cost statistics for a run."""
    llm_calls: int = Field(default=0)
    tokens_in: int = Field(default=0)
    tokens_out: int = Field(default=0)
    total_tokens: int = Field(default=0)
    cost_usd: float = Field(default=0.0)


class ZeusResponse(BaseModel):
    """Final output from Zeus."""
    output: str = Field(..., description="Combined deliverables (Markdown)")
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made (always present)")
    known_issues: list[str] = Field(default_factory=list, description="Known issues (always present)")
    run_id: str = Field(..., description="Unique run identifier")
    usage: UsageStats = Field(default_factory=UsageStats)

    # 5 deliverables
    executive_summary: str = Field(default="", description="Deliverable 1: Executive Summary")
    solution_design_document: str = Field(default="", description="Deliverable 2: Solution Design Document")
    foundation_documentation: str = Field(default="", description="Deliverable 3: Foundation Documentation")
    self_evaluation_scorecard: str = Field(default="", description="Deliverable 4: Self-Evaluation Scorecard (rendered)")
    run_log: str = Field(default="", description="Deliverable 5: Run Log")

    # Evaluation
    total_score: float = Field(default=0.0, description="Evaluation score out of 220")
    max_score: float = Field(default=220.0)
    score_percentage: float = Field(default=0.0)
    disqualified: bool = Field(default=False)
    scorecard: SelfEvaluationScorecard | None = Field(default=None, description="Full scorecard object")

    # Provenance & alternatives
    provenance: list[Provenance] = Field(default_factory=list)
    alternative_approaches: list[str] = Field(default_factory=list, description="Summary of alternative inventor approaches")


# ============================================================================
# Traceability Models
# ============================================================================

class BudgetConfig(BaseModel):
    """Budget configuration for a run."""
    max_llm_calls: int = Field(
        default_factory=lambda: _env_int("ZEUS_MAX_LLM_CALLS", 30),
        description="Hard cap on LLM calls (default: 30 for multi-inventor pipeline)"
    )
    target_llm_calls: int = Field(
        default_factory=lambda: _env_int("ZEUS_TARGET_LLM_CALLS", 20),
        description="Soft target for LLM calls"
    )
    max_revisions: int = Field(
        default_factory=lambda: _env_int("ZEUS_MAX_REVISIONS", 3),
        description="Max revision loops"
    )
    per_call_timeout: float = Field(
        default_factory=lambda: _env_float("ZEUS_PER_CALL_TIMEOUT", 120.0),
        description="Timeout per LLM call in seconds"
    )
    total_run_timeout: float = Field(
        default_factory=lambda: _env_float("ZEUS_TOTAL_RUN_TIMEOUT", 900.0),
        description="Total run timeout in seconds (15 min default)"
    )


class BudgetUsed(BaseModel):
    """Budget tracking for a run."""
    llm_calls: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    revisions: int = 0


class RunRecord(BaseModel):
    """Complete record of a Zeus run for traceability."""
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    request: ZeusRequest

    # Phase 0
    problem_brief: ProblemBrief | None = None

    # Phase 1
    inventor_configs: list[InventorConfig] = Field(default_factory=list)
    inventor_solutions: list[InventorSolution] = Field(default_factory=list)

    # Phase 2
    cross_critiques: list[CrossCritique] = Field(default_factory=list)

    # Phase 3
    synthesis_result: SynthesisResult | None = None

    # Phase 4
    library_critique: LibraryCritiqueResult | None = None

    # Phase 5
    refinement_history: list[RefinementIteration] = Field(default_factory=list)
    final_draft: str = Field(default="", description="Final refined draft content")

    # Phase 6
    self_evaluation: SelfEvaluationScorecard | None = None
    final_response: ZeusResponse | None = None

    # Traceability
    model_version: str = "anthropic/claude-sonnet-4"
    prompt_versions: dict = Field(default_factory=dict)
    budget_used: BudgetUsed = Field(default_factory=BudgetUsed)
    errors: list[str] = Field(default_factory=list)
