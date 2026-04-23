#!/usr/bin/env python3
"""Export the delivery novel into Fanqie-friendly per-chapter files."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "我给中本聪送外卖" / "正文"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "发布" / "番茄" / "我给中本聪送外卖"

RISK_TERMS = [
    "比特币",
    "BTC",
    "btc",
    "买币",
    "炒币",
    "投资",
    "收益",
    "交易所",
    "钱包",
    "私钥",
    "洗钱",
    "赌博",
    "诈骗",
    "引导交易",
    "私下交易",
    "平台漏洞",
    "绕过风控",
]


@dataclass
class ChapterExport:
    number: int
    title: str
    source: str
    output: str
    body_chars: int
    total_chars: int
    risk_terms: list[str]


def project_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def chapter_files(source_dir: Path) -> list[tuple[int, Path]]:
    items: list[tuple[int, Path]] = []
    for path in source_dir.glob("*.md"):
        match = re.match(r"(\d+)_", path.name)
        if match:
            items.append((int(match.group(1)), path))
    return sorted(items, key=lambda item: item[0])


def extract_heading_and_body(text: str, fallback_title: str) -> tuple[str, str]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    # Drop YAML frontmatter if present.
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                lines = lines[index + 1 :]
                break

    title = fallback_title
    body_start = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            body_start = index + 1
            break

    return normalize_title(title), "\n".join(lines[body_start:]).strip()


def normalize_title(title: str) -> str:
    title = title.strip()
    title = re.sub(r"^第[零〇一二三四五六七八九十百千0-9]+章\s*", "", title)
    title = re.sub(r"^序章\s*", "", title)
    return title.strip() or "未命名"


def clean_body(text: str) -> str:
    lines = []
    in_html = False

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("<div") or stripped.startswith("<a "):
            in_html = True
            continue
        if in_html:
            if stripped.startswith("</div"):
                in_html = False
            continue

        if stripped.startswith("!["):
            continue
        if stripped == "---":
            lines.append("")
            continue

        if stripped.startswith("# "):
            continue
        if stripped.startswith("## "):
            line = stripped[3:]
        elif stripped.startswith("### "):
            line = stripped[4:]
        elif stripped.startswith("> "):
            line = stripped[2:]
        elif stripped == ">":
            line = ""

        line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
        line = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", line)
        line = re.sub(r"`([^`]+)`", r"\1", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        lines.append(line.rstrip())

    cleaned = []
    previous_empty = False
    for line in lines:
        is_empty = line.strip() == ""
        if is_empty and previous_empty:
            continue
        cleaned.append("" if is_empty else line)
        previous_empty = is_empty

    while cleaned and cleaned[0] == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return "\n".join(cleaned).strip()


def compact_char_count(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def risk_terms(text: str) -> list[str]:
    return [term for term in RISK_TERMS if term in text]


def export_chapter(number: int, source: Path, chapters_dir: Path) -> ChapterExport:
    fallback = source.stem.split("_", 1)[-1]
    title, raw_body = extract_heading_and_body(read_text(source), fallback)
    body = clean_body(raw_body)
    platform_title = f"第{number:03d}章 {title}"
    output_name = f"第{number:03d}章_{safe_filename(title)}.txt"
    output_path = chapters_dir / output_name
    chapter_text = f"{platform_title}\n\n{body}"
    write_text(output_path, chapter_text)

    return ChapterExport(
        number=number,
        title=platform_title,
        source=str(source.relative_to(PROJECT_ROOT)),
        output=str(output_path.relative_to(PROJECT_ROOT)),
        body_chars=compact_char_count(body),
        total_chars=compact_char_count(chapter_text),
        risk_terms=risk_terms(chapter_text),
    )


def chapter_export_text(chapter: ChapterExport) -> str:
    return read_text(project_path(chapter.output)).rstrip()


def safe_filename(title: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', "_", title)
    name = re.sub(r"\s+", "", name)
    return name[:80] or "未命名"


def write_manifest(
    output_dir: Path,
    chapters: list[ChapterExport],
    target_initial_chars: int,
) -> None:
    total_body_chars = sum(chapter.body_chars for chapter in chapters)
    payload = {
        "book": "我给中本聪送外卖",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "chapter_count": len(chapters),
        "total_body_chars": total_body_chars,
        "target_initial_chars": target_initial_chars,
        "ready_for_initial_submission": total_body_chars >= target_initial_chars,
        "ai_assisted": True,
        "chapters": [asdict(chapter) for chapter in chapters],
    }
    write_text(
        output_dir / "manifest.json",
        json.dumps(payload, ensure_ascii=False, indent=2),
    )


def write_combined_text(output_dir: Path, chapters: list[ChapterExport]) -> None:
    combined = "\n\n\n".join(chapter_export_text(chapter) for chapter in chapters)
    write_text(output_dir / "all_chapters.txt", combined)


def write_copy_page(output_dir: Path, chapters: list[ChapterExport]) -> None:
    all_text = read_text(output_dir / "all_chapters.txt").rstrip()
    chapter_cards = []

    for chapter in chapters:
        element_id = f"chapter-{chapter.number:03d}"
        chapter_text = chapter_export_text(chapter)
        chapter_cards.append(
            f"""<section class="card">
      <div class="card-head">
        <h2>{html.escape(chapter.title)}</h2>
        <span>{chapter.body_chars} 字符</span>
      </div>
      <button type="button" data-copy-target="{element_id}">复制本章</button>
      <textarea id="{element_id}" readonly>{html.escape(chapter_text)}</textarea>
    </section>"""
        )

    text = f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <title>番茄发布复制页 - 我给中本聪送外卖</title>
    <style>
      body {{
        margin: 32px auto;
        max-width: 960px;
        background: #f7f3ea;
        color: #211b16;
        font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      }}
      h1 {{
        margin-bottom: 8px;
      }}
      .summary {{
        color: #6c5f52;
        margin-bottom: 24px;
      }}
      .card {{
        background: #fffdf8;
        border: 1px solid #eadfce;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(77, 56, 36, 0.08);
        margin: 18px 0;
        padding: 18px;
      }}
      .card-head {{
        align-items: baseline;
        display: flex;
        justify-content: space-between;
        gap: 16px;
      }}
      h2 {{
        font-size: 20px;
        margin: 0 0 12px;
      }}
      button {{
        background: #1f2933;
        border: 0;
        border-radius: 999px;
        color: white;
        cursor: pointer;
        font-size: 15px;
        margin: 4px 0 12px;
        padding: 9px 18px;
      }}
      button:hover {{
        background: #111827;
      }}
      textarea {{
        box-sizing: border-box;
        width: 100%;
        min-height: 260px;
        border: 1px solid #ded2c0;
        border-radius: 10px;
        color: #211b16;
        font: 15px/1.75 "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        padding: 14px;
        resize: vertical;
        white-space: pre-wrap;
      }}
      #toast {{
        position: fixed;
        right: 24px;
        bottom: 24px;
        background: #1f2933;
        border-radius: 999px;
        color: #fff;
        opacity: 0;
        padding: 10px 18px;
        transition: opacity 160ms ease;
      }}
      #toast.show {{
        opacity: 1;
      }}
    </style>
  </head>
  <body>
    <h1>我给中本聪送外卖：番茄复制页</h1>
    <p class="summary">打开本文件后，点击按钮即可复制对应章节纯文本。不会登录平台，不会自动发布。</p>

    <section class="card">
      <div class="card-head">
        <h2>整本合并稿</h2>
        <span>{sum(chapter.body_chars for chapter in chapters)} 字符</span>
      </div>
      <button type="button" data-copy-target="all-chapters">复制全部</button>
      <textarea id="all-chapters" readonly>{html.escape(all_text)}</textarea>
    </section>

    {chr(10).join(chapter_cards)}

    <div id="toast">已复制</div>

    <script>
      async function copyText(id) {{
        const target = document.getElementById(id)
        target.focus()
        target.select()

        try {{
          await navigator.clipboard.writeText(target.value)
        }} catch (error) {{
          document.execCommand('copy')
        }}

        const toast = document.getElementById('toast')
        toast.classList.add('show')
        setTimeout(() => toast.classList.remove('show'), 1300)
      }}

      document.querySelectorAll('[data-copy-target]').forEach((button) => {{
        button.addEventListener('click', () => copyText(button.dataset.copyTarget))
      }})
    </script>
  </body>
</html>"""
    write_text(output_dir / "copy.html", text)


