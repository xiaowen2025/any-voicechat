<template>
  <v-navigation-drawer
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :width="isMobile ? '80%' : drawerWidth"
    :class="{ 'resizable-drawer': !isMobile }"
    :temporary="isMobile"
    app
  >
    <div
      v-if="!isMobile"
      class="drag-handle"
      @mousedown="startResize"
    ></div>
    <!-- You can add navigation links here later -->
    <v-list-item class="my-2">
      <v-row align="center" no-gutters>
        <v-col>
          <span class="font-weight-bold">Context</span>
        </v-col>
      </v-row>
    </v-list-item>
    <v-divider></v-divider>
    <v-list-item>
      <v-switch
        :model-value="searchToolEnabled"
        @update:model-value="toggleSearchTool"
        label="Enable Search Tool"
        color="primary"
      ></v-switch>
    </v-list-item>
    <v-expansion-panels v-model="panel" multiple>
      <context-viewer
        v-for="(item, name, index) in context"
        :key="name"
        :doc-name="name"
        :title="formatTitle(name)"
        :content="item.value || item.default_value"
        @update:content="updateContext(name, $event)"
      ></context-viewer>
    </v-expansion-panels>
    <template v-slot:append>
      <div class="pa-2">
        <v-row>
          <v-col>
            <v-btn icon @click="$emit('toggle-settings')" title="Settings">
              <v-icon>mdi-cog</v-icon>
            </v-btn>
          </v-col>
          <v-col class="d-flex justify-end">
            <v-btn icon @click.stop="$emit('update:modelValue', false)" title="Close">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import ContextViewer from "./ContextViewer.vue";
import { useSettingsStore } from "../stores/settings";
import { useResizableDrawer } from "../composables/useResizableDrawer";
import { onMounted, ref, computed, watch } from "vue";
import { storeToRefs } from "pinia";

const props = defineProps({
  modelValue: Boolean,
  isMobile: Boolean,
});

defineEmits(["update:modelValue", "toggle-settings"]);

const settingsStore = useSettingsStore();
const { settings } = storeToRefs(settingsStore);
const { updateSettings } = settingsStore;
const context = computed(() => settings.value?.context_dict || {});
const { drawerWidth, startResize } = useResizableDrawer(500);

const panel = ref([]);

const searchToolEnabled = computed(() => settings.value?.search_tool || false);

function toggleSearchTool(value) {
  const newSettings = { ...settings.value, search_tool: value };
  updateSettings(newSettings);
}

function formatTitle(name) {
  if (!name) return "";
  const words = name.split("_");
  return words
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function updateContext(name, content) {
  const newSettings = { ...settings.value };
  if (newSettings.context_dict && newSettings.context_dict[name]) {
    newSettings.context_dict[name].value = content;
    updateSettings(newSettings);
  }
}

function expandAllPanels() {
    if (context.value) {
        panel.value = Object.keys(context.value).map((_, index) => index);
    }
}

watch(() => props.isMobile, (newIsMobile) => {
    if (!newIsMobile) {
        expandAllPanels();
    }
});


onMounted(() => {
  if (context.value && !props.isMobile) {
    expandAllPanels();
  }
});
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

:deep(.v-list-item-title),
:deep(.v-label),
:deep(.v-expansion-panel-title__text) {
  font-size: 1.1rem !important;
}

.font-weight-bold {
    font-size: 1.2rem !important;
}
</style>
