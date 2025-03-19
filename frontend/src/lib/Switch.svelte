<script>
  let {
    checked = false,
    label = null,
    disabled = false,
    id = null,
    onToggle,
    class: className = "",
  } = $props();

  function toggle() {
    if (disabled) return;
    // if first time, check if permission to send browser notifications is granted
    if (Notification.permission !== "granted") {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          console.log("Notifications permission granted");
          checked = !checked;
          onToggle(checked);
        } else {
          console.log("Notifications permission denied");
          return;
        }
      });
    } else {
      checked = !checked;
      onToggle(checked);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      toggle();
    }
  }
</script>

<div class="flex items-center {className}">
  {#if label}
    <label for={id} class="mr-2 text-sm font-medium text-gray-700">
      {label}
    </label>
  {/if}

  <button
    type="button"
    {id}
    aria-checked={checked}
    aria-label={label || "Toggle"}
    role="switch"
    tabindex="0"
    class="relative inline-flex h-6 w-11 items-center rounded-full {checked
      ? 'bg-blue-200'
      : 'bg-gray-200'}
                     transition-colors duration-200 ease-in-out focus:outline-none
                     {disabled
      ? 'opacity-50 cursor-not-allowed'
      : 'cursor-pointer'}"
    onclick={toggle}
    onkeydown={handleKeyDown}
    {disabled}
  >
    <span class="sr-only">{label || "Toggle"}</span>
    <span
      aria-hidden="true"
      class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform duration-200 ease-in-out {checked
        ? 'translate-x-5.5'
        : 'translate-x-0.5'}"
    ></span>
  </button>
</div>
