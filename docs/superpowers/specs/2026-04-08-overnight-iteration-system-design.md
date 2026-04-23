# Overnight Iteration System — Design Spec

**Date**: 2026-04-08
**Status**: Approved
**Goal**: Build an autonomous overnight system that continuously improves code quality and chapter content, producing isolated PRs for morning review.

---

## 1. Problem Statement

The project has two improvement surfaces — React/Python code and 38 chapters of content — both with existing tooling (lint, tests, quality scoring) but no automated iteration loop. The user has abundant Claude Code tokens and wants a system that works overnight, producing reviewable PRs by morning.

## 2. Requirements

- **Scope**: Code (React website + Python scripts) AND content (chapter quality)
- **Review model**: Each improvement in an isolated git worktree, delivered as a GitHub PR
- **Task source**: Fully automatic — system scans for problems and prioritizes them
- **Stop condition**: Fixed N rounds (configurable, default 20)
- **Priority**: Rotating — odd rounds = code, even rounds = content
- **Runtime**: Local Mac, started before sleep, uses `caffeinate` to prevent sleep
- **Safety**: Never touches main branch directly; all changes via PR

## 3. Architecture

```
scripts/overnight/
├── __main__.py        # Entry point + caffeinate wrapper
├── config.py          # Rounds, timeout, repo paths
├── scanner.py         # Phase 1: scan code + content → findings.md
├── planner.py         # Phase 2: prioritize findings → task_plan.md
├── executor.py        # Phase 3: execute rounds in worktrees
├── reporter.py        # Phase 4: generate morning report → progress.md
└── runs/              # Per-night output directory
    └── YYYY-MM-DD/
        ├── findings.md
        ├── task_plan.md
        └── progress.md
```

### Phase 1: Scanning (`scanner.py`)

Collects quality signals from both code and content.

**Code signals:**

| Signal | Tool | Output |
|--------|------|--------|
| JS lint errors | `npm run lint` | Error count + file list |
| Test coverage gaps | `npx vitest --coverage` | Uncovered files/functions |
| Python lint | `ruff check scripts/` | Warning list |
| Missing tests | Compare `src/components/` vs `__tests__/` | Components without tests |

**Content signals:**

| Signal | Tool | Output |
|--------|------|--------|
| Chapter quality scores | `make score-all` (5-dimension scoring) | Per-chapter JSON |
| Lowest-scoring chapters | Sort by average, take bottom N | Chapters to refine |
| Weakest dimensions | Per-chapter min dimension | Targeted improvement areas |

Output: `findings.md` — a ranked list of all discovered issues with severity scores.

### Phase 2: Planning (`planner.py`)

Reads `findings.md` and generates `task_plan.md` with interleaved code/content tasks.

**Task types:**

| Type | Trigger | Execution | Verification |
|------|---------|-----------|-------------|
| `pipeline-fix` | Known bugs in scoring/rewrite pipeline | Fix pipeline code | Pipeline runs without error |
| `code-lint` | Lint errors exist | Fix lint errors | `npm run lint` passes |
| `code-test` | Component has no tests | Add unit tests | Tests pass + coverage increases |
| `code-refactor` | High complexity / duplication | Refactor | All existing tests pass |
| `content-refine` | Dimension score < 7 | Targeted refinement (NOT full rewrite) | Dimension score improves |

**Priority rules:**
1. Round 1 always runs `pipeline-fix` if known issues exist (fix the tools first)
2. Odd rounds: code tasks, sorted by severity (lint > missing tests > refactor)
3. Even rounds: content tasks, sorted by lowest score first
4. Within content: target the single weakest dimension per chapter

**task_plan.md format:**

```markdown
# Overnight Task Plan — 2026-04-08

## Round 1 — pipeline-fix
- **target**: scripts/content_pipeline/quality_scorer.py
- **issue**: score_chapter() uses OpenAI API format, incompatible with ClaudeCodeClient
- **action**: Add ClaudeCodeClient support to score_chapter
- **verify**: `python -m scripts.content_pipeline.cli score 1` succeeds
- **status**: pending

## Round 2 — content-refine
- **target**: 正文/11_风起云涌：第一次泡沫.md
- **issue**: readability: 5/10
- **weaknesses**: ["段落长度单一", "开头缺乏画面感"]
- **suggestions**: ["增加句式变化", "用具体场景开头"]
- **action**: Refine for readability only, preserve all other aspects
- **verify**: readability score improves (currently 5)
- **status**: pending
```

### Phase 3: Execution (`executor.py`)

Processes each round sequentially:

```
for round in task_plan:
    0. Startup cleanup (first round only):
       git worktree list | grep overnight-wt | awk '{print $1}' → remove each
       git branch --list 'overnight/*' → delete local-only branches from previous runs

    1. Create worktree (always branch from main):
       git worktree add ../overnight-wt-{N} -b overnight/round-{N}-{slug} main

    2. Build prompt:
       - Task description from task_plan.md
       - Pre-read relevant file contents
       - Verification criteria
       - "Only modify the specified files. Do not touch unrelated code."

    3. Run Claude:
       claude -p --model opus --cwd <worktree_path> \
         --output-format text --no-session-persistence \
         --allowedTools "Edit,Write,Read,Glob,Grep,Bash(npm run lint),Bash(npx vitest),Bash(ruff check)"
       (stdin: the built prompt, timeout: 15 minutes)
       Tool restrictions prevent Claude from accessing browser, network, or files outside worktree.

    4. Verify:
       - code-lint → run lint, check 0 errors
       - code-test → run tests, check pass + coverage delta
       - code-refactor → run existing tests, check all pass
       - content-refine → re-score chapter, check target dimension improved
       - pipeline-fix → run the pipeline command, check no error

    5. If verified:
       git add + commit + push
       gh pr create --title "overnight: {description}" --body "..."
       Record success in progress.md

    6. If failed:
       Record failure reason in progress.md
       For content: if score decreased, discard changes entirely

    7. Cleanup:
       git worktree remove ../overnight-wt-{N}
```

