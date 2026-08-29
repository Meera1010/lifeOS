/**
 * LifeOS SPA Hash Router System
 */

import { state } from './state.js';

class Router {
  constructor() {
    this.routes = {};
    window.addEventListener('hashchange', () => this.handleRoute());
  }

  register(path, viewHandler) {
    this.routes[path] = viewHandler;
  }

  async handleRoute() {
    let hash = window.location.hash.replace('#', '') || 'dashboard';

    // Route guards
    if (!state.isAuthenticated() && hash !== 'login' && hash !== 'register') {
      window.location.hash = '#login';
      return;
    }

    if (state.isAuthenticated() && (hash === 'login' || hash === 'register')) {
      window.location.hash = '#dashboard';
      return;
    }

    if (hash === 'admin' && !state.isAdmin()) {
      window.location.hash = '#dashboard';
      return;
    }

    state.currentView = hash;

    // Highlight sidebar active item
    document.querySelectorAll('.nav-item').forEach(item => {
      const view = item.getAttribute('data-view');
      if (view === hash) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    const handler = this.routes[hash] || this.routes['dashboard'];
    const container = document.getElementById('main-content');
    if (container && handler) {
      container.innerHTML = '<div style="display:flex;justify-content:center;padding:50px;"><div style="color:var(--text-muted);">Loading view...</div></div>';
      try {
        await handler(container);
      } catch (err) {
        console.error(`[Router Error] Failed to render view ${hash}:`, err);
        container.innerHTML = `<div class="card"><h3 style="color:var(--accent-danger)">Error Loading View</h3><p>${err.message}</p></div>`;
      }
    }
  }

  navigate(path) {
    window.location.hash = `#${path}`;
  }
}

export const router = new Router();
