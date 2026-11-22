# Story 1.3 – oppsett på Windows og uten nett

## 2026-11-22 kl. 15:26 — Mounia-03

### Oppgave
Starte story 1.3 («Confirm the setup on Windows and without a network») med BMAD, lære av arbeidsmåten i story 1.2, jobbe selvstendig og effektivt, unngå unødvendige spørsmål, subagenter og dobbeltarbeid, og ikke committe eller pushe uten godkjenning. Senere samme dag:
- Etter testen uten nett på macOS: lese testloggene og oppdatere QA-loggen og den relevante dokumentasjonen.
- Brukeren kan ikke installere noe på jobb-PC-en og mente bare å teste den ferdige nettsiden i en nettleser på Windows. Story 1.3 skulle derfor oppfylles uten installasjon der, med et skille mellom nettlesertesten og oppsettet på Windows uten nett, en enkel alternativ testmetode og begrensningene dokumentert, uten å endre kravene.
- BMAD Code Review av story 1.3, testen uten nett på macOS på nytt, og alle rettingene i én runde.
- Eksporten av økten med maskering, sesjonsloggen og `issues.md`, med godkjenning før commit, push og fletting.

### Plan
- `bmad-build` på grenen `story/1-3-windows-and-offline-setup`, laget fra `main` (`850250d`). Epic-1-konteksten var gyldig, så ingen subagent trengtes. Storyen fulgte «oneshot»-ruten; spesifikasjonen er [spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md](../../_bmad-output/implementation-artifacts/spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md).
- Testen uten nett på macOS: Claude skrev skript i den midlertidige mappa for økten, og brukeren kjørte dem i Terminal og slo selv nettet av og på, fordi økten mister forbindelsen uten nett. Skriptene sletter ingen data: `docker compose down` beholder volumet.
- Windows: første akseptkriterium har en reserve når ingen Windows x64-PC kan brukes. Brukeren valgte å føre begrensningen i QA-loggen, README og statustabellen (D-3) og å la `.github/workflows/windows-setup.yml` teste oppsettet uten Docker på GitHubs Windows-maskin. Nettlesertesten på Windows hører til NFR-6 og story 4.4.
- BMAD Code Review med fire subagenter, som BMAD krever. Brukeren tok to beslutninger og godkjente resten.
- Eksporten: bare delen etter eksporten for story 1.2 beholdes, som for story 1.2.

### Resultat
- **macOS uten nett:** kjøring 1 (09.34–09.44, `850250d`) passerte, men Docker Desktop var trolig ikke avsluttet. Kjøring 2 (14.56–14.58, `fedaef2`) passerte med Docker Desktop helt avsluttet og nettet av: Docker Desktop svarte etter 6 sekunder, databasen var klar etter 4, og Prognose svarte 200 etter 2. Testen fant at Terminal ikke fant `docker`. README er rettet (`3363596`, `fedaef2`), og i kjøring 2 fant et nytt Terminal-vindu `docker`.
- **Windows:** ingenting kan installeres på jobb-PC-en, og gruppen har ingen annen Windows x64-PC, så oppsettet med Docker Desktop og oppstarten uten nett er ikke testet på Windows. Windows-workflowen (`0eaea95`, rettet i `fedaef2`) passerte i kjøring 1–4. Kjøring 3 på `fedaef2` lastet ned CPython 3.13.15 og viste at bare SYSTEM, administratorene og brukeren kunne lese `.secret_key` i en klone i brukermappa.
- **BMAD Code Review:** 46 funn fra fire granskere, samlet i 24 punkter: 2 beslutninger (kjøre macOS-testen på nytt; kjøre Windows-testen også for `src/**` og `.python-version`), 19 rettet, 1 utsatt (Windows-versjonene, `deferred-work.md`) og 2 avvist. Funnene står i [kommentaren i PR #12](https://github.com/IBE160-2026/G40-lyamouri/pull/12#issuecomment-7080488795).
- **Commits på grenen:** `3363596`, `683e13f`, `5f0f8c3`, `f772c42`, `0eaea95`, `739d3bd`, `fedaef2` og `edc48af`. CI-kjøring nr. 10 og Windows-testen nr. 4 passerte på `edc48af`, og 104 tester og Ruff passerte lokalt.
- **Dokumenter:** README, QA-loggen (oppføringene om macOS og Windows og én med KI-feilene fra reviewene), statustabellen, KI-styringsloggen (tilfelle 30), arkitekturspinen med en rad i endringsloggen, spesifikasjonen, arbeidsloggen, `deferred-work.md` og `sprint-status.yaml`, der story 1.3 er `done`.
- **Eksporten:** [1-3-2026-11-22.txt](sessions/1-3-2026-11-22.txt) er maskert og har bare delen etter eksporten for story 1.2 (3756 linjer). Delen fra story 1.2 var lik den forrige eksporten.
- **`issues.md`:** lukket i dag: Dockers vilkår på Macen, jobb-PC-en, `.secret_key` på Windows og den kalde oppstarten av Docker Desktop på macOS. Punktene om oppsettstiden og `.secret_key` har fått merknader, og det er fem nye punkter (under).
- **Flettingen:** Grenen ble pushet via SSH med eksporten, denne loggen og arbeidsloggen (`7c81a15`, `ace8f5b` og `68603a5`), etter brukerens godkjenning. CI-kjøring nr. 11 og Windows-testen nr. 5 på `68603a5` passerte. Etter brukerens godkjenning ble PR #12 flettet lokalt med «Create a merge commit» og noreply-adressen, og `main` ble pushet via SSH, fordi `windows-setup.yml` kom inn i `main`. Merge-commiten er `36e4035`, og GitHub viser PR #12 som flettet 22. november kl. 15.33. CI-kjøring nr. 12 på `main` passerte med 104 tester. Lokal `main` og GitHub ble synkronisert på `36e4035`, og arbeidskopien var ren. Grenen `story/1-3-windows-and-offline-setup` er beholdt.

### Åpne punkter
- Story 4.4: kjør Windows-testen med `workflow_dispatch` på siste commit, og før resultatet i QA-loggen.
- Får gruppen tilgang til en Windows x64-PC der uv og Docker Desktop kan installeres, kjøres hele README-oppsettet og oppstarten uten nett der (D-3).
- Story 4.1: Windows-versjonene i README og spinen er ute av Microsofts vanlige støtte; sjekk kravene til Docker Desktop 4.99.0 og foreslå minsteversjoner (krever godkjenning).
- «ø» i meldingene fra `manage.py` vises feil i loggen fra GitHub på Windows; sjekk det i et vanlig PowerShell-vindu hvis en Windows-PC blir tilgjengelig.
- Story 4.4: test den ferdige nettsiden i en nettleser på Windows-PC-en på jobben via LAN-modusen, hvis jobbnettet og IT-reglene tillater det (NFR-6).
