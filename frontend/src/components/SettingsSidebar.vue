<template>
  <v-navigation-drawer app :width="drawerWidth" class="resizable-drawer">
    <div class="drag-handle" @mousedown="startResize"></div>
    <!-- You can add navigation links here later -->
    <v-list-item title="Settings" subtitle="Click text to Edit" class="font-weight-bold">
      <template v-slot:append>
        <v-switch
          :model-value="isDarkTheme"
          hide-details
          inset
          label="Dark Mode"
          @update:modelValue="$emit('toggle-theme')"
        ></v-switch>
      </template>
    </v-list-item>
    <v-divider></v-divider>
    <v-expansion-panels v-model="panel">
      <document-viewer doc-name="cv" title="CV"></document-viewer>
      <document-viewer
        doc-name="job_description"
        title="Job Description"
      ></document-viewer>
      <document-viewer
        doc-name="role_description"
        title="Interviewer Style"
      ></document-viewer>
    </v-expansion-panels>
  </v-navigation-drawer>
</template>

<script>
import DocumentViewer from "./DocumentViewer.vue";

export default {
  name: "SettingsSidebar",
  props: {
    isDarkTheme: Boolean,
  },
  emits: ["toggle-theme"],
  components: {
    DocumentViewer,
  },
  data() {
    return {
      drawerWidth: 500, // Default width
      panel: 0, // Default open panel
    };
  },
  methods: {
    startResize(event) {
      event.preventDefault();
      document.addEventListener("mousemove", this.doResize);
      document.addEventListener("mouseup", this.stopResize);
    },
    doResize(event) {
      this.drawerWidth = event.clientX;
    },
    stopResize() {
      document.removeEventListener("mousemove", this.doResize);
      document.removeEventListener("mouseup", this.stopResize);
    },
  },
};
</script>

<style scoped>
.resizable-drawer {
  position: relative;
}

.drag-handle {
  position: absolute;
  top: 0;
  right: -5px;
  width: 10px;
  height: 100%;
  cursor: col-resize;
  z-index: 10;
}
</style>
