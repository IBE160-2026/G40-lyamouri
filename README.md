# G40 — Mounia

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Kom i gang

Prognose kjører på din egen maskin: appen med uv, og databasen PostgreSQL i Docker. Kommandoene er de samme i Terminal på macOS og i PowerShell på Windows. Ingen av dem krever at du aktiverer et virtuelt miljø, lager en `.env`-fil, skaffer en nøkkel eller redigerer en fil.

### Dette trenger du

- **uv** 0.12.13 eller nyere ([installasjon](https://docs.astral.sh/uv/getting-started/installation/)). uv installerer selv Python 3.13 for prosjektet hvis maskinen mangler det.
- **Docker Desktop** 4.99.0 eller nyere ([nedlasting](https://www.docker.com/products/docker-desktop/)), og det må være startet. Docker Desktop er gratis for personlig bruk og utdanning. Versjon 4.99.0 krever macOS 14 eller nyere. På Windows trenger det WSL 2 og maskinvarevirtualisering slått på. På macOS må Terminal finne `docker`. Svarer den `command not found: docker`, ligger verktøyene i `~/.docker/bin`. Velg da **System** under Docker Desktop → Settings → Advanced, eller legg mappa til i PATH med `echo 'export PATH="$HOME/.docker/bin:$PATH"' >> ~/.zprofile` (bruker du bash, `~/.bash_profile`) og åpne et nytt Terminal-vindu. På Windows åpner du et nytt PowerShell-vindu etter installasjonen, og starter maskinen på nytt hvis Docker Desktop ber om det, så PowerShell finner `uv` og `docker`.
- **Git**, for å klone repoet.

Prognose støtter macOS på Apple silicon eller Intel, og Windows 10 22H2 eller Windows 11 23H2 på x64. Windows på ARM støttes ikke i versjon 1, fordi databasedriveren psycopg ikke har en ferdig pakke for det. Hele oppsettet er testet på macOS med Apple M1, også oppstart uten nett med Docker Desktop helt avsluttet (se [QA-loggen](docs/qa-logg.md)). På macOS trenger Prognose derfor ikke nett etter første oppsett, fordi Docker-imaget, Python og pakkene da ligger på maskinen. På Windows er oppsettet med Docker Desktop og oppstart uten nett ikke testet, fordi gruppen ikke har en Windows x64-PC der uv og Docker Desktop kan installeres. Delen uten Docker, altså `uv sync --locked`, `migrate`, `load_seed` og `runserver`, testes automatisk på Windows Server 2025 x64 i GitHub Actions for hver pull request som endrer koden eller avhengighetene.

### Start Prognose

Klon repoet og gå inn i mappa:

```
git clone https://github.com/IBE160-2026/G40-lyamouri.git
cd G40-lyamouri
```

Kjør så disse fem kommandoene, én om gangen:

```
docker compose up -d --wait
uv sync --locked
uv run python src/manage.py migrate
uv run python src/manage.py load_seed
uv run python src/manage.py runserver --insecure
```

1. `docker compose up -d --wait` starter databasen og venter til den er klar. Første gang laster Docker ned PostgreSQL-imaget.
2. `uv sync --locked` installerer Python 3.13 hvis det mangler, og de nøyaktige pakkeversjonene i `uv.lock`.
3. `migrate` lager tabellene i databasen.
4. `load_seed` lager nøkkelen som signerer øktene (se [Nøkler og hemmeligheter](#nøkler-og-hemmeligheter)) og laster de to testbedriftene inn i den tomme databasen (se [Testbedrifter](#testbedrifter)).
5. `runserver --insecure` starter Prognose. Åpne http://127.0.0.1:8000/ i nettleseren og logg inn som en av testbedriftene (se [Testbedrifter](#testbedrifter)). `--insecure` lar utviklingsserveren levere appens statiske filer, som stilark, selv om feilsøkingsmodus er av. Det åpner ikke appen for andre maskiner.

Både appen og databasen svarer bare på din egen maskin (127.0.0.1).

Er en `DATABASE_URL` eksportert i terminalen, for eksempel for et annet prosjekt, bruker Prognose og testene den databasen i stedet for databasen fra `compose.yaml`, og pytest lager og sletter da testdatabasen sin der. Fjern variabelen først, med `unset DATABASE_URL` i Terminal på macOS eller `Remove-Item Env:DATABASE_URL` i PowerShell.

## Testbedrifter

Prognose har to syntetiske testbedrifter, uten virkelige data. Dataene lages av en generator som gir de samme filene hver gang, og ligger i [`data/seed/`](data/seed/). [`data/README.md`](data/README.md) forklarer skjemaet, produktene og mønstrene. Filene har bare passordhasher, så passordene står her. De gjelder bare for disse testdataene på din egen maskin, og skal ikke brukes noe annet sted:

| Bedrift | Kundenummer | Passord |
|---|---|---|
| Testbedrift A | 1001 | `testbedrift-a` |
| Testbedrift B | 1002 | `testbedrift-b` |

Generatoren kjøres med `uv run python data/generate_seed.py`, og den skriver de samme filene hver gang. Dataene lastes inn i databasen med `uv run python src/manage.py load_seed`.

`load_seed` sjekker først alle filene i `data/seed/`: skjemaversjonen, at hver uke har et helt tall på 0 eller mer, at alle produktene i en bedrift slutter samme uke, og at passordfeltet er en hash og ikke et passord. Er en fil feil, laster og sletter kommandoen ingenting og sier hva som er galt. Deretter lager den bedriftene med produkter, salgsuker og innstillinger, med standardverdiene fra FR-20.

- **Ikke tom database:** `load_seed` stopper med en melding og endrer ingenting. Den sletter og overskriver aldri data på egen hånd. Dataene og innstillingene ligger igjen når appen og databasen stoppes og startes på nytt, for eksempel med `docker compose down` og `docker compose up -d --wait`. Bruker du `docker compose down -v`, slettes volumet med databasen, og du må kjøre `migrate` og `load_seed` på nytt.
- **Tilbake til testdataene:** `uv run python src/manage.py load_seed --reset` sletter alle bedrifter med produkter, salgsuker og innstillinger og alle økter, og laster testdataene på nytt, uten duplikater. Et `--reset` nullstiller derfor også innstillingene og de justerte mengdene, som ligger i øktene. Kommandoen ber deg skrive `nullstill`. Skriver du noe annet, endres ingenting. Ingen annen kommando eller bygging kjører `--reset`, og `.secret_key` beholdes.

### Logg inn og logg ut

Åpne http://127.0.0.1:8000/ og skriv inn kundenummeret og passordet fra tabellen over, for eksempel `1001` og `testbedrift-a`. Du kommer til produktoversikten med bare den bedriftens produkter. Toppfeltet viser bedriften og den siste registrerte uka, og «Logg ut» avslutter økten. Feil kundenummer eller passord gir den samme meldingen, uten å si hvilket av dem som er feil. Alle andre sider krever innlogging. Trykker du Tilbake etter utloggingen, laster Safari siden på nytt (et lite script, `app.js`), og du ender på innloggingen. Uten script kan Tilbake vise den gamle siden, men et klikk eller en oppdatering gir innloggingen.

Innloggingen bruker en økt som ligger i databasen. Nøkkelen i `.secret_key` signerer økten, så fila må finnes før du starter appen (`load_seed` lager den). Mangler den, får hver start av serveren en ny nøkkel, og du må logge inn på nytt.

### Test på en ekte telefon over lokalnettet

Dette er bare for den manuelle testen av telefonvisningen (NFR-6), og trengs ikke for å bruke Prognose. Maskinen og telefonen må være på samme private nettverk som du stoler på: appen bruker vanlig HTTP, så passordet og øktinformasjonskapselen går ukryptert over nettverket. Testpassordene er offentlige og gjelder bare testdataene. Telefonen og maskinen får hver sin økt, siden adressen er en annen enn 127.0.0.1.

`PROGNOSE_LAN_HOST` er maskinens egen IPv4-adresse på det private nettverket. Uten den godtar Prognose bare `127.0.0.1` og `localhost` (Djangos `ALLOWED_HOSTS`, AD-13). Variabelen legger til akkurat den ene adressen, og den må være satt når serveren starter. En adresse som ikke er privat (10.x.x.x, 172.16.x.x til 172.31.x.x eller 192.168.x.x), og `*`, avvises med en feilmelding. Åpner du `http://<adressen>:8000/` på telefonen uten at variabelen var satt ved oppstart, viser Django `DisallowedHost`. Stopp da serveren og start den på nytt som i steg 2. Adressen kan endre seg når maskinen kobler til nettverket på nytt, så sjekk den hver gang.

1. Finn maskinens IPv4-adresse på det private nettverket, for eksempel `192.168.1.20`.
2. Start appen i et nytt terminalvindu: `PROGNOSE_LAN_HOST=192.168.1.20 uv run python src/manage.py runserver --insecure 0.0.0.0:8000` (i PowerShell: `$env:PROGNOSE_LAN_HOST = "192.168.1.20"` og så `uv run python src/manage.py runserver --insecure 0.0.0.0:8000`). Feilsøkingsmodus er av, og databasen svarer fortsatt bare på 127.0.0.1.
3. Åpne `http://192.168.1.20:8000/` i Safari på telefonen og logg inn som hver testbedrift.
4. Stopp appen med Ctrl+C og fjern variabelen etterpå (`Remove-Item Env:PROGNOSE_LAN_HOST` i PowerShell, eller lukk terminalvinduet på macOS).

## Nøkler og hemmeligheter

- Prognose trenger ingen API-nøkkel, betalt tjeneste eller tredjepartskonto.
- `load_seed` lager nøkkelen som signerer øktene, i fila `.secret_key` i prosjektmappa, når fila mangler. En nøkkel som finnes, endres aldri. Git ignorerer fila, så nøkkelen kommer aldri inn i repoet. Er fila tom, stopper `load_seed` og ber deg slette den og kjøre kommandoen på nytt. På macOS kan bare du lese fila. På Windows avhenger det av mappa hvem som kan lese den, så bruker flere samme PC, bør du klone repoet i din egen brukermappe, `C:\Users\<navn>`. Da kan bare du, SYSTEM og administratorene lese den, og `icacls .secret_key` viser hvem som har tilgang.
- Den lokale databasen har ikke passord. Den tar bare imot tilkoblinger fra din egen maskin, på 127.0.0.1:15432, men der kan alle brukere av maskinen koble seg til. Prognose er derfor laget for én bruker per maskin.
- Alle variablene i [`.env.example`](.env.example) er valgfrie, og ingen av dem trengs for oppsettet over. Fila forklarer hver av dem.

## Tester

Testene bruker den lokale PostgreSQL-serveren, så start den først med `docker compose up -d --wait`. pytest lager sin egen testdatabase, `test_prognose`, på den samme serveren og sletter den etterpå, så appens data blir ikke rørt. Databasebrukeren må derfor ha rett til å lage databaser, og det har brukeren `prognose` fra `compose.yaml`. Kjør så:

```
uv run pytest
uv run ruff check
uv run ruff format --check
```

- `uv run pytest` kjører alle testene. Forventet resultat er at siste linje bare melder `passed`, uten `failed`, `error` eller `skipped`. En test hoppes bare over når den mangler et verktøy: testen av `compose.yaml` hvis `docker` ikke finnes i PATH, og testene av `.gitignore` utenfor en git-klone. Da melder siste linje også `skipped`, og den sjekken er ikke gjort på den maskinen.
- `uv run ruff check` sjekker kodestilen i alle Python-filene i repoet, unntatt de genererte migreringene og skriptene som BMAD (`_bmad/`) og Claude Code (`.claude/`) har med seg, og skal svare `All checks passed!`.
- `uv run ruff format --check` sjekker formateringen av de samme filene og skal svare at alle er formatert (`files already formatted`).

Fasiten for testene er referanseregnearket [`reference/reference-examples.xlsx`](reference/reference-examples.xlsx), med referanseeksemplene fra PRD-en og de forventede verdiene for regeltestproduktene. [`reference/README.md`](reference/README.md) forklarer arkene og hvordan verdiene er kontrollert.

GitHub Actions kjører de samme kommandoene på Linux for hver pull request og hver push til `main`, etter `uv sync --locked` og med databasen fra `compose.yaml` ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)). Gruppen fletter en pull request først når kjøringen på dens siste commit har bestått, og kjører den på nytt hvis `main` har endret seg siden. Det er gruppens rutine. GitHub håndhever den ikke, fordi gruppen ikke har admin-rettigheter i organisasjonen.

## Medlemmer

- Flesche Mounia Lyamouri
