/**
 * LifeOS REST API HTTP Client Wrapper
 */

export class APIClient {
  static getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    const token = localStorage.getItem('lifeos_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  static async request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : endpoint;
    const config = {
      method: options.method || 'GET',
      headers: APIClient.getHeaders(),
      ...options
    };

    if (options.body && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);

      let data = {};
      const contentType = response.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        try {
          data = await response.json();
        } catch (jsonErr) {
          data = { error: 'Invalid JSON response from server.' };
        }
      } else {
        const text = await response.text();
        data = { error: text || `HTTP ${response.status} Error` };
      }

      if (response.status === 401) {
        localStorage.removeItem('lifeos_token');
        if (window.location.hash !== '#login' && window.location.hash !== '#register') {
          window.location.hash = '#login';
        }
        throw new Error(data.error || 'Authentication required. Please log in.');
      }

      if (!response.ok) {
        throw new Error(data.error || `HTTP Error ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`[API Error] ${endpoint}:`, error.message);
      throw error;
    }
  }

  static get(endpoint) {
    return APIClient.request(endpoint, { method: 'GET' });
  }

  static post(endpoint, body) {
    return APIClient.request(endpoint, { method: 'POST', body });
  }

  static put(endpoint, body) {
    return APIClient.request(endpoint, { method: 'PUT', body });
  }

  static delete(endpoint) {
    return APIClient.request(endpoint, { method: 'DELETE' });
  }
}
