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

  initGuardTester();
});

/*
  Live guardrails tester — a JS port of the real .claude/guard.sh shipped
  on this page, kept rule-for-rule in step with it (same flag-order
  handling, same "only look after push" rule, same secrets patterns).
  Both implementations are run against the same table of cases before
  shipping; tools/sync-guardrails.py keeps the page's code blocks
  generated from the script itself. If guard.sh changes, change this too.
*/
function checkDestructiveFs(command) {
  const c = " " + command + " ";

  if (/(^|[;&|(]|\s)rm(\s|$)/.test(c)) {
    const rec = /(\s-[a-zA-Z]*[rR][a-zA-Z]*(\s|$)|\s--recursive(\s|$))/.test(c);
    const force = /(\s-[a-zA-Z]*f[a-zA-Z]*(\s|$)|\s--force(\s|$))/.test(c);
    const target = /(\s\/(\s|$)|\s\/\*|\s~|\$HOME|\s\.\/?(\s|$)|\s\.\.\/?(\s|$)|--no-preserve-root)/.test(c);
    if (rec && force && target) {
      return "recursive force-delete aimed at root, home, or the working directory.";
    }
  }
  if (/dd\s.*of=\/dev\//.test(c)) {
    return "raw disk write via dd — this can destroy a whole disk.";
  }
  if (command.includes(":(){ :|:& };:")) {
    return "fork bomb pattern detected.";
  }
  return null;
}

function checkProtectedBranch(command) {
  if (command.includes("filter-branch")) {
    return "history-rewriting operation (filter-branch).";
  }

  // Only what comes after "push", so `cd main && git push origin dev`
  // isn't mistaken for a push to main.
  const m = /[Pp]ush([\s\S]*)$/.exec(command);
  if (!m) return null;
  const afterPush = m[1];

  if (/(^|\s)\+[^\s]*(main|master)(\s|:|$)/.test(afterPush)) {
    return "force-push to main/master via a + refspec.";
  }

  const forced = /(\s-f(\s|$)|--force(\s|$)|--force-with-lease)/.test(afterPush);
  if (!forced) return null;

  if (/(^|\s|:)(main|master)(\s|:|$)/.test(afterPush)) {
    return "force-push to main/master.";
  }
  if (/\s--all(\s|$)/.test(afterPush)) {
    return "force-push --all rewrites every branch, main/master included.";
  }
  return null;
}

function checkSkipSafety(command) {
  if (command.includes("--no-verify") || command.includes("--no-gpg-sign")) {
    return "a flag that skips commit hooks or signature verification.";
  }
  if (/chmod\s+(-[a-zA-Z]+\s+)*777/.test(command)) {
    return "chmod 777 — overly permissive file permissions.";
  }
  if (/(curl|wget)[^|]*\|\s*(sudo\s+)*(ba|z|k|da|c)?sh(\s|$)/.test(command)) {
    return "piping a remote script straight into a shell — read it first.";
  }
  return null;
}

function checkSecretWriteViaBash(command) {
  if (/(>>?|tee\s+(-a\s+)*)\s*[^\s]*(\.env|id_rsa|id_ed25519|\.aws\/credentials|credentials\.json|\.ssh\/)/.test(command)) {
    return "writing to a secrets file from the shell. Edit it by hand instead.";
  }
  return null;
}

function checkSensitiveWrite(filePath) {
  const contains = [
    ".env",
    "id_rsa",
    "id_ed25519",
    ".aws/credentials",
    ".ssh/",
    "credentials.json",
  ];
  for (const s of contains) {
    if (filePath.includes(s)) {
      return `write to a sensitive/credentials path (${filePath}). Edit it by hand instead.`;
    }
  }
  if (filePath.endsWith(".git/config")) {
    return `write to a sensitive/credentials path (${filePath}). Edit it by hand instead.`;
  }
  return null;
}

function initGuardTester() {
  const cmdInput = document.getElementById("testerCmd");
  const pathInput = document.getElementById("testerPath");
  const runBtn = document.getElementById("testerRun");
  const result = document.getElementById("testerResult");
  if (!cmdInput || !pathInput || !runBtn || !result) return;

  const okIcon =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>';
  const blockIcon =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="m15 9-6 6M9 9l6 6"/></svg>';
  const emptyIcon =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>';

  function render(state, message) {
    result.hidden = false;
    result.className = "hook-tester__result hook-tester__result--" + state;
    const icon = state === "block" ? blockIcon : state === "ok" ? okIcon : emptyIcon;
    result.innerHTML = icon + "<span>" + message + "</span>";
    if (state === "block") {
      // restart the shake animation on repeated blocks
      void result.offsetWidth;
      result.classList.add("hook-tester__result--shake");
    }
  }

  function run() {
    const command = cmdInput.value.trim();
    const filePath = pathInput.value.trim();

    if (!command && !filePath) {
      render("empty", "Type a command or a file path above, then check it.");
      return;
    }

    if (command) {
      const reason =
        checkDestructiveFs(command) ||
        checkProtectedBranch(command) ||
        checkSkipSafety(command) ||
        checkSecretWriteViaBash(command);
      if (reason) {
        render("block", "Blocked — " + reason);
        return;
      }
    }

    if (filePath) {
      const reason = checkSensitiveWrite(filePath);
      if (reason) {
        render("block", "Blocked — " + reason);
        return;
      }
    }

    render("ok", "Allowed — none of the five checks match this.");
  }

  runBtn.addEventListener("click", run);
  [cmdInput, pathInput].forEach((input) => {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") run();
    });
  });

  document.querySelectorAll(".hook-tester__chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const target = chip.dataset.target === "path" ? pathInput : cmdInput;
      const other = target === pathInput ? cmdInput : pathInput;
      target.value = chip.dataset.value;
      other.value = "";
      run();
      target.focus();
    });
  });
}
