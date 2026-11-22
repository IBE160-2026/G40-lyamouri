# Story 1.3 – oppsett på Windows og uten nett

## 2026-11-22 kl. 09:53 — Mounia-03

### Oppgave
Starte story 1.3 («Confirm the setup on Windows and without a network») med BMAD, lære av arbeidsmåten i story 1.2, jobbe selvstendig og effektivt, unngå unødvendige spørsmål, subagenter og dobbeltarbeid, og ikke committe eller pushe uten godkjenning. Etter testen uten nett på macOS ba brukeren om at loggene leses og at QA-loggen og den relevante dokumentasjonen oppdateres.

### Plan
- `bmad-build` på grenen `story/1-3-windows-and-offline-setup`, laget fra `main` (`850250d`). Epic-1-konteksten var gyldig, så ingen subagent trengtes. Storyen fulgte «oneshot»-ruten, fordi den har små endringer og ingen uavklarte valg; spesifikasjonen er [spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md](../../_bmad-output/implementation-artifacts/spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md).
- Windows-PC-en er bare tilgjengelig 25. november og 7. desember, så storyen blir ferdig etter Windows-testen 25. november. Grenen står åpen til da.
- Testen uten nett på macOS: Claude skrev et skript i den midlertidige mappa for økten, og brukeren kjørte det i Terminal og slo selv nettet av og på, fordi økten mister forbindelsen uten nett. Skriptet sletter ingen data: `docker compose down` beholder volumet.

### Resultat
- Testen uten nett på macOS passerte 22. november: databasen var klar etter 5 sekunder, og Prognose svarte 200 med «Prognose» etter 1 sekund. Docker Desktop svarte etter 1 sekund og var trolig ikke helt avsluttet, så en kald oppstart av Docker Desktop uten nett er ikke vist. Resultatet står i [QA-loggen](../../docs/qa-logg.md#2026-11-22--oppstart-uten-nett-på-macos-story-13-nfr-1-sm-2-dr-9).
- Funn: Terminal-appen fant ikke `docker`, fordi verktøyene lå i `~/.docker/bin`. README forklarer nå hva man gjør når Terminal svarer `command not found: docker`, og sier at Prognose ikke trenger nett etter første oppsett, testet på macOS.
- Planen for Windows-testen 25. november står i spesifikasjonen: tidtaking av installasjonen, de fem README-kommandoene i PowerShell fra en ren klone, `icacls .secret_key`, tidene fra `Get-History` og oppstart uten nett.
- `sprint-status.yaml`: story 1.3 står som `in-progress`.
- `issues.md`: punktet om Dockers vilkår på Macen er lukket. Punktene om oppsettstiden og jobb-PC-en har fått merknader.

### Åpne punkter
- Windows-testen 25. november på PC-en på jobben, hvis IT-reglene og Dockers lisens tillater at uv og Docker Desktop installeres. Ellers en annen Windows x64-PC, eller en merknad i README og statustabellen om at Windows ikke er testet (D-3). Dekkes av punktet om jobb-PC-en i `issues.md`.
- En kald oppstart av Docker Desktop uten nett sjekkes på Windows 25. november og i story 4.4.
