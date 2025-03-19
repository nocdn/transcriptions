<script>
  let { transcriptionText, fileName } = $props();
  import { Save, Copy, ArrowRight, Check, ArrowUp } from "lucide-svelte";
  import Button from "./Button.svelte";

  let copying = $state(false);
  let scrollableContent = $state();
  let showingScrollButton = $state(false);

  $effect(() => {
    if (!scrollableContent) return;

    const handleScroll = () => {
      showingScrollButton = scrollableContent.scrollTop > 20;
    };
    handleScroll();
    scrollableContent.addEventListener("scroll", handleScroll);

    return () => {
      scrollableContent.removeEventListener("scroll", handleScroll);
    };
  });
</script>

{#snippet saveIcon()}
  <Save size={16} />
{/snippet}

{#snippet copyIcon()}
  <Copy size={15} />
{/snippet}

{#snippet checkIcon()}
  <Check size={15} strokeWidth={3} color="darkgreen" />
{/snippet}

<transcription
  class="w-full max-w-full h-full flex flex-col gap-4 relative pl-4 overflow-x-hidden"
>
  {#if transcriptionText !== ""}
    <p
      class="text-xl font-medium pl-2 pt-3 font-geist inline-flex gap-4 items-center motion-opacity-in-0"
    >
      Result <ArrowRight size={16} class="opacity-40" />
      <Button
        label="Download"
        onClick={() => {
          const blob = new Blob([transcriptionText], { type: "text/plain" });
          const url = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.download = fileName.split(".").slice(0, -1).join(".") + ".txt";
          link.click();
        }}
        icon={saveIcon}
        iconPosition="trailing"
        hoverColor="#FAFAFA"
        class="rounded-xl py-1.5 text-sm"
      />
      {#if !copying}
        <Button
          label="Copy"
          onClick={() => {
            copying = true;
            setTimeout(() => {
              copying = false;
            }, 1000);
            navigator.clipboard.writeText(transcriptionText);
          }}
          icon={copyIcon}
          iconPosition="trailing"
          hoverColor="#FAFAFA"
          class="rounded-xl py-1.5 text-sm"
        />
      {:else}
        <Button
          label="Copy"
          onClick={() => {}}
          icon={checkIcon}
          iconPosition="trailing"
          hoverColor="#FAFAFA"
          class="rounded-xl py-1.5 text-sm"
        />
      {/if}
      <span class="font-geist-mono opacity-60 text-sm ml-4 overflow-x-scroll"
        >{fileName}</span
      >
    </p>
    <div class="overflow-y-scroll h-full" bind:this={scrollableContent}>
      <p
        class="text-md pl-2 pr-12"
        style="font-family: system-ui, sans-serif; font-size: 18px; font-weight: 430;"
      >
        {transcriptionText}
      </p>
    </div>
  {/if}

  {#if showingScrollButton}
    <button
      class="absolute bottom-4 right-4 rounded-full h-10 w-10 text-sm py-1.5 shadow-sm bg-white border border-gray-200 grid place-content-center text-black hover:bg-gray-50 motion-opacity-in-0 motion-blur-in-sm transition-all"
      onclick={() => {
        scrollableContent?.scrollTo({ top: 0, behavior: "smooth" });
      }}><ArrowUp strokeWidth={2.5} size={20} /></button
    >
  {/if}
</transcription>
