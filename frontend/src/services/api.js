import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication API
export const loginWithEmailPassword = (username, password) =>
  api.post('/auth/login/', { username, password });

export const googleAuthLogin = (idToken, email, displayName) =>
  api.post('/auth/google-login/', { id_token: idToken, email, display_name: displayName });

export const registerUser = (data) =>
  api.post('/auth/register/', data);

export const fetchCurrentUser = () =>
  api.get('/auth/current-user/');

export const requestPasswordReset = (email) =>
  api.post('/auth/password-reset-request/', { email });

export const confirmPasswordReset = (uid, token, password, password_confirm) =>
  api.post('/auth/password-reset-confirm/', { uid, token, password, password_confirm });

// Questions API
export const questionsAPI = {
  getAll: (params) => api.get('/questions/', { params }),
  getById: (id) => api.get(`/questions/${id}/`),
  byCategory: () => api.get('/questions/by_category/'),
  byDifficulty: () => api.get('/questions/by_difficulty/'),
};

// Quizzes API
export const quizzesAPI = {
  getAll: (params) => api.get('/quizzes/', { params }),
  getById: (id) => api.get(`/quizzes/${id}/`),
  start: (id) => api.post(`/quizzes/${id}/start/`),
  byType: (type) => api.get(`/quizzes/by_type/?type=${type}`),
};

// Quiz Sessions API
export const sessionsAPI = {
  getAll: () => api.get('/sessions/'),
  getById: (id) => api.get(`/sessions/${id}/`),
  submitAnswer: (id, data) => api.post(`/sessions/${id}/submit_answer/`, data),
  finish: (id) => api.post(`/sessions/${id}/finish/`),
  review: (id) => api.get(`/sessions/${id}/review/`),
  createCustomSession: (data) => api.post('/sessions/create_custom/', data),
};

// User Profile API
export const profileAPI = {
  getMe: () => api.get('/profile/me/'),
  update: (data) => api.put('/profile/', data),
};

// Bookmarks API
export const bookmarksAPI = {
  getAll: () => api.get('/bookmarks/'),
  create: (questionId) => api.post('/bookmarks/', { question_id: questionId }),
  isBookmarked: (questionId) => api.get(`/bookmarks/is_bookmarked/?question_id=${questionId}`),
};

// Leaderboard API
export const leaderboardAPI = {
  getAll: (period = 'week') => api.get('/leaderboard/', { params: { period } }),
  topPerformers: (period = 'week') => api.get('/leaderboard/top_performers/?period=' + period),
};

// Auth API
export const authAPI = {
  login: (token) => api.post('/auth/google/', { access_token: token }),
  logout: () => api.post('/auth/logout/'),
};

export default api;
