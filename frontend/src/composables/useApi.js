import { ref } from 'vue';

export function useApi() {
  const context = ref({});

  async function loadContext() {
    try {
      const response = await fetch('/api/context');
      const data = await response.json();
      if (response.ok) {
        context.value = data;
      } else {
        console.error('Error fetching context:', data.error);
      }
    } catch (error) {
      console.error('Error fetching context:', error);
    }
  }

  async function updateContext(contextName, content) {
    try {
      const response = await fetch(`/api/context/${contextName}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: content }),
      });
      const result = await response.json();
      if (response.ok) {
        console.log(`Context '${contextName}' updated.`);
        if (context.value[contextName]) {
          context.value[contextName].value = content;
        }
      } else {
        alert(`Error updating context: ${result.error}`);
      }
    } catch (error) {
      alert(`Error updating context: ${error}`);
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
