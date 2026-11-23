# Story 1.5 – referanseregnearket som fasit

## 2026-11-23 kl. 16:07 — Mounia-03

### Oppgave
Lese prosjektreglene, sprintplanen, story 1.5 og de relevante BMAD-dokumentene, bekrefte at `main` var ren og synkronisert med GitHub, og starte story 1.5 («Reference spreadsheet as the answer key») etter BMAD og sensorveiledningen. Claude skulle:
- følge det godkjente omfanget, gjenbruke eksisterende arbeid og jobbe selvstendig;
- bruke subagenter bare til gjennomganger;
- be om godkjenning før commit, push og fletting;
- ikke lese utenfor prosjektmappen eller eksponere hemmeligheter.

Økten gikk over 22. og 23. november, med to stopp for bruksgrensen. Den omfattet også BMAD Code Review, to kontroller i Excel, eksporten og denne loggen.

### Plan
- `bmad-build` med den fulle ruten, på grenen `story/1-5-reference-spreadsheet-as-the-answer-key`, laget fra `main` (`da87fd7`). Spesifikasjonen er [spec-1-5-reference-spreadsheet-as-the-answer-key.md](../../_bmad-output/implementation-artifacts/spec-1-5-reference-spreadsheet-as-the-answer-key.md), og brukeren godkjente den med om lag 2 700 tokens, over den anbefalte grensen på 1 600.
- Epic-1-konteksten var formelt utdatert av samme grunn som i story 1.4, så Claude brukte den som den var. Subagenter ble bare brukt til BMAD Code Review, og byggingen og Blind Hunter i byggeøkten ble gjort uten subagenter.
- Før byggingen bestemte brukeren at E30 står som i PRD-en, at regnearket fører «lav», og at spørsmålet om varselets virkning på tillitsmerket flyttes til story 5.2 ([tilfelle 33](../../docs/ki-styringslogg.md#33-e30-og-tillitsmerket-22-november-2026)).
- Claude skrev regnearket med openpyxl fra et skript i den midlertidige mappa. Det samme skriptet regnet ut alt på nytt med en uavhengig utregning av R-1 til R-17, og regnet ut formlene i `checks` med avrundingen i Excel. Skriptet er ikke committet, fordi regnearket er den eneste fasiten (AD-17).
- Gjennomganger: Blind Hunter i byggeøkten, og BMAD Code Review med fire uavhengige subagenter på PR #16 (D-8).

### Resultat
- **Regnearket** `reference/reference-examples.xlsx` har:
  - 52 tilfeller: E1–E30 fra PRD §5.7, med én rad per variant, og de fire FR-21-variantene;
  - 11 regeltestprodukter: seriene fra E1–E4, E7–E10 og E15–E19, med E8-produktet og Strøsand 25 kg i Testbedrift A;
  - arket `checks` med 754 rader, der 401 kontrollerer en verdi med en synlig formel;
  - `check_log` med fire kontroller.

  [`reference/README.md`](../../reference/README.md) dokumenterer arkene, kolonnene og notasjonen.
- **Leseren og testene:** `tests/answer_key.py` og 19 tester i `tests/test_reference_spreadsheet.py`.
  - Testene leser eksemplene, FR-21-tabellen og FR-20-standardene fra PRD-en, og Strøsands 12 siste uker fra mockupen.
  - De sammenligner inndataene med kildene og tallene i kontrollformlene med inndataene.
- **Kontrollene:**
  - Ingen verdi avvek fra PRD §5.7 i den uavhengige utregningen.
  - Brukeren kontrollerte regnearket i Excel for Mac 16.78 to ganger og lukket det uten å lagre: 376 av 376 før BMAD Code Review og 401 av 401 etter. Fila beholdt sin SHA-1 begge gangene.
  - 50 feil som ble lagt inn én om gangen, ble alle fanget, og 151 tester og Ruff passerte.
- **Feil i KI-generert kode:**
  - Claudes egne kontrollformler for varslene ga feil svar for historikker kortere enn 12 uker. Skriptet fant feilen før fila ble skrevet.
  - Blind Hunter i byggeøkten fant 13 funn: 4 ble rettet og 9 avvist.
- **BMAD Code Review:** 61 funn, med kommentaren i [PR #16](https://github.com/IBE160-2026/G40-lyamouri/pull/16#issuecomment-7104814518). Brukeren tok tre beslutninger:
  - nye tester for inndataene;
  - å rette E12 i PRD §5.7 til «no old-data warning», med en rad i §12;
  - å beholde toleransen på 0,0005.

  21 funn ble rettinger. 20 er gjort i commitene, og den siste er de åpne punktene i `issues.md` under. 2 funn ble utsatt (`deferred-work.md`), og 5 ble avvist. Tilfelle 34 i KI-styringsloggen og QA-loggen beskriver dem.
- **Commits på grenen:**
  - `0ae5920`: regnearket, testene og spesifikasjonen;
  - `99b73bc`: dokumentene;
  - `dd4a269`: rettingene fra BMAD Code Review;
  - `7e62aa3`: dokumentene etter reviewen;
  - `024b204`: eksporten.

  Brukeren godkjente hver av dem før commit og push. CI-kjøring nr. 21 passerte på `99b73bc`, og nr. 22 på `7e62aa3`.
- **Eksporten:** [1-5-2026-11-23.txt](sessions/1-5-2026-11-23.txt) dekker økten etter `/clear`. Den er maskert: 25 stier til prosjektmappa ble `<repo>`, og 2 stier til den midlertidige mappa ble `<tmp>`. Noen av stiene var brutt over to linjer, og maskeringen beholdt bruddene. Kontrollen etterpå fant ingen lokale stier, brukernavn, e-poster, nøkler eller tokens.
- **`issues.md`:** punktet om regnearket (fra 3. november) og punktet om E30 (fra 21. november) er løst. Punktet om spørsmål 4 i PRD §10 har fått en merknad, og fem nye punkter står under.
- **Ikke gjort:** flettingen av PR #16 venter på brukerens godkjenning.

### Åpne punkter
- Story 1.6: den eneste leseren av notasjonen i regnearket («S», «S2», «none», listene og flaggene) ligger i `tests/answer_key.py`. Bestem hvor den felles leseren skal ligge, så generatoren ikke kopierer den (BH-31, `deferred-work.md`).
- Story 1.7: skjematesten sjekker ikke grensene i FR-20. Når `forecasting/settings.py` finnes, bør testen sjekke innstillingene i regnearket mot grensene der (BH-3).
- Story 5.1: ukeprognosene for E14 uten sesongjustering, den «flate» siden av siste rad i FR-21-tabellen, er ikke ført i regnearket. Før dem, for eksempel på E30 (off) (BH-23, `deferred-work.md`).
- Story 5.2: E30 kan ikke vise at varselet om sesongmønster senker tillitsmerket, fordi E14-dataene har 8 gyldige uker. Vurder et eksempel i stil med E29: 104 uker med sesongmønster, «middels» uten og «høy» med sesongjustering. Det krever en endring i PRD-en (tilfelle 33).
- Story 5.2: R-17 gir Strøsand 25 kg indeksen 1,5735 for ukenummer 42 på grunn av den uvanlige uka. Når FR-36 bygges, får produktet derfor et varsel om sesongmønster som mockupen ikke viser, og varselet forsvinner når uvanlige uker holdes utenfor. Avgjør om det er greit, eller om R-17 skal regne uten de uvanlige ukene.
