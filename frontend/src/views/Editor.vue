<template>
  <div id="editor">
    <v-content>
      <v-container>
        <v-progress-linear :active="loading" :indeterminate="loading"
                           absolute top color="black accent-4">
        </v-progress-linear>
        <v-row justify="space-between">
          <v-col>
            <h1>Editor</h1>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            Last saved: {{ last_saved }}
          </v-col>
        </v-row>
        <v-row justify="space-between">
          <v-col md="2">
            <v-row no-gutters>
              <v-col>
                <v-btn href="/" icon> <v-icon> home </v-icon> </v-btn>
              </v-col>
              <v-col>
                <v-btn @click="set_markdown" icon> <v-icon> save </v-icon> </v-btn>
              </v-col>
            </v-row>
          </v-col>
          <v-col md="4">
            <v-row no-gutters>
              <v-col>
                <v-btn @click="publish"> Publish <v-icon> check_circle </v-icon> </v-btn>
              </v-col>
              <v-col>
                <v-btn @click="unpublish"> Unpublish <v-icon> unpublished </v-icon> </v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row>
          <v-col md="6" xs="12" style="height: 75vh">
            <textarea :value="markdown_content" @input="update"
                      style="width: 100%; height: 100%">
            </textarea>
          </v-col>
          <v-col md="6" xs="12" style="height: 75vh">
            <div v-html="render_markdown" class="content_html"></div>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
    <v-snackbar v-model="show_alert">
      {{ alert_msg }} <v-btn color="#fff" text @click="show_alert=false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import showdown from 'showdown';
import showdownHighlight from 'showdown-highlight';
import loadsh from 'loadsh';

export default {
  name: 'Editor',
  data() {
    return {
      markdown_content: '',
      converter: new showdown.Converter({
        extensions: [showdownHighlight],
      }),
      loading: true,
      show_alert: false,
      alert_msg: '',
      page: '',
      last_saved: '',
    };
  },
  computed: {
    render_markdown() {
      this.converter.setFlavor('github');
      return this.converter.makeHtml(this.markdown_content);
    },
  },
  methods: {
    // eslint-disable-next-line func-names
    update: loadsh.debounce(function (e) {
      this.markdown_content = e.target.value;
    }, 300),
    get_markdown() {
      this.$http.get(`${this.$backend_address}/markdown_content`, {
        params: {
          path: this.page,
          file_type: 1,
        },
        withCredentials: true,
      })
        .then((response) => {
          this.loading = false;
          this.markdown_content = response.data.markdown;
        });
    },
    set_markdown() {
      this.$http.post(`${this.$backend_address}/markdown_content`, {
        markdown: this.markdown_content,
      }, {
        withCredentials: true,
        params: {
          path: this.page,
          file_type: 1,
        },
      })
        .then((response) => {
          if (response.data.INFO) {
            this.last_saved = response.data.time;
          } else {
            this.last_saved = 'unable to save';
            this.show_alert = true;
            this.alert_msg = 'unable to save';
          }
        });
    },
    publish() {
      this.$http.get(`${this.$backend_address}/publish`, {
        withCredentials: true,
        params: {
          path: this.page,
        },
      })
        .then((response) => {
          this.loading = false;
          if (response.data.INFO) {
            this.show_alert = true;
            this.alert_msg = response.data.INFO;
          }
        });
    },
    unpublish() {
      this.$http.get(`${this.$backend_address}/unpublish`, {
        withCredentials: true,
        params: {
          path: this.page,
        },
      })
        .then((response) => {
          this.loading = false;
          if (response.data.INFO) {
            this.show_alert = true;
            this.alert_msg = response.data.INFO;
          }
        });
    },
  },
  created() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if (urlParams.has('page')) {
      this.page = urlParams.get('page');
      this.get_markdown();
    } else {
      this.markdown_content = '';
    }
  },
};
</script>

<style scoped>
.content_html a {
  text-decoration: underline;
  color: black;
}

#editor textarea {
  border: none;
  resize: none;
  outline: none;
  background-color: #f6f6f6;
  font-size: 16px;
  padding: 20px;
}

</style>
