"""Phase 6: Output Assembly prompts."""


class AssemblyPrompts:
    """Prompts for Phase 6: formatting final deliverables."""

    VERSION = "2.0.0"

    SYSTEM = """You are an expert document assembler. Your role is to format a solution into the required deliverable structure, ensuring completeness, consistency, and evaluability."""

    ASSEMBLE = """Format the following solution into the 5 required deliverables per the Output Specification.

FINAL SOLUTION:
{solution}

PROBLEM BRIEF:
{problem_brief}

OBJECTIVES:
{objectives}

CONSTRAINTS:
{constraints}

OUTPUT SPECIFICATION:
{output_spec}

EVALUATION CRITERIA:
{eval_criteria}

PROVENANCE DATA:
{provenance}

ALTERNATIVE APPROACHES:
{alternatives}

REFINEMENT HISTORY:
{refinement_history}

ASSUMPTIONS COLLECTED:
{assumptions}

Format into these 5 deliverables:

1. **Executive Summary** (max 2 pages):
   - Solution Name, One-Sentence Summary, Evaluation Summary, Problem Addressed,
   - Core Mechanism, Key Innovations, Initial Scope vs Long-term Vision,
   - Critical Dependencies, Expected Outcomes

2. **Solution Design Document**:
   - Solution Overview (with Mermaid architecture diagram)
   - Pain Point Resolution, Objectives Alignment, Focused Mastery Design,
   - Adaptability Design, Mechanism Design, Failure Mode Analysis,
   - Constraint Compliance, Implementation Considerations

3. **Foundation Documentation**:
   - Consolidated Inputs Inventory, First Principles Analysis,
   - Secrets Analysis, Observations Analysis, Technologies Analysis,
   - Methodologies Analysis, Mental Models Analysis, Key Assumptions Inventory

4. **Self-Evaluation Scorecard**:
   - Score each of the 13 criteria (1-5) with justification
   - HARD constraint compliance (PASS/FAIL)
   - Disqualification check
   - Identified weaknesses

5. **Run Log**:
   - Process Summary, Input Utilization, Assumptions Log,
   - Missing Inputs

Return a JSON object:
{{
    "executive_summary": "Deliverable 1 content in Markdown",
    "solution_design_document": "Deliverable 2 content in Markdown",
    "foundation_documentation": "Deliverable 3 content in Markdown",
    "self_evaluation_scorecard": "Deliverable 4 content in Markdown",
    "run_log": "Deliverable 5 content in Markdown",
    "evaluation": {{
        "criteria_scores": [
            {{"section": "1.1", "name": "Capital Preservation", "objective": "1 (MUST)", "raw_score": 1-5, "weight": 5.0, "justification": "..."}},
            {{"section": "1.2", "name": "Return Competitiveness", "objective": "2 (MUST)", "raw_score": 1-5, "weight": 5.0, "justification": "..."}},
            {{"section": "1.3", "name": "Human Cognitive Efficiency", "objective": "7 (MUST)", "raw_score": 1-5, "weight": 5.0, "justification": "..."}},
            {{"section": "2.1", "name": "First Principles Foundation", "objective": "3 (MUST)", "raw_score": 1-5, "weight": 5.0, "justification": "..."}},
            {{"section": "2.2", "name": "Secrets & Differentiated Innovation", "objective": "4 (MUST)", "raw_score": 1-5, "weight": 5.0, "justification": "..."}},
            {{"section": "2.3", "name": "Focused Mastery", "objective": "5 (MUST)", "raw_score": 1-5, "weight": 5.0, "justification": "..."}},
            {{"section": "2.4", "name": "Adaptability", "objective": "6 (MUST)", "raw_score": 1-5, "weight": 5.0, "justification": "..."}},
            {{"section": "3.1", "name": "Simplicity", "objective": "8 (COULD)", "raw_score": 1-5, "weight": 2.0, "justification": "..."}},
            {{"section": "3.2", "name": "Human Input Capacity", "objective": "9 (COULD)", "raw_score": 1-5, "weight": 2.0, "justification": "..."}},
            {{"section": "3.3", "name": "Transparency", "objective": "10 (COULD)", "raw_score": 1-5, "weight": 2.0, "justification": "..."}},
            {{"section": "4.3", "name": "Crypto-Native", "objective": "C3 (SOFT)", "raw_score": 1-5, "weight": 1.0, "justification": "..."}},
            {{"section": "4.4", "name": "Regulatory Environment", "objective": "C4 (SOFT)", "raw_score": 1-5, "weight": 1.0, "justification": "..."}},
            {{"section": "4.5", "name": "Capital Requirements", "objective": "C5 (SOFT)", "raw_score": 1-5, "weight": 1.0, "justification": "..."}}
        ],
        "hard_constraints": [
            {{"constraint_id": "C1", "name": "Team Scale", "passed": true/false, "notes": "..."}},
            {{"constraint_id": "C2", "name": "Digital and Remote", "passed": true/false, "notes": "..."}}
        ],
        "identified_weaknesses": ["Weakest areas and why"]
    }}
}}"""

    @classmethod
    def get_version_info(cls) -> dict:
        return {"assembly_prompts": cls.VERSION}
