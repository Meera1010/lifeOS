/**
 * LifeOS Authentication View Controller (Login & Registration)
 */

import { APIClient } from '../api.js';
import { state } from '../state.js';
import { showToast } from '../components/ui.js';

export async function renderAuthView(container, isRegister = false) {
  if (isRegister) {
    container.innerHTML = `
      <div style="max-width: 420px; margin: 40px auto;" class="card">
        <h2 style="margin-bottom: 8px; text-align: center;">Create LifeOS Account</h2>
        <p style="color: var(--text-muted); text-align: center; margin-bottom: 24px;">Join the Personal Life Management & Analytics Platform</p>
        
        <form id="register-form">
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input type="text" id="reg-name" class="form-control" placeholder="Alex Morgan" required>
          </div>
          <div class="form-group">
            <label class="form-label">Username</label>
            <input type="text" id="reg-username" class="form-control" placeholder="alex_dev" required>
          </div>
          <div class="form-group">
            <label class="form-label">Email Address</label>
            <input type="email" id="reg-email" class="form-control" placeholder="alex@example.com" required>
          </div>
          <div class="form-group">
            <label class="form-label">Password</label>
            <input type="password" id="reg-password" class="form-control" placeholder="••••••••" required>
          </div>
          <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 12px;">Create Account</button>
        </form>
        <p style="text-align: center; margin-top: 16px; font-size: 0.85rem; color: var(--text-muted);">
          Already have an account? <a href="#login" style="color: var(--accent-primary);">Sign In</a>
        </p>
      </div>
    `;

    document.getElementById('register-form').onsubmit = async (e) => {
      e.preventDefault();
      try {
        const payload = {
          full_name: document.getElementById('reg-name').value,
          username: document.getElementById('reg-username').value,
          email: document.getElementById('reg-email').value,
          password: document.getElementById('reg-password').value
        };
        const res = await APIClient.post('/api/auth/register', payload);
        state.setToken(res.data.token);
        state.setUser(res.data.user);
        showToast('Registration successful! Welcome to LifeOS.', 'success');
        window.location.hash = '#dashboard';
      } catch (err) {
        showToast(err.message, 'error');
      }
    };

  } else {

    container.innerHTML = `
      <div style="max-width: 420px; margin: 60px auto;" class="card">
        <h2 style="margin-bottom: 8px; text-align: center;">Sign In to LifeOS</h2>
        <p style="color: var(--text-muted); text-align: center; margin-bottom: 24px;">Enter your credentials to access your dashboard</p>
        
        <form id="login-form">
          <div class="form-group">
            <label class="form-label">Username or Email</label>
            <input type="text" id="login-user" class="form-control" placeholder="username or email" required>
          </div>
          <div class="form-group">
            <label class="form-label">Password</label>
            <input type="password" id="login-password" class="form-control" placeholder="••••••••" required>
          </div>
          <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 12px;">Sign In</button>
        </form>
        <p style="text-align: center; margin-top: 16px; font-size: 0.85rem; color: var(--text-muted);">
          Don't have an account? <a href="#register" style="color: var(--accent-primary);">Register Now</a>
        </p>
      </div>
    `;

    document.getElementById('login-form').onsubmit = async (e) => {
      e.preventDefault();
      try {
        const payload = {
          username: document.getElementById('login-user').value,
          password: document.getElementById('login-password').value
        };
        const res = await APIClient.post('/api/auth/login', payload);
        state.setToken(res.data.token);
        state.setUser(res.data.user);
        showToast('Login successful! Welcome back.', 'success');
        window.location.hash = '#dashboard';
      } catch (err) {
        showToast(err.message, 'error');
      }
    };
  }
}
