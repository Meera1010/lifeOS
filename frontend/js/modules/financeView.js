/**
 * LifeOS Finance Manager View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal, ChartEngine } from '../components/ui.js';

export async function renderFinanceView(container) {
  const summaryRes = await APIClient.get('/api/finance/summary');
  const summary = summaryRes.data || {};

  const txRes = await APIClient.get('/api/finance/transactions');
  const transactions = txRes.data || [];

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>💰 Personal Finance Manager</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Track income, expenses, category budgets, and net savings rate.</p>
      </div>
      <button class="btn btn-primary" id="btn-log-tx">+ Log Transaction</button>
    </div>

    <!-- Monthly Summary Metric Cards -->
    <div class="finance-stats-grid">
      <div class="finance-card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">Total Income</div>
        <div class="amount-income" style="font-size: 1.5rem;">+$${summary.total_income || 0}</div>
      </div>
      <div class="finance-card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">Total Expenses</div>
        <div class="amount-expense" style="font-size: 1.5rem;">-$${summary.total_expenses || 0}</div>
      </div>
      <div class="finance-card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">Net Savings</div>
        <div style="font-size: 1.5rem; font-weight: 800;">$${summary.net_savings || 0}</div>
      </div>
      <div class="finance-card">
        <div style="font-size: 0.8rem; color: var(--text-muted);">Savings Rate</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: var(--accent-info);">${summary.savings_rate || 0}%</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 340px; gap: 20px; margin-bottom: 24px;">
      <!-- Transactions Table -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">💳 Recent Transactions</div>
        </div>
        <div class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th>Type</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              ${transactions.length === 0 ? '<tr><td colspan="5" style="text-align:center;">No transactions logged.</td></tr>' : ''}
              ${transactions.map(t => `
                <tr>
                  <td>${t.transaction_date}</td>
                  <td style="font-weight: 600;">${t.description}</td>
                  <td>${t.category ? t.category.name : 'General'}</td>
                  <td><span class="badge ${t.type === 'income' ? 'badge-completed' : 'badge-urgent'}">${t.type}</span></td>
                  <td style="font-weight: 700; color: ${t.type === 'income' ? 'var(--accent-success)' : 'var(--text-primary)'};">
                    ${t.type === 'income' ? '+' : '-'}$${t.amount}
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>

      <!-- Spending Breakdown Chart -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">🍰 Spending Breakdown</div>
        </div>
        <canvas id="spending-pie-canvas" width="280" height="260" style="margin: 0 auto; display: block;"></canvas>
      </div>
    </div>
  `;

  setTimeout(() => {
    const cats = summary.category_breakdown || [];
    const labels = cats.map(c => c.category_name);
    const values = cats.map(c => c.total_amount);
    const colors = cats.map(c => c.color);
    ChartEngine.renderPieChart('spending-pie-canvas', labels.length ? labels : ['Expenses'], values.length ? values : [100], colors.length ? colors : ['#ef4444']);
  }, 50);

  document.getElementById('btn-log-tx').onclick = () => {
    openModal(
      'Log Financial Transaction',
      `
        <form id="modal-tx-form">
          <div class="form-group">
            <label class="form-label">Transaction Description</label>
            <input type="text" id="m-tx-desc" class="form-control" placeholder="e.g. Monthly Grocery Shopping" required>
          </div>
          <div class="form-group">
            <label class="form-label">Type</label>
            <select id="m-tx-type" class="form-control">
              <option value="expense" selected>Expense</option>
              <option value="income">Income</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Amount ($)</label>
            <input type="number" step="0.01" id="m-tx-amount" class="form-control" placeholder="0.00" required>
          </div>
          <div class="form-group">
            <label class="form-label">Date</label>
            <input type="date" id="m-tx-date" class="form-control">
          </div>
        </form>
      `,
      async () => {
        const description = document.getElementById('m-tx-desc').value;
        const type = document.getElementById('m-tx-type').value;
        const amount = document.getElementById('m-tx-amount').value;
        const transaction_date = document.getElementById('m-tx-date').value;

        try {
          const res = await APIClient.post('/api/finance/transactions', { description, type, amount, transaction_date });
          showToast('Transaction logged!', 'success');
          if (res.data && res.data.budget_alert && res.data.budget_alert.triggered) {
            showToast(`⚠️ Budget Alert: Exceeded threshold for ${res.data.budget_alert.category_name}!`, 'error', 6000);
          }
          renderFinanceView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };
}
