#!/usr/bin/env python3
"""
电子书构建脚本 v3
支持两种引擎：
  - pandoc: Pandoc + XeLaTeX（排版专业，默认）
  - honkit: HonKit → EPUB（快速）

用法：
  python3 scripts/build_ebook.py zh              # 中文完整版 PDF+EPUB
  python3 scripts/build_ebook.py en              # 英文完整版 PDF+EPUB
  python3 scripts/build_ebook.py zh en           # 双语
  python3 scripts/build_ebook.py zh --sample     # 中文试读版
  python3 scripts/build_ebook.py zh --honkit     # 仅 EPUB
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

# 试读版章节（精彩篇章）
SAMPLE_CHAPTERS_ZH = [
    "00_引子：一束照进现实的理想之光.md",
    "01_创世纪：预言与失败.md",
    "02_创世纪：密码朋克的技术拼图.md",
    "03_创世纪：危机与创世.md",
    "06_初出茅庐：价值发现.md",  # 披萨日
]
SAMPLE_CHAPTERS_EN = [
    "00_prologue_a_beam_of_idealistic_light.md",
    "01_genesis_prophecy_and_failure.md",
    "02_genesis_the_cypherpunk_technical_puzzle.md",
    "03_genesis_crisis_and_creation.md",
    "06_first_steps_value_discovery.md",
]

# 图片编号映射（章节文件名前缀 → 图片文件名）
def get_chapter_image(fname: str) -> str | None:
    """根据章节文件名推断配图路径"""
    m = re.match(r'^(\d+)_', fname)
    if m:
        num = int(m.group(1))
        img_path = REPO_ROOT / "img" / f"{num:02d}.png"
        if img_path.exists():
            return str(img_path)
    if fname.startswith("特别篇") or fname.startswith("special"):
        img_path = REPO_ROOT / "img" / "special_kirk.png"
        if img_path.exists():
            return str(img_path)
    return None


def _clean_common(content: str) -> str:
    """通用清理：删除网页专属元素（PDF 和 EPUB 共用）"""

    # 删除 shields.io 徽章
    content = re.sub(r'!\[(?:status|author|date|difficulty)\]\(.*?shields\.io.*?\)\n?', '', content)
    content = re.sub(r'!\[(?:status|author|date|difficulty)\]\(https://img\.shields\.io/.*?\)\n?', '', content)

    # 删除图片标签（PDF 由 inject_chapter_image 统一注入）
    content = re.sub(r'!\[配图\]\(.*?\)\n?', '', content)
    content = re.sub(r'!\[.*?配图.*?\]\(.*?\)\n?', '', content)
    content = re.sub(r'^!\[.*?\]\(\.\./img.*?\)\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^!\[.*?\]\(img/.*?\)\s*$', '', content, flags=re.MULTILINE)
    # 英文章节也可能有 cover 图
    content = re.sub(r'^!\[cover\]\(.*?\)\s*$', '', content, flags=re.MULTILINE)

    # 删除 HTML 图片块
    content = re.sub(r'<picture>.*?</picture>\n?', '', content, flags=re.DOTALL)
    content = re.sub(r'<img\s+src="\.\.?/img.*?>\n?', '', content)

    # 删除 > 💡 引言块（含社交链接）
    content = re.sub(
        r'^> 💡.*?(?=\n[^>]|\n\n[^>]|\Z)',
        '', content, flags=re.MULTILINE | re.DOTALL
    )

    # 删除社交链接残留
    content = re.sub(r'^>\s*欢迎关注.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*进入微信.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*文章开源.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*$\n', '', content, flags=re.MULTILINE)

    # 删除捐赠块
    content = re.sub(
        r'<div align="center"[^>]*style="[^"]*border.*?f7931a.*?</div>',
        '', content, flags=re.DOTALL
    )

    # 删除页脚导航
    content = re.sub(
        r'<div align="center">\s*\n.*?(?:返回主页|Return to Homepage|关注作者).*?</div>',
        '', content, flags=re.DOTALL
    )
    content = re.sub(r'<div align="center">\s*</div>', '', content)

    # 删除 emoji（宋体无法渲染）
    content = re.sub(
        '['
        '\U0001F300-\U0001F9FF'
        '\U00002702-\U000027B0'
        '\U0001FA00-\U0001FAFF'
        '\U00002600-\U000026FF'
        '\U000023F0-\U000023FF'
        '\U00002705'
        '\U0000270D'
        '\U0000FE0F'
        ']+ *',
        '',
        content
    )

    # 清理多余空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = re.sub(r'^(#[^\n]+\n)\n{2,}', r'\1\n', content)

    return content


def _merge_short_paragraphs(content: str, max_len: int = 35) -> str:
    """合并连续的短段落，减少 PDF 中过多缩进导致的碎片感。

    规则：
    - 连续 2+ 个纯文本短段落（< max_len 字符）合并为一段
    - 不合并：标题行(#)、引用(>)、列表(- *)、LaTeX代码块、空行后的长段落
    - 保留独立的短段落（前后都是长段落或特殊行）
    """
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 跳过特殊行（标题、引用、列表、代码、空行）
        if (not line.strip() or
            line.startswith('#') or
            line.startswith('>') or
            line.startswith('- ') or
            line.startswith('* ') or
            line.startswith('```') or
            line.startswith('\\') or
            '```{=latex}' in line):
            result.append(line)
            i += 1
            continue

        # 当前是普通文本行，检查是否是短段落的开始
        stripped = line.strip()
        if len(stripped) > max_len:
            result.append(line)
            i += 1
            continue

        # 短段落：往后看，收集连续的短段落
        batch = [stripped]
        j = i + 1

        while j < len(lines):
            # 期望下一行是空行（段落分隔）
            if j < len(lines) and lines[j].strip() == '':
                # 再下一行是否也是短段落？
                if j + 1 < len(lines):
                    next_line = lines[j + 1].strip()
                    if (next_line and
                        len(next_line) <= max_len and
                        not next_line.startswith('#') and
                        not next_line.startswith('>') and
                        not next_line.startswith('- ') and
                        not next_line.startswith('* ') and
                        not next_line.startswith('```')):
                        batch.append(next_line)
                        j += 2  # 跳过空行和下一段
                        continue
            break

        # 只有 2+ 个短段落才合并
        if len(batch) >= 2:
            result.append(''.join(batch))
        else:
            result.append(line)

        i = j

    return '\n'.join(result)


def clean_for_pdf(content: str, lang: str = "zh") -> str:
    """PDF 专用清理：注入 LaTeX 代码"""
    content = _clean_common(content)

    # 合并连续短段落（减少碎片感）
    content = _merge_short_paragraphs(content)

    # 替换宋体不支持的特殊符号
    content = content.replace('→', ' -- ')
    content = content.replace('×', 'x')
    content = content.replace('≈', '约等于')

    # 检测章末趣闻 → funfact LaTeX 环境
    parts = re.split(r'\n---\s*\n', content)
    funfact_idx = None
    for i in range(len(parts) - 1, -1, -1):
        if parts[i].strip():
            if parts[i].strip().startswith('*') and parts[i].strip().endswith('*') and '##' not in parts[i]:
                funfact_idx = i
            break

    if funfact_idx is not None and funfact_idx > 0:
        fun_fact_text = parts[funfact_idx].strip()[1:-1].strip()
        fun_fact_latex = (
            '\n\n```{=latex}\n'
            '\\begin{funfact}\n'
            '```\n\n'
            + fun_fact_text +
            '\n\n```{=latex}\n'
            '\\end{funfact}\n'
            '```\n'
        )
        content = '\n---\n'.join(parts[:funfact_idx]) + fun_fact_latex

    # 水平线 → LaTeX 小间隔（不要太大，避免段落松散）
    SECTION_BREAK = '\n\n```{=latex}\n\\vspace{0.6em}\n```\n\n'
    content = re.sub(r'\n---\s*\n', lambda m: SECTION_BREAK, content)

    return content.strip() + '\n'


def clean_for_epub(content: str, lang: str = "zh") -> str:
    """EPUB 专用清理：不注入任何 LaTeX 代码"""
    content = _clean_common(content)

    # 趣闻保留为斜体（markdown 原样），不包装 LaTeX 环境
    # 水平线保留为 ---（HonKit 原生支持）
    # 不替换特殊符号（EPUB 字体支持更广）

    return content.strip() + '\n'


def inject_chapter_image(content: str, fname: str, with_images: bool = True) -> str:
    """在章节标题后插入配图（无 caption，无编号）"""
    if not with_images:
        return content

    img_path = get_chapter_image(fname)
    if not img_path:
        return content

    # 找到第一个 # 标题行，在其后插入图片
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('# '):
            img_latex = (
                '\n\n```{=latex}\n'
                '\\begin{center}\n'
                f'\\includegraphics[width=0.85\\textwidth]{{{img_path}}}\n'
                '\\end{center}\n'
                '\\vspace{0.5em}\n'
                '```\n'
            )
            lines.insert(i + 1, img_latex)
            break

    return '\n'.join(lines)


def get_source_dir(lang: str) -> Path:
    """获取章节源目录"""
    if lang == "zh":
        return REPO_ROOT / "正文"
    return REPO_ROOT / "en"


def get_chapter_files(src_dir: Path, lang: str) -> list[str]:
    """获取章节文件列表（排序）"""
    return sorted([
        f.name for f in src_dir.glob("*.md")
        if f.name not in ("README.md", "INTRO.md", "SUMMARY.md")
        and not f.name.startswith(".")
    ])


def build_pandoc_pdf(lang: str = "zh", sample: bool = False):
    """用 Pandoc + XeLaTeX 构建 PDF"""
    src_dir = get_source_dir(lang)
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

    if sample:
        if lang == "zh":
            pdf_out = ebook_dir / "Bitcoin-Stories-ZH-Sample.pdf"
            chapter_filter = set(SAMPLE_CHAPTERS_ZH)
        else:
            pdf_out = ebook_dir / "Bitcoin-Stories-EN-Sample.pdf"
            chapter_filter = set(SAMPLE_CHAPTERS_EN)
    else:
        if lang == "zh":
            pdf_out = ebook_dir / "比特币那些事儿.pdf"
        else:
            pdf_out = ebook_dir / "Stories-about-Bitcoin.pdf"
        chapter_filter = None

    chapter_files = get_chapter_files(src_dir, lang)
    if chapter_filter:
        chapter_files = [f for f in chapter_files if f in chapter_filter]

    print(f"[{lang}] 源目录: {src_dir}")
    print(f"[{lang}] 章节数: {len(chapter_files)}" + (" (试读版)" if sample else ""))

    with tempfile.TemporaryDirectory(prefix="ebook-pandoc-") as tmp:
        tmp_dir = Path(tmp)

        cleaned_files = []
        for fname in chapter_files:
            src_file = src_dir / fname
            if not src_file.exists():
                print(f"  跳过: {fname}")
                continue

            content = src_file.read_text(encoding="utf-8")
            content = clean_for_pdf(content, lang)
            content = inject_chapter_image(content, fname)

            out_file = tmp_dir / fname
            out_file.write_text(content, encoding="utf-8")
            cleaned_files.append(str(out_file))

        if not cleaned_files:
            print("错误：没有可用的章节文件")
            return False

        pandoc_cmd = [
            "pandoc",
            f"--metadata-file={metadata_file}",
            f"--include-in-header={preamble_file}",
            f"--pdf-engine={XELATEX}",
            "--top-level-division=chapter",
            f"--resource-path={src_dir}:{REPO_ROOT}:{REPO_ROOT / 'img'}",
            "--toc",
            "--toc-depth=1",
            "-o", str(pdf_out),
        ] + cleaned_files

        print(f"[{lang}] 正在生成 PDF...")

        result = subprocess.run(
            pandoc_cmd, capture_output=True, text=True,
            env={**os.environ, "PATH": f"/usr/local/texlive/2026/bin/universal-darwin:{os.environ.get('PATH', '')}"}
        )

        if result.returncode != 0:
            print(f"PDF 生成失败:")
            for line in result.stderr.split('\n'):
                if 'error' in line.lower() or 'fatal' in line.lower() or '!' in line[:3]:
                    print(f"  {line}")
            stderr_lines = result.stderr.strip().split('\n')
            if len(stderr_lines) > 20:
                print(f"\n  ... 最后 20 行:")
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

    # 中文 EPUB 需要先构建 zh/
    if lang == "zh":
        epub_out = ebook_dir / "比特币那些事儿.epub"
        title = "比特币那些事儿"
        # 确保 zh/ 已构建
        build_zh = REPO_ROOT / "scripts" / "build_zh.py"
        if build_zh.exists():
            print(f"[{lang}] 先构建 zh/...")
            subprocess.run([sys.executable, str(build_zh)], capture_output=True)
    else:
        epub_out = ebook_dir / "Stories-about-Bitcoin.epub"
        title = "Stories about Bitcoin"

    with tempfile.TemporaryDirectory(prefix="ebook-epub-") as tmp:
        tmp_dir = Path(tmp)

        for f in src_dir.glob("*.md"):
            if f.name in ("README.md", "INTRO.md"):
                continue
            content = f.read_text(encoding="utf-8")
            if f.name != "SUMMARY.md":
                content = clean_for_epub(content, lang)
            (tmp_dir / f.name).write_text(content, encoding="utf-8")

        # 扁平化 SUMMARY.md
        summary = (src_dir / "SUMMARY.md").read_text(encoding="utf-8")
        summary = re.sub(r'^##\s+.*$', '', summary, flags=re.MULTILINE)
        summary = re.sub(r'^---\s*$', '', summary, flags=re.MULTILINE)
        summary = re.sub(r'.*INTRO\.md.*\n?', '', summary)
        summary = re.sub(r'\n{3,}', '\n\n', summary)
        (tmp_dir / "SUMMARY.md").write_text(summary.strip() + '\n', encoding="utf-8")

        (tmp_dir / "README.md").write_text(f"# {title}\n", encoding="utf-8")
        book_config = {
            "title": title,
            "author": "beihaili",
            "language": "zh-hans" if lang == "zh" else "en",
        }
        (tmp_dir / "book.json").write_text(json.dumps(book_config, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"[{lang}] 生成 EPUB...")
        result = subprocess.run(["honkit", "epub", str(tmp_dir), str(epub_out)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"EPUB 生成失败:\n{result.stderr}")
            return False
        print(f"[{lang}] EPUB: {epub_out} ({epub_out.stat().st_size // 1024}KB)")

    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]

    langs = args if args else ["zh", "en"]
    use_honkit = "--honkit" in flags
    sample = "--sample" in flags

    for lang in langs:
        print(f"\n{'='*50}")
        print(f"构建 {lang} 电子书" + (" (试读版)" if sample else ""))
        print(f"{'='*50}")

        if use_honkit:
            build_honkit_epub(lang)
        elif sample:
            build_pandoc_pdf(lang, sample=True)
        else:
            build_pandoc_pdf(lang)
            build_honkit_epub(lang)

    print("\n✅ 完成！文件在 ebook/ 目录")


if __name__ == "__main__":
    main()
