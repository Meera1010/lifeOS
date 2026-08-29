/**
 * LifeOS Personal Analytics View Controller
 */

import { APIClient } from '../api.js';

export async function renderAnalyticsView(container) {
  const res = await APIClient.get('/api/analytics/reports?period=monthly');
  const report = res.data || {};
  const lifeScore = report.life_score || {};
  const breakdown = lifeScore.breakdown || {};

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>📈 Personal Analytics Engine</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Comprehensive data analytics across all life pillars.</p>
      </div>
    </div>

    <div class="analytics-grid">
      <!-- Life Score Pillars Breakdown -->
      <div class="card" style="grid-column: span 6;">
        <div class="card-header">
          <div class="card-title">📊 Life Score Pillars</div>
          <span style="font-size: 1.25rem; font-weight: 800; color: var(--accent-primary);">${lifeScore.overall_score || 0}%</span>
        </div>
        
        <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 16px;">
          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
              <span>Productivity (20%)</span>
              <span style="font-weight: 700;">${breakdown.productivity || 0}%</span>
            </div>
            <div class="progress-container"><div class="progress-bar" style="width: ${breakdown.productivity || 0}%;"></div></div>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
              <span>Habits Consistency (20%)</span>
              <span style="font-weight: 700;">${breakdown.habits || 0}%</span>
            </div>
            <div class="progress-container"><div class="progress-bar" style="width: ${breakdown.habits || 0}%; background: var(--accent-success);"></div></div>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
              <span>Goal Completion (20%)</span>
              <span style="font-weight: 700;">${breakdown.goals || 0}%</span>
            </div>
            <div class="progress-container"><div class="progress-bar" style="width: ${breakdown.goals || 0}%; background: var(--accent-warning);"></div></div>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
              <span>Learning Progress (15%)</span>
              <span style="font-weight: 700;">${breakdown.learning || 0}%</span>
            </div>
            <div class="progress-container"><div class="progress-bar" style="width: ${breakdown.learning || 0}%; background: var(--accent-purple);"></div></div>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
              <span>Financial Discipline (15%)</span>
              <span style="font-weight: 700;">${breakdown.finance || 0}%</span>
            </div>
            <div class="progress-container"><div class="progress-bar" style="width: ${breakdown.finance || 0}%; background: var(--accent-info);"></div></div>
          </div>
        </div>
      </div>

      <!-- Improvement Suggestions Card -->
      <div class="card" style="grid-column: span 6;">
        <div class="card-header">
          <div class="card-title">💡 Personalized Recommendations</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 12px;">
          ${(lifeScore.suggestions || []).map(s => `
            <div class="insight-item info">
              <div class="insight-msg" style="font-size: 0.9rem;">${s}</div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}
