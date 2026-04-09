"""
Executor module for the overnight iteration system.

Orchestrates one full improvement round:
  create worktree → run Claude → verify → commit + PR → cleanup
"""

import json
import os
import re
import shutil
import subprocess
from datetime import datetime, date
from pathlib import Path
from typing import Any

from scripts.overnight import config
from scripts.overnight.prompts import build_prompt


# ---------------------------------------------------------------------------
# Low-level shell helper
# ---------------------------------------------------------------------------


def _run_cmd(cmd: list[str], cwd: Path | None = None, timeout: int = 120) -> str:
    """
    Run a command (list of args) and return its stdout.

    Uses shell=False to prevent shell injection from paths and branch names
    that may contain spaces, Chinese characters, or special shell characters.

    Args:
        cmd: Command as a list of strings (e.g. ["git", "worktree", "list"]).
        cwd: Working directory; defaults to PROJECT_ROOT.
        timeout: Seconds before timeout (default 120).

    Returns:
        Decoded stdout string.

    Raises:
        subprocess.CalledProcessError: If the command exits non-zero.
        subprocess.TimeoutExpired: If the command times out.
    """
    cwd = cwd or config.PROJECT_ROOT
    result = subprocess.run(
        cmd,
        shell=False,
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=timeout,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr
        )
    return result.stdout


# ---------------------------------------------------------------------------
# Disk space check
# ---------------------------------------------------------------------------


def check_disk_space(min_gb: float = config.MIN_DISK_GB) -> bool:
    """
    Check that at least min_gb gigabytes of free disk space are available.

    Uses os.statvfs on the project root directory.

    Args:
        min_gb: Minimum required free space in GB (default from config).

    Returns:
        True if enough space is available, False otherwise.
    """
    stat = os.statvfs(str(config.PROJECT_ROOT))
    free_bytes = stat.f_frsize * stat.f_bavail
    free_gb = free_bytes / (1024 ** 3)
    return free_gb >= min_gb


# ---------------------------------------------------------------------------
# Worktree management
# ---------------------------------------------------------------------------


def cleanup_previous_runs() -> None:
    """
    Remove any leftover overnight worktrees and their branches.

    Steps:
      1. List all worktrees via `git worktree list`.
      2. Force-remove any whose path contains "overnight-wt-".
      3. Delete orphaned local branches matching overnight/*.
    """
    # Step 1: list worktrees
    raw = _run_cmd(["git", "worktree", "list"], cwd=config.PROJECT_ROOT)

    # Step 2: remove overnight worktrees
    for line in raw.splitlines():
        # Each line: "/absolute/path  abc1234 [branch-name]"
        path_str = line.split()[0] if line.strip() else ""
        if "overnight-wt-" in path_str:
            try:
                _run_cmd(
                    ["git", "worktree", "remove", "--force", path_str],
                    cwd=config.PROJECT_ROOT,
                )
            except subprocess.CalledProcessError:
                # Best-effort — continue if already gone
                pass

    # Step 3: delete orphaned overnight/* branches
    try:
        branch_output = _run_cmd(
            ["git", "branch", "--list", "overnight/*"],
            cwd=config.PROJECT_ROOT,
        )
        for branch_line in branch_output.splitlines():
            branch = branch_line.strip().lstrip("* ")
            if branch.startswith("overnight/"):
                try:
                    _run_cmd(
                        ["git", "branch", "-D", branch],
                        cwd=config.PROJECT_ROOT,
                    )
                except subprocess.CalledProcessError:
                    pass
    except subprocess.CalledProcessError:
        pass


def create_worktree(round_num: int, slug: str) -> Path:
    """
    Create a new git worktree for the given round.

    The worktree is created at WORKTREE_BASE/overnight-wt-{N} on a new branch
    named overnight/round-{N}-{slug}, based on main.

    Args:
        round_num: Round number (1-based).
        slug: URL-friendly label for the branch name.

    Returns:
        Path to the new worktree directory.
    """
    wt_name = f"overnight-wt-{round_num}"
    wt_path = config.WORKTREE_BASE / wt_name
    branch_name = f"overnight/round-{round_num}-{slug}"

    # Ensure parent directory exists
    config.WORKTREE_BASE.mkdir(parents=True, exist_ok=True)

    _run_cmd(
        ["git", "worktree", "add", str(wt_path), "-b", branch_name, "main"],
        cwd=config.PROJECT_ROOT,
        timeout=60,
    )

    # Symlink node_modules from main repo so vitest/eslint work in worktree
    main_nm = config.WEBSITE_DIR / "node_modules"
    wt_website = wt_path / "new-website"
    if main_nm.exists() and wt_website.exists():
        wt_nm = wt_website / "node_modules"
        if not wt_nm.exists():
            wt_nm.symlink_to(main_nm)

    return wt_path


