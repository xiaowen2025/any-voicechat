import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
  const isApiKeySet = ref(false);

  async function setApiKey() {
    const apiKey = localStorage.getItem('geminiApiKey');
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
          isApiKeySet.value = true;
          console.log('API key set successfully');
        } else {
          isApiKeySet.value = false;
          console.error('Failed to set API key:', data.message);
        }
      } catch (error) {
        isApiKeySet.value = false;
        console.error('Error setting API key:', error);
      }
    } else {
      isApiKeySet.value = false;
    }
  }

  return {
    isApiKeySet,
    setApiKey,
  };
});
