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
        <v-col cols="auto">
          <v-btn icon @click.stop="$emit('update:modelValue', false)" title="Close">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-list-item>
    <v-divider></v-divider>
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
      <div class="pa-2 d-flex justify-start align-center">
        <v-btn icon @click="$emit('toggle-settings')" title="Settings">
          <v-icon>mdi-cog</v-icon>
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import ContextViewer from "./ContextViewer.vue";
import { useSettings } from "../composables/useSettings";
import { useResizableDrawer } from "../composables/useResizableDrawer";
import { onMounted, ref, computed, watch } from "vue";

const props = defineProps({
  modelValue: Boolean,
  isMobile: Boolean,
});

defineEmits(["update:modelValue", "toggle-settings"]);

const { settings, updateSettings } = useSettings();
const context = computed(() => settings.value?.context_dict || {});
const { drawerWidth, startResize } = useResizableDrawer(500);

const panel = ref([]);

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
</style>
