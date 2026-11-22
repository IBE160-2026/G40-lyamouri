# Story 1.4 – norsk app-skall og feilsider

## 2026-11-22 kl. 19:51 — Mounia-03

### Oppgave
Lese prosjektreglene, sprintplanen, story 1.4 og de relevante BMAD-dokumentene, kontrollere `main` og det tidligere arbeidet, og starte story 1.4 («Norwegian app shell and error pages») etter BMAD-metoden og sensorveiledningen. Storyens omfang skulle holdes, uten dobbeltarbeid og unødvendig tokenbruk. Claude skulle jobbe selvstendig, men be om godkjenning før commit, push, PR og fletting, og ikke lese filer utenfor prosjektmappen eller eksponere hemmeligheter. Senere samme dag:
- BMAD Code Review av PR #14, en sjekk av fokusringen for hånd og alle de 15 rettingene.
- Eksporten av økten med maskering, sesjonsloggen og `issues.md`, med godkjenning før commit, push og fletting.

### Plan
- `bmad-build` på grenen `story/1-4-app-shell-and-error-pages`, laget fra `main` (`dc7673e`), med den fulle ruten. Spesifikasjonen er [spec-1-4-norwegian-app-shell-and-error-pages.md](../../_bmad-output/implementation-artifacts/spec-1-4-norwegian-app-shell-and-error-pages.md), og brukeren godkjente den med om lag 2 400 tokens, over den anbefalte grensen på 1 600.
- Epic-1-konteksten var formelt utdatert, fordi spinen ble endret i story 1.3, men endringen gjaldt bare Windows-testen. Brukeren valgte å bruke konteksten som den var, og godkjente subagenter bare til gjennomgangene, ikke til byggingen.
- Byggeøkten skrev koden selv og sjekket den med mutasjoner fra et skript i den midlertidige mappa og med `curl` mot runserver. Brukeren sjekket sidene i Safari.
- Gjennomganger: Blind Hunter i byggeøkten, og BMAD Code Review med fire uavhengige subagenter på PR #14 (D-8).

### Resultat
- **Koden:**
  - `src/web/static/web/app.css` har alle tokenene fra `DESIGN.md` som CSS-variabler, fokusringen, toppfeltet, panelet og berøringsreglene.
  - `web/base.html` og `web/error.html` er basismalen og panelet for feilsidene, og feilmalene er `400.html`, `403.html`, `403_csrf.html`, `404.html`, `500.html` og `503.html`.
  - `web/middleware.py` har `ErrorPageMiddleware`, først i `MIDDLEWARE`, og signalmottakeren `note_database_error`, som `apps.py` kobler til `got_request_exception`. `LOGGING` i `settings.py` setter opp `django.request` og `django.security`, og startsiden bruker basismalen.
  - Testene står i `tests/test_app_shell.py` og `tests/test_error_pages.py`. De leser tokenene fra `DESIGN.md` og tekstene fra meldingskatalogen i `EXPERIENCE.md`.
