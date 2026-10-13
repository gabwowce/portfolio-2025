# Informacijos rinkimas apie projektus

Kiekvienam projektui (lojalumo sistema, kalbų platforma, TikMaker) reikia dviejų dalių:

- **A. Iš kodo:** paleisk žemiau esantį promptą Claude Code, atidarytame to projekto repozitorijoje.
- **B. Iš tavęs:** atsakymai į klausimus, kurių kode nėra.

Abi dalis atsiųsk man, ir aš iš jų sudėliosiu galutinius tekstus dizainui.

---

## A. Promptas Claude Code (paleisti kiekvieno projekto repozitorijoje)

```
Išanalizuok šį projektą ir parašyk jo aprašymą mano portfolio svetainei. Rašyk lietuviškai.

Taisyklės:
- Rašyk tik tai, ką gali patvirtinti kodu. Prie kiekvieno teiginio, kurio nesi tikras, rašyk [PATIKRINTI].
- Nieko neišsigalvok: jokių naudotojų skaičių, verslo rezultatų ar procentų, kurių nėra kode.
- Neįtrauk slaptažodžių, raktų, vidinių URL, klientų duomenų ir asmenų vardų.
- Kalba paprasta: „Kas tai“ ir sekcijų įžangos turi būti suprantamos verslo žmogui, techninė dalis – programuotojui.

Pateik būtent tokia struktūra:

1. KAS TAI (2 sakiniai): kokia tai sistema, kam ji skirta ir kokią problemą sprendžia.

2. NAUDOTOJŲ TIPAI: kas naudojasi sistema (pvz. administratorius, mokinys, vadybininkas) ir ką kiekvienas joje daro.

3. PAGRINDINĖS SRITYS: visi moduliai / puslapiai, sugrupuoti į sritis. Prie kiekvienos srities: 1 sakinys ir maršrutų / ekranų sąrašas.

4. TRYS STIPRIAUSIOS DALYS portfolio puslapiui. Pasirink 3 sritis, kurios geriausiai parodo sudėtingumą ar naudą. Prie kiekvienos:
   - antraštė (2–4 žodžiai);
   - įžanga (1–2 sakiniai, verslo kalba);
   - 3–5 punktai: ką konkrečiai galima daryti;
   - kokią ekrano kopiją daryti (kuris puslapis, kokia būsena, kas turi matytis).

5. TECHNINIAI SPRENDIMAI: 3–5 įdomiausi sprendimai, kurie parodo kompetenciją (architektūra, duomenų srautai, būsenos valdymas, API sluoksnis, našumas, prieinamumas, testai, i18n, autentifikacija ir teisės, automatika). Prie kiekvieno: kas padaryta, kodėl tai svarbu, ir failas / aplankas, kuriame tai matosi.

6. MASTAS (tik suskaičiuoti skaičiai, nurodyk, kaip skaičiavai):
   - maršrutų / puslapių skaičius;
   - API endpointų skaičius (jei yra backend arba API klientas);
   - duomenų bazės lentelių / modelių skaičius;
   - komponentų skaičius;
   - kalbų ir vertimo raktų skaičius;
   - testų skaičius;
   - commit'ų skaičius ir pirmo bei paskutinio commit'o datos (git log).

7. STACKAS: pagrindinės technologijos iš package.json ar kitų priklausomybių failų, sugrupuotos: frontend, backend, duomenų bazė, infrastruktūra, išorinės paslaugos (AI, mokėjimai, el. paštas ir pan.). Tik tai, kas realiai naudojama kode.

8. AUTORYSTĖ (iš git log): kiek commit'ų mano (Gabrielė / gabwowce) ir kiek kitų autorių, kurias projekto dalis daugiausia keičiau aš.
```

---

## B. Klausimai tau (kode šito nėra)

Atsakyk trumpai, po 1–2 sakinius.

**Apie projektą**
1. Kam sukurta: klientui, darbdaviui (UVS ar kt.), sau?
2. Ar galiu viešai minėti kliento / įmonės pavadinimą? Ar galima rodyti logotipą ir tikrus duomenis, ar reikia juos uždengti?
3. Metai: nuo kada iki kada dirbai prie projekto?
4. Būsena dabar: veikia produkcijoje, kuriama, MVP, vidinis įrankis?
5. Ar yra viešai pasiekiama nuoroda (live demo, GitHub)?

**Tavo rolė**
6. Ar dirbai viena, ar komandoje? Jei komandoje, kas dar dirbo (be vardų, tik rolės: backend programuotojas, dizaineris ir pan.)?
7. Už ką buvai atsakinga tu: dizainas, frontend, backend, duomenų bazė, diegimas, bendravimas su klientu?
8. Ar dizainą kūrei pati, ar gavai iš dizainerio?

**Problema ir rezultatas**
9. Kaip tai buvo daroma prieš šią sistemą? (Excel, popierius, kita sistema, rankiniu būdu?)
10. Kas pasikeitė, kai sistema pradėjo veikti? Jei turi realų skaičių (sutaupytas laikas, naudotojų skaičius, užsakymų skaičius), parašyk jį. Jei neturi, parašyk tiesiog, kas pagerėjo.
11. Kuo šis projektas buvo sunkiausias ir kaip tai išsprendei? (Tai bus įdomiausia dalis darbdaviui.)
12. Ką darytum kitaip, jei darytum iš naujo? (Neprivaloma, bet darbdaviams tai patinka.)

**Ekrano kopijos**
13. Padaryk 3–4 ekrano kopijas pagal A dalies 4 punkto pasiūlymus:
    - naršyklės langas 1440 px pločio, be naršyklės juostų ir žymių;
    - šviesi tema (jei sistema turi abi);
    - su realistiškais, bet ne tikrais duomenimis, arba su uždengtais duomenimis;
    - PNG formatu (aš paversiu į WebP).
