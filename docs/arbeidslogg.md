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

## 4. Videre dokumentasjon

Nye arbeidsøkter skal føres inn med dato. Hver oppføring skal beskrive hva som faktisk ble gjort, hvilke beslutninger som ble tatt, og hva som gjenstår. Arbeid skal ikke føres som fullført før det er kontrollert.
