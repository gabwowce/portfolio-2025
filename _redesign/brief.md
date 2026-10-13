# codeart.lt perdizainas: planas ir promptas

Aplankas prasideda `_`, todėl GitHub Pages (Jekyll) jo nepublikuoja: šis failas
codeart.lt nepasirodys.

---

## 1. Kas dabar negerai (konkrečiai)

**Hero turi ~14 elementų, kurie konkuruoja tarpusavyje:** viršutinė eilutė su
tašku, H1 su `</>` ženkleliu, aprašymas, 2 mygtukai, 3 „statistikos“, „Priimu
naujus projektus“ ženklelis, oranžinė-žalia sfera, tinklelio fonas, personažas,
pakylos žiedas, lenta su 4 žingsniais ir 3 ranka rašytomis eilutėmis, „Žemyn“
užrašas. Akis nežino, kur žiūrėti.

**Procesas papasakotas du kartus ir nesutampa:** lentoje hero dalyje yra 4
žingsniai, o iškart po jos „Kaip iš tikrųjų vyksta darbas“ turi 3 žingsnius su
dideliais SVG maketais. Lankytojas turi perskaityti du skirtingus procesus.

**„Statistikos“ nėra statistikos:** „Full-stack“ ir „Nuo idėjos iki produkto“
yra šūkiai, apsimetantys skaičiais.

**Klasikiniai AI generuoto dizaino ženklai:** švytinti sfera, tinklelio fonas,
viršutinė eilutė su tašku ir mažomis didžiosiomis raidėmis (eyebrow), švytintys
mygtukai, „pill“ ženkleliai, trečias (ranka rašytas) šriftas, kontrasto frazės
(„Ne tik rašau kodą…“, „Ne „greitai padariau““), DIDŽIOSIOMIS RAIDĖMIS
rašomos antraštės, 3D AI generuotas personažas.

**Nėra ritmo tarp sekcijų:** commit `72899ab` panaikino sekcijų ribas, o
fiksuotas tinklelio fonas eina per visą puslapį, todėl viskas susilieja į
vieną paviršių.

**Darbai per toli:** pagrindiniame puslapyje projektai yra tik 4-oje vietoje
(po hero, proceso ir „Pažink mane“). Frontend programuotojos portfolio
svarbiausias įrodymas yra darbai.

### Dvi techninės problemos

- **Pelės šviesa:** kode ji veikia (patikrinta Chromium, 1440 px, pelė
  pajudinta: tinklelis aplink žymeklį šviečia). Jei nematai, labiausiai tikėtina,
  kad Windows nustatymuose išjungti *Animation effects* (Settings → Accessibility
  → Visual effects). Tada naršyklė praneša `prefers-reduced-motion: reduce`, ir
  svetainė efektą sąmoningai išjungia (`css/style.css`, `body::after`). Kita
  galimybė: naršyklėje užsilikusi sena versija.
- **Nuotraukos kokybė:** hero `<picture>` ir `<img>` abu gauna parallax
  `translate3d` su trupmeniniais pikseliais (`css/hero-rich.css`, ~565 eil.),
  todėl naršyklė perpiešia paveikslėlį atskirame GPU sluoksnyje ir jį suminkština.
  Be to, `standing-with-loptop` originale figūra yra tik 819 px pločio, o
  `tools/build-person-webp.py` ją padidina iki 900 px ir suspaudžia WebP
  kokybe 82. Naujame dizaine parallax nebelieka, o paveikslėlius reikia
  generuoti originaliu dydžiu, nedidinant.

---

## 2. Principai (kuo norime pasižymėti)

1. **Vienas puslapis atsako į lankytojo klausimus jų eiliškumu:** ką darai ir
   kam → parodyk → ką galiu užsisakyti → kaip tai vyksta → kas tu → kiek kainuoja
   / kiek trunka → kaip susisiekti.
2. **Viena sekcija = viena mintis.** Antraštė, 1–2 sakiniai, turinys. Jei
   sekcijai reikia paaiškinimo, ji per sudėtinga.
3. **Vienas pagrindinis veiksmas visur:** „Aptarti projektą“. Antrinis tik
   hero dalyje: „Peržiūrėti darbus“.
