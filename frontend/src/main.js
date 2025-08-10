import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { themes as customThemes } from './themes';

async function initializeApp() {
  const app = createApp(App);

  const availableThemes = Object.keys(customThemes);
  let theme = localStorage.getItem('theme') || 'Default';
  if (!availableThemes.includes(theme)) {
    theme = 'Default';
    localStorage.setItem('theme', theme);
  }
  const darkMode = localStorage.getItem('darkMode') === 'true';
  const themeName = darkMode ? `${theme}Dark` : theme;
  vuetify.theme.global.name.value = themeName;

  app.use(vuetify);
  app.mount('#app');
}

initializeApp();

