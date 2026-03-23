# 电子书排版方案：Pandoc + XeLaTeX

## 当前状态

- Pandoc: **已安装** (v3.8.3)
- LaTeX: **未安装**
- 预处理脚本: `scripts/build_ebook.py` (已有，清理网页元素)

---

## 第一步：安装 LaTeX 环境

两个选择，选一个：

### 方案 A：MacTeX（推荐新手，5GB，啥都有）

```bash
brew install --cask mactex
# 安装后重启终端，或执行：
eval "$(/usr/libexec/path_helper)"
# 验证：
xelatex --version
```

### 方案 B：TinyTeX（轻量，100MB 起，按需装包）

```bash
curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh

# 安装中文排版必需包
tlmgr install ctex xecjk zhnumber fandol fontspec \
  fancyhdr geometry titlesec tocloft changepage \
  booktabs longtable float caption hyperref \
  xcolor bookmark csquotes epigraph \
  upquote parskip unicode-math \
  amsmath lm lm-math fourier-orns tcolorbox pgf environ etoolbox

# 验证：
xelatex --version
```

---

## 第二步：创建排版配置文件

### `ebook/metadata-zh.yaml` — 中文版元数据

```yaml
---
title: 比特币那些事儿
subtitle: "1976—2025：从密码朋克到数字黄金"
author: beihaili
date: "2025"
lang: zh-CN

# 文档类
documentclass: ctexbook
classoption:
  - b5paper
  - 12pt
  - openright
  - twoside

# 页面布局
geometry:
  - inner=2.5cm
  - outer=2cm
  - top=2.5cm
  - bottom=2cm
  - bindingoffset=0.5cm

# 排版
linestretch: 1.5
toc: true
toc-depth: 1
toc-title: "目　录"
numbersections: false

# 字体
CJKmainfont: Songti SC
CJKsansfont: Hiragino Sans GB
CJKmonofont: Heiti SC
mainfont: Palatino
sansfont: Helvetica Neue
monofont: Menlo

# 链接
colorlinks: true
linkcolor: black
urlcolor: "blue!70!black"

# 自定义 LaTeX
header-includes: |
  \usepackage{fancyhdr}
  \usepackage{changepage}

  %% ===== 章节标题：只显示标题，不显示"第X章" =====
  \ctexset{
    chapter = {
      name = {},
      number = {},
      format = \huge\bfseries\centering,
      beforeskip = 50pt,
      afterskip = 40pt,
    },
    section = {
      format = \Large\bfseries,
      beforeskip = 20pt,
      afterskip = 10pt,
    }
  }

  %% ===== 天眉 + 页码 =====
  \pagestyle{fancy}
  \fancyhf{}
  \fancyhead[LE]{\small\itshape 比特币那些事儿}
  \fancyhead[RO]{\small\itshape \leftmark}
  \fancyfoot[C]{\thepage}
  \renewcommand{\headrulewidth}{0.4pt}
  \fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0pt}
  }

  %% ===== 水平线 → 三星号间隔 =====
  \def\horizontalrule{%
    \par\vspace{1.5em}%
    \noindent\hfil{\large *\quad *\quad *}\hfil%
    \par\vspace{1.5em}%
  }

  %% ===== 引用块样式（题词/引言） =====
  \renewenvironment{quote}{%
    \vspace{0.8em}%
    \begin{adjustwidth}{2em}{2em}%
    \small\itshape
  }{%
    \end{adjustwidth}%
    \vspace{0.8em}%
  }

  %% ===== 版权页 =====
  \AtBeginDocument{
    \thispagestyle{empty}
    \null\vfill
    \begin{center}
    {\Large\bfseries 比特币那些事儿}\\[0.5em]
    {\large\itshape Stories about Bitcoin}\\[2em]
    {\normalsize 作者：beihaili}\\[1em]
    {\small 本书以 CC-BY-SA 4.0 许可证开源}\\[0.5em]
    {\small 在线阅读：\url{https://beihaili.github.io/Stories-about-Bitcoin/zh/}}\\[0.5em]
    {\small ⚡ Lightning: \texttt{latebrook396888@getalby.com}}\\[0.3em]
    {\small ₿ BTC: \texttt{bc1qjt7uhztd2pumpx6p5w0sl8jxfzmxp3nyahysmcqklqfkecqftuysu733ca}}\\[2em]
    {\footnotesize 2025年 · 第一版}
    \end{center}
    \vfill
    \clearpage
  }
---
```

### `ebook/metadata-en.yaml` — 英文版元数据

