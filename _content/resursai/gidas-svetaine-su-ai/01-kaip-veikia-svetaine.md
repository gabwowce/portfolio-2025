# 1. Kaip veikia svetainė

Kad susikurtumėte svetainę su AI, programuotoju tapti nereikia. Bet kelias sąvokas suprasti reikia: AI agentas jas vartos, klausinės jūsų ir lauks sprendimų. Jei nežinote, kuo skiriasi domenas nuo talpinimo ar CSS nuo JavaScript, nesuprasite, ką AI siūlo, ir negalėsite paaiškinti, ko norite.

Šis skyrius trumpas ir be kodo. Jo pabaigoje žinosite, iš ko susideda svetainė, kur ji „gyvena“ ir ką sukursime šiame gide.

---

## 1.1. Kas vyksta, kai atidarote svetainę

Kai naršyklėje įvedate adresą, pavyzdžiui, `codeart.lt`, per sekundės dalį įvyksta keli žingsniai [1]:

1. **Naršyklė ieško adreso.** Ji kreipiasi į DNS (angl. *Domain Name System*), kuri veikia kaip interneto adresų knyga. DNS pasako, koks yra tikrasis serverio adresas, vadinamas IP adresu (pvz. `192.0.2.172`).
2. **Naršyklė siunčia užklausą.** Ji siunčia serveriui HTTP užklausą: „atsiųsk man šį puslapį“.
3. **Serveris atsako.** Jei viskas gerai, jis atsako kodu „200 OK“ ir siunčia svetainės failus mažomis dalimis.
4. **Naršyklė parodo puslapį.** Ji sudėlioja gautus failus ir parodo jums puslapį.

Iš to svarbu įsiminti du dalykus:

- **Domenas** (`codeart.lt`) yra tik vardas adresų knygoje. Jis nurodo, kur ieškoti svetainės.
- **Serveris** yra kompiuteris, kuriame laikomi svetainės failai. Paslauga, kuri suteikia tokį serverį, vadinama **talpinimu** (angl. *hosting*).

Kartais vietoj puslapio pamatysite klaidos kodą. Dažniausi: **404** reiškia, kad toks puslapis nerastas, **500** – kad serveryje įvyko klaida [9].

---

## 1.2. Iš ko sudarytas puslapis: HTML, CSS ir JavaScript

Kiekvieną interneto puslapį sudaro trys sluoksniai [2]:

| Sluoksnis | Už ką atsakingas | Pavyzdys |
|---|---|---|
| **HTML** | turinys ir struktūra | antraštės, tekstas, nuotraukos, nuorodos |
| **CSS** | išvaizda | spalvos, šriftai, išdėstymas, kaip puslapis atrodo telefone |
| **JavaScript** | elgsena | meniu, kuris atsidaro paspaudus, formos patikrinimas prieš siunčiant |

Palyginimas su namu: HTML yra sienos ir kambariai, CSS yra apdaila ir baldai, JavaScript yra elektra ir jungikliai.

Kodėl tai svarbu dirbant su AI: kai prašysite pakeitimo, žinosite, kurį sluoksnį jis liečia. „Padaryk antraštę didesnę“ yra CSS pakeitimas. „Pridėk skyrių apie kainas“ yra HTML. „Tegul meniu užsidaro paspaudus nuorodą“ yra JavaScript. Kuo tiksliau įvardysite, tuo mažiau AI turės spėlioti.

---

## 1.3. Statinė ar dinaminė svetainė

Svetainės būna dviejų tipų [3]:

- **Statinė svetainė** kiekvienam lankytojui rodo tą patį turinį. Visi puslapiai paruošti iš anksto, o serveris juos tiesiog atiduoda.
- **Dinaminė svetainė** puslapį sudėlioja kiekvienam lankytojui atskirai, dažniausiai iš duomenų bazės. Ji gali rodyti skirtingą turinį pagal tai, kas prisijungęs ar ką lankytojas pasirinko.

Čia atsiranda dar trys žodžiai, kuriuos AI vartos dažnai:

- **Frontend** – tai, kas veikia lankytojo naršyklėje: HTML, CSS, JavaScript.
- **Backend** – programa serveryje, kuri apdoroja užklausas, pavyzdžiui, tikrina slaptažodį ar išsaugo užsakymą.
- **Duomenų bazė** – vieta, kur saugomi duomenys: vartotojai, užsakymai, įrašai.

