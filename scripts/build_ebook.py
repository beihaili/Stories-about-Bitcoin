#!/usr/bin/env python3
"""
电子书构建脚本
从网页版 Markdown 生成干净的电子书（EPUB/PDF）

流程：
1. 复制 zh/ 或 en/ 的 Markdown 到临时目录
2. 清理网页专属元素（徽章、社交链接、捐赠块等）
3. 生成干净的 INTRO.md（书的前言，非网页介绍页）
4. 用 HonKit 生成 EPUB
5. 用 Calibre ebook-convert 生成 PDF（带页眉页脚页码）
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
BTC_ADDRESS = "bc1qjt7uhztd2pumpx6p5w0sl8jxfzmxp3nyahysmcqklqfkecqftuysu733ca"
LN_ADDRESS = "latebrook396888@getalby.com"


def clean_chapter(content: str, lang: str = "zh") -> str:
    """清理单个章节的网页专属元素"""

    # 1. 删除 shields.io 徽章行
    content = re.sub(r'!\[(?:status|author|date|difficulty)\]\(https://img\.shields\.io/.*?\)\n?', '', content)
    # 也删除本地引用的徽章
    content = re.sub(r'!\[(?:status|author|date|difficulty)\]\(.*?shields\.io.*?\)\n?', '', content)

    # 2. 删除所有配图标签（各种路径格式）
    content = re.sub(r'!\[配图\]\(.*?\)\n?', '', content)
    content = re.sub(r'!\[.*?配图.*?\]\(.*?\)\n?', '', content)
    # 删除独立的图片引用行（如 ![alt](../img/XX.png)）
    content = re.sub(r'^!\[.*?\]\(\.\./img.*?\)\s*$', '', content, flags=re.MULTILINE)

    # 3. 删除 <picture>/<source>/<img> 图片块（HonKit 章节里的响应式图片）
    content = re.sub(r'<picture>.*?</picture>\n?', '', content, flags=re.DOTALL)
    # 删除独立的 <img> 标签
    content = re.sub(r'<img\s+src="\.\.?/img.*?>\n?', '', content)

    # 4. 删除 > 💡 引言块（包含社交链接的整个 blockquote）
    # 匹配从 > 💡 开始，到连续 > 行结束的整个块
    content = re.sub(
        r'^> 💡.*?(?=\n[^>]|\n\n[^>]|\Z)',
        '',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # 5. 删除社交链接 blockquote 残留
    content = re.sub(r'^>\s*欢迎关注.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*进入微信.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*文章开源.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^>\s*\n', '', content, flags=re.MULTILINE)

    # 6. 删除捐赠块
    content = re.sub(
        r'<div align="center"[^>]*style="[^"]*border.*?f7931a.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # 7. 删除页脚导航链接块
    content = re.sub(
        r'<div align="center">\s*\n.*?(?:返回主页|Return to Homepage).*?</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # 8. 清理多余空行（超过2个连续空行变成2个）
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # 9. 清理开头的多余空行
    content = re.sub(r'^(#[^\n]+\n)\n{2,}', r'\1\n', content)

    return content.strip() + '\n'


def create_ebook_intro(lang: str = "zh") -> str:
    """创建适合电子书的前言页"""
    if lang == "zh":
        return """# 比特币那些事儿

*用《明朝那些事儿》的风格讲述比特币的传奇历史*

**作者**：beihaili

---

这是一部讲述比特币历史的作品。从1976年哈耶克写下《货币的非国家化》，到2025年比特币突破十万美元——我们用故事的方式，记录这场持续半个世纪的货币革命。

33个章节，覆盖密码朋克的理想、中本聪的创世、丝绸之路的争议、Mt.Gox的崩塌、扩容战争的撕裂、ETF的突破，以及战略储备的诞生。

每一个章节都是一段真实的历史，每一个人物都有名有姓。

---

*"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"*

——创世区块，2009年1月3日

---

**开源项目**：本书以 CC-BY-SA 4.0 许可证开源

**在线阅读**：https://beihaili.github.io/Stories-about-Bitcoin/zh/

**支持作者**：
- ⚡ Lightning: `latebrook396888@getalby.com`
- ₿ BTC: `bc1qjt7uhztd2pumpx6p5w0sl8jxfzmxp3nyahysmcqklqfkecqftuysu733ca`
"""
    else:
        return """# Stories about Bitcoin

*Bitcoin History Told in the Style of "Those Things in Ming Dynasty"*

**Author**: beihaili

---

This is a chronicle of Bitcoin's history. From Hayek's *Denationalization of Money* in 1976 to Bitcoin breaking $100,000 in 2025 — we tell this half-century monetary revolution through stories.

33 chapters covering the Cypherpunk dream, Satoshi's genesis, the Silk Road controversy, Mt. Gox's collapse, the Scaling Wars, the ETF breakthrough, and the birth of the Strategic Bitcoin Reserve.

Every chapter is real history. Every character has a name.

---

*"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"*

— Genesis Block, January 3, 2009

---

**Open Source**: This book is licensed under CC-BY-SA 4.0

**Read Online**: https://beihaili.github.io/Stories-about-Bitcoin/en/

