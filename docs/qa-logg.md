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

**Gjenstår.** Begge testene kjøres i første story og på nytt på siste commit (DR-9, SM-2). (Merknad 21. november: testene på Windows og uten nett er nå story 1.3.) (Merknad 22. november: oppstarten uten nett med Docker Desktop passerte på macOS, og oppsettet på Windows er bare testet uten Docker; se [oppstart uten nett på macOS](#2026-11-22--oppstart-uten-nett-på-macos-story-13-nfr-1-sm-2-dr-9) og [oppsettet på Windows](#2026-11-22--oppsettet-på-windows-story-13-sm-2-nfr-1-dr-1-d-3).)

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
- Brukeren sjekker `/` i Safari i responsiv visning ved 320 px, 390 × 844 og 820 × 1180 før pull requesten. (Gjort 20. november og på nytt 21. november, se [responsiv visning i Safari](#2026-11-20-og-2026-11-21--responsiv-visning-av-startsiden-i-safari-story-11-nfr-6-ux-dr7).)
- De fem kommandoene kjøres på nytt fra en `git clone` av den pushede grenen før pull requesten flettes. (Gjort 21. november, se [klonetesten fra GitHub](#2026-11-21--klonetest-fra-github-story-11-nfr-1-nfr-3-sm-2).)
- Tidtakingen av hele oppsettet fra klonen, utført av en person (SM-2), hører til Story 4.1 og 4.4.
- Oppsett på Windows x64 og oppstart uten nett hører til Story 1.3. (Oppstarten uten nett på macOS er gjort 22. november, med Docker Desktop helt avsluttet i kjøring 2, se [oppstart uten nett på macOS](#2026-11-22--oppstart-uten-nett-på-macos-story-13-nfr-1-sm-2-dr-9). Oppsettet på Windows er bare testet uten Docker, se [oppsettet på Windows](#2026-11-22--oppsettet-på-windows-story-13-sm-2-nfr-1-dr-1-d-3).)

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
| BOM-testen kunne ikke oppdage en feil, og BOM-tegnet var usynlig i kildekoden | Blind Hunter; bekreftet | En `KEY=VALUE`-linje rett etter BOM, og BOM skrevet som `"\ufeff"` |
| To tester lovet mer enn de sjekket, eller viste til feil beslutning (AD-11 for svaret 405) | Blind Hunter | Navnene og docstringene beskriver det testene sjekker |
| README og QA-loggen sa ikke hva som er testet, hvilken database testene bruker eller hva Ruff sjekker, og QA-loggen manglet én kjøring | Blind Hunter | Tekstene er rettet |
| `REQUIRED_FIELDS` i `web.Company` var en liste, som Ruff flagget (RUF012) | Ruff under implementeringen | Endret til en tuppel |

**Kjente feil som ikke ble rettet.** Reviewen bekreftet også disse feilene, men de ble avvist, fordi de er lite sannsynlige i vanlig bruk og rettingen ville gitt mer kode, eller fordi en senere story eier dem. Begrunnelsene står under «Review Triage Log» i spesifikasjonen, og BMAD Code Review 21. november beholdt vurderingene.

| Feil | Funnet av | Hvorfor den ikke ble rettet |
|---|---|---|
| Mangler `.secret_key`, får hver prosess en tilfeldig nøkkel uten advarsel, så en innlogging ville ikke overlevd en omstart før `load_seed` har kjørt | Blind Hunter | Ufarlig til innloggingen kommer i story 1.8, som skal vurdere en advarsel (`issues.md`) |
| `create_user` godtar et tomt navn | Blind Hunter og Edge Case Hunter | Bare seed-dataene i story 1.7 lager bedrifter, og de har navn |
| Et anførselstegn som ikke lukkes i `.env`, blir stående i verdien, så `PROGNOSE_DEBUG='1` gir DEBUG av | Edge Case Hunter; gjenskapt | Krever en skrivefeil, og rettingen gir en ny gren |
| To samtidige kjøringer av `load_seed` kan se en tom `.secret_key` | Edge Case Hunter | Krever to kjøringer i samme øyeblikk |
| `createsuperuser` stopper med `AttributeError` | Edge Case Hunter | Superbrukere er utenfor storyen etter spesifikasjonen |
| Et kundenummer med mellomrom foran eller bak, eller bare mellomrom, godtas | Edge Case Hunter | Bare seed-dataene lager bedrifter, og innloggingen kommer i story 1.8 |
| Porten 15432 kan være opptatt av en annen klone | Edge Case Hunter | Docker sier selv hvilken port som er opptatt, og hjelpen for en opptatt port i README er story 4.1 |

Testen av at git ignorerer `.secret_key` og `.env`, som også ble avvist i del A, ble lagt til i BMAD Code Review 21. november.

**Utsatt.** Telefontesten starter appen på `0.0.0.0`, slik AD-13 sier. Det er ett punkt som to granskere fant. Forslaget om å binde den til den private adressen står i `deferred-work.md`, fordi det krever en endring i arkitekturen som brukeren må godkjenne.

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

## 2026-11-21 – Klonetest fra GitHub (Story 1.1; NFR-1, NFR-3, SM-2)

**Hvorfor.** Story 1.1 krever at Prognose starter fra en ny klone (`epics.md`, linje 707–710 i `2791949`). Det første oppsettet 20. november brukte en ren kopi av filene, så QA-loggen og `issues.md` krevde en kjøring fra en ekte `git clone` av den pushede grenen før pull requesten flettes.

**Oppsett.**
- Claude Code kjørte testen 21. november 2026 etter brukerens godkjenning. Ingen person kjørte den.
- Samme maskin og programvare som 20. november: macOS 15.6.1 på Apple M1, Docker Desktop 4.99.0 med Docker Compose v5.7.0, og uv 0.12.13. Imaget `postgres:18.7`, Python 3.13 og pakkene lå allerede lokalt.
- Grenen ble klonet fra GitHub med `git clone --branch story/1-1-start-prognose-locally https://github.com/IBE160-2026/G40-lyamouri.git` til en midlertidig mappe utenfor repoet. README kloner `main`, som ennå ikke har story 1.1, så testen klonet grenen.
- Mappa med klonen fikk et annet navn enn `G40-lyamouri`, slik at Docker Compose ikke brukte repoets database og volum. Repoets database var stoppet mens testen kjørte, fordi begge bruker porten 15432. Klonen, databasen og volumet til klonen ble slettet etterpå.
- Klient: `curl` mot `http://127.0.0.1:8000/`, og `lsof` for adressene appen og databasen lyttet på. Ingen nettleser var med.

**Resultat.**

| Steg | Resultat | Tid (sekunder) |
|---|---|---|
| `git clone --branch story/1-1-start-prognose-locally` | HEAD var `3edf54b`, den samme commiten som grenen på GitHub | 1,3 |
| `docker compose up -d --wait` | databasen var klar («healthy») | 2,8 |
| `uv sync --locked` | fullførte uten feil | 0,2 |
| `uv run python src/manage.py migrate` | fullførte uten feil | 2,6 |
| `uv run python src/manage.py load_seed` | «Lagde .secret_key med en ny hemmelig nøkkel.»; fila kan bare leses av eieren (modus 600) | 0,2 |
| `uv run python src/manage.py runserver --insecure` | appen svarte på første forespørsel | 1,0 |
| Totalt for de fem kommandoene | | 7,1 |

| Kontroll | Resultat |
|---|---|
| Endrede filer rett etter utsjekkingen | ingen |
| Filer i klonen | alle 458 sporede filer, blant dem `uv.lock`, `.python-version`, `compose.yaml`, `.env.example` og `src/web/migrations/0001_initial.py` |
| `docs/DESIGN.md` | en symbolsk lenke, og målet finnes |
| `curl http://127.0.0.1:8000/` | status 200, med `<html lang="nb">` og «Prognose» |
| `lsof` på porten 8000 og 15432 | appen lyttet bare på `127.0.0.1:8000`, og databasen bare på `127.0.0.1:15432` |
| Passord i databasen | rollen `prognose` har ikke lagret passord |
| `.env`, nøkkel og redigering av filer | ingen av stegene trengte noe av dette |

Tidene er lave, fordi imaget, Python og pakkene allerede lå lokalt.

**Gjenstår.** Det samme som etter det første oppsettet 20. november; se «Gjenstår» i den oppføringen.

## 2026-11-20 og 2026-11-21 – Responsiv visning av startsiden i Safari (Story 1.1; NFR-6, UX-DR7)

**Hvorfor.** Hver side en story legger til, skal sjekkes i nettleserens responsive visning minst ved 320 px, 390 × 844 (iPhone 13) og 820 × 1180 (iPad), og pull requesten skal nevne sjekkene (reglene for hver story i `epics.md`, linje 594 i `2791949`; NFR-6, UX-DR7). Story 1.1 la til siden `/`.

**Oppsett.**
- Brukeren testet selv i den responsive visningen i Safari, først 20. november 2026 og på nytt 21. november etter del B. Begge resultatene ble ført 21. november etter brukerens bekreftelse.
- Safari 18.6 på macOS 15.6.1, på Mac-en der Prognose kjører, fordi appen bare svarer på 127.0.0.1. Versjonen er lest fra programmet 21. november.
- Siden `/` fra `93c9147`. Malen, viewet og URL-en er ikke endret siden, fordi del B bare endret dokumenter.

**Resultat.** Begge dagene viste alle tre størrelsene «Prognose» og teksten.

| Tilsvarer | 20. november | 21. november, etter del B |
|---|---|---|
| Den minste bredden i NFR-6 | 320 px bred: ingen sidelengs rulling eller avkuttet tekst | 320 × 844: ingen avkuttet tekst eller synlig sidelengs rulling |
| iPhone 13 | 390 × 844: ingen sidelengs rulling eller avkuttet tekst | 390 × 844: ingen avkuttet tekst eller synlig sidelengs rulling |
| iPad | 820 × 1180: ingen sidelengs rulling eller avkuttet tekst | 820 × 1180: ingen avkuttet tekst eller synlig sidelengs rulling |

**Gjenstår.**
- Pull requesten for story 1.1 skal nevne de tre størrelsene som sjekker i responsiv visning.
- Testen på en ekte iPhone 13 over det lokale nettet hører til story 1.8 (NFR-6).

## 2026-11-21 – Motsigelse i planen om CI før story 1.2 (DR-7, DR-9)

**Hvordan det ble funnet.** Claude fant motsigelsen 21. november 2026, da brukeren ba om å få sjekket om story 1.1 kan flettes før CI finnes. Kontrollen av Implementation Readiness 19. november fant den ikke. Linjenumrene under gjelder filene i commit `2791949`.

**Feil.** Reglene for alle stories i `epics.md` (linje 589) og punkt 5 i rutinen for code review (linje 611) krever at testene og Ruff passerer lokalt og i CI før en story flettes. AD-17 i arkitekturspinen fletter en pull request bare når GitHub Actions passerer (linje 207 og 222). Den samme planen legger CI i story 1.2, etter story 1.1 (`epics.md`, linje 357 og 620), så story 1.1 kunne aldri oppfylle regelen. Begge dokumentene er skrevet av Claude med BMAD og godkjent av brukeren. PRD-en krever ikke CI i DR-7.

**Retting.** Brukeren godkjente unntaket D-9 21. november:
- Story 1.1 kan flettes når `uv run pytest`, `uv run ruff check` og `uv run ruff format --check` passerer lokalt på grenens siste commit, og pull requesten nevner beslutningen og resultatene med commiten.
- Den første CI-kjøringen kommer med pull requesten for story 1.2 og kjører alle testene, også testene fra story 1.1. Alle senere stories følger regelen slik den står.
- `epics.md` har fått D-9 og henvisninger i regelen for alle stories, i punkt 5 i rutinen og i sammendraget av «Checks before a pull request». Arkitekturspinen har fått en merknad i AD-17 og i raden «Checks before a pull request». Begge endringsloggene har fått en rad.

**Commit eller pull request:** `fa237e7`.

**KI-styringsloggen:** [tilfelle 27](ki-styringslogg.md#27-regelen-om-ci-og-story-11-21-november-2026).

## 2026-11-21 – Feil i KI-generert kode og tekst fra BMAD Code Review av story 1.1 (DR-9)

**Hvordan det ble funnet.** Brukeren kjørte BMAD Code Review (`bmad-code-review`) på hele grenen for story 1.1 21. november, etter rutinen for code review, med fire uavhengige KI-granskere: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. Claude kontrollerte hvert funn mot koden og kildene, og funn som allerede var vurdert i reviewene av del A og del B, beholdt vurderingen sin. Alle 34 funnene står med vurdering under «Review Findings» i `_bmad-output/implementation-artifacts/spec-1-1-start-prognose-locally-from-a-fresh-clone.md`, og beslutningene står i kommentaren i PR #8. Brukeren bestemte selv tre funn. 21 ble rettet, 2 utsatt og 11 avvist.

**Feilene som ble rettet.** Rettingene i kode og tester ligger i `e36043a`. Rettingene i dokumentene ligger i `bcd8223`.

| Feil | Funnet av | Retting |
|---|---|---|
| Testen av svaret på POST til `/` brukte en testklient uten CSRF-sjekk, så den viste 405, mens en nettleser eller curl får Djangos engelske CSRF-side med 403 | Acceptance Auditor og Blind Hunter; gjenskapt | Testen bruker en klient med CSRF-sjekk og forventer 403 for POST og 405 for OPTIONS. Den norske siden for 403 kommer i story 1.4 |
| Ingen test sikret at `manage.py` og pytest alltid bruker `prognose.settings`, og `wsgi.py` brukte fortsatt `setdefault` | Verification Gap, Blind Hunter og Edge Case Hunter | Tre tester, og `wsgi.py` setter alltid `prognose.settings` |
| Testen av at `.env` ikke endrer `os.environ`, kjørte ikke den ekte leseren | Verification Gap | Testen av den ekte leseren sammenligner `os.environ` før og etter |
| Ingen test sikret at `runserver` som standard bare lytter på 127.0.0.1, port 8000 | Blind Hunter | En ny test |
| Ingen test sikret at git ignorerer `.secret_key` og `.env`, selv om `.gitignore` på designgrenen manglet `.secret_key` 16. november | Verification Gap | Tester med `git check-ignore`, som hoppes over utenfor et git-repo, etter brukerens beslutning |
| Kommentaren i `load_seed` lovet at bare eieren kan lese `.secret_key`, også på Windows, der modusen bare setter skrivebeskyttelse | Edge Case Hunter og Blind Hunter | Kommentaren gjelder macOS og Linux, og story 1.3 sjekker tilgangen på Windows (`issues.md`) |
| En `DATABASE_URL` som er eksportert for et annet prosjekt, går foran uten at noe advarer om det | Blind Hunter | En advarsel i README og `.env.example`, etter brukerens beslutning |
| DR-5 sier at hver test nevner FR-n eller E-n, men de fleste testene i story 1.1 kontrollerer ingen FR | Acceptance Auditor | D-10 i `epics.md`, etter brukerens beslutning |
| QA-loggen hadde et usynlig BOM-tegn i en tabellrad, sa «første story» om testene på Windows, hadde linjenumre som D-9 flyttet, og manglet de bekreftede feilene som ble avvist i del A | Edge Case Hunter, Acceptance Auditor og Blind Hunter | Rettet, og linjenumrene viser nå til en commit |
| KI-styringsloggen sa at story 1.1 ga ingen tilfeller, selv om D-9 retter regler som Claude skrev | Blind Hunter | [Tilfelle 27](ki-styringslogg.md#27-regelen-om-ci-og-story-11-21-november-2026) og [tilfelle 28](ki-styringslogg.md#28-beslutningene-i-bmad-code-review-av-story-11-21-november-2026) i KI-styringsloggen |
| Teksten i PR #8 sa «fire `uv run`-kommandoer», mens README kjører `uv sync --locked` og tre `uv run`, og to commits nevner ikke storyen | Edge Case Hunter og Acceptance Auditor | Teksten er rettet, og kommentaren i PR #8 nevner de to commitene |
| Ingen resultater av testene og Ruff for siste commit var ført | Blind Hunter | De tre kontrollene passerte i en ny klone av `c2a70a6` ([oppføringen om kontrollene](#2026-11-21--testene-og-ruff-i-en-ny-klone-av-story-11-d-9-dr-7)), og de kjøres på nytt på grenens siste commit før flettingen, med resultatet i PR #8 |

**Utsatt.** At databaseporten bare publiseres på 127.0.0.1, sjekkes bare for hånd med `lsof`. En automatisk sjekk av `docker compose config` hører til CI i story 1.2 (`deferred-work.md`). (Løst 21. november i story 1.2: compose-testen sjekker det, og CI kjører den. Se [den første CI-kjøringen](#2026-11-21--første-ci-kjøring-på-linux-story-12-ad-17-ad-1-nfr-2-dr-7-d-1-d-9).)

**Avvist.** 11 funn, med begrunnelse under «Review Findings» i spesifikasjonen og i KI-styringsloggen ([tilfelle 28](ki-styringslogg.md#28-beslutningene-i-bmad-code-review-av-story-11-21-november-2026)).

## 2026-11-21 – Testene og Ruff i en ny klone av story 1.1 (D-9, DR-7)

**Hvorfor.** Etter D-9 kan story 1.1 flettes før CI finnes, når `uv run pytest`, `uv run ruff check` og `uv run ruff format --check` passerer lokalt på grenens siste commit. BMAD Code Review fant at ingen resultater for siste commit var ført (BH-11).

**Oppsett.**
- Claude Code kjørte kontrollene 21. november 2026, etter at brukeren hadde godkjent rettingene fra BMAD Code Review. Ingen person kjørte dem.
- Grenen ble klonet fra GitHub med `git clone --branch story/1-1-start-prognose-locally https://github.com/IBE160-2026/G40-lyamouri.git` til en midlertidig mappe utenfor repoet, og klonen ble slettet etterpå.
- Samme maskin som ved klonetesten: macOS 15.6.1 på Apple M1, med uv 0.12.13 og Python 3.13.15. Testene brukte repoets PostgreSQL 18.7 fra `compose.yaml`, som allerede kjørte, så klonen startet ingen egen database.
- Ingen `DATABASE_URL`, `DJANGO_SETTINGS_MODULE` eller `PROGNOSE_`-variabel var satt i terminalen.

**Resultat.**

| Steg | Resultat | Tid (sekunder) |
|---|---|---|
| `git clone --branch story/1-1-start-prognose-locally` | HEAD var `c2a70a6`, den samme commiten som grenen på GitHub. Koden og testene er de samme som i `e36043a` | 1,1 |
| `uv sync --locked` | fullførte uten feil | 0,2 |
| `uv run pytest` | 82 beståtte tester, ingen hoppet over | 4,9 |
| `uv run ruff check` | «All checks passed!» | 0,4 |
| `uv run ruff format --check` | «22 files already formatted» | under 0,1 |

| Kontroll | Resultat |
|---|---|
| Endrede eller usporede filer rett etter kloningen | ingen |
| Endrede eller usporede filer etter kontrollene | ingen, så det kontrollene lager, for eksempel `.venv`, ignoreres av git |

**Gjenstår.** Senere commits i PR #8 endrer bare dokumenter og logger. Etter D-9 kjøres de tre kontrollene på nytt på grenens siste commit rett før flettingen, og resultatet med den commiten står i PR #8. (Gjort 21. november: kontrollene passerte i en ny klone av `9c8a5dd`, og resultatet står i PR #8. Den første CI-kjøringen kom med PR #10. Se [den første CI-kjøringen](#2026-11-21--første-ci-kjøring-på-linux-story-12-ad-17-ad-1-nfr-2-dr-7-d-1-d-9).)

## 2026-11-21 – Første CI-kjøring på Linux (Story 1.2; AD-17, AD-1, NFR-2, DR-7, D-1, D-9)

**Hvorfor.** Story 1.2 bygger CI med GitHub Actions. Etter D-9 skulle den første CI-kjøringen komme med pull requesten for story 1.2 og kjøre alle testene på Linux, også dem fra story 1.1. Kjøringen er også organisasjonssjekken i D-1. Den skulle dessuten vise at compose-testen kjører i CI. Testen kom fra funnet VG-4 i [BMAD Code Review av story 1.1](#2026-11-21--feil-i-ki-generert-kode-og-tekst-fra-bmad-code-review-av-story-11-dr-9): bare en manuell `lsof` sjekket at databaseporten publiseres på 127.0.0.1.

**Oppsett.**
- Workflowen `.github/workflows/ci.yml` startet på `pull_request` for PR #10, på commit `b2dd344`, 21. november 2026 kl. 22.34 norsk tid (21.34 UTC). Det var kjøring nr. 1 av workflowen, med ID 44952275264: <https://github.com/IBE160-2026/G40-lyamouri/actions/runs/44952275264>. GitHub sletter loggene etter 90 dager som standard, så resultatene står her.
- Runneren var `ubuntu-24.04` med runner 2.338.2. `actions/checkout` v7.0.1 og `astral-sh/setup-uv` v10.3.3 er låst til commit-hash, setup-uv installerte uv 0.12.13, og uv brukte CPython 3.13.15, samme versjon som lokalt.
- Pushen: tokenet i nøkkelringen mangler rettigheten `workflow`, som GitHub krever for filer i `.github/workflows/`, og to forsøk på å gi `gh`-tokenet den med `gh auth refresh` endte med «context deadline exceeded». Brukeren laget derfor en SSH-nøkkel og registrerte den på GitHub, og grenen ble pushet én gang via SSH. Remoten er fortsatt HTTPS.

**Organisasjonssjekken (D-1).** Endepunktene `repos/IBE160-2026/G40-lyamouri/actions/permissions` og `orgs/IBE160-2026/actions/permissions` svarte 403, fordi de krever admin-rettigheter. Etter brukerens beslutning er den første grønne kjøringen bekreftelsen. Kjøringen startet og passerte, så GitHub Actions er slått på for repoet i IBE160-2026, og begge actions er tillatt med disse commit-hashene. Andre actions er ikke prøvd.

**Resultat.**

| Steg | Resultat | Tid (sekunder) |
|---|---|---|
| `actions/checkout` og `astral-sh/setup-uv` | uv 0.12.13 installert | 5 |
| `uv sync --locked` | CPython 3.13.15 og 14 pakker | 1 |
| `docker compose up -d --wait` | `postgres:18.7` hentet, og databasen var klar («Healthy») | 15 |
| `uv run pytest` | 99 tester samlet og bestått på Linux, ingen hoppet over | 3 |
| `uv run ruff check` | «All checks passed!» | under 1 |
| `uv run ruff format --check` | «25 files already formatted» | under 1 |
| Hele kjøringen, med oppsett og opprydding | bestått | 36 |

De 99 testene er de 82 fra story 1.1 og de 17 nye. Ingen ble hoppet over, så compose-testen kjørte og viste at oppsettet i `compose.yaml` bare publiserer databaseporten på 127.0.0.1. Testen leser oppsettet, ikke porten mens databasen kjører.

**Mutasjonsbevis.** Lokalt på macOS, før commit, fikk hver av disse endringene sin test til å feile, og alle ble tilbakestilt:
- `import django` i `src/forecasting/__init__.py`: importtesten (AD-1);
- et nytt felt på `web.Company` uten migrering: `test_migrations_match_the_models` (AD-17);
- `"15432:5432"` i `compose.yaml`: compose-testen (NFR-3, AD-14);
- `if: false` på pytest-steget i workflowen: workflow-testen, som etter BMAD Code Review heter `test_no_check_can_be_skipped_or_ignored` (DR-7).

**Gjenstår.** Tokenet i nøkkelringen mangler fortsatt `workflow`-rettigheten. Derfor må hver push som endrer `.github/workflows/`, også flettingen av PR #10 til `main`, gå via SSH, helt til tokenet får rettigheten (`issues.md`). CI kjører på nytt for hver ny commit på PR #10 og etter flettingen til `main`.

## 2026-11-22 – Feil i KI-generert kode og tekst fra reviewene av story 1.2 (DR-9)

**Hvordan det ble funnet.** Claude Code skrev koden, testene og tekstene i story 1.2 med `bmad-build`. Før første commit gikk byggeøkten selv gjennom diffen med Blind Hunter, Edge Case Hunter og Verification Gap, uten subagenter etter brukerens valg. Matrise-revisjonen i `bmad-build` sjekket i tillegg at hver rad i I/O-matrisen hadde en test som kjørte. 22. november kjørte BMAD Code Review med fire uavhengige KI-granskere på PR #10: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. Claude kontrollerte hvert funn mot koden og gjenskapte feilene der tabellen sier det. Alle funnene står med vurdering under «Review Triage Log» og «Review Findings» i `_bmad-output/implementation-artifacts/spec-1-2-check-every-pull-request-automatically.md`.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Compose-testen leste fila som `COMPOSE_FILE` pekte på, ikke nødvendigvis `compose.yaml` | Blind Hunter og Edge Case Hunter i `bmad-build`; gjenskapt | Testen leste `compose.yaml` med `--file`, og BMAD Code Review endret det igjen (se nedenfor) | `b2dd344` |
| Med `if: false` på pytest-steget passerte alle workflow-testene | Blind Hunter i `bmad-build`; gjenskapt | Testen sjekket `if` og `continue-on-error` på stegene for installasjon, database og pytest | `b2dd344` |
| To rader i I/O-matrisen hadde ingen test som kjørte: compose-testen uten `docker`, og en pytest-feil i CI | Matrise-revisjonen i `bmad-build` | `test_compose_test_is_skipped_without_docker` og `tests/test_ci_workflow.py` | `b2dd344` |
| Compose-testen så ikke oppsettet som `docker compose up` laster: en `compose.override.yaml` som publiserte 5432 på alle adresser, passerte. Testen kjørte også `docker` ved navn etter å ha funnet den med `shutil.which` | Edge Case Hunter og Blind Hunter i BMAD Code Review; gjenskapt | Testen leser oppsettet uten `--file` og uten `COMPOSE_FILE`, slik `up` gjør, og kjører den `docker` den fant | `e24727e` |
| Workflow-testen så bare innstillinger på stegnivå. Disse endringene passerte alle tre testene: `if` eller `continue-on-error` på jobben, en fjernet `pull_request`-trigger, en annen runner, skriverettigheter, `persist-credentials: true`, `env` med `PYTEST_ADDOPTS`, en ekstra action og en ny kommando bare i README | Alle fire granskerne i BMAD Code Review; gjenskapt med mutasjoner | Testen sjekker hele workflow-fila: triggere, runner, rettigheter, actions, `if`, `continue-on-error`, `env` og README «Tester» begge veier | `e24727e` |
| Importtesten godtok database- og nettverksmodulene i standardbiblioteket, som `sqlite3`, `urllib` og `socket` | Verification Gap, Edge Case Hunter og Blind Hunter i BMAD Code Review | Etter brukerens valg avvises modulene i kjernen, med eksempelrader i testen | `e24727e` |
| Alle push til `main` delte én kø, så GitHub kunne avbryte en ventende kjøring | Acceptance Auditor, Edge Case Hunter og Blind Hunter i BMAD Code Review | Etter brukerens valg får hver kjøring utenfor en pull request sin egen gruppe | `e24727e` |
| README lovet bare `passed` selv om en test kan hoppes over, og omtalte fletteregelen som om GitHub håndhevet den | Acceptance Auditor, Blind Hunter og Edge Case Hunter i BMAD Code Review | Teksten er rettet | `e24727e` |
| QA-loggen manglet denne oppføringen og push-begrensningen, forklarte ikke VG-4, viste to oppføringer fra story 1.1 som åpne og hadde en upresis kjøringspost | Acceptance Auditor og Blind Hunter i BMAD Code Review | Rettet i QA-loggen, og push-begrensningen står i `issues.md` | PR #10 |
| PR-teksten sa ikke hvorfor statustabellen er uendret | Acceptance Auditor i BMAD Code Review | PR-teksten er rettet | PR #10 |

**Kjente feil som ikke ble rettet.**

| Feil | Funnet av | Hvorfor den ikke ble rettet |
|---|---|---|
| Dynamiske importer, `importlib.import_module` og `__import__`, passerer importtesten | Blind Hunter i `bmad-build` og Edge Case Hunter i BMAD Code Review | Lite sannsynlig i kjernen, og en sjekk av kall gir en ny gren |
| `docker compose config` kjører uten tidsgrense | Edge Case Hunter i begge reviewene | Kommandoen leser bare filer, og CI stopper jobben etter 15 minutter |
| `network_mode: host` ville gått forbi sjekken av porten | Edge Case Hunter i BMAD Code Review | Lite sannsynlig i dette oppsettet, og rettingen gir en ny sjekk |
| Workflow-testen leser YAML som tekst, så en konstruksjon den ikke ser, for eksempel et anker, kan slippe gjennom | Claude, etter Blind Hunters funn | Ingen avhengighet leser YAML, og review fanger slike endringer |

**Avvist.** De andre funnene fra `bmad-build` er avvist med begrunnelse i spesifikasjonen.

**KI-styringsloggen:** [tilfelle 29](ki-styringslogg.md#29-beslutningene-i-reviewene-av-story-12-22-november-2026).

## 2026-11-22 – Oppstart uten nett på macOS (Story 1.3; NFR-1, SM-2, DR-9)

**Hvorfor.** Story 1.3 skal vise at Prognose starter uten nett etter at det er startet én gang, på macOS og på Windows. Dette er macOS-delen.

**Oppsett.**
- Brukeren kjørte testen to ganger 22. november 2026 i Terminal-appen, med skript som Claude skrev, og slo selv nettet av og på. Skriptene er ikke committet. De registrerte versjonene, stegene og tidene, målte tiden med `date +%s` og gjorde dette:
  - sjekket nettet med `curl` mot github.com, der `000` betyr ingen forbindelse;
  - startet Docker Desktop med `open -a Docker` og spurte `docker info` hvert 2. sekund til det svarte;
  - kjørte `docker compose up -d --wait`;
  - startet `uv run python src/manage.py runserver --insecure`, spurte `http://127.0.0.1:8000/` med `curl` hvert sekund til siden svarte 200, og sjekket at den viste «Prognose».
- Maskinen var macOS 15.6.1 på Apple M1 (arm64), med uv 0.12.13 og Docker Desktop 4.99.0 med Docker Engine 29.9.3. Prognose var startet før, så imaget `postgres:18.7`, Python og pakkene lå lokalt.
- Før nettet ble slått av, ble databasen stoppet med `docker compose down`, som fjerner containeren og beholder volumet. Appen kjørte ikke.

**Kjøring 1, kl. 09.34–09.44 på commit `850250d`.** Brukeren skulle avslutte Docker Desktop og slå av Wi-Fi, men skriptet sjekket ikke at Docker Desktop var avsluttet.

| Steg | Resultat | Tid (sekunder) |
|---|---|---|
| Nettprøve mot github.com | ingen forbindelse (`000`) | under 5 |
| Docker Desktop startet med `open -a Docker` | svarte på `docker info` | 1 |
| `docker compose up -d --wait` | databasen var klar («Healthy») | 5 |
| `uv run python src/manage.py runserver --insecure` | `http://127.0.0.1:8000/` svarte 200 med «Prognose» | 1 |

Docker Desktop svarte så raskt at det trolig ikke var helt avsluttet. Kjøring 1 viser at databasen og appen starter uten nett, men ikke at Docker Desktop selv starter uten nett fra avsluttet tilstand.

**Kjøring 2, kl. 14.56–14.58 på commit `fedaef2`.** Etter BMAD Code Review valgte brukeren å kjøre testen på nytt. Skriptet sjekket først at Terminal finner `docker`, og fortsatte bare når ingen prosess fra Docker Desktop kjørte, `docker info` feilet og nettet ikke svarte. To forsøk stoppet før testen: kl. 11.19 kjørte Docker Desktop fortsatt, og kl. 14.51 fant ikke Terminal-vinduet `docker`.

| Steg | Resultat | Tid (sekunder) |
|---|---|---|
| `command -v docker` i et nytt Terminal-vindu | fant `~/.docker/bin/docker`, slik PATH-rettingen i README gir | – |
| Sjekk av at Docker Desktop var avsluttet | ingen prosess fra Docker Desktop, og `docker info` feilet | – |
| Nettprøve mot github.com | ingen forbindelse (`000`) | under 5 |
| Kald start av Docker Desktop med `open -a Docker` | svarte på `docker info` | 6 |
| `docker compose up -d --wait` | containeren ble laget fra det lokale imaget, og databasen var klar («Healthy») | 4 |
| `uv run python src/manage.py runserver --insecure` | `http://127.0.0.1:8000/` svarte 200 med «Prognose» | 2 |

Kjøring 2 viser at Docker Desktop, databasen og appen starter uten nett på macOS, også når Docker Desktop er helt avsluttet. Valget **System** i Docker Desktop, den andre rettingen for `docker` i README, er ikke prøvd.

**Feil som ble funnet og rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Terminal-appen fant ikke `docker`, fordi Docker Desktop hadde lagt verktøyene i `~/.docker/bin`, som ikke var i PATH. Den som følger README, får da `command not found: docker` allerede ved første kommando, og README nevnte det ikke | Testskriptet i kjøring 1, som brukte `~/.docker/bin/docker` og skrev det i loggen | README forklarer hvordan Terminal finner `docker`: valget **System** i Docker Desktop, eller `~/.docker/bin` i PATH og et nytt Terminal-vindu. Etter BMAD Code Review nevner den også bash. Kjøring 2 fant `docker` på den andre måten | `3363596`, `fedaef2` |

**De tidligere kjøringene på macOS.** Oppsettet 20. november og klonetesten 21. november kjørte Claude Code i sitt eget skall, ikke en person i Terminal-appen (se de oppføringene). De viser derfor ikke om Terminal-appen finner `docker`. Kjøring 1 her ble kjørt av en person i Terminal-appen, og der viste feilen seg ved første kommando.

**Gjenstår.** Ingenting for macOS i story 1.3. Tidtakingen av hele oppsettet, utført av en person, hører til story 4.1 og 4.4. For Windows, se [oppsettet på Windows](#2026-11-22--oppsettet-på-windows-story-13-sm-2-nfr-1-dr-1-d-3).

## 2026-11-22 – Oppsettet på Windows (Story 1.3; SM-2, NFR-1, DR-1, D-3)

**Begrensningen (D-3).** Brukeren opplyste 22. november at ingen programmer kan installeres på Windows x64-PC-en på jobben, og gruppen har ingen annen Windows x64-PC. Om en lånt PC, en PC på skolen eller en virtuell Windows-maskin i skyen kunne vært brukt, er ikke undersøkt (`issues.md`). Etter første akseptkriterium i story 1.3 er oppsettet med Docker Desktop og WSL 2 og oppstarten uten nett derfor ikke testet på Windows, og README og statustabellen sier det.

**Delvis test i GitHub Actions.** Etter brukerens valg kjører `.github/workflows/windows-setup.yml` README-oppsettet uten Docker på GitHubs egen Windows-maskin, i Windows PowerShell. GitHubs Windows-maskiner kan ikke kjøre Linux-containeren fra `compose.yaml`, så testen bruker maskinens egen PostgreSQL i stedet for Docker. Etter BMAD Code Review kjører workflowen for hver pull request som endrer koden (`src/**`), avhengighetene, `.python-version` eller workflowen, og manuelt med `workflow_dispatch`. GitHub sletter loggene etter 90 dager som standard, så resultatene står her.
- Kjøring nr. 1, med ID 45006768015, startet for PR #12 på commit `0eaea95`, 22. november 2026 kl. 10.16 norsk tid (09.16 UTC), og passerte på 40 sekunder: <https://github.com/IBE160-2026/G40-lyamouri/actions/runs/45006768015>. uv brukte da CPython 3.13.17, som allerede lå på maskinen. Kjøring nr. 2 (45007112153, `739d3bd`) hadde samme workflow og passerte på 36 sekunder.
- Kjøring nr. 3, med ID 45009667642, kjørte workflowen slik den ble rettet etter BMAD Code Review, på commit `fedaef2`, kl. 10.52 norsk tid (09.52 UTC): <https://github.com/IBE160-2026/G40-lyamouri/actions/runs/45009667642>. Tabellen gjelder den.
- Maskinen var Microsoft Windows Server 2025 Datacenter 10.0.26100, 64-bit, med runner-imaget `win25-vs2026` 20261116.315.1, Windows PowerShell 5.1.26100.33822, uv 0.12.13 og PostgreSQL 17.12. Workflowen setter `UV_PYTHON_PREFERENCE: only-managed`, så uv lastet ned Python selv, slik README lover for en PC uten Python.

| Steg | Resultat | Tid (sekunder) |
|---|---|---|
| PostgreSQL-tjenesten startet, etter en sjekk av at det finnes nøyaktig én | «accepting connections» | 5 |
| `uv sync --locked` | lastet ned CPython 3.13.15 og installerte 16 pakker | 5 |
| `uv run python src/manage.py migrate` | alle migreringene, også `web.0001_initial` | 4 |
| `uv run python src/manage.py load_seed` | lagde `.secret_key` | 1 |
| `icacls .secret_key` i arbeidsmappa | se under | under 1 |
| En ny klone i brukermappa, `C:\Users\runneradmin\prognose`, med `load_seed` og `icacls .secret_key` | se under; steget feiler hvis `BUILTIN\Users`, `Everyone` eller `Authenticated Users` har tilgang | 18 |
| `uv run python src/manage.py runserver --insecure` | `http://127.0.0.1:8000/` svarte 200 med «Prognose» etter 1 sekund | 2 |
| Hele jobben, med oppsett og opprydding | bestått | 57 |

`icacls` viste dette, med maskinnavnet byttet ut med `<maskin>`. I arbeidsmappa arver fila mappas regler, merket `(I)`, og alle lokale brukere (`BUILTIN\Users`) kan lese den:

```
.secret_key BUILTIN\Administrators:(I)(F)
            NT AUTHORITY\SYSTEM:(I)(F)
            BUILTIN\Users:(I)(RX)
```

I klonen i brukermappa kan bare SYSTEM, administratorene og brukeren lese den. Reglene der er ikke merket `(I)`, altså ikke arvet. Brukeren `runneradmin` er administrator, og brukermappa på GitHubs maskin er ikke nødvendigvis lik den på en vanlig PC:

```
.secret_key NT AUTHORITY\SYSTEM:(F)
            BUILTIN\Administrators:(F)
            <maskin>\runneradmin:(F)
```

Testen viser at uv med nedlastingen av Python, pakkene med `psycopg[binary]`, migreringene, `load_seed` og `runserver` virker på Windows x64, og hvem som kan lese `.secret_key` i en klone i brukermappa. Den viser ikke:
- Docker Desktop med WSL 2, databasen fra `compose.yaml` eller oppstart uten nett;
- oppsettet uten variabler fra README: workflowen setter `DATABASE_URL` til maskinens PostgreSQL 17.12 på port 5432, med brukeren `postgres` og passordet fra `PGPASSWORD`, mens README bruker standardverdien, brukeren `prognose` uten passord på port 15432, med PostgreSQL 18.7 fra `compose.yaml`;
- hvilken adresse `runserver` lytter på (på macOS sjekket med `lsof`);
- testene fra «Tester» i README, `uv run pytest` (`deferred-work.md`);
- tiden for installasjonen av uv og Docker Desktop med WSL 2, eller en person som følger README i et vanlig PowerShell-vindu på en vanlig PC.

**Kjent feil som ikke ble rettet i koden.**

| Feil | Funnet av | Hvorfor den ikke ble rettet |
|---|---|---|
| `load_seed` ber om modusen 600 for `.secret_key`, men på Windows setter modusen bare skrivebeskyttelsen. I arbeidsmappa på GitHubs maskin kunne derfor alle lokale brukere lese nøkkelen | Windows-testen med `icacls` (punktet fra BMAD Code Review av story 1.1, EC-5 og BH-7) | Databasen uten passord er uansett åpen for alle brukere av maskinen, så README sier at Prognose er laget for én bruker per maskin. Den som deler en PC, kloner i brukermappa, der bare SYSTEM, administratorene og brukeren kunne lese nøkkelen i kjøring 3, og `icacls .secret_key` viser hvem som har tilgang (`739d3bd`, `fedaef2`) |

**Observasjon.** I meldingen fra `load_seed` vises «nøkkel» som «n�kkel» i loggen fra GitHub, i kjøring 1 og 3. Der går utdataene gjennom en pipe, og Python skriver da med Windows' tegnsett, mens GitHub leser UTF-8. I et vanlig PowerShell-vindu skriver Python rett til konsollen, og etter Pythons dokumentasjon skal «ø» da vises riktig. Det er ikke prøvd. Sendes utdataene videre i Windows PowerShell 5.1, for eksempel med `> logg.txt`, kan «ø» bli feil også der (`issues.md`).

**Gjenstår.**
- Oppsettet med Docker Desktop og oppstarten uten nett på Windows kan bare testes på en Windows x64-PC der uv og Docker Desktop kan installeres (`issues.md`).
- Tiden for installasjonen av uv og Docker Desktop er ikke målt i story 1.3, verken på macOS eller Windows, så story 4.1 må si i README at den ikke er målt (`issues.md`).
- Story 4.4 kjører Windows-testen med `workflow_dispatch` på siste commit og fører resultatet her (`issues.md`).
- README og arkitekturspinen nevner Windows 10 22H2 og Windows 11 23H2, som Microsoft ikke lenger gir vanlige oppdateringer for. Story 4.1 sjekker hvilke versjoner Docker Desktop 4.99.0 krever (`issues.md`, `deferred-work.md`).

## 2026-11-22 – Feil i KI-generert kode og tekst fra reviewene av story 1.3 (DR-9)

**Hvordan det ble funnet.** Claude Code skrev Windows-workflowen, testskriptene og tekstene i story 1.3 med `bmad-build`. Før reviewen gikk byggeøkten selv gjennom diffen med Blind Hunter, uten subagenter, og fant 3 funn (BH-1 til BH-3 under «Review Triage Log» i `_bmad-output/implementation-artifacts/spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md`). 22. november kjørte BMAD Code Review med fire uavhengige KI-granskere på PR #12: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. De fant 46 funn. Claude kontrollerte hvert funn mot koden, loggene og kjøringene og samlet dem etter felles årsak i 24 punkter: brukeren bestemte 2, 19 ble rettet, 1 utsatt og 2 avvist. Spesifikasjonen har ingen oppgaveliste, så alle funnene og beslutningene står i kommentaren i PR #12.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Workflowen startet PostgreSQL-tjenesten med navnet `postgresql-x64-17`, som endres med neste PostgreSQL i GitHubs image, og med null eller flere tjenester ville starten feilet med en uklar melding | Blind Hunter i `bmad-build` (BH-1), og Blind Hunter og Edge Case Hunter i BMAD Code Review | Workflowen finner tjenesten med `Get-Service postgresql*` og krever nøyaktig én | `fedaef2` |
| Workflowen kjørte bare når den selv endret seg, så en endring i avhengighetene eller koden som bryter oppsettet på Windows, kunne flettes uten test, mens README sa at delen uten Docker er testet automatisk | Blind Hunter i `bmad-build` (BH-2) og alle fire granskerne i BMAD Code Review | Den kjører også for `pyproject.toml` og `uv.lock`, og etter brukerens valg for `src/**` og `.python-version` | `fedaef2` |
| `runserver`-steget prøvde på nytt ved alle feil, så et svar med 500 eller en server som stoppet, ble meldt som manglende svar etter 60 sekunder, og avslutningskoden fra `taskkill` kunne felle et steg som hadde passert | Blind Hunter, Edge Case Hunter og Verification Gap i BMAD Code Review | Steget melder HTTP-statusen eller avslutningskoden til serveren med en gang og nullstiller `$LASTEXITCODE` etter `taskkill` | `fedaef2` |
| Kjøring 1 viste ikke at uv laster ned Python, slik README lover, fordi uv brukte en CPython som lå på maskinen | Blind Hunter i BMAD Code Review | `UV_PYTHON_PREFERENCE: only-managed`, og i kjøring 3 lastet uv ned CPython 3.13.15 | `fedaef2` |
| Ingen test knyttet Windows-workflowen til README, så den kunne fortsette å teste gamle kommandoer | Blind Hunter i BMAD Code Review | `test_the_windows_workflow_runs_the_readme_setup_without_docker` | `fedaef2` |
| `icacls` skrev bare ut tilgangen, og rådet i README om brukermappa var aldri sjekket | Alle fire granskerne i BMAD Code Review | Workflowen kloner i brukermappa og feiler hvis andre brukere kan lese `.secret_key`, og kjøring 3 passerte | `fedaef2` |
| README lovet at bare brukeren, SYSTEM og administratorene kan lese nøkkelen i brukermappa, men databasen uten passord er åpen for alle brukere av maskinen. README nevnte heller ikke bash, et nytt PowerShell-vindu etter installasjonen eller hvor brukermappa er | Blind Hunter og Edge Case Hunter i BMAD Code Review | README sier at Prognose er laget for én bruker per maskin, og nevner resten | `fedaef2` |
| README og QA-loggen sa at oppstarten uten nett var testet, men Docker Desktop var trolig ikke avsluttet, og PATH-rettingen for `docker` var ikke prøvd | Blind Hunter, Edge Case Hunter og Acceptance Auditor i BMAD Code Review | Etter brukerens valg ble testen kjørt på nytt med Docker Desktop helt avsluttet, og README sier hva som er testet på hver plattform | PR #12 |
| QA-loggen førte en kjøring av en eldre workflow og manglet runner-imaget, utskriften fra `icacls`, forskjellene fra README-oppsettet og at GitHub sletter loggene. Den viste til Windows-testen 25. november, sa ikke at tiden for installasjonen ikke er målt, og omtalte «ø» i PowerShell som om det var prøvd | Alle fire granskerne i BMAD Code Review | Kjøring 3 av den rettede workflowen er ført med det som manglet, og resten er rettet her og i arbeidsloggen. De åpne punktene står i `issues.md` | PR #12 |
| Arkitekturspinen og statustabellen var ikke oppdatert for den nye workflowen og begrensningen på Windows, QA-loggen sa ikke hva som ble vurdert som en annen Windows-PC, og KI-styringsloggen manglet et tilfelle for story 1.3 | Acceptance Auditor og Blind Hunter i BMAD Code Review | Rettet, med en rad i endringsloggen til spinen og [tilfelle 30](ki-styringslogg.md#30-windows-testen-og-reviewene-av-story-13-22-november-2026) | PR #12 |

**Kjente feil som ikke ble rettet.**

| Feil | Funnet av | Hvorfor den ikke ble rettet |
|---|---|---|
| Testene i «Tester», `uv run pytest`, kjører ikke på Windows | Blind Hunter i `bmad-build` (BH-3) | Utenfor kriteriene i story 1.3, som gjelder oppsettet og oppstarten (`deferred-work.md`) |
| README og arkitekturspinen nevner Windows 10 22H2 og Windows 11 23H2, som Microsoft ikke lenger gir vanlige oppdateringer for | Blind Hunter i BMAD Code Review | Versjonene kom fra PRD-en og spinen før story 1.3, og en endring av plattformkravet trenger godkjenning. Story 4.1 sjekker kravene til Docker Desktop 4.99.0 (`deferred-work.md`, `issues.md`) |
| `load_seed` begrenser ikke hvem som kan lese `.secret_key` på Windows | Windows-testen | Se [oppsettet på Windows](#2026-11-22--oppsettet-på-windows-story-13-sm-2-nfr-1-dr-1-d-3) |

**Avvist.** En klone som flyttes inn i brukermappa, kan beholde de gamle tilgangsreglene, men README ber deg klone der, og det er sjeldent. At README ikke lenger sier at Intel-Mac er utestet, stemmer ikke: README nevner bare Apple M1 som testet.

**KI-styringsloggen:** [tilfelle 30](ki-styringslogg.md#30-windows-testen-og-reviewene-av-story-13-22-november-2026).

## 2026-11-22 – App-skallet og feilsidene i runserver og Safari (Story 1.4; NFR-6, NFR-10, AD-12, UX-DR7)

**Hvorfor.** Hver side en story endrer eller legger til, skal sjekkes i nettleserens responsive visning ved 320 px, 390 × 844 (iPhone 13) og 820 × 1180 (iPad), og pull requesten skal nevne sjekkene (reglene for hver story i `epics.md`; NFR-6, UX-DR7). Story 1.4 ga startsiden app-skallet og la til feilsidene, som alle bruker det samme panelet. Testklienten i Django viser ikke alt en ekte server sender, så Claude sjekket også svarene gjennom runserver.

**Oppsett.**
- Claude startet appen med `uv run python src/manage.py runserver --insecure` på grenen `story/1-4-app-shell-and-error-pages`, med DEBUG av, og spurte med `curl`. Koden er den samme som i den første commiten i PR #14.
- Brukeren sjekket selv `/` og `/finnes-ikke/` i den responsive visningen i Safari 22. november 2026, på samme Mac som i story 1.1, og etter BMAD Code Review også fokusringen. Brukeren leste versjonene for hånd samme dag: Safari 18.6 og macOS 15.6.

**Resultat med runserver.**

| Forespørsel | Svar |
|---|---|
| `GET /` | 200 med app-skallet |
| `GET /finnes-ikke/` | 404 med «Siden finnes ikke» og lenken «Til produktoversikten»; `Content-Length` stemmer med innholdet |
| `GET /static/web/app.css` | 200 med `text/css`, også med DEBUG av |
| En statisk fil som ikke finnes | 404 med den norske siden |
| `OPTIONS /` | 405 med Server error-siden. Først var `Content-Length` 0 og siden tom (se feilene under); etter rettingen 717 byte med riktig lengde |
| `DELETE /` | 403 med siden for utløpt skjema, fordi CSRF-sjekken kommer før sjekken av metoden |
| Konsollen | Forespørselslinjene fra runserver som før, og nå også advarslene «Not Found» og «Forbidden (CSRF cookie not set.)» med DEBUG av |

**Resultat i Safari.** Begge sidene var i orden ved alle tre størrelsene.

| Tilsvarer | Størrelse | `/` og `/finnes-ikke/` |
|---|---|---|
| Den minste bredden i NFR-6 | 320 px bred | ingen avkuttet tekst, overlapp eller sidelengs rulling |
| iPhone 13 | 390 × 844 | ingen avkuttet tekst, overlapp eller sidelengs rulling |
| iPad | 820 × 1180 | ingen avkuttet tekst, overlapp eller sidelengs rulling |

Safari ba også selv om `/apple-touch-icon.png` og `/apple-touch-icon-precomposed.png`. Begge ga 404 og en linje «Not Found» i konsollen, men det påvirker ikke sidene.

**Fokusringen.** Den første sjekken nevnte ikke fokusringen, og BMAD Code Review påpekte det (BH-20). Brukeren åpnet derfor `/finnes-ikke/` på nytt, trykket ⌥Tab og godkjente den blå ringen rundt lenken «Til produktoversikten». I Safari flytter Tab bare til lenker med ⌥Tab eller med innstillingen «Press Tab to highlight each item on a webpage».

**Gjenstår.**
- Pull requesten for story 1.4 skal nevne de tre størrelsene. (Gjort i PR #14.)
- 503-siden kan ikke sjekkes for hånd før story 1.8, fordi ingen side leser databasen ennå. Testene dekker den, og story 1.8 tester den med en innlogget bruker.
- Berøringsreglene og testen på en ekte iPhone 13 hører til story 1.8 (NFR-6).

## 2026-11-22 – Feil i KI-generert kode og tekst fra byggingen og reviewene av story 1.4 (DR-9)

**Hvordan det ble funnet.** Claude Code skrev stilarket, malene, mellomvaren, loggoppsettet og testene i story 1.4 med `bmad-build`. Claude fant den første feilen da storyen ble planlagt, ved å lese koden i Django 5.2.19. To feil fant Claude under byggingen: én ved å lese hvordan Python setter opp loggingen, og én med `curl` mot runserver da oppgavene ble kontrollert. Testklienten i Django sjekker ikke `Content-Length`, så ingen test fanget den. Deretter gikk byggeøkten selv gjennom diffen med Blind Hunter, uten subagenter, og fant 10 funn (BH-1 til BH-10 under «Review Triage Log» i `_bmad-output/implementation-artifacts/spec-1-4-norwegian-app-shell-and-error-pages.md`): 2 ble rettet og 8 avvist. 22. november kjørte BMAD Code Review med fire uavhengige KI-granskere på PR #14: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. Bruksgrensen stoppet alle fire én gang, og hver fortsatte fra arbeidet som var lagret. De fant 35 funn. Claude kontrollerte hvert funn mot koden og kildekoden til Django og samlet dem etter felles årsak: brukeren bestemte 1, 23 funn ble rettet i 15 punkter, 2 ble utsatt og 9 avvist. Alle står under «Review Findings» i spesifikasjonen og i kommentaren i PR #14.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| AD-12 i arkitekturspinen sier at 503-håndteringen sitter i den ytterste mellomvaren, men Django gjør om et unntak til et svar i laget der det oppstår, så en `try/except` der ville aldri sett databasefeilen, og en stoppet database ville gitt 500-siden | Claude, da storyen ble planlagt | Signalet `got_request_exception` merker forespørselen, og `ErrorPageMiddleware`, den første i `MIDDLEWARE`, viser 503-siden. Kravet og spinen er uendret ([tilfelle 31](ki-styringslogg.md#31-503-siden-og-den-ytterste-mellomvaren-22-november-2026)) | `9ae95fc` |
| Spesifikasjonen ba om å sette opp loggeren `django`, men da nullstiller Python barneloggeren `django.server`, og runserver ville sluttet å skrive forespørslene | Claude, under byggingen | `LOGGING` setter opp `django.request` og `django.security` i stedet, og runserver skriver forespørslene som før | `9ae95fc` |
| 405-svaret hadde `Content-Length: 0` etter at mellomvaren hadde lagt inn feilsiden, fordi `CommonMiddleware` hadde satt lengden for det tomme svaret, så nettleseren ville vist en blank side | Claude, med `curl` mot runserver | Mellomvaren setter lengden etter den nye siden og beholder de andre hodene, også på 503-siden. Testene sjekker at `Content-Length` stemmer | `9ae95fc` |
| Raden «Server error» i I/O-matrisen var delt mellom to tester | Claude, i kontrollen av matrisen | Én test dekker både siden og loggen | `9ae95fc` |
| Testen for `var()` sjekket ikke kortformen `font` | Blind Hunter i `bmad-build` (BH-4) | `font` er med blant egenskapene som sjekkes | `9ae95fc` |
| En test sjekket den ytterste mellomvaren etter at innstillingene var endret, så den så ut til å sjekke feil liste | Blind Hunter i `bmad-build` (BH-8) | Sjekken står før endringen | `9ae95fc` |
| Med DEBUG på ble 503-siden sendt som ren tekst til en forespørsel som ikke godtar HTML, fordi mellomvaren beholdt `Content-Type` fra feilsøkingssiden i Django | Blind Hunter og Edge Case Hunter i BMAD Code Review (BH-13, EC-2) | Mellomvaren setter `Content-Type: text/html; charset=utf-8`, og en ny test sjekker 503-siden med DEBUG på | `5063f67` |
| Testene av stilarket slapp gjennom en token som ble gitt en annen verdi i en annen regel eller i `@media`, `var()` med reserveverdi, radier skrevet som enkeltegenskaper, `outline: 0px` og andre måter å fjerne fokusringen på, `URL(` og `@IMPORT` med store bokstaver og en ny egenskap i en typografirolle | Blind Hunter, Edge Case Hunter og Acceptance Auditor i BMAD Code Review (BH-16, EC-9 til EC-14, AA-7) | Testene sjekker alt dette, og seks nye mutasjoner viser at rettingene virker | `5063f67` |
| Testen av loggen så bare etter `postgresql://`, ikke etter `postgres://`, innholdet i forespørselen eller passordet til databasen | Blind Hunter, Edge Case Hunter og Acceptance Auditor i BMAD Code Review (BH-15, EC-15, AA-6) | Testen ser etter alt dette | `5063f67` |
| Ingen test sjekket at `django.server` beholder handleren sin, at de to loggerne ikke sender postene videre, eller at en advarsel som «Not Found» når konsollen | Verification Gap i BMAD Code Review (VG-1, VG-2) | To tester sjekker det | `5063f67` |
| Testene nevnte ikke alle krav-ID-ene de sjekker: UX-DR13, NFR-5 og UX-DR41 for feilsidene, og UX-DR2, UX-DR3 og UX-DR7 for app-skallet | Blind Hunter og Acceptance Auditor i BMAD Code Review (BH-19, AA-1, AA-4) | ID-ene står i testene | `5063f67` |
| Kommentaren om berøringsreglene nevnte bare radioknapper og bryteren, mens regelen unntar alle avkrysningsbokser | Acceptance Auditor i BMAD Code Review (AA-5) | Kommentaren nevner avkrysningsboksene, og storyene som legger dem til, får et åpent punkt | `5063f67` |
| Fokusringen var ikke sjekket for hånd, og versjonene av Safari og macOS var overført fra story 1.1 | Blind Hunter i BMAD Code Review (BH-20) | Brukeren sjekket ringen og leste versjonene, se oppføringen om runserver og Safari over | `b37c3b3` |
| Loggene viste bare til PR #14, ikke til commiten, og arbeidsloggen sa at storyen ventet på sin første commit | Blind Hunter i BMAD Code Review (BH-17) | Commitene står i loggene, og statusen er rettet | `b37c3b3` |

**Kjente feil som ikke ble rettet.**

| Feil | Funnet av | Hvorfor den ikke ble rettet |
|---|---|---|
| Berøringsreglene gjelder bare når berøring er hovedinngangen (`pointer: coarse`), så en PC med berøringsskjerm der musen er hovedinngangen, beholder PC-størrelsene | Blind Hunter i `bmad-build` (BH-1) | Brukeren valgte å beholde `pointer: coarse`: telefonene og iPad-ene i NFR-6 får reglene, og PC-er beholder den kompakte visningen som FR-25 trenger ved 1366 × 768 |
| En økt som er lest og endret, og som ikke kan lagres etter visningen, gir Server error-siden (400) i stedet for 503 | Blind Hunter i `bmad-build` (BH-3) | Det skjer bare hvis databasen stopper mellom lesingen og lagringen i samme forespørsel, og Django gjør om feilen før noen krok kan se den |
| Lenken «Til produktoversikten» gir 404-siden til story 1.8 lager `/produkter/` | Blind Hunter i `bmad-build` (BH-6) | Adressen kommer fra URL-kartet i AD-11, som spesifikasjonen bestemmer. Story 1.8 bytter til `{% url %}` (`issues.md`) |
| «Last siden på nytt og prøv igjen.» etter en POST: å laste siden på nytt sender det gamle skjemaet på nytt | Blind Hunter i `bmad-build` (BH-10) | Teksten er ordrett fra meldingskatalogen, slik storyen krever. Story 4.2 kan endre den (`issues.md`) |
| Den blå fokusringen får om lag 2,4:1 mot det marineblå toppfeltet, under 3:1 i WCAG 1.4.11 | Blind Hunter i BMAD Code Review (BH-12) | Toppfeltet har ingenting som kan få fokus før story 1.8, og fargen krever en designbeslutning, fordi `DESIGN.md` ikke har noen fokusfarge for toppfeltet (`deferred-work.md`, `issues.md`) |
| Databasen har ikke noe tidsavbrudd ved tilkobling, så en database som tar imot tilkoblingen uten å svare, holder forespørselen i opptil 130 sekunder | Edge Case Hunter i BMAD Code Review (EC-6) | Innstillingen kommer fra story 1.1 og står i `env.py`, som story 1.4 ikke endrer (`deferred-work.md`) |
| En vranglås eller en avbrutt spørring gir også 503-siden, selv om databasen kjører | Edge Case Hunter i BMAD Code Review (EC-4) | Det er lite sannsynlig med én lokal bruker, og å skille feilene fra hverandre krever SQLSTATE-koder |
| Konsollen skriver «Internal Server Error» for en databasefeil som gir 503 | Edge Case Hunter og Verification Gap i BMAD Code Review (EC-5, VG-3) | Tracebacken viser databasefeilen, og en retting krever et privat flagg i Django eller en ekstra logglinje |

**Avvist.** Ingen visning sender andre tomme feilsvar enn 405 (BH-2). Fargesjekken fanger heksverdiene, som er den reelle risikoen, men av fargenavnene bare `white` og `black` (BH-5). At 503-siden også vises med DEBUG på, er med vilje, fordi tracebacken står i konsollen (BH-7). Stien til UX-mappa står i begge testfilene, men flyttes mappa, feiler begge (BH-9). I BMAD Code Review ble også disse avvist: ingen 405 eller merket svar strømmes (EC-1), AD-12 gir alle 405-svar den norske siden (EC-3), designet bruker bare h1 til h3 (EC-7), spinen knytter loggreglene til NFR-4 (AA-3), og en review endrer ikke spesifikasjonen den gjennomgår (BH-18, EC-8).

**Åpne punkter.** De åpne punktene som denne oppføringen viser til, står i `issues.md` fra [sesjonsloggen for story 1.4](../.logs/mounia-03/980-2026-11-22-19-51-47-story-1-4-app-skall-og-feilsider.md), og den maskerte eksporten av økten ligger i `.logs/mounia-03/sessions/1-4-2026-11-22.txt` (BH-11, AA-2).

**KI-styringsloggen:** [tilfelle 31](ki-styringslogg.md#31-503-siden-og-den-ytterste-mellomvaren-22-november-2026).

## 2026-11-23 – Kontrollen av referanseregnearket (Story 1.5; DR-3, AD-17, DR-9)

**Hvorfor.** Story 1.5 krever at hvert forventet resultat i referanseregnearket regnes ut på nytt, for hånd eller med synlige formler, og at regnearket fører kontrollen med dato. Et avvik fra PRD §5.7 skal regnes ut på nytt for hånd, og den siden som var feil, skal rettes og føres her (AD-17, DR-9).

**Oppsett.**
- Claude Code tastet inn de forventede verdiene fra PRD §5.7 og regnet ut FR-21-variantene og regeltestproduktene for hånd. Regnearket [`reference/reference-examples.xlsx`](../reference/reference-examples.xlsx) ble skrevet med openpyxl fra et skript i den midlertidige mappa. Skriptet er ikke committet, fordi regnearket er den eneste fasiten (AD-17).
- Det samme skriptet regnet ut hvert tilfelle og hvert produkt på nytt med en egen utregning av R-1 til R-17, uavhengig av verdiene fra PRD-en. Det regnet også ut de 376 kontrollformlene i arket `checks` med avrundingen i Excel.
- Skriptet sjekket at Strøsand 25 kg får de utsolgte ukene 38 og 39 og den uvanlige uka 42 når siste registrerte uke er uke 45 i 2026, som i mockupen.
- Brukeren åpnet regnearket i Excel for Mac 16.78 (23100802) 23. november 2026, leste sammendraget i arket `checks` (cellene K1 til K3) og lukket det uten å lagre. Excel regnet da ut alle formlene selv. Kontrollen står i arket `check_log`.

**Resultat.**

| Kontroll | Resultat |
|---|---|
| Verdiene fra PRD §5.7 mot den uavhengige utregningen | ingen avvik i de 48 tilfellene fra §5.7 (E12 ble først ført som avvik i BMAD Code Review, se under) |
| FR-21-variantene og regeltestproduktene mot den uavhengige utregningen | ingen avvik |
| Kontrollformlene i `checks`, regnet ut med avrundingen i Excel | 376 av 376 stemmer |
| Brukerens kontroll i Excel for Mac 16.78 | K1 = 376 kontroller som stemmer, K2 = 376 kontroller, K3 = SANN |
| 21 feil lagt inn i regnearket og PRD-en, én om gangen | testene fanget alle |

Etter kontrollen ble regnearket skrevet på nytt med brukerens rad i `check_log`. Fila brukeren kontrollerte, hadde SHA-1 `c019e309f3a84b4564822beeeeadecb32fe4e7ab` både før og etter at den var åpen i Excel. Claude sammenlignet den med den nye fila celle for celle med openpyxl: arkene `about`, `cases`, `products` og `checks` var identiske, og `check_log` hadde fått én rad. Regnearket, leseren og testene er committet i `0ae5920`.

**Etter BMAD Code Review.** Rettingene endret arket `checks`: hver liste med uker fikk en rad «other», R-11 fikk egne formler, og varslene viser til radene. PRD-en fikk også rettet E12 (se under). Claude regnet ut alle 401 kontrollene på nytt med det uavhengige skriptet og avrundingen i Excel: alle stemmer, og ingen verdi avviker fra PRD §5.7. 50 feil som ble lagt inn i regnearket og PRD-en én om gangen, ble alle fanget av testene: de 21 fra byggingen og 29 nye fra reviewen.

**Brukerens andre kontroll.** Brukeren åpnet den nye versjonen i Excel for Mac 16.78 (23100802) 23. november 2026 og lukket den uten å lagre. Versjonen hadde SHA-1 `fa2e7b57076836b360aae3eb216c17bd2af18f98`, både før og etter at den var åpen. Sammendraget i `checks` viste K1 = 401 kontroller som stemmer, K2 = 401 kontroller og K3 = SANN. Etter kontrollen ble regnearket skrevet på nytt med brukerens rad i `check_log`. Claude sammenlignet celle for celle med openpyxl: de fire andre arkene var identiske med versjonen brukeren kontrollerte.

**Funn som ikke er en feil.** R-17 (bør-ha) gir Strøsand 25 kg indeksen 1,5735 for ukenummer 42 på grunn av den uvanlige uka. Når FR-36 bygges, får produktet derfor et varsel om sesongmønster som mockupen ikke viser. Story 5.2 avgjør det (`issues.md`).

## 2026-11-23 – Feil i KI-generert kode og tekst fra byggingen av story 1.5 (DR-9)

**Hvordan det ble funnet.** Claude Code skrev regnearket, kontrollformlene, leseren og testene i story 1.5 med `bmad-build`. Skriptet som skrev regnearket, sammenlignet hver kontrollformel med verdien i fasiten før fila ble skrevet. Deretter gikk byggeøkten selv gjennom diffen med Blind Hunter, uten subagenter, og fant 13 funn (BH-1 til BH-13): 4 ble rettet i 3 punkter og 9 avvist.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Kontrollformlene for varslene om utsolgte uker, uvanlige uker og nytt nivå de siste 12 ukene sammenlignet den siste slike uka med «N − 12». Var historikken kortere enn 12 uker og produktet hadde ingen slik uke, ble formelen sann, og 33 kontroller ga feil svar | Sammenligningen i skriptet, før regnearket ble skrevet | Formlene sammenligner med den første uka i perioden, `MAX(1; N − 11)`, og alle 376 kontrollene stemmer | `0ae5920` |
| `reference/README.md` sa ikke at openpyxl ikke flytter referansene i formlene når rader settes inn eller slettes, og at testene ikke regner ut formlene. En senere endring kunne dermed gitt formler som viser til feil rad, uten at noen test feilet | Blind Hunter i `bmad-build` (BH-1) | README-en sier at nye rader legges til slutt i `checks`, og at sammendraget leses i Excel eller Numbers etter hver endring | `0ae5920` |
| README-en forklarte ikke hva `recorded` er for visningstekst og for uker og varsler, og sa uten å ha sjekket det at Numbers viser funksjonsnavnene på programmets språk | Blind Hunter i `bmad-build` (BH-6, BH-13) | README-en forklarer begge, og setningen nevner bare Excel | `0ae5920` |
| Testen for lokale stier så ikke etter `/home/` | Blind Hunter i `bmad-build` (BH-4) | `/home/` er med i mønsteret | `0ae5920` |

**Avvist.** Blind Hunter fant 13 funn, og 9 ble avvist:
- **BH-2:** Testene regner ikke ut formlene, men skriptet regnet dem ut før fila ble skrevet, og kontrollen i Excel leser resultatet.
- **BH-3:** Grensene for innstillingene i FR-20 defineres én gang i `forecasting/settings.py` i story 1.7, og testen bør sjekke dem derfra. Det er et åpent punkt for story 1.7.
- **BH-5:** gir en høylytt feil som stopper testene.
- **BH-7:** handler om tall som beskriver tilstanden da kontrollen ble gjort.
- **BH-8 og BH-9:** stemte ikke.
- **BH-10:** ville bare endret spesifikasjonen.
- **BH-11:** gjelder standardverdiene, som kommer fra PRD-en.
- **BH-12:** gjelder et importvalg som prosjektet ikke bruker.

Alle funnene står under «Review Triage Log» i [spesifikasjonen for story 1.5](../_bmad-output/implementation-artifacts/spec-1-5-reference-spreadsheet-as-the-answer-key.md).

## 2026-11-23 – Feil i KI-generert kode og tekst fra BMAD Code Review av story 1.5 (DR-9)

**Hvordan det ble funnet.** Fire uavhengige KI-granskere i `bmad-code-review` gikk gjennom PR #16: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. De så diffen fra `da87fd7` til `99b73bc` og en tekstutgave av regnearket. De fant 61 funn, og funn med samme årsak ble samlet i punkter:
- 3 beslutninger, som brukeren tok;
- 21 rettinger;
- 2 utsatte punkter;
- 5 avviste funn.

Alle står under «Review Findings» i spesifikasjonen. Rettingene i regnearket, testene, leseren og PRD-en er committet i `dd4a269`.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting |
|---|---|---|
| Ingen test sammenlignet seriene, innstillingene og lagerbeholdningen med PRD-en, og formlene i `checks` bruker innskrevne tall. For eksempel passerte både testene og Excel-kontrollen hvis E20 fikk serien «10, 10, 10, 12» eller E8-produktet lager 40 i stedet for 50 | AA-1, VG-1, BH-17, BH-18 og EC-26 | Brukeren valgte nye tester uten å endre formlene. Testene sammenligner hver serie og innstillingene og lageret som PRD-teksten oppgir, med PRD §5.7. De sammenligner også produktene med alle tilfellene i eksempelet sitt, Strøsand 25 kg med tabellen i mockupen og tallene i kontrollformlene med inndataene |
| E12 (96) hadde varselet om utsolgte uker, mens PRD §5.7 sa «8 weeks: no warning». Uke 97–104 må være utsolgte, så det var PRD-en som var upresis: eksempelet tester bare varselet om gamle data | AA-2 | Brukeren godkjente å rette PRD-en til «no old-data warning», med en rad i PRD §12. Regnearket siterer den nye teksten |
| Ikke alle beslutningene etter R-10 og R-11 hadde en kontrollert formel. Uka etter de uvanlige ukene i E8, E15 og E19 hadde ingen sjekk, så en uvanlig uke som manglet i lista, slapp gjennom. Radene som holdt en uke uvanlig, kopierte bare R-10-flagget, og varslene brukte innskrevne uker | AA-5, BH-19, EC-23, EC-27 og VG-5 | Hver liste med uker har en rad «other», R-11 har egne formler, og varslene viser til radene. Arbeidsboka ble skrevet på nytt og kontrollert igjen |
| En innstilling kunne mangle eller stå som «none», og et må-ha-tilfelle kunne ha varselet om sesongmønster | AA-4, VG-2, BH-21, EC-1, EC-13 og EC-16 | Alle ni innstillingene må stå i hvert tilfelle, «none» avvises for inndata, og `seasonal_pattern` står bare i bør-ha-tilfeller |
| Testen sjekket ikke innstillingen som en FR-21-variant endrer, og godtok varianter som PRD-en ikke har | VG-2, EC-9 og EC-10 | Variantene må være nøyaktig dem PRD-en har. Hver variant har den nye verdien, og ellers samme serie og innstillinger som eksempelet |
| En variant, E18 b-produktet eller Strøsand 25 kg kunne forsvinne uten at noen test feilet | BH-20, EC-8, EC-11 og EC-12 | Testene krever begge variantene av hvert eksempel, hvert bokstavtilfelle i FR-3 og demoproduktet |
| Lista i FR-3 kunne bli tom hvis PRD-en skrev den annerledes | VG-4, BH-22 og EC-7 | Lista leses strengt og kan ikke være tom |
| Ingen test knyttet `match` og sammendraget K1–K3 til raden sin, så `=TRUE` eller en slettet rad kunne blinde Excel-kontrollen | VG-3, BH-28 og EC-22 | Testene sjekker formelen i hver match-celle og de tre formlene i sammendraget |
| Feil i skjemaet sa ikke hvilken celle det gjaldt, og leseren så ikke etter formler utenfor kolonnene i overskriften | AA-3, AA-7, BH-26, EC-4 og EC-5 | Feilen nevner arket og cellen, og hele raden sjekkes for formler |
| Testen for NFR-4 sjekket ikke navnet på den som sist lagret fila | BH-27 og EC-25 | Testen krever `G40-lyamouri` som oppretter og ingen `lastModifiedBy` |
| Mindre hull i testene: uker i feil rekkefølge, gjentatte uker, uker som er utsolgte, gjentatte varsler, visningstekst som «14.3», en siste rad i `check_log` som ikke dekker kontrollene, en periode ført som FALSE, en fast sti i leseren, prioriteten «(Could)» og én test for to rader i matrisen | EC-2, EC-6, EC-14, EC-15, EC-20, EC-21, EC-24, BH-24 og AA-10 | Hver er rettet i testene eller leseren |
| Dokumentene hadde tre feil: «52 tilfellene» for raden om §5.7, grunnene for BH-10 til BH-12 og «Rad 1 i hvert ark». I tillegg manglet kolonnene `note` og `check_log` i README-en, arbeidsloggen manglet statuslinjen, og det var ikke skrevet ned at fila som ble committet, er den som ble kontrollert | BH-15, BH-16, AA-8, AA-9 og BH-29 | Rettet i QA-loggen, README-en og arbeidsloggen |
| `issues.md` manglet de åpne punktene som loggene viser til | AA-6 og BH-14 | Føres med sesjonsloggen før flettingen |

**Utsatt.**
- **Story 1.6 (BH-31):** den eneste leseren av notasjonen ligger i `tests/`, og story 1.6 bestemmer hvor den felles leseren skal ligge.
- **Story 5.1 (BH-23):** ukeprognosene for E14 uten sesongjustering er ikke ført, og story 5.1 fører dem.

Begge står i `deferred-work.md`.

**Avvist.**
- **BH-30:** ankeret uke 45 i 2026 står i README-en.
- **EC-17:** «none» i en tall-liste gir en høylytt feil.
- **EC-3, EC-18 og EC-19:** overskrifter og kontrollrader endres ikke for hånd, og Excel-kontrollen viser en 1 i stedet for TRUE.

## 2026-11-23 – Feil i KI-generert kode og tekst fra byggingen av story 1.6 (DR-9)

**Hvordan det ble funnet.** Claude Code skrev generatoren, testene og dokumentene i story 1.6 med `bmad-build`. Et uavhengig skript for R-1 til R-16 (ikke committet) regnet ut begge seed-filene før de ble committet, og testene i `tests/test_seed_data.py` ble kjørt mot dem. Deretter gikk byggeøkten selv gjennom diffen med Blind Hunter, uten subagenter, og fant 10 funn (BH-1 til BH-10): 6 ble rettet og 4 avvist.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Saltet «prognoseSeedA» hadde 13 tegn. Django godtar et salt først fra 22 tegn, så første innlogging ville ha skrevet hashen om med et tilfeldig salt, og det faste saltet ville ikke holdt | `must_update` i testen av hashene | Saltene har 24 tegn («prognoseSeedTestbedriftA» og «…B») | `1dff8db` |
| Testen for nytt nivå sammenlignet hver uke med de tre foregående ukene, også de uvanlige, så den overså Skruer | Testen av mønstrene | Testen bruker grunnlinjen før den første av de tre ukene | `1dff8db` |
| Windows med `core.autocrlf` ville ha sjekket seed-filene ut med CRLF, så testen som sammenligner byte for byte feilet hos en sensor på Windows | Blind Hunter i `bmad-build` (BH-3) | `.gitattributes` holder JSON-filene med LF, og en test leser den | `1dff8db` |
| `patches` og `tail` kunne treffe feil uke med en negativ indeks, `validate` godtok negativt lager, en konstant var ubrukt, feilmeldingen brukte ordet «frø», og importen av leseren var uten forklaring | Blind Hunter i `bmad-build` (BH-1, BH-2, BH-4 til BH-6) | Begge gir feil, lageret sjekkes, konstanten er slettet, og meldingen og kommentaren er rettet | `1dff8db` |

**Avvist.** BH-7 til BH-10: hash-testen er varsellampen når Django endrer standarden, mønstertestene er med vilje enklere enn reglene, parserne feiler høylytt, og `data` på stien skygger ingen moduler. De står under «Review Triage Log» i [spesifikasjonen for story 1.6](../_bmad-output/implementation-artifacts/spec-1-6-generate-the-synthetic-seed-data.md).

## 2026-11-23 – Feil i KI-generert kode og tekst fra BMAD Code Review av story 1.6 (DR-9)

**Hvordan det ble funnet.** Fire uavhengige KI-granskere i `bmad-code-review` gikk gjennom PR #18: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. De så diffen fra `main` til `1dff8db`, uten seed-filene og spesifikasjonen. De fant 42 funn: 9 med middels alvor og 33 med lavt, ingen høye. 26 ble rettet, 5 ble beslutninger som brukeren tok, og 11 ble avvist. CI og Windows-testen passerte på `1dff8db` før reviewen.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Skruer (10004) og Gjerdestolpe (20014) hadde en uke på 9 midt i det nye nivået (21, 22, 21, 9, 22, 21, 21). Reglene ble ikke brutt, men serien så feil ut for den som leste grafen | VG-3 og AA-6 | Uka er satt til 22. Halen og dermed prognosene og forslagene er uendret | `ecbf55d` |
| Generatoren hoppet stille over regnearkprodukter som ingen bedrift plasserer, og beholdt den siste av to rader med samme produkt. En rad uten bedrift, salg eller lager ga en rå `KeyError` | BH-3, EC-2 og EC-3 | Alle tre gir en feil med navnet på produktet, og ingenting skrives | `ecbf55d` |
| `validate` sammenlignet ikke siste uke med den konfigurerte, og sjekket ikke tomme eller gjentatte navn, kundenumre eller tom serie | BH-4, EC-4 og AA-4 | Alle er med, og testene dekker grenene i `validate` og `series_of` (VG-6) | `ecbf55d` |
| Testen for personvern skannet også base64-hashen, så `+47` eller åtte sifre kunne treffe ved en tilfeldighet etter en ny generering | BH-6, EC-11 og AA-8 | Hashen hoppes over i skanningen | `ecbf55d` |
| De to filene ble skrevet én og én, så en feil på den andre kunne etterlate et halvt par | BH-14 og EC-6 | Begge tekstene lages før noen fil åpnes | `ecbf55d` |
| Ingen committet test dekket «Denne uken» for Testbedrift A: forslagene, summen på 31, produktet uten prognose, de fire varslene og de 21 rolige produktene. Lager 25→5 på Kabelstrips ga fortsatt grønne tester | EC-13, VG-2, AA-2 og BH-7 | Ny test som regner R-8 på de tre siste gyldige ukene og sammenligner med mockupen. Fire feil som ble lagt inn, ble fanget | `ecbf55d` |
| Teksten sa at sesongen har toppen i uke 26 og bunnen i uke 52, men formelen gir uke 27 og uke 1 | BH-2 | Teksten er rettet | `ecbf55d` |
| `data/README.md` lister ikke alle produktene, terskelen for «lager dekker» var ikke definert, og trend og sesong bare i B var uten forklaring | AA-3, BH-9 og BH-10 | De 21+11 stabile produktene og B-mønsterproduktene er listet, terskelen er definert, og forklaringen står der | `ecbf55d` |
| Testene av skjemaet og LF-linjeslutt var for svake: ingen test sjekket nøklene i skjemaet, og LF-testen leste bare teksten i `.gitattributes`. `pattern_table` leste forbi neste overskrift, og «lager dekker»-mønsteret godtok et produkt uten gyldige uker | BH-4, BH-12, EC-9 og EC-10 | Nøklene testes, `git check-attr` brukes, tabellen kuttes ved neste overskrift, og mønsteret krever 3 gyldige uker | `ecbf55d` |
| Statustabellen nevnte 7 av testene, kommentaren om saltet sa «128 bit entropi», innloggingene manglet «bare for demo», og notatene hadde feil testtall | BH-11, BH-5, BH-15 og AA-5 | Rettet | `ecbf55d` |

**Brukerens beslutninger.** Windows (EC-12, VG-1): teksten i `data/README.md` sier at testene bare er kjørt på macOS og Linux, og det utsatte punktet om pytest i Windows-jobben er utvidet. «Denne uken»: testen over, og story 2.8 sjekker det med kjernen. Alle patchene ble gjort.

**Utsatt.**
- **Story 2.8:** «Denne uken», tillitsmerkene og de 21 rolige produktene sjekkes mot kjernen, og R-8-regningen i testen byttes ut med kjernen.
- **Windows:** pytest med seed-testene i Windows-jobben, og stifiltrene i `windows-setup.yml`.

**Avvist.** 11 funn: blant annet at `main()` bare fanger `ValueError`, at iterasjonene ikke er festet, at mockup-parseren er skjør, at `.gitattributes` ligger utenfor spesifikasjonen og at seed-filene lå utenfor diffen. Alle står under «Review Findings» i [spesifikasjonen](../_bmad-output/implementation-artifacts/spec-1-6-generate-the-synthetic-seed-data.md).

## 2026-11-23 – Omstartssjekken av dataene (Story 1.7; FR-4, SM-5)

**Hva som ble testet.** At produktene, salgsukene og innstillingene er uendret når appen og databasen stoppes og startes på nytt, og at `load_seed --reset` bare gjør noe etter den skrevne bekreftelsen (FR-4, SM-5, DR-4).

**Hvordan.** Brukeren kjørte sjekken på macOS 23. november 2026, på arbeidstreet til story 1.7, mot Docker Compose-databasen etter `migrate` og `load_seed`. Resultatet står her slik brukeren meldte det i chatten. Claude kjørte ikke Docker selv.

**Resultat: bestått.**
- Før og etter omstarten av Docker (`docker compose down`, så `docker compose up -d --wait`) var tallene de samme: 2 bedrifter, 62 produkter, 5 016 salgsuker og 2 innstillinger.
- `window=5` for en bedrift, satt før omstarten, var fortsatt 5 etterpå.
- `load_seed --reset` med svaret `nullstill` lastet testdataene på nytt, og `window` var tilbake til 3.
- Et annet svar, «nei», ble avvist uten endringer.

**Ikke testet.** Omstarten på Windows (testmaskinen er bare tilgjengelig 25. november og 7. desember, og Windows-jobben i GitHub Actions har ingen Docker). Omstarten gjentas på siste commit (story 4.4).

## 2026-11-23 – Feil i KI-generert kode og tekst fra byggingen av story 1.7 (DR-9)

**Hvordan det ble funnet.** Claude Code skrev modellene, leseren, kommandoen, testene og dokumentene i story 1.7 med `bmad-build`, uten subagenter. Testene, Ruff og `makemigrations --check` fant tre feil. Deretter gikk byggeøkten selv gjennom diffen med Blind Hunter og fant 10 funn (BH-1 til BH-10): 3 ble rettet, 6 avvist og 1 utsatt som uverifisert.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| `Meta` i modellene brukte lister, som Ruff avviser (RUF012), og `ordering` som tuppel ga en annen modelltilstand enn migrasjonen | Ruff og `test_migrations_match_the_models` | Tupler i `Meta`, og `ordering` er tatt bort, fordi spørringene sorterer på `position` selv. Migrasjonen er laget på nytt | `85308ac` |
| Regelen som leser grensene i FR-20 fra PRD-en krevde enheten «weeks» eller «%» bak tallene, så raden for glattingsfaktoren («0.1 to 0.9») ga en `KeyError` | `test_the_ranges_are_the_ones_in_the_prd` | Enheten er valgfri | `85308ac` |
| `schema_version` 1.0 ble godtatt som versjon 1, fordi 1.0 == 1 i Python | Blind Hunter i `bmad-build` (BH-1) | Typen må være `int`, og testen har et tilfelle for 1.0 | `85308ac` |
| Ingen test leste teksten som `--reset` viser før bekreftelsen, og testen som skulle sjekke at bare kommandoen nevner `--reset`, het noe annet enn den gjorde | Blind Hunter i `bmad-build` (BH-2 og BH-3) | Testen sjekker at teksten nevner selskapene, innstillingene, de justerte mengdene og ordet, og navnet er rettet | `85308ac` |

**Utsatt.** Klonesteget i `windows-setup.yml` kan bare verifiseres av Windows-kjøringen i pull requesten (BH-8), se [Deferred from: code review of spec-1-7](../_bmad-output/implementation-artifacts/deferred-work.md).

**Avvist.** BH-4 til BH-7, BH-9 og BH-10: antall spørringer, grenene i modellene (Story 3.1), hasher som ikke er PBKDF2, at generatoren og leseren sjekker det samme to ganger, meldingen uten input og slettingen som leser radene. De står under «Review Triage Log» i [spesifikasjonen for story 1.7](../_bmad-output/implementation-artifacts/spec-1-7-load-the-seed-data-with-an-explicit-reset.md).

## 2026-11-23 – Feil i KI-generert kode og tekst fra BMAD Code Review av story 1.7 (DR-9)

**Hvordan det ble funnet.** Fire uavhengige KI-granskere i `bmad-code-review` gikk gjennom arbeidstreet til story 1.7 mot `main` (`16d93b7`), før noe var committet: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. Diffen var uten spesifikasjonen, som bare Edge Case Hunter og Acceptance Auditor fikk. De fant 46 funn: 7 med middels alvor og 39 med lavt. 20 ble rettet, 2 utsatt, 4 var feil funn og 20 ble avvist. Ingen trengte en beslutning av brukeren.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| En fil som ikke kan leses, ga en melding med hele den lokale stien fra operativsystemets feiltekst. Det bryter regelen om at ingen melding har lokale stier | AA-4 | Feilteksten vises ikke, og en test bruker en mappe med navnet `mappe.json` | `85308ac` |
| Leseren godtok 200 tegn i passordhashen, men kolonnen tar 128, og tall over 2 147 483 647. Feilen ville kommet som en rå databasefeil midt i lastingen, etter at `--reset` var bekreftet | BH-4, BH-5, EC-1, EC-2 og VG-1 | Grensene leses fra modellene, tallgrensen er med, og en test sjekker verdiene nøyaktig på grensen | `85308ac` |
| Steget i Windows-jobben godtok hvilken som helst feil med kode 1, også en ødelagt seed-fil | BH-12, EC-13 og VG-3 | Steget krever teksten «Databasen har allerede data» (verifiseres av Windows-kjøringen) | `85308ac` |
| Meldinger om gjentatte kunde- eller varenumre nevnte ikke filen, og meldingen om ulike sluttuker nevnte ikke produktene | EC-17 og AA-3 | Filene og produktene er nevnt, og testene sjekker teksten | `85308ac` |
| Kunde- og bedriftsnavn med mellomrom først eller sist ble godtatt, så et kundenummer som « 1001» ikke kunne skrives inn | EC-5 | Avvises | `85308ac` |
| Testen av at bare kommandoen kjører `--reset`, leste en kort liste filer | BH-10, EC-15 og AA-6 | Alle filer som git sporer, leses, unntatt kommandoen, dokumentene og testene. En `--reset` lagt i `pyproject.toml` ble fanget | `85308ac` |
| Suksessmeldingen kom før transaksjonen var avsluttet, og meldingene sa «ingenting er endret», selv om nøkkelfila kan være laget | BH-1 og BH-11 | Meldingen skrives etter commit, og tekstene sier «ingen data» | `85308ac` |
| README nevnte ikke at `docker compose down -v` sletter databasen, og en setning i statustabellen var utdatert | BH-13 | Begge er rettet | `85308ac` |
| Statustabellen sa «delvis bygd» for FR-4, mens spesifikasjonen sier «bygd» | EC-19 og AA-1 | Står som «bygd» etter omstartssjekken over | `85308ac` |

**Utsatt.**
- **Story 3.1:** modellen for innstillingene har ingen validering av grensene i FR-20 (BH-6 og EC-10).
- **Windows:** klonesteget kan bare verifiseres av pull requestens Windows-kjøring.

**Avvist.** 20 funn, og 4 var feil. Blant dem: et valg som hopper over den skrevne bekreftelsen (`--noinput`), at to kjøringer samtidig kan passere sjekken, at databasen ikke er migrert, `OverflowError` for uke 9999, og at `--reset` kan forkortes til `--res`. Alle står under «Review Triage Log» i [spesifikasjonen](../_bmad-output/implementation-artifacts/spec-1-7-load-the-seed-data-with-an-explicit-reset.md).

## 2026-11-23 – Feil i KI-generert kode og tekst fra byggingen av story 1.8 (DR-9)

**Hvordan det ble funnet.** Av testene, Ruff og en ny lesing av koden før første kjøring, under byggingen av story 1.8 på grenen `story/1-8-log-in-and-see-only-your-own-companys-products` (baseline `7aeb0a7`). Claude bygde innloggingen, utloggingen, produktoversikten og toppfeltet inline, uten subagent.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Første utkast av `login` kalte en metode som ikke finnes (`form.cleaned_data_for_login()`), og `csrf_failure` brukte et attributt som ikke finnes (`request.resolver_match_path`). Begge var plassholdere skrevet før koden var koblet sammen | Ny lesing av koden før første kjøring | `authenticate()` får verdiene fra `cleaned_data`, og stien sammenlignes med `reverse("login")` | `a078c90` |
| CSS-en brukte `font-weight: 600` og `700` og `line-height: 1` direkte, mot regelen i story 1.4 om at skrifter bare kommer fra designtokens | `test_rules_take_colors_fonts_and_radii_only_from_the_tokens` | Reglene bruker `var(--font-label-weight)`, `var(--font-page-title-weight)` og ingen egen linjehøyde | `a078c90` |
| Testhjelperen `session_ids` brukte klientens `session`-egenskap, som lager og lagrer en økt når det ikke finnes noen. Testen av at en mislykket CSRF-sjekk ikke lager økter, så en økt som ikke var der | `test_login_without_a_valid_csrf_token_is_refused` (`Session.objects.count()` var 1) | Hjelperen leser den lagrede økta fra informasjonskapselen | `a078c90` |
| To sider med hvert sitt maskerte CSRF-token er aldri like byte for byte, så testen av at en ny innlasting gir samme side feilet | `test_logged_in_user_is_sent_from_the_login_page_to_the_overview` | Testen fjerner tokenene før sammenligningen | `a078c90` |
| `error.html` hadde en fast lenke til `/produkter/` (BH-6 i story 1.4), som nå er en rute | Åpent punkt i `issues.md` | Lenken bruker `{% url 'products' %}` | `a078c90` |

**Mutasjoner.** Koden ble brutt på 9 steder og satt tilbake, og testene fanget alle: produktene eller uka uten filter på bedriften, innloggingskravet fjernet, CSRF-feilvisningen fjernet, utloggingen som tar GET, innloggingen uten CSRF-sjekk, en melding som nevner feltet og `next` som følges.

## 2026-11-23 – Feil i KI-generert kode og tekst fra BMAD Code Review av story 1.8 (DR-9)

**Hvordan det ble funnet.** Fire uavhengige KI-granskere i `bmad-code-review` gikk gjennom arbeidstreet til story 1.8 mot `main` (`7aeb0a7`), før noe var committet: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. Diffen var på 73,5 kB. Spesifikasjonen gikk bare til Edge Case Hunter og Acceptance Auditor. De fant 35 funn: 7 med middels alvor (som grupper) og resten lave eller feil. 19 ble rettet, 13 avvist og 3 var feil funn. Ingen trengte en beslutning av brukeren. Brukeren ba om særlig tester av tilgangen mellom bedriftene og av CSRF-håndteringen.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| En mislykket CSRF-sjekk på en side som ikke er innloggingen, ga 403 også når ingen var logget inn. En utlogging fra et skjema som overlevde økta og CSRF-kapselen, ga «Skjemaet er utløpt». Spesifikasjonen sier at utloggede besøkende får innloggingssiden | EC-1, AA-1 og AA-2 | `csrf_failure` sender en POST fra en besøkende uten innlogging til innloggingssiden, og testen av «ikke innlogget» kjører nå også med CSRF-sjekken på | `a078c90` |
| Innloggede sider ble ikke merket som ikke-lagringsverdige, så Tilbake etter «Logg ut» kunne vise en annen bedrifts liste fra nettleserens historikk | BH-3 | `@never_cache` på oversikten, og en test av `Cache-Control` for hver rute i `ROUTES` | `a078c90` |
| Testen av utloggingen leste bare informasjonskapselen, så den viste ikke at økta var slettet på tjeneren | BH-4 | Testen krever at økt-raden er borte og at den gamle kapselen ikke lenger gir innlogging | `a078c90` |
| Kildeskanningen etter managers utenfor `queries.py` kunne omgås med `models.Product.objects`, en importert alias, `get_model` og en related manager i en mal | BH-7, EC-9 og VG-2 | Alle `.objects`, import av en bedriftsmodell og `get_model` teller, malene skannes, og en test viser at skanningen finner de fire omgåelsene | `a078c90` |
| Testen av at innloggingen ikke skriver om hashen sjekket bare `startswith` og at `last_login` var satt, så en omskriving av hashen ville ikke blitt fanget | AA-3 | Hashen før og etter sammenlignes. En mutasjon som skrev om hashen, ble fanget | `a078c90` |
| Siste registrerte uke over et årsskifte var ikke testet, selv om seed-dataene krysser nyttår. Sorteringen på bare uke ville gitt «uke 52, 2025» | VG-1 | `test_latest_data_week_crosses_the_new_year`. En mutasjon på sorteringen ble fanget | `a078c90` |
| Kundenummeret ble ikke beholdt etter et mislykket forsøk med et NUL-tegn, mot matrisen i spesifikasjonen, og testen hoppet over det tilfellet | EC-6 og AA-4 | Det innskrevne nummeret vises igjen (malen escaper det), og testen har ikke lenger unntaket | `a078c90` |
| Siden for produktoversikten var ikke under skall-testen, og testen av tilgangen brukte bare to små bedrifter | BH-5, VG-3 og AA-7 | `test_logged_in_page_has_the_shell_and_the_app_header`, og `test_the_seed_companies_see_only_their_own_products` med de ekte seed-dataene og passordene | `a078c90` |
| Isolasjonstesten kunne feile tilfeldig på sifre i et maskert CSRF-token, og `test_manage` samlet hele innloggingssuiten med en feil innstillingsmodul | BH-8 og BH-9 | Tokenene fjernes før sjekken, og `test_manage` samler `tests/test_company.py` | `a078c90` |
| Feltene hadde ikke `aria-invalid` etter en feil, og README nevnte ikke at telefontesten sender passordet over vanlig HTTP | BH-12 og BH-15 | `aria-invalid="true"` på begge feltene, og en setning i README | `a078c90` |

**Utsatt.** Ingen funn ble utsatt. Hashen i endringslogg-radene («hash følger») ble fylt inn etter commiten (`a078c90`).

**Avvist.** 13 funn, og 3 var feil. Blant dem: ingen begrensning av antall forsøk eller lengden på feltene (én bruker per maskin, passordene er offentlige), ingen tom-tilstand eller tabelltekst for en bedrift uten produkter (katalogen har ingen tekst, og Epic 2 erstatter listen), at en utdatert innloggingsskjema fra en innlogget bruker bare sender brukeren til oversikten (spesifikasjonen, og en mislykket sjekk skal aldri bytte bedrift), ingen `next` etter innlogging, og at CSS-reglene for felt gjelder alle skjemaer. De står under «Review Triage Log» i [spesifikasjonen](../_bmad-output/implementation-artifacts/spec-1-8-log-in-and-see-only-your-own-companys-products.md).

## 2026-11-23 – Funn i Safari-testen av story 1.8 (FR-1, NFR-10, DR-9)

**Hvordan det ble funnet.** Brukeren testet innloggingen i Safari på macOS 23. november 2026, på arbeidstreet til story 1.8 etter BMAD Code Review. Resultatet står her slik brukeren meldte det i chatten. Claude kjørte ikke Safari selv.

**Feilene.**

| Feil | Årsak | Retting | Commit |
|---|---|---|---|
| Etter utlogging fra A og B viste Tilbake-knappen produktoversikten igjen. En oppdatering av siden sendte til innloggingen | Serveren var riktig: `Cache-Control: no-store` ble sendt (sjekket med curl), og en forespørsel uten økt ble sendt til innloggingen. Safari viser siden fra tilbake-hurtigbufferen, og WebKit overlater det til `pageshow`. Claudes rettelse i reviewen (`never_cache`) var derfor ikke nok i Safari | `app.js` laster en gjenopprettet side på nytt (`pageshow` med `persisted`), bare på innloggede sider. Brukeren valgte det, og AD-11 er utvidet med en rad i endringsloggene. Testene sjekker script-taggen, innholdet og at utloggede sider ikke har script. Verifisert i node og med en ekte server | `a078c90` |
| Et gammelt innloggingsskjema sendt på nytt etter innlogging og utlogging ga «Skjemaet er utløpt» | Innloggingen bytter CSRF-token, så skjemaet fra Tilbake-historikken feiler sjekken. Visningen fra reviewen omdirigerte bare innloggede brukere. Gjenskapt med curl | `csrf_failure` sender hver POST fra en besøkende uten innlogging til en ny innloggingsside (ingen innlogging skjer), og logger avslaget selv, siden Django bare logger en 403. Siden «Skjemaet er utløpt» er igjen for en innlogget brukers andre skjemaer. Tre tester og to mutasjoner | `a078c90` |

**Ikke en feil.** At en oppdatering etter utlogging sender til innloggingen er riktig oppførsel.

## 2026-11-23 – Manuelle tester av innlogging og isolasjon (Story 1.8; FR-1, FR-2, NFR-6, NFR-10, SM-4)

**Hva som ble testet.** At hver testbedrift logger inn og ser bare egne produkter og egen siste uke, at utloggingen og Tilbake-knappen virker, at et gammelt innloggingsskjema ikke gir en feilside, og at sidene ser riktige ut ved 320 px, 390 × 844 og 820 × 1180 og på en ekte telefon.

**Hvordan.** Brukeren testet 23. november 2026, på arbeidstreet til story 1.8, først etter BMAD Code Review ([funnene fra Safari](#2026-11-23--funn-i-safari-testen-av-story-18-fr-1-nfr-10-dr-9)) og så på nytt etter rettingene. Resultatet står her slik brukeren meldte det i chatten. Claude kjørte ikke Safari selv.

**Resultat av retesten: bestått.**
- **Safari på Mac (responsiv visning):** Tilbake etter utlogging virker for Testbedrift A og B, og produktoversikten vises ikke. Et gammelt innloggingsskjema sendt på nytt gir et nytt, tomt skjema uten CSRF-melding. Innloggingen og produktoversikten ser riktige ut ved 320, 390 og 820 px. Den hvite fokusringen er bekreftet på «Produktoversikt» og «Logg ut» ved 320 px.
- **Ekte iPhone 13 i Safari over lokalnettet (NFR-6), iOS 27.0.1:** innloggingen virker for begge testbedriftene. A viser egne produkter og uke 45, 2026, og B egne produkter og uke 44, 2026. Layout, tekst og berøringsknapper fungerer visuelt bra. Etter utlogging og Tilbake vises innloggingssiden. Appen ble stoppet med Ctrl+C etter testen, og `PROGNOSE_LAN_HOST` var bare satt på startkommandoen.

**Ikke bekreftet.** At iPhone ikke zoomer inn ved inntasting i feltene (16 px tekst). Det sjekkes på nytt på den ekte telefonen i story 4.4 (`issues.md`). Windows er ikke testet (testmaskinen er tilgjengelig 25. november og 7. desember).

## 2026-11-24 – Feil i KI-generert kode og tekst fra byggingen av story 2.1 (DR-9)

**Hvordan det ble funnet.** Av mutasjonstestene og testene under byggingen av story 2.1 på grenen `story/2-1-find-the-valid-weeks-unusual-weeks-and-level-shifts` (baseline `1b8927d`). Claude bygde `src/forecasting/weeks.py` og testene inline, uten subagent. Reglene R-1, R-10 og R-11 ga riktig svar for alle tilfellene i regnearket ved første kjøring.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Det første settet med 20 mutasjoner av `weeks.py` fanget alle, men testene hadde tre hull som det ikke dekket: uker som sjekkes fra 1 eller 2 tidligere uker (E19), en baseline på 1 som aldri flagges, og at funksjonen bare virker for en liste. Mutasjonssettet var skrevet ut fra koden og ikke ut fra hvert ledd i R-10 | Verification Gap-granskeren og et andre sett mutasjoner (se neste del) | Tester for hvert ledd: `test_a_week_with_fewer_than_three_earlier_valid_weeks_is_not_checked`, en baseline på 1 i `test_the_baseline_uses_the_three_most_recent_earlier_weeks_only` og en generator i `test_the_classification_does_not_change_its_input_and_takes_any_iterable`. Alle 29 mutasjoner fanges nå | `5548f4e` |

**Mutasjoner.** `weeks.py` ble brutt på 29 steder og satt tilbake etter hvert sett, og filen ble sammenlignet byte for byte med kopien: `>=` for `>`, faktoren 3, baseline på 2 eller 4 uker eller over alle tidligere uker, gjennomsnitt, største eller minste verdi i stedet for medianen, null-baseline tillatt, utsolgte uker regnet som gyldige, nytt nivå av 2 eller 4 uker, et brutt løp, og uker som sjekkes fra 1 eller 2 tidligere uker.

## 2026-11-24 – Feil i KI-generert kode og tekst fra BMAD Code Review av story 2.1 (DR-9)

**Hvordan det ble funnet.** Fire uavhengige KI-granskere i `bmad-code-review` gikk gjennom arbeidstreet til story 2.1 mot `main` (`1b8927d`), før noe var committet: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. Diffen var på 24,8 kB (55,3 kB med dokumentene for Acceptance Auditor). Spesifikasjonen gikk til Edge Case Hunter og Acceptance Auditor. Byggeflyten har bare de tre første lagene, så Acceptance Auditor, som rutinen for kodegjennomgang og story 1.1 til 1.8 bruker, ble lagt til før commiten. Den første Verification Gap-kjøringen fikk en feilskrevet filsti i oppdraget fra Claude, fant filen likevel og meldte ingen funn, så den ble gjentatt med riktig sti. De fant 29 funn: 3 med middels alvor (som grupper), og resten lave eller feil. 16 ble rettet, 5 avvist og 8 var feil funn. Ingen trengte en beslutning av brukeren.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Regelen «færre enn 3 tidligere uker sjekkes ikke» var ikke testet: en endring til `>= 1` eller `>= 2` tidligere uker passerte alle 46 testene, fordi første tre uker i E19 aldri hopper | VG-1 | `test_a_week_with_fewer_than_three_earlier_valid_weeks_is_not_checked` | `5548f4e` |
| Regnearket oppgir de gyldige ukene bare som antall, og testen sammenlignet bare antallet. Feil uker med riktig antall ville passert, og den eneste sjekken av posisjoner gjentok funksjonens egen regel | BH-6 og EC-5 | Hvert tilfelle og produkt sammenligner også posisjonene med R-1, og E7 oppgir 1, 2, 5 og 6 | `5548f4e` |
| Ingen direkte test av en baseline på 0, av et nytt nivå etter det første, eller av en funksjon som tar en generator, selv om testnavnet sa «any sequence» | BH-8, EC-4, BH-5, EC-1 og VG-2 | Tre nye tester, og `tuple(weeks)` først i funksjonen | `5548f4e` |
| Testen av produktene kunne bli tom uten feil, og importtesten krevde nøyaktig samme mengde og gjentok AD-1-testen uten å si hvorfor den er nødvendig | BH-7, EC-6, BH-10 og EC-7 | Antallet kontrollerte produkter må være lik antallet i regnearket, og importtesten sjekker en delmengde og sier at den holder klokken ute | `5548f4e` |
| Testene for håndlagde historier bar E-n-navn som om de var rader i regnearket, en sjekk som ikke kunne feile (`len(run) == 3`) og et tidspunkt i `sprint-status.yaml` som Claude hadde funnet på | BH-9, VG-3, BH-12 og AA-1 | Teksten sier «som i E8» og så videre, sjekken er fjernet, og tidspunktet er klokka da filen ble endret | `5548f4e` |

**Utsatt.** Ingen funn ble utsatt.

**Avvist.** 5 funn, og 8 var feil. Blant dem: ingen kontroll av flyttall, `None` eller negative tall (tallene kommer fra heltallskolonner og den kontrollerte seed-dataen), at `Week` er en `NamedTuple` i stedet for en dataklasse, at basislisten bygges på nytt for hver uke (høyst 104 uker), og at dokumentene og statusen ikke var med i diffen (de er siste oppgave, etter reviewen). De står under «Review Triage Log» i [spesifikasjonen](../_bmad-output/implementation-artifacts/spec-2-1-find-the-valid-weeks-unusual-weeks-and-level-shifts.md).

**Merknad om prosessen.** Granskerne endret `weeks.py` selv for å teste mutasjoner i arbeidstreet, og én av dem satte filen tilbake feil én gang (`OUTLIER_FACTOR = 3`) og rettet det. Claude sammenlignet filen med kopien fra før reviewen, og den var identisk. Neste gang bør oppdraget si at granskerne ikke skal endre filer i arbeidstreet.

## 2026-11-24 – Feil i KI-generert kode og tekst fra byggingen av story 2.2 (DR-9)

**Hvordan det ble funnet.** Av testene og mutasjonstestene under byggingen av story 2.2 på grenen `story/2-2-calculate-the-base-forecast-with-the-moving-average-or-exponential-smoothing` (baseline `a66efb4`). Claude bygde `src/forecasting/forecast.py` og testene inline, uten subagent. Reglene R-2, R-3, R-4 og R-6 ga riktig svar for alle 24 tilfellene og alle 11 produktene i regnearket ved første kjøring.

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| Ruff (B008) avviste testens hjelpefunksjon, som hadde `ForecastSettings()` som standardverdi for et argument | `uv run ruff check` | En felles `DEFAULT_SETTINGS` utenfor funksjonen | `0c31ef6` |
| Testen av vinduet brukte en feil rekkevidde (`range(14, 36, 2)` i stedet for `range(14, 38, 2)`), så den beregnede forventningen manglet siste uke | Claude, ved gjennomlesing av testen før første kjøring | Rekkevidden er rettet | `0c31ef6` |

**Mutasjoner.** `forecast.py` ble brutt på 55 steder og satt tilbake, og filen ble sammenlignet byte for byte med kopien: innstillingen snudd, uvanlige uker alltid eller aldri utelatt, nytt nivå utelatt, alle uker brukt, vinduet én for lite eller for mye, de første i stedet for de siste ukene, byttet α, startnivå 0, første uke brukt to ganger, første nivå som prognose, utsolgte uker som salg, grensen på 3 gyldige uker satt til 2, til 4, med `<=` eller fjernet, vindussjekken med `<=` eller fjernet, eksponentiell glatting som krever 2 uker eller vinduet, årsakene byttet, ukjent metode tatt for eksponentiell glatting, avrunding, heltallsdivisjon, `Decimal` uten omgjøring, lagerbeholdningen brukt, ukene ikke gjort om til en tuple, posisjoner fra 0, tomme felt for uvanlige uker, nytt nivå, innstillinger og antall uker, nivåer for det glidende gjennomsnittet, og 19 på kontrollen av innstillinger (ikke kalt, kalt for sent, metoden, vindustypen, hver ende av vinduet eller α flyttet eller gjort streng, `Decimal` mot flyttall, og vinduet ikke kontrollert for eksponentiell glatting). 54 ble fanget. Mellom to runder overlevde to: en kontroll av `bool` som aldri kan slå inn (0 og 1 er under det minste vinduet), som er fjernet, og vinduet for eksponentiell glatting, som fikk en test. Den siste er en ekvivalent mutant: sjekken av 3 gyldige uker gjort på kalkulasjonsukene, som ikke kan skilles fra den ekte, fordi 3 gyldige uker alltid gir minst 3 kalkulasjonsuker (R-10 sjekker aldri de tre første ukene).

## 2026-11-24 – Feil i KI-generert kode og tekst fra BMAD Code Review av story 2.2 (DR-9)

**Hvordan det ble funnet.** Fire uavhengige, skrivebeskyttede KI-granskere i `bmad-code-review` gikk gjennom arbeidstreet til story 2.2 mot `main` (`a66efb4`), før noe var committet: Blind Hunter, Edge Case Hunter, Verification Gap og Acceptance Auditor. Diffen var på 18,4 kB. Spesifikasjonen gikk til Edge Case Hunter og Acceptance Auditor. Claude skrev igjen en feil filsti i oppdraget til Verification Gap, som meldte «ingen hull» på 40 sekunder, så oppdraget ble gjentatt med riktig sti og med krav om at granskeren oppgir hvilken diff den leste. De fant 23 funn: 2 med middels alvor (som grupper), og resten lave eller feil. 14 ble rettet, 7 avvist og 2 var feil funn. Ett punkt gikk til brukeren, som ba om en vurdering av om kjernen skal avvise et ugyldig vindu og en ugyldig α (se under).

**Feilene som ble rettet.**

| Feil | Funnet av | Retting | Commit |
|---|---|---|---|
| To tellinger i `test_the_listed_examples_are_all_checked` sammenlignet leseren med sitt eget filter og kunne aldri feile, selv om teksten sa at en fjernet rad ikke går ubemerket hen | BH-2, EC-7, EC-8 og EC-10 | Eneste tilfelle som er utelatt må være E14, og alle regeltestprodukter må kontrolleres | `0c31ef6` |
| E23 og FR-21-variantene stod i matrisen, men ikke i listen over eksempler | BH-3 og AA-2 | E23, FR-21 a og FR-21 b er lagt til | `0c31ef6` |
| R-6 var ikke testet med 2 gyldige uker og et vindu på 2, eller med nøyaktig 3 gyldige uker for eksponentiell glatting | BH-6 | Vindu 2 i testen av 2 gyldige uker, og en test av 3 gyldige uker for begge metoder | `0c31ef6` |
| Ingen test sa at det glidende gjennomsnittet ikke har nivåer, og fem tester nevnte bare en av E-n og FR-n | VG-1 og AA-1 | `levels == ()` i testen, og E-n og FR-n i teksten til testene | `0c31ef6` |
| Kjernen kontrollerte bare metoden: vindu 0 ga `ZeroDivisionError`, og et negativt vindu eller en α utenfor 0,1 til 0,9 ga et tall som ligner en prognose. Funnet ble først avvist, siden skjemaet i story 3.1 skal kontrollere verdiene | BH-1 og EC-1 til EC-4, og brukerens spørsmål | `check_settings` avviser metode, vindu og α utenfor definisjonene i `settings.py` med `ValueError`, før noe beregnes, for begge metodene og også uten prognose. Grensene leses fra `settings.py`. 28 nye tester og 19 mutasjoner | `0c31ef6` |

**Utsatt.** Ingen funn ble utsatt.

**Avvist.** 7 funn, og 2 var feil. Blant dem: negative tall og `None` (verdiene kommer fra heltallskolonner og den kontrollerte seed-dataen), at årsaken er en tekststreng og ikke en `Enum` (som metodene og varslene), og at kalkulasjonsukene bare sammenlignes som antall (verdien av prognosen og nivåene viser hvilke uker som er brukt). De står under «Review Triage Log» i [spesifikasjonen](../_bmad-output/implementation-artifacts/spec-2-2-calculate-the-base-forecast-with-the-moving-average-or-exponential-smoothing.md).

**Merknad om prosessen.** Granskerne leste og rapporterte bare. Claude sammenlignet hashene av alle filer i `src`, `tests`, `reference`, `docs` og implementasjonsfilene før og etter reviewen, og de var identiske.
