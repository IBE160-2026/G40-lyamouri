# Opprydding før arkitekturen

## 2026-11-16 kl. 20:26

### Oppgave
Først ba brukeren om en gjennomgang av prosjektmappa:
- finne utdaterte, unødvendige eller doble filer;
- foreslå hva som bør beholdes, arkiveres eller slettes;
- ikke endre eller slette noe, og bevare all viktig dokumentasjon og Git-historikken.

Deretter ba brukeren om at alle kjente problemer ryddes opp før BMAD-arkitekturen:
- kontrollere og rette secret key etter DR-2;
- rette datoen i arkivets README;
- undersøke grenene for konflikter som kan forebygges;
- kontrollere samsvar med PRD-en, filhenvisninger og personvern.

Designkonseptene A–D og all viktig dokumentasjon skulle beholdes. Ingen filer skulle slettes, historikken skulle ikke skrives om, og ingen grener skulle flettes uten godkjenning. Trygge rettelser skulle committes og pushes, arbeidsloggen oppdateres og arkitekturen ikke startes.

### Plan
- Kartlegge sporede, usporede og ignorerte filer, grener, pull requests, like filer (kontrollsum) og store filer, bare med lesekommandoer.
- Sammenligne secret key-håndteringen og `.gitignore` med story-grenen, og legge inn en lik blokk slik at fila ikke får flettekonflikt.
- Prøveflette grenene i en isolert klon i Claudes midlertidige mappe, før og etter rettingen.
- Kontrollere filhenvisninger i dokumentene som er i bruk med et skript, uten å endre logger, memlogger og arkiv, som er historikk.
- Søke etter lokale stier, brukernavn, e-postadresser, nøkler og tokens på alle grener og i hele historikken.
- Committe i tre deler: rettelsene, arbeidsloggen og denne loggen.

### Resultat
- **Gjennomgang (ingen endringer):**
  - Git sporer 403 filer, og ingen er store.
  - De like filene er bevisste: lenken `docs/DESIGN.md`, konsept D i `.working/` og i `mockups/`, og fem par inne i BMAD-skillene.
  - Lokale rester fra story 1.1 er ignorert og ikke slettet: `__pycache__` i `accounts/`, `explanation/`, `forecasting/`, `planning/` og `prognose/`, `.ruff_cache/`, `_bmad/render/` og `.DS_Store`.
  - `.venv/`, `db.sqlite3` og `.secret_key` hører til skjelettet i PR #1.
  - `epics.md` og `sprint-status.yaml` er utdatert, og PR #1 (story 1.1) er åpen og bygger på den arkiverte arkitekturen.
- **Secret key (DR-2, NFR-3):**
  - Ingen gren har noen gang committet `.secret_key`, `db.sqlite3` eller `.env`.
  - Story-grenen lager nøkkelen med `load_seed` (rettighet 600). Til fila finnes, bruker den en tilfeldig nøkkel i minnet, og på Vercel krever den miljøvariabler.
  - `.gitignore` på `design/after-prd-feedback` har nå samme blokk som story-grenen, byte for byte: `db.sqlite3*`, `staticfiles/` og `.secret_key`.
  - `git check-ignore` bekrefter regelen, og de to filene vises ikke lenger som usporede.
  - Alle DR-2-punktene for `.gitignore` er kontrollert med eksempelstier, og seed-dataene blir fortsatt versjonert.
- **Arkivets README:** statuslinjen sier nå at PRD-en sist ble oppdatert 2026-11-16. Oppdateringen fra 2026-11-15 er i `main` gjennom PR #2, og endringene fra 2026-11-16 ligger på designgrenen. Det er kontrollert med `git merge-base`.
- **Prøvefletting** (isolert klon, slettet etterpå):
  - Designgrenen kan flettes inn i `main` uten konflikt, både før og etter rettingen.
  - PR #1 har konflikt med `main` i `issues.md` og `docs/arbeidslogg.md`, og GitHub viser den som «CONFLICTING». Begge sider har lagt til oppføringer på samme sted.
  - Den like `.gitignore`-blokken gir ingen ny konflikt i noen rekkefølge.
- **Filhenvisninger:** 57 uløste henvisninger i 9 dokumenter. Nesten alle er falske treff: planlagte kodestier, et annet prosjekts filer i `technology.md`, grennavn og stier relative til en annen mappe.
  - Ekte brutte henvisninger finnes bare i `epics.md`: de arkiverte mockupene, `PRODUCT.md` i rotmappen og de gamle inndatastiene.
  - De relative lenkene inne i den godkjente `DESIGN.md` virker ikke når fila leses gjennom `docs/DESIGN.md`.
- **Personvern:**
  - Ingen lokale stier, brukernavn, e-postadresser, private nøkler, tokens eller innebygde Django-nøkler finnes i noen fil på noen gren eller i historikken.
  - De to database-adressene på story-grenen er falske testverdier (bruker «u», vert «h»).
  - Navnet står i `README.md` (medlemsliste), som persona i PRD-en og UX-en og i BMAD-konfigurasjonen. Det har ligget i `main` siden 3. november.
  - 58 commits på alle grener har automatisk forfatter med brukernavn og maskinnavn.
- **Commits på `design/after-prd-feedback`:** `d67211c` (`.gitignore` og arkivets README) og `33b65aa` (arbeidsloggen), og deretter denne loggen. Alt er pushet. Ingenting er flettet, slettet eller skrevet om.

### Åpne punkter
- **PR #1 har konflikt med `main`** i `issues.md` og `docs/arbeidslogg.md`. Den løses ved å beholde begge sider i datorekkefølge. Den kan forebygges ved å oppdatere PR #1 med `main`, men det er en fletting og krever godkjenning. Flettes designgrenen først, må konflikten bare løses én gang.
- **PR #1 og story-grenen** bygger på den arkiverte arkitekturen. De avklares i arkitektursteget og flettes ikke før det.
- **`epics.md` og `sprint-status.yaml`:** forslaget er å arkivere dem med `git mv` når nye epics og ny sprintplan lages etter arkitekturen.
- **Valgfri opprydding som krever godkjenning:** de lokale restene og cachene, og grenen `prd/teacher-feedback`, som er flettet gjennom PR #2.
- **`.gitignore`:** Next.js-delen trengs ikke etter PRD-en og ryddes når stakken er valgt.
- **Lenkene inne i `DESIGN.md`** virker ikke når fila leses gjennom `docs/DESIGN.md`. Det kan ikke rettes uten å endre det godkjente designet.
- **Navn og NFR-4:** avklar om navnet i README, personaen i PRD-en og UX-en og BMAD-konfigurasjonen er greit. NFR-4 sier at filene ikke skal ha personopplysninger.
- **Git-identitet:** 58 commits har automatisk forfatter. Det kan bare rettes ved å skrive om historikken.
