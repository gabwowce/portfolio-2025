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
  Live guardrails tester. This is a JS port of the real .claude/guard.sh
  checks shipped on this page — not a simplified imitation. Each function
  mirrors that script's bash `case` patterns exactly (glob *"x"* ==
  "contains x"; a pattern with no trailing * means "ends with"), and was
  cross-checked against the actual guard.sh output for the same inputs
  before shipping (including the ordered dd if=/of= case, where argument
  order matters). If guard.sh ever changes, this must change with it.
*/
function checkDestructiveFs(command) {
  if (
    command.includes("rm -rf /") ||
    command.includes("rm -rf ~") ||
    command.includes("rm -rf $HOME") ||
    command.includes("rm -rf .")
  ) {
    return "destructive rm -rf targeting root, home, or the current directory.";
  }
  if (
    command.includes("dd if=") &&
    command.includes("of=/dev/") &&
    command.indexOf("of=/dev/") > command.indexOf("dd if=")
  ) {
    return "raw disk write via dd — this can destroy a whole disk.";
  }
  if (command.includes(":(){ :|:& };:")) {
    return "fork bomb pattern detected.";
  }
  return null;
}

function checkProtectedBranch(command) {
  const forcePush =
    (command.includes("push") && command.includes("--force")) ||
    command.includes("push -f");
  if (forcePush && /(^|\s)(main|master)(\s|$)/.test(command)) {
    return "force-push to main/master.";
  }
  if (
    command.includes("filter-branch") ||
    (command.includes("push") &&
      command.includes("--force") &&
      command.includes("--all"))
  ) {
    return "history-rewriting operation (filter-branch / force-push --all).";
  }
  return null;
}

function checkSkipSafety(command) {
  if (command.includes("--no-verify") || command.includes("--no-gpg-sign")) {
    return "a flag that skips commit hooks or signature verification.";
  }
  if (command.includes("chmod 777") || command.includes("chmod -R 777")) {
    return "chmod 777 — overly permissive file permissions.";
  }
  if (
    command.includes("curl") &&
    (command.includes("| bash") || command.includes("|bash"))
  ) {
    return "piping a remote script straight into a shell — read it first.";
  }
  if (
    command.includes("wget") &&
    (command.includes("| sh") || command.includes("|sh"))
  ) {
    return "piping a remote script straight into a shell — read it first.";
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
        checkSkipSafety(command);
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
