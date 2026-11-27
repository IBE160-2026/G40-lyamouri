# Story 2.7: vis bestilling og tillit på produktsiden

## 2026-11-27 kl. 13:06 — Mounia-03

### Oppgave
Starte BMAD story 2.7 («Show what to order and whether to trust it on the product screen») etter prosjektkrav, arkitektur, sensorveiledning og rutinene fra Opus: bygge og teste selvstendig, bruke alle fire uavhengige skrivebeskyttede granskere i BMAD Code Review, mutasjonstesting og skjermtester, dokumentere prompter, beslutninger, modellbruk, KI-arbeid, tester og funn fortløpende, kontrollere dokumentasjon og testtall mot faktiske kjøringer, og ikke committe eller pushe uten godkjenning.

### Plan
- Spesifikasjon: [spec-2-7-…](../../_bmad-output/implementation-artifacts/spec-2-7-show-what-to-order-and-whether-to-trust-it-on-the-product-screen.md), godkjent med beslutning 1–4 og beholdt samlet (ca. 2 100 tokens).
- Bygge inline (underagenter bare til de fire granskerne): laster, produktside, beslutningstekster, «–», maler og stilark, tester med verdier fra regnearket og mockupen.
- Mutasjonstest før og etter review, skjermmålinger i hodeløs Chrome, BMAD Code Review med fire granskere, triage, dokumentasjon.

### Resultat
- Gren `story/2-7-show-what-to-order-and-whether-to-trust-it-on-the-product-screen` fra `0116aaf`. Etter brukerens godkjenning av personvernskanning og tre commits: koden og testene i `a6a69e6`, spesifikasjonen og dokumentene (med README om `PROGNOSE_LAN_HOST`) i `9297674`, og denne loggen med `issues.md` i en egen commit. Brukeren godkjente deretter push og PR: grenen er pushet over SSH, PR #44 har en kommentar med alle 29 funnene (6 rettet i `a6a69e6`, 1 utsatt, 14 avvist), CI-kjøring nr. 82 (1059 tester og Ruff) og Windows-kjøring nr. 22 passerte på `ded99bb`, og PR #44 er flettet som `5844e51` (kl. 14.38, foreldre `0116aaf` og `ded99bb`). CI-kjøring nr. 83 på `main` passerte (1059 tester). Sprint-status har story 2.7 som `done`. Fletteloggen i PR #45 er flettet som `3a3319a` (CI-kjøring nr. 84 på PR-en og nr. 85 på `main`, 1059 tester). Sesjonseksporten `sessions/2-7-2026-11-27.txt` er maskert og kontrollert mot dokumentene, to avvik er rettet (se QA-loggen), og den siste dokumentasjons-PR-en samler eksporten og rettelsene.
- Nytt: `web/company_data.py` (laster, fire spørringer), `explanation/decision.py`, `/produkter/<varenummer>/` med `product.html`, `_product_list.html` og `_trust_label.html`, «–» i `display.py`, to funksjoner i `web/queries.py`, stilark for to/én kolonne og panelene, tre nye testfiler og utvidede eksisterende tester.
- Tester lokalt: 1058 består og 1 hoppes over (Docker), opp fra 960. `ruff check`, `ruff format --check` og `makemigrations --check` er rene. CI-kjøringene har 1059 tester (Docker-sjekken kjører i CI).
- Mutasjoner: 50 før review (fire overlevde, én traff ikke, én ekvivalent mutant) og 54 etter; alle fanget unntatt den ekvivalente.
- BMAD Code Review (4 granskere, skrivebeskyttet, filhash identisk før og etter): 29 funn i 21 grupper, 6 rettet, 1 utsatt (innstillingsrad utenfor FR-20-områdene, `deferred-work.md`), 14 avvist.
- Skjermmåling i hodeløs Chrome 120 (gammel modus): 8 størrelser × 6 produkter, ingen sidelengs rulling; ved 1366 × 640 er mengden, merket og radene synlige uten rulling (høyest 431 px av 640). Ikke Safari og ikke ekte telefon.
- Modell: Sonnet 5.5 bekreftet for byggingen; brukeren oppga ikke noe ønsket nivå, økta viser ikke noe nivå, og modellen granskerne kjørte på (underagenter av typen `general-purpose`) er ikke bekreftet.
- Dokumentert: spesifikasjonen (`done`), statustabellen (FR-25 delvis bygd m.fl.), QA-loggen (3 oppføringer), KI-styringsloggen (tilfelle 44), arbeidsloggen, `deferred-work.md`, `sprint-status.yaml` (story 2.7 `review`). Én feil i eget utkast rettet før commit: varselet om gamle data finnes i seed-dataene (Parasoll 2 m, 20015).

- Brukerens tester ble meldt etter at hovedøkta var logget (Safari på Mac: 10012, 10040, 20015, 390 og 320 px, hoppelenke, fokusring, 404; ekte iPhone 13: A, 10012, 10040, 404) og er ført i QA-loggen; brukeren bekreftet senere også 820 × 1180 (10012, 10040, 20015) og 404 som Testbedrift B mot 10012. README forklarer nå `PROGNOSE_LAN_HOST` og `DisallowedHost`, og Wi-Fi-adressen er maskert til `172.20.10.x`. iPhonen fikk først `DisallowedHost`, løst med `PROGNOSE_LAN_HOST` på startkommandoen uten kodeendring.

### Åpne punkter
- Safari-versjon, macOS- og iOS-versjon og Testbedrift B på iPhonen er ikke meldt av brukeren og står ikke som oppgitt i QA-loggen. Safari ved 1366 × 768 i den responsive visningen er meldt som bestått (10012 og 20015).
- Story 2.8: bruke lasteren og `build_overview` i listen og koble produktnumrene med resultatene; «–» i listen.
- Story 2.9: kolonneetiketten «Uke 1 · uke 46» i `display.py` (flyttet fra 2.7).
- Story 2.11: fremdriftslinjen og forrige/neste-lenkene på produktsiden.
- Story 3.1: stoppe en innstillingsverdi utenfor FR-20-områdene før den lagres (utsatt EC-1: 500 på alle produktsider i bedriften).
