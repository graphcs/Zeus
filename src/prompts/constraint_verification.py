"""Prompts for Constraint Verification (V3)."""

class ConstraintVerificationPrompts:
    """Prompts for verifying constraints against content."""
    
    SYSTEM = """You are a rigorous QA Auditor for system design documents.
Your role is to verify if a generated design document complies with specific constraints.
You must be objective, strict, and evidence-based.
Do not hallucinate compliance. If it is not in the text, it is unverified."""

    VERIFY_CONSTRAINTS = """Verify if the provided content satisfies the following constraints.

CONTENT:
{content}

CONSTRAINTS TO VERIFY:
{constraints_list}

For each constraint, determine if it is:
- "pass": The content explicitly satisfies the constraint.
- "fail": The content explicitly violates the constraint.
- "unverified": The content does not provide enough information to determine pass/fail, or the constraint is strictly external.

Return a JSON object with this structure:
{{
    "checks": [
        {{
            "constraint": "The exact constraint text provided",
            "status": "pass", 
            "evidence": "Quote or short reasoning"
        }}
    ]
}}
Ensure the list "checks" contains one entry for EACH constraint provided."""
