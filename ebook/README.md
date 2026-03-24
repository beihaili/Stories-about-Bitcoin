# 电子书构建

## 构建命令

```bash
# 中文完整版 PDF + EPUB
python3 scripts/build_ebook.py zh

# 英文完整版 PDF + EPUB
python3 scripts/build_ebook.py en

# 双语
python3 scripts/build_ebook.py zh en

# 试读版（5 章精选）
python3 scripts/build_ebook.py zh --sample
python3 scripts/build_ebook.py en --sample

# 仅 EPUB
python3 scripts/build_ebook.py zh --honkit
```

## 依赖

- **Pandoc** v3.8+：`brew install pandoc`
- **XeLaTeX**：`/usr/local/texlive/2026/bin/universal-darwin/xelatex`（MacTeX）
- **HonKit**：`npm install -g honkit`（EPUB 用）

## 输出文件

| 文件 | 说明 |
|------|------|
| `比特币那些事儿.pdf` | 中文完整版（36 章，含配图） |
| `比特币那些事儿.epub` | 中文 EPUB |
| `Stories-about-Bitcoin.pdf` | 英文完整版 |
| `Stories-about-Bitcoin.epub` | 英文 EPUB |
| `Bitcoin-Stories-ZH-Sample.pdf` | 中文试读版（5 章） |
| `Bitcoin-Stories-EN-Sample.pdf` | 英文试读版（5 章） |

## 排版配置

| 文件 | 用途 |
|------|------|
| `metadata-zh.yaml` | 中文排版元数据（ctexbook, B5, 宋体） |
| `metadata-en.yaml` | 英文排版元数据（book, B5, Palatino） |
| `preamble-zh.tex` | 中文 LaTeX 样式（天眉、趣闻环境、版权页） |
| `preamble-en.tex` | 英文 LaTeX 样式 |

## 构建流程

```
正文/*.md → clean_chapter（清理网页元素）
         → inject_chapter_image（注入章节配图）
         → Pandoc + XeLaTeX → PDF

zh/*.md  → clean_chapter → HonKit → EPUB
```

### 预处理（clean_chapter）

- 删除：shields.io 徽章、社交链接、捐赠块、页脚导航、emoji
- 保留：正文内容、章节标题、小节标题、引用块
- 增强：章末趣闻 → `\begin{funfact}`、水平线 → `\vspace`
- 符号替换：→ × ≈ 等宋体不支持的字符

### 排版特性

- B5 纸张 + 装订偏移（适合印刷）
- 天眉：偶数页书名 / 奇数页章节名
- 版权页：含 Lightning + BTC 捐赠地址
- 每章开头全宽配图（85% 宽度）
- Widow/orphan 控制（无孤行寡行）
- 趣闻环境（缩进斜体小字）
