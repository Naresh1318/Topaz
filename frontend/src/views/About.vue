<template>
  <div class="about">
    <p>{{ page_name }}</p>
    <nav-bar active_page="About"></nav-bar>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'About',
  data() {
    return {
      page_name: 'About',
    };
  },
  components: {
    navBar: NavBar,
  },
};
</script>
