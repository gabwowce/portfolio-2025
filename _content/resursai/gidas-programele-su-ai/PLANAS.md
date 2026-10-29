# Gidas „Kaip susikurti programėlę su AI: nuo idėjos iki paleidimo“

Darbų failas. Čia surašyta, kas gide bus, kaip kiekvienas skyrius rašomas ir tikrinamas, ir kas dar liko padaryti iki paleidimo. Atnaujinama po kiekvieno skyriaus.

Aplankas `_content/` į svetainę nepatenka, todėl juodraščiai čia nematomi lankytojams.

---

## 1. Tikslas ir skaitytojas

**Kam:** žmogui, turinčiam idėją programėlei ar vidiniam verslo įrankiui, bet nemokančiam programuoti (arba mokančiam nedaug). Smulkus verslas, startuolio idėja, specialistas, kuris nori įrankio sau.

**Ką skaitytojas gaus:** aiškų kelią nuo idėjos iki veikiančios pirmos versijos su AI įrankiais, nesudegindamas pinigų ir nepalikdamas saugumo spragų. Ir supratimą, kada laikas perduoti projektą programuotojui.

**Ką gausime mes:**
- el. pašto adresus žmonių, kurie galvoja apie programėlę (MailerLite);
- pasitikėjimą: gidas parodo, kad suprantame ir AI įrankius, ir jų ribas;
- natūralų kelią į paslaugą (5 ir 7 skyriai).

**Kuo skirsis nuo kursų** (CodeAcademy, Vilnius Coding, Ponas Obuolys): nemokamas, lietuviškai, praktinis, parašytas programuotojos, kuri pati kuria su AI ir mato, kur AI sukurtos programėlės lūžta.

## 2. Formatas

- **PDF**, A4, tas pats stilius kaip užduoties šablono PDF (Schibsted Grotesk, Codeart spalvos). Planuojama apimtis 25–35 psl.
- **Notion versija**: tas pats turinys ir užpildomi šablonai. Skelbiama iš Gabrielės Notion paskyros kaip viešas „Duplicate“ šablonas.
- **Kalba:** lietuvių. Kreipiamasi „jūs“, kaip svetainėje.
- **Autorius:** dar nenuspręsta (žr. 7 punktą).

## 3. Kaip rašomas kiekvienas skyrius

Po vieną skyrių, ne visą gidą iš karto. Kiekvienam skyriui:

1. **Analizė.** Ko skaitytojui reikia šiame žingsnyje, kokie klausimai, kokios dažnos klaidos.
2. **Šaltiniai.** Kiekvienas faktas, skaičius, kaina ar data turi šaltinį. Pirmenybė oficialiems puslapiams (Apple, Google, įrankių dokumentacija) ir tyrimams. Antriniai šaltiniai (tinklaraščiai, žiniasklaida) žymimi kaip antriniai.
3. **Juodraštis** šiame aplanke (`NN-pavadinimas.md`), su šaltinių sąrašu skyriaus gale.
4. **Faktų patikra.** Šaltinių lentelė skyriaus faile: kas patvirtinta, iš kur, kada tikrinta.
5. **Peržiūra.** Skyrius keliamas į Claude Docs dokumentą, Gabrielė komentuoja.
6. **Galutinis tekstas.** Komentarai perkeliami į `.md` failą, skyrius pažymimas „baigtas“.

Pastaba apie šaltinius: šios darbo sesijos tinklas neleidžia atidaryti kai kurių svetainių (pvz. support.google.com, webkit.org, veracode.com). Tokiais atvejais faktas patikrintas per paiešką, kuri cituoja oficialų puslapį, o skyriaus šaltinių lentelėje tai pažymėta. Prieš maketuojant PDF šiuos šaltinius reikia atsidaryti ir patikrinti dar kartą.

## 4. Skyriai

| # | Skyrius | Būsena |
|---|---|---|
| 1 | Prieš pradedant: ar jums tikrai reikia programėlės | juodraštis, laukia peržiūros |
| 2 | Planas: problema, vartotojas, MVP | neparašytas |
| 3 | Įrankiai: kurį rinktis | neparašytas |
| 4 | Kūrimas žingsnis po žingsnio | neparašytas |
| 5 | Saugumas ir kokybė prieš paleidžiant | neparašytas |
| 6 | Paleidimas | neparašytas |
| 7 | Kada perduoti programuotojui | neparašytas |
| – | Priedai: plano šablonas, promptų pavyzdžiai, saugumo kontrolinis sąrašas | neparašyti |

