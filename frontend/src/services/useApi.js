import { useSettingsStore } from '@/stores/settings';
import { useConversationStore } from '@/stores/conversation';

export function useApi() {
  const settingsStore = useSettingsStore();
  const conversationStore = useConversationStore();

  async function getAppSettings(appId) {
    try {
      const response = await fetch(`/api/apps/${appId}/settings`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      conversationStore.notes = '';
      conversationStore.analysis = null;
      return await response.json();
    } catch (error) {
      console.error(`Error fetching app settings: ${error}`);
      return null;
    }
  }

  async function saveGeminiApiKey(apiKey) {
    try {
      const response = await fetch('/api/verify_api_key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key: apiKey }),
      });
      const result = await response.json();
      if (result.status === 'success') {
        localStorage.setItem('geminiApiKey', apiKey);
        // Also update the settings object
        const newSettings = { ...settingsStore.settings, gemini_api_key: apiKey };
        settingsStore.updateSettings(newSettings);
        alert('API Key saved successfully!');
        return true;
      } else {
        localStorage.removeItem('geminiApiKey');
        alert(`API Key is invalid: ${result.message}`);
        return false;
      }
    } catch (error) {
      alert(`Error verifying API key: ${error}`);
      return false;
    }
  }

  async function getApps() {
    try {
      const response = await fetch('/api/apps');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error fetching apps: ${error}`);
      return [];
    }
  }

  return {
    getApps,
    getAppSettings,
    saveGeminiApiKey,
  };
}
