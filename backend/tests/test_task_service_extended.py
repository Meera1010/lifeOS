"""
Unit Test Suite for Task Service Edge Cases & Filtering
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService


class TaskServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='task_tester', email='task_tester@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_task_search_and_filter(self):
        TaskService.create_task(self.user.id, {'title': 'Buy Groceries', 'priority': 'low'})
        TaskService.create_task(self.user.id, {'title': 'System Design Refactor', 'priority': 'urgent'})

        tasks = TaskService.get_user_tasks(self.user.id, {'search': 'Groceries'})
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], 'Buy Groceries')

    def test_batch_complete_tasks(self):
        _, t1 = TaskService.create_task(self.user.id, {'title': 'Task A'})
        _, t2 = TaskService.create_task(self.user.id, {'title': 'Task B'})

        success, res = TaskService.batch_operate_tasks(self.user.id, [t1['id'], t2['id']], 'complete')
        self.assertTrue(success)
        self.assertEqual(res['processed_count'], 2)

    def test_add_subtask(self):
        _, t = TaskService.create_task(self.user.id, {'title': 'Master Task'})
        success, updated = TaskService.add_subtask(self.user.id, t['id'], 'Subtask 1')
        self.assertTrue(success)
        self.assertEqual(len(updated['subtasks']), 1)
