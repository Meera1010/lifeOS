/**
 * LifeOS Interactive Data Grid Component with Sorting and Pagination
 */

export class DataGridComponent {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.columns = options.columns || [];
    this.data = options.data || [];
    this.pageSize = options.pageSize || 10;
    this.currentPage = 1;
    this.sortKey = null;
    this.sortOrder = 'asc';
  }

  setData(newData) {
    this.data = newData || [];
    this.currentPage = 1;
    this.render();
  }

  sort(key) {
    if (this.sortKey === key) {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortKey = key;
      this.sortOrder = 'asc';
    }

    this.data.sort((a, b) => {
      let valA = a[key];
      let valB = b[key];

      if (typeof valA === 'string') valA = valA.toLowerCase();
      if (typeof valB === 'string') valB = valB.toLowerCase();

      if (valA < valB) return this.sortOrder === 'asc' ? -1 : 1;
      if (valA > valB) return this.sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

    this.render();
  }

  render() {
    if (!this.container) return;

    const startIdx = (this.currentPage - 1) * this.pageSize;
    const paginatedData = this.data.slice(startIdx, startIdx + this.pageSize);
    const totalPages = Math.ceil(this.data.length / this.pageSize) || 1;

    this.container.innerHTML = `
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              ${this.columns.map(col => `
                <th style="cursor: pointer;" onclick="window.gridInstance.sort('${col.key}')">
                  ${col.label} ${this.sortKey === col.key ? (this.sortOrder === 'asc' ? '▲' : '▼') : ''}
                </th>
              `).join('')}
            </tr>
          </thead>
          <tbody>
            ${paginatedData.length === 0 ? `<tr><td colspan="${this.columns.length}" style="text-align: center; color: var(--text-muted);">No records found.</td></tr>` : ''}
            ${paginatedData.map(row => `
              <tr>
                ${this.columns.map(col => `
                  <td>${col.formatter ? col.formatter(row[col.key], row) : (row[col.key] || '')}</td>
                `).join('')}
              </tr>
            `).join('')}
          </tbody>
        </table>

        <!-- Pagination Controls -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; font-size: 0.85rem; color: var(--text-muted);">
          <div>Showing ${startIdx + 1} to ${Math.min(startIdx + this.pageSize, this.data.length)} of ${this.data.length} entries</div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary btn-sm" ${this.currentPage === 1 ? 'disabled' : ''} onclick="window.gridInstance.changePage(${this.currentPage - 1})">Prev</button>
            <span style="padding: 4px 8px; font-weight: 600; color: var(--text-main);">Page ${this.currentPage} of ${totalPages}</span>
            <button class="btn btn-secondary btn-sm" ${this.currentPage === totalPages ? 'disabled' : ''} onclick="window.gridInstance.changePage(${this.currentPage + 1})">Next</button>
          </div>
        </div>
      </div>
    `;

    window.gridInstance = this;
  }

  changePage(newPage) {
    this.currentPage = newPage;
    this.render();
  }
}
