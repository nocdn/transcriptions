<script>
  import Dropzone from "./lib/Dropzone.svelte";
  import Buttons from "./lib/Buttons.svelte";
  import History from "./lib/History.svelte";
  import Transcription from "./lib/Transcription.svelte";

  let transcriptionText = $state("");
  let selectedFiles = $state([]);

  let loading = $state(false);

  function handleFiles(files) {
    selectedFiles = files;
  }

  async function handleActions(action) {
    if (action === "submit" && selectedFiles.length > 0) {
      try {
        loading = true;
        console.log(loading);
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
        console.log(data.transcription);
        transcriptionText = data.transcription || "";
        loading = false;
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
  <Transcription text={transcriptionText} {loading} />
</main>
