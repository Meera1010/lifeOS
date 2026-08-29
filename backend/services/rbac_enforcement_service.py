"""
LifeOS RBAC Capability & Security Enforcement Service
"""

from typing import Dict, List, Any
from backend.security.rbac import ROLE_PERMISSIONS


class RBACEnforcementService:
    """
    Evaluates role permissions and capability rules for API endpoints.
    """

    @staticmethod
    def user_has_permission(role: str, permission: str) -> bool:
        """Checks if a user role has a specific capability permission."""
        perms = ROLE_PERMISSIONS.get(role, [])
        return "*" in perms or permission in perms

    @staticmethod
    def get_role_capabilities(role: str) -> Dict[str, Any]:
        """Returns list of capabilities granted to role."""
        return {
            "role": role,
            "permissions": ROLE_PERMISSIONS.get(role, [])
        }
