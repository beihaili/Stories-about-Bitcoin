"""Tests for the planner module."""
import json
from pathlib import Path


def test_interleave_tasks():
    from scripts.overnight.planner import interleave_tasks
    code = [{"type": "code-lint", "id": "c1"}, {"type": "code-test", "id": "c2"}]
    content = [{"type": "content-refine", "id": "t1"}, {"type": "content-refine", "id": "t2"}]
    result = interleave_tasks(code, content)
    assert result[0]["type"].startswith("code")
    assert result[1]["type"].startswith("content")
    assert result[2]["type"].startswith("code")
    assert result[3]["type"].startswith("content")


def test_interleave_uneven_lists():
    from scripts.overnight.planner import interleave_tasks
    code = [{"type": "code-lint", "id": "c1"}]
    content = [{"type": "content-refine", "id": "t1"},
               {"type": "content-refine", "id": "t2"},
               {"type": "content-refine", "id": "t3"}]
    result = interleave_tasks(code, content)
    assert len(result) == 4
    assert result[0]["type"].startswith("code")
    assert result[1]["type"].startswith("content")


def test_generate_task_plan(tmp_run_dir, sample_findings):
    from scripts.overnight.planner import generate_task_plan
    json_path = tmp_run_dir / "findings.json"
    json_path.write_text(json.dumps(sample_findings, ensure_ascii=False, indent=2))
    plan_path = generate_task_plan(tmp_run_dir, max_rounds=10)
    assert plan_path.exists()
    content = plan_path.read_text()
    assert "## Round 1" in content
    assert "status: pending" in content


def test_parse_task_plan(tmp_run_dir):
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


def test_update_task_status(tmp_run_dir):
    """update_task_status modifies the correct round's status."""
    from scripts.overnight.planner import update_task_status
    plan = """# Plan

## Round 1 — code-lint
- **target**: a.js
- **status**: pending

## Round 2 — content-refine
- **target**: b.md
- **status**: pending
"""
    plan_path = tmp_run_dir / "task_plan.md"
    plan_path.write_text(plan)
    update_task_status(plan_path, 1, "done")
    content = plan_path.read_text()
    assert "## Round 1" in content
    # Round 1 should be done, Round 2 still pending
    lines = content.split("\n")
    r1_status = [l for l in lines if "status" in l][0]
    r2_status = [l for l in lines if "status" in l][1]
    assert "done" in r1_status
    assert "pending" in r2_status
