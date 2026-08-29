"""
LifeOS Learning Manager Models
"""

from datetime import datetime, date
from backend.models.base import db, TimestampMixin, SoftDeleteMixin, SerializerMixin

class Subject(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "learning_subjects"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), default="#8b5cf6", nullable=False)
    icon = db.Column(db.String(50), default="book-open", nullable=False)
    description = db.Column(db.Text, nullable=True)

    courses = db.relationship("Course", backref="subject", lazy="dynamic")
    study_sessions = db.relationship("StudySession", backref="subject", lazy="dynamic")


class Course(db.Model, TimestampMixin, SoftDeleteMixin, SerializerMixin):
    __tablename__ = "learning_courses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("learning_subjects.id"), nullable=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    provider = db.Column(db.String(100), nullable=True) # Coursera, Udemy, University, Self-study
    instructor = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(30), default="in_progress", nullable=False) # not_started, in_progress, completed, paused
    
    total_modules = db.Column(db.Integer, default=10, nullable=False)
    completed_modules = db.Column(db.Integer, default=0, nullable=False)
    progress_percentage = db.Column(db.Float, default=0.0, nullable=False)
    
    total_hours_estimated = db.Column(db.Float, default=0.0, nullable=False)
    total_hours_spent = db.Column(db.Float, default=0.0, nullable=False)
    
    certificate_url = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    study_sessions = db.relationship("StudySession", backref="course", lazy="dynamic")
    resources = db.relationship("LearningResource", backref="course", cascade="all, delete-orphan", lazy="dynamic")
    notes_list = db.relationship("LearningNote", backref="course", cascade="all, delete-orphan", lazy="dynamic")

    def update_progress(self):
        if self.total_modules > 0:
            val = min(100.0, (self.completed_modules / self.total_modules) * 100.0)
            self.progress_percentage = round(val, 1)
            if self.progress_percentage >= 100.0:
                self.status = "completed"
        db.session.add(self)

    def to_dict(self, exclude=None, include_relationships=True):
        data = super().to_dict(exclude=exclude)
        if include_relationships and self.subject:
            data["subject"] = self.subject.to_dict()
        return data


class StudySession(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "learning_study_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey("learning_courses.id"), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("learning_subjects.id"), nullable=True)
    
    title = db.Column(db.String(200), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    session_date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    topics_covered = db.Column(db.Text, nullable=True)
    key_takeaways = db.Column(db.Text, nullable=True)
    comprehension_rating = db.Column(db.Integer, default=4, nullable=False) # 1 to 5

    def to_dict(self, exclude=None):
        data = super().to_dict(exclude=exclude)
        if isinstance(self.session_date, (date, datetime)):
            data["session_date"] = self.session_date.strftime("%Y-%m-%d")
        return data


class LearningResource(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "learning_resources"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("learning_courses.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    resource_type = db.Column(db.String(50), default="Article", nullable=False) # Article, Book, Video, Repository, PDF
    url_or_path = db.Column(db.String(255), nullable=True)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)


class LearningNote(db.Model, TimestampMixin, SerializerMixin):
    __tablename__ = "learning_notes"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("learning_courses.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=True)
