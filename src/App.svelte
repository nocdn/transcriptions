<!-- App.svelte -->
<script>
  import Dropzone from "./lib/Dropzone.svelte";
  import Buttons from "./lib/Buttons.svelte";
  import History from "./lib/History.svelte";
  import Transcription from "./lib/Transcription.svelte";
  import Settings from "./lib/Settings.svelte";

  import { onMount } from "svelte";

  let transcriptionText = $state("");
  let selectedFiles = $state([]);
  let loading = $state(false);

  function handleFiles(files) {
    selectedFiles = files;
  }

  let isOpen = $state(false);

  function toggleDrawer(e) {
    e.stopPropagation();
    isOpen = !isOpen;
  }

  let settings = $state({
    currentModelProvider: "groq",
    groq: {
      groqModelValue: "whisper-large-v3",
      groqPromptValue: "",
      groqLanguageValue: "en",
    },
    gemini: {
      geminiModelValue: "gemini-2.0-flash-exp",
      geminiPromptValue: "",
    },
    fireworks: {
      fireworksModelValue: "accounts/fireworks/models/whisper-v3-turbo",
      fireworksPromptValue: "",
      fireworksLanguageValue: "en",
    },
  });

  onMount(() => {
    const savedSettings = localStorage.getItem("transcription-settings");
    if (savedSettings) {
      settings = { ...settings, ...JSON.parse(savedSettings) };
    }
  });

  function handleSettingsChange(newSettings) {
    if (newSettings) {
      settings = { ...settings, ...newSettings };
    }
    isOpen = false;
  }

  async function handleActions(action) {
    if (action === "submit" && selectedFiles.length > 0) {
      try {
        loading = true;
        const formData = new FormData();
        formData.append("currentModelProvider", settings.currentModelProvider);
        if (settings.currentModelProvider === "groq") {
          formData.append("groqModelValue", settings.groq.groqModelValue);
          formData.append("groqPromptValue", settings.groq.groqPromptValue);
          formData.append("groqLanguageValue", settings.groq.groqLanguageValue);
        } else if (settings.currentModelProvider === "gemini") {
          formData.append("geminiModelValue", settings.gemini.geminiModelValue);
          formData.append(
            "geminiPromptValue",
            settings.gemini.geminiPromptValue
          );
        } else if (settings.currentModelProvider === "fireworks") {
          formData.append(
            "fireworksModelValue",
            settings.fireworks.fireworksModelValue
          );
          formData.append(
            "fireworksPromptValue",
            settings.fireworks.fireworksPromptValue
          );
          formData.append(
            "fireworksLanguageValue",
            settings.fireworks.fireworksLanguageValue
          );
        } else {
          formData.append("error", "Invalid model provider");
        }
        formData.append("file", selectedFiles[0]);
        console.log(formData);
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
    } else if (action === "history") {
      const response = await fetch("http://localhost:6005/api/history");
      const data = await response.json();
      console.log(data);
    }
  }
</script>

<main
  class="flex flex-col gap-3 w-1/2 min-h-screen px-4 overflow-x-hidden h-full pb-5"
>
  <Dropzone {handleFiles} bind:files={selectedFiles} />
  <div class="flex justify-between">
    <History onButtonClick={handleActions} />
    <Buttons onButtonClick={handleActions} />
  </div>
  <Transcription text={transcriptionText} {loading} />

  <button
    onmousedown={toggleDrawer}
    aria-label="Settings"
    class="border w-fit dark:border-gray-500 rounded-md px-2.5 py-2 hover:bg-gray-100 hover:text-gray-700 hover:outline-1 hover:outline-dashed hover:outline-gray-300 absolute top-3 right-3"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z"
      />
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
      />
    </svg>
  </button>
  {#if isOpen}
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <Settings close={handleSettingsChange} />
  {/if}
</main>
