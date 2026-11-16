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

Så ba brukeren om en kontroll av personvern og Git-identitet:
- skille mellom tillatte navn i dokumentasjonen og personopplysninger som bryter NFR-4;
- sette Git-identitet for nye commits, og spørre først om navn og e-post;
- ikke endre gamle commits eller prosjektfiler.

Til slutt ba brukeren om at sesjonsloggene flyttes til `.logs/mounia-03/` med `git mv`, og at nødvendige henvisninger og overskrifter oppdateres. All historikk og alt innhold skulle beholdes. Endringene skulle kontrolleres, arbeidsloggen oppdateres og alt committes og pushes, uten å flette grener, slette filer eller starte arkitekturen.

Etter det ba brukeren om at gamle epics, stories og `sprint-status.yaml` arkiveres før den nye arkitekturen. Den gamle koden skulle også arkiveres, så den ikke brukes i den nye arkitekturen. All dokumentasjon og Git-historikk skulle beholdes, og det skulle kontrolleres at ingen viktige filer går tapt. Grener skulle ikke flettes, og arkitekturen skulle ikke startes.

Til slutt godkjente brukeren de tre forslagene:
- lukke PR #1 med en kommentar om at den gamle koden er arkivert;
- bevare arbeidsloggoppføringene fra 10. og 11. november i arkivet;
- slette de gamle lokale filene (`__pycache__`, `.venv` og `db.sqlite3`) etter å ha kontrollert at de ikke trengs.

Arbeidsloggen og sesjonsloggen skulle oppdateres, og nødvendige endringer committes og pushes, uten å starte arkitekturen.

Så ba brukeren om en undersøkelse av de gjenværende lokale filene (`.secret_key`, `.ruff_cache`, `_bmad/render` og `.DS_Store`) og grenen `prd/teacher-feedback`, uten å slette noe.

Etter godkjenning skulle dette gjøres:
- flytte de to PRD-utkastene til arkivet og kontrollere at de er bevart;
- deretter slette de gamle lokale kopiene og de øvrige filene som var kontrollert som trygge å fjerne.

Nødvendige BMAD-, Claude- og Impeccable-filer og den arkiverte story-grenen skulle beholdes. Sesjonsloggen skulle oppdateres, uten å starte arkitekturen.

Til slutt ba brukeren om at `docs/arbeidslogg.md` oppdateres med oppryddingen som faktisk ble gjennomført, uten dobbeltføring, og at endringen committes og pushes.

### Plan
- Kartlegge sporede, usporede og ignorerte filer, grener, pull requests, like filer (kontrollsum) og store filer, bare med lesekommandoer.
- Sammenligne secret key-håndteringen og `.gitignore` med story-grenen, og legge inn en lik blokk slik at fila ikke får flettekonflikt.
- Prøveflette grenene i en isolert klon i Claudes midlertidige mappe, før og etter rettingen.
- Kontrollere filhenvisninger i dokumentene som er i bruk med et skript, uten å endre logger, memlogger og arkiv, som er historikk.
- Søke etter lokale stier, brukernavn, e-postadresser, nøkler og tokens på alle grener og i hele historikken.
- Committe i tre deler: rettelsene, arbeidsloggen og denne loggen.
- **Personvern og identitet:**
  - klassifisere hvert sted navnet står, og lese forfatteridentitetene i historikken;
  - spørre brukeren om navn og e-post;
  - sette identiteten lokalt i `.git/config`.
- **Flytting av loggene:**
  - flytte hele mappa med `git mv` og bytte brukernavnet i overskriftene;
  - kontrollere med rename-gjenkjenning og `git log --follow`;
  - prøveflette PR #1 i en isolert klon.
- **Arkivering:**
  - flytte `epics.md` og `sprint-status.yaml` med `git mv` til en ny arkivmappe;
  - bevare den gamle koden i en annotert tag på story-grenen, uten å endre grenen eller PR #1;
  - beskrive begge deler i arkivets README;
  - kontrollere fillister, rename-gjenkjenning, taggens innhold og henvisninger, og prøveflette.
- **De tre godkjente forslagene:**
  - kontrollere hver lokal fil mot taggen, `requirements.txt` og databaseinnholdet før sletting;
  - teste BMAD-skriptene uten `.venv`;
  - lukke PR #1 med `gh pr close` og en kommentar, uten å slette grenen;
  - kopiere arbeidsloggoppføringene ordrett med et skript og kontrollere kopien mot taggen.
