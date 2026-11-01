# 2. Planas: nuo idėjos iki pirmos versijos aprašymo

AI įrankis sukuria tai, ką aprašote. Jei aprašymas miglotas, gausite miglotą programėlę, o paskui ilgai ją taisysite pokalbiais „ne, ne taip“. Valanda, skirta planui, sutaupo daug valandų perdarinėjimo.

Planas svarbus ir dėl kitos priežasties. CB Insights išnagrinėjo 111 žlugusių startuolių istorijų: 35 % jų nurodė, kad jų produkto rinkai tiesiog nereikėjo [1]. Geras planas yra ir būdas patikrinti, ar jūsų produkto reikia, dar prieš jį kuriant.

Šiame skyriuje, remdamiesi 1 skyriaus idėjos kortele, sudarysite:

1. vartotojų ir jų scenarijų sąrašą;
2. pirmos versijos (MVP) apimtį;
3. ekranų ir duomenų sąrašą;
4. planą, kaip patikrinsite, ar idėja pasiteisino.

Visą skyrių lydės vienas pavyzdys: **programėlė pradedantiesiems fotografams**, kurioje jie gauna trumpas užduotis, įkelia nuotraukas ir gauna AI atsiliepimą.

---

## 2.1. Kas naudosis ir ką jie darys

### Vartotojų tipai

Pirmiausia išvardykite, kas naudosis programėle. Ne „visi“, o konkrečios grupės, kurios programėlėje daro skirtingus dalykus.

Pavyzdyje jų yra du:

- **Mokinys:** atlieka užduotis, įkelia nuotraukas, skaito atsiliepimus.
- **Administratorius** (jūs): kuria užduotis ir mato, kas vyksta.

Kiekvienas papildomas tipas (pvz. mokytojas, kuris pats vertina darbus) beveik padvigubina darbą, nes reikia atskirų ekranų ir teisių. Todėl pirmai versijai pasilikite tik tuos, be kurių programėlė neveiktų.

### Scenarijai

Dabar aprašykite, ką kiekvienas vartotojas darys. Patogiausia tai daryti trumpais sakiniais pagal šabloną, kurį programuotojai naudoja nuo 2001 m. [2]:

> Kaip **[vartotojas]** noriu **[ką padaryti]**, kad **[kokia nauda]**.

Pavyzdžiai:

1. Kaip mokinys noriu matyti šios savaitės užduotį, kad žinočiau, ką fotografuoti.
2. Kaip mokinys noriu įkelti nuotrauką iš telefono, kad galėčiau ją pateikti.
3. Kaip mokinys noriu gauti atsiliepimą apie kompoziciją ir šviesą, kad žinočiau, ką daryti geriau.
4. Kaip mokinys noriu matyti savo ankstesnes nuotraukas, kad matyčiau, kaip tobulėju.
5. Kaip administratorius noriu sukurti naują užduotį, kad mokiniai turėtų ką daryti kitą savaitę.

Dalis „kad…“ svarbesnė, nei atrodo. Ji primena, **kodėl** funkcija reikalinga, ir padeda vėliau nuspręsti, ar ji tikrai būtina.

Užrašykite 5–15 scenarijų. Jei jų daugiau nei 20, idėja per didelė pirmai versijai, ir tai išspręsite kitame žingsnyje.

---

## 2.2. MVP: kas būtina pirmai versijai

### Kas yra MVP

MVP (angl. *minimum viable product*) dažnai verčiamas „mažiausias perspektyvus produktas“. Sąvoką išpopuliarinęs Eric Ries ją apibrėžia kaip tokią produkto versiją, kuri leidžia sužinoti daugiausia apie vartotojus įdėjus mažiausiai pastangų [3].

Svarbiausias žodis čia yra „sužinoti“. MVP nėra apkarpyta galutinio produkto versija. Tai bandymas, kuris turi atsakyti į klausimą: ar žmonės tuo naudosis?

### Kaip atrinkti funkcijas

Paprasčiausias būdas yra MoSCoW metodas, kurį 1994 m. sukūrė Dai Clegg ir kuris iki šiol naudojamas projektų valdyme [4]. Kiekvieną scenarijų priskirkite vienai iš keturių grupių:

