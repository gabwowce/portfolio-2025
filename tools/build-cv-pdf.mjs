/*
  Print the CV sheets (lt/cv.html, en/cv.html) to lt/cv.pdf and en/cv.pdf,
  and copy the LT one over the old address docs/CV-Gabrielė-Tamaševičiūtė.pdf.

  Needs the site served locally, because the pages use root-relative
  paths for fonts and styles:
    python3 -m http.server 8765        (from the repo root)
    node tools/build-cv-pdf.mjs        (Playwright must be installed)
*/
import { copyFileSync } from "node:fs";
import { chromium } from "playwright";

const BASE = process.env.BASE_URL || "http://localhost:8765";
const browser = await chromium.launch();
const page = await browser.newPage();

for (const lang of ["lt", "en"]) {
  await page.goto(`${BASE}/${lang}/cv.html`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: `${lang}/cv.pdf`,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
  });
  console.log(`wrote ${lang}/cv.pdf`);
}

await browser.close();

// The old CV address (docs/) may still be in emails and job applications:
// it serves a copy of the current Lithuanian CV, so only the new one exists.
copyFileSync("lt/cv.pdf", "docs/CV-Gabrielė-Tamaševičiūtė.pdf");
console.log("copied lt/cv.pdf to docs/");
