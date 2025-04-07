<script>
  import ModelTable from "./ModelTable.svelte";
  import { X } from "lucide-svelte";

  let { onDismiss = () => {} } = $props();

  let dismissing = $state(false);
  function dismissModal() {
    dismissing = true;
    setTimeout(() => {
      onDismiss();
    }, 300);
  }
</script>

<overlay
  class="fixed top-0 left-0 w-full h-full bg-black/50 z-30 flex items-center justify-center {dismissing
    ? 'animate-bg-fade-out'
    : 'animate-bg-fade-in'}"
  onmousedown={dismissModal}
  role="dialog"
  tabindex="0"
>
  <modal
    class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-1/2 max-w-116 min-w-116 flex flex-col gap-3 overflow-y-scroll {dismissing
      ? 'animate-settings-modal-down'
      : 'animate-settings-modal-up'}"
  >
    <p class="text-md font-bold font-jetbrains-mono flex justify-between ml-1">
      MODEL STATS <X size={16} class="cursor-pointer" />
    </p>
    <ModelTable />
  </modal>s
</overlay>
