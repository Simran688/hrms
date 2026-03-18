import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const authAPI = {
  register: (userData) => axios.post(`${API_BASE_URL}/api/auth/register`, userData),
  login: (credentials) => axios.post(`${API_BASE_URL}/api/auth/login`, credentials),
  getCurrentUser: (token) => {
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    };
    return axios.get(`${API_BASE_URL}/api/auth/me`, config);
  }
};

export default authAPI;
