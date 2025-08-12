# Frontend Documentation

This document provides a comprehensive overview of the frontend architecture, detailing the purpose of each file and directory. It also includes recommendations for future refactoring to enhance maintainability and scalability.

## Folder Structure

Below is a summary of the key directories and files in the `frontend` directory, along with their functions:

-   `jules-scratch/`: This directory is used for temporary files and experiments. It is not part of the main application.
-   `node_modules/`: This directory contains all the project's dependencies. It is managed by `npm` or `yarn` and should not be manually edited.
-   `public/`: This directory holds static assets that are directly served to the browser without being processed by the build tool.
    -   `assets/`: This subdirectory contains images and other static assets that are referenced in the `index.html` file.
    -   `favicon.ico`: The icon for the application that appears in the browser tab.
    -   `pcm-player-processor.js`: An `AudioWorkletProcessor` for playing raw PCM audio data.
    -   `pcm-recorder-processor.js`: An `AudioWorkletProcessor` for recording raw PCM audio data from the microphone.
-   `src/`: This directory contains the main source code of the Vue.js application.
    -   `assets/`: This subdirectory holds static assets that are processed by the build tool, such as images and fonts.
    -   `components/`: This directory contains reusable Vue components that make up the user interface.
    -   `composables/`: This directory contains Vue composables, which are functions that encapsulate and reuse stateful logic.
    -   `plugins/`: This directory holds Vue plugins, such as `vuetify.js` for UI components.
    -   `themes.js`: This file defines the custom themes for the application.
    -   `utils/`: This directory contains utility functions that can be used throughout the application.
    -   `App.vue`: The main root component of the Vue application.
    -   `main.js`: The entry point of the application where the Vue app is initialized.
-   `tests/`: This directory contains the tests for the application.
    -   `unit/`: This subdirectory contains the unit tests for the application.

## File Descriptions

-   `.gitignore`: This file specifies which files and directories should be ignored by Git.
-   `index.html`: The main HTML file that serves as the entry point for the application.
-   `jsconfig.json`: This file is used to configure the JavaScript language service provided by Visual Studio Code.
-   `package-lock.json`: This file records the exact version of each dependency used in the project, ensuring consistent installations.
-   `package.json`: This file defines the project's metadata, dependencies, and scripts.
-   `start_servers.sh`: This script is used to start the development servers.
-   `vite.config.js`: This file is used to configure Vite, the build tool used for the project.
-   `vitest.config.js`: This file is used to configure Vitest, the test runner used for the project.

## Refactor Suggestions

Based on best practices, here are some suggestions for refactoring the frontend codebase:

### 1. State Management with Pinia

The current state management is handled through a combination of `localStorage` and component-level state. This can become difficult to manage as the application grows.

**Suggestion:**

-   Introduce **Pinia** as a centralized state management library. Pinia is the officially recommended state management library for Vue 3 and offers a simple and intuitive API.
-   Create separate stores for different domains of the application, such as `settings`, `user`, and `conversation`. This will make the state more predictable and easier to debug.

### 2. Component-Based Styling

The current styling is a mix of global styles and component-specific styles. This can lead to CSS conflicts and make it difficult to maintain the UI.

**Suggestion:**

-   Adopt a more component-based styling approach. Use the `scoped` attribute in Vue components to ensure that styles are only applied to the current component.
-   For global styles, use a more organized approach, such as a dedicated `styles` directory with separate files for variables, mixins, and base styles.

### 3. Improved Code Organization

The `composables` directory is a good start for organizing reusable logic, but it can be further improved.

**Suggestion:**

-   Group related composables into subdirectories. For example, all composables related to audio could be placed in a `composables/audio` directory.
-   Consider creating a `services` directory for API calls and other external services. This will help to separate the business logic from the UI components.

### 4. Consistent Naming Conventions

The naming of some files and components is inconsistent.

**Suggestion:**

-   Establish and follow a consistent naming convention for all files, components, and variables. For example, all components should be named in `PascalCase` and all composables should start with `use`.

### 5. Enhanced Error Handling

The current error handling is basic and could be improved to provide a better user experience.

**Suggestion:**- Implement a more robust error handling strategy. This could include a global error handler that catches all unhandled errors and displays a user-friendly message.
-   Use a logging library, such as `Sentry` or `LogRocket`, to track errors in production and help with debugging.
