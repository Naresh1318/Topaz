<template>
  <div class="home">
    <nav-bar active_page="Home"></nav-bar>
    <v-content>
      <v-container :style="main_content_css">
        <p>
          Omelette du fromage
        </p>
      </v-container>
    </v-content>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import mobile from '../js/utils';

export default {
  name: 'Home',
  data() {
    return {
      drawer: false,
      page_name: 'Home',
    };
  },
  methods: {},
  computed: {
    main_content_css() {
      if (this.is_mobile) {
        return {
          paddingRight: '1rem',
          paddingLeft: '1rem',
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
  },
  created() {
    if (mobile.isMobile()) {
      this.is_mobile = true;
    }
  },
};
</script>
