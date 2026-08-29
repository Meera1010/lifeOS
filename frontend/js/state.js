/**
 * LifeOS Global Client State Management
 */

class AppState {
  constructor() {
    this.user = null;
    this.token = localStorage.getItem('lifeos_token') || null;
    this.currentView = 'dashboard';
    this.notifications = [];
    this.unreadNotificationCount = 0;
    this.theme = localStorage.getItem('lifeos_theme') || 'dark';
    this.listeners = [];
  }

  setUser(user) {
    this.user = user;
    this.notify();
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('lifeos_token', token);
    } else {
      localStorage.removeItem('lifeos_token');
    }
  }

  setTheme(theme) {
    this.theme = theme;
    localStorage.setItem('lifeos_theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    this.notify();
  }

  isAuthenticated() {
    return !!this.token && !!this.user;
  }

  isAdmin() {
    return this.user && (this.user.role === 'admin' || this.user.role === 'Admin');
  }

  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  notify() {
    this.listeners.forEach(listener => listener(this));
  }
}

export const state = new AppState();
