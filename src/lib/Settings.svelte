<script>
  import { Info } from "lucide-svelte";
  import { Zap } from "lucide-svelte";
  import { Languages } from "lucide-svelte";

  let { close } = $props();

  let advancedChecked = $state(false);
  function handleAdvancedCheckbox() {
    advancedChecked = !advancedChecked;
    console.log("Advanced checked:", advancedChecked);
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
      <div class="space-y-2" style="--ring: 234 89% 74%;">
        <label
          class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="prompt-input">Prompt</label
        ><textarea
          class="flex min-h-[80px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 font-sans"
          id="prompt-input"
          placeholder="Enter any prompt, or leave blank"
        ></textarea>
      </div>
      <div class="space-y-2">
        <label
          class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="language-input">Language</label
        >
        <div class="relative">
          <input
            class="flex h-9 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50 peer pe-9"
            id="language-input"
            placeholder="en"
            type="language"
          />
          <div
            class="pointer-events-none absolute inset-y-0 end-0 flex items-center justify-center pe-3 text-muted-foreground/80 peer-disabled:opacity-50"
          >
            <Languages size={15} />
          </div>
        </div>
      </div>
    </container>
  </div>
</div>
