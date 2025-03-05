<script>
  import { Info, Zap } from "lucide-svelte";
</script>

<models
  class="overflow-hidden border border-gray-300 rounded-lg font-geist-mono"
>
  <table class="w-full caption-bottom text-sm">
    <thead class="bg-[#f9f9fa]">
      <tr
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted bg-muted/50"
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
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular"
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
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular"
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
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular"
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
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular"
          >gemini-2.0-flash</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >$0.063</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >?</td
        >
      </tr>
      <tr
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular"
          >gemini-2.0-flash-lite</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >$0.00675</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >?</td
        >
      </tr>
      <tr
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular"
          >gemini-2.0-pro</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >free</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >?</td
        >
      </tr>

      <tr
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular flex items-center gap-2"
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
      <tr
        class="border-b border-gray-200 transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
      >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2 font-regular"
          >scribe v1</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >$6.67</td
        >
        <td
          class="p-3 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-0.5 py-2"
          >7.7%</td
        >
      </tr>
    </tbody>
  </table>
</models>
