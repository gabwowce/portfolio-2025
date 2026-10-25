# Tekstų auditas: iš „aš“ į „mes“

Tikslas: svetainė turi skambėti kaip studija, kuri dirba su klientu („kuriame“, „atsakome“), o ne kaip vienas programuotojas („kuriu“, „galiu“).

Visi tekstai yra trijose vietose:

- `tools/build-site.py`: pagrindinis, paslaugų, apie, kontaktų ir projektų puslapiai;
- `tools/services_content.py`: 4 paslaugų puslapiai;
- `_content/straipsniai/*.html`: straipsniai.

Eilučių numeriai nurodyti pagal dabartinę failų versiją. EN tekstuose daromi tie patys pakeitimai: I → we, my → our, me → us.

---

## Principai

1. **Klientui skirtuose puslapiuose rašome „mes“**: pagrindinis, paslaugos, kontaktai, DUK, straipsnių pabaigos su kvietimu susisiekti.
2. **Neišgalvojame faktų apie komandą.** Nerašome „10 specialistų komanda“ ar „5 metai rinkoje“. Pakanka sakinio, kuris yra tiesa: projektus veda įkūrėja, o pagal poreikį prisijungia kiti specialistai. Klaidinantys teiginiai apie verslą yra nesąžininga komercinė veikla, be to, klientas tai greitai pastebi.
3. **Gabrielė lieka matoma kaip įkūrėja.** Studijoms tai privalumas: klientas žino, kas atsakingas už jo projektą.
4. **CV puslapis lieka asmeninis.** Jis skirtas darbdaviams, todėl ten „aš“ yra tinkama forma.
5. **Moteriškos giminės formos** („negriaudama“, „viena“, „pati“, „programuotoja“) klientiniuose tekstuose keičiamos į „mes“ formas.

---

## 1. Visoje svetainėje

| Vieta | Dabar | Siūloma |
|---|---|---|
| `build-site.py:242` puslapio pavadinimas | …kūrimas \| Programuotoja Vilniuje | …kūrimas \| Codeart, Vilnius |
| `build-site.py:243` aprašymas paieškai | …Programuotoja Vilniuje. | …Codeart, Vilnius. |
| `build-site.py:320–321` EN | Developer in Vilnius | Codeart, Vilnius |
| `build-site.py:481, 496, 539` pavadinimų galūnė | \| Gabrielė Tamaševičiūtė · Codeart | \| Codeart |
| `build-site.py:1861` projektų pavadinimų galūnė | projektas \| Gabrielė Tamaševičiūtė | projektas \| Codeart |
| `build-site.py:465` apatinis kvietimas | Atsakau per 24 val. su darbų planu ir kaina. | Atsakome per 24 val. su darbų planu ir kaina. |
| `build-site.py:474` | Paprastai atsakau per 24 val. | Paprastai atsakome per 24 val. |
| `build-site.py:304` formos patvirtinimas | atsakysiu el. paštu. | atsakysime el. paštu. |
| `build-site.py:824` poraštė | © 2026 Gabrielė Tamaševičiūtė · Codeart | © 2026 Codeart |
| `build-site.py:1061` struktūriniai duomenys | Codeart — Gabrielė Tamaševičiūtė | Codeart (Gabrielė lieka kaip `founder`) |

**Poraštė.** Jei dirbi pagal individualią veiklą, savo vardą ir pavardę palik rekvizituose kontaktų puslapyje: klientas turi matyti, su kuo sudaro sutartį.

