# Arbeidslogg – IBE160 Programmering med KI

**Prosjekt:** AI-støttet prognoseverktøy for Demand Management
**Repository:** G40-lyamouri
**Oppstart for denne arbeidsloggen:** 13. oktober 2026

## 1. Formål

Arbeidsloggen dokumenterer fremdriften i prosjektet fra 13. oktober 2026. Den skal vise planlegging, beslutninger, bruk av KI, utvikling, testing og kvalitetssikring underveis.

## 2. Arbeidsprinsipper

* Arbeide steg for steg og dokumentere faktisk fremgang.
* Bruke lærerens tilbakemelding som grunnlag for videre arbeid.
* Bestemme og godkjenne innholdet før KI-verktøy utfører endringer.
* Kontrollere forslag og endringer fra KI før de godkjennes.
* Dokumentere viktige beslutninger og begrunnelser.
* Bruke Git og GitHub til å følge prosjektets utvikling.

## 3. Arbeidslogg

### 13. oktober 2026 – Rydding og klargjøring

* Lukket de åpne terminaløktene i VS Code for å få en ryddigere arbeidsflate.
* Fjernet den tidligere filen `docs/product-brief-updated.md`, som ikke skal brukes videre.
* Fjernet den tidligere arbeidsloggen for å starte dokumentasjonen på nytt.
* Beholdt den opprinnelige Product Brief-en og lærerens tilbakemelding som grunnlag for videre arbeid.

**Status:** Oppryddingen er påbegynt. Neste steg er å gjennomgå den opprinnelige Product Brief-en opp mot lærerens tilbakemelding og bestemme nødvendige endringer før BMAD brukes til å oppdatere dokumentet.

### 14. oktober 2026 – Revisjon og godkjenning av Product Brief

* Skrev en revidert Product Brief på norsk ut fra lærerens tilbakemelding og ga den til Claude Code som grunnlag.
* Brukte BMAD-workflowen `bmad-product-brief` i oppdateringsmodus til å oppdatere `brief.md`.
* Kontrollerte at BMAD faktisk ble brukt. Claude Code bekreftet at flere steg i workflowen var hoppet over i første runde, blant annet memlog og sluttstegene. Disse stegene ble deretter fullført.
* Første utkast fra KI inneholdt egne tillegg og forslag, blant annet fire åpne punkter om trend og sesong, avviksregelen, periodelengde og S&OP/MPS. Jeg avviste disse og bestemte at briefen bare skal følge min reviderte tekst.
* `brief.md` ble skrevet om som en direkte oversettelse til engelsk av min tekst, med samme 11 seksjoner. Den er på engelsk fordi BMAD-oppsettet bruker engelsk for dokumenter. Et addendum med de avviste forslagene ble opprettet og deretter slettet.
* Sammenlignet `brief.md` med min reviderte tekst. Innholdet er det samme. Forskjellene gjelder bare språk, formatering og noen ordvalg i oversettelsen.
* Godkjente briefen og fikk status satt til `final`. Beslutningene er logget i `.memlog.md`.
* Anbefalt neste steg fra BMAD (`bmad-help`) er PRD. Det er ikke startet.
* Kontrollerte at bare relevante filer ble tatt med, og committet og pushet `brief.md` og `.memlog.md` til GitHub (commit `5c4fb17`).
* Kontrollerte at arbeidsloggen bare inneholdt arbeid fra 13. oktober, og committet og pushet den (commit `cf05373`).

**Status:** Product Brief er ferdig og godkjent. Neste steg er PRD, som ikke er startet.

### 31. oktober 2026 – Brainstorming før PRD

* Kontrollerte at prosjektmappen og BMAD var på plass, og hentet siste versjon fra GitHub.
* Ba Claude Code foreslå research- og brainstormingtemaer ut fra Product Brief og lærerens tilbakemelding.
* Kjørte `bmad-brainstorming` om planleggerflyten, periodeenhet og kantfall i beregningene, og prioriterte med MoSCoW.
* Viktigste beslutninger: uke som periode og tre ukers prognose, 104 uker syntetiske data, lagerbeholdning og utsolgt-flagg i dataene, utsolgte uker holdes utenfor beregningen, og bestillingsforslaget gjelder neste uke (prognose + sikkerhetsmargin − lager). Sesongjustering ble flyttet til bør-ha for å nå fristen.
* Godtok noen av KI-forslagene, endret andre, og lot forslag jeg ikke hadde bekreftet stå som åpne punkter.
* Committet og pushet brainstormingen og BMAD-rammeverket i to separate commits (`7a185ac` og `7e200ca`).

**Status:** Brainstormingen er ferdig. Neste steg er research før PRD.

### 1. november 2026 – Research før PRD

* Brukte `bmad-deep-recon` med parallelle subagenter til fire research-rapporter: prognosemetoder og datarensing, sikkerhetsmargin og bestillingsmengde, teknologistakk, og KI-forklaring uten betalt API.
* Godkjente kravene og vektene for valgrapportene (teknologistakk og KI-forklaring) før de ble kjørt.
* Kontrollerte at kildene er dokumentert, og at svake eller ubekreftede påstander er merket. Fjernet en lokal filsti fra en fil før commit.
* Committet og pushet researchen og sesjonsloggen (`a55da02` og `f46a88b`).
* Innførte en fast personvernregel: Claude Code skal bare arbeide i prosjektmappen, og personopplysninger, lokale filstier og hemmeligheter skal ikke komme med til GitHub.

**Status:** Researchen er ferdig. Neste steg er PRD.

### 2.–3. november 2026 – PRD

* Brukte `bmad-prd` i veiledet arbeidsmåte. Subagenter leste Product Brief, lærerens tilbakemelding, brainstormingen og research-rapportene, og jeg tok beslutningene underveis.
* Viktigste beslutninger: Prognose anbefaler og innkjøpsansvarlig bestemmer, brukergrensesnittet er på norsk, felles innstillinger for hele bedriften, tillitsmerke med faste regler, synlig utregning av både prognose og bestillingsmengde, malbasert forklaring som må-ha og valgfri lokal språkmodell som bør-ha, og innleveringsfrist 1. desember 2026.
* Gjennomgikk PRD-en med avstemming mot alle kildene, kvalitetsrubrikk, uavhengig beregningskontroll, konsistenssjekk, kontroll mot sensorveiledningen, og struktur- og språkpolering.
* Eksempler på styring av KI: Beregningskontrollen viste at reglene for uvanlige uker og nytt nivå kunne gi to ulike prognoser (51,0 eller 70,333), og dette ble rettet med én gjennomgang i tidsrekkefølge. En avrundingsfeil der 70 ble 71 ble funnet og rettet med en egen regel. Jeg avviste forslaget om å stramme oppsettsmålet til 10 minutter og beholdt 15 minutter, og bestemte at språkmodellen ikke skal avhenge av svar fra læreren.
* Kjørte en automatisk kontroll før ferdigstilling: alle ID-er, regler, terskler og referanseeksempler var uendret etter poleringen, og filene inneholdt ingen personopplysninger, lokale filstier eller hemmeligheter.
* Committet PRD-utkastet (`4ada86d`) og den ferdige PRD-en med status `final` (`d938baa`), og pushet til GitHub.

**Status:** PRD er ferdig og godkjent. Neste steg er å oppdatere Product Brief med endringene, og deretter UX-design (`bmad-ux`) og arkitektur (`bmad-architecture`).

### 6. november 2026 – UX-design med BMAD UX og Impeccable

* Leste den ferdige PRD-en, addendumet, beslutningsloggen, siste sesjonslogg og de åpne punktene før UX-steget startet.
* Fant den offisielle installasjonsmetoden for designskillen Impeccable og installerte versjon 4.8.0 i prosjektet med `npx impeccable install`. Telemetrien ble slått av, og npm-cachen ble holdt inne i prosjektmappen.
* Startet `bmad-ux` og opprettet arbeidsområdet `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/` med beslutningslogg. Impeccable skrev `PRODUCT.md` ut fra PRD-en.
* Utledet åtte designretninger fra brukernes norske hverdag, blant annet ukeplanleggeren, lagerkortet, værmeldingen og orienteringskartet. Impeccable trakk retningen som skulle bygges: orienteringskartet («O-kartet»).
* Startet ti subagenter parallelt for å lage ti designkonsepter. Kvoten for bruk ble brukt opp to ganger før agentene hadde laget noe design, så ingen av konseptene ble ferdige.
* Eksempel på styring av KI: Jeg stoppet planen med ti parallelle agenter, ba om at de ikke ble startet på nytt, og ba om ett gjennomarbeidet design i stedet, der Claude tar designbeslutningene og presenterer resultatet før detaljering.
* Laget designforslaget «O-kartet» som to HTML-skisser: en landingsside med innlogging, utregning, tillitsmerker og «Prøv selv», og en produktoversikt (dashboard) med alle 30 testprodukter sortert etter reglene i PRD-en. Fargene, skriften (Albert Sans) og symbolene for utsolgte uker, uvanlige uker og nytt nivå er beskrevet i `visual-design.md`.
* Kontrollerte skissene med Impeccable-detektoren og et eget kontrollskript: alle faste tekster fra PRD-en er med, all tekst har kontrast etter WCAG AA, og det er ingen JavaScript. Skissene er ikke kontrollert i nettleser, fordi en test med Chrome skrev utenfor prosjektmappen og derfor ble stoppet.
* Ingenting er committet eller pushet.

**Status:** Det visuelle designet er klart til min vurdering og er ikke godkjent ennå. Etter godkjenning kommer detaljeringen i BMAD (produktsiden, samlet bestillingsoversikt, `DESIGN.md` og `EXPERIENCE.md`), og deretter arkitekturen.

### 7. november 2026 – Forbedringer av designet

* Så på skissene i nettleseren og ba om fem forbedringer:
  * en mye mindre varseltrekant;
  * en kortere landingsside uten gjentakelser;
  * en tydeligere innlogging;
  * interne designnotater adskilt fra sidene brukerne ser;
  * bedre tilpasning til mobil.

  Farger, grafer, hovedstruktur og designretning skulle beholdes, og det skulle ikke komme nye funksjoner.
* Eksempel på styring av KI: Den store varseltrekanten var en feil i CSS-koden fra KI, der en regel for grafen også traff ikonet. Feilen ble funnet og rettet etter min tilbakemelding.
* Claude gjorde endringene med BMAD UX og Impeccable (`adapt` for mobil og `distill` for kortere tekst):
  * Forhåndsvisningen av produktoversikten og gjentatte utregninger er fjernet fra landingssiden.
  * Innloggingen har fått en egen knapp i toppen og en tydeligere boks.
  * Designnotatene ligger nå i en egen intern fil.
  * Grafer og tabeller har egne mobilversjoner.
* Impeccable-detektoren fant ingen feil på de to skjermene etter endringene. Ingen filer er slettet, og ingenting er committet eller pushet.

**Status:** Det oppdaterte designet er klart til min vurdering.

### 7. november 2026 – UX-fasen fullført

* Godkjente begge skjermene (landingssiden med innlogging og produktoversikten) og ba Claude fullføre UX-fasen med BMAD og Impeccable uten å endre det godkjente designet.
* Claude skrev UX-dokumentene `DESIGN.md` og `EXPERIENCE.md` og satte dem til `final`. De beskriver farger, skrift, komponenter, tilstander, tilgjengelighet og tilpasning til skjermstørrelser. De har også enkle skisser (wireframes) av produktsiden og samlet bestillingsoversikt, og hovedflyten UJ-1.
* De godkjente skissene ble kopiert til mappen `mockups/`.
* Kontroller:
  * BMAD sin dekningskontroll;
  * avstemming mot PRD-en, der ingen krav falt bort;
  * en uavhengig gjennomgang av struktur og språk, der alle rettingene ble tatt inn;
  * Impeccable-detektoren, som ikke fant noe på skissene.
