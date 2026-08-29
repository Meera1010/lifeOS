# LifeOS — Automated Testing Documentation

LifeOS includes an extensive unit and integration test suite written with Python's standard `unittest` framework.

## Running Tests

Execute the full backend test suite:

```bash
python -m unittest discover -s backend/tests
```

Run test suite with coverage report:

```bash
coverage run -m unittest discover -s backend/tests
coverage report -m
```

## Test Coverage Map

- `test_auth.py`: Registration, login, duplicate email checks, password validation.
- `test_tasks.py`: Task CRUD, subtask toggling, status updates, completion rate calculations.
- `test_habits.py`: Habit creation, completion toggle, streak calculations.
- `test_goals.py`: Goal progress recalculation, milestone toggles.
- `test_finance.py`: Income/expense transactions, monthly budget checks, net savings.
- `test_analytics.py`: Life Score calculation engine, Smart Insights generation.
- `test_achievements.py`: System achievements seeding, unlock condition evaluations.
- `test_admin.py`: User administration, active status toggles, audit logs.
- `test_security.py`: Password hashing, string escaping, XSS prevention.
