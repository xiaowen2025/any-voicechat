<template>
  <v-expansion-panel>
    <v-expansion-panel-title>{{ title }}</v-expansion-panel-title>
    <v-expansion-panel-text>
      <div v-if="!editing">
        <div v-html="renderedMarkdown"></div>
        <v-btn @click="editing = true" class="mt-2">Edit</v-btn>
      </div>
      <div v-else>
        <v-textarea v-model="editableContent" rows="10"></v-textarea>
        <v-btn @click="save" class="mr-2">Save</v-btn>
        <v-btn @click="cancel">Cancel</v-btn>
      </div>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<script>
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt();

export default {
  props: {
    docName: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      content: '',
      editableContent: '',
      editing: false,
    };
  },
  computed: {
    renderedMarkdown() {
      return md.render(this.content);
    },
  },
  async created() {
    await this.fetchDocument();
  },
  methods: {
    async fetchDocument() {
      try {
        const response = await fetch(`/api/documents/${this.docName}`);
        const data = await response.json();
        if (response.ok) {
          this.content = data.content;
          this.editableContent = data.content;
        } else {
          this.content = `Error: ${data.error}`;
        }
      } catch (error) {
        this.content = 'Error fetching document.';
        console.error(error);
      }
    },
    async save() {
      try {
        const response = await fetch(`/api/documents/${this.docName}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ content: this.editableContent }),
        });
        if (response.ok) {
          this.content = this.editableContent;
          this.editing = false;
        } else {
          const data = await response.json();
          console.error('Error saving document:', data.error);
        }
      } catch (error) {
        console.error('Error saving document:', error);
      }
    },
    cancel() {
      this.editableContent = this.content;
      this.editing = false;
    },
  },
};
</script>
