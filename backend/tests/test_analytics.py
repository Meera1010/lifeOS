"""
LifeOS Automated Unit Tests — Analytics & Life Score Engine
"""

import unittest
from backend.app import create_app
from backend.models.base import db
from backend.services.auth_service import AuthService
from backend.services.life_score_engine import LifeScoreEngine
from backend.services.smart_insights_engine import SmartInsightsEngine

class AnalyticsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        ok, res = AuthService.register_user({
            "username": "analyticsuser",
            "email": "analytics@example.com",
            "password": "Password123!"
        })
        self.user_id = res["user"]["id"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_life_score_calculation(self):
        score_data = LifeScoreEngine.calculate_user_life_score(self.user_id)
        self.assertIn("overall_score", score_data)
        self.assertIn("breakdown", score_data)
        self.assertGreaterEqual(score_data["overall_score"], 0.0)

    def test_smart_insights_generation(self):
        insights = SmartInsightsEngine.generate_user_insights(self.user_id)
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)

if __name__ == "__main__":
    unittest.main()
