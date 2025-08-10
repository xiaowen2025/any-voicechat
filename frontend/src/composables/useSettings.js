import { ref } from 'vue';

export function useSettings() {
  const settings = ref(null);

  async function loadSettings() {
    const cachedSettings = localStorage.getItem('settings');
    if (cachedSettings) {
      settings.value = JSON.parse(cachedSettings);
      return;
    }
    try {
      const response = await fetch('/api/settings');
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
