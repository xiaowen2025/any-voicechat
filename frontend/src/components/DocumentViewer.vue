<template>
  <v-expansion-panel>
    <v-expansion-panel-title class="font-weight-bold">{{ title }}</v-expansion-panel-title>
    <v-expansion-panel-text>
      <div v-if="!editing" @click="editing = true" class="editable-content">
        <div v-html="renderedMarkdown"></div>
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
    content: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      editableContent: this.content,
      editing: false,
    };
  },
  computed: {
    renderedMarkdown() {
      return md.render(this.content);
    },
  },
  watch: {
    content(newContent) {
      this.editableContent = newContent;
    },
  },
  methods: {
    async save() {
      try {
        const response = await fetch(`/api/result_docs/${this.docName}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ content: this.editableContent }),
        });
        if (response.ok) {
          this.$emit('update:content', this.editableContent);
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

<style scoped>
.editable-content {
  cursor: pointer;
}
</style>