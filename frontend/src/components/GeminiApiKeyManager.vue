<template>
  <div>
    <v-text-field
      :model-value="geminiApiKey"
      @update:model-value="$emit('update:geminiApiKey', $event)"
      :type="showGeminiApiKey ? 'text' : 'password'"
      label="Gemini API Key"
      outlined
      dense
      class="mb-2"
      @focus="$emit('update:apiKeyEdited', true)"
    >
      <template v-slot:append>
        <v-icon @click="showGeminiApiKey = !showGeminiApiKey">
          {{ showGeminiApiKey ? 'mdi-eye-off' : 'mdi-eye' }}
        </v-icon>
      </template>
    </v-text-field>
    <v-btn v-if="apiKeyEdited" @click="$emit('save-api-key')" class="mb-4 fancy-btn" size="large" rounded="lg">Save API Key</v-btn>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'GeminiApiKeyManager',
  props: {
    geminiApiKey: String,
    apiKeyEdited: Boolean,
  },
  emits: ['update:geminiApiKey', 'update:apiKeyEdited', 'save-api-key'],
  setup() {
    const showGeminiApiKey = ref(false);

    return {
      showGeminiApiKey,
    };
  },
};
</script>

<style scoped>
.fancy-btn {
  background: linear-gradient(45deg, #972408 30%, #fa9256 90%);
  color: white !important;
  box-shadow: 0 3px 5px 2px rgba(255, 105, 135, .3);
}
</style>
