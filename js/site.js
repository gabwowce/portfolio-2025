/*
  codeart.lt – the little behaviour the site needs, nothing else:
  mobile menu, FAQ, the sliding nav underline, reveal on scroll and
  the contact form. Every block checks for its own markup first, so
  the same file runs on every page.
*/
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");
  window.__site = true;

  var reduceMotion =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------- */
  /* Mobile menu                                                      */
  /* ---------------------------------------------------------------- */
  (function () {
    var toggle = document.querySelector("[data-menu-open]");
    var menu = document.getElementById("mobile-menu");
    if (!toggle || !menu) return;
    var closeBtn = menu.querySelector("[data-menu-close]");

    function open() {
      menu.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
      document.body.classList.add("is-locked");
      if (closeBtn) closeBtn.focus();
    }

    function close(returnFocus) {
      if (menu.hidden) return;
      menu.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("is-locked");
      if (returnFocus) toggle.focus();
    }

    toggle.addEventListener("click", open);
    if (closeBtn) {
      closeBtn.addEventListener("click", function () {
        close(true);
      });
    }

    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) close(false);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close(true);
    });

    /* Keep focus inside the open menu. */
    menu.addEventListener("keydown", function (e) {
      if (e.key !== "Tab") return;
      var items = menu.querySelectorAll("a[href], button");
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    /* A menu left open on a phone must not stay open on a wide screen. */
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1100) close(false);
    });
  })();

  /* ---------------------------------------------------------------- */
  /* FAQ                                                              */
  /* ---------------------------------------------------------------- */
  (function () {
    var buttons = document.querySelectorAll("[data-faq]");
    if (!buttons.length) return;

    function set(btn, open) {
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      if (panel) panel.hidden = !open;
    }

    /* Answers are readable without JS; with JS they start closed. */
    buttons.forEach(function (btn) {
      set(btn, false);
      btn.addEventListener("click", function () {
        var willOpen = btn.getAttribute("aria-expanded") !== "true";
        buttons.forEach(function (other) {
          if (other !== btn) set(other, false);
        });
        set(btn, willOpen);
      });
    });
  })();

  /* ---------------------------------------------------------------- */
  /* Sticky header: shadow once the page has scrolled                 */
  /* ---------------------------------------------------------------- */
  (function () {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var raf = null;
    function update() {
      raf = null;
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    }
    window.addEventListener(
      "scroll",
      function () {
        if (!raf) raf = requestAnimationFrame(update);
      },
      { passive: true }
    );
    update();
  })();

  /* ---------------------------------------------------------------- */
  /* Lightbox for screenshots (native <dialog>)                       */
  /* ---------------------------------------------------------------- */
  (function () {
    var dialog = document.getElementById("lightbox");
    if (!dialog || typeof dialog.showModal !== "function") return;
    var img = dialog.querySelector("img");
    var caption = dialog.querySelector("figcaption");

    document.querySelectorAll("[data-lightbox]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var text = btn.getAttribute("data-caption") || "";
        img.src = btn.getAttribute("data-lightbox");
        img.alt = text;
        caption.textContent = text;
        dialog.showModal();
      });
    });

    dialog.querySelector("[data-lightbox-close]").addEventListener("click", function () {
      dialog.close();
    });
    /* A click on the dark backdrop (outside the picture) closes it. */
    dialog.addEventListener("click", function (e) {
      if (e.target === dialog) dialog.close();
    });
    dialog.addEventListener("close", function () {
      img.removeAttribute("src");
    });
  })();

  /* ---------------------------------------------------------------- */
  /* Reveal on scroll – each element animates once                    */
  /* ---------------------------------------------------------------- */
  (function () {
    var els = document.querySelectorAll("[data-reveal]");
    if (!els.length) return;

    function showAll() {
      els.forEach(function (el) {
        el.classList.add("is-in");
      });
    }

    if (reduceMotion || !("IntersectionObserver" in window)) {
      showAll();
      return;
    }

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
    );

    els.forEach(function (el) {
      io.observe(el);
    });

    /* Anything already above the fold when we jump to an anchor. */
    window.addEventListener("load", function () {
      els.forEach(function (el) {
        if (el.getBoundingClientRect().bottom < 0) el.classList.add("is-in");
      });
    });
  })();

  /* ---------------------------------------------------------------- */
  /* Project brief template (article) – PDF, copy, or send it         */
  /* through the contact form. Nothing leaves the browser until the   */
  /* visitor sends the contact form themselves.                       */
  /* ---------------------------------------------------------------- */
  var BRIEF_KEY = "codeart-brief";

  function store(kind) {
    try { return window[kind]; } catch (e) { return null; }
  }

  document.querySelectorAll("form[data-brief]").forEach(function (form) {
    var fields = Array.prototype.slice.call(form.querySelectorAll("input, textarea"));
    var status = form.querySelector(".brief__status");
    var draftKey = BRIEF_KEY + "-draft";
    var local = store("localStorage");

    function say(text, isError) {
      status.textContent = text;
      status.classList.toggle("is-error", !!isError);
    }

    /* keep what was typed if the visitor leaves and comes back */
    try {
      var saved = JSON.parse((local && local.getItem(draftKey)) || "{}");
      fields.forEach(function (f) { if (saved[f.name]) f.value = saved[f.name]; });
    } catch (e) { /* no saved draft */ }
    form.addEventListener("input", function () {
      var data = {};
      fields.forEach(function (f) { data[f.name] = f.value; });
      try { if (local) local.setItem(draftKey, JSON.stringify(data)); } catch (e) { /* storage off */ }
    });

    function text() {
      return fields
        .filter(function (f) { return f.value.trim(); })
        .map(function (f) { return f.name + ":\n" + f.value.trim(); })
        .join("\n\n");
    }

    function withText(fn) {
      var t = text();
      if (!t) { say(form.getAttribute("data-msg-empty"), true); return; }
      fn(t);
    }

    form.querySelector("[data-brief-copy]").addEventListener("click", function () {
      withText(function (t) {
        var ok = function () { say(form.getAttribute("data-msg-copied"), false); };
        var fail = function () { say(form.getAttribute("data-msg-copy-fail"), true); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(t).then(ok, fail);
        } else {
          fail();
        }
      });
    });

    form.querySelector("[data-brief-pdf]").addEventListener("click", function () {
      var btn = this;
      withText(function () {
        btn.disabled = true;
        say(form.getAttribute("data-msg-pdf-busy"), false);
        briefPdf(form).then(function () {
          say(form.getAttribute("data-msg-pdf-done"), false);
        }, function () {
          say(form.getAttribute("data-msg-pdf-fail"), true);
        }).then(function () { btn.disabled = false; });
      });
    });

    form.querySelector("[data-brief-send]").addEventListener("click", function () {
      withText(function (t) {
        var session = store("sessionStorage");
        try { if (session) session.setItem(BRIEF_KEY, t); } catch (e) { /* storage off */ }
        window.location.href = form.getAttribute("data-contact-url");
      });
    });
  });

  /* ---------------------------------------------------------------- */
  /* Brief as a PDF. pdfmake and the font load only on the first click */
  /* and the file is made in the browser, so nothing is sent anywhere. */
  /* ---------------------------------------------------------------- */
  var PDFMAKE = "/js/vendor/pdfmake-0.2.10.min.js";
  var PDF_FONTS = { "sg-regular.ttf": "/fonts/pdf/schibsted-grotesk-Regular.ttf",
                    "sg-semibold.ttf": "/fonts/pdf/schibsted-grotesk-SemiBold.ttf" };
  var MONTHS = ["sausio", "vasario", "kovo", "balandžio", "gegužės", "birželio", "liepos",
                "rugpjūčio", "rugsėjo", "spalio", "lapkričio", "gruodžio"];
  var C = { accent: "#a9502f", text: "#1c1a17", body: "#36322d", muted: "#6a635a",
            line: "#ddd2c1", sand: "#f6f0e6" };
  var pdfReady = null;

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var tag = document.createElement("script");
      tag.src = src;
      tag.onload = resolve;
      tag.onerror = reject;
      document.head.appendChild(tag);
    });
  }

  function toBase64(buffer) {
    var bytes = new Uint8Array(buffer), out = "";
    for (var i = 0; i < bytes.length; i += 0x8000) {
      out += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    }
    return btoa(out);
  }

  function pdfLib() {
    if (!pdfReady) {
      var names = Object.keys(PDF_FONTS);
      pdfReady = Promise.all([loadScript(PDFMAKE)].concat(names.map(function (n) {
        return fetch(PDF_FONTS[n]).then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.arrayBuffer();
        });
      }))).then(function (res) {
        var vfs = {};
        names.forEach(function (n, i) { vfs[n] = toBase64(res[i + 1]); });
        window.pdfMake.vfs = vfs;
        window.pdfMake.fonts = { SG: { normal: "sg-regular.ttf", bold: "sg-semibold.ttf",
                                       italics: "sg-regular.ttf", bolditalics: "sg-semibold.ttf" } };
        return window.pdfMake;
      });
      pdfReady.catch(function () { pdfReady = null; });
    }
    return pdfReady;
  }

  function briefPdf(form) {
    var items = Array.prototype.map.call(form.querySelectorAll(".brief__field"), function (el) {
      var input = el.querySelector("input, textarea");
      return { q: el.querySelector(".brief__q").textContent.trim(),
               hint: (el.querySelector(".brief__hint") || {}).textContent || "",
               a: input.value.trim() };
    });
    var title = items[0].a || "Naujas projektas";
    var d = new Date();
    var date = d.getFullYear() + " m. " + MONTHS[d.getMonth()] + " " + d.getDate() + " d.";

    var body = [
      { text: "PROJEKTO APRAŠYMAS", fontSize: 8.5, bold: true, color: C.accent, characterSpacing: 1.6 },
      { text: title, fontSize: 24, bold: true, color: C.text, lineHeight: 1.1, margin: [0, 8, 0, 6] },
      { text: "Parengta " + date, fontSize: 9, color: C.muted },
      { canvas: [{ type: "line", x1: 0, y1: 0, x2: 483, y2: 0, lineWidth: 1, lineColor: C.line }],
        margin: [0, 18, 0, 6] }
    ];
    items.slice(1).forEach(function (it, i) {
      /* the name became the title, so the rest are numbered from 1 */
      body.push({ text: (i + 1) + ". " + it.q.replace(/^\d+\.\s*/, ""), fontSize: 12, bold: true, color: C.text, margin: [0, 16, 0, 2],
                  headlineLevel: 1 });
      body.push({ text: it.hint.trim(), fontSize: 8.5, color: C.muted, margin: [0, 0, 0, 6] });
      body.push(it.a
        ? { text: it.a, fontSize: 10.5, color: C.body, lineHeight: 1.35 }
        : { text: "Neužpildyta. Galima aptarti vėliau.", fontSize: 10, color: C.muted });
    });
    body.push({
      margin: [0, 28, 0, 0], unbreakable: true,
      table: { widths: ["*"], body: [[{
        fillColor: C.sand, margin: [16, 14, 16, 14], border: [false, false, false, false],
        stack: [
          { text: "Ką daryti toliau?", bold: true, fontSize: 11, color: C.text, margin: [0, 0, 0, 4] },
          { text: [
            "Parodykite šį aprašymą programuotojui arba atsiųskite jį mums ",
            { text: "info@codeart.lt", color: C.accent, link: "mailto:info@codeart.lt" },
            ". Per 24 val. atsiųsime darbų planą ir fiksuotą kainą."
          ], fontSize: 10, color: C.body, lineHeight: 1.35 }
        ]
      }]] },
      layout: "noBorders"
    });

    return pdfLib().then(function (pdfMake) {
      pdfMake.createPdf({
        info: { title: "Projekto aprašymas: " + title, author: "Codeart šablonas" },
        pageSize: "A4",
        pageMargins: [56, 72, 56, 64],
        defaultStyle: { font: "SG", fontSize: 10.5, color: C.body },
        header: { margin: [56, 30, 56, 0], columns: [
          { text: "Codeart", bold: true, fontSize: 11, color: C.accent },
          { text: "codeart.lt", fontSize: 9, color: C.muted, alignment: "right", margin: [0, 2, 0, 0] }
        ] },
        footer: function (page, count) {
          return { margin: [56, 24, 56, 0], columns: [
            { text: "Šablonas: codeart.lt/lt/straipsniai/uzduotis-programuotojui.html", fontSize: 7.5, color: C.muted },
            { text: page + " / " + count, fontSize: 7.5, color: C.muted, alignment: "right", width: 40 }
          ] };
        },
        /* never leave a question at the foot of a page without room for its answer */
        pageBreakBefore: function (node) {
          return node.headlineLevel === 1 && node.startPosition.top > 842 - 64 - 90;
        },
        content: body
      }).download(form.getAttribute("data-file"));
    });
  }

  /* Contact page: pick up a brief sent from the template above. */
  (function () {
    var session = store("sessionStorage");
    var brief = null;
    try { brief = session && session.getItem(BRIEF_KEY); } catch (e) { /* storage off */ }
    var box = brief && document.querySelector('form[data-contact] textarea[name="message"]');
    if (!box) return;
    if (!box.value.trim()) box.value = brief;
    try { session.removeItem(BRIEF_KEY); } catch (e) { /* storage off */ }
  })();

  /* ---------------------------------------------------------------- */
  /* Contact form – posts to Formspree, reports inline                */
  /* ---------------------------------------------------------------- */
  document.querySelectorAll("form[data-contact]").forEach(function (form) {
    var status = form.querySelector(".form__status");
    var button = form.querySelector('button[type="submit"]');
    var msg = {
      sending: form.getAttribute("data-msg-sending"),
      ok: form.getAttribute("data-msg-ok"),
      fail: form.getAttribute("data-msg-fail"),
      invalid: form.getAttribute("data-msg-invalid")
    };

    function say(text, isError) {
      status.textContent = text;
      status.classList.toggle("is-error", !!isError);
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        say(msg.invalid, true);
        var bad = form.querySelector(":invalid");
        if (bad) bad.focus();
        return;
      }

      button.disabled = true;
      say(msg.sending, false);

      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          form.reset();
          say(msg.ok, false);
        })
        .catch(function () {
          say(msg.fail, true);
        })
        .then(function () {
          button.disabled = false;
        });
    });
  });
})();
