<template>
  <v-container fluid class="fill-height pa-4">
    <v-row class="fill-height">
      <v-col cols="12" class="d-flex flex-column">
        <v-card class="flex-grow-1 d-flex flex-column">
          <v-card-text class="flex-grow-1 d-flex flex-column">
            <agent-profile
              :analyser-node="analyserNode"
              :conversation-started="conversationStarted"
            />
            <notes-window />
          </v-card-text>
          <v-card-actions class="d-flex flex-column align-center justify-center">
            <control-buttons
              :conversation-started="conversationStarted"
              :conversation-finished="conversationFinished"
              :is-connecting="isConnecting"
              :is-analysing="isAnalysing"
              @toggle-conversation="$emit('toggle-conversation')"
              @analyse="$emit('analyse')"
            />
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import AgentProfile from './AgentProfile.vue';
import ControlButtons from './ControlButtons.vue';
import NotesWindow from './NotesWindow.vue';

defineProps({
  analyserNode: Object,
  conversationStarted: Boolean,
  conversationFinished: Boolean,
  isConnecting: Boolean,
  isAnalysing: Boolean,
});

defineEmits(['toggle-conversation', 'analyse']);
</script>
