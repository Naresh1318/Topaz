<template>
  <div class="blog">
    <p>{{ page_name }}</p>
    <nav-bar active_page="Blog"></nav-bar>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'Blog',
  data() {
    return {
      page_name: 'Blog',
    };
  },
  components: {
    navBar: NavBar,
  },
};
</script>

<style scoped>

</style>
