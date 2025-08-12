<template>
  <v-dialog :model-value="props.modelValue" @update:model-value="emit('update:modelValue', $event)" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Settings</span>
      </v-card-title>
      <v-card-text v-if="editableSettings">
        <v-tabs v-model="tab" background-color="primary" dark>
          <v-tab value="appAgent">App & Agent</v-tab>
          <v-tab value="general">General</v-tab>
        </v-tabs>
        <v-window v-model="tab">
          <v-window-item value="appAgent">
            <v-container>
              <v-text-field label="App Name" v-model="editableSettings.app_name"></v-text-field>
              <v-textarea label="Agent Description" v-model="editableSettings.agent_description"></v-textarea>
              <v-textarea label="Goal Description" v-model="editableSettings.goal_description"></v-textarea>
              <v-textarea label="Notes Taking Instruction" v-model="editableSettings.notes_taking_instruction"></v-textarea>
              <v-textarea label="Analyse Instruction" v-model="editableSettings.analyse_instruction"></v-textarea>
              <v-select label="Voice" v-model="editableSettings.voice_name" :items="['Puck', 'Leda']"></v-select>
              <v-select label="Language Code" v-model="editableSettings.language_code" :items="languages" item-title="text" item-value="value"></v-select>
            </v-container>
          </v-window-item>
          <v-window-item value="general">
            <v-container>
              <v-row align="center">
                <v-col>
                  <v-select
                    :model-value="selectedTheme"
                    :items="themeNames"
                    label="Theme"
                    dense
                    outlined
                    hide-details
                    @update:model-value="emit('theme-changed', $event)"
                  ></v-select>
                </v-col>
                <v-col>
                  <v-switch
                    :model-value="isDarkMode"
                    @update:model-value="emit('dark-mode-toggled', $event)"
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
          </v-window-item>
        </v-window>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" text @click="copySettings">Copy Settings</v-btn>
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
import { ref, watch, onMounted } from 'vue';
import { useSettings } from '../composables/useSettings';
import { useSnackbar } from '../composables/useSnackbar';
import GeminiApiKeyManager from "./GeminiApiKeyManager.vue";
import { themes } from "../themes";
import { useApi } from "../composables/useApi";

const props = defineProps({
  modelValue: Boolean,
  selectedTheme: String,
  isDarkMode: Boolean,
});

const emit = defineEmits(['update:modelValue', 'api-key-updated', 'theme-changed', 'dark-mode-toggled']);

const { settings, updateSettings } = useSettings();
const { showSnackbar } = useSnackbar();
const { saveGeminiApiKey: saveKey } = useApi();

const editableSettings = ref(null);
const fileInput = ref(null);
const tab = ref('appAgent');
const geminiApiKey = ref("");
const apiKeyEdited = ref(false);
const themeNames = Object.keys(themes);

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
  if (!file) return;

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

function copySettings() {
  const settingsJson = JSON.stringify(settings.value, null, 2);
  navigator.clipboard.writeText(settingsJson).then(() => {
    showSnackbar('Settings copied to clipboard.', 'info');
  }).catch(err => {
    console.error('Could not copy text: ', err);
    showSnackbar('Failed to copy settings.', 'error');
  });
}

async function saveGeminiApiKey() {
  const success = await saveKey(geminiApiKey.value);
  if (success) {
    emit("api-key-updated", !!geminiApiKey.value);
    apiKeyEdited.value = false;
  } else {
    geminiApiKey.value = "";
  }
}

onMounted(() => {
  geminiApiKey.value = localStorage.getItem("geminiApiKey") || "";
  apiKeyEdited.value = !geminiApiKey.value;
  if (geminiApiKey.value) {
    emit("api-key-updated", true);
  }
});
</script>

<style scoped>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
