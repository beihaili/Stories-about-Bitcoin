"""
Content calendar tracker for the content pipeline.

Tracks each chapter's status through the pipeline:
  draft → rewriting → scoring → translating → published

Links with the Twitter slicer to auto-generate social content on publish.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from . import config

STATUSES = ["draft", "rewriting", "scoring", "translating", "review", "published"]


def load_calendar() -> Dict:
    """Load the content calendar from JSON."""
    if config.CALENDAR_FILE.exists():
        with open(config.CALENDAR_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"chapters": {}, "updated_at": None}


def save_calendar(calendar: Dict):
    """Save the content calendar to JSON."""
    calendar["updated_at"] = datetime.now().isoformat()
    config.CALENDAR_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(config.CALENDAR_FILE, "w", encoding="utf-8") as f:
        json.dump(calendar, f, ensure_ascii=False, indent=2)


def get_chapter_status(chapter_num: int) -> Dict:
    """Get the status of a specific chapter."""
    cal = load_calendar()
    key = str(chapter_num)
    return cal["chapters"].get(key, {"status": "unknown", "chapter": chapter_num})


def update_chapter_status(
    chapter_num: int,
    status: str,
    metadata: Optional[Dict] = None,
):
    """Update a chapter's status in the calendar."""
    if status not in STATUSES:
        print(f"Warning: unknown status '{status}'. Valid: {STATUSES}")

    cal = load_calendar()
    key = str(chapter_num)

    if key not in cal["chapters"]:
        cal["chapters"][key] = {
            "chapter": chapter_num,
            "status": status,
            "created_at": datetime.now().isoformat(),
            "history": [],
        }
    else:
        # Record status change
        old_status = cal["chapters"][key].get("status", "unknown")
        cal["chapters"][key]["history"].append({
            "from": old_status,
            "to": status,
            "at": datetime.now().isoformat(),
        })
        cal["chapters"][key]["status"] = status

    # Merge metadata
    if metadata:
        cal["chapters"][key].update(metadata)

    cal["chapters"][key]["updated_at"] = datetime.now().isoformat()
    save_calendar(cal)
    return cal["chapters"][key]


def scan_existing_chapters() -> Dict:
    """
    Scan both repos to auto-detect chapter statuses.
    Checks for zh/en files, drafts, and published chapters.
    """
    cal = load_calendar()

    # Scan local repo drafts
    if config.CHAPTERS_DIR.exists():
        for f in sorted(config.CHAPTERS_DIR.glob("*.txt")):
            parts = f.stem.split("_")
            if parts and parts[0].isdigit():
                ch_num = int(parts[0])
                key = str(ch_num)
                if key not in cal["chapters"]:
                    cal["chapters"][key] = {
                        "chapter": ch_num,
                        "status": "draft",
                        "zh_title": f.stem,
                        "local_file": str(f),
                        "created_at": datetime.now().isoformat(),
                        "history": [],
                    }

    # Scan main repo for published chapters
    if config.MAIN_ZH_DIR.exists():
        for f in sorted(config.MAIN_ZH_DIR.glob("*.md")):
            if f.name in ("SUMMARY.md", "INTRO.md", "GLOSSARY.md", "README.md"):
                continue
            parts = f.stem.split("_")
            if parts and parts[0].isdigit():
                ch_num = int(parts[0])
                key = str(ch_num)
                entry = cal["chapters"].get(key, {
                    "chapter": ch_num,
                    "status": "published",
                    "history": [],
                })

                entry["zh_published"] = True
                entry["zh_file"] = f.name

                # Check if EN version exists
                en_matches = list(config.MAIN_EN_DIR.glob(f"{ch_num:02d}_*.md"))
                if en_matches:
                    entry["en_published"] = True
                    entry["en_file"] = en_matches[0].name
                    entry["status"] = "published"
                else:
                    if entry.get("status") == "published":
                        entry["status"] = "translating"  # ZH exists but EN doesn't

                cal["chapters"][key] = entry

    save_calendar(cal)
    return cal


def trigger_twitter_content(chapter_num: int, lang: str = "zh"):
    """
    After publishing, auto-generate Twitter content for the chapter.
    Calls the twitter_slicer CLI.
    """
    slicer_cli = config.PROJECT_ROOT / "scripts" / "twitter_slicer" / "cli.py"
    if not slicer_cli.exists():
        print(f"  Twitter slicer not found at {slicer_cli}")
        return

    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, str(slicer_cli), "chapter", str(chapter_num), "--lang", lang],
            capture_output=True, text=True, cwd=str(slicer_cli.parent),
        )
        if result.returncode == 0:
            print(f"  Twitter content generated for ch{chapter_num:02d} ({lang})")
        else:
            print(f"  Twitter slicer error: {result.stderr[:200]}")
    except Exception as e:
        print(f"  Twitter slicer failed: {e}")


def format_calendar_table(calendar: Optional[Dict] = None) -> str:
    """Format the calendar as a readable table."""
    if calendar is None:
        calendar = load_calendar()

    chapters = calendar.get("chapters", {})
    if not chapters:
        return "No chapters tracked. Run `scan` to detect existing chapters."

    lines = []
    lines.append(f"Content Calendar (updated: {calendar.get('updated_at', 'never')})")
    lines.append("")
    lines.append(f"{'Ch#':<5} {'Status':<14} {'ZH':<4} {'EN':<4} {'Last Updated':<20}")
    lines.append("-" * 55)

    for key in sorted(chapters.keys(), key=lambda x: int(x)):
        ch = chapters[key]
        ch_num = ch.get("chapter", key)
        status = ch.get("status", "?")
        zh = "Y" if ch.get("zh_published") else "-"
        en = "Y" if ch.get("en_published") else "-"
        updated = ch.get("updated_at", "?")[:16]
        lines.append(f"{ch_num:<5} {status:<14} {zh:<4} {en:<4} {updated:<20}")

    # Summary
    by_status = {}
    for ch in chapters.values():
        s = ch.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1

    lines.append("")
    lines.append("Summary:")
    for status in STATUSES:
        count = by_status.get(status, 0)
        if count:
            lines.append(f"  {status}: {count}")

    return "\n".join(lines)
