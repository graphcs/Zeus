"""Phase 3: Convergent Synthesis prompts."""


class SynthesisPrompts:
    """Prompts for Phase 3: combining inventor solutions into unified draft."""

    VERSION = "2.0.0"

    SYSTEM = """You are an expert solution synthesizer. Your role is to combine the best elements from multiple independent solution proposals into a single unified solution that is better than any individual proposal.

You must:
1. Not just pick a winner - genuinely combine the best elements
2. Maintain coherence (no Frankenstein solutions)
3. Be explicit about tradeoffs made
4. Track which elements came from which inventor (provenance)
5. Preserve dissenting views for reference
6. Resolve conflicts with clear rationale"""

    SYNTHESIZE = """You have received {num_solutions} independent solutions to the same problem. Your task is to synthesize the best unified solution.

PROBLEM BRIEF:
{problem_brief}

OBJECTIVES:
{objectives}

CONSTRAINTS:
{constraints}

EVALUATION CRITERIA:
{eval_criteria}

{library_context}

INVENTOR SOLUTIONS:
{solutions}

{cross_critiques_section}

SYNTHESIS INSTRUCTIONS:
1. **Compare approaches** - Identify where inventors agree (high confidence) and disagree (needs resolution)
2. **Score elements** - For each major element, which inventor's approach best serves the evaluation criteria?
3. **Identify conflicts** - Where solutions are incompatible, what must be resolved?
4. **Resolve conflicts** - Choose with rationale, preserving dissent
5. **Combine best elements** - Create a unified solution that is strictly better than any individual
6. **Track provenance** - Note which inventor contributed which element
7. **Flag open issues** - What remains unresolved?

Return a JSON object:
{{
    "unified_draft": "The complete synthesized solution in Markdown",
    "provenance": [
        {{"element": "description", "source_inventor": "A|B|C|D", "modified": true/false, "reason": "why"}}
    ],
    "resolved_conflicts": [
        {{"conflict": "description", "resolution": "what was decided", "rationale": "why"}}
    ],
    "open_issues": ["Issues that remain unresolved"]
}}"""

    @classmethod
    def get_version_info(cls) -> dict:
        return {"synthesis_prompts": cls.VERSION}
