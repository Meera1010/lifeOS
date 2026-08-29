# LifeOS Domain & API Reference Documentation Part 2

This document provides complete reference specifications for **LifeOS Platform Part 2**.

## 1. Component Architecture & Data Model Matrix 2

- **Entity Model:** Relational schema managed via SQLAlchemy ORM.
- **REST Envelopes:** Standardized success and error response wrappers.
- **Security:** Token-based JWT authorization header verification.

## 2. API Route Endpoints & Query Parameters 2

All endpoints accept and return `application/json` content.
- `GET /api/tasks` — List active tasks with priority and status filters.
- `POST /api/tasks` — Create new task entity.
- `PUT /api/tasks/<id>` — Update task attributes or status.
- `DELETE /api/tasks/<id>` — Soft-delete task record.
