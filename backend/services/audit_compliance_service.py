"""
LifeOS System Audit & Regulatory Compliance Reporting Service
"""

from datetime import datetime
from typing import Dict, Any, List
from backend.models.base import db
from backend.models.audit import AuditLog


class AuditComplianceService:
    """
    Generates audit compliance reports for security events.
    """

    @staticmethod
    def get_compliance_audit_trail(user_id: int = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves recent audit log events."""
        query = AuditLog.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
        return [l.to_dict() for l in logs]
