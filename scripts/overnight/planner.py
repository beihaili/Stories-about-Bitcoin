"""
Planner module for the overnight iteration system.

Reads findings.json and generates an interleaved task queue (code/content
alternating). Pipeline-fix tasks (highest priority) always come first.

Outputs:
  - task_plan.md   — Human-readable markdown plan
  - task_plan.json — Machine-readable plan for the executor
"""

import json
from datetime import date
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def interleave_tasks(
    code_tasks: list[dict],
    content_tasks: list[dict],
) -> list[dict]:
    """
    Interleave code and content tasks in alternating order.

    Pattern: code, content, code, content, ...
    When one list runs out, remaining items from the other are appended.

    Args:
        code_tasks: List of code-type task dicts.
        content_tasks: List of content-type task dicts.

    Returns:
        A single interleaved list starting with a code task.
    """
    result: list[dict] = []
    code_iter = iter(code_tasks)
    content_iter = iter(content_tasks)

    # Strict alternation while both lists have items
    code_exhausted = False
    content_exhausted = False

    while not code_exhausted or not content_exhausted:
        # Try to add a code task
        if not code_exhausted:
            item = next(code_iter, None)
            if item is not None:
                result.append(item)
            else:
                code_exhausted = True

        # Try to add a content task
        if not content_exhausted:
            item = next(content_iter, None)
            if item is not None:
                result.append(item)
            else:
                content_exhausted = True

    return result