### 1. Prieš pradedant
- Ar idėjai išvis reikia programėlės, ar užtenka gatavo įrankio.
- Web aplikacija, PWA ar mobilioji programėlė: skirtumai, parduotuvių mokesčiai ir taisyklės.
- Ko realiai tikėtis iš AI įrankių: ką jie daro gerai, kur klysta (saugumo tyrimai, realūs incidentai).
- Užduotis: idėjos kortelė.

### 2. Planas
- Problema ir vartotojas vienu sakiniu.
- Vartotojo scenarijai (kas, ką, kodėl).
- MVP: kas būtina pirmai versijai, kas palauks. Kaip atskirti.
- Ekranų sąrašas ir duomenys, kuriuos programėlė saugos.
- Užpildomas plano šablonas (siejasi su svetainės užduoties šablonu).
- Reikės šaltinių: MVP sąvoka, tyrimai apie startuolių nesėkmių priežastis (pvz. CB Insights), jei bus naudojami.

### 3. Įrankiai
- Dvi grupės: naršyklėje veikiantys kūrimo įrankiai (Lovable, Bolt, v0) ir programavimo asistentai (Cursor, Claude Code ir pan.).
- Kam kuris tinka, kokias technologijas generuoja, ar galima pasiimti kodą, kainos.
- Rekomendacija pradedančiajam.
- Reikės šaltinių: kiekvieno įrankio oficiali kainų ir dokumentacijos svetainė, tikrinta rašymo dieną (kainos keičiasi dažnai, todėl skyriuje bus data).

### 4. Kūrimas
- Kaip rašyti užduotis AI (promptus), su lietuviškais pavyzdžiais.
- Duomenų bazė ir prisijungimas (Supabase pavyzdžiu).
- Kaip neprarasti darbo: versijos, GitHub.
- Ką daryti, kai AI „užstringa“ ar sugadina tai, kas veikė.
- Reikės šaltinių: Supabase ir pasirinktų įrankių dokumentacija.

### 5. Saugumas ir kokybė
- Dažniausios AI sukurtų programėlių spragos: duomenų bazės teisės (RLS), atviri raktai, prisijungimas.
- Asmens duomenys ir BDAR mažai programėlei.
- Kontrolinis sąrašas prieš paleidžiant.
- Reikės šaltinių: OWASP Top 10, Supabase RLS dokumentacija, VDAI / BDAR šaltiniai, incidentų aprašymai.

### 6. Paleidimas
- Domenas, talpinimas, analitika.
- Teisiniai minimumai: privatumo politika, slapukai.
- Pirmi vartotojai ir grįžtamasis ryšys.
- Reikės šaltinių: talpinimo paslaugų kainos, ePrivacy / slapukų reikalavimai Lietuvoje.

### 7. Kada perduoti programuotojui
- Ženklai, kad laikas.
- Kaip paruošti perdavimą (kodas, prieigos, aprašymas), kad nereikėtų pradėti iš naujo.
- Ką klausti programuotojo prieš pasirenkant.
- Natūralus kvietimas į Codeart.

## 5. Kas dar reikalinga paleidimui

| Darbas | Kas daro | Būsena |
|---|---|---|
| Gido skyriai 1–7 ir priedai | Claude rašo, Gabrielė peržiūri | 1 skyrius juodraštis |
| PDF maketas | Claude | nepradėta |
| Notion versija | Claude paruošia tekstą, Gabrielė įkelia į savo Notion | nepradėta |
| Gido puslapis svetainėje (`/lt/resursai/…`) su el. pašto forma | Claude | nepradėta |
| MailerLite paskyra, domeno patvirtinimas (DNS), automatinis laiškas | Gabrielė, Claude veda žingsnis po žingsnio | nepradėta |
| Privatumo politika svetainėje | Claude parašo juodraštį, Gabrielė patikrina | nepradėta |

## 6. Kaip matuosime

- Atsisiuntimų skaičius per mėnesį (MailerLite).
- Kiek atsisiuntusių atsidaro laiškus ir spaudžia nuorodas.
- Kiek iš jų tampa užklausomis.
- Sprendimas po 2–3 mėnesių: jei atsisiuntimų yra bent kelios dešimtys per mėnesį, verta kurti mokamą versiją.

## 7. Atviri klausimai Gabrielei

1. Kokius AI įrankius naudoji pati ir kuriuos rekomenduotum pradedančiajam? (reikia 3 skyriui)
2. Ar turi realų pavyzdį, ką sukūrei su AI ir kiek laiko tai užtruko? (4 skyriui)
3. Kokias dažniausias AI sukurtų programėlių klaidas esi mačiusi? (5 skyriui)
4. Ar gidas pasirašytas tavo vardu („Gabrielė Tamaševičiūtė, Codeart“), ar tik „Codeart“?
5. Kreipinys: „jūs“ (kaip svetainėje) ar „tu“ (draugiškiau gidui)?
