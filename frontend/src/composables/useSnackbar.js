import { ref } from 'vue';

const visible = ref(false);
const message = ref('');
const color = ref('info');

export function useSnackbar() {
  const showSnackbar = (text, snackbarColor = 'info') => {
    message.value = text;
    color.value = snackbarColor;
    visible.value = true;
  };

  return {
    visible,
    message,
    color,
    showSnackbar,
  };
}
