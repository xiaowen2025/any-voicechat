<template>
  <div class="d-flex flex-column align-center justify-center pa-3">
    <v-avatar class="mb-4" size="125" rounded="lg">
      <v-img :src="agentAvatar"></v-img>
    </v-avatar>
    <canvas ref="visualizer" width="125" height="50"></canvas>
  </div>
</template>

<script>
import agentAvatar from '../assets/agent-avatar.svg';

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
      agentAvatar,
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
  methods: {
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
