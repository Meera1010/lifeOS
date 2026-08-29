"""
LifeOS Role-Based Access Control (RBAC) System
"""

from backend.app.constants import UserRole

# Capability Matrix
ROLE_PERMISSIONS = {
    UserRole.USER.value: {
        "tasks": ["create", "read", "update", "delete"],
        "habits": ["create", "read", "update", "delete"],
        "goals": ["create", "read", "update", "delete"],
        "calendar": ["create", "read", "update", "delete"],
        "finance": ["create", "read", "update", "delete"],
        "learning": ["create", "read", "update", "delete"],
        "focus": ["create", "read", "update", "delete"],
        "journal": ["create", "read", "update", "delete"],
        "analytics": ["read"],
        "achievements": ["read"],
        "profile": ["read", "update"],
        "settings": ["read", "update"],
        "admin": []
    },
    UserRole.ADMIN.value: {
        "tasks": ["create", "read", "update", "delete", "manage_all"],
        "habits": ["create", "read", "update", "delete", "manage_all"],
        "goals": ["create", "read", "update", "delete", "manage_all"],
        "calendar": ["create", "read", "update", "delete", "manage_all"],
        "finance": ["create", "read", "update", "delete", "manage_all"],
        "learning": ["create", "read", "update", "delete", "manage_all"],
        "focus": ["create", "read", "update", "delete", "manage_all"],
        "journal": ["create", "read", "update", "delete", "manage_all"],
        "analytics": ["read", "view_global"],
        "achievements": ["read", "manage_all"],
        "profile": ["read", "update"],
        "settings": ["read", "update"],
        "admin": ["view_users", "create_user", "edit_user", "disable_user", "delete_user", "view_audit_logs", "view_system_stats"]
    }
}

def has_permission(role: str, domain: str, action: str) -> bool:
    """Checks if a given role has permission for a domain action."""
    domain_perms = ROLE_PERMISSIONS.get(role, {}).get(domain, [])
    return action in domain_perms or "manage_all" in domain_perms
