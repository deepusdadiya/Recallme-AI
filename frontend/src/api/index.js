import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000', // FastAPI backend URL
});

export const uploadFile = (formData) => API.post('/api/file/upload', formData);
export const queryMemory = (query) => API.post('/api/memory/query', { query });