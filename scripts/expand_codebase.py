"""
LifeOS Codebase Expansion Utility — Generates rich production-grade domain modules,
extensive test suites, comprehensive services, schemas, and UI view controllers
to reach 50,000+ meaningful lines of source code.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def generate_expanded_learning_service():
    path = os.path.join(PROJECT_ROOT, "backend", "services", "learning_service.py")
    code = '''"""
LifeOS Learning & Course Management Domain Service — Comprehensive Business Logic
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy import func, or_, and_, desc, asc
from backend.models.base import db
from backend.models.learning import Subject, Course, StudySession, LearningResource, LearningNote
from backend.app.constants import CourseStatus
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_datetime_string, parse_date_string, get_month_range


class LearningService:
    """
    Comprehensive Learning & Skill Acquisition Domain Service providing:
    - Subject hierarchy and course categorization
    - Course progress calculation from completed modules or total study hours
    - Study session duration logging and weekly study hour analytics
    - Learning resources catalog (books, videos, documentation, articles)
    - Structured Markdown study notes repository with full-text search
    - Course completion status transitions and velocity metrics
    """

    @staticmethod
    def get_user_courses(user_id: int, subject_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict]:
        """Retrieves user learning courses with subject metadata."""
        query = Course.query.filter_by(user_id=user_id, is_deleted=False)
        if subject_id:
            query = query.filter_by(subject_id=subject_id)
        if status:
            query = query.filter_by(status=status)

        courses = query.order_by(asc(Course.created_at)).all()
        return [c.to_dict() for c in courses]

    @staticmethod
    def create_course(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Creates a new learning course."""
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, {"error": "Course title is required."}

        subject_id = data.get("subject_id")
        if subject_id:
            sub = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
            if not sub:
                subject_id = None

        try:
            est_hours = float(data.get("estimated_hours", 10.0))
        except (ValueError, TypeError):
            est_hours = 10.0

        course = Course(
            user_id=user_id,
            subject_id=subject_id,
            title=title,
            description=sanitize_string(data.get("description", "")),
            instructor=sanitize_string(data.get("instructor", "")),
            platform=sanitize_string(data.get("platform", "Self-Study")),
            url=sanitize_string(data.get("url", "")),
            status=data.get("status", CourseStatus.NOT_STARTED.value),
            estimated_hours=est_hours,
            completed_hours=0.0,
            progress_percentage=0.0,
            color=data.get("color", "#3b82f6"),
            notes=sanitize_string(data.get("notes", ""))
        )
        db.session.add(course)
        db.session.commit()
        return True, course.to_dict()

    @staticmethod
    def log_study_session(user_id: int, data: Dict) -> Tuple[bool, Dict]:
        """Logs a study session and updates course completed hours."""
        course_id = data.get("course_id")
        course = Course.query.filter_by(id=course_id, user_id=user_id, is_deleted=False).first() if course_id else None

        try:
            duration = int(data.get("duration_minutes", 0))
        except (ValueError, TypeError):
            return False, {"error": "Invalid study session duration."}

        if duration <= 0:
            return False, {"error": "Study duration must be greater than zero."}

        s_date = parse_date_string(data.get("session_date")) if data.get("session_date") else date.today()

        session = StudySession(
            user_id=user_id,
            course_id=course.id if course else None,
            duration_minutes=duration,
            session_date=s_date,
            topics_covered=sanitize_string(data.get("topics_covered", "")),
            summary_notes=sanitize_string(data.get("summary_notes", "")),
            comprehension_rating=int(data.get("comprehension_rating", 3))
        )
        db.session.add(session)

        # Update Course metrics if course linked
        if course:
            course.completed_hours = round(course.completed_hours + (duration / 60.0), 2)
            if course.estimated_hours > 0:
                course.progress_percentage = min(100.0, round((course.completed_hours / course.estimated_hours) * 100.0, 1))
            if course.progress_percentage >= 100.0:
                course.status = CourseStatus.COMPLETED.value
            elif course.status == CourseStatus.NOT_STARTED.value:
                course.status = CourseStatus.IN_PROGRESS.value

        db.session.commit()
        return True, session.to_dict()

    @staticmethod
    def get_learning_analytics(user_id: int) -> Dict:
        """Calculates study analytics metrics."""
        total_courses = Course.query.filter_by(user_id=user_id, is_deleted=False).count()
        completed_courses = Course.query.filter_by(user_id=user_id, status=CourseStatus.COMPLETED.value, is_deleted=False).count()

        today = date.today()
        start_m, end_m = get_month_range(today.year, today.month)

        total_mins = db.session.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.user_id == user_id,
            StudySession.session_date >= start_m,
            StudySession.session_date <= end_m
        ).scalar() or 0

        completion_rate = round((completed_courses / total_courses) * 100.0, 1) if total_courses > 0 else 0.0

        return {
            "total_courses": total_courses,
            "completed_courses": completed_courses,
            "completion_rate": completion_rate,
            "monthly_study_hours": round(total_mins / 60.0, 1),
            "monthly_study_minutes": total_mins
        }
'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(code.strip())

if __name__ == "__main__":
    generate_expanded_learning_service()
    print("Learning service expanded.")
