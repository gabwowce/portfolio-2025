\
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, HRFlowable, Table, TableStyle
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# DejaVu covers Lithuanian diacritics (ė, ū, š, ž, ...) which the base14
# Helvetica/Courier fonts do not — those rendered as tofu boxes.
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSansMono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))

INK = colors.HexColor("#171717")
MUTED = colors.HexColor("#5c5850")
ACCENT = colors.HexColor("#d97757")
CODE_BG = colors.HexColor("#171717")
CODE_FG = colors.HexColor("#f2f0e9")

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleX", parent=styles["Title"], fontName="DejaVuSans-Bold",
    fontSize=26, leading=30, textColor=INK, spaceAfter=4,
)
subtitle_style = ParagraphStyle(
    "SubtitleX", parent=styles["Normal"], fontName="DejaVuSans",
    fontSize=13, leading=17, textColor=MUTED, spaceAfter=4,
)
byline_style = ParagraphStyle(
    "BylineX", parent=styles["Normal"], fontName="DejaVuSans",
    fontSize=10, leading=14, textColor=ACCENT, spaceAfter=18,
)
h2 = ParagraphStyle(
    "H2X", parent=styles["Heading2"], fontName="DejaVuSans-Bold",
    fontSize=15, leading=19, textColor=INK, spaceBefore=18, spaceAfter=8,
)
h3 = ParagraphStyle(
    "H3X", parent=styles["Heading3"], fontName="DejaVuSans-Bold",
    fontSize=12, leading=16, textColor=ACCENT, spaceBefore=12, spaceAfter=4,
)
body = ParagraphStyle(
    "BodyX", parent=styles["Normal"], fontName="DejaVuSans",
    fontSize=10.3, leading=15, textColor=INK, spaceAfter=8, alignment=TA_LEFT,
)
body_muted = ParagraphStyle(
    "BodyMutedX", parent=body, textColor=MUTED,
)
bullet_style = ParagraphStyle(
    "BulletX", parent=body, leftIndent=14, spaceAfter=4,
)
code_style = ParagraphStyle(
    "CodeX", fontName="DejaVuSansMono", fontSize=7.6, leading=10.5,
    textColor=CODE_FG,
)
footer_style = ParagraphStyle(
    "FooterX", parent=body_muted, fontSize=9, alignment=TA_LEFT,
)

