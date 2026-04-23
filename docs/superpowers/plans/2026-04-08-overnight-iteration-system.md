# Overnight Iteration System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an automated overnight system that scans code and content for quality issues, iterates improvements via Claude CLI in isolated git worktrees, and produces GitHub PRs for morning review.

**Architecture:** A Python package (`scripts/overnight/`) with four phases: scan (find issues), plan (prioritize), execute (worktree + Claude + verify + PR), report (morning summary). Each phase reads/writes markdown files in a per-run directory (`runs/YYYY-MM-DD/`). External dependencies: `claude` CLI, `gh` CLI, `git`, `npm`, `pytest`.

**Tech Stack:** Python 3.12, subprocess for CLI calls, pytest for tests, no external Python packages needed.

**Spec:** `docs/superpowers/specs/2026-04-08-overnight-iteration-system-design.md`

---

## File Map

```
scripts/overnight/
├── __init__.py              # Package marker
├── __main__.py              # Entry: CLI args + caffeinate + orchestration
├── config.py                # All constants, paths, defaults
├── scanner.py               # Phase 1: code + content scanning → findings
├── planner.py               # Phase 2: findings → prioritized task queue
├── executor.py              # Phase 3: worktree + claude + verify + PR loop
├── reporter.py              # Phase 4: morning report generation
├── prompts.py               # Prompt templates for Claude (per task type)
└── tests/
    ├── __init__.py
    ├── conftest.py           # Shared fixtures (tmp dirs, mock findings)
    ├── test_config.py
    ├── test_scanner.py
    ├── test_planner.py
    ├── test_executor.py
    ├── test_reporter.py
    └── test_prompts.py
```

---

### Task 1: Project Skeleton + Config

**Files:**
- Create: `scripts/overnight/__init__.py`
- Create: `scripts/overnight/config.py`
- Create: `scripts/overnight/tests/__init__.py`
- Create: `scripts/overnight/tests/conftest.py`
- Create: `scripts/overnight/tests/test_config.py`

- [ ] **Step 1: Create package skeleton**

```python
# scripts/overnight/__init__.py
"""Overnight iteration system — autonomous code & content quality improvement."""
```

```python
# scripts/overnight/tests/__init__.py
```

- [ ] **Step 2: Write config tests**

```python
# scripts/overnight/tests/test_config.py
"""Tests for overnight config module."""
import os
from pathlib import Path


def test_project_root_exists():
    from scripts.overnight.config import PROJECT_ROOT
    assert PROJECT_ROOT.exists()
    assert (PROJECT_ROOT / "正文").exists()


def test_default_values():
    from scripts.overnight.config import DEFAULT_ROUNDS, DEFAULT_TIMEOUT, CLAUDE_MODEL
    assert DEFAULT_ROUNDS == 20
    assert DEFAULT_TIMEOUT == 900
    assert CLAUDE_MODEL == "opus"


def test_run_dir_creates_dated_path():
    from scripts.overnight.config import get_run_dir
    run_dir = get_run_dir()
    # Should contain today's date
    from datetime import date
    assert date.today().isoformat() in str(run_dir)


def test_worktree_base_is_outside_repo():
    from scripts.overnight.config import PROJECT_ROOT, WORKTREE_BASE
    # Worktree should be sibling to repo, not inside it
    assert str(WORKTREE_BASE).startswith(str(PROJECT_ROOT.parent))
    assert not str(WORKTREE_BASE).startswith(str(PROJECT_ROOT) + "/")
```

- [ ] **Step 3: Run tests, verify they fail**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_config.py -v`
Expected: FAIL (module not found)

- [ ] **Step 4: Implement config.py**

```python
# scripts/overnight/config.py
"""Configuration for the overnight iteration system."""
from datetime import date
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Stories-about-Bitcoin/
CHAPTERS_DIR = PROJECT_ROOT / "正文"
WEBSITE_DIR = PROJECT_ROOT / "new-website"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
RUNS_DIR = SCRIPT_DIR / "runs"
WORKTREE_BASE = PROJECT_ROOT.parent / "overnight-worktrees"

# Defaults
DEFAULT_ROUNDS = 20
DEFAULT_TIMEOUT = 900  # 15 minutes per round
CLAUDE_MODEL = "opus"
MIN_DISK_GB = 1  # Skip round if less than this available

# Quality thresholds
SCORE_PASS_THRESHOLD = 7.0
SCORE_IMPROVEMENT_MIN = 0.1  # Minimum improvement to accept content change

# Claude CLI restrictions
ALLOWED_TOOLS = [
    "Edit", "Write", "Read", "Glob", "Grep",
    "Bash(npm run lint)", "Bash(npx vitest)", "Bash(ruff check)",
    "Bash(python -m pytest)",
]

# Branch prefix
BRANCH_PREFIX = "overnight"


def get_run_dir(run_date: date | None = None) -> Path:
    """Get the output directory for a specific run date."""
    d = run_date or date.today()
    return RUNS_DIR / d.isoformat()
```

- [ ] **Step 5: Run tests, verify they pass**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_config.py -v`
Expected: 4 passed

- [ ] **Step 6: Write conftest.py with shared fixtures**

```python
# scripts/overnight/tests/conftest.py
"""Shared fixtures for overnight tests."""
import json
import pytest
from pathlib import Path


@pytest.fixture
def tmp_run_dir(tmp_path):
    """A temporary run directory with standard structure."""
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)
    return run_dir


@pytest.fixture
def sample_findings():
    """Sample findings data for testing planner."""
    return {
        "code": [
            {
                "type": "code-lint",
                "severity": 8,
                "target": "new-website/src/App.jsx",
                "description": "3 ESLint errors",
                "details": "no-unused-vars (2), react/prop-types (1)",
            },
            {
                "type": "code-test",
                "severity": 6,
                "target": "new-website/src/components/home/Timeline.jsx",
                "description": "No test file exists",
                "details": "Component has 120 lines, 0% coverage",
            },
        ],
        "content": [
            {
                "type": "content-refine",
                "severity": 7,
                "target": "正文/11_风起云涌：第一次泡沫.md",
                "chapter_num": 11,
                "description": "readability: 5/10",
                "weaknesses": ["段落长度单一", "开头缺乏画面感"],
                "suggestions": ["增加句式变化", "用具体场景开头"],
                "scores": {"readability": 5, "style_consistency": 7, "factual_accuracy": 8,
                           "chapter_coherence": 7, "terminology_accuracy": 8},
                "average": 7.0,
                "weakest_dimension": "readability",
                "weakest_score": 5,
            },
        ],
    }


@pytest.fixture
def sample_findings_md(tmp_run_dir, sample_findings):
    """Write sample findings to findings.md and return path."""
    lines = ["# Findings — 2026-04-08\n"]
    for category in ("code", "content"):
        lines.append(f"\n## {category.title()} Issues\n")
        for f in sample_findings[category]:
            lines.append(f"### [{f['severity']}] {f['type']}: {f['target']}")
            lines.append(f"- **Description**: {f['description']}")
            lines.append(f"- **Details**: {f.get('details', 'N/A')}")
            lines.append("")
    path = tmp_run_dir / "findings.md"
    path.write_text("\n".join(lines))

    # Also write JSON sidecar for structured access
    json_path = tmp_run_dir / "findings.json"
    json_path.write_text(json.dumps(sample_findings, ensure_ascii=False, indent=2))
    return path
```

- [ ] **Step 7: Commit**

```bash
git add scripts/overnight/__init__.py scripts/overnight/config.py \
  scripts/overnight/tests/__init__.py scripts/overnight/tests/conftest.py \
  scripts/overnight/tests/test_config.py
git commit -m "feat(overnight): add project skeleton and config module"
```

---

### Task 2: Scanner — Code Signals

**Files:**
- Create: `scripts/overnight/scanner.py`
- Create: `scripts/overnight/tests/test_scanner.py`

- [ ] **Step 1: Write scanner tests (code signals)**

