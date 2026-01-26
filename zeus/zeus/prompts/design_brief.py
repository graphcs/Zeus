"""Prompts for the Design Brief Team."""


class DesignBriefPrompts:
    """Prompts for generating and critiquing Design Briefs."""

    VERSION = "1.0.0"

    SYSTEM = """You are an expert Design Brief architect. Your role is to transform raw ideas and problem statements into structured, comprehensive Design Briefs.

A Design Brief should be clear, actionable, and complete enough for a solution design team to work from without needing to return for clarification.

Always maintain these principles:
1. Never silently drop constraints - all user constraints must appear in the output
2. Surface assumptions explicitly - when requirements are unclear, state what you assumed
3. Flag uncertainties - identify areas that need clarification
4. Be specific and measurable where possible
5. Consider feasibility and scope realistically"""

    NORMALIZE = """Analyze the following input and extract a structured problem representation.

INPUT:
{prompt}

CONSTRAINTS PROVIDED:
{constraints}

CONTEXT:
{context}

Extract and return a JSON object with:
{{
    "problem_statement": "Clear, concise statement of the core problem to solve",
    "constraints": ["List all constraints - NEVER drop any user-provided constraints"],
    "output_spec": "What the Design Brief should specify",
    "context": {{"key": "value pairs of relevant context"}}
}}

Be thorough. If something is ambiguous, note it but don't omit it."""

    PLAN = """Create a plan for generating a Design Brief for this problem.

PROBLEM:
{problem_statement}

CONSTRAINTS:
{constraints}

OUTPUT SPEC:
{output_spec}

Return a JSON object with a list of steps:
{{
    "steps": [
        {{"step_number": 1, "description": "What to do", "focus_area": "Which aspect this covers"}}
    ]
}}

Include steps for: problem analysis, requirements gathering, scope definition, success criteria, constraints documentation, and assumptions listing."""

    GENERATE = """Generate a comprehensive Design Brief based on the following:

PROBLEM STATEMENT:
{problem_statement}

CONSTRAINTS:
{constraints}

OUTPUT SPECIFICATION:
{output_spec}

CONTEXT:
{context}

PLAN TO FOLLOW:
{plan}

Generate the Design Brief in Markdown format with these sections:
1. **Executive Summary** - Brief overview of the problem and proposed solution direction
2. **Problem Statement** - Detailed problem description
3. **Goals & Objectives** - What success looks like, with measurable criteria where possible
4. **Scope** - What's in scope and explicitly out of scope
5. **Requirements** - Functional and non-functional requirements
6. **Constraints** - All constraints (MUST include all user-provided constraints)
7. **Assumptions** - What you assumed when information was unclear
8. **Success Criteria** - How to measure if the solution meets the brief
9. **Open Questions** - Areas needing clarification

Also return structured metadata:
{{
    "content": "The full Markdown design brief",
    "assumptions": ["List of assumptions made"],
    "uncertainty_flags": ["Areas of uncertainty or things needing clarification"]
}}"""

    CRITIQUE = """Critique the following Design Brief from multiple perspectives.

ORIGINAL PROBLEM:
{problem_statement}

CONSTRAINTS:
{constraints}

DESIGN BRIEF:
{content}

Evaluate from these perspectives:
1. **Completeness** - Are all necessary sections present and sufficiently detailed?
2. **Clarity** - Is the brief unambiguous and actionable?
3. **Measurability** - Are success criteria and requirements measurable?
4. **Scope** - Is the scope well-defined and appropriate?
5. **Feasibility** - Is what's described realistic and achievable?

Also check:
- Are ALL user constraints preserved? List any that were dropped.
- Are assumptions reasonable and clearly stated?
- Are there perspectives or considerations missing?

Return a JSON object:
{{
    "issues": [
        {{
            "role": "Which perspective found this",
            "severity": "blocker|major|minor",
            "description": "What the issue is",
            "suggested_fix": "How to fix it (or null)"
        }}
    ],
    "constraint_violations": ["List any user constraints not reflected in the brief"],
    "missing_perspectives": ["What important viewpoints were not considered"]
}}

Be thorough but fair. Only mark as "blocker" issues that would make the brief unusable."""

    REVISE = """Revise the Design Brief based on critique feedback.

ORIGINAL BRIEF:
{content}

CRITIQUE:
{critique}

ORIGINAL CONSTRAINTS (must all be preserved):
{constraints}

Revise the brief to address the critique issues. Focus on:
1. Fix all blocker issues
2. Address major issues where possible
3. Ensure ALL original constraints are preserved
4. Keep assumptions and uncertainty flags updated

Return:
{{
    "content": "The revised Markdown design brief",
    "assumptions": ["Updated list of assumptions"],
    "uncertainty_flags": ["Updated areas of uncertainty"]
}}"""

    @classmethod
    def get_version_info(cls) -> dict:
        """Get version information for all prompts."""
        return {
            "design_brief_prompts": cls.VERSION,
            "prompts": ["SYSTEM", "NORMALIZE", "PLAN", "GENERATE", "CRITIQUE", "REVISE"],
        }
