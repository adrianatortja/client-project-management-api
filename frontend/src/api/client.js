import axios from 'axios';

// Nullish coalescing (not ||): an explicitly empty string means "same-origin"
// (used in production behind the nginx reverse proxy), which must not fall
// back to the localhost dev default.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

const client = axios.create({ baseURL: API_BASE_URL });

client.interceptors.request.use((config) => {
  const access = localStorage.getItem('access_token');
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

let refreshPromise = null;

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, response } = error;

    if (response?.status !== 401 || config._retried) {
      return Promise.reject(error);
    }

    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) {
      return Promise.reject(error);
    }

    config._retried = true;

    try {
      refreshPromise =
        refreshPromise ||
        axios.post(`${API_BASE_URL}/api/auth/refresh/`, { refresh });
      const { data } = await refreshPromise;
      localStorage.setItem('access_token', data.access);
      config.headers.Authorization = `Bearer ${data.access}`;
      return client(config);
    } catch (refreshError) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
      return Promise.reject(refreshError);
    } finally {
      refreshPromise = null;
    }
  }
);

export default client;
