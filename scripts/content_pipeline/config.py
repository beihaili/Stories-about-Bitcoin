"""Configuration for the content pipeline."""

import os
from pathlib import Path

# Base paths — 合并后只有一个仓库
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # 仓库根目录

# Source data paths
CHAPTERS_DIR = PROJECT_ROOT / "正文"
DRAFTS_DIR = PROJECT_ROOT / "草稿"
RESOURCES_DIR = PROJECT_ROOT / "资料"
KEY_RESOURCES_DIR = RESOURCES_DIR
AI_DIR = PROJECT_ROOT / "AI模型"
STYLE_BOOK = AI_DIR / "明朝那些事儿全本.txt"
STYLE_DNA_FILE = AI_DIR / "风格DNA.txt"
THOUGHTS_FILE = AI_DIR / "我的思考库.json"
HISTORY_INDEX_FILE = AI_DIR / "史料索引.json"

# Output paths
OUTPUT_DIR = SCRIPT_DIR / "output"
REWRITE_OUTPUT = OUTPUT_DIR / "rewrites"
TRANSLATION_OUTPUT = OUTPUT_DIR / "translations"
SCORE_OUTPUT = OUTPUT_DIR / "scores"

# 仓库内路径（不再跨仓库）
MAIN_ZH_DIR = PROJECT_ROOT / "zh"
MAIN_EN_DIR = PROJECT_ROOT / "en"
MAIN_IMG_DIR = PROJECT_ROOT / "img"
MAIN_IMG_800_DIR = PROJECT_ROOT / "img_800px"
MAIN_IMG_WEBP_DIR = PROJECT_ROOT / "img_webp"
MAIN_CHAPTERS_JS = PROJECT_ROOT / "new-website" / "src" / "data" / "chapters.js"
MAIN_FEED_XML = PROJECT_ROOT / "new-website" / "public" / "feed.xml"
MAIN_SITEMAP_XML = PROJECT_ROOT / "new-website" / "public" / "sitemap.xml"
MAIN_ZH_SUMMARY = MAIN_ZH_DIR / "SUMMARY.md"
MAIN_EN_SUMMARY = MAIN_EN_DIR / "SUMMARY.md"

# API config
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Glossary file
GLOSSARY_FILE = SCRIPT_DIR / "glossary.json"

# Content calendar
CALENDAR_FILE = SCRIPT_DIR / "content_calendar.json"

# Core history files (Tier 1)
CORE_HISTORY_FILES = [
    "bitcoin_complete_timeline.json",
    "comprehensive_timeline.json",
    "key_figures.json",
    "bitcoin_pizza_day_complete_history.json",
    "bitcoin_scaling_war_complete_history.json",
    "darknet_silk_road_history.json",
    "silk_road_comprehensive_history.json",
    "bitcoin_security_incidents_comprehensive.json",
    "technical_developments.json",
    "early_bitcoin_community_history.json",
    "legendary_bitcoin_stories.json",
]

# Quality scoring thresholds
QUALITY_AUTO_PASS = 7.0  # Average score >= 7 auto-proceeds to translation
QUALITY_DIMENSIONS = [
    "factual_accuracy",
    "style_consistency",
    "readability",
    "chapter_coherence",
    "terminology_accuracy",
]

# Retrieval config
CHUNK_SIZE = 1800
CHUNK_OVERLAP = 200
MAX_CONTEXT_CHARS = 12000
MIN_RELEVANCE_SCORE = 1

# Site URLs
SITE_BASE = "https://beihaili.github.io/Stories-about-Bitcoin"
