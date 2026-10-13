# codeart.lt perdizainas: planas ir promptas

Aplankas prasideda `_`, todėl GitHub Pages (Jekyll) jo nepublikuoja: šis failas
codeart.lt nepasirodys.

---

## 0. Dvi auditorijos, du įėjimai, vienas domenas

Dabartinė svetainė bando vienu metu kalbėti dviem žmonėms, todėl nė vienam
nekalba gerai: šalia „Fiksuota kaina“ stovi „RTK Query tipai iš schemos“.

| | Užsakovas | Darbdavys / tech lead |
|---|---|---|
| Klausia | Ar išspręs mano problemą? Kiek kainuos? Kaip pradėti? | Kaip ji mąsto? Kokia jos rolė komandoje? Koks stackas? |
| Nori matyti | rezultatą, procesą, kainą, kontaktą | techninius sprendimus, patirtį, CV, GitHub |
| Įeina per | Google, rekomendaciją → `codeart.lt` | tavo atsiųstą nuorodą → `codeart.lt/portfolio` |

**Struktūra:**

- `codeart.lt` (`/lt/`, `/en/`): tik užsakovams. Mažai techninių terminų.
  Viena pagrindinė užduotis: „Aptarti projektą“.
- `codeart.lt/portfolio` (`/lt/portfolio/`, `/en/portfolio/`): tik
  darbdaviams. CV ir portfolio viename puslapyje. Pagrindinėje navigacijoje jos
  nėra, tik poraštėje („CV ir portfolio“). Darbdaviams tiesiog siunti šią
  nuorodą. Darbdaviams Lietuvoje dažniausiai užtenka LT versijos, bet
  tarptautinėms įmonėms reikia EN.
- Projektų puslapiai (`/lt/projektai/lojalumo-sistema/` ir t. t.) bendri.
  Viršuje rezultatas, žemiau techninė dalis. Užsakovas perskaito pradžią,
  darbdavys skaito iki galo.
- Dizaino sistema bendra (spalvos, šriftai, komponentai), todėl abu
  puslapiai atrodo kaip viena svetainė.

**Ką turi nuspręsti tu (keičia `/portfolio` tekstus):** ko ieškai darbdavio
puslapiu? Naujos pilnos darbo vietos, papildomų projektų ar tik nori turėti
nuorodą „jei kas paklaus“? Nuo to priklauso pirmas sakinys ir ar rašyti
„Atvira pasiūlymams“.

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
yra šūkiai, apsimetantys skaičiais. O „3+ metai kuriant sistemas“ neatitinka
tavo pačios „Apie“ puslapio: programuoji profesionaliai nuo 2024 m. birželio
(UVS), laisvai samdoma dirbi nuo 2025 m. kovo. 2026 m. spalį tai yra ~2,3
metų. Tiksliau būtų „2+ metai“ arba visai be skaičiaus.

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
   pirmiausia suprantu problemą.“ Po tekstu 3 faktai eilute: „2+ metai
   profesionaliai kuriant sistemas“, „Frontend, backend ir API“, „Dirbu su
   esamu kodu“.
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

## 4b. Antra žinutė Claude Design (tame pačiame pokalbyje)

Abi pirmos kryptys (A redakcinė, B struktūrinė) yra pilki skeletai su
tuščiais laukeliais: iš jų sunku spręsti, nes trūksta tikrų vaizdų ir bet
kokio asmeniškumo. Iš „per daug“ peršokome į „nieko“. Prie žinutės pridėk
tikrus vaizdus (nuotrauką, 3 projektų ekranų kopijas).

────────────────────────────────────────────────────────────

Nė viena kryptis kol kas netinka. Kas tinka ir kas ne:
- iš B imame struktūrą: hero dešinėje tikro projekto ekranas naršyklės
  rėmelyje, darbai sąrašu su linijomis tarp jų;
- iš A imame šiltumą: sekcijos atskirtos skirtingu fono tonu;
- netinka: per didelė H1 (užima pusę ekrano), per smulkus ir per blyškus
  tekstas, A serifinės antraštės primena teisininkų biurą, o ne
  programuotoją, B tekstas serifiniu šriftu po groteskine antrašte atrodo
  atsitiktinai. Vienas groteskinis šriftas antraštėms ir tekstui, kitas tik
  kodui/žymoms (monospace);
- trūksta vieno asmeniško elemento. Ne dekoracijos, o kažko, kas parodo,
  kad tai frontend programuotojos darbas (pvz. tikslios mikrosąveikos ant
  projektų kortelių, švelni pelės šviesa tik hero dalyje).

Pridedu tikrus vaizdus, naudok juos vietoj laukelių.

**Pakeitimas: svetainė turi dvi auditorijas, todėl du puslapius.**

1. **Pagrindinis puslapis (`codeart.lt`) – tik užsakovams.** Struktūra ir
   tekstai lieka tokie, kokie buvo pirmame prompte. Projektų žymas palik
   mažas ir tylias, užsakovui jos antraeilės. Poraštėje pridėk nuorodą
   „CV ir portfolio“.

