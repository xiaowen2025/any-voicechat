# Frontend Documentation

This document provides an overview of the files and folders in the `frontend` directory.

## Folders

-   `.vscode/`: Contains Visual Studio Code specific settings, such as recommended extensions (`extensions.json`) and workspace settings (`settings.json`).
-   `public/`: Contains static assets that are directly served to the browser without being processed by the build tool (Vite).
    -   `favicon.ico`: The icon for the website shown in the browser tab.
    -   `pcm-player-processor.js`: An [AudioWorkletProcessor](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorkletProcessor) for playing raw PCM audio data.
    -   `pcm-recorder-processor.js`: An [AudioWorkletProcessor](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorkletProcessor) for recording raw PCM audio data from the microphone.
-   `src/`: Contains the main source code of the Vue.js application.
    -   `assets/`: Contains static assets that are processed by the build tool, such as CSS files and images.
    -   `components/`: Contains reusable Vue components.
    -   `plugins/`: Contains Vue plugins, such as `vuetify.js` for UI components.
    -   `App.vue`: The main root component of the Vue application.
    -   `main.js`: The entry point of the application where the Vue app is initialized.

## Files

-   `.gitignore`: Specifies which files and folders should be ignored by Git.
-   `design.md`: A document describing the design of the frontend.
-   `index.html`: The main HTML file that serves as the entry point for the application.
-   `jsconfig.json`: A configuration file for JavaScript projects in VS Code, providing IntelliSense and other features.
-   `package-lock.json`: Records the exact version of each dependency used in the project, ensuring consistent installations.
-   `package.json`: Defines the project's metadata, dependencies, and scripts.
-   `README.md`: This file, providing documentation for the frontend.
-   `vite.config.js`: The configuration file for Vite, the build tool used for the project.