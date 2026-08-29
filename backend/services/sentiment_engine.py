"""
LifeOS Journal Sentiment & Valence Analysis Engine
"""

import re
from typing import Dict, List, Tuple

# Positive & Negative Sentiment Keyword Lexicons
POSITIVE_WORDS = {
    "great", "excellent", "amazing", "productive", "happy", "accomplished", "focus",
    "flow", "inspired", "grateful", "success", "energized", "calm", "confident",
    "clarity", "triumph", "joy", "peaceful", "motivated", "triumphant", "growth"
}

NEGATIVE_WORDS = {
    "tired", "stressed", "anxious", "frustrated", "overwhelmed", "distracted",
    "exhausted", "failure", "delay", "sad", "unmotivated", "procrastinate",
    "worried", "stuck", "doubt", "lonely", "anger", "conflict", "problem"
}

class SentimentEngine:

    @staticmethod
    def analyze_text_sentiment(text: str) -> Dict:
        """
        Analyzes journal entry text content using rule-based lexicon scoring:
        - Valence Score: -1.0 (extremely negative) to +1.0 (extremely positive)
        - Sentiment Label: positive, neutral, negative
        - Extracted Keywords
        """
        if not text or not isinstance(text, str):
            return {
                "valence_score": 0.0,
                "sentiment": "neutral",
                "positive_count": 0,
                "negative_count": 0,
                "matched_keywords": []
            }

        # Tokenize text
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        total_words = len(words)

        if total_words == 0:
            return {
                "valence_score": 0.0,
                "sentiment": "neutral",
                "positive_count": 0,
                "negative_count": 0,
                "matched_keywords": []
            }

        pos_matches = [w for w in words if w in POSITIVE_WORDS]
        neg_matches = [w for w in words if w in NEGATIVE_WORDS]

        pos_count = len(pos_matches)
        neg_count = len(neg_matches)

        if pos_count == 0 and neg_count == 0:
            score = 0.0
            sentiment = "neutral"
        else:
            score = (pos_count - neg_count) / (pos_count + neg_count)
            if score > 0.2:
                sentiment = "positive"
            elif score < -0.2:
                sentiment = "negative"
            else:
                sentiment = "neutral"

        return {
            "valence_score": round(score, 2),
            "sentiment": sentiment,
            "positive_count": pos_count,
            "negative_count": neg_count,
            "matched_keywords": list(set(pos_matches + neg_matches))
        }

    @staticmethod
    def compute_emotional_wellbeing_index(entries: List[Dict]) -> Dict:
        """Computes aggregate emotional well-being index across journal entries."""
        if not entries:
            return {"wellbeing_index": 50.0, "dominant_sentiment": "neutral"}

        total_valence = 0.0
        sentiments = {"positive": 0, "neutral": 0, "negative": 0}

        for e in entries:
            analysis = SentimentEngine.analyze_text_sentiment(e.get("content", ""))
            total_valence += analysis["valence_score"]
            sentiments[analysis["sentiment"]] += 1

        avg_valence = total_valence / len(entries)
        index = round(min(100.0, max(0.0, (avg_valence + 1.0) * 50.0)), 1)
        dominant = max(sentiments, key=sentiments.get)

        return {
            "wellbeing_index": index,
            "dominant_sentiment": dominant,
            "sentiment_counts": sentiments
        }
