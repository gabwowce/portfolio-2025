# 1. Prieš pradedant: ar jums tikrai reikia programėlės?

Brangiausia klaida kuriant programėlę yra sukurti ne tą dalyką. Su AI įrankiais pirmą versiją galima turėti per kelias dienas, todėl ši klaida tapo dar lengvesnė: kodas atsiranda greičiau, nei spėjate pagalvoti, ar jo apskritai reikia.

Šis skyrius padės per pusvalandį atsakyti į tris klausimus:

1. Ar jūsų idėjai reikia savos programėlės, ar užtenka esamų įrankių?
2. Jei reikia, kokios: web aplikacijos, PWA ar mobiliosios programėlės?
3. Ko tikėtis iš AI įrankių ir ko iš jų nesitikėti?

Skyriaus pabaigoje užpildysite **idėjos kortelę**. Ją naudosite 2 skyriuje, kai planuosite pirmą versiją.

---

## 1.1. Trys klausimai prieš pradedant

Šiandien kuriamos programėlės nebėra vien verslo įrankiai. Žmonės kuria AI asistentus, mokymų ir kursų platformas, žaidimus, bendruomenes, įrankius sau. Nesvarbu, ką kuriate, prieš pradedant verta atsakyti į tris klausimus.

### Kam ir kokią vertę kuriate?

Aprašykite vienu sakiniu pagal šį pavyzdį:

> **[Kas]** galės **[ką padaryti ar patirti]**, nors dabar **[kas trukdo ar ko trūksta]**.

Pavyzdžiai:

- **AI įrankis:** „Smulkių el. parduotuvių savininkai galės per minutę sukurti prekių aprašymus lietuviškai, nors dabar kiekvienam aprašymui sugaišta po pusvalandį.“
- **Mokymai:** „Pradedantieji fotografai galės mokytis trumpomis užduotimis telefone ir gauti atsiliepimą apie savo nuotraukas, nors dabar kursai yra ilgi vaizdo įrašai be grįžtamojo ryšio.“
- **Pramoga:** „Draugų kompanijos galės žaisti lietuvišką viktoriną vakarėlyje iš savo telefonų, be jokios registracijos.“
- **Verslo įrankis:** „Gėlių parduotuvės floristės matys visus dienos užsakymus vienoje vietoje, nors dabar pristatymai kartais pamirštami.“

Jei sakinio parašyti nepavyksta, dar nežinote, kam kuriate. Tai normalu: pirmiausia pasikalbėkite su keliais žmonėmis, kuriems produktas skirtas.

### Ką jie naudoja dabar?

Jūsų produktas visada su kažkuo konkuruoja, net jei tai ne kita programėlė:

- AI įrankis konkuruoja su ChatGPT ar Claude, kuriuos žmonės jau naudoja;
- kursai – su YouTube ir nemokamais straipsniais;
- žaidimas ar pramoga – su viskuo, kas telefone kovoja dėl dėmesio;
- verslo įrankis – su Excel lentele ir Messenger grupe.

Užsirašykite, ką jūsų žmonės naudoja dabar ir kodėl jie turėtų pereiti prie jūsų produkto. Jei atsakymas tik „mano gražesnis“, to neužteks: žmonės lieka prie to, prie ko pripratę.

### Ar jau yra panašių sprendimų?

Panašūs produktai nėra blogas ženklas. Atvirkščiai, jie įrodo, kad žmonėms to reikia. Klausimas kitas: ką galite pasiūlyti, ko jie neturi? Dažnai tai lietuvių kalba, siauresnė auditorija (pvz. tik kirpykloms), paprastesnis naudojimas arba kitokia kaina.

Taip pat pasitikrinkite, ar idėjos negalima įgyvendinti visai be programavimo:

| Idėja | Ką patikrinti pirmiausia |
|---|---|
| AI asistentas konkrečiai temai | ar užtenka savo GPT ChatGPT aplinkoje ar Claude projekto su gerai parašytais nurodymais ir jūsų dokumentais [13], [14] |
| Kursai ar mokymai | kursų platformos (pvz. Teachable, Thinkific) arba uždara Notion erdvė |
| Bendruomenė | Discord, Facebook ar Skool grupė |
| Registracija, formos, apklausos | Google Forms, Tally, rezervacijų sistemos |
| El. parduotuvė | Shopify, WooCommerce |

Savo programėlę verta kurti, kai:

- idėja neįtelpa į esamus įrankius ir tenka juos laužyti ar dubliuoti darbą rankomis;
- norite sujungti kelis dalykus į vieną patirtį (pvz. mokymus su AI grįžtamuoju ryšiu);
- programėlė pati yra jūsų produktas, už kurį mokės kiti;
- esamų įrankių prenumeratos per kelerius metus kainuotų daugiau nei savas sprendimas.

