# Story 2.5: varsler, notater og tillitsmerke

## 2026-11-27 kl. 10:28 — Mounia-03

### Oppgave
Starte BMAD-arbeidet med story 2.5 («Give each product its warnings, notes and confidence label») med Sonnet 5.5 High: bygge de aktive varslene, notatene og tillitsmerket i kjernen med tekstene fra meldingskatalogen, teste dem mot referanseregnearket med mutasjoner, kjøre BMAD Code Review med alle fire uavhengige, skrivebeskyttede granskere, dokumentere alt og legge fram beslutningene før implementeringen. Ingen commit eller push uten godkjenning.

### Plan
- `bmad-build` med epic 2-konteksten (gyldig) og story 2.4 som kontinuitet. Spesifikasjonen ble lagt fram med to beslutninger (frasen for gamle data, og om meldingskatalogen skulle få den). Brukeren valgte alternativ A på begge, og godkjente implementeringen.
- Kompilere epic 2-konteksten på nytt etter endringen i `EXPERIENCE.md`.
- Bygge `src/forecasting/trust.py`, `src/explanation/trust.py` og `week_at_position`, tester fra regnearket og seed-dataene, mutasjonstester, BMAD Code Review (fire lag), triage, rettinger og dokumentene.
- Spesifikasjon: [spec-2-5-give-each-product-its-warnings-notes-and-confidence-label.md](../../_bmad-output/implementation-artifacts/spec-2-5-give-each-product-its-warnings-notes-and-confidence-label.md).

### Resultat
- Grenen `story/2-5-give-each-product-its-warnings-notes-and-confidence-label` fra `b27a277`. Brukeren ba om å få godkjenne før noe ble committet, avgjorde de to funnene som ble lagt fram, og godkjente tre commiter, SSH-push og pull request. Koden, testene og katalogen i `e74a814`, spesifikasjonen og dokumentene i `0dac0f7`, og denne loggen i den siste commiten. Personvernskanningen av alle tilføyde linjer og nye filer fant ingenting. Grenen ble pushet over SSH og PR #37 opprettet med en kommentar med alle 26 funnene; CI-kjøring nr. 68 og Windows-kjøring nr. 20 passerte på `c50e400`, og PR-en ble flettet lokalt med `--no-ff` (`747244a`, foreldre `b27a277` og `c50e400`, 27. november kl. 10.45) og `main` pushet over SSH. CI-kjøring nr. 69 på `main` passerte.
- Nye filer: `src/forecasting/trust.py`, `src/explanation/trust.py`, `tests/test_trust.py`, `tests/test_trust_texts.py`, `tests/test_trust_seed.py`. Endret: `src/forecasting/forecast.py` (`ProductResult` har `warnings`, `notes`, `confidence_label`, `confidence_condition` og flere felt; `weeks_repeat_week_1` er erstattet av `notes`), `src/forecasting/horizon.py` (`week_at_position`), `tests/test_horizon.py`, `tests/test_week_forecasts.py`, `EXPERIENCE.md` (begrunnelsesraden og en rad i endringsloggen), `epic-2-context.md`, `sprint-status.yaml` (story 2.5 `review`) og dokumentene (statustabell, QA-logg med to avsnitt, KI-styringslogg tilfelle 42, arbeidslogg). Ingen modell, migrasjon, avhengighet, mal eller seed-endring.
- 877 tester består og 1 hoppes over (Docker), `ruff check`, `ruff format --check` og `makemigrations --check` er rene.
- Mutasjoner: 42 før reviewen og 45 etter, alle fanget. Skriptet ga først foreldet bytekode (en mutasjon og tilbakestillingen i samme sekund), så alle 45 ble kjørt på nytt med bytekode av og tømt cache. Én overlevde først (R-16 telte kalkulasjonsuker i stedet for gyldige uker), og en ny test fanger den.
- BMAD Code Review: 26 funn fra Blind Hunter, Edge Case Hunter, Verification Gap (ingen) og Acceptance Auditor. 8 grupper rettet, 2 avgjort av brukeren (frasen om gamle data er merket som vakttilfelle i katalogen, og entallet «Produktet har 1 gyldig uke.» er lagt inn) og 10 avvist, ingen utsatt. Hashene av alle filer var identiske før og etter, så granskerne endret ingenting. Jeg skrev en feil sti til diff-filen i prompten til én granske og rettet den med en melding før den rapporterte.
- Lukkede punkter: `no_forecast_reason`, `required_calculation_weeks`, `unusual_weeks` og `level_shift_weeks` i varslene (story 2.2), og flagget `weeks_repeat_week_1` (story 2.4).

### Åpne punkter
- Story 2.6 til 2.9: lasteren gir `warning_texts` den siste ISO-uka til selskapet, og skjermene viser varslene, notatet og begrunnelsen fra `explanation/trust.py`.
- Story 5.2 og FR-17b: legge til tekstene for nytt nivå og sesongmønster i `warning_texts`, som feiler høyt til de finnes.
- Eksporten av økta med `/export` til `.logs/mounia-03/sessions/2-5-2026-11-27.txt` er ikke gjort: brukeren kjører den, og Claude maskerer og committer den.
