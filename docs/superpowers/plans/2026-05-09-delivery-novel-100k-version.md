# Delivery Novel 100k Version Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current 43-chapter expansion of `我给中本聪送外卖` into a stable 100k+ Fanqie-ready version with enough word-count margin, clean continuity, and publishable risk posture.

**Architecture:** Keep the accepted structure: 43 chapters, mid-book insertions, original ending preserved as chapter 43. Do not add new chapters or extend the ending; use small targeted edits to thicken thin transitions, improve platform safety, and preserve emotional closure.

**Tech Stack:** Markdown manuscript files, existing Fanqie export script `scripts/export_fanqie_delivery.py`, `jq` manifest checks, git checkpoint commits.

---

## File Map

- Modify: `我给中本聪送外卖/正文/*.md`
  - Only targeted polish; no new chapters unless a later user request changes scope.
- Modify: `我给中本聪送外卖/设定/结构/10万字正式版计划.md`
  - Story-facing execution plan and acceptance criteria.
- Create: `我给中本聪送外卖/设定/结构/章节评分/10万字正式版通读审稿报告.md`
  - Continuity, pacing, risk, and word-count audit after edits.
- Modify: `我给中本聪送外卖/交接.md`
  - Update current status, validation command, and final word count after export.
- Optional Modify: `我给中本聪送外卖/设定/README.md`
  - Add the formal 100k plan/report links if new files are created.
- Generated, ignored: `发布/番茄/我给中本聪送外卖/`
  - Regenerated for verification, not committed unless project policy changes.

## Task 1: Baseline Audit

**Files:**
- Read: `发布/番茄/我给中本聪送外卖/manifest.json`
- Create: `我给中本聪送外卖/设定/结构/10万字正式版计划.md`
- Create: `我给中本聪送外卖/设定/结构/章节评分/10万字正式版通读审稿报告.md`

- [ ] **Step 1: Confirm current export baseline**

Run:

```bash
python3 scripts/export_fanqie_delivery.py --clean --target-initial-chars 100000
jq '{chapter_count,total_body_chars,ready_for_initial_submission,generated_at}' 发布/番茄/我给中本聪送外卖/manifest.json
```

Expected:

```text
chapter_count: 43
total_body_chars: >= 100000
ready_for_initial_submission: true
```

- [ ] **Step 2: Identify thin chapters and risk-heavy chapters**

Run:

```bash
jq -r '.chapters[] | [.number,.title,.body_chars,((.risk_terms // [])|join(","))] | @tsv' 发布/番茄/我给中本聪送外卖/manifest.json
```

Audit rules:

- Chapters under 1800 characters are candidates for small thickening only if the scene feels abrupt.
- Chapters with risk terms `收益`, `投资`, `买币`, `炒币`, `私下交易`, `洗钱`, `诈骗` need manual safety review.
- Final two chapters must stay compact unless continuity requires a small line-level bridge.

- [ ] **Step 3: Write the story-facing plan**

Create `我给中本聪送外卖/设定/结构/10万字正式版计划.md` with:

- target version definition;
- current baseline;
- exact edit candidates;
- no-go rules;
- validation commands;
- acceptance checklist.

## Task 2: Safe Word-Count Margin

**Files:**
- Modify candidate chapters only:
  - `我给中本聪送外卖/正文/18_给工具加一个退出键.md`
  - `我给中本聪送外卖/正文/21_把路线表交出去.md`
  - `我给中本聪送外卖/正文/26_换站点的人.md`
  - `我给中本聪送外卖/正文/28_一笔几秒钟的帮忙.md`
  - `我给中本聪送外卖/正文/30_粗糙的试运行.md`
  - `我给中本聪送外卖/正文/32_钥匙也能锁门.md`
  - `我给中本聪送外卖/正文/39_母亲终于听懂了.md`
  - `我给中本聪送外卖/正文/42_铁盒里的缺席者.md`
  - `我给中本聪送外卖/正文/43_这次是我自己接单.md`

- [ ] **Step 1: Add 1800-2500 characters total, not per chapter**

Target additions:

- 18: add a concrete “退出键” user-facing moment, 250-350 characters.
- 21: add one handoff consequence after route table release, 250-350 characters.
- 26: add one station-migration detail connecting to chapter 27, 250-350 characters.
- 28: add one “fast help still needs explanation” bridge into chapter 29, 250-350 characters.
- 30: add one rough trial-rule detail connecting to chapter 31, 250-350 characters.
- 32: add one address-verification discomfort detail connecting to chapter 33, 250-350 characters.
- 39: add one mother/practical-stability detail, 200-300 characters.
- 42 or 43: only add 100-200 characters if the final handoff feels too abrupt.

No new subplot. No new historical character. No financial tutorial.

- [ ] **Step 2: Export and check margin**

Run:

```bash
python3 scripts/export_fanqie_delivery.py --clean --target-initial-chars 100000
jq '{chapter_count,total_body_chars,ready_for_initial_submission}' 发布/番茄/我给中本聪送外卖/manifest.json
```

Expected:

```text
chapter_count: 43
total_body_chars: 103000-105000 preferred, never below 100000
ready_for_initial_submission: true
```

If the total is above 105000, do not cut unless pacing visibly worsens.

## Task 3: Continuity and Risk Pass

**Files:**
- Modify: affected chapters from Task 2 only.
- Create/Update: `我给中本聪送外卖/设定/结构/章节评分/10万字正式版通读审稿报告.md`

- [ ] **Step 1: Check structure continuity**

Checklist:

- 26 -> 27: migration theme becomes new station reality.
- 28 -> 29: fast payment becomes confirmation anxiety.
- 30 -> 31: rough trial becomes exit and public-account dispute.
- 32 -> 33: real address verification becomes fake-address spread.
- 36 -> 37: open-source noise becomes paid-course packaging.
- 40 -> 41 -> 42 -> 43: price high -> repayment ledger -> iron box -> active delivery.

- [ ] **Step 2: Check platform safety**

Risk rules:

- Keep “not investment advice” as behavior, not lecture.
- Use refusal scenes instead of disclaimer paragraphs.
- Preserve “不荐币、不承诺收益、不拉人头、不引导交易”.
- Do not add precise wallet operation tutorials.

- [ ] **Step 3: Write audit report**

Report must include:

- final chapter count and character count;
- edited chapter list;
- continuity result;
- risk-term result;
- final recommendation for Fanqie replacement/paste order.

## Task 4: Documentation and Handoff

**Files:**
- Modify: `我给中本聪送外卖/交接.md`
- Optional Modify: `我给中本聪送外卖/设定/README.md`

- [ ] **Step 1: Update handoff**

Record:

- current formal version date;
- final export statistics;
- active plan/report files;
- exact export command;
- note that chapter 43 remains final.

- [ ] **Step 2: Re-run checks**

Run:

```bash
python3 scripts/export_fanqie_delivery.py --clean --target-initial-chars 100000
git diff --check -- 我给中本聪送外卖 docs/superpowers/plans/2026-05-09-delivery-novel-100k-version.md
```

Expected:

- export succeeds;
- no whitespace errors;
- manifest still reports 43 chapters and `ready_for_initial_submission: true`.

- [ ] **Step 3: Commit**

Run:

```bash
git add 我给中本聪送外卖 docs/superpowers/plans/2026-05-09-delivery-novel-100k-version.md
git commit -m "docs: prepare delivery novel 100k version"
```

Only commit after final verification passes.
