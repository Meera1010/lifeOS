# LifeOS Technical Architecture Specification Part 28

This document represents part 28 of the authoritative technical documentation suite for **LifeOS — Personal Life Management & Analytics Platform**.

## 1. System Architecture Blueprint & Layering Matrix 28

The **LifeOS** platform is engineered using a robust 3-tier software architecture:

1. **Presentation Layer:** Vanilla HTML5, Vanilla CSS3 Dark Cyber Design System, Vanilla ES6+ Hash Router.
2. **Domain Logic Layer:** Python Flask Application Factory, REST API Blueprints, Analytical Rule Engines.
3. **Persistence Layer:** SQLite 3 Relational Database Engine with WAL mode enabled.

## 2. API Contract Specification & Response Envelopes 28

All HTTP REST endpoints return standardized JSON envelopes:

```json
{
  "success": true,
  "data": { ... },
  "message": "Request processed successfully.",
  "timestamp": "2026-08-29T15:00:00Z"
}
```

## 3. Database Schema Dictionary & Foreign Key Rules 28

- `users` — Stores account credentials, PBKDF2 password hashes, roles, and status flags.
- `tasks` — Manages actionable tasks, priorities, categories, due dates, and soft-delete flags.
- `habits` — Manages habit tracking, daily/weekly frequencies, and active streak counters.
- `goals` — Tracks short and long-term OKRs, weighted milestones, and progress percentages.
- `transactions` — Logs income and expense financial transactions with categories.
