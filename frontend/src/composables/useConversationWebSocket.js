import { ref } from 'vue';
import { useSettings } from './useSettings';

export function useConversationWebSocket() {
  const websocket = ref(null);
  const messages = ref([]);
  const notes = ref('');
  const analysis = ref(null);
  const isConnecting = ref(false);
  const conversationStarted = ref(false);
  const conversationFinished = ref(false);
  const currentMessageId = ref(null);
  const { settings } = useSettings();

  let playAudioCallback = null;
  let stopPlaybackCallback = null;

  const connect = (playAudio, stopPlayback) => {
    playAudioCallback = playAudio;
    stopPlaybackCallback = stopPlayback;

    isConnecting.value = true;
    conversationFinished.value = false;
    currentMessageId.value = null;
    notes.value = '';
    analysis.value = null;

    const userId = Math.floor(Math.random() * 1000);
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/${userId}?is_audio=true`;
    
    websocket.value = new WebSocket(wsUrl);

    websocket.value.onopen = () => {
      console.log('WebSocket connection established');
      if (settings.value) {
        websocket.value.send(JSON.stringify(settings.value));
        console.log('Settings sent to server');
      }
      messages.value.push({ id: Date.now(), sender: 'system', text: 'Connection established. You can start speaking.' });
      conversationStarted.value = true;
      isConnecting.value = false;
    };

    websocket.value.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("[AGENT TO CLIENT] ", message);

      if (message.turn_complete) {
        currentMessageId.value = null;
        if (stopPlaybackCallback) stopPlaybackCallback();
        return;
      }

      if (message.interrupted) {
        if (stopPlaybackCallback) stopPlaybackCallback();
        return;
      }

      if (message.mime_type === 'audio/pcm' && message.data) {
        if (playAudioCallback) playAudioCallback(message.data);
      }
      if (message.input_transcription) {
        const lastLine = notes.value.trim().split('\n').pop();
        if (!lastLine.startsWith('**You:**')) {
          notes.value += `\n\n**You:** ${message.input_transcription.text}`;
        } else {
          notes.value += `${message.input_transcription.text}`;
        }
      }
      if (message.output_transcription) {
        const lastLine = notes.value.trim().split('\n').pop();
        if (!lastLine.startsWith('**Agent:**')) {
          notes.value += `\n\n**Agent:** ${message.output_transcription.text}`;
        } else {
          notes.value += `${message.output_transcription.text}`;
        }
      }
    };

    websocket.value.onclose = () => {
      console.log('WebSocket connection closed');
      messages.value.push({ id: Date.now(), sender: 'system', text: 'Connection closed.' });
      conversationStarted.value = false;
      isConnecting.value = false;
    };

    websocket.value.onerror = (error) => {
      console.error('WebSocket error:', error);
      messages.value.push({ id: Date.now(), sender: 'system', text: 'Connection error.' });
      conversationStarted.value = false;
      isConnecting.value = false;
    };
  };


  const disconnect = () => {
    if (websocket.value && websocket.value.readyState < 2) { // OPEN or CONNECTING
      websocket.value.close();
    }
    conversationStarted.value = false;
    isConnecting.value = false;
    conversationFinished.value = true;
  };

  return {
    websocket,
    messages,
    notes,
    analysis,
    isConnecting,
    conversationStarted,
    conversationFinished,
    connect,
    disconnect,
  };
}

