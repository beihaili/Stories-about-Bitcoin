# README 门面改造 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 README 改造为推广级门面（双语、39 章、写作样本），同步更新 CONTRIBUTING.md 和 CLAUDE.md，发布 ebook v3.0。

**Architecture:** 按文件逐个更新——README.md（完整重写）→ CONTRIBUTING.md（小修）→ CLAUDE.md（数字更新）→ ebook 构建发布。每个文件独立 commit。

**Tech Stack:** Markdown, Pandoc + XeLaTeX (ebook), GitHub CLI (release)

---

### Task 1: 重写 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 用以下内容完整替换 README.md**

```markdown
<div align="center">

# Stories about Bitcoin | 比特币那些事儿

**Bitcoin's history, told as literature — not textbook.**

A bilingual (Chinese/English) open-source book covering 1976–2025 in 39 chapters.<br>
From Hayek's dream of private money to Bitcoin crossing $100,000.

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg?style=flat-square)](https://creativecommons.org/licenses/by-sa/4.0/)
[![GitHub stars](https://img.shields.io/github/stars/beihaili/Stories-about-Bitcoin?style=flat-square)](https://github.com/beihaili/Stories-about-Bitcoin/stargazers)
[![Deploy](https://img.shields.io/github/actions/workflow/status/beihaili/Stories-about-Bitcoin/deploy.yml?branch=main&label=website&style=flat-square)](https://beihaili.github.io/Stories-about-Bitcoin/)

[Read Online (ZH)](https://beihaili.github.io/Stories-about-Bitcoin/zh/) · [Read Online (EN)](https://beihaili.github.io/Stories-about-Bitcoin/en/) · [Download Ebook](https://github.com/beihaili/Stories-about-Bitcoin/releases/tag/v3.0)

</div>

> *745 Seventh Avenue, Manhattan. Lehman Brothers headquarters. The lights were still on — many employees hadn't gone home all weekend. They knew the firm wouldn't survive the day, but up until the very last moment, they were still trying to reach potential buyers. No one picked up the phone.*
>
> *At 1:45 a.m., Lehman Brothers filed for bankruptcy. $613 billion in debt. 158 years of history.*
>
> *People inside the building started packing cardboard boxes.*
>
> *That headline — "Chancellor on brink of second bailout for banks" — would, three months later, be carved into a piece of code that can never be deleted by an anonymous programmer.*
>
> — Chapter 3: Crisis and Creation

| | |
|---|---|
| 📖 Read Online | [Chinese](https://beihaili.github.io/Stories-about-Bitcoin/zh/) · [English](https://beihaili.github.io/Stories-about-Bitcoin/en/) |
| 📥 Download | [PDF & EPUB (v3.0)](https://github.com/beihaili/Stories-about-Bitcoin/releases/tag/v3.0) |
| 💬 Community | [Discord (English)](https://discord.gg/TTFuH9de) · [WeChat (中文)](https://forms.gle/QMBwL6LwZyQew1tX8) |
| ⚡ Support | Lightning: `latebrook396888@getalby.com` |

<details>
<summary><strong>Table of Contents (39 chapters across 9 periods)</strong></summary>

### Prologue
- 00 — A Beam of Idealistic Light

### Genesis (1976–2009)
- 01 Prophecy and Failure — Hayek, Chaum, and early digital cash
- 02 The Cypherpunk Technical Puzzle — the technical groundwork
- 03 Crisis and Creation — 2008 financial crisis, the whitepaper, genesis block

### First Steps (2009–2010)
- 04 The First Believer — Hal Finney
- 05 Community and Tools — BitcoinTalk, early ecosystem
- 06 Value Discovery — from worthless to worth something
- 07 The First Crisis and Recovery — the value overflow bug
- 08 Satoshi's Mysterious Departure — Satoshi leaves

### Rising Storm (2011–2012)
- 09 The First Collision of Ideals and Reality — Silk Road
- 10 The Rise of the Mt. Gox Empire — rise of Mt. Gox
- 11 The First Bubble — $1 → $32 → $2
- 12 The Hash Power Revolution — CPU to GPU to ASIC
- 13 Ecosystem Emergence — payment services, global adoption seeds

### Undercurrents (2013–2016)
- 14 The Cyprus Moment — Cyprus banking crisis
- 15 Washington's Scrutiny — US regulatory attention
- 16 China's Policy Rollercoaster — China's policy swings
- 17 The Fall of Mt. Gox — 850,000 BTC gone
- 18 Global Regulatory Divergence — regulatory divergence worldwide
- 19 The Scaling Debate Emerges — block size debate begins

### Civil War & Independence (2017)
- 20 The Scaling War Intensifies — SegWit vs big blocks
- 21 Bitcoin Independence Day — SegWit activation, BCH fork
- 22 Price Frenzy and Speculative Bubble — $20K and the 2017 mania

### Suit Revolution (2018–2021)
- 23 The Awakening of Institutions — institutions start paying attention
- 24 Safe-Haven Shift During COVID-19 — COVID and the digital gold narrative
- 25 The Institutional Entry Milestone — MicroStrategy, Tesla, corporate treasuries
- 26 The Great Mining Migration — China mining ban, global hashrate redistribution
- 27 Lightning Strikes — Lightning Network from whitepaper to street payments

### Future Promise (2021–2025)
- 28 The El Salvador Pioneer — first nation to adopt Bitcoin as legal tender
- 29 The New Geopolitical Variable — Bitcoin in international politics
- 30 The Domino Collapse — Luna, Three Arrows Capital, FTX
- 31 Trust Shattered Again — aftermath of the collapses
- 32 The Inscription Storm — Ordinals and BRC-20
- 33 The Historic ETF Breakthrough — spot ETF approval
- 34 The Election and Strategic Reserve — 2024 US election
- 35 The $100K Breakthrough — Bitcoin crosses six figures
- 36 The Absent Ones — pioneers who didn't live to see this
- 37 The Light Still Burns — epilogue

### Special Edition
- Charlie Kirk's Bitcoin Journey

</details>

## Contributing

Translations, fact-checking, and code contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Development

```bash
# Website (React SPA)
cd new-website && npm install && npm run dev    # localhost:5173

