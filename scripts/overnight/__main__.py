"""
Overnight Iteration System — Entry Point

Usage:
    python -m scripts.overnight --rounds 20
    python -m scripts.overnight --dry-run
    python -m scripts.overnight --resume
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path

# Ensure project root is importable
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.overnight import config
from scripts.overnight.scanner import scan_code, scan_content, write_findings
from scripts.overnight.planner import generate_task_plan, parse_task_plan, update_task_status
from scripts.overnight.executor import cleanup_previous_runs, execute_round, check_disk_space
from scripts.overnight.reporter import generate_report
from scripts.overnight.budget import BudgetTracker


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments for the overnight runner.

    Returns an argparse.Namespace with fields:
        rounds, timeout, dry_run, resume, code_only, content_only
    """
    parser = argparse.ArgumentParser(
        description="Overnight Iteration System — automated code & content improvement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m scripts.overnight --rounds 20\n"
            "  python -m scripts.overnight --dry-run\n"
            "  python -m scripts.overnight --resume --code-only\n"
        ),
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=20,
        help="Maximum number of improvement rounds to run (default: 20)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Seconds per Claude round before timeout (default: 900)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Scan and plan only — do not execute any rounds",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=False,
        help="Resume the last incomplete run (reuse scan/plan if fresh)",
    )
    parser.add_argument(
        "--code-only",
        action="store_true",
        default=False,
        help="Only execute code improvement tasks",
    )
    parser.add_argument(
        "--content-only",
        action="store_true",
        default=False,
        help="Only execute content refinement tasks",
    )
    parser.add_argument(
        "--budget-aware",
        action="store_true",
        default=False,
        help="Track token usage, rescan hourly, burn remaining quota before window resets",
    )
    parser.add_argument(
        "--window-hours",
        type=float,
        default=5.0,
        help="Max plan rolling window in hours (default: 5.0)",
    )
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Prerequisite checks
# ---------------------------------------------------------------------------


