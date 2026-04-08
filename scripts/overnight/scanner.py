"""
Scanner module for the overnight iteration system.

Collects quality signals from both code (ESLint, missing tests, ruff, pipeline bugs)
and content (chapter score JSON files). Outputs findings.md + findings.json.
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from scripts.overnight import config


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def scan_code() -> list[dict]:
    """
    Collect all code quality signals:
    - ESLint errors in the React website
    - Missing test files for components
    - Ruff warnings in Python scripts
    - Known bugs in the content pipeline

    Returns a list of finding dicts, sorted by severity descending.
    """
    findings: list[dict] = []

    # 1. ESLint
    eslint_result = _run_eslint()
    if eslint_result["error_count"] > 0:
        for file_path in eslint_result["files"]:
            findings.append({
                "type": "code-lint",
                "severity": 8,
                "target": _rel(file_path),
                "description": f"ESLint errors in {Path(file_path).name}",
                "details": eslint_result.get("raw", ""),
            })
        # Also add a summary finding if there are many
        if not eslint_result["files"]:
            findings.append({
                "type": "code-lint",
                "severity": 8,
                "target": "new-website/src",
                "description": f"ESLint: {eslint_result['error_count']} errors",
                "details": eslint_result.get("raw", ""),
            })

    # 2. Missing tests
    missing = find_missing_tests(config.WEBSITE_DIR / "src")
    for item in missing:
        findings.append({
            "type": "code-test",
            "severity": 6,
            "target": _rel(item["path"]),
            "description": f"No test file for {item['component']}",
            "details": f"Component at {item['path']} has no corresponding test",
        })

    # 3. Ruff (Python linting) — may not be installed, handle gracefully
    ruff_findings = _run_ruff()
    findings.extend(ruff_findings)

    # 4. Known pipeline bugs
    pipeline_findings = scan_pipeline_issues()
    findings.extend(pipeline_findings)

    # Sort by severity descending
    findings.sort(key=lambda f: f.get("severity", 0), reverse=True)
    return findings


def scan_content() -> list[dict]:
    """
    Read existing score JSON files and return chapters below the pass threshold.

    Returns a list of finding dicts for chapters that need improvement.
    """
    findings: list[dict] = []
    score_dir = config.SCRIPTS_DIR / "content_pipeline" / "output" / "scores"

    if not score_dir.exists():
        return findings

    for score_file in sorted(score_dir.glob("score_ch*.json")):
        try:
            with open(score_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        # Extract chapter number from filename: score_ch05.json → 5
        match = re.search(r"score_ch(\d+)\.json", score_file.name)
        chapter_num = int(match.group(1)) if match else None

        # Find the chapter file path
        chapter_path = _find_chapter_path(chapter_num) if chapter_num is not None else None

        parsed = parse_score_json(data, chapter_num=chapter_num, chapter_path=chapter_path)
        if parsed is None:
            continue

        # Only report chapters below the pass threshold
        avg = data.get("average", 0)
        if avg < config.SCORE_PASS_THRESHOLD:
            findings.append({
                "type": "content-refine",
                "severity": _content_severity(avg),
                "target": chapter_path or f"chapter {chapter_num}",
                "chapter_num": chapter_num,
                "description": (
                    f"{parsed['weakest_dimension']}: {parsed['weakest_score']}/10"
                ),
                "weaknesses": data.get("weaknesses", []),
                "suggestions": data.get("suggestions", []),
                "scores": data.get("scores", {}),
                "average": avg,
                "weakest_dimension": parsed["weakest_dimension"],
                "weakest_score": parsed["weakest_score"],
            })

    findings.sort(key=lambda f: f.get("severity", 0), reverse=True)
    return findings


def scan_pipeline_issues() -> list[dict]:
    """
    Detect known bugs in scripts/content_pipeline/quality_scorer.py:

    1. Uses OpenAI-only API (client.chat.completions.create) — needs ClaudeCodeClient
    2. Hard-truncates chapter text to 12000 chars — loses tail of long chapters

    Returns finding dicts with severity >= 9 and type "pipeline-fix".
    """
    findings: list[dict] = []
    scorer_path = config.SCRIPTS_DIR / "content_pipeline" / "quality_scorer.py"

    if not scorer_path.exists():
        return findings

    try:
        source = scorer_path.read_text(encoding="utf-8")
    except OSError:
        return findings

    # Bug 1: OpenAI-only API call without ClaudeCodeClient support
    if "client.chat.completions.create" in source:
        findings.append({
            "type": "pipeline-fix",
            "severity": 9,
            "target": _rel(scorer_path),
            "description": "quality_scorer uses OpenAI-only API (chat.completions.create)",
            "details": (
                "score_chapter() calls client.chat.completions.create which is "
                "OpenAI SDK only. Should use ClaudeCodeClient or the Anthropic SDK "
                "to support the Claude model."
            ),
        })

    # Bug 2: Hard chapter_text[:12000] truncation
    if re.search(r"chapter_text\[:\d+\]", source):
        findings.append({
            "type": "pipeline-fix",
            "severity": 9,
            "target": _rel(scorer_path),
            "description": "quality_scorer truncates chapter_text with hard [:12000] limit",
            "details": (
                "chapter_text[:12000] silently drops the end of long chapters "
                "before scoring. Should use token-aware truncation or remove the "
                "hard limit when using Claude's large context window."
            ),
        })

    return findings


def parse_eslint_output(output: str) -> dict:
    """
    Parse ESLint CLI output into a structured dict.

    Returns:
        {
            "error_count": int,       # number of error-severity issues
            "warning_count": int,     # number of warning-severity issues
            "files": list[str],       # file paths that have errors
            "raw": str,               # original output
        }
    """
    error_count = 0
    warning_count = 0
    files_with_errors: list[str] = []
    current_file: str | None = None

    for line in output.splitlines():
        stripped = line.strip()

        # File path lines look like: "/path/to/File.jsx" (no leading whitespace)
        if line and not line.startswith(" ") and not line.startswith("\t"):
            # Try to detect file paths — they start with / or ./ and end with extension
            if re.match(r"^[./].*\.[jt]sx?$", stripped):
                current_file = stripped

        # Error/warning lines: "  3:10  error  message  rule"
        match = re.match(r"^\s+\d+:\d+\s+(error|warning)\s+", line)
        if match:
            severity_word = match.group(1)
            if severity_word == "error":
                error_count += 1
                if current_file and current_file not in files_with_errors:
                    files_with_errors.append(current_file)
            else:
                warning_count += 1

    # Also try to parse the summary line: "✖ N problems (X errors, Y warnings)"
    summary_match = re.search(r"(\d+) errors?,\s*(\d+) warnings?", output)
    if summary_match:
        # Use summary counts if they're larger (more reliable)
        parsed_errors = int(summary_match.group(1))
        parsed_warnings = int(summary_match.group(2))
        if parsed_errors > error_count:
            error_count = parsed_errors
        if parsed_warnings > warning_count:
            warning_count = parsed_warnings

    return {
        "error_count": error_count,
        "warning_count": warning_count,
        "files": files_with_errors,
        "raw": output,
    }


def find_missing_tests(src_dir: Path) -> list[dict]:
    """
    Compare .jsx/.tsx components with their __tests__/ directories.

    A component is considered "missing tests" if there is no corresponding
    `.test.jsx` / `.test.tsx` file in the sibling `__tests__/` directory.

    Returns a list of dicts: [{"component": "Navbar.jsx", "path": "/abs/path"}]
    """
    missing: list[dict] = []

    if not src_dir.exists():
        return missing

    # Find all component files (exclude test files, main.jsx, App.jsx at root level)
    for component_file in sorted(src_dir.rglob("*.jsx")) + sorted(src_dir.rglob("*.tsx")):
        # Skip files inside __tests__ directories
        if "__tests__" in component_file.parts:
            continue
        # Skip main entry point and non-component files at src root
        if component_file.parent == src_dir:
            continue

        component_name = component_file.name  # e.g. "Navbar.jsx"
        tests_dir = component_file.parent / "__tests__"

        # Check if a test file exists for this component
        stem = component_file.stem  # e.g. "Navbar"
        has_test = False
        if tests_dir.exists():
            for ext in (".test.jsx", ".test.tsx", ".test.js", ".test.ts", ".spec.jsx", ".spec.tsx"):
                if (tests_dir / f"{stem}{ext}").exists():
                    has_test = True
                    break

        if not has_test:
            missing.append({
                "component": component_name,
                "path": str(component_file),
            })

    return missing


def parse_score_json(
    data: dict,
    chapter_num: int | None = None,
    chapter_path: str | None = None,
) -> dict | None:
    """
    Extract the weakest scoring dimension from a score JSON dict.

    Returns a dict with:
        {
            "chapter_num": int | None,
            "chapter_path": str | None,
            "weakest_dimension": str,
            "weakest_score": int | float,
            "average": float,
        }
    Returns None if the score data is malformed.
    """
    scores = data.get("scores", {})
    if not scores:
        return None

    # Find the dimension with the lowest score
    weakest_dim = min(scores, key=lambda d: scores[d])
    weakest_score = scores[weakest_dim]
    avg = data.get("average", 0)

    return {
        "chapter_num": chapter_num,
        "chapter_path": chapter_path,
        "weakest_dimension": weakest_dim,
        "weakest_score": weakest_score,
        "average": avg,
    }


def write_findings(
    code: list[dict],
    content: list[dict],
    run_dir: Path,
) -> tuple[Path, Path]:
    """
    Write findings to run_dir/findings.json and run_dir/findings.md.

    Returns (json_path, md_path).
    """
    run_dir.mkdir(parents=True, exist_ok=True)

    all_findings = {"code": code, "content": content}

    # --- JSON (for planner) ---
    json_path = run_dir / "findings.json"
    json_path.write_text(
        json.dumps(all_findings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # --- Markdown (for human reading) ---
    lines = [f"# Findings — {run_dir.name}\n"]

    for category, label in [("code", "Code Issues"), ("content", "Content Issues")]:
        items = all_findings[category]
        lines.append(f"\n## {label} ({len(items)} items)\n")
        if not items:
            lines.append("_No issues found._\n")
            continue
        for f in items:
            severity = f.get("severity", "?")
            ftype = f.get("type", "unknown")
            target = f.get("target", "")
            desc = f.get("description", "")
            lines.append(f"### [{severity}] {ftype}: {target}")
            lines.append(f"- **Description**: {desc}")
            details = f.get("details", "")
            if details:
                lines.append(f"- **Details**: {details}")
            # Content-specific fields
            if "weaknesses" in f and f["weaknesses"]:
                lines.append(f"- **Weaknesses**: {'; '.join(f['weaknesses'])}")
            if "suggestions" in f and f["suggestions"]:
                lines.append(f"- **Suggestions**: {'; '.join(f['suggestions'])}")
            lines.append("")

    md_path = run_dir / "findings.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, md_path


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _run_eslint() -> dict:
    """
    Run ESLint on the React website source directory.

    Returns the parsed output dict from parse_eslint_output().
    Handles the case where npm / eslint is not available.
    """
    src_dir = config.WEBSITE_DIR / "src"
    try:
        result = subprocess.run(
            ["npx", "eslint", str(src_dir), "--ext", ".jsx,.tsx,.js,.ts", "--max-warnings=0"],
            capture_output=True,
            text=True,
            cwd=str(config.WEBSITE_DIR),
            timeout=60,
        )
        output = result.stdout + result.stderr
        return parse_eslint_output(output)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return {"error_count": 0, "warning_count": 0, "files": [], "raw": ""}


def _run_ruff() -> list[dict]:
    """
    Run ruff on scripts/ to find Python linting issues.

    Returns a list of finding dicts (may be empty).
    Catches FileNotFoundError gracefully if ruff is not installed.
    """
    findings: list[dict] = []
    try:
        result = subprocess.run(
            ["ruff", "check", str(config.SCRIPTS_DIR), "--output-format=json"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return []

        try:
            issues = json.loads(result.stdout)
        except (json.JSONDecodeError, ValueError):
            # ruff returned non-JSON output — not critical
            return []

        # Group by file for cleaner findings
        files_seen: set[str] = set()
        for issue in issues:
            filepath = issue.get("filename", "")
            if filepath not in files_seen:
                files_seen.add(filepath)
                findings.append({
                    "type": "code-ruff",
                    "severity": 5,
                    "target": _rel(filepath),
                    "description": f"ruff: {issue.get('message', '')} ({issue.get('code', '')})",
                    "details": f"Line {issue.get('location', {}).get('row', '?')}",
                })

    except FileNotFoundError:
        # ruff is not installed — skip silently
        pass
    except subprocess.TimeoutExpired:
        pass

    return findings


def _run_score_all() -> list[dict]:
    """
    Read all score JSON files from the scores output directory.

    NOTE: This is intentionally NOT calling scan_content() to avoid
    infinite recursion. The score-reading logic is duplicated inline.

    Returns a list of raw score dicts with metadata.
    """
    results: list[dict] = []
    score_dir = config.SCRIPTS_DIR / "content_pipeline" / "output" / "scores"

    if not score_dir.exists():
        return results

    for score_file in sorted(score_dir.glob("score_ch*.json")):
        try:
            with open(score_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            match = re.search(r"score_ch(\d+)\.json", score_file.name)
            chapter_num = int(match.group(1)) if match else None
            data["_chapter_num"] = chapter_num
            data["_score_file"] = str(score_file)
            results.append(data)
        except (json.JSONDecodeError, OSError):
            continue

    return results


def _find_chapter_path(chapter_num: int) -> str | None:
    """Find the 正文/ file path for a given chapter number."""
    chapters_dir = config.CHAPTERS_DIR
    if not chapters_dir.exists():
        return None

    # Chapter files are named like "05_初出茅庐：社区与工具.md"
    pattern = f"{chapter_num:02d}_*.md"
    matches = list(chapters_dir.glob(pattern))
    if matches:
        return str(matches[0])

    # Also try without zero-padding for single-digit
    pattern_no_pad = f"{chapter_num}_*.md"
    matches = list(chapters_dir.glob(pattern_no_pad))
    if matches:
        return str(matches[0])

    return None


def _rel(path: str | Path) -> str:
    """Return a path relative to PROJECT_ROOT, or the path as-is if outside."""
    try:
        return str(Path(path).relative_to(config.PROJECT_ROOT))
    except ValueError:
        return str(path)


def _content_severity(average: float) -> int:
    """Map a chapter average score to a finding severity (1-10)."""
    if average < 5.0:
        return 9
    elif average < 6.0:
        return 8
    elif average < 7.0:
        return 7
    else:
        return 6
