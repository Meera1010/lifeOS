"""
Unit Test Suite for Domain Algorithmic Engines
"""

import unittest
from backend.services.spaced_repetition_engine import SpacedRepetitionEngine
from backend.services.sentiment_engine import SentimentEngine


class EnginesTestCase(unittest.TestCase):

    def test_spaced_repetition_sm2(self):
        reps, interval, ef, next_date = SpacedRepetitionEngine.calculate_next_review(
            quality_rating=5,
            repetition_count=0,
            interval_days=1,
            easiness_factor=2.5
        )
        self.assertEqual(reps, 1)
        self.assertEqual(interval, 1)
        self.assertGreaterEqual(ef, 2.5)

    def test_sentiment_engine(self):
        res_pos = SentimentEngine.analyze_text_sentiment("Amazing, happy, productive, flow state!")
        self.assertEqual(res_pos['sentiment'], 'positive')
        self.assertGreater(res_pos['valence_score'], 0.0)

        res_neg = SentimentEngine.analyze_text_sentiment("Stressed, exhausted, overwhelmed, failure.")
        self.assertEqual(res_neg['sentiment'], 'negative')
        self.assertLess(res_neg['valence_score'], 0.0)
