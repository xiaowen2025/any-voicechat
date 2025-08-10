<template>
  <v-form>
    <v-text-field
      v-model="editableSettings.app_name"
      label="App Name"
    ></v-text-field>
    <v-textarea
      v-model="editableSettings.agent_description"
      label="Agent Description"
      auto-grow
      rows="2"
    ></v-textarea>

    <h3>Context</h3>
    <div v-for="(value, key) in editableSettings.context_dict" :key="key" class="context-item">
      <v-text-field
        v-model="value.value"
        :label="value.description"
      ></v-text-field>
    </div>

    <v-textarea
      v-model="editableSettings.goal_description"
      label="Goal Description"
      auto-grow
      rows="2"
    ></v-textarea>
    <v-textarea
      v-model="editableSettings.notes_taking_instruction"
      label="Notes Taking Instruction"
      auto-grow
      rows="2"
    ></v-textarea>
    <v-textarea
      v-model="editableSettings.analyse_instruction"
      label="Analyse Instruction"
      auto-grow
      rows="2"
    ></v-textarea>
  </v-form>
</template>

<script>
export default {
  name: 'SettingsForm',
  props: {
    modelValue: {
      type: Object,
      required: true,
    },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      editableSettings: {},
    };
  },
  watch: {
    modelValue: {
      handler(newValue) {
        this.editableSettings = JSON.parse(JSON.stringify(newValue));
      },
      immediate: true,
      deep: true,
    },
    editableSettings: {
      handler(newValue) {
        this.$emit('update:modelValue', newValue);
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.context-item {
  margin-bottom: 16px;
}
</style>
