import json
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text

console = Console()

def render_audit_gate(gate_name: str, status: str, logs: str):
    """
    Displays a color-coded panel for the 5-Gate Audit pipeline.
    Status should be 'PASS' (Green) or 'FAIL' / 'BLOCK' (Red).
    """
    is_success = status.upper() == "PASS"
    border_color = "green" if is_success else "red"
    title_text = f"[{border_color} bold]GATE: {gate_name} - {status.upper()}[/]"
    
    content = Text(logs)
    
    panel = Panel(
        content,
        title=title_text,
        border_style=border_color,
        expand=False
    )
    console.print(panel)


def render_loop_progress(current_iteration: int, max_iterations: int):
    """
    A live progress bar for Teacher/Student evolutionary loops.
    """
    console.print(f"[cyan bold]Evolutionary Loop Bound: {current_iteration}/{max_iterations}[/cyan bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task = progress.add_task("[cyan]Processing iterative generation...", total=max_iterations)
        progress.update(task, completed=current_iteration)


def render_rubric_checklist(rubric_json: str):
    """
    A formatted table displaying the Teacher's required test criteria.
    Expects json string: {"mission": "...", "criteria": [{"id": 1, "task": "...", "passed": bool}]}
    """
    try:
        data = json.loads(rubric_json)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid Rubric JSON provided.[/red]")
        return

    mission = data.get("mission", "Unknown Mission")
    criteria = data.get("criteria", [])

    console.print(f"\n[bold magenta]TEACHER RUBRIC MISSION:[/bold magenta] {mission}")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Criteria requirement")
    table.add_column("Status", justify="center")

    for item in criteria:
        req_id = str(item.get("id", "-"))
        task_desc = str(item.get("task", "Unknown Task"))
        passed = item.get("passed", False)
        
        status_text = "[green]✔ PASS[/green]" if passed else "[red]✖ PENDING[/red]"
        table.add_row(req_id, task_desc, status_text)

    console.print(table)
    console.print("")

def render_matrix_view(student_code: str, execution_logs: str):
    """
    Renders a split screen representation of the Teacher loop.
    Left: Student stream
    Right: Execution Grader logs
    """
    from rich.layout import Layout
    
    layout = Layout()
    layout.split_row(
        Layout(name="student", ratio=1),
        Layout(name="grader", ratio=1)
    )
    
    student_panel = Panel(Text(student_code[:1000] + "\n...(truncated)" if len(student_code) > 1000 else student_code), title="[bold blue]STUDENT: Code Synthesis[/bold blue]", border_style="blue")
    grader_panel = Panel(Text(execution_logs[-1000:] if len(execution_logs) > 1000 else execution_logs), title="[bold yellow]GRADER: ACI Output[/bold yellow]", border_style="yellow")
    
    layout["student"].update(student_panel)
    layout["grader"].update(grader_panel)
    
    console.print(layout)
    console.print("")
