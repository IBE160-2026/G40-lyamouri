# Story 2.4: ukeprognoser, scenarioer og foreslått bestillingsmengde

## 2026-11-24 kl. 18:19 — Mounia-03

### Oppgave
Starte BMAD-arbeidet med story 2.4 («Calculate the week forecasts, the scenarios and the suggested order quantity») etter sprintplanen, sensorveiledningen og prosjektets rutiner: bygge ukeprognosene, scenarioene og den foreslåtte bestillingsmengden i kjernen, teste dem mot referanseregnearket med mutasjoner, kjøre BMAD Code Review med alle fire uavhengige, skrivebeskyttede granskere, dokumentere flyttingen av skjermpunktene til story 2.7 og legge fram samlet resultat før noe committes eller pushes. Ikke starte story 2.5.

### Plan
- `bmad-build` med epic 2-konteksten (gyldig) og story 2.3 som kontinuitet. Spesifikasjonen ble lagt fram med beslutningene, og brukeren godkjente den og ba om at den ble holdt samlet.
- Utvide `ProductResult`, `ForecastSettings` og `forecast_product`, lage `src/forecasting/horizon.py`, og tester som leser de oppgitte verdiene fra regnearket.
- Mutasjonstester, BMAD Code Review (fire lag), triage, rettinger og dokumentene.
- Spesifikasjon: [spec-2-4-calculate-the-week-forecasts-the-scenarios-and-the-suggested-order-quantity.md](../../_bmad-output/implementation-artifacts/spec-2-4-calculate-the-week-forecasts-the-scenarios-and-the-suggested-order-quantity.md).

### Resultat
- Grenen `story/2-4-calculate-the-week-forecasts-the-scenarios-and-the-suggested-order-quantity` fra `f30fc3c`. Brukeren ba om å få godkjenne før noe ble committet. Etter godkjenningen: koden og testene i `05b0844`, spesifikasjonen og dokumentene i neste commit, denne loggen i den siste, alle i PR-en for story 2.4.
- Nye filer: `src/forecasting/horizon.py`, `tests/test_week_forecasts.py`, `tests/test_horizon.py`. Endret: `src/forecasting/forecast.py`, `src/forecasting/settings.py`, `tests/test_forecast.py`, `tests/test_rounding.py`, `sprint-status.yaml` (story 2.4 `review`) og dokumentene (statustabell med FR-7, FR-10, FR-11 og FR-12 som delvis bygd, QA-logg, KI-styringslogg tilfelle 41, arbeidslogg).
- Kjernen gir nå tre ukeprognoser, scenarioer per uke, marginbeløpet, det uavrundede resultatet (med fortegn), bestillingsmengden (gulv på 0, én avrunding opp) og lageret, og ingenting av det uten prognose. E5 gir 70 og ikke 71, E6 gir 0, E21 gir 1, og E28 viser trendetterslepet (18,0 mot 22).
- Pushet over SSH og opprettet PR #34 med en kommentar med alle 36 funnene. CI-kjøring nr. 62 og Windows-kjøring nr. 19 passerte på `5325444`, og PR #34 ble flettet lokalt med `--no-ff` 27. november kl. 09.45 (`0a17607`, foreldre `f30fc3c` og `5325444`). CI-kjøring nr. 63 på `main` passerte. Fletteloggen og `sprint-status.yaml` (story 2.4 `done`) kom i PR #35 (CI-kjøring nr. 64 grønn, flettet 27. november kl. 09.47 som `cbfba74`, og CI-kjøring nr. 65 på `main` grønn).
- Den gjenopprettede vakttesten `test_the_spreadsheet_examples_for_rounding_are_all_checked` var med i den siste kjøringen før commit (714 bestått).
- 714 tester består, 1 hoppes over (Docker), `ruff check`, `ruff format --check` og `makemigrations --check` er rene.
- 33 mutasjoner før reviewen og 36 etter: alle fanget. «Marginen på feil uke» er en ekvivalent mutant til Epic 5.
- BMAD Code Review: 36 funn fra Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. 8 grupper rettet, 10 avvist, ingen utsatt. Granskerne fant at et skript av meg hadde slettet vakttesten i `test_rounding.py`; den er gjenopprettet. Hashene av prosjektfilene var identiske før og etter, så granskerne endret ingenting.
- Flyttet fra story 2.4 til story 2.7: «–» for manglende verdi (E23) og kolonneetiketten «Uke 1 · uke 46» i `display.py`, fordi ingen skjerm viser dem ennå.
- Lukkede punkter: gulvet på 0 og den lånte formelen (story 2.3), og `stock_on_hand` i `forecast_product` (story 2.2).
- Brukeren kjørte `/export`. Eksporten ble maskert (den eneste hjemmestien, `~/G40-lyamouri` i toppteksten, ble `<project-root>`), kontrollert før og etter med skanning etter stier, brukernavn, e-poster, nøkler, passord, telefonnumre, maskinnavn og midlertidige mapper, og lagt i `.logs/mounia-03/sessions/2-4-2026-11-27.txt`. Den kommer sammen med de siste loggoppdateringene i PR #36.

### Åpne punkter
- Story 2.7: lage «–» for manglende verdi (E23) og kolonneetiketten «Uke 1 · uke 46» i `display.py` (flyttet fra story 2.4).
- Story 2.6 til 2.9: lasteren gir `horizon_weeks` den siste ISO-uka til selskapet, og visningen skriver etikettene med `display.week_label`.
- Story 2.5: erstatte flagget `weeks_repeat_week_1` med notatet og varslene.
- Epic 5: `weeks_repeat_week_1` og at bestillingen bare leser uke 1 må endres og testes når ukeprognosene kan være ulike.
