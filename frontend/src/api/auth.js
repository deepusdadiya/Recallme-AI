import apiClient from '../utils/axios';

export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append('username', email);  // OAuth2 spec uses 'username'
  formData.append('password', password);

  const res = await apiClient.post('/api/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  const token = res.data.access_token;
  localStorage.setItem('token', token);
  return token;
}