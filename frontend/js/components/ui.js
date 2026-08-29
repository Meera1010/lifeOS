/**
 * LifeOS UI Helpers, Modals, Toasts & Micro-Chart Engine
 */

export function showToast(message, type = 'info', duration = 4000) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icon = type === 'success' ? '✅' : (type === 'error' ? '❌' : 'ℹ️');
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

export function openModal(title, contentHTML, onConfirm = null) {
  const overlay = document.getElementById('app-modal');
  const titleEl = document.getElementById('modal-title');
  const bodyEl = document.getElementById('modal-body');
  const submitBtn = document.getElementById('btn-modal-submit');
  const cancelBtn = document.getElementById('btn-modal-cancel');
  const closeBtn = document.getElementById('btn-close-modal');

  if (!overlay || !bodyEl) return;

  titleEl.textContent = title;
  bodyEl.innerHTML = contentHTML;
  overlay.classList.add('active');

  const closeModalHandler = () => {
    overlay.classList.remove('active');
  };

  closeBtn.onclick = closeModalHandler;
  cancelBtn.onclick = closeModalHandler;

  submitBtn.onclick = async () => {
    if (onConfirm) {
      const success = await onConfirm();
      if (success !== false) closeModalHandler();
    } else {
      closeModalHandler();
    }
  };
}

export function closeModal() {
  const overlay = document.getElementById('app-modal');
  if (overlay) overlay.classList.remove('active');
}

/**
 * Custom Canvas Micro-Chart Renderer Engine
 */
export class ChartEngine {

  static renderRadialGauge(canvasId, score, maxScore = 100) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) - 12;

    ctx.clearRect(0, 0, width, height);

    // Background track
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, 2.25 * Math.PI);
    ctx.lineWidth = 14;
    ctx.strokeStyle = '#334155';
    ctx.lineCap = 'round';
    ctx.stroke();

    // Value Arc
    const percentage = Math.min(1.0, Math.max(0.0, score / maxScore));
    const endAngle = 0.75 * Math.PI + percentage * (1.5 * Math.PI);

    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, '#4f46e5');
    gradient.addColorStop(1, '#06b6d4');

    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, endAngle);
    ctx.lineWidth = 14;
    ctx.strokeStyle = gradient;
    ctx.lineCap = 'round';
    ctx.stroke();
  }

  static renderLineChart(canvasId, labels, dataPoints, label = 'Series') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    const padding = 40;

    ctx.clearRect(0, 0, w, h);

    if (!dataPoints || dataPoints.length === 0) return;

    const maxVal = Math.max(...dataPoints, 100);
    const stepX = (w - padding * 2) / (dataPoints.length - 1 || 1);

    // Draw Grid Lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padding + ((h - padding * 2) / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(w - padding, y);
      ctx.stroke();
    }

    // Line Plot
    ctx.beginPath();
    dataPoints.forEach((val, idx) => {
      const x = padding + idx * stepX;
      const y = h - padding - (val / maxVal) * (h - padding * 2);
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });

    ctx.strokeStyle = '#4f46e5';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Data Points
    dataPoints.forEach((val, idx) => {
      const x = padding + idx * stepX;
      const y = h - padding - (val / maxVal) * (h - padding * 2);
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI);
      ctx.fillStyle = '#06b6d4';
      ctx.fill();

      // Label text
      if (labels[idx]) {
        ctx.fillStyle = '#94a3b8';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(labels[idx], x, h - 12);
      }
    });
  }

  static renderPieChart(canvasId, labels, values, colors) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    const centerX = w / 2;
    const centerY = h / 2;
    const radius = Math.min(centerX, centerY) - 20;

    ctx.clearRect(0, 0, w, h);

    const total = values.reduce((a, b) => a + b, 0);
    if (total === 0) return;

    let startAngle = 0;
    values.forEach((val, idx) => {
      const sliceAngle = (val / total) * 2 * Math.PI;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
      ctx.closePath();
      ctx.fillStyle = colors[idx] || '#4f46e5';
      ctx.fill();
      startAngle += sliceAngle;
    });
  }
}
