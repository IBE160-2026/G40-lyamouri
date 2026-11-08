# Sprintplanlegging for Prognose

## 2026-11-08 kl. 15:39 — 

### Oppgave
Kjøre BMAD sprint planning med godkjente epics og stories, med må-ha og fristen først. Ingen koding, ingen subagenter, og ingen commit eller push uten godkjenning.

### Plan
- `bmad-sprint-planning`: klarhetskontroll først, og deretter sprintstatusfila med skillens skript.
- Rette story 1.1 slik kontrollen anbefalte, før sprintplanen ble laget.

### Resultat
- Klarhetskontrollen ga CONCERNS: story 1.1 hadde ingen kilde for den lokale sesjonshemmeligheten (NFR-3, AD-12). Rettet etter brukerens valg: den første versjonen av `load_seed` lager bare hemmelighetsfila, og story 1.2 legger til dataene. Endringen står i endringsloggen i `epics.md`.
- `_bmad-output/implementation-artifacts/sprint-status.yaml`: 7 epics og 29 stories med status `backlog`, og 7 valgfrie retrospektiver. Skriptet varslet om to overskrifter som ikke er epics («Epic Breakdown» og «Epic List»), og det stemmer. Valideringen er bestått.
- Milepælene og rekkefølgen på bør-ha står som kommentar i sprintstatusfila:
  - epic 1 innen 11. november;
  - epic 2 innen 18. november (SM-1);
  - epic 3 innen 21. november (SM-3), og story 4.1–4.3 starter;
  - bør-ha 22.–27. november i rekkefølgen 5.1–5.3, 6.1–6.2 og 7.1;
  - sluttkontroll (4.4) og buffer 28.–30. november, og innlevering 1. desember.
- Lukket i `issues.md`: rekkefølgen på bør-ha og milepælene (PRD §10, spørsmål 1).
- Commits: `425d818` Legg til sprintplan og rett story 1.1, `e6bc1ec` Fyll inn commit i endringsloggen i epics.md og `a647a2f` Oppdater arbeidsloggen med sprintplanleggingen, pushet til GitHub sammen med denne loggen.

### Åpne punkter
- Ved commit: fylle inn commit-hashen i endringsloggen i `epics.md`.
