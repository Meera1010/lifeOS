/**
 * LifeOS Learning Hub View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal } from '../components/ui.js';

export async function renderLearningView(container) {
  const coursesRes = await APIClient.get('/api/learning/courses');
  const courses = coursesRes.data || [];

  const analyticsRes = await APIClient.get('/api/learning/analytics');
  const analytics = analyticsRes.data || {};

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>📚 Learning Hub</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Manage learning courses, subjects, study sessions, and study hours.</p>
      </div>
      <div style="display: flex; gap: 10px;">
        <button class="btn btn-secondary" id="btn-log-study">+ Log Study Session</button>
        <button class="btn btn-primary" id="btn-create-course">+ Add Course</button>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="metrics-row" style="margin-bottom: 24px;">
      <div class="metric-stat-card">
        <div>
          <div class="stat-val">${analytics.total_courses || 0}</div>
          <div class="stat-lbl">Active Courses</div>
        </div>
      </div>
      <div class="metric-stat-card">
        <div>
          <div class="stat-val">${analytics.weekly_study_hours || 0} hrs</div>
          <div class="stat-lbl">Weekly Study Time</div>
        </div>
      </div>
      <div class="metric-stat-card">
        <div>
          <div class="stat-val">${analytics.completion_rate || 0}%</div>
          <div class="stat-lbl">Course Completion Rate</div>
        </div>
      </div>
    </div>

    <div class="courses-grid">
      ${courses.length === 0 ? '<div class="card" style="grid-column: span 12; text-align: center; color: var(--text-muted);">No courses added yet.</div>' : ''}
      ${courses.map(c => `
        <div class="card">
          <div class="card-header" style="margin-bottom: 8px;">
            <span class="badge badge-medium">${c.provider || 'Self-Study'}</span>
            <span style="font-size: 0.8rem; color: var(--text-muted);">${c.total_hours_spent || 0} hrs logged</span>
          </div>
          <h3 style="font-size: 1.1rem; margin-bottom: 6px;">${c.title}</h3>
          <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 14px;">${c.notes || 'Course materials & progress.'}</p>
          
          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
              <span>Modules: ${c.completed_modules}/${c.total_modules}</span>
              <span style="font-weight: 700;">${c.progress_percentage}%</span>
            </div>
            <div class="progress-container">
              <div class="progress-bar" style="width: ${c.progress_percentage}%;"></div>
            </div>
          </div>
        </div>
      `).join('')}
    </div>
  `;

  document.getElementById('btn-create-course').onclick = () => {
    openModal(
      'Add Learning Course',
      `
        <form id="modal-course-form">
          <div class="form-group">
            <label class="form-label">Course Title</label>
            <input type="text" id="m-course-title" class="form-control" placeholder="e.g. Distributed Systems Architecture" required>
          </div>
          <div class="form-group">
            <label class="form-label">Provider / Platform</label>
            <input type="text" id="m-course-provider" class="form-control" placeholder="e.g. Coursera, MIT OpenCourseWare, Self-Study">
          </div>
          <div class="form-group">
            <label class="form-label">Total Modules / Chapters</label>
            <input type="number" id="m-course-modules" class="form-control" value="10">
          </div>
        </form>
      `,
      async () => {
        const title = document.getElementById('m-course-title').value;
        const provider = document.getElementById('m-course-provider').value;
        const total_modules = document.getElementById('m-course-modules').value;

        try {
          await APIClient.post('/api/learning/courses', { title, provider, total_modules });
          showToast('Course added!', 'success');
          renderLearningView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };

  document.getElementById('btn-log-study').onclick = () => {
    openModal(
      'Log Study Session',
      `
        <form id="modal-study-form">
          <div class="form-group">
            <label class="form-label">Session Topic / Title</label>
            <input type="text" id="m-study-title" class="form-control" placeholder="e.g. SQLite WAL Mode & B-Trees" required>
          </div>
          <div class="form-group">
            <label class="form-label">Duration (Minutes)</label>
            <input type="number" id="m-study-duration" class="form-control" value="45" required>
          </div>
          <div class="form-group">
            <label class="form-label">Topics & Key Takeaways</label>
            <textarea id="m-study-takeaways" class="form-control" rows="3" placeholder="What did you learn?"></textarea>
          </div>
        </form>
      `,
      async () => {
        const title = document.getElementById('m-study-title').value;
        const duration_minutes = document.getElementById('m-study-duration').value;
        const key_takeaways = document.getElementById('m-study-takeaways').value;

        try {
          await APIClient.post('/api/learning/study-sessions', { title, duration_minutes, key_takeaways });
          showToast('Study session logged!', 'success');
          renderLearningView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };
}
