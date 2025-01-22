<!-- Settings.svelte -->
<script>
  import { onMount } from "svelte";
  import { Info } from "lucide-svelte";
  import { Zap } from "lucide-svelte";
  import { Languages } from "lucide-svelte";

  let { close, settings } = $props();

  let advancedChecked = $state(false);
  let selectedFormat = $state("1");

  let groqModelValue = $state("whisper-large-v3");
  let groqPromptValue = $state("");
  let groqLanguageValue = $state("en");

  let geminiModelValue = $state("gemini-2.0-flash-exp");
  let geminiPromptValue = $state("");

  let fireworksModelValue = $state(
    "accounts/fireworks/models/whisper-v3-turbo"
  );
  let fireworksPromptValue = $state("");
  let fireworksLanguageValue = $state("en");

  // Load settings from localStorage on mount
  onMount(() => {
    const savedSettings = localStorage.getItem("transcription-settings");
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      currentModelProvider = settings.currentModelProvider;

      groqModelValue = settings.groq.groqModelValue;
      groqPromptValue = settings.groq.groqPromptValue;
      groqLanguageValue = settings.groq.groqLanguageValue;

      geminiModelValue = settings.gemini.geminiModelValue;
      geminiPromptValue = settings.gemini.geminiPromptValue;

      fireworksModelValue = settings.fireworks.fireworksModelValue;
      fireworksPromptValue = settings.fireworks.fireworksPromptValue;
      fireworksLanguageValue = settings.fireworks.fireworksLanguageValue;
    }
  });

  function handleAdvancedCheckbox() {
    advancedChecked = !advancedChecked;
  }

  function handleCancel() {
    close();
  }

  let generalModelValue = $state("whisper-large-v3");
  function handleModelChange() {
    if (generalModelValue.includes("gemini")) {
      currentModelProvider = "gemini";
    } else if (generalModelValue.includes("fireworks")) {
      currentModelProvider = "fireworks";
    } else {
      currentModelProvider = "groq";
    }
  }

  let currentModelProvider = $state("groq");

  function handleSave() {
    const settings = {
      currentModelProvider,
      groq: {
        groqModelValue,
        groqPromptValue,
        groqLanguageValue,
      },
      gemini: {
        geminiModelValue,
        geminiPromptValue,
      },
      fireworks: {
        fireworksModelValue,
        fireworksPromptValue,
        fireworksLanguageValue,
      },
    };

    // Save to localStorage
    localStorage.setItem("transcription-settings", JSON.stringify(settings));
    close(settings);
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
  class="fixed top-0 left-0 w-full h-full bg-black/50 z-10 flex items-center justify-center"
  onmousedown={close}
>
  <div
    class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-1/2 max-w-md"
    onmousedown={(e) => e.stopPropagation()}
  >
    <h2
      class="text-2xl font-semibold mb-4 dark:text-white flex justify-between"
    >
      Settings

      <label class="inline-flex items-center cursor-pointer">
        <span class="me-3 text-sm font-medium text-gray-900 dark:text-gray-300"
          >Advanced</span
        >
        <input
          type="checkbox"
          value=""
          class="sr-only peer"
          onchange={handleAdvancedCheckbox}
        />
        <div
          class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"
        ></div>
      </label>
    </h2>
    <container class="flex flex-col gap-4">
      <div class="space-y-2">
        <label
          class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="model-select">Select model</label
        >
        <div class="relative">
          <select
            class="peer inline-flex w-full cursor-pointer appearance-none items-center rounded-lg border border-input bg-background text-sm text-foreground shadow-sm shadow-black/5 transition-shadow focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 has-[option[disabled]:checked]:text-muted-foreground h-9 pe-8 ps-3"
            id="model-select"
            bind:value={generalModelValue}
            onchange={handleModelChange}
            ><option value="whisper-large-v3">whisper-large-v3</option><option
              value="whisper-large-v3-turbo">whisper-large-v3-turbo</option
            ><option value="distil-whisper-large-v3-en"
              >distil-whisper-large-v3</option
            ><option value="gemini-2.0-flash-exp">gemini-2.0-flash-exp</option
            ><option value="gemini-1.5-flash-latest"
              >gemini-1.5-flash-latest</option
            ><option value="gemini-1.5-flash-8b">gemini-1.5-flash-8b</option
            ><option value="gemini-1.5-pro-002">gemini-1.5-pro-002</option
            ><option value="accounts/fireworks/models/whisper-v3-turbo"
              >fireworks/whisper-v3-turbo</option
            ></select
          ><span
            class="pointer-events-none absolute inset-y-0 end-0 flex h-full w-9 items-center justify-center text-muted-foreground/80 peer-disabled:opacity-50"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide lucide-chevron-down"
              aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg
            ></span
          >
        </div>
      </div>
      <div class="overflow-hidden border rounded-lg">
        <table class="w-full caption-bottom text-sm">
          <thead class="bg-[#f9f9fa]">
            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted bg-muted/50"
            >
              <th
                class="px-3 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:w-px [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 h-9 py-2"
                >Model</th
              >
              <th
                class="px-3 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:w-px [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 h-9 py-2"
                >Cost /h</th
              >
              <th
                title="Word Error Rate, lower means higher accuracy"
                class="px-3 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:w-px [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 h-9 py-2 flex items-center gap-2"
                >WER <Info size={14} /></th
              >
            </tr>
          </thead>
          <tbody class="[&_tr:last-child]:border-0">
            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
            >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-medium"
                >large-v3</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >$0.111</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >10.3%</td
              >
            </tr>
            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
            >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-medium"
                >large-v3-turbo</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >$0.04</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >12%</td
              >
            </tr>
            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
            >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-medium"
                >distil-large-v3</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >$0.02</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >13%</td
              >
            </tr>

            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
            >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-medium"
                >gemini-1.5-flash</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >$6.75</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >9.6%</td
              >
            </tr>
            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
            >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-medium"
                >gemini-1.5-pro</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >$112.50</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >5.5%</td
              >
            </tr>
            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
            >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-medium"
                >gemini-2.0-flash</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >~$0.00</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >~4.5%</td
              >
            </tr>
            <tr
              class="border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
            >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-medium flex items-center gap-2"
                >whisper-v3-turbo <Zap size={14} color="#efb701" /></td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >$0.06</td
              >
              <td
                class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
                >13.7%</td
              >
            </tr>
          </tbody>
        </table>
      </div>
      {#if currentModelProvider === "groq"}
        <div class="space-y-2" style="--ring: 234 89% 74%;">
          <label
            class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="prompt-input">Prompt for groq</label
          ><textarea
            class="flex min-h-[80px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 font-sans"
            id="prompt-input"
            placeholder="Enter any prompt, or leave blank"
            bind:value={groqPromptValue}
          ></textarea>
        </div>
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="language-input">Language for groq</label
          >
          <div class="relative">
            <input
              class="flex h-9 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 peer pe-9"
              id="language-input"
              placeholder="en"
              type="language"
              bind:value={groqLanguageValue}
            />
            <div
              class="pointer-events-none absolute inset-y-0 end-0 flex items-center justify-center pe-3 text-muted-foreground/80 peer-disabled:opacity-50"
            >
              <Languages size={15} />
            </div>
          </div>
        </div>
      {:else if currentModelProvider === "gemini"}
        <!-- Gemini -->
        <div class="space-y-2" style="--ring: 234 89% 74%;">
          <label
            class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="prompt-input">Prompt for gemini</label
          ><textarea
            class="flex min-h-[80px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 font-sans"
            id="prompt-input"
            placeholder="Enter any prompt, or leave blank"
            bind:value={geminiPromptValue}
          ></textarea>
        </div>
      {:else if currentModelProvider === "fireworks"}
        <!-- Fireworks -->
        <div class="space-y-2" style="--ring: 234 89% 74%;">
          <label
            class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="prompt-input">Prompt for fireworks</label
          ><textarea
            class="flex min-h-[80px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 font-sans"
            id="prompt-input"
            placeholder="Enter any prompt, or leave blank"
            bind:value={fireworksPromptValue}
          ></textarea>
        </div>
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="language-input">Language for fireworks</label
          >
          <div class="relative">
            <input
              class="flex h-9 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 peer pe-9"
              id="language-input"
              placeholder="en"
              type="language"
              bind:value={fireworksLanguageValue}
            />
            <div
              class="pointer-events-none absolute inset-y-0 end-0 flex items-center justify-center pe-3 text-muted-foreground/80 peer-disabled:opacity-50"
            >
              <Languages size={15} />
            </div>
          </div>
        </div>
      {/if}
      {#if advancedChecked}
        <fieldset class="space-y-4">
          <legend class="text-sm font-medium leading-none text-foreground">
            Response format
          </legend>
          <div
            role="radiogroup"
            aria-required="false"
            dir="ltr"
            class="flex flex-wrap gap-2"
            tabindex="0"
            style="outline: none;"
          >
            <div
              class="relative flex flex-col items-start gap-4 rounded-lg border border-input p-3 shadow-sm shadow-black/5 has-[[data-state=checked]]:border-ring"
            >
              <div class="flex items-center gap-2">
                <!-- svelte-ignore a11y_consider_explicit_label -->
                <button
                  type="button"
                  role="radio"
                  aria-checked={selectedFormat === "1"}
                  data-state={selectedFormat === "1" ? "checked" : "unchecked"}
                  value="1"
                  class="aspect-square size-4 rounded-full border border-input shadow-sm shadow-black/5 outline-offset-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring/70 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:border-primary data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground after:absolute after:inset-0"
                  id="response-format-plaintext"
                  data-radix-collection-item=""
                  onmousedown={() => (selectedFormat = "1")}
                >
                  {#if selectedFormat === "1"}
                    <span
                      data-state="checked"
                      class="flex items-center justify-center text-current"
                    >
                      <svg
                        width="6"
                        height="6"
                        viewBox="0 0 6 6"
                        fill="currentcolor"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <circle cx="3" cy="3" r="3"></circle>
                      </svg>
                    </span>
                  {/if}
                </button>
                <label
                  class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  for="response-format-plaintext"
                >
                  Plain text
                </label>
              </div>
            </div>

            <div
              class="relative flex flex-col items-start gap-4 rounded-lg border border-input p-3 shadow-sm shadow-black/5 has-[[data-state=checked]]:border-ring"
            >
              <div class="flex items-center gap-2">
                <!-- svelte-ignore a11y_consider_explicit_label -->
                <button
                  type="button"
                  role="radio"
                  aria-checked={selectedFormat === "2"}
                  data-state={selectedFormat === "2" ? "checked" : "unchecked"}
                  value="2"
                  class="aspect-square size-4 rounded-full border border-input shadow-sm shadow-black/5 outline-offset-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring/70 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:border-primary data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground after:absolute after:inset-0"
                  id="response-format-sections"
                  data-radix-collection-item=""
                  onmousedown={() => (selectedFormat = "2")}
                >
                  {#if selectedFormat === "2"}
                    <span
                      data-state="checked"
                      class="flex items-center justify-center text-current"
                    >
                      <svg
                        width="6"
                        height="6"
                        viewBox="0 0 6 6"
                        fill="currentcolor"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <circle cx="3" cy="3" r="3"></circle>
                      </svg>
                    </span>
                  {/if}
                </button>
                <label
                  class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  for="response-format-sections"
                >
                  Sections
                </label>
              </div>
            </div>

            <div
              class="relative flex flex-col items-start gap-4 rounded-lg border border-input p-3 shadow-sm shadow-black/5 has-[[data-state=checked]]:border-ring"
            >
              <div class="flex items-center gap-2">
                <!-- svelte-ignore a11y_consider_explicit_label -->
                <button
                  type="button"
                  role="radio"
                  aria-checked={selectedFormat === "3"}
                  data-state={selectedFormat === "3" ? "checked" : "unchecked"}
                  value="3"
                  class="aspect-square size-4 rounded-full border border-input shadow-sm shadow-black/5 outline-offset-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring/70 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:border-primary data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground after:absolute after:inset-0"
                  id="response-format-json"
                  data-radix-collection-item=""
                  onmousedown={() => (selectedFormat = "3")}
                >
                  {#if selectedFormat === "3"}
                    <span
                      data-state="checked"
                      class="flex items-center justify-center text-current"
                    >
                      <svg
                        width="6"
                        height="6"
                        viewBox="0 0 6 6"
                        fill="currentcolor"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <circle cx="3" cy="3" r="3"></circle>
                      </svg>
                    </span>
                  {/if}
                </button>
                <label
                  class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  for="response-format-json"
                >
                  JSON
                </label>
              </div>
            </div>
          </div>
        </fieldset>
      {/if}
      <div class="w-full flex justify-between">
        <button
          class="text-sm font-medium flex gap-3 items-center border border-input dark:border-gray-500 rounded-md px-4 py-2 hover:bg-[#F6EAEA] hover:text-red-800 hover:outline-1 hover:outline-dashed hover:outline-[#b8040487]"
          onmousedown={handleCancel}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="size-4"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
            />
          </svg>
          Cancel
        </button>
        <button
          class="text-sm font-medium flex gap-4 items-center border border-input dark:border-gray-500 rounded-md px-4 py-2 hover:bg-[#EEF2FF] hover:text-blue-800 hover:outline-1 hover:outline-dashed hover:outline-[#3d3f85] shadow-sm"
          onmousedown={handleSave}
        >
          Save
          <div class="hidden md:flex gap-1 font-xs opacity-50 items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="10"
              height="10"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide lucide-command"
            >
              <path
                d="M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3"
              ></path>
            </svg>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="10"
              height="10"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide lucide-plus"
            >
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="10"
              height="10"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide lucide-corner-down-left"
            >
              <polyline points="9 10 4 15 9 20"></polyline>
              <path d="M20 4v7a4 4 0 0 1-4 4H4"></path>
            </svg>
          </div>
        </button>
      </div>
    </container>
  </div>
</div>
