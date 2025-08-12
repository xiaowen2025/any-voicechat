<template>
  <div class="notes-window">
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center font-weight-bold">
        <span>Notes</span>
      </v-card-title>
      <v-card-text>
        <div class="notes-content" v-html="renderedMarkdown"></div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn icon @click="resetNotes">
          <v-icon>mdi-restore</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import MarkdownIt from 'markdown-it';
import { useSharedConversation } from '../composables/useSharedConversation';

const { notes } = useSharedConversation();
const md = new MarkdownIt();

const renderedMarkdown = computed(() => {
  return md.render(notes.value);
});

function resetNotes() {
  notes.value = '';
}
</script>

<style scoped>
.notes-window {
  margin: 2px 0;
}

.notes-content {
  font-size: 1.2rem;
  line-height: 1.6;
}
</style>
