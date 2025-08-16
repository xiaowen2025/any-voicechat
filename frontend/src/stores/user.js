import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
  const isApiKeySet = ref(false);

  async function setApiKey() {
    const apiKey = localStorage.getItem('geminiApiKey');
    if (apiKey) {
      isApiKeySet.value = true;
    } else {
      isApiKeySet.value = false;
    }
  }

  return {
    isApiKeySet,
    setApiKey,
  };
});
