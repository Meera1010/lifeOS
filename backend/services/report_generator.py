"""
LifeOS Executive Life Report Generator Domain Service
"""

from datetime import datetime, date
from typing import Dict, Any
from backend.services.analytics_service import AnalyticsService
from backend.services.life_score_engine import LifeScoreEngine


class ReportGenerator:
    """
    Executive Report Generator Domain Service providing:
    - Weekly and monthly markdown report generation
    - Life Score pillar breakdown synthesis
    - Performance summary & key recommendation formatting
    """

    @staticmethod
    def generate_weekly_report_markdown(user_id: int) -> str:
        """Generates a Markdown executive report for the past week."""
        life_score = LifeScoreEngine.calculate_user_life_score(user_id)
        exec_dash = AnalyticsService.get_executive_dashboard(user_id)

        now_str = datetime.utcnow().strftime("%Y-%m-%d")

        md = "# 📊 LifeOS Executive Weekly Performance Report\n"
        md += f"**Generated Date:** {now_str}\n"
        md += f"**User ID:** {user_id}\n\n---\n\n"
        md += "## 🏆 Life Score Summary\n"
        md += f"- **Overall Life Score:** {life_score['overall_score']}%\n"
        md += f"- **Score Change:** {life_score['score_change']:+f}% compared to previous period\n\n"
        md += "### Pillar Performance Breakdown\n"
        md += f"- **Productivity:** {life_score['breakdown']['productivity']}%\n"
        md += f"- **Habits:** {life_score['breakdown']['habits']}%\n"
        md += f"- **Goals:** {life_score['breakdown']['goals']}%\n"
        md += f"- **Learning:** {life_score['breakdown']['learning']}%\n"
        md += f"- **Finance:** {life_score['breakdown']['finance']}%\n"
        md += f"- **Focus:** {life_score['breakdown']['focus']}%\n\n---\n\n"
        md += "## 💡 Key Action Recommendations\n"

        for sug in life_score.get("suggestions", []):
            md += f"- {sug}\n"

        md += "\n---\n*Report generated automatically by LifeOS Personal Life Management Platform.*\n"
        return md
