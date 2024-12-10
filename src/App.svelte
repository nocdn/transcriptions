<script>
  import Dropzone from "./lib/Dropzone.svelte";
  import Buttons from "./lib/Buttons.svelte";
  import GroqButtons from "./lib/GroqButtons.svelte";
  import History from "./lib/History.svelte";
  import Transcription from "./lib/Transcription.svelte";

  let messageFromChild = "Waiting for button click...";

  function handleButtonClick(event) {
    messageFromChild = event.detail.message;
    // Access other data from event.detail if you sent it
    console.log("Event Details:", event.detail);
  }
</script>

<main class="flex flex-col gap-3 w-1/2">
  <Dropzone />
  <div class="flex justify-between">
    <History />
    <Buttons />
  </div>
  <Transcription text="" on:buttonClick={handleButtonClick} />
</main>
