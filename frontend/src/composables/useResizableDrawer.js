import { ref } from 'vue';

export function useResizableDrawer(defaultWidth = 500) {
  const drawerWidth = ref(defaultWidth);

  function doResize(event) {
    drawerWidth.value = event.clientX;
  }

  function stopResize() {
    document.removeEventListener("mousemove", doResize);
    document.removeEventListener("mouseup", stopResize);
  }

  function startResize(event) {
    event.preventDefault();
    document.addEventListener("mousemove", doResize);
    document.addEventListener("mouseup", stopResize);
  }

  return {
    drawerWidth,
    startResize,
  };
}
