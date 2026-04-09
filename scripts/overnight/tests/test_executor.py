"""Tests for the executor module."""
import subprocess
from unittest.mock import patch, MagicMock, call
from pathlib import Path


def test_cleanup_previous_runs():
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
        assert mock_run.call_count >= 3


def test_create_worktree():
    from scripts.overnight.executor import create_worktree
    with patch("scripts.overnight.executor._run_cmd") as mock_run:
        mock_run.return_value = ""
        with patch("scripts.overnight.config.WORKTREE_BASE", Path("/tmp/wt")):
            path = create_worktree(1, "lint-fix")
            assert "overnight-wt-1" in str(path)
            # cmd is now a list; check that it contains the expected tokens
            cmd_list = mock_run.call_args[0][0]
            assert isinstance(cmd_list, list)
            assert "worktree" in cmd_list
            assert "add" in cmd_list
            assert "main" in cmd_list


def test_remove_worktree():
    from scripts.overnight.executor import remove_worktree
    with patch("scripts.overnight.executor._run_cmd") as mock_run:
        mock_run.return_value = ""
        remove_worktree(Path("/tmp/overnight-wt-1"))
        cmd_list = mock_run.call_args[0][0]
        assert isinstance(cmd_list, list)
        assert "worktree" in cmd_list
        assert "remove" in cmd_list


def test_check_disk_space():
    from scripts.overnight.executor import check_disk_space
    assert check_disk_space() is True


def test_create_content_backup(tmp_path):
    from scripts.overnight.executor import create_content_backup
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
