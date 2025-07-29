<template>
  <v-card-actions class="pa-4 justify-center">
    <v-btn
      v-if="!showAnalyseButton"
      @click="$emit('toggle-interview')"
      :class="{ 'fancy-btn': !interviewStarted }"
      :color="interviewStarted ? 'red' : ''"
      :disabled="isConnecting || !isApiKeySet"
      :loading="isConnecting"
      variant="tonal"
      size="large"
      rounded="lg"
      class="font-weight-bold"
    >
      <template v-slot:prepend>
        <v-icon>{{ interviewStarted ? 'mdi-stop-circle-outline' : 'mdi-play-circle-outline' }}</v-icon>
      </template>
      
      <template v-slot:loader>
        <v-progress-circular indeterminate size="24" width="2"></v-progress-circular>
      </template>

      {{ interviewStarted ? 'Stop Interview' : 'Start Interview' }}
    </v-btn>

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
        <v-icon>mdi-chart-bar</v-icon>
      </template>
      Analyse Interview
    </v-btn>
  </v-card-actions>
</template>

<script>
export default {
  props: {
    interviewStarted: {
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
.fancy-btn {
  background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
  color: white !important;
  box-shadow: 0 3px 5px 2px rgba(255, 105, 135, .3);
}
</style>