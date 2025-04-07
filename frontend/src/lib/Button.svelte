<script>
  import { onMount } from "svelte";

  let {
    label = "Button",
    color = "black",
    hoverColor = "gray",
    icon = null,
    iconPosition = "none",
    class: className = "",
    onClick,
  } = $props();

  import tinycolor from "tinycolor2";
  let darkenedHex = $state("");
  let darkestHex = $state("");

  onMount(() => {
    darkenedHex = tinycolor(hoverColor).darken(6).toString();
    darkestHex = tinycolor(hoverColor).darken(70).toString();
  });
</script>

<button
  onclick={onClick}
  class="text-md font-semibold flex gap-4 items-center border border-gray-200 border-input dark:border-gray-500 rounded-md px-4 py-2 cursor-pointer font-jetbrains-mono {className} transition-colors duration-100"
  style="--darkest-color: {darkestHex}; --hover-color: {hoverColor}; --border-color: {darkenedHex}"
  >{#if iconPosition === "leading"}{@render icon()}{label}{:else if iconPosition === "trailing"}{label}{@render icon()}{:else}{label}{/if}</button
>

<style>
  button:hover {
    background-color: var(--hover-color);
    border-color: var(--border-color);
    color: var(--darkest-color);
  }
</style>
