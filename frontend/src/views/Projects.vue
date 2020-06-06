<template>
  <div class="projects">
    <nav-bar active_page="Projects"></nav-bar>
    <v-content>
      <v-app-bar v-if="show_app_bar()" color="#fff" light flat>
       <v-toolbar-title>Logged in as admin</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn @click="show_visibility_toggle = !show_visibility_toggle" icon>
          <v-icon v-if="!show_visibility_toggle">fa-eye-slash</v-icon>
          <v-icon v-else>fa-close</v-icon>
        </v-btn>
        <v-btn href="/logout" color="dark" dark>Logout</v-btn>
      </v-app-bar>
      <github-project-selector v-if="show_visibility_toggle" @submitted="get_repos">
      </github-project-selector>
      <v-container :style="main_content_css">
        <v-progress-linear :active="loading" :indeterminate="loading"
                           absolute top color="black accent-4">
        </v-progress-linear>
        <div class="pa-1" v-for="project in projects" :key="project.title">
          <div v-if="project.visible === 1">
            <v-divider></v-divider>
            <project-card :title="project.title" :url="project.url"
                          :description="project.description" :stars="project.stars"
                          :primary_language="project.primary_language"
                          :primary_language_color="project.primary_language_color"
                          :image_url="project.image_url" :is_mobile="is_mobile"></project-card>
          </div>
        </div>
      </v-container>
    </v-content>
    <div v-if="this.is_mobile">
      <footer-comp></footer-comp>
    </div>
  </div>
</template>

<script>
import mobile from '../js/utils';
import NavBar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';
import GithubProjectSelector from '../components/GithubProjectSelector.vue';
import ProjectCard from '../components/ProjectCard.vue';

export default {
  name: 'Projects',
  data() {
    return {
      page_name: 'Projects',
      projects: [],
      latest_project: {},
      updated: '',
      is_mobile: false,
      loading: true,
      is_admin: false,
      show_visibility_toggle: false,
    };
  },
  methods: {
    get_repos() {
      // Get all public repos
      this.$http.get(`${this.$backend_address}/public_repos`)
        .then((response) => {
          this.loading = false;
          this.projects = response.data.repos;
          // eslint-disable-next-line prefer-destructuring
          this.latest_project = this.projects[0];
          this.updated = response.data.updated;
        });
    },
    show_app_bar() {
      if (mobile.isMobile()) {
        return false;
      }
      return this.is_admin;
    },
  },
  computed: {
    main_content_css() {
      if (this.is_mobile) {
        return {
          paddingRight: '0rem',
          paddingLeft: '0rem',
        };
      }
      return {
        paddingRight: '2rem',
        paddingLeft: '2rem',
      };
    },
  },
  components: {
    navBar: NavBar,
    projectCard: ProjectCard,
    githubProjectSelector: GithubProjectSelector,
    footerComp: Footer,
  },
  created() {
    this.get_repos();
    if (mobile.isMobile()) {
      this.is_mobile = true;
    }
    this.$is_authenticated()
      .then((response) => {
        if (response.data.is_authenticated) {
          this.is_admin = true;
        }
      });
  },
};
</script>
