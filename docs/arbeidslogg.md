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

## 4. Videre dokumentasjon

Nye arbeidsøkter skal føres inn med dato. Hver oppføring skal beskrive hva som faktisk ble gjort, hvilke beslutninger som ble tatt, og hva som gjenstår. Arbeid skal ikke føres som fullført før det er kontrollert.
