<template>
  <v-dialog v-model="dialog" max-width="800px">
    <v-card>
      <v-card-title>
        <span class="headline">Edit Avatar</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="8">
              <v-card
                class="d-flex justify-center align-center"
                :class="{ 'grey lighten-4': !imageSrc }"
                style="height: 300px; border: 2px dashed; cursor: pointer;"
                :style="{ 'border-color': $vuetify.theme.current.colors.secondary }"
                @click="triggerFileInput"
                @dragover.prevent
                @drop.prevent="onDrop"
              >
                <div v-if="!imageSrc" class="text-center">
                  <v-icon size="48">mdi-cloud-upload</v-icon>
                  <p>Drag & Drop or Click to Upload</p>
                </div>
                <div v-else style="width: 100%; height: 100%;" @click.stop>
                  <vue-cropper
                    ref="cropper"
                    :src="imageSrc"
                    :aspect-ratio="4/3"
                    style="width: 100%; height: 100%;"
                    :key="cropperKey"
                    @crop="crop"
                    @ready="crop"
                  ></vue-cropper>
                </div>
              </v-card>
              <input type="file" ref="fileInput" @change="loadImage" accept="image/*" style="display: none;" />
            </v-col>
            <v-col cols="12" md="4">
              <div class="d-flex flex-column align-center">
                <p class="font-weight-bold">Preview</p>
                <v-avatar size="200" rounded="lg">
                  <v-img :src="croppedImage" v-if="croppedImage" contain></v-img>
                  <div v-else class="grey lighten-2" style="width: 100%; height: 100%;"></div>
                </v-avatar>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="secondary" text @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="generateAvatar" :loading="loading">
          <v-icon left>mdi-auto-fix</v-icon>
          AI Generate
        </v-btn>
        <v-btn color="primary" @click="cropAndSave" :disabled="!croppedImage">Save</v-btn>
      </v-card-actions>
      <v-overlay :value="loading" absolute>
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-card>
  </v-dialog>
</template>

<script>
import VueCropper from 'vue-cropperjs';
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
      croppedImage: null,
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
    onDrop(event) {
      const file = event.dataTransfer.files[0];
      this.handleFile(file);
    },
    loadImage(event) {
      const file = event.target.files[0];
      this.handleFile(file);
    },
    handleFile(file) {
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageSrc = e.target.result;
          this.cropperKey += 1;
        };
        reader.readAsDataURL(file);
      }
    },
    crop() {
      if (!this.$refs.cropper) return;
      this.croppedImage = this.$refs.cropper.getCroppedCanvas().toDataURL('image/png');
    },
    async cropAndSave() {
      if (!this.croppedImage) return;

      const options = {
        maxSizeMB: 1,
        maxWidthOrHeight: 800,
        useWebWorker: true,
      };

      try {
        const blob = await (await fetch(this.croppedImage)).blob();
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
