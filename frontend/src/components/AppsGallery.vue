<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center mb-4">Apps Gallery</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="app in apps"
        :key="app.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card class="d-flex flex-column fill-height" @click="selectApp(app.id)">
          <v-img :src="app.avatar" aspect-ratio="4/3"></v-img>
          <v-card-title>{{ app.name }}</v-card-title>
          <v-card-text class="flex-grow-1">
            {{ app.summary }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';

const apps = ref([]);
const emit = defineEmits(['app-selected', 'close']);

async function fetchApps() {
  try {
    const response = await fetch('/api/apps');
    if (response.ok) {
      const fetchedApps = await response.json();
      apps.value = fetchedApps.map(app => ({
        ...app,
        avatar: `/assets/avatar_${app.id}.png`
      }));
    } else {
      console.error('Error fetching apps:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching apps:', error);
  }
}

function selectApp(appId) {
  emit('app-selected', appId);
}

onMounted(() => {
  fetchApps();
});
</script>

<style scoped>
.v-card {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}
.v-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
</style>
