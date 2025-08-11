<template>
  <v-dialog :model-value="props.modelValue" @update:model-value="emit('update:modelValue', $event)" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Settings</span>
      </v-card-title>
      <v-card-text v-if="editableSettings">
        <v-text-field label="App Name" v-model="editableSettings.app_name"></v-text-field>
        <v-textarea label="Agent Description" v-model="editableSettings.agent_description"></v-textarea>
        <v-textarea label="Goal Description" v-model="editableSettings.goal_description"></v-textarea>
        <v-textarea label="Notes Taking Instruction" v-model="editableSettings.notes_taking_instruction"></v-textarea>
        <v-textarea label="Analyse Instruction" v-model="editableSettings.analyse_instruction"></v-textarea>

        <v-select
          label="Voice"
          v-model="editableSettings.voice_name"
          :items="['Puck', 'Leda']"
        ></v-select>

        <v-select
          label="Language Code"
          v-model="editableSettings.language_code"
          :items="languages"
          item-title="text"
          item-value="value"
        ></v-select>

      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" text @click="downloadSettings">Download Settings</v-btn>
        <v-spacer></v-spacer>
        <v-btn text @click="emit('update:modelValue', false)">Close</v-btn>
        <v-btn text @click="triggerFileUpload">Import Settings</v-btn>
        <input type="file" ref="fileInput" @change="handleFileUpload" accept=".json" style="display: none" />
        <v-btn color="primary" variant="elevated" @click="saveSettings">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useSettings } from '../composables/useSettings';
import { useSnackbar } from '../composables/useSnackbar';

const props = defineProps({
  modelValue: Boolean,
});

const emit = defineEmits(['update:modelValue']);

const { settings, updateSettings } = useSettings();
const { showSnackbar } = useSnackbar();
const editableSettings = ref(null);
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

watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    // When the dialog opens, clone the settings to a local ref for editing
    editableSettings.value = JSON.parse(JSON.stringify(settings.value));
    if (editableSettings.value && !editableSettings.value.language_code) {
        editableSettings.value.language_code = 'en-US';
    }
  }
});

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
      const currentSettings = settings.value || {};
      
      const finalSettings = { ...currentSettings, ...newSettings };
      finalSettings.context_dict = newSettings.context_dict || {};
      
      updateSettings(finalSettings);
      showSnackbar('Settings imported successfully.', 'success');
      emit('update:modelValue', false);
    } catch (error) {
      console.error('Error parsing JSON file:', error);
      showSnackbar('Error importing settings. Make sure the file is a valid JSON.', 'error');
    }
  };
  reader.readAsText(file);
}

function saveSettings() {
  if (editableSettings.value) {
    updateSettings(editableSettings.value);
    showSnackbar('Settings saved successfully.', 'success');
  }
  emit('update:modelValue', false);
}

function downloadSettings() {
  const blob = new Blob([JSON.stringify(settings.value, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'settings.json';
  a.click();
  URL.revokeObjectURL(url);
  showSnackbar('Settings downloaded.', 'info');
}
</script>

<style scoped>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
