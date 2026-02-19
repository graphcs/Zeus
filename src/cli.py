"""CLI interface for Zeus."""

import asyncio
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from src.core.run_controller import run_zeus
from src.core.persistence import Persistence
from src.models.schemas import UsageStats
from src.utils.read_file import read_file_content as read_file_utils
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(
    name="zeus",
    help="Zeus - Multi-Inventor Design System",
    add_completion=False,
)
console = Console()


def print_response(response) -> None:
    """Print the Zeus response with evaluation scorecard."""
    # Main output
    console.print(Markdown(response.output))

    # Evaluation Scorecard
    console.print()
    score_pct = response.score_percentage
    if score_pct >= 85:
        score_color = "green"
    elif score_pct >= 70:
        score_color = "cyan"
    elif score_pct >= 55:
        score_color = "yellow"
    else:
        score_color = "red"

    dq_status = "[red]DISQUALIFIED[/red]" if response.disqualified else "[green]QUALIFIED[/green]"

    eval_lines = [
        f"Score: [{score_color}]{response.total_score:.1f} / {response.max_score:.0f} ({score_pct:.1f}%)[/{score_color}]",
        f"Status: {dq_status}",
    ]

    if response.scorecard:
        # Show per-criterion scores
        eval_lines.append("")
        eval_lines.append("[bold]Criteria Scores:[/bold]")
        for cs in response.scorecard.criteria_scores:
            eval_lines.append(f"  {cs.section} {cs.name}: {cs.raw_score}/5 (x{cs.weight} = {cs.weighted_score:.1f})")

        if response.scorecard.hard_constraints:
            eval_lines.append("")
            eval_lines.append("[bold]HARD Constraints:[/bold]")
            for hc in response.scorecard.hard_constraints:
                status = "[green]PASS[/green]" if hc.passed else "[red]FAIL[/red]"
                eval_lines.append(f"  {hc.constraint_id} {hc.name}: {status}")

        if response.scorecard.disqualification_reasons:
            eval_lines.append("")
            eval_lines.append("[red][bold]Disqualification Reasons:[/bold][/red]")
            for reason in response.scorecard.disqualification_reasons:
                eval_lines.append(f"  - {reason}")

        if response.scorecard.identified_weaknesses:
            eval_lines.append("")
            eval_lines.append("[bold]Identified Weaknesses:[/bold]")
            for w in response.scorecard.identified_weaknesses:
                eval_lines.append(f"  - {w}")

    console.print(Panel(
        "\n".join(eval_lines),
        title="Evaluation Scorecard",
        border_style="cyan",
    ))

    # Assumptions
    console.print()
    console.print(Panel(
        "\n".join(f"- {a}" for a in response.assumptions),
        title="Assumptions",
        border_style="blue",
    ))

    # Known Issues
    console.print()
    console.print(Panel(
        "\n".join(f"- {i}" for i in response.known_issues),
        title="Known Issues",
        border_style="yellow",
    ))

    # Usage stats
    if response.usage:
        console.print()
        u = response.usage
        usage_text = (
            f"LLM Calls: {u.llm_calls} | "
            f"Tokens: {u.tokens_in:,} in / {u.tokens_out:,} out ({u.total_tokens:,} total) | "
            f"Cost: ${u.cost_usd:.4f}"
        )
        console.print(Panel(usage_text, title="Usage", border_style="green"))

    console.print()
    console.print(f"[dim]Run ID: {response.run_id}[/dim]")


def read_file_content(file_path: Path) -> str:
    """Read content from a file using utils."""
    try:
        return read_file_utils(file_path)
    except FileNotFoundError:
        console.print(f"[yellow]Warning: File not found: {file_path}[/yellow]")
        return ""
    except Exception as e:
        console.print(f"[red]Error reading file {file_path}: {e}[/red]")
        return ""


