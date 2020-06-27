<template>
  <div class="home">
    <nav-bar active_page="Home"></nav-bar>
    <v-content>
      <v-app-bar v-if="show_app_bar()" color="#fff" light flat>
       <v-toolbar-title>Logged in as admin</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="open_editor('Home.md')">
          <v-icon>fa-edit</v-icon>
        </v-btn>
        <v-btn href="/logout" color="dark" dark>Logout</v-btn>
      </v-app-bar>
      <v-container :style="main_content_css">
        <v-progress-linear :active="loading" :indeterminate="loading"
                           absolute top color="black accent-4">
        </v-progress-linear>
        <v-row>
          <v-col md="4" xs="12" order-md="2">
            <v-card elevation="8"
                    style="border-radius: 4px; box-shadow: 0 0 50px 2px #e3dcdc !important;">
              <v-img height="300px" :src="profile_picture_url"></v-img>
            </v-card>
          </v-col>
          <v-col md="8" xs="12" order-md="1">
            <div class="content_html" id="content_html"></div>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
    <div v-if="this.is_mobile">
      <footer-comp></footer-comp>
    </div>
  </div>
</template>
<script>
import showdown from 'showdown';
import showdownHighlight from 'showdown-highlight';
import NavBar from '../components/NavBar.vue';
import mobile from '../js/utils';
import Footer from '../components/Footer.vue';

export default {
  name: 'Home',
  data() {
    return {
      drawer: false,
      page_name: 'Home',
      markdown_content: null,
      profile_picture_url: '',
      loading: true,
      is_admin: false,
    };
  },
  methods: {
    render_markdown() {
      const converter = new showdown.Converter({
        extensions: [showdownHighlight],
      });
      converter.setFlavor('github');
      const contentElement = document.getElementById('content_html');
      contentElement.innerHTML = converter.makeHtml(this.markdown_content);
    },
    get_n_render_markdown() {
      this.$http.get(`${this.$backend_address}/markdown_content`, {
        params: {
          path: 'Home.md',
          file_type: 0,
        },
      })
        .then((response) => {
          this.loading = false;
          this.markdown_content = response.data.markdown;
          this.render_markdown();
        });
    },
    get_theme() {
      this.$http.get(`${this.$backend_address}/theme`)
        .then((response) => {
          this.profile_picture_url = response.data.theme.profile_picture_url;
        });
    },
    show_app_bar() {
      if (mobile.isMobile()) {
        return false;
      }
      return this.is_admin;
    },
    open_editor(page) {
      this.$router.push(`/editor?page=${page}`);
    },
  },
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
    footerComp: Footer,
  },
  created() {
    if (mobile.isMobile()) {
      this.is_mobile = true;
    }
    this.get_theme();
    this.$is_authenticated()
      .then((response) => {
        if (response.data.is_authenticated) {
          this.is_admin = true;
        }
      });
  },
  beforeMount() {
    this.get_n_render_markdown();
  },
};
</script>

<style>
#content_html a {
  text-decoration: underline;
  color: black;
}
</style>
