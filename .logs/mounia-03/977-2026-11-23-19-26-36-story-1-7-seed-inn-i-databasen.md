# Story 1.7 – seed-dataene inn i databasen, med en eksplisitt nullstilling

## 2026-11-23 kl. 19:26 — Mounia-03

### Oppgave
Starte story 1.7 («Load the seed data into an empty database, with an explicit reset») etter prosjektreglene, BMAD og sensorveiledningen: kontrollere at `main` er ren og synkronisert, lese bare de nødvendige filene, lage spesifikasjon, implementere, teste og kjøre BMAD Code Review med fire uavhengige granskere. Brukeren ba om at Claude skulle:
- bruke subagenter bare til gjennomgangene, dokumentere faktiske resultater og spørre ved faglige beslutninger;
- be om manuelle tester og `/export` når det trengs;
- committe, pushe, opprette PR og flette først etter godkjenning, og føre fletteloggen etter etablert rutine;
- stoppe ved feil eller usikkerhet, ikke lese utenfor prosjektmappen og ikke starte story 1.8.

### Plan
- `bmad-build` med den fulle ruten, på grenen `story/1-7-load-the-seed-data-with-an-explicit-reset`, laget fra `main` (`16d93b7`). Spesifikasjonen er [spec-1-7-load-the-seed-data-with-an-explicit-reset.md](../../_bmad-output/implementation-artifacts/spec-1-7-load-the-seed-data-with-an-explicit-reset.md).
- Epic-1-konteksten var formelt utdatert, men endringene i PRD-en og spinen gjelder ikke story 1.7, så Claude brukte den som den var. Byggingen og Blind Hunter i byggeøkten ble gjort uten subagent, og subagenter ble bare brukt til BMAD Code Review (D-8).
- Brukeren godkjente spesifikasjonen slik den var (om lag 2 600 tokens), med ordet «nullstill» som bekreftelse og justeringen av klonesteget i Windows-jobben. Claude valgte selv at en avvist bekreftelse gir en feil, og at lesingen ligger i `web/seed.py`.
- Reviewen ga ingen funn som trengte en beslutning, så Claude gjorde patchene og sa fra om det. Brukeren kjørte omstartssjekken på macOS (Docker), siden Docker ikke er på Claudes PATH.

### Resultat
- **Koden** (commit `85308ac`): `src/forecasting/settings.py` (FR-20-verdiene én gang), modellene `Product`, `SalesWeek` og `CompanySettings` med migrasjon `0002`, `src/web/seed.py` (leser og validerer filene uten database), `load_seed` med `--reset` og skrevet bekreftelse i én transaksjon, og `SEED_DIR` i innstillingene. `.secret_key` lages før kommandoen stopper på en database med data (punktet fra story 1.1). Hashen lastes uendret, så en innlogging ikke skriver den om.
- **Tester:** 238 tester passerer, 1 hoppes over (Docker-sjekken, fordi Docker ikke er på PATH i Claudes skall), og Ruff og `makemigrations --check` er grønne. 66 nye tester i `tests/test_load_seed.py`, `tests/test_seed_reader.py` og `tests/test_forecasting_settings.py`, og en ny test i `tests/test_reference_spreadsheet.py` (BH-3). 11 feil som ble lagt inn én om gangen, ble alle fanget. Kommandoene ble kjørt mot den lokale databasen: 2 bedrifter, 62 produkter og 5 016 salgsuker, og en ny kjøring stoppet med den norske meldingen.
- **BMAD Code Review** med fire uavhengige KI-granskere på arbeidstreet: 46 funn (7 middels, 39 lave), 20 rettet, 2 utsatt, 4 feil og 20 avvist. Blant de rettede: en melding som viste hele den lokale stien, grenser i leseren som ikke fulgte kolonnene, og et Windows-steg som godtok hvilken som helst feil. Fullt resultat under «Review Triage Log» i spesifikasjonen, [tilfelle 36](../../docs/ki-styringslogg.md#36-grensene-i-leseren-og-reviewen-av-story-17-23-november-2026) og [QA-loggen](../../docs/qa-logg.md#2026-11-23--feil-i-ki-generert-kode-og-tekst-fra-bmad-code-review-av-story-17-dr-9).
- **Omstartssjekken** (FR-4, SM-5), kjørt av brukeren på macOS: 2 bedrifter, 62 produkter, 5 016 salgsuker og 2 innstillinger uendret etter Docker-omstart, `window=5` bevart, `--reset` med «nullstill» satte den tilbake til 3, og «nei» endret ingenting ([QA-loggen](../../docs/qa-logg.md#2026-11-23--omstartssjekken-av-dataene-story-17-fr-4-sm-5)). FR-4 står som bygd i statustabellen, og FR-20 som delvis bygd.
- **Avvik fra BMAD:** Claude gjorde patchene uten å vente på valget i trinn 5 i `bmad-code-review`, og brukeren fikk se dem før commiten. Loggfilene ligger i commiten med dokumentene, ikke i en egen tredje commit, fordi brukeren godkjente to commits.
- **Eksporten** `.logs/mounia-03/sessions/1-7-2026-11-23.txt` er maskert: den ene stien til prosjektmappa ble `<repo>`, og stien til den midlertidige mappa ble `<scratchpad>`. Kontrollen etterpå fant ingen lokale stier, brukernavn, e-poster, nøkler eller tokens.
- **Flettingen:**
  - Etter brukerens godkjenning ble koden og dokumentene committet (`85308ac` og `b3b5157`), og grenen ble pushet over SSH. PR #20 ble opprettet med en kommentar med alle 46 funnene.
  - CI-kjøring nr. 34 og Windows-kjøring nr. 14 passerte på `b3b5157`. Windows lastet 62 produkter og 5 016 salgsuker, og klonesteget fikk meldingen «Databasen har allerede data», så Windows-steget er verifisert.
  - Claude flettet lokalt med `git merge --no-ff` (merge-commit `10b048a`, foreldre `16d93b7` og `b3b5157`) og pushet `main` over SSH. Det første forsøket feilet på et flagg som `git merge` ikke har, før noe var flettet. GitHub viser PR #20 som flettet 23. november kl. 19.29, og CI-kjøring nr. 35 på `main` passerte. Grenen er beholdt.
  - Story 1.7 står som `done` i sprintstatusen og i spesifikasjonen. Story 1.8 er ikke startet.

### Åpne punkter
- Story 3.1: modellen `CompanySettings` har ingen validering av grensene i FR-20, bare testene bruker dem (`deferred-work.md`, BH-6 og EC-10).
- Story 4.4: gjenta omstartssjekken (FR-4, SM-5) på siste commit, også på Windows, der den ikke er kjørt.
