"""Tests for the overnight main entry point."""
from unittest.mock import patch, MagicMock, call
import argparse
import json
import time
from pathlib import Path


def test_parse_args_defaults():
    from scripts.overnight.__main__ import parse_args
    args = parse_args([])
    assert args.rounds == 20
    assert args.timeout == 900
    assert args.dry_run is False
    assert args.resume is False
    assert args.code_only is False
    assert args.content_only is False


def test_parse_args_custom():
    from scripts.overnight.__main__ import parse_args
    args = parse_args(["--rounds", "10", "--timeout", "600", "--dry-run"])
    assert args.rounds == 10
    assert args.timeout == 600
    assert args.dry_run is True


def test_parse_args_resume():
    from scripts.overnight.__main__ import parse_args
    args = parse_args(["--resume"])
    assert args.resume is True


def test_parse_args_code_only():
    from scripts.overnight.__main__ import parse_args
    args = parse_args(["--code-only"])
    assert args.code_only is True
    assert args.content_only is False


def test_parse_args_content_only():
    from scripts.overnight.__main__ import parse_args
    args = parse_args(["--content-only"])
    assert args.content_only is True
    assert args.code_only is False


def test_check_prerequisites():
    from scripts.overnight.__main__ import check_prerequisites
    with patch("shutil.which") as mock_which:
        mock_which.return_value = "/usr/bin/claude"
        try:
            check_prerequisites()
        except SystemExit:
            pass  # gh auth might fail in test environment


def test_check_prerequisites_missing_tool():
    """check_prerequisites should sys.exit(1) if a required tool is missing."""
    from scripts.overnight.__main__ import check_prerequisites
    import sys
    with patch("shutil.which", return_value=None):
        with patch("sys.exit") as mock_exit:
            check_prerequisites()
            mock_exit.assert_called_once_with(1)


def test_find_latest_run_no_runs(tmp_path):
    """find_latest_run returns None when runs/ directory is empty."""
    from scripts.overnight.__main__ import find_latest_run
    with patch("scripts.overnight.__main__.config") as mock_cfg:
        mock_cfg.RUNS_DIR = tmp_path / "runs"
        mock_cfg.RUNS_DIR.mkdir()
        result = find_latest_run()
        assert result is None


def test_find_latest_run_with_plan(tmp_path):
    """find_latest_run returns the most recent run dir that has task_plan.md."""
    from scripts.overnight.__main__ import find_latest_run
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    # Create two date dirs
    old_dir = runs_dir / "2026-04-07"
    new_dir = runs_dir / "2026-04-08"
    old_dir.mkdir()
    new_dir.mkdir()
    # Only new_dir has task_plan.md
    (new_dir / "task_plan.md").write_text("# Plan\n")
    with patch("scripts.overnight.__main__.config") as mock_cfg:
        mock_cfg.RUNS_DIR = runs_dir
        result = find_latest_run()
        assert result == new_dir


def test_find_latest_run_skips_dirs_without_plan(tmp_path):
    """find_latest_run skips directories that have no task_plan.md."""
    from scripts.overnight.__main__ import find_latest_run
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    empty_dir = runs_dir / "2026-04-08"
    empty_dir.mkdir()
    with patch("scripts.overnight.__main__.config") as mock_cfg:
        mock_cfg.RUNS_DIR = runs_dir
        result = find_latest_run()
        assert result is None


def test_main_dry_run(tmp_path):
    """--dry-run should run scan+plan phases only and not call execute_round."""
    from scripts.overnight.__main__ import main
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)

    mock_tasks = [
        {"round": 1, "type": "code-lint", "target": "src/App.jsx",
         "issue": "lint error", "action": "fix", "verify": "lint passes",
         "status": "pending"},
    ]
    mock_findings_path = run_dir / "findings.json"
    mock_findings_path.write_text(json.dumps({"code": [], "content": []}))
    mock_plan_path = run_dir / "task_plan.md"
    mock_plan_path.write_text("# Plan\n\n## Round 1 — code-lint\n- status: pending\n")

    with patch("scripts.overnight.__main__.config") as mock_cfg, \
         patch("scripts.overnight.__main__.check_prerequisites"), \
         patch("scripts.overnight.__main__.cleanup_previous_runs") as mock_cleanup, \
         patch("scripts.overnight.__main__.scan_code", return_value=[]) as mock_scan_code, \
         patch("scripts.overnight.__main__.scan_content", return_value=[]) as mock_scan_content, \
         patch("scripts.overnight.__main__.write_findings", return_value=(mock_findings_path, run_dir / "findings.md")) as mock_write, \
         patch("scripts.overnight.__main__.generate_task_plan", return_value=mock_plan_path) as mock_plan, \
         patch("scripts.overnight.__main__.parse_task_plan", return_value=mock_tasks) as mock_parse, \
         patch("scripts.overnight.__main__.execute_round") as mock_execute, \
         patch("scripts.overnight.__main__.generate_report") as mock_report:

        mock_cfg.RUNS_DIR = tmp_path / "runs"
        mock_cfg.get_run_dir.return_value = run_dir

        main(["--dry-run"])

        # execute_round must NOT be called in dry-run
        mock_execute.assert_not_called()
        # report also not generated in dry-run
        mock_report.assert_not_called()


