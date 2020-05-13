<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="11">
          <h1> Logged in as admin! </h1>
        </v-col>
        <v-col cols="1">
          <v-btn href="/logout" color="dark" dark>Logout</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card class="rounded-card">
            <v-card-title>Add blog from other sources</v-card-title>
            <v-card-text>
              <v-row>
                <v-col>
                  <v-text-field v-model="title" label="Title" required color="dark"></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-textarea v-model="description" label="Description"
                              required color="dark"></v-textarea>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field v-model="url" label="URL" required color="dark"></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field v-model="time_stamp" label="Label Text" type="date" required
                                color="dark"></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field v-model="image_url" label="Image URL"
                                required color="dark"></v-text-field>

                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-btn @click="submit_entry()" color="dark" dark>Submit</v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row justify="center" style="margin-top: 2rem" no-gutters>
        <v-col lg="4">
          <h2>Projects</h2>
        </v-col>
        <v-col lg="4">
          <v-text-field v-model="search" label="Search" single-line hide-details></v-text-field>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col lg="10">
          <v-data-table :headers="projects_header" :items="projects" :search="search">
            <template v-slot:item.visibility="{ item }">
              <v-icon small class="mr-2" @click="toggle_visibility(item)">
                {{ item_visibility_text[item.visible] }}
              </v-icon>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar v-model="show_alert"> {{ alert_text }}
      <v-btn color="#fff" text @click="show_alert=false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  name: 'Admin',
  data() {
    return {
      projects: [],
      selected_projects: [],
      search: '',
      projects_header:
        [
          {
            text: 'Title', align: 'left', sorted: false, value: 'title',
          },
          {
            text: 'Url', value: 'url',
          },
          {
            text: 'Primary language', value: 'primary_language',
          },
          {
            text: 'Stars', value: 'stars',
          },
          {
            text: 'Timestamp', value: 'timestamp',
          },
          {
            text: 'Visibility', value: 'visibility',
          },
        ],
      blogs: [],
      publications: [],
      title: '',
      description: '',
      url: '',
      image_url: '',
      time_stamp: '',
      type: 'blog',
      show_alert: false,
      alert_text: '',
      item_visibility_text: {
        1: 'mdi-eye', 0: 'mdi-eye-off',
      },
    };
  },
  methods: {
    /**
     * Try submitting entry
     */
    submit_entry() {
      if (this.type === '') {
        this.alert_text = 'Fill all entries';
        this.show_alert = true;
      }
      this.$http.post(`${this.$backend_address}/${this.type}s`, {
        title: this.title,
        description: this.description,
        url: this.url,
        image_url: this.image_url,
        time_stamp: this.time_stamp,
      }, {
        withCredentials: true,
      })
        .then((response) => {
          if (response.data.INFO) {
            this.alert_text = response.data.INFO;
            this.show_alert = true;
          }
        });
    },

    card_width() {
      if (this.is_mobile()) return '90%';
      return '40%';
    },
    /**
     * Get all repos and set this.projects and this.latest_project
     */
    get_repos() {
      // Get all public repos
      this.$http.get(`${this.$backend_address}/public_repos`)
        .then((response) => {
          this.projects = response.data.repos;
          this.updated = response.data.updated;
        });
    },
    /**
     * Get all blogs and set this.blogs
     */
    get_blogs() {
      // Get all blogs
      this.$http.get(`${this.$backend_address}/blogs`)
        .then((response) => {
          this.blogs = response.data.blogs;
        });
    },
    /**
     * Get all publications and set this.publications
     */
    get_publications() {
      // Get all publications
      this.$http.get(`${this.$backend_address}/publications`)
        .then((response) => {
          this.publications = response.data.publications;
        });
    },
    /**
     * Send a POST request to update visibility
     * @param projects, list of projects to update
     */
    send_selection(projects) {
      if (projects === []) {
        this.alert_text = 'Nothing selected';
        this.show_alert = true;
      }
      this.$http.post(`${this.$backend_address}/public_repos`, {
        projects,
      }, {
        withCredentials: true,
      })
        .then((response) => {
          if (response.data.INFO) {
            this.alert_text = response.data.INFO;
            this.show_alert = true;
          }
        });
    },
    /**
     * Toggle visibility of project and send a post request to the backend
     * @param item, project object
     */
    toggle_visibility(item) {
      if (item.visible === 1) {
        // eslint-disable-next-line no-param-reassign
        item.visible = 0;
      } else {
        // eslint-disable-next-line no-param-reassign
        item.visible = 1;
      }
      this.send_selection([item]);
    },
  },
  created() {
    this.get_repos();
    this.get_blogs();
    this.get_publications();
  },
};
</script>

<style scoped>

</style>
