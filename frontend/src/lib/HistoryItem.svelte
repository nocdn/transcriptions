<script>
  let {
    title,
    date,
    fileExtension,
    fileNameNoExt,
    transcription,
    onDelete,
    onShowTranscription,
  } = $props();
  import { Eye, ArrowDownToLine, Trash2 } from "lucide-svelte";
  import SpinnerRed from "./Spinner.svelte";
  let hovering = $state(false);
  let deleting = $state(false);
  let showPopover = $state(false);
  let timer = $state();
</script>

<historyItem
  role="button"
  tabindex="0"
  onmouseenter={() => (hovering = true)}
  onmouseleave={() => (hovering = false)}
  class="bg-white p-2 flex gap-4 items-center rounded-xl hover:bg-gray-50"
>
  <div
    role="button"
    tabindex="0"
    onmousedown={() => {
      deleting = true;
      onDelete();
    }}
    class="w-16 min-h-12 grid place-content-center rounded-lg bg-gray-100 font-geist-mono font-semibold text-center mb-auto hover:bg-[#F6EAEA] transition-all cursor-pointer"
  >
    {#if hovering}
      {#if deleting}
        <SpinnerRed class="motion-preset-fade motion-duration-750" />
      {:else}
        <Trash2
          size={20}
          strokeWidth={2.25}
          class="motion-preset-fade motion-duration-500 text-red-900"
        />
      {/if}
    {:else if deleting}
      <SpinnerRed class="motion-preset-fade motion-duration-750" />
    {:else}
      <p class="motion-preset-fade motion-duration-500">
        {fileExtension}
      </p>
    {/if}
  </div>
  <div class="flex flex-col gap-0.75 min-w-0 flex-1">
    <p
      class="text-sm font-medium break-words hyphens-auto line-clamp-2 leading-tight motion-preset-fade"
    >
      {title}
    </p>
    <p class="text-sm font-geist-mono text-gray-400 motion-preset-fade">
      {date}
    </p>
  </div>
  <icons class="flex gap-4 items-center ml-auto pl-2 pr-4 shrink-0">
    <div class="relative">
      <Eye
        size={22}
        class="cursor-pointer hover:animate-slow-peek opacity-60 hover:opacity-100 transition-opacity"
        onmouseenter={() => {
          timer = setTimeout(() => {
            showPopover = true;
          }, 790);
        }}
        onmouseleave={() => {
          clearTimeout(timer);
          showPopover = false;
        }}
        onclick={() => {
          onShowTranscription(transcription, title);
        }}
      />
      {#if showPopover}
        <div
          class="w-64 h-66 absolute bottom-9 left-1/2 -translate-x-1/2 bg-white rounded-xl border border-gray-200 shadow-xl z-10 p-3 font-geist-mono text-md break-words hyphens-auto animate-preview-popover"
        >
          <p class="line-clamp-[10] overflow-ellipsis">
            {transcription}
          </p>
        </div>
      {/if}
    </div>
    <ArrowDownToLine
      size={20}
      class="cursor-pointer hover:text-blue-900 opacity-60 hover:opacity-100 transition-opacity"
      onclick={() => {
        // download transcription as txt file
        const blob = new Blob([transcription], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = fileNameNoExt + ".txt";
        link.click();
      }}
    />
  </icons>
</historyItem>