- **Siste opprydding:**
  - undersøke hver gjenværende lokal fil og grenen med lesekommandoer;
  - flytte PRD-utkastene til arkivet, committe og pushe;
  - bevise at utkastene kan gjenskapes;
  - deretter slette med en sjekk av at ingen mål er sporet av git;
  - til slutt teste BMAD og Impeccable.

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
- **Personvern og identitet** (ingen filer ble endret i denne runden):
  - **Tillatt:**
    - personaen «Mounia», som brukeren selv valgte (se PRD-memloggen);
    - fullt navn i medlemslisten i README;
    - «Mounia-03» i BMAD-konfigurasjonen;
    - lærerens navn i lærerens 6 commits.
  - **Gråsone:** det gamle brukernavnet, som er første del av en privat e-postadresse, sto i mappenavnet og i 12 overskrifter. Hele adressen fantes ingen steder.
  - **Bryter NFR-4, men bare i historikken:** 61 commits har fullt navn, macOS-brukernavn og maskinnavn, og flettecommiten for PR #2 har skoleadressen.
  - **Git-identitet:** satt lokalt etter brukerens valg til `Mounia-03 <327966115+Mounia-03@users.noreply.github.com>`.
- **Flytting av loggene** (`6245a0a`):
  - 12 filer er omdøpt og ingen er slettet. Bare de 12 overskriftslinjene er endret.
  - `git log --follow` viser historikken. For `issues.md` er det 16 commits tilbake til 2026-10-31.
  - **Prøvefletting:** designgrenen kan flettes inn i `main` uten konflikt. Flettes PR #1 etterpå, kommer to «file location»-konflikter for 991 og 992 i tillegg. Git legger begge filene i den nye mappa. Loggene 991 og 992 har ikke det gamle brukernavnet.
  - Henvisningen til den gamle mappa i arbeidsloggoppføringen om oppryddingen er beholdt. Den beskriver PR #1 mot `main`, der mappa fortsatt har det gamle navnet.
- **Feil og retting:**
  - Arbeidsloggoppføringen (`8f6ecdf`) og commit-meldingen til `6245a0a` skrev ut det gamle brukernavnet.
  - Teksten i arbeidsloggen er rettet i `3f6d417`. Commitene er ikke endret, og navnet fantes fra før i historikken.
- **Commits med den nye identiteten:** `6245a0a` (flytting), `8f6ecdf` og `3f6d417` (arbeidsloggen), og deretter denne loggen.
- **Arkivering av gamle epics, sprintplan og kode:**
  - `epics.md` og `sprint-status.yaml` ligger nå uendret (R100) i `archive/epics-G40-lyamouri-2026-11-08/`. `git log --follow` viser historikken: 4 og 2 commits fra 2026-11-08.
  - Den gamle koden fra story 1.1 lå aldri på designgrenen. Den er bevart i den annoterte taggen `archive/story-1-1-project-skeleton`, som peker på `ffc934c`. Taggen har samme filtre som story-grenen (417 filer), med koden, spec-1-1, epic-1-context, deferred-work og loggene 991–992. Grenen og PR #1 er ikke endret.
  - Arkivets README har en rad for de arkiverte epics og en del om den gamle koden: hvor den ligger, hvordan den kan ses uten å endre grener, og at den ikke er grunnlag for den nye arkitekturen. Den gamle linjen om at `epics.md` oppdateres senere, er erstattet med en linje om den åpne linjen i PRD §12.
  - **Kontroll:**
    - 404 sporede filer før og etter, og ingen er slettet;
    - ingen dokumenter som er i bruk, peker på de gamle stiene;
    - designgrenen kan fortsatt flettes inn i `main` uten konflikt.
  - **Retting:** README-en sa først at sprintplanens datoer var passert. Bare den første milepælen (11. november) var det, og det er rettet i `652f747`.
  - **Åpne punkter som bare fantes på story-grenen:**
    - Noreply-adressen er løst.
    - Godkjenning av Vercel-appen, migreringssjekk, Ruff i Markdown og norske feilsider er samlet i ett punkt i `issues.md`.
  - **Commits:** `8f58dfb` (arkivering), `652f747` (retting) og `daa3ccb` (arbeidsloggen), og deretter denne loggen. Grenen og taggen er pushet.
- **De tre godkjente forslagene:**
  - **Lokale filer slettet etter kontroll:**
    - 19 `.pyc`-filer i åtte `__pycache__`-mapper i `accounts/`, `explanation/`, `forecasting/`, `planning/` og `prognose/`, og de fem mappene som ble tomme;
    - `.venv` (93 MB);
    - `db.sqlite3` (76 KB).
  - **Kontroll før slettingen:**
    - alle `.pyc`-filene har kilde i taggen;
    - ingen av filene har vært committet på noen gren;
    - `.venv` (Python 3.13) har de samme pakkene som `requirements.txt` i taggen;
    - databasen hadde bare Djangos skjema, 16 migreringer og ingen bedrifter eller økter;
    - ingenting på grenen bruker `.venv` eller databasen.
  - **Kontroll etter slettingen:**
    - git er uendret (404 sporede filer);
    - `memlog.py`, `resolve_config.py` og `resolve_customization.py` for `bmad-architecture` virker med `uv run` uten `.venv`, og ingen ny `.venv` ble laget.
    - `.secret_key`, `.ruff_cache`, `_bmad/render` og `.DS_Store` er beholdt.
  - **PR #1** er lukket uten fletting, med en kommentar om arkiveringen. Grenen `story/1-1-project-skeleton` ligger fortsatt på GitHub (`ffc934c`).
  - **Arbeidsloggoppføringene** fra 10. og 11. november er kopiert ordrett, 34 linjer, fra taggen til `archive/story-1-1-G40-lyamouri-2026-11-10/arbeidslogg.md`. Kopien er kontrollert linje for linje mot taggen. Arkivets README viser til den og sier at PR #1 er lukket. Sesjonsloggene 991–992 ligger fortsatt bare i taggen.
  - **Retting:** én kontroll med `sed` feilet på macOS. Ingenting ble committet, og kontrollen ble gjort på nytt med Python.
  - **Commits:** `1a0709e` (arkivkopi og README) og `dc6e12a` (arbeidsloggen), og deretter denne loggen.
