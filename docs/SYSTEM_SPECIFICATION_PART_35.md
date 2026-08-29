# LifeOS Architecture & System Specification Part 35

This document forms part 35 of the technical documentation for **LifeOS — Personal Life Management & Analytics Platform**.

## 1. Executive Summary & Core Requirements Specification 35

- **System Architecture:** 3-Tier Layered Architecture (Presentation, Business Logic, Persistence).
- **Backend Framework:** Python Flask with Application Factory & SQLAlchemy ORM.
- **Frontend Stack:** Single Page Application (SPA), Vanilla HTML5, Vanilla CSS3 (Dark Cyber Theme), Vanilla ES6+ JS.
- **Database Engine:** SQLite 3 with WAL Mode, foreign keys, soft delete mixins, and indexed schemas.

## 2. API Endpoint Specification & Response Envelopes 35

All REST API endpoints conform to standard JSON response envelopes:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully.",
  "timestamp": "2026-08-29T15:00:00Z"
}
```

## 3. Data Dictionary & Entity Relationship Definitions 35

- `users` (id, username, email, password_hash, role, is_active, created_at, updated_at)
- `tasks` (id, user_id, title, description, status, priority, category, due_date, is_deleted)
- `habits` (id, user_id, title, frequency, target_days, current_streak, best_streak, is_deleted)
- `goals` (id, user_id, title, category, target_date, progress_pct, status, is_deleted)
- `transactions` (id, user_id, amount, transaction_type, category, transaction_date, is_deleted)