def remove_worktree(wt_path: Path) -> None:
    """
    Force-remove a git worktree.

    Args:
        wt_path: Absolute path to the worktree directory.
    """
    _run_cmd(
        ["git", "worktree", "remove", "--force", str(wt_path)],
        cwd=config.PROJECT_ROOT,
        timeout=60,
    )


# ---------------------------------------------------------------------------
# Content backup
# ---------------------------------------------------------------------------


def create_content_backup(chapter_path: Path, history_dir: Path) -> Path:
    """
    Copy a chapter file to the history directory before modification.

    Backup filename: {YYYY-MM-DD}_{stem}_pre-overnight.md

    Args:
        chapter_path: Path to the chapter file to back up.
        history_dir: Directory where backup files are stored.

    Returns:
        Path to the newly created backup file.
    """
    history_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    backup_name = f"{today}_{chapter_path.stem}_pre-overnight.md"
    backup_path = history_dir / backup_name
    shutil.copy2(chapter_path, backup_path)
    return backup_path


# ---------------------------------------------------------------------------
# Claude invocation
# ---------------------------------------------------------------------------


def run_claude(
    prompt: str,
    worktree_path: Path,
    timeout: int = config.DEFAULT_TIMEOUT,
) -> str:
    """
    Run the Claude CLI with the given prompt passed via stdin.

    Executes:
      claude -p --model {model} --output-format text
             --allowedTools {tools}
    with subprocess cwd set to the worktree directory.

    Args:
        prompt: The prompt text to send via stdin.
        worktree_path: The worktree directory (subprocess cwd).
        timeout: Seconds before timeout (default from config).

    Returns:
        Claude's text output (stdout).

    Raises:
        subprocess.CalledProcessError: If claude exits non-zero.
        subprocess.TimeoutExpired: If the call times out.
    """
    tools_str = ",".join(config.ALLOWED_TOOLS)
    cmd = [
        "claude", "-p",
        "--model", config.CLAUDE_MODEL,
        "--output-format", "text",
        "--no-session-persistence",
        "--permission-mode", "auto",
        "--allowedTools", tools_str,
    ]
    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(worktree_path),
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr
        )
    return result.stdout


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def verify_task(
    task: dict[str, Any],
    worktree_path: Path,
    before_score: dict | None = None,
) -> dict[str, Any]:
    """
    Dispatch to the type-specific verifier for the given task.

    Args:
        task: Task dict containing at least {"type": str, "target": str}.
        worktree_path: Path to the worktree where changes were made.
        before_score: Optional pre-change score dict for content-refine tasks.

    Returns:
        A dict: {"passed": bool, "reason": str, "details": dict}
    """
    task_type = task.get("type", "")

    if task_type == "code-lint":
        return _verify_lint(worktree_path)
    elif task_type == "code-ruff":
        return _verify_ruff(task, worktree_path)
    elif task_type == "code-test":
        return _verify_tests(worktree_path)
    elif task_type == "code-refactor":
        # Refactor must not break existing tests
        return _verify_tests(worktree_path)
    elif task_type == "content-refine":
        return _verify_content(task, worktree_path, before_score)
    elif task_type == "pipeline-fix":
        return _verify_pipeline(task, worktree_path)
    else:
        return {"passed": False, "reason": f"Unknown task type: {task_type!r}", "details": {}}


def _verify_lint(worktree_path: Path) -> dict[str, Any]:
    """Run npm run lint in new-website; pass if exit code 0."""
    website_dir = worktree_path / "new-website"
    try:
        _run_cmd(["npm", "run", "lint"], cwd=website_dir, timeout=120)
        return {"passed": True, "reason": "npm run lint passed", "details": {}}
    except subprocess.CalledProcessError as exc:
        return {
            "passed": False,
            "reason": "npm run lint failed",
            "details": {"stderr": exc.stderr, "stdout": exc.output},
        }
    except Exception as exc:
        return {"passed": False, "reason": str(exc), "details": {}}


