import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import { useSettingsStore } from './stores/settings';
import './styles/main.scss';

async function initializeApp() {
  const app = createApp(App);
  const pinia = createPinia();
  app.use(pinia);

  const settingsStore = useSettingsStore();
  const themeName = settingsStore.darkMode ? `${settingsStore.currentTheme}Dark` : settingsStore.currentTheme;
  vuetify.theme.global.name.value = themeName;

  app.use(vuetify);
  app.mount('#app');
}

initializeApp();