```yaml
---
title: Stories about Bitcoin
subtitle: "1976—2025: From Cypherpunks to Digital Gold"
author: beihaili
date: "2025"
lang: en

documentclass: book
classoption:
  - b5paper
  - 12pt
  - openright
  - twoside

geometry:
  - inner=2.5cm
  - outer=2cm
  - top=2.5cm
  - bottom=2cm
  - bindingoffset=0.5cm

linestretch: 1.4
toc: true
toc-depth: 1
numbersections: false

mainfont: Palatino
sansfont: Helvetica Neue
monofont: Menlo

colorlinks: true
linkcolor: black
urlcolor: "blue!70!black"

header-includes: |
  \usepackage{fancyhdr}
  \usepackage{changepage}
  \usepackage{titlesec}

  %% 章节标题
  \titleformat{\chapter}[display]
    {\huge\bfseries\centering}{}{0pt}{}
  \titlespacing*{\chapter}{0pt}{50pt}{40pt}

  %% 天眉 + 页码
  \pagestyle{fancy}
  \fancyhf{}
  \fancyhead[LE]{\small\itshape Stories about Bitcoin}
  \fancyhead[RO]{\small\itshape \leftmark}
  \fancyfoot[C]{\thepage}
  \renewcommand{\headrulewidth}{0.4pt}
  \fancypagestyle{plain}{
    \fancyhf{}
    \fancyfoot[C]{\thepage}
    \renewcommand{\headrulewidth}{0pt}
  }

  %% 水平线 → 三星号
  \def\horizontalrule{%
    \par\vspace{1.5em}%
    \noindent\hfil{\large *\quad *\quad *}\hfil%
    \par\vspace{1.5em}%
  }

  %% 引用块
  \renewenvironment{quote}{%
    \vspace{0.8em}%
    \begin{adjustwidth}{2em}{2em}%
    \small\itshape
  }{%
    \end{adjustwidth}%
    \vspace{0.8em}%
  }
---
```

---

## 第三步：更新预处理脚本

在 `scripts/build_ebook.py` 的 `build_ebook()` 函数里添加 Pandoc+XeLaTeX 路径。

核心构建命令：

```bash
# 中文版
pandoc \
  --metadata-file=ebook/metadata-zh.yaml \
  --pdf-engine=xelatex \
  --shift-heading-level-by=-1 \
  --resource-path=zh:. \
  --toc \
  -o ebook/比特币那些事儿.pdf \
  zh_clean/INTRO.md \
  zh_clean/00_引子*.md \
  zh_clean/01_*.md \
  zh_clean/02_*.md \
  ... (按 SUMMARY.md 顺序列出所有清理后的章节文件)
```

关键参数说明：
- `--shift-heading-level-by=-1`：让 `# H1` 成为 `\chapter`（而非 `\section`）
- `--pdf-engine=xelatex`：支持中文字体
- `--toc`：自动生成目录（显示**真实页码**）
- `--resource-path`：图片搜索路径

---

## 第四步：构建流程

```bash
# 1. 安装 LaTeX（选一个）
brew install --cask mactex   # 或用 TinyTeX

# 2. 构建中文版
cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin
python3 scripts/build_ebook.py zh --engine pandoc

# 3. 构建英文版
python3 scripts/build_ebook.py en --engine pandoc

# 4. 检查输出
open ebook/比特币那些事儿.pdf
```

---

## 预期效果对比

| 特性 | HonKit 版（当前） | Pandoc+LaTeX 版 |
|------|---------------|----------------|
| 封面 | Calibre 自动生成 | 自定义标题页+版权页 |
| 目录 | 章节编号(1.1) | **真实页码** |
| 空白页 | 有多余空白页 | **无** |
| 天眉 | 固定"比特币那些事儿" | **偶数页书名/奇数页章节名** |
| 页码 | 左下角 | **底部居中** |
| 水平线 | 丑陋的横线 | **优雅的 * * *** |
| 引言 | 普通缩进 | **缩进+斜体小字** |
| 字体 | 系统默认 | **宋体正文+黑体标题** |
| 纸张 | A4 | **B5（书籍标准）** |
| 行距 | 默认 | **1.5倍（阅读舒适）** |
| 装订边距 | 无 | **内侧加宽+装订偏移** |

---

## 文件结构

```
Stories-about-Bitcoin/
├── ebook/
│   ├── README.md              ← 本文件
│   ├── metadata-zh.yaml       ← 中文排版配置
│   ├── metadata-en.yaml       ← 英文排版配置
│   ├── 比特币那些事儿.pdf      ← 输出
│   ├── 比特币那些事儿.epub     ← 输出
│   ├── Stories-about-Bitcoin.pdf
│   └── Stories-about-Bitcoin.epub
├── scripts/
│   └── build_ebook.py         ← 构建脚本（预处理+生成）
```
