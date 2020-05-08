<template>
  <div class="projects">
    <nav-bar active_page="Projects"></nav-bar>
    <v-content>
      <info-card></info-card>
      <p>{{ page_name }}</p>
    </v-content>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import InfoCard from '../components/ProjectCard.vue';

export default {
  name: 'Projects',
  data() {
    return {
      page_name: 'Projects',
    };
  },
  components: {
    navBar: NavBar,
    infoCard: InfoCard,
  },
};
</script>

<style scoped>

</style>