## 2. Pagrindinis puslapis

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:265` skyriaus antraštė | Su kuo galiu padėti | Su kuo galime padėti |
| `:476` įžanga | Kuriu nuo nulio, tobulinu esamas sistemas ir pridedu naujų funkcijų. | Kuriame sistemas nuo nulio, tobuliname esamas ir pridedame naujų funkcijų. |
| `:268` | Padedu išgryninti sprendimą, suprojektuoju sąsają ir sukuriu sistemą… | Padedame išgryninti sprendimą, suprojektuojame sąsają ir sukuriame sistemą… |
| `:270` | Pirmiausia randu, kur problema, tada tvarkau… | Pirmiausia randame, kur problema, tada tvarkome… |
| `:272` | Perprantu esamą kodą ir kuriu naujas funkcijas, negriaudama… | Perprantame esamą kodą ir kuriame naujas funkcijas, negriaudami… |
| `:279` žingsnis „Paleidimas“ | Įdiegiu sistemą ir paruošiu instrukcijas… Mano darbui taikoma 3 mėn. garantija. | Įdiegiame sistemą ir paruošiame instrukcijas… Darbams taikoma 3 mėn. garantija. |
| `:281` | Apie mane | Kas veda projektus *(arba „Apie mus“)* |
| `:283` | Esu Gabrielė. Man patinka kurti sistemas… | žr. pasiūlymą žemiau |
| `:285` | Daugiau apie mane → | Daugiau apie mus → |
| `:288` DUK | …per 24 val. atsiunčiu darbų planą… | …per 24 val. atsiunčiame darbų planą… |
| `:289` DUK | Tikslų terminą nurodau plane… | Tikslų terminą nurodome plane… |
| `:290` DUK | …galiu tęsti darbą su jūsų esama sistema… | …galime tęsti darbą su jūsų esama sistema… |
| `:291` DUK | Smulkius pageidavimus dažniausiai tiesiog įtraukiu: man svarbu… | Smulkius pageidavimus dažniausiai tiesiog įtraukiame: mums svarbu… |
| `:292` DUK | …galiu sukurti pokalbių asistentą… | …galime sukurti pokalbių asistentą… |
| `:293` DUK | Kartu su sistema paruošiu naudojimo instrukcijas… | Kartu su sistema paruošiame naudojimo instrukcijas… |
| `:296` | Paprastai atsakau per 24 val. | Paprastai atsakome per 24 val. |

**Bloko „Apie“ tekstas (`:283`):**

> Codeart kuria verslo sistemas ir web aplikacijas, kurios iš tikrųjų padeda: sutaupo laiko, sumažina chaosą ir leidžia susitelkti į tai, kas svarbu. Projektus veda įkūrėja Gabrielė Tamaševičiūtė, o pagal poreikį prisijungia patikrinti dizaino, backend ar mobiliųjų programėlių specialistai.

## 3. Paslaugų puslapis (`lt/services.html`)

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:484` H1 | Su kuo galiu padėti | Su kuo galime padėti |
| `:485` | …Padedu ją sukurti, sutvarkyti arba išplėsti. | …Padedame ją sukurti, sutvarkyti arba išplėsti. |
| `:486` | Ką darau | Ką darome |
| `:489` | Kiekvienam projektui pateikiu fiksuotą kainos pasiūlymą… | Kiekvienam projektui pateikiame fiksuotą kainos pasiūlymą… |
| `:490` | …dėl mano įgyvendinto sprendimo, ją ištaisau… | …dėl mūsų įgyvendinto sprendimo, ją ištaisome… |
| `:494` | 3 mėn. garantija mano darbui | 3 mėn. garantija atliktiems darbams |
| `:650` | Išgryninu sprendimą, suprojektuoju visą sistemą ir sukuriu ją… | Išgryniname sprendimą, suprojektuojame visą sistemą ir sukuriame ją… |
| `:651–653` | Išgryninu… / Suprojektuoju… / Sukuriu… | Išgryniname… / Suprojektuojame… / Sukuriame… |
| `:656` | Pirmiausia randu, kur problema, tada tvarkau… | Pirmiausia randame, kur problema, tada tvarkome… |
| `:657–659` | Randu… / Sutvarkau… ir pagerinu… / Neliečiu… | Randame… / Sutvarkome… ir pageriname… / Neliečiame… |
| `:662` | Perprantu esamą kodą ir kuriu…, negriaudama… | Perprantame esamą kodą ir kuriame…, negriaudami… |
| `:663–665` | Perprantu… / Kuriu… / Negriaunu… | Perprantame… / Kuriame… / Negriauname… |

## 4. Paslaugų puslapiai (`services_content.py`)

