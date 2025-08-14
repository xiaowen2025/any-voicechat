<template>
  <div class="notes-window">
    <v-card>
      <v-tabs v-model="activeTab" bg-color="secondary">
        <v-tab value="transcription"><v-icon>mdi-text-box-outline</v-icon></v-tab>
        <v-tab value="analysis"><v-icon>mdi-thought-bubble-outline</v-icon></v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="activeTab">
          <v-window-item value="transcription">
            <div class="notes-content" v-html="renderedMarkdown"></div>
          </v-window-item>

          <v-window-item value="analysis">
            <div
              class="notes-content"
              :class="{ 'shimmer': isAnalysing && !analysis }"
              v-html="renderedAnalysis"
            ></div>
          </v-window-item>
        </v-window>
      </v-card-text>
      <v-card-actions v-if="hasContent">
        <v-btn icon @click="copyContent">
          <v-icon>mdi-content-copy</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn icon @click="resetData">
          <v-icon>mdi-restore</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import MarkdownIt from 'markdown-it';
import { storeToRefs } from 'pinia';
import { useConversationStore } from '../stores/conversation';

const conversationStore = useConversationStore();
const { notes, analysis, isAnalysing, activeTab } = storeToRefs(conversationStore);
const md = new MarkdownIt();

const hasContent = computed(() => {
  return notes.value && notes.value.length > 0;
});

const renderedMarkdown = computed(() => {
  return md.render(notes.value);
});

const renderedAnalysis = computed(() => {
  if (isAnalysing.value && !analysis.value) {
    return `
      <div class="placeholder-line"></div>
      <div class="placeholder-line"></div>
      <div class="placeholder-line"></div>
    `;
  }
  if (analysis.value) {
    return md.render(analysis.value);
  }
  return 'No analysis available yet.';
});

function copyContent() {
  const contentToCopy = activeTab.value === 'transcription' ? notes.value : analysis.value;
  if (contentToCopy) {
    navigator.clipboard.writeText(contentToCopy);
  }
}

function resetData() {
  notes.value = '';
  analysis.value = null;
}
</script>

<style lang="scss" scoped>
.notes-window {
  margin: 2px 0;
}

.notes-content {
  font-size: 1.2rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.shimmer .placeholder-line {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  height: 1.2rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
