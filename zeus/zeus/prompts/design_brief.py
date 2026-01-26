"""Prompts for the Design Brief Team."""


class DesignBriefPrompts:
    """Prompts for generating and critiquing Design Briefs."""

    VERSION = "1.1.0"  # V1: Added tradeoffs and issue categories

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

Also document any significant TRADEOFFS you made - decisions where you chose one approach over another.

Return structured metadata:
{{
    "content": "The full Markdown design brief",
    "assumptions": ["List of assumptions made"],
    "uncertainty_flags": ["Areas of uncertainty or things needing clarification"],
    "tradeoffs": [
        {{
            "chose": "What you chose",
            "over": "What you rejected",
            "rationale": "Why you made this choice",
            "impact": "low|medium|high"
        }}
    ]
}}"""

    CRITIQUE = """Critique the following Design Brief from multiple perspectives.

ORIGINAL PROBLEM:
{problem_statement}

CONSTRAINTS:
{constraints}

DESIGN BRIEF:
{content}

You MUST evaluate from ALL six required perspectives:

1. **scope** - Requirements and scope coverage
   - Are all necessary sections present and sufficiently detailed?
   - Is the scope well-defined with clear boundaries?
   - Are requirements complete and unambiguous?

2. **architecture** - Technical architecture and feasibility
   - Is the proposed approach technically sound?
   - Is what's described realistic and achievable?
   - Are there architectural gaps or inconsistencies?

3. **risk** - Risk assessment
   - What are the key risks and uncertainties?
   - Are there mitigation strategies?
   - What could go wrong?

4. **security** - Security and operations considerations
   - Are there security implications to consider?
   - What operational concerns exist?
   - Are there data privacy or access control issues?

5. **compliance** - Compliance with constraints
   - Are ALL user constraints preserved? List any that were dropped.
   - Does the brief comply with stated requirements?
   - Are there regulatory or policy considerations?

6. **evaluation** - Evaluation and success criteria
   - Are success criteria measurable?
   - How will we know if the solution works?
   - Are there clear acceptance criteria?

Also check:
- Are assumptions reasonable and clearly stated?
- Are there perspectives or considerations missing beyond the six required?

Return a JSON object:
{{
    "issues": [
        {{
            "role": "scope|architecture|risk|security|compliance|evaluation",
            "severity": "blocker|major|minor",
            "category": "correctness|completeness|clarity|feasibility|maintainability|performance|security|compliance",
            "description": "What the issue is",
            "suggested_fix": "How to fix it (or null)"
        }}
    ],
    "constraint_violations": ["List any user constraints not reflected in the brief"],
    "missing_perspectives": ["Any perspectives beyond the 6 that were not considered"]
}}

Issue categories:
- correctness: Logical or factual errors
- completeness: Missing required elements
- clarity: Ambiguous or unclear content
- feasibility: Implementation concerns
- maintainability: Long-term health concerns
- performance: Efficiency concerns
- security: Security vulnerabilities
- compliance: Policy/regulation issues

IMPORTANT: You must provide at least one issue or observation from EACH of the 6 perspectives, even if it's just to note that the perspective was adequately addressed (as a "minor" observation).

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
    "uncertainty_flags": ["Updated areas of uncertainty"],
    "tradeoffs": [
        {{
            "chose": "What you chose",
            "over": "What you rejected",
            "rationale": "Why you made this choice",
            "impact": "low|medium|high"
        }}
    ]
}}"""

    @classmethod
    def get_version_info(cls) -> dict:
        """Get version information for all prompts."""
        return {
            "design_brief_prompts": cls.VERSION,
            "prompts": ["SYSTEM", "NORMALIZE", "PLAN", "GENERATE", "CRITIQUE", "REVISE"],
        }
