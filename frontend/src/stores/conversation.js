import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useSettingsStore } from './settings';
import { useUserStore } from './user';

export const useConversationStore = defineStore('conversation', () => {
  const settingsStore = useSettingsStore();
  const websocket = ref(null);
  const messages = ref([]);
  const notes = ref('');
  const currentAvatar = ref('/assets/avatar_language_pal.png');
  const analysis = ref(null);
  const isAnalysing = ref(false);
  const activeTab = ref('transcription');
  const isConnecting = ref(false);
  const conversationStarted = ref(false);
  const conversationFinished = ref(false);
  const currentMessageId = ref(null);

  let playAudioCallback = null;
  let stopPlaybackCallback = null;

  const connect = (playAudio, stopPlayback) => {
    const settingsStore = useSettingsStore();
    const userStore = useUserStore();

    playAudioCallback = playAudio;
    stopPlaybackCallback = stopPlayback;

    isConnecting.value = true;
    conversationFinished.value = false;
    currentMessageId.value = null;
    notes.value = '';
    analysis.value = null;
    isAnalysing.value = false;
    activeTab.value = 'transcription';

    const userId = Math.floor(Math.random() * 1000);
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/${userId}?is_audio=true`;
    
    websocket.value = new WebSocket(wsUrl);

    websocket.value.onopen = () => {
      console.log('WebSocket connection established');
      if (settingsStore.settings) {
        const settingsMessage = {
          type: 'settings',
          settings: settingsStore.settings,
        };
        websocket.value.send(JSON.stringify(settingsMessage));
        console.log('Settings sent to server');
      }
      messages.value.push({ id: Date.now(), sender: 'system', text: 'Connection established. You can start speaking.' });
      conversationStarted.value = true;
      isConnecting.value = false;
    };

    websocket.value.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("[AGENT TO CLIENT] ", message);

      if (message.type === 'context_updated') {
        settingsStore.updateContext(message.context_dict);
        return;
      }

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

    websocket.value.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
      // A close event with code 1006 means the connection was terminated abnormally.
      // If the API key isn't set, it's the likely cause.
      if (event.code === 1006 && !userStore.isApiKeySet) {
        messages.value.push({
          id: Date.now(),
          sender: 'system',
          text: 'Connection failed. Please set your Gemini API key in the settings.',
        });
      } else {
        messages.value.push({ id: Date.now(), sender: 'system', text: 'Connection closed.' });
      }
      conversationStarted.value = false;
      isConnecting.value = false;
    };

    websocket.value.onerror = (error) => {
      console.error('WebSocket error:', error);
      messages.value.push({ id: Date.now(), sender: 'system', text: 'An error occurred with the connection.' });
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

  const setActiveTab = (tabName) => {
    activeTab.value = tabName;
  };

  return {
    websocket,
    messages,
    notes,
    analysis,
    isAnalysing,
    activeTab,
    isConnecting,
    conversationStarted,
    conversationFinished,
    currentAvatar,
    connect,
    disconnect,
    setActiveTab,
  };
});
