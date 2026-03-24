#!/usr/bin/env python3
"""
Content Pipeline CLI for Stories about Bitcoin.

Commands:
    rewrite <chapter>              Rewrite a chapter using Director-Writer agents
    translate <chapter>            Translate a Chinese chapter to English
    score <chapter>                Score a chapter's quality (5 dimensions)
    sync <chapter>                 Sync chapter files to main repo
    batch <start> <end>            Run full pipeline for a range of chapters
    calendar [scan|show]           Show/update content calendar
    models [list|tiers]            Show available models and tiers

Examples:
    python -m scripts.content_pipeline.cli rewrite 5
    python -m scripts.content_pipeline.cli rewrite 5 --tier premium
    python -m scripts.content_pipeline.cli translate 5
    python -m scripts.content_pipeline.cli score 5
    python -m scripts.content_pipeline.cli sync 5 --commit
    python -m scripts.content_pipeline.cli batch 1 10 --tier default
    python -m scripts.content_pipeline.cli calendar scan
    python -m scripts.content_pipeline.cli models tiers
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Ensure the project root is in path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.content_pipeline import config
from scripts.content_pipeline.models import (
    get_tier, resolve_tier_models, list_models, list_tiers, estimate_cost,
)


def find_chapter_file(chapter_num: int) -> Path:
    """Find the source chapter file in the local repo."""
    # Search in 正文/ directory
    chapters_dir = config.CHAPTERS_DIR
    if chapters_dir.exists():
        for ext in ("*.txt", "*.md"):
            for f in chapters_dir.glob(ext):
                parts = f.stem.split("_")
                if parts and parts[0].isdigit() and int(parts[0]) == chapter_num:
                    return f

    # Search in main repo zh/
    zh_dir = config.MAIN_ZH_DIR
    if zh_dir.exists():
        for f in zh_dir.glob(f"{chapter_num:02d}_*.md"):
            return f

    return None


def cmd_rewrite(args):
    """Rewrite a chapter using the Director-Writer pipeline."""
    from scripts.content_pipeline.core import (
        create_client, HistoryManager, StyleManager, ThoughtsLibrary,
        StoryDirector, MingWriter, ChunkSummarizer,
    )
    from scripts.content_pipeline.calendar import update_chapter_status

    chapter_num = args.chapter
    tier_name = args.tier
    models = resolve_tier_models(tier_name)

    print(f"Rewriting chapter {chapter_num} (tier: {tier_name})")
    est = estimate_cost(tier_name, 15000, 5000)
    print(f"  Estimated cost: ~${est['total']:.2f}")

    # Find source material
    source_file = find_chapter_file(chapter_num)
    source_text = ""
    if source_file:
        with open(source_file, "r", encoding="utf-8") as f:
            source_text = f.read()
        print(f"  Source: {source_file.name} ({len(source_text)} chars)")
    else:
        print(f"  No source file found for chapter {chapter_num}")

    # Initialize — 根据后端选择创建 client
    from scripts.content_pipeline.core import ClaudeCodeClient
    backend = os.environ.get("REWRITE_BACKEND", "claude-code")
    print(f"  Backend: {backend}")

    if backend == "claude-code":
        # 使用 Claude Code Max 计划额度
        planner_client = ClaudeCodeClient(model="opus")
        writer_client = ClaudeCodeClient(model="opus")
        scorer_client = ClaudeCodeClient(model="opus")
        summarizer_client = ClaudeCodeClient(model="opus")
    else:
        client = create_client(backend="openrouter")
        planner_client = writer_client = scorer_client = summarizer_client = client

    update_chapter_status(chapter_num, "rewriting")

    # Load context (skip summarizer for speed unless --index flag)
    summarizer = None
    if args.rebuild_index:
        summarizer = ChunkSummarizer(summarizer_client, models["summarizer"])

    history_mgr = HistoryManager(summarizer=summarizer)
    style_mgr = StyleManager()
    thoughts_lib = ThoughtsLibrary()

    print("Loading knowledge base...")
    history_mgr.load_all_history()
    style_mgr.load()
    style_mgr.load_dna()
    thoughts_lib.load()

    # Director plans
    topic = args.topic or f"Chapter {chapter_num}"
    if source_text:
        # Extract title from source
        for line in source_text.split("\n")[:5]:
            if line.startswith("#"):
                topic = line.lstrip("# ").strip()
                break

    print(f"\nDirector planning: {topic}")
    director = StoryDirector(planner_client, models["director"])
    history_context = history_mgr.get_relevant_history(topic)
    thoughts = thoughts_lib.get_writing_guidance()

    plan = director.plan_chapter(topic, source_text[:4000], history_context, thoughts)
    if not plan:
        print("Director failed to produce a plan. Aborting.")
        return

    print(f"  Plan: {plan.get('title', 'untitled')}")
    print(f"  Emotion: {plan.get('core_emotion', '?')}")

    # Save plan
    config.REWRITE_OUTPUT.mkdir(parents=True, exist_ok=True)
    plan_path = config.REWRITE_OUTPUT / f"ch{chapter_num:02d}_plan.json"
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    # Writer drafts
    print(f"\nWriter drafting...")
    writer = MingWriter(writer_client, models["writer"])
    article = writer.write(plan, style_mgr.get_prompt())

    # Save output
    output_path = config.REWRITE_OUTPUT / f"ch{chapter_num:02d}_rewrite.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(article)

    print(f"\nChapter saved: {output_path}")
    print(f"Length: {len(article)} chars")
    print(f"Preview: {article[:200]}...")

    # Auto-score if requested
    if args.auto_score:
        print("\nAuto-scoring...")
        _score_text(scorer_client, models["scorer"], article, chapter_num)

    update_chapter_status(chapter_num, "scoring", {"rewrite_file": str(output_path)})


def cmd_translate(args):
    """Translate a Chinese chapter to English."""
    from scripts.content_pipeline.core import create_client
    from scripts.content_pipeline.translator import translate_chapter, save_translation
    from scripts.content_pipeline.calendar import update_chapter_status

    chapter_num = args.chapter
    tier_name = args.tier
    models = resolve_tier_models(tier_name)

    print(f"Translating chapter {chapter_num} (model: {models['translator']})")

    # Find Chinese source
    zh_text = ""
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            zh_text = f.read()
    else:
        # Check rewrite output first, then main repo
        rewrite_path = config.REWRITE_OUTPUT / f"ch{chapter_num:02d}_rewrite.md"
        if rewrite_path.exists():
            with open(rewrite_path, "r", encoding="utf-8") as f:
                zh_text = f.read()
            print(f"  Source: rewrite output")
        else:
            source_file = find_chapter_file(chapter_num)
            if source_file:
                with open(source_file, "r", encoding="utf-8") as f:
                    zh_text = f.read()
                print(f"  Source: {source_file.name}")

    if not zh_text:
        print(f"No Chinese source found for chapter {chapter_num}")
        return

    print(f"  Source length: {len(zh_text)} chars")
    update_chapter_status(chapter_num, "translating")

    client = create_client()
    translated, diff = translate_chapter(client, models["translator"], zh_text, chapter_num)

    output_path = save_translation(translated, diff, chapter_num)
    print(f"\nTranslation saved: {output_path}")
    print(f"Length: {len(translated)} chars")
    if diff:
        diff_lines = diff.count("\n")
        print(f"Diff against existing: {diff_lines} lines changed")

    update_chapter_status(chapter_num, "review", {"translation_file": str(output_path)})


def cmd_score(args):
    """Score a chapter's quality."""
    from scripts.content_pipeline.core import create_client
    from scripts.content_pipeline.calendar import update_chapter_status

    chapter_num = args.chapter
    tier_name = args.tier
    models = resolve_tier_models(tier_name)

    # Find text to score
    text = ""
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        rewrite_path = config.REWRITE_OUTPUT / f"ch{chapter_num:02d}_rewrite.md"
        if rewrite_path.exists():
            with open(rewrite_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            source_file = find_chapter_file(chapter_num)
            if source_file:
                with open(source_file, "r", encoding="utf-8") as f:
                    text = f.read()

    if not text:
        print(f"No text found to score for chapter {chapter_num}")
        return

    client = create_client()
    update_chapter_status(chapter_num, "scoring")
    result = _score_text(client, models["scorer"], text, chapter_num)

    if result.get("verdict") == "pass":
        print("\nVerdict: PASS — ready for translation")
        update_chapter_status(chapter_num, "translating", {"score": result["average"]})
    else:
        print(f"\nVerdict: NEEDS REVIEW (avg: {result.get('average', 0)})")
        update_chapter_status(chapter_num, "review", {"score": result.get("average", 0)})


def _score_text(client, model, text, chapter_num):
    """Internal scoring helper."""
    from scripts.content_pipeline.quality_scorer import score_chapter, format_score_report, save_score

    print(f"  Scoring with {model}...")
    result = score_chapter(client, model, text, chapter_num)
    save_score(result, chapter_num)

    report = format_score_report(result, f"Chapter {chapter_num}")
    print(report)
    return result


def _find_existing_filename(directory, chapter_num):
    """Find existing chapter filename in a directory (zh/ or en/)."""
    from pathlib import Path
    d = Path(directory)
    if not d.exists():
        return None
    # Match both zero-padded and non-padded
    for pattern in (f"{chapter_num:02d}_*.md", f"{chapter_num}_*.md"):
        matches = list(d.glob(pattern))
        if matches:
            return matches[0].name
    return None


def cmd_sync(args):
    """Sync chapter: build zh/ from 正文/, update feed/sitemap, optionally sync en/."""
    import subprocess as _sp
    from scripts.content_pipeline.publish import publish_chapter

    chapter_num = args.chapter

    # 1. 先运行 build_zh.py 重建 zh/
    print("Building zh/ from 正文/...")
    build_script = config.PROJECT_ROOT / "scripts" / "build_zh.py"
    _sp.run([sys.executable, str(build_script)], check=True)

    # 2. 找中文章节信息（用于 feed/sitemap）
    source = find_chapter_file(chapter_num)
    if not source:
        print(f"No source found for chapter {chapter_num}")
        return

    zh_text = source.read_text(encoding="utf-8")
    zh_filename = source.name
    zh_title = f"第{chapter_num}章"
    for line in zh_text.split("\n")[:5]:
        if line.startswith("#"):
            zh_title = line.lstrip("# ").strip()
            break

    # 3. 找英文翻译（可选）
    en_text = None
    en_filename = ""
    en_title = f"Chapter {chapter_num}"

    trans_path = config.TRANSLATION_OUTPUT / f"ch{chapter_num:02d}_en.md"
    if trans_path.exists():
        en_text = trans_path.read_text(encoding="utf-8")

    existing_en = _find_existing_filename(config.MAIN_EN_DIR, chapter_num)
    if existing_en:
        en_filename = existing_en
    elif en_text:
        for line in en_text.split("\n")[:5]:
            if line.startswith("#"):
                en_title = line.lstrip("# ").strip()
                break
        safe_en = en_title.lower().replace(" ", "_").replace(":", "").replace("'", "")
        safe_en = "".join(c for c in safe_en if c.isalnum() or c == "_")
        en_filename = f"{chapter_num:02d}_{safe_en}.md"
    else:
        en_filename = f"{chapter_num:02d}_chapter_{chapter_num}.md"

    publish_chapter(
        chapter_num=chapter_num,
        en_text=en_text,
        en_filename=en_filename,
        zh_filename=zh_filename,
        zh_title=zh_title,
        en_title=en_title,
        commit=args.commit,
    )

    if args.twitter:
        from scripts.content_pipeline.calendar import trigger_twitter_content
        trigger_twitter_content(chapter_num, "zh")
        trigger_twitter_content(chapter_num, "en")


def cmd_batch(args):
    """Run full pipeline for a range of chapters."""
    from scripts.content_pipeline.calendar import update_chapter_status

    start = args.start
    end = args.end
    tier_name = args.tier

    print(f"Batch pipeline: chapters {start}-{end} (tier: {tier_name})")
    est = estimate_cost(tier_name, 15000, 5000)
    total_est = est["total"] * (end - start + 1)
    print(f"  Estimated total cost: ~${total_est:.2f}")

    if not args.yes:
        confirm = input("  Proceed? [y/N] ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return

    results = []
    for ch_num in range(start, end + 1):
        print(f"\n{'='*60}")
        print(f"CHAPTER {ch_num}")
        print(f"{'='*60}")

        try:
            # Step 1: Rewrite
            args_rw = argparse.Namespace(
                chapter=ch_num, tier=tier_name, topic=None,
                rebuild_index=False, auto_score=True,
            )
            cmd_rewrite(args_rw)

            # Step 2: Check score
            score_path = config.SCORE_OUTPUT / f"score_ch{ch_num:02d}.json"
            if score_path.exists():
                with open(score_path, "r") as f:
                    score_data = json.load(f)
                if score_data.get("verdict") != "pass":
                    print(f"  Ch{ch_num}: Score too low ({score_data.get('average')}), skipping translation")
                    results.append({"chapter": ch_num, "status": "needs_review", "score": score_data.get("average")})
                    continue

            # Step 3: Translate
            args_tr = argparse.Namespace(
                chapter=ch_num, tier=tier_name, input=None,
            )
            cmd_translate(args_tr)

            # Step 4: Sync (without auto-commit in batch mode)
            if args.sync:
                args_sy = argparse.Namespace(
                    chapter=ch_num, commit=False, twitter=args.twitter,
                )
                cmd_sync(args_sy)

            results.append({"chapter": ch_num, "status": "completed"})

        except Exception as e:
            print(f"  Error processing chapter {ch_num}: {e}")
            results.append({"chapter": ch_num, "status": "error", "error": str(e)})

    # Summary
    print(f"\n{'='*60}")
    print("BATCH SUMMARY")
    print(f"{'='*60}")
    for r in results:
        print(f"  Ch.{r['chapter']:02d}: {r['status']}")


def cmd_calendar(args):
    """Show or update the content calendar."""
    from scripts.content_pipeline.calendar import (
        scan_existing_chapters, format_calendar_table, load_calendar,
    )

    action = args.action

    if action == "scan":
        print("Scanning repositories for chapter status...")
        cal = scan_existing_chapters()
        print(format_calendar_table(cal))
    elif action == "show":
        cal = load_calendar()
        print(format_calendar_table(cal))
    else:
        print(f"Unknown calendar action: {action}")
        print("Use: calendar scan | calendar show")


def cmd_models(args):
    """Show available models and tiers."""
    action = args.action

    if action == "list":
        list_models()
    elif action == "tiers":
        list_tiers()
    else:
        list_models()
        print()
        list_tiers()


def main():
    parser = argparse.ArgumentParser(
        description="Content Pipeline CLI for Stories about Bitcoin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # rewrite
    p_rewrite = subparsers.add_parser("rewrite", help="Rewrite a chapter")
    p_rewrite.add_argument("chapter", type=int, help="Chapter number")
    p_rewrite.add_argument("--tier", choices=["budget", "default", "premium"], default="default")
    p_rewrite.add_argument("--topic", type=str, default=None, help="Override topic")
    p_rewrite.add_argument("--rebuild-index", action="store_true", help="Rebuild history index")
    p_rewrite.add_argument("--auto-score", action="store_true", help="Auto-score after writing")

    # translate
    p_translate = subparsers.add_parser("translate", help="Translate chapter to English")
    p_translate.add_argument("chapter", type=int, help="Chapter number")
    p_translate.add_argument("--tier", choices=["budget", "default", "premium"], default="default")
    p_translate.add_argument("--input", type=str, default=None, help="Input file path")

    # score
    p_score = subparsers.add_parser("score", help="Score chapter quality")
    p_score.add_argument("chapter", type=int, help="Chapter number")
    p_score.add_argument("--tier", choices=["budget", "default", "premium"], default="default")
    p_score.add_argument("--input", type=str, default=None, help="Input file path")

    # sync
    p_sync = subparsers.add_parser("sync", help="Sync chapter to main repo")
    p_sync.add_argument("chapter", type=int, help="Chapter number")
    p_sync.add_argument("--commit", action="store_true", help="Auto git commit")
    p_sync.add_argument("--twitter", action="store_true", help="Generate Twitter content")

    # batch
    p_batch = subparsers.add_parser("batch", help="Run pipeline for chapter range")
    p_batch.add_argument("start", type=int, help="Start chapter number")
    p_batch.add_argument("end", type=int, help="End chapter number")
    p_batch.add_argument("--tier", choices=["budget", "default", "premium"], default="default")
    p_batch.add_argument("--sync", action="store_true", help="Auto-sync to main repo")
    p_batch.add_argument("--twitter", action="store_true", help="Generate Twitter content")
    p_batch.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")

    # calendar
    p_calendar = subparsers.add_parser("calendar", help="Content calendar")
    p_calendar.add_argument("action", nargs="?", default="show", choices=["scan", "show"])

    # models
    p_models = subparsers.add_parser("models", help="Show models and tiers")
    p_models.add_argument("action", nargs="?", default="list", choices=["list", "tiers"])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "rewrite": cmd_rewrite,
        "translate": cmd_translate,
        "score": cmd_score,
        "sync": cmd_sync,
        "batch": cmd_batch,
        "calendar": cmd_calendar,
        "models": cmd_models,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
