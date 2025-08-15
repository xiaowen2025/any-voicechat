import { ref, onUnmounted } from 'vue';
import {
  base64ToArray,
  arrayBufferToBase64,
  convertFloat32ToPCM,
} from './utils.js';

/**
 * @module useAudio
 * @description A Vue composable for handling audio recording, playback, and processing.
 * This composable manages the AudioContext, microphone input, and audio worklets for
 * recording and playing PCM audio data. It also provides a visualizer node.
 */

/**
 * Sets up and manages audio functionality.
 *
 * @param {import('vue').Ref<WebSocket>} websocket - A ref to the WebSocket instance for sending audio data.
 * @param {Function} onAudioData - Callback function to handle incoming audio data.
 * @returns {object} An object containing audio control functions and refs.
 * @property {import('vue').Ref<AnalyserNode>} analyserNode - The audio analyser node for visualization.
 * @property {Function} startAudio - Initializes and starts the audio recording and playback.
 * @property {Function} stopAudio - Stops audio recording and playback and cleans up resources.
 * @property {Function} playAudio - Plays a chunk of audio data.
 * @property {Function} stopPlayback - Stops the audio playback.
 */
export function useAudio(websocket, onAudioData) {
  const audioPlayerNode = ref(null);
  const audioPlayerContext = ref(null);
  const audioRecorderNode = ref(null);
  const audioRecorderContext = ref(null);
  const micStream = ref(null);
  const audioBuffer = ref([]);
  const bufferTimer = ref(null);
  const analyserNode = ref(null);

  /**
   * Initializes and starts the audio recording and playback systems.
   * This function sets up the AudioContext for both player and recorder,
   * adds the necessary audio worklet modules, and requests microphone access.
   * @returns {Promise<void>}
   */
  const startAudio = async () => {
    // Start audio player
    audioPlayerContext.value = new AudioContext({ sampleRate: 24000 });
    await audioPlayerContext.value.audioWorklet.addModule('/pcm-player-processor.js');
    audioPlayerNode.value = new AudioWorkletNode(audioPlayerContext.value, 'pcm-player-processor');
    audioPlayerNode.value.connect(audioPlayerContext.value.destination);

    // Start audio recorder
    audioRecorderContext.value = new AudioContext({ sampleRate: 16000 });
    await audioRecorderContext.value.audioWorklet.addModule('/pcm-recorder-processor.js');
    micStream.value = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, channelCount: 1 } });
    const source = audioRecorderContext.value.createMediaStreamSource(micStream.value);
    audioRecorderNode.value = new AudioWorkletNode(audioRecorderContext.value, 'pcm-recorder-processor');
    
    audioRecorderNode.value.port.onmessage = (event) => {
      const pcmData = convertFloat32ToPCM(event.data);
      audioBuffer.value.push(new Uint8Array(pcmData));
      if (!bufferTimer.value) {
        bufferTimer.value = setInterval(sendBufferedAudio, 200);
      }
    };
    
    source.connect(audioRecorderNode.value);

    // --- Visualizer Setup ---
    analyserNode.value = audioRecorderContext.value.createAnalyser();
    analyserNode.value.fftSize = 256;
    source.connect(analyserNode.value);
  };

  /**
   * Sends the buffered audio data over the WebSocket connection.
   * This function is called periodically by a timer. It combines the
   * buffered audio chunks into a single ArrayBuffer, converts it to
   * Base64, and sends it as a JSON message.
   */
  const sendBufferedAudio = () => {
    if (audioBuffer.value.length === 0 || !websocket.value || websocket.value.readyState !== WebSocket.OPEN) {
      return;
    }
    
    let totalLength = 0;
    for (const chunk of audioBuffer.value) {
      totalLength += chunk.length;
    }
    
    const combinedBuffer = new Uint8Array(totalLength);
    let offset = 0;
    for (const chunk of audioBuffer.value) {
      combinedBuffer.set(chunk, offset);
      offset += chunk.length;
    }
    
    const base64data = arrayBufferToBase64(combinedBuffer.buffer);
    const message = { mime_type: "audio/pcm", data: base64data };
    websocket.value.send(JSON.stringify(message));
    
    audioBuffer.value = [];
  };

  /**
   * Stops the audio recording and playback systems and cleans up all resources.
   * This includes stopping the microphone, disconnecting nodes, and closing the AudioContexts.
   */
  const stopAudio = () => {
    if (bufferTimer.value) {
      clearInterval(bufferTimer.value);
      bufferTimer.value = null;
    }

    if (audioRecorderNode.value) {
      audioRecorderNode.value.disconnect();
      audioRecorderNode.value = null;
    }
    if (analyserNode.value) {
      analyserNode.value.disconnect();
      analyserNode.value = null;
    }
    if (micStream.value) {
      micStream.value.getTracks().forEach(track => track.stop());
      micStream.value = null;
    }
    if (audioRecorderContext.value) {
      audioRecorderContext.value.close();
      audioRecorderContext.value = null;
    }

    if (audioPlayerNode.value) {
      audioPlayerNode.value.disconnect();
      audioPlayerNode.value = null;
    }
    if (audioPlayerContext.value) {
      audioPlayerContext.value.close();
      audioPlayerContext.value = null;
    }
  };

  /**
   * Plays a chunk of audio data received from the server.
   * @param {string} data - The Base64 encoded audio data to play.
   */
  const playAudio = (data) => {
    if (audioPlayerNode.value) {
      const audioData = base64ToArray(data);
      audioPlayerNode.value.port.postMessage(audioData);
    }
  };

  /**
   * Notifies the audio player worklet that the audio stream has ended.
   */
  const stopPlayback = () => {
    if (audioPlayerNode.value) {
      audioPlayerNode.value.port.postMessage({ command: "endOfAudio" });
    }
  };

  onUnmounted(() => {
    stopAudio();
  });

  return {
    analyserNode,
    startAudio,
    stopAudio,
    playAudio,
    stopPlayback,
  };
}
