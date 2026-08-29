"""
LifeOS SQLAlchemy Base Model & Reusable Mixins
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TimestampMixin:
    """Provides created_at and updated_at timestamps for all models."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    """Provides soft-delete functionality without removing rows from DB."""
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.session.add(self)

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        db.session.add(self)

class SerializerMixin:
    """Generic serialization helper for SQLAlchemy models to Python dict / JSON."""
    
    def to_dict(self, exclude=None, include_relationships=False):
        exclude = set(exclude or [])
        result = {}
        for column in self.__table__.columns:
            if column.name in exclude:
                continue
            val = getattr(self, column.name)
            if isinstance(val, datetime):
                result[column.name] = val.isoformat()
            else:
                result[column.name] = val
        return result

    @classmethod
    def find_by_id(cls, model_id):
        return cls.query.get(model_id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, soft=True):
        if soft and hasattr(self, "soft_delete"):
            self.soft_delete()
        else:
            db.session.delete(self)
        db.session.commit()
