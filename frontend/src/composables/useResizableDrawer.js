import { ref } from 'vue';

export function useResizableDrawer(initialWidth = 500) {
  const drawerWidth = ref(initialWidth);

  function doResize(event) {
    drawerWidth.value = event.clientX;
  }

  function stopResize() {
    document.removeEventListener('mousemove', doResize);
    document.removeEventListener('mouseup', stopResize);
  }

  function startResize(event) {
    event.preventDefault();
    document.addEventListener('mousemove', doResize);
    document.addEventListener('mouseup', stopResize);
  }

  return {
    drawerWidth,
    startResize,
  };
}