# Build zh/ from source chapters
python3 scripts/build_zh.py

# Ebook (requires Pandoc + XeLaTeX)
python3 scripts/build_ebook.py zh    # Chinese PDF + EPUB
python3 scripts/build_ebook.py en    # English PDF + EPUB
```

## Contributors

<a href="https://github.com/beihaili/Stories-about-Bitcoin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=beihaili/Stories-about-Bitcoin" />
</a>

## License

- **Content** (chapters, images): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code** (website, scripts): [MIT](LICENSE)

⚡ Lightning: `latebrook396888@getalby.com`<br>
₿ On-chain: `bc1qjt7uhztd2pumpx6p5w0sl8jxfzmxp3nyahysmcqklqfkecqftuysu733ca`

---

<div align="center">

# 🇨🇳 中文版

</div>

## 这本书讲什么

一部用文学笔法写成的比特币编年史。从1976年哈耶克的《货币非国有化》写到2025年比特币突破十万美元，39章，中英双语，完全开源免费。

不是教科书，不是技术手册——是像《明朝那些事儿》那样，把历史讲成故事。

> *曼哈顿第七大道745号，雷曼兄弟总部。大楼里的灯还亮着——很多人整个周末都没回家。他们知道公司撑不过今天了，但直到最后一刻还在试图联系潜在的买家。没有人接电话。*
>
> *上午1点45分，雷曼兄弟向法院递交了破产申请。6130亿美元的债务。158年的历史。*
>
> *一栋楼里的人开始收拾纸箱。*
>
> *这条头版标题——"Chancellor on brink of second bailout for banks"——会在三个月后被一个匿名程序员刻进一段永远无法删除的代码里。*
>
> — 第三章：危机与创世

| | |
|---|---|
| 📖 在线阅读 | [中文](https://beihaili.github.io/Stories-about-Bitcoin/zh/) · [English](https://beihaili.github.io/Stories-about-Bitcoin/en/) |
| 📥 下载电子书 | [PDF & EPUB (v3.0)](https://github.com/beihaili/Stories-about-Bitcoin/releases/tag/v3.0) |
| 💬 社区 | [Discord (English)](https://discord.gg/TTFuH9de) · [微信群](https://forms.gle/QMBwL6LwZyQew1tX8) |

<details>
<summary><strong>目录（39章 · 9个时期）</strong></summary>

### 序言
- 00 — 引子：一束照进现实的理想之光

### 创世纪篇 (1976–2009)
- 01 预言与失败 — 哈耶克、乔姆与早期数字现金
- 02 密码朋克的技术拼图 — 密码学运动的技术基础
- 03 危机与创世 — 2008金融危机、白皮书、创世区块

### 初出茅庐篇 (2009–2010)
- 04 第一个信徒 — 哈尔·芬尼
- 05 社区与工具 — BitcoinTalk、早期生态
- 06 价值发现 — 从一文不值到有所值
- 07 第一次危机与修复 — 数值溢出漏洞
- 08 中本聪的神秘退场 — 创造者消失

### 风起云涌篇 (2011–2012)
- 09 理想与现实的第一次碰撞 — 丝绸之路
- 10 Mt.Gox帝国的崛起 — 交易所霸主
- 11 第一次泡沫 — 1美元→32美元→2美元
- 12 算力革命 — CPU到GPU到ASIC
- 13 生态萌芽 — 支付服务与全球扩展

### 暗潮汹涌篇 (2013–2016)
- 14 塞浦路斯时刻 — 银行危机
- 15 华盛顿的审视 — 美国监管目光
- 16 中国政策过山车 — 中国政策摇摆
- 17 Mt.Gox的覆灭 — 85万枚比特币消失
- 18 全球监管分化 — 各国监管路径分裂
- 19 扩容争议萌芽 — 区块大小之争开端

### 内战与独立篇 (2017)
- 20 扩容战争白热化 — SegWit vs 大区块
- 21 比特币独立日 — SegWit激活、BCH分叉
- 22 价格狂欢与投机泡沫 — 2万美元与2017年狂热

### 西装革命篇 (2018–2021)
- 23 机构觉醒的开端 — 机构开始关注
- 24 新冠疫情下的避险转向 — COVID与数字黄金叙事
- 25 机构入场里程碑 — MicroStrategy、特斯拉、企业国库
- 26 矿业大迁徙 — 中国禁矿、全球算力再分配
- 27 闪电降临 — 闪电网络从白皮书到街头支付

### 未来可期篇 (2021–2025)
- 28 萨尔瓦多先驱 — 全球首个比特币法币化国家
- 29 地缘政治新变量 — 比特币在国际政治中的角色
- 30 多米诺崩塌 — Luna、三箭资本、FTX
- 31 信任再次破碎 — 连环崩盘的余波
- 32 铭文风暴 — Ordinals与BRC-20
- 33 ETF历史性突破 — 现货ETF获批
- 34 大选与战略储备 — 2024美国大选
- 35 十万美元突破 — 六位数时代
- 36 缺席的人 — 没能等到这一天的先驱者
- 37 光未熄灭 — 尾声

### 特别篇
- 查理·柯克的比特币之路

</details>

## 参与贡献

翻译校对、事实核查、代码改进均欢迎。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

- **内容**（章节、插图）：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **代码**（网站、脚本）：[MIT](LICENSE)

⚡ Lightning: `latebrook396888@getalby.com`<br>
₿ On-chain: `bc1qjt7uhztd2pumpx6p5w0sl8jxfzmxp3nyahysmcqklqfkecqftuysu733ca`
```

