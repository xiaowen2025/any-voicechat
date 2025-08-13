<template>
  <v-navigation-drawer
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :width="drawerWidth"
    :class="{ 'resizable-drawer': !isMobile }"
    app
  >
    <div
      v-if="!isMobile"
      class="drag-handle"
      @mousedown="startResize"
    ></div>
    <!-- You can add navigation links here later -->
    <v-list-item class="my-2">
      <v-row align="center">
        <v-col>
          <span class="font-weight-bold">Context</span>
        </v-col>
        <v-col class="d-flex justify-end">
          <v-btn icon @click="$emit('toggle-settings')" title="Settings">
            <v-icon>mdi-cog</v-icon>
          </v-btn>
        </v-col>
      </v-row>
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
  </v-navigation-drawer>
</template>

<script>
import DocumentViewer from "./DocumentViewer.vue";
import { useSettings } from "../composables/useSettings";
import { useResizableDrawer } from "../composables/useResizableDrawer";
import { onMounted, ref, computed } from "vue";

export default {
  name: "SettingsSidebar",
  props: {
    modelValue: Boolean,
  },
  emits: ["update:modelValue", "toggle-settings"],
  components: {
    DocumentViewer,
  },
  setup(props, { emit }) {
    const { settings, updateSettings } = useSettings();
    const context = computed(() => settings.value?.context_dict || {});
    const { drawerWidth, startResize, isMobile } = useResizableDrawer(500);

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

    onMounted(() => {
      if (context.value) {
        panel.value = Object.keys(context.value).map((_, index) => index);
      }
    });

    return {
      drawerWidth,
      panel,
      context,
      formatTitle,
      startResize,
      updateContext,
      isMobile,
    };
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
