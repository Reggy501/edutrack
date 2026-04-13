import axios from 'axios';

const API_BASE = 'http://localhost';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: (credentials) => api.post('/api/auth/login/', credentials),
  register: (data) => api.post('/api/auth/register/', data),
  profile: () => api.get('/api/auth/profile/'),
};

export const studentService = {
  getAll: () => api.get('/api/students/'),
  create: (data) => api.post('/api/students/', data),
  update: (id, data) => api.patch(`/api/students/${id}/`, data),
  delete: (id) => api.delete(`/api/students/${id}/`),
  getActive: () => api.get('/api/students/active/'),
};

export const attendanceService = {
  getAll: () => api.get('/api/attendance/'),
  create: (data) => api.post('/api/attendance/', data),
  getByStudent: (id) => api.get(`/api/attendance/by_student/?student_id=${id}`),
  getByDate: (date) => api.get(`/api/attendance/by_date/?date=${date}`),
};

export const gradeService = {
  getAll: () => api.get('/api/grades/'),
  create: (data) => api.post('/api/grades/', data),
  getByStudent: (id) => api.get(`/api/grades/by_student/?student_id=${id}`),
  getReportCard: (id, term, year) => api.get(`/api/grades/report_card/?student_id=${id}&term=${term}&year=${year}`),
};

export const notificationService = {
  getAll: () => api.get('/api/notifications/'),
  sendAttendanceAlert: (data) => api.post('/api/notifications/send_attendance_alert/', data),
};

export default api;
