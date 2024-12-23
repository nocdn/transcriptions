<script>
  let text = "";
  export { text };

  function copyToClipboard() {
    navigator.clipboard.writeText(text);
  }
</script>

<div
  class="outline-2 outline-dashed outline-gray-300 rounded-md p-4 flex flex-col gap-4 font-sans text-sm font-medium"
>
  <div id="header" class="flex justify-between">
    <p class="bg-gray-100 text-xs font-medium p-2 w-fit rounded-md">Result:</p>
    <div
      class="bg-gray-100 text-xs font-medium p-2 w-fit rounded-md flex gap-2"
    >
      <a class="">Download .txt</a>
      <p>|</p>
      <a href="#" onclick={copyToClipboard}>Copy</a>
    </div>
  </div>
  {text}
</div>
