import { ref } from 'vue';

export function useInterviewWebSocket(playAudio, stopPlayback) {
  const websocket = ref(null);
  const messages = ref([]);
  const notes = ref('');
  const isConnecting = ref(false);
  const conversationStarted = ref(false);
  const interviewFinished = ref(false);
  const currentMessageId = ref(null);

  const connect = () => {
    isConnecting.value = true;
    interviewFinished.value = false;
    currentMessageId.value = null;
    notes.value = '';

    const userId = Math.floor(Math.random() * 1000);
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/${userId}?is_audio=true`;
    
    websocket.value = new WebSocket(wsUrl);

    websocket.value.onopen = () => {
      console.log('WebSocket connection established');
      messages.value.push({ id: Date.now(), sender: 'system', text: 'Connection established. You can start speaking.' });
      conversationStarted.value = true;
      isConnecting.value = false;
    };

    websocket.value.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("[AGENT TO CLIENT] ", message);

      if (message.turn_complete) {
        currentMessageId.value = null;
        return;
      }

      if (message.interrupted) {
        if (stopPlayback) stopPlayback();
        return;
      }

      if (message.mime_type === 'audio/pcm' && message.data) {
        if (playAudio) playAudio(message.data);
      }

      if (message.mime_type === 'text/plain') {
        if (currentMessageId.value === null) {
          currentMessageId.value = `msg-${Date.now()}`;
          messages.value.push({ id: currentMessageId.value, sender: 'agent', text: message.data });
        } else {
          const msg = messages.value.find(m => m.id === currentMessageId.value);
          if (msg) {
            msg.text += message.data;
          }
        }
      }

      if (message.input_transcription) {
        notes.value += `**You:** ${message.input_transcription.text}\n\n`;
      }
      if (message.output_transcription) {
        notes.value += `**Agent:** ${message.output_transcription.text}\n\n`;
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
    interviewFinished.value = true;
  };

  return {
    websocket,
    messages,
    notes,
    isConnecting,
    conversationStarted,
    interviewFinished,
    connect,
    disconnect,
  };
}
