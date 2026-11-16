# Forberedelse av nytt designarbeid

## 2026-11-15 kl. 21:50

### Oppgave
Hente oppdatert `main` fra GitHub, opprette en ny gren for designarbeidet, arkivere gammelt UX-design og gammel arkitektur uten å slette historikken, og kontrollere at den oppdaterte PRD-en er grunnlaget. Selve designarbeidet skulle ikke startes, og ingenting skulle committes eller pushes.

### Plan
- Hente `main` med `git pull --ff-only`, slik at PR #2 kom med.
- Lage den nye grenen `design/after-prd-feedback` fra `main`.
- Flytte den gamle UX-mappen og arkitekturmappen til `_bmad-output/planning-artifacts/archive/` med `git mv`, og legge til en README der.
- Kontrollere PRD-en, og finne ut hva som fortsatt viser til de gamle stiene.

### Resultat
- **`main`:** lokal `main` er spolt fram til `87d9abc` (PR #2) og er lik GitHub.
- **Ny gren:** `design/after-prd-feedback`, laget lokalt fra `87d9abc`.
- **Arkivert:** `ux-G40-lyamouri-2026-11-06/` og `architecture-G40-lyamouri-2026-11-08/` ligger nå i `_bmad-output/planning-artifacts/archive/`.
  - Flyttingen ble gjort med `git mv` og gir 16 omdøpinger, alle 100 % like, så historikken følger filene.
  - En README i arkivet forklarer hvorfor mappene er arkivert, og hva som er grunnlaget nå.
- **Ikke arkivert:** lærerens `architecture/technology.md`. Den beskriver oppsettet i et annet prosjekt og er et innspill til den nye arkitekturen.
- **Grunnlaget:** PRD-en har status `final`, er oppdatert 2026-11-15, er lik `main` på GitHub og er den eneste PRD-en. Det finnes ingen gjeldende UX eller arkitektur utenfor arkivet.
- **Status:** endringene er staget, men ikke committet eller pushet. Designarbeidet er ikke startet.

### Åpne punkter
- Lage nytt UX-design (`bmad-ux`) og ny arkitektur (`bmad-architecture`) fra den oppdaterte PRD-en på `design/after-prd-feedback`, og vurdere lærerens `technology.md` i arkitektursteget.
- Når det nye designet og den nye arkitekturen finnes, må `epics.md` oppdateres: FR-17b, story 3.3 og 7.1, SM-10 og de tre henvisningene til arkiverte stier. Det samme gjelder unntakene i `.impeccable/config.json`.
- `.secret_key` og `db.sqlite3` er heller ikke git-ignorert på denne grenen før PR #1 er flettet. Det står alt i `issues.md` (punktet fra 2026-11-15).
