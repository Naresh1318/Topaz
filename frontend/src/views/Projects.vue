<template>
  <div class="projects">
    <nav-bar active_page="Projects"></nav-bar>
    <v-content>
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
      <v-footer style="background-color: white;">
        <p style="color: gray">
          {{ updated }}
        </p>
      </v-footer>
    </v-content>
  </div>
</template>

<script>
import mobile from '../js/utils';
import NavBar from '../components/NavBar.vue';
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
  },
  created() {
    this.get_repos();
    if (mobile.isMobile()) {
      this.is_mobile = true;
    }
  },
};
</script>
