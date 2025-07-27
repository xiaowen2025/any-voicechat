<template>
  <div class="d-flex flex-column align-center justify-center pa-3">
    <v-avatar class="mb-4" size="300" rounded="lg" @click="triggerAvatarUpload" style="cursor: pointer;">
      <v-img :src="currentAvatar"></v-img>
    </v-avatar>
    <input type="file" ref="avatarUploader" @change="handleAvatarChange" accept="image/*" style="display: none;" />
    <canvas ref="visualizer" width="125" height="50"></canvas>
  </div>
</template>

<script>
import defaultAvatar from '../assets/agent-avatar.svg';
import imageCompression from 'browser-image-compression';

export default {
  props: {
    analyserNode: {
      type: Object,
      default: null,
    },
    interviewStarted: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      currentAvatar: defaultAvatar,
      visualizerAnimationId: null,
    };
  },
  watch: {
    interviewStarted(newValue) {
      if (newValue) {
        this.drawVisualizer();
      } else {
        this.stopVisualizer();
      }
    },
    analyserNode(newNode) {
        if (this.interviewStarted && newNode) {
            this.drawVisualizer();
        }
    }
  },
  mounted() {
    this.loadAvatar();
  },
  methods: {
    triggerAvatarUpload() {
      this.$refs.avatarUploader.click();
    },
    async handleAvatarChange(event) {
      const file = event.target.files[0];
      if (!file) return;

      const options = {
        maxSizeMB: 1,
        maxWidthOrHeight: 800,
        useWebWorker: true,
      };

      try {
        const compressedFile = await imageCompression(file, options);
        const reader = new FileReader();
        reader.onload = (e) => {
          const base64String = e.target.result;
          localStorage.setItem('userAvatar', base64String);
          this.currentAvatar = base64String;
        };
        reader.readAsDataURL(compressedFile);
      } catch (error) {
        console.error('Error compressing or reading the image:', error);
      }
    },
    loadAvatar() {
      const savedAvatar = localStorage.getItem('userAvatar');
      if (savedAvatar) {
        this.currentAvatar = savedAvatar;
      }
    },
    drawVisualizer() {
      const canvas = this.$refs.visualizer;
      if (!canvas || !this.analyserNode) return;
      const canvasCtx = canvas.getContext('2d');
      const bufferLength = this.analyserNode.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const draw = () => {
        if (!this.interviewStarted) {
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
