import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useAppsStore } from './apps';

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

  async function saveSettings(newSettings) {
    const appsStore = useAppsStore();
    if (appsStore.apps.length === 0) {
      await appsStore.fetchApps();
    }
    const predefinedAppIds = appsStore.apps.map((app) => app.id);

    const toSnakeCase = (str) => str.replace(/\s+/g, '_').toLowerCase();

    const baseId = toSnakeCase(newSettings.app_name);
    let id = baseId;
    let counter = 1;

    const allLocalStorageKeys = Object.keys(localStorage);

    while (predefinedAppIds.includes(id) || allLocalStorageKeys.includes(id)) {
      id = `${baseId}_${counter}`;
      counter++;
    }

    localStorage.setItem(id, JSON.stringify(newSettings));
    settings.value = newSettings;
  }

  async function updateContext(newContextDict) {
    if (settings.value && settings.value.context_dict) {
      const newContext = { ...settings.value.context_dict };
      for (const key in newContextDict) {
        if (Object.prototype.hasOwnProperty.call(newContext, key)) {
          newContext[key].value = newContextDict[key];
        }
      }
      settings.value = { ...settings.value, context_dict: newContext };
      localStorage.setItem('settings', JSON.stringify(settings.value));
    }
  }

  return {
    settings,
    currentTheme,
    darkMode,
    loadSettings,
    updateSettings,
    saveSettings,
    updateContext,
    setTheme,
    setDarkMode,
  };
});
