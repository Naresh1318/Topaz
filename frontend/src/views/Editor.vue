<template>
  <div id="editor">
    <h1>Editor</h1>
    <textarea :value="markdown_content" @input="update"></textarea>
    <div v-html="render_markdown"></div>
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
  },
};
</script>

<style scoped>

</style>
