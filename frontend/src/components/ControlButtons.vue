<template>
  <v-card-actions class="pa-4 justify-center flex-column">
    <v-btn
      v-if="!showAnalyseButton"
      @click="$emit('toggle-interview')"
      :color="conversationStarted ? 'red' : 'primary'"
      :disabled="isConnecting || !isApiKeySet"
      :loading="isConnecting"
      variant="elevated"
      size="x-large"
      fab
    >
      <v-icon>{{ conversationStarted ? 'mdi-stop' : 'mdi-microphone' }}</v-icon>
      
      <template v-slot:loader>
        <v-progress-circular indeterminate size="24" width="2"></v-progress-circular>
      </template>

    </v-btn>

    <v-alert
      v-if="!isApiKeySet && !showAnalyseButton"
      type="info"
      variant="tonal"
      class="mt-4"
      dense
    >
      Please set your Gemini API key in the settings to begin.
    </v-alert>

    <v-btn
      v-if="showAnalyseButton"
      @click="$emit('analyse')"
      :loading="isAnalysing"
      color="primary"
      variant="tonal"
      size="large"
      rounded="lg"
      class="font-weight-bold"
    >
      <template v-slot:prepend>
        <v-icon>mdi-chart-bubble</v-icon>
      </template>
      Analyse
    </v-btn>
  </v-card-actions>
</template>

<script>
export default {
  props: {
    conversationStarted: {
      type: Boolean,
      required: true,
    },
    interviewFinished: {
      type: Boolean,
      required: true,
    },
    isConnecting: {
      type: Boolean,
      required: true,
    },
    isAnalysing: {
      type: Boolean,
      required: true,
    },
    isApiKeySet: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['toggle-interview', 'analyse'],
  computed: {
    showAnalyseButton() {
      return this.interviewFinished;
    }
  },
};
</script>

<style scoped>
</style>
