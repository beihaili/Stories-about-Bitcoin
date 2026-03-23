#!/usr/bin/env python3
"""
电子书构建脚本 v2
支持两种引擎：
  - honkit: HonKit → EPUB → Calibre PDF（快速，排版一般）
  - pandoc: Pandoc + XeLaTeX（慢，排版专业）

用法：
  python3 scripts/build_ebook.py zh              # 默认 pandoc 引擎
  python3 scripts/build_ebook.py zh --honkit     # HonKit 引擎
  python3 scripts/build_ebook.py zh en           # 双语
"""

import os
import re
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
XELATEX = "/usr/local/texlive/2026/bin/universal-darwin/xelatex"


def clean_chapter(content: str, lang: str = "zh") -> str:
    """清理单个章节的网页专属元素"""

    # 1. 删除 shields.io 徽章行
    content = re.sub(r'!\[(?:status|author|date|difficulty)\]\(.*?shields\.io.*?\)\n?', '', content)
    content = re.sub(r'!\[(?:status|author|date|difficulty)\]\(https://img\.shields\.io/.*?\)\n?', '', content)

    # 2. 删除所有配图/图片标签
    content = re.sub(r'!\[配图\]\(.*?\)\n?', '', content)
    content = re.sub(r'!\[.*?配图.*?\]\(.*?\)\n?', '', content)
    content = re.sub(r'^!\[.*?\]\(\.\./img.*?\)\s*$', '', content, flags=re.MULTILINE)

    # 3. 删除 HTML 图片块
    content = re.sub(r'<picture>.*?</picture>\n?', '', content, flags=re.DOTALL)
    content = re.sub(r'<img\s+src="\.\.?/img.*?>\n?', '', content)

    # 4. 删除 > 💡 引言块（包含社交链接的整个 blockquote）
    content = re.sub(
        r'^> 💡.*?(?=\n[^>]|\n\n[^>]|\Z)',
        '', content, flags=re.MULTILINE | re.DOTALL
    )

    # 5. 删除社交链接 blockquote 残留
    content = re.sub(r'^>\s*欢迎关注.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*进入微信.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*文章开源.*?\n', '', content, flags=re.MULTILINE)
    # 清理只有 > 的空引用行（但保留有内容的引用）
    content = re.sub(r'^>\s*$\n', '', content, flags=re.MULTILINE)

    # 6. 删除捐赠块
    content = re.sub(
        r'<div align="center"[^>]*style="[^"]*border.*?f7931a.*?</div>',
        '', content, flags=re.DOTALL
    )

    # 7. 删除页脚导航链接块
    content = re.sub(
        r'<div align="center">\s*\n.*?(?:返回主页|Return to Homepage).*?</div>',
        '', content, flags=re.DOTALL
    )

    # 8. 删除其他 HTML 残留
    content = re.sub(r'<div align="center">\s*</div>', '', content)

    # 9. 删除所有 emoji（宋体无法渲染，会变成小方框）及其后的多余空格
    content = re.sub(
        '['
        '\U0001F300-\U0001F9FF'   # Emoticons, Misc Symbols, Supplemental
        '\U00002702-\U000027B0'   # Dingbats
        '\U0001FA00-\U0001FAFF'   # Symbols extended
        '\U00002600-\U000026FF'   # Misc symbols (⚡⚠ etc)
        '\U000023F0-\U000023FF'   # Misc technical (⏰ etc)
        '\U00002705'              # ✅
        '\U0000270D'              # ✍
        '\U0000FE0F'              # Variation selector
        ']+ *',                   # 吃掉 emoji 后的空格
        '',
        content
    )

    # 10. 将 Markdown 水平线 --- 替换为 Pandoc raw LaTeX 三星号
    ASTERISK_BREAK = '\n\n```{=latex}\n\\medskip\n\\begin{center}\n*\\quad\\quad *\\quad\\quad *\n\\end{center}\n\\medskip\n```\n\n'
    content = re.sub(r'\n---\s*\n', lambda m: ASTERISK_BREAK, content)

    # 11. 清理多余空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = re.sub(r'^(#[^\n]+\n)\n{2,}', r'\1\n', content)

    return content.strip() + '\n'


