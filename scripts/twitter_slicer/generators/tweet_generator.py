"""Format and validate individual tweets."""

import os
from datetime import date

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    MAX_TWEET_CHARS, MAX_TWEET_CHARS_ZH,
    HASHTAGS_ZH, HASHTAGS_EN, CONTENT_TYPES, QUEUE_DIR,
)


class TweetGenerator:
    """Formats raw content into tweet-ready markdown with frontmatter."""

    @staticmethod
    def add_hashtags(text, lang='zh'):
        """Add hashtags to tweet text if they fit."""
        tags = HASHTAGS_ZH if lang == 'zh' else HASHTAGS_EN
        tag_str = ' '.join(tags)
        limit = MAX_TWEET_CHARS_ZH if lang == 'zh' else MAX_TWEET_CHARS

        if len(text) + len(tag_str) + 1 <= limit:
            return text + '\n' + tag_str
        # Try with fewer tags
        for n in range(len(tags), 0, -1):
            partial = ' '.join(tags[:n])
            if len(text) + len(partial) + 1 <= limit:
                return text + '\n' + partial
        return text

    @staticmethod
    def char_count(text):
        """Count characters for tweet length check."""
        return len(text)

    @staticmethod
    def is_within_limit(text, lang='zh'):
        """Check if tweet text fits within character limit."""
        limit = MAX_TWEET_CHARS_ZH if lang == 'zh' else MAX_TWEET_CHARS
        return len(text) <= limit

    @staticmethod
    def truncate(text, limit=280):
        """Truncate text to fit limit, adding ellipsis."""
        if len(text) <= limit:
            return text
        return text[:limit - 3] + '...'

    @staticmethod
    def format_frontmatter(content_type, lang='zh', source='', scheduled_date=None,
                           char_count=0, extra=None):
        """Generate YAML frontmatter for a tweet file."""
        d = scheduled_date or date.today().isoformat()
        lines = [
            '---',
            'type: single_tweet',
            f'lang: {lang}',
            f'content_type: {content_type}',
            f'source: {source}',
            f'scheduled_date: {d}',
            f'char_count: {char_count}',
            'status: pending',
        ]
        if extra:
            for k, v in extra.items():
                lines.append(f'{k}: {v}')
        lines.append('---')
        return '\n'.join(lines)

    @classmethod
    def save_tweet(cls, text, content_type, lang='zh', source='',
                   scheduled_date=None, seq=1):
        """Save a formatted tweet to the queue directory."""
        d = scheduled_date or date.today().isoformat()
        text_with_tags = cls.add_hashtags(text, lang)
        count = cls.char_count(text_with_tags)

        frontmatter = cls.format_frontmatter(
            content_type=content_type,
            lang=lang,
            source=source,
            scheduled_date=d,
            char_count=count,
        )

        content = f"{frontmatter}\n\n{text_with_tags}\n"

        os.makedirs(QUEUE_DIR, exist_ok=True)
        filename = f"{d}_{content_type}_{lang}_{seq:02d}.md"
        filepath = os.path.join(QUEUE_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath, count

    @classmethod
    def save_thread(cls, tweets, content_type, lang='zh', source='',
                    scheduled_date=None, seq=1):
        """Save a tweet thread to the queue directory."""
        d = scheduled_date or date.today().isoformat()

        lines = ['---', 'type: thread', f'lang: {lang}',
                 f'content_type: {content_type}', f'source: {source}',
                 f'scheduled_date: {d}', f'tweet_count: {len(tweets)}',
                 'status: pending', '---', '']

        for i, tweet in enumerate(tweets, 1):
            tagged = cls.add_hashtags(tweet, lang) if i == len(tweets) else tweet
            lines.append(f'### Tweet {i}/{len(tweets)}')
            lines.append('')
            lines.append(tagged)
            lines.append('')
            lines.append(f'> {cls.char_count(tagged)} chars')
            lines.append('')

        os.makedirs(QUEUE_DIR, exist_ok=True)
        filename = f"{d}_{content_type}_thread_{lang}_{seq:02d}.md"
        filepath = os.path.join(QUEUE_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return filepath