**Bendri visiems (`build-site.py:2070–2082`):**

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:2074` | Tikslų terminą nurodau plane… | Tikslų terminą nurodome plane… |
| `:2076` | …dėl mano įgyvendinto sprendimo, ją ištaisau nemokamai. | …dėl mūsų įgyvendinto sprendimo, ją ištaisome nemokamai. |
| `:2077` | Pavyzdys iš mano darbų | Pavyzdys iš mūsų darbų |
| `:2092` EN | I can build what isn't listed too. Tell me… | we can build what isn't listed too. Tell us… |

**Verslo sistemos:**

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:42` | …sukuriu vieną sistemą… | …sukuriame vieną sistemą… |
| `:49` | Sistemą kuriu būtent jūsų darbui. | Sistemą kuriame būtent jūsų darbui. |
| `:53` | Pavyzdžiui, galiu sukurti | Pavyzdžiui, galime sukurti *(taip pat `:136`, `:288`)* |
| `:70` projektas | Komandoje buvau pagrindinė frontend programuotoja ir dirbau dalį backend darbų. | Projekte atsakėme už visą frontend dalį ir dalį backend darbų. *(žr. 1 klausimą pabaigoje)* |
| `:72` | Jau pirmame atsakyme atvirai pasakysiu… | Jau pirmame atsakyme atvirai pasakysime… |
| `:73` | …dažniausiai taip ir patariu. | …dažniausiai taip ir patariame. |
| `:74` | Duomenis perkeliu iš Excel… | Duomenis perkeliame iš Excel… |
| `:75` | Sistemą kuriu taip… Naujas funkcijas galiu pridėti ir aš, ir kitas programuotojas… | Sistemą kuriame taip, kad ją būtų galima plėsti. Naujas funkcijas galime pridėti mes arba bet kuri kita komanda: kodas priklauso jums. |

**Programėlės ir web aplikacijos:**

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:130` aprašymas paieškai | Sukuriu pirmą veikiančią… | Sukuriame pirmą veikiančią… |
| `:132` | Padedu ją išgryninti ir sukuriu… | Padedame ją išgryninti ir sukuriame… |
| `:152` projektas | Visą sistemą sukūriau viena: … | Visą sistemą sukūrėme nuo nulio: … |
| `:156` | Tik tada skaičiuoju kainą. | Tik tada skaičiuojame kainą. |
| `:157` | Perduodu visą kodą… tęsti su manimi ar su kitu programuotoju. | Perduodame visą kodą ir prieigas, todėl ateityje galite tęsti su mumis arba su kita komanda. |
| `:158` | Peržiūriu esamą kodą ir pasakau… | Peržiūrime esamą kodą ir pasakome… |

**Integracijos:**

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:206` aprašymas paieškai | Sujungiu jūsų programas… | Sujungiame jūsų programas… |
| `:208` | Sujungiu el. parduotuves… | Sujungiame el. parduotuves… |
| `:212` | Pavyzdžiui, galiu sujungti | Pavyzdžiui, galime sujungti |
| `:219` | …jį suprojektuoju ir sukuriu. | …jį suprojektuojame ir sukuriame. |
| `:231` | Pirmiausia patikrinu… ir tik tada pasiūlau… | Pirmiausia patikriname… ir tik tada pasiūlome… |
| `:232` | …pasiūlysiu jį. | …pasiūlysime jį. |

**AI chatbot:**

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:306` projektas | Visą įrankį sukūriau viena: … | Visą įrankį sukūrėme patys: … |
| `:309` | Tikslų įvertinimą pateikiu… | Tikslų įvertinimą pateikiame… |

`:308` ir `:311` jau parašyti „mes“ forma („išbandome“, „Renkamės“), todėl dabar tie patys puslapiai maišo „aš“ ir „mes“. Pakeitus kitus, tekstas taps vientisas.

## 5. Apie puslapis (`lt/about.html`)

Šiam puslapiui reikia daugiausia darbo. Dabar jis yra asmeninis CV: „Esu Gabrielė“, darbo patirtis, išsilavinimas. Siūlau jį paversti „Apie mus“ puslapiu:

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:496` pavadinimas | Apie mane \| Gabrielė Tamaševičiūtė · Codeart | Apie mus \| Codeart |
| `:497` aprašymas paieškai | Gabrielė Tamaševičiūtė, programuotoja iš Vilniaus: kaip dirbu… | Codeart – verslo sistemų ir web aplikacijų kūrimas Vilniuje: kaip dirbame, vertybės ir kas veda projektus. |
| `:498` | Apie mane | Apie mus |
| `:499` H1 | Esu Gabrielė | Kuriame sistemas, kuriomis naudojamasi kasdien |
| `:500–504` pastraipos | 3 pastraipos pirmuoju asmeniu | žr. žemiau |
| `:507` | Kaip dirbu | Kaip dirbame |
| `:509` | Galvoju apie visą sistemą / Žiūriu… kuriu. Vertinu… | Galvojame apie visą sistemą / Žiūrime ne tik į ekraną, kurį tuo metu kuriame. Vertiname… |
| `:510` | Pirma suprantu problemą / …ieškau priežasties. Tik tada keičiu kodą. | Pirma suprantame problemą / …ieškome priežasties. Tik tada keičiame kodą. |
| `:511` | Galiu dirbti su esamu kodu / Galiu perprasti… | Dirbame ir su esamu kodu / Galime perprasti… |
| `:512` | Seku… / Naudoju AI įrankius… ir integruoju… | Sekame… / Naudojame AI įrankius… ir integruojame… |
| `:518` | Ką pažadu, tą ir padarau. | Ką pažadame, tą ir padarome. |
| `:521` | Man rūpi rezultatas, ne tik užduotis. | Mums rūpi rezultatas, ne tik užduotis. |
| `:523–537` patirtis, išsilavinimas, kalbos | asmeninė karjera | išimti iš šio puslapio, palikti tik CV puslapyje |

