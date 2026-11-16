# Arbeidslogg 10. og 11. november 2026 (arkivert)

Disse to oppføringene er kopiert ordrett fra `docs/arbeidslogg.md` i taggen `archive/story-1-1-project-skeleton` (commit `ffc934c`). De beskriver story 1.1 og oppsettet av GitHub CLI på grenen `story/1-1-project-skeleton`. Pull request #1 ble lukket uten fletting 16. november 2026, så `docs/arbeidslogg.md` på `design/after-prd-feedback` har dem ikke. Koden de omtaler, er arkivert i den samme taggen og brukes ikke i den nye arkitekturen.

---

### 10. november 2026 – Story 1.1: prosjektskjelett lokalt og på Vercel

* Kjørte `bmad-build` for story 1.1 på en egen gren, `story/1-1-project-skeleton`. Claude laget epic 1-konteksten og spesifikasjonen. Jeg godkjente spesifikasjonen (`ready-for-dev`), valgte å beholde den samlet og ba Claude stoppe før implementeringen. Spesifikasjonen ble committet og pushet (`ce6afbb`).
* Eksempel på styring av KI: jeg minnet Claude på at Vercel skal bruke PostgreSQL via Neon. Det ble låst i spesifikasjonen: på Vercel er databasen alltid Neon PostgreSQL via `DATABASE_URL`, aldri SQLite.
* Senere samme kveld fortsatte jeg byggingen. En subagent implementerte spesifikasjonen:
  * Django 5.2-skjelettet med innstillinger for lokal kjøring (SQLite) og publisering på Vercel (Neon PostgreSQL);
  * brukermodellen `accounts.Company` i den første migreringen;
  * norsk startside, 404- og 500-side og helsesjekken `/helse/`;
  * `load_seed`, som foreløpig bare lager den lokale nøkkelen;
  * tester og README-avsnittene «Kom i gang lokalt» og «Publisering».
* Claude kontrollerte resultatet mot spesifikasjonen og kjørte README-oppsettet på en ren kopi av prosjektet. Django-sjekken, migreringssjekken, testene og Ruff var grønne.
* Kvalitetssikring: tre uavhengige review-agenter fant til sammen 40 funn.
  * 14 ble rettet, blant annet tre hull i testene og at Neon-adressen nå holdes utenfor skallhistorikken.
  * 1 ble utsatt: en migreringssjekk før pull requester, ført i `deferred-work.md`.
  * 25 ble avvist, med begrunnelse i triageloggen i spesifikasjonen.
  * Etter rettingene passerte alle 30 testene.
* Eksempel på styring av KI: jeg bestemte at ingenting skulle committes eller pushes uten min godkjenning. Etter godkjenningen kontrollerte Claude at filene ikke inneholdt lokale stier, e-postadresser eller nøkler. Deretter ble arbeidet committet og pushet til grenen (`571d4dc`).

**Status:** Story 1.1 er bygget og står til review i sprintplanen. Neste steg er pull requesten og publiseringen på Vercel med Neon. Resultatene av kontosjekkene (AR-17) skal føres inn i pull requesten.

### 11. november 2026 – GitHub CLI

* Sjekket at GitHub CLI (`gh`) ikke var installert på Mac-en. Homebrew fantes heller ikke.
* Installerte `gh` 2.103.3 fra den offisielle macOS-pakken på GitHubs utgivelsesside, uten Homebrew. Før installasjonen kontrollerte Claude flere ting:
  * at sjekksummen stemte med GitHubs sjekksumfil;
  * at programmet er signert av GitHub;
  * at pakken ikke har installasjonsskript;
  * at alle filene havner under `/usr/local`.
* Selve pakkefila er ikke signert, men programmet i den er det. Jeg installerte pakken selv med administratorpassordet.
* Kontrollen etterpå viste at `gh` ligger i `/usr/local/bin`, at signaturen er gyldig, og at alle 238 filene fra pakken finnes.
* Logget inn med `gh auth login` via nettleseren og en engangskode, med min eksisterende GitHub-konto. Tokenet ligger i nøkkelringen på Mac-en og har rettighetene `repo`, `read:org` og `gist`.
* Eksempel på styring av KI: jeg ba Claude ikke endre Git-innstillinger eller prosjektfiler. Claude startet innloggingen uten spørsmål, slik at `gh` ikke satte opp Git-autentisering. Etterpå sjekket Claude at Git-innstillingene var like før og etter.

**Status:** GitHub CLI er installert og innlogget. Neste steg er pull requesten for story 1.1.
