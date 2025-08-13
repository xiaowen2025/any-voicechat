import { ref, computed } from 'vue';
import { useDisplay } from 'vuetify';

export function useResizableDrawer(defaultWidth = 500) {
  const drawerWidth = ref(defaultWidth);
  const { mobile } = useDisplay();
  const isMobile = computed(() => mobile.value);

  function doResize(event) {
    drawerWidth.value = event.clientX;
  }

  function stopResize() {
    document.removeEventListener('mousemove', doResize);
    document.removeEventListener('mouseup', stopResize);
  }

  function startResize(event) {
    if (isMobile.value) return;
    event.preventDefault();
    document.addEventListener('mousemove', doResize);
    document.addEventListener('mouseup', stopResize);
  }

  return {
    drawerWidth,
    startResize,
    isMobile,
  };
}