**Pastraipos (`:500–504`):**

> Codeart kuria verslo sistemas ir web aplikacijas, kurios žmonėms iš tikrųjų padeda: sutaupo laiko, sumažina chaosą ir leidžia susitelkti į tai, kas svarbu. Geriausias įvertinimas mums – kai sistema naudojamasi kasdien.

> Dirbame per visą grandinę: nuo poreikio išgryninimo ir sąsajos projektavimo iki architektūros, API, duomenų bazės ir paleidimo.

> Studiją įkūrė programuotoja Gabrielė Tamaševičiūtė. Ji veda kiekvieną projektą ir yra jūsų pagrindinis kontaktas, o pagal projekto apimtį komandą papildo patikrinti dizaino, backend ar mobiliųjų programėlių specialistai.

Nuotrauką palik prie trečios pastraipos kaip įkūrėjos bloką.

Patirtį („Jaunesnioji programuotoja“, „Planuotoja“, „Administratorė“) ir studijas („studijuoju“) iš šio puslapio verta išimti. Darbdaviui jos naudingos, bet klientui, kuris renkasi studiją, kelia klausimą, ar tai tikrai komanda. Jos lieka CV puslapyje.

## 6. Kontaktų puslapis

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:540` aprašymas paieškai | …Paprastai atsakau per 24 val. | …Paprastai atsakome per 24 val. |
| `:549` | Jei ko nors trūksta, paklausiu el. paštu. …ar galiu būti tinkamas žmogus jūsų projektui. | Jei ko nors trūksta, paklausime el. paštu. …ar esame tinkama komanda jūsų projektui. |
| `:550` | Per 24 val. po to atsiunčiu darbų planą… | Per 24 val. po to atsiunčiame darbų planą… |

## 7. Projektų puslapiai

| Vieta | Dabar | Siūloma |
|---|---|---|
| `:1666` kalbų platforma, „Rolė“ | Viena kūriau visą sistemą: duomenų bazę, … | Visas kūrimo ciklas: duomenų bazė, serverio logika, mokinio platforma, turinio valdymas ir testai. |
| `:1726` TikMaker, būsena | Darbo įrankis, kurį naudoju savo turiniui. | Vidinis įrankis, kurį naudojame savo turiniui. |
| `:1752` TikMaker, „Rolė“ | Viena kūriau visą įrankį: … | Visas įrankis: redaktorius, video variklis, serveris ir testai. |
| `:1821` lojalumo sistema, „Rolė“ | Pagrindinė frontend programuotoja komandoje… | Visa frontend dalis ir dalis backend darbų, kartu su backend programuotoju. |
| `:1829` lojalumo sistema | Daugiau apie šį projektą galiu papasakoti pokalbio metu. | Daugiau apie šį projektą papasakosime susitikimo metu. |
| `:1860` etiketė | Rolė | Ką darėme |

„Rolė“ laukeliams siūlau neutralią formą („Visas kūrimo ciklas: …“), o ne „sukūrėme“. Taip tekstas tinka studijai ir neteigia nieko, kas nebūtų tiesa.

## 8. Straipsniai

**Paskelbti:**

| Failas:eilutė | Dabar | Siūloma |
|---|---|---|
| `ai-verslui.html:146` | Kuriu individualias verslo sistemas… | Kuriame individualias verslo sistemas… |
| `siuntu-automatizavimas.html:113` | Kuriu automatizavimo sprendimus… | Kuriame automatizavimo sprendimus… |
| `uzduotis-programuotojui.html:15` | …parodysiu, kaip paruošti…, pateiksiu… | …parodysime, kaip paruošti…, pateiksime… |
| `uzduotis-programuotojui.html:96` | …arba išsiųskite man. | …arba išsiųskite mums. |
| `web-ar-mobilioji-programele.html:88` | Web aplikacijų kūrimas pas mane prasideda… | Web aplikacijų kūrimas pas mus prasideda… |

**Juodraščiai** (verta pataisyti prieš paskelbiant):

| Failas:eilutė | Dabar | Siūloma |
|---|---|---|
| `crm-pagal-uzsakyma-ar-gatavas.html:24` | …sąžiningai patarsiu… | …sąžiningai patarsime… |
| `excel-nebepakanka.html:38, 45` | Dažniausiai patariu…; …rašiau straipsnyje… | Dažniausiai patariame…; …rašėme straipsnyje… |
| `kiek-kainuoja-programele.html:14` | Šiame straipsnyje padėsiu suprasti… | Šiame straipsnyje padėsime suprasti… |
| `kiek-kainuoja-programele.html:26` | Plačiau apie tai rašiau… | Plačiau apie tai rašėme… |
| `kiek-kainuoja-programele.html:39` | Tai mano kainos. Didelės agentūros dažnai prašo daugiau, nes projektą veda kelių žmonių komanda. Pavienis programuotojas ar maža studija… | Tai mūsų kainos. Didelės agentūros dažnai prašo daugiau dėl didesnės administracijos. Maža studija gali pasiūlyti mažesnę kainą už tą patį rezultatą. |
| `kiek-kainuoja-verslo-sistema.html:28` | …mano kainų rėžiai… pateikiu… | …mūsų kainų rėžiai… pateikiame… |
| `kiek-kainuoja-verslo-sistema.html:14, 39` | išgirstu, parodau, nurodau | išgirstame, parodome, nurodome |
| `kiek-kainuoja-verslo-sistema.html:42` | Dirbu už fiksuotą kainą… | Dirbame už fiksuotą kainą… |
| `kiek-kainuoja-verslo-sistema.html:59` | …atsiųsiu darbų planą… | …atsiųsime darbų planą… |
| `no-code-ar-programuotojas.html:10` | Atsakau kaip programuotoja, kuri pati naudoja šiuos įrankius. | Atsakome kaip komanda, kuri pati kasdien naudoja šiuos įrankius. |
| `no-code-ar-programuotojas.html:14` | Aš pati juos naudoju greitiems prototipams. | Patys juos naudojame greitiems prototipams. |
| `no-code-ar-programuotojas.html:44–49` | darau; peržiūriu, įvertinu, sutvarkau, perkeliu, paleidžiu | darome; peržiūrime, įvertiname, sutvarkome, perkeliame, paleidžiame |
| `parduotuve-ir-apskaita.html:52` | Apie tai rašiau… | Apie tai rašėme… |

Straipsnių autorė gali likti Gabrielė (struktūriniuose duomenyse ji jau nurodyta). Straipsnis, kurį pasirašo konkretus žmogus, atrodo patikimiau, o tekstas vis tiek gali būti „mes“ forma.

## 9. Ne tekstai, bet tam pačiam įvaizdžiui

- **Meniu „Portfolio“ veda į CV darbdaviams** (`lt/portfolio.html`). Studijai geriau meniu punktas „Darbai“, vedantis į projektus, o CV nuoroda tik poraštėje.
- **El. paštas `gt1230112301@gmail.com`.** Adresas su domenu (pvz. `labas@codeart.lt`) atrodo kaip įmonės.
- **LinkedIn kontaktuose** yra asmeninis profilis. Gali likti, bet ateityje verta turėti ir Codeart įmonės puslapį.

## Klausimai prieš keičiant

1. **Lojalumo sistema.** Ar tai darbdavio (UVS) projektas? Jei taip, ar galima jį rodyti kaip Codeart darbą? Gali būti, kad saugiau jį pateikti tik CV puslapyje.
2. **„Mes“ ir projektuose.** Ar „Rolė“ laukeliuose rašyti „sukūrėme“, ar neutralią formą, kaip siūlau?
3. **Apie puslapis.** Ar perdaryti jį į „Apie mus“ ir išimti asmeninę patirtį, ar palikti asmeninį ir pridėti tik įvadinę pastraipą apie studiją?