@app.command()
def solve(
    prompt: str = typer.Argument(..., help="Problem statement or idea to solve"),
    constraint: Optional[list[str]] = typer.Option(
        None, "--constraint", "-c",
        help="Add a constraint (can be used multiple times)",
    ),
    objective: Optional[list[str]] = typer.Option(
        None, "--objective", "-o",
        help="Add an objective (can be used multiple times)",
    ),
    file: Optional[list[Path]] = typer.Option(
        None, "--file", "-f",
        help="Additional context file (e.g. .md, .pdf, .docx, .txt)",
    ),
    library: Optional[list[Path]] = typer.Option(
        None, "--library", "-l",
        help="Path to a library file (can be used multiple times)",
    ),
    output_spec: Optional[Path] = typer.Option(
        None, "--output-spec",
        help="Path to output specification file",
    ),
    eval_criteria: Optional[Path] = typer.Option(
        None, "--eval-criteria",
        help="Path to evaluation criteria file",
    ),
    cross_pollinate: bool = typer.Option(
        False, "--cross-pollinate",
        help="Enable Phase 2 cross-pollination between inventors",
    ),
    inventors: int = typer.Option(
        4, "--inventors", "-n",
        help="Number of parallel inventors (1-10)",
        min=1, max=10,
    ),
    model: Optional[str] = typer.Option(
        None, "--model", "-m",
        help="Override the default model",
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output",
        help="Save output to file",
    ),
) -> None:
    """Generate a solution using Zeus's multi-inventor pipeline.

    Example:
        zeus solve "Design a scalable e-commerce platform"
        zeus solve "Build a trading system" -c "Must be async" -o "High availability"
        zeus solve "Design an API" -l library1.md -l library2.md --cross-pollinate
    """
    constraints = list(constraint) if constraint else []
    objectives = list(objective) if objective else []
    library_paths = [str(p) for p in library] if library else []

    # Process context from files
    context_parts = []
    if file:
        for f in file:
            content = read_file_content(f)
            if content:
                context_parts.append(content)
    combined_context = "\n\n".join(context_parts) if context_parts else None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Starting Zeus...", total=None)

        def on_progress(msg: str) -> None:
            progress.update(task, description=msg)

        try:
            response = asyncio.run(run_zeus(
                prompt=prompt,
                constraints=constraints,
                objectives=objectives,
                context=combined_context,
                library_paths=library_paths,
                output_spec_path=str(output_spec) if output_spec else None,
                eval_criteria_path=str(eval_criteria) if eval_criteria else None,
                enable_cross_pollination=cross_pollinate,
                num_inventors=inventors,
                model=model,
                on_progress=on_progress,
            ))
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    print_response(response)

    if output_file:
        output_file.write_text(response.output)
        console.print(f"\n[green]Output saved to {output_file}[/green]")


@app.command()
def history(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of runs to show"),
) -> None:
    """Show recent Zeus runs."""
    persistence = Persistence()
    runs = persistence.list_runs(limit=limit)

    if not runs:
        console.print("[dim]No runs found[/dim]")
        return

    console.print(f"\n[bold]Recent Zeus Runs[/bold] (showing {len(runs)})\n")

    for run in runs:
        status = "ok" if run["has_response"] else "failed"
        errors = f" ({run['errors']} errors)" if run["errors"] > 0 else ""
        score_str = ""
        if run.get("score") is not None:
            score_str = f" [{run['score']:.0f}/220]"
        console.print(
            f"  {status} {run['run_id'][:8]}... "
            f"[dim]{run['timestamp']}[/dim]{score_str}{errors}"
        )


@app.command()
def show(
    run_id: str = typer.Argument(..., help="Run ID (or prefix) to show"),
) -> None:
    """Show details of a specific run."""
    persistence = Persistence()
    record = persistence.load(run_id)

    if not record:
        console.print(f"[red]Run not found:[/red] {run_id}")
        raise typer.Exit(1)

    console.print(f"\n[bold]Run details: {record.run_id}[/bold]\n")
    console.print(f"Timestamp: {record.timestamp}")
    console.print(f"Model: {record.model_version}")

    if record.budget_used:
        total_tokens = record.budget_used.tokens_in + record.budget_used.tokens_out
        console.print(f"\nBudget Used:")
        console.print(f"  LLM Calls: {record.budget_used.llm_calls}")
        console.print(f"  Tokens: {record.budget_used.tokens_in:,} in / {record.budget_used.tokens_out:,} out ({total_tokens:,} total)")

    if record.inventor_solutions:
        console.print(f"\nInventors: {len(record.inventor_solutions)}")
        for sol in record.inventor_solutions:
            console.print(f"  - {sol.inventor_id} ({sol.inventor_type}): {len(sol.content)} chars")

    if record.errors:
        console.print(f"\n[red]Errors:[/red]")
        for error in record.errors:
            console.print(f"  - {error}")

    if record.final_response:
        console.print("\n[bold]Final Response:[/bold]")
        print_response(record.final_response)


@app.command()
def ui() -> None:
    """Launch the Zeus Web UI."""
    import subprocess
    import sys

    package_dir = Path(__file__).parent
    ui_path = package_dir / "ui.py"

    if not ui_path.exists():
        console.print(f"[red]Error: UI file not found at {ui_path}[/red]")
        raise typer.Exit(1)

    console.print(f"Starting Zeus UI from {ui_path}...")
    console.print("Press Ctrl+C to stop.")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(ui_path)])
    except KeyboardInterrupt:
        console.print("\nStopped Zeus UI.")


@app.callback()
def main() -> None:
    """Zeus - Multi-Inventor Design System.

    Generate solutions using parallel inventors, convergent synthesis,
    library-informed critique, and iterative refinement.
    """
    pass


if __name__ == "__main__":
    app()
