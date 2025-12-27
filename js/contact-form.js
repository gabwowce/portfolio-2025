// ====== KONTAKTŲ FORMA – VALIDACIJA (paprasta versija) ======
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".contact-form");
  if (!form) return;

  console.log("[contact-form] init");

  const submitBtn = form.querySelector('button[type="submit"]');
  const note = form.querySelector(".form-note");
  const PHONE_PREFIX = "+370 ";
  const PHONE_MAX_DIGITS = 8;

  let showErrors = false; // iki pirmo paspaudimo klaidų nerodom

  // --- helperiai klaidoms ---
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

  // --- tel. lauko logika: +370 + max 8 skaitmenys ---
  const initPhoneField = () => {
    const phoneField = form.elements["phone"];
    if (!phoneField) return;

    if (!phoneField.value) phoneField.value = PHONE_PREFIX;

    phoneField.setAttribute("inputmode", "numeric");
    phoneField.setAttribute("autocomplete", "tel");

    phoneField.addEventListener("keydown", (e) => {
      const pos = phoneField.selectionStart ?? 0;
      if (
        (e.key === "Backspace" && pos <= PHONE_PREFIX.length) ||
        (e.key === "Delete" &&
          pos < PHONE_PREFIX.length &&
          phoneField.selectionEnd <= PHONE_PREFIX.length)
      ) {
        e.preventDefault();
      }
    });

    phoneField.addEventListener("input", () => {
      let val = phoneField.value;
      if (!val.startsWith(PHONE_PREFIX)) {
        const rest = val.replace(/[^\d]/g, "").slice(0, PHONE_MAX_DIGITS);
        val = PHONE_PREFIX + rest;
      } else {
        const rest = val
          .slice(PHONE_PREFIX.length)
          .replace(/[^\d]/g, "")
          .slice(0, PHONE_MAX_DIGITS);
        val = PHONE_PREFIX + rest;
      }
      phoneField.value = val;
    });
  };

  initPhoneField();

  // --- VALIDACIJA ---
  const validate = () => {
    clearFieldErrors();

    const nameField = form.elements["name"];
    const emailField = form.elements["email"];
    const phoneField = form.elements["phone"];
    const messageField = form.elements["message"];

    const name = (nameField?.value || "").trim();
    const email = (emailField?.value || "").trim();
    const phoneRaw = phoneField?.value || "";
    const message = (messageField?.value || "").trim();

    let phoneRest = phoneRaw.startsWith(PHONE_PREFIX)
      ? phoneRaw.slice(PHONE_PREFIX.length)
      : phoneRaw;
    phoneRest = phoneRest.trim();
    const digitsOnly = phoneRest.replace(/[^\d]/g, "");

    let ok = true;

    // vardas
    if (!name) {
      setFieldError(nameField, "Įveskite savo vardą.");
      ok = false;
    } else if (name.length < 2) {
      setFieldError(nameField, "Vardas per trumpas (mažiausiai 2 simboliai).");
      ok = false;
    } else if (/\d/.test(name)) {
      setFieldError(nameField, "Varde neturėtų būti skaičių.");
      ok = false;
    }

    // el. paštas
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

    // tel.
    if (!phoneRest) {
      setFieldError(phoneField, "Įveskite telefono numerį.");
      ok = false;
    } else if (!phoneRaw.startsWith(PHONE_PREFIX)) {
      setFieldError(phoneField, "Telefono numeris turi prasidėti +370.");
      ok = false;
    } else if (digitsOnly.length < PHONE_MAX_DIGITS) {
      setFieldError(
        phoneField,
        `Telefono numeris per trumpas – po +370 turi būti bent ${PHONE_MAX_DIGITS} skaitmenys.`
      );
      ok = false;
    }

    // žinutė
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

  // mygtukas aktyvus – bet tikrina viską click metu
  if (submitBtn) submitBtn.disabled = false;

  // live: kai jau paspaudėm kartą – klaidos dingsta vos pataisius lauką
  form.addEventListener("input", () => {
    if (!showErrors) return;
    validate();
  });

  // *** ČIA pagrindinis handleris – būtent ant mygtuko ***
  // --- modal helpers ---
  const successModal = document.getElementById("contactSuccessModal");
  const closeModalEls = successModal
    ? successModal.querySelectorAll("[data-modal-close]")
    : [];

  const openSuccessModal = () => {
    if (!successModal) {
      // fallback, jei nėra HTML modalo
      alert("Ačiū! Jūsų žinutė išsiųsta.");
      return;
    }
    successModal.classList.add("is-open");
    successModal.setAttribute("aria-hidden", "false");
  };

  const closeSuccessModal = () => {
    if (!successModal) return;
    successModal.classList.remove("is-open");
    successModal.setAttribute("aria-hidden", "true");
  };

  closeModalEls.forEach((el) => {
    el.addEventListener("click", () => {
      closeSuccessModal();
    });
  });

  if (successModal) {
    successModal.addEventListener("click", (e) => {
      if (e.target.classList.contains("contact-modal__backdrop")) {
        closeSuccessModal();
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeSuccessModal();
    });
  }

  // *** Pagrindinis Siųsti mygtuko handleris ***
  submitBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    console.log("[contact-form] submit button clicked");

    showErrors = true;

    const ok = validate();
    if (!ok) {
      // klaidos parodytos, nesiunčiam
      return;
    }

    // mygtukas – „Siunčiama…“
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = "Siunčiama…";

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: {
          Accept: "application/json", // kad Formspree NEredirectintų
        },
      });

      if (res.ok) {
        // formą nuvalom
        form.reset();
        clearFieldErrors();
        initPhoneField();
        showErrors = false;

        setNote("", "");
        openSuccessModal();
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
