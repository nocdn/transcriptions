<script>
  import ModelTable from "./ModelTable.svelte";
  import ModelPicker from "./ModelPicker.svelte";
  import Button from "./Button.svelte";
  import { onMount } from "svelte";
  import { Languages, Command, Plus, CornerDownLeft } from "lucide-svelte";

  let { close } = $props();

  // initial settings structure
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

  let currentModelProvider = $state("groq");
  let currentModelValue = $state("whisper-large-v3");
  let currentPromptValue = $state("");
  let currentLanguageValue = $state("en");

  // helper function to get the current model value based on provider
  function getCurrentModelValue() {
    switch (currentModelProvider) {
      case "groq":
        return settings.groq.groqModelValue;
      case "gemini":
        return settings.gemini.geminiModelValue;
      case "fireworks":
        return settings.fireworks.fireworksModelValue;
      case "elevenlabs":
        return settings.elevenlabs.elevenlabsModelValue;
      default:
        return "whisper-large-v3";
    }
  }

  // update current prompt and language values when provider changes
  function updateCurrentValues() {
    switch (currentModelProvider) {
      case "groq":
        currentPromptValue = settings.groq.groqPromptValue;
        currentLanguageValue = settings.groq.groqLanguageValue;
        break;
      case "gemini":
        currentPromptValue = settings.gemini.geminiPromptValue;
        currentLanguageValue = settings.gemini.geminiLanguageValue;
        break;
      case "fireworks":
        currentPromptValue = settings.fireworks.fireworksPromptValue;
        currentLanguageValue = settings.fireworks.fireworksLanguageValue;
        break;
      case "elevenlabs":
        currentPromptValue = settings.elevenlabs.elevenlabsPromptValue;
        currentLanguageValue = settings.elevenlabs.elevenlabsLanguageValue;
        break;
    }
  }

  // update settings object when current values change
  $effect(() => {
    switch (currentModelProvider) {
      case "groq":
        settings.groq.groqPromptValue = currentPromptValue;
        settings.groq.groqLanguageValue = currentLanguageValue;
        break;
      case "gemini":
        settings.gemini.geminiPromptValue = currentPromptValue;
        settings.gemini.geminiLanguageValue = currentLanguageValue;
        break;
      case "fireworks":
        settings.fireworks.fireworksPromptValue = currentPromptValue;
        settings.fireworks.fireworksLanguageValue = currentLanguageValue;
        break;
      case "elevenlabs":
        settings.elevenlabs.elevenlabsPromptValue = currentPromptValue;
        settings.elevenlabs.elevenlabsLanguageValue = currentLanguageValue;
        break;
    }
  });

  // update current values when provider changes
  $effect(() => {
    updateCurrentValues();
  });

  function handleModelChange(model) {
    // update model provider based on model selection
    if (model.includes("fireworks")) {
      currentModelProvider = "fireworks";
      settings.fireworks.fireworksModelValue = model;
    } else if (model.includes("gemini")) {
      currentModelProvider = "gemini";
      settings.gemini.geminiModelValue = model;
    } else if (model.includes("scribe")) {
      currentModelProvider = "elevenlabs";
      settings.elevenlabs.elevenlabsModelValue = model;
    } else {
      currentModelProvider = "groq";
      settings.groq.groqModelValue = model;
    }

    // update current model value and settings
    currentModelValue = model;
    settings.currentModelProvider = currentModelProvider;
    updateCurrentValues();
    console.log("Selected model:", model, "Provider:", currentModelProvider);
  }

  function handleCancel() {
    close();
  }

  function handleSave() {
    localStorage.setItem("transcription-settings", JSON.stringify(settings));
    close(settings);
  }

  onMount(() => {
    const savedSettings = localStorage.getItem("transcription-settings");
    if (savedSettings) {
      try {
        const parsedSettings = JSON.parse(savedSettings);
        // deep merge the saved settings with the default settings structure
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

        // set current model provider
        currentModelProvider = settings.currentModelProvider || "groq";

        // set current model value based on provider
        currentModelValue = getCurrentModelValue();

        // update current prompt and language values
        updateCurrentValues();

        console.log("Loaded settings:", settings);
      } catch (error) {
        console.error("Error parsing saved settings:", error);
      }
    }
  });
</script>

{#snippet cmdPlusIcon()}
  <div class="flex gap-1 items-center opacity-60">
    <Command size={12} />
    <Plus size={11} />
    <CornerDownLeft size={12} />
  </div>
{/snippet}

<overlay
  class="fixed top-0 left-0 w-full h-full bg-black/50 z-10 flex items-center justify-center motion-opacity-in-0 motion-duration-300"
  onmousedown={close}
  role="dialog"
  tabindex="0"
>
  <modal
    class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-1/2 max-w-lg min-w-lg flex flex-col gap-4 overflow-y-scroll"
    onmousedown={(e) => e.stopPropagation()}
    role="dialog"
    tabindex="0"
  >
    <header>
      <p class="text-2xl font-medium font-geist-mono">Settings</p>
    </header>
    <ModelPicker onChoice={handleModelChange} modelChoice={currentModelValue} />
    <ModelTable />
    <!-- Prompt input -->
    {#if currentModelProvider === "groq" || currentModelProvider === "gemini" || currentModelProvider === "fireworks"}
      <prompt>
        <label
          class="text-sm font-medium font-geist-mono leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="prompt-input"
          >Prompt for {currentModelProvider}
        </label>
        <textarea
          class="flex min-h-[80px] w-full rounded-lg border border-gray-200 border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 font-sans"
          id="prompt-input"
          placeholder="Enter any prompt, or leave blank"
          bind:value={currentPromptValue}
        ></textarea>
      </prompt>
    {/if}
    <!-- Language input -->
    {#if currentModelProvider === "groq" || currentModelProvider === "fireworks"}
      <languageInput class="space-y-2 inline-flex flex-col">
        <label
          class="text-sm font-medium font-geist-mono leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="language-input"
          >Language for {currentModelProvider}
        </label>
        <div class="relative">
          <input
            class="flex h-9 w-full font-mono rounded-lg border border-gray-200 border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 peer pe-9"
            id="language-input"
            placeholder="en"
            type="language"
            bind:value={currentLanguageValue}
          />
          <div
            class="pointer-events-none absolute inset-y-0 end-0 flex items-center justify-center pe-3 text-muted-foreground/80 peer-disabled:opacity-50"
          >
            <Languages size={15} />
          </div>
        </div>
      </languageInput>
    {:else}
      <p
        class="font-mono text-sm opacity-50 inline-flex items-center gap-2 pl-1"
      >
        <Languages size={13} class="opacity-65" />language detected
        automatically
      </p>
    {/if}
    <!-- Cancel and Save buttons -->
    <buttons class="flex justify-between items-center">
      <Button
        label="Cancel"
        onClick={handleCancel}
        iconPosition="none"
        hoverColor="#FAFAFA"
        class="rounded-xl py-1.5 text-sm"
      />
      <Button
        label="Submit"
        onClick={handleSave}
        icon={cmdPlusIcon}
        iconPosition="trailing"
        hoverColor="#EEF2FF"
        class="rounded-xl py-1.5 text-sm"
      />
    </buttons>
  </modal>
</overlay>

<!-- Hiding the scrollbar -->
<style>
  modal {
    scrollbar-width: none;
  }
</style>