- **Funn under byggingen:**
  - AD-12 kan ikke bygges med en `try/except` i den ytterste mellomvaren, fordi Django gjør om unntak til svar i hvert lag. Løsningen er signalet ([tilfelle 31](../../docs/ki-styringslogg.md#31-503-siden-og-den-ytterste-mellomvaren-22-november-2026)).
  - Å sette opp loggeren `django` ville nullstilt `django.server`.
  - 405-svaret ble sendt med `Content-Length: 0`, som `curl` mot runserver viste.
- **Gjennomgangene:**
  - Blind Hunter i byggeøkten: 10 funn, 2 rettet og 8 avvist. Brukeren valgte å beholde berøringsreglene for `pointer: coarse`.
  - BMAD Code Review: bruksgrensen stoppet de fire subagentene én gang, og de fortsatte fra arbeidet som var lagret. De fant 35 funn: 1 beslutning, 21 funn rettet i 14 punkter (`5063f67` og `b37c3b3`), 2 funn i ett punkt som denne loggen løser (de åpne punktene og eksporten), 2 utsatt (`deferred-work.md`) og 9 avvist. Den viktigste rettingen gjør at 503-siden også er HTML med DEBUG på. Alle funnene står i [kommentaren i PR #14](https://github.com/IBE160-2026/G40-lyamouri/pull/14#issuecomment-7083857499).
- **Tester:** 132 tester og Ruff passerte lokalt, og alle 14 mutasjonene ble fanget. CI-kjøring nr. 15 og Windows-testen nr. 6 passerte på `f3a10dd`, og CI-kjøring nr. 16 og Windows-testen nr. 7 på `b37c3b3`.
- **For hånd:**
  - Brukeren sjekket `/` og `/finnes-ikke/` i den responsive visningen i Safari ved 320 px, 390 × 844 og 820 × 1180, uten feil. Etter BMAD Code Review godkjente brukeren også fokusringen og leste versjonene: Safari 18.6 og macOS 15.6.
  - Claude sjekket svarene gjennom runserver med DEBUG av.
- **Commits på grenen:** `9ae95fc` (koden), `f3a10dd` (dokumentene), `5063f67` (rettingene fra BMAD Code Review) og `b37c3b3` (dokumentene etter reviewen). Brukeren godkjente hver av dem før commit og push. PR #14 er opprettet mot `main`.
- **Dokumenter:** statustabellen, QA-loggen (to oppføringer), KI-styringsloggen (tilfelle 31 og 32), arbeidsloggen, `deferred-work.md`, `sprint-status.yaml` og spesifikasjonen.
- **Eksporten:** [1-4-2026-11-22.txt](sessions/1-4-2026-11-22.txt) dekker hele økten etter `/clear`. Den er maskert: 27 stier til prosjektmappa ble `<repo>`, og 1 sti til den midlertidige mappa ble `<tmp>`. Kontrollen etterpå fant ingen lokale stier, brukernavn, e-poster, nøkler eller sesjonsnøkkel.
- **`issues.md`:** sju nye punkter (under). Ingen gamle punkter ble løst i økten.
- **Flettingen:** Etter brukerens godkjenning ble eksporten, denne loggen og dokumentene committet og pushet (`a5b82cd`, `fde748f` og `990ee9d`), og CI-kjøring nr. 17 og Windows-testen nr. 8 passerte på `990ee9d`. PR #14 ble flettet lokalt med «Create a merge commit» og noreply-adressen, og `main` ble pushet over HTTPS, fordi ingen workflow-filer var endret. Det første forsøket stoppet før flettingen, fordi `git merge -F -` ikke leser meldingen fra standard input, og ingenting ble endret eller pushet. Merge-commiten er `c5bd9cc`, og GitHub viser PR #14 som flettet 22. november kl. 19.57. CI-kjøring nr. 18 på `main` passerte. Lokal `main` og GitHub ble synkronisert på `c5bd9cc`, og grenen `story/1-4-app-shell-and-error-pages` er beholdt.

### Åpne punkter
- Story 1.8: bytt lenken «Til produktoversikten» i `web/error.html` fra `/produkter/` til `{% url %}` når ruten finnes (BH-6).
- Story 1.8: velg en fokusfarge for lenkene i det marineblå toppfeltet. Den blå ringen gir om lag 2,4:1, under 3:1 i WCAG 1.4.11, og `DESIGN.md` har ingen fokusfarge der, så det krever en designbeslutning og en rad i endringsloggen til UX-en (BH-12, `deferred-work.md`).
- Story 1.8: sjekk berøringsreglene (mål på minst 44 × 44 px og 16 px tekst i felt) på den ekte iPhone 13, fordi den responsive visningen i Safari ikke viser dem.
- Story 3.1, 3.3 og 5.1: radioknappene, bryteren og avkrysningsboksen «Sesongjustering» må få et mål på minst 44 × 44 px på berøringsskjermer gjennom etiketten, fordi stilarket unntar dem fra regelen om 44 px (AA-5).
- Story 4.2: «Last siden på nytt og prøv igjen.» kan villede etter en POST, fordi en ny innlasting sender det gamle skjemaet på nytt. Vurder teksten i meldingskatalogen; en endring krever godkjenning (BH-10).
- Vurder å presisere AD-12 i arkitekturspinen: den ytterste mellomvaren ser databasefeilen gjennom signalet `got_request_exception`, fordi Django gjør om unntak til svar i hvert lag. Det krever godkjenning og en rad i endringsloggen (BH-11, tilfelle 31).
- Databasen har ikke noe tidsavbrudd ved tilkobling, så psycopg venter i opptil 130 sekunder når porten svarer, men PostgreSQL ikke gjør det. Vurder `connect_timeout` når en story endrer `env.py`, senest i story 4.4 (EC-6, `deferred-work.md`).
