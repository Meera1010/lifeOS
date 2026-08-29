/**
 * LifeOS Settings View Controller
 */

import { APIClient } from '../api.js';
import { state } from '../state.js';
import { showToast } from '../components/ui.js';

export async function renderSettingsView(container) {
  const res = await APIClient.get('/api/users/settings');
  const settings = res.data || {};

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>⚙️ Platform Settings</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Preferences, dark/light theme, time format, and security.</p>
      </div>
    </div>

    <div style="max-width: 600px; display: flex; flex-direction: column; gap: 20px;">
      <!-- Theme & Appearance -->
      <div class="card">
        <h3 style="margin-bottom: 14px;">Appearance & Theme</h3>
        <div class="form-group">
          <label class="form-label">Color Theme</label>
          <select id="setting-theme" class="form-control">
            <option value="dark" ${settings.theme === 'dark' ? 'selected' : ''}>Dark Cyber Theme</option>
            <option value="light" ${settings.theme === 'light' ? 'selected' : ''}>Light Theme</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Time Format</label>
          <select id="setting-time-format" class="form-control">
            <option value="12h" ${settings.time_format === '12h' ? 'selected' : ''}>12-Hour (AM/PM)</option>
            <option value="24h" ${settings.time_format === '24h' ? 'selected' : ''}>24-Hour Military</option>
          </select>
        </div>
        <button class="btn btn-primary" id="btn-save-settings">Save Preferences</button>
      </div>

      <!-- Password Change -->
      <div class="card">
        <h3 style="margin-bottom: 14px;">Security & Password</h3>
        <form id="password-change-form">
          <div class="form-group">
            <label class="form-label">Current Password</label>
            <input type="password" id="pwd-old" class="form-control" required>
          </div>
          <div class="form-group">
            <label class="form-label">New Password</label>
            <input type="password" id="pwd-new" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-secondary">Update Password</button>
        </form>
      </div>
    </div>
  `;

  document.getElementById('btn-save-settings').onclick = async () => {
    const theme = document.getElementById('setting-theme').value;
    const time_format = document.getElementById('setting-time-format').value;

    try {
      await APIClient.put('/api/users/settings', { theme, time_format });
      state.setTheme(theme);
      showToast('Settings saved successfully!', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  document.getElementById('password-change-form').onsubmit = async (e) => {
    e.preventDefault();
    const old_password = document.getElementById('pwd-old').value;
    const new_password = document.getElementById('pwd-new').value;

    try {
      await APIClient.post('/api/auth/change-password', { old_password, new_password });
      showToast('Password successfully changed!', 'success');
      document.getElementById('password-change-form').reset();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };
}
