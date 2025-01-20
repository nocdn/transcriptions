<script>
  let { isOpen } = $props();

  function toggleDrawer() {
    isOpen = !isOpen;
  }

  function closeDrawer() {
    isOpen = false;
  }
</script>

<div class="w-fit h-fit bg-white rounded-md z-60">
  <h2>Model Selection:</h2>
  <select class="w-full h-fit">
    <option value="distil-whisper-large-v3-en"
      >distil-whisper-large-v3-en</option
    >
    <option value="whisper-large-v3-turbo">whisper-large-v3-turbo</option>
    <option value="whisper-large-v3-en">whisper-large-v3-en</option>
    <option value="gemini-2.0-flash-exp">gemini-2.0-flash-exp</option>
    <option value="gemini-1.5-flash-latest">gemini-1.5-flash-002</option>
    <option value="gemini-1.5-flash-8b">gemini-1.5-flash-8b</option>
    <option value="gemini-1.5-pro-002">gemini-1.5-pro-002</option>
    <option value="accounts/fireworks/models/whisper-v3-turbo"
      >fireworks/whisper-v3-turbo</option
    >
  </select>
</div>
