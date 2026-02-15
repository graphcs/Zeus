"""Phase 0: Intake & Problem Understanding prompts."""


class IntakePrompts:
    """Prompts for Phase 0: normalizing input into a ProblemBrief."""

    VERSION = "2.0.0"

    SYSTEM = """You are an expert problem analyst. Your role is to normalize raw problem statements into structured, clear problem briefs that multiple independent solution inventors can work from.

You must:
1. Never silently drop constraints - all user constraints must appear in output
2. Surface implicit assumptions explicitly
3. Classify the problem type to inform inventor configuration
4. Flag ambiguities that need resolution
5. Preserve objectives with their priority levels"""

    NORMALIZE = """Analyze the following input and produce a structured Problem Brief.

PROBLEM STATEMENT:
{prompt}

OBJECTIVES:
{objectives}

CONSTRAINTS:
{constraints}

CONTEXT:
{context}

OUTPUT SPECIFICATION (if provided):
{output_spec}

EVALUATION CRITERIA (if provided):
{eval_criteria}

You must produce a JSON object with:
{{
    "problem_statement": "Clear, normalized restatement of the core problem",
    "objectives": ["All objectives, preserving user-provided ones first"],
    "constraints": ["All constraints - NEVER drop any user-provided constraints"],
    "classification": {{
        "problem_type": "strategy_design|system_architecture|process_design|product_design|general",
        "uncertainty_level": "low|medium|high",
        "key_domains": ["Relevant domains"],
        "recommended_library_emphasis": ["Which libraries matter most for this problem"]
    }},
    "implicit_assumptions": ["Assumptions you are making about the problem"],
    "ambiguities": ["Areas that are unclear or could be interpreted multiple ways"],
    "context": {{"key": "value pairs of parsed context"}}
}}

Be thorough. Surface everything implicit. Do not omit anything ambiguous."""

    @classmethod
    def get_version_info(cls) -> dict:
        return {"intake_prompts": cls.VERSION}
