# LifeOS — User & Platform Operator Guide

Welcome to **LifeOS** — your personal life management and analytics platform.

## Quick Start Guide

### 1. Installation & Environment Setup
Clone repository and navigate to directory:

```bash
cd e:\lifeos
python -m pip install -r requirements.txt
```

### 2. Database Initialization
Initialize database tables and seed realistic sample data:

```bash
python data/init_db.py
```

### 3. Launch Application
Start local web server on port 5000:

```bash
python run.py
```

Open browser at `http://127.0.0.1:5000`.

### 4. Credentials
Default seeded accounts:
- **Normal User**: Username `alex_dev` | Password `UserPass123!`
- **Administrator**: Username `admin` | Password `AdminPass123!`

---

## Core Feature Overview

1. **Dashboard**: Daily overview, Life Score gauge, quick metrics, weekly productivity chart, Smart Insights.
2. **Task Manager**: Organize tasks by priority, set due dates, add subtasks, and track progress.
3. **Habit Tracker**: Build daily streaks, view 30-day completion heatmap matrix.
4. **Goal Management**: Define short/long-term goals with milestones.
5. **Calendar**: Interactive monthly schedule combining events, task deadlines, and goal milestones.
6. **Finance Manager**: Log income/expenses, monitor savings rate, and category spending breakdown.
7. **Learning Hub**: Track courses, subjects, study session hours, and notes.
8. **Focus & Pomodoro**: 25-minute Pomodoro timer clock, distraction logger.
9. **Journal**: Daily rich text reflections, mood tracking.
10. **Personal Analytics**: Pillar score breakdowns and recommendation insights.
11. **Achievements**: 50+ unlockable badges across all system modules.
12. **Admin Panel**: User administration and audit logs.
