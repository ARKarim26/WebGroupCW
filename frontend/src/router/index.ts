// Example of how to use Vue Router
import { createRouter, createWebHistory } from 'vue-router';

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import LoginPage from '../pages/LoginPage.vue'; 
import ProfilePage from '../pages/ProfilePage.vue';
import RegisterPage from '../pages/RegisterPage.vue';
import ArticlesListPage from '../pages/ArticlesListPage.vue';
import ArticleDetailPage from '../pages/ArticleDetailPage.vue';

let base = (import.meta.env.MODE === 'development') ? import.meta.env.BASE_URL : '';

// 2. Define some routes
const router = createRouter({
  history: createWebHistory(base),
  routes: [
    { path: '/', name: 'Main Page', component: MainPage },
    { path: '/register', name: 'Register', component: RegisterPage },
    { path: '/login', name: 'Login Page', component: LoginPage },
    { path: '/profile', name: 'Profile Page', component: ProfilePage },
    { path: '/articles', name: 'Articles List', component: ArticlesListPage },
    { path: '/articles/:id', name: 'Article Detail', component: ArticleDetailPage },
  ]
});

export default router;

