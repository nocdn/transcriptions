<script>
  import ModelPicker from "./ModelPicker.svelte";
  import StatsModal from "./StatsModal.svelte";
  import Button from "./Button.svelte";
  import Switch from "./Switch.svelte";
  import { onMount } from "svelte";
  import {
    Languages,
    Command,
    Plus,
    CornerDownLeft,
    Info,
  } from "lucide-svelte";

  let { close } = $props();

  // updated settings structure to include webhookUrl property
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
    notificationEnabled: false,
    webhookUrl: "",
  });

  let currentModelProvider = $state("groq");
  let currentModelValue = $state("whisper-large-v3");
  let currentPromptValue = $state("");
  let currentLanguageValue = $state("en");

  // helper fn to get current model value based on provider
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
    console.log("selected model:", model, "provider:", currentModelProvider);
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
        // deep merge the saved settings with the default structure
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
          webhookUrl: parsedSettings.webhookUrl || "",
        };
        currentModelProvider = settings.currentModelProvider || "groq";
        currentModelValue = getCurrentModelValue();
        updateCurrentValues();
        console.log("loaded settings:", settings);
      } catch (error) {
        console.error("error parsing saved settings:", error);
      }
    }
  });

  let showingStatsModal = $state(false);
  let dismissingSettingsModal = $state(false);
</script>

{#snippet cmdPlusIcon()}
  <div class="flex gap-1 items-center opacity-60">
    <Command size={12} />
    <Plus size={11} />
    <CornerDownLeft size={12} />
  </div>
{/snippet}

{#snippet infoIcon()}
  <Info size={15} />
{/snippet}

<overlay
  class="fixed top-0 left-0 w-full h-full bg-black/50 z-10 flex items-center justify-center {dismissingSettingsModal
    ? 'animate-bg-fade-out'
    : 'animate-bg-fade-in'}"
  onmousedown={() => {
    dismissingSettingsModal = true;
    setTimeout(() => {
      handleCancel();
    }, 300);
  }}
  role="dialog"
  tabindex="0"
>
  <modal
    class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-1/2 max-w-lg min-w-lg flex flex-col gap-4 overflow-y-scroll {dismissingSettingsModal
      ? 'animate-settings-modal-down'
      : 'animate-settings-modal-up'}"
    onmousedown={(e) => e.stopPropagation()}
    role="dialog"
    tabindex="0"
  >
    <header class="flex items-center justify-between mb-3">
      <p class="text-lg font-bold font-jetbrains-mono">SETTINGS</p>
      <div class="flex items-center gap-2">
        <p class="font-jetbrains-mono text-xs mr-2">NOTIFICATIONS</p>
        <Switch
          id="notification-switch"
          checked={settings.notificationEnabled}
          onToggle={(value) => {
            settings.notificationEnabled = value;
          }}
        />
      </div>
    </header>
    <ModelPicker onChoice={handleModelChange} modelChoice={currentModelValue} />
    <Button
      label="MODEL STATS"
      onClick={() => (showingStatsModal = true)}
      iconPosition="trailing"
      icon={infoIcon}
      hoverColor="#FAFAFA"
      class="rounded-lg py-1.5 text-xs w-fit gap-0"
    />
    {#if currentModelProvider === "groq" || currentModelProvider === "gemini" || currentModelProvider === "fireworks"}
      <prompt>
        <label
          class="text-sm font-medium font-geist-mono leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="prompt-input">prompt for {currentModelProvider}</label
        >
        <textarea
          class="flex min-h-[80px] w-full rounded-lg border border-gray-200 border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 font-sans"
          id="prompt-input"
          placeholder="enter any prompt, or leave blank"
          bind:value={currentPromptValue}
        ></textarea>
      </prompt>
    {/if}
    {#if currentModelProvider === "groq" || currentModelProvider === "fireworks"}
      <languageInput class="space-y-2 inline-flex flex-col">
        <label
          class="text-sm font-medium font-geist-mono leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="language-input">language for {currentModelProvider}</label
        >
        <div class="relative">
          <input
            class="flex h-9 w-full font-mono rounded-lg border border-gray-200 border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 peer pe-9 ps-3"
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
    <div class="">
      <label
        for="webhook-url"
        class="text-sm font-medium font-geist-mono text-foreground"
      >
        webhook url <span class="opacity-50">(optional)</span>
      </label>
      <input
        id="webhook-url"
        type="url"
        placeholder="https://example.com/webhook"
        bind:value={settings.webhookUrl}
        class="mt-1 flex h-9 w-full font-mono rounded-lg border border-gray-200 bg-background px-3 py-2 text-sm text-foreground shadow-sm transition-shadow placeholder:text-muted-foreground/70"
      />
    </div>
    <buttons class="flex justify-between items-center">
      <Button
        label="Cancel"
        onClick={() => {
          dismissingSettingsModal = true;
          setTimeout(() => {
            handleCancel();
          }, 300);
        }}
        iconPosition="none"
        hoverColor="#FAFAFA"
        class="rounded-xl py-1.5 text-sm"
      />
      <Button
        label="Submit"
        onClick={() => {
          dismissingSettingsModal = true;
          setTimeout(() => {
            handleSave();
          }, 300);
        }}
        icon={cmdPlusIcon}
        iconPosition="trailing"
        hoverColor="#EEF2FF"
        class="rounded-xl py-1.5 text-sm"
      />
    </buttons>
  </modal>
</overlay>

{#if showingStatsModal}
  <StatsModal onDismiss={() => (showingStatsModal = false)} />
{/if}

<style>
  modal {
    scrollbar-width: none;
  }
</style>
