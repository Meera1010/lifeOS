"""
LifeOS Full Scale Builder — Generates comprehensive route test suites and technical documentation.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def write_file(rel_path, content):
    abs_path = os.path.join(PROJECT_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_route_test_suites():
    # 1. test_routes_tasks.py
    write_file("backend/tests/test_routes_tasks.py", '''"""
Integration Test Suite for Tasks API Blueprint Routes
"""

import unittest
import json
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User


class TasksRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='route_task_user', email='route_task@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

        # Login to get JWT Token
        res = self.client.post('/api/auth/login', json={'email': 'route_task@example.com', 'password': 'Password123!'})
        self.token = json.loads(res.data)['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_tasks_api_lifecycle(self):
        # Create Task
        res_create = self.client.post('/api/tasks', json={'title': 'API Route Task', 'priority': 'high'}, headers=self.headers)
        self.assertEqual(res_create.status_code, 201)
        data_c = json.loads(res_create.data)['data']
        task_id = data_c['id']

        # Get Tasks
        res_get = self.client.get('/api/tasks', headers=self.headers)
        self.assertEqual(res_get.status_code, 200)

        # Update Task
        res_put = self.client.put(f'/api/tasks/{task_id}', json={'status': 'completed'}, headers=self.headers)
        self.assertEqual(res_put.status_code, 200)

        # Delete Task
        res_del = self.client.delete(f'/api/tasks/{task_id}', headers=self.headers)
        self.assertEqual(res_del.status_code, 200)
''')

    # 2. test_routes_habits.py
    write_file("backend/tests/test_routes_habits.py", '''"""
Integration Test Suite for Habits API Blueprint Routes
"""

import unittest
import json
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User


class HabitsRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='route_habit_user', email='route_habit@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

        res = self.client.post('/api/auth/login', json={'email': 'route_habit@example.com', 'password': 'Password123!'})
        self.token = json.loads(res.data)['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_habits_api_lifecycle(self):
        res_create = self.client.post('/api/habits', json={'title': 'API Route Habit'}, headers=self.headers)
        self.assertEqual(res_create.status_code, 201)
        habit_id = json.loads(res_create.data)['data']['id']

        res_toggle = self.client.post(f'/api/habits/{habit_id}/toggle', json={'status': 'completed'}, headers=self.headers)
        self.assertEqual(res_toggle.status_code, 200)

        res_matrix = self.client.get('/api/habits/calendar-matrix', headers=self.headers)
        self.assertEqual(res_matrix.status_code, 200)
''')

    # 3. test_routes_finance.py
    write_file("backend/tests/test_routes_finance.py", '''"""
Integration Test Suite for Finance API Blueprint Routes
"""

import unittest
import json
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User


class FinanceRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='route_fin_user', email='route_fin@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

        res = self.client.post('/api/auth/login', json={'email': 'route_fin@example.com', 'password': 'Password123!'})
        self.token = json.loads(res.data)['data']['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_finance_api_lifecycle(self):
        res_create = self.client.post('/api/finance/transactions', json={
            'type': 'income',
            'amount': 3000.0,
            'description': 'Freelance Client Payment'
        }, headers=self.headers)
        self.assertEqual(res_create.status_code, 201)

        res_summary = self.client.get('/api/finance/summary', headers=self.headers)
        self.assertEqual(res_summary.status_code, 200)
''')

def generate_docs():
    write_file("docs/MODULES.md", '''# LifeOS — System Modules Reference & Blueprint Catalog

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
''')

def main():
    print("Building route test suites and module documentation...")
    generate_route_test_suites()
    generate_docs()
    print("Build complete.")

if __name__ == "__main__":
    main()
