"""Configuration for the Twitter content slicer."""

import os

# Base paths (relative to this script's directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

# Data source paths
CHAPTERS_DIR = os.path.join(PROJECT_ROOT, '正文')
RESOURCES_DIR = os.path.join(PROJECT_ROOT, '资料')
# 重点资料已合并到资料目录
KEY_RESOURCES_DIR = RESOURCES_DIR

# Specific data files
COMPREHENSIVE_TIMELINE = os.path.join(RESOURCES_DIR, 'comprehensive_timeline.json')
COMPLETE_TIMELINE = os.path.join(KEY_RESOURCES_DIR, 'bitcoin_complete_timeline.json')
QUOTES_FILE = os.path.join(RESOURCES_DIR, 'quotes.json')
EMAILS_FILE = os.path.join(RESOURCES_DIR, 'emails.json')
STORIES_FILE = os.path.join(RESOURCES_DIR, 'legendary_bitcoin_stories.json')

# Output paths
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')
QUEUE_DIR = os.path.join(OUTPUT_DIR, 'queue')
POSTED_DIR = os.path.join(OUTPUT_DIR, 'posted')

# Tweet constraints
MAX_TWEET_CHARS = 280
MAX_TWEET_CHARS_ZH = 270  # Leave room for hashtags
THREAD_MAX_TWEETS = 6

# Default hashtags
HASHTAGS_ZH = ['#比特币', '#Bitcoin']
HASHTAGS_EN = ['#Bitcoin', '#BTC', '#CryptoHistory']

# Content type labels
CONTENT_TYPES = {
    'today_in_history': '历史上的今天',
    'quote': '中本聪语录',
    'chapter_hook': '章节钩子',
    'chapter_drama': '戏剧性段落',
    'chapter_fact': '趣闻事实',
    'chapter_epigraph': '卷首引言',
    'story': '传奇故事',
    'thread': '推文串',
}

# Priority authors for quotes
PRIORITY_AUTHORS = ['Satoshi Nakamoto', 'Hal Finney']

# Keywords for dramatic paragraph detection
DRAMA_KEYWORDS_ZH = [
    '历史', '改变', '第一次', '首次', '从未', '颠覆', '震惊',
    '革命', '里程碑', '转折', '命运', '传奇', '疯狂', '崩溃',
    '暴涨', '暴跌', '突破', '诞生', '消失', '秘密',
]

# OpenRouter API config (optional, for --polish mode)
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
OPENROUTER_MODEL = 'anthropic/claude-sonnet-4-20250514'
