<template>
  <v-card>
    <v-card-title>Analysis</v-card-title>
    <v-card-text>
      <div v-html="renderedMarkdown"></div>
    </v-card-text>
  </v-card>
</template>

<script>
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt();

export default {
  name: 'AnalysisViewer',
  props: {
    content: {
      type: String,
      required: true,
    },
  },
  computed: {
    renderedMarkdown() {
      return md.render(this.content);
    },
  },
};
</script>

<style scoped>
/* Add any specific styles for the analysis viewer here */
</style>
