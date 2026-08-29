/**
 * LifeOS Task Manager View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal } from '../components/ui.js';

export async function renderTasksView(container) {
  const res = await APIClient.get('/api/tasks');
  const tasks = res.data || [];

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>📋 Task Manager</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Organize tasks, subtasks, priorities, and deadlines.</p>
      </div>
      <button class="btn btn-primary" id="btn-create-task">+ Create Task</button>
    </div>

    <div class="tasks-toolbar">
      <div class="filters-group">
        <select id="filter-priority" class="filter-select">
          <option value="">All Priorities</option>
          <option value="urgent">Urgent</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <select id="filter-status" class="filter-select">
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>
    </div>

    <div class="task-list" id="task-list-container">
      ${tasks.length === 0 ? '<div style="padding: 40px; text-align: center; color: var(--text-muted);">No tasks found. Click "+ Create Task" to get started.</div>' : ''}
      ${tasks.map(t => `
        <div class="task-card-item" data-id="${t.id}">
          <div class="task-left">
            <div class="custom-checkbox ${t.status === 'completed' ? 'checked' : ''}" onclick="toggleTaskStatus(${t.id}, '${t.status}')">
              ${t.status === 'completed' ? '✓' : ''}
            </div>
            <div>
              <div class="task-title ${t.status === 'completed' ? 'completed' : ''}">${t.title}</div>
              <div class="task-meta">
                <span class="badge badge-${t.priority}">${t.priority}</span>
                <span>📅 ${t.due_date ? t.due_date.split('T')[0] : 'No due date'}</span>
                <span>⏱️ ${t.estimated_minutes}m est</span>
                <span>Subtasks: ${t.progress_percentage}%</span>
              </div>
            </div>
          </div>
          <button class="btn btn-secondary btn-sm" onclick="deleteTask(${t.id})">Delete</button>
        </div>
      `).join('')}
    </div>
  `;

  // Create Task Modal Trigger
  document.getElementById('btn-create-task').onclick = () => {
    openModal(
      'Create New Task',
      `
        <form id="modal-task-form">
          <div class="form-group">
            <label class="form-label">Task Title</label>
            <input type="text" id="m-task-title" class="form-control" placeholder="e.g. Prepare Quarterly Presentation" required>
          </div>
          <div class="form-group">
            <label class="form-label">Priority</label>
            <select id="m-task-priority" class="form-control">
              <option value="low">Low</option>
              <option value="medium" selected>Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Due Date</label>
            <input type="date" id="m-task-due" class="form-control">
          </div>
          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea id="m-task-desc" class="form-control" rows="3" placeholder="Optional notes..."></textarea>
          </div>
        </form>
      `,
      async () => {
        const title = document.getElementById('m-task-title').value;
        const priority = document.getElementById('m-task-priority').value;
        const due_date = document.getElementById('m-task-due').value;
        const description = document.getElementById('m-task-desc').value;

        try {
          await APIClient.post('/api/tasks', { title, priority, due_date, description });
          showToast('Task created successfully!', 'success');
          renderTasksView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };

  // Expose global action functions
  window.toggleTaskStatus = async (taskId, currentStatus) => {
    const newStatus = currentStatus === 'completed' ? 'pending' : 'completed';
    try {
      await APIClient.put(`/api/tasks/${taskId}`, { status: newStatus });
      renderTasksView(container);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  window.deleteTask = async (taskId) => {
    try {
      await APIClient.delete(`/api/tasks/${taskId}`);
      showToast('Task deleted.', 'info');
      renderTasksView(container);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };
}