* Eksempel på styring av KI: Gjennomgangen fant at mobilfilteret var beskrevet med feil bruddpunkt (640 px i stedet for 560 px), og at grafbeskrivelsen ikke passet med Chart.js. Begge ble rettet i dokumentene, uten å endre designet.
* Claude foreslo hvilke filer som kan slettes. Etter min godkjenning og en kontroll av at kopiene var identiske, ble verktøycachen, de uferdige agentfilene og de doble kopiene slettet. Ingenting er committet eller pushet.

**Status:** UX-fasen er ferdig. Neste steg er arkitektur (`bmad-architecture`).

### 8. november 2026 – Arkitektur

* Kjørte `bmad-architecture` på rask vei med den godkjente PRD-en og UX-designet som grunnlag. Leveransen er én arkitekturspine som byggeunderlag.
* Mine valg:
  * Django + SQLite;
  * Django 5.2 LTS med Python 3.13 i stedet for nyeste Django 6.1;
  * `runserver` brukes bare lokalt;
  * justeringer lagres i økten, og alle produkter beregnes ved hver visning;
  * en enkel arkitektur som kan videreutvikles, og fristen prioriteres.
* Spinen har 14 arkitekturbeslutninger. Beregningsreglene ligger i en ren Python-kjerne uten Django, all bedriftsisolasjon går gjennom én spørremodul, og det er én testkommando og én fasit. Versjonene ble sjekket mot primærkildene.
* Eksempel på styring av KI: Claude foreslo nyeste Django 6.1. Jeg valgte heller langtidsversjonen 5.2 for stabilitet frem mot fristen.
* Etterpå ba jeg Claude sjekke om Django 5.2 kan publiseres på Vercel. Ifølge dokumentasjonen til Vercel går det, men det er ikke testet med en faktisk publisering ennå. SQLite beholdes lokalt, og PostgreSQL (Neon sin gratisplan) er planlagt for valgfri publisering etter må-ha. Arkitekturen fikk en ny beslutning (AD-15): miljøvariabelen `DATABASE_URL` bestemmer hvilken database som brukes.
* Så bestemte jeg at Vercel skal være publiseringsløsningen, ikke bare et valg. PRD-en fikk et nytt leveransekrav (DR-10) og et nytt suksessmål (SM-9). Arkitekturen fikk en ny beslutning (AD-16): bare `main` publiseres, og databaseendringer kjøres av eieren fra egen PC. Den første storyen publiserer et prosjektskjelett, slik at publiseringen blir prøvd ut tidlig.

**Status:** Arkitekturen er ferdig (`final`). Neste steg er epics og stories (`bmad-create-epics-and-stories`).

### 8. november 2026 – Epics og stories

* Kjørte `bmad-create-epics-and-stories` med godkjent PRD, UX og arkitektur som grunnlag, med må-ha og fristen først.
* Resultatet er 7 epics og 29 stories i `_bmad-output/planning-artifacts/epics.md`. Epic 1–4 er må-ha, og epic 5–7 er bør-ha, med kan-ha sist. Den første storyen publiserer prosjektskjelettet på Vercel.
* Eksempel på styring av KI: jeg ba Claude sjekke at addendumet var dekket. Kontrollen fant fire punkter fra addendumet og PRD §10 som manglet i kravlisten, og de ble lagt til uten nye funksjoner. Sluttkontrollen fant også to stories som viste til senere stories, og de ble rettet.

**Status:** Epics og stories er ferdige. Neste steg er sprintplanlegging (`bmad-sprint-planning`).

### 8. november 2026 – Sprintplanlegging

* Kjørte `bmad-sprint-planning`. Klarhetskontrollen fant at story 1.1 manglet en kilde for den lokale sesjonshemmeligheten. Jeg valgte å rette storyen før sprintplanen ble laget, og endringen står i endringsloggen i `epics.md`.
* Sprintplanen ligger i `_bmad-output/implementation-artifacts/sprint-status.yaml`. Milepæler: epic 1 innen 11. november, epic 2 innen 18. november, epic 3 innen 21. november, bør-ha 22.–27. november, sluttkontroll 28.–30. november og innlevering 1. desember.

**Status:** Sprintplanen er klar. Neste steg er story 1.1 med `bmad-build`.

### 15. november 2026 – PRD etter lærerens tilbakemelding

* Hentet lærerens formative tilbakemelding på PRD-en (12. november) fra `main` med `git pull`. Læreren kalte PRD-en uvanlig sterk. Før videre arbeid ba læreren om:
  * en kutt-linje for publiseringen;
  * en avgrenset mengde tillatte tall i forklaringen;
  * én prioritet per FR.
* Kjørte `bmad-prd` i oppdateringsmodus på en egen gren, `prd/teacher-feedback`, og gikk gjennom alle punktene:
  * kutt-linje for publiseringen og gruppering av leveransekravene;
  * tillatte tall i forklaringen og plassholdere for språkmodellen;
  * FR-17 delt i FR-17 og FR-17b, og en tabell over prioritet og suksessmål per FR;
  * testbare konsekvenser i FR-24, FR-25 og NFR-6;
  * rekkefølgen på bør-ha-delene og et nytt suksessmål, SM-10, for at brukere forstår tillitsmerket;
  * presiseringer i ordlisten, R-16, SM-1 og SM-7.
* Kvalitetssikring: tre uavhengige agenter avstemte endringene mot tilbakemeldingen, vurderte PRD-en mot BMAD-rubrikken og sjekket konsistensen. 10 avvik ble rettet, og en struktur- og prosarunde ble lagt inn. Alle 30 referanseeksemplene stemmer fortsatt.
* Eksempel på styring av KI: Claude lot FR-24 følge det godkjente UX-designet, der årsaken står over tre kolonner, i stedet for lærerens eksempel. Jeg bestemte at FR-24 skal oppfylle lærerens funksjonelle krav: prognosekolonnen viser årsaken, og bestillingskolonnen viser «–». UX-en oppdateres senere.
* Jeg godkjente kutt-linjen, som er knyttet til datoen i sprintplanen for ferdig må-ha. Jeg godkjente også grupperingen av leveransekravene, begrunnelsen for rekkefølgen på bør-ha-delene, SM-10 og plassholderregelen.
* PRD-en er satt til `final` igjen og committet (`47a8857`).

**Status:** PRD-en er oppdatert. Neste steg er å oppdatere epics, arkitektur og UX etter endringene med `bmad-correct-course`.

### 15.–16. november 2026 – Nytt UX-design etter PRD-oppdateringen

* Bestemte at det gamle UX-designet og den gamle arkitekturen ikke skulle rettes, men lages på nytt fra den oppdaterte PRD-en. Laget grenen `design/after-prd-feedback` fra `main` og flyttet de gamle mappene til `_bmad-output/planning-artifacts/archive/` med en README, uten å slette historikken (`f28ca71`).
* Startet `bmad-ux` på nytt med PRD-en som eneste grunnlag og ba om tre tydelig ulike designkonsepter før noe endelig design:
  * A «Arket»: en tett tabell og et regneark;
  * B «Innkjøpsmøtet»: en guidet ukeflyt med kort;
  * C «Instrumentpanelet»: liste og detalj på én skjerm med en stor graf.
* Vurderte konseptene og valgte et fjerde, kombinert konsept D med en moderne palett i blått, turkis og grønt:
  * fra C: hovedoppsettet, produktlisten til venstre og den store prognosegrafen;
  * fra B: produktkort, tydelige bestillingsforslag og en enkel arbeidsflyt;
  * fra A: detaljerte beregninger, salgsdata og forklaringer.

  A, B og C beholdes uendret som dokumentasjon.
* Så D i Safari og ba om to forbedringer: grafen skulle stå rett under bestillingsforslaget og tillitsmerket, og bryteren under grafen skulle få normal størrelse.
* Eksempler på styring av KI:
  * Et skript fra Claude lukket en av mine faner i Safari. Jeg bestemte at Claude bare skal åpne filer med `open -a Safari`, og ikke styre faner eller vinduer.
  * Den enorme bryteren var en feil i CSS-koden fra KI: regelen som gjør grafen like bred som panelet, traff også bryteren da den ble flyttet inn i grafpanelet. Det er samme type feil som varseltrekanten 7. november. Den ble rettet med én CSS-linje etter min tilbakemelding, og en kontrollsum viste at ingenting annet var endret.
  * Jeg ba om at grafen skulle flyttes høyere. Claude forklarte at varslene må stå over grafen fordi FR-25 krever at de er synlige uten å rulle på en skjerm på 1366 × 768, så grafen kunne bare flyttes et stykke opp.
* Claude fant at forklaringsteksten i A, B og C bruker ukenummer som FR-27 ikke tillater, og at flere tekster avviker fra PRD-en. D bruker de nøyaktige tekstene fra PRD-en.
* Godkjente D og ba Claude fullføre BMAD UX uten nye designendringer uten behov og uten subagenter. Claude skrev `DESIGN.md` og `EXPERIENCE.md` og satte dem til `final`:
  * `DESIGN.md`: farger med målt kontrast, skrift, avstander, former og komponenter.
  * `EXPERIENCE.md`: skjermkart, enkle skisser av innloggingen og samlet bestillingsoversikt (PRD §0), norske tekster for alle varsler og merknader, atferd, tilstander, regler for beregninger og forklaring, tilgjengelighet og tre brukerflyter. Én av flytene viser at en person utenfor gruppen kan forklare tillitsmerket «lav» (SM-10).
  * D ble kopiert til `mockups/`.
* Ett avvik fra mockupen: PRD-en krever en markør i grafen for hver utsolgte uke, uvanlige uke og uke med nytt nivå (FR-15–FR-17). `EXPERIENCE.md` sier derfor at grafen viser hele salgshistorikken, mens mockupen bare viser de siste 12 ukene. Spinene gjelder ved avvik.
* Kontroller:
  * BMAD sin dekningskontroll (`review-coverage.md`);
  * en gjennomgang av struktur og språk med åtte rettinger;
  * maskinelle kontroller av token-henvisninger, lenker og komponentnavn;
  * Impeccable-detektoren;
  * et søk etter personopplysninger, lokale stier og hemmeligheter i alle filene som ble committet.

  BMAD sin gjennomgang med subagenter (Reviewer Gate) ble ikke kjørt, fordi jeg ba om at subagenter ikke skulle brukes.
* Oppdaterte henvisningene i endringsloggen i PRD-en (§12) og i README-en i arkivet. `epics.md` og `.impeccable/config.json` oppdateres når den nye arkitekturen finnes.
* Committet konseptene, UX-dokumentene og beslutningsloggen (`5db2fe7`) og pushet til `design/after-prd-feedback`. Ingenting er flettet til `main`.

