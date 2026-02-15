"""Phase 5: Iterative Refinement prompts."""


class RefinementPrompts:
    """Prompts for Phase 5: refining the unified draft based on critique."""

    VERSION = "2.0.0"

    SYSTEM = """You are an expert solution refiner. Your role is to address issues identified by critics while maintaining solution coherence and quality. Focus on the highest-severity issues first."""

    REFINE = """Refine the solution to address the identified issues.

CURRENT SOLUTION DRAFT (version {version}):
{draft}

ISSUES TO ADDRESS (prioritized by severity):
{issues}

PROBLEM BRIEF:
{problem_brief}

CONSTRAINTS (must all be preserved):
{constraints}

{library_context}

INSTRUCTIONS:
1. Address all blocker issues - these MUST be resolved
2. Address major issues where possible
3. Ensure ALL constraints remain satisfied
4. Maintain overall solution coherence
5. Do not introduce new problems while fixing old ones
6. Document what was changed and why

Return a JSON object:
{{
    "refined_draft": "The complete revised solution in Markdown",
    "issues_addressed": ["List of issues that were resolved"],
    "issues_deferred": ["Issues not addressed and why"],
    "changes_made": ["Summary of changes"]
}}"""

    @classmethod
    def get_version_info(cls) -> dict:
        return {"refinement_prompts": cls.VERSION}
