# codeart.lt perdizainas: perdavimas programavimui

Šiame pakete yra galutinis codeart.lt dizainas, paruoštas įgyvendinti esamame repozitorijoje `gabwowce/portfolio-2025` (GitHub Pages, `CNAME` → codeart.lt).

## Kaip naudoti (Claude Code)

1. Dizaino failai (`design/*.dc.html`) yra **maketai, ne galutinis kodas**. Juose stiliai rašyti tiesiai elementuose (inline), yra `{{...}}` šablonų vietos ir `class Component extends DCLogic` skriptai. Šiuos failus perskaityk kaip vizualinę ir turinio specifikaciją, o svetainę perrašyk į švarų, semantinį HTML ir vieną CSS failą.
2. Tekstai maketuose yra galutiniai. Jų netrumpink ir nepildyk naujais faktais. Vietos `[TAIP PAŽYMĖTOS]` bus užpildytos vėliau, todėl palik jas aiškiai matomas.
3. Visi vaizdai yra `assets/`, o maketai į juos rodo per `../assets/…`.

## Įgyvendinimo taisyklės

- Statinis HTML + CSS, be framework'ų. JS tik ten, kur reikia: mobile meniu, DUK išskleidimas, aktyvios nuorodos linija navigacijoje, atsiradimas slenkant, kontaktų forma.
- Vienas `css/site.css` su dizaino tokenais (CSS kintamieji) vietoje dabartinių ~19 CSS failų.
- Išsaugoti esamus URL, `hreflang`, JSON-LD, `sitemap.xml` ir kanoninius adresus.
- Pirmiausia LT versija, po to EN.
- Vaizdai: `loading="lazy"` visiems, išskyrus hero; `width`/`height` atributai; WebP originaliu dydžiu, be didinimo.
- Visur turi būti `prefers-reduced-motion: reduce` palaikymas: jokio judesio, viskas matoma iš karto.
- Prieinamumas: tikri `<button>` / `<a>`, `aria-expanded` DUK ir meniu mygtukams, paspaudžiami plotai ≥ 44 × 44 px, matomas focus (2px #1C1A17, offset 2px).

## Puslapiai

| Maketas | Paskirtis | Siūlomas URL |
|---|---|---|
| `Main.dc.html` (+ `HomeMobile`, `HomeMobileMenu`) | Pagrindinis, užsakovams | `/` (LT), `/en/` |
| `Portfolio.dc.html` (+ `PortfolioMobile`) | CV ir portfolio, darbdaviams | `/portfolio` |
| `Projektas-Kalbos.dc.html` (+ mobile) | Kalbų mokymosi platforma | `/portfolio/kalbu-platforma` |
| `Projektas-TikMaker.dc.html` (+ mobile) | TikMaker | `/portfolio/tikmaker` |
| `Projektas-AC.dc.html` (+ mobile) | Lojalumo valdymo sistema (trumpas) | `/portfolio/lojalumo-sistema` |
| `CV-1.dc.html` | Vienas A4 lapas, CV PDF | `/cv.pdf` (generuoti iš print CSS arba atskiro HTML) |
| `DesignSystem.dc.html` | Dizaino sistemos lapas (tik nuoroda, ne puslapis) | – |

Mobile maketai (`*Mobile.dc.html`) tik įterpia desktop failą 390 px pločiu, todėl tai ta pati responsyvi svetainė. Riba tarp desktop ir mobile: **760 px**.

Projektų tvarka visur: 1) Kalbų mokymosi platforma, 2) TikMaker, 3) Lojalumo valdymo sistema. Nuorodos „Kitas darbas“ eina ratu tokia pačia tvarka.

## Dizaino tokenai

**Spalvos**
- `--bg-base: #F6F0E6` (hero, 02, 04, 06 sekcijos), `--bg-raised: #FBF7F0` (01, 03, 05), `--surface: #FFFFFF`
- `--line: #DDD2C1`, `--line-frame: #D3C8B6`, `--line-input: #8F8577`, `--line-strong: #1C1A17`
- `--text: #1C1A17`, `--text-body: #36322D`, `--text-muted: #5B544C`, `--text-meta: #6A635A`
- `--accent: #A9502F` (tik mygtukai, nuorodos, aktyvios būsenos), `--accent-hover: #8C4229`
- Dėmės: `--blob-sand: #EEDFC6` (hero `#ECDDC4`, lojalumo sistema), `--blob-rose: #F2D9D3` (kalbų platforma), `--blob-lavender: #EBDCE1` (TikMaker), `--blob-apricot: #F2DDCB` („Apie mane“)

**Šriftai:** Schibsted Grotesk 400/500/600 (antraštės ir tekstas), JetBrains Mono 400/500 (tik žymos, datos, sekcijų numeriai). Google Fonts, `latin-ext`.

