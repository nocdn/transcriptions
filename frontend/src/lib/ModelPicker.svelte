<script>
  import { ChevronDown } from "lucide-svelte";
  let { onChoice, modelChoice } = $props();
</script>

<models class="space-y-1 inline-flex flex-col">
  <label
    class="text-sm font-medium font-mono leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
    for="model-select">Select model</label
  >
  <div class="relative">
    <select
      class="peer font-geist-mono inline-flex w-full cursor-pointer appearance-none items-center rounded-lg border border-gray-200 border-input bg-background text-sm text-foreground shadow-sm shadow-black/5 transition-shadow focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 has-[option[disabled]:checked]:text-muted-foreground h-9 pe-8 ps-3"
      id="model-select"
      bind:value={modelChoice}
      onchange={() => {
        onChoice(modelChoice);
      }}
      ><option value="whisper-large-v3">whisper-large-v3</option><option
        value="whisper-large-v3-turbo">whisper-large-v3-turbo</option
      ><option value="distil-whisper-large-v3-en"
        >distil-whisper-large-v3</option
      ><option value="gemini-2.0-flash">gemini-2.0-flash</option><option
        value="gemini-2.0-flash-lite-preview-02-05"
        >gemini-2.0-flash-lite</option
      ><option value="gemini-2.0-pro-exp-02-05">gemini-2.0-pro</option><option
        value="fireworks/whisper-v3-turbo">fireworks/whisper-v3-turbo</option
      ><option value="scribe_v1">scribe v1</option></select
    ><span
      class="pointer-events-none absolute inset-y-0 end-0 flex h-full w-9 items-center justify-center text-muted-foreground/80 peer-disabled:opacity-50"
      ><ChevronDown size={16} /></span
    >
  </div>
</models>
