import { createApp } from 'vue'
import App from './App.vue'
import createCustomVuetify from './plugins/vuetify'
import { themes as customThemes } from './themes';

async function initializeApp() {
  let config;
  try {
    const response = await fetch('/config.json');
    config = await response.json();
  } catch (error) {
    console.error('Error loading config:', error);
    // Fallback to default config
    config = {
      title: "App",
    };
  }

  const app = createApp(App);

  const availableThemes = Object.keys(customThemes);
  let theme = localStorage.getItem('theme') || 'Default';
  if (!availableThemes.includes(theme)) {
    theme = 'Default';
    localStorage.setItem('theme', theme);
  }
  const darkMode = localStorage.getItem('darkMode') === 'true';
  const themeName = darkMode ? `${theme}Dark` : theme;
  const vuetify = createCustomVuetify(themeName);

  app.provide('config', config);
  app.use(vuetify);
  app.mount('#app');
}

initializeApp();

