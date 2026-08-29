/**
 * LifeOS Focus & Pomodoro Timer View Controller
 */

import { APIClient } from '../api.js';
import { showToast } from '../components/ui.js';

let timerInterval = null;
let secondsRemaining = 25 * 60;
let isRunning = false;
let distractionsCount = 0;

export async function renderFocusView(container) {
  const settingsRes = await APIClient.get('/api/focus/settings');
  const settings = settingsRes.data || { work_duration: 25 };

  secondsRemaining = settings.work_duration * 60;

  container.innerHTML = `
    <div class="card-header" style="margin-bottom: 20px;">
      <div>
        <h2>⏱️ Productivity & Focus Timer</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Deep work focus sessions, Pomodoro intervals, distraction tracking.</p>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 340px; gap: 20px;">
      <div class="card timer-display-container">
        <div style="text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); font-size: 0.85rem;">Focus Session</div>
        <div class="timer-clock" id="timer-clock-display">25:00</div>
        
        <div class="timer-controls">
          <button class="btn btn-primary" id="btn-timer-toggle">Start Focus</button>
          <button class="btn btn-secondary" id="btn-timer-reset">Reset</button>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title">🛡️ Distraction Log</div>
        </div>
        <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 16px;">Log any interruptions during this session to protect your flow state.</p>
        
        <div style="display: flex; gap: 8px; margin-bottom: 16px;">
          <input type="text" id="distraction-input" class="form-control" placeholder="e.g. Checked email notification">
          <button class="btn btn-secondary" id="btn-add-distraction">Log</button>
        </div>

        <div id="distraction-list" style="display: flex; flex-direction: column; gap: 8px;">
          <div style="font-size: 0.85rem; color: var(--text-muted);">Logged Distractions: <strong id="distraction-count-text">0</strong></div>
        </div>
      </div>
    </div>
  `;

  const clockEl = document.getElementById('timer-clock-display');
  const toggleBtn = document.getElementById('btn-timer-toggle');
  const resetBtn = document.getElementById('btn-timer-reset');

  function updateClockDisplay() {
    const mins = Math.floor(secondsRemaining / 60);
    const secs = secondsRemaining % 60;
    clockEl.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }

  toggleBtn.onclick = () => {
    if (isRunning) {
      clearInterval(timerInterval);
      isRunning = false;
      toggleBtn.textContent = 'Resume Focus';
      toggleBtn.className = 'btn btn-primary';
    } else {
      isRunning = true;
      toggleBtn.textContent = 'Pause';
      toggleBtn.className = 'btn btn-secondary';

      timerInterval = setInterval(async () => {
        if (secondsRemaining > 0) {
          secondsRemaining--;
          updateClockDisplay();
        } else {
          clearInterval(timerInterval);
          isRunning = false;
          toggleBtn.textContent = 'Start Focus';
          showToast('🎉 Focus Session Completed! Take a short break.', 'success', 8000);
          
          try {
            await APIClient.post('/api/focus/sessions', {
              duration_minutes: settings.work_duration,
              actual_minutes: settings.work_duration,
              distraction_count: distractionsCount
            });
          } catch (e) {
            console.error(e);
          }
        }
      }, 1000);
    }
  };

  resetBtn.onclick = () => {
    clearInterval(timerInterval);
    isRunning = false;
    secondsRemaining = settings.work_duration * 60;
    updateClockDisplay();
    toggleBtn.textContent = 'Start Focus';
    toggleBtn.className = 'btn btn-primary';
  };

  document.getElementById('btn-add-distraction').onclick = () => {
    const input = document.getElementById('distraction-input');
    if (input.value.trim()) {
      distractionsCount++;
      document.getElementById('distraction-count-text').textContent = distractionsCount;
      showToast('Distraction logged.', 'info');
      input.value = '';
    }
  };
}
