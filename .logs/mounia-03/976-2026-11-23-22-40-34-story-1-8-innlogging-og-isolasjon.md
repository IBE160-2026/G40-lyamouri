# Story 1.8 – innlogging og isolasjon mellom bedriftene

## 2026-11-23 kl. 22:40 — Mounia-03

### Oppgave
Starte story 1.8 («Log in and see only your own company's products») etter prosjektreglene, BMAD og sensorveiledningen: kontrollere at `main` er ren og synkronisert, lese bare de nødvendige filene, lage spesifikasjon, implementere, teste grundig og kjøre BMAD Code Review med fire uavhengige granskere. Brukeren ba om særlig tester av tilgangen mellom bedriftene og av CSRF-håndteringen, om manuelle tester (Safari og ekte iPhone 13), og om at Claude ikke committer, pusher eller starter story 1.9 eller 2.1 før godkjenning.

### Plan
- `bmad-build` med den fulle ruten på grenen `story/1-8-log-in-and-see-only-your-own-companys-products`, laget fra `main` (`7aeb0a7`). Spesifikasjonen er [spec-1-8-log-in-and-see-only-your-own-companys-products.md](../../_bmad-output/implementation-artifacts/spec-1-8-log-in-and-see-only-your-own-companys-products.md).
- Epic-1-konteksten ble brukt som den var (som i story 1.7). Byggingen ble gjort uten subagent, og subagenter ble bare brukt i BMAD Code Review (D-8).
- Brukeren valgte en hvit fokusring i toppfeltet (WCAG 1.4.11) og godkjente spesifikasjonen. Claude valgte selv å ikke bygge en advarsel for manglende `.secret_key`, og å la feilsidene bare ha ordmerket.
- Etter reviewen fant brukerens Safari-test to feil. Brukeren valgte en liten `app.js` (AD-11 utvidet) mot Safaris tilbake-hurtigbuffer, og Claude rettet CSRF-visningen for gamle skjemaer.

### Resultat
- **Koden** (commit `a078c90`): innlogging på `/`, utlogging med POST på `/logg-ut/`, `/produkter/` med bare bedriftens produkter, `LoginRequiredMiddleware` (nektet som standard, uten `next`), `web/queries.py` (bedriften som første argument), `web/forms.py`, `forecasting/display.py` (ukeetiketten «uke 45, 2026»), toppfeltet med bedriften og uka, en hvit fokusring, `csrf_failure`, `never_cache` og `app.js`. Ingen ny modell, migrering eller avhengighet.
- **Tester:** 312 tester passerer, 1 hoppes over (Docker-sjekken). Ruff og `makemigrations --check` er grønne. Nye filer: `test_login.py`, `test_product_overview.py`, `test_isolation.py` (to-konto-testen, også mot de ekte seed-dataene), `test_forecasting_display.py` og `conftest.py`. 20 mutasjoner i koden ble alle fanget.
- **BMAD Code Review** med fire uavhengige granskere: 35 funn, 19 rettet, 13 avvist og 3 feil, ingen utsatt, og ingen trengte en beslutning ([tilfelle 37](../../docs/ki-styringslogg.md#37-utlogging-csrf-og-tilgangen-mellom-bedriftene-i-story-18-23-november-2026), [QA-loggen](../../docs/qa-logg.md)).
- **Manuelle tester**, meldt av brukeren 23. november 2026: i Safari på Mac fungerer Tilbake etter utlogging for A og B, et gammelt innloggingsskjema gir et nytt skjema uten CSRF-melding, layouten er riktig ved 320, 390 og 820 px, og den hvite fokusringen er bekreftet. På den ekte iPhone 13 fungerer innloggingen for begge, A viser uke 45, 2026 og B uke 44, 2026 med bare egne produkter, og layout, tekst og berøringsknapper er bra. Tilbake etter utlogging gir innloggingssiden. Automatisk zoom ved inntasting er ikke sikkert bekreftet.
- **Sluttkontroller:** personvernskanning av de 32 filene fant ingen lokale stier, e-poster, nøkler eller feilsøkingskode.
- **Dokumenter:** spesifikasjonen, README, statustabellen (FR-1 bygd, FR-2 delvis bygd), QA-loggen, KI-styringsloggen, AD-11 og endringsloggene i spinen, epics og EXPERIENCE (hvit fokusring og `app.js`) er oppdatert. Sprintstatusen står på `review`.
- **Avvik fra rutinen:** CLAUDE.md ber skillen committe loggen lokalt, men brukeren ba om at ingenting committes før status er presentert og godkjent. Loggen, eksporten og dokumentene ligger derfor i den andre commiten (som i story 1.7), ikke i en egen loggcommit.
- **Eksporten** `.logs/mounia-03/sessions/1-8-2026-11-23.txt` er maskert: stien til den midlertidige mappa ble `<scratchpad>`. Kontrollen etterpå fant ingen lokale stier, brukernavn, e-poster, nøkler eller tokens. iPhone-testen er ført med iOS 27.0.1.

- **Flettingen:**
  - Etter brukerens godkjenning ble koden og dokumentene committet (`a078c90` og `5b681c5`), og grenen ble pushet over SSH. PR #22 ble opprettet med en kommentar med alle 35 funnene.
  - CI-kjøring nr. 38 og Windows-kjøring nr. 15 passerte på `5b681c5`. CI kjørte 313 tester (Docker-testen med) og Ruff, og Windows-jobben kjørte oppsettet uten Docker.
  - Claude flettet lokalt med `git merge --no-ff` (merge-commit `d147241`, foreldre `7aeb0a7` og `5b681c5`) og pushet `main` over SSH. GitHub viser PR #22 som flettet 23. november kl. 23.00, og CI-kjøring nr. 39 på `main` passerte. Grenen er beholdt.
  - Story 1.8 står som `done` i sprintstatusen og i spesifikasjonen. Story 2.1 er ikke startet.

### Åpne punkter
- Story 4.4: sjekke på nytt på den ekte iPhone 13 at feltene ikke zoomer inn ved inntasting (16 px), som ikke ble bekreftet i story 1.8.
- Hver senere story med en rute eller liste: legge den til i `ROUTES` i `tests/test_isolation.py`, gi den en eksempeladresse i `tests/test_login.py` hvis den har en parameter, og sette `never_cache` på sider med bedriftsdata. Story 2.7 må også la et oppslag av en annen bedrifts produkt gi samme 404-side.
- Story 2.3: la filteret for tall ta over utskriften av lageret i `products.html`, og bygge videre på `header_week_label`.
