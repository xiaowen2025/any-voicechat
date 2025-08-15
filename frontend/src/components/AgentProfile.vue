<template>
  <div class="d-flex flex-column align-center justify-center pa-3">
    <v-avatar class="agent-avatar mb-4 w-100" rounded="lg" @click="openAvatarEditor">
      <v-img :src="currentAvatar" aspect-ratio="1.33" contain></v-img>
    </v-avatar>
    <div ref="visualizer" class="visualizer"></div>
    <AvatarEditor v-model="avatarEditorDialog" @avatar-saved="onAvatarSaved" />
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount, computed } from 'vue';
import { storeToRefs } from 'pinia';
import WaveSurfer from 'wavesurfer.js';
import RecordPlugin from 'wavesurfer.js/dist/plugins/record.esm.js';
import { useTheme } from 'vuetify';
import AvatarEditor from './AvatarEditor.vue';
import { useConversationStore } from '../stores/conversation';

const props = defineProps({
  analyserNode: {
    type: Object,
    default: null,
  },
  conversationStarted: {
    type: Boolean,
    default: false,
  },
});

const theme = useTheme();
const conversationStore = useConversationStore();
const { currentAvatar } = storeToRefs(conversationStore);
const avatarEditorDialog = ref(false);
const visualizer = ref(null);
const wavesurfer = ref(null);
const record = ref(null);

const primaryColor = computed(() => theme.current.value.colors.primary);

function openAvatarEditor() {
  avatarEditorDialog.value = true;
}

function onAvatarSaved(newAvatar) {
  currentAvatar.value = newAvatar;
  localStorage.setItem('userAvatar', newAvatar);
  avatarEditorDialog.value = false;
}

const initializeVisualizer = () => {
  if (!visualizer.value) return;

  wavesurfer.value = WaveSurfer.create({
    container: visualizer.value,
    waveColor: primaryColor.value,
    progressColor: primaryColor.value,
    height: 60,
    barWidth: 2,
    barGap: 3,
    barRadius: 2,
    cursorWidth: 0,
  });

  record.value = wavesurfer.value.registerPlugin(RecordPlugin.create());

  record.value.on('record-start', () => {
    console.log('Recording started');
  });

  record.value.on('record-end', () => {
    console.log('Recording stopped');
  });

  record.value.startMic();
};

const destroyVisualizer = () => {
  if (record.value) {
    record.value.stopMic();
  }
  if (wavesurfer.value) {
    wavesurfer.value.destroy();
    wavesurfer.value = null;
  }
};

watch(() => props.conversationStarted, (newValue) => {
  if (newValue) {
    initializeVisualizer();
  } else {
    destroyVisualizer();
  }
});

watch(primaryColor, () => {
  if (wavesurfer.value) {
    wavesurfer.value.setOptions({
      waveColor: primaryColor.value,
      progressColor: primaryColor.value,
    });
  }
});

onBeforeUnmount(() => {
  destroyVisualizer();
});
</script>

<style lang="scss" scoped>
.agent-avatar {
  max-width: 400px;
  height: auto;
  cursor: pointer;
}

.visualizer {
  width: 125px;
  height: 50px;
  margin-bottom: 1rem;
}
</style>
