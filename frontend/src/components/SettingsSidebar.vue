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
    <v-container>
      <v-text-field
        v-model="geminiApiKey"
        :type="showGeminiApiKey ? 'text' : 'password'"
        label="Gemini API Key"
        outlined
        dense
        class="mb-2"
        @focus="apiKeyEdited = true"
      >
        <template v-slot:append>
          <v-icon @click="showGeminiApiKey = !showGeminiApiKey">
            {{ showGeminiApiKey ? 'mdi-eye-off' : 'mdi-eye' }}
          </v-icon>
        </template>
      </v-text-field>
      <v-btn v-if="apiKeyEdited" @click="saveGeminiApiKey" class="mb-4 fancy-btn" size="large" rounded="lg">Save API Key</v-btn>
    </v-container>
    <v-divider></v-divider>
    <v-expansion-panels v-model="panel">
      <document-viewer
        doc-name="cv"
        title="CV"
        :content="cvContent"
        @update:content="cvContent = $event"
      ></document-viewer>
      <document-viewer
        doc-name="job_description"
        title="Job Description"
        :content="jobDescriptionContent"
        @update:content="jobDescriptionContent = $event"
      ></document-viewer>
      <document-viewer
        doc-name="role_description"
        title="Interviewer Style"
        :content="roleDescriptionContent"
        @update:content="roleDescriptionContent = $event"
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
  emits: ["toggle-theme", "api-key-updated"],
  components: {
    DocumentViewer,
  },
  data() {
    return {
      drawerWidth: 500, // Default width
      panel: 0, // Default open panel
      geminiApiKey: "",
      showGeminiApiKey: false,
      apiKeyEdited: false,
      cvContent: "",
      jobDescriptionContent: "",
      roleDescriptionContent: "",
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
    async saveGeminiApiKey() {
      try {
        const response = await fetch('/api/verify_api_key', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ key: this.geminiApiKey }),
        });
        const result = await response.json();
        if (result.status === 'success') {
          localStorage.setItem('geminiApiKey', this.geminiApiKey);
          this.$emit('api-key-updated', !!this.geminiApiKey);
          this.apiKeyEdited = false;
          alert('API Key saved successfully!');
        } else {
          this.geminiApiKey = '';
          localStorage.removeItem('geminiApiKey');
          this.$emit('api-key-updated', false);
          alert(`API Key is invalid: ${result.message}`);
        }
      } catch (error) {
        alert(`Error verifying API key: ${error}`);
      }
    },
    async fetchDocument(docName) {
      try {
        const response = await fetch(`/api/documents/${docName}`);
        const data = await response.json();
        if (response.ok) {
          return data.content;
        } else {
          return `Error: ${data.error}`;
        }
      } catch (error) {
        console.error(error);
        return 'Error fetching document.';
      }
    },
    async loadAllDocuments() {
      this.cvContent = await this.fetchDocument("cv");
      this.jobDescriptionContent = await this.fetchDocument("job_description");
      this.roleDescriptionContent = await this.fetchDocument("role_description");
    },
  },
  mounted() {
    this.geminiApiKey = localStorage.getItem("geminiApiKey") || "";
    this.apiKeyEdited = !this.geminiApiKey;
    this.loadAllDocuments();
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

.fancy-btn {
  background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
  color: white;
  box-shadow: 0 3px 5px 2px rgba(255, 105, 135, .3);
}
</style>