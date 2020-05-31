<template>
  <div>
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
        <v-col>
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
  name: 'GithubProjectSelector',
  data() {
    return {
      projects: [],
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
      show_alert: false,
      alert_text: '',
      item_visibility_text: {
        1: 'mdi-eye', 0: 'mdi-eye-off',
      },
    };
  },
  methods: {
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
            this.$emit('submitted');
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
  },
};
</script>

<style scoped>

</style>
