import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Questions API
export const questionsAPI = {
  getAll: (params) => api.get('/questions/', { params }),
  getById: (id) => api.get(`/questions/${id}/`),
  getRandom: () => api.get('/questions/random/'),
  getCategories: () => api.get('/questions/categories/'),
  filter: (filters) => api.get('/questions/', { params: filters }),
};

// Quiz Sessions API
export const quizAPI = {
  createSession: (data) => api.post('/quiz-sessions/create_session/', data),
  getSession: (id) => api.get(`/quiz-sessions/${id}/`),
  getUserSessions: (userId) => api.get('/quiz-sessions/', { params: { user_id: userId } }),
  submitAnswer: (sessionId, data) => api.post(`/quiz-sessions/${sessionId}/submit_answer/`, data),
  completeQuiz: (sessionId) => api.post(`/quiz-sessions/${sessionId}/complete/`),
};

// Users API
export const usersAPI = {
  register: (data) => api.post('/users/register/', data),
  getUser: (id) => api.get(`/users/${id}/`),
  getUserStats: (id) => api.get(`/users/${id}/stats/`),
};

// Bookmarks API
export const bookmarksAPI = {
  getAll: (userId) => api.get('/bookmarks/', { params: { user_id: userId } }),
  toggle: (data) => api.post('/bookmarks/toggle/', data),
};

// Leaderboard API
export const leaderboardAPI = {
  getWeekly: (weekStart) => api.get('/leaderboard/', { params: { week_start: weekStart } }),
};

export default api;
