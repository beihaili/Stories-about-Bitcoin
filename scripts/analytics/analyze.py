"""
Analytics analysis for Stories about Bitcoin.

Reads GoatCounter JSON data and produces:
- Chapter rankings (zh/en)
- Period popularity analysis
- Language ratio analysis
- Dropout analysis (chapter-to-chapter retention)
- Referrer/source breakdown
- Markdown summary report

Usage:
    python analyze.py                              # Analyze latest data
    python analyze.py --input data/goatcounter_2026-02-26.json
    python analyze.py --output report.md           # Custom output path
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

# Chapter-to-period mapping (chapter_num -> period_id)
CHAPTER_PERIODS = {
    0: "prologue",
    1: "genesis", 2: "genesis", 3: "genesis", 4: "genesis", 5: "genesis",
    6: "first-steps", 7: "first-steps", 8: "first-steps", 9: "first-steps",
    10: "first-steps",
    11: "rising-storm", 12: "rising-storm", 13: "rising-storm",
    14: "rising-storm", 15: "rising-storm", 16: "rising-storm",
    17: "undercurrents", 18: "undercurrents", 19: "undercurrents",
    20: "undercurrents", 21: "undercurrents", 22: "undercurrents",
    23: "undercurrents", 24: "undercurrents",
    25: "breaking-waves", 26: "breaking-waves", 27: "breaking-waves",
    28: "breaking-waves", 29: "breaking-waves",
    30: "future-promise", 31: "future-promise", 32: "future-promise",
}

PERIOD_NAMES = {
    "prologue": {"zh": "序言", "en": "Prologue"},
    "genesis": {"zh": "创世纪 (1976-2009)", "en": "Genesis (1976-2009)"},
    "first-steps": {"zh": "初出茅庐 (2009-2010)", "en": "First Steps (2009-2010)"},
    "rising-storm": {"zh": "风起云涌 (2011-2012)", "en": "Rising Storm (2011-2012)"},
    "undercurrents": {"zh": "暗潮汹涌 (2013-2015)", "en": "Undercurrents (2013-2015)"},
    "breaking-waves": {"zh": "破浪前行 (2016-2020)", "en": "Breaking Waves (2016-2020)"},
    "future-promise": {"zh": "未来可期 (2021-2024)", "en": "Future Promise (2021-2024)"},
    "special": {"zh": "特别篇", "en": "Special"},
}


def find_latest_data():
    """Find the most recent GoatCounter data file."""
    if not DATA_DIR.exists():
        return None
    files = sorted(DATA_DIR.glob("goatcounter_*.json"), reverse=True)
    # Prefer files without 'export' in name
    for f in files:
        if "export" not in f.name:
            return f
    return files[0] if files else None


def load_data(filepath):
    """Load GoatCounter JSON report."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_chapter_rankings(data):
    """Rank chapters by total hits for each language."""
    rankings = {}
    for lang in ("zh", "en"):
        chapters = data.get("chapter_rankings", {}).get(lang, [])
        rankings[lang] = sorted(chapters, key=lambda x: x["count"], reverse=True)
    return rankings


def analyze_periods(data):
    """Aggregate hits by historical period."""
    period_hits = defaultdict(lambda: {"zh": 0, "en": 0, "total": 0})

    for lang in ("zh", "en"):
        for ch in data.get("chapter_rankings", {}).get(lang, []):
            ch_num = ch.get("chapter_num")
            if ch_num is not None and ch_num in CHAPTER_PERIODS:
                period = CHAPTER_PERIODS[ch_num]
                period_hits[period][lang] += ch["count"]
                period_hits[period]["total"] += ch["count"]

    # Sort by total
    sorted_periods = sorted(
        period_hits.items(), key=lambda x: x[1]["total"], reverse=True
    )
    return sorted_periods


def analyze_language_ratio(data):
    """Calculate en/zh ratio per chapter to identify international audience signals."""
    zh_by_chapter = {}
    en_by_chapter = {}

    for ch in data.get("chapter_rankings", {}).get("zh", []):
        if ch["chapter_num"] is not None:
            zh_by_chapter[ch["chapter_num"]] = ch["count"]
    for ch in data.get("chapter_rankings", {}).get("en", []):
        if ch["chapter_num"] is not None:
            en_by_chapter[ch["chapter_num"]] = ch["count"]

    ratios = []
    all_chapters = set(zh_by_chapter.keys()) | set(en_by_chapter.keys())
    for ch_num in sorted(all_chapters):
        zh = zh_by_chapter.get(ch_num, 0)
        en = en_by_chapter.get(ch_num, 0)
        ratio = en / zh if zh > 0 else float("inf") if en > 0 else 0
        ratios.append({
            "chapter": ch_num,
            "zh_hits": zh,
            "en_hits": en,
            "en_zh_ratio": round(ratio, 2),
            "total": zh + en,
        })

    return ratios


