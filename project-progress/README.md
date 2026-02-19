# Project Progress Dashboard

**Purpose:** Daily-updated visibility into project health and velocity
**Owner:** Jorge (VP AI-SecOps)
**Status:** Phase 2 Implementation
**Last Updated:** 2026-02-18

---

## Overview

The Project Progress Dashboard provides real-time insights into the health and velocity of all Seven Fortunas projects.

**Key Metrics:**
- Sprint velocity trends
- Feature completion rate
- Burndown charts
- Active blockers and risks
- Team utilization

**Update Frequency:** Daily (6 AM UTC via GitHub Actions)

---

## Dashboard Structure

```
dashboards/project-progress/
├── README.md                    # This file
├── index.html                   # Dashboard UI (Phase 2)
├── styles.css                   # Dashboard styling (Phase 2)
├── scripts/
│   ├── update_dashboard.py      # Data aggregation script
│   ├── generate_ai_summary.py   # Weekly AI-generated summary
│   └── requirements.txt         # Python dependencies
├── data/
│   ├── project-progress-latest.json  # Latest metrics (updated daily)
│   ├── historical/              # 52 weeks historical data
│   └── ai-summaries/            # Weekly AI summaries
└── templates/
    └── weekly-summary-template.md   # Template for AI summaries
```

---

## Metrics Collected

### 1. Sprint Velocity
**Description:** Story points completed per sprint
**Data Source:** GitHub Projects API
**Calculation:** `sum(completed_story_points) / num_sprints`

**Display:**
- Line chart showing velocity over last 6 sprints
- Average velocity with confidence interval
- Trend indicator (↑ increasing, → stable, ↓ decreasing)

---

### 2. Feature Completion Rate
**Description:** Percentage of features completed vs. planned
**Data Source:** feature_list.json
**Calculation:** `(features_completed / total_features) × 100%`

**Display:**
- Progress bar
- Completion percentage
- Estimated completion date (based on velocity)

---

### 3. Burndown Chart
**Description:** Remaining work over time
**Data Source:** GitHub Projects API, feature_list.json
**Calculation:** Daily snapshot of remaining story points

**Display:**
- Line chart with ideal vs. actual burndown
- Days ahead/behind schedule
- Scope change indicator

---

### 4. Active Blockers & Risks
**Description:** Issues blocking progress
**Data Source:** GitHub Issues API (label:blocked)
**Calculation:** Count of open issues with "blocked" label

**Display:**
- Count of blockers
- Top 5 blockers (by priority)
- Blocker age (days open)

---

### 5. Team Utilization
**Description:** Team capacity vs. workload
**Data Source:** GitHub Projects API (assignee field)
**Calculation:** `assigned_points / team_capacity`

**Display:**
- Utilization percentage per team member
- Overloaded team members (>100%)
- Idle capacity (0% utilization)

---

## Data Collection

### Daily Update (6 AM UTC)

**Triggered by:** GitHub Actions workflow `project-dashboard-update.yml`

**Process:**
1. Fetch data from GitHub APIs:
   - Projects API (sprint velocity, burndown)
   - Issues API (blockers, completion rate)
   - Commits API (activity trends)
2. Parse `feature_list.json` (feature completion)
3. Calculate metrics
4. Save to `project-progress-latest.json`
5. Archive historical snapshot

**Script:** `scripts/update_dashboard.py`

---

### Weekly AI Summary (Monday 9 AM UTC)

**Triggered by:** GitHub Actions workflow `weekly-project-summary.yml`

**Process:**
1. Load last week's metrics
2. Identify trends (velocity changes, blocker patterns)
3. Generate AI summary using Claude:
   - Key accomplishments
   - Velocity trends
   - Risk areas
   - Recommendations
4. Save to `data/ai-summaries/YYYY-WW.md`
5. Email summary to team

**Script:** `scripts/generate_ai_summary.py`

---

## Data Format

### project-progress-latest.json

