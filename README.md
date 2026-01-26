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
pip install -e .
```

### Configuration

Set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="your-api-key"
```

---

## Usage

### Generate a Design Brief

Transform a raw idea into a structured design document:

```bash
zeus brief "Build a system that automatically reviews code changes"
```

With constraints:

```bash
zeus brief "Build a code review system" \
  --constraint "Must support async operations" \
  --constraint "No external dependencies beyond the LLM"
```

Save output to file:

```bash
zeus brief "Build a notification system" --output design_brief.md
```

### Generate a Target Solution

Transform a Design Brief into a comprehensive solution:

```bash
zeus solution --file design_brief.md
```

With additional constraints:

```bash
zeus solution --file design_brief.md --constraint "Must use PostgreSQL"
```

### View Run History

```bash
zeus history              # List recent runs
zeus history --limit 20   # Show more runs
zeus show <run-id>        # View details of a specific run
```

---

## Example

### Input

```bash
zeus brief "Design a rate limiting system for an API gateway"
```

### Output

The system produces a structured Design Brief containing:

- **Problem Statement**: Normalized and clarified problem definition
- **Objectives**: What success looks like
- **Constraints**: Hard requirements the solution must respect
- **Output Specification**: Expected deliverables
- **Assumptions**: Explicit assumptions made during analysis
- **Known Issues**: Limitations, uncertainties, or areas needing clarification

Every run also returns a `run_id` for full traceability. The complete execution history, including intermediate artifacts and critique results, is persisted to `zeus/run_records/`.

---

## Programmatic Usage

```python
import asyncio
from zeus.core.run_controller import run_zeus

async def main():
    response = await run_zeus(
        prompt="Build a task management system",
        mode="brief",
        constraints=["Must support offline mode"],
    )

    print(response.output)
    print("Assumptions:", response.assumptions)
    print("Known Issues:", response.known_issues)
    print("Run ID:", response.run_id)

asyncio.run(main())
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
│   ├── cli.py                  # Command-line interface
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
pytest                          # Run all tests
pytest tests/test_schemas.py    # Run specific test file
```

---

## License

MIT