def analyze_dropout(data):
    """
    Analyze chapter-to-chapter retention.
    If chapter N has X hits and chapter N+1 has Y hits,
    retention = Y/X. Low retention = dropout point.
    """
    dropout = {"zh": [], "en": []}

    for lang in ("zh", "en"):
        chapters = data.get("chapter_rankings", {}).get(lang, [])
        by_num = {ch["chapter_num"]: ch["count"] for ch in chapters if ch["chapter_num"] is not None}

        max_ch = max(by_num.keys()) if by_num else 0
        for ch_num in range(max_ch):
            current = by_num.get(ch_num, 0)
            next_ch = by_num.get(ch_num + 1, 0)
            if current > 0:
                retention = round(next_ch / current, 2)
                dropout[lang].append({
                    "from_chapter": ch_num,
                    "to_chapter": ch_num + 1,
                    "from_hits": current,
                    "to_hits": next_ch,
                    "retention": retention,
                })

    return dropout


def analyze_referrers(data):
    """Categorize referrers into source groups."""
    referrers = data.get("referrers", {})
    if not referrers:
        return {}

    categories = {
        "search": {"keywords": ["google", "bing", "duckduckgo", "baidu", "yandex"], "hits": 0, "details": []},
        "social": {"keywords": ["twitter", "t.co", "x.com", "reddit", "facebook", "linkedin", "weibo"], "hits": 0, "details": []},
        "github": {"keywords": ["github"], "hits": 0, "details": []},
        "direct": {"keywords": [], "hits": 0, "details": []},
        "other": {"keywords": [], "hits": 0, "details": []},
    }

    # GoatCounter referrers can be in different formats depending on API version
    refs = referrers if isinstance(referrers, list) else referrers.get("refs", [])
    for ref in refs:
        if isinstance(ref, dict):
            name = ref.get("name", ref.get("ref", "")).lower()
            count = ref.get("count", 0)
        else:
            continue

        categorized = False
        for cat_name, cat_info in categories.items():
            if cat_name in ("direct", "other"):
                continue
            if any(kw in name for kw in cat_info["keywords"]):
                cat_info["hits"] += count
                cat_info["details"].append({"name": name, "count": count})
                categorized = True
                break

        if not categorized:
            if not name or name == "(direct)":
                categories["direct"]["hits"] += count
            else:
                categories["other"]["hits"] += count
                categories["other"]["details"].append({"name": name, "count": count})

    return {k: {"hits": v["hits"], "details": v["details"]} for k, v in categories.items()}


