import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import './styles/main.scss';
import { useSettingsStore } from '@/stores/settings';

async function initializeApp() {
  const app = createApp(App);
  const pinia = createPinia();
  app.use(pinia);

  const settingsStore = useSettingsStore(pinia);
  const themeName = settingsStore.currentTheme;
  const darkMode = settingsStore.darkMode;
  vuetify.theme.global.name.value = darkMode ? `${themeName}Dark` : themeName;

  app.use(vuetify);
  app.mount('#app');
}

initializeApp();

