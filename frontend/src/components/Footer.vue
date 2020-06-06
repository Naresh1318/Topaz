<template>
  <v-footer>
    <v-row>
      <v-col style="text-align: center">
        {{ new Date().getFullYear() }} — <strong>{{ this.hacker }}</strong>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col v-for="website in footer" cols="2" style="text-align: center"
             :key="website.link">
        <a :href="website.link" style="text-decoration: none">
          <v-icon>{{ website.icon }}</v-icon>
        </a>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      footer: {},
      hacker: '',
    };
  },
  methods: {
    get_theme() {
      this.$http.get(`${this.$backend_address}/theme`)
        .then((response) => {
          this.footer = response.data.theme.nav_bar_footer;
          this.hacker = response.data.theme.name;
        });
    },
  },
  created() {
    this.get_theme();
  },
};
</script>

<style scoped>

</style>
