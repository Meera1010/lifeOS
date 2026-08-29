/**
 * LifeOS User Profile View Controller
 */

import { APIClient } from '../api.js';
import { state } from '../state.js';
import { showToast } from '../components/ui.js';

export async function renderProfileView(container) {
  const res = await APIClient.get('/api/users/profile');
  const profileData = res.data || {};
  const prof = profileData.profile || {};

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>👤 User Profile</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Manage personal bio, occupation, location, and account identity.</p>
      </div>
    </div>

    <div style="max-width: 600px;" class="card">
      <form id="profile-form">
        <div class="form-group">
          <label class="form-label">Full Name</label>
          <input type="text" id="p-fullname" class="form-control" value="${prof.full_name || ''}">
        </div>
        <div class="form-group">
          <label class="form-label">Email Address</label>
          <input type="email" id="p-email" class="form-control" value="${profileData.email || ''}" required>
        </div>
        <div class="form-group">
          <label class="form-label">Bio / Tagline</label>
          <textarea id="p-bio" class="form-control" rows="3">${prof.bio || ''}</textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Occupation</label>
          <input type="text" id="p-occupation" class="form-control" value="${prof.occupation || ''}">
        </div>
        <div class="form-group">
          <label class="form-label">Location</label>
          <input type="text" id="p-location" class="form-control" value="${prof.location || ''}">
        </div>
        <div class="form-group">
          <label class="form-label">Life Motto</label>
          <input type="text" id="p-motto" class="form-control" value="${prof.life_motto || ''}">
        </div>
        <button type="submit" class="btn btn-primary" style="margin-top: 12px;">Save Profile Changes</button>
      </form>
    </div>
  `;

  document.getElementById('profile-form').onsubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        full_name: document.getElementById('p-fullname').value,
        email: document.getElementById('p-email').value,
        bio: document.getElementById('p-bio').value,
        occupation: document.getElementById('p-occupation').value,
        location: document.getElementById('p-location').value,
        life_motto: document.getElementById('p-motto').value
      };
      const res = await APIClient.put('/api/users/profile', payload);
      state.setUser(res.data);
      showToast('Profile updated successfully!', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    }
  };
}
