<template>
  <v-app v-if="themeLoaded">
    <settings-sidebar
      v-model="showSettings"
      :selected-theme="selectedTheme"
      :is-dark-mode="isDarkMode"
      @theme-changed="changeTheme"
      @dark-mode-toggled="toggleDarkMode"
      @api-key-updated="updateApiKeyStatus"
    />

    <v-app-bar v-if="config">
      <v-app-bar-nav-icon @click.stop="showSettings = !showSettings"></v-app-bar-nav-icon>
      <v-toolbar-title class="text-center w-100">{{ config.title }}</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid class="fill-height pa-4">
        <v-row class="fill-height">
          <v-col :cols="analysisCompleted ? 6 : 12" class="d-flex flex-column">
            <v-card class="flex-grow-1 d-flex flex-column">
              <v-card-text class="flex-grow-1 d-flex flex-column">
                <agent-profile
                  :analyser-node="analyserNode"
                  :conversation-started="conversationStarted"
                />
                <notes-window ref="notes" />
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
                <status-window :messages="messages" class="flex-grow-1" />
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col v-if="analysisCompleted" cols="6" class="d-flex flex-column">
            <analysis-viewer :content="analysisContent" />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, inject, nextTick } from 'vue';
import { useTheme } from 'vuetify';
import AgentProfile from './components/AgentProfile.vue';
import StatusWindow from './components/StatusWindow.vue';
import ControlButtons from './components/ControlButtons.vue';
import SettingsSidebar from './components/SettingsSidebar.vue';
import NotesWindow from './components/NotesWindow.vue';
import AnalysisViewer from "./components/AnalysisViewer.vue";
import { useAudio } from './composables/useAudio';
import { useInterviewWebSocket } from './composables/useInterviewWebSocket';
import { themes as customThemes } from './themes';

// --- Injected ---
const config = inject('config');

// --- Reactive State ---

// Theme
const theme = useTheme();
const availableThemes = Object.keys(customThemes);
let initialTheme = localStorage.getItem('theme') || 'Default';
if (!availableThemes.includes(initialTheme)) {
  initialTheme = 'Default';
}
const selectedTheme = ref(initialTheme);
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true');
const themeLoaded = ref(false);

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

// --- Functions ---

const applyTheme = async () => {
  const themeName = isDarkMode.value ? `${selectedTheme.value}Dark` : selectedTheme.value;
  theme.global.name.value = themeName;
  await nextTick();
  themeLoaded.value = true;
};

const changeTheme = (themeName) => {
  selectedTheme.value = themeName;
  localStorage.setItem('theme', themeName);
  applyTheme();
};

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  localStorage.setItem('darkMode', isDarkMode.value);
  applyTheme();
};

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
    await startInterview();
  }
}

async function startInterview() {
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

onMounted(() => {
  setApiKey();
  applyTheme();
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
