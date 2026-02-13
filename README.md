# 7F Lens Intelligence Platform

Multi-dimensional dashboards tracking enterprise-critical vectors for Seven Fortunas.

## Vision

The 7F Lens provides real-time intelligence on trends, developments, and opportunities across domains critical to Seven Fortunas's mission of digital inclusion.

## Available Dashboards

### 🤖 AI Advancements Tracker (MVP - Active)
Track latest developments in AI/ML including:
- Model releases (GPT, Claude, Gemini, open-source LLMs)
- Research breakthroughs (papers, techniques)
- Tool releases (frameworks, platforms)
- Regulatory developments
- Community sentiment

**Status:** In development (MVP Week)  
**Update Frequency:** Every 6 hours  
**Data Sources:** RSS feeds, GitHub releases, Reddit, YouTube

[View AI Dashboard →](ai/)

### 📊 Coming Soon

- **Fintech Trends** (Phase 2) - Payments, tokenization, DeFi, regulations
- **EduTech Intelligence** (Phase 2) - EdTech innovations, EduPeru market analysis
- **Security Intelligence** (Phase 2) - Threats, compliance, best practices
- **Investment & Opportunities** (Phase 2) - Funding, partnerships, market signals

## Architecture

```
dashboards/
├── ai/                         # AI Advancements Dashboard
│   ├── README.md              # Auto-generated dashboard view
│   ├── config/
│   │   └── sources.yaml       # Data source configuration
│   ├── data/
│   │   ├── latest.json        # Current aggregated data
│   │   └── archive/           # Historical snapshots
│   ├── scripts/
│   │   ├── fetch_sources.py   # Data aggregation script
│   │   └── generate_summary.py # AI summarization
│   └── summaries/
│       └── YYYY-MM-DD.md      # Weekly AI summaries
└── [future dashboards...]
```

## How It Works

1. **Data Aggregation** - GitHub Actions fetch data from RSS, Reddit, YouTube, GitHub APIs every 6 hours
2. **AI Processing** - Claude API summarizes top developments weekly
3. **Display** - Auto-generated markdown dashboards, updated automatically
4. **Intelligence** - Trend analysis, relevance scoring, historical tracking

## Configuration

Dashboard sources are configurable via `.../config/sources.yaml` files. Team members can use the `7f-dashboard-configurator` skill to add/remove sources.

## Status

- [x] Dashboard repository created
- [ ] AI dashboard structure initialized
- [ ] Data aggregation scripts implemented
- [ ] GitHub Actions workflows configured
- [ ] First data aggregation run
- [ ] Auto-update operational

**Timeline:** MVP Week (Days 0-5)

---

**Owner:** Seven Fortunas VP AI-SecOps (@jorge-at-sf)  
**Contributors:** Founding team
