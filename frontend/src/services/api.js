import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses (token expired/invalid)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Employee API calls
export const employeeAPI = {
  getAll: () => api.get('/api/employees'),
  create: (data) => api.post('/api/employees', data),
  delete: (employeeId) => api.delete(`/api/employees/${employeeId}`),
  getNextId: () => api.get('/api/employees/next-id'),
};

// Attendance API calls
export const attendanceAPI = {
  getByEmployee: (employeeId, startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return api.get(`/api/attendance/${employeeId}?${params}`);
  },
  create: (data) => api.post('/api/attendance', data),
  getStats: (employeeId) => api.get(`/api/attendance/${employeeId}/stats`),
};

export default api;
