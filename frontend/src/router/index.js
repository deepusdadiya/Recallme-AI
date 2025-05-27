import { createRouter, createWebHistory } from 'vue-router'
import HeroPage from '../views/HeroPage.vue'
import LoginPage from '../views/LoginPage.vue'
import DashboardPage from '../views/DashboardPage.vue'

const routes = [
  { path: '/', component: HeroPage },
  { path: '/login', component: LoginPage },
  { path: '/dashboard', component: DashboardPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router