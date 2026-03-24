"""Extract and compress legendary Bitcoin stories for tweets."""

import json
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STORIES_FILE


class StoryExtractor:
    """Compress legendary Bitcoin stories into single tweets and thread outlines."""

    def __init__(self):
        self.stories = []
        self._load_stories()

    def _load_stories(self):
        """Load legendary stories data."""
        if not os.path.exists(STORIES_FILE):
            return
        with open(STORIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.stories = data.get('legendary_bitcoin_stories', {}).get('stories', [])

    def get_story_count(self):
        return len(self.stories)

    def get_all_stories(self):
        """Get all stories with extracted tweet content."""
        results = []
        for story in self.stories:
            results.append(self._process_story(story))
        return results

    def get_story(self, story_id):
        """Get a specific story by ID."""
        for story in self.stories:
            if story.get('id') == story_id:
                return self._process_story(story)
        return None

    def _process_story(self, story):
        """Process a story into tweet-ready format."""
        title = story.get('title', '')
        english_title = story.get('english_title', '')
        date = story.get('date', story.get('period', story.get('timeline', '')))

        # Extract participants
        participants = [p.get('name', '') for p in story.get('participants', [])]

        # Extract key details
        details = story.get('story_details', {})
        significance = story.get('historical_significance', [])
        cultural = story.get('cultural_impact', {})

        # Build a single-tweet summary
        single_tweet_zh = self._compress_to_tweet_zh(title, date, details, significance)
        single_tweet_en = self._compress_to_tweet_en(english_title, date, details, significance)

        # Build thread outline
        thread_zh = self._build_thread_zh(title, date, participants, details, significance, cultural)

        return {
            'id': story.get('id'),
            'title': title,
            'english_title': english_title,
            'date': date,
            'participants': participants,
            'single_tweet_zh': single_tweet_zh,
            'single_tweet_en': single_tweet_en,
            'thread_zh': thread_zh,
        }

    def _compress_to_tweet_zh(self, title, date, details, significance):
        """Compress story to a single Chinese tweet."""
        parts = [f"🔥 {title}"]
        if date:
            parts.append(f"({date})")

        # Add the most striking detail
        for key in ['transaction_amount', 'total_loss', 'peak_value',
                     'current_value_2024', 'market_impact']:
            if key in details:
                parts.append(f"\n\n{details[key]}")
                break

        # Add first significance point
        if significance:
            parts.append(f"\n\n💡 {significance[0]}")

        return ' '.join(parts[:2]) + ''.join(parts[2:])

    def _compress_to_tweet_en(self, title, date, details, significance):
        """Compress story to a single English tweet."""
        parts = [f"🔥 {title}"]
        if date:
            parts.append(f"({date})")

        for key in ['transaction_amount', 'total_loss', 'peak_value',
                     'current_value_2024', 'market_impact']:
            if key in details:
                parts.append(f"\n\n{details[key]}")
                break

        if significance:
            parts.append(f"\n\n💡 {significance[0]}")

        return ' '.join(parts[:2]) + ''.join(parts[2:])

    def _build_thread_zh(self, title, date, participants, details, significance, cultural):
        """Build a tweet thread (3-6 tweets) from a story."""
        thread = []

        # Tweet 1: Hook
        hook = f"🧵 {title}"
        if date:
            hook += f" ({date})"
        hook += "\n\n这是比特币历史上最传奇的故事之一。"
        if participants:
            hook += f"\n\n主角：{', '.join(participants[:3])}"
        thread.append(hook)

        # Tweet 2: Key details
        detail_lines = []
        for key, val in details.items():
            if isinstance(val, str) and len(val) < 100:
                detail_lines.append(f"• {val}")
            if len(detail_lines) >= 4:
                break
        if detail_lines:
            thread.append("📊 关键数据\n\n" + '\n'.join(detail_lines))

        # Tweet 3: Significance
        if significance:
            sig_text = "💡 历史意义\n\n"
            for s in significance[:3]:
                sig_text += f"• {s}\n"
            thread.append(sig_text.strip())

        # Tweet 4: Cultural impact (if available)
        if cultural:
            impact_lines = []
            for key, val in cultural.items():
                if isinstance(val, str) and len(val) < 100:
                    impact_lines.append(f"• {val}")
                elif isinstance(val, list):
                    for item in val[:2]:
                        if isinstance(item, str):
                            impact_lines.append(f"• {item}")
            if impact_lines:
                thread.append("🌍 文化影响\n\n" + '\n'.join(impact_lines[:4]))

        return thread