def check_prerequisites() -> None:
    """
    Verify that required tools (claude, git, gh) are available in PATH.
    Also checks that `gh auth status` succeeds (GitHub auth is configured).

    Calls sys.exit(1) with an explanatory message if anything is missing.
    """
    required_tools = ["claude", "git", "gh"]
    missing = [t for t in required_tools if shutil.which(t) is None]
    if missing:
        print(
            f"[overnight] ERROR: Required tool(s) not found in PATH: {', '.join(missing)}",
            file=sys.stderr,
        )
        print("[overnight] Install them and re-run.", file=sys.stderr)
        sys.exit(1)

    # Check GitHub auth
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            print("[overnight] ERROR: 'gh auth status' failed — run 'gh auth login' first.", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        # gh already verified above; this branch shouldn't be reached normally
        print("[overnight] ERROR: 'gh' not found when running auth check.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("[overnight] WARNING: 'gh auth status' timed out — continuing anyway.", file=sys.stderr)


# ---------------------------------------------------------------------------
# Run directory discovery
# ---------------------------------------------------------------------------


def find_latest_run() -> Path | None:
    """
    Find the most recent run directory under config.RUNS_DIR that contains
    a task_plan.md file.

    Returns:
        Path to the most recent valid run directory, or None if none exists.
    """
    runs_dir = config.RUNS_DIR
    if not runs_dir.exists():
        return None

    # Sort date-named directories in descending order (most recent first)
    candidates = sorted(
        (d for d in runs_dir.iterdir() if d.is_dir()),
        key=lambda d: d.name,
        reverse=True,
    )
    for run_dir in candidates:
        if (run_dir / "task_plan.md").exists():
            return run_dir

    return None


# ---------------------------------------------------------------------------
# Caffeinate wrapper (macOS only)
# ---------------------------------------------------------------------------


def run_with_caffeinate() -> None:
    """
    Re-exec this process under `caffeinate -i` to prevent macOS from sleeping.

    If OVERNIGHT_CAFFEINATED env var is already set, call main() directly
    (we're already inside caffeinate). If caffeinate is not found (non-macOS),
    fall through and run main() directly.
    """
    if os.environ.get("OVERNIGHT_CAFFEINATED"):
        # Already running under caffeinate — proceed with main()
        main()
        return

    try:
        # Re-exec with caffeinate, passing through all original argv
        caffeinate_cmd = [
            "caffeinate", "-i",
            sys.executable, "-m", "scripts.overnight",
        ] + sys.argv[1:]

        env = os.environ.copy()
        env["OVERNIGHT_CAFFEINATED"] = "1"

        subprocess.run(caffeinate_cmd, env=env)
    except FileNotFoundError:
        # caffeinate not available (non-macOS) — run directly
        main()


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    """
    Orchestrate the overnight iteration system.

    Phases:
        0: Cleanup leftover worktrees from previous runs
        1: Scan for code/content issues (skip if --resume with fresh findings)
        2: Generate task plan (skip if --resume with existing plan)
        [dry-run stops here]
        3: Execute rounds (filtered by --code-only / --content-only)
        4: Generate morning report
    """
    args = parse_args(argv)

    # Verify required tools (claude, git, gh) are available before doing anything
    check_prerequisites()

    start_time = datetime.now()

    # Budget tracker (always created; only prints/acts when --budget-aware)
    tracker = BudgetTracker(window_hours=args.window_hours)

    print(f"[overnight] Starting run — {start_time.strftime('%Y-%m-%d %H:%M')}", flush=True)
    mode_str = "budget-aware" if args.budget_aware else f"rounds: {args.rounds}"
    print(f"[overnight] Mode: {mode_str} | Timeout: {args.timeout}s "
          f"| dry-run: {args.dry_run} | resume: {args.resume}", flush=True)

    # --- Phase 0: Cleanup previous runs ---
    print("[overnight] Phase 0: Cleaning up leftover worktrees...", flush=True)
    try:
        cleanup_previous_runs()
    except Exception as exc:
        print(f"[overnight] WARNING: cleanup failed: {exc}", flush=True)

    # --- Determine run directory ---
    run_dir = config.get_run_dir()

    # For --resume, try to find the latest existing run first
    if args.resume:
        latest = find_latest_run()
        if latest is not None:
            run_dir = latest
            print(f"[overnight] Resuming run from: {run_dir}", flush=True)
        else:
            print("[overnight] No previous run found — starting fresh.", flush=True)
            args.resume = False  # fall through to normal scan

    run_dir.mkdir(parents=True, exist_ok=True)
    findings_path = run_dir / "findings.json"
    plan_path = run_dir / "task_plan.md"

    # --- Phase 1: Scan ---
    _need_scan = True
    if args.resume and findings_path.exists():
        # Check freshness: skip scan if findings are < 1 hour old
        age = time.time() - findings_path.stat().st_mtime
        if age < 3600:
            print(f"[overnight] Phase 1: Findings are fresh ({age:.0f}s old) — skipping scan.", flush=True)
            _need_scan = False
        else:
            print(f"[overnight] Phase 1: Findings are stale ({age:.0f}s old) — re-scanning.", flush=True)

    if _need_scan:
        print("[overnight] Phase 1: Scanning for code and content issues...", flush=True)
        code_findings = scan_code()
        content_findings = scan_content()
        findings_path, _ = write_findings(code_findings, content_findings, run_dir)
        print(f"[overnight]   Code issues: {len(code_findings)} | "
              f"Content issues: {len(content_findings)}", flush=True)

    # --- Phase 2: Plan ---
    _need_plan = True
    if args.resume and plan_path.exists() and not _need_scan:
        # Only reuse the existing plan if we also reused the existing findings.
        # If findings were stale and re-scanned (_need_scan was True), we must
        # regenerate the plan so it reflects the fresh findings.
        print("[overnight] Phase 2: Existing task plan found — reusing.", flush=True)
        _need_plan = False

    if _need_plan:
        print("[overnight] Phase 2: Generating task plan...", flush=True)
        plan_path = generate_task_plan(run_dir, max_rounds=args.rounds)
        print(f"[overnight]   Plan written to: {plan_path}", flush=True)

    # --- Dry run: stop after planning ---
    if args.dry_run:
        print("[overnight] --dry-run flag set — stopping after plan. No rounds executed.", flush=True)
        return

    # --- Parse tasks ---
    tasks = parse_task_plan(plan_path)

    # Filter by --code-only / --content-only
    if args.code_only:
        tasks = [t for t in tasks if not t.get("type", "").startswith("content")]
        print(f"[overnight] --code-only: {len(tasks)} tasks after filtering.", flush=True)
    elif args.content_only:
        tasks = [t for t in tasks if t.get("type", "").startswith("content")]
        print(f"[overnight] --content-only: {len(tasks)} tasks after filtering.", flush=True)

    # Skip tasks already marked done/failed/skipped (relevant for --resume)
    pending_tasks = [
        t for t in tasks
        if t.get("status", "pending") == "pending"
    ]
    print(f"[overnight] Phase 3: {len(pending_tasks)} pending tasks to execute.", flush=True)

    # --- Phase 3: Execute rounds ---
    results: list[dict] = []
    last_scan_time = datetime.now()
    total_round_counter = len(pending_tasks)  # for generating new round numbers

    # Load any prior results from results.json (crash recovery for --resume)
    results_json_path = run_dir / "results.json"
    if args.resume and results_json_path.exists():
        try:
            results = json.loads(results_json_path.read_text(encoding="utf-8"))
            print(f"[overnight] Loaded {len(results)} prior results from results.json.", flush=True)
        except (json.JSONDecodeError, OSError):
            results = []

    task_queue = list(pending_tasks)  # mutable copy

    while task_queue:
        task = task_queue.pop(0)
        round_num = task.get("round", 0)
        task_type = task.get("type", "unknown")
        target = task.get("target", "")

        print(f"\n[overnight] Round {round_num}: {task_type} — {target}", flush=True)

        result = execute_round(task, round_num, run_dir, timeout=args.timeout)
        results.append(result)

        # Budget tracking — estimate tokens from prompt/response lengths
        prompt_len = result.get("prompt_len", 0)
        response_len = result.get("response_len", 0)
        if prompt_len or response_len:
            tracker.record_round(
                "x" * prompt_len,   # reconstruct approximate length
                "x" * response_len,
            )

        status = result.get("status", "error")
        reason = result.get("verification", {}).get("reason", "")
        pr_url = result.get("pr_url") or ""
        print(f"[overnight]   Status: {status} | {reason[:80]}", flush=True)
        if pr_url:
            print(f"[overnight]   PR: {pr_url}", flush=True)

        # Print budget status
        if args.budget_aware:
            print(f"[overnight]   {tracker.format_status_line()}", flush=True)

        # Update task status in plan
        try:
            update_task_status(plan_path, round_num, status)
        except Exception as exc:
            print(f"[overnight] WARNING: Could not update task status: {exc}", flush=True)

        # Save intermediate results.json (crash recovery)
        try:
            results_json_path.write_text(
                json.dumps(results, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"[overnight] WARNING: Could not save intermediate results: {exc}", flush=True)

        # --- Budget-aware: hourly rescan + burn mode ---
        if args.budget_aware and not task_queue:
            # Queue is empty — should we keep going?
            if tracker.hours_remaining() <= 0:
                print("[overnight] Window expired — stopping.", flush=True)
                break

            if tracker.should_burn():
                print("[overnight] BURN MODE — quota remaining, generating more tasks...", flush=True)
                # Rescan for fresh issues
                try:
                    new_code = scan_code()
                    new_content = scan_content()
                    write_findings(new_code, new_content, run_dir)
                    last_scan_time = datetime.now()
                    new_plan_path = generate_task_plan(run_dir, max_rounds=10)
                    new_tasks = parse_task_plan(new_plan_path)
                    new_pending = [t for t in new_tasks if t.get("status") == "pending"]
                    if new_pending:
                        # Renumber to avoid conflicts
                        for t in new_pending:
                            total_round_counter += 1
                            t["round"] = total_round_counter
                        task_queue.extend(new_pending)
                        print(f"[overnight]   Added {len(new_pending)} new tasks.", flush=True)
                    else:
                        print("[overnight]   No new tasks found. Stopping.", flush=True)
                        break
                except Exception as exc:
                    print(f"[overnight]   Rescan failed: {exc}. Stopping.", flush=True)
                    break

            elif tracker.should_rescan(last_scan_time):
                print("[overnight] Hourly rescan — checking for new issues...", flush=True)
                try:
                    new_code = scan_code()
                    new_content = scan_content()
                    write_findings(new_code, new_content, run_dir)
                    last_scan_time = datetime.now()
                    new_plan_path = generate_task_plan(run_dir, max_rounds=args.rounds)
                    new_tasks = parse_task_plan(new_plan_path)
                    new_pending = [t for t in new_tasks if t.get("status") == "pending"]
                    if new_pending:
                        for t in new_pending:
                            total_round_counter += 1
                            t["round"] = total_round_counter
                        task_queue.extend(new_pending)
                        print(f"[overnight]   Added {len(new_pending)} new tasks from rescan.", flush=True)
                except Exception as exc:
                    print(f"[overnight]   Rescan failed: {exc}", flush=True)
            else:
                # Non-budget-aware already drained the queue, just stop
                break

    # --- Phase 4: Generate report ---
    print("\n[overnight] Phase 4: Generating morning report...", flush=True)
    end_time = datetime.now()
    try:
        report_path = generate_report(results, start_time, end_time, run_dir)
        print(f"[overnight] Report written to: {report_path}", flush=True)
    except Exception as exc:
        print(f"[overnight] WARNING: Report generation failed: {exc}", flush=True)

    # Summary
    done = sum(1 for r in results if r.get("status") == "done")
    total = len(results)
    duration = (end_time - start_time).total_seconds() / 60
    print(
        f"\n[overnight] Done — {done}/{total} rounds succeeded in {duration:.1f} min.",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_with_caffeinate()
