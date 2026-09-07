document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".code-block__copy[data-copy]").forEach((btn) => {
    const block = btn.closest(".code-block");
    const code = block && block.querySelector("pre");
    if (!code) return;

    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        const original = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => {
          btn.textContent = original;
        }, 1800);
      } catch {
        btn.textContent = "Copy failed";
      }
    });
  });
});
