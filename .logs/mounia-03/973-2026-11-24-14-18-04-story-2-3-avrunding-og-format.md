# Story 2.3: avrunding og felles tallformat

## 2026-11-24 kl. 14:18 — Mounia-03

### Oppgave
Starte BMAD-arbeidet med story 2.3 («Round and format every number the same way») etter sprintplanen, sensorveiledningen og prosjektets rutiner: bygge avrundingen og det norske tallformatet slik AD-3 og referanseregnearket krever, teste det med mutasjoner, kjøre BMAD Code Review med alle fire uavhengige, skrivebeskyttede granskere og legge fram samlet resultat før noe committes eller pushes.

### Plan
- `bmad-build` med epic 2-konteksten (gyldig) og story 2.2 som kontinuitet. Spesifikasjonen ble lagt fram med beslutningene, og brukeren godkjente den.
- Bygge `src/forecasting/rounding.py`, utvide `src/forecasting/display.py`, lage tallfiltrene og la `products.html` bruke dem. Tester som leser de oppgitte verdiene fra regnearket.
- Mutasjonstester, BMAD Code Review (fire lag), triage, rettinger og dokumentene.
- Spesifikasjon: [spec-2-3-round-and-format-every-number-the-same-way.md](../../_bmad-output/implementation-artifacts/spec-2-3-round-and-format-every-number-the-same-way.md).

### Resultat
- Grenen `story/2-3-round-and-format-every-number-the-same-way` fra `1e213d4`. Brukeren ba om å få godkjenne før noe ble committet. Etter godkjenningen: koden og testene i `92da6bf`, spesifikasjonen og dokumentene i neste commit, denne loggen i den siste, alle i PR #31.
- Nye filer: `src/forecasting/rounding.py`, `src/web/templatetags/prognose.py`, `tests/test_rounding.py`, `tests/test_number_filters.py`, `tests/test_no_formatting_outside_the_core.py`. Endret: `src/forecasting/display.py`, `src/web/templates/web/products.html`, `tests/test_forecasting_display.py`, `sprint-status.yaml` (story 2.3 `review`) og dokumentene (statustabell, QA-logg, KI-styringslogg tilfelle 40, arbeidslogg).
- Avrundingen følger AD-3: først 6 desimaler, så opp til hele enheter eller halvt bort fra null, med `decimal`. E5 gir 70, E20 «10,3», E21 «0,07» og 1, og alle viste verdier i regnearket stemmer.
- 641 tester består, 1 hoppes over (Docker), `ruff check`, `ruff format --check` og `makemigrations --check` er rene.
- 54 mutasjoner før reviewen og 11 etter: alle fanget.
- BMAD Code Review: 34 funn fra Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. 7 grupper rettet (inndatakontroll i avrundingen, bredere vakttest, sterkere filtertester og dokumentene), 7 avvist, ingen utsatt. Hashene av prosjektfilene var identiske før og etter, så granskerne endret ingenting.
- Lukket punkt: lageret i `products.html` via filteret (fra story 1.8).

### Åpne punkter
- Story 2.4: gulvet på 0 i koden, erstatte den lånte formelen i testen, og «–» og kolonneetiketten «Uke 1 · uke 46» i `display.py`.
- Story 2.7 til 2.9: avgjøre om malene trenger filtre for ukeetiketter, og hvem som setter `with_year`.
