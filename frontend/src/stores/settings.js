import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref(null);
  const currentTheme = ref(localStorage.getItem('theme') || 'Default');
  const darkMode = ref(localStorage.getItem('darkMode') === 'true');

  function setTheme(theme, newTheme) {
    currentTheme.value = newTheme;
    localStorage.setItem('theme', newTheme);
    theme.global.name.value = darkMode.value ? `${newTheme}Dark` : newTheme;
  }

  function setDarkMode(theme, isDark) {
    darkMode.value = isDark;
    localStorage.setItem('darkMode', isDark);
    theme.global.name.value = isDark ? `${currentTheme.value}Dark` : currentTheme.value;
  }

  async function loadSettings() {
    const cachedSettings = localStorage.getItem('settings');
    if (cachedSettings) {
      settings.value = JSON.parse(cachedSettings);
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
    currentTheme,
    darkMode,
    loadSettings,
    updateSettings,
    setTheme,
    setDarkMode,
  };
});