| Grupė | Reikšmė | Pavyzdys |
|---|---|---|
| **Būtina** (Must) | be šito programėlė neteikia pagrindinės vertės | matyti užduotį, įkelti nuotrauką, gauti AI atsiliepimą |
| **Svarbu** (Should) | labai praverstų, bet galima apsieiti kelias savaites | ankstesnių nuotraukų istorija |
| **Būtų gerai** (Could) | malonus priedas | pasidalinti nuotrauka su draugais, ženkleliai už atliktas užduotis |
| **Ne šį kartą** (Won't) | sąmoningai atidedama | mokėjimai, mokytojų paskyros, programėlė App Store |

Pirmoje versijoje kuriate **tik „Būtina“**. Viskam kitam užtenka tikrinimo klausimo:

> Jei šios funkcijos nebūtų, ar žmogus vis tiek gautų tai, dėl ko atėjo?

Jei taip, funkcija ne pirmai versijai.

### Ko dažniausiai nereikia pirmai versijai

- **Mokėjimų.** Pirmus mokančius vartotojus galima aptarnauti sąskaita ar banko pavedimu.
- **Kelių prisijungimo būdų.** Užtenka vieno, pavyzdžiui, el. pašto.
- **Kelių kalbų.** Pradėkite nuo tos, kuria kalba jūsų pirmi vartotojai.
- **Sudėtingo administravimo.** Iš pradžių duomenis galite tvarkyti tiesiai duomenų bazėje ar lentelėje.
- **Pranešimų, ženklelių, socialinių funkcijų.** Jos padeda išlaikyti vartotojus, bet tik tada, kai jie jau naudojasi.

### MVP gali būti ir be kodo

Kartais idėją galima patikrinti dar nieko nekūrus. Žinomiausias pavyzdys yra Dropbox: kol produktas dar nebuvo paruoštas, įkūrėjas Drew Houston paskelbė trumpą vaizdo įrašą, kuriame parodė, kaip jis veiks. Po vaizdo įrašo laukiančiųjų sąrašas išaugo nuo 5 000 iki 75 000 žmonių per naktį [5].

Panašūs būdai:

- **Puslapis su registracija.** Aprašote produktą ir kviečiate užsiregistruoti. Registracijų skaičius parodo susidomėjimą.
- **Rankinis variantas.** Pirmiems vartotojams paslaugą atliekate patys. Pavyzdyje: mokiniai siunčia nuotraukas el. paštu, o atsiliepimą rašote su AI pagalba rankomis. Jei per mėnesį niekas nesiunčia, programėlės nereikėjo.

---

## 2.3. Ekranai ir duomenys

### Ekranų sąrašas

Iš „Būtina“ scenarijų sudarykite ekranų sąrašą. Pavyzdyje jų užtenka šešių:

1. Prisijungimas ir registracija.
2. Šios savaitės užduotis.
3. Nuotraukos įkėlimas.
4. Atsiliepimas apie nuotrauką.
5. Mano nuotraukos (jei „Svarbu“ funkcija patenka į pirmą versiją).
6. Administratoriaus: užduočių sąrašas ir naujos užduoties kūrimas.

Kiekvieną ekraną nupieškite ant popieriaus: kas jame matosi ir kur galima paspausti. Gražumas nesvarbus. Svarbu, kad pamatytumėte, ar vartotojas gali nueiti nuo pirmo iki paskutinio žingsnio. Eskizo nuotrauka pravers ir rašant užduotis AI įrankiui (apie tai 4 skyriuje).

### Duomenys

Kiekviena programėlė kažką saugo. Užrašykite, ką, paprastais žodžiais. Pavyzdyje:

| Kas saugoma | Kokia informacija | Ar tai asmens duomenys? |
|---|---|---|
| Vartotojas | vardas, el. paštas, slaptažodis, rolė (mokinys ar administratorius) | taip |
| Užduotis | pavadinimas, aprašymas, savaitė | ne |
| Nuotrauka | failas, kas įkėlė, kuriai užduočiai, kada | taip (vartotojo darbas, gali būti matomi žmonės) |
| Atsiliepimas | tekstas, kuriai nuotraukai, kada sukurtas | susijęs su vartotoju |

Ir ryšiai tarp jų, irgi paprastai:

- vienas vartotojas gali įkelti daug nuotraukų;
- kiekviena nuotrauka priklauso vienai užduočiai;
- kiekviena nuotrauka turi vieną atsiliepimą.

Ši lentelė yra viena svarbiausių viso plano dalių. Pagal ją AI įrankis sukurs duomenų bazę, o stulpelis „Ar tai asmens duomenys?“ pravers 5 skyriuje, kai tikrinsite saugumą ir BDAR reikalavimus.

---

## 2.4. Kaip patikrinsite, ar pasiteisino

### Pasikalbėkite prieš kurdami

Parodykite planą 3–5 žmonėms, kuriems programėlė skirta. Bet neklauskite „ar naudotumėte?“: į tokį klausimą žmonės dažniausiai mandagiai atsako „taip“.

Knygoje „The Mom Test“ Rob Fitzpatrick siūlo tris taisykles [6]:

1. **Kalbėkite apie jų gyvenimą, ne apie savo idėją.**
2. **Klauskite apie konkrečius praeities atvejus, ne apie ateitį.** Ne „ar mokytumėtės su tokia programėle?“, o „kada paskutinį kartą bandėte tobulinti fotografavimą? Ką darėte?“
3. **Daugiau klausykite nei kalbėkite.**

Jei pokalbiuose niekas neprisimena, kad problema jiems būtų rūpėjusi, tai vertinga žinia. Geriau ją sužinoti dabar.

### Iš anksto nuspręskite, kas yra sėkmė

Prieš paleisdami pirmą versiją užsirašykite, koks rezultatas reikš, kad verta tęsti. Pavyzdžiui:

> Per 4 savaites bent 15 žmonių įkels bent po 3 nuotraukas.

Skaičius užsirašykite **prieš** paleidimą. Po paleidimo bet koks rezultatas atrodo „neblogas“, ir sunku sąžiningai nuspręsti, ar tęsti.

---

## Užduotis: pirmos versijos planas

Užpildykite šabloną. Jis bus jūsų pagrindinis dokumentas 4 skyriuje, kai kursite su AI, ir 7 skyriuje, jei perduosite projektą programuotojui.

| Dalis | Jūsų atsakymas |
|---|---|
| **Vertės sakinys** (iš 1 skyriaus) | |
| **Vartotojų tipai** ir ką kiekvienas daro | |
| **Scenarijai** („Kaip … noriu …, kad …“), 5–15 | |
| **Būtina** pirmai versijai | |
| **Vėliau** (Svarbu, Būtų gerai, Ne šį kartą) | |
| **Ekranai** (sąrašas ir eskizai) | |
| **Duomenys** (kas saugoma, ar tai asmens duomenys) | |
| **Kaip patikrinsiu prieš kurdamas** (su kuo kalbėsiu) | |
| **Sėkmės kriterijus** (skaičius ir terminas) | |

Jei vėliau kreipsitės į programuotoją, šis planas atitinka ir mūsų [užduoties programuotojui šabloną](https://codeart.lt/lt/straipsniai/uzduotis-programuotojui.html).

## Skyriaus kontrolinis sąrašas

- [ ] Išvardijau vartotojų tipus ir palikau tik būtinus.
- [ ] Užrašiau 5–15 scenarijų „Kaip … noriu …, kad …“.
- [ ] Suskirsčiau juos į Būtina, Svarbu, Būtų gerai ir Ne šį kartą.
- [ ] Turiu ekranų sąrašą ir eskizus ant popieriaus.
- [ ] Turiu duomenų lentelę ir pažymėjau asmens duomenis.
- [ ] Pasikalbėjau su bent 3 būsimais vartotojais.
- [ ] Užsirašiau sėkmės kriterijų su skaičiumi ir terminu.

---

## Šaltiniai

1. CB Insights, „The Top 12 Reasons Startups Fail“ (2021 m. atnaujinimas, 111 startuolių istorijų). https://www.cbinsights.com/research/report/startup-failure-reasons-top/ (adresas neatidarytas; skaičiai patikrinti per antrinius šaltinius, žr. lentelę)
2. Agile Alliance, „User Story“ (Connextra formatas „As a … I want … so that …“, 2001). https://www.agilealliance.org/glossary/user-story/
3. Eric Ries, „Minimum Viable Product: a guide“, 2009; „The Lean Startup“, 2011. Apibrėžimas: „that version of a new product which allows a team to collect the maximum amount of validated learning about customers with the least effort“. Cituojama pagal https://en.wikipedia.org/wiki/Minimum_viable_product
4. Wikipedia, „MoSCoW method“ (Dai Clegg, Oracle UK, 1994, DSDM). https://en.wikipedia.org/wiki/MoSCoW_method ; Agile Business Consortium, „Mastering MoSCoW Prioritisation“. https://www.agilebusiness.org/resource/video-mastering-moscow-prioritisation.html
5. TechCrunch, „(Founder Stories) How Dropbox Got Its First 10 Million Users“, 2011-11-01. https://techcrunch.com/2011/11/01/founder-storie-how-dropbox-got-its-first-10-million-users/
6. Rob Fitzpatrick, „The Mom Test“, 2013. Trijų taisyklių santrauka: https://www.sachinrekhi.com/the-mom-test-rob-fitzpatrick

### Faktų patikra

| Faktas | Šaltinis | Kaip patikrinta | Data |
|---|---|---|---|
| 35 % žlugusių startuolių nurodė „rinkai nereikėjo“ (111 istorijų, 2021) | [1] | keli antriniai šaltiniai sutampa; CB Insights puslapio atidaryti nepavyko. Senesnėje versijoje (apie 101 istorija) buvo 42 %, todėl internete dažnai cituojamas tas skaičius | 2026-11-01 |
| Vartotojo istorijos formatas sukurtas Connextra komandoje 2001 m. | [2] | paieška cituoja Agile Alliance ir Wikipedia | 2026-11-01 |
| Eric Ries MVP apibrėžimas | [3] | keli šaltiniai cituoja tą pačią formuluotę; originalios knygos neatidaryta | 2026-11-01 |
| MoSCoW: Dai Clegg, 1994, DSDM | [4] | keli šaltiniai sutampa; oficialus Agile Business Consortium puslapis mokamas | 2026-11-01 |
| Dropbox: nuo 5 000 iki 75 000 per naktį | [5] | paieška cituoja TechCrunch ir Houston citatą; TechCrunch atidaryti nepavyko | 2026-11-01 |
| „The Mom Test“ trys taisyklės | [6] | keli knygos santraukų šaltiniai sutampa | 2026-11-01 |

Prieš maketuojant PDF: atsidaryti [1], [4], [5] tiesiogiai. Šios darbo sesijos tinklas neleidžia atidaryti cbinsights.com, techcrunch.com ir wikipedia.org.