Jei nė vienas punktas netinka, pradėkite nuo esamo įrankio ir patikrinkite, ar žmonės juo naudosis. Tai ne pralaimėjimas: po kelių mėnesių tiksliai žinosite, ko trūksta, ir tai bus geriausia užduotis savai programėlei.

---

## 1.2. Web aplikacija, PWA ar mobilioji programėlė?

„Programėle“ kasdien vadinami trys skirtingi dalykai:

- **Web aplikacija** veikia naršyklėje, atidaroma nuoroda. Nieko diegti nereikia, veikia ir kompiuteryje, ir telefone.
- **PWA** (angl. *progressive web app*) yra web aplikacija, kurią galima „įdiegti“ į telefono pagrindinį ekraną. Ji atsidaro kaip atskira programėlė, be naršyklės juostos, ir gali siųsti pranešimus.
- **Mobilioji programėlė** kuriama atskirai iPhone ir Android telefonams ir platinama per App Store bei Google Play.

### Kas yra PWA, paprastai

PWA yra svetainė, kuri elgiasi kaip programėlė. Ją kuriate vieną kartą, kaip web aplikaciją, o vartotojas gali ją „įsidėti“ į telefoną be App Store ar Google Play.

Kaip tai atrodo vartotojui:

1. Telefone atsidaro jūsų nuorodą, kaip įprastą svetainę.
2. iPhone Safari naršyklėje paspaudžia „Bendrinti“ ir pasirenka pridėjimą prie pagrindinio ekrano. Android telefone Chrome gali pats pasiūlyti įdiegti programėlę.
3. Telefono ekrane atsiranda jūsų ikona. Paspaudus programėlė atsidaro per visą ekraną, be naršyklės adreso juostos, kaip įprasta programėlė.

Kodėl tai patogu: nereikia parduotuvių patvirtinimo ir mokesčių, o atnaujinus svetainę visi vartotojai iš karto gauna naują versiją. Trūkumas: vartotojas pats turi žinoti, kad programėlę galima įsidiegti, todėl tai tenka paaiškinti, pavyzdžiui, trumpa instrukcija pirmą kartą atsidarius.

### Kuo jos skiriasi praktiškai

| | Web aplikacija | PWA | Mobilioji programėlė |
|---|---|---|---|
| Kaip pasiekia vartotojas | nuoroda | nuoroda, tada „Pridėti prie pagrindinio ekrano“ | parduotuvė (App Store, Google Play) |
| Pranešimai telefone | ne | taip; iPhone nuo iOS 16.4, tik įdiegus į pagrindinį ekraną [1] | taip |
| Prieiga prie telefono funkcijų | ribota | ribota; pvz. Bluetooth įrenginiai iPhone naršyklėje nepalaikomi [2] | pilna |
| Mokesčiai parduotuvėms | nėra | nėra | Apple 99 USD per metus [3], Google 25 USD vieną kartą [4] |
| Patvirtinimas prieš paleidžiant | nereikia | nereikia | reikia; naujoms asmeninėms Google paskyroms – uždaras testavimas su ne mažiau kaip 12 testuotojų 14 dienų [5] |
| Atnaujinimai | iš karto visiems | iš karto visiems | per parduotuvę |
| Ką kuria AI įrankiai naršyklėje | taip, tai jų pagrindas (pvz. Lovable generuoja React web aplikacijas [6]) | dažniausiai galima pritaikyti | retai, reikia kitų įrankių |

Jei programėlėje parduosite skaitmeninį turinį ar prenumeratas, parduotuvės ima ir komisinį mokestį nuo pardavimų. Pavyzdžiui, Apple mažiems kūrėjams (iki 1 mln. USD pajamų per metus) taiko sumažintą 15 % mokestį [7].

### Ar galima pasikliauti PWA?

Iš esmės taip, bet verta žinoti, kad taisykles nustato telefonų gamintojai. 2024 m. pradžioje Apple paskelbė, kad ES šalyse (taigi ir Lietuvoje) iOS 17.4 nebeleis įdiegti web aplikacijų į pagrindinį ekraną. Po kelių savaičių, kilus kūrėjų pasipiktinimui, sprendimas buvo atšauktas [8]. Funkcija veikia toliau, bet ši istorija primena, kad dalis jūsų programėlės ateities priklauso ne nuo jūsų.

### Kaip pasirinkti

**Pradėkite nuo web aplikacijos ar PWA**, jei:

- programėle naudosis darbuotojai ar esami klientai, kuriems galite tiesiog duoti nuorodą;
- norite greitai patikrinti idėją;
- programėlei užtenka pranešimų, kameros nuotraukų įkėlimo ir vietos nustatymo, kai ji atidaryta.

**Rinkitės mobiliąją programėlę**, jei:

- žmonės jūsų produkto ieškos parduotuvėse, ir būtent ten jį ras;
- reikia telefono funkcijų, kurių naršyklė neleidžia (pvz. Bluetooth įrenginiai iPhone [2]);
- programėlė turi patikimai veikti be interneto ilgą laiką.

Daugumai pirmų versijų užtenka web aplikacijos ar PWA. Jei idėja pasiteisins, mobiliąją programėlę galėsite kurti vėliau, jau žinodami, ko vartotojams tikrai reikia.

---

## 1.3. Ko tikėtis iš AI įrankių

AI įrankiai iš tiesų pakeitė, kaip greitai galima sukurti pirmą versiją. Per kelias valandas galite turėti veikiančią sąsają: sąrašus, formas, prisijungimą, duomenų bazę. Anksčiau tam reikėjo programuotojo ir kelių savaičių.

Bet greitis turi kainą, ir ją verta žinoti iš anksto.

### Ką AI daro gerai

- Greitai sukuria ekranus, formas ir sąrašus pagal aprašymą.
- Padeda pamatyti idėją „gyvai“ ir parodyti ją kitiems.
- Paaiškina klaidas ir siūlo, kaip jas taisyti.
- Puikiai tinka prototipui, kuriuo tikrinate, ar idėja kam nors reikalinga.

### Kur AI dažniausiai klysta

**Saugumas.** 2025 m. saugumo bendrovė Veracode išbandė daugiau nei 100 AI modelių su 80 programavimo užduočių. 45 % atvejų sugeneruotas kodas turėjo žinomų saugumo spragų [9]. Svarbiausia išvada: didesni ir naujesni modeliai saugumo požiūriu nebuvo reikšmingai geresni, nors veikiantį kodą rašė vis geriau [9]. Vėlesnis tų pačių metų atnaujinimas parodė, kad kai kurie naujausi modeliai pagerėjo, bet problema neišnyko [10].

**Realus pavyzdys.** 2025 m. pavasarį buvo paskelbta saugumo spraga CVE-2025-48757, susijusi su Lovable sukurtomis programėlėmis. Daugelyje jų duomenų bazėje (Supabase) nebuvo tinkamai nustatytos prieigos taisyklės (angl. *Row Level Security*), todėl pašaliniai asmenys galėjo skaityti ir keisti duomenis be prisijungimo [11]. Tyrėjų patikrintoje imtyje pažeidžiamos buvo apie 170 iš 1 645 programėlių [12].

Programėlės **veikė**. Jų kūrėjai nematė jokios problemos, nes spraga nesimato naudojantis programėle įprastai. Ji matosi tik tam, kas jos ieško.

**Sudėtinga logika.** Kol programėlė maža, AI ją keičia drąsiai. Kai taisyklių daugėja (vartotojų rolės, mokėjimai, išimtys), kiekvienas naujas pakeitimas vis dažniau sugadina tai, kas jau veikė. Apie tai, kaip su tuo tvarkytis, kalbėsime 4 skyriuje.

### Ką tai reiškia jums

AI įrankis yra kaip labai greitas, bet nepatyręs padėjėjas. Jis padarys daug ir greitai, bet atsakomybė už rezultatą lieka jums. Todėl šiame gide:

- 4 skyriuje išmoksite dirbti su AI taip, kad neprarastumėte kontrolės;
- 5 skyriuje rasite saugumo kontrolinį sąrašą, kurį verta pereiti prieš įleidžiant pirmus vartotojus;
- 7 skyriuje sužinosite, kaip atpažinti momentą, kai prototipą laikas perduoti programuotojui.

---

## Užduotis: idėjos kortelė

Užpildykite penkias eilutes. Jei kurios nors nežinote, palikite tuščią ir grįžkite po pokalbio su būsimais vartotojais.

| Klausimas | Jūsų atsakymas |
|---|---|
| **Problema** (vienu sakiniu) | |
| **Kam ji aktuali** (kas tie žmonės, kiek jų) | |
| **Kaip sprendžiama dabar** | |
| **Kodėl esami įrankiai netinka** | |
| **Formatas** (web, PWA ar mobilioji) ir kodėl | |

## Skyriaus kontrolinis sąrašas

- [ ] Problemą galiu aprašyti vienu sakiniu.
- [ ] Žinau, kaip ji sprendžiama dabar ir kas tame nepatogu.
- [ ] Patikrinau, ar idėjos neužtenka įgyvendinti esamais įrankiais.
- [ ] Pasirinkau formatą: web aplikacija, PWA ar mobilioji programėlė.
- [ ] Suprantu, kad AI pagreitina darbą, bet už saugumą atsakau pats.

---

## Šaltiniai

