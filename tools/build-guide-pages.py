#!/usr/bin/env python3
"""
Build the written guide pages for the Claude Code track.

Each page is a real, standalone, indexable article AND gets lifted into a
lesson panel by build-resources.py. Rather than hand-copying the header,
footer and <head> into every file, this takes the finished hooks page as a
shell and swaps the metadata and the <main> body. So the chrome can only
ever be in one state across all of them.

Facts here are taken from the official Claude Code docs, not from memory:
  quickstart · memory (CLAUDE.md) · slash-commands/skills · mcp

Run:  python3 tools/build-guide-pages.py
Then: python3 tools/build-resources.py   (wires them into the track)
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / "en" / "resources" / "claude-code-hooks.html"

VERIFIED = "Verified against the official Claude Code documentation, September 2026."


def e(s):
    return html.escape(s, quote=False)


# --------------------------------------------------------------------------
# Small builders, so the bodies below stay readable
# --------------------------------------------------------------------------

def sec(title, *blocks, wide=False):
    cls = "resource-section resource-section--wide" if wide else "resource-section"
    inner = "\n".join(blocks)
    return (f'        <section class="{cls} u-reveal">\n'
            f'            <h2>{title}</h2>\n{inner}\n'
            f'        </section>\n')


def p(text):
    return f'            <p>{text}</p>'


def muted(text):
    return f'            <p class="muted">{text}</p>'


def ul(*items):
    lis = "\n".join(f'                <li>{i}</li>' for i in items)
    return f'            <ul>\n{lis}\n            </ul>'


def code(label, body):
    return ('            <div class="code-block">\n'
            f'                <span class="code-block__label">{label}</span>\n'
            '                <button class="code-block__copy" data-copy>Copy</button>\n'
            f'<pre><code>{e(body)}</code></pre>\n'
            '            </div>')


def callout(*paras):
    inner = "\n".join(f'                <p>{x}</p>' for x in paras)
    return f'            <div class="callout">\n{inner}\n            </div>'


def cats(*triples):
    cards = "\n".join(
        '                <div class="cat">\n'
        f'                    <b>{t}</b>\n'
        f'                    <p>{d}</p>\n'
        f'                    <span>{s}</span>\n'
        '                </div>' for t, d, s in triples)
    return f'            <div class="cat-grid">\n{cards}\n            </div>'


def flow(*steps):
    """steps: (kind, label, text) where kind is '', 'hook' or 'deny'."""
    out = []
    for i, (kind, label, text) in enumerate(steps):
        if i:
            out.append('                <div class="flowline__arrow" aria-hidden="true">&#8594;</div>')
        k = f" flowline__step--{kind}" if kind else ""
        out.append(f'                <div class="flowline__step{k}">\n'
                   f'                    <b>{label}</b>\n'
                   f'                    <span>{text}</span>\n'
                   '                </div>')
    return '            <div class="flowline">\n' + "\n".join(out) + '\n            </div>'


def table(headers, rows):
    head = "".join(f'<th>{h}</th>' for h in headers)
    body = "\n".join(
        '                        <tr>' + "".join(f'<td>{c}</td>' for c in r) + '</tr>'
        for r in rows)
    return ('            <div class="evt-wrap">\n'
            '                <table class="evt">\n'
            f'                    <thead>\n                        <tr>{head}</tr>\n                    </thead>\n'
            f'                    <tbody>\n{body}\n                    </tbody>\n'
            '                </table>\n'
            '            </div>')


def verified(extra=""):
    link = ('<a href="https://code.claude.com/docs/en/overview" target="_blank" '
            'rel="noopener">official documentation</a>')
    return (f'            <p class="verified">{VERIFIED} Claude Code moves quickly, '
            f'so check the {link} before relying on a detail here.{extra}</p>')


def whats_next(*cards):
    inner = "\n".join(
        f'                <a class="card resource-card" href="{href}">\n'
        f'                    <span class="resource-card__type">{kind}</span>\n'
        f'                    <h3 class="resource-card__title" style="margin-top:8px">{title}</h3>\n'
        f'                </a>' for kind, title, href in cards)
    return ('        <section class="resource-section u-reveal">\n'
            '            <h2>What\'s next</h2>\n'
            f'            <div class="resource-next">\n{inner}\n            </div>\n'
            '        </section>\n')


# --------------------------------------------------------------------------
# 1 · What Claude Code is, and getting it running
# --------------------------------------------------------------------------

INTRO = dict(
    slug="claude-code-intro",
    kind="Guide · Getting started",
    h1="Claude Code, from zero",
    lead="An agent in your terminal, not a chat in your browser. It reads your files, runs commands and edits code itself &mdash; so the first thing worth understanding is what it can reach.",
    title="Claude Code for beginners – install, first session, permissions",
    desc="What Claude Code actually is, how to install it, how the first session works, and what an agent with access to your terminal can and cannot reach. Free, read on the page.",
    body="\n".join([
        sec("The difference that matters",
            flow(("", "Browser chat", "you paste code in, it answers, you paste the answer back"),
                 ("hook", "Claude Code", "it opens the files itself, runs the tests, and edits the code in place")),
            p("A chat assistant is a very good autocomplete that cannot see your project. Claude Code is the same model wired into your machine: it can list a directory, read a file, run <code>npm test</code>, and write changes to disk."),
            p("That is the whole appeal, and also the whole risk. Everything else in this guide is about the second half of that sentence."),
            ),
        sec("01 · Install it",
            p("Pick one. The native installer keeps itself up to date in the background; the package managers do not."),
            code("macOS, Linux, WSL", "curl -fsSL https://claude.ai/install.sh | bash"),
            code("Windows PowerShell", "irm https://claude.ai/install.ps1 | iex"),
            p("Or through a package manager, if you would rather:"),
            code("Homebrew / WinGet", "brew install --cask claude-code\n\nwinget install Anthropic.ClaudeCode"),
            p("Check it landed:"),
            code("terminal", "claude --version"),
            muted("That prints a version number followed by <code>(Claude Code)</code>. Homebrew and WinGet installs do not auto-update &mdash; run <code>brew upgrade claude-code</code> or <code>winget upgrade Anthropic.ClaudeCode</code> yourself now and then."),
            ),
        sec("02 · Log in",
            p("Start it once and it walks you through authentication in the browser:"),
            code("terminal", "claude"),
            p("You can sign in with a Claude subscription (Pro, Max, Team or Enterprise), a Claude Console account with pre-paid credits, or an enterprise cloud provider. Credentials are stored, so this is a one-time step. To switch accounts later, type <code>/login</code> inside a running session."),
            ),
        sec("03 · Your first session",
            p("Claude Code works inside a directory. Go to a project and start it there &mdash; that directory is what it can see."),
            code("terminal", "cd /path/to/your/project\nclaude"),
            p("Do not start by asking it to build something. Start by asking it to explain something, because that tells you how much it actually understands:"),
            code("in the session", "what does this project do?\nwhere is the main entry point?\nexplain the folder structure"),
            muted("You do not have to paste files in or add them to context by hand. It reads what it needs as it goes."),
            ),
        sec("04 · Your first change",
            p("Now give it something to do:"),
            code("in the session", "add a hello world function to the main file"),
            p("It finds the file, shows you the change, and depending on the permission mode either asks first or just does it."),
            callout("<strong>Permission modes decide how often you are asked.</strong>",
                    "On Pro, Max and Team plans, interactive sessions start in <strong>Auto</strong> mode: a classifier reviews actions instead of you, and most edits and commands run without a prompt. On other plans they start in <strong>Manual</strong> mode, where you approve things yourself.",
                    "Press <kbd>Shift+Tab</kbd> at any time to cycle modes. If you are pointing it at something you care about, start stricter than you think you need to."),
            ),
        sec("05 · The commands worth memorising",
            p("Two kinds: shell commands that start a session, and slash commands you type inside one."),
            table(["Command", "What it does"], [
                ("claude", "start an interactive session"),
                ("claude \"task\"", "start with the first prompt already typed"),
                ("claude -p \"query\"", "run one query, print the answer, exit &mdash; good in scripts"),
                ("claude -c", "continue the most recent conversation in this directory"),
                ("claude -r", "pick a previous conversation to resume"),
                ("/help", "list the commands available to you"),
                ("/clear", "clear the conversation and start fresh"),
                ("/context", "show what is actually loaded into context right now"),
                ("/exit", "leave (or Ctrl+D twice)"),
            ]),
            muted("Type <code>/</code> on its own to see every command and skill available in this project."),
            ),
        sec("06 · What it can reach",
            p("The working directory you launched it in, and what your user account can touch from a shell. That is a bigger surface than most people picture the first time."),
            cats(("Reads", "Any file under the directory you started it in, without asking you to attach anything.", "the project"),
                 ("Runs", "Shell commands, with your permissions. Tests, builds, git, package installs.", "your account"),
                 ("Writes", "Edits files in place and creates new ones.", "on disk")),
            p("Which is why the next three steps of this guide exist: <a href=\"claude-code-context.html\">telling it about your project</a> so it stops guessing, and <a href=\"claude-code-guardrails.html\">putting guardrails on</a> so the things you never want touched stay untouched."),
            ),
        sec("Getting unstuck",
            ul("Be specific. &ldquo;Fix the login bug where users see a blank screen after wrong credentials&rdquo; beats &ldquo;fix the bug&rdquo;.",
               "Let it look before it leaps &mdash; ask it to analyse the schema before asking it to change anything.",
               "Break big asks into numbered steps; it follows a list well.",
               "<kbd>&uarr;</kbd> for history, <kbd>Tab</kbd> to complete a command, <code>/help</code> when lost."),
            verified(),
            ),
    ]),
    next=[("Next step", "Project, context and CLAUDE.md", "claude-code-context.html"),
          ("All guides", "Browse the rest", "../resources.html")],
)


# --------------------------------------------------------------------------
# 2 · Project, context and CLAUDE.md
# --------------------------------------------------------------------------

CONTEXT = dict(
    slug="claude-code-context",
    kind="Guide · Context",
    h1="Project, context and CLAUDE.md",
    lead="Every session starts with an empty head. CLAUDE.md is where you write down, once, the things you would otherwise re-explain every single time.",
    title="CLAUDE.md explained – project context, rules and auto memory",
    desc="Where CLAUDE.md lives, what belongs in it, how imports and path-scoped rules work, and how auto memory differs from the instructions you write yourself. Free, read on the page.",
    body="\n".join([
        sec("The tell that you need one",
            p("You correct the same thing twice. You explain the folder layout again. You say &ldquo;we use pnpm, not npm&rdquo; for the third session running."),
            p("Every Claude Code session begins with a fresh context window. Nothing carries over on its own. <code>CLAUDE.md</code> is the file it reads at the start of every session, so anything in there is something you never have to type again."),
            callout("<strong>Write it down the second time, not the fifth.</strong>",
                    "Good triggers: Claude makes the same mistake twice, a code review catches something it should have known, or a new teammate would have needed the same explanation."),
            ),
        sec("01 · Let it write the first draft",
            p("Do not start from a blank file. Inside your project, run:"),
            code("in the session", "/init"),
            p("It reads the codebase and writes a starting <code>CLAUDE.md</code> with the build commands, test commands and conventions it can find. If one already exists, <code>/init</code> suggests improvements instead of overwriting it."),
            muted("Then refine by hand. The useful half is what it could not discover on its own: why things are the way they are, and the rules that differ from the tool defaults."),
            ),
        sec("02 · Where the file goes",
            p("There are four places, and they all load &mdash; broadest first, so the most specific instruction is the last thing read."),
            table(["Scope", "Location", "For"], [
                ("Managed policy", "<code>/Library/Application Support/ClaudeCode/CLAUDE.md</code> (macOS)<br><code>/etc/claude-code/CLAUDE.md</code> (Linux, WSL)", "org-wide rules pushed by IT"),
                ("User", "<code>~/.claude/CLAUDE.md</code>", "your preferences, every project"),
                ("Project", "<code>./CLAUDE.md</code> or <code>./.claude/CLAUDE.md</code>", "the team's rules, committed to git"),
                ("Local", "<code>./CLAUDE.local.md</code>", "your own notes for this project &mdash; gitignore it"),
            ]),
            p("Files in directories above your working directory load at launch too, root-down. Files in subdirectories load on demand, when Claude reads something in that folder. To see what actually loaded in this session, run <code>/context</code> and look under <strong>Memory files</strong>."),
            ),
        sec("03 · What to write in it",
            p("Facts that should hold in every session: build and test commands, project layout, naming conventions, the &ldquo;always do X&rdquo; rules."),
            p("Specific beats tidy. Instructions you can verify get followed; vague ones get ignored."),
            cats(("Works", "&ldquo;Use 2-space indentation&rdquo;<br>&ldquo;Run <code>npm test</code> before committing&rdquo;<br>&ldquo;API handlers live in <code>src/api/handlers/</code>&rdquo;", "concrete, checkable"),
                 ("Doesn't", "&ldquo;Format code properly&rdquo;<br>&ldquo;Test your changes&rdquo;<br>&ldquo;Keep files organised&rdquo;", "nothing to check against")),
            ul("<strong>Keep it under about 200 lines.</strong> It loads into context every session, so a long file costs tokens and, counter-intuitively, gets followed less closely.",
               "<strong>Use headers and bullets.</strong> Claude scans structure the way you do.",
               "<strong>Remove contradictions.</strong> If two rules disagree, it may pick either one.",
               "<strong>Multi-step procedures do not belong here</strong> &mdash; those are <a href=\"claude-code-commands.html\">skills</a>."),
            ),
        sec("04 · Splitting it up",
            p("Two mechanisms, for two different problems."),
            p("<strong>Imports</strong> pull another file in with <code>@path</code>. Good for organisation; it does not save context, because imported files load at launch as well."),
            code("CLAUDE.md", "See @README for the project overview and @package.json for the npm scripts.\n\n# Additional instructions\n- git workflow @docs/git-instructions.md"),
            muted("To mention a path without importing it, wrap it in backticks. <code>@README</code> imports; <code>`@README`</code> stays literal."),
            p("<strong>Path-scoped rules</strong> in <code>.claude/rules/</code> only enter context when Claude touches a matching file, so they genuinely reduce noise:"),
            code(".claude/rules/api.md", "---\npaths:\n  - \"src/api/**/*.ts\"\n---\n\n# API rules\n\n- Every endpoint validates its input\n- Use the standard error response shape"),
            p("A rule with no <code>paths</code> field loads every session, same as <code>.claude/CLAUDE.md</code>. Personal rules that apply everywhere go in <code>~/.claude/rules/</code>."),
            ),
        sec("05 · The memory you don't write",
            p("Alongside the file you maintain, Claude keeps notes of its own. Auto memory is on by default, stored per repository on your machine."),
            cats(("user", "your role, expertise, how you like to work", "who you are"),
                 ("feedback", "corrections you gave, approaches you confirmed", "what you told it"),
                 ("project", "decisions and ongoing work it cannot read from the code", "what's going on"),
                 ("reference", "where things live outside the repo &mdash; tracker, dashboard", "where to look")),
            p("It deliberately skips anything it could work out from the codebase, and anything your CLAUDE.md already says. Run <code>/memory</code> to browse, edit or delete what it saved &mdash; it is all plain markdown &mdash; and to toggle the feature off."),
            code("~/.claude/settings.json", "{\n  \"autoMemoryEnabled\": false\n}"),
            ),
        sec("06 · When CLAUDE.md is the wrong tool",
            p("This is the part people learn the hard way. CLAUDE.md is <em>context</em>, not configuration. Claude reads it and tries to follow it. Nothing enforces it."),
            callout("<strong>If it absolutely must happen, it is not an instruction &mdash; it is a hook.</strong>",
                    "&ldquo;Never edit <code>.env</code>&rdquo; in CLAUDE.md is a request. The same rule as a <a href=\"claude-code-hooks.html\">PreToolUse hook</a> is enforced by your machine, whatever the model decides."),
            p("Same for anything that must run at a fixed moment &mdash; before every commit, after every edit. That is a lifecycle event, not a note."),
            ),
        sec("Troubleshooting",
            ul("<strong>It is ignoring the file.</strong> Run <code>/context</code> first &mdash; if it is not listed under Memory files, it never loaded, and the problem is the location, not the wording.",
               "<strong>It is too big.</strong> Over ~200 lines adherence drops. Move sections into path-scoped rules so they load only when relevant.",
               "<strong>Instructions vanished after <code>/compact</code>.</strong> The project-root CLAUDE.md is re-read from disk after compaction. Anything you only said in conversation is not &mdash; which is the argument for writing it down.",
               "<strong>Rules contradict each other.</strong> Review the whole chain: user, project, nested, and <code>.claude/rules/</code>."),
            verified(),
            ),
    ]),
    next=[("Next step", "Guardrails: stopping the agent before it breaks things", "claude-code-guardrails.html"),
          ("All guides", "Browse the rest", "../resources.html")],
)


# --------------------------------------------------------------------------
# 5 · Your own commands and skills
# --------------------------------------------------------------------------

COMMANDS = dict(
    slug="claude-code-commands",
    kind="Guide · Skills and commands",
    h1="Your own commands and skills",
    lead="If you are typing the same prompt a third time, it is not a prompt any more. It is a command you have not written down yet.",
    title="Claude Code skills and custom slash commands – a practical guide",
    desc="How to turn a repeated prompt into a reusable skill: where SKILL.md lives, the frontmatter that matters, arguments, injecting live command output, and pre-approving tools. Free, read on the page.",
    body="\n".join([
        sec("The moment to write one",
            flow(("", "Once", "you type the prompt"),
                 ("", "Twice", "you retype it, slightly differently"),
                 ("hook", "Third time", "write the skill")),
            p("The cost of a skill is about five minutes. The cost of not writing it is retyping a paragraph forever, slightly differently each time, and getting slightly different results because of it."),
            ),
        sec("01 · Where they live",
            p("A skill is a folder with a <code>SKILL.md</code> inside. The folder name becomes the command name."),
            table(["Location", "Scope", "Invoked as"], [
                ("<code>~/.claude/skills/&lt;name&gt;/SKILL.md</code>", "you, every project", "<code>/&lt;name&gt;</code>"),
                ("<code>.claude/skills/&lt;name&gt;/SKILL.md</code>", "this project, committed to git", "<code>/&lt;name&gt;</code>"),
                ("<code>.claude/commands/&lt;name&gt;.md</code>", "legacy command file, still works", "<code>/&lt;name&gt;</code>"),
            ]),
            muted("Legacy command files namespace by subdirectory: <code>.claude/commands/frontend/component.md</code> becomes <code>/frontend:component</code>."),
            ),
        sec("02 · What a SKILL.md looks like",
            p("YAML frontmatter, then plain markdown instructions. That is the whole format."),
            code(".claude/skills/review/SKILL.md", "---\nname: review\ndescription: Review the current diff for bugs before I open a PR\nargument-hint: [branch]\n---\n\n## Review the diff against $ARGUMENTS\n\n1. Read the full diff, not just the changed lines\n2. Flag anything that would fail CI\n3. Check the tests actually cover the new branch of logic\n4. Report findings worst-first, and stop"),
            p("The fields worth knowing:"),
            table(["Field", "What it does"], [
                ("<code>description</code>", "when Claude should reach for this by itself &mdash; the one field you should always write"),
                ("<code>argument-hint</code>", "what shows in autocomplete after you type the command"),
                ("<code>allowed-tools</code>", "tools pre-approved for this turn, so it does not stop to ask"),
                ("<code>disable-model-invocation</code>", "only you can run it; Claude will not trigger it on its own"),
                ("<code>user-invocable</code>", "set false to hide it from the <code>/</code> menu and let only Claude use it"),
            ]),
            ),
        sec("03 · Arguments",
            p("Everything typed after the command lands in <code>$ARGUMENTS</code>:"),
            code("SKILL.md", "Summarise these changes: $ARGUMENTS"),
            muted("<code>/summarise add search to the header</code> &rarr; Claude sees the whole sentence."),
            p("For more than one, use positions:"),
            code("SKILL.md", "---\narguments: [component, fromLang, toLang]\n---\n\nMigrate the $component component from $fromLang to $toLang.\nPreserve behaviour and tests."),
            muted("<code>/migrate Button JavaScript TypeScript</code>."),
            ),
        sec("04 · The part that makes skills actually useful",
            p("A skill does not have to be static text. It can run commands and paste the real output into the prompt before Claude ever reads it."),
            code("SKILL.md", "## Current state\n!`git status --short`\n!`git diff --stat`\n\n## Instructions\nReview only the files listed above."),
            p("And it can pull whole files in with <code>@</code>:"),
            code("SKILL.md", "## Conventions to follow\n@./.eslintrc.json\n\n## Code under review\n@./src/main.js"),
            callout("<strong>This is the difference between a snippet and a tool.</strong>",
                    "A skill with <code>!`git diff`</code> in it is never stale. It describes <em>how to look</em>, and the looking happens fresh every time you run it."),
            ),
        sec("05 · Pre-approving the tools it needs",
            p("A skill that stops four times to ask permission is not saving you anything. <code>allowed-tools</code> grants exactly what this command needs, for this turn only:"),
            code(".claude/skills/commit/SKILL.md", "---\nname: commit\ndescription: Stage and commit the current changes\ndisable-model-invocation: true\nallowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)\n---\n\nStage the changes, write a message describing why rather than what,\nand commit. Do not push."),
            muted("Note <code>disable-model-invocation: true</code>. Anything that writes, deploys or publishes should be something you trigger deliberately, not something the model can decide to run."),
            ),
        sec("06 · A full one, end to end",
            code("~/.claude/skills/fix-issue/SKILL.md", "---\nname: fix-issue\ndescription: Fix a GitHub issue by number. Use when asked to fix an issue.\nargument-hint: [issue-number]\narguments: [issue]\nallowed-tools: Bash(gh issue view *)\ndisable-model-invocation: true\n---\n\n## Fix issue #$issue\n\n### The issue\n!`gh issue view $issue --json title,body,comments`\n\n### Steps\n1. Understand what is actually being reported above\n2. Find the relevant files yourself\n3. Implement the fix in the smallest change that works\n4. Run `npm test`\n5. Commit as `fix(#$issue): <what changed>`"),
            p("Run <code>/fix-issue 123</code> and Claude starts with the real issue text already in front of it, rather than asking you to paste it."),
            ),
        sec("Rules of thumb",
            ul("Write the <code>description</code> for Claude, not for yourself &mdash; it is what decides whether the skill gets picked up automatically.",
               "Keep <code>SKILL.md</code> short. It loads when invoked, so a long one costs context every time.",
               "Ground it in live data with <code>!</code> instead of describing the state in prose.",
               "Anything destructive gets <code>disable-model-invocation: true</code>."),
            verified(),
            ),
    ]),
    next=[("Next step", "MCP: wiring in your own tools", "claude-code-mcp.html"),
          ("All guides", "Browse the rest", "../resources.html")],
)


# --------------------------------------------------------------------------
# 6 · MCP
# --------------------------------------------------------------------------

MCP = dict(
    slug="claude-code-mcp",
    kind="Guide · MCP",
    h1="MCP: wiring in your own tools",
    lead="By default the agent sees files. MCP is how you hand it your database, your issue tracker or an internal API &mdash; and exactly as far as you allow, no further.",
    title="MCP in Claude Code – connect your database, API and internal tools",
    desc="What MCP is, how to add local and remote servers, the three scopes, what .mcp.json looks like, how authentication and tool permissions work, and why you should not trust a server blindly. Free, read on the page.",
    body="\n".join([
        sec("The signal that you need it",
            p("You keep copying things into the chat. A stack trace out of Sentry. A ticket out of Jira. A row out of the database. Every paste is context you had to fetch by hand, and it is stale the moment you paste it."),
            flow(("", "Without MCP", "you look it up, copy it, paste it, and it is a snapshot"),
                 ("hook", "With MCP", "Claude queries the source itself, when it needs it")),
            p("MCP (Model Context Protocol) is an open standard for connecting an agent to external tools and data. Claude Code speaks it, so anything with an MCP server &mdash; and most of the tools you already use have one &mdash; becomes something Claude can read and act on directly."),
            ),
        sec("01 · Three kinds of server",
            cats(("stdio", "Runs as a process on your machine. Good for local things: a database, a filesystem tool, something you wrote yourself.", "--transport stdio"),
                 ("http", "A remote service over HTTP. This is what most hosted tools give you.", "--transport http"),
                 ("sse", "The older remote transport. Deprecated, still supported.", "--transport sse")),
            ),
        sec("02 · Adding one",
            p("A local server runs a command. Everything after <code>--</code> is passed to that command untouched:"),
            code("terminal", "claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \\\n  -- npx -y airtable-mcp-server"),
            p("A remote one just takes a URL:"),
            code("terminal", "claude mcp add --transport http notion https://mcp.notion.com/mcp"),
            p("With a token, if the service uses one rather than OAuth:"),
            code("terminal", "claude mcp add --transport http secure-api https://api.example.com/mcp \\\n  --header \"Authorization: Bearer your-token\""),
            ),
        sec("03 · Scope: who gets this server",
            p("The flag that decides whether this is yours, this project's, or the team's."),
            table(["Scope", "Loads in", "Shared", "Stored in"], [
                ("<code>local</code> (default)", "this project only", "no", "<code>~/.claude.json</code>"),
                ("<code>project</code>", "this project only", "yes, via git", "<code>.mcp.json</code> in the repo"),
                ("<code>user</code>", "all your projects", "no", "<code>~/.claude.json</code>"),
            ]),
            code("terminal", "claude mcp add --transport http shared-server --scope project https://example.com/mcp"),
            ),
        sec("04 · The committed file",
            p("Project-scoped servers land in <code>.mcp.json</code> at the repo root, so a teammate who clones the project gets the same tooling:"),
            code(".mcp.json", "{\n  \"mcpServers\": {\n    \"notion\": {\n      \"type\": \"http\",\n      \"url\": \"https://mcp.notion.com/mcp\"\n    },\n    \"database-tools\": {\n      \"type\": \"stdio\",\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"@example/mcp-server\"],\n      \"env\": {\n        \"DB_URL\": \"postgresql://localhost/mydb\"\n      }\n    }\n  }\n}"),
            callout("<strong>Do not commit secrets into it.</strong>",
                    "Expand them from the environment instead: <code>${API_KEY}</code>, or <code>${API_BASE_URL:-https://api.example.com}</code> to supply a default."),
            ),
        sec("05 · Logging in",
            p("Most hosted servers use OAuth. Add the server, then authenticate from inside a session:"),
            code("terminal", "claude mcp add --transport http sentry https://mcp.sentry.dev/mcp"),
            code("in the session", "/mcp"),
            p("That opens the browser login flow. From the shell, <code>claude mcp login sentry</code> does the same, and <code>claude mcp logout sentry</code> clears the credentials again."),
            ),
        sec("06 · How the tools show up",
            p("Once connected, the server's tools appear under a predictable name:"),
            code("naming", "mcp__<server-name>__<tool-name>\n\n# a `query` tool from a server named `database`\nmcp__database__query"),
            p("Which matters, because that name is what you write in permission rules, in a skill's <code>allowed-tools</code>, in a subagent's tool list, and in <a href=\"claude-code-hooks.html\">hook matchers</a>. A matcher of <code>mcp__database__.*</code> catches everything that server exposes."),
            muted("So the guardrails you already know apply here unchanged: an MCP tool is just another tool call, and a PreToolUse hook can deny it like any other."),
            ),
        sec("07 · Managing them",
            code("terminal", "claude mcp list              # everything configured\nclaude mcp get notion        # details for one\nclaude mcp remove notion     # disconnect it\nclaude mcp add-from-claude-desktop   # import what you already set up"),
            muted("<code>/mcp</code> inside a session shows live connection status, which is the first thing to check when a tool silently is not there."),
            ),
        sec("08 · The part to be careful about",
            p("An MCP server decides what content enters Claude's context. That makes a server you do not control a genuine attack surface, not a theoretical one."),
            ul("<strong>Trust the server before you connect it.</strong> A server that fetches external content can feed instructions into your session &mdash; this is prompt injection, and the agent has your permissions.",
               "<strong>Project-scoped servers ask for approval before first use</strong>, because they arrive in a file someone else can commit.",
               "<strong><code>headersHelper</code> runs a shell command on your machine</strong> to produce auth headers. Read it before you approve it.",
               "<strong>Scope narrowly.</strong> A read-only database server is a very different risk from one that can write."),
            callout("The useful instinct: connecting an MCP server is closer to installing a dependency than to changing a setting. Apply the same suspicion you would to an unfamiliar npm package."),
            verified(),
            ),
    ]),
    next=[("Back to the start", "Claude Code, from zero", "claude-code-intro.html"),
          ("All guides", "Browse the rest", "../resources.html")],
)


PAGES = [INTRO, CONTEXT, COMMANDS, MCP]


# --------------------------------------------------------------------------
# Assembly: take the hooks page as a shell, swap metadata and <main>
# --------------------------------------------------------------------------

def build(spec, shell):
    url = f"https://codeart.lt/en/resources/{spec['slug']}.html"
    s = shell

    s = re.sub(r'<title>.*?</title>', f'<title>{e(spec["title"])} | Free Resource</title>', s, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', rf'\1{e(spec["desc"])}', s)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', rf'\1{url}', s)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', rf'\1{e(spec["h1"])}', s)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', rf'\1{e(spec["desc"])}', s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', rf'\1{url}', s)

    # JSON-LD
    s = re.sub(r'("headline": ")[^"]*', rf'\1{e(spec["h1"])}', s)
    s = re.sub(r'("description": ")[^"]*', rf'\1{e(spec["desc"])}', s)
    s = re.sub(r'("url": ")https://codeart\.lt/en/resources/[^"]*', rf'\1{url}', s)

    # hero
    s = re.sub(r'(<span class="resource-card__type">)[^<]*', rf'\1{e(spec["kind"])}', s)
    s = re.sub(r'(<h1 class="display-l u-reveal">).*?(</h1>)', lambda m: m.group(1) + spec["h1"] + m.group(2), s, flags=re.S)
    s = re.sub(r'(<p class="lead u-reveal">).*?(</p>)', lambda m: m.group(1) + spec["lead"] + m.group(2), s, flags=re.S)

    # body
    body = spec["body"] + "\n" + whats_next(*spec["next"])
    start = s.index('<main class="content content--single container">')
    start = s.index('>', start) + 1
    end = s.index('</main>')
    s = s[:start] + "\n\n" + body + "\n" + s[end:]
    return s


def main():
    shell = SHELL.read_text()
    out = ROOT / "en" / "resources"
    for spec in PAGES:
        (out / f"{spec['slug']}.html").write_text(build(spec, shell))
        print(f"wrote en/resources/{spec['slug']}.html")


if __name__ == "__main__":
    main()
