"""Evaluator - V1 evaluation signals and metrics computation."""

import re
from typing import Literal
from src.models.schemas import (
    Candidate,
    Critique,
    CritiqueIssue,
    RunRecord,
    EvaluationSummary,
)


# Section checklists for completeness scoring
BRIEF_REQUIRED_SECTIONS = [
    "executive summary", "problem statement", "goals", "scope",
    "requirements", "constraints", "tradeoff", "assumptions",
    "success criteria", "open questions",
]
SOLUTION_REQUIRED_SECTIONS = [
    "solution overview", "architecture", "components", "data model",
    "api", "interface", "security", "scalability", "performance",
    "error handling", "tradeoff", "testing", "implementation",
    "constraints compliance", "assumptions", "risk", "open questions",
]


class CompletenessChecker:
    """Checks output completeness against required section checklists."""

    @staticmethod
    def check(content: str, mode: str) -> tuple[float, list[str]]:
        """Scan markdown headings against the mode's required sections.

        Args:
            content: The generated markdown content.
            mode: Either "brief" or "solution".

        Returns:
            Tuple of (score 0.0-1.0, list of missing section names).
        """
        checklist = BRIEF_REQUIRED_SECTIONS if mode == "brief" else SOLUTION_REQUIRED_SECTIONS

        # Extract all headings (h1-h3) from content
        headings = re.findall(r"^#{1,3}\s+(.+)", content, re.MULTILINE | re.IGNORECASE)
        headings_lower = [h.strip().lower() for h in headings]

        found = set()
        for section in checklist:
            for heading in headings_lower:
                if section in heading or heading in section:
                    found.add(section)
                    break

        missing = [s for s in checklist if s not in found]
        score = len(found) / len(checklist) if checklist else 1.0
        return score, missing


# Issue category definitions for taxonomy
ISSUE_CATEGORIES = {
    "correctness": "Logical errors or incorrect implementations",
    "completeness": "Missing requirements or incomplete coverage",
    "constraint_violation": "Violation of stated constraints",
    "clarity": "Unclear or ambiguous content",
    "uncertainty": "Areas needing clarification",
    "safety": "Safety or security concerns",
    "feasibility": "Implementation or operational feasibility issues",
    "general": "General observations or other concerns",
}


class ConfidenceEvaluator:
    """Evaluates confidence level in a solution based on critique results.
    
    Confidence Rules (V1):
    - LOW: Any blocker issues OR coverage < 50% OR 3+ major issues
    - HIGH: No blockers, ≤1 major, coverage ≥ 83% (5/6 perspectives)
    - MEDIUM: Everything else
    """
    
    @staticmethod
    def evaluate(
        critique: Critique | None,
        coverage_score: float,
    ) -> Literal["low", "medium", "high"]:
        """Compute confidence level.
        
        Args:
            critique: The final critique (v2 if exists, else v1).
            coverage_score: Perspective coverage score (0.0-1.0).
            
        Returns:
            Confidence level: "low", "medium", or "high".
        """
        if critique is None:
            # No critique available - low confidence
            return "low"
        
        # Count issues by severity
        blockers = sum(1 for i in critique.issues if i.severity == "blocker")
        majors = sum(1 for i in critique.issues if i.severity == "major")
        
        # LOW confidence criteria
        if blockers > 0:
            return "low"
        if coverage_score < 0.5:  # Less than 3/6 perspectives
            return "low"
        if majors >= 3:
            return "low"
        
        # HIGH confidence criteria
        if blockers == 0 and majors <= 1 and coverage_score >= 0.83:  # 5/6 or 6/6
            return "high"
        
        # Everything else is MEDIUM
        return "medium"


class TradeoffExtractor:
    """Extracts explicit tradeoffs from candidates and critiques.
    
    Tradeoffs are design decisions where one quality was sacrificed
    for another (e.g., "Chose simplicity over performance").
    """
    
    @staticmethod
    def extract(candidate: Candidate | None, critique: Critique | None) -> list[str]:
        """Extract tradeoffs from the candidate and critique.
        
        Args:
            candidate: The final candidate.
            critique: The final critique.
            
        Returns:
            List of tradeoff descriptions.
        """
        tradeoffs = []
        
        if candidate is None:
            return tradeoffs
        
        # Extract from candidate content using keyword patterns
        tradeoffs.extend(TradeoffExtractor._extract_from_text(candidate.content))
        
        # Extract from uncertainty flags (often indicate tradeoffs)
        if candidate.uncertainty_flags:
            for flag in candidate.uncertainty_flags:
                if any(keyword in flag.lower() for keyword in ["vs", "over", "instead", "sacrifice", "trade"]):
                    tradeoffs.append(flag)
        
        # Extract from critique constraint violations (may indicate accepted tradeoffs)
        if critique and critique.constraint_violations:
            for violation in critique.constraint_violations[:2]:  # Limit to avoid noise
                tradeoffs.append(f"Constraint relaxed: {violation}")
        
        return tradeoffs[:10]  # Limit to top 10 most relevant
    
    @staticmethod
    def _extract_from_text(content: str) -> list[str]:
        """Extract tradeoff statements from text using patterns.
        
        Args:
            content: The candidate content to analyze.
            
        Returns:
            List of extracted tradeoff statements.
        """
        tradeoffs = []
        
        # Common tradeoff patterns
        patterns = [
            "tradeoff:",
            "trade-off:",
            "chose",
            "prioritized",
            "sacrificed",
            "over",
            "instead of",
        ]
        
        lines = content.split("\n")
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip empty lines and headers
            if not line_lower or line_lower.startswith("#"):
                continue
            
            # Check if line contains tradeoff keywords
            if any(pattern in line_lower for pattern in patterns):
                # Clean the line
                cleaned = line.strip().lstrip("*-•").strip()
                if 10 < len(cleaned) < 200:  # Reasonable length
                    tradeoffs.append(cleaned)
        
        return tradeoffs