def _verify_ruff(task: dict, worktree_path: Path) -> dict[str, Any]:
    """Run ruff check on the target file; pass if exit code 0 (no violations)."""
    target = task.get("target", "")
    target_path = worktree_path / target
    try:
        _run_cmd(["ruff", "check", str(target_path)], cwd=worktree_path, timeout=60)
        return {"passed": True, "reason": "ruff check passed", "details": {}}
    except subprocess.CalledProcessError as exc:
        return {
            "passed": False,
            "reason": "ruff check failed",
            "details": {"stderr": exc.stderr, "stdout": exc.output},
        }
    except Exception as exc:
        return {"passed": False, "reason": str(exc), "details": {}}


def _verify_tests(worktree_path: Path) -> dict[str, Any]:
    """Run npx vitest run in new-website; pass if exit code 0."""
    website_dir = worktree_path / "new-website"
    try:
        _run_cmd(["npx", "vitest", "run"], cwd=website_dir, timeout=180)
        return {"passed": True, "reason": "npx vitest run passed", "details": {}}
    except subprocess.CalledProcessError as exc:
        return {
            "passed": False,
            "reason": "npx vitest run failed",
            "details": {"stderr": exc.stderr, "stdout": exc.output},
        }
    except Exception as exc:
        return {"passed": False, "reason": str(exc), "details": {}}


def _verify_content(
    task: dict,
    worktree_path: Path,
    before_score: dict | None,
) -> dict[str, Any]:
    """
    Re-score the chapter and compare with before_score.

    Passes if the weakest dimension improved by at least SCORE_IMPROVEMENT_MIN.
    Falls back to a simple "file was modified" check if scoring is unavailable.
    """
    target = task.get("target", "")
    weakest_dim = task.get("weakest_dimension", "")
    before_dim_score = task.get("weakest_score")

    # Locate the modified chapter file in the worktree
    chapter_path = worktree_path / target

    if not chapter_path.exists():
        return {
            "passed": False,
            "reason": f"Chapter file not found in worktree: {target}",
            "details": {},
        }

    # If we have a before score, try to re-score and compare
    if before_score and weakest_dim and before_dim_score is not None:
        try:
            # Try to import the quality scorer if available
            from scripts.content_pipeline.quality_scorer import score_chapter  # type: ignore
            after_data = score_chapter(chapter_path.read_text(encoding="utf-8"))
            after_scores = after_data.get("scores", {})
            after_dim_score = after_scores.get(weakest_dim, before_dim_score)
            improvement = after_dim_score - float(before_dim_score)

            if improvement >= config.SCORE_IMPROVEMENT_MIN:
                return {
                    "passed": True,
                    "reason": (
                        f"{weakest_dim} improved from {before_dim_score} "
                        f"to {after_dim_score} (+{improvement:.1f})"
                    ),
                    "details": {"before": before_dim_score, "after": after_dim_score},
                }
            else:
                return {
                    "passed": False,
                    "reason": (
                        f"{weakest_dim} did not improve enough: "
                        f"{before_dim_score} → {after_dim_score}"
                    ),
                    "details": {"before": before_dim_score, "after": after_dim_score},
                }
        except ImportError:
            pass

    # Fallback: just verify the file exists and is non-empty
    content = chapter_path.read_text(encoding="utf-8")
    if content.strip():
        return {
            "passed": True,
            "reason": "Chapter file exists and is non-empty (scorer unavailable)",
            "details": {},
        }
    return {"passed": False, "reason": "Chapter file is empty after edit", "details": {}}


def _verify_pipeline(task: dict, worktree_path: Path) -> dict[str, Any]:
    """
    Verify a pipeline fix by attempting to import the modified module.

    Simple import check: if the file can be parsed as Python without errors,
    the fix is likely valid. Full pytest is optional.
    """
    target = task.get("target", "")
    module_path = worktree_path / target

    if not module_path.exists():
        return {"passed": False, "reason": f"Target not found: {target}", "details": {}}

    try:
        # Use py_compile to check for syntax errors
        import py_compile
        py_compile.compile(str(module_path), doraise=True)
        return {"passed": True, "reason": "Python syntax check passed", "details": {}}
    except py_compile.PyCompileError as exc:
        return {"passed": False, "reason": f"Syntax error: {exc}", "details": {}}
    except Exception as exc:
        return {"passed": False, "reason": str(exc), "details": {}}


