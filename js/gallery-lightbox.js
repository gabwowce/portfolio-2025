/*
  A small generic lightbox for project screenshots.

  Any element carrying data-gallery (a JSON array of {src, alt}) becomes
  clickable; clicking it - or hitting Enter/Space on it - opens a full-screen
  viewer over the selected image, with prev/next arrows when there is more
  than one shot. This is the only place in the site that needs it, so it is
  one small file rather than a dependency.

  Progressive enhancement: without JS, or if data-gallery fails to parse,
  the element is just a static thumbnail - nothing is hidden behind the
  lightbox that isn't already visible as the card's own image.
*/
(function () {
  "use strict";

  const triggers = document.querySelectorAll("[data-gallery]");
  if (!triggers.length) return;

  let overlay, imgEl, counterEl, items = [], index = 0;

  function build() {
    overlay = document.createElement("div");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.hidden = true;
    overlay.innerHTML = `
      <button type="button" class="lightbox__close" aria-label="Close">✕</button>
      <button type="button" class="lightbox__nav lightbox__nav--prev" aria-label="Previous">‹</button>
      <figure class="lightbox__figure">
        <img class="lightbox__img" alt="" />
        <figcaption class="lightbox__counter"></figcaption>
      </figure>
      <button type="button" class="lightbox__nav lightbox__nav--next" aria-label="Next">›</button>
    `;
    document.body.appendChild(overlay);
    imgEl = overlay.querySelector(".lightbox__img");
    counterEl = overlay.querySelector(".lightbox__counter");

    overlay.querySelector(".lightbox__close").addEventListener("click", close);
    overlay.querySelector(".lightbox__nav--prev").addEventListener("click", () => step(-1));
    overlay.querySelector(".lightbox__nav--next").addEventListener("click", () => step(1));
    overlay.addEventListener("click", (e) => { if (e.target === overlay) close(); });
    document.addEventListener("keydown", (e) => {
      if (overlay.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    });
  }

  function render() {
    const it = items[index];
    imgEl.src = it.src;
    imgEl.alt = it.alt || "";
    counterEl.textContent = items.length > 1 ? `${index + 1} / ${items.length}` : "";
    const multi = items.length > 1;
    overlay.querySelectorAll(".lightbox__nav").forEach((b) => (b.hidden = !multi));
  }

  function step(dir) {
    index = (index + dir + items.length) % items.length;
    render();
  }

  function open(list, startAt) {
    if (!overlay) build();
    items = list;
    index = startAt || 0;
    overlay.hidden = false;
    document.body.style.overflow = "hidden";
    render();
    overlay.querySelector(".lightbox__close").focus();
  }

  function close() {
    if (!overlay) return;
    overlay.hidden = true;
    document.body.style.overflow = "";
  }

  triggers.forEach((el) => {
    let data;
    try {
      data = JSON.parse(el.getAttribute("data-gallery"));
    } catch (e) {
      return;
    }
    if (!Array.isArray(data) || !data.length) return;

    el.setAttribute("role", "button");
    el.setAttribute("tabindex", "0");
    if (data.length > 1 && !el.hasAttribute("aria-label")) {
      el.setAttribute("aria-label", `View ${data.length} screenshots`);
    }
    el.addEventListener("click", () => open(data, 0));
    el.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open(data, 0);
      }
    });
  });
})();
