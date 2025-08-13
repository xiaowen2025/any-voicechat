import { ref, computed } from 'vue';
import { useDisplay } from 'vuetify';

export function useResizableDrawer(defaultWidth = 500) {
  const { mobile } = useDisplay();
  const isMobile = computed(() => mobile.value);
  const desktopWidth = ref(defaultWidth);

  const drawerWidth = computed(() => {
    return isMobile.value ? '100vw' : desktopWidth.value;
  });

  function doResize(event) {
    if (!isMobile.value) {
      desktopWidth.value = event.clientX;
    }
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
