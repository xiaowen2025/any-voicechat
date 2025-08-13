<template>
  <div class="d-flex flex-column align-center justify-center pa-3">
    <v-avatar class="mb-4 w-100" style="max-width: 400px; height: auto; cursor: pointer;" rounded="lg" @click="openAvatarEditor">
      <v-img :src="currentAvatar" aspect-ratio="1.33" contain></v-img>
    </v-avatar>
    <canvas ref="visualizer" width="125" height="50"></canvas>
    <AvatarEditor v-model="avatarEditorDialog" @avatar-saved="onAvatarSaved" />
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';
import { storeToRefs } from 'pinia';
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

const conversationStore = useConversationStore();
const { currentAvatar } = storeToRefs(conversationStore);
const visualizerAnimationId = ref(null);
const avatarEditorDialog = ref(false);
const visualizer = ref(null);

function openAvatarEditor() {
  avatarEditorDialog.value = true;
}

function onAvatarSaved(newAvatar) {
  currentAvatar.value = newAvatar;
  localStorage.setItem('userAvatar', newAvatar);
  avatarEditorDialog.value = false;
}

function drawVisualizer() {
  const canvas = visualizer.value;
  if (!canvas || !props.analyserNode) return;
  const canvasCtx = canvas.getContext('2d');
  const bufferLength = props.analyserNode.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  const draw = () => {
    if (!props.conversationStarted) {
      canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
      return;
    }
    visualizerAnimationId.value = requestAnimationFrame(draw);
    props.analyserNode.getByteFrequencyData(dataArray);
    canvasCtx.fillStyle = 'rgb(240, 240, 240)';
    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
    const barWidth = (canvas.width / bufferLength) * 2.5;
    let barHeight;
    let x = 0;
    for (let i = 0; i < bufferLength; i++) {
      barHeight = dataArray[i] / 2;
      canvasCtx.fillStyle = `rgb(66, 165, 245)`;
      canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
      x += barWidth + 1;
    }
  };
  draw();
}

function stopVisualizer() {
  if (visualizerAnimationId.value) {
    cancelAnimationFrame(visualizerAnimationId.value);
    visualizerAnimationId.value = null;
    const canvas = visualizer.value;
    if (canvas) {
      const canvasCtx = canvas.getContext('2d');
      canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
    }
  }
}

watch(() => props.conversationStarted, (newValue) => {
  if (newValue) {
    drawVisualizer();
  } else {
    stopVisualizer();
  }
});

watch(() => props.analyserNode, (newNode) => {
  if (props.conversationStarted && newNode) {
    drawVisualizer();
  }
});

onBeforeUnmount(() => {
  stopVisualizer();
});
</script>
