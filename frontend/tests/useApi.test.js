import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useApi } from '../src/services/useApi';
import { useSettingsStore } from '../src/stores/settings';

describe('useApi', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('getAppSettings should return mock data', async () => {
    const api = useApi();
    const settingsStore = useSettingsStore();
    const data = await api.getAppSettings('test-app');

    expect(data).toEqual({
      app_id: 'test-app',
      app_name: 'Mock App test-app',
      logo: '/mock-logo.png',
      description: 'This is a mock application.',
      assistant_instructions: 'You are a mock assistant.',
      gemini_api_key: 'mock_api_key',
    });
  });
});
