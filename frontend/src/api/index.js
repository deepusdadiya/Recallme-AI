import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000',
});

export async function uploadFile(formData) {
  const token = localStorage.getItem('token');

  return axios.post('http://localhost:8000/api/file/upload', formData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });
}

export const queryMemory = (query) => API.post('/api/memory/query', { query });