/**
 * LifeOS Calendar View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal } from '../components/ui.js';

export async function renderCalendarView(container) {
  const today = new Date();
  const res = await APIClient.get(`/api/calendar/month-view?year=${today.getFullYear()}&month=${today.getMonth() + 1}`);
  const data = res.data || {};
  const events = data.events || [];

  container.innerHTML = `
    <div class="calendar-header-toolbar">
      <div>
        <h2>📅 Calendar & Events</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Unified schedule containing events, task deadlines, and goal milestones.</p>
      </div>
      <button class="btn btn-primary" id="btn-create-event">+ Add Event</button>
    </div>

    <div class="card" style="padding: 0; overflow: hidden;">
      <div class="month-grid">
        <div class="day-cell-header">MON</div>
        <div class="day-cell-header">TUE</div>
        <div class="day-cell-header">WED</div>
        <div class="day-cell-header">THU</div>
        <div class="day-cell-header">FRI</div>
        <div class="day-cell-header">SAT</div>
        <div class="day-cell-header">SUN</div>

        ${Array.from({ length: 35 }).map((_, idx) => {
          const dayNum = (idx % 31) + 1;
          const dayEvents = events.filter(e => {
            const d = new Date(e.start_time);
            return d.getDate() === dayNum;
          });

          return `
            <div class="day-cell">
              <span class="day-number">${dayNum}</span>
              ${dayEvents.map(ev => `
                <div class="event-chip" style="background-color: ${ev.color || '#3b82f6'};" title="${ev.title}">
                  ${ev.title}
                </div>
              `).join('')}
            </div>
          `;
        }).join('')}
      </div>
    </div>
  `;

  document.getElementById('btn-create-event').onclick = () => {
    openModal(
      'Schedule Calendar Event',
      `
        <form id="modal-event-form">
          <div class="form-group">
            <label class="form-label">Event Title</label>
            <input type="text" id="m-event-title" class="form-control" placeholder="e.g. Team Planning Sync" required>
          </div>
          <div class="form-group">
            <label class="form-label">Start Time</label>
            <input type="datetime-local" id="m-event-start" class="form-control" required>
          </div>
          <div class="form-group">
            <label class="form-label">End Time</label>
            <input type="datetime-local" id="m-event-end" class="form-control">
          </div>
          <div class="form-group">
            <label class="form-label">Location / Link</label>
            <input type="text" id="m-event-location" class="form-control" placeholder="e.g. Conference Room A or Zoom link">
          </div>
        </form>
      `,
      async () => {
        const title = document.getElementById('m-event-title').value;
        const start_time = document.getElementById('m-event-start').value;
        const end_time = document.getElementById('m-event-end').value;
        const location = document.getElementById('m-event-location').value;

        try {
          await APIClient.post('/api/calendar/events', { title, start_time, end_time, location });
          showToast('Event scheduled!', 'success');
          renderCalendarView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };
}
