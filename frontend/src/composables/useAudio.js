import { ref, onUnmounted } from 'vue';

function base64ToArray(base64) {
  const binaryString = window.atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

function arrayBufferToBase64(buffer) {
  let binary = "";
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

function convertFloat32ToPCM(inputData) {
  const pcm16 = new Int16Array(inputData.length);
  for (let i = 0; i < inputData.length; i++) {
    pcm16[i] = inputData[i] * 0x7fff;
  }
  return pcm16.buffer;
}

export function useAudio(websocket, onAudioData) {
  const audioPlayerNode = ref(null);
  const audioPlayerContext = ref(null);
  const audioRecorderNode = ref(null);
  const audioRecorderContext = ref(null);
  const micStream = ref(null);
  const audioBuffer = ref([]);
  const bufferTimer = ref(null);
  const analyserNode = ref(null);

  const startAudio = async () => {
    // Start audio player
    audioPlayerContext.value = new AudioContext({ sampleRate: 24000 });
    await audioPlayerContext.value.audioWorklet.addModule('/pcm-player-processor.js');
    audioPlayerNode.value = new AudioWorkletNode(audioPlayerContext.value, 'pcm-player-processor');
    audioPlayerNode.value.connect(audioPlayerContext.value.destination);

    // Start audio recorder
    audioRecorderContext.value = new AudioContext({ sampleRate: 16000 });
    await audioRecorderContext.value.audioWorklet.addModule('/pcm-recorder-processor.js');
    micStream.value = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1 } });
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

  const playAudio = (data) => {
    if (audioPlayerNode.value) {
      const audioData = base64ToArray(data);
      audioPlayerNode.value.port.postMessage(audioData);
    }
  };

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