```json
{
  "timestamp": "2026-02-18T06:00:00Z",
  "sprint_velocity": {
    "current_sprint": "Sprint-2026-W08",
    "velocity_last_6_sprints": [18, 22, 20, 15, 19, 21],
    "average_velocity": 19.2,
    "trend": "stable",
    "confidence": 0.80
  },
  "feature_completion": {
    "total_features": 42,
    "completed": 32,
    "pending": 10,
    "blocked": 0,
    "completion_rate": 0.762,
    "estimated_completion_date": "2026-03-15"
  },
  "burndown": {
    "sprint": "Sprint-2026-W08",
    "total_points": 74,
    "remaining_points": 20,
    "ideal_remaining": 22,
    "days_elapsed": 10,
    "days_remaining": 4,
    "status": "on_track"
  },
  "blockers": {
    "count": 0,
    "top_blockers": []
  },
  "team_utilization": {
    "Jorge": {
      "assigned_points": 40,
      "capacity": 40,
      "utilization": 1.0
    }
  }
}
```

---

## Integration with 7F Lens

**7F Lens Dashboard #2:** Project Progress Dashboard

**URL:** `https://sevenfortunas.dev/dashboards/project-progress`

**Shared Infrastructure:**
- Same hosting (GitHub Pages)
- Same authentication (GitHub OAuth)
- Same styling (7F Lens CSS framework)
- Same update mechanism (GitHub Actions)

**Dashboard Navigation:**
1. AI Advancements Dashboard (Dashboard #1)
2. **Project Progress Dashboard (Dashboard #2)** ← This dashboard
3. Security Intelligence Dashboard (Dashboard #3)
4. EdTech Innovations Dashboard (Dashboard #4)
5. FinTech Trends Dashboard (Dashboard #5)

---

## Usage

### View Dashboard
```bash
# Open in browser
open dashboards/project-progress/index.html

# Or visit live dashboard
open https://sevenfortunas.dev/dashboards/project-progress
```

---

### Manual Update
```bash
# Update metrics
cd dashboards/project-progress
python scripts/update_dashboard.py

# Generate AI summary
python scripts/generate_ai_summary.py
```

---

### Query Metrics via CLI
```bash
# Show current metrics
jq . dashboards/project-progress/data/project-progress-latest.json

# Show velocity trend
jq '.sprint_velocity' dashboards/project-progress/data/project-progress-latest.json

# Show feature completion
jq '.feature_completion' dashboards/project-progress/data/project-progress-latest.json
```

---

## Phase 2 Implementation Plan

**Priority:** P2 (Week 2-3 after MVP launch)

**Implementation Steps:**
1. **Week 1:**
   - Implement `update_dashboard.py`
   - Create GitHub Actions workflow
   - Test data collection from APIs
   - Validate metrics calculations

2. **Week 2:**
   - Implement `generate_ai_summary.py`
   - Create dashboard UI (index.html, styles.css)
   - Test mobile responsiveness
   - Deploy to GitHub Pages

3. **Week 3:**
   - Integrate with 7F Lens navigation
   - Configure email notifications
   - Test end-to-end workflow
   - Train team on dashboard usage

---

## Dependencies

**Python Packages:**
```txt
requests>=2.31.0
anthropic>=0.20.0
PyGithub>=2.1.1
python-dotenv>=1.0.0
```

**GitHub APIs:**
- Projects API (v2 GraphQL)
- Issues API (REST)
- Commits API (REST)

**Secrets Required:**
- `GITHUB_TOKEN` (project and repo access)
- `ANTHROPIC_API_KEY` (for AI summaries)

---

## See Also
- [Sprint Management Guide](../docs/sprint-management-guide.md)
- [GitHub Projects Setup](../docs/github-projects-setup.md)
- FR-8.1: Sprint Management
- FR-8.2: Sprint Dashboard
- FR-4.1: AI Advancements Dashboard

---

**Status:** Phase 2 placeholder - Structure created, full implementation pending
**Next Steps:** Implement data collection scripts, create dashboard UI, deploy to 7F Lens
