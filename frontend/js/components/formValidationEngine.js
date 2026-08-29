/**
 * LifeOS Form Validation & Sanitization Engine
 */

export class FormValidationEngine {
  static validateRequired(value, fieldName) {
    if (!value || String(value).trim() === '') {
      return `${fieldName} is required and cannot be empty.`;
    }
    return null;
  }

  static validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!re.test(String(email).toLowerCase())) {
      return 'Please enter a valid email address.';
    }
    return null;
  }

  static validateMinLength(value, minLen, fieldName) {
    if (String(value).length < minLen) {
      return `${fieldName} must be at least ${minLen} characters long.`;
    }
    return null;
  }

  static validateNumericRange(value, min, max, fieldName) {
    const num = Number(value);
    if (isNaN(num) || num < min || num > max) {
      return `${fieldName} must be a number between ${min} and ${max}.`;
    }
    return null;
  }

  static sanitizeInput(str) {
    if (typeof str !== 'string') return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
  }
}