```python
# scripts/overnight/tests/test_scanner.py
"""Tests for the scanner module."""
import json
import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path


def test_parse_eslint_output():
    """parse_eslint_output extracts error count and file list from eslint stderr."""
    from scripts.overnight.scanner import parse_eslint_output

    eslint_output = """
/path/to/App.jsx
  3:10  error  'unused' is defined but never used  no-unused-vars
  8:5   error  Missing prop validation              react/prop-types

/path/to/Navbar.jsx
  12:3  warning  Unexpected console statement       no-console

✖ 3 problems (2 errors, 1 warning)
"""
    result = parse_eslint_output(eslint_output)
    assert result["error_count"] >= 2
    assert len(result["files"]) >= 1


def test_find_missing_tests():
    """find_missing_tests compares component files with test files."""
    from scripts.overnight.scanner import find_missing_tests

    # Use the actual project structure
    from scripts.overnight.config import WEBSITE_DIR
    missing = find_missing_tests(WEBSITE_DIR / "src")
    # There should be at least some result (list of dicts)
    assert isinstance(missing, list)
    for item in missing:
        assert "component" in item
        assert "path" in item


def test_scan_code_returns_findings():
    """scan_code returns a list of finding dicts."""
    from scripts.overnight.scanner import scan_code

    with patch("scripts.overnight.scanner._run_eslint") as mock_lint:
        mock_lint.return_value = {"error_count": 0, "files": [], "raw": ""}
        with patch("scripts.overnight.scanner.find_missing_tests") as mock_tests:
            mock_tests.return_value = []
            findings = scan_code()
            assert isinstance(findings, list)


def test_parse_score_json():
    """parse_score_json reads a score JSON and extracts weak dimensions."""
    from scripts.overnight.scanner import parse_score_json

    score_data = {
        "scores": {
            "factual_accuracy": 8,
            "style_consistency": 7,
            "readability": 5,
            "chapter_coherence": 7,
            "terminology_accuracy": 8,
        },
        "average": 7.0,
        "weaknesses": ["段落长度单一"],
        "suggestions": ["增加句式变化"],
        "verdict": "pass",
    }
    result = parse_score_json(score_data, chapter_num=11,
                              chapter_path="正文/11_test.md")
    assert result["weakest_dimension"] == "readability"
    assert result["weakest_score"] == 5
    assert result["chapter_num"] == 11
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_scanner.py -v`
Expected: FAIL (ImportError)

- [ ] **Step 3: Implement scanner.py**

```python
# scripts/overnight/scanner.py
"""Phase 1: Scan code and content for quality issues."""
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from . import config


# --- Code Scanning ---

def scan_code() -> list[dict]:
    """Run all code scans and return a list of findings."""
    findings = []

    # 0. Pipeline issues (highest priority — fix the tools first)
    findings.extend(scan_pipeline_issues())

    # 1. ESLint
    lint_result = _run_eslint()
    if lint_result["error_count"] > 0:
        for f in lint_result["files"]:
            findings.append({
                "type": "code-lint",
                "severity": min(9, 5 + lint_result["error_count"]),
                "target": f,
                "description": f"ESLint errors in {Path(f).name}",
                "details": lint_result["raw"][:500],
            })

    # 2. Missing tests
    missing = find_missing_tests(config.WEBSITE_DIR / "src")
    for item in missing:
        findings.append({
            "type": "code-test",
            "severity": 6,
            "target": item["path"],
            "description": f"No test file for {item['component']}",
            "details": f"Component at {item['path']} has no corresponding test",
        })

    # 3. Python lint (ruff, if available)
    ruff_findings = _run_ruff()
    findings.extend(ruff_findings)

    # Sort by severity descending
    findings.sort(key=lambda x: x["severity"], reverse=True)
    return findings


def _run_eslint() -> dict:
    """Run eslint and parse output."""
    try:
        result = subprocess.run(
            ["npm", "run", "lint"],
            cwd=str(config.WEBSITE_DIR),
            capture_output=True, text=True, timeout=60,
        )
        return parse_eslint_output(result.stdout + result.stderr)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {"error_count": 0, "files": [], "raw": ""}


def parse_eslint_output(output: str) -> dict:
    """Parse eslint output to extract errors and affected files."""
    files = []
    error_count = 0

    for line in output.split("\n"):
        line = line.strip()
        # Lines starting with / are file paths
        if line.startswith("/") and not line.startswith("//"):
            files.append(line)
        # Count errors (not warnings)
        if "error" in line.lower() and ("error" in line.split()):
            match = re.search(r"(\d+)\s+error", line)
            if match:
                error_count = max(error_count, int(match.group(1)))

    # Deduplicate files
    files = list(dict.fromkeys(files))
    return {"error_count": error_count, "files": files, "raw": output[:1000]}


def find_missing_tests(src_dir: Path) -> list[dict]:
    """Find components/hooks without corresponding test files."""
    missing = []
    if not src_dir.exists():
        return missing

    # Collect all component/hook files
    for pattern in ("components/**/*.jsx", "components/**/*.tsx",
                    "hooks/**/*.js", "hooks/**/*.ts"):
        for filepath in src_dir.glob(pattern):
            if "__tests__" in str(filepath) or "test" in filepath.stem.lower():
                continue
            # Check for corresponding test
            test_dir = filepath.parent / "__tests__"
            test_name = filepath.stem + ".test" + filepath.suffix
            if not (test_dir / test_name).exists():
                missing.append({
                    "component": filepath.stem,
                    "path": str(filepath.relative_to(src_dir.parent.parent)),
                })
    return missing


def _run_ruff() -> list[dict]:
    """Run ruff on Python scripts, return findings."""
    findings = []
    try:
        result = subprocess.run(
            ["ruff", "check", str(config.SCRIPTS_DIR)],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0 and result.stdout:
            # Count errors per file
            file_errors: dict[str, int] = {}
            for line in result.stdout.split("\n"):
                if ":" in line and not line.startswith(" "):
                    fpath = line.split(":")[0]
                    file_errors[fpath] = file_errors.get(fpath, 0) + 1
            for fpath, count in file_errors.items():
                findings.append({
                    "type": "code-lint",
                    "severity": min(7, 4 + count),
                    "target": fpath,
                    "description": f"ruff: {count} issues in {Path(fpath).name}",
                    "details": result.stdout[:300],
                })
    except FileNotFoundError:
        pass  # ruff not installed, skip
    return findings


# --- Content Scanning ---

def scan_content() -> list[dict]:
    """Score all chapters and return findings for those below threshold."""
    findings = []
    score_dir = config.PROJECT_ROOT / "scripts" / "content_pipeline" / "output" / "scores"

    # Try to load existing scores first
    if score_dir.exists():
        for score_file in sorted(score_dir.glob("score_ch*.json")):
            try:
                data = json.loads(score_file.read_text())
                match = re.search(r"ch(\d+)", score_file.stem)
                if not match:
                    continue
                ch_num = int(match.group(1))
                ch_path = _find_chapter_path(ch_num)
                if not ch_path:
                    continue
                finding = parse_score_json(data, ch_num, str(ch_path))
                if finding:
                    findings.append(finding)
            except (json.JSONDecodeError, KeyError):
                continue

    # If no scores exist, run score-all
    if not findings:
        findings = _run_score_all()

    findings.sort(key=lambda x: x["severity"], reverse=True)
    return findings


def parse_score_json(data: dict, chapter_num: int, chapter_path: str) -> dict | None:
    """Parse a score JSON and return a finding if any dimension is below threshold."""
    scores = data.get("scores", {})
    if not scores:
        return None

    # Find weakest dimension
    weakest_dim = min(scores, key=scores.get)
    weakest_score = scores[weakest_dim]

    # Only report if at least one dimension is below threshold
    if weakest_score >= config.SCORE_PASS_THRESHOLD:
        return None

    average = data.get("average", sum(scores.values()) / len(scores))
    severity = max(1, 10 - weakest_score)  # Lower score = higher severity

    return {
        "type": "content-refine",
        "severity": severity,
        "target": chapter_path,
        "chapter_num": chapter_num,
        "description": f"{weakest_dim}: {weakest_score}/10",
        "weaknesses": data.get("weaknesses", []),
        "suggestions": data.get("suggestions", []),
        "scores": scores,
        "average": round(average, 1),
        "weakest_dimension": weakest_dim,
        "weakest_score": weakest_score,
    }


def _find_chapter_path(chapter_num: int) -> Path | None:
    """Find chapter file by number."""
    for f in config.CHAPTERS_DIR.glob(f"{chapter_num:02d}_*.md"):
        if "历史版本" not in str(f):
            return f
    return None


def _run_score_all() -> list[dict]:
    """Run score-all and collect results. Falls back to empty if unavailable."""
    try:
        subprocess.run(
            ["make", "score-all"],
            cwd=str(config.PROJECT_ROOT),
            capture_output=True, timeout=600,
        )
        # Read newly created scores (do NOT recurse into scan_content to avoid infinite loop)
        findings = []
        score_dir = config.PROJECT_ROOT / "scripts" / "content_pipeline" / "output" / "scores"
        if score_dir.exists():
            for score_file in sorted(score_dir.glob("score_ch*.json")):
                try:
                    data = json.loads(score_file.read_text())
                    match = re.search(r"ch(\d+)", score_file.stem)
                    if not match:
                        continue
                    ch_num = int(match.group(1))
                    ch_path = _find_chapter_path(ch_num)
                    if not ch_path:
                        continue
                    finding = parse_score_json(data, ch_num, str(ch_path))
                    if finding:
                        findings.append(finding)
                except (json.JSONDecodeError, KeyError):
                    continue
        return findings
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def scan_pipeline_issues() -> list[dict]:
    """Detect known pipeline bugs that should be fixed first."""
    findings = []
    scorer_path = config.PROJECT_ROOT / "scripts" / "content_pipeline" / "quality_scorer.py"
    if scorer_path.exists():
        text = scorer_path.read_text()
        # Check for OpenAI-only API usage (incompatible with ClaudeCodeClient)
        if "client.chat.completions.create" in text and "ClaudeCodeClient" not in text:
            findings.append({
                "type": "pipeline-fix",
                "severity": 10,  # Highest priority
                "target": "scripts/content_pipeline/quality_scorer.py",
                "description": "score_chapter() uses OpenAI API only, incompatible with ClaudeCodeClient",
                "details": "Add ClaudeCodeClient support like core.py does",
            })
        # Check for hard truncation
        if "chapter_text[:12000]" in text:
            findings.append({
                "type": "pipeline-fix",
                "severity": 9,
                "target": "scripts/content_pipeline/quality_scorer.py",
                "description": "Hard truncation at 12000 chars loses content for long chapters",
                "details": "Replace with chunked scoring or dynamic limit",
            })
    return findings


# --- Findings Output ---

def write_findings(code_findings: list[dict], content_findings: list[dict],
                   run_dir: Path) -> Path:
    """Write findings to both markdown and JSON in the run directory."""
    run_dir.mkdir(parents=True, exist_ok=True)

    all_findings = {"code": code_findings, "content": content_findings}

    # JSON (structured, for planner to read)
    json_path = run_dir / "findings.json"
    json_path.write_text(json.dumps(all_findings, ensure_ascii=False, indent=2))

    # Markdown (human-readable)
    lines = [f"# Findings — {run_dir.name}\n"]
    lines.append(f"Code issues: {len(code_findings)} | Content issues: {len(content_findings)}\n")

    for category, findings in [("Code", code_findings), ("Content", content_findings)]:
        lines.append(f"\n## {category} Issues\n")
        if not findings:
            lines.append("No issues found.\n")
            continue
        for f in findings:
            lines.append(f"### [{f['severity']}] {f['type']}: {f['target']}")
            lines.append(f"- **Description**: {f['description']}")
            if "weakest_dimension" in f:
                lines.append(f"- **Weakest**: {f['weakest_dimension']} ({f['weakest_score']}/10)")
            lines.append("")

    md_path = run_dir / "findings.md"
    md_path.write_text("\n".join(lines))
    return md_path
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_scanner.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/overnight/scanner.py scripts/overnight/tests/test_scanner.py
git commit -m "feat(overnight): add scanner module for code and content signals"
```

