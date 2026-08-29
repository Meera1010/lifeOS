/**
 * LifeOS Main Application Bootstrapper
 */

import { state } from './state.js';
import { router } from './router.js';
import { APIClient } from './api.js';

import { renderAuthView } from './modules/authView.js';
import { renderDashboardView } from './modules/dashboardView.js';
import { renderTasksView } from './modules/tasksView.js';
import { renderHabitsView } from './modules/habitsView.js';
import { renderGoalsView } from './modules/goalsView.js';
import { renderCalendarView } from './modules/calendarView.js';
import { renderFinanceView } from './modules/financeView.js';
import { renderLearningView } from './modules/learningView.js';
import { renderFocusView } from './modules/focusView.js';
import { renderJournalView } from './modules/journalView.js';
import { renderAnalyticsView } from './modules/analyticsView.js';
import { renderAchievementsView } from './modules/achievementsView.js';
import { renderProfileView } from './modules/profileView.js';
import { renderSettingsView } from './modules/settingsView.js';
import { renderAdminView } from './modules/adminView.js';

class App {
  async init() {
    // 1. Initialize Theme
    state.setTheme(state.theme);

    // 2. Register Client Routes
    router.register('login', container => renderAuthView(container, false));
    router.register('register', container => renderAuthView(container, true));
    router.register('dashboard', renderDashboardView);
    router.register('tasks', renderTasksView);
    router.register('habits', renderHabitsView);
    router.register('goals', renderGoalsView);
    router.register('calendar', renderCalendarView);
    router.register('finance', renderFinanceView);
    router.register('learning', renderLearningView);
    router.register('focus', renderFocusView);
    router.register('journal', renderJournalView);
    router.register('analytics', renderAnalyticsView);
    router.register('achievements', renderAchievementsView);
    router.register('profile', renderProfileView);
    router.register('settings', renderSettingsView);
    router.register('admin', renderAdminView);

    // 3. Authenticate Current Token
    if (state.token) {
      try {
        const res = await APIClient.get('/api/auth/me');
        state.setUser(res.data);
      } catch (err) {
        state.setToken(null);
        state.setUser(null);
      }
    }

    // 4. Update UI Header with User Profile
    this.updateUserNavbarUI();
    state.subscribe(() => this.updateUserNavbarUI());

    // 5. Global Search Listener
    const searchInput = document.getElementById('global-search-input');
    if (searchInput) {
      searchInput.onkeypress = async (e) => {
        if (e.key === 'Enter' && searchInput.value.trim()) {
          const q = searchInput.value.trim();
          window.location.hash = `#search?q=${encodeURIComponent(q)}`;
        }
      };
    }

    // 6. Handle Initial Hash
    await router.handleRoute();
  }

  updateUserNavbarUI() {
    const avatarEl = document.getElementById('nav-user-avatar');
    const nameEl = document.getElementById('nav-user-name');
    const roleEl = document.getElementById('nav-user-role');
    const adminNav = document.getElementById('admin-nav-item');

    if (state.user) {
      if (avatarEl) avatarEl.textContent = state.user.username.charAt(0).toUpperCase();
      if (nameEl) nameEl.textContent = state.user.username;
      if (roleEl) roleEl.textContent = state.user.role;

      if (adminNav) {
        adminNav.style.display = state.isAdmin() ? 'flex' : 'none';
      }
    } else {
      if (avatarEl) avatarEl.textContent = '?';
      if (nameEl) nameEl.textContent = 'Guest';
      if (roleEl) roleEl.textContent = 'Not Logged In';
      if (adminNav) adminNav.style.display = 'none';
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new App();
  app.init();
});
