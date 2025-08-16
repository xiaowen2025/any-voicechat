import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
  const isApiKeySet = ref(false);
  const isLoggedIn = ref(false);
  const userEmail = ref(null);
  const error = ref(null);

  async function setApiKey() {
    const apiKey = localStorage.getItem('geminiApiKey');
    if (apiKey) {
      try {
        const response = await fetch('/api/set_api_key', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ key: apiKey }),
        });
        const data = await response.json();
        if (data.status === 'success') {
          isApiKeySet.value = true;
          console.log('API key set successfully');
        } else {
          isApiKeySet.value = false;
          console.error('Failed to set API key:', data.message);
        }
      } catch (error) {
        isApiKeySet.value = false;
        console.error('Error setting API key:', error);
      }
    } else {
      isApiKeySet.value = false;
    }
  }

  async function requestOtp(email) {
    error.value = null;
    try {
      const response = await fetch('/api/auth/request-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
      if (response.ok) {
        userEmail.value = email;
      } else {
        const data = await response.json();
        error.value = data.detail || 'Failed to request OTP';
      }
    } catch (e) {
      error.value = 'An unexpected error occurred.';
    }
  }

  async function verifyOtp(email, otp) {
    error.value = null;
    try {
      const response = await fetch('/api/auth/verify-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, otp }),
      });
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        isLoggedIn.value = true;
      } else {
        const data = await response.json();
        error.value = data.detail || 'Failed to verify OTP';
      }
    } catch (e) {
      error.value = 'An unexpected error occurred.';
    }
  }

  function checkLoginStatus() {
    const token = localStorage.getItem('token');
    if (token) {
      isLoggedIn.value = true;
    }
  }

  function logout() {
    localStorage.removeItem('token');
    isLoggedIn.value = false;
    userEmail.value = null;
    error.value = null;
  }

  return {
    isApiKeySet,
    setApiKey,
    isLoggedIn,
    userEmail,
    error,
    requestOtp,
    verifyOtp,
    checkLoginStatus,
    logout,
  };
});
