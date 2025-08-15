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
    <div v-if="isMobile && showReminder" class="d-flex align-center">
      <p class="text-caption mr-2">On mobile device, please use earphones.</p>
      <v-btn icon small @click="dismissReminder">
        <v-icon small>mdi-close</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../stores/conversation';
import { useDisplay } from 'vuetify';

// Mobile detection
const { mobile: isMobile } = useDisplay();

const showReminder = ref(false);

onMounted(() => {
  if (localStorage.getItem('hideEarphoneReminder') !== 'true') {
    showReminder.value = true;
  }
});

const dismissReminder = () => {
  localStorage.setItem('hideEarphoneReminder', 'true');
  showReminder.value = false;
};

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
