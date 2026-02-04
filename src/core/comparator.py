"""Comparator - V2 Regression analysis."""

from src.models.schemas import (
    RunRecord,
    EvaluationSummary,
    RegressionDelta,
)

class Comparator:
    """Compares current run against a baseline for regression analysis."""
    
    @staticmethod
    def compare(current: RunRecord, baseline: RunRecord) -> RegressionDelta | None:
        """Compare current run with baseline run.
        
        Args:
            current: The current execution run record.
            baseline: The baseline run record.
            
        Returns:
            RegressionDelta if comparison is possible, else None.
        """
        if not current.final_response or not baseline.final_response:
            return None
            
        # Extract Evaluation Summaries
        curr_eval = current.final_response.evaluation_summary
        base_eval = baseline.final_response.evaluation_summary
        
        if not curr_eval or not base_eval:
            return None
            
        # Parse into objects if they are dicts
        if isinstance(curr_eval, dict):
            curr_eval = EvaluationSummary.model_validate(curr_eval)
        if isinstance(base_eval, dict):
            base_eval = EvaluationSummary.model_validate(base_eval)
            
        # Compute Deltas
        coverage_delta = curr_eval.coverage_score - base_eval.coverage_score
        
        # Issue deltas (Positive means MORE issues, which is bad)
        issues_delta = curr_eval.total_issues - base_eval.total_issues
        blocker_delta = curr_eval.blockers - base_eval.blockers
        major_delta = curr_eval.majors - base_eval.majors
        constraints_delta = curr_eval.constraint_violations - base_eval.constraint_violations
        
        # Determine "Is Worse"
        # Heuristic: Worse if blockers increased, OR majors increased, OR coverage dropped significantly
        is_worse = False
        
        if blocker_delta > 0:
            is_worse = True
        elif major_delta > 0:
            is_worse = True
        elif coverage_delta < -0.15: # Significant drop in coverage (e.g. missing 1 perspective ~ 0.16)
            is_worse = True
            
        return RegressionDelta(
            is_worse=is_worse,
            coverage_delta=round(coverage_delta, 2),
            issues_delta=issues_delta,
            blocker_delta=blocker_delta,
            major_delta=major_delta,
            constraints_delta=constraints_delta,
            baseline_run_id=baseline.run_id,
            baseline_timestamp=baseline.timestamp
        )
