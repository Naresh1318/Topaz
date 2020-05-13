<template>
  <div class="blog">
    <nav-bar active_page="Blog"></nav-bar>
    <v-content>
      <div class="pa-1" v-for="blog in blogs" :key="blog.title">
        <v-divider></v-divider>
        <regular-old-card :title="blog.title" :description="blog.description"
        :url="blog.url" :image_url="blog.image_url"></regular-old-card>
      </div>
      <v-footer style="background-color: white">
        <p style="color: gray">
          Updated: {{ updated }}
        </p>
      </v-footer>
    </v-content>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import RegularOldCard from '../components/RegularOldCard.vue';

export default {
  name: 'Blog',
  data() {
    return {
      page_name: 'Blog',
      blogs: [],
      updated: '',
    };
  },
  methods: {
    get_bogs() {
      // Get all public repos
      this.$http.get(`${this.$backend_address}/blogs`)
        .then((response) => {
          this.blogs = response.data.blogs;
          this.updated = response.data.updated;
        });
    },
  },
  components: {
    navBar: NavBar,
    regularOldCard: RegularOldCard,
  },
  created() {
    this.get_bogs();
  },
};
</script>

<style scoped>
.blog {
  padding-left: 1rem;
  padding-right: 1rem;
}
</style>
