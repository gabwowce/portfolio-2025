document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".newsletter");
  if (!form) return;

  const btn = form.querySelector("button");
  const note = form.querySelector(".form-note");

  // Tiny inline SVG icons
  const icons = {
    spinner:
      '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="3" opacity=".25"/><path class="svg-spin" d="M12 3a9 9 0 0 1 9 9" fill="none" stroke="currentColor" stroke-width="3"/></svg>',
    check:
      '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    cross:
      '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>',
  };

  const setBtnState = (state, text, noteText = "", noteKind = "") => {
    btn.classList.remove("is-sending", "is-ok", "is-err");
    note.className = "form-note";
    if (state) btn.classList.add(state);
    note.textContent = "";
    if (noteText) {
      note.textContent = noteText;
      if (noteKind) note.classList.add(noteKind);
    }
    btn.innerHTML = text; // replace button content (icon + label)
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Sending…
    btn.disabled = true;
    setBtnState("is-sending", `${icons.spinner} Sending…`);

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: {
          Accept: "application/json",
        },
      });

      if (res.ok) {
        form.reset();
        setBtnState(
          "is-ok",
          `${icons.check} Sent`,
          "Thanks! Your message was sent.",
          "ok"
        );
      } else {
        let msg = "Could not send. Please try again.";
        try {
          const data = await res.json();
          if (
            data &&
            Array.isArray(data.errors) &&
            data.errors[0] &&
            typeof data.errors[0].message === "string"
          ) {
            msg = data.errors[0].message;
          }
        } catch (_) {}
        setBtnState("is-err", `${icons.cross} Try again`, msg, "err");
      }
    } catch {
      setBtnState(
        "is-err",
        `${icons.cross} Try again`,
        "Network error. Check your connection and try again.",
        "err"
      );
    } finally {
      // Restore default button after 3.5s
      setTimeout(() => {
        btn.disabled = false;
        setBtnState("", "Say hi 👋");
      }, 8000);
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  /* Header blur tik kai scroll > 8px */
  const setScrolled = () => {
    document.documentElement.classList.toggle("scrolled", window.scrollY > 8);
  };
  setScrolled();
  window.addEventListener("scroll", setScrolled, {
    passive: true,
  });

  /* Process rail – tik jei yra DOM'e */
  const rail = document.getElementById("processRail");
  if (rail) {
    const updateProgress = () => {
      const rect = rail.getBoundingClientRect();
      const vh = window.innerHeight || document.documentElement.clientHeight;
      const visible = Math.max(
        0,
        Math.min(rect.bottom, vh) - Math.max(rect.top, 0)
      );
      const ratio = Math.max(
        0,
        Math.min(1, visible / Math.min(rect.height, vh))
      );
      rail.style.setProperty("--progress", ratio.toFixed(3));
    };
    updateProgress();
    window.addEventListener("scroll", updateProgress, {
      passive: true,
    });
    window.addEventListener("resize", updateProgress);

    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            rail.style.setProperty("--pct", "100");
          }
        });
      },
      {
        threshold: 0.2,
      }
    );
    obs.observe(rail);
  }

  /* Segmented filtras (jei naudojamas) */
  const seg = document.querySelector(".segmented");
  if (seg) {
    const btns = Array.from(seg.querySelectorAll(".seg-btn"));
    let thumb = seg.querySelector(".seg-thumb");
    if (!thumb) {
      thumb = document.createElement("span");
      thumb.className = "seg-thumb";
      seg.prepend(thumb);
    }

    const moveThumb = (btn) => {
      const x = btn.offsetLeft;
      const w = btn.offsetWidth;
      thumb.style.width = w + "px";
      thumb.style.transform = `translateX(${x}px)`;
    };

    const setActive = (btn) => {
      btns.forEach((b) => {
        const active = b === btn;
        b.classList.toggle("is-active", active);
        b.setAttribute("aria-selected", String(active));
      });
      moveThumb(btn);
    };

    // init
    const current = seg.querySelector(".seg-btn.is-active") || btns[0];
    if (current) setActive(current);

    // click
    seg.addEventListener("click", (e) => {
      const btn = e.target.closest(".seg-btn");
      if (!btn) return;
      setActive(btn);

      const f = btn.dataset.filter; // 'all' | 'web' | 'mobile' | ...
      // Numatytai filtruoja projektus; kiti sąrašai (pvz. resursų temos)
      // nurodo savo taikinį per data-filter-target.
      const target = seg.dataset.filterTarget || ".featured-grid .project";
      document.querySelectorAll(target).forEach((card) => {
        const cats = (card.dataset.cat || "").split(/\s+/); // palaiko 'web desktop'
        const show = f === "all" || cats.includes(f);
        card.classList.toggle("is-hidden", !show);
      });
    });

    // responsive – perbraižyti poziciją
    window.addEventListener("resize", () =>
      moveThumb(seg.querySelector(".seg-btn.is-active") || btns[0])
    );
  }
});

