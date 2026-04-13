"""
Token budget tracking for the overnight iteration system.

Estimates token usage per round (from prompt/response lengths) and decides
whether to switch to "burn mode" when approaching the end of a Max plan
5-hour rolling window with unused quota.

Usage:
    tracker = BudgetTracker(window_hours=5)
    tracker.record_round(prompt_text, response_text)
    if tracker.should_burn():
        # generate extra tasks and keep going
"""
from datetime import datetime


# Max plan 5h window — rough capacity estimate.
# Actual limits vary; this is a conservative estimate for rate-based decisions.
# We don't need the exact number — we just need to detect "low usage rate".
ESTIMATED_WINDOW_TOKENS = 30_000_000  # ~30M tokens per 5h window (conservative)


class BudgetTracker:
    """Track token usage and decide when to ramp up consumption."""

    def __init__(self, window_hours: float = 5.0, burn_threshold: float = 0.30):
        """
        Args:
            window_hours: Length of the Max plan rolling window.
            burn_threshold: If estimated remaining > this fraction in the last
                            hour, switch to burn mode.
        """
        self.window_hours = window_hours
        self.burn_threshold = burn_threshold
        self.start_time = datetime.now()
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.rounds_completed = 0
        self.round_history: list[dict] = []

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_round(self, prompt: str, response: str) -> dict:
        """
        Record a completed round's token usage (estimated from text lengths).

        Chinese text: ~2 chars/token. English: ~4 chars/token.
        Mixed content: ~3 chars/token (conservative).

        Returns:
            Dict with estimated input/output tokens for this round.
        """
        input_tokens = max(1, len(prompt) // 3)
        output_tokens = max(1, len(response) // 3)

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.rounds_completed += 1

        entry = {
            "round": self.rounds_completed,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "timestamp": datetime.now().isoformat(),
        }
        self.round_history.append(entry)
        return entry

    # ------------------------------------------------------------------
    # Time calculations
    # ------------------------------------------------------------------

    def hours_elapsed(self) -> float:
        """Hours since this tracker was created."""
        return (datetime.now() - self.start_time).total_seconds() / 3600

    def hours_remaining(self) -> float:
        """Estimated hours until the 5h window resets."""
        return max(0.0, self.window_hours - self.hours_elapsed())

    def in_last_hour(self) -> bool:
        """Are we in the final hour of the window?"""
        return self.hours_remaining() <= 1.0

    # ------------------------------------------------------------------
    # Usage estimation
    # ------------------------------------------------------------------

    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    def tokens_per_hour(self) -> float:
        """Average token consumption rate."""
        hours = self.hours_elapsed()
        if hours < 0.01:
            return 0.0
        return self.total_tokens() / hours

    def estimated_usage_fraction(self) -> float:
        """
        Estimate what fraction of the 5h window budget we've used.
        Returns a float 0.0–1.0 (can exceed 1.0 if estimate is off).
        """
        return self.total_tokens() / ESTIMATED_WINDOW_TOKENS

    def estimated_remaining_fraction(self) -> float:
        """Estimated fraction of the window budget still available."""
        return max(0.0, 1.0 - self.estimated_usage_fraction())

    # ------------------------------------------------------------------
    # Burn mode decision
    # ------------------------------------------------------------------

    def should_burn(self) -> bool:
        """
        Should we switch to aggressive token consumption?

        True when:
        - We're in the last hour of the 5h window, AND
        - Estimated remaining quota > burn_threshold (default 30%)

        Also True when:
        - We've been running for > 1 hour, AND
        - Token consumption rate is very low (< 5% of window per hour)
        """
        remaining = self.estimated_remaining_fraction()

        # In the last hour with plenty left
        if self.in_last_hour() and remaining > self.burn_threshold:
            return True

        # Running a while but barely using anything
        hours = self.hours_elapsed()
        if hours >= 1.0:
            rate_per_hour = self.tokens_per_hour()
            # If at this rate we'd use < 50% of window in 5 hours, burn
            projected_total = rate_per_hour * self.window_hours
            if projected_total < ESTIMATED_WINDOW_TOKENS * 0.5:
                return True

        return False

    def should_rescan(self, last_scan_time: datetime) -> bool:
        """
        Should we rescan for new tasks?
        True if it's been >= 1 hour since the last scan.
        """
        elapsed = (datetime.now() - last_scan_time).total_seconds()
        return elapsed >= 3600

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict:
        """Get a snapshot of current budget status for logging."""
        return {
            "hours_elapsed": round(self.hours_elapsed(), 2),
            "hours_remaining": round(self.hours_remaining(), 2),
            "rounds_completed": self.rounds_completed,
            "total_tokens_est": self.total_tokens(),
            "tokens_per_hour": round(self.tokens_per_hour()),
            "usage_fraction": round(self.estimated_usage_fraction(), 3),
            "remaining_fraction": round(self.estimated_remaining_fraction(), 3),
            "burn_mode": self.should_burn(),
        }

    def format_status_line(self) -> str:
        """One-line status for logging."""
        s = self.get_status()
        mode = "BURN" if s["burn_mode"] else "normal"
        return (
            f"[budget] {s['hours_elapsed']:.1f}h elapsed | "
            f"~{s['usage_fraction']:.0%} used | "
            f"~{s['remaining_fraction']:.0%} remaining | "
            f"{s['tokens_per_hour']:,.0f} tok/h | "
            f"mode: {mode}"
        )
