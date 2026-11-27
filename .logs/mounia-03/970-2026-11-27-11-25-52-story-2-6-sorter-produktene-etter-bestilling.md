# Story 2.6: sorter produktene etter hva som må bestilles først

## 2026-11-27 kl. 11:25 — Mounia-03

### Oppgave
Starte BMAD-arbeidet med story 2.6 («Sort the products by what needs ordering first») med Sonnet 5.5 High: uker dekning og «bestill snart»-status, `build_overview` (grupper, ukefigurer, gjennomgangsrekkefølge, forrige og neste produkt) og en test som kjører alle må-ha-eksemplene og regeltestproduktene mot regnearket. Beslutninger skulle legges fram før implementeringen, og ingenting skulle committes eller pushes uten godkjenning.

### Plan
- `bmad-build` med Epic 2-konteksten (gyldig) og story 2.5 som kontinuitet. Spesifikasjonen ble lagt fram med seks beslutninger og størrelsen (omtrent 2 150 tokens); brukeren godkjente beslutning 1–6 og beholdt den samlede spesifikasjonen.
- Bygge inline (ingen subagent i byggingen), mutasjonstest, BMAD Code Review med fire uavhengige, skrivebeskyttede granskere, triage, rettinger og dokumenter.
- Spesifikasjon: [spec-2-6-sort-the-products-by-what-needs-ordering-first.md](../../_bmad-output/implementation-artifacts/spec-2-6-sort-the-products-by-what-needs-ordering-first.md).

### Resultat
- Grenen `story/2-6-sort-the-products-by-what-needs-ordering-first` fra `3671eba`. Koden og testene er committet i `94e8b61` og spesifikasjonen og dokumentene i `5c12ccd`; grenen er pushet over SSH og flettet i PR #40.
- Nye filer: `src/forecasting/overview.py`, `tests/test_overview.py`, `tests/test_reference_examples.py`. Endret: `src/forecasting/forecast.py` (`ProductResult` har `weeks_of_cover` og `order_soon`). Ingen endring i modeller, migrasjoner, avhengigheter, maler, seed-filer, `display.py` eller meldingskatalogen.
- 960 tester består og 1 hoppes over (Docker); `ruff check`, `ruff format --check` og `makemigrations --check` er rene.
- Svepet kjører alle 45 må-ha-tilfellene i regnearket (E1–E13, E15–E21, E23, E24, E28, E29 og FR-21 a–d) og de 11 regeltestproduktene fra seed-filene gjennom kjernen. Testbedrift A gir 4 produkter å bestille snart, 31 enheter, 1 uten prognose og 4 med varsel, som mockupen og UX-DR46.
- Mutasjoner: 23, alle fanget. Fire overlevde først (en for svak test av likhetsbryteren, en ekvivalent mutant, to som ikke traff fordi Ruff hadde brutt linjene) og én for svak test av «bestill snart» fra det uavrundede resultatet (`steady(50, 55)` fanger den).
- BMAD Code Review: 19 funn (Blind Hunter 9, Edge Case Hunter 7, Verification Gap 0, Acceptance Auditor 3) i 13 grupper: 6 rettet, 7 avvist, ingen utsatt, ingen trengte en avgjørelse fra brukeren. Hashene av alle filer var identiske før og etter. Byggearbeidsflyten har bare tre granskerlag; Acceptance Auditor ble startet fra laget i `bmad-code-review`.
- Dokumentene er oppdatert: spesifikasjonen (`done`), statustabellen (FR-24 delvis bygd, og FR-3), QA-loggen, KI-styringsloggen (tilfelle 43), arbeidsloggen og `sprint-status.yaml` (story 2.6 `review`).
- Spørsmål 4 i PRD §10 er lukket for regeltestproduktene (se `issues.md`).
- Brukeren godkjente personvernskanning (ingen treff i tilføyde linjer og nye filer) og tre commits, og så SSH-push og pull request etter bestått kontroll, med fletting først når CI og Windows-testene er grønne på siste kodecommit. Story 2.7 er ikke startet. Sesjonseksporten og den siste dokumentasjons-PR-en tas før avslutning.
- Commit-hashene er fylt inn i QA-loggen og KI-styringsloggen (`94e8b61`).
- Pushet grenen over SSH og opprettet PR #40 med en kommentar med alle 19 funnene fra BMAD Code Review, gruppert i 13, med beslutningene og rettings-commiten (`94e8b61`). CI-kjøring nr. 74 (960 tester og Ruff) og Windows-kjøring nr. 21 passerte på `6e835e8`, siste commit på grenen.
- Flettet PR #40 etter at begge kontrollene var grønne. Claude flettet lokalt med `git merge --no-ff`, uten squash eller rebase, og med noreply-adressen som forfatter: innholdet i `main` er identisk med PR-hodet, `main` ble pushet over SSH, og GitHub viser PR #40 som flettet 27. november kl. 11.39, med `93bd2d1` som merge-commit (foreldre `3671eba` og `6e835e8`). CI-kjøring nr. 75 på `main` passerte. Grenen `story/2-6-sort-the-products-by-what-needs-ordering-first` er beholdt.
- `sprint-status.yaml` har story 2.6 som `done` (i PR-en for fletteloggen).

### Åpne punkter
- Story 2.7 og 2.8: lage «–» for manglende uker dekning (`weeks_of_cover` er `None`) og la visningen koble produktnumrene fra `build_overview` med resultatene.
- Story 2.8: lasteren (`web/company_data.py`) gir `build_overview` resultatene og en tom `adjustments`; `adjustments` gir `ValueError` til FR-29 er bygd (Epic 8).
- Story 5.2: mønsterproduktene i spørsmål 4 i PRD §10 (se punktet om E30 og R-17).