**Support the Author**:
- ⚡ Lightning: `latebrook396888@getalby.com`
- ₿ BTC: `bc1qjt7uhztd2pumpx6p5w0sl8jxfzmxp3nyahysmcqklqfkecqftuysu733ca`
"""


def build_ebook(lang: str = "zh"):
    """构建电子书"""
    src_dir = REPO_ROOT / lang
    ebook_dir = REPO_ROOT / "ebook"
    ebook_dir.mkdir(exist_ok=True)

    # 创建临时工作目录
    with tempfile.TemporaryDirectory(prefix="ebook-") as tmp:
        tmp_dir = Path(tmp)

        # 复制所有 Markdown 文件
        for f in src_dir.glob("*.md"):
            if f.name in ("README.md",):
                continue
            content = f.read_text(encoding="utf-8")
            if f.name == "INTRO.md":
                # 替换为电子书专用的前言
                content = create_ebook_intro(lang)
            else:
                content = clean_chapter(content, lang)
            (tmp_dir / f.name).write_text(content, encoding="utf-8")

        # 创建扁平化的 SUMMARY.md（去掉 section headers，避免每个篇占一整页）
        summary_content = (src_dir / "SUMMARY.md").read_text(encoding="utf-8")
        # 移除 ## 章节分组标题行（如 "## 🌟 序言"、"## 🔮 创世纪篇"）
        summary_content = re.sub(r'^##\s+.*$', '', summary_content, flags=re.MULTILINE)
        # 移除 --- 分隔线
        summary_content = re.sub(r'^---\s*$', '', summary_content, flags=re.MULTILINE)
        # 清理多余空行
        summary_content = re.sub(r'\n{3,}', '\n\n', summary_content)
        (tmp_dir / "SUMMARY.md").write_text(summary_content.strip() + '\n', encoding="utf-8")

        # 创建 book.json
        if lang == "zh":
            book_config = {
                "title": "比特币那些事儿",
                "author": "beihaili",
                "description": "用《明朝那些事儿》的风格讲述比特币的传奇历史",
                "language": "zh-hans",
                "structure": {"readme": "INTRO.md"},
                "pdf": {
                    "fontSize": 12,
                    "paperSize": "a4",
                    "margin": {"top": 56, "bottom": 56, "left": 62, "right": 62}
                }
            }
            epub_out = ebook_dir / "比特币那些事儿.epub"
            pdf_out = ebook_dir / "比特币那些事儿.pdf"
        else:
            book_config = {
                "title": "Stories about Bitcoin",
                "author": "beihaili",
                "description": "Bitcoin History Told in the Style of Those Things in Ming Dynasty",
                "language": "en",
                "structure": {"readme": "INTRO.md"},
                "pdf": {
                    "fontSize": 12,
                    "paperSize": "a4",
                    "margin": {"top": 56, "bottom": 56, "left": 62, "right": 62}
                }
            }
            epub_out = ebook_dir / "Stories-about-Bitcoin.epub"
            pdf_out = ebook_dir / "Stories-about-Bitcoin.pdf"

        (tmp_dir / "book.json").write_text(
            json.dumps(book_config, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        # 生成 EPUB
        print(f"[{lang}] 生成 EPUB...")
        result = subprocess.run(
            ["honkit", "epub", str(tmp_dir), str(epub_out)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"EPUB 生成失败:\n{result.stderr}")
            return False
        print(f"[{lang}] EPUB: {epub_out} ({epub_out.stat().st_size // 1024}KB)")

        # 用 ebook-convert 从 EPUB 生成 PDF（更好的排版控制）
        title = book_config["title"]
        print(f"[{lang}] 生成 PDF...")

        pdf_args = [
            "ebook-convert", str(epub_out), str(pdf_out),
            "--paper-size", "a4",
            "--pdf-default-font-size", "12",
            "--pdf-mono-font-size", "10",
            "--margin-top", "72",
            "--margin-bottom", "56",
            "--margin-left", "72",
            "--margin-right", "72",
            "--pdf-page-numbers",
            "--chapter", "//h:h1",
            "--page-breaks-before", "//h:h1",
            "--insert-blank-line",
            "--pdf-sans-family", "PingFang SC" if lang == "zh" else "Helvetica",
            "--pdf-serif-family", "Songti SC" if lang == "zh" else "Georgia",
        ]

        result = subprocess.run(pdf_args, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"PDF 生成失败:\n{result.stderr}")
            # 如果失败，回退到 honkit pdf
            print(f"[{lang}] 回退到 HonKit PDF...")
            subprocess.run(
                ["honkit", "pdf", str(tmp_dir), str(pdf_out)],
                capture_output=True, text=True
            )

        if pdf_out.exists():
            print(f"[{lang}] PDF: {pdf_out} ({pdf_out.stat().st_size // 1024 // 1024}MB)")

    return True


def main():
    langs = sys.argv[1:] if len(sys.argv) > 1 else ["zh", "en"]
    for lang in langs:
        print(f"\n{'='*50}")
        print(f"构建 {lang} 电子书")
        print(f"{'='*50}")
        build_ebook(lang)

    print("\n✅ 完成！文件在 ebook/ 目录")


if __name__ == "__main__":
    main()
