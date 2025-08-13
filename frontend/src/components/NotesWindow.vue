<template>
  <div class="notes-window">
    <v-card>
      <v-tabs v-model="tab" bg-color="secondary">
        <v-tab value="transcription"><v-icon>mdi-text-box-outline</v-icon></v-tab>
        <v-tab value="analysis"><v-icon>mdi-thought-bubble-outline</v-icon></v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="tab">
          <v-window-item value="transcription">
            <div class="notes-content" v-html="renderedMarkdown"></div>
          </v-window-item>

          <v-window-item value="analysis">
            <div class="notes-content" v-html="renderedAnalysis"></div>
          </v-window-item>
        </v-window>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn icon @click="resetData">
          <v-icon>mdi-restore</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import MarkdownIt from 'markdown-it';
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../stores/conversation';

const conversationStore = useConversationStore();
const { notes, analysis } = storeToRefs(conversationStore);
const md = new MarkdownIt();
const tab = ref('transcription');

const renderedMarkdown = computed(() => {
  return md.render(notes.value);
});

const renderedAnalysis = computed(() => {
  if (analysis.value) {
    return md.render(analysis.value);
  }
  return 'No analysis available yet.';
});

function resetData() {
  notes.value = '';
  analysis.value = null;
}
</script>

<style scoped>
.notes-window {
  margin: 2px 0;
}

.notes-content {
  font-size: 1.2rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