2. **Naujas puslapis `codeart.lt/portfolio` – darbdaviams.** CV ir portfolio
   viename. Ta pati dizaino sistema, bet tankesnis, labiau dokumento
   formos. Turi gerai atrodyti ir atspausdintas (A4), nes jis atstoja CV.
   Struktūra:
   - **Viršus:** „Gabrielė Tamaševičiūtė“, „Frontend / full-stack
     programuotoja · React, TypeScript“, „Vilnius“. Vienas sakinys:
     „Kuriu vidines verslo sistemas nuo architektūros iki sąsajos.“
     [Būsena: įrašyti, pvz. „Atvira pasiūlymams“]. Nuorodos eilute: CV (PDF),
     GitHub, LinkedIn, el. paštas.
   - **Atrinkti darbai:** 3 projektai, kiekvienas su: problema (1 sakinys),
     mano rolė, 2–3 techniniai sprendimai, stackas, rezultatas. Pirmas:
     *Lojalumo valdymo sistema (B2B backoffice).* Rolė: atsakinga už
     frontendą, rašau technines užduotis backend kolegai, deriname API
     kontraktus prieš įgyvendinimą. Sprendimai: API tipai generuojami iš
     backend schemos (RTK Query), todėl neatitikimai matomi prieš
     produkciją; AG Grid didelėms lentelėms; kiekviena funkcija veikia
     vienodai masiniame veiksme ir detalės dialoge. Mastas: ~27 maršrutai,
     8 sritys, 2 × ~2200 vertimo raktų, rolės ir auditas. Stackas: React,
     TypeScript, RTK Query, AG Grid, REST API. Antras: *TikMaker* (React,
     TypeScript, Remotion, ElevenLabs). Trečias: *keepmi* (Next.js,
     next-intl, Supabase, Stripe).
   - **Patirtis** (laiko juosta):
     - Programuotoja (Mid), UVS · 2026 kov. – dabar · React, TypeScript,
       C#/.NET. Vidinė verslo sistema nuo nulio: vienintelė frontend
       programuotoja, suprojektavau architektūrą ir sąsają, planuoju
       backend struktūrą ir deleguoju užduotis backend kolegai.
     - Web ir mobile app programuotoja, laisvai samdoma · 2025 kov. –
       dabar · React, Next.js, TypeScript. Projektai nuo poreikių iki
       paleidimo, tarp jų „Kibinukai“ užsakymų sistema.
     - Jaunesnioji programuotoja, UVS · 2024 birž. – 2026 vas. · C#/.NET,
       WPF. SCO sistemos ekranai, nauji funkcionalumai, klaidų analizė,
       UI prieinamumas.
     - Ankstesnė patirtis (viena eilutė): planuotoja, Girteka Europe West
       (2021–2023); administratorė, UAB „Jarinta“ (2021).
   - **Technologijos:** trys grupės be įgūdžių juostų ir procentų:
     Frontend (React, TypeScript, Next.js, Tailwind, RTK Query, AG Grid),
     Backend ir duomenys (REST API, Supabase, autentifikacija, duomenų
     bazės), Kita (C#/.NET, WPF, Figma, WordPress, LLM integracijos, AI
     agentai).
   - **Kaip dirbu komandoje:** 3 trumpi punktai: galvoju apie visą sistemą,
     ne tik ekraną; pirma randu priežastį, tik tada keičiu kodą; perprantu
     svetimą kodą ir jį gerinu palaipsniui.
   - **Išsilavinimas:** Vilniaus kolegija, Programų sistemos, 2023–2027
     (studijuoju).
   - **Apačioje:** el. paštas ir mygtukas „Atsisiųsti CV (PDF)“.

Pateik: pagrindinį puslapį pagal naują kryptį (desktop + mobile) ir
`/portfolio` puslapį (desktop + mobile + kaip atrodo atspausdintas A4).

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
4. **Eilė:** pagrindinis LT → `/lt/portfolio/` darbdaviams → projektų
   puslapiai → paslaugos → apie → kontaktai → EN versija → senų CSS failų ir nenaudojamų paveikslėlių išvalymas.

### Sprendimas, kurį turi priimti tu

**Personažas ar tikra nuotrauka?** 3D AI generuotas personažas yra stipriausias
„AI svetainės“ signalas šiame puslapyje. Tikra nuotrauka (net paprasta,
telefonu, prie lango) labiau kelia pasitikėjimą klientams, kurie perka
paslaugą iš žmogaus. Jei personažas tau svarbus kaip prekės ženklas, palik jį
vienoje vietoje (pvz. „Apie mane“), ne visur.

---

## 4c. Trečia žinutė Claude Design: išskirtinė detalė + pilni puslapiai

Pagrindinė detalė: „Specifikacijų“ režimas (kaip Figma Dev Mode). Jis parodo
tai, ką frontend programuotoja mato kurdama: tarpus, šriftų dydžius ir
tinklelį. Užsakovui tai tylus kokybės ženklas, o darbdaviui tiesioginis
kompetencijos įrodymas. Antra detalė: poraštėje sąžininga eilutė apie
paties puslapio kodą (skaičiai įrašomi tik išmatavus galutinę versiją).

Tekstas žinutei yra pokalbyje ir kartojamas čia nebus. Jei jo prireiks, jis
kartu su šiuo failu išsaugotas `_redesign/prompt-3.txt`.
