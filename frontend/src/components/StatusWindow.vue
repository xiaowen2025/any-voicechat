<template>
  <div class="flex-grow-1">
    <div class="notes-container" ref="notesContainer">
      <div v-for="message in messages" :key="message.id" :class="`message ${message.sender}`">
        <pre>{{ message.text }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatusWindow',
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
  watch: {
    messages: {
      handler() {
        this.$nextTick(() => {
          const container = this.$refs.notesContainer;
          if (container) container.scrollTop = container.scrollHeight;
        });
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.notes-container {
  width: 100%;
  margin: 0 auto;
  border: none;
  padding: 0;
  text-align: left;
  height: 100px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
}

.message.user {
  align-self: flex-end;
  background-color: #dcf8c6;
  color: #000;
}

.message.agent {
  align-self: flex-start;
  background-color: #f1f0f0;
  color: #000;
}

.message.system {
  align-self: center;
  color: gray;
  font-style: italic;
}

pre {
  white-space: pre-wrap;
  font-family: inherit;
}
</style>
