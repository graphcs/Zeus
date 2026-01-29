# Zeus

**A Multi-Agent Design System for Structured Problem Solving**

Zeus transforms raw ideas into structured Design Briefs and comprehensive Target Solutions through an automated, critique-led pipeline. Every output is independently critiqued, fully traceable, and includes explicit assumptions and known limitations.

---

## Overview

Zeus operates as a Design Team Agent with two primary modes:

| Mode | Input | Output |
|------|-------|--------|
| **Brief** | Raw idea or problem statement | Structured Design Brief |
| **Solution** | Design Brief | Comprehensive Target Solution |

The system enforces a bounded, linear pipeline where every generation undergoes multi-perspective critique. Automatic revision occurs only for blocker-level issues, with a maximum of one revision per run.

---

## Installation

```bash
cd zeus
uv sync
```

### Configuration

Set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="your-api-key"
```

---

## Usage

```bash
uv run streamlit zeus/ui.py
``` 

---

## Pipeline Architecture

```
Normalize → Plan → Generate v1 → Critique v1 → [Revise → Critique v2] → Assemble → Log
```

1. **Normalize**: Convert raw input into a structured `NormalizedProblem`
2. **Plan**: Create a linear execution plan
3. **Generate**: Produce initial candidate with assumptions
4. **Critique**: Multi-perspective review (scope, architecture, risk, security, compliance, evaluation)
5. **Revise** (conditional): Fix blocker/major issues (max 1 revision)
6. **Assemble**: Produce final output with assumptions and known issues
7. **Log**: Persist complete `RunRecord` for traceability

---

## System Guarantees

- **Critique is mandatory**: Every generation is critiqued without exception
- **Full traceability**: Every run produces a unique `run_id` and persisted record
- **Transparency**: `assumptions[]` and `known_issues[]` are always present
- **Constraint preservation**: Constraints are never silently dropped
- **Bounded iteration**: Maximum one revision loop enforced
- **Graceful degradation**: Failures produce best-effort output with logged errors

---

## Project Structure

```
zeus/
├── zeus/
│   ├── cli.py   # Command Line Interface
|   ├── ui.py    # Streamlit UI            
│   ├── core/
│   │   ├── run_controller.py   # Pipeline orchestration
│   │   ├── normalizer.py       # Input normalization
│   │   ├── planner.py          # Linear planning
│   │   ├── generator.py        # LLM-based generation
│   │   ├── critic.py           # Multi-view critique
│   │   ├── assembler.py        # Output assembly
│   │   └── persistence.py      # RunRecord storage
│   ├── llm/
│   │   └── openrouter.py       # OpenRouter API client
│   ├── models/
│   │   └── schemas.py          # Pydantic data models
│   └── prompts/
│       ├── design_brief.py     # Brief mode prompts
│       └── solution_designer.py # Solution mode prompts
├── run_records/                # Persisted run history (JSON)
└── tests/                      # Test suite
```

---

## Testing

```bash
cd zeus
pytest                          # Run all tests
pytest tests/test_schemas.py    # Run specific test file
```

### Golden Scenarios

Zeus includes golden scenario tests that validate the MVP behavioral contract. These tests make real LLM calls and verify end-to-end system behavior.

**Requirements:**
- `OPENROUTER_API_KEY` environment variable must be set
- Tests may take several minutes to complete (each scenario involves 4-6 LLM calls)

**Run all golden scenarios:**

```bash
export OPENROUTER_API_KEY="your-api-key"
cd zeus
pytest tests/test_golden_scenarios.py -v --timeout=600
```

**Run a specific scenario:**

```bash
pytest tests/test_golden_scenarios.py::TestGoldenScenarios::test_case_1_api_design -v
```

**Available scenarios:**

| Test | Description | Expected Behavior |
|------|-------------|-------------------|
| `test_case_1_api_design` | API design with constraints | No revision, constraints respected |
| `test_case_2_conflicting_constraints` | Conflicting architectural constraints | Surfaces conflict in known_issues |
| `test_case_3_structured_output` | Structured JSON output request | Best-effort output |
| `test_case_4_underspecified_requirements` | Under-specified requirements | Infers assumptions |
| `test_case_5_multiview_coverage` | Multi-view critique coverage | 6-perspective critique |
| `test_case_6_failure_modes` | Failure mode documentation | Includes failure table |
| `test_case_7_constraint_enforcement` | Section title constraints | Required sections present |

**Test results:** See `tests/golden_scenarios_results.md` for detailed results from the last test run.

---

## MVP Compliance

Zeus implements the bounded, critique-led solver defined in the [MVP Brief V0.3](docs/3.%20MVP_Brief_V0_Bounded_Critique_Led_Solver_v0.3_with_mermaid.md).

### System Invariants

All invariants from §6 of the MVP spec are enforced:

1. **Critique mandatory** - At least one critic step runs on every generation
2. **Traceability** - Every run has a unique `run_id` and persisted `RunRecord`
3. **Transparency fields** - `assumptions[]` and `known_issues[]` always present
4. **No silent constraint loss** - Constraints preserved; ambiguities surfaced
5. **Budget enforcement** - Max 1 revision loop, configurable call caps and timeouts
6. **Graceful degradation** - Failures yield best-effort response + logged incident
7. **Generator/Critic separable** - Components can be replaced independently
8. **Provenance recorded** - Model + prompt versions in RunRecord
9. **Append-only RunRecords** - No in-place mutation

### Multi-View Critique

Every generation is critiqued from 6 required perspectives:

- **scope** - Requirements/scope coverage
- **architecture** - Technical architecture review
- **risk** - Risk assessment
- **security** - Security/ops considerations
- **compliance** - Constraint compliance
- **evaluation** - Evaluation/experimentation readiness

