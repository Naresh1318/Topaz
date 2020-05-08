<template>
  <div class="projects">
    <p>{{ page_name }}</p>
    <nav-bar active_page="Projects"></nav-bar>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'Projects',
  data() {
    return {
      page_name: 'Projects',
    };
  },
  components: {
    navBar: NavBar,
  },
};
</script>

<style scoped>

</style>