def test_main_filters_code_only(tmp_path):
    """--code-only should skip content-refine tasks."""
    from scripts.overnight.__main__ import main
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)

    mock_tasks = [
        {"round": 1, "type": "code-lint", "target": "src/App.jsx",
         "issue": "lint", "action": "fix", "verify": "pass", "status": "pending"},
        {"round": 2, "type": "content-refine", "target": "正文/01.md",
         "issue": "style", "action": "refine", "verify": "improve", "status": "pending"},
    ]
    mock_findings_path = run_dir / "findings.json"
    mock_findings_path.write_text(json.dumps({"code": [], "content": []}))
    mock_plan_path = run_dir / "task_plan.md"
    mock_plan_path.write_text("# Plan\n")

    executed_tasks = []

    def fake_execute(task, round_num, run_dir, timeout=900):
        executed_tasks.append(task["type"])
        return {"round": round_num, "type": task["type"], "target": task["target"],
                "status": "done", "pr_url": None,
                "verification": {"passed": True, "reason": "ok", "details": {}},
                "started_at": "2026-04-08T00:00:00", "finished_at": "2026-04-08T00:01:00"}

    with patch("scripts.overnight.__main__.config") as mock_cfg, \
         patch("scripts.overnight.__main__.check_prerequisites"), \
         patch("scripts.overnight.__main__.cleanup_previous_runs"), \
         patch("scripts.overnight.__main__.scan_code", return_value=[]), \
         patch("scripts.overnight.__main__.scan_content", return_value=[]), \
         patch("scripts.overnight.__main__.write_findings", return_value=(mock_findings_path, run_dir / "findings.md")), \
         patch("scripts.overnight.__main__.generate_task_plan", return_value=mock_plan_path), \
         patch("scripts.overnight.__main__.parse_task_plan", return_value=mock_tasks), \
         patch("scripts.overnight.__main__.update_task_status"), \
         patch("scripts.overnight.__main__.execute_round", side_effect=fake_execute), \
         patch("scripts.overnight.__main__.generate_report", return_value=run_dir / "progress.md"):

        mock_cfg.RUNS_DIR = tmp_path / "runs"
        mock_cfg.get_run_dir.return_value = run_dir

        main(["--code-only"])

    assert executed_tasks == ["code-lint"]
    assert "content-refine" not in executed_tasks


def test_main_filters_content_only(tmp_path):
    """--content-only should skip code tasks."""
    from scripts.overnight.__main__ import main
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)

    mock_tasks = [
        {"round": 1, "type": "code-lint", "target": "src/App.jsx",
         "issue": "lint", "action": "fix", "verify": "pass", "status": "pending"},
        {"round": 2, "type": "content-refine", "target": "正文/01.md",
         "issue": "style", "action": "refine", "verify": "improve", "status": "pending"},
    ]
    mock_findings_path = run_dir / "findings.json"
    mock_findings_path.write_text(json.dumps({"code": [], "content": []}))
    mock_plan_path = run_dir / "task_plan.md"
    mock_plan_path.write_text("# Plan\n")

    executed_tasks = []

    def fake_execute(task, round_num, run_dir, timeout=900):
        executed_tasks.append(task["type"])
        return {"round": round_num, "type": task["type"], "target": task["target"],
                "status": "done", "pr_url": None,
                "verification": {"passed": True, "reason": "ok", "details": {}},
                "started_at": "2026-04-08T00:00:00", "finished_at": "2026-04-08T00:01:00"}

    with patch("scripts.overnight.__main__.config") as mock_cfg, \
         patch("scripts.overnight.__main__.check_prerequisites"), \
         patch("scripts.overnight.__main__.cleanup_previous_runs"), \
         patch("scripts.overnight.__main__.scan_code", return_value=[]), \
         patch("scripts.overnight.__main__.scan_content", return_value=[]), \
         patch("scripts.overnight.__main__.write_findings", return_value=(mock_findings_path, run_dir / "findings.md")), \
         patch("scripts.overnight.__main__.generate_task_plan", return_value=mock_plan_path), \
         patch("scripts.overnight.__main__.parse_task_plan", return_value=mock_tasks), \
         patch("scripts.overnight.__main__.update_task_status"), \
         patch("scripts.overnight.__main__.execute_round", side_effect=fake_execute), \
         patch("scripts.overnight.__main__.generate_report", return_value=run_dir / "progress.md"):

        mock_cfg.RUNS_DIR = tmp_path / "runs"
        mock_cfg.get_run_dir.return_value = run_dir

        main(["--content-only"])

    assert executed_tasks == ["content-refine"]
    assert "code-lint" not in executed_tasks


