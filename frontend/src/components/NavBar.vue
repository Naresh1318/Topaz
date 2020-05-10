<template>
  <div>
    <v-navigation-drawer class="nav_bar" app width="300">
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
                Naresh Nagabushan
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
export default {
  name: 'NavBar',
  props: ['active_page'],
  data() {
    return {
      pages: {
        Home: '/',
        Projects: '/projects',
        Blog: '/blog',
      },
      footer: {
        github: {
          link: 'https://github.com/Naresh1318',
          icon: 'fa-github',
        },
        medium: {
          link: 'https://medium.com/@rnaresh.n',
          icon: 'fa-medium',
        },
        linkedin: {
          link: 'https://www.linkedin.com/in/naresh-nagabushan-2946b013a',
          icon: 'fa-linkedin',
        },
        twitter: {
          link: 'https://twitter.com/Naresh_Reddy_',
          icon: 'fa-twitter',
        },
      },
    };
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
