"""
Unit Test Suite for Export Service (JSON and CSV)
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.services.export_service import ExportService


class ExportServiceExtendedTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='export_user', email='export@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_json_and_csv_export(self):
        TaskService.create_task(self.user.id, {'title': 'Exportable Task'})
        
        json_data = ExportService.export_user_data_json(self.user.id)
        self.assertEqual(json_data['platform'], 'LifeOS')
        self.assertEqual(len(json_data['data']['tasks']), 1)

        csv_str = ExportService.export_tasks_csv(self.user.id)
        self.assertIn('Exportable Task', csv_str)
