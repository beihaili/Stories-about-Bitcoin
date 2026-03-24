#!/usr/bin/env python3
"""CLI entry point for the Twitter content slicer.

Usage:
    python cli.py today                    # Today's 'on this day' events
    python cli.py today --date 2009-01-03  # Specific date
    python cli.py quotes 10               # 10 random quotes
    python cli.py quotes --satoshi         # Satoshi-only quotes
    python cli.py chapter 5               # Slice chapter 5
    python cli.py chapter all             # Slice all chapters
    python cli.py stories                 # All legendary stories
    python cli.py batch 30                # 30-day mixed content queue
"""

import argparse
import sys
import os
from datetime import date, timedelta

# Ensure imports work regardless of cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extractors.timeline_extractor import TimelineExtractor
from extractors.quote_extractor import QuoteExtractor
from extractors.chapter_slicer import ChapterSlicer
from extractors.story_extractor import StoryExtractor
from generators.tweet_generator import TweetGenerator
from generators.thread_generator import ThreadGenerator


def cmd_today(args):
    """Generate 'today in history' tweets."""
    extractor = TimelineExtractor()
    gen = TweetGenerator()

    if args.date:
        parts = args.date.split('-')
        month, day = int(parts[1]), int(parts[2])
    else:
        today = date.today()
        month, day = today.month, today.day

    events = extractor.get_events_for_date(month, day)

    if not events:
        print(f"No events found for {month:02d}-{day:02d}")
        # Try same month
        month_events = extractor.get_events_for_month(month)
        if month_events:
            print(f"Events in this month ({len(month_events)}):")
            for ev in month_events:
                d = f"{ev['day']:02d}" if ev['day'] else '??'
                print(f"  {month:02d}-{d}: {ev['title']}")
        return

    print(f"Found {len(events)} event(s) for {month:02d}-{day:02d}:\n")

    for i, ev in enumerate(events, 1):
        tweet_text = extractor.format_today_tweet(ev, lang=args.lang)
        filepath, count = gen.save_tweet(
            tweet_text,
            content_type='today_in_history',
            lang=args.lang,
            source=ev['source'],
            scheduled_date=args.date or date.today().isoformat(),
            seq=i,
        )
        print(f"[{i}] {ev['title']} ({ev['year']})")
        print(f"    → {filepath} ({count} chars)")
        print()


def cmd_quotes(args):
    """Generate quote tweets."""
    extractor = QuoteExtractor()
    gen = TweetGenerator()

    limit = args.count or 10
    quotes = extractor.get_all_quotes(
        limit=limit,
        satoshi_only=args.satoshi,
    )

    if not quotes:
        print("No quotes found")
        return

    print(f"Generating {len(quotes)} quote tweet(s):\n")

    for i, q in enumerate(quotes, 1):
        tweet_text = extractor.format_quote_tweet(q, lang=args.lang)
        filepath, count = gen.save_tweet(
            tweet_text,
            content_type='quote',
            lang=args.lang,
            source='quotes.json' if 'BitcoinTalk' in q['source'] else 'emails.json',
            seq=i,
        )
        print(f"[{i}] {q['author']}: {q['text'][:60]}...")
        print(f"    → {filepath} ({count} chars)")
        print()


def cmd_chapter(args):
    """Slice chapter(s) into tweets."""
    slicer = ChapterSlicer()
    gen = TweetGenerator()
    thread_gen = ThreadGenerator()

    if args.chapter_id == 'all':
        chapters = slicer.slice_all()
    else:
        chapter = slicer.slice_chapter(int(args.chapter_id))
        if not chapter:
            print(f"Chapter {args.chapter_id} not found")
            return
        chapters = [chapter]

    total_saved = 0
    for ch in chapters:
        num = ch['chapter_num']
        title = ch['title']
        print(f"\n=== Chapter {num}: {title} ===")
        print(f"  Hooks: {len(ch['hooks'])}, Dramatic: {len(ch['dramatic'])}, "
              f"Facts: {len(ch['facts'])}, Epigraphs: {len(ch['epigraphs'])}, "
              f"Climaxes: {len(ch['climaxes'])}")

        seq = 1

        # Save individual tweets for hooks
        for hook in ch['hooks'][:2]:
            tweet = slicer.format_chapter_tweet(hook, num, title, 'hook', args.lang)
            filepath, count = gen.save_tweet(
                tweet, content_type='chapter_hook', lang=args.lang,
                source=f'chapter_{num:02d}', seq=seq,
            )
            print(f"  [{seq}] hook → {os.path.basename(filepath)} ({count} chars)")
            seq += 1
            total_saved += 1

        # Save dramatic paragraphs
        for drama in ch['dramatic'][:2]:
            tweet = slicer.format_chapter_tweet(drama, num, title, 'drama', args.lang)
            filepath, count = gen.save_tweet(
                tweet, content_type='chapter_drama', lang=args.lang,
                source=f'chapter_{num:02d}', seq=seq,
            )
            print(f"  [{seq}] drama → {os.path.basename(filepath)} ({count} chars)")
            seq += 1
            total_saved += 1

        # Save epigraphs
        for ep in ch['epigraphs'][:1]:
            tweet = slicer.format_chapter_tweet(ep, num, title, 'epigraph', args.lang)
            filepath, count = gen.save_tweet(
                tweet, content_type='chapter_epigraph', lang=args.lang,
                source=f'chapter_{num:02d}', seq=seq,
            )
            print(f"  [{seq}] epigraph → {os.path.basename(filepath)} ({count} chars)")
            seq += 1
            total_saved += 1

        # Generate a thread from chapter
        thread_tweets = thread_gen.from_chapter_slices(ch, num, title, args.lang)
        if len(thread_tweets) >= 3:
            filepath = gen.save_thread(
                thread_tweets, content_type='chapter_thread', lang=args.lang,
                source=f'chapter_{num:02d}', seq=1,
            )
            print(f"  [T] thread ({len(thread_tweets)} tweets) → {os.path.basename(filepath)}")
            total_saved += 1

    print(f"\nTotal: {total_saved} content pieces saved")


