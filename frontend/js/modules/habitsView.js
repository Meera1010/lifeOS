/**
 * LifeOS Habit Tracker View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal } from '../components/ui.js';

export async function renderHabitsView(container) {
  const habitsRes = await APIClient.get('/api/habits');
  const habits = habitsRes.data || [];

  const matrixRes = await APIClient.get('/api/habits/calendar-matrix?days=30');
  const matrixData = matrixRes.data || { dates: [], matrix: {} };

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>⚡ Habit Tracker</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Track daily streaks, completion consistency, and build long-term momentum.</p>
      </div>
      <button class="btn btn-primary" id="btn-create-habit">+ Create Habit</button>
    </div>

    <div class="habits-grid">
      ${habits.length === 0 ? '<div class="card" style="grid-column: span 12; text-align: center; color: var(--text-muted);">No active habits logged.</div>' : ''}
      ${habits.map(h => `
        <div class="card habit-card">
          <div>
            <div class="habit-header">
              <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background-color: ${h.color};"></div>
                <h3 style="font-size: 1rem;">${h.title}</h3>
              </div>
              <div class="streak-badge">
                <span>🔥 ${h.current_streak}</span>
              </div>
            </div>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 14px;">${h.description || 'Daily habit consistency tracking.'}</p>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 12px; margin-top: 12px;">
            <span style="font-size: 0.8rem; color: var(--text-muted);">Best Streak: <strong>${h.best_streak} days</strong></span>
            <button class="btn ${h.completed_today ? 'btn-success' : 'btn-secondary'} btn-sm" onclick="toggleHabitToday(${h.id}, '${h.completed_today}')">
              ${h.completed_today ? '✓ Completed Today' : 'Mark Done Today'}
            </button>
          </div>
        </div>
      `).join('')}
    </div>

    <!-- 30-Day Completion Calendar Matrix -->
    <div class="card calendar-matrix-card">
      <div class="card-header">
        <div class="card-title">📅 30-Day Completion Heatmap</div>
      </div>
      <div class="table-container">
        <table class="matrix-table">
          <thead>
            <tr>
              <th style="width: 180px;">Habit</th>
              ${matrixData.dates.map(d => `<th style="font-size: 0.65rem; padding: 2px;">${d.slice(8)}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
            ${Object.keys(matrixData.matrix).map(hid => {
              const item = matrixData.matrix[hid];
              return `
                <tr>
                  <td style="font-weight: 600; font-size: 0.85rem;">${item.habit_title}</td>
                  ${matrixData.dates.map(d => {
                    const st = item.completions[d];
                    const cls = st === 'completed' ? 'completed' : (st === 'missed' ? 'missed' : '');
                    return `<td><div class="matrix-cell ${cls}" title="${d}: ${st}"></div></td>`;
                  }).join('')}
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;

  // Create Habit Trigger
  document.getElementById('btn-create-habit').onclick = () => {
    openModal(
      'Create New Habit',
      `
        <form id="modal-habit-form">
          <div class="form-group">
            <label class="form-label">Habit Name</label>
            <input type="text" id="m-habit-title" class="form-control" placeholder="e.g. 30 Mins Daily Workout" required>
          </div>
          <div class="form-group">
            <label class="form-label">Category</label>
            <input type="text" id="m-habit-category" class="form-control" value="Health">
          </div>
          <div class="form-group">
            <label class="form-label">Frequency</label>
            <select id="m-habit-freq" class="form-control">
              <option value="daily" selected>Daily</option>
              <option value="weekly">Weekly</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Description</label>
            <input type="text" id="m-habit-desc" class="form-control" placeholder="Optional description...">
          </div>
        </form>
      `,
      async () => {
        const title = document.getElementById('m-habit-title').value;
        const category = document.getElementById('m-habit-category').value;
        const frequency = document.getElementById('m-habit-freq').value;
        const description = document.getElementById('m-habit-desc').value;

        try {
          await APIClient.post('/api/habits', { title, category, frequency, description });
          showToast('Habit created!', 'success');
          renderHabitsView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };

  window.toggleHabitToday = async (habitId, isCompleted) => {
    try {
      await APIClient.post(`/api/habits/${habitId}/toggle`, { status: isCompleted === 'true' ? 'none' : 'completed' });
      renderHabitsView(container);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };
}
