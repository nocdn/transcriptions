<script>
  let { title, date, fileExtension, fileNameNoExt, transcription } = $props();
  import { Eye, ArrowDownToLine } from "lucide-svelte";
</script>

<historyItem class="bg-white p-2 flex gap-4 items-center rounded-xl">
  <p
    class="w-16 h-12 grid place-content-center rounded-lg bg-gray-100 font-geist-mono font-semibold text-center"
  >
    {fileExtension}
  </p>
  <div class="flex flex-col gap-0.75">
    <p class="text-md font-medium">{title}</p>
    <p class="text-sm font-geist-mono text-gray-400">{date}</p>
  </div>
  <icons class="flex gap-4 items-center opacity-60 ml-auto pr-4">
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
