<script>
  let { title, date, fileExtension, fileNameNoExt, transcription, onDelete } =
    $props();
  import { Eye, ArrowDownToLine, Trash2 } from "lucide-svelte";
  import SpinnerRed from "./Spinner.svelte";
  let hovering = $state(false);
  let deleting = $state(false);
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
      class="text-sm font-medium break-words hyphens-auto line-clamp-2 leading-tight"
    >
      {title}
    </p>
    <p class="text-sm font-geist-mono text-gray-400">{date}</p>
  </div>
  <icons class="flex gap-4 items-center opacity-60 ml-auto pl-2 pr-4 shrink-0">
    <Eye size={22} class="cursor-pointer hover:animate-slow-peek" />
    <ArrowDownToLine
      size={20}
      class="cursor-pointer hover:text-blue-900"
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