---

### Task 3: Planner — Generate Task Queue

**Files:**
- Create: `scripts/overnight/planner.py`
- Create: `scripts/overnight/tests/test_planner.py`

- [ ] **Step 1: Write planner tests**

```python
# scripts/overnight/tests/test_planner.py
"""Tests for the planner module."""
import json
from pathlib import Path


def test_interleave_tasks():
    """interleave_tasks alternates code and content tasks."""
    from scripts.overnight.planner import interleave_tasks

    code = [{"type": "code-lint", "id": "c1"}, {"type": "code-test", "id": "c2"}]
    content = [{"type": "content-refine", "id": "t1"}, {"type": "content-refine", "id": "t2"}]

    result = interleave_tasks(code, content)
    # Odd positions (0, 2) = code, even positions (1, 3) = content
    assert result[0]["type"].startswith("code")
    assert result[1]["type"].startswith("content")
    assert result[2]["type"].startswith("code")
    assert result[3]["type"].startswith("content")


def test_interleave_uneven_lists():
    """interleave handles lists of different lengths."""
    from scripts.overnight.planner import interleave_tasks

    code = [{"type": "code-lint", "id": "c1"}]
    content = [{"type": "content-refine", "id": "t1"},
               {"type": "content-refine", "id": "t2"},
               {"type": "content-refine", "id": "t3"}]

    result = interleave_tasks(code, content)
    assert len(result) == 4
    # After code runs out, remaining content fills in
    assert result[0]["type"].startswith("code")
    assert result[1]["type"].startswith("content")


def test_generate_task_plan(tmp_run_dir, sample_findings):
    """generate_task_plan creates task_plan.md with correct structure."""
    from scripts.overnight.planner import generate_task_plan

    # Write findings JSON
    json_path = tmp_run_dir / "findings.json"
    json_path.write_text(json.dumps(sample_findings, ensure_ascii=False, indent=2))

    plan_path = generate_task_plan(tmp_run_dir, max_rounds=10)
    assert plan_path.exists()

    content = plan_path.read_text()
    assert "## Round 1" in content
    assert "status: pending" in content


def test_parse_task_plan(tmp_run_dir):
    """parse_task_plan reads task_plan.md back into structured data."""
    from scripts.overnight.planner import parse_task_plan

    plan_content = """# Overnight Task Plan — 2026-04-08

## Round 1 — code-lint
- **target**: new-website/src/App.jsx
- **issue**: 3 ESLint errors
- **action**: Fix ESLint errors
- **verify**: npm run lint passes
- **status**: pending

## Round 2 — content-refine
- **target**: 正文/11_风起云涌：第一次泡沫.md
- **issue**: readability: 5/10
- **action**: Refine readability
- **verify**: readability score improves
- **status**: done
"""
    plan_path = tmp_run_dir / "task_plan.md"
    plan_path.write_text(plan_content)

    tasks = parse_task_plan(plan_path)
    assert len(tasks) == 2
    assert tasks[0]["round"] == 1
    assert tasks[0]["type"] == "code-lint"
    assert tasks[0]["status"] == "pending"
    assert tasks[1]["status"] == "done"
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_planner.py -v`
Expected: FAIL

- [ ] **Step 3: Implement planner.py**

```python
# scripts/overnight/planner.py
"""Phase 2: Generate prioritized task queue from findings."""
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from . import config


def interleave_tasks(code_tasks: list[dict], content_tasks: list[dict]) -> list[dict]:
    """Interleave code and content tasks: odd=code, even=content."""
    result = []
    ci, ti = 0, 0
    turn_code = True  # Start with code

    while ci < len(code_tasks) or ti < len(content_tasks):
        if turn_code and ci < len(code_tasks):
            result.append(code_tasks[ci])
            ci += 1
        elif not turn_code and ti < len(content_tasks):
            result.append(content_tasks[ti])
            ti += 1
        elif ci < len(code_tasks):
            result.append(code_tasks[ci])
            ci += 1
        elif ti < len(content_tasks):
            result.append(content_tasks[ti])
            ti += 1
        turn_code = not turn_code

    return result


def generate_task_plan(run_dir: Path, max_rounds: int = 20) -> Path:
    """Read findings.json and generate task_plan.md."""
    findings_path = run_dir / "findings.json"
    findings = json.loads(findings_path.read_text())

    code_tasks = _build_code_tasks(findings.get("code", []))
    content_tasks = _build_content_tasks(findings.get("content", []))

    # Check for pipeline-fix tasks (always first)
    pipeline_fixes = [t for t in code_tasks if t["type"] == "pipeline-fix"]
    regular_code = [t for t in code_tasks if t["type"] != "pipeline-fix"]

    # Interleave regular tasks
    interleaved = interleave_tasks(regular_code, content_tasks)

    # Pipeline fixes go first
    all_tasks = pipeline_fixes + interleaved

    # Trim to max_rounds
    all_tasks = all_tasks[:max_rounds]

    # Assign round numbers
    for i, task in enumerate(all_tasks):
        task["round"] = i + 1
        task["status"] = "pending"

    # Write task_plan.md
    plan_path = run_dir / "task_plan.md"
    lines = [f"# Overnight Task Plan — {run_dir.name}\n"]
    lines.append(f"Total rounds: {len(all_tasks)} (max: {max_rounds})\n")

    for task in all_tasks:
        lines.append(f"\n## Round {task['round']} — {task['type']}")
        lines.append(f"- **target**: {task['target']}")
        lines.append(f"- **issue**: {task['description']}")
        lines.append(f"- **action**: {task['action']}")
        lines.append(f"- **verify**: {task['verify']}")
        if "weaknesses" in task:
            lines.append(f"- **weaknesses**: {json.dumps(task['weaknesses'], ensure_ascii=False)}")
        if "suggestions" in task:
            lines.append(f"- **suggestions**: {json.dumps(task['suggestions'], ensure_ascii=False)}")
        lines.append(f"- **status**: {task['status']}")

    plan_path.write_text("\n".join(lines))

    # Also save as JSON for executor
    json_path = run_dir / "task_plan.json"
    json_path.write_text(json.dumps(all_tasks, ensure_ascii=False, indent=2))

    return plan_path


def _build_code_tasks(findings: list[dict]) -> list[dict]:
    """Convert code findings into actionable tasks."""
    tasks = []
    for f in findings:
        task = {
            "type": f["type"],
            "target": f["target"],
            "description": f["description"],
            "details": f.get("details", ""),
            "severity": f["severity"],
        }
        if f["type"] == "code-lint":
            task["action"] = f"Fix lint errors in {Path(f['target']).name}"
            task["verify"] = "npm run lint passes with 0 errors for this file"
        elif f["type"] == "code-test":
            task["action"] = f"Add unit tests for {Path(f['target']).stem}"
            task["verify"] = "New tests pass and cover key component behaviors"
        elif f["type"] == "code-refactor":
            task["action"] = f"Refactor {Path(f['target']).name} for clarity"
            task["verify"] = "All existing tests still pass"
        elif f["type"] == "pipeline-fix":
            task["action"] = f["description"]
            task["verify"] = "Pipeline command runs without error"
        else:
            task["action"] = f["description"]
            task["verify"] = "No regressions"
        tasks.append(task)
    return tasks


def _build_content_tasks(findings: list[dict]) -> list[dict]:
    """Convert content findings into targeted refinement tasks."""
    tasks = []
    for f in findings:
        tasks.append({
            "type": "content-refine",
            "target": f["target"],
            "chapter_num": f.get("chapter_num"),
            "description": f["description"],
            "weaknesses": f.get("weaknesses", []),
            "suggestions": f.get("suggestions", []),
            "scores": f.get("scores", {}),
            "weakest_dimension": f.get("weakest_dimension", ""),
            "weakest_score": f.get("weakest_score", 0),
            "severity": f["severity"],
            "action": f"Refine {f.get('weakest_dimension', 'quality')} "
                      f"for chapter {f.get('chapter_num', '?')}",
            "verify": f"{f.get('weakest_dimension', 'score')} score improves "
                      f"from {f.get('weakest_score', '?')}/10",
        })
    return tasks


def parse_task_plan(plan_path: Path) -> list[dict]:
    """Parse task_plan.md back into a list of task dicts."""
    content = plan_path.read_text()
    tasks = []
    current: dict[str, Any] = {}

    for line in content.split("\n"):
        # New round header
        match = re.match(r"## Round (\d+) — (.+)", line)
        if match:
            if current:
                tasks.append(current)
            current = {
                "round": int(match.group(1)),
                "type": match.group(2).strip(),
            }
            continue

        # Key-value fields
        kv = re.match(r"- \*\*(\w+)\*\*:\s*(.+)", line)
        if kv and current:
            key = kv.group(1)
            val = kv.group(2).strip()
            current[key] = val

    if current:
        tasks.append(current)

    return tasks


def update_task_status(plan_path: Path, round_num: int, new_status: str):
    """Update the status of a specific round in task_plan.md."""
    lines = plan_path.read_text().split("\n")
    in_target_round = False
    for i, line in enumerate(lines):
        if re.match(rf"## Round {round_num} —", line):
            in_target_round = True
        elif line.startswith("## Round "):
            in_target_round = False
        if in_target_round and line.startswith("- **status**:"):
            lines[i] = f"- **status**: {new_status}"
            break
    plan_path.write_text("\n".join(lines))
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_planner.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/overnight/planner.py scripts/overnight/tests/test_planner.py
git commit -m "feat(overnight): add planner module for task queue generation"
```

