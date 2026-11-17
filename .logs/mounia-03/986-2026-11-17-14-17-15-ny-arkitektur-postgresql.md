# Ny arkitektur med PostgreSQL

## 2026-11-17 kl. 14:17 — Mounia-03

### Oppgave
Brukeren ba om en ny BMAD-arkitektur bygget på den godkjente PRD-en, UX-designet og `technology.md`, som brukeren kaller sine teknologipreferanser, tilpasset prosjektet. De åpne punktene i `issues.md` skulle undersøkes først, og den gamle arkitekturen skulle ikke gjenbrukes ukritisk.

Underveis bestemte brukeren:
- PostgreSQL er et krav både lokalt og publisert, og lokalt kjører det med Docker Compose.
- Løsningen skulle testes på Mac før godkjenningen.
- P1–P10 og de små avklaringene er godkjent, med ett forbehold for P6 og `load_seed`: ingen automatisk sletting eller overskriving av brukerdata.

Til slutt skulle Claude:
- oppdatere PRD-en, addendumet og UX-en;
- skrive spinen og et kort notat til læreren;
- gjennomgå arbeidet uten agenter;
- dokumentere testen og oppdatere loggene.

Implementeringen skulle ikke startes, og ingenting skulle committes eller pushes før brukeren har godkjent resultatet.

### Plan
- Lese PRD-en, addendumet, UX-spinene, `technology.md`, `issues.md`, den arkiverte arkitekturen og notatene fra story 1.1. Verifisere versjoner og tjenester på nettet.
- Legge fram anbefalingene P1–P10 til godkjenning, og undersøke konsekvensene av PostgreSQL lokalt.
- Installere Docker Desktop etter godkjenning, og teste PostgreSQL med en midlertidig `compose.yaml` utenfor prosjektet.
- Oppdatere PRD-en, addendumet, UX-en og `docs/PRODUCT.md`, skrive spinen fra memloggen og gjøre gjennomgangen selv.
- BMAD-arbeidsmappa: `_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/`, med `.memlog.md`, `ARCHITECTURE-SPINE.md`, `teknologinotat.md` og `reviews/review-inline.md`.

### Resultat
- **Arkitekturspinen** (`final`) har 17 beslutninger:
  - Django 5.2.19 LTS med en ren beregningskjerne i `forecasting/` og `explanation/`;
  - én beregningsvei per bedrift;
  - én modul for avrunding og norsk tallformat;
  - isolasjon mellom bedriftene i én modul;
  - ISO-uker;
  - innstillinger definert ett sted;
  - Post/Redirect/Get;
  - grafen som SVG laget på serveren, og et fast adressekart;
  - norske feilsider;
  - kjøremodusene;
  - PostgreSQL 18 med Docker Compose lokalt og Neon publisert;
  - seed-data med en bekreftet tilbakestilling;
  - trygg publisering;
  - én testkommando med regnearket som eneste fasit.
- **Brukerens forbehold** er bygget inn:
  - byggesteget på Vercel migrerer bare når endringene bare legger til, og laster seed-data bare i en tom database;
  - `load_seed` sletter aldri data uten `--reset` og en bekreftelse.
- **PRD-en** fikk tre nye rader i §12, og den åpne linjen i §12 er fjernet. Endrede krav:
  - FR-4, NFR-1, NFR-2, NFR-3 og NFR-9;
  - DR-1, DR-2, DR-4 og DR-10;
  - SM-2, SM-5, §10 spørsmål 2 og oppsummeringen øverst.
- **Andre dokumenter:**
  - addendumet: §1 og en datert del i §2;
  - `EXPERIENCE.md`: feilsidene «Database unavailable», «Server error» og «Expired form» i skjermkartet, meldingskatalogen, komponentene og tilstandene, og en ny feilvei i flyt 2, med en rad i endringsloggen;
  - `DESIGN.md`: én linje;
  - `docs/PRODUCT.md`: stakken og tilbakestillingen.
- **Docker Desktop 4.99.0** er installert fra Dockers offisielle kilde. Diskbildet var helt, appen er signert av Docker Inc og notarisert, og den krever macOS 14.0.
- **PostgreSQL-testen på Mac:**
  - første oppstart tok 17 sekunder og en omstart 3 sekunder;
  - tilkoblingen virket uten passord, bare fra `127.0.0.1`;
  - testen brukte PostgreSQL 18.7 med UTF-8;
  - Django kjørte 15 migreringer på 0,15 sekunder;
  - 10 400 salgsuker ble lagret på 0,17 sekunder;
  - dataene var der etter omstart;
  - PostgreSQL brukte 30 MB minne, og Docker rundt 550 MB.

  Resultatet står i `docs/qa-logg.md`. Oppstart uten nett og oppsett på Windows er markert som ikke gjennomført.
- **Gjennomgangen:**
  - Kontrollskriptet `lint_spine.py` fant ingen feil.
  - Alle 64 krav fra PRD-en er bundet til spinen, og det finnes ingen henvisninger til krav eller AD-er som ikke finnes.
  - 12 hull og mangler er lukket. Detaljene står i `reviews/review-inline.md`.
- **Lærernotatet** `teknologinotat.md` forklarer hva som er tatt med, tilpasset og droppet fra `technology.md`.
- **Lukket i `issues.md`:**
  - punktet om ny arkitektur og vurdering av `technology.md` (15. november);
  - punktet om de åpne punktene fra story 1.1 (16. november).

  Punktet om QA-loggen er delvis løst, seks punkter har fått merknader, og fire nye punkter er lagt til.
- **Sluttkontroll før commit:** to utdaterte utsagn ble rettet.
  - Arkivets README sa at PRD-en sist ble oppdatert 16. november, at den nye arkitekturen ikke var laget, og at PRD-en hadde en åpen linje i §12.
  - Addendum §2 beskrev databasekravet som en lokal fil.
- **Tillatelser:** et forsøk på å teste PostgreSQL fra en Python-pakke ble stoppet av tillatelsessystemet. Det ble ikke prøvd på nytt.
- **Uendret:** ingen kode og ingen commits. `story/1-1-project-skeleton` og taggen er ikke rørt. Sesjonsloggen er heller ikke committet, fordi brukeren har bedt om at ingenting committes før resultatet er godkjent.

### Åpne punkter
- Gå gjennom og godkjenne resultatet av arkitekturen og dokumentendringene.
- Ved commit: fylle inn commit-hashen der PRD-en (§12) og `EXPERIENCE.md` sier «not committed yet».
- Bekrefte at Dockers vilkår er godtatt i Docker Desktop.
- Lage nye epics og stories (`bmad-create-epics-and-stories`) og en ny sprintplan fra den nye arkitekturen.
- Teste oppstart uten nett og oppsett på Windows (x64) i første story og på siste commit (står allerede i `issues.md` som merknad 2026-11-17).
- Kontrollene i første story står under Deferred i spinen: Vercel-appen i organisasjonen, Vercel-oppdagelsen av `src/manage.py`, Neon i Frankfurt og GitHub Actions.