def parse_summary(summary_path: Path) -> list[str]:
    """从 SUMMARY.md 解析章节文件顺序"""
    content = summary_path.read_text(encoding="utf-8")
    files = []
    for match in re.finditer(r'\[.*?\]\((.+?\.md)\)', content):
        fname = match.group(1)
        if fname not in ("README.md",):
            files.append(fname)
    return files


def build_pandoc_pdf(lang: str = "zh"):
    """用 Pandoc + XeLaTeX 构建专业排版的 PDF"""
    src_dir = REPO_ROOT / lang
    ebook_dir = REPO_ROOT / "ebook"
    ebook_dir.mkdir(exist_ok=True)

    metadata_file = ebook_dir / f"metadata-{lang}.yaml"
    preamble_file = ebook_dir / f"preamble-{lang}.tex"
    if not metadata_file.exists():
        print(f"错误：找不到 {metadata_file}")
        return False
    if not preamble_file.exists():
        print(f"错误：找不到 {preamble_file}")
        return False

    if lang == "zh":
        pdf_out = ebook_dir / "比特币那些事儿.pdf"
    else:
        pdf_out = ebook_dir / "Stories-about-Bitcoin.pdf"

    # 获取章节顺序
    chapter_files = parse_summary(src_dir / "SUMMARY.md")
    print(f"[{lang}] 找到 {len(chapter_files)} 个章节")

    # 创建临时工作目录
    with tempfile.TemporaryDirectory(prefix="ebook-pandoc-") as tmp:
        tmp_dir = Path(tmp)

        # 清理并复制章节文件
        cleaned_files = []
        for fname in chapter_files:
            src_file = src_dir / fname
            if not src_file.exists():
                print(f"  跳过（不存在）: {fname}")
                continue

            content = src_file.read_text(encoding="utf-8")

            if fname == "INTRO.md":
                # 前言页：不用标题（标题页已有），改为"前言"
                if lang == "zh":
                    content = "# 前言\n\n" + _preface_zh()
                else:
                    content = "# Preface\n\n" + _preface_en()
            else:
                content = clean_chapter(content, lang)

            out_file = tmp_dir / fname
            out_file.write_text(content, encoding="utf-8")
            cleaned_files.append(str(out_file))

        if not cleaned_files:
            print("错误：没有可用的章节文件")
            return False

        # 构建 Pandoc 命令
        pandoc_cmd = [
            "pandoc",
            f"--metadata-file={metadata_file}",
            f"--include-in-header={preamble_file}",
            f"--pdf-engine={XELATEX}",
            "--top-level-division=chapter",
            f"--resource-path={src_dir}:{REPO_ROOT}",
            "--toc",
            "--toc-depth=1",
            "-o", str(pdf_out),
        ] + cleaned_files

        print(f"[{lang}] 正在用 Pandoc + XeLaTeX 生成 PDF...")
        print(f"  文件数: {len(cleaned_files)}")

        result = subprocess.run(
            pandoc_cmd, capture_output=True, text=True,
            env={**os.environ, "PATH": f"/usr/local/texlive/2026/bin/universal-darwin:{os.environ.get('PATH', '')}"}
        )

        if result.returncode != 0:
            print(f"PDF 生成失败:")
            # 显示关键错误行（过滤掉 LaTeX 的冗长日志）
            for line in result.stderr.split('\n'):
                if 'error' in line.lower() or 'fatal' in line.lower() or '!' in line[:3]:
                    print(f"  {line}")
            # 显示最后 20 行作为上下文
            stderr_lines = result.stderr.strip().split('\n')
            if len(stderr_lines) > 20:
                print(f"\n  ... 最后 20 行日志:")
                for line in stderr_lines[-20:]:
                    print(f"  {line}")
            return False

        size_mb = pdf_out.stat().st_size / 1024 / 1024
        print(f"[{lang}] PDF: {pdf_out} ({size_mb:.1f}MB)")

    return True