(function () {
  if (window.__navInit) return;
  window.__navInit = true;

  var body = document.body;
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("primaryNav");
  var overlay = document.getElementById("navOverlay");
  var closeBtn = document.getElementById("navClose");

  function setNavOpen(open) {
    body.classList.toggle("nav-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", String(open));
    if (overlay) overlay.hidden = !open;
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      setNavOpen(!body.classList.contains("nav-open"));
    });
  }
  if (overlay) {
    overlay.addEventListener("click", function () {
      setNavOpen(false);
    });
  }
  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      setNavOpen(false);
    });
  }
  if (nav) {
    nav.addEventListener("click", function (e) {
      if (e && e.target && e.target.closest && e.target.closest("a")) {
        setNavOpen(false);
      }
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setNavOpen(false);
  });
})();
/* === Featured image rotator === */
(() => {
  const wrap = document.querySelector(".project-xl .container-canva");
  if (!wrap) return;

  const track = wrap.querySelector("#card .slides");
  const slides = Array.from(track ? track.children : []);
  const dots = wrap.querySelector(".carousel-ui .dots");
  const carEl = wrap.querySelector("#card .carousel");
  if (!track || slides.length < 2 || !dots || !carEl) return;

  const intervalMs = Number(carEl.getAttribute("data-auto")) || 3000;

  // sukurti dots
  slides.forEach((_, idx) => {
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("aria-label", `Go to slide ${idx + 1}`);
    b.addEventListener("click", () => go(idx, true));
    dots.appendChild(b);
  });

  let i = 0,
    timer = null;
  const update = () => {
    track.style.transform = `translateX(-${i * 100}%)`;
    dots
      .querySelectorAll("button")
      .forEach((b, idx) => b.setAttribute("aria-current", String(idx === i)));
  };
  const go = (to, user = false) => {
    i = (to + slides.length) % slides.length;
    update();
    if (user) restart();
  };
  const nextSlide = () => go(i + 1);

  const start = () => {
    if (!timer) timer = setInterval(nextSlide, intervalMs);
  };
  const stop = () => {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  };
  const restart = () => {
    stop();
    start();
  };

  // pauzė ant hover
  wrap.addEventListener("mouseenter", stop);
  wrap.addEventListener("mouseleave", start);

  // start tik kai matoma
  const io = new IntersectionObserver(
    ([e]) => {
      e.isIntersecting ? start() : stop();
    },
    {
      threshold: 0.2,
    }
  );
  io.observe(wrap);

  // init
  update();
})();
// Lengvas IO su „stagger“
(() => {
  const opts = { threshold: 0.12, rootMargin: "0px 0px -8% 0px" };

  // 1) Grupės: .u-stagger (vaikai po vieną su delay)
  const ioGroup = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const wrap = e.target;

      // paimam TIK animuojamus vaikus
      const kids = Array.from(wrap.querySelectorAll(":scope > .u-reveal"));
      // nustatom jų indeksą --i (kad neskaičiuotų neanimuojamų elementų)
      kids.forEach((el, i) => el.style.setProperty("--i", i));

      // uždedam in-view klases (delay pritaikys CSS pagal --i ir --stagger)
      wrap.classList.add("is-inview");
      kids.forEach((el) => el.classList.add("is-inview"));

      ioGroup.unobserve(wrap); // vieną kartą
    });
  }, opts);

  document.querySelectorAll(".u-stagger").forEach((w) => ioGroup.observe(w));

  // 2) Pavieniai elementai: .u-reveal (ne esantys u-stagger vaikais)
  const ioSingle = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-inview");
      ioSingle.unobserve(e.target);
    });
  }, opts);

  document.querySelectorAll(".u-reveal").forEach((el) => {
    // jei nėra artimo .u-stagger tėvo – animuojam kaip singlą
    const parent = el.parentElement;
    if (!(parent && parent.classList.contains("u-stagger"))) {
      ioSingle.observe(el);
    }
  });
})();

(function () {
  var a = document.getElementById("langSwitch");
  if (!a) return;

  var p = location.pathname;

  // heuristika: /lt/... ↔ /en/...
  var isLT = p.indexOf("/lt/") !== -1;
  var isEN = p.indexOf("/en/") !== -1;

  function swapLang(path) {
    if (path.indexOf("/lt/") !== -1) return path.replace("/lt/", "/en/");
    if (path.indexOf("/en/") !== -1) return path.replace("/en/", "/lt/");
    // jei ne LT ir ne EN, darykim prielaidą, kad dabar LT ir veskim į EN root
    return "/en/";
  }

  var target = swapLang(p);

  a.href = target;
  a.textContent = isLT ? "EN" : "LT";
  a.setAttribute("hreflang", isLT ? "en" : "lt");
  a.setAttribute(
    "aria-label",
    isLT ? "Switch to English" : "Perjungti į lietuvių"
  );
})();

