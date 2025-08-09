<template>
  <v-navigation-drawer
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    app
    :width="drawerWidth"
    class="resizable-drawer"
  >
    <div class="drag-handle" @mousedown="startResize"></div>
    <!-- You can add navigation links here later -->
    <v-list-item title="Settings" subtitle="Click text to Edit" class="font-weight-bold">
      <template v-slot:append>
        <v-switch
          :model-value="isDarkMode"
          @update:model-value="$emit('dark-mode-toggled', $event)"
          label="Dark Mode"
        ></v-switch>
        <v-select
          :model-value="selectedTheme"
          :items="themeNames"
          label="Theme"
          dense
          outlined
          hide-details
          @update:model-value="$emit('theme-changed', $event)"
        ></v-select>
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
        v-for="(item, name) in context"
        :key="name"
        :doc-name="name"
        :title="formatTitle(name)"
        :content="item.value || item.default_value"
        @update:content="updateContext(name, $event)"
      ></document-viewer>
    </v-expansion-panels>
  </v-navigation-drawer>
</template>

<script>
import DocumentViewer from "./DocumentViewer.vue";
import { themes } from '../themes';

export default {
  name: "SettingsSidebar",
  props: {
    modelValue: Boolean,
    selectedTheme: String,
    isDarkMode: Boolean,
  },
  emits: ["update:modelValue", "api-key-updated", "theme-changed", "dark-mode-toggled"],
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
      context: {},
    };
  },
  computed: {
    themeNames() {
      return Object.keys(themes);
    }
  },
  methods: {
    formatTitle(name) {
      if (!name) return '';
      const words = name.split('_');
      return words.map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
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
          alert(`API Key is invalid: ${result.message}`);
        }
      } catch (error) {
        alert(`Error verifying API key: ${error}`);
      }
    },
    async loadContext() {
      try {
        const response = await fetch('/api/context');
        const data = await response.json();
        if (response.ok) {
          this.context = data;
        } else {
          console.error('Error fetching context:', data.error);
        }
      } catch (error) {
        console.error('Error fetching context:', error);
      }
    },
    async updateContext(contextName, content) {
      try {
        const response = await fetch(`/api/context/${contextName}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ value: content }),
        });
        const result = await response.json();
        if (response.ok) {
          console.log(`Context '${contextName}' updated.`);
          if (this.context[contextName]) {
              this.context[contextName].value = content;
          }
        } else {
          alert(`Error updating context: ${result.error}`);
        }
      } catch (error) {
        alert(`Error updating context: ${error}`);
      }
    }
  },
  mounted() {
    this.geminiApiKey = localStorage.getItem("geminiApiKey") || "";
    this.apiKeyEdited = !this.geminiApiKey;
    this.loadContext();
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
  background: linear-gradient(45deg, #972408 30%, #fa9256 90%);
  color: white !important;
  box-shadow: 0 3px 5px 2px rgba(255, 105, 135, .3);
}
</style>