# ---------------------------------------------------------------------------
# Commit and PR
# ---------------------------------------------------------------------------


def commit_and_pr(
    worktree_path: Path,
    task: dict[str, Any],
    round_num: int,
    verification: dict[str, Any],
) -> str | None:
    """
    Stage all changes, commit, push, and open a GitHub PR.

    CRITICAL: Uses subprocess.run with LIST args (NOT shell=True) for the
    commit step to avoid shell injection from Chinese chapter names and
    special characters (colons, dots, etc.) in commit messages.

    Args:
        worktree_path: Path to the worktree with changes.
        task: Task dict for commit message context.
        round_num: Current round number.
        verification: Verification result dict.

    Returns:
        PR URL string, or None if PR creation failed.
    """
    task_type = task.get("type", "unknown")
    target = task.get("target", "")
    reason = verification.get("reason", "")

    # Build commit message — safe for Chinese and special chars via list args
    msg = f"overnight({task_type}): round {round_num} — {target}\n\nVerification: {reason}"

    # Determine current branch name from worktree
    try:
        branch_raw = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=str(worktree_path),
            timeout=30,
        )
        branch = branch_raw.stdout.strip()
    except Exception:
        branch = f"overnight/round-{round_num}-unknown"

    # Step 1: git add -A (list args, safe)
    subprocess.run(
        ["git", "add", "-A"],
        cwd=str(worktree_path),
        check=True,
        timeout=60,
    )

    # Step 2: git commit -m {msg} (list args — avoids shell injection)
    subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=str(worktree_path),
        check=True,
        timeout=60,
    )

    # Step 3: git push -u origin {branch}
    subprocess.run(
        ["git", "push", "-u", "origin", branch],
        cwd=str(worktree_path),
        check=True,
        timeout=120,
    )

    # Step 4: gh pr create
    pr_title = f"overnight: round {round_num} — {task_type} ({target})"
    pr_body = (
        f"## Overnight Round {round_num}\n\n"
        f"**Type**: {task_type}\n"
        f"**Target**: `{target}`\n"
        f"**Verification**: {reason}\n\n"
        f"_Auto-generated by the overnight iteration system._"
    )
    try:
        result = subprocess.run(
            ["gh", "pr", "create",
             "--title", pr_title,
             "--body", pr_body,
             "--head", branch,
             "--base", "main"],
            capture_output=True,
            text=True,
            cwd=str(worktree_path),
            timeout=60,
        )
        if result.returncode == 0:
            # gh pr create outputs the PR URL on stdout
            return result.stdout.strip()
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Target file pre-reader
# ---------------------------------------------------------------------------


def _read_target_files(task: dict[str, Any]) -> dict[str, str]:
    """
    Pre-read target file contents for inclusion in the Claude prompt.

    For code tasks, reads the target file from PROJECT_ROOT.
    For content-refine tasks, reads the chapter from CHAPTERS_DIR.

    Returns:
        Dict mapping filename → file content (empty dict on read failure).
    """
    target = task.get("target", "")
    if not target:
        return {}

    # Resolve against project root
    abs_path = config.PROJECT_ROOT / target

    if not abs_path.exists():
        return {}

    try:
        content = abs_path.read_text(encoding="utf-8")
        return {target: content}
    except OSError:
        return {}


# ---------------------------------------------------------------------------
# Slug helper
# ---------------------------------------------------------------------------


def _slugify(text: str) -> str:
    """
    Convert text to a URL-friendly slug (lowercase, hyphens, ASCII only).

    Examples:
        "Fix ESLint errors" → "fix-eslint-errors"
        "第一次泡沫"        → "content-refine"  (falls back for non-ASCII)

    Args:
        text: Input string to slugify.

    Returns:
        Slug string suitable for use in branch names.
    """
    # Lowercase and replace whitespace with hyphens
    slug = text.lower().strip()
    slug = re.sub(r"[\s_]+", "-", slug)
    # Remove non-ASCII, non-alphanumeric, non-hyphen characters
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    # If nothing is left (e.g., pure Chinese), use a type-based fallback
    return slug or "task"


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------


