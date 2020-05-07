<template>
  <div class="home">
    <p>{{ page_name }}</p>
    <nav-bar text="Calling from home"></nav-bar>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'Home',
  data() {
    return {
      page_name: 'Home',
    };
  },
  components: {
    navBar: NavBar,
  },
};
</script>
