# LifeOS — Personal Life Management & Analytics Platform

**LifeOS** is a comprehensive, production-grade web platform for personal productivity, habit formation, goal tracking, financial analytics, learning systems, focus management, and executive life scoring.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Build](#build)
- [Run](#run)
- [Usage](#usage)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)

---

## 🎯 Overview

LifeOS integrates 15 core domain management modules into a unified Single Page Application (SPA):
1. **Executive Dashboard:** Daily overview, composite Life Score gauge, smart behavioral insights.
2. **Task Manager:** Priorities, category tags, recurring schedules, subtask hierarchies.
3. **Habit Tracker:** Active streak counters, 30-day completion heatmap matrices, consistency scoring.
4. **Goal Management (OKRs):** Short & long-term targets, weighted milestones, progress history.
5. **Unified Calendar:** Consolidated monthly schedule combining events, task deadlines, and milestones.
6. **Finance Manager:** Income & expense tracking, monthly budget thresholds, savings goals, cash flow forecasts.
7. **Learning Hub:** Course tracker, study session logs, SuperMemo SM-2 flashcard spaced repetition.
8. **Focus & Pomodoro:** 25-minute Pomodoro timer, distraction logger, flow state ratings.
9. **Journal & Reflections:** Rich entries, mood selection, NLP text sentiment and valence index.
10. **Personal Analytics:** Dynamic 6-pillar score breakdown, activity trends, cross-domain correlations.
11. **Achievements System:** Gamification engine evaluating 100+ system badges across 5 tiers.
12. **Notification Engine:** System alerts for task due dates, budget warnings, and achievement unlocks.
13. **User Profile:** Account bio, occupation, location, life motto, system metrics.
14. **Settings:** Theme selector (Dark Cyber / Light), time format (12h/24h), security configuration.
15. **Admin Panel:** User management, account disable/enable, security audit logs, health diagnostics.

---

## 🏗️ Architecture

- **Backend:** Python Flask Application Factory (`backend/app/`), SQLAlchemy ORM (`backend/models/`), PBKDF2-SHA256 password security, JWT authorization middleware (`backend/security/`).
- **Frontend:** Single Page Application (SPA) using Vanilla HTML5 (`frontend/index.html`), Vanilla CSS3 (`frontend/css/`), Vanilla ES6+ JavaScript (`frontend/js/`), custom HTML5 Canvas micro-chart engine (`frontend/js/components/chartEngine.js`).
- **Database:** SQLite 3 (`data/lifeos.db`) with WAL mode, foreign keys, soft-delete mixins, and indexed schemas.

---

## 🛠️ Dependencies

- **Python 3.8+**
- **Flask (v2.2.5)**
- **Flask-SQLAlchemy (v3.0.5)**
- **Flask-CORS (v3.0.10)**
- **PyJWT (v2.6.0)**
- **SQLAlchemy (v1.4.49)**

Manifests and lockfiles:
- `requirements.txt`
- `requirements.lock`
- `package.json`
- `package-lock.json`

---

## ⚙️ Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/Meera1010/lifeOS.git
cd lifeOS
```

### Step 2: Create & Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Alternatively using npm:
```bash
npm install
```

---

## 🔨 Build

To initialize the SQLite database and seed realistic sample data:

```bash
python data/init_db.py
```

Or using Makefile / npm:
```bash
make build
# OR
npm run build
```

---

## 🚀 Run

### Option A: Using Python Entrypoint (Recommended)
```bash
python run.py
```
Or:
```bash
python main.py
```

### Option B: Using npm Scripts
```bash
npm start
# OR
npm run serve
```

### Option C: Using Makefile
```bash
make run
```

Open browser at `http://127.0.0.1:5000`

---

## 🔑 Default Credentials

- **Standard User:** Username: `alex_dev` | Password: `UserPass123!`
- **Admin User:** Username: `admin` | Password: `AdminPass123!`

---

## 🧪 Testing

Execute automated unit test suites:

```bash
python -m unittest discover -s backend/tests
```

Or using Makefile:
```bash
make test
```

---

## 🐳 Docker Deployment

Build Docker container:
```bash
docker build -t lifeos .
```

Run Docker container:
```bash
docker run -p 5000:5000 lifeos
```

Or using Docker Compose:
```bash
docker-compose up --build
```
