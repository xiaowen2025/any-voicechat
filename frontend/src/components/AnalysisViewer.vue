<template>
  <div class="analysis-container">
    <v-dialog v-model="showAnalysis" max-width="800px" scrollable>
      <v-card>
        <v-card-title class="text-h5">
          Analysis
        </v-card-title>
        <v-btn absolute top right icon @click="showAnalysis = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-divider></v-divider>
        <v-card-text class="pa-5">
          <div v-if="content" class="analysis-content" v-html="renderedMarkdown"></div>
          <div v-else>No analysis exists yet.</div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-btn
      v-if="!showAnalysis"
      class="analysis-bubble"
      fab
      dark
      large
      color="primary"
      @click="showAnalysis = true"
    >
      <v-icon dark>mdi-chart-bubble</v-icon>
    </v-btn>
  </div>
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
  data() {
    return {
      showAnalysis: false,
    };
  },
  computed: {
    renderedMarkdown() {
      return md.render(this.content);
    },
  },
};
</script>

<style scoped>
.analysis-container {
  text-align: right;
  margin-top: 16px;
}

.analysis-content {
  font-size: 1.2rem;
  line-height: 1.6;
}
</style>
