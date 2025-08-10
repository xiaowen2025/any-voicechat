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

<script>
import MarkdownIt from 'markdown-it';

export default {
  name: 'NotesWindow',
  components: {

  },
  props: {
    content: {
      type: String,
      default: ''
    }
  },
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
        const response = await fetch('/api/result_docs/notes');
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
        await fetch('/api/result_docs/notes', {
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
.notes-window {
  margin: 2px 0;
}

.notes-content {
  font-size: 1.2rem;
  line-height: 1.6;
}
</style>
