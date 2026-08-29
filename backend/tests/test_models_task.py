"""
Unit Test Suite for Task and Subtask Models
"""

import unittest
from datetime import datetime
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.models.task import Task, Subtask, TaskCategory, TaskTag


class TaskModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='model_user', email='model@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_task_serialization(self):
        task = Task(
            user_id=self.user.id,
            title='Serialize Test Task',
            priority='high',
            status='pending',
            estimated_minutes=45
        )
        db.session.add(task)
        db.session.commit()

        d = task.to_dict()
        self.assertEqual(d['title'], 'Serialize Test Task')
        self.assertEqual(d['priority'], 'high')
        self.assertEqual(d['estimated_minutes'], 45)

    def test_subtask_toggle(self):
        task = Task(user_id=self.user.id, title='Parent Task')
        db.session.add(task)
        db.session.flush()

        sub = Subtask(task_id=task.id, title='Child Subtask', is_completed=False)
        db.session.add(sub)
        db.session.commit()

        self.assertFalse(sub.is_completed)
        sub.toggle_completion()
        self.assertTrue(sub.is_completed)
