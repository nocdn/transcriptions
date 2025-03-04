<script>
  let {
    label = "Button",
    color = "black",
    hoverColor = "gray",
    icon,
    iconPosition = "leading",
    class: className = "",
    onClick,
  } = $props();
</script>

<button
  onclick={onClick}
  class="text-md font-semibold flex gap-4 items-center border border-gray-200 border-input dark:border-gray-500 rounded-md px-4 py-2 cursor-pointer font-mono {className}"
  >{#if iconPosition === "leading"}{@render icon()}{label}{:else}{label}{@render icon()}{/if}</button
>
