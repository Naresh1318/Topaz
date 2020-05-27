<template>
  <div class="blog">
    <nav-bar active_page="Blog"></nav-bar>
    <v-content>
      <v-container :style="main_content_css">
        <v-progress-linear :active="loading" indeterminate="loading"
                           absolute top color="black accent-4">
        </v-progress-linear>
        <div class="pa-1" v-for="blog in blogs" :key="blog.title">
          <v-divider></v-divider>
          <regular-old-card :title="blog.title" :description="blog.description"
                            :url="blog.url" :image_url="blog.image_url"></regular-old-card>
        </div>
      </v-container>
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
import mobile from '../js/utils';

export default {
  name: 'Blog',
  data() {
    return {
      page_name: 'Blog',
      blogs: [],
      updated: '',
      loading: true,
    };
  },
  methods: {
    get_bogs() {
      // Get all public repos
      this.$http.get(`${this.$backend_address}/blogs`)
        .then((response) => {
          this.loading = false;
          this.blogs = response.data.blogs;
          this.updated = response.data.updated;
        });
    },
  },
  computed: {
    main_content_css() {
      if (this.is_mobile) {
        return {
          paddingRight: '0rem',
          paddingLeft: '0rem',
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
    regularOldCard: RegularOldCard,
  },
  created() {
    this.get_bogs();
    if (mobile.isMobile()) {
      this.is_mobile = true;
    }
  },
};
</script>
