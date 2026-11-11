# Story 1.1: prosjektskjelett lokalt og på Vercel

## 2026-11-10 kl. 19:26 — 

### Oppgave
Starte BMAD-build for story 1.1 etter godkjent plan og arkitektur, med subagenter bare ved behov. Brukeren godkjente spesifikasjonen og ba om å stoppe før implementeringen, og minnet om at PostgreSQL via Neon skal brukes på Vercel.

### Plan
- `bmad-build`, steg 1 og 2: epic 1-konteksten og spesifikasjonen. Begge ble laget uten subagenter, fordi planleggingsdokumentene allerede var lest.
- Egen gren for storyen: `story/1-1-project-skeleton` (DR-7).
- Spesifikasjon: `_bmad-output/implementation-artifacts/spec-1-1-project-skeleton-running-locally-and-on-vercel.md`.

### Resultat
- `epic-1-context.md` ligger i `_bmad-output/implementation-artifacts/`.
- Spesifikasjonen er godkjent og har status `ready-for-dev`. Den er på omtrent 2 070 tokens, og brukeren valgte å beholde den samlet.
- Brukerens påminnelse er låst i spesifikasjonen: på Vercel er databasen alltid Neon PostgreSQL via `DATABASE_URL`, aldri SQLite.
- `sprint-status.yaml`: story 1.1 har status `ready-for-dev`, og valideringen er bestått.
- Ingen kode er skrevet. Commit `ce6afbb` Legg til spesifikasjon for story 1.1 er pushet til GitHub på grenen `story/1-1-project-skeleton`, sammen med denne loggen.

### Åpne punkter
- Ingen nye. Eierstegene for Vercel og Neon står i spesifikasjonen, og sjekken av kontogrensene står allerede i `issues.md`.

## 2026-11-10 kl. 20:44

### Oppgave
Fortsette BMAD-build med story 1.1 fra den godkjente spesifikasjonen (`ready-for-dev`), etter godkjent arkitektur og sprintplan. Subagenter ved behov, ingen commit eller push uten godkjenning, og korte svar. Til slutt ba brukeren om kontroll av git-status og personvern, commit og push til grenen, og en sjekk av at grenen er i synk med GitHub, uten merge.

### Plan
- `bmad-build` steg 3–5: én subagent implementerte spesifikasjonen. Deretter sjekket jeg diffen mot oppgavene og I/O-matrisen selv, og kjørte README-flyten på en ren kopi.
- Review med tre uavhengige subagenter (blind hunter, edge case hunter, verification gap). Funnene ble sortert i spesifikasjonens Review Triage Log, og patchene gikk tilbake til implementeringsagenten.
- Spesifikasjon: `_bmad-output/implementation-artifacts/spec-1-1-project-skeleton-running-locally-and-on-vercel.md`.

### Resultat
- Django 5.2.19-skjelettet er på plass:
  - `prognose/`: settings med hjelpefunksjoner i `env.py`, urls og wsgi.
  - `accounts.Company` er brukermodellen i første migrering.
  - `planning`: startside, `/helse/` og `load_seed`, som foreløpig bare lager `.secret_key`.
  - Norske maler for start, 404 og 500, og ett stilark.
  - Oppsettfiler: `requirements.txt` med eksakte pinner, `ruff.toml`, `vercel.json` (fra1, bare `main`), `.env.example` og `.python-version`.
  - README har fått seksjonene «Kom i gang lokalt» og «Publisering».
- Verifisert:
  - `check`, `makemigrations --check`, 30 tester, `ruff check` og `ruff format --check` er grønne.
  - README-flyten er kjørt på en ren kopi med nytt `.venv`. `/` gir 200 med `lang="nb"`, stilarket gir 200, `/finnes-ikke/` gir norsk 404, og `/helse/` svarer `ok`.
  - `collectstatic` med `VERCEL=1` trenger ingen database.
  - Pinnene finnes for Linux x86_64 (Vercel), Windows og macOS.
- Review ga 40 funn:
  - 14 er rettet med 9 endringer: tre testhull (DEBUG fra `.env`, lokal `DATABASE_URL`, konsollogging), Neon-URL-en holdes utenfor skallhistorikken, og mindre rettelser i README, `.gitignore` og favicon.
  - 1 er utsatt til `deferred-work.md`.
  - 25 er avvist, med begrunnelse i triageloggen.
  - Rettet 2026-11-11: her sto først «9 er patchet» og «30 er avvist». Det var antall rettingsinstrukser, ikke antall funn i triageloggen.
  - Hver ny test feilet mot sin mutasjon.
