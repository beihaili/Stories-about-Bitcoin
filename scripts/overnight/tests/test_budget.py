"""Tests for the budget tracking module."""
from datetime import datetime, timedelta
from unittest.mock import patch


def test_record_round_estimates_tokens():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker()
    entry = tracker.record_round("Hello world prompt", "Response text here")

    assert entry["input_tokens"] > 0
    assert entry["output_tokens"] > 0
    assert tracker.rounds_completed == 1
    assert tracker.total_tokens() > 0


def test_hours_elapsed():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker()
    tracker.start_time = datetime.now() - timedelta(hours=2)
    assert 1.9 < tracker.hours_elapsed() < 2.1


def test_hours_remaining():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker(window_hours=5.0)
    tracker.start_time = datetime.now() - timedelta(hours=3)
    assert 1.9 < tracker.hours_remaining() < 2.1


def test_in_last_hour():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker(window_hours=5.0)

    # 2 hours in — not in last hour
    tracker.start_time = datetime.now() - timedelta(hours=2)
    assert tracker.in_last_hour() is False

    # 4.5 hours in — in last hour
    tracker.start_time = datetime.now() - timedelta(hours=4, minutes=30)
    assert tracker.in_last_hour() is True


def test_should_burn_in_last_hour_with_low_usage():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker(window_hours=5.0, burn_threshold=0.30)
    # 4.5 hours in, barely any tokens used
    tracker.start_time = datetime.now() - timedelta(hours=4, minutes=30)
    tracker.record_round("short", "short")  # tiny usage

    assert tracker.should_burn() is True


def test_should_not_burn_early():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker(window_hours=5.0)
    # Only 30 minutes in, but with low usage — don't burn yet (not enough data)
    tracker.start_time = datetime.now() - timedelta(minutes=30)
    tracker.record_round("short", "short")

    assert tracker.should_burn() is False


def test_should_rescan_after_one_hour():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker()
    old_time = datetime.now() - timedelta(hours=1, minutes=5)
    assert tracker.should_rescan(old_time) is True

    recent_time = datetime.now() - timedelta(minutes=30)
    assert tracker.should_rescan(recent_time) is False


def test_format_status_line():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker()
    tracker.record_round("a" * 3000, "b" * 6000)
    line = tracker.format_status_line()
    assert "[budget]" in line
    assert "elapsed" in line
    assert "remaining" in line


def test_get_status_dict():
    from scripts.overnight.budget import BudgetTracker

    tracker = BudgetTracker()
    tracker.record_round("prompt text", "response text")
    status = tracker.get_status()

    assert "hours_elapsed" in status
    assert "burn_mode" in status
    assert "total_tokens_est" in status
    assert status["rounds_completed"] == 1
