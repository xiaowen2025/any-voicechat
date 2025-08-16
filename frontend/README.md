# Frontend Documentation

This document provides a comprehensive overview of the frontend architecture, detailing the purpose of each file and directory. It also includes recommendations for future refactoring to enhance maintainability and scalability.

## Folder Structure

Below is a summary of the key directories and files in the `frontend` directory, along with their functions:

-   `node_modules/`: This directory contains all the project's dependencies. It is managed by `npm` or `yarn` and should not be manually edited.
-   `public/`: This directory holds static assets that are directly served to the browser without being processed by the build tool.
    -   `assets/`: This subdirectory contains images and other static assets that are referenced in the `index.html` file.
    -   `favicon.ico`: The icon for the application that appears in the browser tab.
    -   `pcm-player-processor.js`: An `AudioWorkletProcessor` for playing raw PCM audio data.
    -   `pcm-recorder-processor.js`: An `AudioWorkletProcessor` for recording raw PCM audio data from the microphone.
-   `src/`: This directory contains the main source code of the Vue.js application.
    -   `components/`: This directory contains reusable Vue components that make up the user interface.
    -   `composables/`: This directory contains Vue composables, which are functions that encapsulate and reuse stateful logic.
    -   `mocks/`: This directory contains mock API handlers for testing purposes.
    -   `plugins/`: This directory holds Vue plugins, such as `vuetify.js` for UI components.
    -   `services/`: This directory contains services for making API calls.
    -   `stores/`: This directory contains Pinia stores for state management.
    -   `styles/`: This directory contains the application's stylesheets.
    -   `themes.js`: This file defines the custom themes for the application.
    -   `App.vue`: The main root component of the Vue application.
    -   `main.js`: The entry point of the application where the Vue app is initialized.
-   `tests/`: This directory contains the tests for the application. It includes unit tests for stores and composables.

## File Descriptions

-   `index.html`: The main HTML file that serves as the entry point for the application.
-   `package-lock.json`: This file records the exact version of each dependency used in the project, ensuring consistent installations.
-   `package.json`: This file defines the project's metadata, dependencies, and scripts.
-   `start_servers.sh`: This script is used to start the development servers.
-   `vite.config.js`: This file is used to configure Vite, the build tool used for the project.
-   `vitest.config.js`: This file is used to configure Vitest, the test runner used for the project.
-   `tests/setup.js`: This file sets up the mock server before tests run and cleans up afterward.

## Testing

### Frontend Testing Strategy

Run tests:  

```bash
(cd frontend && npm install && npm run test:unit)
```

### Mock Service Worker (msw)

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

### How to Write Tests with Mocked APIs

With this setup, writing tests for components that fetch data is now straightforward.

#### Adding New Mock Handlers

If you have a new API endpoint to test, add a new handler to `frontend/src/mocks/handlers.js`.

#### Writing the Test

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

# Refactor Plan

Component Organization: The frontend/src/components/ directory is currently flat. As more components are added, you might consider creating subdirectories to group related components. For example, SettingsSidebar.vue and SettingsWindow.vue could be moved into a components/settings/ directory.

State Management with Pinia: The conversation.js store is quite large and manages a lot of different states (WebSocket connection, messages, notes, analysis). If this store continues to grow, it could become difficult to manage. Consider splitting it into smaller, more focused stores. For example, you could have a separate store for managing the WebSocket connection.

API Services: The useApi.js service currently handles different types of API calls. As you add more endpoints, this file could grow large. It might be beneficial to split it into multiple services based on the API resources they handle (e.g., an appService.js for app settings and a keyService.js for API key management).

Styling Structure: The styles directory is currently very simple. For a larger application, you might want to adopt a more structured approach for your CSS/SCSS, such as organizing styles by component or using a methodology like BEM (Block, Element, Modifier).