"""
Reporter module for the overnight iteration system.

Generates the morning report (progress.md) and saves results.json so the
user can review what happened during the overnight run.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Status → display icon mapping
# ---------------------------------------------------------------------------

_STATUS_ICON: dict[str, str] = {
    "done": "pass",
    "failed": "FAIL",
    "error": "ERR",
    "skipped": "SKIP",
    "no-changes": "---",
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_report(
    results: list[dict[str, Any]],
    start_time: datetime,
    end_time: datetime,
    run_dir: Path,
) -> Path:
    """
    Write progress.md and results.json to run_dir and return the progress.md path.

    Args:
        results:    List of result dicts produced by executor.execute_round().
                    Each dict has: round, type, target, status, pr_url, verification.
        start_time: When the overnight run began.
        end_time:   When the overnight run finished.
        run_dir:    Directory where output files are written.

    Returns:
        Path to the written progress.md file.
    """
    # ---- persist raw results ------------------------------------------------
    json_path = run_dir / "results.json"
    json_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ---- derive summary stats -----------------------------------------------
    counts = _count_statuses(results)
    code_prs = sum(
        1 for r in results
        if r.get("status") == "done" and str(r.get("type", "")).startswith("code")
    )
    content_prs = sum(
        1 for r in results
        if r.get("status") == "done" and str(r.get("type", "")).startswith("content")
    )
    duration_h = (end_time - start_time).total_seconds() / 3600

    # ---- build markdown content ---------------------------------------------
    lines: list[str] = []

    # Header
    date_str = start_time.strftime("%Y-%m-%d")
    lines.append(f"# Overnight Run — {date_str}")
    lines.append(
        f"Started: {start_time.strftime('%H:%M')} | "
        f"Finished: {end_time.strftime('%H:%M')} | "
        f"Duration: {duration_h:.1f}h | "
        f"Rounds: {len(results)}"
    )
    lines.append("")

    # Summary section
    lines.append("## Summary")
    lines.append(f"- Completed: {counts['done']}")
    lines.append(f"- Failed: {counts['failed']}")
    lines.append(f"- Errors: {counts['error']}")
    lines.append(f"- Skipped: {counts['skipped']}")
    lines.append(f"- No changes: {counts['no-changes']}")
    lines.append(f"- Code PRs: {code_prs} | Content PRs: {content_prs}")
    lines.append("")

    # Results table
    lines.append("## Results")
    lines.append("| # | Type | Target | Result | PR | Detail |")
    lines.append("|---|------|--------|--------|----|--------|")
    for r in results:
        icon = _STATUS_ICON.get(r.get("status", ""), r.get("status", "?"))
        pr_url = r.get("pr_url") or ""
        # Display PR as short link text if possible
        pr_display = _format_pr(pr_url)
        reason = r.get("verification", {}).get("reason", "")
        # Truncate long reasons for table readability
        short_reason = reason[:60] + "…" if len(reason) > 60 else reason
        lines.append(
            f"| {r.get('round', '')} "
            f"| {r.get('type', '')} "
            f"| {r.get('target', '')} "
            f"| {icon} "
            f"| {pr_display} "
            f"| {short_reason} |"
        )
    lines.append("")

    # Failed tasks section
    failed = [r for r in results if r.get("status") in ("failed", "error")]
    if failed:
        lines.append("## Failed Tasks")
        for r in failed:
            lines.append(
                f"### Round {r.get('round', '?')}: "
                f"{r.get('type', '')} — {r.get('target', '')}"
            )
            reason = r.get("verification", {}).get("reason", "")
            lines.append(f"- Reason: {reason}")
            lines.append("")

    # Suggestions section
    actionable = [r for r in results if r.get("status") in ("failed", "error")]
    if actionable:
        lines.append("## Suggestions for Next Run")
        for r in actionable:
            lines.append(
                f"- Round {r.get('round', '?')} ({r.get('target', '')}): "
                "may need manual review"
            )
        lines.append("")

    # Write progress.md
    progress_path = run_dir / "progress.md"
    progress_path.write_text("\n".join(lines), encoding="utf-8")
    return progress_path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _count_statuses(results: list[dict]) -> dict[str, int]:
    """Return a dict mapping each known status to its occurrence count."""
    counts = {key: 0 for key in _STATUS_ICON}
    for r in results:
        status = r.get("status", "")
        if status in counts:
            counts[status] += 1
        # unknown statuses are ignored
    return counts


def _format_pr(pr_url: str) -> str:
    """
    Format a PR URL or identifier for the Markdown table cell.

    Examples:
        "https://github.com/user/repo/pull/42" → "[#42](https://…/pull/42)"
        "#1"                                   → "#1"
        ""                                     → ""
    """
    if not pr_url:
        return ""
    if pr_url.startswith("http"):
        # Extract pull number from URL
        parts = pr_url.rstrip("/").split("/")
        if len(parts) >= 2 and parts[-2] == "pull":
            num = parts[-1]
            return f"[#{num}]({pr_url})"
        return pr_url
    # Already short form like "#42"
    return pr_url
