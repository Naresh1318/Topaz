<template>
  <div id="blogViewer">
    <v-content>
      <v-container>
        <v-progress-linear :active="loading" :indeterminate="loading"
                           absolute top color="black accent-4">
        </v-progress-linear>
        <v-row>
          <v-col xs="12">
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
      file_type: 0,
    };
  },
  computed: {
    render_markdown() {
      this.converter.setFlavor('github');
      return this.converter.makeHtml(this.markdown_content);
    },
  },
  methods: {
    get_markdown() {
      this.$http.get(`${this.$backend_address}/markdown_content`, {
        params: {
          path: this.page,
          file_type: this.file_type,
        },
        withCredentials: true,
      })
        .then((response) => {
          this.loading = false;
          this.markdown_content = response.data.markdown;
        });
    },
  },
  created() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if (urlParams.has('page') && urlParams.has('file_type')) {
      this.page = urlParams.get('page');
      this.file_type = urlParams.get('file_type');
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