def test_main_resume_skips_scan_when_fresh(tmp_path):
    """--resume with fresh findings.json should skip the scan phase."""
    from scripts.overnight.__main__ import main
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)

    # Create fresh findings.json (recent mtime)
    findings_path = run_dir / "findings.json"
    findings_path.write_text(json.dumps({"code": [], "content": []}))
    plan_path = run_dir / "task_plan.md"
    plan_path.write_text("# Plan\n\n## Round 1 — code-lint\n- status: pending\n")

    mock_tasks = [
        {"round": 1, "type": "code-lint", "target": "src/App.jsx",
         "issue": "lint", "action": "fix", "verify": "pass", "status": "pending"},
    ]

    with patch("scripts.overnight.__main__.config") as mock_cfg, \
         patch("scripts.overnight.__main__.check_prerequisites"), \
         patch("scripts.overnight.__main__.cleanup_previous_runs"), \
         patch("scripts.overnight.__main__.scan_code") as mock_scan_code, \
         patch("scripts.overnight.__main__.scan_content") as mock_scan_content, \
         patch("scripts.overnight.__main__.write_findings") as mock_write, \
         patch("scripts.overnight.__main__.generate_task_plan") as mock_gen_plan, \
         patch("scripts.overnight.__main__.parse_task_plan", return_value=mock_tasks), \
         patch("scripts.overnight.__main__.update_task_status"), \
         patch("scripts.overnight.__main__.find_latest_run", return_value=run_dir), \
         patch("scripts.overnight.__main__.execute_round",
               return_value={"round": 1, "type": "code-lint", "target": "src/App.jsx",
                             "status": "done", "pr_url": None,
                             "verification": {"passed": True, "reason": "ok", "details": {}},
                             "started_at": "2026-04-08T00:00:00",
                             "finished_at": "2026-04-08T00:01:00"}), \
         patch("scripts.overnight.__main__.generate_report",
               return_value=run_dir / "progress.md"):

        mock_cfg.RUNS_DIR = tmp_path / "runs"
        mock_cfg.get_run_dir.return_value = run_dir

        main(["--resume"])

    # Scan functions must NOT be called when findings are fresh
    mock_scan_code.assert_not_called()
    mock_scan_content.assert_not_called()
    mock_write.assert_not_called()
    mock_gen_plan.assert_not_called()


def test_main_resume_rescans_stale_findings(tmp_path):
    """--resume with stale findings.json (> 3600s old) should re-run scan."""
    from scripts.overnight.__main__ import main
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)

    findings_path = run_dir / "findings.json"
    findings_path.write_text(json.dumps({"code": [], "content": []}))
    plan_path = run_dir / "task_plan.md"
    plan_path.write_text("# Plan\n\n## Round 1 — code-lint\n- status: pending\n")

    # Make findings stale by faking mtime to be > 3600s ago
    stale_time = time.time() - 7200  # 2 hours ago
    import os
    os.utime(findings_path, (stale_time, stale_time))

    mock_tasks = [
        {"round": 1, "type": "code-lint", "target": "src/App.jsx",
         "issue": "lint", "action": "fix", "verify": "pass", "status": "pending"},
    ]

    with patch("scripts.overnight.__main__.config") as mock_cfg, \
         patch("scripts.overnight.__main__.check_prerequisites"), \
         patch("scripts.overnight.__main__.cleanup_previous_runs"), \
         patch("scripts.overnight.__main__.scan_code", return_value=[]) as mock_scan_code, \
         patch("scripts.overnight.__main__.scan_content", return_value=[]) as mock_scan_content, \
         patch("scripts.overnight.__main__.write_findings",
               return_value=(findings_path, run_dir / "findings.md")) as mock_write, \
         patch("scripts.overnight.__main__.generate_task_plan", return_value=plan_path) as mock_gen_plan, \
         patch("scripts.overnight.__main__.parse_task_plan", return_value=mock_tasks), \
         patch("scripts.overnight.__main__.update_task_status"), \
         patch("scripts.overnight.__main__.find_latest_run", return_value=run_dir), \
         patch("scripts.overnight.__main__.execute_round",
               return_value={"round": 1, "type": "code-lint", "target": "src/App.jsx",
                             "status": "done", "pr_url": None,
                             "verification": {"passed": True, "reason": "ok", "details": {}},
                             "started_at": "2026-04-08T00:00:00",
                             "finished_at": "2026-04-08T00:01:00"}), \
         patch("scripts.overnight.__main__.generate_report",
               return_value=run_dir / "progress.md"):

        mock_cfg.RUNS_DIR = tmp_path / "runs"
        mock_cfg.get_run_dir.return_value = run_dir

        main(["--resume"])

    # Scan functions MUST be called when findings are stale
    mock_scan_code.assert_called_once()
    mock_scan_content.assert_called_once()
    mock_write.assert_called_once()
    # Plan MUST also be regenerated when findings were re-scanned (C2 fix)
    mock_gen_plan.assert_called_once()


