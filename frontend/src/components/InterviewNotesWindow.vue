<template>
  <div class="interview-notes-window">
    <v-card>
      <v-card-title class="font-weight-bold">
        Interview Notes
      </v-card-title>
      <v-card-text>
        <div v-html="renderedMarkdown"></div>
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

<script>
import MarkdownIt from 'markdown-it';

export default {
  name: 'InterviewNotesWindow',
  data() {
    return {
      notes: '',
      intervalId: null,
      md: new MarkdownIt(),
    };
  },
  computed: {
    renderedMarkdown() {
      return this.md.render(this.notes);
    }
  },
  methods: {
    async fetchNotes() {
      try {
        const response = await fetch('/api/documents/interview_note');
        if (response.ok) {
          const data = await response.json();
          this.notes = data.content;
        } else {
          this.notes = '# Could not load notes.';
        }
      } catch (error) {
        console.error('Error fetching interview notes:', error);
        this.notes = '# Error loading notes.';
      }
    },
    async saveNotes() {
      try {
        await fetch('/api/documents/interview_note', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ content: this.notes }),
        });
      } catch (error) {
        console.error('Error saving interview notes:', error);
      }
    },
    async resetNotes() {
      this.notes = '';
      await this.saveNotes();
    },
  },
  created() {
    this.fetchNotes();
    this.intervalId = setInterval(this.fetchNotes, 3000);
  },
  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
};
</script>

<style scoped>
.interview-notes-window {
  margin: 16px 0;
}
</style>
