<script>
  import { FilePlus2, FileAudio } from "lucide-svelte";
  import Spinner from "./Spinner.svelte";

  let {
    handleFiles,
    files = $bindable([]),
    maxSize = "40MB",
    processing = false,
  } = $props();
  let inputFileName = $derived(files.length > 0 ? files[0].name : ""); //derive inputFileName

  // Add additional variable for styles
  let dropzoneClass =
    "rounded-2xl bg-[#FAFAFA] border-2 border-dotted border-gray-300 min-h-48 w-full flex flex-col justify-center items-center gap-5 p-4 text-center cursor-pointer";

  function onDrop(event) {
    event.preventDefault();
    const droppedFiles = event.dataTransfer.files;
    if (droppedFiles.length > 0) {
      files = droppedFiles;
      handleFiles(files);
      console.log(`Dropped file: ${files[0]?.name}`);
    }
    event.currentTarget.classList.remove("dragover");
  }

  function calculateFileSizeColor(size) {
    if (size < 1024 * 1024 * 10) {
      return "text-green-600";
    } else if (size < 1024 * 1024 * 40) {
      return "text-yellow-600";
    } else {
      return "text-red-600";
    }
  }

  // Format file size to human-readable format
  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";

    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  function onSelect(event) {
    const selectedFiles = event.target.files;
    if (selectedFiles.length > 0) {
      files = selectedFiles;
      handleFiles(files);
      console.log(`Selected file: ${files[0].name}`);
    }
  }

  function openFileDialog() {
    if (!processing) {
      document.getElementById("fileInput").click();
    }
  }

  function onDragOver(event) {
    event.preventDefault();
    if (!processing) {
      event.currentTarget.classList.add("dragover");
    }
  }

  function onDragLeave(event) {
    event.currentTarget.classList.remove("dragover");
  }
</script>

<!-- Hidden file input element -->
<input
  id="fileInput"
  type="file"
  accept="audio/*,video/*"
  onchange={onSelect}
  class="hidden"
/>

<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<dropzone
  tabindex="0"
  onclick={openFileDialog}
  ondrop={onDrop}
  ondragover={onDragOver}
  ondragleave={onDragLeave}
  onkeydown={(e) => e.key === "Enter" && openFileDialog()}
  class="{dropzoneClass} {processing ? 'pointer-events-none opacity-80' : ''}"
>
  {#if !processing}
    {#if files.length > 0}
      <div class="bg-white rounded-xl p-3 border border-gray-200">
        <FileAudio size={20} />
      </div>
      <div class="flex flex-col gap-0.5">
        <div class="flex justify-center">
          <p
            class="text-md font-medium break-words hyphens-auto line-clamp-2 leading-tight max-w-4/5 flex"
          >
            {files[0].name}
          </p>
        </div>
        <p class="font-[450] {calculateFileSizeColor(files[0].size)}">
          {formatFileSize(files[0].size)}
        </p>
        <p class="opacity-50 text-sm mt-1">Click to choose a different file</p>
      </div>
    {:else}
      <div class="bg-white rounded-xl p-3 border border-gray-200">
        <FilePlus2 size={20} />
      </div>
      <div class="flex flex-col gap-0.5">
        <p class="text-md font-medium">Click to upload, or drag and drop</p>
        <p class="opacity-50 font-[450]">
          Audio or video files up to {maxSize} each
        </p>
      </div>
    {/if}
  {:else}
    <div class="flex flex-col gap-0.5 items-center justify-center">
      <Spinner />
      <p class="text-md font-medium motion-opacity-in-0">Transcribing...</p>
      <p class="text-sm font-geist-mono opacity-40">please be patient</p>
    </div>
  {/if}
</dropzone>
