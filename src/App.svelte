<script>
  import Dropzone from "./lib/Dropzone.svelte";
  import Buttons from "./lib/Buttons.svelte";
  import GroqButtons from "./lib/GroqButtons.svelte";
  import History from "./lib/History.svelte";
</script>

<main class="flex flex-col gap-3 w-1/2">
  <Dropzone />
  <div class="flex justify-between">
    <History />
    <Buttons />
  </div>
</main>
