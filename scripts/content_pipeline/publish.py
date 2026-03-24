"""
Publish helper — updates feed.xml, sitemap.xml, and image placeholders.

zh/ 章节构建由 build_zh.py 处理，本模块只负责周边资产更新。

Usage:
    python -m scripts.content_pipeline.cli sync 5
    python -m scripts.content_pipeline.cli sync 5 --commit
"""

import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

from . import config


def update_en_summary(chapter_num: int, filename: str, title: str):
    """Update en/SUMMARY.md with a new or updated entry."""
    summary_path = config.MAIN_EN_SUMMARY
    if not summary_path.exists():
        print(f"  Warning: {summary_path} not found, skipping")
        return

    content = summary_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    entry_pattern = re.compile(rf"^\* \[.*\]\({re.escape(filename)}\)$")
    new_entry = f"* [{title}]({filename})"

    for i, line in enumerate(lines):
        if entry_pattern.match(line.strip()):
            lines[i] = new_entry
            summary_path.write_text("\n".join(lines), encoding="utf-8")
            print(f"  Updated en/SUMMARY.md entry for ch{chapter_num:02d}")
            return

    # 找正确的插入位置
    last_lower_idx = -1
    for i, line in enumerate(lines):
        match = re.match(r"^\* \[.*\]\((\d+)_", line.strip())
        if match:
            existing_num = int(match.group(1))
            if existing_num < chapter_num:
                last_lower_idx = i

    if last_lower_idx >= 0:
        lines.insert(last_lower_idx + 1, new_entry)
    else:
        lines.append(new_entry)
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Added en/SUMMARY.md entry for ch{chapter_num:02d}")


def update_feed_xml(chapter_num: int, zh_title: str, en_title: str, zh_filename: str):
    """Add a new item to the RSS feed.xml."""
    feed_path = config.MAIN_FEED_XML
    if not feed_path.exists():
        print(f"  Warning: {feed_path} not found, skipping")
        return

    content = feed_path.read_text(encoding="utf-8")

    if zh_filename.replace(".md", ".html") in content:
        print(f"  feed.xml already contains ch{chapter_num:02d}")
        return

    html_name = zh_filename.replace(".md", ".html")
    encoded_name = quote(html_name, safe="")
    url = f"{config.SITE_BASE}/zh/{encoded_name}"

    new_item = f"""    <item>
      <title>{zh_title} | {en_title}</title>
      <link>{url}</link>
      <description>第{chapter_num}章 — {zh_title}</description>
      <guid isPermaLink="true">{url}</guid>
    </item>"""

    content = content.replace("  </channel>", f"{new_item}\n  </channel>")
    feed_path.write_text(content, encoding="utf-8")
    print(f"  Updated feed.xml with ch{chapter_num:02d}")


def update_sitemap_xml(chapter_num: int, zh_filename: str, en_filename: str):
    """Add chapter URLs to sitemap.xml."""
    sitemap_path = config.MAIN_SITEMAP_XML
    if not sitemap_path.exists():
        print(f"  Warning: {sitemap_path} not found, skipping")
        return

    content = sitemap_path.read_text(encoding="utf-8")

    zh_html = zh_filename.replace(".md", ".html")
    en_html = en_filename.replace(".md", ".html")

    if zh_html in content:
        print(f"  sitemap.xml already contains ch{chapter_num:02d}")
        return

    zh_url = f"{config.SITE_BASE}/zh/{zh_html}"
    en_url = f"{config.SITE_BASE}/en/{en_html}"

    new_entries = f"""  <url>
    <loc>{zh_url}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>{en_url}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>"""

    content = content.replace("</urlset>", f"{new_entries}\n</urlset>")
    sitemap_path.write_text(content, encoding="utf-8")
    print(f"  Updated sitemap.xml with ch{chapter_num:02d}")


def ensure_image_placeholder(chapter_num: int):
    """Create a placeholder image if none exists for this chapter."""
    img_name = f"{chapter_num:02d}.png"
    img_path = config.MAIN_IMG_DIR / img_name

    if img_path.exists():
        return

    print(f"  Warning: {img_path} not found, creating placeholder...")

    for offset in range(1, 5):
        for neighbor in (chapter_num - offset, chapter_num + offset):
            neighbor_path = config.MAIN_IMG_DIR / f"{neighbor:02d}.png"
            if neighbor_path.exists():
                shutil.copy2(neighbor_path, img_path)
                print(f"  Created placeholder img/{img_name} (from {neighbor:02d}.png)")
                _generate_image_variants(img_name)
                return

    print(f"  Could not create placeholder for img/{img_name}")


def _generate_image_variants(img_name: str):
    """Generate 800px and WebP variants of an image."""
    img_path = config.MAIN_IMG_DIR / img_name
    img_800_path = config.MAIN_IMG_800_DIR / img_name
    webp_name = img_name.replace(".png", ".webp")
    img_webp_path = config.MAIN_IMG_WEBP_DIR / webp_name

    if not img_800_path.exists():
        try:
            subprocess.run(
                ["sips", "-Z", "800", str(img_path), "--out", str(img_800_path)],
                capture_output=True, check=True,
            )
            print(f"  Generated img_800px/{img_name}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  Warning: Could not generate 800px variant")

    if not img_webp_path.exists():
        try:
            subprocess.run(
                ["cwebp", "-q", "80", str(img_path), "-o", str(img_webp_path)],
                capture_output=True, check=True,
            )
            print(f"  Generated img_webp/{webp_name}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  Warning: Could not generate WebP variant")


def publish_chapter(
    chapter_num: int,
    en_text: str | None,
    en_filename: str,
    zh_filename: str,
    zh_title: str,
    en_title: str,
    commit: bool = False,
):
    """
    Publish a chapter: sync en/ (if provided), update feed/sitemap, ensure images.
    zh/ is built separately by build_zh.py.
    """
    print(f"\nPublishing chapter {chapter_num:02d}...")

    # 1. Sync English if provided
    if en_text:
        dest = config.MAIN_EN_DIR / en_filename
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(en_text, encoding="utf-8")
        print(f"  Synced en/{en_filename}")
        update_en_summary(chapter_num, en_filename, en_title)

    # 2. Update feed.xml
    update_feed_xml(chapter_num, zh_title, en_title, zh_filename)

    # 3. Update sitemap.xml
    update_sitemap_xml(chapter_num, zh_filename, en_filename)

    # 4. Ensure image exists
    ensure_image_placeholder(chapter_num)

    print(f"  Publish complete for ch{chapter_num:02d}")

    # 5. Optional git commit
    if commit:
        repo_dir = str(config.PROJECT_ROOT)
        try:
            subprocess.run(
                ["git", "add", "-A"],
                cwd=repo_dir, capture_output=True, check=True,
            )
            msg = f"Publish chapter {chapter_num:02d}: {zh_title}"
            subprocess.run(
                ["git", "commit", "-m", msg],
                cwd=repo_dir, capture_output=True, check=True,
            )
            print(f"  Git commit created: {msg}")
        except subprocess.CalledProcessError as e:
            print(f"  Git commit failed: {e.stderr.decode() if e.stderr else e}")
