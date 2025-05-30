// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import Dashboard from '../views/Dashboard.vue';
import UploadMemory from '../components/UploadFile.vue';
import AskMemory from '../components/QueryMemory.vue';
import Signup from '../views/Signup.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/dashboard', component: Dashboard },
  { path: '/upload', component: UploadMemory },
  { path: '/ask', component: AskMemory },
  {path: '/signup', component: Signup}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;