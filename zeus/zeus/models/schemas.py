"""Data contracts for Zeus - Design Team Agent."""

import os
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field
import uuid


def _env_int(key: str, default: int) -> int:
    """Get integer from environment variable or default."""
    val = os.getenv(key)
    return int(val) if val else default


def _env_float(key: str, default: float) -> float:
    """Get float from environment variable or default."""
    val = os.getenv(key)
    return float(val) if val else default


# ============================================================================
# Input Models
# ============================================================================

class ZeusRequest(BaseModel):
    """Input request to Zeus."""
    prompt: str = Field(..., description="Raw idea or design brief")
    mode: Literal["brief", "solution"] = Field(..., description="Which team to invoke")
    constraints: list[str] = Field(default_factory=list, description="User-specified constraints")
    context: str | dict | None = Field(default=None, description="Additional context")


# ============================================================================
# Internal Models
# ============================================================================

class NormalizedProblem(BaseModel):
    """Structured representation of the input problem."""
    problem_statement: str = Field(..., description="Clear problem statement")
    constraints: list[str] = Field(default_factory=list, description="All constraints (never dropped)")
    output_spec: str = Field(..., description="Expected output specification")
    context: dict = Field(default_factory=dict, description="Parsed context")


class Tradeoff(BaseModel):
    """A design tradeoff made in the solution."""
    chose: str = Field(..., description="What was chosen")
    over: str = Field(..., description="What was sacrificed")
    rationale: str = Field(..., description="Why this choice was made")
    impact: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Impact level of this tradeoff"
    )


class Candidate(BaseModel):
    """A generated design brief or solution candidate."""
    content: str = Field(..., description="Design brief or solution content")
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made")
    uncertainty_flags: list[str] = Field(default_factory=list, description="Areas of uncertainty")
    tradeoffs: list[Tradeoff] = Field(default_factory=list, description="Design tradeoffs made")


# V1 Constants
ISSUE_CATEGORIES = Literal[
    "correctness", "completeness", "clarity", "feasibility",
    "maintainability", "performance", "security", "compliance"
]

# Set for runtime validation
VALID_ISSUE_CATEGORIES = frozenset({
    "correctness", "completeness", "clarity", "feasibility",
    "maintainability", "performance", "security", "compliance"
})

CONFIDENCE_LEVELS = Literal["low", "medium", "high"]

REQUIRED_PERSPECTIVES = frozenset({
    "scope", "architecture", "risk", "security", "compliance", "evaluation"
})

# Mapping of alternative names to canonical perspective names
PERSPECTIVE_ALIASES: dict[str, str] = {
    # Scope aliases
    "completeness": "scope",
    "scope_check": "scope",
    "boundaries": "scope",
    "requirements": "scope",
    "scope_definition": "scope",
    # Architecture aliases
    "structural": "architecture",
    "design": "architecture",
    "system_design": "architecture",
    "technical": "architecture",
    "feasibility": "architecture",
    # Risk aliases
    "failure_modes": "risk",
    "risks": "risk",
    "risk_assessment": "risk",
    # Security aliases
    "security_review": "security",
    "vulnerabilities": "security",
    "security_ops": "security",
    "ops": "security",
    "operations": "security",
    # Compliance aliases
    "regulatory": "compliance",
    "policy": "compliance",
    "governance": "compliance",
    "constraints": "compliance",
    "constraint_compliance": "compliance",
    # Evaluation aliases
    "testability": "evaluation",
    "success_criteria": "evaluation",
    "metrics": "evaluation",
    "measurability": "evaluation",
    "testing": "evaluation",
    "experimentation": "evaluation",
}


class CritiqueIssue(BaseModel):
    """A single issue identified during critique."""
    role: str = Field(..., description="Critique perspective, e.g., 'completeness', 'architecture'")
    severity: Literal["blocker", "major", "minor"] = Field(..., description="Issue severity")
    category: ISSUE_CATEGORIES = Field(
        default="completeness",
        description="Issue category from taxonomy"
    )
    description: str = Field(..., description="Issue description")
    suggested_fix: str | None = Field(default=None, description="Suggested fix if available")


class Critique(BaseModel):
    """Multi-view critique of a candidate."""
    issues: list[CritiqueIssue] = Field(default_factory=list, description="Identified issues")
    constraint_violations: list[str] = Field(default_factory=list, description="Violated constraints")
    missing_perspectives: list[str] = Field(default_factory=list, description="Perspectives not covered")


class PlanStep(BaseModel):
    """A single step in the generation plan."""
    step_number: int
    description: str
    focus_area: str