| | Statinė svetainė | Dinaminė svetainė |
|---|---|---|
| Pavyzdžiai | įmonės pristatymas, portfolio, renginio puslapis | el. parduotuvė, rezervacijų sistema, svetainė su paskyromis |
| Ko reikia | frontend | frontend, backend, duomenų bazė |
| Kiek dalių prižiūrėti | mažai | daug |

**Šiame gide kuriame statinę svetainę.** Tai paprasčiausias ir patikimiausias būdas pradėti. Kontaktų formą prijungsime per išorinę paslaugą (6 skyrius), todėl savo backend ir duomenų bazės nereikės.

---

## 1.4. Kur gyvena svetainė

Jūsų svetainė bus trijose vietose. Kiekviena atlieka savo darbą:

1. **Jūsų kompiuteris.** Čia su Claude Code kuriate ir keičiate svetainę.
2. **GitHub – kodo saugykla.** GitHub saugykloje (angl. *repository*) laikomi visi svetainės failai ir kiekvieno jų pakeitimų istorija [4]. Tai ir atsarginė kopija, ir galimybė grįžti prie bet kurios ankstesnės versijos.
3. **Vercel – talpinimas.** Vercel paima kodą iš GitHub ir paskelbia jį internete. Kiekvieną kartą, kai įkeliate pakeitimus į GitHub, Vercel automatiškai atnaujina svetainę [5].

Ir ketvirtas dalykas, kuris viską sujungia:

4. **Domenas.** `.lt` domenas registruojamas per akredituotą paslaugų teikėją. Jų sąrašą skelbia .lt domenų registras DOMREG [6]. Domenas su Vercel susiejamas DNS įrašu: pagrindiniam domenui (`jusudomenas.lt`) naudojamas A įrašas, subdomenui (`www.jusudomenas.lt`) – CNAME įrašas [7].

Visas kelias atrodo taip:

> **Jūs + Claude Code** (kompiuteryje) → **GitHub** (kodas ir istorija) → **Vercel** (svetainė internete) → **domenas** → **lankytojas**

Vieną dalyką verta žinoti iš karto: nemokamas Vercel planas (Hobby) skirtas tik asmeniniam, nekomerciniam naudojimui. Svetainė, kurioje reklamuojamos prekės ar paslaugos, Vercel taisyklėse laikoma komercine [8]. Ką rinktis verslo svetainei, aptarsime 6 skyriuje.

---

## 1.5. Svetainė, web aplikacija ar PWA?

Šis gidas skirtas svetainei. Bet verta žinoti, kur baigiasi svetainė:

- **Svetainė** pristato informaciją: kas jūs, ką siūlote, kaip susisiekti. Lankytojai ją skaito.
- **Web aplikacija** yra įrankis: lankytojai prisijungia, kažką kuria, saugo, perka. Jai reikia backend ir duomenų bazės.
- **PWA** (angl. *progressive web app*) yra web aplikacija, kurią galima įsidėti į telefono pagrindinį ekraną ir atidaryti kaip programėlę.

Jei jums reikia paskyrų, mokėjimų ar asmeninių duomenų saugojimo, jums reikia web aplikacijos. Pagrindai, kuriuos išmoksite šiame gide (darbas su Claude Code, GitHub, Vercel), praverstų ir jai, bet web aplikacijai reikia daugiau: apie tai 8 skyriuje.

---

## 1.6. Ką sukursime šiame gide

Gido pabaigoje turėsite:

- svetainę su 4 puslapiais: pagrindinis, apie, paslaugos ir kontaktai;
- dizainą, kuris gerai atrodo ir telefone, ir kompiuteryje;
- veikiančią kontaktų formą;
- savo domeną su saugiu ryšiu (HTTPS);
- kodą savo GitHub paskyroje, kurį galėsite keisti bet kada;
- įgūdžius, kaip toliau keisti ir plėsti svetainę su AI.

---

## Žodynėlis

