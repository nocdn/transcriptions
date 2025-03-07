<script>
  import Dropzone from "./lib/Dropzone.svelte";
  import Button from "./lib/Button.svelte";
  import HistoryItem from "./lib/HistoryItem.svelte";
  import Transcription from "./lib/Transcription.svelte";
  import SettingsModal from "./lib/SettingsModal.svelte";
  import Spinner from "./lib/Spinner.svelte";

  import { onMount } from "svelte";

  import {
    Command,
    Plus,
    CornerDownLeft,
    Trash2,
    Settings,
    HeartCrack,
  } from "lucide-svelte";

  let transcriptionText = $state("");
  let selectedFiles = $state([]);
  let loading = $state(false);
  let rateLimited = $state(false);
  let currentFileName = $state("");

  function handleFiles(files) {
    selectedFiles = files;
  }

  let isOpen = $state(false);

  function toggleDrawer() {
    isOpen = !isOpen;
    console.log("isOpen", isOpen);
  }

  let settings = $state({
    currentModelProvider: "groq",
    groq: {
      groqModelValue: "whisper-large-v3",
      groqPromptValue: "",
      groqLanguageValue: "en",
    },
    gemini: {
      geminiModelValue: "gemini-2.0-flash",
      geminiPromptValue: "",
    },
    fireworks: {
      fireworksModelValue: "fireworks/whisper-v3-turbo",
      fireworksPromptValue: "",
      fireworksLanguageValue: "en",
    },
    elevenlabs: {
      elevenlabsModelValue: "scribe_v1",
    },
  });

  let history = $state([]);
  let fetchingHistory = $state(false);

  onMount(() => {
    const savedSettings = localStorage.getItem("transcription-settings");
    if (savedSettings) {
      try {
        const parsedSettings = JSON.parse(savedSettings);
        // deep merge saved settings with the default settings
        settings = {
          ...settings,
          ...parsedSettings,
          groq: { ...settings.groq, ...(parsedSettings.groq || {}) },
          gemini: { ...settings.gemini, ...(parsedSettings.gemini || {}) },
          fireworks: {
            ...settings.fireworks,
            ...(parsedSettings.fireworks || {}),
          },
          elevenlabs: {
            ...settings.elevenlabs,
            ...(parsedSettings.elevenlabs || {}),
          },
        };
      } catch (error) {
        console.error("Error parsing saved settings:", error);
      }
    }

    fetchHistory();
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
        rateLimited = false;
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
        } else if (settings.currentModelProvider === "elevenlabs") {
          formData.append(
            "elevenlabsModelValue",
            settings.elevenlabs.elevenlabsModelValue
          );
        } else {
          formData.append("error", "Invalid model provider");
        }
        formData.append("file", selectedFiles[0]);
        currentFileName = selectedFiles[0].name;
        console.log(formData);
        const response = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        if (response.status === 429) {
          rateLimited = true;
          loading = false;
          return;
        }

        const data = await response.json();
        console.log(data.transcription);
        transcriptionText = data.transcription || "";
        loading = false;
        fetchHistory();
      } catch (error) {
        console.error(error);
      }
    } else if (action === "cancel") {
      // selectedFiles = [];
      // transcriptionText = "";
      window.location.reload();
    }
  }

  async function fetchHistory() {
    fetchingHistory = true;
    const response = await fetch("/api/history");
    const data = await response.json();
    fetchingHistory = false;
    console.log(data);
    history = data;
  }

  async function handleDeleteHistoryItem(filename) {
    const response = await fetch("/api/delete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ filename }),
    });
    const data = await response.json();
    console.log("delete", data);
    fetchHistory();
  }

  function handleShowTranscription(transcription, filename) {
    transcriptionText = transcription;
    currentFileName = filename;
  }

  function returnMaxFileSize(provider) {
    switch (provider) {
      case "groq":
        return "100MB";
      case "gemini":
        return "2GB";
      case "fireworks":
        return "1GB";
      case "elevenlabs":
        return "1GB";
      default:
        return "40MB";
    }
  }
</script>

{#snippet cmdPlusIcon()}
  <div class="flex gap-1 items-center opacity-60">
    <Command size={12} />
    <Plus size={11} />
    <CornerDownLeft size={12} />
  </div>
{/snippet}

{#snippet cancelIcon()}
  <Trash2 size={15} />
{/snippet}

<main class="w-dvw h-dvh grid grid-cols-[24rem_1fr] gap-4">
  <column class="flex flex-col gap-3 h-dvh pt-4 pl-4 pb-4">
    <p class="text-xl font-medium pl-1 pt-3 font-geist">Transcribe:</p>
    <Dropzone
      {handleFiles}
      bind:files={selectedFiles}
      processing={loading}
      maxSize={returnMaxFileSize(settings.currentModelProvider)}
    />
    <div class="flex justify-between items-center">
      <Button
        label="Cancel"
        onClick={() => handleActions("cancel")}
        icon={cancelIcon}
        iconPosition="leading"
        hoverColor="#F6EAEA"
        class="rounded-xl py-2.5"
      />
      <Button
        label="Submit"
        onClick={() => {
          console.log("submit");
          handleActions("submit");
        }}
        icon={cmdPlusIcon}
        iconPosition="trailing"
        hoverColor="#EEF2FF"
        class="rounded-xl py-2.5"
      />
    </div>
    <p class="text-xl font-medium pl-1 pt-5 font-geist">History:</p>
    <historyContainer
      class="border border-gray-200 rounded-xl flex flex-col gap-0.5"
    >
      {#if !fetchingHistory}
        {#if history.length > 0}
          {#each history as item}
            <HistoryItem
              title={item.filename}
              date={item.date}
              fileExtension={item.fileExtension}
              fileNameNoExt={item.fileNameNoExt}
              transcription={item.transcription}
              onDelete={() => handleDeleteHistoryItem(item.filename)}
              onShowTranscription={handleShowTranscription}
            />
          {/each}
        {:else}
          <p
            class="text-md font-semibold font-mono text-gray-400 p-3 pl-4 inline-flex items-center gap-3 motion-opacity-in-0"
          >
            no file history <HeartCrack size={16} strokeWidth={2.5} />
          </p>
        {/if}
      {:else if fetchingHistory}
        <p
          class="text-md font-semibold font-mono text-gray-400 p-3 inline-flex items-center gap-2 motion-opacity-in-0"
        >
          <Spinner class="opacity-50" /> fetching history
        </p>
      {/if}
    </historyContainer>
    <button
      onclick={() => {
        console.log("clicked settings");
        toggleDrawer();
      }}
      class="rounded-lg w-13 h-12 mt-auto border border-gray-200 grid place-content-center hover:bg-gray-50 cursor-pointer"
    >
      <Settings size={20} />
    </button>
  </column>
  <column class="flex flex-col gap-3 h-dvh pt-4 pr-1 pb-4">
    <Transcription {transcriptionText} fileName={currentFileName} />
  </column>
</main>

{#if isOpen}
  <SettingsModal close={handleSettingsChange} />
{/if}