class Plan(BaseModel):
    """Linear plan for generation."""
    steps: list[PlanStep] = Field(default_factory=list)


# ============================================================================
# Output Models
# ============================================================================

class UsageStats(BaseModel):
    """Token usage and cost statistics for a run."""
    llm_calls: int = Field(default=0, description="Number of LLM calls made")
    tokens_in: int = Field(default=0, description="Total input tokens")
    tokens_out: int = Field(default=0, description="Total output tokens")
    total_tokens: int = Field(default=0, description="Total tokens (in + out)")
    cost_usd: float = Field(default=0.0, description="Estimated cost in USD")


class ZeusResponse(BaseModel):
    """Final output from Zeus."""
    # Core fields
    output: str = Field(..., description="Design Brief or Target Solution (Markdown)")
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made (always present)")
    known_issues: list[str] = Field(default_factory=list, description="Known issues (always present)")
    run_id: str = Field(..., description="Unique run identifier")
    usage: UsageStats = Field(default_factory=UsageStats, description="Token usage and cost")

    # V1 Evaluation Signals
    confidence: CONFIDENCE_LEVELS = Field(
        default="medium",
        description="Confidence level based on critique severity"
    )
    coverage_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Perspective coverage ratio (0.0-1.0)"
    )
    covered_perspectives: list[str] = Field(
        default_factory=list,
        description="List of perspectives covered in critique"
    )
    missing_perspectives: list[str] = Field(
        default_factory=list,
        description="List of perspectives not covered"
    )
    tradeoffs: list[Tradeoff] = Field(
        default_factory=list,
        description="Design tradeoffs documented"
    )

    # V1 Issue breakdown for CLI display
    issue_counts: dict[str, int] = Field(
        default_factory=lambda: {"blockers": 0, "majors": 0, "minors": 0},
        description="Count of issues by severity"
    )
    issues_by_category: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Known issues grouped by category"
    )


# ============================================================================
# Traceability Models
# ============================================================================

class BudgetConfig(BaseModel):
    """Budget configuration for a run.

    Defaults can be overridden via environment variables:
    - ZEUS_MAX_LLM_CALLS
    - ZEUS_TARGET_LLM_CALLS
    - ZEUS_MAX_REVISIONS
    - ZEUS_PER_CALL_TIMEOUT
    - ZEUS_TOTAL_RUN_TIMEOUT
    """
    max_llm_calls: int = Field(
        default_factory=lambda: _env_int("ZEUS_MAX_LLM_CALLS", 6),
        description="Hard cap on LLM calls (default: 6 for full pipeline)"
    )
    target_llm_calls: int = Field(
        default_factory=lambda: _env_int("ZEUS_TARGET_LLM_CALLS", 4),
        description="Soft target for LLM calls"
    )
    max_revisions: int = Field(
        default_factory=lambda: _env_int("ZEUS_MAX_REVISIONS", 1),
        description="Max revision loops"
    )
    per_call_timeout: float = Field(
        default_factory=lambda: _env_float("ZEUS_PER_CALL_TIMEOUT", 60.0),
        description="Timeout per LLM call in seconds"
    )
    total_run_timeout: float = Field(
        default_factory=lambda: _env_float("ZEUS_TOTAL_RUN_TIMEOUT", 300.0),
        description="Total run timeout in seconds (5 min default)"
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
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mode: Literal["brief", "solution"]
    request: ZeusRequest
    normalized_problem: NormalizedProblem | None = None
    plan: Plan | None = None
    candidate_v1: Candidate | None = None
    critique_v1: Critique | None = None
    candidate_v2: Candidate | None = None
    critique_v2: Critique | None = None
    final_response: ZeusResponse | None = None
    model_version: str = "anthropic/claude-sonnet-4"
    prompt_versions: dict = Field(default_factory=dict)
    budget_used: BudgetUsed = Field(default_factory=BudgetUsed)
    errors: list[str] = Field(default_factory=list)

    def has_blockers(self, critique: Critique | None) -> bool:
        """Check if critique has any blocker-level issues."""
        if critique is None:
            return False
        return any(issue.severity == "blocker" for issue in critique.issues)

    def needs_revision(self) -> bool:
        """Check if revision is needed and allowed."""
        # Revision needed if blockers exist and we haven't done a revision yet
        return self.has_blockers(self.critique_v1) and self.candidate_v2 is None

    def can_revise(self) -> bool:
        """Check if revision budget allows another iteration."""
        return self.budget_used.revisions < 1  # Max 1 revision enforced
