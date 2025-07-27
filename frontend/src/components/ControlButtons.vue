<template>
  <v-card-actions class="justify-center">
    <v-btn @click="$emit('toggle-interview')" :color="interviewStarted ? 'red' : 'primary'" :disabled="isConnecting">
      <v-progress-circular indeterminate v-if="isConnecting" size="20" class="mr-2"></v-progress-circular>
      {{ interviewStarted ? 'Stop Interview' : 'Start Mock Interview' }}
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
