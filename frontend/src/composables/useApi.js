import { ref } from 'vue';
import { useSettings } from './useSettings';

export function useApi() {
  const { loadSettings, getContext, updateContext: updateSettingsContext } = useSettings();
  const context = ref({});

  async function loadContext() {
    loadSettings();
    context.value = getContext();
  }

  async function updateContext(contextName, content) {
    updateSettingsContext(contextName, content);
    context.value[contextName].value = content;
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

  return {
    context,
    loadContext,
    updateContext,
    saveGeminiApiKey,
  };
}
