/**
 * LifeOS Achievements View Controller — 50+ System Achievements Grid
 */

import { APIClient } from '../api.js';

export async function renderAchievementsView(container) {
  const res = await APIClient.get('/api/achievements');
  const achievements = res.data || [];
  const totalUnlocked = achievements.filter(a => a.unlocked).length;
  const totalPoints = achievements.filter(a => a.unlocked).reduce((sum, a) => sum + a.points, 0);

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>🏆 Achievement System</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Unlock badges and earn points by maintaining habits, crushing goals, and staying productive.</p>
      </div>
      <div style="display: flex; gap: 16px;">
        <div class="card" style="padding: 10px 16px;">
          <span style="font-size: 0.8rem; color: var(--text-muted);">Unlocked</span>
          <div style="font-weight: 800; font-size: 1.2rem; color: var(--accent-success);">${totalUnlocked}/${achievements.length}</div>
        </div>
        <div class="card" style="padding: 10px 16px;">
          <span style="font-size: 0.8rem; color: var(--text-muted);">Total Points</span>
          <div style="font-weight: 800; font-size: 1.2rem; color: var(--accent-warning);">${totalPoints} pts</div>
        </div>
      </div>
    </div>

    <div class="achievements-grid">
      ${achievements.map(a => `
        <div class="achievement-card tier-${a.badge_tier} ${a.unlocked ? 'unlocked' : ''}">
          <div style="font-size: 1.8rem; width: 44px; text-align: center;">${a.unlocked ? '🏆' : '🔒'}</div>
          <div>
            <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 2px;">${a.title}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 6px;">${a.description}</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-secondary);">
              <span style="text-transform: uppercase; font-weight: 600;">${a.badge_tier}</span>
              <span style="font-weight: 700; color: var(--accent-warning);">+${a.points} pts</span>
            </div>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}
