// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import Dashboard from '../views/Dashboard.vue';
import UploadMemory from '../components/UploadFile.vue';
import AskMemory from '../components/QueryMemory.vue';
import Signup from '../views/Signup.vue';
import { isAuthenticated } from '../utils/auth';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true }  },
  { path: '/upload', component: UploadMemory, meta: { requiresAuth: true }  },
  { path: '/query', component: AskMemory, meta: { requiresAuth: true }  },
  {path: '/signup', component: Signup}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = isAuthenticated()
  if (to.meta.requiresAuth && !loggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router;