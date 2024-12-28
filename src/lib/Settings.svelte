<script>
  let { isOpen } = $props();

  function toggleDrawer() {
    isOpen = !isOpen;
  }

  function closeDrawer() {
    isOpen = false;
  }
</script>

<div class="fixed inset-0 z-10 isolate pointer-events-none h-screen">
  <!-- Overlay -->
  <!-- <div
    id="settings-overlay"
    class="fixed inset-0 bg-black/30 z-40 transition-opacity duration-300 {isOpen
      ? 'opacity-100 pointer-events-auto'
      : 'opacity-0'}"
    on:click={closeDrawer}
    on:keydown={(e) => e.key === "Escape" && closeDrawer()}
    tabindex="0"
    aria-label="Close settings"
  ></div> -->

  <!-- Drawer -->
  <div
    id="settings-drawer"
    class="fixed bottom-0 left-0 right-0 w-full h-[80vh] bg-white shadow-lg z-50 transform transition-transform duration-300 ease-in-out rounded-t-xl overflow-y-auto {isOpen
      ? 'translate-y-0 pointer-events-auto'
      : 'translate-y-full'}"
  >
    <!-- Your drawer content here -->
  </div>
</div>