def generate_markdown_report(data, rankings, periods, ratios, dropout, referrer_cats):
    """Generate a human-readable Markdown analytics report."""
    lines = []
    date_range = data.get("date_range", {})
    start = date_range.get("start", "?")
    end = date_range.get("end", "?")

    lines.append("# Stories about Bitcoin — Analytics Report")
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Period: {start} to {end}")
    lines.append(f"Homepage hits: {data.get('homepage_hits', 'N/A')}")

    # Total stats
    totals = data.get("totals")
    if totals:
        lines.append(f"\nTotal stats: {json.dumps(totals)}")

    # Chapter rankings
    for lang, label in [("zh", "Chinese"), ("en", "English")]:
        lines.append(f"\n## Top {label} Chapters")
        lines.append(f"\n| Rank | Ch# | Hits | Path |")
        lines.append("|------|-----|------|------|")
        for i, ch in enumerate(rankings.get(lang, [])[:20], 1):
            lines.append(f"| {i} | {ch.get('chapter_num', '?'):02d} | {ch['count']} | `{ch['path'][-50:]}` |")

    # Period analysis
    lines.append("\n## Period Popularity")
    lines.append(f"\n| Period | ZH Hits | EN Hits | Total |")
    lines.append("|--------|---------|---------|-------|")
    for period_id, hits in periods:
        name = PERIOD_NAMES.get(period_id, {}).get("en", period_id)
        lines.append(f"| {name} | {hits['zh']} | {hits['en']} | {hits['total']} |")

    # Language ratio
    lines.append("\n## Language Ratio (EN/ZH)")
    lines.append("\nHigh EN/ZH ratio = strong international audience signal.")
    lines.append(f"\n| Ch# | ZH | EN | Ratio | Total |")
    lines.append("|-----|----|----|-------|-------|")
    for r in sorted(ratios, key=lambda x: x["en_zh_ratio"], reverse=True)[:15]:
        lines.append(f"| {r['chapter']:02d} | {r['zh_hits']} | {r['en_hits']} | {r['en_zh_ratio']} | {r['total']} |")

    # Dropout analysis
    lines.append("\n## Dropout Analysis (Low Retention Points)")
    for lang, label in [("zh", "Chinese"), ("en", "English")]:
        lines.append(f"\n### {label} — Chapters with <50% retention")
        low_retention = [d for d in dropout.get(lang, []) if d["retention"] < 0.5 and d["from_hits"] > 2]
        if low_retention:
            lines.append(f"\n| From | To | From Hits | To Hits | Retention |")
            lines.append("|------|----|-----------|---------|-----------|")
            for d in sorted(low_retention, key=lambda x: x["retention"]):
                lines.append(
                    f"| Ch.{d['from_chapter']:02d} | Ch.{d['to_chapter']:02d} "
                    f"| {d['from_hits']} | {d['to_hits']} | {d['retention']:.0%} |"
                )
        else:
            lines.append("No significant dropout points found (or insufficient data).")

    # Referrer analysis
    if referrer_cats:
        lines.append("\n## Traffic Sources")
        lines.append(f"\n| Source | Hits |")
        lines.append("|--------|------|")
        for cat, info in sorted(referrer_cats.items(), key=lambda x: x[1]["hits"], reverse=True):
            lines.append(f"| {cat.title()} | {info['hits']} |")
            for detail in info.get("details", [])[:5]:
                lines.append(f"| — {detail['name']} | {detail['count']} |")

    # Growth recommendations
    lines.append("\n## Growth Recommendations")
    lines.append("\nBased on data patterns:")

    # Auto-generate recommendations based on data
    total_zh = sum(ch["count"] for ch in rankings.get("zh", []))
    total_en = sum(ch["count"] for ch in rankings.get("en", []))
    if total_en > 0 and total_zh > 0:
        overall_ratio = total_en / total_zh
        if overall_ratio > 0.3:
            lines.append("- **Strong international signal** — EN readers are {:.0%} of ZH. Prioritize C8 (community translation).".format(overall_ratio))
        else:
            lines.append("- EN readership is low ({:.0%} of ZH). Focus on Chinese community first (C3).".format(overall_ratio))

    search_hits = referrer_cats.get("search", {}).get("hits", 0) if referrer_cats else 0
    social_hits = referrer_cats.get("social", {}).get("hits", 0) if referrer_cats else 0
    if search_hits > social_hits * 2:
        lines.append("- **Search dominates traffic** — Invest in SEO (C4 search, C5 PDF export).")
    elif social_hits > 0:
        lines.append("- Social traffic is present — Scale up Twitter publishing (C1).")
    else:
        lines.append("- Social traffic near zero — **Urgently start C1** (Twitter content publishing).")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze GoatCounter data for Stories about Bitcoin"
    )
    parser.add_argument(
        "--input", type=str, default=None,
        help="Path to GoatCounter JSON data file (default: latest in data/)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output path for Markdown report (default: data/analytics_report.md)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Also output structured JSON analysis"
    )
    args = parser.parse_args()

    # Find input data
    if args.input:
        input_path = Path(args.input)
    else:
        input_path = find_latest_data()

    if not input_path or not input_path.exists():
        print("No GoatCounter data found. Run goatcounter_fetch.py first.")
        sys.exit(1)

    print(f"Analyzing: {input_path}")
    data = load_data(input_path)

    # Run analyses
    rankings = analyze_chapter_rankings(data)
    periods = analyze_periods(data)
    ratios = analyze_language_ratio(data)
    dropout = analyze_dropout(data)
    referrer_cats = analyze_referrers(data)

    # Generate report
    report_md = generate_markdown_report(
        data, rankings, periods, ratios, dropout, referrer_cats
    )

    # Save Markdown report
    output_path = Path(args.output) if args.output else DATA_DIR / "analytics_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Markdown report saved: {output_path}")

    # Optionally save JSON analysis
    if args.json:
        analysis = {
            "generated_at": datetime.now().isoformat(),
            "source_file": str(input_path),
            "rankings": rankings,
            "periods": dict(periods),
            "language_ratios": ratios,
            "dropout": dropout,
            "referrer_categories": referrer_cats,
        }
        json_path = output_path.with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        print(f"JSON analysis saved: {json_path}")

    # Print highlights
    print(f"\n{'='*50}")
    print("HIGHLIGHTS")
    print(f"{'='*50}")
    print(f"Homepage: {data.get('homepage_hits', 'N/A')} hits")
    print(f"ZH chapters tracked: {len(rankings.get('zh', []))}")
    print(f"EN chapters tracked: {len(rankings.get('en', []))}")
    if rankings.get("zh"):
        top = rankings["zh"][0]
        print(f"Top ZH chapter: Ch.{top.get('chapter_num', '?'):02d} ({top['count']} hits)")
    if rankings.get("en"):
        top = rankings["en"][0]
        print(f"Top EN chapter: Ch.{top.get('chapter_num', '?'):02d} ({top['count']} hits)")

    return report_md


if __name__ == "__main__":
    main()
