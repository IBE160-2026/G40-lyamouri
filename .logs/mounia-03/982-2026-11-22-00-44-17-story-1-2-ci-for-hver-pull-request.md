# Story 1.2 – CI for hver pull request

## 2026-11-22 kl. 00:44 — Mounia-03

### Oppgave
Starte og fullføre story 1.2 («Check every pull request automatically») etter prosjektets arbeidsflyt: lese spesifikasjonen, BMAD-reglene, lærerens krav og beslutningene fra story 1.1, blant dem D-9 og D-10, bygge CI, skrive tester, rette feil, kjøre BMAD-kontrollene og oppdatere dokumentasjonen, QA-loggen, `issues.md`, arbeidsloggen og sprintstatusen. VG-4 og andre åpne punkter for story 1.2 skulle følges, eksisterende arbeid gjenbrukes, og unødvendige subagenter unngås. Brukeren ville godkjenne viktige beslutninger, commit, push og fletting, og story 1.3 skulle ikke startes.

### Plan
- `bmad-build` steg 1–5 på grenen `story/1-2-check-every-pull-request`, laget fra `main` (`374db81`).
  - Brukeren valgte subagenter bare der reglene krever det: én til å kompilere epic-1-konteksten på nytt, fordi D-9 og D-10 var nyere enn den, og fire i BMAD Code Review. Implementeringen og reviewen i `bmad-build` gjorde byggeøkten selv.
  - Spesifikasjonen er [spec-1-2-check-every-pull-request-automatically.md](../../_bmad-output/implementation-artifacts/spec-1-2-check-every-pull-request-automatically.md). Brukeren bestemte at den første grønne kjøringen er organisasjonssjekken (D-1), fordi API-et for reglene for Actions svarer 403 uten admin-rettigheter.
  - VG-4 ble en pytest-test av `docker compose config`, ikke et eget CI-steg, fordi AD-17 vil at alle sjekker også kjører lokalt.
- Pushen: tokenet i nøkkelringen mangler `workflow`-rettigheten, og to forsøk med `gh auth refresh -s workflow` endte med «context deadline exceeded». Brukeren laget en SSH-nøkkel og registrerte den på GitHub. Claude la GitHubs vertsnøkler fra `gh api meta` inn i `~/.ssh/known_hosts`, kontrollerte fingeravtrykkene og pushet grenen via SSH. Remoten er fortsatt HTTPS.
- BMAD Code Review med fire subagenter. Tre stoppet på bruksgrensen og fortsatte der de slapp, og resultatet fra Acceptance Auditor ble beholdt.
- Eksporten ble laget med `/export` og maskert med samme skript som for story 1.1. Etter brukerens valg ble delen som allerede står i eksporten for story 1.1, fjernet.

### Resultat
- Commits på `story/1-2-check-every-pull-request`:
  - `668808b` Legg til spesifikasjonen for story 1.2, med epic-1-konteksten og sprintstatusen.
  - `b2dd344` Legg til CI med GitHub Actions for story 1.2.
  - `e24727e` Rett funnene fra BMAD Code Review av story 1.2 i koden og testene.
  - `5297ed0` Før inn funnene fra BMAD Code Review av story 1.2 i dokumentene.
- CI: `.github/workflows/ci.yml` kjører `uv sync --locked`, databasen fra `compose.yaml`, `uv run pytest`, `uv run ruff check` og `uv run ruff format --check` på `ubuntu-24.04`, for hver pull request og hver push til `main`.
  - Begge actions er låst til commit-hash, workflowen har bare lesetilgang og ingen hemmeligheter, og Ruff kjører også når pytest feiler.
  - Hver kjøring utenfor en pull request har sin egen gruppe, så ingen push til `main` avbrytes.
- Tester: importtesten for AD-1, som også avviser database- og nettverksmodulene i standardbiblioteket, compose-testen for VG-4 og workflow-testen. `makemigrations --check` fra story 1.1 gjenbrukes. 103 tester og Ruff passerer lokalt.
- [PR #10](https://github.com/IBE160-2026/G40-lyamouri/pull/10):
  - Kjøring nr. 1 på `b2dd344` passerte med 99 tester, også de 82 fra story 1.1 (D-9). Den er organisasjonssjekken.
  - Kjøring nr. 2 på `5297ed0` passerte med 103 tester. Begge tok 36 sekunder.
- Reviewene:
  - `bmad-build`: 11 funn, 4 rettet og 7 avvist.
  - BMAD Code Review: 34 funn, 31 rettet i 12 rettinger og 3 avvist. Brukeren valgte at importtesten avviser database- og nettverksmodulene i standardbiblioteket, og at hver push til `main` får sin egen kjøring.
  - 16 mutasjoner viste at rettingene virker.
- Dokumenter:
  - README «Tester» forklarer CI, en hoppet test og fletteregelen.
  - QA-loggen har den første CI-kjøringen og [feilene fra reviewene](../../docs/qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-reviewene-av-story-12-dr-9), og KI-styringsloggen har tilfelle 29.
  - `sprint-status.yaml` setter story 1.2 til `done`. VG-4 er lukket i `deferred-work.md` og `issues.md`.
- Eksporten: [1-2-2026-11-22.txt](sessions/1-2-2026-11-22.txt) starter der [1-1-2026-11-21.txt](sessions/1-1-2026-11-21.txt) slutter, med `/export` 21. november kl. 18.58, og går til 22. november kl. 00.37.
  - Den dekker slutten av story 1.1, med flettingen av PR #8 og PR #9, og hele story 1.2.
  - De første 9422 linjene av den nye eksporten var de samme som den forrige, bortsett fra ukedagen i 25 tidsmerker, og de er fjernet.
  - Fila er maskert. Den har ingen stier, brukernavn, nøkler eller e-postadresser utenom `git@github.com`, og navnet fra medlemslista i README står én gang, i en diff av README.
- Lukket i `issues.md`: VG-4. Nytt punkt: push via SSH for endringer i `.github/workflows/`.
- Grenen pushes med denne loggen etter brukerens godkjenning. Etter en grønn kjøring legges kommentaren med alle funnene inn i PR #10, og PR-en flettes via SSH når brukeren godkjenner det.

### Åpne punkter
- Push som endrer `.github/workflows/`, også flettingen av PR #10 til `main`, må gå via SSH, fordi tokenet i nøkkelringen mangler `workflow`-rettigheten. Gi tokenet rettigheten, eller bytt remoten til SSH.
