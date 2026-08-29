# LifeOS — Database Schema & Data Dictionary

The LifeOS persistence layer utilizes SQLite 3 with SQLAlchemy ORM. The relational model contains 19 tables.

## Entity Relationship Summary

```
                      +-------------------+
                      |       Users       |
                      +---------+---------+
                                | 1:1
              +-----------------+-----------------+
              |                 |                 |
     +--------v-------+ +-------v-------+ +-------v-------+
     |  UserProfiles  | | UserSettings  | | DashboardPref |
     +----------------+ +---------------+ +---------------+
                                | 1:N
        +-----------------------+-----------------------+
        |                       |                       |
+-------v-------+       +-------v-------+       +-------v-------+
|     Tasks     |       |    Habits     |       |     Goals     |
+-------+-------+       +-------+-------+       +-------+-------+
        | 1:N                   | 1:N                   | 1:N
+-------v-------+       +-------v-------+       +-------v-------+
|   Subtasks    |       | HabitComplet  |       |  Milestones   |
+---------------+       +---------------+       +---------------+
```

## Detailed Table Schemas

### 1. `users`
- `id` (INTEGER, Primary Key)
- `username` (VARCHAR(80), Unique, Indexed)
- `email` (VARCHAR(120), Unique, Indexed)
- `password_hash` (VARCHAR(256), NOT NULL)
- `role` (VARCHAR(20), Default: 'user')
- `is_active` (BOOLEAN, Default: True)
- `last_login` (DATETIME)
- `created_at`, `updated_at` (DATETIME)

### 2. `tasks`
- `id` (INTEGER, Primary Key)
- `user_id` (INTEGER, FK -> users.id, Indexed)
- `title` (VARCHAR(200), Indexed)
- `description` (TEXT)
- `priority` (VARCHAR(20), Default: 'medium')
- `status` (VARCHAR(20), Default: 'pending')
- `due_date` (DATETIME, Indexed)
- `estimated_minutes` (INTEGER)
- `actual_minutes` (INTEGER)
- `is_recurring` (BOOLEAN)
- `recurrence_pattern` (VARCHAR(50))

### 3. `habits`
- `id` (INTEGER, Primary Key)
- `user_id` (INTEGER, FK -> users.id, Indexed)
- `title` (VARCHAR(150))
- `category` (VARCHAR(50))
- `frequency` (VARCHAR(20))
- `current_streak` (INTEGER, Default: 0)
- `best_streak` (INTEGER, Default: 0)
- `total_completions` (INTEGER, Default: 0)

### 4. `goals`
- `id` (INTEGER, Primary Key)
- `user_id` (INTEGER, FK -> users.id, Indexed)
- `title` (VARCHAR(200))
- `category` (VARCHAR(50))
- `timeframe` (VARCHAR(30))
- `progress_percentage` (FLOAT, Default: 0.0)

### 5. `finance_transactions`
- `id` (INTEGER, Primary Key)
- `user_id` (INTEGER, FK -> users.id, Indexed)
- `category_id` (INTEGER, FK -> finance_categories.id)
- `type` (VARCHAR(20)) -- 'income', 'expense'
- `amount` (FLOAT)
- `transaction_date` (DATE, Indexed)

### 6. `achievements`
- `code` (VARCHAR(50), Unique, Primary Key)
- `title` (VARCHAR(100))
- `badge_tier` (VARCHAR(20)) -- 'bronze', 'silver', 'gold', 'platinum', 'diamond'
- `points` (INTEGER)
- `threshold` (INTEGER)