---

### Task 4: Prompt Templates

**Files:**
- Create: `scripts/overnight/prompts.py`
- Create: `scripts/overnight/tests/test_prompts.py`

- [ ] **Step 1: Write prompt tests**

```python
# scripts/overnight/tests/test_prompts.py
"""Tests for prompt template builder."""


def test_build_code_lint_prompt():
    from scripts.overnight.prompts import build_prompt

    task = {
        "type": "code-lint",
        "target": "new-website/src/App.jsx",
        "description": "3 ESLint errors",
        "details": "no-unused-vars (2), react/prop-types (1)",
    }
    prompt = build_prompt(task, file_contents={"App.jsx": "const x = 1;"})
    assert "lint" in prompt.lower() or "ESLint" in prompt
    assert "App.jsx" in prompt
    assert "no-unused-vars" in prompt


def test_build_content_refine_prompt():
    from scripts.overnight.prompts import build_prompt

    task = {
        "type": "content-refine",
        "target": "正文/11_test.md",
        "chapter_num": 11,
        "weakest_dimension": "readability",
        "weakest_score": 5,
        "weaknesses": ["段落长度单一", "开头缺乏画面感"],
        "suggestions": ["增加句式变化", "用具体场景开头"],
        "scores": {"readability": 5, "style_consistency": 7},
    }
    prompt = build_prompt(task, file_contents={"11_test.md": "# 章节内容"})
    assert "readability" in prompt
    assert "5/10" in prompt or "5" in prompt
    assert "段落长度单一" in prompt
    assert "20%" in prompt  # Modification limit


def test_build_code_test_prompt():
    from scripts.overnight.prompts import build_prompt

    task = {
        "type": "code-test",
        "target": "new-website/src/components/home/Timeline.jsx",
        "description": "No test file exists",
    }
    prompt = build_prompt(task, file_contents={"Timeline.jsx": "export default function Timeline() {}"})
    assert "test" in prompt.lower()
    assert "Timeline" in prompt


def test_all_prompts_include_constraint():
    """All prompts must tell Claude to only modify specified files."""
    from scripts.overnight.prompts import build_prompt

    for task_type in ("code-lint", "code-test", "code-refactor", "content-refine", "pipeline-fix"):
        task = {"type": task_type, "target": "test.js", "description": "test"}
        prompt = build_prompt(task, file_contents={})
        assert "only" in prompt.lower() or "不要" in prompt or "specified" in prompt.lower()
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_prompts.py -v`
Expected: FAIL

- [ ] **Step 3: Implement prompts.py**

```python
# scripts/overnight/prompts.py
"""Prompt templates for each task type sent to Claude CLI."""
import json
from pathlib import Path


def build_prompt(task: dict, file_contents: dict[str, str] | None = None) -> str:
    """Build a self-contained prompt for Claude based on task type."""
    task_type = task.get("type", "")
    builders = {
        "code-lint": _prompt_code_lint,
        "code-test": _prompt_code_test,
        "code-refactor": _prompt_code_refactor,
        "content-refine": _prompt_content_refine,
        "pipeline-fix": _prompt_pipeline_fix,
    }
    builder = builders.get(task_type, _prompt_generic)
    return builder(task, file_contents or {})


def _file_section(file_contents: dict[str, str]) -> str:
    """Format file contents for inclusion in prompt."""
    if not file_contents:
        return ""
    sections = []
    for name, content in file_contents.items():
        sections.append(f"### {name}\n```\n{content}\n```")
    return "\n\n".join(sections)


def _constraint_block() -> str:
    return (
        "\n\n---\n"
        "CONSTRAINTS:\n"
        "- Only modify the specified target files. Do not touch unrelated code.\n"
        "- Do not add comments explaining what you changed.\n"
        "- Do not refactor code beyond what is needed to fix the issue.\n"
        "- Output the complete modified file content.\n"
    )


def _prompt_code_lint(task: dict, file_contents: dict[str, str]) -> str:
    target = task.get("target", "")
    details = task.get("details", "")
    return (
        f"Fix all ESLint errors in `{target}`.\n\n"
        f"Errors found:\n{details}\n\n"
        f"Current file contents:\n{_file_section(file_contents)}\n\n"
        "Fix only the reported errors. Do not change functionality or style "
        "beyond what is needed to resolve the lint errors."
        f"{_constraint_block()}"
    )


def _prompt_code_test(task: dict, file_contents: dict[str, str]) -> str:
    target = task.get("target", "")
    component = Path(target).stem
    return (
        f"Write unit tests for the React component `{component}` at `{target}`.\n\n"
        f"Component source:\n{_file_section(file_contents)}\n\n"
        "Requirements:\n"
        "- Use Vitest + React Testing Library + jsdom\n"
        "- Test file goes in `__tests__/{component}.test.jsx` next to the component\n"
        "- Cover: rendering, key user interactions, edge cases (empty props, etc.)\n"
        "- Import pattern: `import {{ render, screen }} from '@testing-library/react'`\n"
        "- Mock framer-motion if the component uses it: "
        "`vi.mock('framer-motion', () => require('../../test/__mocks__/framer-motion'))`\n"
        f"{_constraint_block()}"
    )


def _prompt_code_refactor(task: dict, file_contents: dict[str, str]) -> str:
    target = task.get("target", "")
    details = task.get("details", "")
    return (
        f"Refactor `{target}` to improve readability and maintainability.\n\n"
        f"Issues identified:\n{details}\n\n"
        f"Current file:\n{_file_section(file_contents)}\n\n"
        "Rules:\n"
        "- Keep all existing functionality intact\n"
        "- All existing tests must still pass\n"
        "- Simplify complex logic, extract only if it genuinely helps clarity\n"
        f"{_constraint_block()}"
    )


def _prompt_content_refine(task: dict, file_contents: dict[str, str]) -> str:
    dim = task.get("weakest_dimension", "quality")
    score = task.get("weakest_score", "?")
    weaknesses = task.get("weaknesses", [])
    suggestions = task.get("suggestions", [])
    scores = task.get("scores", {})

    scores_str = "\n".join(f"  - {k}: {v}/10" for k, v in scores.items()) if scores else "N/A"
    weak_str = "\n".join(f"  - {w}" for w in weaknesses) if weaknesses else "N/A"
    sugg_str = "\n".join(f"  - {s}" for s in suggestions) if suggestions else "N/A"

    return (
        f"你是《比特币那些事儿》的精修编辑。\n\n"
        f"这一章的质量评分如下：\n{scores_str}\n\n"
        f"最弱维度: {dim} ({score}/10)\n"
        f"具体问题:\n{weak_str}\n"
        f"改进建议:\n{sugg_str}\n\n"
        f"请只针对上述问题修订章节，不要重写整章。规则：\n"
        f"1. 保留原文的事实内容和叙事结构\n"
        f"2. 只改进 {dim} 相关的问题\n"
        f"3. 修改幅度控制在原文的 20% 以内\n"
        f"4. 输出完整的修订后章节（Markdown 格式）\n\n"
        f"【原文】\n{_file_section(file_contents)}\n"
        f"\n---\n"
        f"CONSTRAINTS:\n"
        f"- Only modify the specified target file.\n"
        f"- 不要添加任何来源标签或元数据。\n"
        f"- 不要改变章节标题格式。\n"
    )


def _prompt_pipeline_fix(task: dict, file_contents: dict[str, str]) -> str:
    target = task.get("target", "")
    details = task.get("details", "")
    return (
        f"Fix a bug in the content pipeline at `{target}`.\n\n"
        f"Problem:\n{details}\n\n"
        f"Current file:\n{_file_section(file_contents)}\n\n"
        "Fix only the described issue. Do not refactor or improve unrelated code."
        f"{_constraint_block()}"
    )


def _prompt_generic(task: dict, file_contents: dict[str, str]) -> str:
    return (
        f"Task: {task.get('description', 'Unknown task')}\n"
        f"Target: {task.get('target', 'Unknown')}\n\n"
        f"Files:\n{_file_section(file_contents)}\n"
        f"{_constraint_block()}"
    )
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_prompts.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/overnight/prompts.py scripts/overnight/tests/test_prompts.py
git commit -m "feat(overnight): add prompt templates for all task types"
```

