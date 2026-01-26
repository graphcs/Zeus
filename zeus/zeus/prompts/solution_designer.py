"""Prompts for the Solution Designer Team."""


class SolutionDesignerPrompts:
    """Prompts for generating and critiquing Target Solutions."""

    VERSION = "1.0.0"

    SYSTEM = """You are an expert Solution Architect. Your role is to transform Design Briefs into comprehensive Target Solution designs.

A Target Solution should be detailed enough for an implementation team to build from, with clear architecture, component definitions, and rationale for design decisions.

Always maintain these principles:
1. Honor all constraints from the Design Brief - never silently drop them
2. Document architectural decisions with rationale
3. Surface assumptions explicitly
4. Consider security, scalability, and maintainability
5. Identify risks and propose mitigations
6. Make the design testable and verifiable"""

    NORMALIZE = """Analyze the following Design Brief and extract a structured problem representation for solution design.

DESIGN BRIEF:
{prompt}

ADDITIONAL CONSTRAINTS:
{constraints}

CONTEXT:
{context}

Extract and return a JSON object with:
{{
    "problem_statement": "Core problem from the design brief",
    "constraints": ["All constraints - from brief AND additional ones provided"],
    "output_spec": "What the Target Solution should specify",
    "context": {{"requirements": [...], "scope": "...", "success_criteria": [...]}}
}}

Preserve all requirements and constraints from the Design Brief."""

    PLAN = """Create a plan for designing a Target Solution for this problem.

PROBLEM:
{problem_statement}

CONSTRAINTS:
{constraints}

OUTPUT SPEC:
{output_spec}

CONTEXT:
{context}

Return a JSON object with a list of steps:
{{
    "steps": [
        {{"step_number": 1, "description": "What to do", "focus_area": "Which aspect this covers"}}
    ]
}}

Include steps for: architecture design, component definition, interface specification, data modeling, security considerations, risk assessment, and implementation guidance."""

    GENERATE = """Generate a comprehensive Target Solution based on the following:

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

Generate the Target Solution in Markdown format with these sections:
1. **Solution Overview** - High-level summary of the proposed solution
2. **Architecture** - System architecture with components and their relationships
3. **Components** - Detailed specification of each component
   - Purpose
   - Responsibilities
   - Interfaces
   - Dependencies
4. **Data Model** - Key data structures and storage approach
5. **API/Interfaces** - External and internal interfaces
6. **Security Considerations** - Security measures and threat mitigations
7. **Scalability & Performance** - How the solution handles growth
8. **Error Handling** - Failure modes and recovery strategies
9. **Testing Strategy** - How to verify the solution works
10. **Implementation Notes** - Guidance for builders
11. **Constraints Compliance** - How each constraint is satisfied
12. **Assumptions** - What was assumed
13. **Risks & Mitigations** - Identified risks and proposed mitigations
14. **Open Questions** - Unresolved items needing decisions

Return structured metadata:
{{
    "content": "The full Markdown target solution",
    "assumptions": ["List of assumptions made"],
    "uncertainty_flags": ["Areas of uncertainty or decisions deferred"]
}}"""

    CRITIQUE = """Critique the following Target Solution from multiple expert perspectives.

ORIGINAL PROBLEM:
{problem_statement}

CONSTRAINTS:
{constraints}

DESIGN BRIEF CONTEXT:
{context}

TARGET SOLUTION:
{content}

Evaluate from these perspectives:
1. **Requirements Coverage** - Does the solution address all requirements from the brief?
2. **Architecture** - Is the architecture sound, maintainable, and appropriate?
3. **Risk Assessment** - Are risks identified and adequately mitigated?
4. **Security** - Are security considerations thorough?
5. **Compliance** - Does it meet all stated constraints?
6. **Evaluability** - Can the solution be tested and verified?

Also check:
- Are ALL constraints honored? List any violations.
- Are architectural decisions justified with rationale?
- Are there missing components or interfaces?
- Is the solution over-engineered or under-engineered?

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
    "constraint_violations": ["List any constraints not satisfied"],
    "missing_perspectives": ["What important viewpoints were not considered"]
}}

Be thorough but constructive. Only mark as "blocker" issues that would make the solution unimplementable or fundamentally flawed."""

    REVISE = """Revise the Target Solution based on critique feedback.

ORIGINAL SOLUTION:
{content}

CRITIQUE:
{critique}

ORIGINAL CONSTRAINTS (must all be satisfied):
{constraints}

CONTEXT:
{context}

Revise the solution to address the critique issues. Focus on:
1. Fix all blocker issues
2. Address major issues
3. Ensure ALL constraints are satisfied
4. Update assumptions and uncertainty flags
5. Strengthen areas identified as weak

Return:
{{
    "content": "The revised Markdown target solution",
    "assumptions": ["Updated list of assumptions"],
    "uncertainty_flags": ["Updated areas of uncertainty"]
}}"""

    @classmethod
    def get_version_info(cls) -> dict:
        """Get version information for all prompts."""
        return {
            "solution_designer_prompts": cls.VERSION,
            "prompts": ["SYSTEM", "NORMALIZE", "PLAN", "GENERATE", "CRITIQUE", "REVISE"],
        }
