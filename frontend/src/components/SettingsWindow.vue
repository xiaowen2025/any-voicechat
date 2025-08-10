<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Settings</span>
      </v-card-title>
      <v-card-text v-if="settings">
        <v-text-field label="App Name" v-model="settings.app_name"></v-text-field>
        <v-textarea label="Agent Description" v-model="settings.agent_description"></v-textarea>
        <v-textarea label="Goal Description" v-model="settings.goal_description"></v-textarea>
        <v-textarea label="Notes Taking Instruction" v-model="settings.notes_taking_instruction"></v-textarea>
        <v-textarea label="Analyse Instruction" v-model="settings.analyse_instruction"></v-textarea>

        <v-select
          label="Voice"
          v-model="settings.voice_name"
          :items="['Puck', 'Leda']"
        ></v-select>

        <v-select
          label="Language Code"
          v-model="settings.language_code"
          :items="languages"
          item-title="text"
          item-value="value"
        ></v-select>

      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="$emit('update:modelValue', false)">Close</v-btn>
        <v-btn color="blue darken-1" text @click="triggerFileUpload">Upload JSON</v-btn>
        <input type="file" ref="fileInput" @change="handleFileUpload" accept=".json" style="display: none" />
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
    const settings = ref(null);
    const fileInput = ref(null);
    const languages = ref([
        { text: 'English (US)', value: 'en-US' },
        { text: 'Chinese (Simplified)', value: 'zh-CN' },
        { text: 'German', value: 'de-DE' },
        { text: 'French', value: 'fr-FR' },
        { text: 'Hindi', value: 'hi-IN' },
        { text: 'Japanese', value: 'ja-JP' },
        { text: 'Spanish', value: 'es-ES' },
        { text: 'Portuguese', value: 'pt-BR' },
        { text: 'Russian', value: 'ru-RU' },
    ]);

    function triggerFileUpload() {
      fileInput.value.click();
    }

    function handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) {
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const newSettings = JSON.parse(e.target.result);
          settings.value = { ...settings.value, ...newSettings };
          saveSettings();
        } catch (error) {
          console.error('Error parsing JSON file:', error);
        }
      };
      reader.readAsText(file);
    }

    async function loadSettings() {
      try {
        const response = await fetch('/api/settings');
        const data = await response.json();
        if (response.ok) {
          settings.value = data;
          if (!settings.value.language_code) {
            settings.value.language_code = 'en-US';
          }
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
          body: JSON.stringify(settings.value),
        });
        const data = await response.json();
        if (response.ok) {
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
      settings,
      saveSettings,
      languages,
      fileInput,
      triggerFileUpload,
      handleFileUpload,
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
