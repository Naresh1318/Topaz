import Vue from 'vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';


function isAuthenticated() {
  return axios.get(`${Vue.prototype.$backend_address}/is_authenticated`,
    {
      withCredentials: true,
    });
}

function logout() {
  return axios.get(`${Vue.prototype.$backend_address}/logout`,
    {
      withCredentials: true,
    });
}

Vue.prototype.$http = axios;
// debugging only
// Vue.prototype.$backend_address = 'http://localhost:5000';
Vue.prototype.$backend_address = '';
Vue.prototype.$is_authenticated = isAuthenticated;
Vue.prototype.$logout = logout;
Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
