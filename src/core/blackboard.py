"""Blackboard - V4 Shared state for the agent pool.

The blackboard is the minimal shared state that specialist reviewers
and the synthesizer operate on. It holds the current candidate,
the accumulated issue list, and resolved flags.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from src.models.schemas import Candidate, Critique, CritiqueIssue


class IssueStatus(str, Enum):
    """Resolution status of an issue on the blackboard."""
    OPEN = "open"
    RESOLVED = "resolved"
    DEFERRED = "deferred"
    WONT_FIX = "wont_fix"


@dataclass
class BlackboardIssue:
    """An issue tracked on the blackboard with resolution metadata."""
    issue: CritiqueIssue
    status: IssueStatus = IssueStatus.OPEN
    resolved_by: str | None = None  # Which specialist resolved it
    resolution_note: str | None = None

    @property
    def is_open(self) -> bool:
        return self.status == IssueStatus.OPEN

    def resolve(self, specialist: str, note: str) -> None:
        """Mark this issue as resolved by a specialist."""
        self.status = IssueStatus.RESOLVED
        self.resolved_by = specialist
        self.resolution_note = note

    def defer(self, note: str) -> None:
        """Defer this issue to a future iteration."""
        self.status = IssueStatus.DEFERRED
        self.resolution_note = note


@dataclass
class Blackboard:
    """Minimal shared state for the V4 agent pool.

    Holds the current candidate, accumulated issues from all specialists,
    and resolution tracking. Designed for debuggability: every mutation
    is recorded in the event log.

    Attributes:
        candidate: The current best candidate (updated by synthesizer).
        issues: All issues from all specialist reviews, with status.
        event_log: Ordered log of every mutation for traceability.
    """
    candidate: Candidate
    issues: list[BlackboardIssue] = field(default_factory=list)
    event_log: list[str] = field(default_factory=list)

    # Budget tracking
    specialist_calls_used: int = 0
    max_specialist_calls: int = 3  # V4 cap: ≤2-3 total across roles

    @property
    def open_issues(self) -> list[BlackboardIssue]:
        """Return only unresolved issues."""
        return [i for i in self.issues if i.is_open]

    @property
    def open_blockers(self) -> list[BlackboardIssue]:
        """Return only unresolved blocker issues."""
        return [
            i for i in self.issues
            if i.is_open and i.issue.severity == "blocker"
        ]

    @property
    def open_majors(self) -> list[BlackboardIssue]:
        """Return only unresolved major issues."""
        return [
            i for i in self.issues
            if i.is_open and i.issue.severity == "major"
        ]

    @property
    def has_budget(self) -> bool:
        """Check if the specialist call budget allows another call."""
        return self.specialist_calls_used < self.max_specialist_calls

    def add_issues_from_critique(self, critique: Critique, source: str = "critic") -> None:
        """Import issues from a Critique into the blackboard.

        Args:
            critique: The critique to import from.
            source: Label for the source agent (for traceability).
        """
        for issue in critique.issues:
            self.issues.append(BlackboardIssue(issue=issue))
        self._log(f"Added {len(critique.issues)} issues from {source}")

    def add_specialist_issues(
        self, issues: list[CritiqueIssue], specialist: str
    ) -> None:
        """Add issues discovered by a specialist reviewer.

        Args:
            issues: New issues found by the specialist.
            specialist: Name of the specialist agent.
        """
        for issue in issues:
            self.issues.append(BlackboardIssue(issue=issue))
        self._log(f"Specialist '{specialist}' added {len(issues)} new issues")

    def mark_resolved(
        self, indices: list[int], specialist: str, note: str
    ) -> None:
        """Mark specific issues as resolved.

        Args:
            indices: Indices into self.issues to mark resolved.
            specialist: Which specialist resolved them.
            note: Resolution description.
        """
        for idx in indices:
            if 0 <= idx < len(self.issues):
                self.issues[idx].resolve(specialist, note)
        self._log(
            f"Specialist '{specialist}' resolved {len(indices)} issues: {note}"
        )

    def update_candidate(self, candidate: Candidate, source: str) -> None:
        """Replace the current candidate with an updated version.

        Args:
            candidate: The new candidate.
            source: Which agent produced the update.
        """
        self.candidate = candidate
        self._log(f"Candidate updated by '{source}'")

    def use_specialist_call(self) -> None:
        """Consume one specialist call from the budget."""
        self.specialist_calls_used += 1
        self._log(
            f"Specialist call used ({self.specialist_calls_used}/{self.max_specialist_calls})"
        )

    def summary(self) -> dict:
        """Produce a snapshot summary for the RunRecord.

        Returns:
            Dict with issue counts, resolution stats, and event log.
        """
        total = len(self.issues)
        open_count = sum(1 for i in self.issues if i.is_open)
        resolved = sum(1 for i in self.issues if i.status == IssueStatus.RESOLVED)
        deferred = sum(1 for i in self.issues if i.status == IssueStatus.DEFERRED)

        # Issues resolved per specialist
        resolved_by: dict[str, int] = {}
        for issue in self.issues:
            if issue.resolved_by:
                resolved_by[issue.resolved_by] = resolved_by.get(issue.resolved_by, 0) + 1

        return {
            "total_issues": total,
            "open": open_count,
            "resolved": resolved,
            "deferred": deferred,
            "specialist_calls_used": self.specialist_calls_used,
            "max_specialist_calls": self.max_specialist_calls,
            "resolved_by_specialist": resolved_by,
            "event_log": list(self.event_log),
        }

    def _log(self, message: str) -> None:
        """Append an event to the event log."""
        self.event_log.append(message)
