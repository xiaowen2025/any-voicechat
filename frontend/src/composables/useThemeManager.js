// frontend/src/composables/useThemeManager.js
import { ref, computed } from 'vue';
import { useTheme } from 'vuetify';
import { themes as customThemes } from '@/themes';

export function useThemeManager() {
  const theme = useTheme();
  const availableThemes = computed(() => Object.keys(customThemes));

  // Load initial values from localStorage or set defaults
  let initialTheme = localStorage.getItem('theme') || 'Default';
  if (!availableThemes.value.includes(initialTheme)) {
    initialTheme = 'Default';
  }
  const selectedTheme = ref(initialTheme);
  const isDarkMode = ref(localStorage.getItem('darkMode') === 'true');

  const applyTheme = () => {
    const themeName = isDarkMode.value ? `${selectedTheme.value}Dark` : selectedTheme.value;
    theme.global.name.value = themeName;
  };

  const changeTheme = (themeName) => {
    if (availableThemes.value.includes(themeName)) {
      selectedTheme.value = themeName;
      localStorage.setItem('theme', themeName);
      applyTheme();
    }
  };

  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value;
    localStorage.setItem('darkMode', String(isDarkMode.value));
    applyTheme();
  };

  const initTheme = () => {
    applyTheme();
  };

  return {
    selectedTheme,
    isDarkMode,
    availableThemes,
    changeTheme,
    toggleDarkMode,
    initTheme,
  };
}
