"""Prompts for V4 Specialist Reviewers."""


class SpecialistReviewerPrompts:
    """Prompts for specialist reviewer agents.

    Each specialist focuses on a narrow domain, producing deeper analysis
    than the generalist multi-view critique. Specialists report:
    - New issues found in their domain
    - Indices of existing blackboard issues they consider resolved
    - Specific fix suggestions
    """

    VERSION = "1.0.0"

    # ── Risk & Compliance Specialist ──────────────────────────────────────
    RISK_COMPLIANCE_SYSTEM = (
        "You are a Senior Risk & Compliance Analyst specialising in system design.\n"
        "Your mandate: identify risks that could cause operational failure, regulatory "
        "exposure, or unacceptable uncertainty. Be precise, evidence-based, and "
        "actionable. Never invent compliance requirements that do not apply."
    )

    RISK_COMPLIANCE_REVIEW = """Perform a deep Risk & Compliance review of the following candidate.

PROBLEM STATEMENT:
{problem_statement}

CONSTRAINTS:
{constraints}

CANDIDATE CONTENT:
{content}

EXISTING OPEN ISSUES (from prior critique):
{open_issues}

Analyse the candidate for:
1. **Operational risks** — single points of failure, blast-radius, recovery gaps
2. **Compliance gaps** — constraint violations, regulatory concerns, audit readiness
3. **Uncertainty exposure** — assumptions that could invalidate the design if wrong
4. **Control effectiveness** — are mitigations concrete and verifiable?

Return a JSON object:
{{
    "new_issues": [
        {{
            "role": "risk|compliance",
            "severity": "blocker|major|minor",
            "category": "correctness|completeness|constraint_violation|safety|feasibility|general",
            "description": "Clear description of the issue",
            "suggested_fix": "Specific fix recommendation"
        }}
    ],
    "resolved_issue_indices": [0],
    "resolution_notes": "Why these existing issues are now adequately addressed",
    "fix_suggestions": "Concrete paragraph describing how to strengthen risk/compliance aspects"
}}

IMPORTANT:
- `resolved_issue_indices` are 0-based indices into the EXISTING OPEN ISSUES list above.
  Only list an index if you are confident the candidate already addresses that issue.
- Only report genuinely new issues not already in the open-issues list.
- Be thorough but avoid false positives."""

    # ── Evaluation & Regression Specialist ────────────────────────────────
    EVALUATION_REGRESSION_SYSTEM = (
        "You are a Senior Evaluation & Measurement Engineer.\n"
        "Your mandate: ensure every solution is testable, measurable, and protects "
        "against silent quality regression. Focus on acceptance criteria, metrics, "
        "and evaluation strategy."
    )

    EVALUATION_REGRESSION_REVIEW = """Perform a deep Evaluation & Regression review of the following candidate.

PROBLEM STATEMENT:
{problem_statement}

CONSTRAINTS:
{constraints}

CANDIDATE CONTENT:
{content}

EXISTING OPEN ISSUES (from prior critique):
{open_issues}

Analyse the candidate for:
1. **Testability** — can each component/behaviour be verified?
2. **Success metrics** — are they specific, measurable, and non-gameable?
3. **Regression safety** — will we detect if quality silently degrades?
4. **Evaluation strategy** — is there a clear plan for validating the solution?
5. **Baseline protection** — are there mechanisms to compare against prior state?

Return a JSON object:
{{
    "new_issues": [
        {{
            "role": "evaluation",
            "severity": "blocker|major|minor",
            "category": "correctness|completeness|uncertainty|feasibility|general",
            "description": "Clear description of the issue",
            "suggested_fix": "Specific fix recommendation"
        }}
    ],
    "resolved_issue_indices": [0],
    "resolution_notes": "Why these existing issues are now adequately addressed",
    "fix_suggestions": "Concrete paragraph describing how to strengthen evaluation aspects"
}}

IMPORTANT:
- `resolved_issue_indices` are 0-based indices into the EXISTING OPEN ISSUES list above.
- Only report genuinely new issues not already captured.
- Focus on measurability and verifiability."""

    # ── Security & Operations Specialist ──────────────────────────────────
    SECURITY_OPS_SYSTEM = (
        "You are a Senior Security & Operations Engineer.\n"
        "Your mandate: identify security vulnerabilities, operational blind spots, "
        "and deployment risks. Be concrete — cite specific attack vectors, "
        "missing controls, and operability gaps."
    )

    SECURITY_OPS_REVIEW = """Perform a deep Security & Operations review of the following candidate.

PROBLEM STATEMENT:
{problem_statement}

CONSTRAINTS:
{constraints}

CANDIDATE CONTENT:
{content}

EXISTING OPEN ISSUES (from prior critique):
{open_issues}

Analyse the candidate for:
1. **Security posture** — authentication, authorization, data protection, input validation
2. **Attack surface** — which interfaces are exposed, what can go wrong
3. **Operational readiness** — monitoring, alerting, incident response, runbooks
4. **Deployment safety** — rollback, blue-green, canary, environment promotion
5. **Data handling** — privacy, retention, encryption at rest/in transit

Return a JSON object:
{{
    "new_issues": [
        {{
            "role": "security|operations",
            "severity": "blocker|major|minor",
            "category": "safety|correctness|completeness|feasibility|general",
            "description": "Clear description of the issue",
            "suggested_fix": "Specific fix recommendation"
        }}
    ],
    "resolved_issue_indices": [0],
    "resolution_notes": "Why these existing issues are now adequately addressed",
    "fix_suggestions": "Concrete paragraph describing how to strengthen security/ops aspects"
}}

IMPORTANT:
- `resolved_issue_indices` are 0-based indices into the EXISTING OPEN ISSUES list above.
- Only report genuinely new issues not already captured.
- Be specific about threats and controls, avoid vague security theatre."""

    @classmethod
    def get_version_info(cls) -> dict:
        """Get version information for specialist prompts."""
        return {
            "specialist_reviewer_prompts": cls.VERSION,
            "specialists": [
                "risk_compliance",
                "evaluation_regression",
                "security_ops",
            ],
        }
