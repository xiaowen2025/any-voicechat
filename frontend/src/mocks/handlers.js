import { http, HttpResponse } from 'msw';

export const handlers = [
  // Mock for getAppSettings
  http.get('/api/apps/:appId/settings', (req, res, ctx) => {
    const { appId } = req.params;
    console.log(`Intercepted GET /api/apps/${appId}/settings`);
    return HttpResponse.json({
      app_id: appId,
      app_name: `Mock App ${appId}`,
      logo: '/mock-logo.png',
      description: 'This is a mock application.',
      assistant_instructions: 'You are a mock assistant.',
      gemini_api_key: 'mock_api_key',
    });
  }),

  // Mock for saveGeminiApiKey
  http.post('/api/verify_api_key', (req, res, ctx) => {
    console.log('Intercepted POST /api/verify_api_key');
    const { key } = req.body;
    if (key === 'valid-key') {
      return HttpResponse.json({ status: 'success' });
    } else {
      return HttpResponse.json({ status: 'error', message: 'Invalid API Key' });
    }
  }),
];
