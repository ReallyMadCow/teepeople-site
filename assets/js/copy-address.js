async function copyAddress(link) {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(link.textContent.trim());
      return true;
    }
  } catch {
    // Try copying from the selected link when clipboard access is blocked.
  }

  const selection = window.getSelection();
  if (!selection) return false;

  selection.selectAllChildren(link);
  try {
    if (!document.execCommand("copy")) return false;
    selection.removeAllRanges();
    return true;
  } catch {
    // Keep the address selected for manual copying.
    return false;
  }
}

const copyStatus = document.getElementById("copy-address-status");

for (const button of document.querySelectorAll("[data-copy-address]")) {
  const link = button.previousElementSibling;
  const label = button.textContent;
  let reset;

  button.hidden = false;
  button.addEventListener("click", async () => {
    const copied = await copyAddress(link);
    const address = link.textContent.trim();
    clearTimeout(reset);
    button.textContent = copied ? "Copied" : "Copy failed";
    copyStatus.textContent = copied ? `${address} copied.` : `Copy failed. You can copy ${address} manually.`;
    reset = setTimeout(() => {
      button.textContent = label;
    }, 2500);
  });
}
