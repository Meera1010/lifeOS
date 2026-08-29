"""
LifeOS Spaced Repetition Engine (SuperMemo SM-2 Algorithm Implementation)
"""

from datetime import datetime, date, timedelta
from typing import Dict, Tuple

class SpacedRepetitionEngine:
    """
    Implements the SuperMemo SM-2 Spaced Repetition Algorithm for learning courses and flashcards.
    
    Algorithm Constants:
    - Minimum Easiness Factor (EF): 1.3
    - Quality Rating Scale: 0 (total blackout) to 5 (perfect response)
    """

    DEFAULT_EASINESS_FACTOR = 2.5
    MIN_EASINESS_FACTOR = 1.3

    @staticmethod
    def calculate_next_review(quality_rating: int, repetition_count: int, interval_days: int, easiness_factor: float) -> Tuple[int, int, float, date]:
        """
        Calculates next review schedule based on SM-2 formula:
        - EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        - Interval(1) = 1 day
        - Interval(2) = 6 days
        - Interval(n) = Interval(n-1) * EF'
        """
        q = max(0, min(5, quality_rating))
        ef = easiness_factor

        if q >= 3:
            if repetition_count == 0:
                new_interval = 1
            elif repetition_count == 1:
                new_interval = 6
            else:
                new_interval = int(round(interval_days * ef))
            
            new_repetition_count = repetition_count + 1
        else:
            new_repetition_count = 0
            new_interval = 1

        # Calculate new Easiness Factor
        new_ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        if new_ef < SpacedRepetitionEngine.MIN_EASINESS_FACTOR:
            new_ef = SpacedRepetitionEngine.MIN_EASINESS_FACTOR

        next_date = date.today() + timedelta(days=new_interval)

        return new_repetition_count, new_interval, round(new_ef, 3), next_date

    @staticmethod
    def format_review_card_state(repetition_count: int, interval_days: int, easiness_factor: float, next_date: date) -> Dict:
        """Formats flashcard review state dictionary."""
        return {
            "repetition_count": repetition_count,
            "interval_days": interval_days,
            "easiness_factor": easiness_factor,
            "next_review_date": next_date.strftime("%Y-%m-%d"),
            "is_due_today": next_date <= date.today()
        }
