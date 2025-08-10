<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">Edit Avatar</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" class="d-flex justify-center">
              <v-progress-circular
                v-if="loading"
                indeterminate
                color="primary"
              ></v-progress-circular>
            </v-col>
            <v-col cols="12">
              <input type="file" ref="fileInput" @change="loadImage" accept="image/*" style="display: none;" />
              <v-btn @click="triggerFileInput">Select Image</v-btn>
            </v-col>
            <v-col cols="12">
              <div v-if="imageSrc">
                <vue-cropper
                  ref="cropper"
                  :src="imageSrc"
                  :aspect-ratio="1"
                  style="width: 100%;"
                  :key="cropperKey"
                ></vue-cropper>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialog = false">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="cropAndSave">Save</v-btn>
        <v-btn color="deep-purple accent-4" text @click="generateAvatar" :loading="loading">AI Generate</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { VueCropper } from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import imageCompression from 'browser-image-compression';

export default {
  components: {
    VueCropper,
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue', 'avatar-saved'],
  data() {
    return {
      imageSrc: null,
      loading: false,
      cropperKey: 0,
    };
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit('update:modelValue', val);
      },
    },
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    loadImage(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageSrc = e.target.result;
          this.cropperKey += 1;
        };
        reader.readAsDataURL(file);
      }
    },
    async cropAndSave() {
      if (!this.$refs.cropper) return;
      const croppedCanvas = this.$refs.cropper.getCroppedCanvas();
      const croppedImageData = croppedCanvas.toDataURL('image/png');

      const options = {
        maxSizeMB: 1,
        maxWidthOrHeight: 800,
        useWebWorker: true,
      };

      try {
        const blob = await (await fetch(croppedImageData)).blob();
        const compressedFile = await imageCompression(blob, options);
        const reader = new FileReader();
        reader.onload = (e) => {
          const base64String = e.target.result;
          localStorage.setItem('userAvatar', base64String);
          this.$emit('avatar-saved', base64String);
          this.dialog = false;
        };
        reader.readAsDataURL(compressedFile);
      } catch (error) {
        console.error('Error compressing or reading the image:', error);
      }
    },
    async generateAvatar() {
      this.loading = true;
      try {
        const response = await fetch('/api/avatar/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            prompt: 'minimalist flat design with cute cartoon character face with elements relevant to the current app settings',
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to generate avatar');
        }

        const data = await response.json();
        this.imageSrc = `data:image/png;base64,${data.image}`;
        this.cropperKey += 1;
      } catch (error) {
        console.error('Error generating avatar:', error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
