<template>
  <div class="analysis-container">
    <div class="analysis-window" v-if="showAnalysis">
        <v-card>
          <v-card-title>
            Analysis
            <v-spacer></v-spacer>
            <v-btn icon @click="showAnalysis = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text class="pa-5">
            <div v-if="content" class="analysis-content" v-html="renderedMarkdown"></div>
            <div v-else>No analysis exists yet.</div>
          </v-card-text>
        </v-card>
    </div>
    <v-btn
      class="analysis-bubble"
      fab
      dark
      large
      color="primary"
      @click="showAnalysis = !showAnalysis"
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
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.analysis-window {
  width: 600px;
  max-width: 90vw;
  margin-bottom: 16px;
}

.analysis-content {
  font-size: 1.2rem;
  line-height: 1.6;
  max-height: 60vh;
  overflow-y: auto;
}
</style>
