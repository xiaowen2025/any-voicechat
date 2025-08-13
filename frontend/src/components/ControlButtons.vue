<template>
  <div class="d-flex flex-column align-center justify-center">
    <v-btn
      :disabled="isConnecting || isAnalysing"
      :loading="isConnecting"
      :color="conversationStarted ? 'error' : 'primary'"
      @click="$emit('toggle-conversation')"
      icon
      size="x-large"
      class="mb-2"
    >
      <v-icon size="x-large">{{ conversationStarted ? 'mdi-stop' : 'mdi-microphone' }}</v-icon>
    </v-btn>
    <v-btn
      v-if="conversationFinished"
      :disabled="isAnalysing"
      :loading="isAnalysing"
      @click="$emit('analyse')"
      color="secondary"
      class="mt-2"
    >
      Analyse
    </v-btn>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../stores/conversation';

const conversationStore = useConversationStore();
const {
  conversationStarted,
  conversationFinished,
  isConnecting,
} = storeToRefs(conversationStore);

defineProps({
  isAnalysing: Boolean,
});

defineEmits(['toggle-conversation', 'analyse']);
</script>
