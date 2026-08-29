"""
LifeOS System Health & Diagnostics Service
"""

import sys
import os
import platform
from typing import Dict, Any
from backend.models.base import db
from backend.models.user import User


class SystemHealthService:
    """
    System Health Diagnostics Domain Service providing:
    - Platform environment inspection
    - Database connection health checks
    - Runtime performance metrics
    """

    @staticmethod
    def inspect_system_health() -> Dict[str, Any]:
        """Runs full health check diagnostic suite."""
        db_healthy = False
        user_count = 0
        try:
            user_count = User.query.count()
            db_healthy = True
        except Exception:
            db_healthy = False

        return {
            "status": "healthy" if db_healthy else "degraded",
            "database_connected": db_healthy,
            "total_registered_users": user_count,
            "environment": {
                "python_version": sys.version,
                "platform": platform.platform(),
                "os": os.name
            }
        }