- [ ] **Step 2: 验证渲染效果**

在本地用以下命令快速检查 markdown 结构：

```bash
# 确认没有 markdown 语法错误
head -5 README.md   # 应该看到 <div align="center">
grep -c "##" README.md   # 统计标题数量，预期约 10-12 个
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs(README): 门面改造——双语结构、写作样本、39章目录"
```

---

### Task 2: 更新 CONTRIBUTING.md

**Files:**
- Modify: `CONTRIBUTING.md:1-6`

- [ ] **Step 1: 更新章节数和年份**

将第2行：
```
an open-source bilingual Bitcoin history book covering 1976-2024 in 36 chapters
```
改为：
```
an open-source bilingual Bitcoin history book covering 1976-2025 in 39 chapters
```

- [ ] **Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs(CONTRIBUTING): 更新章节数(39)和年份(2025)"
```

---

### Task 3: 更新 CLAUDE.md (in-repo)

**Files:**
- Modify: `CLAUDE.md`（仓库内的，不是 ~/.claude/ 下的）

- [ ] **Step 1: 更新关键数字**

需要修改的位置：
- "36 chapters (00-34 + special)" → "39 chapters (00-37 + special)"
- "36 chapters" 出现的所有位置
- "00-34" → "00-37"
- chapters.js 注释中 "36 章" 相关引用
- `img/00-34.png` → `img/00-37.png`

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(CLAUDE.md): 更新章节数和文件引用至37章"
```

