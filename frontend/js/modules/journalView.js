/**
 * LifeOS Journal & Reflection View Controller
 */

import { APIClient } from '../api.js';
import { showToast, openModal } from '../components/ui.js';

export async function renderJournalView(container) {
  const res = await APIClient.get('/api/journal/entries');
  const entries = res.data || [];

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>📖 Daily Journal & Reflection</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Reflect on your daily thoughts, track mood, energy levels, and private entries.</p>
      </div>
      <button class="btn btn-primary" id="btn-new-journal">+ New Entry</button>
    </div>

    <div class="journal-layout">
      <!-- Journal List Sidebar -->
      <div class="journal-sidebar-list">
        <h4 style="margin-bottom: 8px;">Entries History</h4>
        ${entries.length === 0 ? '<div style="color: var(--text-muted); font-size: 0.85rem;">No journal entries logged.</div>' : ''}
        ${entries.map(e => `
          <div class="card" style="padding: 12px; cursor: pointer;" onclick="loadJournalEntry(${e.id})">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted);">
              <span>${e.entry_date}</span>
              <span>${e.mood}</span>
            </div>
            <div style="font-weight: 600; font-size: 0.9rem; margin-top: 4px;">${e.title}</div>
          </div>
        `).join('')}
      </div>

      <!-- Journal Entry Reader / Editor -->
      <div class="journal-reader" id="journal-reader-container">
        ${entries.length > 0 ? `
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div>
              <span class="badge badge-medium">${entries[0].mood.toUpperCase()}</span>
              <span style="font-size: 0.85rem; color: var(--text-muted); margin-left: 8px;">${entries[0].entry_date}</span>
            </div>
            <button class="btn btn-secondary btn-sm" onclick="deleteJournalEntry(${entries[0].id})">Delete</button>
          </div>
          <h2 style="margin-bottom: 12px;">${entries[0].title}</h2>
          <div style="line-height: 1.7; color: var(--text-primary); font-size: 0.95rem;">${entries[0].content}</div>
        ` : '<div style="text-align: center; color: var(--text-muted); padding: 80px;">Select or create a daily journal entry.</div>'}
      </div>
    </div>
  `;

  document.getElementById('btn-new-journal').onclick = () => {
    openModal(
      'New Daily Journal Entry',
      `
        <form id="modal-journal-form">
          <div class="form-group">
            <label class="form-label">Entry Title</label>
            <input type="text" id="m-journal-title" class="form-control" placeholder="e.g. Reflections on Productivity Flow" required>
          </div>
          <div class="form-group">
            <label class="form-label">Mood</label>
            <select id="m-journal-mood" class="form-control">
              <option value="great">Great 😁</option>
              <option value="good" selected>Good 🙂</option>
              <option value="neutral">Neutral 😐</option>
              <option value="low">Low 😔</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Content</label>
            <textarea id="m-journal-content" class="form-control" rows="6" placeholder="Write your daily thoughts..." required></textarea>
          </div>
        </form>
      `,
      async () => {
        const title = document.getElementById('m-journal-title').value;
        const mood = document.getElementById('m-journal-mood').value;
        const content = document.getElementById('m-journal-content').value;

        try {
          await APIClient.post('/api/journal/entries', { title, mood, content });
          showToast('Journal entry saved!', 'success');
          renderJournalView(container);
          return true;
        } catch (err) {
          showToast(err.message, 'error');
          return false;
        }
      }
    );
  };

  window.deleteJournalEntry = async (id) => {
    try {
      await APIClient.delete(`/api/journal/entries/${id}`);
      showToast('Journal entry deleted.', 'info');
      renderJournalView(container);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };
}
