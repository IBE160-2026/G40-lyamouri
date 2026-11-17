# Teknologinotat: slik er technology.md tilpasset Prognose

**Til:** læreren i IBE160
**Fra:** G40-lyamouri
**Dato:** 17. november 2026

## Kort fortalt

`technology.md` beskriver en stor nettplattform for et forlag:
- FastAPI og Next.js bak en Caddy-proxy;
- PostgreSQL, Redis og Supabase Storage;
- Docker Compose lokalt og Railway i produksjon;
- betaling, e-post og en KI-assistent.

Prognose er en MVP for én innkjøpsansvarlig per bedrift, med frist 1. desember 2026. PRD-en krever:
- én app med én database (NFR-9);
- installasjon fra README-en på macOS og Windows på høyst 15 minutter (SM-2);
- at appen virker uten nett lokalt (NFR-1);
- publisering på Vercel (DR-10).

Vi har derfor tatt med mønstrene og verktøyene som passer, og latt resten ligge. Bindende valg står i arkitekturspinen (`ARCHITECTURE-SPINE.md`) i samme mappe.

## Tatt med

| Fra technology.md | I Prognose |
|---|---|
| Python med uv og låsefil | Python 3.13 med uv, `pyproject.toml` og `uv.lock`. uv installerer også riktig Python for sensor. |
| pytest | pytest med pytest-django. Referanseeksemplene E1–E30 leses fra regnearket. |
| PostgreSQL | PostgreSQL 18 både lokalt og publisert. Vi valgte PostgreSQL som en mer langsiktig løsning enn SQLite. |
| Docker Compose lokalt | Bare for databasen: én `compose.yaml` med PostgreSQL 18.7, uten passord og bare tilgjengelig fra egen maskin. |
| Migrering før publisering, seed-data hvis databasen er tom | Byggesteget på Vercel kjører migreringer og laster seed-data bare i en tom database. |
| Null konfigurasjon lokalt og reserve når en tjeneste mangler | Appen kjører lokalt uten nøkler. Den valgfrie lokale språkmodellen faller tilbake til malteksten, og testene bruker en falsk modell. |
| Appen nekter å starte uten hemmelighet i produksjon | På Vercel stopper appen hvis `SECRET_KEY` eller `DATABASE_URL` mangler. |
| `.env.example` med forklaring | Lister alle valgfrie variabler og om de er hemmelige. |

## Tilpasset

| Fra technology.md | I Prognose | Hvorfor |
|---|---|---|
| FastAPI | Django 5.2 LTS | Innlogging, økter, CSRF-vern, skjemaer og migreringer er innebygd. Med FastAPI måtte vi bygget dette selv. Forskningsrapporten ga Django 83 poeng og FastAPI 65. |
| Next.js, React, Tailwind og shadcn/ui | Django-maler med ren HTML og CSS | UX-en krever ren HTML uten UI-bibliotek, og at alt virker med lenker og skjemaer uten JavaScript. |
| Recharts | Grafen tegnes som SVG på serveren | Den godkjente mockupen er SVG uten skript. Da trengs verken grafbibliotek eller JavaScript, og markørene kan testes. |
| Supabase Postgres | Neon Postgres, gratisplan | Supabase pauser gratisprosjekter etter omtrent en uke uten bruk, og da kan sensor møte en død adresse. |
| Railway og en egen `production`-gren | Vercel fra `main` | PRD-en (DR-10) binder Vercel og gratisplaner. |
| Hele appen i Docker | Bare databasen i Docker | Appen kjører med uv, så det finnes én måte å kjøre den på, og kommandoene er like på macOS og Windows. |

## Droppet

- **Caddy, Redis og Supabase Storage:** én prosess og én database er nok, og appen har ingen filer.
- **Betaling, e-post og regnskap (Stripe, Vipps, Resend, Fiken):** utenfor MVP-en.
- **OpenRouter og andre KI-tjenester:** AG-5 forbyr eksterne KI-tjenester. KI lager aldri tall i Prognose.
- **JWT og rate limiting:** innloggingen bruker økter (FR-1), og testinnloggingene står åpent i README-en.
- **Funksjonsflagg:** bør-ha-funksjonene er enten bygget eller ikke. Det eneste flagget er bryteren for den lokale språkmodellen (FR-28).
- **Backup, overvåking og Cloudflare:** demoen har bare syntetiske data, og en bevisst tilbakestilling gjenoppretter den (DR-4).
- **Playwright og Vitest:** ikke i v1. Djangos testklient dekker hovedflyten og isolasjonen mellom bedriftene.

## Sikkerhet for dataene

- Publisering sletter eller overskriver aldri data.
- Byggesteget kjører bare migreringer som legger til. Alt annet stopper byggingen, og eieren bestemmer selv.
- Seed-data lastes bare inn i en tom database.
- Bare en tilbakestilling som brukeren bekrefter, sletter data.

## Testet

17. november 2026 ble PostgreSQL 18.7 testet med Docker Compose på en Mac (macOS 15.6.1, Apple M1, 8 GB):
- databasen var klar på 17 sekunder første gang og 3 sekunder ved omstart;
- tilkoblingen fungerte fra Python og Django, og æ, ø og å kom riktig tilbake;
- dataene var der etter omstart;
- PostgreSQL brukte 30 MB minne.

Oppstart uten nett og oppsett på Windows er ikke testet ennå. Detaljene står i `docs/qa-logg.md`.
