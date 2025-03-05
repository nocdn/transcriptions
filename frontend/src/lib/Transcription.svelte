<script>
  let { transcriptionText, fileName } = $props();
  import { Save, Copy, ArrowRight, Check } from "lucide-svelte";
  import Button from "./Button.svelte";

  let copying = $state(false);
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

<transcription class="w-full h-full flex flex-col gap-4">
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
    </p>
    <p class="text-md font-geist-mono pl-2">
      {transcriptionText}
    </p>
  {/if}
</transcription>
