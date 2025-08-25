import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useSettingsStore } from '../../src/stores/settings';
import { useAppsStore } from '../../src/stores/apps';

describe('useSettingsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    // Clear local storage before each test
    localStorage.clear();
  });

  it('should have a null initial settings value', () => {
    const store = useSettingsStore();
    expect(store.settings).toBe(null);
  });

  it('updateSettings should update the settings and localStorage', async () => {
    const store = useSettingsStore();
    const newSettings = { gemini_api_key: 'test-key' };
    await store.updateSettings(newSettings);

    expect(store.settings).toEqual(newSettings);
    expect(localStorage.getItem('settings')).toEqual(JSON.stringify(newSettings));
  });

  it('loadSettings should load settings from localStorage', async () => {
    const settings = { gemini_api_key: 'test-key' };
    localStorage.setItem('settings', JSON.stringify(settings));

    const store = useSettingsStore();
    await store.loadSettings();

    expect(store.settings).toEqual(settings);
  });

  it('loadSettings should migrate geminiApiKey from localStorage', async () => {
    localStorage.setItem('geminiApiKey', 'old-key');
    const settings = { app_name: 'test-app' };
    localStorage.setItem('settings', JSON.stringify(settings));

    const store = useSettingsStore();
    await store.loadSettings();

    expect(store.settings.gemini_api_key).toBe('old-key');
    expect(localStorage.getItem('geminiApiKey')).toBe(null);
  });

  it('saveSettings should handle duplicated app names', async () => {
    const store = useSettingsStore();
    const newSettings = { app_name: 'Test App', agent_description: 'A test agent.' };
    await store.saveSettings(newSettings);

    const expectedId = 'test_app_1';
    expect(localStorage.getItem(expectedId)).toEqual(JSON.stringify(newSettings));
    expect(store.settings).toEqual(newSettings);
  });
});