def execute_round(
    task: dict[str, Any],
    round_num: int,
    run_dir: Path,
    timeout: int = config.DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """
    Orchestrate one complete improvement round.

    Steps:
      1. Check disk space
      2. Backup chapter (content-refine tasks only)
      3. Create git worktree
      4. Pre-read target files
      5. Build Claude prompt
      6. Run Claude CLI
      7. Verify the change
      8. Commit + create PR (if verification passed)
      9. Cleanup worktree
      10. Return result dict

    Args:
        task: Task dict from the planner (must include type, target, round).
        round_num: Round number (1-based).
        run_dir: Directory for storing logs and round artifacts.
        timeout: Seconds before the Claude CLI call times out.

    Returns:
        Result dict with keys: round, type, target, status, pr_url,
        verification, started_at, finished_at.
    """
    started_at = datetime.now().isoformat()
    task_type = task.get("type", "unknown")
    target = task.get("target", "")

    result: dict[str, Any] = {
        "round": round_num,
        "type": task_type,
        "target": target,
        "status": "error",
        "pr_url": None,
        "verification": {"passed": False, "reason": "Not started", "details": {}},
        "started_at": started_at,
        "finished_at": None,
    }

    wt_path: Path | None = None

    try:
        # Step 1: Disk space check
        if not check_disk_space():
            result["status"] = "skipped"
            result["verification"]["reason"] = "Insufficient disk space"
            return result

        # Step 2: Backup for content tasks
        if task_type == "content-refine" and target:
            chapter_abs = config.CHAPTERS_DIR / Path(target).name
            history_dir = config.CHAPTERS_DIR / "历史版本"
            if chapter_abs.exists():
                try:
                    create_content_backup(chapter_abs, history_dir)
                except OSError:
                    pass  # Backup failure is non-fatal

        # Step 3: Create worktree
        slug = _slugify(task.get("description", task.get("issue", task_type)))
        wt_path = create_worktree(round_num, slug[:30])  # cap slug length for branch names

        # Step 4: Pre-read target files
        file_contents = _read_target_files(task)

        # Step 5: Build prompt
        prompt = build_prompt(task, file_contents)

        # Step 6: Run Claude
        try:
            run_claude(prompt, wt_path, timeout=timeout)
        except subprocess.CalledProcessError as exc:
            result["status"] = "error"
            result["verification"]["reason"] = f"Claude CLI failed: {exc.stderr or exc.output}"
            return result
        except subprocess.TimeoutExpired:
            result["status"] = "error"
            result["verification"]["reason"] = "Claude CLI timed out"
            return result

        # Step 7: Verify
        before_score = {
            "weakest_dimension": task.get("weakest_dimension"),
            "weakest_score": task.get("weakest_score"),
            "scores": task.get("scores", {}),
        } if task_type == "content-refine" else None

        verification = verify_task(task, wt_path, before_score)
        result["verification"] = verification

        # Check if there are actually any changes to commit
        diff_check = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=str(wt_path),
            capture_output=True,
        )
        # Also check unstaged changes
        diff_unstaged = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(wt_path),
            capture_output=True,
            text=True,
        )

        has_changes = bool(diff_unstaged.stdout.strip())

        if not has_changes:
            result["status"] = "no-changes"
            result["verification"]["reason"] = "No file changes detected after Claude run"
            return result

        # Step 8: Commit and PR (only if verification passed)
        if verification.get("passed"):
            try:
                pr_url = commit_and_pr(wt_path, task, round_num, verification)
                result["pr_url"] = pr_url
                result["status"] = "done"
            except subprocess.CalledProcessError as exc:
                result["status"] = "failed"
                result["verification"]["reason"] = (
                    f"Commit/PR failed: {exc.stderr or str(exc)}"
                )
        else:
            result["status"] = "failed"

    except Exception as exc:
        result["status"] = "error"
        result["verification"]["reason"] = f"Unexpected error: {exc}"

    finally:
        # Step 9: Always cleanup the worktree
        if wt_path is not None and wt_path.exists():
            try:
                remove_worktree(wt_path)
            except Exception:
                pass  # Best-effort cleanup

        result["finished_at"] = datetime.now().isoformat()

    return result
