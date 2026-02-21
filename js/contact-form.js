// ====== FORMOS (VISOS) – VALIDACIJA + Formspree submit + Success modal summary ======
document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form.contact-form");
  if (!forms.length) return;

  console.log("[contact-form] init forms:", forms.length);

  // --- modal helpers (global) ---
  const successModal = document.getElementById("contactSuccessModal");
  const successSummaryEl = document.getElementById("contactSuccessSummary");

  const closeModalEls = successModal
    ? successModal.querySelectorAll("[data-modal-close]")
    : [];

  const escapeHtml = (s) =>
    String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");

  const renderSuccessSummary = (payload) => {
    if (!successSummaryEl) return;

    if (!payload) {
      successSummaryEl.innerHTML = "";
      successSummaryEl.hidden = true;
      return;
    }

    const rows = [
      ["Vardas", payload.name],
      ["El. paštas", payload.email],
      ["Telefonas", payload.phone || "—"],
      ["Terminas", payload.timeline || "—"],
      ["Žinutė", payload.message],
    ].filter(([, v]) => String(v ?? "").trim().length);

    successSummaryEl.innerHTML = `
      <dl class="contact-summary">
        ${rows
          .map(
            ([k, v]) => `
          <div class="contact-summary__row">
            <dt>${escapeHtml(k)}</dt>
            <dd>${escapeHtml(v)}</dd>
          </div>`
          )
          .join("")}
      </dl>
    `;
    successSummaryEl.hidden = false;
  };

  const openSuccessModal = (payload) => {
    if (!successModal) {
      // fallback alert
      alert(
        `Ačiū! Žinutė išsiųsta.\n\nVardas: ${
          payload?.name || ""
        }\nEl. paštas: ${payload?.email || ""}\nTelefonas: ${
          payload?.phone || "—"
        }\nTerminas: ${payload?.timeline || "—"}\n\nŽinutė:\n${
          payload?.message || ""
        }`
      );
      return;
    }

    renderSuccessSummary(payload);

    successModal.classList.add("is-open");
    successModal.setAttribute("aria-hidden", "false");
  };

  const closeSuccessModal = () => {
    if (!successModal) return;

    successModal.classList.remove("is-open");
    successModal.setAttribute("aria-hidden", "true");
    renderSuccessSummary(null);
  };

  closeModalEls.forEach((el) =>
    el.addEventListener("click", closeSuccessModal)
  );

  if (successModal) {
    // click on backdrop closes
    successModal.addEventListener("click", (e) => {
      if (e.target.classList.contains("contact-modal__backdrop")) {
        closeSuccessModal();
      }
    });

    // Esc closes
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeSuccessModal();
    });
  }

  // === attach logic for each form separately ===
  forms.forEach((form) => {
    const submitBtn = form.querySelector('button[type="submit"]');
    const note = form.querySelector(".form-note");

    if (!submitBtn) return;

    const PHONE_PREFIX = "+370 ";
    const PHONE_MAX_DIGITS = 8;

    let showErrors = false;

    const clearFieldErrors = () => {
      form.querySelectorAll(".fi").forEach((wrapper) => {
        wrapper.classList.remove("error");
        const msg = wrapper.querySelector(".field-error");
        if (msg) msg.textContent = "";
      });
    };

    const setFieldError = (field, message) => {
      if (!showErrors || !field) return;

      const wrapper = field.closest(".fi");
      if (!wrapper) return;

      wrapper.classList.add("error");
      let msg = wrapper.querySelector(".field-error");
      if (!msg) {
        msg = document.createElement("p");
        msg.className = "field-error";
        wrapper.appendChild(msg);
      }
      msg.textContent = message;
    };

    const setNote = (text, kind) => {
      if (!note) return;

      if (!showErrors) {
        note.textContent = "";
        note.className = "form-note";
        return;
      }

      note.textContent = text || "";
      note.className = "form-note";
      if (kind) note.classList.add(kind);
    };

    // --- phone field (only if exists) ---
    const initPhoneField = () => {
      const phoneField = form.elements["phone"];
      if (!phoneField) return;

      // ensure prefix
      if (!phoneField.value) phoneField.value = PHONE_PREFIX;

      phoneField.setAttribute("inputmode", "numeric");
      phoneField.setAttribute("autocomplete", "tel");

      // IMPORTANT: avoid adding listeners multiple times
      if (phoneField.dataset.bound === "1") return;
      phoneField.dataset.bound = "1";

      phoneField.addEventListener("keydown", (e) => {
        const pos = phoneField.selectionStart ?? 0;
        const end = phoneField.selectionEnd ?? 0;

        if (
          (e.key === "Backspace" && pos <= PHONE_PREFIX.length) ||
          (e.key === "Delete" &&
            pos < PHONE_PREFIX.length &&
            end <= PHONE_PREFIX.length)
        ) {
          e.preventDefault();
        }
      });

      phoneField.addEventListener("input", () => {
        let val = phoneField.value || "";

        // rebuild with prefix
        const digits = val.replace(/[^\d]/g, "");
        let rest = digits;

        // if user pasted +370XXXXXXXX or 370XXXXXXXX -> normalize to last 8 digits
        if (rest.startsWith("370")) rest = rest.slice(3);
        rest = rest.slice(0, PHONE_MAX_DIGITS);

        phoneField.value = PHONE_PREFIX + rest;
      });
    };

    initPhoneField();

    // --- timeline (custom select -> hidden input name="timeline") ---
    const timelineHidden = form.querySelector(
      'input[type="hidden"][name="timeline"]'
    );

    // validate for THIS form
    const validate = () => {
      clearFieldErrors();

      const nameField = form.elements["name"];
      const emailField = form.elements["email"];
      const phoneField = form.elements["phone"]; // may be undefined
      const messageField = form.elements["message"];

      const name = (nameField?.value || "").trim();
      const email = (emailField?.value || "").trim();
      const message = (messageField?.value || "").trim();

      let ok = true;

      // name
      if (!name) {
        setFieldError(nameField, "Įveskite savo vardą.");
        ok = false;
      } else if (name.length < 2) {
        setFieldError(
          nameField,
          "Vardas per trumpas (mažiausiai 2 simboliai)."
        );
        ok = false;
      } else if (/\d/.test(name)) {
        setFieldError(nameField, "Varde neturėtų būti skaičių.");
        ok = false;
      }

      // email
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email) {
        setFieldError(emailField, "Įveskite el. pašto adresą.");
        ok = false;
      } else if (!emailPattern.test(email)) {
        setFieldError(
          emailField,
          "Įveskite teisingą el. paštą (pvz., vardas@pavyzdys.lt)."
        );
        ok = false;
      }

      // phone (only for the form that has it)
      if (phoneField) {
        const phoneRaw = phoneField.value || "";
        const hasPrefix = phoneRaw.startsWith(PHONE_PREFIX);

        const rest = hasPrefix ? phoneRaw.slice(PHONE_PREFIX.length) : phoneRaw;
        const digitsOnly = rest.replace(/[^\d]/g, "");

        if (!rest.trim()) {
          setFieldError(phoneField, "Įveskite telefono numerį.");
          ok = false;
        } else if (!hasPrefix) {
          setFieldError(phoneField, "Telefono numeris turi prasidėti +370.");
          ok = false;
        } else if (digitsOnly.length < PHONE_MAX_DIGITS) {
          setFieldError(
            phoneField,
            `Telefono numeris per trumpas – po +370 turi būti bent ${PHONE_MAX_DIGITS} skaitmenys.`
          );
          ok = false;
        }
      }

      // timeline (only where it exists)
      if (timelineHidden) {
        const value = (timelineHidden.value || "").trim();
        if (!value) {
          setFieldError(timelineHidden, "Pasirinkite terminą.");
          ok = false;
        }
      }

      // message
      if (!message) {
        setFieldError(messageField, "Įveskite žinutę.");
        ok = false;
      } else if (message.length < 20) {
        setFieldError(
          messageField,
          "Žinutė turėtų būti bent 20 simbolių, kad galėčiau geriau suprasti poreikį."
        );
        ok = false;
      }

      if (!ok) setNote("Patikrinkite pažymėtus laukus.", "err");
      else setNote("", "");

      return ok;
    };

    // enable submit
    submitBtn.disabled = false;

    // live validation after first submit attempt
    form.addEventListener("input", () => {
      if (!showErrors) return;
      validate();
    });

    // revalidate on timeline hidden change
    if (timelineHidden) {
      timelineHidden.addEventListener("change", () => {
        if (!showErrors) return;
        validate();
      });
    }

    // SUBMIT HANDLER: on form submit (works with Enter too)
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      console.log("[contact-form] submit", form);

      showErrors = true;

      const ok = validate();
      if (!ok) return;

      // collect payload BEFORE reset
      const payload = {
        name: (form.elements["name"]?.value || "").trim(),
        email: (form.elements["email"]?.value || "").trim(),
        phone: (form.elements["phone"]?.value || "").trim(),
        timeline: (form.elements["timeline"]?.value || "").trim(),
        message: (form.elements["message"]?.value || "").trim(),
      };

      const originalText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = "Siunčiama…";

      try {
        const res = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: { Accept: "application/json" },
        });

        if (res.ok) {
          form.reset();
          clearFieldErrors();
          initPhoneField();
          showErrors = false;

          setNote("", "");
          openSuccessModal(payload);
        } else {
          setNote("Nepavyko išsiųsti. Bandykite dar kartą.", "err");
        }
      } catch (err) {
        console.error(err);
        setNote(
          "Tinklo klaida. Patikrinkite internetą ir bandykite dar kartą.",
          "err"
        );
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
      }
    });
  });
});
