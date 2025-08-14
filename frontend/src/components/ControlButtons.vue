<template>
  <div class="d-flex flex-column align-center justify-center">
    <v-btn
      :disabled="isConnecting || isAnalysing"
      :loading="isConnecting || isAnalysing"
      :color="buttonColor"
      @click="handleClick"
      icon
      size="x-large"
      class="mb-2"
    >
      <v-icon size="x-large">{{ buttonIcon }}</v-icon>
    </v-btn>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../stores/conversation';

const conversationStore = useConversationStore();
const {
  notes,
  conversationStarted,
  isConnecting,
  isAnalysing,
} = storeToRefs(conversationStore);

const emit = defineEmits(['toggle-conversation', 'analyse']);

const hasContent = computed(() => notes.value && notes.value.length > 0);

const buttonIcon = computed(() => {
  if (conversationStarted.value) {
    return 'mdi-stop';
  }
  if (hasContent.value && !conversationStarted.value) {
    return 'mdi-thought-bubble-outline';
  }
  return 'mdi-microphone';
});

const buttonColor = computed(() => {
  if (conversationStarted.value) {
    return 'error';
  }
  if (hasContent.value && !conversationStarted.value) {
    return 'secondary';
  }
  return 'primary';
});

const handleClick = () => {
  if (conversationStarted.value) {
    emit('toggle-conversation');
  } else if (hasContent.value) {
    emit('analyse');
  } else {
    emit('toggle-conversation');
  }
};
</script>
