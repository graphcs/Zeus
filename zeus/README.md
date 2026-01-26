# Zeus - Design Team Agent

Zeus is a Design Team agent for multi-agent systems. It transforms raw ideas into structured Design Briefs, and Design Briefs into comprehensive Target Solutions.

## Features

- **Design Brief Team**: Takes a raw idea/problem → produces a structured Design Brief
- **Solution Designer Team**: Takes a Design Brief → produces a Target Design Solution
- **Multi-view Critique**: Every generation is critiqued from multiple perspectives
- **Automatic Revision**: Blocker issues trigger automatic revision (max 1 revision)
- **Full Traceability**: Every run is persisted with complete history

## Installation

```bash
# Clone and install
cd zeus
pip install -e .

# Or install dependencies directly
pip install httpx pydantic typer python-dotenv rich
```

## Configuration

Set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## Usage

### Generate a Design Brief

```bash
# From an idea
zeus brief "Build a system that automatically reviews code changes"

# With constraints
zeus brief "Build a code review system" \
  --constraint "Must be async" \
  --constraint "No external dependencies"

# Save to file
zeus brief "Build a notification system" --output design_brief.md
```

### Generate a Target Solution

```bash
# From a design brief file
zeus solution --file design_brief.md

# From text directly
zeus solution "$(cat design_brief.md)"

# With additional constraints
zeus solution --file design_brief.md --constraint "Must use PostgreSQL"
```

### View Run History

```bash
# List recent runs
zeus history

# Show details of a specific run
zeus show <run-id>
```

## Architecture

```
zeus/
├── zeus/
│   ├── cli.py              # CLI interface
│   ├── core/
│   │   ├── run_controller.py    # Pipeline orchestration
│   │   ├── normalizer.py        # Input normalization
│   │   ├── planner.py           # Linear planning
│   │   ├── generator.py         # LLM-based generation
│   │   ├── critic.py            # Multi-view critique
│   │   ├── assembler.py         # Output assembly
│   │   └── persistence.py       # RunRecord storage
│   ├── llm/
│   │   └── openrouter.py        # OpenRouter client
│   ├── models/
│   │   └── schemas.py           # Pydantic data models
│   └── prompts/
│       ├── design_brief.py      # Design Brief prompts
│       └── solution_designer.py # Solution Designer prompts
└── run_records/                 # Persisted run records (JSON)
```

## Pipeline Flow

1. **Normalize**: Convert input to structured `NormalizedProblem`
2. **Plan**: Create linear plan for generation
3. **Generate v1**: Produce initial candidate
4. **Critique v1**: Multi-view critique (always runs)
5. **Revise** (if blockers): Fix blocker issues
6. **Critique v2** (if revised): Re-evaluate
7. **Assemble**: Produce final output with assumptions and known issues

## Key Invariants

- Critique runs on every generation
- Every run has a run_id and persisted RunRecord
- `assumptions[]` and `known_issues[]` always present in output
- Constraints never silently dropped
- Max 1 revision loop enforced
- Graceful degradation on LLM failures

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

## License

MIT