def generate_task_plan(run_dir: Path, max_rounds: int = 20) -> Path:
    """
    Read findings.json from run_dir and generate a task plan.

    Priority order:
      1. pipeline-fix tasks (highest severity, go first)
      2. Interleaved code / content tasks

    Writes task_plan.md and task_plan.json to run_dir.

    Args:
        run_dir: Directory containing findings.json.
        max_rounds: Cap the total number of rounds.

    Returns:
        Path to task_plan.md.
    """
    json_path = run_dir / "findings.json"
    findings = json.loads(json_path.read_text(encoding="utf-8"))

    code_findings: list[dict] = findings.get("code", [])
    content_findings: list[dict] = findings.get("content", [])

    # Split code findings into pipeline-fix (highest priority) vs. regular
    pipeline_tasks = [f for f in code_findings if f.get("type") == "pipeline-fix"]
    regular_code = [f for f in code_findings if f.get("type") != "pipeline-fix"]

    # Build task dicts from findings
    pipeline_task_list = _build_code_tasks(pipeline_tasks)
    code_task_list = _build_code_tasks(regular_code)
    content_task_list = _build_content_tasks(content_findings)

    # Compose final task sequence
    all_tasks: list[dict] = pipeline_task_list + interleave_tasks(code_task_list, content_task_list)

    # Enforce max_rounds cap
    all_tasks = all_tasks[:max_rounds]

    # Assign round numbers
    for i, task in enumerate(all_tasks, start=1):
        task["round"] = i

    # Write markdown plan
    run_date = run_dir.name  # e.g. "2026-04-08"
    plan_path = _write_task_plan_md(run_dir, all_tasks, run_date)

    # Write JSON plan (for executor)
    json_plan_path = run_dir / "task_plan.json"
    json_plan_path.write_text(
        json.dumps(all_tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return plan_path


def parse_task_plan(plan_path: Path) -> list[dict]:
    """
    Parse task_plan.md into a list of task dicts.

    Each dict contains:
        round, type, target, issue, action, verify, status,
        and optionally: weaknesses, suggestions (content tasks).

    Args:
        plan_path: Path to task_plan.md.

    Returns:
        List of task dicts, one per ## Round section.
    """
    lines = plan_path.read_text(encoding="utf-8").splitlines()
    tasks: list[dict] = []
    current_task: dict | None = None

    for line in lines:
        # Detect a new round header: "## Round N — type"
        if line.startswith("## Round "):
            # Save previous task if any
            if current_task is not None:
                tasks.append(current_task)

            # Parse "## Round 3 — code-lint"
            header = line[len("## Round "):].strip()
            parts = header.split(" — ", 1)
            try:
                round_num = int(parts[0])
            except ValueError:
                round_num = 0
            task_type = parts[1].strip() if len(parts) > 1 else "unknown"

            current_task = {"round": round_num, "type": task_type}
            continue

        # Parse bullet fields: "- **key**: value" or "- key: value"
        if current_task is not None and line.startswith("- "):
            key: str | None = None
            value: str | None = None

            rest = line[2:]  # strip "- "
            if rest.startswith("**") and "**: " in rest[2:]:
                # Bold key format: "**key**: value"
                inner = rest[2:]  # strip leading "**"
                key, _, value = inner.partition("**: ")
                key = key.strip()
                value = value.strip()
            elif ": " in rest and not rest.startswith("*"):
                # Plain key format: "key: value"
                key, _, value = rest.partition(": ")
                key = key.strip()
                value = value.strip()

            if key is not None and value is not None:
                # Attempt to decode JSON arrays for weaknesses/suggestions
                if key in ("weaknesses", "suggestions"):
                    try:
                        current_task[key] = json.loads(value)
                    except (json.JSONDecodeError, ValueError):
                        current_task[key] = value
                else:
                    current_task[key] = value

    # Don't forget the last task
    if current_task is not None:
        tasks.append(current_task)

    return tasks


def update_task_status(plan_path: Path, round_num: int, new_status: str) -> None:
    """
    Update the status of a specific round in task_plan.md.

    Uses a line-by-line approach: find the ## Round N section header,
    then update the first "- **status**:" line that follows it,
    and stop before the next ## Round section.

    Args:
        plan_path: Path to task_plan.md.
        round_num: The round number to update (1-based).
        new_status: New status string (e.g. "done", "failed", "skipped").
    """
    lines = plan_path.read_text(encoding="utf-8").splitlines(keepends=True)

    target_header = f"## Round {round_num} "
    in_target_section = False
    status_updated = False

    new_lines: list[str] = []
    for line in lines:
        stripped = line.strip()

        # Detect entry into the target section
        if stripped.startswith(target_header):
            in_target_section = True
            new_lines.append(line)
            continue

        # Detect start of a different section (exit target section)
        if in_target_section and stripped.startswith("## Round ") and not stripped.startswith(target_header):
            in_target_section = False

        # Replace status line within target section (only once)
        # Handle both "- **status**: value" and "- status: value" formats
        is_status_line = (
            stripped.startswith("- **status**:") or stripped.startswith("- status:")
        )
        if in_target_section and not status_updated and is_status_line:
            # Preserve original indentation
            indent = line[: len(line) - len(line.lstrip())]
            # Mirror the original format (bold key or plain key)
            if stripped.startswith("- **status**:"):
                new_lines.append(f"{indent}- **status**: {new_status}\n")
            else:
                new_lines.append(f"{indent}- status: {new_status}\n")
            status_updated = True
            continue

        new_lines.append(line)

    plan_path.write_text("".join(new_lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _build_code_tasks(findings: list[dict]) -> list[dict]:
    """
    Convert code/pipeline findings into structured task dicts.

    Maps finding type to appropriate action and verification strings.

    Args:
        findings: List of code finding dicts from scanner.

    Returns:
        List of task dicts ready for the plan.
    """
    tasks: list[dict] = []
    for f in findings:
        ftype = f.get("type", "code-fix")
        target = f.get("target", "")
        description = f.get("description", "")

        # Determine action and verify based on type
        if ftype == "code-lint":
            action = "Fix ESLint errors"
            verify = "npm run lint passes"
        elif ftype == "code-test":
            action = "Add missing unit tests"
            verify = "npm run test:run passes with new tests"
        elif ftype == "code-ruff":
            action = "Fix ruff Python linting issues"
            verify = "ruff check passes with no errors"
        elif ftype == "pipeline-fix":
            action = f"Fix: {description}"
            verify = "python -m pytest scripts/ passes"
        else:
            action = f"Fix: {description}"
            verify = "Relevant tests or checks pass"

        tasks.append({
            "type": ftype,
            "target": target,
            "issue": description,
            "action": action,
            "verify": verify,
            "details": f.get("details", ""),
            "severity": f.get("severity", 0),
        })

    return tasks


def _build_content_tasks(findings: list[dict]) -> list[dict]:
    """
    Convert content findings into structured task dicts.

    Includes weaknesses and suggestions from the score JSON.

    Args:
        findings: List of content finding dicts from scanner.

    Returns:
        List of task dicts ready for the plan.
    """
    tasks: list[dict] = []
    for f in findings:
        target = f.get("target", "")
        description = f.get("description", "")
        weaknesses = f.get("weaknesses", [])
        suggestions = f.get("suggestions", [])
        weakest_dim = f.get("weakest_dimension", "")

        action = f"Refine {weakest_dim}" if weakest_dim else "Refine readability"
        verify = f"{weakest_dim} score improves" if weakest_dim else "readability score improves"

        tasks.append({
            "type": "content-refine",
            "target": target,
            "issue": description,
            "action": action,
            "verify": verify,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
            "severity": f.get("severity", 0),
            "chapter_num": f.get("chapter_num"),
            "average": f.get("average"),
        })

    return tasks


def _write_task_plan_md(run_dir: Path, tasks: list[dict], run_date: str) -> Path:
    """
    Write the task plan as a human-readable markdown file.

    Format per round:
        ## Round N — {type}
        - **target**: {path}
        - **issue**: {description}
        - **action**: {what to do}
        - **verify**: {how to verify}
        - **weaknesses**: {JSON array, content tasks only}
        - **suggestions**: {JSON array, content tasks only}
        - **status**: pending

    Args:
        run_dir: Directory to write the plan into.
        tasks: List of task dicts with round numbers assigned.
        run_date: ISO date string for the plan header.

    Returns:
        Path to the written task_plan.md.
    """
    lines: list[str] = [f"# Overnight Task Plan — {run_date}\n"]

    for task in tasks:
        round_num = task["round"]
        task_type = task["type"]
        target = task.get("target", "")
        issue = task.get("issue", "")
        action = task.get("action", "")
        verify = task.get("verify", "")

        lines.append(f"\n## Round {round_num} — {task_type}")
        lines.append(f"- **target**: {target}")
        lines.append(f"- **issue**: {issue}")
        lines.append(f"- **action**: {action}")
        lines.append(f"- **verify**: {verify}")

        # Content-task-specific fields
        if task_type == "content-refine":
            weaknesses = task.get("weaknesses", [])
            suggestions = task.get("suggestions", [])
            lines.append(f"- **weaknesses**: {json.dumps(weaknesses, ensure_ascii=False)}")
            lines.append(f"- **suggestions**: {json.dumps(suggestions, ensure_ascii=False)}")

        lines.append("- status: pending")

    # Trailing newline
    lines.append("")

    plan_path = run_dir / "task_plan.md"
    plan_path.write_text("\n".join(lines), encoding="utf-8")
    return plan_path