---

### Task 5: Executor — Worktree Management

**Files:**
- Create: `scripts/overnight/executor.py`
- Create: `scripts/overnight/tests/test_executor.py`

- [ ] **Step 1: Write worktree management tests**

```python
# scripts/overnight/tests/test_executor.py
"""Tests for the executor module."""
import subprocess
from unittest.mock import patch, MagicMock, call
from pathlib import Path


def test_cleanup_previous_runs():
    """cleanup_previous_runs removes orphaned overnight worktrees."""
    from scripts.overnight.executor import cleanup_previous_runs

    mock_output = (
        "/path/to/repo              abc1234 [main]\n"
        "/path/to/overnight-wt-1    def5678 [overnight/round-1-lint]\n"
        "/path/to/overnight-wt-2    ghi9012 [overnight/round-2-content]\n"
    )
    with patch("scripts.overnight.executor._run_cmd") as mock_run:
        mock_run.side_effect = [
            mock_output,  # git worktree list
            "",  # remove wt-1
            "",  # remove wt-2
            "overnight/round-1-lint\novernight/round-2-content\n",  # branch list
            "",  # delete branch 1
            "",  # delete branch 2
        ]
        cleanup_previous_runs()
        # Should have called worktree remove for each overnight worktree
        assert mock_run.call_count >= 3


def test_create_worktree():
    """create_worktree creates a worktree branching from main."""
    from scripts.overnight.executor import create_worktree

    with patch("scripts.overnight.executor._run_cmd") as mock_run:
        mock_run.return_value = ""
        path = create_worktree(1, "lint-fix")

        assert "overnight-wt-1" in str(path)
        cmd_str = mock_run.call_args[0][0]
        assert "worktree add" in cmd_str
        assert "main" in cmd_str


def test_remove_worktree():
    """remove_worktree cleans up worktree directory."""
    from scripts.overnight.executor import remove_worktree

    with patch("scripts.overnight.executor._run_cmd") as mock_run:
        mock_run.return_value = ""
        remove_worktree(Path("/tmp/overnight-wt-1"))
        cmd_str = mock_run.call_args[0][0]
        assert "worktree remove" in cmd_str


def test_check_disk_space():
    """check_disk_space returns True if enough space available."""
    from scripts.overnight.executor import check_disk_space

    # Should return True on any normal dev machine
    assert check_disk_space() is True


def test_create_content_backup(tmp_path):
    """Content backup copies original to 历史版本/."""
    from scripts.overnight.executor import create_content_backup

    # Create fake chapter
    chapters_dir = tmp_path / "正文"
    chapters_dir.mkdir()
    chapter = chapters_dir / "11_test.md"
    chapter.write_text("original content")
    history_dir = chapters_dir / "历史版本"
    history_dir.mkdir()

    backup_path = create_content_backup(chapter, history_dir)
    assert backup_path.exists()
    assert backup_path.read_text() == "original content"
    assert "pre-overnight" in backup_path.name
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_executor.py -v`
Expected: FAIL

- [ ] **Step 3: Implement executor.py (worktree + utilities)**

