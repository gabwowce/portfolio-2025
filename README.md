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
| `/lt/resources.html`, `/en/resources.html` | Guides (older design, built by `tools/build-resources.py`) |

The redesigned pages use only `css/site.css` and `js/site.js`. Fonts are self-hosted in `fonts/`.

## Editing the redesigned pages

All text and markup for both languages lives in `tools/build-site.py`. Edit it there, never in the generated HTML:

```sh
python3 tools/build-site.py           # writes the pages, redirects and sitemap.xml
python3 -m http.server 8765           # serve the repo root
node tools/build-cv-pdf.mjs           # prints lt/cv.pdf and en/cv.pdf (needs Playwright)
```

The design handoff (mockups, tokens, assets) is in `_redesign/handoff/`. Folders starting with `_` are not published.
