<template>
  <v-card-actions class="pa-4 justify-center">
    <v-btn
      @click="$emit('toggle-interview')"
      :color="interviewStarted ? 'red' : 'primary'"
      :disabled="isConnecting"
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

      {{ interviewStarted ? 'Stop Interview' : 'Start' }}
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
    isConnecting: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['toggle-interview'],
};
</script>
