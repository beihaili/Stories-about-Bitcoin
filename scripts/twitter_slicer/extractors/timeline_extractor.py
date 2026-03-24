"""Extract 'Today in History' events from timeline data."""

import json
import re
from datetime import datetime
from dateutil import parser as dateparser

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import COMPREHENSIVE_TIMELINE, COMPLETE_TIMELINE


class TimelineExtractor:
    """Extracts timeline events and matches them to specific dates (MM-DD)."""

    def __init__(self):
        self.events = []
        self._load_comprehensive_timeline()
        self._load_complete_timeline()

    def _load_comprehensive_timeline(self):
        """Load detailed_events from comprehensive_timeline.json."""
        if not os.path.exists(COMPREHENSIVE_TIMELINE):
            return
        with open(COMPREHENSIVE_TIMELINE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for ev in data.get('comprehensive_bitcoin_timeline', {}).get('detailed_events', []):
            parsed = self._parse_event(ev, source='comprehensive_timeline.json')
            if parsed:
                self.events.append(parsed)

    def _load_complete_timeline(self):
        """Load events from bitcoin_complete_timeline.json (nested by period)."""
        if not os.path.exists(COMPLETE_TIMELINE):
            return
        with open(COMPLETE_TIMELINE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for period in data.get('bitcoin_complete_timeline', {}).get('periods', []):
            for ev in period.get('events', []):
                parsed = self._parse_event_v2(ev, source='bitcoin_complete_timeline.json')
                if parsed:
                    # Deduplicate: skip if same date+title already exists
                    key = (parsed['month'], parsed['day'], parsed['title'][:20])
                    existing_keys = {
                        (e['month'], e['day'], e['title'][:20]) for e in self.events
                    }
                    if key not in existing_keys:
                        self.events.append(parsed)

    def _parse_date(self, date_str):
        """Parse various date formats. Returns (year, month, day) or partial tuple."""
        if not date_str:
            return None, None, None

        date_str = str(date_str).strip()

        # Year range: "2015-2016"
        if re.match(r'^\d{4}-\d{4}$', date_str):
            return int(date_str[:4]), None, None

        # Year only: "1976"
        if re.match(r'^\d{4}$', date_str):
            return int(date_str), None, None

        # Year-month: "2009-10"
        m = re.match(r'^(\d{4})-(\d{1,2})$', date_str)
        if m:
            return int(m.group(1)), int(m.group(2)), None

        # Full date: "2009-01-03" or "2009-01-03 18:15:05"
        m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', date_str)
        if m:
            return int(m.group(1)), int(m.group(2)), int(m.group(3))

        # ISO 8601: "2008-10-31T18:10:00Z"
        try:
            dt = dateparser.parse(date_str)
            return dt.year, dt.month, dt.day
        except (ValueError, TypeError):
            return None, None, None

    def _parse_event(self, ev, source):
        """Parse a comprehensive_timeline event."""
        year, month, day = self._parse_date(ev.get('date', ''))
        if year is None:
            return None
        return {
            'year': year,
            'month': month,
            'day': day,
            'title': ev.get('title', ''),
            'description': ev.get('description', ''),
            'significance': ev.get('significance', ''),
            'category': ev.get('category', ''),
            'key_quotes': ev.get('key_quotes', []),
            'source': source,
        }

    def _parse_event_v2(self, ev, source):
        """Parse a bitcoin_complete_timeline event (uses 'event' instead of 'title')."""
        year, month, day = self._parse_date(ev.get('date', ''))
        if year is None:
            return None
        return {
            'year': year,
            'month': month,
            'day': day,
            'title': ev.get('event', ''),
            'description': ev.get('description', ''),
            'significance': ev.get('significance', ''),
            'category': '',
            'key_quotes': [],
            'source': source,
        }

    def get_events_for_date(self, month, day):
        """Get all events matching a specific MM-DD."""
        results = []
        for ev in self.events:
            if ev['month'] == month and ev['day'] == day:
                results.append(ev)
        return sorted(results, key=lambda e: e['year'])

    def get_events_for_month(self, month):
        """Get all events in a specific month (for monthly planning)."""
        results = []
        for ev in self.events:
            if ev['month'] == month:
                results.append(ev)
        return sorted(results, key=lambda e: (e['year'], e['day'] or 0))

    def get_all_dated_events(self):
        """Get all events that have at least month+day info."""
        return sorted(
            [ev for ev in self.events if ev['month'] and ev['day']],
            key=lambda e: (e['month'], e['day'], e['year']),
        )

    def format_today_tweet(self, event, lang='zh'):
        """Format a single 'today in history' tweet."""
        date_str = f"{event['year']}年{event['month']}月{event['day']}日" if lang == 'zh' else f"{event['year']}-{event['month']:02d}-{event['day']:02d}"

        if lang == 'zh':
            header = f"📅 历史上的今天 | {date_str}"
            body = f"\n\n{event['title']}\n\n{event['description']}"
            if event['significance']:
                body += f"\n\n💡 {event['significance']}"
        else:
            header = f"📅 On This Day | {date_str}"
            body = f"\n\n{event['title']}\n\n{event['description']}"
            if event['significance']:
                body += f"\n\n💡 {event['significance']}"

        return header + body
