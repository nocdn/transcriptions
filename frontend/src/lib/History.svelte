<script>
  let { onButtonClick } = $props();
</script>

<button
  onclick={() => {
    onButtonClick("history");
  }}
  class="text-sm font-medium flex gap-3 items-center border border-input dark:border-gray-500 rounded-md px-4 py-2 hover:bg-gray-100 hover:text-gray-700 hover:outline-1 hover:outline-dashed hover:outline-gray-300"
>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="1.5"
    stroke="currentColor"
    class="size-4"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
    />
  </svg>
  History
</button>
