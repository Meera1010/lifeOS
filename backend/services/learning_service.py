"""
LifeOS Learning Manager Domain Service
"""

from datetime import datetime, date, timedelta
from sqlalchemy import func
from backend.models.base import db
from backend.models.learning import Subject, Course, StudySession, LearningResource, LearningNote
from backend.security.validators import sanitize_string
from backend.utilities.date_utils import parse_date_string, get_month_range, get_week_range

class LearningService:

    @staticmethod
    def get_user_courses(user_id: int, subject_id: int = None) -> list:
        query = Course.query.filter_by(user_id=user_id, is_deleted=False)
        if subject_id:
            query = query.filter_by(subject_id=subject_id)
        courses = query.order_by(Course.created_at.desc()).all()
        return [c.to_dict() for c in courses]

    @staticmethod
    def create_course(user_id: int, data: dict) -> tuple:
        title = sanitize_string(data.get("title", ""))
        if not title:
            return False, "Course title is required."

        course = Course(
            user_id=user_id,
            subject_id=data.get("subject_id"),
            title=title,
            provider=sanitize_string(data.get("provider", "")),
            instructor=sanitize_string(data.get("instructor", "")),
            total_modules=int(data.get("total_modules", 10)),
            completed_modules=int(data.get("completed_modules", 0)),
            total_hours_estimated=float(data.get("total_hours_estimated", 0.0)),
            notes=sanitize_string(data.get("notes", ""))
        )
        course.update_progress()
        db.session.add(course)
        db.session.commit()
        return True, course.to_dict()

    @staticmethod
    def log_study_session(user_id: int, data: dict) -> tuple:
        title = sanitize_string(data.get("title", "")) or "Study Session"

        try:
            duration = int(data.get("duration_minutes", 0))
        except (ValueError, TypeError):
            return False, "Invalid session duration."

        if duration <= 0:
            return False, "Duration must be greater than zero minutes."

        session = StudySession(
            user_id=user_id,
            course_id=data.get("course_id"),
            subject_id=data.get("subject_id"),
            title=title,
            duration_minutes=duration,
            session_date=parse_date_string(data.get("session_date")) if data.get("session_date") else date.today(),
            topics_covered=sanitize_string(data.get("topics_covered", "")),
            key_takeaways=sanitize_string(data.get("key_takeaways", "")),
            comprehension_rating=int(data.get("comprehension_rating", 4))
        )
        db.session.add(session)

        # Update course spent hours
        if data.get("course_id"):
            course = Course.query.get(data["course_id"])
            if course and course.user_id == user_id:
                course.total_hours_spent += round(duration / 60.0, 2)
                db.session.add(course)

        db.session.commit()
        return True, session.to_dict()

    @staticmethod
    def get_learning_analytics(user_id: int) -> dict:
        total_courses = Course.query.filter_by(user_id=user_id, is_deleted=False).count()
        completed_courses = Course.query.filter_by(user_id=user_id, status="completed", is_deleted=False).count()
        
        start_w, end_w = get_week_range(date.today())
        weekly_mins = db.session.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.user_id == user_id,
            StudySession.session_date >= start_w,
            StudySession.session_date <= end_w
        ).scalar() or 0

        start_m, end_m = get_month_range(date.today().year, date.today().month)
        monthly_mins = db.session.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.user_id == user_id,
            StudySession.session_date >= start_m,
            StudySession.session_date <= end_m
        ).scalar() or 0

        return {
            "total_courses": total_courses,
            "completed_courses": completed_courses,
            "weekly_study_hours": round(weekly_mins / 60.0, 1),
            "monthly_study_hours": round(monthly_mins / 60.0, 1),
            "completion_rate": round((completed_courses / total_courses) * 100.0, 1) if total_courses > 0 else 0.0
        }
