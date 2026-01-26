"""CLI interface for Zeus."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from zeus.core.run_controller import run_zeus
from zeus.core.persistence import Persistence
from zeus.models.schemas import ZeusResponse, Tradeoff

app = typer.Typer(
    name="zeus",
    help="Zeus - Design Team Agent for multi-agent systems",
    add_completion=False,
)
console = Console()


def _format_confidence(confidence: str) -> str:
    """Format confidence level with color."""
    colors = {"high": "green", "medium": "yellow", "low": "red"}
    color = colors.get(confidence, "white")
    return f"[{color}]{confidence.upper()}[/{color}]"


def _format_coverage(score: float, covered: list[str], missing: list[str]) -> str:
    """Format coverage metrics."""
    pct = int(score * 100)
    total = len(covered) + len(missing)

    lines = [f"{pct}% ({len(covered)}/{total} perspectives)"]

    # Show perspective status
    perspective_parts = []
    for p in sorted(covered):
        perspective_parts.append(f"[green]✓[/green] {p}")
    for p in sorted(missing):
        perspective_parts.append(f"[red]✗[/red] {p}")

    if perspective_parts:
        lines.append("  ".join(perspective_parts))

    return "\n".join(lines)


def _format_tradeoffs(tradeoffs: list[Tradeoff]) -> str:
    """Format tradeoffs list."""
    if not tradeoffs:
        return "[dim]No tradeoffs documented[/dim]"

    lines = []
    for t in tradeoffs:
        impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
        color = impact_colors.get(t.impact, "white")
        lines.append(f"• {t.chose} [dim]over[/dim] {t.over} [{color}][{t.impact.upper()}][/{color}]")
        lines.append(f"  [dim]{t.rationale}[/dim]")

    return "\n".join(lines)


def _format_issues_by_category(issues_by_category: dict[str, list[str]]) -> str:
    """Format issues grouped by category."""
    if not issues_by_category:
        return "[dim]No issues identified[/dim]"

    lines = []
    # Sort categories for consistent display
    for category in sorted(issues_by_category.keys()):
        issues = issues_by_category[category]
        lines.append(f"[bold]{category.title()}[/bold] ({len(issues)})")
        for issue in issues:
            lines.append(f"  • {issue}")

    return "\n".join(lines)


def print_response(response: ZeusResponse) -> None:
    """Print the Zeus response in a formatted way."""
    # Main output
    console.print(Markdown(response.output))

    # V1: Confidence with breakdown
    console.print()
    confidence_text = _format_confidence(response.confidence)
    counts = response.issue_counts
    breakdown = f"{counts['blockers']} blockers, {counts['majors']} major, {counts['minors']} minor"
    console.print(Panel(
        f"Confidence: {confidence_text}\n[dim]Based on: {breakdown}[/dim]",
        title="🎯 Confidence",
        border_style="cyan",
    ))

    # V1: Coverage
    console.print()
    coverage_text = _format_coverage(
        response.coverage_score,
        response.covered_perspectives,
        response.missing_perspectives,
    )
    console.print(Panel(
        coverage_text,
        title="📊 Coverage",
        border_style="cyan",
    ))

    # V1: Tradeoffs
    if response.tradeoffs:
        console.print()
        tradeoffs_text = _format_tradeoffs(response.tradeoffs)
        console.print(Panel(
            tradeoffs_text,
            title=f"⚖️ Tradeoffs ({len(response.tradeoffs)})",
            border_style="cyan",
        ))

    # Assumptions
    console.print()
    console.print(Panel(
        "\n".join(f"• {a}" for a in response.assumptions),
        title="📋 Assumptions",
        border_style="blue",
    ))

    # Known Issues (grouped by category if available)
    console.print()
    if response.issues_by_category:
        issues_text = _format_issues_by_category(response.issues_by_category)
    else:
        issues_text = "\n".join(f"• {i}" for i in response.known_issues)
    console.print(Panel(
        issues_text,
        title="⚠️ Known Issues",
        border_style="yellow",
    ))

    # Usage stats
    if response.usage:
        console.print()
        usage = response.usage
        usage_text = (
            f"LLM Calls: {usage.llm_calls} | "
            f"Tokens: {usage.tokens_in:,} in / {usage.tokens_out:,} out ({usage.total_tokens:,} total) | "
            f"Cost: ${usage.cost_usd:.4f}"
        )
        console.print(Panel(
            usage_text,
            title="📊 Usage",
            border_style="green",
        ))

    # Run ID
    console.print()
    console.print(f"[dim]Run ID: {response.run_id}[/dim]")


@app.command()
def brief(
    prompt: str = typer.Argument(..., help="The idea or problem to create a design brief for"),
    constraint: Optional[list[str]] = typer.Option(
        None,
        "--constraint", "-c",
        help="Add a constraint (can be used multiple times)",
    ),
    context: Optional[str] = typer.Option(
        None,
        "--context",
        help="Additional context as a string",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model", "-m",
        help="Override the default model",
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Save output to file",
    ),
) -> None:
    """Generate a Design Brief from an idea or problem statement.

    Example:
        zeus brief "Build a system that automatically reviews code changes"
        zeus brief "Build a code review system" -c "Must be async" -c "No external deps"
    """
    constraints = list(constraint) if constraint else []

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
                mode="brief",
                constraints=constraints,
                context=context,
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
def solution(
    prompt: Optional[str] = typer.Argument(
        None,
        help="The design brief text (alternative to --file)",
    ),
    file: Optional[Path] = typer.Option(
        None,
        "--file", "-f",
        help="Path to design brief file",
        exists=True,
        readable=True,
    ),
    constraint: Optional[list[str]] = typer.Option(
        None,
        "--constraint", "-c",
        help="Add a constraint (can be used multiple times)",
    ),
    context: Optional[str] = typer.Option(
        None,
        "--context",
        help="Additional context as a string",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model", "-m",
        help="Override the default model",
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Save output to file",
    ),
) -> None:
    """Generate a Target Solution from a Design Brief.

    Example:
        zeus solution --file design_brief.md
        zeus solution "$(cat design_brief.md)"
    """
    # Get input from file or argument
    if file:
        input_text = file.read_text()
    elif prompt:
        input_text = prompt
    else:
        console.print("[red]Error:[/red] Provide either a prompt argument or --file option")
        raise typer.Exit(1)

    constraints = list(constraint) if constraint else []

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
                prompt=input_text,
                mode="solution",
                constraints=constraints,
                context=context,
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

    console.print(f"\n[bold]Recent Zeus Runs[/bold] (showing {len(runs)} of {limit} max)\n")

    for run in runs:
        status = "✅" if run["has_response"] else "❌"
        errors = f" ({run['errors']} errors)" if run["errors"] > 0 else ""
        console.print(
            f"  {status} [{run['mode']}] {run['run_id'][:8]}... "
            f"[dim]{run['timestamp']}[/dim]{errors}"
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

    console.print(f"\n[bold]Run Details: {record.run_id}[/bold]\n")
    console.print(f"Mode: {record.mode}")
    console.print(f"Timestamp: {record.timestamp}")
    console.print(f"Model: {record.model_version}")

    if record.budget_used:
        total_tokens = record.budget_used.tokens_in + record.budget_used.tokens_out
        console.print(f"\nBudget Used:")
        console.print(f"  LLM Calls: {record.budget_used.llm_calls}")
        console.print(f"  Tokens: {record.budget_used.tokens_in:,} in / {record.budget_used.tokens_out:,} out ({total_tokens:,} total)")
        console.print(f"  Revisions: {record.budget_used.revisions}")

    if record.errors:
        console.print(f"\n[red]Errors:[/red]")
        for error in record.errors:
            console.print(f"  - {error}")

    if record.final_response:
        console.print("\n[bold]Final Response:[/bold]")
        print_response(record.final_response)


@app.callback()
def main() -> None:
    """Zeus - Design Team Agent.

    Generate Design Briefs from ideas, or Target Solutions from Design Briefs.
    """
    pass


if __name__ == "__main__":
    app()
