<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Settings</span>
      </v-card-title>
      <v-card-text>
        <v-textarea
          v-model="editableSettings"
          auto-grow
          rows="15"
        ></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="$emit('update:modelValue', false)">Close</v-btn>
        <v-btn color="blue darken-1" text @click="saveSettings">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useSettings } from '../composables/useSettings';

export default {
  name: 'SettingsWindow',
  props: {
    modelValue: Boolean,
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const { settings, loadSettings, saveSettings } = useSettings();
    const editableSettings = ref('');

    function load() {
      const currentSettings = loadSettings();
      editableSettings.value = JSON.stringify(currentSettings, null, 2);
    }

    function saveSettingsLocal() {
      try {
        const newSettings = JSON.parse(editableSettings.value);
        saveSettings(newSettings);
        emit('update:modelValue', false);
        window.location.reload();
      } catch (error) {
        console.error('Error parsing settings:', error);
        alert('Error parsing settings: Please ensure it is valid JSON.');
      }
    }

    onMounted(load);

    watch(() => props.modelValue, (newValue) => {
      if (newValue) {
        load();
      }
    });

    return {
      editableSettings,
      saveSettings: saveSettingsLocal,
    };
  },
};
</script>

<style scoped>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
