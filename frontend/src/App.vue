<template>
  <v-app v-if="isThemeLoaded">
    <settings-sidebar
      v-model="showSettings"
      :permanent="!isMobile"
      :temporary="isMobile"
      @toggle-settings="isSettingsWindowVisible = !isSettingsWindowVisible"
      @close="showSettings = false"
    />
    <settings-window
      v-model="isSettingsWindowVisible"
      :selected-theme="selectedTheme"
      :is-dark-mode="isDarkMode"
      @theme-changed="changeTheme"
      @dark-mode-toggled="toggleDarkMode"
      @api-key-updated="updateApiKeyStatus"
    />
    <v-app-bar>
      <v-app-bar-nav-icon @click.stop="showSettings = !showSettings"></v-app-bar-nav-icon>
      <v-toolbar-title class="text-center w-100">{{ appName }}</v-toolbar-title>
      <v-btn icon @click="showAppsGallery = !showAppsGallery">
        <v-icon>{{ showAppsGallery ? 'mdi-close' : 'mdi-apps' }}</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <apps-gallery
        v-if="showAppsGallery"
        @app-selected="handleAppSelection"
        @close="showAppsGallery = false"
      />
      <v-container v-else fluid class="fill-height pa-4">
        <v-row class="fill-height">
          <v-col cols="12" class="d-flex flex-column">
            <v-card class="flex-grow-1 d-flex flex-column">
              <v-card-text class="flex-grow-1 d-flex flex-column">
                <agent-profile
                  :analyser-node="analyserNode"
                  :conversation-started="conversationStarted"
                />
                <notes-window />
              </v-card-text>
              <v-card-actions class="d-flex flex-column align-center justify-center">
                <control-buttons
                  :conversation-started="conversationStarted"
                  :conversation-finished="conversationFinished"
                  :is-connecting="isConnecting"
                  :is-analysing="isAnalysing"
                  @toggle-conversation="toggleConversation"
                  @analyse="analyseConversation"
                />
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-snackbar
      v-model="snackbar.visible.value"
      :color="snackbar.color.value"
      timeout="3000"
      @update:modelValue="snackbar.visible.value = $event"
    >
      {{ snackbar.message.value }}
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick, computed } from 'vue';
import { useDisplay } from 'vuetify';
import AgentProfile from './components/AgentProfile.vue';
import ControlButtons from './components/ControlButtons.vue';
import SettingsSidebar from './components/SettingsSidebar.vue';
import SettingsWindow from './components/SettingsWindow.vue';
import NotesWindow from './components/NotesWindow.vue';
import AppsGallery from './components/AppsGallery.vue';
import { useAudio } from './composables/useAudio';
import { useSharedConversation } from './composables/useSharedConversation';
import { useThemeManager } from './composables/useThemeManager';
import { useSettings } from './composables/useSettings';
import { useSnackbar } from './composables/useSnackbar';
import { useApi } from './composables/useApi';
import { useApiKey } from './composables/useApiKey';

// --- Reactive State ---
const showAppsGallery = ref(false);
const cachedSettings = JSON.parse(localStorage.getItem('settings') || '{}');
const appName = ref(cachedSettings.app_name || 'App');
const { settings, loadSettings, updateSettings } = useSettings();
const snackbar = useSnackbar();
const { getAppSettings } = useApi();
const { setApiKey } = useApiKey();


// Theme
const {
  selectedTheme,
  isDarkMode,
  changeTheme,
  toggleDarkMode,
  initTheme,
} = useThemeManager();
const isThemeLoaded = ref(false);

// Display
const { mobile } = useDisplay();
const isMobile = computed(() => mobile.value);

// Component State
const showSettings = ref(!isMobile.value);
const isSettingsWindowVisible = ref(false);
const isAnalysing = ref(false);

// Composables
const audioWebsocket = ref(null);
const {
  analyserNode,
  startAudio,
  stopAudio,
  playAudio,
  stopPlayback,
} = useAudio(audioWebsocket);

const {
  websocket,
  messages,
  notes,
  analysis,
  isConnecting,
  conversationStarted,
  conversationFinished,
  currentAvatar,
  connect,
  disconnect,
} = useSharedConversation();

// --- Watchers ---

watch(websocket, (newWebsocketInstance) => {
  audioWebsocket.value = newWebsocketInstance;
});

watch(settings, (newSettings) => {
  if (newSettings && newSettings.app_name) {
    appName.value = newSettings.app_name;
    document.title = newSettings.app_name;
  }
});

// --- Functions ---

async function handleAppSelection(appId) {
  try {
    const newSettings = await getAppSettings(appId);
    if (newSettings) {
      updateSettings(newSettings);
      const newAvatar = `/assets/avatar_${appId}.png`;
      currentAvatar.value = newAvatar;
      localStorage.setItem('userAvatar', newAvatar);
      showAppsGallery.value = false;
    } 
  } catch (error) {
    console.error('Error loading app:', error);
  }
}

async function analyseConversation() {
  isAnalysing.value = true;
  try {
    console.log('Sending notes for analysis:', notes.value);
    const response = await fetch('/api/analyse', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ notes: notes.value, settings: settings.value }), // Send notes and settings in the request body
    });
    if (response.ok) {
      const data = await response.json();
      analysis.value = data.analysis;
    } else {
      console.error('Error analysing conversation:', response.statusText);
    }
  } catch (error) {
    console.error('Error analysing conversation:', error);
  } finally {
    isAnalysing.value = false;
    conversationFinished.value = false; // Ready for a new conversation
  }
}

function updateApiKeyStatus() {
  setApiKey();
}

async function toggleConversation() {
  if (conversationStarted.value) {
    stopConversation();
  } else {
    await startConversation();
  }
}

async function startConversation() {
  analysis.value = null;
  try {
    await startAudio();
    connect(playAudio, stopPlayback);
  } catch (error) {
    console.error('Error starting conversation:', error);
    messages.value.push({ id: Date.now(), sender: 'system', text: 'Error accessing microphone. Please grant permission and try again.' });
    stopAudio();
  }
}

function stopConversation() {
  stopAudio();
  disconnect();
}

// --- Lifecycle Hooks ---

onMounted(async () => {
  loadSettings();
  const savedAvatar = localStorage.getItem('userAvatar');
  if (savedAvatar) {
    currentAvatar.value = savedAvatar;
  }
  setApiKey();
  initTheme();
  await nextTick();
  isThemeLoaded.value = true;
});

onBeforeUnmount(() => {
  stopConversation();
});
</script>

<style>
body {
  font-family: 'Inter', sans-serif;
}

.v-app-bar-title {
  font-weight: 600;
}

pre {
  white-space: pre-wrap;
  font-family: inherit;
}
</style>
