"""
LifeOS Production Architectural Scaler — Builds rich, non-duplicate, functional source code
across all modules, services, tests, views, components, and documentation.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def write_file(rel_path, content):
    abs_path = os.path.join(PROJECT_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_frontend_widgets():
    # 1. modalManager.js
    write_file("frontend/js/components/modalManager.js", '''/**
 * LifeOS UI Component — Modal Dialog Stack Manager
 */

export class ModalManager {
  static openModal(title, bodyHtml, onConfirm = null) {
    const overlay = document.getElementById('modal-overlay');
    const container = document.getElementById('modal-container');

    if (!overlay || !container) return;

    container.innerHTML = `
      <div class="card" style="width: 100%; max-width: 500px; padding: 24px;">
        <div class="card-header" style="margin-bottom: 16px;">
          <div class="card-title">${title}</div>
          <button class="btn btn-secondary btn-sm" id="modal-close-btn">&times;</button>
        </div>
        <div class="modal-body" style="margin-bottom: 20px;">
          ${bodyHtml}
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 12px;">
          <button class="btn btn-secondary" id="modal-cancel-btn">Cancel</button>
          ${onConfirm ? `<button class="btn btn-primary" id="modal-confirm-btn">Confirm</button>` : ''}
        </div>
      </div>
    `;

    overlay.style.display = 'flex';

    document.getElementById('modal-close-btn').onclick = () => ModalManager.closeModal();
    document.getElementById('modal-cancel-btn').onclick = () => ModalManager.closeModal();

    if (onConfirm) {
      document.getElementById('modal-confirm-btn').onclick = async () => {
        const success = await onConfirm();
        if (success !== false) {
          ModalManager.closeModal();
        }
      };
    }
  }

  static closeModal() {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) overlay.style.display = 'none';
  }
}
''')

    # 2. toastManager.js
    write_file("frontend/js/components/toastManager.js", '''/**
 * LifeOS UI Component — Animated Toast Notification Manager
 */

export class ToastManager {
  static showToast(message, type = 'info', durationMs = 3500) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span style="font-weight: 600;">${type.toUpperCase()}:</span>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, durationMs);
  }
}
''')

def generate_services_and_models():
    # rbac_enforcement_service.py
    write_file("backend/services/rbac_enforcement_service.py", '''"""
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
''')

def main():
    print("Building frontend components and security services...")
    generate_frontend_widgets()
    generate_services_and_models()
    print("Build complete.")

if __name__ == "__main__":
    main()
