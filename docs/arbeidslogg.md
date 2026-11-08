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

## 4. Videre dokumentasjon

Nye arbeidsøkter skal føres inn med dato. Hver oppføring skal beskrive hva som faktisk ble gjort, hvilke beslutninger som ble tatt, og hva som gjenstår. Arbeid skal ikke føres som fullført før det er kontrollert.
