/**
 * LifeOS Canvas Micro-Chart Engine — Full Analytical Visualizer Suite
 */

export class ChartEngine {
  /**
   * Renders a custom radial score gauge on a HTML5 Canvas context.
   */
  static renderRadialGauge(canvas, score, maxScore = 100, options = {}) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width || 200;
    const height = canvas.height || 200;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) - 20;

    ctx.clearRect(0, 0, width, height);

    // Background track arc
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, 2.25 * Math.PI, false);
    ctx.lineWidth = options.trackWidth || 14;
    ctx.strokeStyle = options.trackColor || '#1e293b';
    ctx.lineCap = 'round';
    ctx.stroke();

    // Progress arc
    const pct = Math.min(1.0, Math.max(0.0, score / maxScore));
    const startAngle = 0.75 * Math.PI;
    const endAngle = startAngle + (pct * 1.5 * Math.PI);

    const grad = ctx.createLinearGradient(0, 0, width, height);
    grad.addColorStop(0, options.colorStart || '#6366f1');
    grad.addColorStop(1, options.colorEnd || '#10b981');

    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle, false);
    ctx.lineWidth = options.progressWidth || 14;
    ctx.strokeStyle = grad;
    ctx.lineCap = 'round';
    ctx.stroke();

    // Text Label
    ctx.fillStyle = options.textColor || '#f8fafc';
    ctx.font = '800 2.2rem Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`${Math.round(score)}%`, centerX, centerY - 5);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '600 0.8rem Inter, sans-serif';
    ctx.fillText(options.label || 'LIFE SCORE', centerX, centerY + 25);
  }

  /**
   * Renders a responsive line chart with gradient fill.
   */
  static renderLineChart(canvas, labels, data, options = {}) {
    if (!canvas || !data || data.length === 0) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width || 400;
    const height = canvas.height || 200;
    const padding = 30;

    ctx.clearRect(0, 0, width, height);

    const maxVal = Math.max(...data, 10);
    const minVal = 0;

    const stepX = (width - padding * 2) / (data.length - 1 || 1);
    const scaleY = (height - padding * 2) / (maxVal - minVal);

    // Draw Grid Lines
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = height - padding - (i * (height - padding * 2) / 4);
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(width - padding, y);
      ctx.stroke();
    }

    // Line Path
    ctx.beginPath();
    data.forEach((val, i) => {
      const x = padding + (i * stepX);
      const y = height - padding - ((val - minVal) * scaleY);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });

    ctx.strokeStyle = options.strokeColor || '#6366f1';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Fill Area Under Line
    ctx.lineTo(width - padding - (0 * stepX), height - padding);
    ctx.lineTo(padding, height - padding);
    ctx.closePath();

    const grad = ctx.createLinearGradient(0, padding, 0, height - padding);
    grad.addColorStop(0, options.fillStart || 'rgba(99, 102, 241, 0.3)');
    grad.addColorStop(1, 'rgba(99, 102, 241, 0.0)');
    ctx.fillStyle = grad;
    ctx.fill();

    // Draw Data Points
    data.forEach((val, i) => {
      const x = padding + (i * stepX);
      const y = height - padding - ((val - minVal) * scaleY);
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, 2 * Math.PI);
      ctx.fillStyle = '#6366f1';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  }

  /**
   * Renders a responsive bar chart for categorical metrics.
   */
  static renderBarChart(canvas, labels, data, options = {}) {
    if (!canvas || !data || data.length === 0) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width || 400;
    const height = canvas.height || 200;
    const padding = 30;

    ctx.clearRect(0, 0, width, height);

    const maxVal = Math.max(...data, 10);
    const barWidth = ((width - padding * 2) / data.length) * 0.6;
    const stepX = (width - padding * 2) / data.length;

    data.forEach((val, i) => {
      const barHeight = (val / maxVal) * (height - padding * 2);
      const x = padding + (i * stepX) + (stepX - barWidth) / 2;
      const y = height - padding - barHeight;

      ctx.fillStyle = options.barColor || '#10b981';
      ctx.fillRect(x, y, barWidth, barHeight);

      // Label below bar
      if (labels[i]) {
        ctx.fillStyle = '#94a3b8';
        ctx.font = '500 0.75rem Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(labels[i], x + barWidth / 2, height - 10);
      }
    });
  }

  /**
   * Renders a donut pie chart for spending and time breakdowns.
   */
  static renderPieChart(canvas, dataSegments, options = {}) {
    if (!canvas || !dataSegments || dataSegments.length === 0) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width || 200;
    const height = canvas.height || 200;
    const centerX = width / 2;
    const centerY = height / 2;
    const outerRadius = Math.min(centerX, centerY) - 10;
    const innerRadius = outerRadius * 0.6;

    ctx.clearRect(0, 0, width, height);

    const total = dataSegments.reduce((sum, s) => sum + s.value, 0);
    if (total === 0) return;

    let currentAngle = -0.5 * Math.PI;

    dataSegments.forEach(seg => {
      const sliceAngle = (seg.value / total) * 2 * Math.PI;

      ctx.beginPath();
      ctx.arc(centerX, centerY, outerRadius, currentAngle, currentAngle + sliceAngle, false);
      ctx.arc(centerX, centerY, innerRadius, currentAngle + sliceAngle, currentAngle, true);
      ctx.closePath();

      ctx.fillStyle = seg.color || '#3b82f6';
      ctx.fill();

      currentAngle += sliceAngle;
    });
  }
}