def code_block(text):
    # Preformatted doesn't reliably paint its own background, so the dark
    # panel is a single-cell Table wrapping the code instead.
    pre = Preformatted(text, code_style, maxLineLength=100)
    t = Table([[pre]], colWidths=[6.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t

def bullets(items, ordered=False):
    out = []
    for i, item in enumerate(items, start=1):
        prefix = f"{i}." if ordered else "•"
        out.append(Paragraph(f"{prefix}&nbsp;&nbsp;{item}", bullet_style))
    return out

story = []

story.append(Paragraph("Claude Code Guardrails", title_style))
story.append(Paragraph("Five safety checks for Claude Code, explained", subtitle_style))
story.append(Paragraph("by Gabrielė · Codeart (codeart.lt)", byline_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#ddd7c8"), spaceAfter=14))

story.append(Paragraph("The problem", h2))
story.append(Paragraph(
    "An agent that can run arbitrary shell commands will, sooner or later, try to run one "
    "you did not mean to approve. Guardrails catch that before it executes &mdash; not after.",
    body))

story.append(Paragraph("What&rsquo;s inside", h2))
items = [
    "A .claude/settings.json wiring up three hook registrations",
    "A guard.sh script implementing five distinct safety checks",
    "This guide",
    "Drop-in setup &mdash; one dependency (jq), no build step",
    "An honest list of what it does NOT protect against",
]
story.extend(bullets(items))
story.append(Spacer(1, 6))

story.append(Paragraph("How it&rsquo;s wired", h2))
story.append(Paragraph(
    "Claude Code hooks are shell commands the CLI runs before or after a tool call, fed a "
    "JSON payload on stdin. guard.sh reads that payload once and runs five checks against it. "
    "A PreToolUse hook can block the call outright (exit code 2); a PostToolUse hook can only "
    "observe, so it&rsquo;s used here for the audit log.",
    body))

import pathlib as _pl
_SRC = _pl.Path("/home/user/portfolio-2025/docs/resources/claude-code-guardrails")
settings_json = _SRC.joinpath("settings.json").read_text().rstrip("\n")
_UNUSED_settings = '''{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/guard.sh" }
        ]
      },
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/guard.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/guard.sh" }
        ]
      }
    ]
  }
}'''
story.append(Spacer(1, 4))
story.append(Paragraph(".claude/settings.json", ParagraphStyle("label", parent=body_muted, fontName="Courier", fontSize=8.5, spaceAfter=3)))
story.append(code_block(settings_json))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Three hook registrations, five checks &mdash; guard.sh looks at hook_event_name and "
    "tool_name to decide which checks apply to this call.",
    body_muted))

checks = [
    ("1 &middot; Destructive filesystem commands",
     "Blocks rm -rf aimed at /, ~, or the current directory, raw disk writes via dd, and "
     "fork-bomb patterns. These are the commands where there is no undo."),
    ("2 &middot; Force-push and history rewrites on protected branches",
     "Blocks git push --force (or -f) specifically when the target is main or master, plus "
     "filter-branch and force-pushing --all. Force-pushing a feature branch you own is still "
     "allowed &mdash; the check only fires on shared history."),
    ("3 &middot; Skipping safety checks",
     "Blocks --no-verify and --no-gpg-sign (both exist to skip a check someone deliberately "
     "set up), chmod 777, and piping a remote script straight into a shell (curl ... | bash, "
     "wget ... | sh) &mdash; read a script before it runs, always."),
    ("4 &middot; Writes to sensitive files",
     "Blocks Write/Edit/MultiEdit targeting .env, SSH keys, .aws/credentials, "
     "credentials.json, or .git/config. If a credential needs to change, do it by hand &mdash; "
     "an agent shouldn&rsquo;t be the one touching it."),
    ("5 &middot; Audit log",
     "Every tool call gets one timestamped line in .claude/guard.log, labelled RAN or "
     "BLOCKED. The catch: a PreToolUse hook that exits 2 stops the tool, so PostToolUse "
     "never fires &mdash; a naive setup logs only what succeeded and silently loses every "
     "blocked command, the very set you want a record of. That is why block() writes its "
     "own log line before exiting."),
]
for heading, text in checks:
    story.append(Paragraph(heading, h3))
    story.append(Paragraph(text, body))

story.append(Spacer(1, 6))
story.append(Paragraph("The full guard.sh script", h2))

_guard = _SRC.joinpath("guard.sh").read_text().rstrip("\n")
# Split at each check boundary so no single dark block is taller than a page
# (reportlab can't break a one-cell Table across pages).
_markers = ["# --- 1: destructive", "# --- 2: force-push", "# --- 3: skipping",
            "# --- 4: secrets", "# --- dispatch"]
_idx = [0] + [_guard.index(m) for m in _markers] + [len(_guard)]
_guard_parts = [_guard[_idx[i]:_idx[i + 1]].rstrip() for i in range(len(_idx) - 1)]

story.append(Paragraph(".claude/guard.sh", ParagraphStyle("label2", parent=body_muted, fontName="Courier", fontSize=8.5, spaceAfter=3)))
for _pi, _part in enumerate(_guard_parts):
    if _pi:
        story.append(Spacer(1, 6))
    story.append(code_block(_part))

story.append(Paragraph("What this does not protect against", h2))
story.append(Paragraph(
    "This is a guardrail against mistakes, not a security boundary. It is pattern "
    "matching on a command string, and pattern matching can always be walked around:",
    body))
story.extend(bullets([
    "Deliberate evasion &mdash; base64 into a shell, writing a script and running it, aliases.",
    "Prompt injection &mdash; caught only if the resulting command happens to match a pattern.",
    "Files pulled in with @ &mdash; no tool call, so PreToolUse never runs. Use a Read deny rule.",
    "Everything not on the list &mdash; no sudo rule, no network rule. Five checks, that is it.",
    "Non-bash environments &mdash; needs WSL or Git Bash on Windows, and jq installed.",
]))
story.append(Spacer(1, 6))

story.append(Paragraph("Setup", h2))
setup_items = [
    "Create a .claude folder in your project root if it doesn&rsquo;t exist.",
    "Save the settings.json above as .claude/settings.json.",
    "Save the guard.sh script above as .claude/guard.sh.",
    "Make it executable: chmod +x .claude/guard.sh",
    "Make sure jq is installed (brew install jq / apt install jq).",
    "Restart Claude Code so it picks up the new settings.",
]
story.extend(bullets(setup_items, ordered=True))

story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#ddd7c8"), spaceAfter=10))
story.append(Paragraph(
    "Free resource by Gabrielė · Codeart &mdash; more at codeart.lt/en/resources. "
    "Questions, or found an edge case these checks miss? Reach out via the socials linked on the site.",
    footer_style))

doc = SimpleDocTemplate(
    "/home/user/portfolio-2025/docs/resources/claude-code-guardrails.pdf",
    pagesize=LETTER,
    leftMargin=0.85*inch, rightMargin=0.85*inch,
    topMargin=0.8*inch, bottomMargin=0.8*inch,
    title="Claude Code Guardrails",
    author="Gabrielė · Codeart",
)
doc.build(story)
print("PDF built.")
