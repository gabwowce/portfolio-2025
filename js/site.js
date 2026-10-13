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
      if (window.innerWidth >= 760) close(false);
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
  /* Sliding underline under the current section's nav link           */
  /* ---------------------------------------------------------------- */
  (function () {
    var bar = document.querySelector(".site-nav__indicator");
    if (!bar) return;
    var links = Array.prototype.slice.call(
      document.querySelectorAll(".site-nav__links a[data-nav]")
    );
    var sections = links
      .map(function (a) {
        return document.getElementById(a.getAttribute("data-nav"));
      })
      .filter(Boolean);
    var raf = null;

    function update() {
      raf = null;
      var active = null;
      sections.forEach(function (s) {
        if (s.getBoundingClientRect().top <= 120) active = s.id;
      });
      /* Past the last section (contact), nothing in the nav is current. */
      var contact = document.getElementById("kontaktai") ||
        document.getElementById("contact");
      if (contact && contact.getBoundingClientRect().top <= 120) active = null;

      var link = active
        ? document.querySelector('.site-nav__links a[data-nav="' + active + '"]')
        : null;
      if (link) {
        bar.style.width = link.offsetWidth + "px";
        bar.style.transform = "translateX(" + link.offsetLeft + "px)";
        bar.style.opacity = "1";
        links.forEach(function (a) {
          if (a === link) a.setAttribute("aria-current", "true");
          else a.removeAttribute("aria-current");
        });
      } else {
        bar.style.opacity = "0";
        links.forEach(function (a) {
          a.removeAttribute("aria-current");
        });
      }
    }

    function schedule() {
      if (!raf) raf = requestAnimationFrame(update);
    }

    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    update();
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
  /* Contact form – posts to Formspree, reports inline                */
  /* ---------------------------------------------------------------- */
  (function () {
    var form = document.querySelector("form[data-contact]");
    if (!form) return;
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
  })();
})();
