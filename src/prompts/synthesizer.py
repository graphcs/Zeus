"""Prompts for V4 Synthesizer."""


class SynthesizerPrompts:
    """Prompts for the synthesizer agent.

    The synthesizer takes the current candidate, all specialist feedback,
    and produces a revised candidate that incorporates the best fixes
    while preserving existing strengths.
    """

    VERSION = "1.0.0"

    SYSTEM = (
        "You are a Lead Architect responsible for synthesizing feedback from "
        "multiple specialist reviewers into a single, coherent, improved design.\n"
        "Your mandate: produce a revised candidate that addresses the most "
        "critical issues while maintaining design coherence and not introducing "
        "regressions. Preserve all constraints and existing strengths."
    )

    SYNTHESIZE = """You are given the current candidate and feedback from specialist reviewers.
Produce a revised candidate that addresses the identified issues.

PROBLEM STATEMENT:
{problem_statement}

CONSTRAINTS (must all be preserved):
{constraints}

CURRENT CANDIDATE:
{content}

SPECIALIST REVIEWS:
{specialist_reviews}

OPEN ISSUES (unresolved):
{open_issues}

Instructions:
1. Address all blocker issues first, then majors.
2. Incorporate specialist fix suggestions where they improve the design.
3. Do NOT remove existing sections or constraints.
4. If a fix would conflict with another, choose the safer option and document the tradeoff.
5. Update assumptions and uncertainty flags to reflect changes.

Return a JSON object:
{{
    "content": "The complete revised Markdown content",
    "assumptions": ["Updated list of assumptions"],
    "uncertainty_flags": ["Updated areas of uncertainty"],
    "reasoning_trace": "Explanation of what was changed and why",
    "comparison_analysis": "Delta vs the pre-synthesis candidate",
    "resolved_issue_indices": [0, 1, 2],
    "resolution_notes": "Summary of what was fixed"
}}

IMPORTANT:
- `resolved_issue_indices` are 0-based indices into the OPEN ISSUES list above.
- The content must be complete — do not use placeholders like '...' or 'same as before'.
- Preserve the overall structure and section ordering of the original."""

    @classmethod
    def get_version_info(cls) -> dict:
        """Get version information for synthesizer prompts."""
        return {
            "synthesizer_prompts": cls.VERSION,
            "prompts": ["SYSTEM", "SYNTHESIZE"],
        }
