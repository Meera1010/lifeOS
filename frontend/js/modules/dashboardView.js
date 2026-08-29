/**
 * LifeOS Dashboard View Controller
 */

import { APIClient } from '../api.js';
import { state } from '../state.js';
import { ChartEngine } from '../components/ui.js';

export async function renderDashboardView(container) {
  const res = await APIClient.get('/api/dashboard/overview');
  const data = res.data;
  const lifeScore = data.life_score || {};
  const tasks = data.tasks_summary || {};
  const habits = data.habits_summary || {};
  const goals = data.goals_summary || {};
  const insights = data.smart_insights || [];

  container.innerHTML = `
    <div class="dashboard-header">
      <h1 class="greeting-text">Good Morning, ${state.user ? state.user.username : 'User'}! 👋</h1>
      <p class="subtitle-text">Here is your personal life management & analytics summary for today.</p>
    </div>

    <div class="dashboard-grid">
      <!-- Life Score Radial Gauge Card -->
      <div class="card life-score-card">
        <div class="card-title">Life Score</div>
        <div class="gauge-container">
          <canvas id="life-score-gauge-canvas" width="160" height="160"></canvas>
          <div class="gauge-center-text">
            <span class="gauge-score-value">${lifeScore.overall_score || 82}%</span>
            <span class="gauge-score-label">Composite</span>
          </div>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted);">
          Change: <span style="color: ${lifeScore.score_change >= 0 ? 'var(--accent-success)' : 'var(--accent-danger)'}; font-weight: 700;">
            ${lifeScore.score_change >= 0 ? '+' : ''}${lifeScore.score_change || 0}%
          </span> vs previous period
        </p>
      </div>

      <!-- Quick Metrics Row -->
      <div class="metrics-row">
        <div class="metric-stat-card">
          <div class="stat-icon-wrapper" style="background: rgba(79, 70, 229, 0.15); color: var(--accent-primary);">📋</div>
          <div>
            <div class="stat-val">${tasks.completed_tasks || 0}/${tasks.total_tasks || 0}</div>
            <div class="stat-lbl">Tasks Done</div>
          </div>
        </div>

        <div class="metric-stat-card">
          <div class="stat-icon-wrapper" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-success);">⚡</div>
          <div>
            <div class="stat-val">${habits.active_streaks || 0}</div>
            <div class="stat-lbl">Active Streaks</div>
          </div>
        </div>

        <div class="metric-stat-card">
          <div class="stat-icon-wrapper" style="background: rgba(245, 158, 11, 0.15); color: var(--accent-warning);">🎯</div>
          <div>
            <div class="stat-val">${goals.completed_goals || 0}/${goals.total_goals || 0}</div>
            <div class="stat-lbl">Goals Crushed</div>
          </div>
        </div>
      </div>

      <!-- Weekly Productivity Line Chart Card -->
      <div class="card chart-card-lg">
        <div class="card-header">
          <div class="card-title">📈 Weekly Productivity Trend</div>
          <span style="font-size: 0.8rem; color: var(--text-muted);">Last 7 Days</span>
        </div>
        <canvas id="productivity-trend-canvas" width="600" height="220" style="width: 100%; height: 220px;"></canvas>
      </div>

      <!-- Smart Insights Card -->
      <div class="card insights-card">
        <div class="card-header">
          <div class="card-title">💡 Smart Insights</div>
        </div>
        <div class="insights-list">
          ${insights.map(i => `
            <div class="insight-item ${i.type || 'info'}">
              <div class="insight-title">${i.title}</div>
              <div class="insight-msg">${i.message}</div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;

  // Render Charts using Custom Canvas Engine
  setTimeout(() => {
    ChartEngine.renderRadialGauge('life-score-gauge-canvas', lifeScore.overall_score || 82, 100);
    
    const chartData = data.productivity_chart || {};
    const labels = chartData.labels || ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    const pts = chartData.datasets ? chartData.datasets[0].data : [65, 72, 80, 78, 85, 90, 82];
    ChartEngine.renderLineChart('productivity-trend-canvas', labels, pts, 'Productivity');
  }, 50);
}
