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
          return;
        }
      } catch (error) {
        console.error('Error fetching settings:', error);
        return;
      }
    }

    // After loading settings, also load the Gemini API key from local storage
    const geminiApiKey = localStorage.getItem('geminiApiKey');
    if (geminiApiKey) {
      settings.value = { ...settings.value, gemini_api_key: geminiApiKey };
    }
    localStorage.setItem('settings', JSON.stringify(settings.value));
  }

  async function updateSettings(newSettings) {
    settings.value = newSettings;
    localStorage.setItem('settings', JSON.stringify(newSettings));
    if (newSettings.gemini_api_key) {
      localStorage.setItem('geminiApiKey', newSettings.gemini_api_key);
    }
  }

  return {
    settings,
    loadSettings,
    updateSettings,
  };
}
