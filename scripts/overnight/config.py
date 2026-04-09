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
MIN_DISK_GB = 1

# Quality thresholds
SCORE_PASS_THRESHOLD = 7.0
SCORE_IMPROVEMENT_MIN = 0.1

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
