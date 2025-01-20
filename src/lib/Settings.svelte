<script>
  import { Info } from "lucide-svelte";

  let { close } = $props();
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
  class="fixed top-0 left-0 w-full h-full bg-black/50 z-10 flex items-center justify-center"
  onmousedown={close}
>
  <div
    class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-1/2 max-w-md"
    onmousedown={(e) => e.stopPropagation()}
  >
    <h2 class="text-2xl font-semibold mb-4 dark:text-white">Settings</h2>
    <container class="flex flex-col gap-4">
      <p class="mb-4 dark:text-gray-300">Model:</p>
      <div class="space-y-2">
        <label
          class="text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="model-select">Select model</label
        >
        <div class="relative">
          <select
            class="peer inline-flex w-full cursor-pointer appearance-none items-center rounded-lg border border-input bg-background text-sm text-foreground shadow-sm shadow-black/5 transition-shadow focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 has-[option[disabled]:checked]:text-muted-foreground h-9 pe-8 ps-3"
            id="model-select"
            ><option value="whisper-large-v3-turbo"
              >whisper-large-v3-turbo</option
            ><option value="whisper-large-v3-en">whisper-large-v3-en</option
            ><option value="gemini-2.0-flash-exp">gemini-2.0-flash-exp</option
            ><option value="gemini-1.5-flash-latest"
              >gemini-1.5-flash-latest</option
            ><option value="gemini-1.5-flash-8b">gemini-1.5-flash-8b</option
            ><option value="gemini-1.5-pro-002">gemini-1.5-pro-002</option
            ><option value="accounts/fireworks/models/whisper-v3-turbo"
              >fireworks/whisper-v3-turbo</option
            ></select
          ><span
            class="pointer-events-none absolute inset-y-0 end-0 flex h-full w-9 items-center justify-center text-muted-foreground/80 peer-disabled:opacity-50"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide lucide-chevron-down"
              aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg
            ></span
          >
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Whisper models:</th>
            <th>Cost /h</th>
            <th
              title="Word Error Rate: ratio of errors to the total number of words in reference. Lower is better."
              style="display: flex; align-items: center; gap: 8px"
            >
              WER <Info />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>large</td>
            <td>$0.111</td>
            <td>10.3%</td>
          </tr>
          <tr>
            <td>large-turbo</td>
            <td>$0.04</td>
            <td>12%</td>
          </tr>
          <tr>
            <td>distil-large</td>
            <td>$0.02</td>
            <td>13%</td>
          </tr>
          <tr>
            <td style="font-weight: bold; padding-top: 10px">
              Gemini models:
            </td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>gemini-1.5-flash</td>
            <td>$6.75</td>
            <td>9.6%</td>
          </tr>
          <tr>
            <td>gemini-1.5-pro</td>
            <td>$112.50</td>
            <td>5.5%</td>
          </tr>
        </tbody>
      </table>
    </container>
  </div>
</div>