def write_readme(
    output_dir: Path,
    chapters: list[ChapterExport],
    target_initial_chars: int,
) -> None:
    total_body_chars = sum(chapter.body_chars for chapter in chapters)
    risk_lines = []
    for chapter in chapters:
        if chapter.risk_terms:
            terms = "、".join(chapter.risk_terms)
            risk_lines.append(f"- {chapter.title}：{terms}")

    if not risk_lines:
        risk_lines.append("- 未命中本地风险词。")

    status = "是" if total_body_chars >= target_initial_chars else "否"
    chapter_lines = [
        f"- {chapter.title}：{chapter.body_chars} 字符，`{chapter.output}`"
        for chapter in chapters
    ]

    text = f"""# 番茄发布复制包

本目录由 `scripts/export_fanqie_delivery.py` 自动生成，供人工复制到番茄作者后台使用。

## 汇总

- 作品：我给中本聪送外卖
- 章节数：{len(chapters)}
- 正文字符数：{total_body_chars}
- 初始投稿准备线：{target_initial_chars}
- 是否达到准备线：{status}
- AI 辅助写作：是，后台如询问请按平台规则如实选择

## 章节

{chr(10).join(chapter_lines)}

## 可复制文件

- `copy.html`：本地一键复制页面，打开后可复制单章或整本
- `all_chapters.txt`：整本合并纯文本
- `chapters/*.txt`：一章一份纯文本，第一行是章节标题

## 发布前人工复核词

{chr(10).join(risk_lines)}

## 安全流程

1. 先在番茄作者后台手动创建作品，确认书名、分类、简介、封面和 AI/版权条款。
2. 打开 `copy.html`，点击对应章节的“复制本章”。
3. 粘贴到番茄作者后台编辑器。
4. 人工确认标题、正文、是否使用 AI、定时发布时间后再发布。
5. 发布后自行记录后台状态，避免重复发章。
"""
    write_text(output_dir / "README.md", text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export delivery novel chapters for Fanqie publishing."
    )
    parser.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--target-initial-chars",
        type=int,
        default=20000,
        help="Local readiness threshold for first submission checks.",
    )
    parser.add_argument("--clean", action="store_true", help="Remove old export dir first.")
    parser.add_argument("--dry-run", action="store_true", help="Print report only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_dir = project_path(args.source_dir)
    output_dir = project_path(args.output_dir)
    chapters_dir = output_dir / "chapters"

    files = chapter_files(source_dir)
    if not files:
        raise SystemExit(f"No numbered Markdown chapters found in {source_dir}")

    if args.dry_run:
        for number, path in files:
            title, body = extract_heading_and_body(read_text(path), path.stem)
            print(f"{number:03d} {normalize_title(title)} {compact_char_count(clean_body(body))}")
        return 0

    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)

    chapters_dir.mkdir(parents=True, exist_ok=True)
    exported = [export_chapter(number, path, chapters_dir) for number, path in files]
    write_combined_text(output_dir, exported)
    write_copy_page(output_dir, exported)
    write_manifest(output_dir, exported, args.target_initial_chars)
    write_readme(output_dir, exported, args.target_initial_chars)

    total_body_chars = sum(chapter.body_chars for chapter in exported)
    print(f"exported chapters: {len(exported)}")
    print(f"total body chars: {total_body_chars}")
    print(f"output dir: {output_dir}")
    if total_body_chars < args.target_initial_chars:
        print(
            "readiness: below initial submission threshold "
            f"({total_body_chars}/{args.target_initial_chars})"
        )
    else:
        print("readiness: initial submission threshold reached")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