---

### Task 4: 构建 ebook v3.0

**Files:**
- 构建产物：`ebook/` 目录下的 PDF + EPUB

- [ ] **Step 1: 构建中文版**

```bash
python3 scripts/build_ebook.py zh
```

Expected: 生成中文 PDF + EPUB，包含 39 章。

- [ ] **Step 2: 构建英文版**

```bash
python3 scripts/build_ebook.py en
```

Expected: 生成英文 PDF + EPUB，包含 39 章。

- [ ] **Step 3: 验证构建产物**

```bash
ls -la ebook/*.pdf ebook/*.epub
```

Expected: 4 个文件（zh PDF, zh EPUB, en PDF, en EPUB）。

---

### Task 5: 发布 GitHub Release v3.0

- [ ] **Step 1: 构建 sample 版本**

```bash
python3 scripts/build_ebook.py zh --sample
python3 scripts/build_ebook.py en --sample
```

- [ ] **Step 2: 推送所有 commit**

```bash
git push origin main
```

- [ ] **Step 3: 创建 GitHub Release**

```bash
gh release create v3.0 \
  ebook/Stories-about-Bitcoin-zh.pdf \
  ebook/Stories-about-Bitcoin-zh.epub \
  ebook/Stories-about-Bitcoin-en.pdf \
  ebook/Stories-about-Bitcoin-en.epub \
  ebook/Stories-about-Bitcoin-zh-sample.pdf \
  ebook/Stories-about-Bitcoin-en-sample.pdf \
  --title "v3.0 — 39 Chapters (37 + Special + Prologue)" \
  --notes "$(cat <<'NOTES'
## What's New

- **3 new chapters**: Lightning Strikes (ch27), The Domino Collapse (ch30), The Inscription Storm (ch32)
- Full book now spans 39 chapters (00–37 + special edition)
- Chapter 11 (The First Bubble) rewritten with richer narrative
- All English translations updated to match new chapter numbering

## Downloads

| File | Description |
|------|-------------|
| `Stories-about-Bitcoin-zh.pdf` | Chinese full book (PDF) |
| `Stories-about-Bitcoin-zh.epub` | Chinese full book (EPUB) |
| `Stories-about-Bitcoin-en.pdf` | English full book (PDF) |
| `Stories-about-Bitcoin-en.epub` | English full book (EPUB) |
| `*-sample.pdf` | Preview (first 5 chapters) |

Read online: [Chinese](https://beihaili.github.io/Stories-about-Bitcoin/zh/) · [English](https://beihaili.github.io/Stories-about-Bitcoin/en/)
NOTES
)"
```

- [ ] **Step 4: 验证 release**

```bash
gh release view v3.0
```

Expected: 显示 v3.0 release 信息和 6 个附件。

---

### Task 6: 更新父目录 CLAUDE.md

**Files:**
- Modify: `/Users/beihai/code/Bitcoin/bitcoinstory/CLAUDE.md`

- [ ] **Step 1: 更新章节数描述**

将 "35 chapters + SP" 等过时引用更新为 37 chapters + SP (共 39 个文件)。

- [ ] **Step 2: 不需要 commit**（父目录不在 git 仓库中）
