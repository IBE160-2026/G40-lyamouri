# QA-logg

QA-loggen oppfyller DR-9 og NFR-4 i PRD-en:
- Hver feil i KI-generert kode eller tekst som en test, referanseregnearket, en gjennomgang eller en manuell test finner, føres med hvordan den ble funnet, rettingen og commiten eller pull requesten.
- Personvernkontrollen av hele Git-historikken føres her, og den gjentas på siste commit før innlevering.
- Den manuelle sjekklisten på siste commit føres her.

**Plassering.** PRD-en lar arkitektursteget fastsette mappene (DR-2). Fila ligger i `docs/` sammen med de andre prosessdokumentene, slik den arkiverte arkitekturen fra 8. november bestemte. Arkitekturspinen fra 17. november bekrefter plasseringen.

**Tidligere funn.** Feil i KI-generert tekst i planleggingsfasen står under «Kvalitetssikring» i `docs/arbeidslogg.md` og gjentas ikke her.

## 2026-11-16 – Git-forfatteridentiteter i historikken (NFR-4)

**Hvordan det ble funnet.** Mangelen ble først oppdaget i UX-arbeidet 15.–16. november: Git hadde ikke navn og e-post satt i skallet Claude brukte, så commitene fikk identiteten macOS lager automatisk. 16. november kartla Claude forfatteridentitetene på alle grener, `main` og taggen `archive/story-1-1-project-skeleton`.

**Funn.** Forfatteridentitetene i historikken 16. november 2026:

| Identitet | Commits | Vurdering |
|---|---|---|
| Automatisk fra macOS: fullt navn, macOS-brukernavn og maskinnavn. Ett av de to maskinnavnene inneholder fornavnet. | 61 | Bryter NFR-4: fullt navn og lokale maskindata |
| Flettingen av PR #2 på GitHub: GitHub-navnet og skoleadressen | 1 | Bryter NFR-4: e-postadresse |
| Lærerens egne commits, med lærerens navn og skoleadresse | 6 | Tillatt: lærerens egen identitet |
| `Mounia-03` med GitHubs noreply-adresse | alle fra `6245a0a` | I orden |

Adressene og maskinnavnene står ikke her, fordi filene ikke skal ha personopplysninger (NFR-4).

Filene på alle grener og i hele historikken har ingen lokale stier, e-postadresser, nøkler eller tokens. Navnet i medlemslisten i README, personaen «Mounia» og «Mounia-03» i BMAD-konfigurasjonen er vurdert som tillatt. Det gamle brukernavnet i sesjonsloggene, som er første del av en privat e-postadresse, er fjernet fra filene. Det står fortsatt i eldre versjoner av loggene og i commit-meldingen til `6245a0a`.

**Retting.**
- Git-identiteten er satt lokalt i repoet til `Mounia-03` med GitHubs noreply-adresse. Alle commits fra og med `6245a0a` har den.
- Sesjonsloggene er flyttet til `.logs/mounia-03/`, og det gamle brukernavnet er fjernet fra overskriftene (`6245a0a`).

**Beslutning: historikken bevares.** Gamle commits er ikke endret, av fire grunner:
1. Omskriving krever force-push av `main` og de andre grenene, også av flettingen av PR #2 og lærerens commits.
2. Alle commit-hashene som PRD-en, UX-en, arkivet, arbeidsloggen og sesjonsloggene viser til, ville slutte å virke. Det bryter sporbarheten som DR-5 og DR-8 krever.
3. Taggen `archive/story-1-1-project-skeleton` og pull requestene #1 og #2 på GitHub viser til de gamle commitene.
4. Opplysningene er lite sensitive. Navnet står allerede i medlemslisten i README, og ingen passord, nøkler eller tokens er eksponert.

Beslutningen ble tatt 16. november 2026, etter Claudes anbefaling.

**Gjenstår.**
- Slå på «Keep my email addresses private» på GitHub, så flettinger på GitHub ikke bruker skoleadressen igjen.
- Sette samme Git-identitet i andre kloner av repoet.
- Gjenta personvernkontrollen av hele historikken på siste commit før innlevering, og føre resultatet her (NFR-4).

## 2026-11-17 – Test av lokal PostgreSQL med Docker Compose (SM-2, NFR-1, NFR-8)

**Hvorfor.** Brukeren bestemte i arkitektursteget at Prognose skal bruke PostgreSQL både lokalt og publisert. Løsningen med Docker Compose skulle testes før arkitekturen ble godkjent (FR-4, AD-14 i arkitekturspinen).

**Oppsett.**
- macOS 15.6.1 på Apple M1 med 8 GB minne. Ingen nettleser var med, fordi bare databasen og tilkoblingen ble testet.
- Docker Desktop 4.99.0, lastet ned fra Dockers offisielle kilde. Fila var hel, appen er signert av Docker Inc og notarisert av Apple, og den krever macOS 14.0 eller nyere.
- Docker-motor 29.9.3 og Docker Compose v5.7.0.
- En midlertidig `compose.yaml` utenfor prosjektet med de samme innstillingene som arkitekturen: `postgres:18.7`, porten `127.0.0.1:15432`, ingen passord, et navngitt volum og en helsesjekk.
- Python 3.13 med Django 5.2.19 og psycopg 3.3.9, installert med uv.

**Resultat.**

