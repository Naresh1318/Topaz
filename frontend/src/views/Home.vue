<template>
  <div class="home">
    <nav-bar active_page="Home"></nav-bar>
    <v-content>
      <div class="pa-3" v-for="project in projects" :key="project.title">
        <project-card :title="project.title" :url="project.url"
        :description="project.description" :stars="project.stars"
        :primary_language="project.primary_language"
        :primary_language_color="project.primary_language_color"
        :image_url="project.image_url"></project-card>
      </div>
    </v-content>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import ProjectCard from '../components/ProjectCard.vue';

export default {
  name: 'Home',
  data() {
    return {
      page_name: 'Home',
      projects: [],
      latest_project: {},
      updated: {},
    };
  },
  methods: {
    get_repos() {
      // Get all public repos
      this.$http.get(`${this.$backend_address}/public_repos`)
        .then((response) => {
          this.projects = response.data.repos;
          // eslint-disable-next-line prefer-destructuring
          this.latest_project = this.projects[0];
          this.updated = response.data.updated;
        });
    },
  },
  components: {
    navBar: NavBar,
    projectCard: ProjectCard,
  },
  created() {
  },
};
</script>
