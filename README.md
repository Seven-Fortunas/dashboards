# Seven Fortunas Dashboards

**Live:** [AI Advancements](https://seven-fortunas.github.io/dashboards/ai/), the latest AI research, releases and industry news, refreshed every 6 hours.

## What's here

| Folder | What it is |
|---|---|
| [`ai/`](ai/) | The AI Advancements dashboard: the React page, the update script, and its source list (`ai/config/sources.yaml`) |
| `fintech/`, `edutech/`, `security/` | Source lists for fintech, edtech and security feeds. They have no published page. |
| `performance/` | Time limits and retry settings for the update job |

## How it updates

The **Update AI Advancements Dashboard** workflow runs every 6 hours. It runs `ai/scripts/update_dashboard.py`, which reads the sources in `ai/config/sources.yaml` (RSS feeds, sitemaps, GitHub releases, Reddit and YouTube), caches the results in `ai/data/`, and the page is redeployed. If some sources fail, the rest still update and the page says how many failed; if all of them fail, it shows the last cached data with a warning. A separate workflow writes a weekly summary.

To update by hand, start **Update AI Advancements Dashboard** from the Actions tab.

## License

See [LICENSE](LICENSE).
