"""Phase 4: Library-Informed Critique prompts."""


class LibraryCritiquePrompts:
    """Prompts for Phase 4: critiquing unified draft through library lenses."""

    VERSION = "2.0.0"

    SYSTEM = """You are an expert critic evaluating a solution through the lens of a specific reference library. Your role is to systematically validate the solution against the library's principles, identifying what's embodied, what's violated, and what's missing."""

    # Per-library critique prompts with specific questions
    CRITIQUE_TEMPLATES = {
        "first_principles": {
            "name": "First Principles Critic",
            "questions": [
                "Does the solution violate any first principles in the library?",
                "Which principles are clearly embodied in the solution?",
                "Which principles are missing and should be incorporated?",
                "Are the solution's foundational assumptions durable over time?",
                "Does the solution depend on temporary conditions rather than fundamental truths?",
            ],
        },
        "secrets": {
            "name": "Secrets Critic",
            "questions": [
                "Which secrets from the library are embedded in the solution?",
                "Which secrets are missing and could strengthen the solution?",
                "Is the competitive edge defensible?",
                "How will secrets erode over time, and is there a refresh mechanism?",
                "Does the solution represent Zero-to-One innovation or incremental improvement?",
            ],
        },
        "mental_models": {
            "name": "Mental Models Critic",
            "questions": [
                "What cognitive biases might be present in the solution?",
                "What mental models from the library would improve the solution?",
                "Are there blind spots the solution hasn't considered?",
                "Are multiple mental models used to compensate for individual model limitations?",
                "Do any mental models produce conflicting conclusions?",
            ],
        },
        "observations": {
            "name": "Observations Critic",
            "questions": [
                "Does the solution align with current observations and trends?",
                "What signals or trends were missed?",
                "Which observations are the solution most dependent on?",
                "Are transient observations confused with durable ones?",
            ],
        },
        "technologies": {
            "name": "Technologies Critic",
            "questions": [
                "Is the chosen technology stack mature and appropriate?",
                "Are there better technology alternatives?",
                "What are the technology dependencies and risks?",
                "Is the solution critically dependent on any single technology?",
                "Are experimental technologies properly risk-assessed?",
            ],
        },
        "methodologies": {
            "name": "Methodologies Critic",
            "questions": [
                "Does the process follow best practices from the library?",
                "Are there methodology gaps?",
                "Are methodologies adapted appropriately to this context?",
                "What are the known limitations of the chosen methodologies?",
            ],
        },
    }

    CRITIQUE = """You are the {critic_name}.

UNIFIED SOLUTION DRAFT:
{draft}

REFERENCE LIBRARY ({library_name}):
{library_content}

EVALUATION CRITERIA:
{eval_criteria}

Evaluate the solution through the lens of this library. Answer these questions:
{questions}

Return a JSON object:
{{
    "library_name": "{library_name}",
    "violations": ["Principles/elements from the library that the solution violates"],
    "embodied": ["Principles/elements from the library that are well-embodied"],
    "missing": ["Principles/elements from the library that should be incorporated"],
    "coverage_pct": 0-100,
    "issues": [
        {{
            "severity": "blocker|major|minor",
            "description": "What the issue is",
            "suggested_fix": "How to fix it (or null)"
        }}
    ]
}}

Be thorough but fair. Only mark as "blocker" issues that would make the solution fundamentally flawed."""

    @classmethod
    def get_version_info(cls) -> dict:
        return {"library_critique_prompts": cls.VERSION}
