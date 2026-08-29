/**
 * LifeOS UI Component — Modal Dialog Stack Manager
 */

export class ModalManager {
  static openModal(title, bodyHtml, onConfirm = null) {
    const overlay = document.getElementById('modal-overlay');
    const container = document.getElementById('modal-container');

    if (!overlay || !container) return;

    container.innerHTML = `
      <div class="card" style="width: 100%; max-width: 500px; padding: 24px;">
        <div class="card-header" style="margin-bottom: 16px;">
          <div class="card-title">${title}</div>
          <button class="btn btn-secondary btn-sm" id="modal-close-btn">&times;</button>
        </div>
        <div class="modal-body" style="margin-bottom: 20px;">
          ${bodyHtml}
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 12px;">
          <button class="btn btn-secondary" id="modal-cancel-btn">Cancel</button>
          ${onConfirm ? `<button class="btn btn-primary" id="modal-confirm-btn">Confirm</button>` : ''}
        </div>
      </div>
    `;

    overlay.style.display = 'flex';

    document.getElementById('modal-close-btn').onclick = () => ModalManager.closeModal();
    document.getElementById('modal-cancel-btn').onclick = () => ModalManager.closeModal();

    if (onConfirm) {
      document.getElementById('modal-confirm-btn').onclick = async () => {
        const success = await onConfirm();
        if (success !== false) {
          ModalManager.closeModal();
        }
      };
    }
  }

  static closeModal() {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) overlay.style.display = 'none';
  }
}