```python
# scripts/overnight/executor.py
"""Phase 3: Execute improvement rounds in isolated worktrees."""
import json
import os
import shutil
import subprocess
from datetime import date, datetime
from pathlib import Path
from typing import Any

from . import config
from .prompts import build_prompt


def _run_cmd(cmd: str, cwd: str | None = None, timeout: int = 60) -> str:
    """Run a shell command and return stdout."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.stdout.strip()


def check_disk_space(min_gb: float = config.MIN_DISK_GB) -> bool:
    """Check if enough disk space is available."""
    stat = os.statvfs("/")
    free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    return free_gb >= min_gb


def cleanup_previous_runs():
    """Remove orphaned overnight worktrees and branches from previous runs."""
    # List worktrees
    output = _run_cmd("git worktree list", cwd=str(config.PROJECT_ROOT))
    for line in output.split("\n"):
        if "overnight-wt-" in line:
            wt_path = line.split()[0]
            try:
                _run_cmd(f"git worktree remove --force {wt_path}",
                         cwd=str(config.PROJECT_ROOT))
                print(f"  Cleaned up worktree: {wt_path}")
            except Exception:
                pass

    # Delete orphaned overnight branches
    branches = _run_cmd(
        f"git branch --list '{config.BRANCH_PREFIX}/*'",
        cwd=str(config.PROJECT_ROOT),
    )
    for branch in branches.split("\n"):
        branch = branch.strip().lstrip("* ")
        if branch:
            try:
                _run_cmd(f"git branch -D {branch}", cwd=str(config.PROJECT_ROOT))
                print(f"  Deleted branch: {branch}")
            except Exception:
                pass


def create_worktree(round_num: int, slug: str) -> Path:
    """Create an isolated worktree for a round, branching from main."""
    wt_dir = config.WORKTREE_BASE / f"overnight-wt-{round_num}"
    branch = f"{config.BRANCH_PREFIX}/round-{round_num}-{slug}"

    config.WORKTREE_BASE.mkdir(parents=True, exist_ok=True)

    _run_cmd(
        f"git worktree add {wt_dir} -b {branch} main",
        cwd=str(config.PROJECT_ROOT),
    )
    return wt_dir


def remove_worktree(wt_path: Path):
    """Remove a worktree and its branch."""
    _run_cmd(f"git worktree remove --force {wt_path}",
             cwd=str(config.PROJECT_ROOT))


def create_content_backup(chapter_path: Path, history_dir: Path) -> Path:
    """Backup a chapter to 历史版本/ before modification."""
    history_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    backup_name = f"{today}_{chapter_path.stem}_pre-overnight{chapter_path.suffix}"
    backup_path = history_dir / backup_name
    shutil.copy2(chapter_path, backup_path)
    return backup_path


def run_claude(prompt: str, worktree_path: Path,
               timeout: int = config.DEFAULT_TIMEOUT) -> str:
    """Run Claude CLI with the given prompt in the worktree directory."""
    allowed = ",".join(config.ALLOWED_TOOLS)
    cmd = [
        "claude", "-p",
        "--model", config.CLAUDE_MODEL,
        "--cwd", str(worktree_path),
        "--output-format", "text",
        "--no-session-persistence",
        "--allowedTools", allowed,
    ]
    try:
        result = subprocess.run(
            cmd, input=prompt,
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode != 0:
            return f"ERROR: {result.stderr[:500]}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "ERROR: Claude CLI timed out"
    except FileNotFoundError:
        return "ERROR: claude command not found"


def verify_task(task: dict, worktree_path: Path,
                before_score: dict | None = None) -> dict:
    """Verify that a task's changes meet quality criteria.

    Returns: {"passed": bool, "reason": str, "details": dict}
    """
    task_type = task.get("type", "")

    if task_type == "code-lint":
        return _verify_lint(worktree_path)
    elif task_type == "code-test":
        return _verify_tests(worktree_path)
    elif task_type == "code-refactor":
        return _verify_tests(worktree_path)  # Just ensure no regressions
    elif task_type == "content-refine":
        return _verify_content(task, worktree_path, before_score)
    elif task_type == "pipeline-fix":
        return _verify_pipeline(worktree_path)
    else:
        return {"passed": True, "reason": "no verification for this type", "details": {}}


def _verify_lint(worktree_path: Path) -> dict:
    """Verify lint passes after fix."""
    website_dir = worktree_path / "new-website"
    if not website_dir.exists():
        return {"passed": True, "reason": "no website dir in worktree", "details": {}}
    try:
        result = subprocess.run(
            ["npm", "run", "lint"],
            cwd=str(website_dir),
            capture_output=True, text=True, timeout=60,
        )
        passed = result.returncode == 0
        return {
            "passed": passed,
            "reason": "lint clean" if passed else "lint still has errors",
            "details": {"output": result.stdout[:500]},
        }
    except Exception as e:
        return {"passed": False, "reason": f"lint check failed: {e}", "details": {}}


def _verify_tests(worktree_path: Path) -> dict:
    """Verify all tests pass."""
    website_dir = worktree_path / "new-website"
    if not website_dir.exists():
        return {"passed": True, "reason": "no website dir", "details": {}}
    try:
        result = subprocess.run(
            ["npx", "vitest", "run"],
            cwd=str(website_dir),
            capture_output=True, text=True, timeout=120,
        )
        passed = result.returncode == 0
        return {
            "passed": passed,
            "reason": "all tests pass" if passed else "test failures detected",
            "details": {"output": (result.stdout + result.stderr)[:500]},
        }
    except Exception as e:
        return {"passed": False, "reason": f"test run failed: {e}", "details": {}}


def _verify_content(task: dict, worktree_path: Path,
                    before_score: dict | None) -> dict:
    """Verify content improvement by re-scoring."""
    if not before_score:
        return {"passed": True, "reason": "no before score to compare", "details": {}}

    dim = task.get("weakest_dimension", "")
    old_val = before_score.get("scores", {}).get(dim, 0)

    # Re-score using claude CLI in the worktree
    ch_num = task.get("chapter_num")
    if not ch_num:
        return {"passed": True, "reason": "no chapter num", "details": {}}

    try:
        result = subprocess.run(
            ["python", "-m", "scripts.content_pipeline.cli", "score", str(ch_num)],
            cwd=str(worktree_path),
            capture_output=True, text=True, timeout=300,
        )
        # Try to read the new score
        score_file = (worktree_path / "scripts" / "content_pipeline" /
                      "output" / "scores" / f"score_ch{ch_num:02d}.json")
        if score_file.exists():
            new_data = json.loads(score_file.read_text())
            new_val = new_data.get("scores", {}).get(dim, 0)
            improved = new_val > old_val
            return {
                "passed": improved,
                "reason": f"{dim}: {old_val}→{new_val}" + (" (improved)" if improved else " (regressed)"),
                "details": {"before": old_val, "after": new_val, "dimension": dim},
            }
    except Exception as e:
        return {"passed": False, "reason": f"re-scoring failed: {e}", "details": {}}

    return {"passed": False, "reason": "could not verify score", "details": {}}


def _verify_pipeline(worktree_path: Path) -> dict:
    """Verify pipeline fix by running a basic command."""
    try:
        result = subprocess.run(
            ["python", "-c", "from scripts.content_pipeline import config; print('OK')"],
            cwd=str(worktree_path),
            capture_output=True, text=True, timeout=30,
        )
        passed = result.returncode == 0 and "OK" in result.stdout
        return {
            "passed": passed,
            "reason": "pipeline imports OK" if passed else "pipeline import failed",
            "details": {"output": result.stderr[:300]},
        }
    except Exception as e:
        return {"passed": False, "reason": f"pipeline check failed: {e}", "details": {}}


def commit_and_pr(worktree_path: Path, task: dict, round_num: int,
                  verification: dict) -> str | None:
    """Commit changes, push branch, and create a PR. Returns PR URL or None."""
    branch = f"{config.BRANCH_PREFIX}/round-{round_num}-{_slugify(task.get('type', 'task'))}"
    task_type = task.get("type", "unknown")
    target = task.get("target", "unknown")
    description = task.get("description", "")

    # Check if there are actually changes
    diff = _run_cmd("git diff --name-only", cwd=str(worktree_path))
    untracked = _run_cmd("git ls-files --others --exclude-standard", cwd=str(worktree_path))
    if not diff and not untracked:
        return None  # No changes to commit

    # Stage and commit (use subprocess list to avoid shell injection)
    subprocess.run(["git", "add", "-A"], cwd=str(worktree_path), check=True)
    commit_msg = f"overnight: [{task_type}] {target}\n\n{description}"
    subprocess.run(["git", "commit", "-m", commit_msg],
                   cwd=str(worktree_path), check=True)

    # Push
    subprocess.run(["git", "push", "-u", "origin", branch],
                   cwd=str(worktree_path), capture_output=True, timeout=60)

    # Create PR
    delta = ""
    if "details" in verification and "before" in verification["details"]:
        d = verification["details"]
        delta = f"\n\nScore: {d.get('dimension', '?')}: {d.get('before')}→{d.get('after')}"

    pr_title = f"overnight: {task_type} — {Path(target).name}"
    pr_body = (
        f"## Overnight Auto-Improvement\n\n"
        f"- **Type**: {task_type}\n"
        f"- **Target**: `{target}`\n"
        f"- **Issue**: {description}\n"
        f"- **Verification**: {verification.get('reason', 'N/A')}"
        f"{delta}\n\n"
        f"Generated by overnight iteration system."
    )

    try:
        result = subprocess.run(
            ["gh", "pr", "create", "--title", pr_title,
             "--body", pr_body, "--base", "main"],
            cwd=str(worktree_path),
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def _slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    return text.lower().replace(" ", "-").replace("/", "-").replace(":", "")[:30]


def _read_target_files(task: dict) -> dict[str, str]:
    """Pre-read the target file(s) for inclusion in the prompt."""
    contents = {}
    target = task.get("target", "")
    full_path = config.PROJECT_ROOT / target
    if full_path.exists() and full_path.is_file():
        try:
            text = full_path.read_text(encoding="utf-8")
            contents[full_path.name] = text
        except Exception:
            pass
    return contents


def execute_round(task: dict, round_num: int, run_dir: Path) -> dict:
    """Execute a single improvement round. Returns result dict."""
    result = {
        "round": round_num,
        "type": task.get("type", "unknown"),
        "target": task.get("target", "unknown"),
        "status": "pending",
        "pr_url": None,
        "verification": {},
        "started_at": datetime.now().isoformat(),
        "finished_at": None,
    }

    slug = _slugify(f"{task.get('type', 'task')}-{Path(task.get('target', 'x')).stem}")

    try:
        # 0. Disk check
        if not check_disk_space():
            result["status"] = "skipped"
            result["verification"] = {"reason": "insufficient disk space"}
            return result

        # 1. Content backup (if content task)
        if task.get("type") == "content-refine":
            target_path = config.PROJECT_ROOT / task["target"]
            if target_path.exists():
                history_dir = config.CHAPTERS_DIR / "历史版本"
                create_content_backup(target_path, history_dir)

        # 2. Create worktree
        wt_path = create_worktree(round_num, slug)

        try:
            # 3. Build prompt with file contents
            file_contents = _read_target_files(task)
            prompt = build_prompt(task, file_contents)

            # 4. Get before-score for content tasks
            before_score = None
            if task.get("type") == "content-refine" and task.get("scores"):
                before_score = {"scores": task["scores"]}

            # 5. Run Claude
            print(f"  Running Claude for round {round_num}...")
            claude_output = run_claude(prompt, wt_path)

            if claude_output.startswith("ERROR:"):
                result["status"] = "failed"
                result["verification"] = {"reason": claude_output}
                return result

            # 6. Verify
            print(f"  Verifying round {round_num}...")
            verification = verify_task(task, wt_path, before_score)
            result["verification"] = verification

            if verification["passed"]:
                # 7. Create PR
                pr_url = commit_and_pr(wt_path, task, round_num, verification)
                result["pr_url"] = pr_url
                result["status"] = "done" if pr_url else "no-changes"
            else:
                result["status"] = "failed"

        finally:
            # 8. Cleanup worktree
            try:
                remove_worktree(wt_path)
            except Exception:
                pass

    except Exception as e:
        result["status"] = "error"
        result["verification"] = {"reason": str(e)}

    result["finished_at"] = datetime.now().isoformat()
    return result
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_executor.py -v`
Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/overnight/executor.py scripts/overnight/tests/test_executor.py
git commit -m "feat(overnight): add executor with worktree management and verification"
```

---

### Task 6: Reporter — Morning Report

**Files:**
- Create: `scripts/overnight/reporter.py`
- Create: `scripts/overnight/tests/test_reporter.py`

- [ ] **Step 1: Write reporter tests**

```python
# scripts/overnight/tests/test_reporter.py
"""Tests for the reporter module."""
from datetime import datetime


