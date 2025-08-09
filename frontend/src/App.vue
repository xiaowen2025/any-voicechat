<template>
  <v-app>
    <settings-sidebar
      v-model="showSettings"
      :is-dark-theme="isDarkTheme"
      @toggle-theme="toggleTheme"
      @api-key-updated="updateApiKeyStatus"
    />

    <v-app-bar app>
      <v-app-bar-nav-icon @click.stop="showSettings = !showSettings"></v-app-bar-nav-icon>
      <v-toolbar-title>Interview Simulator</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid class="fill-height pa-4">
        <v-row class="fill-height">
          <v-col :cols="analysisCompleted ? 6 : 12" class="d-flex flex-column">
            <v-card class="flex-grow-1 d-flex flex-column">
              <v-card-text class="flex-grow-1 d-flex flex-column">
                <agent-profile
                  :analyser-node="analyserNode"
                  :interview-started="interviewStarted"
                />
                <notes-window ref="interviewNotes" />
              </v-card-text>
              <v-card-actions class="d-flex flex-column align-center justify-center">
                <control-buttons
                  :interview-started="interviewStarted"
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
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { useTheme } from 'vuetify';
import AgentProfile from './components/AgentProfile.vue';
import StatusWindow from './components/StatusWindow.vue';
import ControlButtons from './components/ControlButtons.vue';
import SettingsSidebar from './components/SettingsSidebar.vue';
import NotesWindow from './components/NotesWindow.vue';
import AnalysisViewer from "./components/AnalysisViewer.vue";
import { useAudio } from './composables/useAudio';
import { useInterviewWebSocket } from './composables/useInterviewWebSocket';

// --- Reactive State ---

// Theme
const theme = useTheme();
const isDarkTheme = ref(theme.global.current.value.dark);

// Component State
const showSettings = ref(true);
const isApiKeySet = ref(false);
const isAnalysing = ref(false);
const analysisCompleted = ref(false);
const analysisContent = ref('');
const interviewNotes = ref(null); // for the ref in the template

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
  interviewStarted,
  interviewFinished,
  connect,
  disconnect,
} = useInterviewWebSocket(playAudio, stopPlayback);

// --- Watchers ---

watch(websocket, (newWebsocketInstance) => {
  audioWebsocket.value = newWebsocketInstance;
});

// --- Functions ---

const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark';
  isDarkTheme.value = theme.global.current.value.dark;
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
  if (interviewStarted.value) {
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
