# LifeOS — System Modules Reference & Blueprint Catalog

LifeOS contains 15 core functional modules, each powered by a dedicated Flask Blueprint, domain service, database ORM model, and single-page application view controller.

## Core Modules Overview

1. **Dashboard (`/api/dashboard`)**: Unified overview of daily tasks, habit streaks, Life Score gauge, and smart recommendations.
2. **Task Manager (`/api/tasks`)**: Priority task management with subtasks, tags, categories, and recurring schedules.
3. **Habit Tracker (`/api/habits`)**: Daily habit streaks, 30-day heatmap matrix, and habit scoring.
4. **Goal Management (`/api/goals`)**: Short-term and long-term goals with weighted milestones.
5. **Calendar (`/api/calendar`)**: Unified schedule combining events, task deadlines, and goal target dates.
6. **Finance Manager (`/api/finance`)**: Income and expense tracking, budget thresholds, and savings goals.
7. **Learning Manager (`/api/learning`)**: Course tracking, study sessions, and SuperMemo SM-2 spaced repetition flashcards.
8. **Focus & Pomodoro (`/api/focus`)**: 25-minute Pomodoro timer clock and distraction logger.
9. **Journal (`/api/journal`)**: Markdown daily reflections with rule-based sentiment analysis.
10. **Personal Analytics (`/api/analytics`)**: Composite Life Score calculation engine and trend analytics.
11. **Achievements (`/api/achievements`)**: Gamification engine with 100+ unlockable system badges.
12. **Notifications (`/api/notifications`)**: Alert drawer for task due dates, budget warnings, and achievement unlocks.
13. **User Profile (`/api/users/profile`)**: Personal bio, occupation, location, and motto customization.
14. **Settings (`/api/users/settings`)**: Theme selector (Dark Cyber / Light), time format, and security.
15. **Admin Dashboard (`/api/admin`)**: User account administration, active status toggles, system statistics, and audit logs.
