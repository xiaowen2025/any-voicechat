<template>
  <v-card>
    <v-card-title>Analysis</v-card-title>
    <v-card-text class="pa-5">
      <div class="analysis-content" v-html="renderedMarkdown"></div>
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
.analysis-content {
  font-size: 1.2rem;
  line-height: 1.6;
}
</style>
