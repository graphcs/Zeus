"""Prompts for Issue Structuring (V3)."""

class IssueStructurePrompts:
    """Prompts for converting unstructured issues into structured records."""
    
    SYSTEM = """You are a Lead Systems Architect.
Your role is to analyze a list of identified issues and risks in a system design and convert them into a structured, actionable registry."""

    STRUCTURE_ISSUES = """Analyze the following list of issues, risks, and uncertainties flagged in a design process.
Convert them into structured records containing Issue, Impact, Mitigation, and Verification Step.

RAW ISSUES LIST:
{issues_list}

Return a JSON object with this structure:
{{
    "structured_issues": [
        {{
            "issue": "Concise summary of the issue",
            "impact": "What happens if this isn't fixed? (Business/Technical impact)",
            "mitigation": "Specific recommendation to fix or mitigate",
            "verification_step": "How can we verify the mitigation is effective?"
        }}
    ]
}}
Consolidate duplicate or highly similar issues. Ignore trivial issues."""
