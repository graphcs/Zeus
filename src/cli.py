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
from src.core.run_controller import run_zeus
from src.core.persistence import Persistence
from src.models.schemas import UsageStats, VerificationReport, StructuredKnownIssue
from src.utils.read_file import read_file_content as read_file_utils
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

app = typer.Typer(
    name="zeus",
    help="Zeus - Design Team Agent for multi-agent systems",
    add_completion=False,
)
console = Console()


def print_response(
    output: str,
    assumptions: list[str],
    known_issues: list[str],
    run_id: str,
    usage: UsageStats | None = None,
    confidence: str | None = None,
    coverage_score: float | None = None,
    tradeoffs: list[str] | None = None,
    evaluation_summary: dict | None = None,
    verification_report: VerificationReport | None = None,
    structured_issues: list[StructuredKnownIssue] | None = None,
) -> None:
    """Print the Zeus response in a formatted way with V1 evaluation signals.
    
    Args:
        output: Main output content
        assumptions: List of assumptions
        known_issues: List of known issues
        run_id: Run identifier
        usage: Optional usage statistics
        confidence: V1 confidence level (low/medium/high)
        coverage_score: V1 coverage score (0.0-1.0)
        tradeoffs: V1 design tradeoffs
        evaluation_summary: V1 complete evaluation summary
        verification_report: V3 constraint verification report
        structured_issues: V3 structured known issues
    """
    # Main output
    console.print(Markdown(output))

    # V1: Evaluation Summary Panel
    if confidence or coverage_score is not None or evaluation_summary:
        console.print()
        
        # Build evaluation summary
        eval_lines = []
        
        if confidence:
            # Color-code confidence
            conf_colors = {"low": "red", "medium": "yellow", "high": "green"}
            conf_color = conf_colors.get(confidence, "white")
            conf_emoji = {"low": "🔴", "medium": "🟡", "high": "🟢"}
            emoji = conf_emoji.get(confidence, "⚪")
            eval_lines.append(f"{emoji} Confidence: [{conf_color}]{confidence.upper()}[/{conf_color}]")
        
        if coverage_score is not None:
            # Format coverage as percentage with color
            coverage_pct = int(coverage_score * 100)
            if coverage_pct >= 83:  # 5/6 or 6/6
                cov_color = "green"
            elif coverage_pct >= 50:  # 3/6 or 4/6
                cov_color = "yellow"
            else:
                cov_color = "red"
            eval_lines.append(f"📊 Critique Coverage: [{cov_color}]{coverage_pct}%[/{cov_color}] ({int(coverage_score * 6)}/6 perspectives)")
        
        # Add detailed metrics if available
        if evaluation_summary:
            eval_lines.append("")
            eval_lines.append("[bold]Issue Breakdown:[/bold]")
            blockers = evaluation_summary.get('blockers', 0)
            majors = evaluation_summary.get('majors', 0)
            minors = evaluation_summary.get('minors', 0)
            total = evaluation_summary.get('total_issues', 0)
            
            if blockers > 0:
                eval_lines.append(f"  🚫 Blockers: [red]{blockers}[/red]")
            if majors > 0:
                eval_lines.append(f"  ⚠️  Majors: [yellow]{majors}[/yellow]")
            if minors > 0:
                eval_lines.append(f"  ℹ️  Minors: [blue]{minors}[/blue]")
            
            if total == 0:
                eval_lines.append("  ✨ No issues found")
            
            # Show missing perspectives
            missing = evaluation_summary.get('missing_perspectives', [])
            if missing:
                eval_lines.append("")
                eval_lines.append(f"[yellow]Missing Perspectives:[/yellow] {', '.join(missing)}")
        
        if eval_lines:
            console.print(Panel(
                "\n".join(eval_lines),
                title="🎯 V1 Evaluation",
                border_style="cyan",
            ))

    # V3: Constraints Verification
    if verification_report:
        console.print()
        ver_lines = []
        
        v_score = verification_report.coverage_score
        v_pct = int(v_score * 100)
        v_color = "green" if v_pct == 100 else "yellow" if v_pct >= 50 else "red"
        
        ver_lines.append(f"🛡️ Verification Coverage: [{v_color}]{v_pct}%[/{v_color}]")
        ver_lines.append("")
        
        # Only show table if checks exist
        if verification_report.checks:
            ver_lines.append("[bold]Constraint Checks:[/bold]")
            for check in verification_report.checks:
                icon = {"pass": "✅", "fail": "❌", "unverified": "❓"}.get(check.status, "❓")
                status_color = {"pass": "green", "fail": "red", "unverified": "yellow"}.get(check.status, "white")
                ver_lines.append(f"  {icon} [{status_color}]{check.status.upper()}[/{status_color}]: {check.constraint}")
                if check.evidence:
                    ver_lines.append(f"     [dim]Evidence: {check.evidence}[/dim]")

        console.print(Panel(
            "\n".join(ver_lines),
            title="🛡️ Constraints Verification (V3)",
            border_style="green",
        ))

    # Tradeoffs (V1)
    if tradeoffs:
        console.print()
        console.print(Panel(
            "\n".join(f"• {t}" for t in tradeoffs),
            title="⚖️ Design Tradeoffs",
            border_style="magenta",
        ))

    # Assumptions
    console.print()
    console.print(Panel(
        "\n".join(f"• {a}" for a in assumptions),
        title="📋 Assumptions",
        border_style="blue",
    ))

    # Known Issues (V3 Structured or Legacy)
    console.print()
    if structured_issues:
        issue_lines = []
        for i, issue in enumerate(structured_issues):
            issue_lines.append(f"[bold]{i+1}. {issue.issue}[/bold]")
            issue_lines.append(f"   [red]Impact:[/red] {issue.impact}")
            issue_lines.append(f"   [green]Mitigation:[/green] {issue.mitigation}")
            issue_lines.append(f"   [blue]Verification:[/blue] {issue.verification_step}")
            issue_lines.append("")
            
        console.print(Panel(
            "\n".join(issue_lines),
            title="⚠️ Known Issues Registry (V3)",
            border_style="yellow",
        ))
    else:
        # Legacy lists
        console.print(Panel(
            "\n".join(f"• {i}" for i in known_issues),
            title="⚠️ Known Issues",
            border_style="yellow",
        ))

    # Usage stats
    if usage:
        console.print()
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
    console.print(f"[dim]Run ID: {run_id}[/dim]")



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
    file: Optional[list[Path]] = typer.Option(
        None,
        "--file", "-f",
        help="Additional context file (e.g. .md, .pdf, .docx, .txt)",
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

    # Process context from string and files
    context_parts = []
    if context:
        context_parts.append(context)
    
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
                mode="brief",
                constraints=constraints,
                context=combined_context,
                model=model,
                on_progress=on_progress,
            ))
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    print_response(
        response.output,
        response.assumptions,
        response.known_issues,
        response.run_id,
        response.usage,
        response.confidence,
        response.coverage_score,
        response.tradeoffs,
        evaluation_summary=getattr(response, "evaluation_summary", None),
        verification_report=getattr(response, "verification_report", None),
        structured_issues=getattr(response, "structured_issues", None),
    )

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

    # Get evaluation summary if available
    eval_summary = None
    if hasattr(response, 'evaluation_summary'):
        eval_summary = response.evaluation_summary
    
    print_response(
        response.output,
        response.assumptions,
        response.known_issues,
        response.run_id,
        response.usage,
        response.confidence,
        response.coverage_score,
        response.tradeoffs,
        eval_summary,
        verification_report=getattr(response, "verification_report", None),
        structured_issues=getattr(response, "structured_issues", None),
    )

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

    console.print(f"\n[bold]Run details: {record.run_id}[/bold]\n")
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
        # Get fields from final_response, with fallbacks for V1 fields
        usage = getattr(record.final_response, 'usage', None)
        confidence = getattr(record.final_response, 'confidence', None)
        coverage_score = getattr(record.final_response, 'coverage_score', None)
        tradeoffs = getattr(record.final_response, 'tradeoffs', None)
        eval_summary = getattr(record.final_response, 'evaluation_summary', None)
        
        print_response(
            record.final_response.output,
            record.final_response.assumptions,
            record.final_response.known_issues,
            record.final_response.run_id,
            usage,
            confidence,
            coverage_score,
            tradeoffs,
            eval_summary,
            verification_report=getattr(record.final_response, "verification_report", None),
            structured_issues=getattr(record.final_response, "structured_issues", None),
        )


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
    """Zeus - Design Team Agent.

    Generate Design Briefs from ideas, or Target Solutions from Design Briefs.
    """
    pass


if __name__ == "__main__":
    app()
