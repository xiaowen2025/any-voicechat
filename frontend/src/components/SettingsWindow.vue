<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Settings</span>
      </v-card-title>
      <v-card-text>
        <pre>{{ settingsJson }}</pre>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="$emit('update:modelValue', false)">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, onMounted, computed } from 'vue';

export default {
  name: 'SettingsWindow',
  props: {
    modelValue: Boolean,
  },
  emits: ['update:modelValue'],
  setup() {
    const settings = ref({});

    async function loadSettings() {
      try {
        const response = await fetch('/api/settings');
        const data = await response.json();
        if (response.ok) {
          settings.value = data;
        } else {
          console.error('Error fetching settings:', data.error);
        }
      } catch (error) {
        console.error('Error fetching settings:', error);
      }
    }

    onMounted(loadSettings);

    const settingsJson = computed(() => {
      return JSON.stringify(settings.value, null, 2);
    });

    return {
      settings,
      settingsJson,
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
