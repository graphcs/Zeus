"""Phase 1: Divergent Generation prompts for inventors."""


class InventorPrompts:
    """Prompts for Phase 1: parallel divergent generation by inventors."""

    VERSION = "2.0.0"

    # Per-inventor type configurations
    INVENTOR_TYPES = {
        "foundational": {
            "libraries": ["first_principles", "mental_models"],
            "emphasis": "Ground your solution in durable, fundamental truths. Build from first principles. Ensure every major design decision traces to a principle that will remain valid over time.",
        },
        "competitive": {
            "libraries": ["secrets", "technologies", "methodologies"],
            "emphasis": "Maximize competitive advantage and differentiation. Identify non-obvious truths (secrets) that most participants would dismiss. Leverage emerging technologies and proven methodologies for edge.",
        },
        "comprehensive": {
            "libraries": [],  # ALL libraries - handled specially
            "emphasis": "Achieve thorough coverage. Miss nothing. Systematically address every aspect of the problem using all available libraries and frameworks. Completeness over elegance.",
        },
        "tabula_rasa": {
            "libraries": [],  # NO libraries
            "emphasis": "Reason from first principles only, using NO reference libraries. Think independently. Challenge conventional approaches. What solution would you design with only the problem statement and your own reasoning?",
        },
        "domain_specific": {
            "libraries": [],  # Based on classification
            "emphasis": "Focus deeply on the specific domain of this problem. Apply domain expertise and domain-relevant libraries to produce a solution that fits the problem's unique context.",
        },
    }

    SYSTEM = """You are an inventor tasked with developing a solution to the problem defined in the Problem Brief. Your task is to invent a solution that is comprehensive, well-reasoned, and scores as high as possible against the evaluation framework.

Instructions:
1. Accept the problem statement as given (STRICT treatment)
2. All constraints marked HARD are inviolable; SOFT constraints can be relaxed with justification
3. MUST objectives are non-negotiable
4. Leverage your broader knowledge and creativity beyond provided inputs
5. Make assumptions where needed and document them
6. Do not ask clarifying questions - proceed with available information
7. Deliver a complete solution"""

    GENERATE = """You are Inventor {inventor_id} ({inventor_type}).

PROBLEM BRIEF:
{problem_brief}

OBJECTIVES:
{objectives}

CONSTRAINTS:
{constraints}

{library_context}

OUTPUT SPECIFICATION:
{output_spec}

EVALUATION CRITERIA:
{eval_criteria}

YOUR EMPHASIS:
{emphasis}

Generate a COMPLETE solution addressing the problem. Your solution should include:

1. **Executive Summary** - Solution name, one-sentence summary, core mechanism, key innovations
2. **Solution Design** - Architecture, components, mechanisms, decision logic, risk controls
3. **Pain Point Resolution** - How each problem pain point is addressed
4. **Objectives Alignment** - How each objective is met
5. **Failure Mode Analysis** - What could go wrong and how it's mitigated
6. **Constraint Compliance** - How each constraint is satisfied
7. **Implementation Considerations** - Resources, timeline, dependencies

Return a JSON object:
{{
    "content": "The full solution in Markdown format",
    "assumptions": ["List of assumptions made"],
    "reasoning_trace": "Key reasoning steps and decisions made",
    "libraries_used": ["Names of libraries actually referenced in your solution"]
}}"""

    CROSS_CRITIQUE = """You are Inventor {critic_id} ({critic_type}).

You have produced your own solution. Now review another inventor's solution and provide critique from your perspective.

YOUR OWN SOLUTION APPROACH (summary):
{own_solution_summary}

SOLUTION TO CRITIQUE (from Inventor {target_id}):
{target_solution}

PROBLEM BRIEF:
{problem_brief}

Provide critique in JSON:
{{
    "disagreements": ["Points where you fundamentally disagree with their approach"],
    "missed_elements": ["Important elements they failed to address"],
    "strengths": ["Things they did better than your approach"]
}}

Be honest and specific. Focus on substantive disagreements, not style."""

    @classmethod
    def get_version_info(cls) -> dict:
        return {"inventor_prompts": cls.VERSION}
