<template>
  <v-app v-if="isThemeLoaded">
    <settings-sidebar
      v-model="showSettings"
      :selected-theme="selectedTheme"
      :is-dark-mode="isDarkMode"
      @theme-changed="changeTheme"
      @dark-mode-toggled="toggleDarkMode"
      @api-key-updated="updateApiKeyStatus"
    />

    <v-app-bar>
      <v-app-bar-nav-icon @click.stop="showSettings = !showSettings"></v-app-bar-nav-icon>
      <v-toolbar-title class="text-center w-100">{{ appName }}</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid class="fill-height pa-4">
        <v-row class="fill-height">
          <v-col cols="12" class="d-flex flex-column">
            <v-card class="flex-grow-1 d-flex flex-column">
              <v-card-text class="flex-grow-1 d-flex flex-column">
                <agent-profile
                  :analyser-node="analyserNode"
                  :conversation-started="conversationStarted"
                />
                <notes-window ref="notes" :content="analysisContent" />
                <analysis-viewer :content="analysisContent" />
              </v-card-text>
              <v-card-actions class="d-flex flex-column align-center justify-center">
                <control-buttons
                  :conversation-started="conversationStarted"
                  :interview-finished="interviewFinished"
                  :is-connecting="isConnecting"
                  :is-analysing="isAnalysing"
                  :is-api-key-set="isApiKeySet"
                  @toggle-interview="toggleInterview"
                  @analyse="analyseInterview"
                />
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import AgentProfile from './components/AgentProfile.vue';
import ControlButtons from './components/ControlButtons.vue';
import SettingsSidebar from './components/SettingsSidebar.vue';
import NotesWindow from './components/NotesWindow.vue';
import AnalysisViewer from './components/AnalysisViewer.vue';
import { useAudio } from './composables/useAudio';
import { useInterviewWebSocket } from './composables/useInterviewWebSocket';
import { useThemeManager } from './composables/useThemeManager';
import { useSettings } from './composables/useSettings';

// --- Reactive State ---
const appName = ref('Any Voicechat');
const { settings, loadSettings } = useSettings();

// Theme
const {
  selectedTheme,
  isDarkMode,
  changeTheme,
  toggleDarkMode,
  initTheme,
} = useThemeManager();
const isThemeLoaded = ref(false);

// Component State
const showSettings = ref(true);
const isApiKeySet = ref(false);
const isAnalysing = ref(false);
const analysisCompleted = ref(false);
const analysisContent = ref('');
const notes = ref(null); // for the ref in the template

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
  isConnecting,
  conversationStarted,
  interviewFinished,
  connect,
  disconnect,
} = useInterviewWebSocket(playAudio, stopPlayback);

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

async function fetchAnalysis() {
  try {
    const response = await fetch('/api/result_docs/analysis');
    if (response.ok) {
      const data = await response.json();
      analysisContent.value = data.content;
    } else {
      console.error('Error fetching analysis:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching analysis:', error);
  }
}

function onAnalysisComplete(analysis) {
  analysisContent.value = analysis;
  analysisCompleted.value = true;
}

async function analyseInterview() {
  isAnalysing.value = true;
  try {
    const response = await fetch('/api/analyse', { method: 'POST' });
    if (response.ok) {
      const data = await response.json();
      onAnalysisComplete(data.analysis);
    } else {
      console.error('Error analysing interview:', response.statusText);
    }
  } catch (error) {
    console.error('Error analysing interview:', error);
  } finally {
    isAnalysing.value = false;
    interviewFinished.value = false; // Ready for a new interview
  }
}

function updateApiKeyStatus() {
  setApiKey();
}

async function toggleInterview() {
  if (conversationStarted.value) {
    stopInterview();
  } else {
    await startConversation();
  }
}

async function startConversation() {
  analysisCompleted.value = false;
  analysisContent.value = '';
  try {
    await startAudio();
    connect();
  } catch (error) {
    console.error('Error starting interview:', error);
    messages.value.push({ id: Date.now(), sender: 'system', text: 'Error accessing microphone. Please grant permission and try again.' });
    stopAudio();
  }
}

function stopInterview() {
  stopAudio();
  disconnect();
}

async function setApiKey() {
  const apiKey = localStorage.getItem("geminiApiKey");
  if (apiKey) {
    try {
      const response = await fetch('/api/set_api_key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key: apiKey }),
      });
      const data = await response.json();
      if (data.status === 'success') {
        isApiKeySet.value = true;
        console.log('API key set successfully');
      } else {
        isApiKeySet.value = false;
        console.error('Failed to set API key:', data.message);
      }
    } catch (error) {
      isApiKeySet.value = false;
      console.error('Error setting API key:', error);
    }
  } else {
    isApiKeySet.value = false;
  }
}

// --- Lifecycle Hooks ---

onMounted(async () => {
  loadSettings();
  fetchAnalysis();
  setApiKey();
  initTheme();
  await nextTick();
  isThemeLoaded.value = true;
});

onBeforeUnmount(() => {
  stopInterview();
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
