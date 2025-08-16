# Frontend 

## Core Frontend Stack

The frontend is built on a modern, Vue-based stack. Here are the core technologies used:

- **[Vue 3](https://vuejs.org/)**: The progressive JavaScript framework used for building the user interface. We use the Composition API with `<script setup>` syntax for better organization and code reuse.

- **[Vite](https://vitejs.dev/)**: The build tool and development server. Vite provides a faster and leaner development experience compared to other bundlers like Webpack.

- **[Vuetify 3](https://vuetifyjs.com/)**: A Material Design component framework for Vue. It provides a rich set of pre-built UI components, which helps in rapid development.

- **[Pinia](https://pinia.vuejs.org/)**: The official state management library for Vue.js. It's used to manage the application's global state in a centralized and predictable way.

- **[Vitest](https://vitest.dev/)**: A fast and simple testing framework for Vite projects. It's used for writing and running unit tests for our components, stores, and composables.  

## State Management

We use **[Pinia](https://pinia.vuejs.org/)** for state management. Pinia provides a simple and intuitive API for managing global state. The stores are located in the `src/stores` directory. Each store is responsible for a specific domain of the application's state:

- **`conversation.js`**: Manages the state related to the conversation with the AI agent. This includes:
  - The list of messages in the conversation.
  - The user's notes.
  - The analysis of the conversation.
  - The state of the WebSocket connection.
  - Whether the conversation is in progress, finished, or being analyzed.

- **`settings.js`**: Manages the application's settings. This includes:
  - The current theme (light/dark mode and color scheme).
  - The settings for the currently selected app (e.g., agent's name, persona).

- **`user.js`**: Manages user-specific data. This includes:
  - The user's API key for accessing the backend services.


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


## Stack Examples  

- **[Vue 3](https://vuejs.org/)**: The progressive JavaScript framework for building the user interface. We use the Composition API with `<script setup>` syntax for better organization and code reuse.

  *Example from `frontend/src/App.vue`*:
  ```vue
  <template>
    <v-app>
      <v-app-bar>
        <v-toolbar-title>{{ appName }}</v-toolbar-title>
      </v-app-bar>
      <v-main>
        <!-- ... -->
      </v-main>
    </v-app>
  </template>

  <script setup>
  import { ref } from 'vue';
  const appName = ref('My App');
  </script>
  ```

- **[Vite](https://vitejs.dev/)**: The build tool and development server. It provides a faster and leaner development experience.

  *Example from `frontend/vite.config.js`*:
  ```javascript
  import { defineConfig } from 'vite'
  import vue from '@vitejs/plugin-vue'

  export default defineConfig({
    plugins: [
      vue(),
      // ... other plugins
    ],
  })
  ```

- **[Vuetify 3](https://vuetifyjs.com/)**: A Material Design component framework for Vue. It provides a rich set of pre-built UI components.

  *Example from `frontend/src/App.vue`*:
  ```vue
  <v-btn icon @click="showAppsGallery = !showAppsGallery">
    <v-icon>{{ showAppsGallery ? 'mdi-close' : 'mdi-apps' }}</v-icon>
  </v-btn>
  ```

- **[Pinia](https://pinia.vuejs.org/)**: The official state management library for Vue.js.

  *Defining a store in `frontend/src/stores/settings.js`*:
  ```javascript
  import { defineStore } from 'pinia';
  import { ref } from 'vue';

  export const useSettingsStore = defineStore('settings', () => {
    const settings = ref(null);
    // ...
    return { settings };
  });
  ```

  *Using the store in `frontend/src/App.vue`*:
  ```javascript
  import { useSettingsStore } from './stores/settings';
  const settingsStore = useSettingsStore();
  const { settings } = storeToRefs(settingsStore);
  ```

- **[SCSS/Sass](https://sass-lang.com/)**: A CSS preprocessor for more maintainable stylesheets.

  *Global styles are imported in `frontend/src/main.js`*:
  ```javascript
  import './styles/main.scss';
  ```

- **[Vitest](https://vitest.dev/)**: A fast testing framework for Vite projects.

  *Example from `frontend/tests/stores/settings.test.js`*:
  ```javascript
  import { describe, it, expect, beforeEach } from 'vitest';
  import { setActivePinia, createPinia } from 'pinia';
  import { useSettingsStore } from '../../src/stores/settings';

  describe('useSettingsStore', () => {
    beforeEach(() => {
      setActivePinia(createPinia());
    });

    it('should have a null initial settings value', () => {
      const store = useSettingsStore();
      expect(store.settings).toBe(null);
    });
  });
  ```
