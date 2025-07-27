
# Frontend
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
