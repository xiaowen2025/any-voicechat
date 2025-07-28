<template>
  <v-app>
    <settings-sidebar
      :is-dark-theme="isDarkTheme"
      @toggle-theme="toggleTheme"
      @api-key-updated="updateApiKeyStatus"
    />

    <v-main>
      <v-container fluid class="fill-height pa-4">
        <v-card class="flex-grow-1 d-flex flex-column">
          <v-card-text class="flex-grow-1 d-flex flex-column">
            <agent-profile
              :analyser-node="analyserNode"
              :interview-started="interviewStarted"
            />
            <interview-notes-window />
          </v-card-text>
          <v-card-actions class="d-flex flex-column align-center justify-center">
            <control-buttons
              :interview-started="interviewStarted"
              :is-connecting="isConnecting"
              :is-api-key-set="isApiKeySet"
              @toggle-interview="toggleInterview"
            />
            <status-window :messages="messages" class="flex-grow-1" />
          </v-card-actions>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { useTheme } from 'vuetify';
import AgentProfile from './components/AgentProfile.vue';
import StatusWindow from './components/StatusWindow.vue';
import ControlButtons from './components/ControlButtons.vue';
import SettingsSidebar from './components/SettingsSidebar.vue';
import InterviewNotesWindow from './components/InterviewNotesWindow.vue';