**Tipografija (px, dydis/eilutė; mobile skliaustuose):** H1 56/60 (36/40), H2 40/44 (28/32), H3 projekto 28/34 (24/30), H3 24/30, Lead 20/32, Body 18/28, Small 15/22, Mono 13/20. Antraštėms `letter-spacing` nuo −0.015em iki −0.03em.

**Tarpai:** 4, 8, 12, 16, 24, 32, 40, 48, 64, 96, 128. Sekcijos 128 (mobile 64), antraštė → turinys 48 (32), projekto eilutė 96 (mobile 48/56).

**Tinklelis:** konteineris 1280, šoninės paraštės 40 (mobile 20), turinys 1200, 12 kolonų po 78, tarpas 24.

## Komponentai ir elgsena

- **Navigacija:** desktop rodo nuorodas, LT / EN ir mygtuką „Aptarti projektą“. Aktyvios sekcijos nuoroda pabraukiama 1.5px akcento linija, kuri slenka tarp nuorodų (320 ms). Mobile turi 64px juostą ir hamburger mygtuką, kuris atidaro viso ekrano meniu su didelėmis nuorodomis, LT / EN ir pilno pločio mygtuku. Uždarymo mygtukas yra toje pačioje vietoje.
- **Sekcijos antraštė:** `01 —` (Mono 13/20, `--text-meta`, `aria-hidden`) + H2.
- **Hero:** tekstas užima 1–5 kolonas, scena 6–12. Scenoje nešiojamo kompiuterio maketas (CSS: tamsus dangtis su 1.5px šviesiu kraštu, sidabrinis pagrindas 14px), už jo smėlio dėmė. `plant.webp` stovi kairėje, už kompiuterio (žemesnis z-index), apačia sulygiuota su pagrindu, apie 400px aukščio. Mobile augalo nėra.
- **Projekto eilutė (pagrindinis puslapis):** tekstas 1–4 kolonose, ekranas 6–12 naršyklės rėmelyje (1px, r12, 26px juosta, langas 19:10). Už ekrano organinė SVG dėmė, išlendanti 40–72px. Užvedus pelę dėmė pasisuka ±2° ir padidėja 2.5 % per 400 ms, o ekrano kopija lėtai paslenka `object-position` iš viršaus į apačią (1400 ms).
- **Atsiradimas slenkant:** `IntersectionObserver` (threshold 0.15). Elementai pereina iš `opacity: 0` ir `translateY(16px)` (ekranai 32px) per 700–900 ms. Grupėse pasirodo vienas po kito su 100 ms tarpu. Kiekvienas elementas animuojamas tik vieną kartą.
- **DUK:** `<button aria-expanded>`, mažiausiai 64px aukščio, „+“ ikona pasisuka 45°.
- **Forma:** etiketė virš lauko, laukas 48px aukščio, kraštas `--line-input`.
- **Organinės dėmės:** SVG keliai yra maketuose (`viewBox="-2 -2 104 104"`, `preserveAspectRatio="none"`). Spalva vienalytė, be gradientų ir šešėlių.

## Vaizdai (`assets/`)

| Failas | Kur naudojamas |
|---|---|
| `hero-dashboard.webp` | Hero kompiuterio ekranas (pavyzdinė TransLog sistema) |
| `kalbos-mokinys.webp` | Kalbų platforma: kortelės pagrindiniame ir /portfolio |
| `kalbos-admin.webp` | Kalbų platformos puslapis, 01 |
| `kalbos-uzduotis.webp` | Kalbų platformos puslapis, 02 |
| `tikmaker-editor.webp` | TikMaker kortelės ir puslapio 01 |
| `ac-cards-redacted-1400.webp` | Lojalumo sistemos kortelės ir puslapio 01 (duomenys uždengti) |
| `ac-loyalty-redacted-1400.webp` | Lojalumo sistemos puslapio 02 (duomenys uždengti) |
| `about-illustration.webp` | „Apie mane“ |
| `plant.webp` | Hero augalas (permatomas fonas, naudoti be filtrų) |

## Dar trūksta (laukeliai maketuose)

- Kalbų platforma: kliento pavadinimas, būsena; ekrano kopijos 01 (aprėpties lentelė), 02 (atsakymo grįžtamasis ryšys), 03 (importo dialogas). Dabar 01 ir 02 vietoje laikinai stovi artimiausi turimi ekranai.
- TikMaker: ekrano kopijos 02 (Visuals biblioteka) ir 03 (subtitrai / Render MP4).
- /portfolio ir CV: [BŪSENA], LinkedIn nuoroda.
- Pagrindinis: DUK kaina ir terminas, „Atsakau per X darbo dienas“.
- „Kiti darbai“ sąraše dalies projektų Live / GitHub nuorodos yra `#`.
