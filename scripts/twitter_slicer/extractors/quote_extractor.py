"""Extract quotable content from Satoshi's forum posts and emails."""

import json
import re
import os

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import QUOTES_FILE, EMAILS_FILE, PRIORITY_AUTHORS


class QuoteExtractor:
    """Extracts impactful single-sentence quotes from forum posts and emails."""

    def __init__(self):
        self.quotes = []
        self.emails = []
        self._load_quotes()
        self._load_emails()

    def _load_quotes(self):
        """Load forum post quotes."""
        if not os.path.exists(QUOTES_FILE):
            return
        with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
            self.quotes = json.load(f)

    def _load_emails(self):
        """Load email archive."""
        if not os.path.exists(EMAILS_FILE):
            return
        with open(EMAILS_FILE, 'r', encoding='utf-8') as f:
            self.emails = json.load(f)

    def get_forum_quotes(self, limit=None, satoshi_only=False):
        """Get formatted forum quotes, prioritized by impact."""
        results = []
        for q in self.quotes:
            text = q.get('text', '').strip()
            if not text:
                continue
            # All quotes in this file are from Satoshi (forum posts)
            results.append({
                'text': text,
                'author': 'Satoshi Nakamoto',
                'date': q.get('date', ''),
                'source': f"BitcoinTalk #{q.get('post_id', '')}",
                'categories': q.get('categories', []),
                'char_count': len(text),
            })

        # Sort by length (shorter quotes are punchier) then by date
        results.sort(key=lambda x: (x['char_count'], x['date']))

        if limit:
            results = results[:limit]
        return results

    def get_email_quotes(self, limit=None, satoshi_only=False):
        """Extract quotable sentences from emails."""
        results = []
        for email in self.emails:
            if satoshi_only and email.get('sent_from') != 'Satoshi Nakamoto':
                continue

            sentences = self._extract_quotable_sentences(email.get('text', ''))
            if not sentences:
                continue

            # Parse date
            date_str = email.get('date', '')
            if 'T' in date_str:
                date_str = date_str.split('T')[0]

            author = email.get('sent_from', 'Unknown')
            is_priority = author in PRIORITY_AUTHORS

            for sentence in sentences:
                results.append({
                    'text': sentence,
                    'author': author,
                    'date': date_str,
                    'source': f"Email: {email.get('subject', '')}",
                    'source_url': email.get('url', ''),
                    'is_priority': is_priority,
                    'char_count': len(sentence),
                })

        # Priority authors first, then sort by length
        results.sort(key=lambda x: (not x['is_priority'], x['char_count']))

        if limit:
            results = results[:limit]
        return results

    def get_all_quotes(self, limit=None, satoshi_only=False):
        """Get combined quotes from forum posts and emails."""
        forum = self.get_forum_quotes(satoshi_only=satoshi_only)
        email = self.get_email_quotes(satoshi_only=satoshi_only)

        combined = forum + email
        # Prioritize: Satoshi > Hal Finney > others, then shorter
        combined.sort(key=lambda x: (
            0 if x['author'] == 'Satoshi Nakamoto' else
            1 if x['author'] == 'Hal Finney' else 2,
            x['char_count'],
        ))

        if limit:
            combined = combined[:limit]
        return combined

    def get_quotes_for_date(self, month, day):
        """Get quotes matching a specific MM-DD for date-based content."""
        results = []
        for q in self.get_all_quotes():
            if not q['date']:
                continue
            parts = q['date'].split('-')
            if len(parts) >= 3:
                q_month, q_day = int(parts[1]), int(parts[2])
                if q_month == month and q_day == day:
                    results.append(q)
        return results

    @staticmethod
    def _extract_quotable_sentences(text):
        """Find the most quotable sentences from email body text."""
        if not text:
            return []

        # Clean: remove quoted text (lines starting with >)
        lines = text.split('\n')
        clean_lines = [l for l in lines if not l.strip().startswith('>')]
        clean_text = ' '.join(clean_lines)

        # Remove URLs, email signatures, mailing list footers
        clean_text = re.sub(r'http\S+', '', clean_text)
        clean_text = re.sub(r'-{5,}.*', '', clean_text)
        clean_text = re.sub(r'Satoshi Nakamoto\s*$', '', clean_text.strip())

        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)

        # Filter: keep sentences that are impactful
        keywords = [
            'freedom', 'trust', 'privacy', 'decentrali', 'peer-to-peer',
            'electronic cash', 'proof-of-work', 'double-spending',
            'anonymous', 'government', 'bank', 'inflation', 'censorship',
            'network', 'transaction', 'blockchain', 'mining', 'node',
            'bitcoin', 'coin', 'secure', 'solution', 'problem',
        ]

        quotable = []
        for s in sentences:
            s = s.strip()
            if len(s) < 30 or len(s) > 280:
                continue
            # Must contain at least one keyword
            lower = s.lower()
            if any(kw in lower for kw in keywords):
                quotable.append(s)

        # Return top 3 shortest (punchiest)
        quotable.sort(key=len)
        return quotable[:3]

    def format_quote_tweet(self, quote, lang='zh'):
        """Format a quote as a tweet."""
        author = quote['author']
        date_str = quote['date']

        if lang == 'zh':
            header = f'💬 {author}'
            if date_str:
                header += f' ({date_str})'
            body = f'\n\n"{quote["text"]}"'
            footer = f'\n\n📍 {quote["source"]}'
        else:
            header = f'💬 {author}'
            if date_str:
                header += f' ({date_str})'
            body = f'\n\n"{quote["text"]}"'
            footer = f'\n\n📍 {quote["source"]}'

        return header + body + footer
