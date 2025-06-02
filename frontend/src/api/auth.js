import apiClient from '../utils/axios';

export async function login(email, password) {
  const res = await apiClient.post('/api/auth/login', {
    email,
    password
  });

  const token = res.data.access_token;
  localStorage.setItem('token', token);
  return token;
}
