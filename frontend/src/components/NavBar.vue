<template>
  <div>
    <v-app-bar v-if="is_mobile()" height="175px"
         style="background-color: black;">
      <v-toolbar-title style="margin: auto">
        <v-row>
          <v-col cols="12" style="text-align: center">
            <div style="font-family: 'Beth Ellen', sans-serif; color: white">
              {{ hacker }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col v-for="(page, name) in pages" :key="name">
            <router-link v-if="name === active_page" class="btn-text" :to="page"
                         style="text-decoration: underline">
              {{ name }}
            </router-link>
            <router-link v-else class="btn-text" :to="page">
              {{ name }}
            </router-link>
          </v-col>
        </v-row>
      </v-toolbar-title>
    </v-app-bar>
    <v-navigation-drawer v-else class="nav_bar" app :width="get_width()" v-model="drawer">
      <v-card class="nav_bar_card" dark raised height="100%">
        <v-container style="height: 90vh">
          <v-row align="center" style="height: 100%">
            <v-col>
              <v-row v-for="(page, name) in pages" :key="name">
                <v-col v-if="name === active_page">
                  <router-link class="btn-text" :to="page" style="text-decoration: underline">
                    {{ name }}
                  </router-link>
                </v-col>
                <v-col v-else>
                  <router-link class="btn-text" :to="page">
                    {{ name }}
                  </router-link>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-container>

        <!-- Navigation footer -->
        <v-container style="bottom: 0; position: absolute">
          <v-row>
            <v-col cols="12" style="text-align: center">
              <div style="font-family: 'Beth Ellen', sans-serif">
                {{ hacker }}
              </div>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col v-for="website in footer" cols="2" style="text-align: center"
                   :key="website.link">
              <a :href="website.link" style="text-decoration: none">
                <v-icon>{{ website.icon }}</v-icon>
              </a>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-navigation-drawer>
  </div>
</template>

<script>
import mobile from '../js/utils';

export default {
  name: 'NavBar',
  props: {
    active_page: String,
  },
  data() {
    return {
      drawer: false,
      pages: {
        Home: '/',
        Projects: '/projects',
        Blog: '/blog',
      },
      footer: {},
      hacker: '',
    };
  },
  methods: {
    get_theme() {
      this.$http.get(`${this.$backend_address}/theme`)
        .then((response) => {
          this.footer = response.data.theme.nav_bar_footer;
          this.hacker = response.data.theme.name;
        });
    },
    get_width() {
      if (mobile.isMobile()) {
        return '100%';
      }
      return '300';
    },

    is_mobile() {
      if (mobile.isMobile()) {
        return true;
      }
      this.drawer = true;
      return false;
    },
  },
  created() {
    this.get_theme();
  },
};
</script>

<style scoped>
.nav_bar {
  font-family: 'Source Sans Pro', sans-serif !important;
}

.nav_bar_card {
  border-radius: 0 !important;
  background-color: #101010 !important;
}

.btn-text {
  font-family: 'Source Sans Pro', sans-serif;
  position: relative;
  display: inline-block;
  font-size: 24px;
  font-weight: 400;
  text-align: center;
  color: #fff;
  padding: 0.75rem;
  text-decoration: none;
}

.btn-text:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
