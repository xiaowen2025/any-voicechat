<template>
  <v-app>
    <settings-sidebar
      :model-value="showSettings"
      @update:model-value="showSettings = $event"
      @toggle-settings="isSettingsWindowVisible = !isSettingsWindowVisible"
    />
    <settings-window
      v-model="isSettingsWindowVisible"
      @api-key-updated="updateApiKeyStatus"
    />
    <v-app-bar>
      <v-app-bar-nav-icon @click.stop="showSettings = !showSettings"></v-app-bar-nav-icon>
      <v-toolbar-title>{{ appName }}</v-toolbar-title>
      <v-spacer></v-spacer>
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
      <conversation-view
        v-else
        :analyser-node="analyserNode"
        :conversation-started="conversationStarted"
        :conversation-finished="conversationFinished"
        :is-connecting="isConnecting"
        :is-analysing="isAnalysing"
        @toggle-conversation="toggleConversation"
        @analyse="analyseConversation"
      />
    </v-main>
    <v-snackbar
      v-model="snackbar.visible.value"
      :color="snackbar.color.value"
      timeout="3000"
    >
      {{ snackbar.message.value }}
    </v-snackbar>
    <v-overlay
      :model-value="!isThemeLoaded"
      class="align-center justify-center"
      persistent
    >
      <v-progress-circular indeterminate size="64" />
    </v-overlay>
  </v-app>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick, computed } from 'vue';
import { useDisplay } from 'vuetify';
import { storeToRefs } from 'pinia';
import { defineAsyncComponent } from 'vue';
import SettingsSidebar from './components/SettingsSidebar.vue';
import SettingsWindow from './components/SettingsWindow.vue';

const ConversationView = defineAsyncComponent(() => import('./components/ConversationView.vue'));
const AppsGallery = defineAsyncComponent(() => import('./components/AppsGallery.vue'));
import { useAudio } from './composables/audio/useAudio';
import { useSnackbar } from './composables/useSnackbar';
import { useApi } from './services/useApi';
import { useConversationStore } from './stores/conversation';
import { useSettingsStore } from './stores/settings';
import { useUserStore } from './stores/user';

// --- Stores ---
const conversationStore = useConversationStore();
const settingsStore = useSettingsStore();
const userStore = useUserStore();

const {
  websocket,
  messages,
  notes,
  analysis,
  isAnalysing,
  isConnecting,
  conversationStarted,
  conversationFinished,
  currentAvatar,
} = storeToRefs(conversationStore);
const { connect, disconnect, setActiveTab } = conversationStore;

const { settings, currentTheme, darkMode } = storeToRefs(settingsStore);
const { loadSettings, updateSettings } = settingsStore;

const { setApiKey } = userStore;

// --- Reactive State ---
const showAppsGallery = ref(false);
const appName = ref(settings.value?.app_name || 'App');
const snackbar = useSnackbar();
const { getAppSettings } = useApi();

// Theme
const isThemeLoaded = ref(false);

// Display
const { mobile } = useDisplay();
const isMobile = computed(() => mobile.value);

// Component State
const showSettings = ref(!isMobile.value);
const isSettingsWindowVisible = ref(false);

// Composables
const audioWebsocket = ref(null);
const {
  analyserNode,
  startAudio,
  stopAudio,
  playAudio,
  stopPlayback,
} = useAudio(audioWebsocket);

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

async function loadApp(appId) {
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

function handleAppSelection(appId) {
  const newUrl = `/apps/${appId}`;
  window.location.assign(newUrl);
}

async function analyseConversation() {
  isAnalysing.value = true;
  setActiveTab('analysis');
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

onMounted(() => {
  const path = window.location.pathname;
  const appMatch = path.match(/^\/apps\/([a-zA-Z0-9_-]+)/);

  if (appMatch) {
    const appId = appMatch[1];
    loadApp(appId);
  } else if (path === '/apps') {
    showAppsGallery.value = true;
    showSettings.value = false;
  } else {
    loadSettings();
  }

  const savedAvatar = localStorage.getItem('userAvatar');
  if (savedAvatar) {
    currentAvatar.value = savedAvatar;
  }
  setApiKey();
  nextTick().then(() => {
    isThemeLoaded.value = true;
  });
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