4. **Dekoracija tik viena.** Visas „wow“ biudžetas atiduodamas vienam
   dalykui (pvz. švelni pelės šviesa hero dalyje). Visa kita rami.
5. **Dizainas pats yra įrodymas.** Švarus tipografinis ritmas, tikslūs
   tarpai, greitas puslapis, gerai parašytas HTML/CSS. Tai frontend
   programuotojos portfolio: kodas turi būti rašytas ranka ir švarus.

---

## 3. Nauja pagrindinio puslapio struktūra

| # | Sekcija | Kas joje | Ko joje nebėra |
|---|---------|----------|----------------|
| 1 | Hero | H1, 1 sakinys, 2 mygtukai, 1 eilutė pasitikėjimui, 1 vaizdas | sfera, tinklelis, lenta, statistikos, ženkleliai |
| 2 | Darbai | 3 projektai: vaizdas, pavadinimas, 1 sakinys, 3 žymos, nuoroda | 4 skaičių blokai, ilgi „Mano vaidmuo“ tekstai (jie eina į projekto puslapį) |
| 3 | Paslaugos | 3 kortelės: pavadinimas, „Tinka, kai…“, 2 sakiniai | 6 žymų sąrašai kiekvienoje kortelėje |
| 4 | Kaip dirbame | 4 žingsniai, po vieną sakinį, be iliustracijų | SVG maketai, antras procesas |
| 5 | Apie mane | nuotrauka, 3 sakiniai, 3 faktai | 4 vertybių kortelės + 6 punktų sąrašas |
| 6 | DUK | 5 klausimai, išskleidžiami | |
| 7 | Kontaktas | forma (3 laukai) + el. paštas | naujienlaiškio forma poraštėje |

---

## 4. Promptas dizaino įrankiui

Kopijuok viską tarp linijų į **Claude Design** (rekomenduoju) arba Lovable.
Kartu įkelk: 1) dabartinio puslapio ekrano kopiją su prierašu „taip NEDARYTI“,
2) personažo iliustraciją arba savo tikrą nuotrauką, 3) 3 projektų ekrano
kopijas (`img/ac-cards-redacted-1400.webp`, TikMaker ir keepmi vaizdus).
Jei turi svetainių, kurios patinka išdėstymu (pvz. nutapyk.lt), įkelk jų
ekrano kopijas su prierašu „patinka aiškumas ir išdėstymas, ne stilius“.

────────────────────────────────────────────────────────────

Sukurk vieno puslapio portfolio svetainės dizainą programuotojai, kuri kuria
individualias verslo sistemas ir web aplikacijas. Svetainė lietuvių kalba.

**Kam ši svetainė:** Lietuvos smulkiam ir vidutiniam verslui (savininkams,
vadovams, ne programuotojams), kuriems reikia vidinės sistemos, valdymo
skydelio ar web aplikacijos, ir IT įmonėms, ieškančioms frontend/full-stack
programuotojos. Lankytojas turi per 10 sekundžių suprasti: ką ji daro, ar ji
tai jau yra dariusi, ir kaip pradėti.

**Svarbiausias reikalavimas – aiškumas.** Puslapis turi skaitytis kaip
gerai parašytas dokumentas: viena sekcija = viena mintis, aiški hierarchija,
daug laisvos erdvės, jokios perteklinės informacijos. Lankytojas niekada
neturi galvoti „ką čia turiu daryti?“.

**Griežti apribojimai (NEDARYTI):**
- jokių gradientinių sferų, švytėjimų, tinklelio fonų, triukšmo tekstūrų,
  glassmorphism;
- jokių „eyebrow“ eilučių virš antraščių (mažos didžiosios raidės su tašku);
- jokių ranka rašytų šriftų, jokių emoji, jokių dekoratyvių kodo simbolių
  (`</>`, `{}`);
- antraštės rašomos sakinio forma, NE DIDŽIOSIOMIS RAIDĖMIS;
- jokių netikrų statistikų ir šūkių skaičių vietoje;
- jokių pilių (pill) ženklelių „Available for work“ stiliumi;
- ne daugiau kaip 2 šriftai (vienas antraštėms, vienas tekstui) ir 1 akcento
  spalva, naudojama tik mygtukams, nuorodoms ir aktyvioms būsenoms;