- Status: spesifikasjonen er `done`, og story 1.1 står som `review` i `sprint-status.yaml` (epic 1 er `in-progress`).
- Etter godkjenning fant personvernsøket ingen stier, e-postadresser eller nøkler, bare tydelige testverdier. Commit `571d4dc` Legg til prosjektskjelettet for story 1.1 er pushet til GitHub på grenen `story/1-1-project-skeleton`, sammen med denne loggen. Ingenting er flettet.
- Punktet om README-sekvensen fra 2026-11-01 står fortsatt åpent: oppsettet er skrevet og testet, men testdataene kommer først i story 1.2.

### Åpne punkter
- Publiseringen (eierstegene i README «Publisering») og kontosjekkene (AR-17) står allerede i `issues.md`, i punktet fra 2026-11-08.
- Norske sider for 400, 403 og CSRF-feil (`403_csrf.html`) mangler, så Django viser engelske standardsider. Ta det med i story 1.3, der innloggingsskjemaet gjør CSRF-siden synlig.
- Migreringssjekk før pull requester (`makemigrations --check`, og `migrate --check` mot Neon) krever en arkitekturbeslutning. Den er utsatt i `deferred-work.md`.
- Ruff 0.17 sjekker også Python-kodeblokker i Markdown, så en uformatert Python-blokk i `.logs/` eller `docs/` får `ruff format --check .` til å feile. Hold slike blokker formatert, eller bestem om `.logs` og `docs` skal unntas i `ruff.toml`.

## 2026-11-11 kl. 19:02

### Oppgave
Sjekke hva som er klart for publisering på Vercel med Neon, ut fra README og arkitekturen, uten å endre noe. Deretter opprette en pull request fra `story/1-1-project-skeleton` til `main` med GitHub CLI, uten merge og uten å endre kode eller Git-innstillinger. Til slutt sjekke om organisasjonen IBE160-2026 tillater Vercels GitHub-app (AR-17), uten å installere, koble til eller endre noe.

### Plan
- Lese README «Publisering» og arkitekturspinen, og sjekke repoet og GitHub. Alt var bare lesing.
- Skrive PR-teksten fra dokumentert arbeid, kjøre personvernsøk på den og opprette PR-en med `gh pr create`.
- AR-17: lese med `gh api`, uten å endre noe:
  - rollen i organisasjonen og i repoet;
  - hvilke rettigheter Vercel-appen ber om;
  - om organisasjonen har spor av Vercel.

### Resultat
- **Klarhet:**
  - Repoet er klart for Vercel og Neon.
  - Det som mangler, er Vercel-prosjektet, Neon, `SECRET_KEY`, fletting, `migrate` mot Neon, sjekk av produksjonsadressen og AR-17-resultatene.
  - Ingen Vercel-kobling er synlig på GitHub ennå, og repoet er offentlig.
  - Node og `npx` finnes for reserveløsningen med Vercel CLI.
- **Pull request:** PR #1 «Story 1.1: Prosjektskjelett lokalt og på Vercel» er opprettet: <https://github.com/IBE160-2026/G40-lyamouri/pull/1>.
  - Den er åpen og flettbar, med 7 commits og 42 filer (head `13fc098`).
  - Den har sjekklister for eierstegene før og etter fletting (AC 2) og plass til AR-17-resultatene (AC 3).
- **Kontroll:** personvernsøket i PR-teksten fant ingen treff. `main` er urørt (`f4938a9`), Git-konfigurasjonen har samme fingeravtrykk som før, og ingen kode er endret.
- **AR-17:** kan ikke bekreftes.
  - Brukeren er medlem av IBE160-2026, ikke eier, og har `pull`, `push` og `triage` i repoet, ikke admin.
  - Vercels GitHub-app ber om organisasjonsrettigheten `members=read`. Derfor kan bare en eier av organisasjonen installere den, og et medlem kan bare be om det.
  - Lista over installerte apper krever eierrettigheter og ble ikke lest. Jeg ba ikke om ekstra tilgang.
  - Brukeren ser ett repo i organisasjonen, og det har ingen Vercel-publiseringer.

### Åpne punkter
- Be eieren av IBE160-2026 godkjenne Vercels GitHub-app for G40-lyamouri, via importen i Vercel. Blir den ikke godkjent i tide, brukes reserveløsningen i README steg 1: Vercel CLI fra en fersk klon etter fletting. Resultatet føres i PR #1 under «AR-17-resultater».
- Resten av publiseringen står allerede i `issues.md` (punktet fra 2026-11-08), og sjekklistene står i PR #1.
