<template>
  <div class="home">
    <nav-bar active_page="Home"></nav-bar>
    <v-content>
      <v-container>
        <p>
          Omelette du fromage
        </p>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'Home',
  data() {
    return {
      drawer: false,
      page_name: 'Home',
    };
  },
  methods: {},
  components: {
    navBar: NavBar,
  },
};
</script>
