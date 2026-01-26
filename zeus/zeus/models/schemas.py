"""Data contracts for Zeus - Design Team Agent."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
import uuid


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


class Candidate(BaseModel):
    """A generated design brief or solution candidate."""
    content: str = Field(..., description="Design brief or solution content")
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made")
    uncertainty_flags: list[str] = Field(default_factory=list, description="Areas of uncertainty")


class CritiqueIssue(BaseModel):
    """A single issue identified during critique."""
    role: str = Field(..., description="Critique perspective, e.g., 'completeness', 'architecture'")
    severity: Literal["blocker", "major", "minor"] = Field(..., description="Issue severity")
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

class ZeusResponse(BaseModel):
    """Final output from Zeus."""
    output: str = Field(..., description="Design Brief or Target Solution (Markdown)")
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made (always present)")
    known_issues: list[str] = Field(default_factory=list, description="Known issues (always present)")
    run_id: str = Field(..., description="Unique run identifier")


# ============================================================================
# Traceability Models
# ============================================================================

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
