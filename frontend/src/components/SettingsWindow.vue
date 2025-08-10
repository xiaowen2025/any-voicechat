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

export default {
  name: 'SettingsWindow',
  props: {
    modelValue: Boolean,
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const settings = ref({});
    const editableSettings = ref('');

    async function loadSettings() {
      try {
        const response = await fetch('/api/settings');
        const data = await response.json();
        if (response.ok) {
          settings.value = data;
          editableSettings.value = JSON.stringify(data, null, 2);
        } else {
          console.error('Error fetching settings:', data.error);
        }
      } catch (error) {
        console.error('Error fetching settings:', error);
      }
    }

    async function saveSettings() {
      try {
        const response = await fetch('/api/settings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: editableSettings.value,
        });
        const data = await response.json();
        if (response.ok) {
          settings.value = JSON.parse(editableSettings.value);
          emit('update:modelValue', false);
          window.location.reload();
        } else {
          console.error('Error saving settings:', data.error);
        }
      } catch (error) {
        console.error('Error saving settings:', error);
      }
    }

    onMounted(loadSettings);

    watch(() => props.modelValue, (newValue) => {
      if (newValue) {
        loadSettings();
      }
    });

    return {
      editableSettings,
      saveSettings,
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