- jokių kortelių kortelėse; jokių animacijų, išskyrus subtilų atsiradimą
  slenkant.

**Vizualinė kryptis:** ramus, redakcinis, profesionalus. Šiltas šviesus fonas
(ne grynai baltas), tamsiai pilkas tekstas, viena terakotinė/oranžinė akcento
spalva (#D9734E arba artima). Aiškus sekcijų atskyrimas: pakaitomis keičiamas
fono tonas ARBA plona linija ir dideli vertikalūs tarpai (min. 120 px desktop).
Teksto stulpelis ne platesnis nei ~65 simboliai. Tamsi tema – antraeilė,
pirmiausia sukurk šviesią.

**Struktūra ir tekstai** (naudok būtent šiuos tekstus; jei kas nors netelpa,
trumpink, nepridėk naujų):

1. **Navigacija:** kairėje „Gabrielė Tamaševičiūtė“; dešinėje: Darbai,
   Paslaugos, Apie, DUK, LT/EN ir mygtukas „Aptarti projektą“.

2. **Hero**
   - H1: „Verslo sistemų ir web aplikacijų kūrimas“
   - Sakinys: „Vidiniai įrankiai, valdymo skydeliai ir web aplikacijos nuo
     idėjos iki paleidimo. Fiksuota kaina, sutarta prieš pradedant.“
   - Mygtukai: „Aptarti projektą“ (pagrindinis), „Peržiūrėti darbus“ (antrinis,
     tekstinis).
   - Po mygtukais viena smulki eilutė: „Programuotoja Vilniuje · React,
     TypeScript, API ir AI funkcijos · Priimu naujus projektus“.
   - Dešinėje vienas vaizdas: mano nuotrauka/iliustracija ARBA geriausio
     projekto ekrano kopija naršyklės rėmelyje. Ne abu.

3. **Darbai** – antraštė „Atlikti darbai“. 3 projektai, pirmas didesnis:
   - **Lojalumo valdymo sistema (B2B backoffice).** „Kortelių, kuponų, akcijų
     ir segmentų valdymas vienoje sistemoje: ~27 maršrutai, 8 sritys, rolės ir
     auditas.“ Žymos: React, TypeScript, REST API. Nuoroda: „Skaityti plačiau“.
   - **TikMaker.** „Vaizdo redaktorius su AI įgarsinimu: balso takelis
     generuojamas tiesiai laiko juostoje.“ Žymos: React, Remotion, ElevenLabs.
   - **keepmi.** „Skaitmeniniai kvietimai ir svečių centras šventės dienai:
     albumas, programa, viktorinos, 3 kalbos, Stripe mokėjimai.“ Žymos:
     Next.js, Supabase, Stripe. Nuoroda: „Live demo“.
   - Apačioje nuoroda „Visi projektai →“.

4. **Paslaugos** – antraštė „Su kuo galiu padėti“. 3 lygiavertės kolonos:
   - **Nauja sistema nuo nulio.** Tinka, kai: reikia ne puslapio, o veikiančio
     produkto. „Padedu išgryninti sprendimą, suprojektuoju sąsają ir sukuriu
     sistemą nuo frontendo iki API ir duomenų bazės.“
   - **Esamos sistemos gerinimas.** Tinka, kai: sistema veikia, bet lėta ar
     sunkiai vystoma. „Pirmiausia randu, kur problema, tada tvarkau tai, kas
     iš tikrųjų trukdo.“
   - **Naujos funkcijos esamai sistemai.** Tinka, kai: produkto nereikia
     perrašyti. „Perprantu esamą kodą ir kuriu naujas funkcijas, negriaudama
     to, kas jau veikia.“

5. **Kaip dirbame** – antraštė „Kaip vyksta darbas“. 4 sunumeruoti žingsniai
   horizontaliai (mobiliajame – vertikaliai), be ikonų:
   1. **Parašote.** Trumpai, ko reikia. Techninių terminų nereikia.
   2. **Planas ir kaina.** Per 24 val. po pokalbio gaunate planą ir fiksuotą
      kainą raštu.
   3. **Kūrimas.** Progresą matote nuolat, ne tik pabaigoje.
   4. **Paleidimas.** Įdiegiu sistemą. Mano darbui taikoma 3 mėn.
      garantija.

6. **Apie mane** – antraštė „Apie mane“. Kairėje nuotrauka, dešinėje:
   „Esu Gabrielė, programuotoja iš Vilniaus. Kuriu sistemas, kuriomis žmonės
   naudojasi kasdien: nuo duomenų modelio iki sąsajos. Prieš keisdama kodą
   pirmiausia suprantu problemą.“ Po tekstu 3 faktai eilute: „3+ metai
   kuriant sistemas“, „Frontend, backend ir API“, „Dirbu su esamu kodu“.
   Nuoroda „Daugiau apie mane →“.

7. **DUK** – antraštė „Dažni klausimai“. Išskleidžiamas sąrašas:
   - Kiek kainuoja projektas? → [įrašyti: nuo X € / kaip skaičiuojama]
   - Kiek laiko trunka? → [įrašyti: tipinis terminas]
   - Ar galite perimti jau veikiančią sistemą? → Taip, perprantu esamą kodą ir
     tobulinu jį palaipsniui.
   - Ar kaina gali pasikeisti eigoje? → Ne. Patvirtinus sąmatą, kaina
     nesikeičia.
   - Ar galite į sistemą įdiegti AI funkcijas? → Taip, nuo paprastų LLM
     funkcijų iki agentų, kurie naudojasi sistemos API.

8. **Kontaktas** – antraštė „Turite projekto idėją?“. Sakinys: „Parašykite
   kelis sakinius, ko reikia. [Atsakau per X darbo dienas.]“ Forma: vardas,
   el. paštas, žinutė, mygtukas „Siųsti“. Šalia: el. paštas, LinkedIn, GitHub.

9. **Poraštė** – viena eilutė: vardas, © metai, LT/EN, el. paštas.

**Ką pateikti:**
1. Pirmiausia 2 skirtingas vizualines kryptis tik hero + darbų sekcijai
   (desktop 1440 px), kad galėčiau pasirinkti.
2. Pasirinktą kryptį – visas puslapis desktop (1440 px) ir mobile (390 px).
3. Trumpą dizaino sistemą: spalvos (hex), šriftai ir dydžių skalė, tarpai,
   mygtukų ir nuorodų būsenos, kortelės komponentas.

────────────────────────────────────────────────────────────

---

## 5. Kaip sujungti su codeart.lt

Svetainė, kurią matai codeart.lt, yra būtent šis repo (`CNAME`). Todėl
„sujungti“ reiškia perrašyti šį repo pagal naują dizainą, o ne jungti dvi
svetaines.

1. **Turinys (1 vakaras, tu).** Perskaityk aukščiau esančius tekstus,
   pataisyk, kas netikslu, įrašyk DUK kainą ir terminus.
2. **Dizainas (Claude Design).** Promptas iš 4 skyriaus → pasirink vieną iš 2
   krypčių → pilnas pagrindinis puslapis desktop + mobile.
3. **Kodas (aš, šiame repo).** Dizainą naudojam kaip maketą, ne kaip kodą.
   Lovable sugeneruotų React + Tailwind + shadcn aplikaciją: ji atrodytų kaip
   tūkstančiai kitų Lovable svetainių ir pakeistų tavo statinį, greitą,
   SEO sutvarkytą puslapį. Vietoje to:
   - vienas naujas `css/site.css` su dizaino tokenais vietoje dabartinių ~19 CSS
     failų;
   - išsaugomi URL, `hreflang`, JSON-LD, `sitemap.xml`, kanoniniai adresai;
   - JS lieka tik tai, ko reikia (meniu, tema, kontaktų forma, DUK).
4. **Eilė:** pagrindinis LT → portfolio → paslaugos → apie → kontaktai →
   EN versija → senų CSS failų ir nenaudojamų paveikslėlių išvalymas.

### Sprendimas, kurį turi priimti tu

**Personažas ar tikra nuotrauka?** 3D AI generuotas personažas yra stipriausias
„AI svetainės“ signalas šiame puslapyje. Tikra nuotrauka (net paprasta,
telefonu, prie lango) labiau kelia pasitikėjimą klientams, kurie perka
paslaugą iš žmogaus. Jei personažas tau svarbus kaip prekės ženklas, palik jį
vienoje vietoje (pvz. „Apie mane“), ne visur.
