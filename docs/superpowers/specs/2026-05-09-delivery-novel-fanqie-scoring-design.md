# Delivery Novel Fanqie Scoring Design

**Goal:** Build a Fanqie recommendation-period scoring and editing system for the 43-chapter, 100k-character version of `我给中本聪送外卖`.

**Scope:** This design covers scoring, prioritization, and revision gates. It does not add chapter 44, change the ending, or explain the Satoshi account mechanism.

## Platform Basis

The scoring system is built around the current Fanqie recommendation workflow and the user's backend tip.

- Fanqie's 2026 workflow notice says long novels can enter a recommendation evaluation phase after reaching 80k words, then a 7-day small-flow validation period; after the validation period, works that reach 100k words enter normal recommendation, otherwise they remain in validation until reaching 100k.
- The same notice says authors may optimize content during validation by referring to chapter completion rate and chapter follow-reading rate.
- Fanqie's earlier recommendation notice also emphasizes checking content before starting recommendation, avoiding broken chapter order, and maintaining stable updates.
- Fanqie's author-level notice treats first recommendation launch and first 100k-word milestone as platform growth tasks, while warning against water content, repeated chapters, and improper data manipulation.

Sources:

- https://fanqienovel.com/writer/zone/article/7602553801446260761
- https://fanqienovel.com/writer/zone/article/7176537729709113401
- https://fanqienovel.com/writer/zone/article/7381822554836566078

## Design Decision

Use a Fanqie-specific 100-point rubric instead of the older literary eight-dimensional score.

The old rubric remains useful for story quality, but this pass optimizes for validation-period behavior: first-screen hook, chapter completion, next-chapter pull, emotional payoff, mobile pacing, continuity, and platform risk control.

The main acceptance rule is not "make every sentence more literary." The rule is:

```text
Readers should understand the pressure in the first screen, finish the chapter without lecture fatigue, and have a concrete reason to open the next chapter.
```

## Scoring Units

Create and maintain these files:

- `我给中本聪送外卖/设定/结构/番茄网文评分系统.md`
  - Canonical scoring rubric and hard caps.
- `我给中本聪送外卖/设定/结构/章节评分/43章番茄GPT55基线评分.md`
  - GPT-5.5 read-only baseline for the current 43 chapters.
- `我给中本聪送外卖/设定/结构/章节评分/43章番茄优化执行表.md`
  - Revision queue, batch rules, and chapter-level action list.
- `docs/superpowers/plans/2026-05-09-delivery-novel-fanqie-score-optimize.md`
  - Execution plan with verification commands.

## Revision Strategy

Work in this order:

1. Fix hard continuity faults before style polishing.
2. Improve chapter endings before rewriting large bodies.
3. Keep financial-risk guardrails intact.
4. Protect the 43-chapter ending and the 100k-word threshold.
5. Keep edits surgical unless a chapter has a structural fault.

## Known Baseline Result

The read-only GPT-5.5 baseline gives the book an approximate `86/100` Fanqie validation score.

Strongest section: chapters 28-35, because concrete money, concrete mistakes, and concrete stop-loss actions carry the reading.

Highest-risk section: chapter 42, because it conflicts with chapter 41's timeline. This must be fixed before broad polishing.

## Verification

After every substantive batch:

```bash
python3 scripts/export_fanqie_delivery.py --clean --target-initial-chars 100000
jq '{chapter_count,total_body_chars,ready_for_initial_submission,generated_at}' 发布/番茄/我给中本聪送外卖/manifest.json
jq -r '.chapters[-5:][] | [.number,.title,.body_chars] | @tsv' 发布/番茄/我给中本聪送外卖/manifest.json
git diff --check -- 我给中本聪送外卖 docs/superpowers
```

Completion requires:

- 43 chapters.
- At least 100000 body characters, preferably 103000-105000.
- Chapter 43 remains `这次是我自己接单`.
- No P0 continuity fault.
- No new investment advice, operation tutorial, or promised-return wording.
