import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import ParticipationPage from './components/ParticipationPage.vue';
import VerificationPage from './components/VerificationPage.vue';
import LoginPage from './components/LoginPage.vue';
import UserListPage from './components/UserListPage.vue';


const routes=[
  {
    path: '/',
    name: 'home',
    component: HomePage, 
  },
  {
    path: '/participation',
    name: 'participation',
    component: ParticipationPage,
  },
  {
    path: '/verify/:uidb64/:token',
    name: 'verification',
    component: VerificationPage,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  {
    path: '/admin/users',
    name: 'user-list',
    component: UserListPage,
  },

];



const router = createRouter({
  history: createWebHistory(),  // Usando el modo history en lugar de hash
  routes,
});

// Agregar un "beforeEach" para proteger las rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');  // Comprobar si el usuario tiene un token de autenticación
  const isAdmin = localStorage.getItem('isAdmin');  // Comprobar si el usuario es admin (guardado al hacer login)

  // Si la ruta requiere autenticación
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/login');  // Redirige al login si no está autenticado
    } else if (to.matched.some(record => record.meta.requiresAdmin) && isAdmin !== 'true') {
      next('/');  // Si es una ruta solo para administradores y no es admin, redirige al home
    } else {
      next();  // Si todo está bien, sigue con la navegación
    }
  } else {
    next();  // Si la ruta no requiere autenticación, permite el acceso
  }
});


export default router;