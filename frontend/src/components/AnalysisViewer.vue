<template>
  <div class="analysis-container">
    <v-navigation-drawer
      v-model="showAnalysis"
      location="right"
      temporary
      :width="drawerWidth"
      class="analysis-sidebar"
    >
      <div
        class="resize-handle"
        @mousedown.prevent="startResize"
      ></div>
      <div style="margin-left: 10px;">
        <div class="d-flex align-center pa-2">
          <span class="text-h5 pl-2">Analysis</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="showAnalysis = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <v-divider></v-divider>
        <div class="pa-5" style="height: calc(100% - 57px); overflow-y: auto;">
          <div v-if="content" class="analysis-content" v-html="renderedMarkdown"></div>
          <div v-else>No analysis exists yet.</div>
        </div>
      </div>
    </v-navigation-drawer>

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
      drawerWidth: 500,
      isResizing: false,
    };
  },
  computed: {
    renderedMarkdown() {
      return md.render(this.content);
    },
  },
  methods: {
    startResize(event) {
      this.isResizing = true;
      document.addEventListener('mousemove', this.resize);
      document.addEventListener('mouseup', this.stopResize);
    },
    resize(event) {
      if (this.isResizing) {
        this.drawerWidth = window.innerWidth - event.clientX;
      }
    },
    stopResize() {
      this.isResizing = false;
      document.removeEventListener('mousemove', this.resize);
      document.removeEventListener('mouseup', this.stopResize);
    },
  },
};
</script>

<style scoped>
.analysis-bubble {
  position: fixed;
  right: 32px;
}

.analysis-container {
  text-align: left;
  margin-top: 16px;
}

.analysis-content {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-left: 16px;
  padding-left: 16px;
}

.analysis-sidebar {
  max-width: 90vw;
  min-width: 300px !important;
}

.resize-handle {
  position: absolute;
  top: 0;
  left: 0;
  width: 10px;
  height: 100%;
  cursor: col-resize;
  z-index: 10;
  transition: background-color 0.2s ease-in-out;
}

.resize-handle:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
