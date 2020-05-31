import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/Projects.vue'),
  },
  {
    path: '/blog',
    name: 'Blog',
    component: () => import('../views/Blog.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    // eslint-disable-next-line no-unused-vars
    beforeEnter(to, from, next) {
      Vue.prototype.$is_authenticated()
        .then((response) => {
          if (!response.data.is_authenticated) {
            next();
          } else {
            next('/');
          }
        });
    },
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../views/Login.vue'),
    beforeEnter(to, from, next) {
      Vue.prototype.$logout()
        .then(() => {
          next('/');
        });
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