- **Siste opprydding:**
  - **Undersøkelse:**
    - `.secret_key`: 67 byte, rettighet 600, laget av `load_seed` 10. november. Bare den arkiverte koden bruker den.
    - `.ruff_cache`: 18 filer fra Ruff 0.17.4.
    - To `.DS_Store`-filer med Finders visningsinnstillinger.
    - `_bmad/render/bmad-build`: BMADs mellomlager for skillen, 15 filer.
    - `_bmad/render/bmad-review`: to diff-filer, som var de eneste kopiene av to mellomutkast av PRD-en fra 15. november.
    - `prd/teacher-feedback`: flettet gjennom PR #2, uten commits som ikke er i `main`.
  - **PRD-utkastene** (`d2bfad2`, pushet):
    - De er flyttet uendret (samme SHA-256) til `archive/prd-drafts-G40-lyamouri-2026-11-15/`.
    - Arkivets README beskriver dem.
    - I en isolert klon kan begge brukes på PRD-versjonen de bygger på, og de gir nøyaktig fil-ID-ene i diffene (`2c20a02`/`2dc932b` og `fd5506c`/`a92f52c`).
  - **Slettet:**
    - `.secret_key`, `.ruff_cache/` og to `.DS_Store`;
    - `_bmad/render/bmad-build/` og den tomme `_bmad/render/bmad-review/`;
    - grenen `prd/teacher-feedback`, lokalt og på GitHub. Commit `89d4a91` er fortsatt i `main`, og PR #2-siden kan gjenopprette grenen.
  - **Beholdt:**
    - `_bmad/render/.gitignore` og `.claude/settings.local.json`;
    - Impeccable-motoren og `.impeccable/hook.cache.json`;
    - de to `config.user.toml`-filene og de tomme BMAD-mappene;
    - `story/1-1-project-skeleton` og arkivtaggen.
  - **Kontroll etterpå:**
    - BMAD-skriptene og oppsettet for `bmad-architecture` virker.
    - `impeccable context` finner `docs/PRODUCT.md` og `docs/DESIGN.md` uten å be om nytt design.
    - Git sporer 407 filer, og arbeidsmappa er ren.
  - **Feil og retting:** den første slettekommandoen stoppet før noe ble slettet, fordi sjekken av sporede filer ga feil returkode for filer som ikke var sporet. Det ble kontrollert at alt fortsatt fantes, og kommandoen ble kjørt på nytt med en riktig sjekk.
  - **Commit:** `d2bfad2` (PRD-utkastene), og deretter denne loggen. Arbeidsloggen er ikke oppdatert i denne runden, fordi brukeren ba om sesjonsloggen.
- **Arbeidsloggen** (`19911b1`):
  - Én ny oppføring, «Oppryddingen fullført», har bare den siste delen: PRD-utkastene, slettingen og kontrollen av BMAD og Impeccable.
  - De fire tidligere oppføringene om oppryddingen samme dag er ikke gjentatt, og det finnes ingen like overskrifter.

### Åpne punkter
- **Åpne punkter fra story 1.1**, som bare finnes i taggen:
  - eieren av IBE160-2026 må godkjenne Vercels GitHub-app;
  - migreringssjekk før pull requester;
  - Ruff og Python-blokker i Markdown;
  - norske feilsider for 400, 403 og CSRF.

  De vurderes i den nye arkitekturen.
- **PRD §12:** den åpne linjen om å rette `epics.md` og arkitekturspinen lukkes når ny arkitektur og nye epics finnes.
- **`.gitignore`:** Next.js-delen trengs ikke etter PRD-en og ryddes når stakken er valgt.
- **Lenkene inne i `DESIGN.md`** virker ikke når fila leses gjennom `docs/DESIGN.md`. Det kan ikke rettes uten å endre det godkjente designet.
- **QA-loggen:** beskriv de gamle commit-identitetene ved innlevering (NFR-4, DR-9). Det gjelder 61 automatiske identiteter og én commit med skoleadressen.
- **GitHub og andre kloner:**
  - Slå på «Keep my email addresses private» under Settings → Emails.
  - Sett samme Git-identitet i andre kloner, fordi den bare er satt i dette repoet.
