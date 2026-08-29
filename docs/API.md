# LifeOS — REST API Specification & Endpoint Reference

All REST API endpoints return standard JSON responses:

```json
{
  "success": true,
  "message": "Operation description",
  "data": { ... }
}
```

## Endpoint Overview

### 1. Authentication
- `POST /api/auth/register` — Register new user account.
- `POST /api/auth/login` — Authenticate credentials & return JWT token.
- `GET /api/auth/me` — Retrieve active user identity.
- `POST /api/auth/change-password` — Update user password.

### 2. Task Manager
- `GET /api/tasks` — List tasks with filters (`priority`, `status`, `category_id`, `search`).
- `POST /api/tasks` — Create new task with subtasks & tags.
- `PUT /api/tasks/<id>` — Update task details or mark status.
- `DELETE /api/tasks/<id>` — Soft-delete task.
- `POST /api/tasks/subtasks/<id>/toggle` — Toggle subtask completion status.
- `GET /api/tasks/statistics` — Get task completion metrics.

### 3. Habit Tracker
- `GET /api/habits` — Get active habits and streaks.
- `POST /api/habits` — Create habit.
- `POST /api/habits/<id>/toggle` — Toggle daily completion.
- `GET /api/habits/calendar-matrix` — Get 30-day completion matrix.

### 4. Goal Management
- `GET /api/goals` — List goals.
- `POST /api/goals` — Create goal.
- `PUT /api/goals/<id>` — Update goal progress.
- `POST /api/goals/milestones/<id>/toggle` — Toggle milestone.

### 5. Personal Finance
- `GET /api/finance/transactions` — Query financial transactions.
- `POST /api/finance/transactions` — Log income or expense.
- `GET /api/finance/summary` — Get monthly income, expense, and savings rate.

### 6. Personal Analytics & Life Score
- `GET /api/analytics/dashboard` — Get central dashboard summary.
- `GET /api/analytics/life-score` — Get dynamic Life Score & pillar breakdown.
- `GET /api/analytics/insights` — Get rule-based Smart Insights.

### 7. Achievements & Gamification
- `GET /api/achievements` — Get 50+ system achievements & unlock status.
- `POST /api/achievements/evaluate` — Evaluate achievement unlock criteria.

### 8. Administrator Panel
- `GET /api/admin/users` — List system user accounts.
- `PUT /api/admin/users/<id>/status` — Enable or disable user account.
- `DELETE /api/admin/users/<id>` — Delete user account.
- `GET /api/admin/audit-logs` — Query system audit logs.
