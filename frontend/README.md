# Frontend 

## Core Frontend Stack

The frontend is built on a modern, Vue-based stack. Here are the core technologies used:

- **[Vue 3](https://vuejs.org/)**: The progressive JavaScript framework used for building the user interface. We use the Composition API with `<script setup>` syntax for better organization and code reuse.

- **[Vite](https://vitejs.dev/)**: The build tool and development server. Vite provides a faster and leaner development experience compared to other bundlers like Webpack.

- **[Vuetify 3](https://vuetifyjs.com/)**: A Material Design component framework for Vue. It provides a rich set of pre-built UI components, which helps in rapid development.

- **[Pinia](https://pinia.vuejs.org/)**: The official state management library for Vue.js. It's used to manage the application's global state in a centralized and predictable way.

- **[Vitest](https://vitest.dev/)**: A fast and simple testing framework for Vite projects. It's used for writing and running unit tests for our components, stores, and composables.  
# Frontend Documentation

This document provides a comprehensive overview of the frontend application, including its structure, core technologies, and main purpose.

## Main Purpose

The frontend is a sophisticated, single-page web application designed to provide a user-friendly interface for interacting with various AI agents. It's built as a chat application where users can select from different "apps" (pre-configured AI agents for specific tasks like language practice or interview simulation), engage in conversations, and manage their settings.

Key features include:
- **App Gallery**: A selection screen to choose from different AI agents.
- **Real-time Conversation**: A chat interface for text-based interaction with the selected agent.
- **Audio I/O**: The application supports voice input and can play back audio responses, using `wavesurfer.js` for waveform visualization.
- **User Profile & Settings**: Users can manage their API key and customize their experience (e.g., avatar, theme).
- **Context & Notes**: Features to view conversation metadata and take personal notes during a chat.
- **Responsive Design**: The UI is built with Vuetify, ensuring it works well across different screen sizes.

## 1. Structure

The project is organized into a logical and maintainable structure. Below is a detailed view of the file tree with annotations explaining the purpose of each directory and important file.

```
frontend/
├── .gitignore             # Specifies intentionally untracked files to ignore.
├── README.md              # The original README with project setup and overview.
├── FRONTEND_DOCS.md       # This documentation file.
├── index.html             # The main HTML entry point for the application.
├── package.json           # Lists project dependencies and npm scripts.
├── package-lock.json      # Records exact versions of dependencies for reproducible builds.
├── public/                # Static assets that are not processed by the build tool.
│   ├── assets/            # Images, icons, and other static resources.
│   │   ├── avatar_casual_chat.png
│   │   ├── avatar_interview_simulator.png
│   │   ├── avatar_language_pal.png
│   │   └── avatar_story_architect.png
│   ├── favicon.ico        # Application icon for the browser tab.
│   ├── pcm-player-processor.js  # AudioWorkletProcessor for playing raw PCM audio.
│   └── pcm-recorder-processor.js # AudioWorkletProcessor for recording audio.
├── src/                   # Contains the main application source code.
│   ├── App.vue            # The root Vue component of the application.
│   ├── components/        # Reusable Vue components that form the UI.
│   │   ├── AgentProfile.vue   # Component to display the AI agent's profile.
│   │   ├── AppsGallery.vue    # Component for the app selection screen.
│   │   ├── AvatarEditor.vue   # A tool for cropping and editing user avatars.
│   │   ├── ContextViewer.vue  # Displays context or metadata about the conversation.
│   │   ├── ControlButtons.vue # UI buttons for actions like record, stop, etc.
│   │   ├── ConversationView.vue # The main chat window component.
│   │   ├── NotesWindow.vue    # A window for users to take notes.
│   │   ├── SettingsSidebar.vue # A sidebar for application settings.
│   │   └── SettingsWindow.vue   # A dedicated window for settings.
│   ├── composables/       # Vue Composition API functions for reusable stateful logic.
│   │   ├── audio/         # Logic related to audio recording and playback.
│   │   │   ├── useAudio.js  # Composable for managing audio state.
│   │   │   └── utils.js     # Utility functions for audio processing.
│   │   ├── useResizableDrawer.js # Logic for making drawer components resizable.
│   │   └── useSnackbar.js     # Composable for showing notification snackbars.
│   ├── main.js            # The entry point where the Vue app is initialized.
│   ├── mocks/             # Mock Service Worker handlers for API mocking during tests.
│   │   ├── handlers.js    # Defines the mock API endpoints and responses.
│   │   └── server.js      # Sets up the MSW server for Node.js environments (testing).
│   ├── plugins/           # Vue plugins.
│   │   └── vuetify.js     # Initializes and configures the Vuetify framework.
│   ├── services/          # Services for external interactions, like API calls.
│   │   └── useApi.js      # A composable for interacting with the backend API.
│   ├── stores/            # Pinia stores for global state management.
│   │   ├── conversation.js # Manages conversation state (messages, status).
│   │   ├── settings.js    # Manages application-wide settings (theme, agent config).
│   │   └── user.js        # Manages user-specific data (API key).
│   ├── styles/            # Global stylesheets.
│   │   ├── _base.scss     # Base styles and variables.
│   │   └── main.scss      # Main SASS file that imports all other styles.
│   └── themes.js          # Defines custom color themes for Vuetify.
├── start_servers.sh       # Script to start the development servers.
├── tests/                 # Contains all the application tests.
│   ├── setup.js           # Setup file for tests (e.g., starting the mock server).
│   ├── stores/            # Unit tests for Pinia stores.
│   │   ├── conversation.test.js
│   │   └── settings.test.js
│   └── useApi.test.js     # Unit test for the API service.
├── vite.config.js         # Configuration file for Vite (the build tool).
└── vitest.config.js       # Configuration file for Vitest (the testing framework).
```

## 2. Core Stacks

This section describes the core frameworks and libraries that power the frontend. For each technology, we explain its role, provide a code example from this project, and discuss potential alternatives.

---

### Vue.js (v3)

-   **Role**: Vue.js is the foundational JavaScript framework used for building the entire user interface. This project uses the Composition API with the `<script setup>` syntax, which allows for more organized, reusable, and scalable component logic.

-   **Example (`src/components/ControlButtons.vue`)**: This snippet shows a basic Vue component using the Composition API to handle user interactions.

    ```vue
    <script setup>
    import { computed } from 'vue';
    import { useConversationStore } from '@/stores/conversation';

    const conversationStore = useConversationStore();
    const { isPlaying, isRecording, isFinished } = storeToRefs(conversationStore);

    const handleButtonClick = () => {
      // ... logic
    };
    </script>

    <template>
      <v-btn :disabled="isFinished" @click="handleButtonClick">
        <v-icon>mdi-play</v-icon>
      </v-btn>
    </template>
    ```

-   **Alternatives**:
    -   **React**: A popular library for building UIs, especially for large-scale applications. It has a massive ecosystem but can be more complex to set up than Vue. It would be preferable for projects requiring integration with React-native or for teams already experienced with its JSX-centric development model.
    -   **Svelte**: A compiler that writes efficient, imperative code. It often results in smaller bundle sizes and faster performance. It's a great choice for performance-critical applications or projects where a minimal footprint is essential.
    -   **Angular**: A full-fledged platform for building complex enterprise-scale applications. It is more opinionated than Vue, providing a rigid structure that can be beneficial for very large teams.

---

### Vite

-   **Role**: Vite serves as the build tool and development server. It offers a significantly faster development experience compared to older tools like Webpack by leveraging native ES modules in the browser during development. For production, it bundles assets efficiently using Rollup.

-   **Example (`vite.config.js`)**: The configuration file is simple and declarative.

    ```javascript
    import { defineConfig } from 'vite'
    import vue from '@vitejs/plugin-vue'
    import vuetify from 'vite-plugin-vuetify'

    export default defineConfig({
      plugins: [
        vue(),
        vuetify({ autoImport: true }),
      ],
      // ... other config
    })
    ```

-   **Alternatives**:
    -   **Webpack**: The most established and powerful bundler. It has a vast plugin ecosystem but is notoriously complex to configure. It might be chosen for projects with highly complex build requirements that Vite's plugin ecosystem cannot satisfy.
    -   **Parcel**: A bundler known for its zero-configuration setup. It's extremely easy to get started with and is a good choice for smaller projects or rapid prototyping where minimal configuration is desired.

---

### Vuetify (v3)

-   **Role**: Vuetify is a Material Design component framework for Vue. It provides a large library of pre-built, beautifully designed UI components (buttons, cards, data tables, etc.), which accelerates development by removing the need to build these from scratch.

-   **Example (`src/components/SettingsWindow.vue`)**: This shows how Vuetify components like `v-card` and `v-text-field` are used to quickly build a settings form.

    ```vue
    <template>
      <v-card>
        <v-card-title>Settings</v-card-title>
        <v-card-text>
          <v-text-field
            label="API Key"
            v-model="apiKey"
            type="password"
          ></v-text-field>
        </v-card-text>
      </v-card>
    </template>
    ```

-   **Alternatives**:
    -   **Tailwind CSS**: A utility-first CSS framework that provides low-level utility classes to build custom designs directly in the HTML. It's highly customizable and excellent for projects that require a unique, non-standard UI design.
    -   **BootstrapVue**: A component library based on the popular Bootstrap CSS framework. It's a solid choice for teams already familiar with Bootstrap's grid system and design philosophy.
    -   **Quasar**: A more comprehensive framework that offers components, app extensions, and even tools for building mobile and desktop apps from the same codebase. It's ideal for projects that plan to target multiple platforms.

---

### Pinia

-   **Role**: Pinia is the official state management library for Vue. It provides a centralized store to hold data that needs to be accessed by multiple components across the application. It's lightweight, intuitive, and integrates perfectly with Vue's Composition API.

-   **Example (`src/stores/user.js`)**: Defining a store is straightforward.

    ```javascript
    import { defineStore } from 'pinia';
    import { ref } from 'vue';

    export const useUserStore = defineStore('user', () => {
      const apiKey = ref('');

      function setApiKey(key) {
        apiKey.value = key;
      }

      return { apiKey, setApiKey };
    });
    ```

-   **Alternatives**:
    -   **Vuex**: The previous official state management library for Vue. It's more boilerplate-heavy and less type-safe than Pinia. It's now considered legacy and is generally only used in older Vue 2 projects.
    -   **Vue Composables**: For very simple state management, one could use Vue's own reactivity APIs (`ref`, `reactive`) within a composable function. This avoids adding another dependency but lacks the developer tools and structured approach of Pinia, making it less suitable for complex state.

---

### Vitest

-   **Role**: Vitest is a testing framework designed specifically for Vite projects. It's fast, simple to configure, and provides a Jest-compatible API, making it easy to write unit and integration tests for components, stores, and composables.

-   **Example (`tests/stores/settings.test.js`)**: The test syntax is clean and familiar to anyone who has used Jest.

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

-   **Alternatives**:
    -   **Jest**: The most popular testing framework in the JavaScript ecosystem. While it can be configured to work with Vite, Vitest offers a more seamless and faster integration.
    -   **Cypress**: An end-to-end testing framework that runs tests in a real browser. It's not a direct alternative to Vitest (which is for unit/integration tests), but rather a complementary tool for testing user flows from start to finish.


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
