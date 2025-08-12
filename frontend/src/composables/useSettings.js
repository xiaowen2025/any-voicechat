import { ref } from 'vue';

// Create a single, shared state for settings
const settings = ref(null);

export function useSettings() {

  async function loadSettings(forceRefresh = false) {
    const cachedSettings = localStorage.getItem('settings');
    if (cachedSettings && !forceRefresh) {
      settings.value = JSON.parse(cachedSettings);
      return;
    }
    try {
      const response = await fetch('/api/apps/language_pal/settings', {
        method: 'GET',
      });
      const data = await response.json();
      if (response.ok) {
        settings.value = data;
        localStorage.setItem('settings', JSON.stringify(data));
      } else {
        console.error('Error fetching settings:', data.error);
      }
    } catch (error) {
      console.error('Error fetching settings:', error);
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
