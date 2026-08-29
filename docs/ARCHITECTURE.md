# LifeOS — System Architecture & Design Documentation

LifeOS is an enterprise-grade, highly scalable personal life management, productivity, financial, learning, journal, habit, goal, and analytics platform designed following the 3-Tier Architecture (Presentation Layer, Business Logic Layer, Data Persistence Layer).

## 1. High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT / FRONTEND                                 |
|  Vanilla JavaScript ES6+ (SPA) | Vanilla CSS3 (Dark/Glassmorphic) | HTML5 Shell |
|  - Custom SPA Router (#dashboard, #tasks, #habits, #goals, #finance, #analytics)  |
|  - Custom Canvas & Micro-Chart Engine (Radial Gauge, Line, Bar, Pie)              |
|  - Global State Store & Token Storage                                             |
+---------------------------------------------------------+-------------------------+
                                                          |
                                           REST API (JSON over HTTP/CORS)
                                                          |
+---------------------------------------------------------v-------------------------+
|                                 BACKEND LOGIC (FLASK)                             |
|  Flask Application Factory & Blueprint Modular Routing                            |
|  - Security Middleware (JWT Bearer Token Auth, RBAC Authorization)                |
|  - Validation Engine (XSS Escaping, Input Bounds, SQL Sanitization)                |
|  - Domain Business Services (18 Dedicated Domain Services)                        |
|  - Life Score Engine & Smart Insights Rule Engine                                 |
|  - 50+ Achievement Gamification Evaluator                                         |
+---------------------------------------------------------+-------------------------+
                                                          |
                                          SQLAlchemy ORM Mapping
                                                          |
+---------------------------------------------------------v-------------------------+
|                                  DATA PERSISTENCE LAYER                           |
|  SQLite 3 Database (Relational Engine)                                            |
|  - 19 Tables with Referential Integrity, Cascade Deletes, Indexes                 |
|  - Seed Data Generator & Audit Log System                                         |
+-----------------------------------------------------------------------------------+
```

## 2. Layered Component Responsibilities

### Presentation Layer (Frontend)
- Built entirely with native HTML5, CSS3 (using CSS Variables and backdrop filters), and Vanilla JavaScript ES6+ without heavy node/react dependencies.
- SPA Client-Side Router handles browser history and view mounts seamlessly.
- Custom Canvas chart engine renders real-time interactive charts directly without third-party JS canvas bloat.

### Business Logic Layer (Backend Services)
- `AuthService`: Authentication, password hashing (PBKDF2:SHA256), JWT token issuance.
- `TaskService`: Task lifecycle, recurring task scheduling, subtask completion calculation.
- `HabitService`: Habit streak calculation, 30-day completion matrix, score computation.
- `GoalService`: Goal milestone tracking, metric recalculation, history logger.
- `FinanceService`: Financial transactions, budget threshold alert engine, savings rate.
- `LearningService`: Course progress calculation, study session time logging.
- `FocusService`: Focus sessions, distraction logs, Pomodoro timer state sync.
- `LifeScoreEngine`: Dynamic 6-pillar composite Life Score calculator.
- `SmartInsightsEngine`: Rule-based analytics engine generating behavioral insights.
- `AchievementEngine`: System evaluating 50+ unique achievements and awarding badges.

### Persistence Layer (Database)
- Relational SQLite 3 schema managed via Flask-SQLAlchemy.
- Soft-delete mixins, timestamp mixins, and serializable base models ensure data consistency.
