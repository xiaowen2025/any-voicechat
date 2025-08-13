import { ref } from 'vue';

// Create a single, shared state for settings
const settings = ref(null);

export function useSettings() {

  async function loadSettings(forceRefresh = false) {
    const cachedSettings = localStorage.getItem('settings');
    if (cachedSettings && !forceRefresh) {
      settings.value = JSON.parse(cachedSettings);
    } else {
      try {
        const response = await fetch('/api/apps/language_pal/settings', {
          method: 'GET',
        });
        const data = await response.json();
        if (response.ok) {
          settings.value = data;
        } else {
          console.error('Error fetching settings:', data.error);
          settings.value = {}; // Initialize to avoid errors
        }
      } catch (error) {
        console.error('Error fetching settings:', error);
        settings.value = {}; // Initialize to avoid errors
      }
    }

    // One-time migration for geminiApiKey from localStorage
    if (settings.value && !settings.value.gemini_api_key) {
      const oldApiKey = localStorage.getItem('geminiApiKey');
      if (oldApiKey) {
        settings.value.gemini_api_key = oldApiKey;
        localStorage.setItem('settings', JSON.stringify(settings.value));
        localStorage.removeItem('geminiApiKey');
      }
    }
  }

  async function updateSettings(newSettings) {
    settings.value = newSettings;
    localStorage.setItem('settings', JSON.stringify(newSettings));
  }

  return {
    settings,
    loadSettings,
    updateSettings,
  };
}
