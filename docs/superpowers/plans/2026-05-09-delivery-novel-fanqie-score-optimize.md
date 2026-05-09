# Delivery Novel Fanqie Score Optimize Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Score and optimize all 43 chapters of `我给中本聪送外卖` for Fanqie recommendation validation while preserving the 100k-word version.

**Architecture:** Keep the novel source in `我给中本聪送外卖/正文/`; keep scoring and editorial decisions in `我给中本聪送外卖/设定/结构/`; keep execution tracking in this plan. Use GPT-5.5 baseline scoring for prioritization, then use human continuity and risk checks for final decisions.

**Tech Stack:** Markdown manuscript files, `scripts/export_fanqie_delivery.py`, `jq`, `git diff --check`.

---

## Files

- Create: `我给中本聪送外卖/设定/结构/番茄网文评分系统.md`
- Create: `我给中本聪送外卖/设定/结构/章节评分/43章番茄GPT55基线评分.md`
- Create: `我给中本聪送外卖/设定/结构/章节评分/43章番茄优化执行表.md`
- Modify: `我给中本聪送外卖/正文/42_铁盒里的缺席者.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/04_第一台亮着的电脑.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/06_披萨冷了，钱活了.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/12_电池、矿机和熟路.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/14_母亲的存款短信.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/18_给工具加一个退出键.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/19_群里吵翻的那一夜.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/20_我不当群主了.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/24_陈浩被裁那晚.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/27_陌生站点的第一天.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/31_退出的人.md`
- Modify, P1 batch: `我给中本聪送外卖/正文/41_第一笔归还.md`
- Modify: `我给中本聪送外卖/交接.md`
- Modify: `我给中本聪送外卖/CLAUDE.md`
- Modify: `我给中本聪送外卖/设定/README.md`

## Task 1: Scoring Framework

- [x] **Step 1: Confirm clean workspace**

Run:

```bash
git status --short
```

Expected: no output after checkpoint commit.

- [x] **Step 2: Verify current Fanqie export baseline**

Run:

```bash
python3 scripts/export_fanqie_delivery.py --clean --target-initial-chars 100000
jq '{chapter_count,total_body_chars,ready_for_initial_submission,generated_at}' 发布/番茄/我给中本聪送外卖/manifest.json
```

Expected: `chapter_count` is `43`, `total_body_chars` is at least `100000`, and `ready_for_initial_submission` is `true`.

- [x] **Step 3: Run read-only GPT-5.5 baseline**

Run:

```bash
codex exec -m gpt-5.5 -s read-only -C /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin
```

Expected: GPT-5.5 outputs a 43-row Fanqie validation scoring table and does not modify files.

- [ ] **Step 4: Commit scoring docs**

Run:

```bash
git add docs/superpowers/specs/2026-05-09-delivery-novel-fanqie-scoring-design.md \
  docs/superpowers/plans/2026-05-09-delivery-novel-fanqie-score-optimize.md \
  我给中本聪送外卖/设定/结构/番茄网文评分系统.md \
  我给中本聪送外卖/设定/结构/章节评分/43章番茄GPT55基线评分.md \
  我给中本聪送外卖/设定/结构/章节评分/43章番茄优化执行表.md
git commit -m "docs: add fanqie scoring framework"
```

## Task 2: P0 Chapter 42 Continuity Fix

- [ ] **Step 1: Rewrite chapter 42 opening state**

Change chapter 42 so it starts after chapter 41:

```text
互助池第一笔归还之后，李觉才把床底的铁盒拿出来。

陈浩已经到杭州一周了。每天晚上发来的消息很短，有时是外包项目的接口文档，有时只是酒店窗外一块灰白的天。出租屋少了一半声音，桌上也少了那根旧工牌挂绳。
```

Remove the current contradiction:

```text
互助池第一天就出了问题。
...
陈浩在旁边收拾行李。
```

- [ ] **Step 2: Keep the privacy-boundary scene, but make it a later echo**

Retain the `公开账本不是公开人的难堪` boundary, but anchor it after the first repayment:

```text
编号 003 的单据最终补齐了。李觉只在账本里写“线下核验通过”，没有上传孩子手背贴着胶布的照片。
```

- [ ] **Step 3: Reconnect to chapter 43**

End chapter 42 with ordinary orders continuing and the book title sentence, so chapter 43 can remain the active-choice ending.

- [ ] **Step 4: Verify chapter 42 no longer contains old timeline markers**

Run:

```bash
rg "互助池第一天|陈浩在旁边收拾行李|要去杭州待两个月" 我给中本聪送外卖/正文/42_铁盒里的缺席者.md
```

Expected: no output.

## Task 3: P1 Head-To-Tail Hook Pass

- [ ] **Step 1: Chapters 04, 06, 12, 14**

Apply only ending or opening hook edits:

- 04: add a customer callback or Zhao Qing question after Li Jue helps one stranger.
- 06: make the table save time, then immediately create a deduction-recovery question for chapter 07.
- 12: make the v0 route tool fail in someone else's hands, setting up chapter 13 overreach.
- 14: move a concrete platform loss or missed medicine order into the first screen, then end with Zhao Qing's account-risk screenshot for chapter 15.

- [ ] **Step 2: Chapters 18, 19, 20**

Differentiate the governance sequence:

- 18: personal exit and sync risk.
- 19: new-rider versus old-rider cost conflict.
- 20: refusal to act as judge.

- [ ] **Step 3: Chapters 24, 27, 31, 41**

Tighten pacing:

- 24: put Chen Hao's layoff message earlier and end with the first paid-packaging signal.
- 27: foreground Zhao Qing's first-day lost earnings and trim route-field explanation.
- 31: reduce rule discussion, keep Lao Liang, Zhao Qing's review, and the observation list.
- 41: put the `先还` transfer in the first screen and point the ending toward the iron box/book draft.

## Task 4: P2 Micro Pass

- [ ] **Step 1: Review P2 chapters from 01 to 43**

For P2 chapters, only edit if the change is low-risk:

- shorten repeated explanation;
- sharpen one ending sentence;
- make one concrete action visible;
- remove any tutorial-like financial operation detail.

- [ ] **Step 2: Do not touch Keep chapters unless verifying typo/continuity**

Keep chapters: 01, 13, 25, 28, 29, 43.

## Task 5: Export And Verification

- [ ] **Step 1: Export Fanqie package**

Run:

```bash
python3 scripts/export_fanqie_delivery.py --clean --target-initial-chars 100000
```

Expected: `readiness: initial submission threshold reached`.

- [ ] **Step 2: Check manifest**

Run:

```bash
jq '{chapter_count,total_body_chars,ready_for_initial_submission,generated_at}' 发布/番茄/我给中本聪送外卖/manifest.json
jq -r '.chapters[-5:][] | [.number,.title,.body_chars] | @tsv' 发布/番茄/我给中本聪送外卖/manifest.json
```

Expected:

- 43 chapters.
- At least 100000 body characters.
- Chapter 43 is `第043章 这次是我自己接单`.

- [ ] **Step 3: Check whitespace**

Run:

```bash
git diff --check -- 我给中本聪送外卖 docs/superpowers
```

Expected: no output.

## Task 6: Documentation And Commit

- [ ] **Step 1: Update handoff and indexes**

Update:

- `我给中本聪送外卖/交接.md`
- `我给中本聪送外卖/CLAUDE.md`
- `我给中本聪送外卖/设定/README.md`

- [ ] **Step 2: Commit final batch**

Run:

```bash
git status --short
git add docs/superpowers 我给中本聪送外卖
git commit -m "docs: score and optimize delivery novel for fanqie"
```
