# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G40 – G40-lyamouri |
| **Product brief** | `_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/brief.md` (commit `e75456f`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Avgrensningen er klok. Dere tar bare modul 4.1 «Prognoser og Demand Management» fra forslaget om KI-støttet MRP II, og sier tydelig at BOM, produksjonsplanlegging og leverandørintegrasjon er utenfor. Det gjør et vanskelig forslag mulig å gjennomføre for én person.
2. Suksesskriteriene er konkrete og testbare: en bedrift ser bare egne data, data lagres mellom økter, og «changing them visibly changes the output» for prognosemetode, sikkerhetsmargin og håndtering av avvik. Det er nesten ferdige testtilfeller.

**De viktigste endringene:**

1. Bestem hva «AI-generated demand forecasts» betyr. Lar dere en språkmodell lage tallene, kan verken dere eller sensor kontrollere om de er riktige. Beregn prognosene med kjente metoder i vanlig kode (for eksempel glidende gjennomsnitt og eksponentiell glatting), og bruk eventuelt KI til å forklare resultatet eller foreslå parametre.
2. Definer hvordan de tre scenarioene (optimistisk, normal, pessimistisk) og sikkerhetsmarginen regnes ut, og hva som regnes som et avvik (outlier). Uten slike regler kan ikke suksesskriteriene testes med fasit.
3. Fyll inn delene som mangler: «What Makes This Different» og «Vision», og beskriv primærbrukeren litt mer konkret (hvilken type bedrift, hvor mange produkter, hvor ofte planleggeren bruker verktøyet).

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** 4) KI-støttet MRP II (vanskelig), avgrenset til modul 4.1 Prognoser og Demand Management. Når bare én modul er med, blir prosjektet middels, slik veiledningen for vanskelighetsgrad sier. Det ligger i omfang nær 2) AI CV- og søknadsassistent (middels), men med mer beregningslogikk og mindre tekstgenerering.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Høy | Prognosemetoder, sesong og trend, scenarioer, sikkerhetsmargin og avviksbehandling må gi faglig riktige tall. Det er kjernen i oppgaven. |
| Datamodell – antall entiteter og relasjoner mellom dem | Middels | Bedrift/konto, produkt, periode, historisk salg, kampanjer, kundeordrer og prognose med parametre. |
| Brukere, roller og innlogging | Middels | Innlogging med kundenummer og passord, og isolasjon mellom bedrifter. Én rolle. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Middels | Uavklart. Hvis KI bare forklarer eller foreslår, er det middels. Hvis KI lager selve tallene, blir det svært vanskelig å kvalitetssikre. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Lav | Ingen eksterne systemer. Eventuelt et språkmodell-API. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Hver bedrift ser sine egne data. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Lav | Syntetiske data kan lastes inn som seed-data. Import av CSV er en mulig, men ikke nødvendig utvidelse. |
| Sikkerhet og personvern | Middels | Passordhashing og dataisolasjon. Dataene er syntetiske, så personvernrisikoen er lav. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer: logg inn → velg produkt → se historikk og prognose i tre scenarioer → juster metode, margin og avvik → se at prognosen endres.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | OK | Én modul med tydelig kjerneflyt er realistisk for én person, særlig hvis antall prognosemetoder begrenses til to–tre. Tidsfristen står som åpen i briefen – sett inn innleveringsdatoen og planlegg bakover. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Kjerneflyten er klar, men prognosemetode, scenario-regler og avviksregler er de viktigste kravene og står som åpne. De må avklares i PRD-en, ikke overlates til KI under implementeringen. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | Webapp med database og innlogging, og vanlige prognosemetoder som finnes i godt dokumenterte biblioteker. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Risiko | Prognoser er fagstoff fra logistikk. Dere må kunne sjekke tallene, for eksempel ved å regne et lite eksempel for hånd eller i regneark og sammenligne med appen. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | OK | Svært godt egnet, forutsatt at metodene beregnes i kode. Et syntetisk datasett med kjent trend og sesong gir fasit å teste mot. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | OK | Syntetiske data og lokal database gjør dette enkelt. Lag en testbedrift med kjent kundenummer og passord i README. Bruker dere språkmodell, trengs en reserve uten nøkkel. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | Risiko | Avhenger av valget i punkt 1 over. Ingen kostnad hvis prognosene regnes i kode, men da må KI-delen av appen beskrives på en annen måte. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. Velg to–tre prognosemetoder i v1 (for eksempel glidende gjennomsnitt, eksponentiell glatting og en enkel sesongjustering), og la KI-funksjonen i appen være en forklaring av prognosen og anbefalingen i klart språk. Det gir tall som kan kontrolleres og en avgrenset KI-funksjon.
2. Ta sesong/trend og historisk salg med i v1, men vurder å flytte kampanje-/markedsdata og innkommende kundeordrer til et senere trinn. Hvert nytt signal krever egne regler og testdata.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Tydelig hva appen er (prognoseverktøy for modul 4.1), og hvorfor sikkerhet er tatt med. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | God beskrivelse av kostnaden ved for lite og for mye lager, og eksempelet med en engangsordre som forstyrrer trenden. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | Juster | De tre beslutningspunktene som justerbare kontroller er et godt grep. Beskriv også hva planleggeren ser på skjermen, for eksempel graf med historikk og tre scenarioer. |
| What Makes This Different – er vurderingen ærlig og realistisk? | Juster | Mangler. Skriv noen ærlige setninger om hva som skiller verktøyet fra et regneark eller et standard ERP-system, for eksempel at beslutningene om metode, margin og avvik blir synlige og dokumenterte. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | Juster | Innkjøps-/lagerplanlegger er riktig. Gjør det mer konkret: hvilken type bedrift, hvor mange produkter og hvilken beslutning de skal ta etter å ha sett prognosen. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Juster | Gode funksjonelle kriterier. Legg til ett kriterium for riktighet, for eksempel «for testdatasettet gir glidende gjennomsnitt over tre perioder samme tall som en håndberegning». |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | OK | Tydelig «In» og «Out», med god begrunnelse. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | Juster | Mangler. En kort visjon kan vise hvordan prognosen senere kan mate S&OP eller MPS – uten at det tas inn i v1. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | God struktur, men de åpne spørsmålene er kjernen i appen. Dokumenter beslutningene om prognosemetode og KI-rolle med begrunnelse – det er godt prosessmateriale. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | OK | Realistisk og tydelig avgrenset til én modul, med nok innhold til å vise reell funksjonalitet. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Juster | Kriteriene er testbare når reglene for metoder, scenarioer og avvik er definert. Lag et testdatasett med kjent fasit. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | Juster | Skjermbildene kan utledes (innlogging, produktoversikt, prognose med kontroller), men en grafisk visning av historikk og scenarioer bør beskrives i UX-steget. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Teknologistakken er åpen. Velg en enkel stakk med én database, og hold prognoselogikken i en egen modul som kan testes isolert. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | OK | Syntetiske data og lokal kjøring gjør det enkelt for sensor, så lenge testbrukeren og eventuell KI-reserve står i README. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Ikke beskrevet. Planlegg hvor det syntetiske datasettet og skriptet som lager det skal ligge, og bruk `.env.example` for eventuelle nøkler. |

## 3. Neste steg for gruppen

1. Bestem hvilke prognosemetoder som er med i v1, hvordan scenarioer, sikkerhetsmargin og avvik beregnes, og hvilken rolle KI har i appen. Skriv det inn i briefen eller PRD-en med begrunnelse.
2. Lag et lite syntetisk datasett med kjent trend og sesong, og regn ut forventede prognoser for hånd eller i regneark. Bruk dem som suksesskriterier og senere som tester.
3. Fyll inn «What Makes This Different», «Vision» og en mer konkret primærbruker, og sett inn innleveringsfristen i stedet for «not yet specified».

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