1. WebKit, „Web Push for Web Apps on iOS and iPadOS“, 2023-02-16. https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
2. Can I use, „Web Bluetooth“ (Safari iOS: nepalaikoma). https://caniuse.com/web-bluetooth
3. Apple Developer, „Apple Developer Program“ („$99 annual membership“). https://developer.apple.com/programs/
4. Google Play Console Help, „How to get started with Play Console“ (vienkartinis 25 USD registracijos mokestis). https://support.google.com/googleplay/android-developer/answer/113468
5. Google Play Console Help, „App testing requirements for new personal developer accounts“. https://support.google.com/googleplay/android-developer/answer/14151465
6. Lovable, FAQ „Tech stack“ (React, Vite, TypeScript). https://lovable.dev/faq/capabilities/tech-stack
7. Apple Developer, „App Store Small Business Program“. https://developer.apple.com/app-store/small-business-program/
8. 9to5Mac, „Apple reverses course, will continue supporting Home Screen web apps in the EU“, 2024-03-01. https://9to5mac.com/2024/03/01/apple-home-screen-web-apps-ios-17-eu/ (antrinis šaltinis, cituoja Apple kūrėjų puslapį)
9. Veracode, pranešimas spaudai „AI-Generated Code Poses Major Security Risks in Nearly Half of All Development Tasks“, 2025-07-30. https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/
10. Veracode, „October 2025 Update: GenAI Code Security Report“. https://www.veracode.com/resources/2025-genai-code-security-report/
11. CVE-2025-48757 aprašymas (NVD). https://nvd.nist.gov/vuln/detail/CVE-2025-48757
12. Superblocks, „Lovable Vulnerability Explained: How 170+ Apps Were Exposed“ (antrinis šaltinis, apibendrina tyrėjo Matt Palmer duomenis). https://www.superblocks.com/blog/lovable-vulnerabilities

13. OpenAI, „Introducing GPTs“, 2023-11-06. https://openai.com/index/introducing-gpts/ (patikrinta pagal žiniasklaidos aprašymus)
14. Simon Willison, „Claude Projects“, 2024-06-25. https://simonwillison.net/2024/Jun/25/claude-projects/ (antrinis šaltinis)

### Faktų patikra

| Faktas | Šaltinis | Kaip patikrinta | Data |
|---|---|---|---|
| Apple Developer Program 99 USD per metus | [3] | atidarytas oficialus puslapis | 2026-10-29 |
| Google Play 25 USD vienkartinis mokestis | [4] | paieška cituoja oficialų puslapį; atidaryti nepavyko (tinklo apribojimas) | 2026-10-29 |
| 12 testuotojų, 14 dienų, asmeninės paskyros po 2023-11-13 | [5] | paieška cituoja oficialų puslapį; atidaryti nepavyko | 2026-10-29 |
| Web Push iPhone nuo iOS 16.4, tik pagrindinio ekrano programėlėms | [1] | paieška cituoja WebKit įrašą ir kelis žiniasklaidos šaltinius; atidaryti nepavyko | 2026-10-29 |
| Web Bluetooth nepalaikoma Safari iOS | [2] | paieška cituoja caniuse | 2026-10-29 |
| Apple ES PWA sprendimas ir atšaukimas 2024 m. | [8] | keli nepriklausomi žiniasklaidos šaltiniai | 2026-10-29 |
| Apple 15 % mažiems kūrėjams iki 1 mln. USD | [7] | paieška cituoja oficialų puslapį | 2026-10-29 |
| Lovable generuoja React + Vite + TypeScript | [6] | paieška cituoja oficialų FAQ | 2026-10-29 |
| Veracode: 45 %, 100+ modelių, 80 užduočių; dydis negerina saugumo | [9] | paieška cituoja pranešimą spaudai ir kelis perpasakojimus; atidaryti nepavyko | 2026-10-29 |
| Veracode spalio atnaujinimas: kai kurie modeliai pagerėjo | [10] | paieška cituoja Veracode puslapį | 2026-10-29 |
| CVE-2025-48757: nepakankamos RLS taisyklės Lovable programėlėse | [11] | paieška cituoja CVE aprašymą keliose CVE duomenų bazėse; NVD atidaryti nepavyko | 2026-10-29 |
| 170 iš 1 645 programėlių | [12] | tik antriniai šaltiniai; prieš maketuojant rasti pirminį tyrėjo įrašą | 2026-10-29 |
| Savo GPT galima susikurti be programavimo | [13] | paieška: keli žiniasklaidos aprašymai, OpenAI puslapio atidaryti nepavyko | 2026-10-30 |
| Claude Projects: dokumentai ir nurodymai projektui | [14] | antriniai šaltiniai | 2026-10-30 |

Prieš maketuojant PDF: atsidaryti [1], [4], [5], [9], [11] tiesiogiai ir rasti pirminį šaltinį skaičiui „170 iš 1 645“.
