<template>
  <v-expansion-panel>
    <v-expansion-panel-title class="font-weight-bold">
      <div v-if="!titleEditing" class="d-flex align-center" style="width: 100%;">
        <span :class="{ 'editable-title': isEditing }" @click.stop="startTitleEdit">{{ title }}</span>
        <v-spacer></v-spacer>
        <template v-if="isEditing">
          <v-btn icon="mdi-pencil" size="small" variant="text" @click.stop="startTitleEdit"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" @click.stop="remove"></v-btn>
        </template>
      </div>
      <div v-else class="d-flex align-center" style="width: 100%;">
        <v-text-field
          v-model="editableTitle"
          dense
          hide-details
          autofocus
          @keyup.enter="saveTitle"
          @keyup.esc="cancelTitleEdit"
        ></v-text-field>
        <v-btn icon="mdi-check" size="small" variant="text" @click.stop="saveTitle"></v-btn>
        <v-btn icon="mdi-close" size="small" variant="text" @click.stop="cancelTitleEdit"></v-btn>
      </div>
    </v-expansion-panel-title>
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
    isEditing: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:content', 'update:docName', 'remove'],
  data() {
    return {
      editableContent: this.content,
      editing: false,
      titleEditing: false,
      editableTitle: this.title,
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
    title(newTitle) {
      if (!this.titleEditing) {
        this.editableTitle = newTitle;
      }
    },
    isEditing(newVal) {
      if (!newVal) {
        this.titleEditing = false;
      }
    }
  },
  methods: {
    save() {
      this.$emit('update:content', this.editableContent);
      this.editing = false;
    },
    cancel() {
      this.editableContent = this.content;
      this.editing = false;
    },
    startTitleEdit() {
      if (!this.isEditing) return;
      this.editableTitle = this.title;
      this.titleEditing = true;
    },
    saveTitle() {
      const newDocName = this.editableTitle.trim().replace(/\s+/g, '_').toLowerCase();
      const oldDocName = this.docName;
      if (newDocName && newDocName !== oldDocName) {
        this.$emit('update:docName', { oldDocName, newDocName });
      }
      this.titleEditing = false;
    },
    cancelTitleEdit() {
      this.titleEditing = false;
      this.editableTitle = this.title;
    },
    remove() {
      this.$emit('remove', this.docName);
    },
  },
};
</script>

<style scoped>
.editable-content {
  cursor: pointer;
}
.editable-title {
  cursor: pointer;
  flex-grow: 1;
}
</style>