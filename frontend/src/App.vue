<template>
  <v-app>
    <v-container>
      <v-card class="mx-auto" max-width="800">
        <v-card-title class="text-h5 text-center">
          Welcome
        </v-card-title>
        <v-card-text>
          <div class="d-flex flex-no-wrap justify-space-between">
            <div class="d-flex flex-column align-center justify-center pa-3">
              <v-avatar class="mb-4" size="125" rounded="lg">
                <v-img :src="agentAvatar"></v-img>
              </v-avatar>
              <canvas ref="visualizer" width="125" height="50"></canvas>
            </div>
            <div class="flex-grow-1">
              <div class="notes-container" ref="notesContainer">
                <div v-for="message in messages" :key="message.id" :class="`message ${message.sender}`">
                  <pre>{{ message.text }}</pre>
                </div>
              </div>
            </div>
          </div>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn @click="toggleInterview" :color="interviewStarted ? 'red' : 'primary'" :disabled="isConnecting">
            <v-progress-circular indeterminate v-if="isConnecting" size="20" class="mr-2"></v-progress-circular>
            {{ interviewStarted ? 'Stop Interview' : 'Start Mock Interview' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
import agentAvatar from './assets/agent-avatar.svg';

export default {
  data() {
    return {
      messages: [],
      interviewStarted: false,
      isConnecting: false,
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
      visualizerAnimationId: null,
      
      agentAvatar,
      currentMessageId: null,
    };
  },
  methods: {
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

          this.$nextTick(() => {
            const container = this.$refs.notesContainer;
            if (container) container.scrollTop = container.scrollHeight;
          });
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
      this.drawVisualizer();
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

    drawVisualizer() {
      const canvas = this.$refs.visualizer;
      if (!canvas || !this.analyserNode) return;
      const canvasCtx = canvas.getContext('2d');
      const bufferLength = this.analyserNode.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const draw = () => {
        if (!this.interviewStarted) {
          canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
          return;
        }
        this.visualizerAnimationId = requestAnimationFrame(draw);
        this.analyserNode.getByteFrequencyData(dataArray);
        canvasCtx.fillStyle = 'rgb(240, 240, 240)';
        canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
        const barWidth = (canvas.width / bufferLength) * 2.5;
        let barHeight;
        let x = 0;
        for (let i = 0; i < bufferLength; i++) {
          barHeight = dataArray[i] / 2;
          canvasCtx.fillStyle = `rgb(66, 165, 245)`;
          canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
          x += barWidth + 1;
        }
      };
      draw();
    },

    stopInterview(closeWebSocket = true) {
      if (this.visualizerAnimationId) {
        cancelAnimationFrame(this.visualizerAnimationId);
        this.visualizerAnimationId = null;
      }
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
    }
  },
  beforeUnmount() {
    this.stopInterview();
  },
};
</script>

<style>
.notes-container {
  width: 100%;
  margin: 0 auto;
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
}

.message.user {
  align-self: flex-end;
  background-color: #dcf8c6;
  color: #000;
}

.message.agent {
  align-self: flex-start;
  background-color: #f1f0f0;
  color: #000;
}

.message.system {
  align-self: center;
  color: gray;
  font-style: italic;
}

pre {
  white-space: pre-wrap;
  font-family: inherit;
}
</style>
