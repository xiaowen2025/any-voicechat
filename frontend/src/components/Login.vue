<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card>
          <v-card-title class="text-center">
            <h2>Login</h2>
          </v-card-title>
          <v-card-text>
            <v-alert v-if="userStore.error" type="error" dense>
              {{ userStore.error }}
            </v-alert>
            <v-form @submit.prevent="handleLogin">
              <div v-if="!otpSent">
                <v-text-field
                  v-model="email"
                  label="Email"
                  required
                  type="email"
                ></v-text-field>
                <v-btn type="submit" color="primary" block :loading="loading">Request OTP</v-btn>
              </div>
              <div v-else>
                <v-text-field
                  v-model="otp"
                  label="OTP"
                  required
                ></v-text-field>
                <v-btn type="submit" color="primary" block :loading="loading">Verify OTP</v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';

const email = ref('');
const otp = ref('');
const otpSent = ref(false);
const loading = ref(false);
const userStore = useUserStore();

async function handleLogin() {
  loading.value = true;
  if (!otpSent.value) {
    await userStore.requestOtp(email.value);
    if (!userStore.error) {
      otpSent.value = true;
    }
  } else {
    await userStore.verifyOtp(email.value, otp.value);
  }
  loading.value = false;
}
</script>