| Kontroll | Resultat |
|---|---|
| `docker compose up -d --wait` første gang, med nedlasting av imaget (167 MB) | klar etter 17 sekunder |
| Omstart uten nedlasting (`--pull never`) | klar etter 3 sekunder |
| Tilkobling fra Python | virker uten passord; porten lytter bare på `127.0.0.1` |
| Database og tegnsett | PostgreSQL 18.7 med UTF-8; æ, ø og å kom riktig tilbake |
| Django 5.2.19, `migrate` | 15 migreringer på 0,15 sekunder |
| 10 400 salgsuker (2 bedrifter × 50 produkter × 104 uker) | lagret på 0,17 sekunder; 5 200 lest på 0,01 sekunder |
| Data etter omstart | alt fantes fortsatt |
| Minne | PostgreSQL 30 MB; Docker og den virtuelle maskinen rundt 550 MB; grensen er 4 GB, og Mac-en hadde 33 % ledig minne |
| `uv sync --locked` på en tom maskin: Python 3.13 og alle pakkene | 3,7 sekunder |
| uv uten nett (`UV_OFFLINE=1`) | `uv run` og `uv sync --locked` virket |

Testcontaineren, volumet og de midlertidige filene ble slettet etterpå. Imaget `postgres:18.7` (701 MB) ligger fortsatt i Docker.

**Ikke gjennomført.**
- **Oppstart uten nett med Docker Desktop:** ikke testet. Claude Code trenger nett, så testen kunne ikke kjøres mens Claude arbeidet. Omstarten viste at Docker ikke trengte å laste ned noe, men Docker Desktop selv ble ikke startet uten nett.
- **Oppsett på Windows (x64) med Docker Desktop:** ikke testet, fordi økten ikke hadde noen Windows-maskin.

**Gjenstår.** Begge testene kjøres i første story og på nytt på siste commit (DR-9, SM-2).

## 2026-11-20 – Første oppsett på macOS fra en ren kopi (Story 1.1; NFR-1, NFR-3, SM-2)

**Hvorfor.** Story 1.1 krever at det første oppsettet på macOS føres med dato, Docker Desktop-versjon, resultat og tid. Oppsettet fulgte de fem kommandoene under «Kom i gang» i README.

**Oppsett.**
- Claude Code kjørte oppsettet tre ganger samme dag, med de samme kontrollene: to ganger før rettingene fra kodegjennomgangen, og én gang etter, på de endelige filene. Ingen person kjørte det.
- macOS 15.6.1 på Apple M1 med 8 GB minne.
- Docker Desktop 4.99.0 med Docker-motor 29.9.3 og Docker Compose v5.7.0. Imaget `postgres:18.7` lå allerede i Docker etter testen 17. november, så det ble ikke lastet ned.
- uv 0.12.13. Python 3.13.15 var installert fra før, og pakkene lå i uv sin lokale hurtigbuffer.
- En midlertidig kopi utenfor repoet med bare filene som skal committes, altså uten `.venv`, `.env` og `.secret_key`. Kopien fikk sitt eget Compose-prosjekt og volum, og begge ble slettet etterpå. Databasen til repoet var stoppet mens kopien kjørte, fordi begge bruker porten 15432.
- Klient: `curl` 8.7.1 mot `http://127.0.0.1:8000/`, og `lsof` for adressene appen og databasen lyttet på. Ingen nettleser var med.

**Resultat.**

| Kommando | Resultat | Kjøring 1 (sekunder) | Kjøring 2 (sekunder) | Kjøring 3 (sekunder) |
|---|---|---|---|---|
| `docker compose up -d --wait` | databasen var klar («healthy») | 3,1 | 2,8 | 2,8 |
| `uv sync --locked` | lagde `.venv` og installerte de 14 låste pakkene; `uv.lock` var uendret | 0,2 | 0,2 | 0,2 |
| `uv run python src/manage.py migrate` | 16 migreringer, den siste `web.0001_initial` | 3,0 | 2,7 | 2,6 |
| `uv run python src/manage.py load_seed` | «Lagde .secret_key med en ny hemmelig nøkkel.»; fila kan bare leses av eieren (modus 600) | 0,2 | 0,2 | 0,3 |
| `uv run python src/manage.py runserver --insecure` | systemsjekken fant ingen feil, og appen svarte på første forespørsel | 1,0 | 1,1 | 1,1 |
| Totalt, fra første kommando til første svar | | 7,8 | 7,2 | 7,2 |

Alle tre kjøringene ga de samme resultatene. Totalen er litt større enn summen av stegene (7,5, 7,0 og 7,0 sekunder), fordi den også tar med tiden mellom kommandoene.

| Kontroll | Resultat |
|---|---|
| `curl http://127.0.0.1:8000/` | status 200, med `<html lang="nb">` og ordmerket «Prognose» |
| `lsof` på porten 8000 | appen lyttet bare på `127.0.0.1:8000` |
| `lsof` på porten 15432 | Docker Desktop lyttet bare på `127.0.0.1:15432` |
| Passord i databasen | rollen `prognose` har ikke lagret passord |
| Virtuelt miljø, `.env`, nøkkel og redigering av filer | ingen av stegene trengte noe av dette |

Tidene er lavere enn ved et første oppsett på en ny maskin, fordi imaget, Python og pakkene allerede lå lokalt. Testen 17. november målte 17 sekunder for `docker compose up -d --wait` med nedlasting av imaget.

**Gjenstår.**
- Brukeren sjekker `/` i Safari i responsiv visning ved 320 px, 390 × 844 og 820 × 1180 før pull requesten.
- De fem kommandoene kjøres på nytt fra en `git clone` av den pushede grenen før pull requesten flettes.
- Tidtakingen av hele oppsettet fra klonen, utført av en person (SM-2), hører til Story 4.1 og 4.4.
- Oppsett på Windows x64 og oppstart uten nett hører til Story 1.3.