export default {
  components: {
    AgentProfile,
    StatusWindow,
    ControlButtons,
    SettingsSidebar,
    InterviewNotesWindow,
  },
  setup() {
    const theme = useTheme();
    const isDarkTheme = theme.global.current.value.dark;

    const toggleTheme = () => {
      theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark';
    };

    return {
      isDarkTheme,
      toggleTheme,
    };
  },
  data() {
    return {
      messages: [],
      interviewStarted: false,
      isConnecting: false,
      isApiKeySet: false,
      websocket: null,
      
      // Audio Player
      audioPlayerNode: null,
      audioPlayerContext: null,

      // Audio Recorder
      audioRecorderNode: null,
      audioRecorderContext: null,
      micStream: null,
      audioBuffer: [],
      bufferTimer: null,

      // Visualizer
      analyserNode: null,
      
      currentMessageId: null,
    };
  },
  methods: {
    updateApiKeyStatus() {
      this.setApiKey();
    },
    async toggleInterview() {
      if (this.interviewStarted) {
        this.stopInterview();
      } else {
        await this.startInterview();
      }
    },
    async startInterview() {
      this.isConnecting = true;
      try {
        // First, get user media permission and set up audio processing
        await this.startAudio();

        // If audio is successful, then establish the WebSocket connection
        const userId = Math.floor(Math.random() * 1000);
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.websocket = new WebSocket(`${wsProtocol}//${window.location.host}/ws/${userId}?is_audio=true`);

        this.websocket.onopen = () => {
          console.log('WebSocket connection established');
          this.messages.push({ id: Date.now(), sender: 'system', text: 'Connection established. You can start speaking.' });
          this.interviewStarted = true;
          this.isConnecting = false;
        };

        this.websocket.onmessage = (event) => {
          const message = JSON.parse(event.data);
          console.log("[AGENT TO CLIENT] ", message);

          if (message.turn_complete) {
            this.currentMessageId = null;
            return;
          }

          if (message.interrupted) {
            if (this.audioPlayerNode) {
              this.audioPlayerNode.port.postMessage({ command: "endOfAudio" });
            }
            return;
          }

          if (message.mime_type === 'audio/pcm' && message.data && this.audioPlayerNode) {
            const audioData = this.base64ToArray(message.data);
            this.audioPlayerNode.port.postMessage(audioData);
          }

          if (message.mime_type === 'text/plain') {
            if (this.currentMessageId === null) {
              this.currentMessageId = `msg-${Date.now()}`;
              this.messages.push({ id: this.currentMessageId, sender: 'agent', text: message.data });
            } else {
              const msg = this.messages.find(m => m.id === this.currentMessageId);
              if (msg) {
                msg.text += message.data;
              }
            }
          }
        };

        this.websocket.onclose = () => {
          console.log('WebSocket connection closed');
          this.messages.push({ id: Date.now(), sender: 'system', text: 'Connection closed.' });
          this.stopInterview(false);
        };

        this.websocket.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.messages.push({ id: Date.now(), sender: 'system', text: 'Connection error.' });
          this.stopInterview(false);
        };

      } catch (error) {
        console.error('Error starting interview:', error);
        this.messages.push({ id: Date.now(), sender: 'system', text: 'Error accessing microphone. Please grant permission and try again.' });
        this.stopInterview(); // Clean up audio resources
        this.isConnecting = false;
      }
    },

    async startAudio() {
      // Start audio player
      this.audioPlayerContext = new AudioContext({ sampleRate: 24000 });
      await this.audioPlayerContext.audioWorklet.addModule('/pcm-player-processor.js');
      this.audioPlayerNode = new AudioWorkletNode(this.audioPlayerContext, 'pcm-player-processor');
      this.audioPlayerNode.connect(this.audioPlayerContext.destination);

      // Start audio recorder
      this.audioRecorderContext = new AudioContext({ sampleRate: 16000 });
      await this.audioRecorderContext.audioWorklet.addModule('/pcm-recorder-processor.js');
      this.micStream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1 } });
      const source = this.audioRecorderContext.createMediaStreamSource(this.micStream);
      this.audioRecorderNode = new AudioWorkletNode(this.audioRecorderContext, 'pcm-recorder-processor');
      
      this.audioRecorderNode.port.onmessage = (event) => {
        const pcmData = this.convertFloat32ToPCM(event.data);
        this.audioBuffer.push(new Uint8Array(pcmData));
        if (!this.bufferTimer) {
          this.bufferTimer = setInterval(this.sendBufferedAudio, 200);
        }
      };
      
      source.connect(this.audioRecorderNode);

      // --- Visualizer Setup ---
      this.analyserNode = this.audioRecorderContext.createAnalyser();
      this.analyserNode.fftSize = 256;
      source.connect(this.analyserNode);
    },

    sendBufferedAudio() {
      if (this.audioBuffer.length === 0 || !this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
        return;
      }
      
      let totalLength = 0;
      for (const chunk of this.audioBuffer) {
        totalLength += chunk.length;
      }
      
      const combinedBuffer = new Uint8Array(totalLength);
      let offset = 0;
      for (const chunk of this.audioBuffer) {
        combinedBuffer.set(chunk, offset);
        offset += chunk.length;
      }
      
      const base64data = this.arrayBufferToBase64(combinedBuffer.buffer);
      const message = { mime_type: "audio/pcm", data: base64data };
      this.websocket.send(JSON.stringify(message));
      
      this.audioBuffer = [];
    },

    stopInterview(closeWebSocket = true) {
      if (this.bufferTimer) {
        clearInterval(this.bufferTimer);
        this.bufferTimer = null;
      }

      if (this.audioRecorderNode) {
        this.audioRecorderNode.disconnect();
        this.audioRecorderNode = null;
      }
      if (this.analyserNode) {
        this.analyserNode.disconnect();
        this.analyserNode = null;
      }
      if (this.micStream) {
        this.micStream.getTracks().forEach(track => track.stop());
        this.micStream = null;
      }
      if (this.audioRecorderContext) {
        this.audioRecorderContext.close();
        this.audioRecorderContext = null;
      }

      if (this.audioPlayerNode) {
        this.audioPlayerNode.disconnect();
        this.audioPlayerNode = null;
      }
      if (this.audioPlayerContext) {
        this.audioPlayerContext.close();
        this.audioPlayerContext = null;
      }

      if (this.websocket && closeWebSocket) {
        this.websocket.close();
      }
      this.interviewStarted = false;
      this.isConnecting = false;
    },

    // Helper functions
    base64ToArray(base64) {
      const binaryString = window.atob(base64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      return bytes.buffer;
    },
    arrayBufferToBase64(buffer) {
      let binary = "";
      const bytes = new Uint8Array(buffer);
      const len = bytes.byteLength;
      for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      return window.btoa(binary);
    },
    convertFloat32ToPCM(inputData) {
      const pcm16 = new Int16Array(inputData.length);
      for (let i = 0; i < inputData.length; i++) {
        pcm16[i] = inputData[i] * 0x7fff;
      }
      return pcm16.buffer;
    },
    async setApiKey() {
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
            this.isApiKeySet = true;
            console.log('API key set successfully');
          } else {
            this.isApiKeySet = false;
            console.error('Failed to set API key:', data.message);
          }
        } catch (error) {
          this.isApiKeySet = false;
          console.error('Error setting API key:', error);
        }
      } else {
        this.isApiKeySet = false;
      }
    },
  },
  mounted() {
    this.setApiKey();
  },
  beforeUnmount() {
    this.stopInterview();
  },
};
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
