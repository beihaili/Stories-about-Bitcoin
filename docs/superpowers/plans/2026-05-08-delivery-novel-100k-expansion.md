# Delivery Novel 100k Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `我给中本聪送外卖` from 80914 characters to at least 103000 characters while preserving the existing final chapter as the true ending.

**Architecture:** Insert six new middle-to-late chapters into the 26-41 range, then shift existing final chapters so the original ending becomes chapter 43. New chapters add concrete reality consequences for existing historical nodes instead of appending a weak after-ending.

**Tech Stack:** Markdown manuscript files, existing `scripts/export_fanqie_delivery.py` exporter, existing novel setting documents under `我给中本聪送外卖/设定/`.

---

### Task 1: Lock Expansion Framework

**Files:**
- Create: `我给中本聪送外卖/设定/结构/10万字扩写方案.md`
- Create: `我给中本聪送外卖/设定/结构/43章分工表.md`
- Modify: `我给中本聪送外卖/设定/README.md`
- Modify: `我给中本聪送外卖/交接.md`

- [ ] **Step 1: Write expansion scheme**

Record the 10.3-10.5 万 target, six insertion points, renumbering map, risk rules, and verification command.

- [ ] **Step 2: Write 43 chapter assignment table**

Create the updated chapter responsibility table. Preserve the original final function: chapter 43 remains active ordinary-order ending.

- [ ] **Step 3: Update setting index and handoff**

Point future writers from the old `38章分工表.md` to the new `43章分工表.md`. Keep the old file as historical background.

### Task 2: Add New Chapter Contracts and Beats

**Files:**
- Create: `我给中本聪送外卖/设定/结构/章节流程/27_陌生站点的第一天_章节合同.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/27_陌生站点的第一天_scene_beats.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/29_那笔钱没到账_章节合同.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/29_那笔钱没到账_scene_beats.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/31_退出的人_章节合同.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/31_退出的人_scene_beats.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/33_那条假地址_章节合同.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/33_那条假地址_scene_beats.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/37_免费工具被标价_章节合同.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/37_免费工具被标价_scene_beats.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/41_第一笔归还_章节合同.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/41_第一笔归还_scene_beats.md`

- [ ] **Step 1: Write six chapter contracts**

Each contract must state reality sting, historical or mechanism echo, Li Jue's misunderstanding, rewritten understanding, concrete action, account state, and risks.

- [ ] **Step 2: Write six scene beat files**

Each beat file must have 7-9 actionable beats with location, present characters, action, and emotional movement.

### Task 3: Reorder Manuscript Files

**Files:**
- Move: `我给中本聪送外卖/正文/27_一笔几秒钟的帮忙.md` -> `我给中本聪送外卖/正文/28_一笔几秒钟的帮忙.md`
- Move: `我给中本聪送外卖/正文/28_粗糙的试运行.md` -> `我给中本聪送外卖/正文/30_粗糙的试运行.md`
- Move: `我给中本聪送外卖/正文/29_钥匙也能锁门.md` -> `我给中本聪送外卖/正文/32_钥匙也能锁门.md`
- Move: `我给中本聪送外卖/正文/30_高息梦醒之后.md` -> `我给中本聪送外卖/正文/34_高息梦醒之后.md`
- Move: `我给中本聪送外卖/正文/31_不是你的钥匙.md` -> `我给中本聪送外卖/正文/35_不是你的钥匙.md`
- Move: `我给中本聪送外卖/正文/32_开源之后的噪音.md` -> `我给中本聪送外卖/正文/36_开源之后的噪音.md`
- Move: `我给中本聪送外卖/正文/33_最大的承认.md` -> `我给中本聪送外卖/正文/38_最大的承认.md`
- Move: `我给中本聪送外卖/正文/34_母亲终于听懂了.md` -> `我给中本聪送外卖/正文/39_母亲终于听懂了.md`
- Move: `我给中本聪送外卖/正文/35_十万美元也不是结局.md` -> `我给中本聪送外卖/正文/40_十万美元也不是结局.md`
- Move: `我给中本聪送外卖/正文/36_铁盒里的缺席者.md` -> `我给中本聪送外卖/正文/42_铁盒里的缺席者.md`
- Move: `我给中本聪送外卖/正文/37_这次是我自己接单.md` -> `我给中本聪送外卖/正文/43_这次是我自己接单.md`

- [ ] **Step 1: Move files from high number to low collision risk order**

Start from old 37 down to old 27 so existing filenames are not overwritten.

- [ ] **Step 2: Confirm sequence gaps**

Run:

```bash
find 我给中本聪送外卖/正文 -maxdepth 1 -type f -name '*.md' -print | sort
```

Expected gaps before writing: 27, 29, 31, 33, 37, 41.

### Task 4: Draft Six New Chapters

**Files:**
- Create: `我给中本聪送外卖/正文/27_陌生站点的第一天.md`
- Create: `我给中本聪送外卖/正文/29_那笔钱没到账.md`
- Create: `我给中本聪送外卖/正文/31_退出的人.md`
- Create: `我给中本聪送外卖/正文/33_那条假地址.md`
- Create: `我给中本聪送外卖/正文/37_免费工具被标价.md`
- Create: `我给中本聪送外卖/正文/41_第一笔归还.md`

- [ ] **Step 1: Draft chapter 27**

Target 3600-4000 characters. Focus on Zhao Qing's unfamiliar station and Li Jue's migration-version tool.

- [ ] **Step 2: Draft chapter 29**

Target 3500-3900 characters. Focus on a small payment not being trusted until both sides understand confirmation.

- [ ] **Step 3: Draft chapter 31**

Target 3600-4100 characters. Focus on the first withdrawals and trust cost after the mutual-aid pool's first fight.

- [ ] **Step 4: Draft chapter 33**

Target 3500-3900 characters. Focus on a fake donation address spreading after the Ukrainian address scene.

- [ ] **Step 5: Draft chapter 37**

Target 3700-4200 characters. Focus on free open-source work being repackaged into a paid course.

- [ ] **Step 6: Draft chapter 41**

Target 3800-4300 characters. Focus on the mutual-aid pool's first repayment after 100k and Li Jue refusing to turn price into identity.

### Task 5: Validate Export and Continuity

**Files:**
- Create: `我给中本聪送外卖/设定/结构/章节评分/10万字扩写验证报告.md`
- Generated: `发布/番茄/我给中本聪送外卖/manifest.json`

- [ ] **Step 1: Export Fanqie package**

Run:

```bash
python3 scripts/export_fanqie_delivery.py --clean --target-initial-chars 100000
```

Expected: `exported chapters: 43`, `total body chars` at least `103000`.

- [ ] **Step 2: Validate manifest**

Run:

```bash
jq '{chapter_count,total_body_chars,ready_for_initial_submission,generated_at}' 发布/番茄/我给中本聪送外卖/manifest.json
```

Expected: `chapter_count` is 43 and `ready_for_initial_submission` is true.

- [ ] **Step 3: Validate final chapter**

Run:

```bash
jq -r '.chapters[-2].title, .chapters[-1].title' 发布/番茄/我给中本聪送外卖/manifest.json
```

Expected:

```text
第042章 铁盒里的缺席者
第043章 这次是我自己接单
```

- [ ] **Step 4: Write validation report**

Record final chapter count, body character count, inserted chapter list, remaining risk terms, and continuity conclusion.
