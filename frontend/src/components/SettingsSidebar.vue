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
    <v-list-item class="my-4 py-5">
      <span class="font-weight-bold text-h4">Settings</span>
    </v-list-item>
    <v-divider></v-divider>
    <v-expansion-panels v-model="panel" multiple>
      <document-viewer
        v-for="(item, name, index) in context"
        :key="name"
        :doc-name="name"
        :title="formatTitle(name)"
        :content="item.value || item.default_value"
        @update:content="updateContext(name, $event)"
      ></document-viewer>
    </v-expansion-panels>
    <template v-slot:append>
      <v-container>
        <v-divider class="mb-4"></v-divider>
        <v-row align="center">
          <v-col>
            <v-select
              :model-value="selectedTheme"
              :items="themeNames"
              label="Theme"
              dense
              outlined
              hide-details
              @update:model-value="$emit('theme-changed', $event)"
            ></v-select>
          </v-col>
          <v-col>
            <v-switch
              :model-value="isDarkMode"
              @update:model-value="$emit('dark-mode-toggled', $event)"
              label="Dark Mode"
              hide-details
            ></v-switch>
          </v-col>
        </v-row>
      </v-container>
      <v-container>
        <gemini-api-key-manager
          :gemini-api-key="geminiApiKey"
          :api-key-edited="apiKeyEdited"
          @update:gemini-api-key="geminiApiKey = $event"
          @update:api-key-edited="apiKeyEdited = $event"
          @save-api-key="saveGeminiApiKey"
        ></gemini-api-key-manager>
      </v-container>
    </template>
  </v-navigation-drawer>
</template>

<script>
import DocumentViewer from "./DocumentViewer.vue";
import GeminiApiKeyManager from "./GeminiApiKeyManager.vue";
import { themes } from '../themes';
import { useApi } from '../composables/useApi';
import { useResizableDrawer } from '../composables/useResizableDrawer';
import { onMounted, ref } from 'vue';

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
    GeminiApiKeyManager,
  },
  setup(props, { emit }) {
    const { context, loadContext, updateContext, saveGeminiApiKey: saveKey } = useApi();
    const { drawerWidth, startResize } = useResizableDrawer(500);
    
    const panel = ref([]);
    const geminiApiKey = ref("");
    const apiKeyEdited = ref(false);

    const themeNames = Object.keys(themes);

    function formatTitle(name) {
      if (!name) return '';
      const words = name.split('_');
      return words.map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }

    async function saveGeminiApiKey() {
      const success = await saveKey(geminiApiKey.value);
      if (success) {
        emit('api-key-updated', !!geminiApiKey.value);
        apiKeyEdited.value = false;
      } else {
        geminiApiKey.value = '';
      }
    }

    onMounted(async () => {
      geminiApiKey.value = localStorage.getItem("geminiApiKey") || "";
      apiKeyEdited.value = !geminiApiKey.value;
      if (geminiApiKey.value) {
        emit('api-key-updated', true);
      }
      await loadContext();
      panel.value = Object.keys(context.value).map((_, index) => index);
    });

    return {
      drawerWidth,
      panel,
      geminiApiKey,
      apiKeyEdited,
      context,
      themeNames,
      formatTitle,
      startResize,
      saveGeminiApiKey,
      updateContext,
    };
  }
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