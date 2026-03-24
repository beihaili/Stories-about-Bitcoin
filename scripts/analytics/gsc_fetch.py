"""
Google Search Console data extraction for Stories about Bitcoin.

Requires google-api-python-client and a service account or OAuth credentials.

Usage:
    python gsc_fetch.py                          # Fetch last 28 days
    python gsc_fetch.py --days 90                # Last 90 days
    python gsc_fetch.py --credentials creds.json # Specify credentials file

Setup:
    1. Enable Search Console API in Google Cloud Console
    2. Create a service account or OAuth client credentials
    3. Add the service account email as a user in GSC
    4. Set GOOGLE_APPLICATION_CREDENTIALS env var or pass --credentials
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

SITE_URL = "https://beihaili.github.io/Stories-about-Bitcoin/"


def get_gsc_service(credentials_file=None):
    """Build the Google Search Console API service."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("Error: google-api-python-client not installed.")
        print("Run: pip install google-api-python-client google-auth")
        sys.exit(1)

    creds_path = credentials_file or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        print("Error: No credentials file. Set GOOGLE_APPLICATION_CREDENTIALS or use --credentials")
        sys.exit(1)

    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    return build("searchconsole", "v1", credentials=creds)


def fetch_search_analytics(service, start_date, end_date, dimensions=None):
    """Fetch search analytics data from GSC."""
    if dimensions is None:
        dimensions = ["query", "page"]

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": 1000,
    }

    response = service.searchanalytics().query(
        siteUrl=SITE_URL, body=body
    ).execute()

    return response.get("rows", [])


def fetch_queries(service, start_date, end_date):
    """Fetch search queries with clicks, impressions, CTR, position."""
    rows = fetch_search_analytics(service, start_date, end_date, ["query"])
    results = []
    for row in rows:
        results.append({
            "query": row["keys"][0],
            "clicks": row["clicks"],
            "impressions": row["impressions"],
            "ctr": round(row["ctr"], 4),
            "position": round(row["position"], 1),
        })
    return sorted(results, key=lambda x: x["impressions"], reverse=True)


def fetch_pages(service, start_date, end_date):
    """Fetch page-level performance data."""
    rows = fetch_search_analytics(service, start_date, end_date, ["page"])
    results = []
    for row in rows:
        results.append({
            "page": row["keys"][0],
            "clicks": row["clicks"],
            "impressions": row["impressions"],
            "ctr": round(row["ctr"], 4),
            "position": round(row["position"], 1),
        })
    return sorted(results, key=lambda x: x["clicks"], reverse=True)


def fetch_countries(service, start_date, end_date):
    """Fetch country-level performance data."""
    rows = fetch_search_analytics(service, start_date, end_date, ["country"])
    results = []
    for row in rows:
        results.append({
            "country": row["keys"][0],
            "clicks": row["clicks"],
            "impressions": row["impressions"],
            "ctr": round(row["ctr"], 4),
            "position": round(row["position"], 1),
        })
    return sorted(results, key=lambda x: x["clicks"], reverse=True)


def identify_opportunities(queries, pages):
    """
    Cross-analyze GSC data to find content opportunities.
    High impressions + low CTR = title/meta description optimization opportunity.
    High impressions + no matching page = content gap opportunity.
    """
    opportunities = {
        "low_ctr_high_impressions": [],
        "high_position_improvement": [],
    }

    for q in queries:
        # High visibility but low click-through
        if q["impressions"] > 50 and q["ctr"] < 0.02:
            opportunities["low_ctr_high_impressions"].append(q)

        # Page 2 (position 11-20) — close to page 1
        if 10 < q["position"] < 20 and q["impressions"] > 20:
            opportunities["high_position_improvement"].append(q)

    return opportunities


def generate_gsc_report(queries, pages, countries, opportunities, start_date, end_date):
    """Generate a Markdown report from GSC data."""
    lines = []
    lines.append("# Google Search Console Report")
    lines.append(f"\nPeriod: {start_date} to {end_date}")
    lines.append(f"Site: {SITE_URL}")

    # Top queries
    lines.append("\n## Top Search Queries")
    lines.append(f"\n| Query | Clicks | Impressions | CTR | Position |")
    lines.append("|-------|--------|-------------|-----|----------|")
    for q in queries[:20]:
        lines.append(
            f"| {q['query']} | {q['clicks']} | {q['impressions']} "
            f"| {q['ctr']:.1%} | {q['position']:.1f} |"
        )

    # Top pages
    lines.append("\n## Top Pages")
    lines.append(f"\n| Page | Clicks | Impressions | CTR | Position |")
    lines.append("|------|--------|-------------|-----|----------|")
    for p in pages[:20]:
        short_page = p["page"].replace(SITE_URL, "/")
        lines.append(
            f"| {short_page} | {p['clicks']} | {p['impressions']} "
            f"| {p['ctr']:.1%} | {p['position']:.1f} |"
        )

    # Countries
    lines.append("\n## Top Countries")
    lines.append(f"\n| Country | Clicks | Impressions | CTR |")
    lines.append("|---------|--------|-------------|-----|")
    for c in countries[:15]:
        lines.append(f"| {c['country']} | {c['clicks']} | {c['impressions']} | {c['ctr']:.1%} |")

    # Opportunities
    lines.append("\n## Optimization Opportunities")

    low_ctr = opportunities.get("low_ctr_high_impressions", [])
    if low_ctr:
        lines.append("\n### High Impressions, Low CTR (optimize title/meta)")
        for q in low_ctr[:10]:
            lines.append(f"- \"{q['query']}\" — {q['impressions']} impressions, {q['ctr']:.1%} CTR")

    improve = opportunities.get("high_position_improvement", [])
    if improve:
        lines.append("\n### Near Page 1 (position 11-20, worth optimizing)")
        for q in improve[:10]:
            lines.append(f"- \"{q['query']}\" — position {q['position']:.1f}, {q['impressions']} impressions")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Google Search Console data for Stories about Bitcoin"
    )
    parser.add_argument("--days", type=int, default=28, help="Days to look back (default: 28)")
    parser.add_argument("--credentials", type=str, default=None, help="Path to credentials JSON")
    parser.add_argument("--output", type=str, default=None, help="Output path for report")
    args = parser.parse_args()

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    print(f"Fetching GSC data: {start_date} to {end_date}")

    service = get_gsc_service(args.credentials)

    queries = fetch_queries(service, start_date, end_date)
    pages = fetch_pages(service, start_date, end_date)
    countries = fetch_countries(service, start_date, end_date)
    opportunities = identify_opportunities(queries, pages)

    # Save raw data
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw_data = {
        "date_range": {"start": start_date, "end": end_date},
        "queries": queries,
        "pages": pages,
        "countries": countries,
        "opportunities": opportunities,
    }
    raw_path = DATA_DIR / f"gsc_{end_date}.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    print(f"Raw data saved: {raw_path}")

    # Generate report
    report = generate_gsc_report(queries, pages, countries, opportunities, start_date, end_date)
    report_path = Path(args.output) if args.output else DATA_DIR / "gsc_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved: {report_path}")

    # Print summary
    print(f"\nTop 5 queries: {', '.join(q['query'] for q in queries[:5])}")
    print(f"Total clicks: {sum(q['clicks'] for q in queries)}")
    print(f"Optimization opportunities: {len(opportunities.get('low_ctr_high_impressions', []))} low CTR, {len(opportunities.get('high_position_improvement', []))} near page 1")


if __name__ == "__main__":
    main()
