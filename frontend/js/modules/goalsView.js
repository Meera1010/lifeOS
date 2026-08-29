/**
 * LifeOS Goal Management View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal } from '../components/ui.js';

export async function renderGoalsView(container) {
  const res = await APIClient.get('/api/goals');
  const goals = res.data || [];

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>🎯 Goal Management</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Track short-term and long-term personal, career, financial, and learning goals.</p>
      </div>
      <button class="btn btn-primary" id="btn-create-goal">+ Create Goal</button>
    </div>

    <div class="goals-grid">
      ${goals.length === 0 ? '<div class="card" style="grid-column: span 12; text-align: center; color: var(--text-muted);">No goals active. Define your vision today.</div>' : ''}
      ${goals.map(g => `
        <div class="card goal-card">
          <div>
            <div class="card-header" style="margin-bottom: 8px;">
              <span class="badge badge-medium" style="text-transform: uppercase;">${g.timeframe.replace('_', ' ')}</span>
              <span style="font-size: 0.8rem; color: var(--text-muted);">Target: ${g.target_date ? g.target_date.split('T')[0] : 'Open'}</span>
            </div>
            <h3 style="font-size: 1.1rem; margin-bottom: 6px;">${g.title}</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 14px;">${g.description || 'Target goal milestones.'}</p>
            
            <div style="margin-bottom: 14px;">
              <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
                <span>Progress</span>
                <span style="font-weight: 700;">${g.progress_percentage}%</span>
              </div>
              <div class="progress-container">
                <div class="progress-bar" style="width: ${g.progress_percentage}%;"></div>
              </div>
            </div>

            <div style="margin-top: 10px;">
              <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); margin-bottom: 4px;">Milestones</div>
              ${(g.milestones || []).map(m => `
                <div class="milestone-item">
                  <input type="checkbox" ${m.is_completed ? 'checked' : ''} onchange="toggleMilestone(${m.id})">
                  <span style="${m.is_completed ? 'text-decoration: line-through; color: var(--text-muted);' : ''}">${m.title}</span>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      `).join('')}
    </div>
  `;

  document.getElementById('btn-create-goal').onclick = () => {
    openModal(
      'Create New Goal',
      `
        <form id="modal-goal-form">
          <div class="form-group">
            <label class="form-label">Goal Title</label>
            <input type="text" id="m-goal-title" class="form-control" placeholder="e.g. Save $10,000 for Investment" required>
          </div>
          <div class="form-group">
            <label class="form-label">Category</label>
            <select id="m-goal-category" class="form-control">
              <option value="personal">Personal</option>
              <option value="career">Career</option>
              <option value="financial">Financial</option>
              <option value="learning">Learning</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Timeframe</label>
            <select id="m-goal-timeframe" class="form-control">
              <option value="short_term">Short-Term (&lt; 6 months)</option>
              <option value="long_term">Long-Term (1+ year)</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Target Date</label>
            <input type="date" id="m-goal-target" class="form-control">
          </div>
        </form>
      `,
      async () => {
        const title = document.getElementById('m-goal-title').value;
        const category = document.getElementById('m-goal-category').value;
        const timeframe = document.getElementById('m-goal-timeframe').value;
        const target_date = document.getElementById('m-goal-target').value;

        try {
          await APIClient.post('/api/goals', { title, category, timeframe, target_date });
          showToast('Goal created!', 'success');
          renderGoalsView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };

  window.toggleMilestone = async (milestoneId) => {
    try {
      await APIClient.post(`/api/goals/milestones/${milestoneId}/toggle`);
      renderGoalsView(container);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };
}