**Content refinement prompt template:**

```
你是《比特币那些事儿》的精修编辑。

这一章的质量评分如下：
{score_json}

最弱维度: {weakest_dimension} ({score}/10)
具体问题: {weaknesses}
改进建议: {suggestions}

请只针对上述问题修订章节，不要重写整章。规则：
1. 保留原文的事实内容和叙事结构
2. 只改进 {weakest_dimension} 相关的问题
3. 修改幅度控制在原文的 20% 以内
4. 输出完整的修订后章节（Markdown 格式）

【原文】
{chapter_text}
```

**Content backup**: Before any content modification, copy the original to `正文/历史版本/YYYY-MM-DD_chNN_pre-overnight.md`.

### Phase 4: Morning Report (`reporter.py`)

Generates the top section of `progress.md`:

```markdown
# Overnight Run — 2026-04-08
Started: 23:30 | Finished: 06:12 | Rounds: 20/20

## Summary
- Completed: 14
- Failed: 4
- Timeout: 2
- Code PRs: 7 | Content PRs: 7

## Results

| # | Type | Target | Result | PR | Delta |
|---|------|--------|--------|----|-------|
| 1 | pipeline-fix | score_chapter compat | pass | #42 | — |
| 2 | content-refine | Ch.11 readability | pass | #43 | 5.2→7.1 |
| 3 | code-test | ChapterCard.jsx | pass | #44 | 0%→89% |
| 4 | content-refine | Ch.17 style | fail | — | 6.0→5.8 |

## Failed Tasks
### Round 4: Ch.17 style_consistency
- Reason: Score decreased after refinement (6.0 → 5.8)
- Suggestion: May need human guidance on tonal direction

## Suggestions for Next Run
- Ch.17 style needs manual input before retrying
- 3 React components still lack tests
- Ch.22, Ch.30 readability still below 7
```

## 4. CLI Interface

```bash
# Standard overnight run
python -m scripts.overnight --rounds 20

# Options
python -m scripts.overnight --rounds 30 --timeout 900
python -m scripts.overnight --rounds 10 --code-only
python -m scripts.overnight --rounds 10 --content-only
python -m scripts.overnight --dry-run          # Scan + plan only, no execution
python -m scripts.overnight --resume            # Resume from last incomplete run
```

**`--resume` semantics**: Finds the most recent `runs/YYYY-MM-DD/task_plan.md`, reads the status of each round. Skips rounds marked `done` or `failed`, resumes from the first `pending` round. If `findings.md` is older than 1 hour, re-runs the scan phase to refresh it.

The `__main__.py` entry point wraps itself with `caffeinate -i` on macOS to prevent system sleep.

## 5. Prerequisites

- `claude` CLI in PATH with active Max plan
- `gh` CLI authenticated (`gh auth status` verified at startup)
- `node`, `npm` in PATH (for website lint/test)
- `ruff` installed (for Python lint)
- macOS with `caffeinate` available

## 6. Safety Mechanisms

1. **Branch isolation**: All changes on `overnight/*` branches, always branched from main
2. **Worktree isolation**: Each round works in a separate worktree directory
3. **Crash cleanup**: On startup, prune orphaned worktrees and branches from previous failed runs
4. **Tool restrictions**: Claude CLI invoked with `--allowedTools` whitelist — no browser, no network, no arbitrary shell
5. **Regression detection**: Content score must improve; if it decreases, changes are discarded
6. **Test gate**: Code changes must pass all existing tests
7. **Single-file principle**: Each PR targets one file/component for easy review
8. **Content backup**: Original chapters backed up to `历史版本/` before modification
9. **Timeout**: 15-minute per-round limit prevents infinite loops
10. **No auto-merge**: All changes delivered as PRs; human merges manually
11. **Disk guard**: Skip round if available disk < 1GB (worktrees with node_modules can be large)

## 6. Known Limitations

- **Serial execution**: One round at a time (could be parallelized in v2)
- **Claude CLI dependency**: Requires `claude` command available in PATH
- **Scoring accuracy**: LLM-based scoring is subjective; score improvements are directional, not absolute
- **Prompt-only modifications**: Claude works via single prompt per round; complex refactors spanning multiple files may need multiple rounds

## 7. First-Run Bootstrap Tasks

The system's first run will prioritize fixing the content pipeline itself:

1. Fix `score_chapter()` to support `ClaudeCodeClient` (currently only works with OpenAI-compatible API)
2. Replace `chapter_text[:12000]` hard truncation with chunked scoring
3. Save structured scoring feedback (weaknesses/suggestions) as JSON for downstream use

These fixes ensure subsequent content-refine rounds use a working, improved pipeline.

## 8. File Locations

- System code: `scripts/overnight/`
- Run outputs: `scripts/overnight/runs/YYYY-MM-DD/`
- Content backups: `正文/历史版本/`
- PR branches: `overnight/round-{N}-{slug}`