| Žodis | Reikšmė |
|---|---|
| Domenas | svetainės vardas, pvz. `codeart.lt` |
| DNS | interneto „adresų knyga“, kuri domeną paverčia serverio adresu |
| IP adresas | tikrasis serverio adresas internete, skaičiai |
| HTTP | kalba, kuria naršyklė ir serveris susikalba |
| Talpinimas (hosting) | paslauga, kuri laiko svetainę serveryje ir rodo ją internete |
| HTML / CSS / JavaScript | puslapio turinys / išvaizda / elgsena |
| Frontend / Backend | kas veikia naršyklėje / kas veikia serveryje |
| Duomenų bazė | vieta, kur saugomi duomenys |
| Saugykla (repository) | GitHub vieta, kur laikomas projekto kodas ir jo istorija |
| Paskelbimas (deploy) | svetainės įkėlimas į internetą |

## Skyriaus kontrolinis sąrašas

- [ ] Suprantu, kuo skiriasi domenas ir talpinimas.
- [ ] Žinau, už ką atsakingi HTML, CSS ir JavaScript.
- [ ] Suprantu, kodėl šiame gide kuriama statinė svetainė.
- [ ] Žinau, ką daro GitHub ir ką daro Vercel.
- [ ] Žinau, kad nemokamas Vercel planas skirtas tik nekomerciniam naudojimui.

---

## Šaltiniai

1. MDN Web Docs, „How the web works“. https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works
2. MDN Web Docs, „What is JavaScript?“ (HTML, CSS ir JavaScript sluoksniai). https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript
3. MDN Web Docs, „Introduction to the server side“ (statinės ir dinaminės svetainės). https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Introduction
4. GitHub Docs, „About repositories“. https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories
5. Vercel Docs, „Deploying Git Repositories with Vercel“. https://vercel.com/docs/git
6. DOMREG, „Lietuvos akredituoti paslaugų teikėjai“. https://www.domreg.lt/paslaugu-teikejai/lietuvos-akredituoti-paslaugu-teikejai/
7. Vercel Docs, „Adding & Configuring a Custom Domain“. https://vercel.com/docs/domains/working-with-domains/add-a-domain
8. Vercel Docs, „Fair Use Guidelines“, skyrius „Commercial usage“; „Hobby plan“. https://vercel.com/docs/limits/fair-use-guidelines ; https://vercel.com/docs/plans/hobby
9. MDN Web Docs, „HTTP response status codes“. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

### Faktų patikra

Visi šaltiniai atidaryti ir perskaityti 2026-11-01.

| Faktas | Šaltinis | Ką sako šaltinis |
|---|---|---|
| Naršyklė per DNS randa serverio IP adresą, siunčia HTTP užklausą, serveris atsako „200 OK“ ir siunčia failus paketais | [1] | „The browser goes to the DNS server and finds the real address of the server… sends an HTTP request message… the server sends the client a "200 OK" message… sending the website's files… as a series of small chunks called packets“ |
| IP adreso pavyzdys `192.0.2.172` | [1] | „They are special numbers that look like this: 192.0.2.172“ |
| HTML – struktūra, CSS – stilius, JavaScript – dinamiškas turinys | [2] | „HTML is the markup language that we use to structure… CSS is a language of style rules… JavaScript is a scripting language that enables you to create dynamically updating content“ |
| Statinė svetainė rodo tą patį turinį; dinaminė gali rodyti skirtingą, dažnai iš duomenų bazės | [3] | „a static site is one that returns the same hard-coded content…“; „A dynamic site can return different data for a URL based on information provided by the user or stored preferences“ |
| Saugykloje laikomas kodas, failai ir kiekvieno failo pakeitimų istorija | [4] | „A repository contains all of your code, your files, and each file's revision history.“ |
| Vercel automatiškai paskelbia pakeitimus po kiekvieno įkėlimo į GitHub | [5] | „Vercel allows for automatic deployments on every branch push and merges onto the production branch“ |
| .lt domenai registruojami per akredituotus paslaugų teikėjus | [6] | DOMREG skelbia Lietuvos ir užsienio akredituotų paslaugų teikėjų sąrašus |
| Pagrindiniam domenui A įrašas, subdomenui CNAME | [7] | „If you're using an Apex domain… configure it with an A record. If you're using a Subdomain… configure it with a CNAME record“ |
| Hobby planas tik nekomerciniam naudojimui; paslaugų reklama laikoma komercine | [8] | „Hobby teams are restricted to non-commercial personal use only.“; pavyzdžiai: „Advertising the sale of a product or service“ |
| 404 – puslapis nerastas, 500 – serverio klaida | [9] | „404 Not Found: The server cannot find the requested resource.“; „500 Internal Server Error: The server has encountered a situation it does not know how to handle.“ |
