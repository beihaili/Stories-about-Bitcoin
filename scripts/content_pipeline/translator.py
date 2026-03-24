"""
Auto Chinese-to-English translator for the content pipeline.

Features:
- Segment-by-segment translation at H1/H2 boundaries
- Glossary-enforced terminology (glossary.json)
- Few-shot style reference from existing en/ chapters
- Outputs translation + diff against existing English version
"""

import difflib
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import config


def load_glossary() -> Dict[str, str]:
    """Load the terminology glossary for consistent translation."""
    if not config.GLOSSARY_FILE.exists():
        return {}

    with open(config.GLOSSARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten all categories into one dict
    glossary = {}
    for category in ("proper_nouns", "technical_terms", "cultural_terms", "organization_terms"):
        glossary.update(data.get(category, {}))

    return glossary


def segment_by_headings(text: str) -> List[Dict]:
    """
    Split markdown text into segments at H1/H2 boundaries.
    Returns list of {level, heading, content} dicts.
    """
    segments = []
    lines = text.split("\n")
    current_heading = ""
    current_level = 0
    current_lines = []

    for line in lines:
        h1_match = re.match(r"^# (.+)$", line)
        h2_match = re.match(r"^## (.+)$", line)

        if h1_match or h2_match:
            # Save previous segment
            if current_lines or current_heading:
                segments.append({
                    "level": current_level,
                    "heading": current_heading,
                    "content": "\n".join(current_lines).strip(),
                })

            if h1_match:
                current_heading = h1_match.group(1)
                current_level = 1
            else:
                current_heading = h2_match.group(1)
                current_level = 2
            current_lines = []
        else:
            current_lines.append(line)

    # Save last segment
    if current_lines or current_heading:
        segments.append({
            "level": current_level,
            "heading": current_heading,
            "content": "\n".join(current_lines).strip(),
        })

    return segments


def load_style_reference(chapter_num: Optional[int] = None) -> str:
    """
    Load an existing English chapter as style reference.
    Picks the closest available chapter to the requested one.
    """
    en_dir = config.MAIN_EN_DIR
    if not en_dir.exists():
        return ""

    # Find available English chapters
    en_files = sorted(en_dir.glob("*.md"))
    if not en_files:
        return ""

    # Try to find closest chapter
    target = chapter_num or 1
    best_file = None
    best_dist = float("inf")

    for f in en_files:
        name = f.stem
        parts = name.split("_")
        if parts and parts[0].isdigit():
            num = int(parts[0])
            dist = abs(num - target)
            if dist < best_dist:
                best_dist = dist
                best_file = f

    if not best_file:
        best_file = en_files[0]

    with open(best_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Return first ~2000 chars as reference
    return content[:2000]


def build_glossary_prompt(glossary: Dict[str, str]) -> str:
    """Format glossary as translation instructions."""
    if not glossary:
        return ""

    lines = ["【术语表 — 必须使用以下翻译】"]
    for zh, en in sorted(glossary.items()):
        lines.append(f"  {zh} → {en}")
    return "\n".join(lines[:60])  # Cap at 60 terms to avoid bloat


TRANSLATE_PROMPT = """You are translating a chapter from 《比特币那些事儿》(Stories about Bitcoin),
a literary narrative history of Bitcoin written in the style of "明朝那些事儿" (Those Things About the Ming Dynasty).

The translation should:
1. Preserve the lively, conversational tone — this is NOT a textbook
2. Keep the author's voice: first person, casual asides, rhetorical questions, humor
3. Translate Chinese idioms into natural English equivalents (don't transliterate)
4. Keep all Markdown formatting (headers, bold, blockquotes, links)
5. Use the exact English terms from the glossary below
6. Maintain paragraph structure and section breaks

{glossary_section}

{style_reference}

【Chinese source text to translate】
```
{source_text}
```

Output ONLY the English translation in Markdown format. Do not add translator notes or explanations."""


def translate_segment(
    client,
    model: str,
    segment: Dict,
    glossary: Dict[str, str],
    style_ref: str = "",
) -> str:
    """Translate a single segment (heading + content)."""
    glossary_section = build_glossary_prompt(glossary)
    style_section = f"【English style reference from existing chapter】\n{style_ref}" if style_ref else ""

    # Build source text with heading
    source_parts = []
    if segment["heading"]:
        prefix = "#" * segment["level"]
        source_parts.append(f"{prefix} {segment['heading']}")
    if segment["content"]:
        source_parts.append(segment["content"])
    source_text = "\n\n".join(source_parts)

    if not source_text.strip():
        return ""

    prompt = TRANSLATE_PROMPT.format(
        glossary_section=glossary_section,
        style_reference=style_section,
        source_text=source_text,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        result = response.choices[0].message.content.strip()
        # Strip markdown code block wrappers if present
        if result.startswith("```markdown"):
            result = result[len("```markdown"):].strip()
        if result.startswith("```"):
            result = result[3:].strip()
        if result.endswith("```"):
            result = result[:-3].strip()
        return result
    except Exception as e:
        return f"[Translation error: {e}]"


def translate_chapter(
    client,
    model: str,
    zh_text: str,
    chapter_num: Optional[int] = None,
) -> Tuple[str, str]:
    """
    Translate a full Chinese chapter to English.

    Returns (translated_text, diff_against_existing).
    """
    glossary = load_glossary()
    style_ref = load_style_reference(chapter_num)
    segments = segment_by_headings(zh_text)

    print(f"  Translating {len(segments)} segments...")

    translated_parts = []
    for i, seg in enumerate(segments):
        print(f"  Segment {i + 1}/{len(segments)}: {seg['heading'][:30] or '(intro)'}...")
        result = translate_segment(client, model, seg, glossary, style_ref)
        translated_parts.append(result)

    translated = "\n\n".join(translated_parts)

    # Generate diff against existing English version
    diff = ""
    if chapter_num is not None:
        existing = _find_existing_english(chapter_num)
        if existing:
            diff = generate_diff(existing, translated)

    return translated, diff


def _find_existing_english(chapter_num: int) -> str:
    """Find and load existing English chapter file."""
    en_dir = config.MAIN_EN_DIR
    if not en_dir.exists():
        return ""

    # Search for matching file
    pattern = f"{chapter_num:02d}_*.md"
    matches = list(en_dir.glob(pattern))
    if not matches:
        # Try without zero-padding
        pattern = f"{chapter_num}_*.md"
        matches = list(en_dir.glob(pattern))

    if matches:
        with open(matches[0], "r", encoding="utf-8") as f:
            return f.read()
    return ""


def generate_diff(existing: str, new: str) -> str:
    """Generate a unified diff between existing and new translation."""
    existing_lines = existing.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)

    diff = difflib.unified_diff(
        existing_lines,
        new_lines,
        fromfile="existing_en.md",
        tofile="new_translation.md",
        lineterm="",
    )

    return "\n".join(diff)


def save_translation(
    translated: str,
    diff: str,
    chapter_num: int,
    output_dir=None,
):
    """Save translated chapter and diff to output directory."""
    out_dir = output_dir or config.TRANSLATION_OUTPUT
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save translation
    trans_path = out_dir / f"ch{chapter_num:02d}_en.md"
    with open(trans_path, "w", encoding="utf-8") as f:
        f.write(translated)

    # Save diff if available
    if diff:
        diff_path = out_dir / f"ch{chapter_num:02d}_diff.patch"
        with open(diff_path, "w", encoding="utf-8") as f:
            f.write(diff)

    return trans_path
