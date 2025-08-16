# Frontend Decoupling and Testing Strategy

This document outlines the investigation and solution for decoupling the frontend from the backend to make it fully testable.

## 1. The Problem: Tightly Coupled Frontend

The frontend was making direct API calls to the backend using `fetch` in the `src/services/useApi.js` composable. The Vite development server was configured to proxy requests from `/api` to a live backend running on `localhost:8000`.

This setup had several disadvantages:

*   **Difficult to Test:** Unit and component tests that relied on API data could not be run without a running backend.
*   **Brittle Tests:** Tests could fail due to backend issues, network problems, or data inconsistencies, making them unreliable.
*   **Slow Tests:** Network requests make tests slow.
*   **Difficult Development:** Frontend developers needed to run the backend to work on components that fetched data.

## 2. The Investigation: Identifying the Coupling

The investigation process involved the following steps:

1.  **`ls -F frontend/`**: Revealed a standard Vue project structure with `package.json`, `vite.config.js`, and a `src` directory.
2.  **`read_file("frontend/package.json")`**: Showed the use of `vite`, `vitest`, and `vue`.
3.  **`read_file("frontend/vite.config.js")`**: The `server.proxy` configuration confirmed that `/api` requests were being forwarded to `http://localhost:8000`. This was the primary source of the coupling.
4.  **`ls -F frontend/src`**: The directory structure suggested that API calls would likely be in a `services` directory.
5.  **`read_file("frontend/src/services/useApi.js")`**: This file contained the `fetch` calls to the backend, confirming how the frontend was making API requests.

## 3. The Solution: Mock Service Worker (msw)

To decouple the frontend from the backend for testing, we introduced **Mock Service Worker (`msw`)**. `msw` is an API mocking library that uses a Service Worker to intercept outgoing requests from the browser.

The implementation involved the following steps:

1.  **Installed `msw`**: Added `msw` as a dev dependency.
    ```bash
    npm install msw --save-dev
    ```

2.  **Created Mock Handlers**: Created `frontend/src/mocks/handlers.js` to define the mock API endpoints and their responses.

    ```javascript
    // frontend/src/mocks/handlers.js
    import { http, HttpResponse } from 'msw';

    export const handlers = [
      http.get('/api/apps/:appId/settings', (req, res, ctx) => {
        // ... returns mock data
      }),
      http.post('/api/verify_api_key', (req, res, ctx) => {
        // ... returns mock data
      }),
    ];
    ```

3.  **Created a Mock Server**: Created `frontend/src/mocks/server.js` to set up the mock server for Node.js environments (like Vitest).

    ```javascript
    // frontend/src/mocks/server.js
    import { setupServer } from 'msw/node';
    import { handlers } from './handlers';

    export const server = setupServer(...handlers);
    ```

4.  **Integrated with Vitest**:
    *   Created `frontend/tests/setup.js` to start the mock server before tests run and clean up afterward.
    *   Modified `frontend/vitest.config.js` to use the `setup.js` file.

## 4. How to Write Tests with Mocked APIs

With this setup, writing tests for components that fetch data is now straightforward.

### Adding New Mock Handlers

If you have a new API endpoint to test, add a new handler to `frontend/src/mocks/handlers.js`.

### Writing the Test

In your test file, you can now call the API-dependent code, and `msw` will intercept the request and return the mock data you defined.

Here's the example test for `useApi.js`:

```javascript
// frontend/tests/useApi.test.js
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useApi } from '../src/services/useApi';

describe('useApi', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('getAppSettings should return mock data', async () => {
    const api = useApi();
    const data = await api.getAppSettings('test-app');

    expect(data.app_name).toBe('Mock App test-app');
  });
});
```

This test runs without a backend, is fast, and is reliable.
