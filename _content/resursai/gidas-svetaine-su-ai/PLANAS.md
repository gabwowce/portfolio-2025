# Gidas „Kaip susikurti svetainę su AI: nuo nulio iki paleidimo“

Darbų failas. Čia surašyta, kas gide bus, kaip kiekvienas skyrius rašomas ir tikrinamas, ir kas dar liko iki paleidimo. Atnaujinama po kiekvieno skyriaus.

Aplankas `_content/` į svetainę nepatenka. Repozitorija vieša, todėl failai matomi GitHub'e.

---

## 1. Kryptis

**Nemokamas gidas moko technologijų, ne verslo.** Vienas konkretus projektas nuo pradžios iki galo: svetainė, sukurta su Claude Code, laikoma GitHub ir paleista per Vercel. Gido pabaigoje skaitytojas turi veikiančią svetainę savo domene ir supranta, kaip ji veikia.

Gidas nemoko, kaip atsirinkti ar patikrinti verslo idėją. Jis moko: kaip veikia svetainė, kokius įrankius rinktis ir kodėl, kaip dirbti su AI programavimo agentu, kokie darbo būdai veikia, kaip paleisti ir patikrinti kokybę bei saugumą.

**Kam:** žmogui, kuris nori pats susikurti svetainę su AI, bet nemoka programuoti ir nežino, nuo ko pradėti.

**Mokami gidai** (vėliau, jei nemokamas pasiteisins), po vieną projekto tipą:
1. Web aplikacija su prisijungimu ir duomenų baze (Supabase, teisės, RLS).
2. AI įrankis: chatbot'as ar asistentas su AI API, žinių baze ir kainų kontrole.
3. Mobilioji programėlė (Expo / React Native) ir publikavimas parduotuvėse.
4. Vidinis verslo įrankis: užsakymai, CRM, integracijos.

Pigesni priedai: CLAUDE.md šablonai, promptų rinkiniai, saugumo kontroliniai sąrašai.

## 2. Formatas

- **PDF**, A4, tas pats stilius kaip užduoties šablono PDF svetainėje. Planuojama 30–40 psl.
- **Notion versija** su kontroliniais sąrašais. Skelbiama iš Gabrielės Notion paskyros.
- **Kalba:** lietuvių, kreipiamasi „jūs“.
- **Pagrindinis įrankių rinkinys:** Claude Code, GitHub, Vercel.

## 3. Kaip rašomas kiekvienas skyrius

Po vieną skyrių. Kiekvienam:

