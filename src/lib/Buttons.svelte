<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch("buttonClick", {
      message: "The button was clicked!",
      // You can add other data here as needed
    });
  }

  function logClick(button) {
    console.log(`Clicked button: ${button}`);
  }
</script>

<div class="flex gap-3">
  <button
    on:click={() => {
      logClick("Cancel");
      handleClick();
    }}
    class="text-sm font-medium flex gap-3 items-center border border-input dark:border-gray-500 rounded-md px-4 py-2 hover:bg-[#F6EAEA] hover:text-red-800 hover:outline-1 hover:outline-dashed hover:outline-[#b8040487]"
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
        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
      />
    </svg>
    Cancel
  </button>
  <button
    on:click={() => {
      logClick("Submit");
    }}
    class="text-sm font-medium flex gap-4 items-center border border-input dark:border-gray-500 rounded-md px-4 py-2 hover:bg-[#ECF7ED] hover:text-green-950 hover:outline-1 hover:outline-dashed hover:outline-[#3d8549]"
  >
    Submit
    <div class="hidden md:flex gap-1 font-xs opacity-50 items-center">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="10"
        height="10"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="lucide lucide-command"
      >
        <path
          d="M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3"
        ></path>
      </svg>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="10"
        height="10"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="lucide lucide-plus"
      >
        <path d="M5 12h14"></path>
        <path d="M12 5v14"></path>
      </svg>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="10"
        height="10"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="lucide lucide-corner-down-left"
      >
        <polyline points="9 10 4 15 9 20"></polyline>
        <path d="M20 4v7a4 4 0 0 1-4 4H4"></path>
      </svg>
    </div>
  </button>
</div>