def build_honkit_epub(lang: str = "zh"):
    """用 HonKit 生成 EPUB"""
    src_dir = REPO_ROOT / lang
    ebook_dir = REPO_ROOT / "ebook"
    ebook_dir.mkdir(exist_ok=True)

    if lang == "zh":
        epub_out = ebook_dir / "比特币那些事儿.epub"
        title = "比特币那些事儿"
    else:
        epub_out = ebook_dir / "Stories-about-Bitcoin.epub"
        title = "Stories about Bitcoin"

    with tempfile.TemporaryDirectory(prefix="ebook-epub-") as tmp:
        tmp_dir = Path(tmp)

        for f in src_dir.glob("*.md"):
            if f.name == "README.md":
                continue
            content = f.read_text(encoding="utf-8")
            if f.name == "INTRO.md":
                content = f"# {title}\n\n" + (_preface_zh() if lang == "zh" else _preface_en())
            elif f.name != "SUMMARY.md":
                content = clean_chapter(content, lang)
            (tmp_dir / f.name).write_text(content, encoding="utf-8")

        # 扁平化 SUMMARY.md
        summary = (src_dir / "SUMMARY.md").read_text(encoding="utf-8")
        summary = re.sub(r'^##\s+.*$', '', summary, flags=re.MULTILINE)
        summary = re.sub(r'^---\s*$', '', summary, flags=re.MULTILINE)
        summary = re.sub(r'\n{3,}', '\n\n', summary)
        (tmp_dir / "SUMMARY.md").write_text(summary.strip() + '\n', encoding="utf-8")

        book_config = {
            "title": title,
            "author": "beihaili",
            "language": "zh-hans" if lang == "zh" else "en",
            "structure": {"readme": "INTRO.md"},
        }
        (tmp_dir / "book.json").write_text(json.dumps(book_config, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"[{lang}] 生成 EPUB...")
        result = subprocess.run(["honkit", "epub", str(tmp_dir), str(epub_out)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"EPUB 生成失败:\n{result.stderr}")
            return False
        print(f"[{lang}] EPUB: {epub_out} ({epub_out.stat().st_size // 1024}KB)")

    return True


def _preface_zh() -> str:
    return """这是一部讲述比特币历史的作品。从1976年哈耶克写下《货币的非国家化》，到2025年比特币突破十万美元——我们用故事的方式，记录这场持续半个世纪的货币革命。

33个章节，覆盖密码朋克的理想、中本聪的创世、丝绸之路的争议、Mt.Gox的崩塌、扩容战争的撕裂、ETF的突破，以及战略储备的诞生。

每一个章节都是一段真实的历史，每一个人物都有名有姓。

> *"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"*
>
> ——创世区块，2009年1月3日
"""


def _preface_en() -> str:
    return """This is a chronicle of Bitcoin's history. From Hayek's *Denationalization of Money* in 1976 to Bitcoin breaking $100,000 in 2025 — we tell this half-century monetary revolution through stories.

33 chapters covering the Cypherpunk dream, Satoshi's genesis, the Silk Road controversy, Mt. Gox's collapse, the Scaling Wars, the ETF breakthrough, and the birth of the Strategic Bitcoin Reserve.

Every chapter is real history. Every character has a name.

> *"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"*
>
> — Genesis Block, January 3, 2009
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]

    langs = args if args else ["zh", "en"]
    use_honkit = "--honkit" in flags

    for lang in langs:
        print(f"\n{'='*50}")
        print(f"构建 {lang} 电子书")
        print(f"{'='*50}")

        if use_honkit:
            build_honkit_epub(lang)
        else:
            # Pandoc PDF + HonKit EPUB
            build_pandoc_pdf(lang)
            build_honkit_epub(lang)

    print("\n✅ 完成！文件在 ebook/ 目录")


if __name__ == "__main__":
    main()
