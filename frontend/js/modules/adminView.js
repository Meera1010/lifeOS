/**
 * LifeOS Administrator Panel View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal } from '../components/ui.js';

export async function renderAdminView(container) {
  const usersRes = await APIClient.get('/api/admin/users');
  const usersData = usersRes.data || [];

  const statsRes = await APIClient.get('/api/admin/statistics');
  const stats = statsRes.data || {};

  const logsRes = await APIClient.get('/api/admin/audit-logs');
  const auditLogs = logsRes.data || [];

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>🛡️ Administrator Dashboard</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Role-based access control, user management, audit logging, system metrics.</p>
      </div>
      <button class="btn btn-primary" id="btn-admin-add-user">+ Create User</button>
    </div>

    <!-- Admin System Metrics -->
    <div class="admin-stats-row">
      <div class="card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">Registered Users</div>
        <div style="font-size: 1.5rem; font-weight: 800;">${stats.total_registered_users || 0}</div>
      </div>
      <div class="card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">Active Accounts</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-success);">${stats.active_users || 0}</div>
      </div>
      <div class="card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">Total Tasks Logged</div>
        <div style="font-size: 1.5rem; font-weight: 800;">${stats.total_tasks_created || 0}</div>
      </div>
      <div class="card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">System Health</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-info);">${stats.system_status || 'Healthy'}</div>
      </div>
    </div>

    <!-- User Management Table -->
    <div class="card" style="margin-bottom: 24px;">
      <div class="card-header">
        <div class="card-title">👥 User Account Management</div>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${usersData.map(u => `
              <tr>
                <td>${u.id}</td>
                <td style="font-weight: 600;">${u.username}</td>
                <td>${u.email}</td>
                <td><span class="badge ${u.role === 'admin' ? 'badge-urgent' : 'badge-medium'}">${u.role}</span></td>
                <td><span class="badge ${u.is_active ? 'badge-completed' : 'badge-pending'}">${u.is_active ? 'Active' : 'Disabled'}</span></td>
                <td>
                  <button class="btn btn-secondary btn-sm" onclick="toggleUserStatus(${u.id})">${u.is_active ? 'Disable' : 'Enable'}</button>
                  <button class="btn btn-danger btn-sm" onclick="deleteUserByAdmin(${u.id})">Delete</button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>

    <!-- System Audit Logs Table -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">📜 Audit Logs</div>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>User ID</th>
              <th>Action</th>
              <th>Resource</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            ${auditLogs.slice(0, 10).map(l => `
              <tr>
                <td style="font-size: 0.8rem;">${l.timestamp}</td>
                <td>${l.user_id || 'System'}</td>
                <td style="font-weight: 600; color: var(--accent-primary);">${l.action}</td>
                <td>${l.resource_type}</td>
                <td style="font-size: 0.85rem; color: var(--text-muted);">${l.details || ''}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;

  document.getElementById('btn-admin-add-user').onclick = () => {
    openModal(
      'Admin — Create New User',
      `
        <form id="modal-admin-user-form">
          <div class="form-group">
            <label class="form-label">Username</label>
            <input type="text" id="m-admin-username" class="form-control" placeholder="newuser" required>
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input type="email" id="m-admin-email" class="form-control" placeholder="user@example.com" required>
          </div>
          <div class="form-group">
            <label class="form-label">Password</label>
            <input type="password" id="m-admin-password" class="form-control" placeholder="DefaultPass123!" required>
          </div>
          <div class="form-group">
            <label class="form-label">Role</label>
            <select id="m-admin-role" class="form-control">
              <option value="user" selected>User</option>
              <option value="admin">Administrator</option>
            </select>
          </div>
        </form>
      `,
      async () => {
        const username = document.getElementById('m-admin-username').value;
        const email = document.getElementById('m-admin-email').value;
        const password = document.getElementById('m-admin-password').value;
        const role = document.getElementById('m-admin-role').value;

        try {
          await APIClient.post('/api/admin/users', { username, email, password, role });
          showToast('User created by admin!', 'success');
          renderAdminView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };

  window.toggleUserStatus = async (userId) => {
    try {
      await APIClient.put(`/api/admin/users/${userId}/status`);
      showToast('User status updated.', 'info');
      renderAdminView(container);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  window.deleteUserByAdmin = async (userId) => {
    try {
      await APIClient.delete(`/api/admin/users/${userId}`);
      showToast('User account deleted.', 'info');
      renderAdminView(container);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };
}
