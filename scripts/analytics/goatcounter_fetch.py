"""
GoatCounter API data extraction for Stories about Bitcoin.

Fetches page hit data from beihai.goatcounter.com and saves to JSON.
Requires GOATCOUNTER_API_TOKEN environment variable.

Usage:
    python goatcounter_fetch.py                    # Fetch all data
    python goatcounter_fetch.py --days 30          # Last 30 days
    python goatcounter_fetch.py --export-csv       # Export full CSV
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

# GoatCounter config
SITE_CODE = "beihai"
BASE_URL = f"https://{SITE_CODE}.goatcounter.com"
API_BASE = f"{BASE_URL}/api/v0"

# Rate limiting: 4 requests/second max
REQUEST_INTERVAL = 0.26  # 260ms between requests for safety


def get_api_token():
    """Get GoatCounter API token from environment."""
    token = os.environ.get("GOATCOUNTER_API_TOKEN", "")
    if not token:
        print("Error: GOATCOUNTER_API_TOKEN environment variable not set.")
        print("Create one at: https://beihai.goatcounter.com/user/api")
        sys.exit(1)
    return token


def api_request(endpoint, params=None, token=None):
    """Make a rate-limited API request to GoatCounter."""
    url = f"{API_BASE}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            time.sleep(REQUEST_INTERVAL)
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} for {endpoint}: {body}")
        return None
    except urllib.error.URLError as e:
        print(f"Connection error for {endpoint}: {e.reason}")
        return None


def fetch_site_stats(token, start_date=None, end_date=None):
    """Fetch total site statistics."""
    params = {}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date

    print("Fetching site total stats...")
    data = api_request("/stats/total", params, token)
    return data


def fetch_hits(token, start_date=None, end_date=None, limit=None):
    """Fetch page hit statistics with path details."""
    params = {}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date
    if limit:
        params["limit"] = limit

    print("Fetching page hits...")
    data = api_request("/stats/hits", params, token)
    return data


def fetch_all_paths(token, start_date=None, end_date=None):
    """
    Fetch hits with pagination to get all paths.
    GoatCounter paginates at ~20 entries by default.
    """
    all_paths = []
    params = {"limit": 100}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date

    print("Fetching all page paths (paginated)...")
    page = 1

    while True:
        print(f"  Page {page}...")
        data = api_request("/stats/hits", params, token)
        if not data or "paths" not in data:
            break

        paths = data.get("paths", [])
        if not paths:
            break

        all_paths.extend(paths)

        # Check for more pages
        if data.get("more", False):
            # Use the last path's ID as cursor
            last_id = paths[-1].get("id")
            if last_id:
                params["exclude"] = ",".join(str(p["id"]) for p in all_paths)
            page += 1
        else:
            break

    return all_paths


def fetch_browsers(token, start_date=None, end_date=None):
    """Fetch browser statistics."""
    params = {}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date

    print("Fetching browser stats...")
    return api_request("/stats/browsers", params, token)


def fetch_systems(token, start_date=None, end_date=None):
    """Fetch OS/system statistics."""
    params = {}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date

    print("Fetching system stats...")
    return api_request("/stats/systems", params, token)


def fetch_locations(token, start_date=None, end_date=None):
    """Fetch location/country statistics."""
    params = {}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date

    print("Fetching location stats...")
    return api_request("/stats/locations", params, token)


def fetch_languages(token, start_date=None, end_date=None):
    """Fetch language statistics."""
    params = {}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date

    print("Fetching language stats...")
    return api_request("/stats/languages", params, token)


def fetch_referrers(token, start_date=None, end_date=None):
    """Fetch referrer statistics."""
    params = {}
    if start_date:
        params["start"] = start_date
    if end_date:
        params["end"] = end_date

    print("Fetching referrer stats...")
    return api_request("/stats/referrers", params, token)


def export_csv(token):
    """Export full data as CSV."""
    print("Requesting CSV export...")
    data = api_request("/export", token=token)
    return data


def classify_path(path):
    """Classify a URL path into chapter, page type, and language."""
    result = {
        "path": path,
        "type": "other",
        "lang": None,
        "chapter_num": None,
    }

    if path.startswith("/Stories-about-Bitcoin/zh/"):
        result["lang"] = "zh"
        filename = path.split("/zh/")[-1]
        if filename and filename != "index.html":
            result["type"] = "chapter"
            # Extract chapter number from filename like "01_..."
            parts = filename.replace(".html", "").split("_")
            if parts and parts[0].isdigit():
                result["chapter_num"] = int(parts[0])
    elif path.startswith("/Stories-about-Bitcoin/en/"):
        result["lang"] = "en"
        filename = path.split("/en/")[-1]
        if filename and filename != "index.html":
            result["type"] = "chapter"
            parts = filename.replace(".html", "").split("_")
            if parts and parts[0].isdigit():
                result["chapter_num"] = int(parts[0])
    elif path in ("/Stories-about-Bitcoin/", "/Stories-about-Bitcoin"):
        result["type"] = "homepage"
    elif path.startswith("/Stories-about-Bitcoin/"):
        result["type"] = "asset"

    return result


def build_report(paths_data, total_data, referrer_data, location_data, language_data):
    """Build a structured analytics report from raw data."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "site": SITE_CODE,
        "totals": total_data,
        "chapter_rankings": {"zh": [], "en": []},
        "homepage_hits": 0,
        "referrers": referrer_data,
        "locations": location_data,
        "languages": language_data,
        "raw_paths": [],
    }

    for path_entry in paths_data or []:
        path = path_entry.get("path", "")
        count = path_entry.get("count", 0)
        info = classify_path(path)

        report["raw_paths"].append({
            "path": path,
            "count": count,
            "classification": info,
        })

        if info["type"] == "chapter" and info["lang"]:
            report["chapter_rankings"][info["lang"]].append({
                "path": path,
                "chapter_num": info["chapter_num"],
                "count": count,
            })
        elif info["type"] == "homepage":
            report["homepage_hits"] += count

    # Sort rankings by count descending
    for lang in ("zh", "en"):
        report["chapter_rankings"][lang].sort(
            key=lambda x: x["count"], reverse=True
        )

    return report


