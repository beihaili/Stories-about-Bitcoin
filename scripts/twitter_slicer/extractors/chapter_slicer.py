"""Extract tweetable content slices from chapter markdown files."""

import os
import re
import glob

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CHAPTERS_DIR, DRAMA_KEYWORDS_ZH


class ChapterSlicer:
    """Parse chapter markdown files and extract 5 types of content."""

    def __init__(self):
        self.chapter_files = self._discover_chapters()

    def _discover_chapters(self):
        """Find all chapter markdown files, sorted by number."""
        pattern = os.path.join(CHAPTERS_DIR, '*.md')
        files = glob.glob(pattern)
        # Filter out README.md
        files = [f for f in files if not os.path.basename(f).startswith('README')]
        # Sort by chapter number prefix
        def sort_key(path):
            name = os.path.basename(path)
            m = re.match(r'(\d+)', name)
            return int(m.group(1)) if m else 999
        return sorted(files, key=sort_key)

    def get_chapter_count(self):
        return len(self.chapter_files)

    def _parse_chapter(self, filepath):
        """Parse a chapter file, returning clean paragraphs and metadata."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        basename = os.path.basename(filepath)
        m = re.match(r'(\d+)_(.+)\.md', basename)
        chapter_num = int(m.group(1)) if m else 0
        chapter_raw_title = m.group(2) if m else basename

        # Remove HTML style blocks
        content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        # Remove HTML div blocks (meta-wrap, nav footers)
        content = re.sub(r'<div[^>]*>.*?</div>', '', content, flags=re.DOTALL)
        # Remove inline HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Remove image references
        content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
        # Remove badge markdown
        content = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', content)

        lines = content.split('\n')
        paragraphs = []
        blockquotes = []
        sections = []
        current_section_paras = []
        current_h2 = ''

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Track H2 sections
            if stripped.startswith('## '):
                if current_h2 and current_section_paras:
                    sections.append({
                        'heading': current_h2,
                        'paragraphs': current_section_paras[:],
                    })
                current_h2 = stripped.lstrip('#').strip()
                current_section_paras = []
                continue

            # Track H3 (subsections, skip)
            if stripped.startswith('#'):
                continue

            # Blockquotes
            if stripped.startswith('>'):
                quote_text = stripped.lstrip('>').strip()
                if quote_text and len(quote_text) > 10:
                    blockquotes.append(quote_text)
                continue

            # Navigation/footer patterns — skip
            if stripped.startswith('[上一章') or stripped.startswith('[下一章'):
                continue
            if stripped.startswith('---'):
                continue

            # Regular paragraphs
            if len(stripped) > 20:
                paragraphs.append(stripped)
                current_section_paras.append(stripped)

        # Don't forget last section
        if current_h2 and current_section_paras:
            sections.append({
                'heading': current_h2,
                'paragraphs': current_section_paras[:],
            })

        return {
            'num': chapter_num,
            'title': chapter_raw_title,
            'paragraphs': paragraphs,
            'blockquotes': blockquotes,
            'sections': sections,
        }

    def slice_chapter(self, chapter_num):
        """Extract all tweetable content from a specific chapter."""
        # Find the matching file
        target = None
        for f in self.chapter_files:
            basename = os.path.basename(f)
            m = re.match(r'(\d+)', basename)
            if m and int(m.group(1)) == chapter_num:
                target = f
                break

        if not target:
            return None

        parsed = self._parse_chapter(target)
        result = {
            'chapter_num': parsed['num'],
            'title': parsed['title'],
            'hooks': self._extract_hooks(parsed),
            'dramatic': self._extract_dramatic(parsed),
            'facts': self._extract_facts(parsed),
            'epigraphs': self._extract_epigraphs(parsed),
            'climaxes': self._extract_climaxes(parsed),
        }
        return result

    def slice_all(self):
        """Slice all chapters."""
        results = []
        for f in self.chapter_files:
            basename = os.path.basename(f)
            m = re.match(r'(\d+)', basename)
            if m:
                chapter_data = self.slice_chapter(int(m.group(1)))
                if chapter_data:
                    results.append(chapter_data)
        return results

    def _extract_hooks(self, parsed):
        """Extract opening hooks — first 2-3 engaging sentences."""
        paras = parsed['paragraphs']
        hooks = []
        for p in paras[:5]:
            # Opening sentences tend to be shorter and punchier
            if len(p) < 200:
                hooks.append(p)
            if len(hooks) >= 3:
                break
        return hooks

    def _extract_dramatic(self, parsed):
        """Extract paragraphs containing drama keywords."""
        results = []
        for p in parsed['paragraphs']:
            matches = sum(1 for kw in DRAMA_KEYWORDS_ZH if kw in p)
            if matches >= 2 and len(p) < 280:
                results.append(p)
            elif matches >= 1 and len(p) < 200:
                results.append(p)
        return results[:5]

    def _extract_facts(self, parsed):
        """Extract sentences containing specific numbers/dates/amounts."""
        fact_pattern = re.compile(
            r'(\d+(?:\.\d+)?(?:亿|万|美元|BTC|%|块|笔|人|个|年|月|日|天))'
        )
        results = []
        for p in parsed['paragraphs']:
            if fact_pattern.search(p) and len(p) < 280:
                results.append(p)
        return results[:5]

    def _extract_epigraphs(self, parsed):
        """Extract blockquotes (often chapter epigraphs)."""
        return [bq for bq in parsed['blockquotes'] if len(bq) < 280]

    def _extract_climaxes(self, parsed):
        """Extract the last paragraph of each section (section climax)."""
        results = []
        for section in parsed['sections']:
            if section['paragraphs']:
                last = section['paragraphs'][-1]
                if len(last) < 280 and len(last) > 30:
                    results.append({
                        'section': section['heading'],
                        'text': last,
                    })
        return results

    def format_chapter_tweet(self, text, chapter_num, chapter_title, content_type, lang='zh'):
        """Format a chapter slice as a tweet."""
        if lang == 'zh':
            header = f"📖 比特币那些事儿 · 第{chapter_num}章"
            body = f"\n\n{text}"
            footer = f"\n\n🔗 全文阅读：{chapter_title}"
        else:
            header = f"📖 Stories about Bitcoin · Ch.{chapter_num}"
            body = f"\n\n{text}"
            footer = f"\n\n🔗 Read more: {chapter_title}"
        return header + body + footer
