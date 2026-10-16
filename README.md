# codeart.lt

Portfolio and services site of Gabrielė Tamaševičiūtė. Static HTML and CSS on GitHub Pages, no framework.

## Structure

| URL | Page |
|---|---|
| `/lt/`, `/en/` | Home, for clients |
| `/lt/portfolio.html`, `/en/portfolio.html` | CV and portfolio, for employers (`/portfolio` redirects to the LT page) |
| `/lt/services.html`, `/en/services.html` | Services, process, price and warranty, FAQ |
| `/lt/about.html`, `/en/about.html` | About: how I work, values, experience, education |
| `/lt/contact.html`, `/en/contact.html` | Contact details and form |
| `/lt/projektai/*.html`, `/en/projects/*.html` | Project pages |
| `/lt/cv.pdf`, `/en/cv.pdf` | One-page CV, printed from `lt/cv.html` and `en/cv.html` |

The redesigned pages use only `css/site.css` and `js/site.js`. Fonts are self-hosted in `fonts/`.

## Editing the redesigned pages

All text and markup for both languages lives in `tools/build-site.py`. Edit it there, never in the generated HTML:

```sh
python3 tools/build-site.py           # writes the pages, redirects and sitemap.xml
python3 -m http.server 8765           # serve the repo root
node tools/build-cv-pdf.mjs           # prints lt/cv.pdf and en/cv.pdf (needs Playwright)
```

The design handoff (mockups, tokens, assets) is in `_redesign/handoff/`. Folders starting with `_` are not published.

## Service pages and articles

Their text lives outside `tools/build-site.py`:

| What | Where | Output |
|---|---|---|
| Service pages, LT and EN | `tools/services_content.py` | `/lt/paslaugos/*.html`, `/en/services/*.html` |
| Articles (LT) | `_content/straipsniai/<slug>.html` | `/lt/straipsniai/<slug>.html`, list at `/lt/straipsniai/` |

An article file starts with a JSON header in an HTML comment (title, description, date, related service, `status`), followed by the body as plain HTML.

Every page has `"status": "draft"` or `"published"`:

```sh
python3 tools/build-site.py --drafts   # preview: drafts are built too, marked and noindex
python3 tools/build-site.py            # normal build: published pages only, draft files are deleted
```

- Never commit a `--drafts` build. Always run the normal build before committing.
- Text in `[square brackets]` is a placeholder that still has to be filled in. The build prints a warning if a published page still contains one.
- Links in a published article that point to a draft are turned into plain text, so the live site never links to a page that isn't online.
- The "Straipsniai" menu link, the list of service pages on `services.html` and the sitemap entries appear automatically once something is published.

To publish an article: fill in the placeholders, set `"status": "published"` and `"date"` to the publication date, run the normal build, then commit.
