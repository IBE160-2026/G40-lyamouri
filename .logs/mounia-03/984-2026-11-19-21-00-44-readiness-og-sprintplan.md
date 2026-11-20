# Readiness og sprintplan

## 2026-11-19 kl. 21:00 — Mounia-03

### Oppgave
Brukeren kjørte `bmad-help` for å se neste steg, og deretter `bmad-sprint-planning`, først bare kontrollen av Implementation Readiness. Etter kontrollen ville brukeren gå videre steg for steg: bestemme milepæler og prioriteringer sammen før noen filer ble endret, ta med rettingene fra kontrollen i samme arbeidsrunde og se de konkrete endringene før de ble skrevet. Ingenting skulle committes eller pushes før brukeren har godkjent det.

### Plan
- `bmad-help`: lese katalogen, konfigurasjonen, artefaktene, loggene og `issues.md`, og anbefale neste steg.
- Implementation Readiness (`references/readiness-gate.md` i skillen): lese PRD-en, arkitekturspinen, UX-spinene og `epics.md`, kontrollere sporbarhet, avhengigheter og motstrid med et skript i scratchpad, og prøvekjøre sprintskriptet uten å skrive fil.
- Sprintplanleggingen steg for steg: et forslag til milepæler og prioriteringer, oppdatert med brukerens opplysninger, deretter de konkrete endringene som diff, og først etter godkjenning skriving, kontroll og logging.
- Sprintplanen: [`sprint-plan.md`](../../_bmad-output/implementation-artifacts/sprint-plan.md).

### Resultat
- **`bmad-help`:** planleggingen er ferdig. Product Brief, PRD, UX, arkitekturspinen og `epics.md` er `final`, og neste påkrevde steg var sprintplanlegging. PR #5 var flettet inn i `main` (`5445a2f`) før økten.
- **Implementation Readiness: CONCERNS.**
  - Alle 37 FR og alle NFR, AG, DR, SM og UX-DR1–46 er dekket av minst én story, unntatt SM-9, som ikke er i v1. Alle henvisninger til AD, D og UX-DR finnes, og ingen story avhenger av en senere story.
  - Funnene:
    1. milepælene manglet et sted å stå, fordi `sprint-status.yaml` bare har statuser;
    2. tekst fra publiseringen sto igjen i `epics.md` og addendumet;
    3. spinen sa både `uv sync` og `uv sync --locked`;
    4. story 1.8 bruker `forecasting/display.py` før story 2.3 lager den.
- **Brukerens beslutninger:**
  - fristen er 8. desember 2026 kl. 23.59, og endringsloggene sier ikke hvor den kommer fra;
  - brukeren jobber 5–6 timer hver dag, også i helgene;
  - Windows-PC-en er tilgjengelig 25. november og 7. desember;
  - SM-10 gjennomføres 3.–4. desember, etter bestått SM-3, uten unntak fra PRD-en;
  - milepælene M0–M6, testdatoene, rekkefølgen og reserverekkefølgen er godkjent. Alle må-ha-stories prioriteres, og story 4.4 kommer sist;
  - rettinger etter sluttkontrollen 7. desember gir en ny endelig versjon, som kontrolleres på nytt.
- **Nye filer** i `_bmad-output/implementation-artifacts/`:
  - `sprint-plan.md`, med grunnlag, milepæler, testdatoer, rekkefølge, reserverekkefølge og endringslogg;
  - `sprint-status.yaml`, laget med `sprint_plan.py generate`: 8 epics, 38 stories med status `backlog` og 8 valgfrie retrospektiver. `story_location` er en relativ sti.
- **Endrede filer,** med rader i endringsloggene:
  - PRD-en: sammendraget, DR-6, §8.2 og en rad i §12;
  - addendumet: §2 (bare lokal kjøremodus siden 2026-11-19), §5 (ny dato for å kontrollere kildene på nytt) og §7 (fristen);
  - teknologinotatet: fristen i «Oppdatert» og i «Kort fortalt»;
  - arkitekturspinen: «Commands» med `uv sync --locked`, og en rad i endringsloggen;
  - `epics.md`:
    - DR-6 og fristregelen, med lenke til sprintplanen;
    - NFR-1 og NFR-2 på hver sin linje, og AD-13 uten «in both modes»;
    - «Configuration» med `PROGNOSE_LAN_HOST`, uten databaseadressen fra publiseringen;
    - «Commands» og story 1.1 med `uv sync --locked`;
    - story 5.1 og 8.2 med AD-15 i stedet for AD-16;
    - to rader i endringsloggen;
  - `docs/arbeidslogg.md`: en ny oppføring for 19. november.
- **AD-15** er riktig henvisning i story 5.1 og 8.2. Regelen sier at `load_seed --reset` er den eneste kommandoen som sletter data, og story 8.2 bruker allerede AD-15 om tilbakestillingen.
- **Kontroller:**
  - `lint_spine.py` fant 0 feil;
  - `sprint_plan.py validate` godkjente `sprint-status.yaml`, og en ny prøvekjøring etter endringene viste at fila er i takt med `epics.md`;
  - kontrollskriptet viste samme dekning som før. AD-16 står bare i historikk og endringslogger, og `uv sync` uten `--locked`, «in both modes» og databaseadressen fra publiseringen står ikke igjen utenfor endringsloggene;
  - personvernskanningen av de 175 nye linjene fant ingen lokale stier, e-postadresser eller hemmeligheter.
- **Nytt funn etter endringene:** addendum §2 (linje 55) sa fortsatt «to be re-checked by 2026-12-01, §5», mens §5 nå sier 2026-12-08. Linjen var ikke med i de første godkjente endringene. Etter brukerens godkjenning ble den rettet til 2026-12-08, og raden i PRD §12 nevner nå begge datoene i addendumet (§2 og §5). Kontrollene ble kjørt på nytt etter rettingen.
- **`issues.md`:**
  - punktet om nye epics og sprintplan er lukket;
  - punktene om README-sekvensen, oppsettstiden, Impeccable-gjennomgangen, sluttkontrollen og jobb-PC-en har fått merknader;
  - to nye punkter: ukeetiketten i story 1.8, som er åpent, og datoen i addendum §2, som ble lukket samme dag.
- **Git:** alle endringene er laget på grenen `plan/sprint-planning`. Brukeren godkjente commit, push og pull request mot `main` etter at kontrollene besto og Git-status bare viste de avtalte filene. Endringene er committet i `67694f7` og pushet, og [PR #6](https://github.com/IBE160-2026/G40-lyamouri/pull/6) mot `main` er opprettet. Commit-hashen og PR-nummeret er ført inn i endringsloggene i en egen commit. Etter brukerens godkjenning ble PR #6 flettet lokalt med «Create a merge commit» og noreply-adressen. Merge-commiten er `41fe0cf`, og GitHub viser PR #6 som flettet 19. november kl. 21.23. Lokal `main` og GitHub ble synkronisert på `41fe0cf`, og arbeidskopien var ren.

### Åpne punkter
- Story 1.8 må selv lage ukeetiketten i `forecasting/display.py`, med test, fordi toppfeltet viser den før story 2.3 bygger ut modulen. Story 2.3 bygger videre på den.