def save_report(report, suffix=""):
    """Save report to JSON file in data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"goatcounter_{date_str}{suffix}.json"
    filepath = DATA_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Report saved: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Fetch GoatCounter analytics for Stories about Bitcoin"
    )
    parser.add_argument(
        "--days", type=int, default=None,
        help="Number of days to look back (default: all time)"
    )
    parser.add_argument(
        "--start", type=str, default=None,
        help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end", type=str, default=None,
        help="End date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--export-csv", action="store_true",
        help="Export full CSV data"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Minimal output"
    )
    args = parser.parse_args()

    token = get_api_token()

    # Determine date range
    end_date = args.end or datetime.now().strftime("%Y-%m-%d")
    if args.start:
        start_date = args.start
    elif args.days:
        start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    else:
        start_date = "2026-02-07"  # Site launch date

    if not args.quiet:
        print(f"Date range: {start_date} to {end_date}")

    # Fetch all data
    total_data = fetch_site_stats(token, start_date, end_date)
    paths_data = fetch_all_paths(token, start_date, end_date)
    referrer_data = fetch_referrers(token, start_date, end_date)
    location_data = fetch_locations(token, start_date, end_date)
    language_data = fetch_languages(token, start_date, end_date)

    # Build and save report
    report = build_report(
        paths_data, total_data, referrer_data, location_data, language_data
    )
    report["date_range"] = {"start": start_date, "end": end_date}

    filepath = save_report(report)

    # Print summary
    if not args.quiet:
        print(f"\n{'='*50}")
        print("SUMMARY")
        print(f"{'='*50}")
        if total_data:
            print(f"Total hits: {total_data}")
        print(f"Paths tracked: {len(paths_data or [])}")
        print(f"Homepage hits: {report['homepage_hits']}")
        print(f"\nTop 10 Chinese chapters:")
        for i, ch in enumerate(report["chapter_rankings"]["zh"][:10], 1):
            print(f"  {i}. Ch.{ch['chapter_num']:02d} — {ch['count']} hits")
        print(f"\nTop 10 English chapters:")
        for i, ch in enumerate(report["chapter_rankings"]["en"][:10], 1):
            print(f"  {i}. Ch.{ch['chapter_num']:02d} — {ch['count']} hits")

    # CSV export
    if args.export_csv:
        csv_data = export_csv(token)
        if csv_data:
            csv_path = DATA_DIR / f"goatcounter_export_{end_date}.json"
            with open(csv_path, "w", encoding="utf-8") as f:
                json.dump(csv_data, f, ensure_ascii=False, indent=2)
            print(f"CSV export saved: {csv_path}")

    return filepath


if __name__ == "__main__":
    main()
