<template>
  <div id="editor">
    <v-content>
      <v-container>
        <v-progress-linear :active="loading" :indeterminate="loading"
                           absolute top color="black accent-4">
        </v-progress-linear>
        <v-row>
          <v-col cols="9">
            <h1>Editor</h1>
            <p>{{ this.saved }}</p>
            <v-btn @click="save_file">Save</v-btn>
            <v-btn>Publish</v-btn>
          </v-col>
          <v-col>
            <v-btn href="/" color="dark" dark>Home</v-btn>
          </v-col>
          <v-col>
            <v-btn href="/logout" color="dark" dark>Logout</v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col md="6" xs="12">
            <textarea :value="markdown_content" @input="update"
                      style="width: 100%; height: 100%">
            </textarea>
          </v-col>
          <v-col md="6" xs="12">
            <div v-html="render_markdown" class="content_html"></div>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
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
      page: '',
      markdown_content: '',
      converter: new showdown.Converter({
        extensions: [showdownHighlight],
      }),
      loading: true,
      saved: false,
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
      this.saved = false;
    }, 300),
    get_markdown() {
      this.$http.get(`${this.$backend_address}/markdown_content`, {
        params: {
          path: this.page,
        },
      })
        .then((response) => {
          this.loading = false;
          this.markdown_content = response.data.markdown;
        });
    },
    start_file_saver() {
      window.setInterval(this.save_file, 60000);
    },
    save_file() {
      this.$http.post(`${this.$backend_address}/markdown_content`, {
        markdown: this.markdown_content,
      }, {
        params: {
          path: this.page,
        },
        withCredentials: true,
      })
        .then((response) => {
          if (response.status === 200) {
            this.saved = true;
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
    this.start_file_saver();
  },
};
</script>

<style>
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