// Hero mouse-parallax + cursor spotlight.
// Sets --mx/--my (cursor position) and --px/--py (-1..1 offset from
// center) on .hero; css/hero.css does the actual transforms. Skipped
// entirely for reduced-motion or touch-only devices — hover:none
// devices have no cursor to react to anyway.
(function () {
  var hero = document.querySelector(".hero");
  if (!hero) return;

  var reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  var noHover = window.matchMedia("(hover: none)").matches;
  if (reduceMotion || noHover) return;

  var raf = null;
  var targetX = 0.5,
    targetY = 0.4;

  function apply() {
    raf = null;
    hero.style.setProperty("--mx", targetX * 100 + "%");
    hero.style.setProperty("--my", targetY * 100 + "%");
    hero.style.setProperty("--px", (targetX * 2 - 1).toFixed(3));
    hero.style.setProperty("--py", (targetY * 2 - 1).toFixed(3));
  }

  hero.addEventListener("pointerleave", function () {
    targetX = 0.5;
    targetY = 0.4;
    if (!raf) raf = requestAnimationFrame(apply);
  });
  hero.addEventListener("pointermove", function (e) {
    var rect = hero.getBoundingClientRect();
    targetX = Math.min(1, Math.max(0, (e.clientX - rect.left) / rect.width));
    targetY = Math.min(1, Math.max(0, (e.clientY - rect.top) / rect.height));
    if (!raf) raf = requestAnimationFrame(apply);
  });
})();

/*
  Theme toggle.
  ------------------------------------------------------------------
  The source of truth is the data-theme attribute on <html>:

    absent            -> follow the OS, via prefers-color-scheme in CSS
    "light" / "dark"  -> the visitor chose, and that overrides the OS

  A stored choice is already applied by the inline script in <head>, so
  this file only handles clicks and keeps the browser UI colour in step.
  Nothing here runs before paint, so there is no flash either way.
*/
(function () {
  var root = document.documentElement;
  var btn = document.getElementById("themeToggle");
  if (!btn) return;

  var darkMedia = window.matchMedia
    ? window.matchMedia("(prefers-color-scheme: dark)")
    : null;

  function activeTheme() {
    var chosen = root.getAttribute("data-theme");
    if (chosen === "dark" || chosen === "light") return chosen;
    return darkMedia && darkMedia.matches ? "dark" : "light";
  }

  /*
    Keep the address-bar / task-switcher colour matching the page. The
    value is read from the live tokens so it can never drift from the
    palette in style.css.
  */
  function syncBrowserChrome() {
    var meta = document.querySelector('meta[name="theme-color"]');
    if (!meta) return;
    var bg = getComputedStyle(root).getPropertyValue("--bg").trim();
    if (bg) meta.setAttribute("content", bg);
  }

  function setTheme(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("theme", theme);
    } catch (e) {
      /* private mode: the choice just won't outlive the tab */
    }
    syncBrowserChrome();
  }

  btn.addEventListener("click", function () {
    setTheme(activeTheme() === "dark" ? "light" : "dark");
  });

  /*
    With no explicit choice stored, follow the OS if it changes while
    the page is open. A stored choice keeps winning.
  */
  if (darkMedia && darkMedia.addEventListener) {
    darkMedia.addEventListener("change", function () {
      if (!root.getAttribute("data-theme")) syncBrowserChrome();
    });
  }

  syncBrowserChrome();
})();

/*
  Page-wide cursor light.
  ------------------------------------------------------------------
  Feeds the mask position for body::after, in viewport coordinates, so
  the lit grid follows the pointer on every page rather than only
  inside the hero. Writes to the root element, not to a section, and
  only ever sets two custom properties - the painting is entirely CSS.
*/
(function () {
  var root = document.documentElement;
  if (!window.matchMedia) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (window.matchMedia("(hover: none)").matches) return;

  var x = 0, y = 0, raf = null;

  function paint() {
    raf = null;
    root.style.setProperty("--gx", x + "px");
    root.style.setProperty("--gy", y + "px");
  }

  window.addEventListener(
    "pointermove",
    function (e) {
      x = e.clientX;
      y = e.clientY;
      if (!root.classList.contains("cursor-lit")) root.classList.add("cursor-lit");
      if (!raf) raf = requestAnimationFrame(paint);
    },
    { passive: true }
  );

  /* Fade the light out when the pointer leaves the window entirely. */
  document.addEventListener("pointerleave", function () {
    root.classList.remove("cursor-lit");
  });
})();
