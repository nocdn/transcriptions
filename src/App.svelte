<script>
  import Dropzone from "./lib/Dropzone.svelte";
  import Buttons from "./lib/Buttons.svelte";
  import History from "./lib/History.svelte";
  import Transcription from "./lib/Transcription.svelte";

  let transcriptionText = "";
  let selectedFiles = $state([]);

  function handleFiles(files) {
    selectedFiles = files;
  }

  async function handleActions(action) {
    if (action === "submit" && selectedFiles.length > 0) {
      try {
        const formData = new FormData();
        formData.append("file", selectedFiles[0]);
        formData.append("model", "distil-whisper-large-v3-en");
        formData.append("language", "en");
        formData.append("response_format", "text");

        const response = await fetch("http://localhost:6005/api/upload", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        transcriptionText = data.transcription || "";
      } catch (error) {
        console.error(error);
      }
    } else if (action === "cancel") {
      selectedFiles = []; // Clear the array
      transcriptionText = "";
    }
  }
</script>

<main class="flex flex-col gap-3 w-1/2">
  <Dropzone {handleFiles} bind:files={selectedFiles} />
  <div class="flex justify-between">
    <History onButtonClick={handleActions} />
    <Buttons onButtonClick={handleActions} />
  </div>
  <Transcription text={transcriptionText} />
</main>
