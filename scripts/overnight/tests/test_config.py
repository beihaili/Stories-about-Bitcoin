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
    from datetime import date
    assert date.today().isoformat() in str(run_dir)


def test_worktree_base_is_outside_repo():
    from scripts.overnight.config import PROJECT_ROOT, WORKTREE_BASE
    assert str(WORKTREE_BASE).startswith(str(PROJECT_ROOT.parent))
    assert not str(WORKTREE_BASE).startswith(str(PROJECT_ROOT) + "/")
