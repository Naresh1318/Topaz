<template>
  <div class="projects">
    <nav-bar active_page="Projects"></nav-bar>
    <v-content>
      <div class="pa-1" v-for="project in projects" :key="project.title">
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
  name: 'Projects',
  data() {
    return {
      page_name: 'Projects',
      projects: [],
      latest_project: {},
      updated: {},
    };
  },
  methods: {
    get_repos() {
      // eslint-disable-next-line no-debugger
      debugger;
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
    this.get_repos();
  },
};
</script>

<style scoped>
.projects {
  padding-left: 1rem;
  padding-right: 1rem;
}
</style>
