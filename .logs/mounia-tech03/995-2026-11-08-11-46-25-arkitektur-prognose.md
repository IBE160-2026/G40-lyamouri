# Arkitektur for Prognose

## 2026-11-08 kl. 11:46 — mounia.tech03

### Oppgave
Starte BMAD-arkitekturen for Prognose med den godkjente PRD-en og UX-designet. Arkitekturen skal være enkel og realistisk. Ingen subagenter, spare tokens, korte svar, og ingen commit eller push uten godkjenning.

### Plan
- `bmad-architecture`, rask vei og bare spine (brukerens valg). Stakken ble valgt av brukeren: Django + SQLite.
- Versjonene ble sjekket mot primærkilder. Gjennomgangen ble gjort i hovedtråden: lint, versjonssjekk og en motpartskontroll av beslutningene.
- Arbeidsmappe: `_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-08/` (`.memlog.md` og `ARCHITECTURE-SPINE.md`).

### Resultat
- **`ARCHITECTURE-SPINE.md` (utkast):**
  - en server-rendret Django-monolitt med en ren beregningskjerne;
  - 14 arkitekturbeslutninger (AD-1 til AD-14);
  - konvensjoner, stakk, mappestruktur og tre diagrammer;
  - en oversikt over hvor hver funksjon hører hjemme, og hva som er utsatt.
- **Versjoner:** Django 6.1.3, Chart.js 4.6.1, Ruff 0.17.4 og Python 3.13 (minimum 3.12).
- **Motpartskontrollen** tettet tre hull: én tallformatering, grenser for innstillingene definert ett sted, og ingen tallformatering i `charts.js`.
- **Lint:** ingen funn.
- Ingenting er committet eller pushet.

### Åpne punkter
- Bekrefte antakelsene fra den raske veien. Deretter settes spinen til `final`.

## 2026-11-08 kl. 12:03 — mounia.tech03

### Oppgave
Brukeren valgte Django 5.2 LTS med Python 3.13, runserver bare lokalt, og godkjente antakelse 3–5 for MVP. Arkitekturen skal være enkel, kunne videreutvikles og prioritere fristen.

### Plan
- Oppdatere spinen og sette den til `final` (rask vei, ingen subagenter).

### Resultat
- Spinen er oppdatert med:
  - Django 5.2.19 LTS og Python 3.13;
  - en regel om at runserver bare brukes på egen PC;
  - en setning om sømmene for videre utvikling;
  - en konvensjon om at må-ha bygges først.
- Spinen har status `final`, og lint gir ingen funn.
- Ingenting er committet eller pushet.

### Åpne punkter
- Neste steg er epics og stories (`bmad-create-epics-and-stories`).
- Commits: `29dd679` Legg til arkitektur for Prognose (Django 5.2 LTS) og `e53053e` Oppdater arbeidsloggen med arkitekturen, pushet til GitHub sammen med denne loggen.

## 2026-11-08 kl. 12:31 — mounia.tech03

### Oppgave
Sjekke at Django 5.2 fungerer med Vercel, beholde SQLite lokalt, planlegge PostgreSQL for publisering, og oppdatere arkitekturen ved behov. Enkel MVP og fristen først.

### Plan
- Sjekke Vercel-dokumentasjonen og versjonene på nettet. Oppdatere spinen i oppdateringsmodus med stabile AD-ID-er.

### Resultat
- Vercel støtter Django ifølge dokumentasjonen (ikke testet med en faktisk publisering): prosjektet oppdages via manage.py og WSGI, Python 3.13 velges med .python-version, og collectstatic kjøres via STATIC_ROOT. PostgreSQL kommer fra Neon sin gratisplan i Vercel Marketplace, og psycopg er 3.3.8.
- Spinen er oppdatert:
  - AD-13: lokal kjøring er standard og må-ha-vei, og publisering på Vercel er valgfri etter må-ha;
  - AD-12: SECRET_KEY kommer fra en miljøvariabel ved publisering;
  - ny AD-15: databasen velges med DATABASE_URL, med bare ORM og migreringer;
  - stakk, diagram og utsatte punkter er oppdatert;
  - kontrollen i hovedtråden la til `psycopg[binary]`, slik at Vercel ikke trenger libpq, og en merknad om `DISABLE_SERVER_SIDE_CURSORS` ved Neon sin pooled tilkobling.
- Lint gir ingen funn. Ingenting er committet eller pushet.