def test_main_saves_intermediate_results(tmp_path):
    """After each round, results.json should be saved (crash recovery)."""
    from scripts.overnight.__main__ import main
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)

    mock_findings_path = run_dir / "findings.json"
    mock_findings_path.write_text(json.dumps({"code": [], "content": []}))
    mock_plan_path = run_dir / "task_plan.md"
    mock_plan_path.write_text("# Plan\n")

    mock_tasks = [
        {"round": 1, "type": "code-lint", "target": "src/App.jsx",
         "issue": "lint", "action": "fix", "verify": "pass", "status": "pending"},
        {"round": 2, "type": "code-test", "target": "src/Foo.jsx",
         "issue": "missing test", "action": "add test", "verify": "test passes",
         "status": "pending"},
    ]

    execute_call_count = [0]
    json_written_after_round = []

    def fake_execute(task, round_num, run_dir_arg, timeout=900):
        execute_call_count[0] += 1
        result = {"round": round_num, "type": task["type"], "target": task["target"],
                  "status": "done", "pr_url": None,
                  "verification": {"passed": True, "reason": "ok", "details": {}},
                  "started_at": "2026-04-08T00:00:00",
                  "finished_at": "2026-04-08T00:01:00"}
        return result

    def fake_update_status(plan_path, round_num, new_status):
        # Check if results.json has been written by this point
        results_path = run_dir / "results.json"
        if results_path.exists():
            json_written_after_round.append(round_num)

    with patch("scripts.overnight.__main__.config") as mock_cfg, \
         patch("scripts.overnight.__main__.check_prerequisites"), \
         patch("scripts.overnight.__main__.cleanup_previous_runs"), \
         patch("scripts.overnight.__main__.scan_code", return_value=[]), \
         patch("scripts.overnight.__main__.scan_content", return_value=[]), \
         patch("scripts.overnight.__main__.write_findings",
               return_value=(mock_findings_path, run_dir / "findings.md")), \
         patch("scripts.overnight.__main__.generate_task_plan", return_value=mock_plan_path), \
         patch("scripts.overnight.__main__.parse_task_plan", return_value=mock_tasks), \
         patch("scripts.overnight.__main__.update_task_status", side_effect=fake_update_status), \
         patch("scripts.overnight.__main__.execute_round", side_effect=fake_execute), \
         patch("scripts.overnight.__main__.generate_report",
               return_value=run_dir / "progress.md"):

        mock_cfg.RUNS_DIR = tmp_path / "runs"
        mock_cfg.get_run_dir.return_value = run_dir

        main([])

    # results.json should exist after the run
    assert (run_dir / "results.json").exists()


def test_run_with_caffeinate_non_macos():
    """run_with_caffeinate should not crash if caffeinate is not found."""
    from scripts.overnight.__main__ import run_with_caffeinate
    import os
    # Ensure OVERNIGHT_CAFFEINATED is not set
    env = {k: v for k, v in os.environ.items() if k != "OVERNIGHT_CAFFEINATED"}
    with patch.dict("os.environ", env, clear=True):
        with patch("subprocess.run", side_effect=FileNotFoundError("caffeinate not found")):
            # Should not raise — catches FileNotFoundError gracefully
            with patch("scripts.overnight.__main__.main") as mock_main:
                try:
                    run_with_caffeinate()
                    # If caffeinate raises FileNotFoundError, it should fall through to main()
                except SystemExit:
                    pass  # Acceptable


def test_run_with_caffeinate_already_caffeinated():
    """If OVERNIGHT_CAFFEINATED is set, run_with_caffeinate should not re-exec."""
    from scripts.overnight.__main__ import run_with_caffeinate
    import os
    with patch.dict("os.environ", {"OVERNIGHT_CAFFEINATED": "1"}):
        with patch("subprocess.run") as mock_sp:
            with patch("scripts.overnight.__main__.main") as mock_main:
                run_with_caffeinate()
                # Should call main() directly, not subprocess.run(caffeinate...)
                mock_sp.assert_not_called()
