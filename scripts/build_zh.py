#!/usr/bin/env python3
"""
构建 zh/ 目录：从 正文/ 复制章节，追加捐赠块，生成 SUMMARY.md。

正文/ 是唯一的 source of truth，zh/ 是构建产物（HonKit 用）。

用法:
    python3 scripts/build_zh.py           # 完整构建
    python3 scripts/build_zh.py --dry-run # 预览，不写文件
"""

import argparse
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CHAPTERS_DIR = REPO_ROOT / "正文"
ZH_DIR = REPO_ROOT / "zh"
TEMPLATE_DIR = Path(__file__).parent / "templates"
DONATION_BLOCK_FILE = TEMPLATE_DIR / "donation_block.html"

# SUMMARY.md 的分组结构（7 篇 + 特别篇）
PERIOD_CONFIG = [
    {
        "emoji": "🌟",
        "title": "序言",
        "range": (0, 0),
    },
    {
        "emoji": "🔮",
        "title": "创世纪篇 (1976-2009)",
        "range": (1, 3),
    },
    {
        "emoji": "👤",
        "title": "初出茅庐篇 (2009-2010)",
        "range": (4, 8),
    },
    {
        "emoji": "🌪️",
        "title": "风起云涌篇 (2011-2012)",
        "range": (9, 13),
    },
    {
        "emoji": "🌊",
        "title": "暗潮汹涌篇 (2013-2016)",
        "range": (14, 19),
    },
    {
        "emoji": "⚔️",
        "title": "内战与独立篇 (2017)",
        "range": (20, 22),
    },
    {
        "emoji": "🏛️",
        "title": "西装革命篇 (2018-2021)",
        "range": (23, 26),
    },
    {
        "emoji": "🚀",
        "title": "未来可期篇 (2021-2025)",
        "range": (27, 34),
    },
]


def load_donation_block() -> str:
    """加载捐赠块模板"""
    if DONATION_BLOCK_FILE.exists():
        return DONATION_BLOCK_FILE.read_text(encoding="utf-8")
    print(f"  Warning: {DONATION_BLOCK_FILE} not found, skipping donation block")
    return ""


def has_donation_block(content: str) -> bool:
    """检查内容是否已包含捐赠块"""
    return "latebrook396888@getalby.com" in content


def find_chapters() -> list[tuple[int | None, str, Path]]:
    """
    扫描 正文/ 下的 md 文件，返回 (章节号, 标题, 路径) 列表。
    章节号为 None 表示特别篇等非编号章节。
    """
    chapters = []
    for f in sorted(CHAPTERS_DIR.glob("*.md")):
        if "历史版本" in str(f) or f.name == "README.md":
            continue
        # 尝试提取编号
        m = re.match(r"(\d+)_(.*?)\.md", f.name)
        if m:
            num = int(m.group(1))
            title = m.group(2)
            chapters.append((num, title, f))
        elif f.name.startswith("特别篇"):
            # 特别篇无编号
            title = f.stem
            chapters.append((None, title, f))
    return chapters


def build_chapter_file(src: Path, donation_block: str) -> str:
    """读取章节源文件，追加捐赠块（如果尚未包含）"""
    content = src.read_text(encoding="utf-8")
    if not has_donation_block(content):
        content = content.rstrip() + "\n\n" + donation_block
    return content


def build_summary(chapters: list[tuple[int | None, str, Path]]) -> str:
    """生成 SUMMARY.md"""
    lines = ["# 比特币那些事儿", "", "* [关于这本书](INTRO.md)", ""]

    # 按编号分组
    numbered = {num: (title, f) for num, title, f in chapters if num is not None}
    specials = [(title, f) for num, title, f in chapters if num is None]

    for period in PERIOD_CONFIG:
        lo, hi = period["range"]
        lines.append("---")
        lines.append("")
        lines.append(f"## {period['emoji']} {period['title']}")

        for n in range(lo, hi + 1):
            if n in numbered:
                title, f = numbered[n]
                lines.append(f"* [{title}]({f.name})")

        lines.append("")

    # 特别篇
    if specials:
        lines.append("---")
        lines.append("")
        lines.append("## 📖 特别篇")
        for title, f in specials:
            lines.append(f"* [{title}]({f.name})")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="从 正文/ 构建 zh/ 目录")
    parser.add_argument("--dry-run", action="store_true", help="预览，不写文件")
    args = parser.parse_args()

    chapters = find_chapters()
    print(f"Found {len(chapters)} chapters in 正文/")

    donation_block = load_donation_block()

    # 清理 zh/ 中旧的构建产物（仅删除章节 md 和 SUMMARY.md）
    if not args.dry_run:
        for f in ZH_DIR.glob("*.md"):
            # 保留 INTRO.md, README.md（HonKit 静态配置）
            if f.name in ("INTRO.md", "README.md"):
                continue
            f.unlink()
            print(f"  Cleaned: zh/{f.name}")

    # 复制章节到 zh/
    count = 0
    for num, title, src in chapters:
        dest = ZH_DIR / src.name
        content = build_chapter_file(src, donation_block)

        if args.dry_run:
            print(f"  [DRY RUN] Would write: zh/{src.name} ({len(content)} chars)")
        else:
            dest.write_text(content, encoding="utf-8")
            print(f"  Built: zh/{src.name}")
        count += 1

    # 生成 SUMMARY.md
    summary = build_summary(chapters)
    summary_path = ZH_DIR / "SUMMARY.md"
    if args.dry_run:
        print(f"  [DRY RUN] Would write: zh/SUMMARY.md ({len(summary)} chars)")
    else:
        summary_path.write_text(summary, encoding="utf-8")
        print(f"  Built: zh/SUMMARY.md")

    print(f"\nDone: {count} chapters + SUMMARY.md")


if __name__ == "__main__":
    main()
