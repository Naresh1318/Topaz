/* eslint-disable arrow-body-style */
import Vue from 'vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';


async function isAuthenticated() {
  await axios.get(`${Vue.prototype.$backend_address}/is_authenticated`,
    {
      withCredentials: true,
    })
    .then((response) => {
      return response.data.is_authenticated;
    });
}

async function logout() {
  await axios.get(`${Vue.prototype.$backend_address}/logout`,
    {
      withCredentials: true,
    })
    .then((response) => {
      return response.data.logged_out;
    });
}

Vue.prototype.$http = axios;
Vue.prototype.$backend_address = 'http://localhost:5000';
Vue.prototype.$is_authenticated = isAuthenticated;
Vue.prototype.$logout = logout;
Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
