/**
 * LifeOS UI Component — Reusable Data Table Component
 */

export class TableComponent {
  static render({ columns, rows, actions }) {
    if (!rows || rows.length === 0) {
      return `<div class="empty-state">No records found.</div>`;
    }

    return `
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              ${columns.map(c => `<th>${c.label}</th>`).join('')}
              ${actions ? `<th>Actions</th>` : ''}
            </tr>
          </thead>
          <tbody>
            ${rows.map(r => `
              <tr>
                ${columns.map(c => `<td>${c.formatter ? c.formatter(r[c.key], r) : (r[c.key] || '')}</td>`).join('')}
                ${actions ? `<td>${actions(r)}</td>` : ''}
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  }
}
