<template>
  <v-dialog
    :model-value="props.modelValue"
    @update:model-value="emit('update:modelValue', $event)"
    max-width="600px"
    :fullscreen="isMobile"
  >
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
              <v-textarea label="Analyse Instruction" v-model="editableSettings.analyse_instruction"></v-textarea>
              <v-select
                label="Voice"
                v-model="editableSettings.voice_name"
                :items="voices"
                item-title="name"
                item-value="name"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props" :subtitle="item.raw.description"></v-list-item>
                </template>
              </v-select>
              <v-select label="Language Code" v-model="editableSettings.language_code" :items="languages" item-title="text" item-value="value"></v-select>
            </v-container>
          </v-window-item>
          <v-window-item value="general">
            <v-container>
              <v-row align="center">
                <v-col>
                  <v-select
                    :model-value="currentTheme"
                    :items="themeNames"
                    label="Theme"
                    dense
                    outlined
                    hide-details
                    @update:model-value="setTheme(theme, $event)"
                  ></v-select>
                </v-col>
                <v-col>
                  <v-switch
                    :model-value="darkMode"
                    @update:model-value="setDarkMode(theme, $event)"
                    label="Dark Mode"
                    hide-details
                  ></v-switch>
                </v-col>
              </v-row>
            </v-container>
            <v-container>
              <v-text-field
                v-model="geminiApiKey"
                :type="showGeminiApiKey ? 'text' : 'password'"
                label="Gemini API Key"
                outlined
                dense
                class="mb-2"
                @focus="apiKeyEdited = true"
              >
                <template v-slot:append-inner>
                  <v-icon @click="showGeminiApiKey = !showGeminiApiKey">
                    {{ showGeminiApiKey ? 'mdi-eye-off' : 'mdi-eye' }}
                  </v-icon>
                </template>
              </v-text-field>
              <v-btn v-if="apiKeyEdited" @click="saveGeminiApiKey" class="mb-4" size="large" rounded="lg">Save API Key</v-btn>
            </v-container>
            <v-container>
              <v-list>
                <v-list-item
                  prepend-icon="mdi-github"
                  title="Check on GitHub"
                  href="https://github.com/xiaowen2025/Vox-Hub"
                  target="_blank"
                ></v-list-item>
              </v-list>
            </v-container>
          </v-window-item>
        </v-window>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="emit('update:modelValue', false)">Close</v-btn>
        <v-spacer></v-spacer>
        <v-menu location="top">
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" text ref="moreButton">More</v-btn>
          </template>
          <v-list>
            <v-list-item @click="copySettings">
              <v-list-item-title>Copy Settings</v-list-item-title>
            </v-list-item>
            <v-list-item @click="triggerFileUpload">
              <v-list-item-title>Import Settings</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <input type="file" ref="fileInput" @change="handleFileUpload" accept=".json" style="display: none" />
        <v-btn color="primary" variant="elevated" @click="saveSettings">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useSettingsStore } from '../stores/settings';
import { useAppsStore } from '../stores/apps';
import { useSnackbar } from '../composables/useSnackbar';
import { themes } from "../themes";
import { useApi } from "../services/useApi";
import { useDisplay, useTheme } from 'vuetify';

const { mobile: isMobile } = useDisplay();
const theme = useTheme();

const languages = [
  { text: 'English (US)', value: 'en-US' },
  { text: 'Chinese (Simplified)', value: 'zh-CN' },
  { text: 'German', value: 'de-DE' },
  { text: 'French', value: 'fr-FR' },
  { text: 'Hindi', value: 'hi-IN' },
  { text: 'Japanese', value: 'ja-JP' },
  { text: 'Spanish', value: 'es-ES' },
  { text: 'Portuguese', value: 'pt-BR' },
  { text: 'Russian', value: 'ru-RU' },
];

const voices = [
  { name: 'Puck', description: 'upbeat' },
  { name: 'Charon', description: 'informative' },
  { name: 'Kore', description: 'Firm' },
  { name: 'Fenrir', description: 'Excitable' },
  { name: 'Aoede', description: 'Breezy' },
  { name: 'Leda', description: 'Youthful' },
  { name: 'Orus', description: 'Firm' },
  { name: 'Zephyr', description: 'Bright' },
];

const props = defineProps({
  modelValue: Boolean,
  openMoreMenu: Boolean,
});

const emit = defineEmits(['update:modelValue', 'api-key-updated']);
const moreButton = ref(null);

const settingsStore = useSettingsStore();
const { settings, currentTheme, darkMode } = storeToRefs(settingsStore);
const {
  updateSettings,
  saveSettings: save,
  setTheme,
  setDarkMode,
} = settingsStore;
const { showSnackbar } = useSnackbar();
const { saveGeminiApiKey: saveKey } = useApi();

const editableSettings = ref(null);
const fileInput = ref(null);
const tab = ref('appAgent');
const geminiApiKey = ref("");
const apiKeyEdited = ref(false);
const showGeminiApiKey = ref(false);
const themeNames = Object.keys(themes);

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
      save(finalSettings);
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
    save(editableSettings.value);
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
    editableSettings.value.gemini_api_key = geminiApiKey.value;
    save(editableSettings.value);
    emit("api-key-updated", !!geminiApiKey.value);
    apiKeyEdited.value = false;
  } else {
    geminiApiKey.value = "";
  }
}

onMounted(() => {
  const appsStore = useAppsStore();
  appsStore.fetchApps();

  if (settings.value?.gemini_api_key) {
    geminiApiKey.value = settings.value.gemini_api_key;
    apiKeyEdited.value = false;
    emit("api-key-updated", true);
  } else {
    apiKeyEdited.value = true;
  }
});
</script>

<style scoped>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
