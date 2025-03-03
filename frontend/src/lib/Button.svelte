<script>
  let {
    text,
    onClick,
    icon,
    hoverColor = "",
    iconPosition = "trailing",
  } = $props();
</script>

<button
  class="border border-gray-200 text-sm font-medium flex gap-4 items-center rounded-md px-4 py-2 cursor-pointer"
  onclick={onClick}
  style:color={hoverColor}
  style:--icon-position={iconPosition}
>
  {#if iconPosition === "leading"}
    {icon} {text}
  {/if}
</button>