**Status:** UX-designet er ferdig (`final`). Neste steg er en ny arkitektur (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – Beslutninger før arkitekturen

* Godkjente de fem antakelsene i UX-designet:
  * produkter uten prognose sorteres etter varenummer;
  * en bekreftelse sier «(uendret)» når en innstilling ikke endrer verdien;
  * samlet bestillingsoversikt viser «–» og «Uten prognose» for et produkt uten prognose, i samme rekkefølge som produktoversikten;
  * avrundingsnotat og faste desimaler ved eksponentiell glatting og sesongjustering;
  * årstall i ukelister.
* Bestemte at demoen skal vise effekten av uvanlige uker. Referanseeksempel E8 ble valgt, fordi det allerede står i PRD-en. Når uvanlige uker holdes utenfor, går grunnprognosen fra 41,0 til 21,3.
* Ønsket hele salgshistorikken i grafen hvis det er enkelt og innenfor PRD-en. Det er det: FR-25 sier allerede at grafen viser salgshistorikken, så PRD-en trengte ingen endring for dette.
* Tillot uke og år i PRD-en bare hvis det ikke påvirker andre krav. Kontrollen viste at bare FR-27 (tillatte tall i forklaringen) måtte endres. FR-28, SM-6, FR-15 og FR-16 virker som før, og ordlisten definerer allerede en uke med år og ukenummer.
* PRD-en ble oppdatert med `bmad-prd` i oppdateringsmodus. Endringene gjelder R-9, R-12, FR-27, FR-30, FR-35, DR-1 og ordlisten, og endringsloggen (§12) har fått fire nye rader. Statusen er fortsatt `final`.
* UX-dokumentene ble oppdatert med `bmad-ux` i oppdateringsmodus. Antakelsene er nå beslutninger med henvisning til PRD-reglene, flyt 1 bruker E8-demoen, og forklaringen kan nevne årstall. Mockupen er ikke endret.
* Filhenvisninger: `.impeccable/config.json` peker nå på de arkiverte mockupene. `epics.md` viser fortsatt til den arkiverte UX-en og arkitekturen og oppdateres etter den nye arkitekturen.
* Kontroller:
  * alle 17 faste norske tekster fra PRD-en står ordrett i UX-en;
  * de sju nye PRD-reglene stemmer med UX-en;
  * ingen antakelser står igjen;
  * YAML, token-henvisninger, lenker og JSON er gyldige;
  * det er ingen personopplysninger, lokale stier eller hemmeligheter i filene.
* Kvalitetssikring: Ett kontrollskript fra Claude meldte først «ingen funn» uten å ha lest filene, fordi skallet ikke delte opp fillisten. Claude oppdaget feilen før commit og kjørte kontrollen på nytt med riktig filliste.
* Committet og pushet til `design/after-prd-feedback`: endringene (`5373e7b`) og commit-hashen i endringsloggene (`220bd3b`). Ingenting er flettet til `main`.

**Status:** PRD-en og UX-designet er oppdatert og `final`. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – PRODUCT.md etter det nye UX-designet

* Oppdaterte `PRODUCT.md` i rotmappen etter den godkjente PRD-en og det nye UX-designet. Fila er produktkonteksten som Impeccable leser, og den beskrev fortsatt det arkiverte designet fra 6. november. Bare denne fila ble endret, og ingen nye krav eller funksjoner ble lagt til.
* Det som er nytt i fila:
  * kildene er PRD-en og de endelige `DESIGN.md` og `EXPERIENCE.md`, ikke arkivet;
  * appen kjører lokalt og som publisert versjon på Vercel med PostgreSQL, med kutt-linjen i PRD §8.1;
  * innloggingssiden er inngangen, så spørsmålet om en egen offentlig side er lukket;
  * må-, bør- og kan-ha følger PRD §8.1–8.3, også rekkefølgen på bør-ha-delene;
  * «Uten prognose», tallformat og avrunding (R-9), årstall i uker (FR-27), hele salgshistorikken i grafen og E8-demoen i «Prøv selv»;
  * språktonen fra `EXPERIENCE.md`. Farger og skrift står i `DESIGN.md` og gjentas ikke.
* Kontroller:
  * alle 18 siterte norske tekster står ordrett i PRD-en eller UX-dokumentene;
  * alle 55 krav-ID-er, seksjonene, ordlisteordene og stiene finnes;
  * listene over må-, bør- og kan-ha er like PRD §8.1–8.3;
  * Impeccable leser fila uten feil;
  * det er ingen personopplysninger, lokale stier eller hemmeligheter i endringen.
* Kvalitetssikring: Claude skrev først «för» i stedet for «for» i den faste teksten «Tallene er avrundet for visning.», og rettet det før kontrollen.
* Funn: Impeccable finner ikke den nye `DESIGN.md`, fordi den leter i rotmappen, mens fila ligger i UX-mappen. Det må løses før Impeccable brukes i byggingen.
* Committet (`e549c78`) og pushet til `design/after-prd-feedback`. Ingenting er flettet til `main`.

**Status:** `PRODUCT.md` samsvarer med PRD-en og UX-designet. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – Impeccable og DR-2 før arkitekturen

* Rettet to punkter før arkitekturen, uten å endre PRD-en eller det godkjente designet:
  1. **Impeccable fant ikke den godkjente `DESIGN.md`** og ville derfor lage et nytt visuelt design. Impeccable leter bare i rotmappen og i `docs/`, mens fila ligger i UX-mappen. Forsøk i en egen testmappe viste at `.impeccable/`-mappen ikke virker, og at Impeccable ikke har noen innstilling for stien. `docs/DESIGN.md` er nå en symbolsk lenke til den godkjente fila. Impeccable leser dermed originalen, og det finnes ingen kopi som kan bli ulik.
  2. **`PRODUCT.md` lå løst i rotmappen**, og det tillater ikke DR-2. Fila er flyttet til `docs/` med `git mv`, så historikken følger med. Rotmappen har nå bare filene `README.md`, `.gitignore` og `CLAUDE.md`.
* Kontroller:
  * `impeccable context` finner `docs/PRODUCT.md` og `docs/DESIGN.md` og ber ikke lenger om et nytt design;
  * Impeccable leste 28 986 tegn, som er den godkjente `DESIGN.md` uten det siste linjeskiftet;
  * `impeccable doctor` fant ingen avvik;
  * en ny klon av grenen ga samme resultat;
  * kontrollsummene viser at alle 38 filene i PRD- og UX-mappene er uendret;
  * innholdskontrollen av `PRODUCT.md` og personvernsøket fant ingen feil.
* Vær oppmerksom på:
  * Impeccable-kommandoer som skriver `DESIGN.md`, for eksempel `document` eller avslutningen av en bygging, vil enten skrive gjennom lenken til den godkjente fila eller erstatte lenken med en egen fil. Begge deler må godkjennes først og føres i endringsloggen til UX-en.
  * På Windows uten støtte for symbolske lenker i git blir `docs/DESIGN.md` en tekstfil med stien. Det påvirker bare Impeccable, ikke appen.
  * Story 4.1 i `epics.md` nevner `PRODUCT.md` som toppnivåfil, og README-en må forklare `docs/` (DR-2). Det rettes når `epics.md` oppdateres etter arkitekturen.
* Committet (`505d131`) og pushet til `design/after-prd-feedback`. Ingenting er flettet til `main`.

**Status:** Impeccable finner det godkjente designet, og rotmappen følger DR-2. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – Opprydding før arkitekturen

* Gikk gjennom prosjektmappa og foreslo hva som skulle beholdes, arkiveres eller slettes. Etter min beslutning ble bare trygge rettelser gjort: ingen filer er slettet, ingen grener er flettet, og historikken er ikke skrevet om. Designkonseptene A–D og all dokumentasjon er beholdt.
* Secret key (DR-2, NFR-3):
  * Ingen gren har noen gang committet `.secret_key`, databasen eller `.env`. Koden på story-grenen har ingen innebygd nøkkel.
  * `.gitignore` på denne grenen manglet `.secret_key` og `db.sqlite3`. Fila har nå samme blokk som story-grenen (PR #1), byte for byte, så den gir ingen konflikt når grenene flettes.
  * Alle DR-2-punktene for `.gitignore` er kontrollert med eksempelstier, og seed-dataene blir fortsatt versjonert.
* Rettet datoen i arkivets README. PRD-en ble sist oppdatert 16. november, og bare oppdateringen fra 15. november er i `main`.
* Prøvefletting av grenene i en isolert kopi:
  * `design/after-prd-feedback` kan flettes inn i `main` uten konflikt.
  * PR #1 (story 1.1) har allerede konflikt med `main` i `.logs/mounia-tech03/issues.md` og `docs/arbeidslogg.md`. Begge sider har lagt til oppføringer på samme sted. Det kan forebygges ved å oppdatere PR #1 med `main`, men det er en fletting og krever godkjenning.
* Kontroller:
  * Filhenvisninger: bare `epics.md` har brutte henvisninger, og den venter på arkitekturen.
  * Personvern: ingen lokale stier, brukernavn, e-postadresser, nøkler eller tokens i noen fil på noen gren eller i historikken. To database-adresser på story-grenen er falske testverdier.
  * 58 commits har en automatisk forfatter med brukernavn og maskinnavn. Det kan bare rettes ved å skrive om historikken, og det er ikke gjort.
* Committet (`d67211c`) og pushet til `design/after-prd-feedback`. Ingenting er flettet til `main`.

**Status:** De trygge rettelsene er gjort. Det som gjenstår, krever godkjenning eller arkitekturen. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – Personvern, Git-identitet og flytting av sesjonsloggene

* Kontrollerte personvern og Git-identitet, og skilte mellom tillatte navn i dokumentasjonen og personopplysninger som bryter NFR-4:
  * **Tillatt:**
    * «Mounia» som persona i PRD-en og UX-en. Det er en oppdiktet rolle, og navnet valgte jeg selv.
    * Fullt navn i medlemslisten i README.
    * GitHub-navnet «Mounia-03» i BMAD-konfigurasjonen.
    * Lærerens navn i lærerens egne commits.
  * **Gråsone:** det gamle brukernavnet i loggene, som er første del av en privat e-postadresse, sto i navnet på loggmappa og i 12 overskrifter i sesjonsloggene.
  * **Bryter NFR-4:** 61 gamle commits har fullt navn, macOS-brukernavn og maskinnavn, og flettecommiten som GitHub laget for PR #2, har skoleadressen min. Dette står bare i Git-historikken, ikke i filene.
* Satte Git-identiteten for nye commits i dette repoet: `Mounia-03` med GitHubs noreply-adresse. Claude spurte meg først, og jeg valgte navnet og adressen. Gamle commits er ikke endret. Det ville krevd force-push og gjort alle commit-hashene i PRD-en, UX-en og loggene ugyldige. De gamle identitetene skal i stedet beskrives i QA-loggen ved innlevering (NFR-4, DR-9).
* Flyttet sesjonsloggene fra `.logs/mounia-tech03/` til `.logs/mounia-03/` med `git mv`. Sesjonslogg-skillen bruker git-navnet, så nye logger havner i samme mappe som de gamle. Det gamle brukernavnet er byttet til «Mounia-03» i de 12 overskriftene.
* Kontroller:
  * alle 12 filene er omdøpt, ingen er slettet, og bare de 12 overskriftslinjene er endret;
  * `git log --follow` viser hele historikken;
  * det gamle brukernavnet finnes ikke lenger i overskriftene eller i noen annen fil.
* Prøvefletting i en isolert kopi: designgrenen kan fortsatt flettes inn i `main` uten konflikt. Flettes PR #1 etterpå, legger git loggene 991 og 992 fra story-grenen i den nye mappa, men ber om bekreftelse. Det kommer i tillegg til de to konfliktene som fantes fra før.
* Henvisningen til den gamle mappa i oppføringen om oppryddingen er beholdt. Den beskriver PR #1 mot `main`, der mappa fortsatt har det gamle navnet.
* Committet (`6245a0a`) og pushet til `design/after-prd-feedback`. Ingenting er flettet eller slettet.

**Status:** Nye commits har en identitet uten privat e-post, og sesjonsloggene ligger i én mappe. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – Arkivering av gamle epics, sprintplan og kode

* Arkiverte den gamle planen og koden før den nye arkitekturen, uten å slette noe, flette grener eller skrive om historikken:
  * `epics.md` og `sprint-status.yaml` er flyttet med `git mv` til `archive/epics-G40-lyamouri-2026-11-08/`. De bygger på den arkiverte UX-en og arkitekturen og på PRD-en før lærerens tilbakemelding, og den første milepælen i sprintplanen (11. november) er passert. Nye epics og ny sprintplan lages etter den nye arkitekturen.
  * Den gamle koden fra story 1.1 ligger ikke på designgrenen. Det er Django-skjelettet som ble bygget 10.–11. november på den arkiverte arkitekturen. Det er bevart uendret i grenen `story/1-1-project-skeleton` (PR #1) og i den nye taggen `archive/story-1-1-project-skeleton`. Der ligger også story-dokumentene, sesjonsloggene 991–992 og arbeidsloggoppføringene for 10. og 11. november.
  * Arkivets README forklarer hva som er arkivert og hvor koden ligger. Den sier også at koden ikke er grunnlag for den nye arkitekturen.
* Kontroller:
  * 404 sporede filer før og etter, de to filene er flyttet uendret, og ingen er slettet;
  * `git log --follow` viser historikken til de flyttede filene;
  * taggen har nøyaktig samme 417 filer som story-grenen, også koden og story-dokumentene;
  * ingen dokumenter som er i bruk, peker på de gamle stiene;
  * designgrenen kan fortsatt flettes inn i `main` uten konflikt.
* Fem åpne punkter fantes bare på story-grenen. Ett er løst (noreply-adressen), og de som kan gjelde den nye byggingen, er ført inn i `issues.md`.
* Kvalitetssikring: Claude skrev først i arkivets README at sprintplanens datoer var passert. Bare den første milepælen var det, og setningen er rettet.
* Committet (`8f58dfb` og `652f747`) og pushet grenen og taggen til GitHub. PR #1 og story-grenen er ikke endret.

**Status:** Den gamle planen og koden er arkivert. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – PR #1 lukket, arbeidslogg arkivert og lokale rester slettet

* Godkjente de tre forslagene fra arkiveringen:
  1. **PR #1 er lukket uten fletting.** Kommentaren sier at den gamle koden er arkivert i taggen `archive/story-1-1-project-skeleton` og ikke brukes i den nye arkitekturen. Grenen `story/1-1-project-skeleton` er beholdt.
  2. **Arbeidsloggoppføringene fra 10. og 11. november** (story 1.1 og GitHub CLI) er kopiert ordrett fra taggen til `archive/story-1-1-G40-lyamouri-2026-11-10/arbeidslogg.md`. Arkivets README viser til dem.
  3. **De gamle lokale filene er slettet etter kontroll:** `__pycache__` i fem gamle appmapper (19 `.pyc`-filer, og mappene som ble tomme), `.venv` (93 MB) og `db.sqlite3`.
* Kontroller før slettingen:
  * alle 19 `.pyc`-filene har kildekoden sin i taggen, og ingen av filene har noen gang vært committet;
  * `.venv` har de samme pakkene som `requirements.txt` i taggen og kan lages på nytt;
  * `db.sqlite3` hadde bare Djangos skjema og ingen data, og kan lages på nytt med `migrate`;
  * ingenting på denne grenen bruker `.venv` eller databasen.
* Kontroller etter slettingen: git er uendret (404 sporede filer), og BMAD-skriptene virker fortsatt uten `.venv`. `.secret_key`, `.ruff_cache`, `_bmad/render` og `.DS_Store` er beholdt, fordi de ikke var med i forslaget.
* Kvalitetssikring: én kontrollkommando fra Claude feilet, fordi macOS-versjonen av `sed` ikke godtok skrivemåten. Ingenting ble committet da, og kontrollen ble gjort på nytt med Python.
* Committet (`1a0709e`) og pushet til `design/after-prd-feedback`. Ingen grener er flettet.

**Status:** Den gamle planen og koden er arkivert, og PR #1 er lukket. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 16. november 2026 – Oppryddingen fullført

* De første delene av oppryddingen samme dag står i de fire oppføringene over. Her står bare den siste delen.
* Undersøkte de siste lokale filene og grenen `prd/teacher-feedback` før noe ble slettet:
  * `.secret_key` ble laget av `load_seed` i story 1.1, og bare den arkiverte koden bruker den. Ny kode lager en ny nøkkel automatisk (NFR-3).
  * `.ruff_cache/` og de to `.DS_Store`-filene er mellomlager og Finder-innstillinger som lages på nytt.
  * `_bmad/render/bmad-build/` er BMADs mellomlager for skillen fra story 1.1.
  * `_bmad/render/bmad-review/` hadde de eneste kopiene av to mellomutkast av PRD-en fra 15. november.
  * `prd/teacher-feedback` er flettet gjennom PR #2, og alle commitene ligger i `main`.
* Arkiverte de to PRD-utkastene før slettingen. De er flyttet uendret til `archive/prd-drafts-G40-lyamouri-2026-11-15/`, committet og pushet (`d2bfad2`). Kontrollen viste:
  * samme kontrollsum som før flyttingen, og identiske filer på GitHub;
  * at begge diffene gir nøyaktig de opprinnelige utkastene når de brukes på PRD-versjonen de bygger på.
* Slettet etter min godkjenning:
  * `.secret_key`, `.ruff_cache/` og de to `.DS_Store`-filene;
  * `_bmad/render/bmad-build/` og den tomme `bmad-review`-mappa;
  * grenen `prd/teacher-feedback`, lokalt og på GitHub. Den kan gjenopprettes fra PR #2-siden.
* Beholdt:
  * BMAD-konfigurasjonen og BMAD-mappene;
  * `.claude/settings.local.json`;
  * Impeccable-motoren og mellomlageret dens;
  * story-grenen med arkivtaggen.
* Kontroll av BMAD og Impeccable etter oppryddingen:
  * BMAD-skriptene virker, også oppsettet for `bmad-architecture`;
  * `impeccable context` finner `docs/PRODUCT.md` og den godkjente `docs/DESIGN.md` uten å be om nytt design;
  * git sporer 407 filer, og arbeidsmappa er ren;
  * GitHub har bare grenene `design/after-prd-feedback`, `main` og `story/1-1-project-skeleton`.
* Kvalitetssikring: den første slettekommandoen fra Claude stoppet før noe ble slettet, fordi sikkerhetssjekken var feil skrevet. Claude kontrollerte at alt fortsatt fantes, og kjørte kommandoen på nytt med riktig sjekk.
* Committet (`d2bfad2`) og pushet til `design/after-prd-feedback`. Ingen grener er flettet.

**Status:** Oppryddingen før arkitekturen er fullført. Disse punktene gjenstår:
* beskrive de gamle commit-identitetene i QA-loggen;
* slå på e-postinnstillingen på GitHub;
* vurdere punktene fra story 1.1 i arkitekturen.

Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 17. november 2026 – QA-logg for Git-identitetene

* Undersøkte hvor QA-loggen (DR-9) skal ligge. Det fantes ingen QA-logg fra før. PRD-en lar arkitektursteget fastsette mappene (DR-2), og den arkiverte arkitekturen la QA-loggen i `docs/` sammen med de andre prosessdokumentene.
* Opprettet `docs/qa-logg.md` som eneste nye fil. Den første oppføringen beskriver de gamle Git-forfatteridentitetene og hvorfor commit-historikken er bevart (NFR-4). Detaljene står bare i QA-loggen.
* Kontroll: fila har ingen adresser, brukernavn eller maskinnavn. Alle krav-ID-er, stier, taggen og commitene den viser til, finnes.
* Committet (`99796e5`) og pushet til `design/after-prd-feedback`.

**Status:** QA-loggen har sin første oppføring, og den nye arkitekturen må bekrefte plasseringen. Neste steg er arkitekturen (`bmad-architecture`), som ikke er startet.

### 17. november 2026 – Ny arkitektur med PostgreSQL

* Startet `bmad-architecture` på designgrenen. Grunnlaget var den godkjente PRD-en, UX-designet og lærerens `technology.md`. Claude leste også `issues.md` og den arkiverte arkitekturen, men gjenbrukte den ikke ukritisk. Flere deler av den var utdatert:
  * skrifttypen Albert Sans;
  * grafbiblioteket Chart.js;
  * den gamle tallkontrollen i forklaringen.

  I tillegg la den nettverkskode i en modul som den selv forbød nettverkskode i.
* Godkjente anbefalingene P1–P10:
  * Django 5.2 LTS med en ren beregningskjerne;
  * uv og pytest;
  * grafen som SVG laget på serveren;
  * Neon for publisering og GitHub Actions for testene;
  * koden i `src/`;
  * regnearket som eneste fasit;
  * PostgreSQL lokalt med Docker Compose.

  P6, om migrering og seed-data i byggesteget på Vercel, ble godkjent med et forbehold.
* Eksempler på styring av KI:
  * Claude foreslo først SQLite lokalt og PostgreSQL bare på Vercel, slik PRD-en sa. Jeg bestemte at PostgreSQL er et krav i begge kjøremodusene, fordi det er mer langsiktig. Claude skulle undersøke konsekvensene for PRD-en før noe ble endret.
  * Jeg godkjente automatisk migrering og seed-data på Vercel bare med et forbehold: ingenting skal slette eller overskrive brukerdata automatisk. Derfor ble arkitekturen og PRD-en (DR-4 og DR-10) endret:
    * byggesteget migrerer bare når endringene bare legger til;
    * `load_seed` laster bare inn i en tom database;
    * bare en tilbakestilling som brukeren bekrefter, sletter data.
  * Jeg ville ha Docker-løsningen bekreftet før godkjenningen. Claude skilte mellom det som var dokumentert, målt og ikke testet. Claude fant også at porten 54320 kan være reservert på Windows, så porten ble endret til 15432.
* Installerte Docker Desktop 4.99.0 fra Dockers offisielle kilde etter godkjenning. Claude kontrollerte signaturen og notariseringen før installasjonen.
* Testet PostgreSQL 18.7 med en midlertidig `compose.yaml` utenfor prosjektet. Resultatet står i `docs/qa-logg.md`. Oppstart uten nett og oppsett på Windows er ikke testet.
* Kvalitetssikring: Claude prøvde å teste PostgreSQL fra en Python-pakke uten Docker. Tillatelsessystemet stoppet det, og Claude prøvde ikke å omgå det.
* Oppdaterte dokumentene:
  * PRD-en: FR-4, NFR-1–3, NFR-9, DR-1, DR-2, DR-4, DR-10, SM-2, SM-5 og §10, med tre nye rader i §12;
  * addendum §2;
  * `EXPERIENCE.md`, med feilsidene og en rad i endringsloggen;
  * én linje i `DESIGN.md`;
  * `docs/PRODUCT.md`;
  * arkivets README, der tre utsagn var blitt utdatert. Det ble oppdaget i sluttkontrollen før commit.
* Claude skrev arkitekturspinen med 17 beslutninger (AD-1–AD-17) og et kort notat til læreren om hvordan `technology.md` er tilpasset.
* Kontroll: Claude gjorde gjennomgangen selv, uten subagenter, slik jeg ba om. Kontrollskriptet fant ingen feil, og 12 hull og mangler i spinen ble lukket.
* Sluttkontroll før commit: Claude viste de åpne punktene og endringene i DR-4 og DR-10. Claude kontrollerte også samsvaret og personvernet i de 14 filene og fant ingen private opplysninger.
* Godkjente arkitekturen og dokumentendringene. Committet de 14 kontrollerte filene (`1441c40`) og commit-hashen i endringsloggene (`c76d6cd`), og pushet til `design/after-prd-feedback`. Ingenting er flettet til `main`.

**Status:** Arkitekturspinen er `final` og committet. Neste steg er nye epics og stories (`bmad-create-epics-and-stories`), som ikke er startet.

### 18. november 2026 – Nye epics og stories og kontroll mot sensorveiledningen

* Kjørte `bmad-create-epics-and-stories` på designgrenen. Grunnlaget var PRD-en med addendumet og lærerens tilbakemelding, arkitekturspinen med teknologinotatet, `DESIGN.md`, `EXPERIENCE.md` og `issues.md`. Jeg godkjente hvert steg og hver epic med presiseringer.
* Resultatet er `epics.md` med status `draft`: 8 epics og 39 stories (28 må-ha, 6 bør-ha og 5 kan-ha), og avklaringene D-1 til D-8. Arkitekturspinen, `EXPERIENCE.md` og `DESIGN.md` ble justert der storyene og gjennomgangen krevde det.
* Viktigste beslutninger:
  * publiseringen på Vercel er story 1.9, rett etter story 1.8 og før epic 2, slik at sensor får en fungerende nettside; kutt-linjen er bare reserven;
  * Windows- og offline-testen er story 1.3 på jobb-PC-en, og ingen av dem blokkerer annen utvikling;
  * story 4.1–4.3 kommer før bør-ha, og story 4.4 sist;
  * forventede resultater hardkodes aldri i tester eller beregningskode;
  * hver bør-ha-story kan bygges alene, og justerte mengder endrer aldri prognosene eller R-12-sorteringen;
  * språkmodellen er valgfri og lokal, og NFR-8 er uendret (D-7).
* BMAD Review, med linsene adversarial og edge case i hovedtråden uten subagenter, fant 29 feil og mangler (A1–A14 og E1–E15) i `epics.md`, arkitekturspinen og `EXPERIENCE.md`. Jeg godkjente at alle ble rettet.
* Kontrollerte planen mot hele sensorveiledningen for del 1, som jeg limte inn. Kontrollen fant åtte mangler som kunne påvirke karakteren. Seks av dem ble lagt inn i `epics.md`, uten nye stories eller funksjoner:
  * en rutine for å eksportere relevante Claude Code-økter per story med `/export`, med personvernsjekk, og for å føre KI-feil og rettelser i KI-styringsloggen og QA-loggen; planleggingsfasen dokumenteres fra arbeidsloggen, memloggene og sesjonsloggene, uten rekonstruerte prompts;
  * `issues.md` er prosjektets oversikt over feil og åpne punkter, og README-en skal lenke til den og forklare bruken;
  * hver ferdige story gjennomgås med BMAD Code Review, og funn, beslutninger og rettelser dokumenteres i pull requesten med commits; ingen ekstra person kreves (D-8);
  * README-en skal ha den publiserte adressen øverst, programmene med versjoner, installasjonen, testkommandoene og forventet oppsettstid med Docker;
  * README-en skal forklare avgrensningen til modul 4.1 med lenke til Product Brief og lærerens tilbakemelding;
  * README-en skal vise hvilke skjermstørrelser og nettlesere som faktisk er testet.

  Punkt 2, at planarbeidet ikke er flettet inn i `main`, venter på at jeg godkjenner commit. Punkt 5, commits spredt over tid, dekkes av regelen om små commits som pushes underveis.
* Bestemte at nettsiden også skal fungere på mobil og iPad. Claude vurderte først NFR-6, PRD-en, UX og arkitekturen uten å endre noe. Deretter ble NFR-6 i PRD-en, `EXPERIENCE.md`, `DESIGN.md` og `epics.md` oppdatert:
  * minste bredde 320 px, uten sidelengs rulling;
  * én kolonne fra 900 px og nedover, med produktet øverst og produktlisten under;
  * grafen og brede tabeller ruller i egen ramme, og utregningslinjene brytes mellom leddene;
  * trykkflater på minst 44 × 44 px og 16 px tekst i skjemafelt på berøringsskjerm;
  * iPhone 13 testes på ekte telefon på den publiserte adressen, mens iPad og Android testes i nettleserens responsive visning, og de to typene test føres hver for seg.

  Arkitekturen er uendret.
* Eksempler på styring av KI:
  * Claude foreslo 15 stories i epic 2. Jeg ba om å slå sammen tre par for å få færre pull requests, og om å beholde alle akseptansekriteriene og testene.
  * Jeg ba Claude kontrollere unntaket fra NFR-8 mot PRD-en og addendumet før kravet eventuelt ble endret. NFR-8 ble beholdt uendret.
  * Claude vurderte først GitHub Issues (A5) ut fra sammendraget av sensorveiledningen. Etter at jeg limte inn hele sensorveiledningen, ble merknaden rettet: den godtar «issues eller tilsvarende».
  * Claude foreslo å lenke til «lærerens godkjenning av avgrensningen». Jeg ba om at ingenting skulle påstås godkjent uten dokumentasjon. Kontrollen viste at lærerens tilbakemelding fra 6. oktober er en vurdering («Avgrensningen er klok»), og at godkjenningen 14. oktober var min egen godkjenning av briefen.
  * Claude anbefalte at README-en skulle si at appen bare er laget for PC. Jeg bestemte i stedet at nettsiden også skal fungere på mobil og iPad.
* Sluttkontroll før commit:
  * alle 39 stories er beholdt, og alle krav er dekket av minst én story;
  * de 29 rettingene står fortsatt;
  * henvisningene, tabellene og mobilkravene stemmer i de fire dokumentene;
  * `lint_spine.py` fant 0 feil, og personvernskanningen fant ingenting.

  Kontrollen fant to avvik: teststørrelsen 1366 × 768 i `EXPERIENCE.md`, og NFR-2 i «Also covers» for epic 2. Jeg godkjente forslagene:
  * PC-størrelsen testes i nettlesere på PC;
  * NFR-2 er lagt til i story 2.6;
  * NFR-6 og UX-DR7 er lagt til i «Also covers» for epic 1, 3 og 4.

  `issues.md` er oppdatert med de åpne punktene.
* Godkjente de åtte filene etter sluttkontrollen. Claude kontrollerte filene som ble staget, og personvernskanningen av linjene som ble lagt til, fant bare to falske treff. Committet de åtte filene (`9dee8b1`) på `design/after-prd-feedback`. Fylte deretter inn commit-hashen i endringsloggene i `epics.md`, PRD-en, arkitekturspinen og `EXPERIENCE.md` i en egen commit (`7d7c970`).
* Godkjente `epics.md` som `final`. Status og innledningen til endringsloggen ble oppdatert, sammen med arbeidsloggen, sesjonsloggen og `issues.md`, i en egen liten commit (`cfdefff`).
* Godkjente push. Claude kontrollerte remoten, forfatterne og linjene som ble pushet, og personvernskanningen fant 0 treff. Pushet `design/after-prd-feedback` med `9dee8b1`, `7d7c970` og `cfdefff` til GitHub, som har samme commit som lokalt.
* Opprettet PR #3 mot `main`:
  * den hadde 43 commits og 65 filer, og kunne flettes uten konflikter;
  * den har ingen automatiske tester, fordi GitHub Actions først kommer i story 1.2;
  * 18 eldre commits har den gamle Git-identiteten, og flettingen tok dem med inn i `main` (QA-loggen, NFR-4).
* Loggene med pushen og PR #3 ble committet (`22e32d9`) og pushet til samme gren. PR #3 fikk dermed 44 commits og kunne fortsatt flettes uten konflikter.
* Godkjente flettingen av PR #3. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `8f0bb14` har den gamle `main` (`87d9abc`) og PR-hodet (`22e32d9`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * etter pushen av `main` viser GitHub PR #3 som flettet 18. november kl. 22.12, med `8f0bb14` som merge-commit;
  * grenen `design/after-prd-feedback` er beholdt.

**Status:** Planarbeidet er flettet inn i `main` (`8f0bb14`), og `epics.md` er `final`. Neste steg er sprintplanlegging (`bmad-sprint-planning`).

### 19. november 2026 – Publisering tatt ut av v1

* Godkjente flettingen av PR #4, som inneholdt loggene for flettingen av PR #3. Claude flettet lokalt med «Create a merge commit» og noreply-adressen (`fd422d0`) og pushet `main`.
* Læreren avklarte på Canvas 19. november 2026 at publisering ikke er obligatorisk. Applikasjonen kan kjøres lokalt, men README.md må forklare hvordan den startes og hvilke API-nøkler som trengs. Beskjeden er gjengitt med egne ord, uten personopplysninger og ikke som ordrett sitat, i `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/avklaring-publisering-2026-11-19.md`.
* Claude undersøkte, uten å endre filer, hvilke krav, stories og dokumenter som ble berørt. Publiseringen var nevnt i ni filer, mest i `epics.md`, arkitekturspinen og PRD-en. NFR-1, SM-2 og FR-28 sa allerede at ingen API-nøkler trengs, men ingen story krevde at README-en sier det rett ut.
* Godkjente anbefalingen:
  * Vercel og Neon tas ut av v1, og story 1.9 fjernes, så epic 1 har 8 stories og planen 38;
  * Prognose har bare lokal kjøremodus, og testen på ekte iPhone 13 gjøres over det lokale nettverket med den valgfrie variabelen `PROGNOSE_LAN_HOST`, første gang i story 1.8;
  * README-en skal øverst forklare hvordan Prognose startes lokalt, og ha en egen del «Nøkler og hemmeligheter» om at ingen API-nøkler, betalte tjenester eller kontoer trengs.
* Oppdaterte PRD-en, addendumet, arkitekturspinen, teknologinotatet, `EXPERIENCE.md`, `docs/PRODUCT.md`, `epics.md` og `issues.md`, med rader i endringsloggene:
  * DR-10, SM-9, AD-16 og D-1 står igjen som historikk, merket som ikke i v1;
  * alle dokumentene er fortsatt `final`;
  * i `docs/PRODUCT.md` ble også linja om miljøet rettet, fordi den fortsatt sa at appen bare er for PC.
* Kontroll:
  * 38 stories, og alle krav er dekket, unntatt SM-9, som ikke er i v1;
  * rettingene fra BMAD Review står, unntatt A14, som gjaldt tilbakestillingen av den publiserte databasen i story 1.9;
  * «Also covers» stemmer for alle epicene, `lint_spine.py` fant 0 feil, og personvernskanningen fant ingenting.
* Godkjente dokumentendringene og de to små tilleggene: README-en kan beskrive mobiltesten over lokalt nett som et valgfritt steg, og linja om miljøet i `docs/PRODUCT.md` er rettet. Endringene committes samlet på en egen gren og sendes som pull request mot `main`, som først flettes når jeg godkjenner det.

**Status:** Publiseringen er tatt ut av v1, og planleggingsdokumentene er oppdatert. Neste steg er å flette pull requesten når jeg godkjenner den, og deretter sprintplanlegging (`bmad-sprint-planning`).

### 19. november 2026 – Implementation Readiness og sprintplan

* PR #5 er flettet inn i `main` med merge-commiten `5445a2f`, og GitHub viser den som flettet 19. november kl. 19.23.
* Kjørte `bmad-help`. Planleggingen er ferdig, og neste påkrevde steg var sprintplanlegging.
* Kjørte kontrollen av Implementation Readiness i `bmad-sprint-planning`. Claude endret ingen filer under kontrollen, og resultatet ble CONCERNS:
  * alle 37 FR og alle NFR, AG, DR, SM og UX-DR er dekket av minst én story, unntatt SM-9, som ikke er med i v1, og ingen story avhenger av en senere story;
  * milepælene manglet et sted å stå, fordi `sprint-status.yaml` bare har statuser;
  * det sto igjen tekst fra publiseringen i `epics.md` og addendumet, blant annet AD-16 i story 5.1 og 8.2;
  * arkitekturspinen sa både `uv sync` og `uv sync --locked`;
  * story 1.8 bruker `forecasting/display.py` før story 2.3 lager den.
* Godkjente sprintplanen med milepælene M0–M6, testdatoer, rekkefølge og reserverekkefølge:
  * innleveringsfristen er 8. desember 2026 kl. 23.59, ikke 1. desember;
  * jeg jobber 5–6 timer hver dag, også i helgene;
  * Windows-PC-en er tilgjengelig 25. november og 7. desember;
  * SM-10 gjennomføres 3.–4. desember, etter at SM-3 har bestått, uten unntak fra PRD-en;
  * alle må-ha-stories prioriteres, reserverekkefølgen gjelder ved forsinkelse, og story 4.4 kommer sist;
  * rettinger etter sluttkontrollen 7. desember gir en ny endelig versjon, som kontrolleres på nytt.
* Claude laget `sprint-plan.md`, og med sprintskriptet `sprint-status.yaml` med 8 epics og 38 stories, i `_bmad-output/implementation-artifacts/`.
* Claude førte den nye fristen inn i PRD-en, `epics.md`, addendumet og teknologinotatet, og rettet funnene fra kontrollen, med rader i endringsloggene. AD-15 ble kontrollert som riktig henvisning i story 5.1 og 8.2.
* Kontroll:
  * `lint_spine.py` fant 0 feil, og `sprint_plan.py validate` godkjente `sprint-status.yaml`;
  * kontrollskriptet viste samme dekning som før, og personvernskanningen av de nye linjene fant ingenting;
  * addendum §2 sa fortsatt at versjonene skal kontrolleres på nytt innen 2026-12-01. Etter min godkjenning ble datoen rettet til 2026-12-08, og PRD §12 nevner rettingen. Kontrollene ble kjørt på nytt uten funn.
* Godkjente commit, push og pull request mot `main` fra grenen `plan/sprint-planning`, uten fletting. Endringene er committet i `67694f7` og sendt som [PR #6](https://github.com/IBE160-2026/G40-lyamouri/pull/6). Commit-hashen og PR-nummeret er ført inn i endringsloggene i en egen commit.
* Godkjente flettingen av PR #6. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `41fe0cf` har den gamle `main` (`5445a2f`) og PR-hodet (`03c3630`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * etter pushen av `main` viser GitHub PR #6 som flettet 19. november kl. 21.23, med `41fe0cf` som merge-commit;
  * lokal `main` og GitHub ble synkronisert og sto på samme commit, og arbeidskopien var ren;
  * grenen `plan/sprint-planning` er beholdt.

**Status:** Sprintplanen er flettet inn i `main` (`41fe0cf`), og M0 i sprintplanen er nådd. Neste steg er story 1.1 med `bmad-build`.

### 20. november 2026 – Story 1.1 del A: lokal oppstart

* Startet story 1.1 med `bmad-build` på grenen `story/1-1-start-prognose-locally`, laget fra `main` (`ae7b72c`), etter sprintplanen og arkitekturspinen. Godkjente subagenter for hele kjøringen, og at storyen deles i del A, den lokale oppstarten, og del B, prosessdokumentene fra planleggingsfasen, med én pull request for begge.
* Godkjente spesifikasjonen for del A. Claude bygde skjelettet med en implementeringsagent: Django 5.2.19 i `src/` med `web.Company` i første migrering, PostgreSQL 18.7 i `compose.yaml` på 127.0.0.1 uten passord, innstillinger fra miljøvariabler og en valgfri `.env`, `load_seed` som lager `.secret_key`, siden `/`, testene og Ruff, og oppsettet i README og `.env.example`.
* Tre KI-granskere gikk gjennom del A og fant 35 funn: 20 ble rettet, 2 utsatt og 13 avvist med begrunnelse i spesifikasjonen. Feilene i KI-generert kode og tekst står i `docs/qa-logg.md`.
* Kontroll: 75 tester og Ruff passerte, og de fem kommandoene i README virket tre ganger fra en ren kopi, på 7,2–7,8 sekunder.
* Godkjente commit og push av del A (`25e04ea`, `93c9147` og `258dccd`) og sesjonsloggen (`d8674ad`).
* Testet `/` i responsiv visning i Safari ved 320 px, 390 × 844 og 820 × 1180, uten avkuttet tekst eller sidelengs rulling. Resultatet ble ført i QA-loggen 21. november.
* Eksporterte økten med `/export`, og Claude maskerte stier og brukernavn i fila.

**Status:** Del A er pushet. Del B, klonetesten fra GitHub og BMAD Code Review gjenstår før flettingen.

### 21. november 2026 – Story 1.1 del B, D-9 og BMAD Code Review

* Claude bygde del B med `bmad-build`: `docs/statustabell.md`, `docs/ki-styringslogg.md` med 26 tilfeller fra planleggingsfasen, og feilene fra planleggingsfasen i `docs/qa-logg.md`. Tre KI-granskere fant 20 funn, og alle ble rettet. Godkjente commit og push (`d2b887d`, `79c9154`, `c8da9ff`, `477a687` og `3edf54b`).
* Godkjente klonetesten: grenen ble klonet fra GitHub, og de fem kommandoene i README virket uten feil på 7,1 sekunder (`936f364`).
* Gjentok Safari-sjekken etter del B ved 320 × 844, 390 × 844 og 820 × 1180, uten avkuttet tekst eller sidelengs rulling (`2791949`).
* Claude fant at reglene krevde CI før flettingen, mens CI først bygges i story 1.2. Godkjente unntaket D-9: story 1.1 flettes når testene og Ruff passerer lokalt på grenens siste commit (`fa237e7` og `5268fe0`).
* Opprettet PR #8 og kjørte `bmad-code-review` med fire KI-granskere på hele grenen:
  * 34 funn: 21 ble rettet, 2 utsatt og 11 avvist, og funn som var vurdert i del A eller del B, beholdt vurderingen sin;
  * avgjorde selv at `.gitignore` skal ha en test, at en test som ikke kontrollerer noen FR, nevner NFR-, DR- eller AD-ID-ene sine (D-10), og at README og `.env.example` skal advare mot en eksportert `DATABASE_URL`;
  * rettingene ligger i `e36043a`, `bcd8223` og `c2a70a6`, og funnene med beslutningene står i kommentaren i PR #8.
* Kontroll: `uv run pytest` med 82 tester, `uv run ruff check` og `uv run ruff format --check` passerte i en ny klone av `c2a70a6` fra GitHub (`5ba7016`). De passerte på nytt i en ny klone av grenens siste commit, `9c8a5dd`, og resultatet står i PR #8.
* Story 1.1 står som `done` i `sprint-status.yaml`. Eksporterte hele økten på nytt, og Claude maskerte den (`77f1960`). Sesjonsloggen og `issues.md` er oppdatert (`b689ad2`).
* Godkjente at arbeidsloggen fikk oppføringene for 20. og 21. november, som manglet (`9c8a5dd`).
* Godkjente flettingen av PR #8. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `e8b82c0` har den gamle `main` (`ae7b72c`) og PR-hodet (`9c8a5dd`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * etter pushen av `main` viser GitHub PR #8 som flettet 21. november kl. 19.32, med `e8b82c0` som merge-commit;
  * lokal `main` og GitHub ble synkronisert og sto på samme commit, og arbeidskopien var ren;
  * grenen `story/1-1-start-prognose-locally` er beholdt.

**Status:** Story 1.1 er flettet inn i `main` (`e8b82c0`). Neste steg er story 1.2, som ikke er startet.

### 21.–22. november 2026 – Story 1.2: CI for hver pull request

* Startet story 1.2 med `bmad-build` på grenen `story/1-2-check-every-pull-request`, laget fra `main` (`374db81`). Godkjente subagenter bare der reglene krever det: én til å kompilere epic-1-konteksten på nytt med D-9 og D-10, og fire i BMAD Code Review.
* Godkjente spesifikasjonen og bestemte at den første grønne kjøringen er organisasjonssjekken (D-1), fordi API-et for reglene for Actions krever admin-rettigheter i IBE160-2026.
* Claude bygde `.github/workflows/ci.yml`, importtesten for AD-1, compose-testen for VG-4 og en test av workflowen, og gjenbrukte `makemigrations --check` fra story 1.1. Reviewen i `bmad-build` ga 11 funn: 4 ble rettet og 7 avvist. Tre mutasjoner viste at testene feiler når de skal.
* Godkjente commit, push og PR #10 (`668808b` og `b2dd344`). Tokenet i nøkkelringen manglet `workflow`-rettigheten, og `gh auth refresh` lyktes ikke. Jeg laget derfor en SSH-nøkkel og registrerte den på GitHub, og grenen ble pushet via SSH.
* Den første CI-kjøringen passerte på Linux på 36 sekunder, med 99 tester, også de 82 fra story 1.1 (D-9).
* Kjørte BMAD Code Review med fire KI-granskere: 34 funn, 31 rettet i 12 rettinger og 3 avvist. Bestemte at importtesten også avviser database- og nettverksmodulene i standardbiblioteket, og at hver push til `main` får sin egen kjøring. Rettingene ligger i `e24727e` og `5297ed0`, og den andre CI-kjøringen passerte med 103 tester.
* Eksporterte økten med `/export`. Claude maskerte den og fjernet delen som allerede står i eksporten for story 1.1. Sesjonsloggen, `issues.md` og sprintstatusen er oppdatert.
* Godkjente commit og push av eksporten, sesjonsloggen og arbeidsloggen (`147a6c8`, `86a5db9` og `e864d02`). CI-kjøring nr. 3 på `e864d02` passerte med 103 tester, og kommentaren med alle 34 funnene ble lagt inn i PR #10.
* Godkjente flettingen av PR #10. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `674c8fd` har den gamle `main` (`374db81`) og PR-hodet (`e864d02`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * `main` ble pushet via SSH, fordi `ci.yml` kom inn i `main`, og GitHub viser PR #10 som flettet 22. november kl. 00.48, med `674c8fd` som merge-commit;
  * CI-kjøring nr. 4, den første på `main`, passerte med 103 tester;
  * lokal `main` og GitHub ble synkronisert og sto på samme commit, og arbeidskopien var ren;
  * grenen `story/1-2-check-every-pull-request` er beholdt.

**Status:** Story 1.2 er flettet inn i `main` (`674c8fd`), og CI sjekker nå hver pull request. Neste story følger rekkefølgen i sprintplanen, og story 1.3 er ikke startet.

### 22. november 2026 – Story 1.3: oppsettet på Windows og uten nett

* Startet story 1.3 med `bmad-build` på grenen `story/1-3-windows-and-offline-setup`, laget fra `main` (`850250d`). Storyen fulgte den korte «oneshot»-ruten, og ingen subagent trengtes, fordi epic-1-konteksten var gyldig.
* Planen var Windows-testen på jobb-PC-en 25. november, fordi PC-en bare er tilgjengelig da og 7. desember.
* Kjørte testen uten nett på macOS i Terminal med et skript som Claude skrev, og slo selv nettet av og på. Databasen var klar etter 5 sekunder, og Prognose svarte etter 1 sekund. Docker Desktop var trolig ikke helt avsluttet.
* Testen viste at Terminal ikke fant `docker`, fordi verktøyene lå i `~/.docker/bin`. Claude rettet README. Godkjente commit og push av rettingen, testen og loggene (`3363596`, `683e13f`, `5f0f8c3` og `f772c42`).
* Fant ut at ingenting kan installeres på jobb-PC-en, og gruppen har ingen annen Windows x64-PC. Valgte å føre begrensningen i QA-loggen, README og statustabellen (D-3) og å la GitHub Actions teste oppsettet uten Docker på en Windows-maskin. Den ferdige nettsiden testes i en nettleser på Windows i story 4.4.
* Claude skrev `.github/workflows/windows-setup.yml`. Den første kjøringen passerte på 40 sekunder og viste at alle lokale brukere kunne lese `.secret_key` i arbeidsmappa, så README råder den som deler PC-en, til å klone i brukermappa. Godkjente commit, push og PR #12 med workflowen og resultatet (`0eaea95` og `739d3bd`).
* Kjørte BMAD Code Review med fire KI-granskere: 46 funn, samlet i 24 punkter. Bestemte at testen uten nett på macOS kjøres på nytt med Docker Desktop helt avsluttet, og at Windows-testen også kjører når koden endres. 19 punkter ble rettet, 1 utsatt og 2 avvist. Rettingene i workflowen, testene og README ligger i `fedaef2`, og Windows-kjøring nr. 3 passerte på den.
* Kjørte testen uten nett på macOS på nytt med et nytt skript. Et nytt Terminal-vindu fant `docker`, og med Docker Desktop helt avsluttet og nettet av startet Docker Desktop på 6 sekunder. Databasen var klar etter 4 sekunder, og Prognose svarte etter 2 sekunder.
* Godkjente commit og push av rettingene og resultatene (`edc48af`). CI-kjøring nr. 10 og Windows-testen nr. 4 passerte, og kommentaren med alle 24 punktene ble lagt inn i PR #12.
* Eksporterte økten med `/export`. Claude maskerte den og beholdt bare delen etter eksporten for story 1.2. Sesjonsloggen og `issues.md` er oppdatert.
* Godkjente commit og push av eksporten, sesjonsloggen og arbeidsloggen (`7c81a15`, `ace8f5b` og `68603a5`). CI-kjøring nr. 11 og Windows-testen nr. 5 på `68603a5` passerte.
* Godkjente flettingen av PR #12. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `36e4035` har den gamle `main` (`850250d`) og PR-hodet (`68603a5`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * `main` ble pushet via SSH, fordi `windows-setup.yml` kom inn i `main`, og GitHub viser PR #12 som flettet 22. november kl. 15.33, med `36e4035` som merge-commit;
  * CI-kjøring nr. 12 på `main` passerte med 104 tester;
  * lokal `main` og GitHub ble synkronisert og sto på samme commit, og arbeidskopien var ren;
  * grenen `story/1-3-windows-and-offline-setup` er beholdt.

**Status:** Story 1.3 er flettet inn i `main` (`36e4035`). Oppsettet på Windows er bare testet uten Docker, og de åpne punktene står i `issues.md`. Neste story følger rekkefølgen i sprintplanen, og story 1.4 er ikke startet.

### 22. november 2026 – Story 1.4: app-skall og norske feilsider

* Startet story 1.4 med `bmad-build` på grenen `story/1-4-app-shell-and-error-pages`, laget fra `main` (`dc7673e`). Epic-1-konteksten var formelt utdatert etter en endring i spinen i story 1.3, men endringen gjaldt bare Windows-testen, så jeg valgte å bruke konteksten som den var. Godkjente subagenter bare til gjennomgangene.
* Godkjente spesifikasjonen, også størrelsen på om lag 2 400 tokens, som er over den anbefalte grensen på 1 600.
* Claude fant at AD-12 ikke kan bygges slik regelen vanligvis leses: Django gjør om et unntak til et svar i laget der det oppstår, så den ytterste mellomvaren ser bare svaret. Løsningen er et signal som merker forespørselen, og kravet og spinen er uendret ([tilfelle 31](ki-styringslogg.md#31-503-siden-og-den-ytterste-mellomvaren-22-november-2026)).
* Claude bygde stilarket med alle tokenene fra `DESIGN.md`, basismalen med toppfeltet, de norske feilsidene, mellomvaren for 503 og 405, loggingen til konsollen og 26 nye tester. Testene leser tokenene fra `DESIGN.md` og tekstene fra meldingskatalogen i `EXPERIENCE.md`. Åtte mutasjoner viste at testene feiler når de skal.
* `curl` mot runserver viste at 405-siden ble sendt med `Content-Length: 0`, så nettleseren ville vist en blank side. Claude rettet mellomvaren og la til en sjekk i testene.
* Reviewen i `bmad-build` (Blind Hunter) ga 10 funn: 2 ble rettet og 8 avvist. Jeg valgte å beholde berøringsreglene for skjermer der berøring er hovedinngangen (`pointer: coarse`).
* Sjekket `/` og `/finnes-ikke/` i den responsive visningen i Safari ved 320 px, 390 × 844 og 820 × 1180, uten avkuttet tekst, overlapp eller sidelengs rulling.
* Godkjente commit, push og PR #14 (`9ae95fc` og `f3a10dd`). CI-kjøring nr. 15 og Windows-testen nr. 6 passerte på `f3a10dd`.
* Kjørte BMAD Code Review med fire KI-granskere. Bruksgrensen stoppet alle fire én gang, og de fortsatte fra arbeidet som var lagret da grensen var tilbakestilt. De fant 35 funn: 23 ble rettet i 15 punkter, 2 utsatt og 9 avvist. Den viktigste rettingen gjør at 503-siden også er HTML med DEBUG på, og resten strammer inn testene og dokumentene. Seks nye mutasjoner viste at rettingene virker, og 132 tester og Ruff passerte.
* Bestemte å sjekke fokusringen for hånd. Den blå ringen rundt lenken på `/finnes-ikke/` var i orden, og versjonene var Safari 18.6 og macOS 15.6.
* Godkjente commit og push av rettingene (`5063f67`) og dokumentene (`b37c3b3`), og kommentaren med alle funnene i PR #14. CI-kjøring nr. 16 og Windows-testen nr. 7 passerte på `b37c3b3`.
* Eksporterte økten med `/export`. Claude maskerte den: 27 stier til prosjektmappa ble `<repo>`, og 1 sti til den midlertidige mappa ble `<tmp>`. Sesjonsloggen og sju nye åpne punkter i `issues.md` er ført, og story 1.4 står som `done` i sprintstatusen.

* Godkjente commit og push av eksporten, sesjonsloggen og dokumentene (`a5b82cd`, `fde748f` og `990ee9d`). CI-kjøring nr. 17 og Windows-testen nr. 8 på `990ee9d` passerte.
* Godkjente flettingen av PR #14. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `c5bd9cc` har den gamle `main` (`dc7673e`) og PR-hodet (`990ee9d`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * `main` ble pushet over HTTPS, fordi ingen workflow-filer var endret, og GitHub viser PR #14 som flettet 22. november kl. 19.57, med `c5bd9cc` som merge-commit;
  * CI-kjøring nr. 18 på `main` passerte;
  * lokal `main` og GitHub ble synkronisert og sto på samme commit, og arbeidskopien var ren;
  * grenen `story/1-4-app-shell-and-error-pages` er beholdt.

**Status:** Story 1.4 er flettet inn i `main` (`c5bd9cc`), og de åpne punktene står i `issues.md`. Neste story følger rekkefølgen i sprintplanen, og story 1.5 er ikke startet.

### 22.–23. november 2026 – Story 1.5: referanseregnearket som fasit

* Startet story 1.5 med `bmad-build` på grenen `story/1-5-reference-spreadsheet-as-the-answer-key`, laget fra `main` (`da87fd7`). Epic-1-konteksten var formelt utdatert av samme grunn som i story 1.4, så Claude brukte den som den var. Subagenter brukes bare til gjennomgangene.
* Bestemte at E30 står som i PRD-en, at regnearket fører «lav», og at spørsmålet om et eksempel som viser hvordan varselet om sesongmønster påvirker tillitsmerket, flyttes til story 5.2 ([tilfelle 33](ki-styringslogg.md#33-e30-og-tillitsmerket-22-november-2026)). Godkjente spesifikasjonen, også størrelsen på om lag 2 700 tokens.
* Claude lagde `reference/reference-examples.xlsx` med 52 tilfeller, 11 regeltestprodukter, kontrollarket `checks` og `check_log`. Tilfellene er E1–E30 fra PRD §5.7, med én rad per variant, og de fire FR-21-variantene. Claude dokumenterte arkene og notasjonen i `reference/README.md`. Verdiene fra PRD §5.7 er ført med samme presisjon, og FR-21-variantene og regeltestproduktene er regnet ut for hånd.
* Claude regnet ut hvert tilfelle på nytt med et uavhengig skript og regnet ut de 376 kontrollformlene med avrundingen i Excel. Ingen verdi avvek fra PRD §5.7. Sammenligningen fant én feil i Claudes egne formler for varslene, og den ble rettet før fila ble skrevet ([QA-loggen](qa-logg.md#2026-11-23--feil-i-ki-generert-kode-og-tekst-fra-byggingen-av-story-15-dr-9)).
* Claude skrev leseren `tests/answer_key.py` og 10 nye tester i `tests/test_reference_spreadsheet.py`. Testene leser listen over eksemplene og FR-21-tabellen fra PRD-en. 21 feil som ble lagt inn i regnearket og PRD-en én om gangen, ble alle fanget, og 142 tester og Ruff passerte.
* Reviewen i `bmad-build` (Blind Hunter) ga 13 funn: 4 ble rettet i `reference/README.md` og testen, og 9 ble avvist. Ett av dem, grensene for innstillingene i FR-20, er et åpent punkt for story 1.7.
* Kontrollerte regnearket i Excel for Mac 16.78 (23100802): sammendraget i `checks` viste at alle 376 kontrollene stemmer (K1 = 376, K2 = 376, K3 = SANN). Lukket regnearket uten å lagre, og kontrollen står i `check_log`.
* Godkjente commit, push og PR #16 (`0ae5920` og `99b73bc`), men ikke flettingen. CI-kjøring nr. 21 passerte på `99b73bc`.
* Kjørte BMAD Code Review med fire KI-granskere: 61 funn, samlet i 3 beslutninger, 21 rettinger, 2 utsatte punkter og 5 avviste funn. Bestemte:
  * nye tester for inndataene, i stedet for formler som leser cellene;
  * å rette E12 i PRD §5.7 til «no old-data warning», med en rad i §12, fordi varselet om utsolgte uker må være aktivt der;
  * å beholde toleransen på 0,0005;
  * å gjøre alle rettingene.
* Claude rettet testene, leseren og arket `checks` med radene «other» og formlene for R-11, og skrev arbeidsboka på nytt. Alle 401 kontrollene stemmer i den uavhengige utregningen. 50 feil som ble lagt inn én om gangen, ble alle fanget, og 151 tester og Ruff passerte.
* Kontrollerte den nye arbeidsboka i Excel for Mac 16.78: K1 = 401, K2 = 401 og K3 = SANN. Lukket den uten å lagre, og kontrollen står i `check_log`.
* Godkjente to commits, én med rettingene (`dd4a269`) og én med dokumentene, push og en kommentar i PR #16 med alle funnene og beslutningene, men ikke flettingen.

* Claude la inn kommentaren med alle 61 funnene og beslutningene i PR #16. CI-kjøring nr. 22 passerte på `7e62aa3`.
* Eksporterte økten med `/export`. Claude maskerte den: 25 stier til prosjektmappa ble `<repo>`, og 2 stier til den midlertidige mappa ble `<tmp>`, også der stiene var brutt over to linjer. Kontrollen etterpå fant ingen lokale stier, brukernavn, e-poster, nøkler eller tokens.
* Sesjonsloggen og fem nye åpne punkter i `issues.md` er ført, og punktene om regnearket og E30 er løst. Story 1.5 står som `done` i sprintstatusen.
* Godkjente commit og push av eksporten (`024b204`), sesjonsloggen med `issues.md` (`df5ebbd`) og dokumentene (`c0959b2`). CI-kjøring nr. 23 passerte på `c0959b2`.
* Godkjente flettingen av PR #16 på vilkår av grønn CI og grønn Windows-test på siste commit. Windows-testen startet ikke av seg selv, fordi PR-en ikke endret koden eller avhengighetene, så Claude startet den for hånd, og kjøring nr. 9 passerte på `c0959b2`. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `4dc963a` har den gamle `main` (`da87fd7`) og PR-hodet (`c0959b2`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * `main` ble pushet over HTTPS, fordi ingen workflow-filer var endret, og GitHub viser PR #16 som flettet 23. november kl. 16.48, med `4dc963a` som merge-commit;
  * CI-kjøring nr. 24 på `main` passerte;
  * lokal `main` og GitHub ble synkronisert og sto på samme commit, og arbeidskopien var ren;
  * grenen `story/1-5-reference-spreadsheet-as-the-answer-key` er beholdt.

**Status:** Story 1.5 er flettet inn i `main` (`4dc963a`), og de åpne punktene for story 1.6, 1.7, 5.1 og 5.2 står i `issues.md`. Neste story følger rekkefølgen i sprintplanen, og story 1.6 er ikke startet.

### 23. november 2026 – Story 1.6: de syntetiske seed-dataene

* Startet story 1.6 med `bmad-build` på grenen `story/1-6-generate-the-synthetic-seed-data`, laget fra `main` (`1610325`). Epic-1-konteksten var formelt utdatert, men endringene gjelder ikke seed-data, så Claude brukte den som den var. Subagenter brukes bare til gjennomgangene.
* Brukeren bestemte at den felles leseren av regnearket ligger i `reference/answer_key_reader.py` (BH-31). Godkjente spesifikasjonen, også størrelsen på om lag 2 700 tokens. Claude valgte selv kundenumre (1001 og 1002) og passord (de står i README-en), og at Testbedrift B slutter i uke 44 mens A slutter i uke 45.
* Claude skrev generatoren `data/generate_seed.py`, de to seed-filene (30 og 32 produkter), `data/README.md`, 17 nye tester i `tests/test_seed_data.py` og flyttet leseren. Et uavhengig skript for R-1 til R-16 (ikke committet) ga 4 produkter å bestille snart (7, 11, 9 og 4, til sammen 31), 1 uten prognose og 4 med varsel for Testbedrift A, og alle 11 regnearkprodukter fikk de forventede verdiene. Ni feil som ble lagt inn én om gangen, ble alle fanget.
* Testene fant at det første saltet var for kort for Django, og at testen av nytt nivå oversåg Skruer ([QA-loggen](qa-logg.md#2026-11-23--feil-i-ki-generert-kode-og-tekst-fra-byggingen-av-story-16-dr-9)). Blind Hunter i byggeøkten ga 10 funn: 6 rettet og 4 avvist.
* Godkjente commit, push og PR #18 (`1dff8db`). CI og Windows-testen passerte på `1dff8db`.
* Kjørte BMAD Code Review med fire KI-granskere: 42 funn, 26 rettet, 5 beslutninger og 11 avvist ([tilfelle 35](ki-styringslogg.md#35-det-første-saltet-og-beslutningene-i-bmad-code-review-av-story-16-23-november-2026)). Brukeren bestemte å mykne teksten om Windows og utsette pytest i Windows-jobben, å legge til en test av «Denne uken» med R-8 i testen til story 2.8, og å gjøre alle patchene.
* Claude rettet generatoren, testene og dokumentene, og kjørte det uavhengige skriptet på nytt med samme resultat. 173 tester og Ruff passerte. Fire feil som ble lagt inn i «Denne uken»-testen, ble alle fanget.
* Godkjente commit og push av rettingene (`ecbf55d`) og dokumentene (`5bfc29e`), og la inn kommentaren i PR #18 med alle 42 funnene og beslutningene. CI-kjøring og Windows-testen passerte på `ecbf55d` og på `5bfc29e`.
* Eksporterte økten med `/export`. Claude maskerte den: 4 stier til prosjektmappa ble `<repo>`, også der en sti var brutt over to linjer. Kontrollen etterpå fant ingen lokale stier, brukernavn, e-poster, nøkler eller tokens. De to testpassordene fra README-en er syntetiske og står i teksten.
* Sesjonsloggen `978-2026-11-23-18-09-42-story-1-6-seed-dataene.md` og fem nye åpne punkter i `issues.md` er ført, og BH-31 er løst. Story 1.6 står som `done` i sprintstatusen.
* Godkjente commit og push av eksporten (`ac8288b`), sesjonsloggen med `issues.md` (`882b9a4`) og dokumentene (`7550f26`). CI-kjøring nr. 30 og Windows-kjøring nr. 13 passerte på `7550f26`.
* Godkjente flettingen av PR #18 på vilkår av grønn CI og grønn Windows-test på siste commit. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter:
  * merge-commiten `62b9434` har den gamle `main` (`1610325`) og PR-hodet (`7550f26`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * `main` ble pushet over HTTPS, fordi ingen workflow-filer var endret, og GitHub viser PR #18 som flettet 23. november kl. 18.12, med `62b9434` som merge-commit;
  * CI-kjøring nr. 31 på `main` passerte;
  * grenen `story/1-6-generate-the-synthetic-seed-data` er beholdt.

**Status:** Story 1.6 er flettet inn i `main` (`62b9434`), og de åpne punktene for story 1.7, 1.8, 2.8 og 4.1 og for pytest i Windows-jobben står i `issues.md`. Neste story følger rekkefølgen i sprintplanen, og story 1.7 er ikke startet.

### 23. november 2026 – Story 1.7: seed-dataene inn i databasen, med en eksplisitt nullstilling

* Startet story 1.7 med `bmad-build` etter prosjektreglene, BMAD og sensorveiledningen. `main` var ren og synkronisert med `origin/main` (`16d93b7`). Claude leste bare sprintplanen, storyen i `epics.md`, de relevante punktene i `issues.md` (linje 95, 117 og 122) og forrige story, og laget grenen `story/1-7-load-the-seed-data-with-an-explicit-reset`. Epic-1-konteksten var formelt utdatert, men endringene gjelder ikke story 1.7, så Claude brukte den som den var. Subagenter brukes bare til gjennomgangene.
* Claude skrev spesifikasjonen. Den er om lag 2 600 tokens, og brukeren godkjente den slik den var, med ordet «nullstill» som bekreftelse og en justering av klonesteget i Windows-jobben. Claude valgte selv at en avvist bekreftelse gir en feil (som `flush` i Django) og at lesingen av filene ligger i `web/seed.py`.
* Claude bygde `forecasting/settings.py`, modellene `Product`, `SalesWeek` og `CompanySettings` med migrasjon `0002`, leseren, `load_seed --reset`, 66 nye tester og dokumentene. Ruff og testene fant tre feil under byggingen, og Blind Hunter i byggeøkten ga 10 funn: 3 rettet, 6 avvist og 1 utsatt ([QA-loggen](qa-logg.md#2026-11-23--feil-i-ki-generert-kode-og-tekst-fra-byggingen-av-story-17-dr-9)). 11 feil som ble lagt inn én om gangen, ble alle fanget. Claude kjørte `migrate` og `load_seed` mot den lokale databasen: 2 bedrifter, 62 produkter og 5 016 salgsuker, og en ny kjøring stoppet med den norske meldingen.
* Kjørte BMAD Code Review med fire uavhengige KI-granskere på arbeidstreet før noe var committet: 46 funn, 20 rettet, 2 utsatt, 4 feil og 20 avvist, og ingen trengte en beslutning ([tilfelle 36](ki-styringslogg.md#36-grensene-i-leseren-og-reviewen-av-story-17-23-november-2026)). Claude gjorde patchene uten å vente på valget i trinn 5, og sa fra om det. 238 tester og Ruff passerte etterpå.
* Brukeren kjørte omstartssjekken på macOS: 2 bedrifter, 62 produkter, 5 016 salgsuker og 2 innstillinger var uendret etter at Docker ble stoppet og startet, `window=5` ble bevart, og `load_seed --reset` med «nullstill» satte den tilbake til 3, mens «nei» ikke endret noe ([QA-loggen](qa-logg.md#2026-11-23--omstartssjekken-av-dataene-story-17-fr-4-sm-5)). FR-4 står som bygd i statustabellen.
* Godkjente de to commitene, SSH-push, opprettelse av PR og fletting når alle kontroller var grønne. Claude maskerte eksporten (stien til prosjektmappa ble `<repo>` og stien til den midlertidige mappa `<scratchpad>`), og kontrollen etterpå fant ingen lokale stier, brukernavn, e-poster, nøkler eller tokens. Commitene er `85308ac` (koden) og `b3b5157` (loggene, eksporten og dokumentene). Loggene ligger i én commit, ikke tre som for story 1.6, fordi brukeren godkjente to. Branchen ble pushet til `git@github.com` fordi `windows-setup.yml` er endret, og Claude opprettet PR #20 med en kommentar med alle 46 funnene.
* CI-kjøring nr. 34 og Windows-kjøring nr. 14 passerte på `b3b5157`. Windows-jobben lastet seed-dataene (62 produkter og 5 016 salgsuker), og klonesteget fikk meldingen «Databasen har allerede data», så det utsatte punktet om Windows-steget er verifisert.
* Godkjente flettingen av PR #20. Claude flettet lokalt med «Create a merge commit» (`git merge --no-ff`), uten squash eller rebase, og med noreply-adressen som forfatter. Det første forsøket feilet på et flagg som `git merge` ikke har, før noe var flettet, og `main` var uendret. Deretter:
  * merge-commiten `10b048a` har den gamle `main` (`16d93b7`) og PR-hodet (`b3b5157`) som foreldre;
  * innholdet i `main` er identisk med PR-hodet, så bare de godkjente endringene ble flettet inn;
  * `main` ble pushet over SSH, fordi en workflow-fil er endret, og GitHub viser PR #20 som flettet 23. november kl. 19.29, med `10b048a` som merge-commit;
  * CI-kjøring nr. 35 på `main` passerte;
  * grenen `story/1-7-load-the-seed-data-with-an-explicit-reset` er beholdt.

**Status:** Story 1.7 er flettet inn i `main` (`10b048a`), og story 1.8 er ikke startet. Åpne punkter for story 3.1 og 4.4 står i `issues.md`.

## 4. Videre dokumentasjon

Nye arbeidsøkter skal føres inn med dato. Hver oppføring skal beskrive hva som faktisk ble gjort, hvilke beslutninger som ble tatt, og hva som gjenstår. Arbeid skal ikke føres som fullført før det er kontrollert.
