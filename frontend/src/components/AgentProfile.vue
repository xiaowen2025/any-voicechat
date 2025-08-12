<template>
  <div class="d-flex flex-column align-center justify-center pa-3">
    <v-avatar class="mb-4" rounded="lg" @click="openAvatarEditor" style="cursor: pointer; width: 400px; height: 300px;">
      <v-img :src="currentAvatar" contain></v-img>
    </v-avatar>
    <canvas ref="visualizer" width="125" height="50"></canvas>
    <AvatarEditor v-model="avatarEditorDialog" @avatar-saved="onAvatarSaved" />
  </div>
</template>

<script>
import defaultAvatar from '../assets/agent-avatar.svg';
import AvatarEditor from './AvatarEditor.vue';

export default {
  components: {
    AvatarEditor,
  },
  props: {
    analyserNode: {
      type: Object,
      default: null,
    },
    conversationStarted: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      currentAvatar: defaultAvatar,
      visualizerAnimationId: null,
      avatarEditorDialog: false,
    };
  },
  watch: {
    conversationStarted(newValue) {
      if (newValue) {
        this.drawVisualizer();
      } else {
        this.stopVisualizer();
      }
    },
    analyserNode(newNode) {
        if (this.conversationStarted && newNode) {
            this.drawVisualizer();
        }
    }
  },
  mounted() {
    this.loadAvatar();
  },
  methods: {
    openAvatarEditor() {
      this.avatarEditorDialog = true;
    },
    loadAvatar() {
      const savedAvatar = localStorage.getItem('userAvatar');
      if (savedAvatar) {
        this.currentAvatar = savedAvatar;
      }
    },
    onAvatarSaved(newAvatar) {
      this.currentAvatar = newAvatar;
      this.avatarEditorDialog = false;
    },
    drawVisualizer() {
      const canvas = this.$refs.visualizer;
      if (!canvas || !this.analyserNode) return;
      const canvasCtx = canvas.getContext('2d');
      const bufferLength = this.analyserNode.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const draw = () => {
        if (!this.conversationStarted) {
          canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
          return;
        }
        this.visualizerAnimationId = requestAnimationFrame(draw);
        this.analyserNode.getByteFrequencyData(dataArray);
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
    },
    stopVisualizer() {
      if (this.visualizerAnimationId) {
        cancelAnimationFrame(this.visualizerAnimationId);
        this.visualizerAnimationId = null;
        const canvas = this.$refs.visualizer;
        if (canvas) {
            const canvasCtx = canvas.getContext('2d');
            canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
        }
      }
    },
  },
  beforeUnmount() {
    this.stopVisualizer();
  },
};
</script>
