<script>
  let { text: propText, loading: propLoading, rateLimited } = $props();
  let text = $derived(propText);
  let loading = $derived(propLoading);

  import Spinner from "./Spinner.svelte";

  function copyToClipboard() {
    navigator.clipboard.writeText(text);
  }

  function downloadtxt() {
    const trimmedText = text.trim();
    const element = document.createElement("a");
    const file = new Blob([trimmedText], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = "transcription.txt";
    document.body.appendChild(element); // required for this to work in FireFox
    element.click();
  }
</script>

<div
  class="outline-2 outline-dashed outline-gray-300 rounded-md p-4 flex flex-col gap-4 font-geist text-sm font-medium overflow-y-auto mb-6 max-h-full min-h-6"
>
  <div id="header" class="flex justify-between">
    <div class="bg-gray-100 text-xs font-medium p-2 px-3 w-fit rounded-md">
      {#if loading}
        <Spinner />
      {:else if rateLimited}
        <p class="text-red-700">Rate limit exceeded</p>
      {:else}
        <p>Result:</p>
      {/if}
    </div>
    <div
      class="bg-gray-100 text-xs font-medium p-2 px-3 w-fit rounded-md flex gap-2"
    >
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore a11y_missing_attribute -->
      <a class="cursor-pointer" onclick={downloadtxt}>Download .txt</a>
      <p>|</p>
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_missing_attribute -->
      <a class="cursor-pointer" onclick={copyToClipboard}>Copy</a>
    </div>
  </div>
  <p>
    {text}
  </p>
</div>