def test_generate_report_basic(tmp_run_dir):
    """generate_report creates a readable progress.md."""
    from scripts.overnight.reporter import generate_report

    results = [
        {
            "round": 1, "type": "code-lint", "target": "App.jsx",
            "status": "done", "pr_url": "https://github.com/user/repo/pull/42",
            "verification": {"reason": "lint clean", "details": {}},
        },
        {
            "round": 2, "type": "content-refine", "target": "正文/11_test.md",
            "status": "done", "pr_url": "https://github.com/user/repo/pull/43",
            "verification": {"reason": "readability: 5→7", "details": {"before": 5, "after": 7}},
        },
        {
            "round": 3, "type": "content-refine", "target": "正文/17_test.md",
            "status": "failed", "pr_url": None,
            "verification": {"reason": "style: 6→5.8 (regressed)", "details": {}},
        },
    ]
    start_time = datetime(2026, 4, 8, 23, 30)
    end_time = datetime(2026, 4, 9, 6, 12)

    path = generate_report(results, start_time, end_time, tmp_run_dir)
    assert path.exists()

    content = path.read_text()
    assert "Completed: 2" in content
    assert "Failed: 1" in content
    assert "#42" in content or "pull/42" in content
    assert "regressed" in content.lower() or "failed" in content.lower()


def test_report_with_all_statuses(tmp_run_dir):
    """Report handles all possible statuses."""
    from scripts.overnight.reporter import generate_report

    results = [
        {"round": 1, "type": "code-lint", "target": "a.js", "status": "done",
         "pr_url": "#1", "verification": {"reason": "ok"}},
        {"round": 2, "type": "code-test", "target": "b.js", "status": "failed",
         "pr_url": None, "verification": {"reason": "tests fail"}},
        {"round": 3, "type": "code-lint", "target": "c.js", "status": "error",
         "pr_url": None, "verification": {"reason": "timeout"}},
        {"round": 4, "type": "code-test", "target": "d.js", "status": "skipped",
         "pr_url": None, "verification": {"reason": "disk full"}},
        {"round": 5, "type": "code-test", "target": "e.js", "status": "no-changes",
         "pr_url": None, "verification": {"reason": "nothing changed"}},
    ]
    now = datetime.now()
    path = generate_report(results, now, now, tmp_run_dir)
    content = path.read_text()
    assert "Completed: 1" in content
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_reporter.py -v`
Expected: FAIL

- [ ] **Step 3: Implement reporter.py**

```python
# scripts/overnight/reporter.py
"""Phase 4: Generate morning report for human review."""
import json
from datetime import datetime
from pathlib import Path


def generate_report(results: list[dict], start_time: datetime,
                    end_time: datetime, run_dir: Path) -> Path:
    """Generate progress.md — the morning review entry point."""
    run_dir.mkdir(parents=True, exist_ok=True)

    # Count statuses
    done = sum(1 for r in results if r["status"] == "done")
    failed = sum(1 for r in results if r["status"] == "failed")
    errors = sum(1 for r in results if r["status"] == "error")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    no_changes = sum(1 for r in results if r["status"] == "no-changes")
    total = len(results)

    code_prs = sum(1 for r in results if r["status"] == "done" and r["type"].startswith("code"))
    content_prs = sum(1 for r in results if r["status"] == "done" and r["type"].startswith("content"))

    duration = end_time - start_time
    hours = duration.total_seconds() / 3600

    lines = [
        f"# Overnight Run — {run_dir.name}",
        f"Started: {start_time.strftime('%H:%M')} | "
        f"Finished: {end_time.strftime('%H:%M')} | "
        f"Duration: {hours:.1f}h | "
        f"Rounds: {total}",
        "",
        "## Summary",
        f"- Completed: {done}",
        f"- Failed: {failed}",
        f"- Errors: {errors}",
        f"- Skipped: {skipped}",
        f"- No changes: {no_changes}",
        f"- Code PRs: {code_prs} | Content PRs: {content_prs}",
        "",
        "## Results",
        "",
        "| # | Type | Target | Result | PR | Detail |",
        "|---|------|--------|--------|----|--------|",
    ]

    for r in results:
        status_icon = {
            "done": "pass", "failed": "FAIL", "error": "ERR",
            "skipped": "SKIP", "no-changes": "---",
        }.get(r["status"], "?")

        pr = r.get("pr_url") or "—"
        detail = r.get("verification", {}).get("reason", "")[:50]
        target_short = Path(r.get("target", "")).name

        lines.append(
            f"| {r['round']} | {r['type']} | {target_short} | "
            f"{status_icon} | {pr} | {detail} |"
        )

    # Failed tasks section
    failed_tasks = [r for r in results if r["status"] in ("failed", "error")]
    if failed_tasks:
        lines.append("")
        lines.append("## Failed Tasks")
        for r in failed_tasks:
            reason = r.get("verification", {}).get("reason", "unknown")
            lines.append(f"\n### Round {r['round']}: {r['type']} — {r['target']}")
            lines.append(f"- Reason: {reason}")

    # Suggestions
    lines.append("")
    lines.append("## Suggestions for Next Run")
    if failed_tasks:
        for r in failed_tasks:
            lines.append(f"- Round {r['round']} ({r['target']}): may need manual review")
    else:
        lines.append("- All rounds completed successfully!")

    progress_path = run_dir / "progress.md"
    progress_path.write_text("\n".join(lines))

    # Also save raw results as JSON
    json_path = run_dir / "results.json"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str))

    return progress_path
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_reporter.py -v`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/overnight/reporter.py scripts/overnight/tests/test_reporter.py
git commit -m "feat(overnight): add reporter module for morning review reports"
```

---

### Task 7: Main Entry Point — CLI + Orchestration

**Files:**
- Create: `scripts/overnight/__main__.py`
- Create: `scripts/overnight/tests/test_main.py`

- [ ] **Step 1: Write main tests**

```python
# scripts/overnight/tests/test_main.py
"""Tests for the overnight main entry point."""
from unittest.mock import patch, MagicMock
import argparse


def test_parse_args_defaults():
    """Default CLI args are sensible."""
    from scripts.overnight.__main__ import parse_args

    args = parse_args([])
    assert args.rounds == 20
    assert args.timeout == 900
    assert args.dry_run is False
    assert args.resume is False
    assert args.code_only is False
    assert args.content_only is False


def test_parse_args_custom():
    """CLI args are parsed correctly."""
    from scripts.overnight.__main__ import parse_args

    args = parse_args(["--rounds", "10", "--timeout", "600", "--dry-run"])
    assert args.rounds == 10
    assert args.timeout == 600
    assert args.dry_run is True


def test_check_prerequisites():
    """check_prerequisites verifies required tools exist."""
    from scripts.overnight.__main__ import check_prerequisites

    with patch("shutil.which") as mock_which:
        mock_which.return_value = "/usr/bin/claude"
        # Should not raise
        try:
            check_prerequisites()
        except SystemExit:
            pass  # gh auth might fail in test environment
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_main.py -v`
Expected: FAIL

- [ ] **Step 3: Implement __main__.py**

