# Delivery Novel Overnight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete a full reviewable draft of `我给中本聪送外卖` by adding chapters 31-37 with workflow artifacts, scoring, revision, export verification, and a local Git commit.

**Architecture:** Treat the novel directory as the source of truth. For each chapter, produce planning artifacts first, then正文, then independent review and score-driven rewrite. Keep generated publishing output under ignored `发布/`.

**Tech Stack:** Markdown source files, existing `scripts/export_fanqie_delivery.py`, Git.

---

### Task 1: Context And Facts

**Files:**
- Read: `我给中本聪送外卖/设定/结构/38章分工表.md`
- Read: `我给中本聪送外卖/设定/结构/AI写作工作流.md`
- Read: `我给中本聪送外卖/设定/结构/章节评分标准.md`
- Read: `正文/31_未来可期：信任再次破碎.md` through `正文/37_未来可期：光未熄灭.md`
- Update: `findings.md`

- [ ] Read the required project context and source chapters.
- [ ] Verify recent historical facts for chapters 31-35 from reliable sources.
- [ ] Record factual boundaries and artistic compression notes in `findings.md`.

### Task 2: Chapter Contracts And Beats

**Files:**
- Create: `我给中本聪送外卖/设定/结构/章节流程/31_信任再次破碎_章节合同.md`
- Create: `我给中本聪送外卖/设定/结构/章节流程/31_信任再次破碎_scene_beats.md`
- Repeat equivalent files for chapters 32-37.

- [ ] Write a chapter contract for each chapter.
- [ ] Write 6-10 actionable scene beats for each chapter.
- [ ] Check each contract contains a concrete returned-to-reality action.

### Task 3: Draft Chapters 31-37

**Files:**
- Create: `我给中本聪送外卖/正文/31_信任再次破碎.md`
- Create: `我给中本聪送外卖/正文/32_铭文风暴.md`
- Create: `我给中本聪送外卖/正文/33_ETF历史性突破.md`
- Create: `我给中本聪送外卖/正文/34_大选与战略储备.md`
- Create: `我给中本聪送外卖/正文/35_十万美元突破.md`
- Create: `我给中本聪送外卖/正文/36_缺席的人.md`
- Create: `我给中本聪送外卖/正文/37_光未熄灭.md`

- [ ] Draft each chapter from its contract and beats.
- [ ] Keep third-person limited perspective.
- [ ] Avoid Markdown headings inside正文.
- [ ] Ensure each chapter ends with action or emotional movement, not explanation.

### Task 4: Review, Score, Rewrite

**Files:**
- Create: `我给中本聪送外卖/设定/结构/章节流程/31_信任再次破碎_审稿.md`
- Repeat equivalent review files for chapters 32-37.
- Create: `我给中本聪送外卖/设定/结构/章节评分/31-37章评分报告.md`

- [ ] Review each chapter against continuity, rules,人物,物件, and chapter assignment.
- [ ] Score each chapter using the eight weighted dimensions.
- [ ] Rewrite chapters whose weakest dimension needs repair.
- [ ] Document the rewrite rationale in the review or scoring report.

### Task 5: Setting Backfill And Whole-Book Checks

**Files:**
- Create: `我给中本聪送外卖/设定/历史锚点/31_2022_FTX信任破碎.md`
- Create: `我给中本聪送外卖/设定/历史锚点/32_2023_铭文风暴.md`
- Create: `我给中本聪送外卖/设定/历史锚点/33_2024_ETF历史性突破.md`
- Create: `我给中本聪送外卖/设定/历史锚点/34_2024_大选与战略储备.md`
- Create: `我给中本聪送外卖/设定/历史锚点/35_2024_十万美元突破.md`
- Modify: `我给中本聪送外卖/设定/README.md`
- Modify: `我给中本聪送外卖/交接.md`

- [ ] Backfill history anchors and setting index.
- [ ] Check object回收 for `01_哈耶克签赠名单.md` and `02_密码朋克宣言打印稿.md`.
- [ ] Run whole-book continuity pass for A/B/C lines.
- [ ] Update handoff document with final state.

### Task 6: Export, Verify, Commit

**Files:**
- Generated ignored output: `发布/番茄/我给中本聪送外卖/`

- [ ] Run `python3 scripts/export_fanqie_delivery.py --dry-run`.
- [ ] Run `python3 scripts/export_fanqie_delivery.py --clean`.
- [ ] Run `git diff --check`.
- [ ] Confirm manifest has chapters 1-37 with no gaps.
- [ ] Stage source files only.
- [ ] Commit with message `feat: 完成外卖故事整本初稿`.