def cmd_stories(args):
    """Generate tweets from legendary stories."""
    extractor = StoryExtractor()
    gen = TweetGenerator()

    stories = extractor.get_all_stories()
    if not stories:
        print("No stories found")
        return

    print(f"Processing {len(stories)} legendary stories:\n")

    for story in stories:
        sid = story['id']
        title = story['title']
        print(f"[{sid}] {title}")

        # Save single tweet
        tweet_text = story['single_tweet_zh'] if args.lang == 'zh' else story['single_tweet_en']
        filepath, count = gen.save_tweet(
            tweet_text, content_type='story', lang=args.lang,
            source='legendary_bitcoin_stories.json', seq=sid,
        )
        print(f"    single → {os.path.basename(filepath)} ({count} chars)")

        # Save thread
        thread = story.get('thread_zh', [])
        if len(thread) >= 2:
            filepath = gen.save_thread(
                thread, content_type='story_thread', lang=args.lang,
                source='legendary_bitcoin_stories.json', seq=sid,
            )
            print(f"    thread ({len(thread)} tweets) → {os.path.basename(filepath)}")


def cmd_batch(args):
    """Generate a mixed content queue for N days."""
    days = args.days or 30
    lang = args.lang

    timeline = TimelineExtractor()
    quotes = QuoteExtractor()
    slicer = ChapterSlicer()
    stories = StoryExtractor()
    gen = TweetGenerator()

    today = date.today()
    total = 0

    print(f"Generating {days}-day content queue starting from {today}:\n")

    # Pre-extract content pools
    all_quotes = quotes.get_all_quotes(limit=days)
    all_stories = stories.get_all_stories()
    chapter_count = slicer.get_chapter_count()

    for i in range(days):
        d = today + timedelta(days=i)
        d_str = d.isoformat()
        day_seq = 1

        print(f"--- {d_str} ---")

        # 1. Today in history (if available)
        events = timeline.get_events_for_date(d.month, d.day)
        for ev in events[:1]:
            tweet = timeline.format_today_tweet(ev, lang)
            gen.save_tweet(
                tweet, content_type='today_in_history', lang=lang,
                source=ev['source'], scheduled_date=d_str, seq=day_seq,
            )
            print(f"  [{day_seq}] today_in_history: {ev['title'][:40]}")
            day_seq += 1
            total += 1

        # 2. Quote (cycle through)
        if i < len(all_quotes):
            q = all_quotes[i]
            tweet = quotes.format_quote_tweet(q, lang)
            gen.save_tweet(
                tweet, content_type='quote', lang=lang,
                source='quotes.json', scheduled_date=d_str, seq=day_seq,
            )
            print(f"  [{day_seq}] quote: {q['author']}")
            day_seq += 1
            total += 1

        # 3. Chapter content (cycle through chapters)
        if chapter_count > 0:
            ch_num = (i % chapter_count)
            ch_data = slicer.slice_chapter(ch_num)
            if ch_data and ch_data['hooks']:
                tweet = slicer.format_chapter_tweet(
                    ch_data['hooks'][0], ch_data['chapter_num'],
                    ch_data['title'], 'hook', lang,
                )
                gen.save_tweet(
                    tweet, content_type='chapter_hook', lang=lang,
                    source=f'chapter_{ch_num:02d}', scheduled_date=d_str, seq=day_seq,
                )
                print(f"  [{day_seq}] chapter_hook: ch.{ch_num}")
                day_seq += 1
                total += 1

        # 4. Story (one per week)
        if i % 7 == 6 and i // 7 < len(all_stories):
            story = all_stories[i // 7]
            tweet = story['single_tweet_zh'] if lang == 'zh' else story['single_tweet_en']
            gen.save_tweet(
                tweet, content_type='story', lang=lang,
                source='legendary_bitcoin_stories.json',
                scheduled_date=d_str, seq=day_seq,
            )
            print(f"  [{day_seq}] story: {story['title'][:30]}")
            total += 1

    print(f"\nTotal: {total} content pieces generated for {days} days")


def main():
    parser = argparse.ArgumentParser(
        description='Twitter content slicer for 比特币那些事儿',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('--lang', default='zh', choices=['zh', 'en'],
                        help='Output language (default: zh)')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # today
    p_today = subparsers.add_parser('today', help='Generate "today in history" tweets')
    p_today.add_argument('--date', help='Specific date (YYYY-MM-DD)')

    # quotes
    p_quotes = subparsers.add_parser('quotes', help='Generate quote tweets')
    p_quotes.add_argument('count', nargs='?', type=int, default=10,
                          help='Number of quotes (default: 10)')
    p_quotes.add_argument('--satoshi', action='store_true',
                          help='Only Satoshi quotes')

    # chapter
    p_chapter = subparsers.add_parser('chapter', help='Slice chapter(s)')
    p_chapter.add_argument('chapter_id', help='Chapter number or "all"')

    # stories
    subparsers.add_parser('stories', help='Generate legendary story tweets')

    # batch
    p_batch = subparsers.add_parser('batch', help='Generate multi-day content queue')
    p_batch.add_argument('days', nargs='?', type=int, default=30,
                         help='Number of days (default: 30)')

    args = parser.parse_args()

    commands = {
        'today': cmd_today,
        'quotes': cmd_quotes,
        'chapter': cmd_chapter,
        'stories': cmd_stories,
        'batch': cmd_batch,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