### Åpne punkter
- Føre publisering inn i endringsloggen i PRD-en (§12), hvis brukeren godkjenner.
- Sette opp Vercel og Neon i en egen story etter må-ha.

## 2026-11-08 kl. 12:59 — mounia.tech03

### Oppgave
Gjøre Vercel til publiseringsløsningen: oppdatere PRD og arkitektur, beholde Django hvis det fungerer, bruke PostgreSQL ved publisering, og avklare alle nødvendige tekniske valg før epics og stories. Enkel MVP og fristen først. Ingen subagenter, ingen commit eller push.

### Plan
- `bmad-prd` og `bmad-architecture` i oppdateringsmodus, med kontrollen i hovedtråden.
- Sjekke dokumentasjonen til Vercel og Neon på nettet.

### Resultat
- Django beholdes. Ifølge dokumentasjonen kjører Vercel Django uten ekstra oppsett, men det er ikke testet med en faktisk publisering ennå.
- PRD-en:
  - nytt DR-10 (publisering på Vercel) og SM-9 (den publiserte versjonen virker);
  - FR-4, NFR-1, NFR-3, NFR-8, NFR-9, DR-1, DR-9, visjonen, ikke-målene, MVP-omfanget og sammendraget er oppdatert;
  - ny rad i endringsloggen (§12), og addendum §2 har fått et avsnitt om publisering.
- Arkitekturen:
  - AD-13 og AD-15 er skrevet om, og AD-16 er ny;
  - AD-9, AD-12, konvensjonene, stakken, mappestrukturen, diagrammet og de utsatte punktene er oppdatert;
  - lint gir ingen funn, og spinen har status `final`.
- Tekniske valg:
  - Vercel Hobby i regionen fra1, og Neon PostgreSQL (gratis) i Frankfurt;
  - bare `main` publiseres, og det finnes ingen forhåndsvisninger;
  - eieren kjører migreringer og testdata fra egen PC med den direkte databaseadressen;
  - `psycopg[binary]` 3.3.8, ingen `pyproject.toml`, og Ruff leser `ruff.toml`.
- Ingenting er committet eller pushet.

### Åpne punkter
- I første story: publisere prosjektskjelettet og sjekke kontogrensene (Vercel-appen i GitHub-organisasjonen og forfatterkontrollen i Hobby-planen).
- Ved commit: fylle inn commit-hashen i endringsloggen i PRD-en (§12).
- Valgfritt: nevne den publiserte adressen i sensorflyten i EXPERIENCE.md (Flow 2).

## 2026-11-08 kl. 13:10 — 

### Oppgave
Kontrollere PRD, arkitektur og Vercel-planen, sjekke at alt er klart for epics og stories, og committe og pushe hvis alt er i orden. Oppdatere arbeidsloggen ved behov. Ingen subagenter og ingen unødvendige endringer.

### Plan
- Kontroller i hovedtråden: lint av spinen, status på PRD, spine og UX-spinene, ID-er og kryssreferanser, git-status og personvern.
- Deretter commit av PRD og arkitektur, commit-hashen inn i endringsloggen i PRD-en (§12), og commit av arbeidsloggen.

### Resultat
- Kontrollene er bestått:
  - lint av spinen gir ingen funn, og spinen har 16 beslutninger med Binds, Prevents og Rule;
  - PRD, spine, DESIGN.md og EXPERIENCE.md har status `final`;
  - ID-ene i PRD-en er komplette (36 FR, 11 NFR, 10 DR, 9 SM og 6 AG), og alle referanser i PRD, spine og addendum peker på ID-er som finnes;
  - Vercel-planen er lik i PRD-en (DR-10), addendumet og spinen (AD-13, AD-15 og AD-16);
  - personvernsjekken fant ingen treff.
- Alt er klart for epics og stories. De utsatte punktene i spinen og spørsmålene i PRD §10 blokkerer ikke dette steget.
- Commits: `21cd020` Oppdater PRD og arkitektur for publisering på Vercel, `e6840f2` Fyll inn commit i endringsloggen i PRD-en og `a93803d` Oppdater arbeidsloggen med Vercel-publiseringen, pushet til GitHub sammen med denne loggen.
- Lukket i `issues.md`: commit-hashen i endringsloggen i PRD-en.

### Åpne punkter
- Ingen nye. Punktene fra tidligere i dag står fortsatt i `issues.md`.
