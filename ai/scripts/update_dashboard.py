#!/usr/bin/env python3
"""
AI Advancements Dashboard Updater
Fetches latest AI news from multiple sources with graceful degradation.

Usage (from repo root):
    python dashboards/ai/scripts/update_dashboard.py
"""

import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import feedparser
import requests
import yaml

# Optional Reddit support
try:
    import praw
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False


class DashboardUpdater:
    def __init__(self, config_path: str = "dashboards/ai/sources.yaml"):
        if not Path(config_path).exists():
            print(f"Error: config not found at {config_path}", file=sys.stderr)
            sys.exit(1)

        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        cache_dir = Path(self.config["cache"]["directory"])
        cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache_file = cache_dir / self.config["cache"]["filename"]
        self.metadata_file = cache_dir / self.config["cache"]["metadata_filename"]
        self.readme_path = Path(
            self.config["cache"].get("readme_path", "dashboards/ai/README.md")
        )

        self.updates: List[Dict[str, Any]] = []
        self.failures: List[Dict[str, str]] = []
        self.source_count = 0
        self.failure_count = 0

    # ------------------------------------------------------------------
    # Source fetchers
    # ------------------------------------------------------------------

    def fetch_rss_feeds(self) -> List[Dict[str, Any]]:
        """Fetch updates from RSS feeds."""
        updates = []
        for source in self.config["sources"].get("rss", []):
            if not source.get("enabled", True):
                continue
            self.source_count += 1
            try:
                feed = feedparser.parse(source["url"])
                if feed.bozo and not feed.entries:
                    raise Exception(f"Feed parse error: {feed.bozo_exception}")
                for entry in feed.entries[:5]:
                    updates.append(
                        {
                            "source": source["name"],
                            "type": "rss",
                            "title": entry.get("title", ""),
                            "link": entry.get("link", ""),
                            "published": entry.get("published", ""),
                            "summary": entry.get("summary", "")[:200],
                        }
                    )
            except Exception as e:
                self.failures.append({"source": source["name"], "error": str(e)})
                self.failure_count += 1
        return updates

    def fetch_sitemap_sources(self) -> List[Dict[str, Any]]:
        """
        Fetch recent articles from sitemap-based sources (e.g. Anthropic).
        Filters to articles published in the last 14 days, then fetches og:title
        from each article page.
        """
        updates = []
        cutoff = datetime.utcnow() - timedelta(days=14)
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (compatible; AI-Dashboard/1.0; "
                "+https://seven-fortunas.github.io/dashboards/ai/)"
            )
        }

        for source in self.config["sources"].get("sitemap", []):
            if not source.get("enabled", True):
                continue
            self.source_count += 1
            try:
                resp = requests.get(
                    source["sitemap_url"],
                    timeout=source.get("timeout", 15),
                    headers=headers,
                )
                resp.raise_for_status()

                ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                root = ET.fromstring(resp.text)
                url_pattern = source.get("url_pattern", "")

                entries = []
                for url_elem in root.findall("sm:url", ns):
                    loc = url_elem.findtext("sm:loc", namespaces=ns) or ""
                    lastmod = url_elem.findtext("sm:lastmod", namespaces=ns) or ""

                    if url_pattern and url_pattern not in loc:
                        continue

                    if lastmod:
                        try:
                            pub_date = datetime.fromisoformat(lastmod[:10])
                            if pub_date < cutoff:
                                continue
                        except ValueError:
                            pass

                    entries.append({"loc": loc, "lastmod": lastmod})

                entries.sort(key=lambda x: x["lastmod"], reverse=True)
                limit = source.get("limit", 5)

                for entry in entries[:limit]:
                    # Derive fallback title from URL slug
                    slug = entry["loc"].rstrip("/").split("/")[-1]
                    title = slug.replace("-", " ").title()
                    description = ""

                    # Fetch article page to extract og:title / og:description
                    try:
                        time.sleep(0.5)
                        article_resp = requests.get(
                            entry["loc"],
                            timeout=source.get("timeout", 10),
                            headers=headers,
                        )
                        if article_resp.ok:
                            html = article_resp.text
                            for pattern in [
                                r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']',
                                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']',
                            ]:
                                m = re.search(pattern, html)
                                if m:
                                    title = m.group(1).strip()
                                    break
                            for pattern in [
                                r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']',
                                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:description["\']',
                            ]:
                                m = re.search(pattern, html)
                                if m:
                                    description = m.group(1).strip()[:200]
                                    break
                    except Exception:
                        pass  # Use slug-derived title

                    updates.append(
                        {
                            "source": source["name"],
                            "type": "sitemap",
                            "title": title,
                            "link": entry["loc"],
                            "published": entry["lastmod"],
                            "summary": description,
                        }
                    )
            except Exception as e:
                self.failures.append({"source": source["name"], "error": str(e)})
                self.failure_count += 1

        return updates

    def fetch_github_releases(self) -> List[Dict[str, Any]]:
        """Fetch latest GitHub releases."""
        updates = []
        token = os.environ.get("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"} if token else {}

        for source in self.config["sources"].get("github", []):
            if not source.get("enabled", True):
                continue
            self.source_count += 1
            try:
                url = f"https://api.github.com/repos/{source['repo']}/releases/latest"
                resp = requests.get(url, headers=headers, timeout=source.get("timeout", 10))
                resp.raise_for_status()
                release = resp.json()
                updates.append(
                    {
                        "source": source["name"],
                        "type": "github",
                        "title": f"Release {release['tag_name']}",
                        "link": release["html_url"],
                        "published": release["published_at"],
                        "summary": (release.get("body") or "")[:200],
                    }
                )
            except Exception as e:
                self.failures.append({"source": source["name"], "error": str(e)})
                self.failure_count += 1

        return updates

    def fetch_reddit_posts(self) -> List[Dict[str, Any]]:
        """Fetch top Reddit posts (requires praw + credentials)."""
        if not REDDIT_AVAILABLE:
            return []

        client_id = os.environ.get("REDDIT_CLIENT_ID")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        if not client_id or not client_secret:
            return []

        updates = []
        try:
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=os.environ.get("REDDIT_USER_AGENT", "AI-Dashboard/1.0"),
            )
            for source in self.config["sources"].get("reddit", []):
                if not source.get("enabled", True):
                    continue
                self.source_count += 1
                try:
                    sub = reddit.subreddit(source["subreddit"])
                    for post in sub.top(time_filter="day", limit=source.get("limit", 10)):
                        updates.append(
                            {
                                "source": f"r/{source['subreddit']}",
                                "type": "reddit",
                                "title": post.title,
                                "link": f"https://reddit.com{post.permalink}",
                                "published": datetime.fromtimestamp(post.created_utc).isoformat(),
                                "summary": (post.selftext or "")[:200],
                            }
                        )
                except Exception as e:
                    self.failures.append({"source": source["subreddit"], "error": str(e)})
                    self.failure_count += 1
        except Exception as e:
            print(f"Reddit auth failed: {e}")

        return updates

    def fetch_x_posts(self) -> List[Dict[str, Any]]:
        """Fetch X/Twitter posts (optional, requires API key)."""
        if not os.environ.get("X_API_KEY"):
            return []
        # X API v2 implementation placeholder
        return []

    # ------------------------------------------------------------------
    # Cache / output
    # ------------------------------------------------------------------

    def load_cached_data(self) -> Dict[str, Any]:
        try:
            if self.cache_file.exists():
                with open(self.cache_file) as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: could not load cache: {e}")
        return {"updates": [], "timestamp": None}

    def save_cached_data(self):
        now = datetime.utcnow().isoformat()
        cache_data = {
            "updates": self.updates,
            "timestamp": now,
            "last_updated": now,          # React app reads this field
            "failures": self.failures,    # {source, error} list (backward compat)
            "failed_sources": [f["source"] for f in self.failures],  # React ErrorBanner
            "failure_count": self.failure_count,
            "source_count": self.source_count,
        }
        with open(self.cache_file, "w") as f:
            json.dump(cache_data, f, indent=2)

        metadata = {
            "last_successful_update": now,
            "consecutive_failures": 0 if self.updates else 1,
        }
        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def check_degradation_level(self) -> str:
        if self.source_count == 0:
            return "total_failure"
        rate = self.failure_count / self.source_count
        threshold = self.config["degradation"]["warning_threshold"]
        if rate >= 1.0:
            return "total_failure"
        elif rate >= threshold:
            return "partial_failure"
        elif rate > 0:
            return "minor_failure"
        return "healthy"

    def generate_dashboard(self):
        """Write README.md with latest updates table and failure list."""
        degradation = self.check_degradation_level()

        # Fall back to cache on total failure
        if degradation == "total_failure":
            cached = self.load_cached_data()
            if cached["updates"]:
                self.updates = cached["updates"]
                ts = cached.get("timestamp")
                if ts:
                    age = datetime.utcnow() - datetime.fromisoformat(ts)
                    max_age = self.config["degradation"]["cache_max_age_hours"]
                    if age < timedelta(hours=max_age):
                        degradation = "using_cache"

        self.updates.sort(key=lambda x: x.get("published", ""), reverse=True)

        self.readme_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.readme_path, "w") as f:
            f.write("# AI Advancements Dashboard\n\n")
            f.write(f"**Last Updated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")

            if degradation == "total_failure":
                f.write("⚠️ **WARNING:** All data sources failed. No cached data available.\n\n")
            elif degradation == "using_cache":
                f.write("⚠️ **WARNING:** All sources failed. Showing cached data.\n\n")
            elif degradation == "partial_failure":
                f.write(
                    f"⚠️ **WARNING:** {self.failure_count}/{self.source_count} data sources failed.\n\n"
                )
            elif degradation == "minor_failure":
                f.write(
                    f"ℹ️ **INFO:** {self.failure_count}/{self.source_count} data sources failed.\n\n"
                )

            if self.updates:
                f.write("## Latest Updates\n\n")
                f.write("| Source | Title | Published |\n")
                f.write("|--------|-------|----------|\n")
                for update in self.updates[:50]:
                    source = update["source"]
                    title = update["title"].replace("|", "\\|")[:80]
                    link = update["link"]
                    published = str(update.get("published", ""))[:10]
                    f.write(f"| {source} | [{title}]({link}) | {published} |\n")
            else:
                f.write("No updates available.\n\n")

            if self.failures:
                f.write("\n## Failed Sources\n\n")
                for failure in self.failures:
                    f.write(f"- **{failure['source']}:** {failure['error']}\n")

        print(f"README written to {self.readme_path}")

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self):
        print("Starting AI Advancements Dashboard update...")

        self.updates.extend(self.fetch_rss_feeds())
        self.updates.extend(self.fetch_sitemap_sources())
        self.updates.extend(self.fetch_github_releases())
        self.updates.extend(self.fetch_reddit_posts())
        self.updates.extend(self.fetch_x_posts())

        self.save_cached_data()
        self.generate_dashboard()

        print(
            f"Done. {len(self.updates)} updates, "
            f"{self.failure_count}/{self.source_count} sources failed."
        )
        if self.failures:
            for f in self.failures:
                print(f"  FAILED: {f['source']} - {f['error']}")


def _find_config() -> str:
    """Locate sources.yaml relative to the repo root."""
    candidates = [
        "dashboards/ai/sources.yaml",  # 7f-infrastructure-project
        "ai/sources.yaml",             # dashboards repo
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    print("Error: sources.yaml not found. Run from repo root.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else _find_config()
    updater = DashboardUpdater(config_path=config_path)
    updater.run()
