<template>
  <div id="editor">
    <v-content>
      <v-container>
        <v-progress-linear :active="loading" :indeterminate="loading"
                           absolute top color="black accent-4">
        </v-progress-linear>
        <v-row>
          <v-col>
            <h1>Editor</h1>
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
      markdown_content: '',
      converter: new showdown.Converter({
        extensions: [showdownHighlight],
      }),
      loading: true,
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
    get_markdown(page) {
      this.$http.get(`${this.$backend_address}/markdown_content`, {
        params: {
          path: page,
        },
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
    if (urlParams.has('page')) {
      this.get_markdown(urlParams.get('page'));
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
