# G40 — Mounia

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Medlemmer

- Flesche Mounia Lyamouri

## Kom i gang lokalt

Prognose er en Django-app som kjører på din egen PC med en lokal SQLite-database. Etter installasjonen trengs ikke nett.

Du trenger Python 3.13 og Git.

### macOS (Terminal)

```sh
git clone https://github.com/IBE160-2026/G40-lyamouri.git
cd G40-lyamouri
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_seed
python manage.py runserver --insecure
```

### Windows (PowerShell)

```powershell
git clone https://github.com/IBE160-2026/G40-lyamouri.git
cd G40-lyamouri
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py load_seed
python manage.py runserver --insecure
```

Stopper PowerShell `Activate.ps1`, kjør `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` i samme vindu og prøv igjen.

Åpne <http://127.0.0.1:8000/> i nettleseren, og stopp serveren med Ctrl+C. Neste gang holder det å aktivere det virtuelle miljøet og starte serveren.

- `load_seed` lager den hemmelige nøkkelen `.secret_key` første gang og endrer den aldri senere. Fila er git-ignorert. Testdataene kommer i en senere versjon.
- `--insecure` lar utviklingsserveren levere stilarket mens Djangos feilsøkingsmodus (DEBUG) er av, slik den er som standard. Bruk det bare lokalt.
- Valgfritt: kopier `.env.example` til `.env` (`cp .env.example .env` på macOS, `Copy-Item .env.example .env` i PowerShell) og sett `DEBUG=1` for å se Djangos feilsøkingssider lokalt.

### Tester og kodekontroll

Kjør dette før hver pull request, med det virtuelle miljøet aktivert:

```sh
python manage.py test
ruff check .
ruff format --check .
```

## Publisering

Prognose publiseres på Vercel i regionen `fra1` med en Neon PostgreSQL-database i Frankfurt, begge på gratisplaner. Bare `main` publiseres (se `vercel.json`). En push til en annen gren lager ingen publisering, så pull requester prøves lokalt.

Ett gruppemedlem eier Vercel-prosjektet og gjør dette:

1. Importer repoet i Vercel, gjerne med prosjektnavnet `prognose-g40`. Velg «Django» som Framework Preset: før den første pull requesten er flettet, har `main` ingen Django-kode, og da velger Vercel «Other» for alle senere publiseringer. Importen starter straks en publisering av dagens `main`, og den feiler fordi Django-koden ikke er flettet inn ennå. Den første feilen er forventet. Tillater ikke GitHub-organisasjonen Vercel-appen, publiserer eieren `main` med `npx vercel@65.12.1 deploy --prod` (krever Node.js) fra en egen, fersk klon av repoet, fordi Vercel CLI ikke leser `.gitignore` og ellers laster opp lokale filer som `.env` og `.secret_key`.
2. Legg til Neon under **Storage** (gratisplan, AWS Frankfurt, `eu-central-1`) og koble databasen til prosjektet. Da setter Vercel `DATABASE_URL` og `DATABASE_URL_UNPOOLED`.
3. Legg inn `SECRET_KEY` for **Production** under **Settings → Environment Variables**. Lag en ny verdi med `python -c "import secrets; print(secrets.token_urlsafe(50))"`.
4. Flett pull requesten inn i `main`, så publiserer Vercel den. Stopper Vercel publiseringen fordi en annen enn eieren står som forfatter av en commit, fletter eieren med en merge-commit.
5. Kopier verdien av `DATABASE_URL_UNPOOLED` fra Neon-databasen under **Storage**, og kjør migreringene mot Neon én gang fra egen PC. Kommandoene leser adressen fra utklippstavlen, så den havner ikke i skallhistorikken, og den gjelder bare for denne ene kommandoen. Lagre den aldri i `.env` eller en annen fil:
   - macOS: `DATABASE_URL="$(pbpaste)" python manage.py migrate`
   - Windows: `try { $env:DATABASE_URL = (Get-Clipboard -Raw).Trim(); python manage.py migrate } finally { Remove-Item Env:DATABASE_URL }`

   Gjør det samme etter hver fletting som legger til en migrering.
6. Sjekk produksjonsdomenet som står under **Domains** i Vercel-prosjektet, for eksempel `https://prognose-g40.vercel.app/`: forsiden og `/static/css/app.css` skal lastes, og `/helse/` skal svare `ok`. Grenadressen (`…-git-main-….vercel.app`) svarer «Bad Request (400)», fordi appen bare godtar produksjonsdomenet og adressen til hver enkelt publisering.

På Vercel er DEBUG alltid av. Appen henter vertsnavnene fra Vercels systemvariabler og stopper med en tydelig feilmelding hvis `SECRET_KEY` eller `DATABASE_URL` mangler.
