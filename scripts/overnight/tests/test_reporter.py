"""Tests for the reporter module."""
from datetime import datetime


def test_generate_report_basic(tmp_run_dir):
    from scripts.overnight.reporter import generate_report
    results = [
        {"round": 1, "type": "code-lint", "target": "App.jsx",
         "status": "done", "pr_url": "https://github.com/user/repo/pull/42",
         "verification": {"reason": "lint clean", "details": {}}},
        {"round": 2, "type": "content-refine", "target": "正文/11_test.md",
         "status": "done", "pr_url": "https://github.com/user/repo/pull/43",
         "verification": {"reason": "readability: 5→7", "details": {"before": 5, "after": 7}}},
        {"round": 3, "type": "content-refine", "target": "正文/17_test.md",
         "status": "failed", "pr_url": None,
         "verification": {"reason": "style: 6→5.8 (regressed)", "details": {}}},
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


def test_report_writes_results_json(tmp_run_dir):
    """generate_report must also write results.json alongside progress.md."""
    import json
    from scripts.overnight.reporter import generate_report

    results = [
        {"round": 1, "type": "code-lint", "target": "x.js", "status": "done",
         "pr_url": None, "verification": {"reason": "ok"}},
    ]
    now = datetime.now()
    path = generate_report(results, now, now, tmp_run_dir)

    json_path = tmp_run_dir / "results.json"
    assert json_path.exists()
    data = json.loads(json_path.read_text())
    assert isinstance(data, list)
    assert data[0]["round"] == 1


def test_report_empty_results(tmp_run_dir):
    """An empty results list should still produce a valid report."""
    from scripts.overnight.reporter import generate_report

    now = datetime.now()
    path = generate_report([], now, now, tmp_run_dir)
    assert path.exists()
    content = path.read_text()
    assert "Completed: 0" in content


def test_report_duration_calculation(tmp_run_dir):
    """Duration in hours should be computed correctly."""
    from scripts.overnight.reporter import generate_report

    start = datetime(2026, 4, 8, 22, 0, 0)
    end = datetime(2026, 4, 9, 4, 30, 0)   # 6.5 hours later
    path = generate_report([], start, end, tmp_run_dir)
    content = path.read_text()
    assert "6.5h" in content


def test_report_pr_count_breakdown(tmp_run_dir):
    """Code PRs and Content PRs should be counted separately."""
    from scripts.overnight.reporter import generate_report

    results = [
        {"round": 1, "type": "code-lint", "target": "a.js", "status": "done",
         "pr_url": "#1", "verification": {"reason": "ok"}},
        {"round": 2, "type": "code-test", "target": "b.js", "status": "done",
         "pr_url": "#2", "verification": {"reason": "ok"}},
        {"round": 3, "type": "content-refine", "target": "ch.md", "status": "done",
         "pr_url": "#3", "verification": {"reason": "ok"}},
    ]
    now = datetime.now()
    path = generate_report(results, now, now, tmp_run_dir)
    content = path.read_text()
    assert "Code PRs: 2" in content
    assert "Content PRs: 1" in content


def test_report_failed_tasks_section(tmp_run_dir):
    """Failed tasks should appear in the 'Failed Tasks' section with their reasons."""
    from scripts.overnight.reporter import generate_report

    results = [
        {"round": 2, "type": "content-refine", "target": "正文/05_test.md",
         "status": "failed", "pr_url": None,
         "verification": {"reason": "quality dropped"}},
    ]
    now = datetime.now()
    path = generate_report(results, now, now, tmp_run_dir)
    content = path.read_text()
    assert "Failed Tasks" in content
    assert "quality dropped" in content
    assert "05_test.md" in content


def test_report_status_icons(tmp_run_dir):
    """Status icons should be mapped correctly in the results table."""
    from scripts.overnight.reporter import generate_report

    results = [
        {"round": 1, "type": "code-lint", "target": "a.js", "status": "done",
         "pr_url": None, "verification": {"reason": "ok"}},
        {"round": 2, "type": "code-lint", "target": "b.js", "status": "failed",
         "pr_url": None, "verification": {"reason": "fail"}},
        {"round": 3, "type": "code-lint", "target": "c.js", "status": "error",
         "pr_url": None, "verification": {"reason": "err"}},
        {"round": 4, "type": "code-lint", "target": "d.js", "status": "skipped",
         "pr_url": None, "verification": {"reason": "skip"}},
        {"round": 5, "type": "code-lint", "target": "e.js", "status": "no-changes",
         "pr_url": None, "verification": {"reason": "nc"}},
    ]
    now = datetime.now()
    path = generate_report(results, now, now, tmp_run_dir)
    content = path.read_text()
    assert "pass" in content
    assert "FAIL" in content
    assert "ERR" in content
    assert "SKIP" in content
    assert "---" in content
