/**
 * LifeOS UI Component — Reusable Metric & Dashboard Card
 */

export class CardComponent {
  static renderMetricCard({ title, value, subtitle, color = 'primary', icon = 'activity' }) {
    return `
      <div class="card metric-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">${title}</div>
            <div style="font-size: 1.8rem; font-weight: 800; margin: 4px 0;">${value}</div>
            ${subtitle ? `<div style="font-size: 0.75rem; color: var(--text-secondary);">${subtitle}</div>` : ''}
          </div>
          <div class="metric-icon" style="color: var(--accent-${color}); background: rgba(255,255,255,0.05); padding: 8px; border-radius: 8px;">
            ${icon}
          </div>
        </div>
      </div>
    `;
  }
}
