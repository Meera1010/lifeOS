"""
LifeOS Automated Unit Tests — Task Manager
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.services.auth_service import AuthService
from backend.services.task_service import TaskService

class TaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        ok, res = AuthService.register_user({
            "username": "taskuser",
            "email": "task@example.com",
            "password": "Password123!"
        })
        self.user_id = res["user"]["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_retrieve_task(self):
        ok, task = TaskService.create_task(self.user_id, {
            "title": "Build Unit Tests",
            "description": "Write comprehensive unit test cases",
            "priority": "high",
            "estimated_minutes": 60,
            "subtasks": [{"title": "Subtask 1"}, {"title": "Subtask 2"}]
        })
        self.assertTrue(ok)
        self.assertEqual(task["title"], "Build Unit Tests")
        self.assertEqual(len(task["subtasks"]), 2)

        tasks = TaskService.get_user_tasks(self.user_id)
        self.assertEqual(len(tasks), 1)

    def test_update_and_complete_task(self):
        ok, task = TaskService.create_task(self.user_id, {"title": "Pending Task"})
        self.assertTrue(ok)

        ok, updated = TaskService.update_task(self.user_id, task["id"], {"status": "completed"})
        self.assertTrue(ok)
        self.assertEqual(updated["status"], "completed")
        self.assertIsNotNone(updated["completed_at"])

    def test_task_statistics(self):
        TaskService.create_task(self.user_id, {"title": "Task 1", "status": "completed"})
        TaskService.create_task(self.user_id, {"title": "Task 2", "status": "pending"})
        
        stats = TaskService.get_task_statistics(self.user_id)
        self.assertEqual(stats["total_tasks"], 2)
        self.assertEqual(stats["completed_tasks"], 1)
        self.assertEqual(stats["completion_rate"], 50.0)

if __name__ == "__main__":
    unittest.main()