1. **Analizė:** ko skaitytojui reikia šiame žingsnyje, kur dažniausiai suklystama.
2. **Šaltiniai:** kiekvienas faktas, kaina, komanda ar nustatymas tikrinamas oficialioje dokumentacijoje (MDN, Claude Code, GitHub, Vercel dokumentacija ir pan.). Puslapis atsidaromas ir perskaitomas, ne cituojamas iš paieškos. Kainos ir sąlygos žymimos tikrinimo data.
3. **Juodraštis** šiame aplanke (`NN-pavadinimas.md`) su šaltiniais ir faktų patikros lentele.
4. **Peržiūra** Claude Docs dokumente „Gidas: svetainė su AI (juodraštis)“ (https://claude.ai/artifact/RmEug4JxdAkFsKZDBoCPT8), Gabrielė komentuoja.
5. **Galutinis tekstas:** komentarai perkeliami į `.md` failą.

Komandos ir nustatymai (instaliavimas, Vercel, domenas) prieš maketuojant PDF dar kartą išbandomi realiame projekte.

## 4. Skyriai

| # | Skyrius | Būsena |
|---|---|---|
| 1 | Kaip veikia svetainė | juodraštis, laukia peržiūros |
| 2 | Įrankiai: Claude Code, GitHub, Vercel ir kodėl būtent jie | neparašytas |
| 3 | Pasiruošimas: paskyros, įdiegimas, projekto aprašymas AI | neparašytas |
| 4 | Kūrimas žingsnis po žingsnio | neparašytas |
| 5 | Darbo būdai ir dažnos klaidos | neparašytas |
| 6 | Paleidimas: Vercel, domenas, forma, SEO pagrindai | neparašytas |
| 7 | Kokybė ir saugumas | neparašytas |
| 8 | Kas toliau: kai reikia daugiau nei svetainės | neparašytas |

### 1. Kaip veikia svetainė
- Kas vyksta, kai atidarote svetainę (DNS, HTTP, serveris, naršyklė).
- HTML, CSS, JavaScript: kas už ką atsakingas.
- Statinė ir dinaminė svetainė; frontend, backend, duomenų bazė.
- Kur gyvena svetainė: kodas (GitHub), talpinimas (Vercel), domenas (.lt).
- Svetainė, web aplikacija ar PWA: kada užtenka svetainės.
- Ką sukursime šiame gide.

### 2. Įrankiai
- Dvi įrankių grupės: naršyklės kūrimo įrankiai (Lovable, Bolt, v0) ir AI programavimo agentai (Claude Code, Cursor). Kuo skiriasi, kada ką rinktis.
- Kodėl šiame gide Claude Code: tikras kodas jūsų kompiuteryje, nepriklausomybė nuo platformos.
- Ko reikės: Claude prenumerata, GitHub paskyra, Vercel paskyra. Kainos su tikrinimo data.
- Svetainės karkasas: paprastas HTML ar karkasas (pvz. Astro, Next.js). Sprendimas ir priežastys.
- AI ribos: saugumo tyrimai (Veracode 2025), Lovable incidentas (CVE-2025-48757). Medžiaga perkeliama iš archyvo.

### 3. Pasiruošimas
- Paskyros: GitHub, Vercel, Claude.
- Įdiegimas: Claude Code (pagal oficialią instrukciją), Git, kodo redaktorius.
- Svetainės aprašymas AI: puslapių sąrašas, turinys, stilius, pavyzdžiai. Iš archyvo perkeliama techninė planavimo dalis (puslapiai, apimtis, kas būtina pirmai versijai).
- Instrukcijų failas CLAUDE.md: kas tai, ką į jį rašyti, pavyzdys.

### 4. Kūrimas žingsnis po žingsnio
- Pirmas promptas ir pirmas paleidimas savo kompiuteryje.
- Kaip prašyti pakeitimų, kaip duoti dizaino pavyzdį ar eskizą.
- Kaip patikrinti, ką AI padarė.
- Git: išsaugojimas (commit), istorija, grįžimas atgal, GitHub.

### 5. Darbo būdai ir dažnos klaidos
- Užduočių skaidymas, plano režimas, kontekstas.
- Kai AI užstringa, sukasi ratu ar sugadina tai, kas veikė.
- Testavimas: telefone, skirtingose naršyklėse.

### 6. Paleidimas
- Vercel: projekto prijungimas iš GitHub, automatinis atnaujinimas.
- Svarbu: Vercel nemokamas planas skirtas tik nekomerciniam naudojimui. Verslo svetainei – Pro planas arba alternatyvos (Netlify, Cloudflare Pages). Galutinis sprendimas, kaip tai pateikti gide, laukia Gabrielės.
- .lt domenas: registracija per akredituotą paslaugų teikėją, DNS įrašai Vercel.
- Kontaktų forma statinėje svetainėje.
- SEO pagrindai: pavadinimai, aprašymai, sitemap, Google Search Console.
- Analitika.

### 7. Kokybė ir saugumas
- Greitis ir kokybė: Lighthouse / PageSpeed Insights.
- Prieinamumas.
- Slapti raktai, formų apsauga nuo šlamšto, priklausomybės.
- Privatumas: slapukai, privatumo politika.

### 8. Kas toliau
- Kai reikia prisijungimo, duomenų bazės, mokėjimų: kuo tai keičia architektūrą.
- Web aplikacija ar PWA ar mobilioji programėlė (medžiaga iš archyvo).
- Mokami gidai ir kada verta kreiptis į programuotoją.

## 5. Kas dar reikalinga paleidimui

| Darbas | Kas daro | Būsena |
|---|---|---|
| Gido skyriai 1–8 | Claude rašo, Gabrielė peržiūri | 1 juodraštis |
| Pavyzdinis projektas, kuriuo išbandomi visi žingsniai | Claude | nepradėta |
| PDF maketas | Claude | nepradėta |
| Notion versija | Claude paruošia, Gabrielė įkelia | nepradėta |
| Gido puslapis svetainėje su el. pašto forma | Claude | nepradėta |
| MailerLite paskyra, domeno patvirtinimas, automatinis laiškas | Gabrielė, Claude veda | nepradėta |
| Privatumo politika svetainėje | Claude juodraštis, Gabrielė patikrina | nepradėta |

## 6. Kaip matuosime

- Atsisiuntimų skaičius per mėnesį (MailerLite).
- Laiškų atidarymai ir paspaudimai.
- Kiek atsisiuntusių tampa užklausomis.
- Po 2–3 mėnesių: jei atsisiuntimų yra bent kelios dešimtys per mėnesį, kuriamas pirmas mokamas gidas.

## 7. Atviri klausimai Gabrielei

1. Vercel nemokamas planas tik nekomerciniam naudojimui. Kaip pateikiam verslo svetainėms: Vercel Pro (20 USD/mėn.), ar rodom Netlify / Cloudflare Pages kaip nemokamą alternatyvą?
2. Ar turi realų pavyzdį, ką sukūrei su Claude Code ir kiek laiko tai užtruko? (4–5 skyriams)
3. Kokias dažniausias klaidas esi mačiusi AI sukurtose svetainėse ar programėlėse? (5 ir 7 skyriams)
4. Ar gidas pasirašytas tavo vardu („Gabrielė Tamaševičiūtė, Codeart“), ar tik „Codeart“?

## 8. Archyvas

`archyvas/` aplanke – pirmos krypties (idėjos ir verslo planavimas) skyriai. Iš jų perkeliama: web / PWA / mobiliosios palyginimas (8 skyrius), AI saugumo tyrimai (2 skyrius), puslapių ir apimties planavimas (3 skyrius).
