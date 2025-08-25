import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useApi } from '../services/useApi';

export const useAppsStore = defineStore('apps', () => {
  const { getApps } = useApi();
  const apps = ref([]);
  const loading = ref(false);
  const error = ref(null);

  async function fetchApps() {
    loading.value = true;
    error.value = null;
    try {
      apps.value = await getApps();
    } catch (e) {
      error.value = e;
    } finally {
      loading.value = false;
    }
  }

  const appNames = computed(() => apps.value.map(app => app.name));

  return {
    apps,
    loading,
    error,
    fetchApps,
    appNames,
  };
});