class EvaluationEngine:
    """Main evaluation engine for V1 structured evaluation signals.
    
    Combines confidence evaluation, coverage metrics, and tradeoff extraction
    to produce a comprehensive EvaluationSummary.
    """
    
    def __init__(self):
        """Initialize evaluation engine."""
        self.confidence_evaluator = ConfidenceEvaluator()
        self.tradeoff_extractor = TradeoffExtractor()
    
    def evaluate(self, record: RunRecord) -> EvaluationSummary:
        """Generate comprehensive evaluation summary for a run.

        Args:
            record: The complete run record.

        Returns:
            EvaluationSummary with all V1 metrics.
        """
        # Use final critique (v2 if exists, else v1)
        final_critique = record.critique_v2 or record.critique_v1

        # Completeness check (works even without critique)
        final_candidate = record.candidate_v2 or record.candidate_v1
        completeness_score = 0.0
        missing_sections: list[str] = []
        if final_candidate:
            completeness_score, missing_sections = CompletenessChecker.check(
                final_candidate.content, record.mode
            )

        if final_critique is None:
            # No critique - return minimal summary
            return EvaluationSummary(
                confidence="low",
                coverage_score=0.0,
                total_issues=0,
                blockers=0,
                majors=0,
                minors=0,
                constraint_violations=0,
                missing_perspectives=[],
                covered_perspectives=[],
                issues_by_category={},
                completeness_score=completeness_score,
                missing_sections=missing_sections,
            )

        # Compute metrics
        severity_counts = self._count_by_severity(final_critique)
        category_counts = self._count_by_category(final_critique)
        coverage_score = self._compute_coverage(final_critique)
        covered, missing = self._analyze_perspectives(final_critique)

        # Evaluate confidence
        confidence = self.confidence_evaluator.evaluate(
            final_critique,
            coverage_score,
        )

        return EvaluationSummary(
            confidence=confidence,
            coverage_score=coverage_score,
            total_issues=len(final_critique.issues),
            blockers=severity_counts["blocker"],
            majors=severity_counts["major"],
            minors=severity_counts["minor"],
            constraint_violations=len(final_critique.constraint_violations),
            missing_perspectives=list(missing),
            covered_perspectives=list(covered),
            issues_by_category=category_counts,
            completeness_score=completeness_score,
            missing_sections=missing_sections,
        )
    
    def _count_by_severity(self, critique: Critique) -> dict[str, int]:
        """Count issues by severity."""
        counts = {"blocker": 0, "major": 0, "minor": 0}
        for issue in critique.issues:
            counts[issue.severity] += 1
        return counts
    
    def _count_by_category(self, critique: Critique) -> dict[str, int]:
        """Count issues by category."""
        counts: dict[str, int] = {}
        for issue in critique.issues:
            category = issue.category or "general"
            counts[category] = counts.get(category, 0) + 1
        return counts
    
    def _compute_coverage(self, critique: Critique) -> float:
        """Compute perspective coverage score (0.0-1.0)."""
        from src.core.critic import REQUIRED_PERSPECTIVES
        
        covered = set()
        for issue in critique.issues:
            # Normalize role to perspective
            role_lower = issue.role.lower().strip()
            for perspective in REQUIRED_PERSPECTIVES:
                if perspective in role_lower or role_lower in perspective:
                    covered.add(perspective)
                    break
        
        return len(covered) / len(REQUIRED_PERSPECTIVES) if REQUIRED_PERSPECTIVES else 0.0
    
    def _analyze_perspectives(self, critique: Critique) -> tuple[set[str], set[str]]:
        """Analyze which perspectives are covered vs missing."""
        from src.core.critic import REQUIRED_PERSPECTIVES
        
        covered = set()
        for issue in critique.issues:
            role_lower = issue.role.lower().strip()
            for perspective in REQUIRED_PERSPECTIVES:
                if perspective in role_lower or role_lower in perspective:
                    covered.add(perspective)
                    break
        
        missing = REQUIRED_PERSPECTIVES - covered
        return covered, missing