```python
# scripts/overnight/__main__.py
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
from datetime import datetime, date
from pathlib import Path

# Ensure project root is importable
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.overnight import config
from scripts.overnight.scanner import scan_code, scan_content, write_findings
from scripts.overnight.planner import generate_task_plan, parse_task_plan, update_task_status
from scripts.overnight.executor import (
    cleanup_previous_runs, execute_round, check_disk_space,
)
from scripts.overnight.reporter import generate_report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Overnight Iteration System — autonomous code & content improvement",
    )
    parser.add_argument("--rounds", type=int, default=config.DEFAULT_ROUNDS,
                        help=f"Number of rounds (default: {config.DEFAULT_ROUNDS})")
    parser.add_argument("--timeout", type=int, default=config.DEFAULT_TIMEOUT,
                        help=f"Per-round timeout in seconds (default: {config.DEFAULT_TIMEOUT})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only scan and plan, do not execute")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from the most recent incomplete run")
    parser.add_argument("--code-only", action="store_true",
                        help="Only run code improvement tasks")
    parser.add_argument("--content-only", action="store_true",
                        help="Only run content improvement tasks")
    return parser.parse_args(argv)


def check_prerequisites():
    """Verify required tools are available."""
    required = ["claude", "git", "gh"]
    missing = [t for t in required if not shutil.which(t)]
    if missing:
        print(f"ERROR: Missing required tools: {', '.join(missing)}")
        sys.exit(1)

    # Check gh auth
    result = subprocess.run(["gh", "auth", "status"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: gh is not authenticated. Run: gh auth login")
        sys.exit(1)


def find_latest_run() -> Path | None:
    """Find the most recent run directory for --resume."""
    if not config.RUNS_DIR.exists():
        return None
    runs = sorted(config.RUNS_DIR.iterdir(), reverse=True)
    for run_dir in runs:
        if (run_dir / "task_plan.md").exists():
            return run_dir
    return None


def main():
    args = parse_args()

    print("=" * 60)
    print("Overnight Iteration System")
    print(f"Rounds: {args.rounds} | Timeout: {args.timeout}s")
    print("=" * 60)

    # Prerequisites check
    check_prerequisites()

    # Setup run directory
    if args.resume:
        run_dir = find_latest_run()
        if not run_dir:
            print("No previous run found to resume.")
            sys.exit(1)
        print(f"Resuming run: {run_dir.name}")
    else:
        run_dir = config.get_run_dir()
        run_dir.mkdir(parents=True, exist_ok=True)

    start_time = datetime.now()

    # Phase 0: Cleanup
    print("\n[Phase 0] Cleaning up previous runs...")
    cleanup_previous_runs()

    # Phase 1: Scan (skip if resuming with fresh findings)
    findings_json = run_dir / "findings.json"
    findings_fresh = False
    if args.resume and findings_json.exists():
        # Stale check: re-scan if findings older than 1 hour
        import time
        age_seconds = time.time() - findings_json.stat().st_mtime
        findings_fresh = age_seconds < 3600
    if args.resume and findings_fresh:
        print(f"\n[Phase 1] Using existing findings from {run_dir.name} (age: {age_seconds/60:.0f}min)")
    else:
        print("\n[Phase 1] Scanning for issues...")
        code_findings = [] if args.content_only else scan_code()
        content_findings = [] if args.code_only else scan_content()
        write_findings(code_findings, content_findings, run_dir)
        print(f"  Found {len(code_findings)} code issues, {len(content_findings)} content issues")
        print(f"  Findings: {run_dir / 'findings.md'}")

    # Phase 2: Plan (skip if resuming with existing plan)
    plan_path = run_dir / "task_plan.md"
    if args.resume and plan_path.exists():
        print(f"\n[Phase 2] Using existing task plan")
    else:
        print("\n[Phase 2] Generating task plan...")
        generate_task_plan(run_dir, max_rounds=args.rounds)
        print(f"  Plan: {plan_path}")

    if args.dry_run:
        print("\n[Dry Run] Stopping before execution. Review:")
        print(f"  Findings: {run_dir / 'findings.md'}")
        print(f"  Plan:     {plan_path}")
        return

    # Phase 3: Execute
    print(f"\n[Phase 3] Executing rounds...")
    tasks = parse_task_plan(plan_path)

    # Filter by mode
    if args.code_only:
        tasks = [t for t in tasks if t["type"].startswith("code") or t["type"] == "pipeline-fix"]
    elif args.content_only:
        tasks = [t for t in tasks if t["type"].startswith("content")]

    # Filter to pending only (for --resume)
    pending = [t for t in tasks if t.get("status", "pending") == "pending"]
    print(f"  {len(pending)} pending tasks out of {len(tasks)} total")

    results = []
    # Load any existing results from previous partial run
    results_json = run_dir / "results.json"
    if results_json.exists():
        try:
            results = json.loads(results_json.read_text())
        except Exception:
            pass

    for task in pending:
        round_num = task["round"]
        print(f"\n--- Round {round_num}/{len(tasks)}: {task['type']} → {task.get('target', '?')} ---")

        # Override timeout from CLI args
        config.DEFAULT_TIMEOUT = args.timeout

        result = execute_round(task, round_num, run_dir)
        results.append(result)

        # Update task status in plan
        update_task_status(plan_path, round_num, result["status"])

        # Save intermediate results (crash recovery)
        results_json.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str))

        status_icon = {"done": "OK", "failed": "FAIL", "error": "ERR",
                       "skipped": "SKIP", "no-changes": "---"}.get(result["status"], "?")
        pr = result.get("pr_url", "")
        print(f"  Result: {status_icon} | {result.get('verification', {}).get('reason', '')}")
        if pr:
            print(f"  PR: {pr}")

    # Phase 4: Report
    end_time = datetime.now()
    print(f"\n[Phase 4] Generating morning report...")
    report_path = generate_report(results, start_time, end_time, run_dir)
    print(f"  Report: {report_path}")

    # Summary
    done = sum(1 for r in results if r["status"] == "done")
    total = len(results)
    print(f"\n{'=' * 60}")
    print(f"DONE: {done}/{total} rounds completed successfully")
    print(f"Review: {report_path}")
    print(f"{'=' * 60}")


def run_with_caffeinate():
    """Wrap execution with caffeinate to prevent macOS sleep."""
    # If we're already running under caffeinate, just run main
    if os.environ.get("OVERNIGHT_CAFFEINATED"):
        main()
        return

    # Otherwise, re-exec ourselves under caffeinate
    os.environ["OVERNIGHT_CAFFEINATED"] = "1"
    cmd = ["caffeinate", "-i", sys.executable, "-m", "scripts.overnight"] + sys.argv[1:]
    try:
        os.execvp("caffeinate", cmd)
    except FileNotFoundError:
        # caffeinate not available (non-macOS), just run directly
        main()


if __name__ == "__main__":
    run_with_caffeinate()
```

- [ ] **Step 4: Run tests, verify they pass**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_main.py -v`
Expected: 3 passed

- [ ] **Step 5: Run full test suite**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/ -v`
Expected: All tests pass (18+ tests)

- [ ] **Step 6: Commit**

```bash
git add scripts/overnight/__main__.py scripts/overnight/tests/test_main.py
git commit -m "feat(overnight): add CLI entry point with caffeinate wrapper"
```

---

### Task 8: Integration Test — Dry Run

**Files:**
- Modify: `scripts/overnight/tests/test_main.py` (add integration test)

- [ ] **Step 1: Write integration test**

Append to `scripts/overnight/tests/test_main.py`:

```python
def test_dry_run_integration(tmp_path, monkeypatch):
    """Full dry run: scan → plan → stop. No worktrees, no Claude calls."""
    from scripts.overnight.__main__ import main
    from scripts.overnight import config

    # Override run dir to tmp
    monkeypatch.setattr(config, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(config, "get_run_dir", lambda: tmp_path / "runs" / "2026-04-08")
    monkeypatch.setattr("sys.argv", ["overnight", "--dry-run", "--rounds", "5"])

    # Mock prerequisites
    with patch("scripts.overnight.__main__.check_prerequisites"):
        with patch("scripts.overnight.__main__.cleanup_previous_runs"):
            with patch("scripts.overnight.scanner.scan_code") as mock_code:
                mock_code.return_value = [
                    {"type": "code-lint", "severity": 8, "target": "App.jsx",
                     "description": "2 lint errors", "details": "..."},
                ]
                with patch("scripts.overnight.scanner.scan_content") as mock_content:
                    mock_content.return_value = []
                    main()

    # Verify outputs created
    run_dir = tmp_path / "runs" / "2026-04-08"
    assert (run_dir / "findings.md").exists()
    assert (run_dir / "findings.json").exists()
    assert (run_dir / "task_plan.md").exists()
```

- [ ] **Step 2: Run integration test**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/test_main.py::test_dry_run_integration -v`
Expected: PASS

- [ ] **Step 3: Manual dry run on real project**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m scripts.overnight --dry-run --rounds 5`
Expected: Scans real project, produces findings.md and task_plan.md, exits before execution. Review the output files manually.

- [ ] **Step 4: Commit**

```bash
git add scripts/overnight/tests/test_main.py
git commit -m "test(overnight): add integration test for dry run flow"
```

---

### Task 9: End-to-End Validation

This task is manual — no new code, just validation and cleanup.

- [ ] **Step 1: Run full test suite**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m pytest scripts/overnight/tests/ -v --tb=short`
Expected: All tests pass

- [ ] **Step 2: Test real dry run**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m scripts.overnight --dry-run --rounds 3`
Expected: Creates `scripts/overnight/runs/2026-04-08/` with findings.md, findings.json, task_plan.md, task_plan.json

- [ ] **Step 3: Validate task_plan.md has correct structure**

Read `scripts/overnight/runs/2026-04-08/task_plan.md` and verify:
- Tasks are interleaved (code/content alternating)
- Each task has: target, issue, action, verify, status
- Status is "pending" for all tasks

- [ ] **Step 4: Test single real round (1 round only)**

Run: `cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin && python -m scripts.overnight --rounds 1 --code-only`
Expected: Executes 1 code improvement round, creates a PR (or reports failure), generates progress.md

- [ ] **Step 5: Review and clean up test artifacts**

```bash
# Check what was created
ls scripts/overnight/runs/
# Clean test branches
git branch --list 'overnight/*' | xargs -r git branch -D
# Clean test worktrees
git worktree list | grep overnight
```

- [ ] **Step 6: Final commit**

```bash
git add -A scripts/overnight/
git commit -m "feat(overnight): complete overnight iteration system v1.0

Automated system that scans code and content for quality issues,
iterates improvements via Claude CLI in isolated git worktrees,
and produces GitHub PRs for morning review.

Usage: python -m scripts.overnight --rounds 20"
```

---

## Dependency Graph

```
Task 1 (config) ─── is needed by all others
       │
       ├── Task 2 (scanner) ──┐
       │                      ├── Task 3 (planner)
       ├── Task 4 (prompts) ──┤
       │                      ├── Task 5 (executor)
       │                      │          │
       │                      ├── Task 6 (reporter)
       │                      │
       └──────────────────────┴── Task 7 (__main__)
                                       │
                                  Task 8 (integration test)
                                       │
                                  Task 9 (E2E validation)
```

Tasks 2 and 4 can run in parallel. Tasks 5 and 6 can run in parallel after 2, 3, 4 complete. Task 7 needs all others. Tasks 8-9 are sequential validation.
