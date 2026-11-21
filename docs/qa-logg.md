# QA-logg

QA-loggen oppfyller DR-9 og NFR-4 i PRD-en:
- Hver feil i KI-generert kode eller tekst som en test, referanseregnearket, en gjennomgang eller en manuell test finner, føres med hvordan den ble funnet, rettingen og commiten eller pull requesten.
- Personvernkontrollen av hele Git-historikken føres her, og den gjentas på siste commit før innlevering.
- Den manuelle sjekklisten på siste commit føres her.

**Plassering.** PRD-en lar arkitektursteget fastsette mappene (DR-2). Fila ligger i `docs/` sammen med de andre prosessdokumentene, slik den arkiverte arkitekturen fra 8. november bestemte. Arkitekturspinen fra 17. november bekrefter plasseringen.

**Tidligere funn.** Feilene i KI-generert tekst og kode fra planleggingsfasen står i oppføringen [2026-11-20 – Feil i KI-generert tekst og kode fra planleggingsfasen](#2026-11-20--feil-i-ki-generert-tekst-og-kode-fra-planleggingsfasen-dr-9), hver med kilden sin. [Innledningen til KI-styringsloggen](ki-styringslogg.md) forklarer hvordan planleggingsfasen er dokumentert.

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

## 2026-11-20 – Feil i KI-generert kode og tekst fra reviewen av story 1.1 del A (DR-9)

**Hvordan det ble funnet.** Claude Code skrev koden, testene og tekstene i story 1.1 del A med `bmad-build`. Før første commit gikk tre uavhengige KI-granskere gjennom diffen: Blind Hunter, Edge Case Hunter og Verification Gap. Claude kontrollerte hvert funn mot koden og gjenskapte de som kunne testes. Ruff fant i tillegg én feil under implementeringen. Alle 35 funnene står med vurdering og begrunnelse under «Review Triage Log» i `_bmad-output/implementation-artifacts/spec-1-1-start-prognose-locally-from-a-fresh-clone.md`. Av dem ble 20 rettet, 2 utsatt og 13 avvist.

**Feilene som ble rettet.** Alle ble rettet før første commit og ligger i `93c9147`.

| Feil | Funnet av | Retting |
|---|---|---|
| En kommentar etter en tom verdi i `.env`, for eksempel `PROGNOSE_LAN_HOST=   # fylles ut`, ble lest som verdien, så innstillingene stoppet | Blind Hunter og Edge Case Hunter; gjenskapt | En verdi uten anførselstegn som starter med `#`, teller som tom |
| `export PROGNOSE_DEBUG=1` i `.env` ble lagret under et annet navn og oversett uten melding | Blind Hunter og Edge Case Hunter; gjenskapt | `export` foran navnet fjernes |
| En `.env` eller `.secret_key` som ikke kan leses som fil, for eksempel en mappe, ga en engelsk traceback i stedet for en norsk melding | Blind Hunter og Edge Case Hunter; gjenskapt | En norsk `ImproperlyConfigured` som sier hva som må rettes |
| Et `#` i passordet i `DATABASE_URL` ga den villedende meldingen «ugyldig vert eller port», og ingenting sa at parametere etter `?` ikke brukes | Blind Hunter og Edge Case Hunter; gjenskapt | Feilmeldingen og `.env.example` forklarer prosentkoding, og `.env.example` sier at parametere ikke brukes |
| En `DJANGO_SETTINGS_MODULE` som var eksportert for et annet prosjekt, vant over `prognose.settings` i `manage.py` og pytest | Edge Case Hunter; gjenskapt | `manage.py` og pytest bruker alltid `prognose.settings` |
| `requires-python` tillot nyere Python enn 3.13, og ingenting håndhevet minsteversjonen av uv som README oppgir | Blind Hunter | `requires-python = "==3.13.*"` og `required-version = ">=0.12.13"`; `uv.lock` er låst på nytt |
| Tre testhull: et passord kunne lekke gjennom en kjedet feil, dekodingen av bruker og databasenavn var ikke testet, og README-kommandoen `runserver --insecure` var ikke testet | Verification Gap, med mutasjonstester | Nye testtilfeller og `tests/test_start_command.py` |
| BOM-testen kunne ikke oppdage en feil, og BOM-tegnet var usynlig i kildekoden | Blind Hunter; bekreftet | En `KEY=VALUE`-linje rett etter BOM, og BOM skrevet som `"﻿"` |
| To tester lovet mer enn de sjekket, eller viste til feil beslutning (AD-11 for svaret 405) | Blind Hunter | Navnene og docstringene beskriver det testene sjekker |
| README og QA-loggen sa ikke hva som er testet, hvilken database testene bruker eller hva Ruff sjekker, og QA-loggen manglet én kjøring | Blind Hunter | Tekstene er rettet |
| `REQUIRED_FIELDS` i `web.Company` var en liste, som Ruff flagget (RUF012) | Ruff under implementeringen | Endret til en tuppel |

**Utsatt.** Telefontesten starter appen på `0.0.0.0`, slik AD-13 sier. Forslaget om å binde den til den private adressen står i `deferred-work.md`, fordi det krever en endring i arkitekturen som brukeren må godkjenne.

## 2026-11-20 – Feil i KI-generert tekst og kode fra planleggingsfasen (DR-9)

**Hvorfor.** Story 1.1 krever at QA-loggen fører feilene i KI-generert tekst og kode fra planleggingsfasen, med hvordan de ble funnet, rettingen og commiten der kilden nevner den (DR-9). Planleggingsfasen gikk fra Product Brief 14. oktober til sprintplanen 19. november 2026, og feilene ble ikke ført i QA-loggen underveis.

**Kildene.** Feilene er hentet fra arbeidsloggen, memloggene, sesjonsloggene og gjennomgangsfilene, og hver feil viser til kildene med fil og linje. Ingen prompt er rekonstruert, og [innledningen til KI-styringsloggen](ki-styringslogg.md) forklarer hvordan planleggingsfasen er dokumentert. Linjenumrene gjelder filene i commit `d8674ad`, og de siterte linjene leses i [repoet ved `d8674ad` på GitHub](https://github.com/IBE160-2026/G40-lyamouri/tree/d8674ad). Lenkene i tabellen under går til filene slik de er nå, og de kan ha endret seg. En commit eller pull request står bare der en kilde nevner den; ellers står det «ikke oppgitt i kilden». Der gruppen styrte KI i saken, lenker feilen til tilfellet i KI-styringsloggen, og tilfellet lenker hit. Kortnavnene viser til disse filene:

| Kortnavn | Fil |
|---|---|
| arbeidsloggen | [`docs/arbeidslogg.md`](arbeidslogg.md) |
| brief-memloggen | [`_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/.memlog.md`](../_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/.memlog.md) |
| brainstorm-memloggen | [`_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/.memlog.md`](../_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/.memlog.md) |
| sesjonslogg 984–997 | Fila i [`.logs/mounia-03/`](../.logs/mounia-03/) som begynner med nummeret, for eksempel `996-2026-11-06-23-23-12-ux-design-prognose.md` |
| `issues.md` | [`.logs/mounia-03/issues.md`](../.logs/mounia-03/issues.md) |
| PRD-memloggen | [`_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/.memlog.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/.memlog.md) |
| PRD-en, addendumet, sammendraget av brainstormingen og gjennomgangene av PRD-en | `prd.md`, `addendum.md`, `extract-brainstorm.md`, `reconcile-brainstorm.md` og `review-*.md` i [`_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/) |
| UX-memloggen | [`_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/.memlog.md`](../_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/.memlog.md) |
| mockupen, `DESIGN.md`, `EXPERIENCE.md` og UX-dekningskontrollen | `mockups/konsept-d-kombinert.html`, `DESIGN.md`, `EXPERIENCE.md` og `review-coverage.md` i [`_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/`](../_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/) |
| den arkiverte UX-memloggen og de arkiverte UX-filene | `.memlog.md`, `EXPERIENCE.md`, `mockups/key-produktoversikt.html`, `review-coverage.md` og `review-structure-prose.md` i [`_bmad-output/planning-artifacts/archive/ux-G40-lyamouri-2026-11-06/`](../_bmad-output/planning-artifacts/archive/ux-G40-lyamouri-2026-11-06/), UX-en fra 6.–7. november |
| arkitektur-memloggen | [`_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/.memlog.md`](../_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/.memlog.md) |
| `epics.md` | [`_bmad-output/planning-artifacts/epics.md`](../_bmad-output/planning-artifacts/epics.md) |

**Utvalget.** Bare feil i tekst og kode er tatt med, ikke atferd under arbeidet. Det gamle brukernavnet i loggene og i commit-meldingen til `6245a0a` står i [oppføringen om Git-identitetene](#2026-11-16--git-forfatteridentiteter-i-historikken-nfr-4) og gjentas ikke.

### Eksempel 1: Avrundingen i E5

- **Feil:** I brainstormingen bestemte brukeren, etter et forslag fra KI-veilederen, at bestillingsmengden rundes opp til hele enheter, og det KI-skrevne sammendraget av brainstormingen førte regelen videre til PRD-arbeidet. En datamaskin regner 100 × 1,1 − 40 til 70,00000000000001, så en ren oppoverrunding gir 71 i E5 i stedet for 70.
- **Hvordan det ble funnet:** Da beregningsreglene i PRD §5 ble skrevet, før gjennomgangene. Ingen kilde sier hvem som oppdaget problemet. Den uavhengige beregningskontrollen bekreftet senere at R-9 gir 70.
- **Retting:** Regelen om å runde verdien til 6 desimaler før den rundes opp ble lagt til, og brukeren godkjente den. Den er nå R-9, og E5 tester den.
- **Commit eller pull request:** `4ada86d`, det første PRD-utkastet (arbeidsloggen, linje 74).
- **Kilde:** arbeidsloggen, linje 72; sesjonslogg 997, linje 19; brainstorm-memloggen, linje 61 og 65; `extract-brainstorm.md`, linje 40; PRD-memloggen, linje 43; `reconcile-brainstorm.md`, linje 29; `review-calculations.md`, linje 15; PRD-en, linje 612 og 671.
- **KI-styringsloggen:** [tilfelle 4](ki-styringslogg.md#4-avrundingen-i-e5-23-november-2026). E5 står i begge loggene fordi DR-5 (PRD-en, linje 761) og story 1.1 (`epics.md`, linje 754) nevner den.

### Eksempel 2: Prognosekonflikten i R-10 og R-11

- **Feil:** PRD-utkastet sa ikke i hvilken rekkefølge reglene for uvanlige uker (R-10) og nytt nivå (R-11) behandler ukene. De samme salgstallene kunne derfor gi grunnprognosen 51,0 eller 70,333. Kvalitetsrubrikken fant den samme tvetydigheten med en kortere serie, der den andre tolkningen ga 71,0.
- **Hvordan det ble funnet:** Den uavhengige beregningskontrollen av PRD-utkastet (funn F1, kritisk, med det foreslåtte eksempelet M1) og kvalitetsrubrikken.
- **Retting:** Brukeren godkjente én gjennomgang i tidsrekkefølge. Tre uvanlige uker på rad blir nytt nivå med en gang, og senere uker sammenlignes med det nye nivået. Addendumet forklarer valget, og E15 tester regelen.
- **Commit eller pull request:** `4ada86d` (PRD-memloggen, linje 89; arbeidsloggen, linje 74).
- **Kilde:** arbeidsloggen, linje 72; sesjonslogg 997, linje 19; PRD-memloggen, linje 66 og 74–75; `review-calculations.md`, linje 30 og 74; `review-rubric.md`, linje 101–105; addendumet, linje 189; PRD-en, linje 616–617 og 682.
- **KI-styringsloggen:** [tilfelle 5](ki-styringslogg.md#5-prognosekonflikten-i-r-10-og-r-11-23-november-2026).

### Eksempel 3: CSS-regelen som traff tegnforklaringen

- **Feil:** I mockupen for konsept D gjør regelen `.chart svg{width:100%}` grafen like bred som panelet. Regelen treffer også symbolene i tegnforklaringen under grafen, så de kan bli vist større enn 14 og 24 px. Den samme regelen gjorde bryteren for uvanlige uker like bred som panelet, og en lignende regel gjorde varseltrekanten for stor 7. november (rad 9 og 3 under [Andre feil fra arbeidsloggen](#andre-feil-fra-arbeidsloggen)).
- **Hvordan det ble funnet:** Claude så det da bryteren ble rettet 16. november, og tok det opp med brukeren. Arbeidsloggen nevner bare bryteren og varseltrekanten.
- **Retting:** Ikke rettet i mockupen. Etter brukerens beskjed ble symbolene stående som de var. Spinene gir de riktige størrelsene og sier at regelen for grafen ikke skal treffe andre SVG-er, og UX-dekningskontrollen fører det som et kjent avvik fra mockupen. Story 2.10 krever at regelen ikke treffer symbolene i tegnforklaringen eller andre SVG-er.
- **Status:** ikke rettet i mockupen; overlatt til story 2.10.
- **Commit eller pull request:** `5db2fe7` for spinene (arbeidsloggen, linje 211) og `9dee8b1` for story 2.10 (arbeidsloggen, linje 492).
- **Kilde:** mockupen, linje 182; sesjonslogg 988, linje 117 og 193; UX-memloggen, linje 22 og 29; `DESIGN.md`, linje 476; `EXPERIENCE.md`, linje 347; UX-dekningskontrollen, linje 49 og 98; `epics.md`, linje 492 og 1444; arbeidsloggen, linje 102 og 194.
- **KI-styringsloggen:** [tilfelle 18](ki-styringslogg.md#18-den-store-bryteren-1516-november-2026), om bryteren.

### Eksempel 4: Feil bruddpunkt og grafbeskrivelse

- **Feil:** Forslaget fra gjennomgangen av struktur og språk til en egen tabell for appen satte filteret på mobil til et rutenett på 2 × 2 ved 640 px, med verdier fra den gjeldende tabellen i UX-dokumentene. Skissen gjør det ved 560 px. Dokumentene ga også grafene `<title>` og `<desc>`, som er SVG-elementer, mens grafene skulle tegnes med Chart.js på et lerret (canvas).
- **Hvordan det ble funnet:** Bruddpunktet kom fram da forslaget ble tatt inn og bruddpunktene ble hentet fra skissen, som bytter filteret ved 560 px. Bare arbeidsloggen sier at gjennomgangen fant feilen i bruddpunktet (linje 122). Gjennomgangen påpekte selv at grafbeskrivelsen ikke passet med Chart.js.
- **Retting:** Dokumentene fikk de faktiske bruddpunktene, med filteret på 2 × 2 ved 560 px, og en tekstoppsummering for grafene med Chart.js. Designet ble ikke endret. UX-en fra 6.–7. november ble arkivert 15. november.
- **Commit eller pull request:** `23a7589` (sesjonslogg 996, linje 191).
- **Kilde:** arbeidsloggen, linje 120–122 og 180; den arkiverte UX-memloggen, linje 43; den arkiverte `review-structure-prose.md`, linje 39, 49 og 138; den arkiverte `key-produktoversikt.html`, linje 165; den arkiverte `EXPERIENCE.md`, linje 207.
- **KI-styringsloggen:** [tilfelle 11](ki-styringslogg.md#11-feil-bruddpunkt-og-grafbeskrivelse-7-november-2026).

### Andre feil fra arbeidsloggen

Hver feil som arbeidsloggen beskriver, og som ikke står i eksemplene over, har sin egen rad. Rad 23 bygger bare på sesjonsloggen. Feil som en gjennomgangsfil beskriver i detalj, står under [Gjennomgangsfilene](#gjennomgangsfilene), med arbeidsloggen som tilleggskilde. Epics, sprintplanen og arkitekturen fra 8. november og UX-en fra 6.–7. november er arkivert. Story-numrene og AD-numrene i rad 4–6 gjelder derfor de arkiverte dokumentene, og et AD-nummer der betyr en annen beslutning i dagens arkitekturspine.

| Nr. | Dato | Feil | Hvordan det ble funnet | Retting | Commit eller pull request | Kilde |
|---|---|---|---|---|---|---|
| 1 | 14. oktober | Det første utkastet av Product Brief hadde egne tillegg og forslag fra KI, blant annet fire åpne punkter og et addendum, i stedet for bare brukerens reviderte tekst | Brukeren, som leste utkastet | Tilleggene ble avvist, `brief.md` ble skrevet om som en direkte oversettelse av brukerens tekst, og addendumet ble slettet | `5c4fb17` (arbeidsloggen, linje 41) | arbeidsloggen, linje 36–37; brief-memloggen, linje 17–20, 22 og 24–26; [KI-tilfelle 2](ki-styringslogg.md#2-ki-tilleggene-i-product-brief-ble-avvist-14-oktober-2026) |
| 2 | 1. november | En fil som skulle committes etter researchen, inneholdt en lokal filsti | Kontrollen før commit | Stien ble fjernet før commit, og brukeren innførte en fast personvernregel | `a55da02` og `f46a88b`, etter rettingen (arbeidsloggen, linje 62) | arbeidsloggen, linje 61–63; [KI-tilfelle 3](ki-styringslogg.md#3-lokal-filsti-og-en-fast-personvernregel-1-november-2026) |
| 3 | 7. november | En CSS-regel for grafen i skissene fra 6. november traff også varselikonet, så trekanten ble like bred som grafen | Brukeren så skissene i nettleseren og ba om en mye mindre trekant | Regelen gjelder bare grafen, og ikonene er 16 px | `23a7589` (sesjonslogg 996, linje 191) | arbeidsloggen, linje 94–95 og 102; sesjonslogg 996, linje 65; den arkiverte UX-memloggen, linje 35; [KI-tilfelle 10](ki-styringslogg.md#10-den-store-varseltrekanten-7-november-2026) |
| 4 | 8. november | Fire punkter fra addendumet og PRD §10 manglet i kravlisten i `epics.md` | Kontrollen av addendumet, som brukeren ba om | Punktene ble lagt til uten nye funksjoner | `f74665b` (sesjonslogg 994, linje 20) | arbeidsloggen, linje 147; sesjonslogg 994, linje 15; [KI-tilfelle 14](ki-styringslogg.md#14-addendumet-i-kravlisten-for-epics-8-november-2026) |
| 5 | 8. november | To stories i epic 1 viste til senere stories, og et kriterium for passordhashing (FR-1) manglet | Sluttvalideringen av epics og stories | Henvisningene og kriteriet ble rettet | `f74665b` (sesjonslogg 994, linje 20) | arbeidsloggen, linje 147; sesjonslogg 994, linje 18; [KI-tilfelle 14](ki-styringslogg.md#14-addendumet-i-kravlisten-for-epics-8-november-2026) |
| 6 | 8. november | Story 1.1 hadde ingen kilde for den lokale sesjonshemmeligheten (NFR-3, og AD-12 i den arkiverte arkitekturen) | Klarhetskontrollen i `bmad-sprint-planning` | Etter brukerens valg lager den første versjonen av `load_seed` bare hemmelighetsfila, og story 1.2 legger til dataene | `425d818` (sesjonslogg 993, linje 22) | arbeidsloggen, linje 153; sesjonslogg 993, linje 13 |
| 7 | 15. november | FR-24 fulgte det godkjente UX-designet, der årsaken står over tre kolonner, i stedet for lærerens funksjonelle krav | Brukeren | Prognosekolonnen viser årsaken, og bestillingskolonnen og uker dekning viser «–» | `47a8857` (arbeidsloggen, linje 174) | arbeidsloggen, linje 172; PRD-memloggen, linje 104 og 115; [KI-tilfelle 15](ki-styringslogg.md#15-fr-24-etter-tilbakemeldingen-15-november-2026) |
| 8 | 15.–16. november | Et skript fra Claude som styrte Safari, lukket en av brukerens faner | Brukeren | Claude åpner bare filer med `open -a Safari` og styrer ikke faner eller vinduer | ikke oppgitt i kilden | arbeidsloggen, linje 193; UX-memloggen, linje 15; sesjonslogg 988, linje 44; [KI-tilfelle 16](ki-styringslogg.md#16-safari-fanene-1516-november-2026) |
| 9 | 15.–16. november | Regelen `.chart svg{width:100%}` i konsept D traff også bryteren for uvanlige uker da den ble flyttet inn i grafpanelet, så bryteren ble like bred som panelet | Brukeren, i Safari | Én ny CSS-linje gir bryteren 40 × 22 px igjen, og en kontrollsum viste at ingenting annet var endret | `5db2fe7` (arbeidsloggen, linje 211) | arbeidsloggen, linje 191 og 194; UX-memloggen, linje 21; mockupen, linje 183; [KI-tilfelle 18](ki-styringslogg.md#18-den-store-bryteren-1516-november-2026) |
| 10 | 15.–16. november | Forklaringsteksten i konsept A–C brukte ukenummer som FR-27 ikke tillater | Claude, da konsept D ble laget | Konsept D og spinene følger FR-27; A–C er beholdt uendret som dokumentasjon | `5db2fe7` (arbeidsloggen, linje 211) | arbeidsloggen, linje 190 og 196; sesjonslogg 988, linje 106; UX-memloggen, linje 18 |
| 11 | 15.–16. november | Flere tekster i konsept A–C avvek fra ordlyden som FR-7, FR-10, FR-12 og FR-21 krever, og søkefeltet i A og C manglet en synlig etikett (NFR-11) | Claude, da konsept D ble laget | Konsept D og spinene følger PRD-en; A–C er beholdt uendret som dokumentasjon | `5db2fe7` (arbeidsloggen, linje 211) | arbeidsloggen, linje 190 og 196; sesjonslogg 988, linje 107–110; UX-memloggen, linje 18 |
| 12 | 15.–16. november | Mockupen for konsept D viser bare de siste 12 ukene, mens FR-15–FR-17 krever en markør for hver utsolgte uke, uvanlige uke og uke med nytt nivå | Da spinene ble skrevet; kildene sier ikke hvem som fant det | `EXPERIENCE.md` sier at grafen viser hele salgshistorikken, og spinene gjelder ved avvik. Mockupen er ikke endret, og brukeren bekreftet valget | `5db2fe7` (arbeidsloggen, linje 211) | arbeidsloggen, linje 201; UX-memloggen, linje 26; sesjonslogg 988, linje 123 |
| 13 | 16. november | Et kontrollskript fra Claude meldte «ingen funn» uten å ha lest filene, fordi skallet ikke delte opp fillisten | Claude, før commit | Kontrollen ble kjørt på nytt med riktig filliste | `5373e7b`, etter den nye kontrollen (arbeidsloggen, linje 236) | arbeidsloggen, linje 235; sesjonslogg 988, linje 152 |
| 14 | 16. november | Claude skrev «för» i stedet for «for» i den faste teksten «Tallene er avrundet for visning.» i `PRODUCT.md` | Claude, før kontrollen | Rettet | `e549c78` (arbeidsloggen, linje 258) | arbeidsloggen, linje 256; sesjonslogg 988, linje 173 |
| 15 | 16. november | `.gitignore` på designgrenen manglet `.secret_key` og `db.sqlite3` | Gjennomgangen av prosjektmappa, som brukeren ba om | Fila fikk samme blokk som story-grenen, byte for byte | `d67211c` (arbeidsloggen, linje 297) | arbeidsloggen, linje 284–288; sesjonslogg 987, linje 84–89 |
| 16 | 16. november | Arkivets README hadde feil dato for når PRD-en sist ble oppdatert | Den samme gjennomgangen | Datoen ble rettet til 16. november | `d67211c` (arbeidsloggen, linje 297) | arbeidsloggen, linje 289; sesjonslogg 987, linje 13 og 90 |
| 17 | 16. november | Claude skrev i arkivets README at sprintplanens datoer var passert, men bare den første milepælen var det | Kildene sier ikke hvordan | Setningen ble rettet | `652f747` (arbeidsloggen, linje 337; sesjonslogg 987, linje 130) | arbeidsloggen, linje 336; sesjonslogg 987, linje 130 |
| 18 | 16. november | En kontrollkommando fra Claude brukte en skrivemåte som macOS-versjonen av `sed` ikke godtar | Kommandoen feilet | Kontrollen ble gjort på nytt med Python, og ingenting ble committet før den var gjort | `1a0709e`, etter den nye kontrollen (arbeidsloggen, linje 354) | arbeidsloggen, linje 353; sesjonslogg 987, linje 152–153 |
| 19 | 16. november | Sikkerhetssjekken i den første slettekommandoen fra Claude var feil skrevet og ga feil returkode for filer som git ikke sporet | Kommandoen stoppet før noe ble slettet | Claude kontrollerte at alt fortsatt fantes, og kjørte kommandoen på nytt med riktig sjekk | ikke oppgitt i kilden | arbeidsloggen, linje 384; sesjonslogg 987, linje 179 |
| 20 | 17. november | Den arkiverte arkitekturen fra 8. november la nettverkskode i en modul som den selv forbød nettverkskode i, og skrifttypen, grafbiblioteket og tallkontrollen i forklaringen var blitt utdatert | Claude, som leste den arkiverte arkitekturen kritisk i arkitektursteget | En ny arkitekturspine; den arkiverte ble ikke gjenbrukt ukritisk | `1441c40` (arbeidsloggen, linje 441) | arbeidsloggen, linje 405–410; arkitektur-memloggen, linje 21 |
| 21 | 17. november | Den foreslåtte porten 54320 kan være reservert på Windows | Claude, da brukeren ville ha Docker-løsningen bekreftet før godkjenningen | Porten ble endret til 15432 | `1441c40` (arbeidsloggen, linje 441) | arbeidsloggen, linje 427; arkitektur-memloggen, linje 39, 44 og 46; [KI-tilfelle 21](ki-styringslogg.md#21-docker-oppsettet-bekreftet-og-ny-port-17-november-2026) |
| 22 | 17. november | Tre utsagn i arkivets README var blitt utdatert, og addendum §2 beskrev databasen som en lokal fil | Sluttkontrollen før commit | Rettet | `1441c40` (arbeidsloggen, linje 441) | arbeidsloggen, linje 437; sesjonslogg 986, linje 77–79 |
| 23 | 18. november | Tre hull i `epics.md`: E20 manglet i story 2.2, story 2.6 manglet kontrollen av regeltestproduktene mot regnearket (PRD §10 spørsmål 4), og R-14 og R-17 manglet for sesongtestproduktet i story 5.1 og 5.2 | Sluttvalideringen i `bmad-create-epics-and-stories` | Alle tre ble rettet | `9dee8b1` (sesjonslogg 985, linje 84) | sesjonslogg 985, linje 51–58 |
| 24 | 18. november | 29 feil og mangler (A1–A14 og E1–E15) i `epics.md`, arkitekturspinen og `EXPERIENCE.md`. De viktigste: demoverdiene, der mockupen hadde to verdier som reglene ikke kan gi (Skruer 21,5 og Kabelstrips 3,7, som demoverdiene nå setter til 21,3 og 3,8), og fordelingen mellom testbedriftene, så testbedrift A har 4 produkter med varsel; manglende akseptansekriterier for svaret 405 og veien til 503-siden; nulldesimaler (funn E14: «10,0» regnes som 10); og at AD-12 skal gi 405 og 503 fra den ytterste mellomvaren | BMAD Review med linsene adversarial og edge case, kjørt i hovedtråden | Brukeren godkjente at alle ble rettet, og funnene A4 og E14 ble kontrollert mot kildene først | `9dee8b1` (arbeidsloggen, linje 492; `epics.md`, linje 2305) | arbeidsloggen, linje 456; sesjonslogg 985, linje 59–74; `epics.md`, linje 2305; `EXPERIENCE.md`, linje 347; [KI-tilfelle 23](ki-styringslogg.md#23-nfr-8-kontrollert-mot-kildene-18-november-2026) |
| 25 | 18. november | Merknaden om GitHub Issues (A5) bygde på sammendraget av sensorveiledningen, ikke på originalen | Brukeren limte inn hele sensorveiledningen | Merknaden viser til den originale sensorveiledningen, som godtar «issues eller tilsvarende» | `9dee8b1` (`epics.md`, linje 2308) | arbeidsloggen, linje 477; sesjonslogg 985, linje 101 og 105; [KI-tilfelle 24](ki-styringslogg.md#24-github-issues-og-funn-a5-18-november-2026) |
| 26 | 18. november | Claude foreslo å lenke til lærerens godkjenning av avgrensningen, men ingen kilde dokumenterte en godkjenning | Brukeren ba om at ingenting skulle påstås godkjent uten dokumentasjon, og kontrollen viste at det ikke fantes noen | Story 4.1 krever at README-en gjengir lærerens tilbakemelding med dens egne ord og ikke kaller den en godkjenning | `9dee8b1` (`epics.md`, linje 2311) | arbeidsloggen, linje 478; sesjonslogg 985, linje 115; [KI-tilfelle 25](ki-styringslogg.md#25-ikke-godkjent-uten-dokumentasjon-18-november-2026) |
| 27 | 18. november | Raden «Test sizes» i `EXPERIENCE.md` sa at også 1366 × 768 bare testes i responsiv visning, mens story 4.1 og 4.4 tester PC-størrelsen i nettlesere på PC | Sluttkontrollen før commit | Raden og UX-DR7 sier nå hvilke størrelser som testes i nettlesere på PC, i responsiv visning og på ekte iPhone 13 | `9dee8b1` (`epics.md`, linje 2313) | arbeidsloggen, linje 486–487; sesjonslogg 985, linje 133 |
| 28 | 18. november | NFR-2 sto i «Also covers» for epic 2, men ingen story i epic 2 nevnte NFR-2 | Sluttkontrollen før commit | NFR-2 ble lagt til i story 2.6, og NFR-6 og UX-DR7 i «Also covers» for epic 1, 3 og 4 | `9dee8b1` (`epics.md`, linje 2313) | arbeidsloggen, linje 486 og 488–489; sesjonslogg 985, linje 134–135 |
| 29 | 19. november | `docs/PRODUCT.md` sa fortsatt at appen bare er for PC, selv om NFR-6 var utvidet til PC, iPad og mobil 18. november | Under oppdateringen etter lærerens avklaring; kilden sier ikke hvem som fant det | Linja om miljøet nevner nå PC, iPad og telefon | `ea06f01` (PR #5), commiten for endringene 19. november (PRD-en, linje 978; arbeidsloggen, linje 525 og 531) | arbeidsloggen, linje 520; sesjonslogg 985, linje 179 |
| 30 | 19. november | Tekst fra publiseringen sto igjen i `epics.md` og addendumet, blant annet AD-16 i story 5.1 og 8.2 | Kontrollen av Implementation Readiness | Teksten ble rettet, og story 5.1 og 8.2 viser til AD-15 | `67694f7` (PR #6) (arbeidsloggen, linje 552; `epics.md`, linje 2316) | arbeidsloggen, linje 536 og 547; sesjonslogg 984, linje 20 |
| 31 | 19. november | Arkitekturspinen sa både `uv sync` og `uv sync --locked` | Kontrollen av Implementation Readiness | Spinen og story 1.1 bruker `uv sync --locked` | `67694f7` (PR #6) (arbeidsloggen, linje 552; `epics.md`, linje 2316) | arbeidsloggen, linje 537; sesjonslogg 984, linje 21 og 37 |
| 32 | 19. november | Story 1.8 bruker `forecasting/display.py` før story 2.3 lager den | Kontrollen av Implementation Readiness | Ikke rettet i planen. Det står som åpent punkt i `issues.md`: story 1.8 lager ukeetiketten selv, med test | ikke oppgitt i kilden | arbeidsloggen, linje 538; sesjonslogg 984, linje 22, 56 og 60; `issues.md`, linje 87 |
| 33 | 19. november | Addendum §2 sa fortsatt at versjonene skal kontrolleres på nytt innen 2026-12-01, mens §5 sa 2026-12-08 | Kontrollene etter endringene | Datoen ble rettet til 2026-12-08 etter brukerens godkjenning, og PRD §12 nevner rettingen | `67694f7` (PR #6) (arbeidsloggen, linje 552) | arbeidsloggen, linje 551; sesjonslogg 984, linje 52 |

### Gjennomgangsfilene

Hver gjennomgangsfil har én rad med antall funn, de viktigste feilene og en lenke. Filene er den detaljerte oversikten over funnene. Ingen av dem nevner en commit; commitene står i kildene som er oppgitt i raden.

| Fil | Gjennomgang | Funn | De viktigste feilene | Retting og commit |
|---|---|---|---|---|
| [`review-calculations.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-calculations.md) | Uavhengig beregningskontroll av PRD-utkastet, 3. november | 19 funn (1 kritisk, 4 høye, 8 middels og 6 lave) og 16 manglende referanseeksempler | F1: rekkefølgen i R-10 og R-11 (eksempel 2); F2: et produkt kunne være både «lav» og «middels»; F4: sesongjusteringen i R-14 kunne dele 0 på 0 | Fila fører ikke rettingene. Brukeren godkjente dem, og PRD-memloggen fører dem (linje 66–68 og 74–75). Commit `4ada86d` (PRD-memloggen, linje 89) |
| [`review-rubric.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-rubric.md) | Kvalitetsrubrikken for PRD-utkastet, 2. november | 21 funn (3 høye, 11 middels og 7 lave) | Må-grensen i SM-1 tok med E14, som tester en bør-ha-regel; regelen for nytt nivå hadde to tolkninger (51,0 eller 71,0); tallene på utregningslinjen i FR-12 kunne gi 20, mens bestillingsmengden var 21 | Fila fører ikke rettingene. PRD-memloggen fører dem (linje 66 og 74–75). Commit `4ada86d` (PRD-memloggen, linje 89) |
| [`review-consistency.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-consistency.md) | Konsistenssjekk av PRD-utkastet og addendumet, 2. november | 38 funn (1 høy, 12 middels og 25 lave) | PR-1: må-grensen tok med en bør-ha-test (E14); IC-3: reglene for tillitsmerket motsa hverandre; IC-2: utregningslinjen i FR-12 viste andre tall enn beregningen brukte | Fila fører ikke rettingene. PRD-memloggen fører dem (linje 74–75). Commit `4ada86d` (PRD-memloggen, linje 89) |
| [`review-sensorveiledning.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-sensorveiledning.md) | Kontroll av PRD-en mot sensorveiledningen for del 1, 3. november | 29 funn (8 høye, 16 middels og 5 lave); de fleste er mangler, ikke feil | 1.7: addendumet viste til feil spørsmål i PRD §10 og sa at E3–E14 bygde på håndregning, mens fasiten gikk til E30 | Delen «Outcome» i fila fører rettingene (linje 139–146), og PRD-memloggen fører beslutningene (linje 78 og 86). Commit `4ada86d` (PRD-memloggen, linje 89) |
| [`review-structure-prd.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-structure-prd.md) | Strukturgjennomgang av PRD-en med `bmad-review`, 3. november | 15 funn og 13 små rettinger | S5: listen over varsler i FR-26 hadde glidd fra R-15; S15: en utdatert henvisning til spørsmål 4 i PRD §10 fra addendum §5 | Brukeren godkjente alle forslagene, og de ble tatt inn (PRD-memloggen, linje 92–93). Commit `d938baa` (arbeidsloggen, linje 74) |
| [`review-prose-prd.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-prose-prd.md) | Språkgjennomgang av PRD-en med `bmad-review`, 3. november | 22 funn og 22 små rettinger | P3: tallene i E3 sto i en annen rekkefølge enn etikettene; P8: FR-15 sa at utsolgte uker ikke telles i noen terskel, mens de teller i lengden på salgshistorikken; P11: «fast tekst» i FR-10 passet ikke med en prosent som kan endres | Brukeren godkjente alle forslagene (PRD-memloggen, linje 92–93). Commit `d938baa` (arbeidsloggen, linje 74) |
| [`review-structure-addendum.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-structure-addendum.md) | Strukturgjennomgang av addendumet, 3. november | 9 funn og 2 små rettinger | A1: kildenøklene viste til §6 i stedet for §8; A6: en henvisning til et spørsmål i PRD §10 som hadde fått nytt nummer | Brukeren godkjente alle forslagene (PRD-memloggen, linje 92–93). Commit `d938baa` (arbeidsloggen, linje 74) |
| [`review-prose-addendum.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-prose-addendum.md) | Språkgjennomgang av addendumet, 3. november | 23 funn og 14 små rettinger | P1: en setning gjenga kilden feil (eksempelet med linjegrafen); P19: regelen fra Product Brief var gjengitt med andre ord enn briefen | Brukeren godkjente alle forslagene (PRD-memloggen, linje 92–93). Commit `d938baa` (arbeidsloggen, linje 74) |
| [`review-consistency-2026-11-15.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-consistency-2026-11-15.md) | Konsistenssjekk av PRD-oppdateringen etter lærerens tilbakemelding, 15. november | 10 funn (3 middels og 7 lave) og 11 avvik i dokumentene etter PRD-en | C-1: FR-25 trakk bør-ha- og kan-ha-tekster inn i et må-ha-krav; C-2: de tillatte tallene i FR-27 utelot tall som FR-26 krever; C-3: kutt-linjen for publisering var ikke ført inn i DR-8, FR-4 og DR-1 | De 10 funnene ble rettet (arbeidsloggen, linje 171; PRD-memloggen, linje 110). De 11 avvikene ble ikke rettet, fordi dokumentene ble arkivert og laget på nytt fra den oppdaterte PRD-en (arbeidsloggen, linje 180 og 326). Commit `47a8857` (arbeidsloggen, linje 174) |
| [`review-rubric-2026-11-15.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/review-rubric-2026-11-15.md) | Kvalitetsrubrikken for PRD-oppdateringen, 15. november | 12 funn (1 høy, 5 middels og 6 lave) | Oppdateringen sa ikke hvilke dokumenter etter PRD-en den endret, og de motsa den (høy); de tillatte tallene i FR-27 utelot tall som FR-26 og UX-en har i forklaringen; plassholderkontrollen i FR-28 godtok en tekst der en plassholder var flyttet til feil setning | Funnene innenfor lærerens punkter ble rettet (PRD-memloggen, linje 110), i commit `47a8857` (arbeidsloggen, linje 174). Fire funn utenfor ble utsatt (PRD-memloggen, linje 111). Av dem ble kontrollen av FR-35 og årstallene i ukelister lukket 16. november (PRD-memloggen, linje 117), i `5373e7b` (PRD-en, linje 971–972). Sluttvalideringen 18. november knyttet §10 spørsmål 4 til regeltestproduktene i story 2.6 (rad 23), men ingen kilde lukker funnet (linje 35). Funnet om E30 (linje 101) har ingen registrert lukking. Begge står under «Gjenstår» |
| [`review-coverage.md`](../_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/review-coverage.md) for UX-en | Dekningskontroll av UX-spinene, 16. november | Ingen nummererte funn | Komponenten «Panel» manglet en rad for atferd; to kjente avvik fra mockupen: grafen viser bare 12 uker, og symbolene i tegnforklaringen kan bli for store | «Panel» fikk en rad (linje 27). Avvikene er ikke rettet i mockupen, og spinene gjelder (linje 47–49 og 98; rad 12 og eksempel 3). `EXPERIENCE.md` (linje 347) fører nå fire avvik fra mockupen: disse to, to verdier som reglene ikke kan gi, og 3 i stedet for 4 produkter med varsel (rad 24; «Gjenstår»). Fila nevner åtte rettinger fra struktur- og språkgjennomgangen (linje 3), men lister dem ikke. Commit `5db2fe7` (arbeidsloggen, linje 211) |
| [`review-inline.md`](../_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/reviews/review-inline.md) for arkitekturen | Gjennomgang av arkitekturspinen i hovedtråden, uten subagenter, 17. november | 12 funn: 8 hull og 4 mangler | Hull 6: `load_seed` kunne skrive en hemmelig fil inn i publiseringen; hull 7: veien tilbake fra Innstillinger kunne bli en åpen videresending (open redirect); hull 3: innlesingen kunne lese data uten bedriftsfilteret | Alle 12 ble rettet i spinen før den ble satt til `final`, og fila viser rettingen for hvert funn (linje 5 og 41–72; arbeidsloggen, linje 439). Commit `1441c40` (arbeidsloggen, linje 441) |
| [`review-coverage.md`](../_bmad-output/planning-artifacts/archive/ux-G40-lyamouri-2026-11-06/review-coverage.md) i arkivet | Dekningskontroll av UX-spinene fra 7. november | 2 lave funn | Samlet bestillingsoversikt manglet en tilstand for når ingen data er lastet, og statussetningen i skissen hadde 3 «Justert av deg», mens demodataene har 2 | Begge ble rettet (den arkiverte UX-memloggen, linje 41; sesjonslogg 996, linje 119). Commit `23a7589` (sesjonslogg 996, linje 191) |
| [`review-structure-prose.md`](../_bmad-output/planning-artifacts/archive/ux-G40-lyamouri-2026-11-06/review-structure-prose.md) i arkivet | Struktur- og språkgjennomgang av UX-spinene, 7. november | 7 strukturfunn, 22 språkfunn og 13 små rettinger | En grafbeskrivelse som ikke passet med Chart.js (linje 138). Forslaget til en egen tabell for appen hadde selv filteret på mobil ved 640 px (linje 49); 560 px kom fra skissen da forslaget ble tatt inn (eksempel 4) | Alle forslagene ble tatt inn (den arkiverte UX-memloggen, linje 43; sesjonslogg 996, linje 121). Commit `23a7589` (sesjonslogg 996, linje 191) |

**Gjenstår.**
- Mockupen for konsept D er ikke rettet. `EXPERIENCE.md` (linje 347) fører fire avvik fra mockupen, og spinene gjelder for alle fire: grafen viser bare de siste 12 ukene (rad 12); symbolene i tegnforklaringen kan bli for store (eksempel 3); to verdier kan ikke oppstå etter reglene, Skruer 21,5 og Kabelstrips 3,7 (rad 24); og «Denne uken» teller 3 produkter med varsel, mens testbedrift A med demoproduktet fra E8 har 4 (rad 24). Story 2.10 krever at regelen for grafen ikke treffer symbolene i tegnforklaringen.
- Story 1.8 må selv lage ukeetiketten i `forecasting/display.py`, med test, fordi toppfeltet viser den før story 2.3 bygger ut modulen (rad 32; åpent punkt i `issues.md`).
- Spørsmål 4 i PRD §10: sluttvalideringen 18. november knyttet det til regeltestproduktene i story 2.6 (rad 23), men ingen kilde lukker funnet om det i `review-rubric-2026-11-15.md` (linje 35).
- E30: funnet i `review-rubric-2026-11-15.md` om at E30 ikke kan vise at varselet om sesongmønster påvirker tillitsmerket (linje 101), har ingen registrert lukking.

## 2026-11-21 – Feil i KI-generert tekst fra reviewen av story 1.1 del B (DR-9)

**Hvordan det ble funnet.** Claude Code skrev statustabellen, KI-styringsloggen og oppføringen over om planleggingsfasen i story 1.1 del B med `bmad-build`. Før første commit gikk tre uavhengige KI-granskere gjennom diffen: Blind Hunter, Edge Case Hunter og Verification Gap. Claude kontrollerte hvert funn mot kildene. Alle 20 funnene står med vurdering og begrunnelse under «Review Triage Log» i `_bmad-output/implementation-artifacts/spec-1-1-planning-phase-process-documents.md`, og alle ble rettet. Selve plassen for epics som ikke blir bygd i statustabellen, hører til story 4.3, og innledningen viser nå til den.

**Feilene som ble rettet.** Alle ble rettet før første commit og ligger i `79c9154`.

| Feil | Funnet av | Retting |
|---|---|---|
| Eksempel 1 og tilfellene 4 og 7 sa feil om hvem som foreslo hva: regelen om å runde opp var brukerens beslutning i brainstormingen, og det KI-skrevne sammendraget gjorde lærerens svar avgjørende for språkmodellen | Blind Hunter; bekreftet mot memloggene | Tekstene følger kildene og sier hvorfor E5 står i begge loggene |
| Eksempel 4 og tilfelle 11 sa at gjennomgangen fant bruddpunktet, men forslaget i gjennomgangen hadde selv 640 px, og 560 px kom fra skissen | Blind Hunter; bekreftet mot den arkiverte gjennomgangen og skissen | Tekstene følger gjennomgangsfila og memloggen |
| Raden for de 29 feilene 18. november nevnte ingen av dem, så de to verdiene i mockupen som ikke kan oppstå etter reglene, sto ingen steder | Blind Hunter; bekreftet mot sesjonslogg 985 | Raden nevner de viktigste feilene |
| «Gjenstår» nevnte bare symbolene i tegnforklaringen, mens `EXPERIENCE.md` fører fire avvik fra mockupen | Blind Hunter | Alle fire står i «Gjenstår» |
| To utsatte funn fra rubrikken 15. november, spørsmål 4 i PRD §10 og E30, var verken ført som lukket eller som åpne | Blind Hunter og Edge Case Hunter | Raden og «Gjenstår» sier hva kildene viser |
| AD-numre fra den arkiverte arkitekturen fra 8. november var ikke merket | Blind Hunter | Merket som den arkiverte arkitekturens |
| Statustabellen lovet en grunn bare for må-ha- og bør-ha-krav som ikke er bygd, og nevnte ikke epics som ikke blir bygd (D-2) eller et oppsett som ikke kunne testes på Windows (D-3) | Edge Case Hunter og Blind Hunter | Innledningen dekker hvert avvik og de to pliktene |
| KI-styringsloggen sa ikke at story 1.1 ga ingen tilfeller | Blind Hunter | En del om byggefasen |
| Lenkene fra KI-styringsloggen til QA-loggen landet på en tabell med 30 rader, og linjenumrene viste til filer som endres | Blind Hunter og Edge Case Hunter | En kolonne med radnummer, og lenker til repoet i `d8674ad` |
| Tre feil manglet i QA-loggen: tilleggene i Product Brief, Safari-skriptet og tre hull fra sluttvalideringen 18. november, og to tilfeller manglet lenker begge veier | Blind Hunter og Edge Case Hunter | Tre nye rader og lenker begge veier |
| FR-1-raden viste ingen tester, selv om tre tester i `tests/test_company.py` nevner FR-1 | Verification Gap | Cellen viser de tre testene |
