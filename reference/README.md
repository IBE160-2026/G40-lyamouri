# Referanseregnearket

[`reference-examples.xlsx`](reference-examples.xlsx) er fasiten for Prognose (DR-3, AD-17). Testene leser inndata og forventede verdier herfra med openpyxl, så ingen forventet verdi står i testkoden. Fra story 1.6 leser seed-generatoren også seriene og lagerbeholdningen til regeltestproduktene herfra (AD-15). Sensor kan sammenligne tallene på skjermen med det samme regnearket.

Denne fila beskriver arkene, kolonnene og notasjonen. [`tests/answer_key.py`](../tests/answer_key.py) leser regnearket slik det står her. [`tests/test_reference_spreadsheet.py`](../tests/test_reference_spreadsheet.py) feiler hvis et tilfelle, en variant, et produkt, en forventet verdi eller en kontroll mangler eller er feil. Testene sammenligner også seriene og innstillingene med PRD §5.7, Strøsand 25 kg med mockupen og tallene i kontrollformlene med inndataene.

## Arkene

| Ark | Innhold |
|---|---|
| `about` | En kort forklaring på norsk. |
| `cases` | Ett tilfelle per rad: referanseeksemplene E1–E30 i PRD §5.7, med E11 a og b, E18 a og b og E29 a–g, og de fire variantene som FR-21 nevner i tillegg. |
| `products` | Regeltestproduktene, bygd av seriene i E1–E4, E7–E10 og E15–E19, og demoproduktet Strøsand 25 kg (FR-3, UX-DR46). |
| `checks` | Kontrollen: hver forventet verdi regnet ut på nytt med en synlig formel. |
| `check_log` | Når kontrollen ble gjort, av hvem, hva den dekket, hvordan og med hvilket resultat. |

Rad 1 i `cases`, `products`, `checks` og `check_log` har kolonnenavnene. I `checks` står også sammendraget i J1:K3, og `about` begynner med en tittel. `cases` og `products` inneholder bare verdier og ingen formler, fordi openpyxl ikke regner ut formler. Leseren stopper hvis den finner en formel noe sted i de to arkene.

## Tilfellene

- Et tilfelle er én salgsserie med ett sett innstillinger. Et eksempel i PRD §5.7 som sammenligner innstillinger, serier eller produkter, har én rad per variant, med varianten i parentes: «E8 (included)» og «E8 (excluded)», «E12 (95)» og «E12 (96)», «E13 (E4)» og «E13 (E6)», «E24 (A)» og «E24 (B)», og «E30 (off)» og «E30 (on)». E9, E15, E16, E18 b og E19 har også én rad for hver innstilling for uvanlige uker. Til sammen er det 52 tilfeller.
- `case` er tilfellets navn. `example` er ID-en i PRD §5.7, og `rule` og `priority` er regelen og prioriteten der. `prd_input` og `prd_result` siterer inndata og forventet resultat i PRD-tabellen ordrett. Testene sammenligner dem med PRD-en, så et eksempel som endres der, må også endres her.
- FR-21-variantene heter «FR-21 a» til «FR-21 d» og har `example` «FR-21». `prd_input` siterer eksempelet i tabellen i FR-21, for eksempel «E1 with window 4 instead of 3». PRD-en gir ikke verdiene, så de er regnet ut for hånd og kontrollert i `checks`. Story 3.2 leser dem herfra.
- Der PRD §5.7 ikke gir en konkret serie, er serien valgt slik:
  - E5 og E6: «100, 100, 100», som gir ukeprognosen 100.
  - E11 b: «10, 10, 10, 30, 10, 10, 10, 30, 10, 10, 10, 10», der uke 4 og 8 er uvanlige.
  - E12: 95 uker med 10 og så 9 utsolgte uker, og 96 uker med 10 og så 8 utsolgte uker.
  - E24: A «10, 10, 10» og B «20, 20, 20», begge uten lager.
  - E29 b: 12 uker med 10.
  - E29 c: 53 uker med 10, så 30, så 50 uker med 10.
  - E29 d: 98 uker med 10, så 30, så 5 uker med 10.
  - E29 f: 50 uker med 10, 3 utsolgte uker og 51 uker med 10.
  - E29 g: 50 uker med 10, 5 utsolgte uker og 49 uker med 10.
- E30 har 8 gyldige uker, så R-16 gir «lav» både med og uten varselet om sesongmønster. Brukeren bestemte 22. november 2026 å beholde E30 slik PRD-en har det og flytte spørsmålet om et eksempel som viser varselets virkning på tillitsmerket, til story 5.2.
- E12 sa «8 weeks: no warning», men uke 97–104 er utsolgte uker i de siste 12 ukene, så varselet om utsolgte uker er aktivt. PRD-en ble rettet til «no old-data warning» 23. november 2026 etter BMAD Code Review, med en rad i PRD §12.

## Salgsserien

- `sales` lister ukene i tidsrekkefølge, skilt med komma og mellomrom, for eksempel «20, 22, S, S2, 21, 23». Posisjon 1 er den eldste uka, og den siste posisjonen er siste registrerte uke. Lange serier er skrevet helt ut.
- Et heltall er antall solgte enheter i en gyldig uke.
- «S» er en utsolgt uke med 0 solgte enheter, og «S2» en utsolgt uke der 2 enheter ble solgt. Ingen regel bruker salget i en utsolgt uke (FR-15), men grafen viser det.

## Innstillingene

Hver rad i `cases` har alle innstillingene, også når de er standardverdiene i FR-20.

| Kolonne | Verdier |
|---|---|
| `method` | `moving_average` eller `exponential_smoothing` |
| `window` | vinduet, et heltall |
| `smoothing_factor` | glattingsfaktoren, for eksempel 0.3 |
| `scenario_percentage`, `safety_margin` | hele prosent: 10 betyr 10 % |
| `unusual_weeks_setting` | `included` eller `excluded` |
| `seasonal_adjustment` | `on` eller `off` |
| `cycle_length` | 52, eller 4 i E14, E25–E27 og E30. Med en syklus på 4 uker har posisjon p ukenummer ((p − 1) mod 4) + 1, som i PRD §5.7 |
| `stock_on_hand` | lagerbeholdningen. Den er 0 der eksempelet ikke oppgir noen, fordi ingen av tilfellets forventede verdier avhenger av den |
| `product_number` | bare i E24, der produktnummeret avgjør rekkefølgen |

## De forventede verdiene

- **Tomt felt:** tilfellet sier ingenting om verdien, og testene sjekker den ikke.
- **«none»:** forventet fravær, for eksempel ingen prognose, ingen uker dekning, ingen uker i lista eller ingen varsler.
- **Tall:** tallceller med presisjonen i PRD §5.7, for eksempel 14.333. Et beregnet tall stemmer når det avviker med mindre enn 0,0005. En ny verdi føres derfor med så mange desimaler at den ligger innenfor 0,0005 av den eksakte verdien, for eksempel 0.0675 og ikke 0.068. En tallcelle viser ikke nuller til slutt, så 12.900 i PRD-en står som 12.9.
- **Visningstekst:** kolonnene som slutter på `_shown`, er tekst med desimalkomma, for eksempel «14,3» og «–», og sammenlignes eksakt.
- **Lister:** verdiene er skilt med komma, for eksempel «4, 5» for posisjoner og «12, 12.9, 12.33» for tall, med desimalpunktum som i PRD-en.
- **Flagg:** «yes» eller «no».
- **Varsler:** `warnings` lister alle de aktive varslene etter R-15, i rekkefølgen der, når tilfellet sier noe om varsler eller tillitsmerket. PRD §5.7 nevner bare varselet som eksempelet tester, så E11 a har for eksempel både `stockout_weeks` og `insufficient_data`. `seasonal_pattern` (FR-36, bør-ha) står bare i bør-ha-tilfellene.

| Kolonne | Betydning |
|---|---|
| `valid_weeks` | antall gyldige uker (R-1) |
| `unusual_weeks` | posisjonene til de uvanlige ukene (R-10) |
| `level_shift_weeks` | posisjonene til ukene med nytt nivå (R-11) |
| `calculation_weeks` | antall uker brukt i beregningen (R-2) |
| `levels` | nivåene i eksponentiell glatting, ett per uke brukt i beregningen (R-4) |
| `week_number_means`, `mean_of_means`, `seasonal_indices` | snittet per ukenummer, snittet av snittene og sesongindeksene (R-14 steg 1 og 2) |
| `adjusted_sales_used` | det sesongjusterte salget i ukene som det glidende gjennomsnittet bruker (R-14 steg 3) |
| `base_forecast`, `base_forecast_shown` | grunnprognosen, og slik den vises (R-3, R-4, R-9) |
| `week_forecasts` | ukeprognosene for uke 1, 2 og 3 (R-5, R-14) |
| `normal`, `optimistic`, `pessimistic` | scenarioene for uke 1 (R-7) |
| `order_unrounded`, `order_unrounded_shown` | ukeprognosen for uke 1 pluss sikkerhetsmarginen minus lagerbeholdningen, før avrundingen, og slik utregningen av bestillingsmengden viser den (R-8, R-9, FR-12) |
| `suggested_order_quantity` | foreslått bestillingsmengde (R-8, R-9) |
| `optimistic_order_unrounded`, `optimistic_order_quantity`, `pessimistic_order_unrounded`, `pessimistic_order_quantity` | bestillingsmengden per scenario (FR-13) |
| `weeks_of_cover`, `weeks_of_cover_shown` | uker dekning, og slik de vises (R-12, R-9) |
| `order_soon` | om produktet skal bestilles snart (R-12) |
| `overview_position` | plassen i produktoversikten blant tilfellene i samme eksempel (R-12) |
| `overstock_note` | merknaden om overlager (FR-14) |
| `weeks_since_latest_valid` | uker fra siste gyldige uke til siste registrerte uke (FR-18) |
| `seasonal_adjustment_used` | om sesongjusteringen ble brukt for produktet (R-14 steg 4) |
| `seasonal_pattern` | om produktet har sesongmønster (R-17) |
| `warnings` | de aktive varslene: `stockout_weeks`, `unusual_weeks`, `level_shift`, `old_data`, `insufficient_data` og `seasonal_pattern` (R-15) |
| `confidence_label` | tillitsmerket: `lav`, `middels` eller `høy` (R-16) |

## Regeltestproduktene

Hvert produkt bruker standardinnstillingene i FR-20, slik de er etter `load_seed`. `product` er eksempelet produktet har serien fra, eller navnet på demoproduktet. `company` er testbedriften (UX-DR46), og `examples` er eksemplene produktet viser. De forventede verdiene er dem FR-3 krever: `base_forecast`, `suggested_order_quantity`, `unusual_weeks`, `level_shift_weeks`, `warnings` (R-15 punkt 1–5) og `confidence_label`.

| Produkt | Bedrift | Lager | Eksempler |
|---|---|---|---|
| E1 | B | 5 | E1, E2, E3, E4 |
| E7 | B | 0 | E7, E17, E29 a |
| E8 | A | 50 | E8 |
| E9, E10, E15, E16, E18 a, E18 b, E19 | B | 0 | eksempelet med samme navn |
| Strøsand 25 kg | A | 5 | E1, E3, E4, E13 |

- E1–E4 bruker samme serie, og E17 bruker serien i E7 med eksponentiell glatting. Innstillingene gjelder hele bedriften, så ett produkt viser begge.
- E8-produktet har 50 på lager. Behovet på 45,1 er da dekket, så produktet kommer ikke under «Bestill snart», og «Denne uken» viser fortsatt 4 produkter som bør bestilles snart (UX-DR46).
- Strøsand 25 kg har 104 uker. Posisjon 93–104 er ukene i mockupen: «11, 13, 12, 14, S, S2, 13, 15, 31, 16, 12, 15». De 92 ukene før gjentar serien i E1. Med uke 45 i 2026 som siste registrerte uke (UX-DR46) er posisjon 97 og 98 de utsolgte ukene 38 og 39, og posisjon 101 er den uvanlige uka 42. Grunnprognosen blir 14,3 og bestillingsmengden 11, som i E1 og E4.
- Story 1.6 bestemmer produktnumrene, navnene på de andre produktene og mønsterproduktene, for eksempel Snøskuffe aluminium.
- R-17 (bør-ha) ville gitt ukenummer 42 hos Strøsand 25 kg indeksen 1,5735 på grunn av den uvanlige uka. Når FR-36 bygges, får produktet derfor også varselet om sesongmønster. Varselet er ikke med i `warnings`, som følger må-ha-reglene. Spørsmålet er et åpent punkt for story 5.2.

## Kontrollen

- `checks` har én rad per kontrollert verdi:
  - `sheet` og `key` peker på tilfellet eller produktet, og `value` er kolonnen.
  - `item` er plassen i en liste, en uke, et varsel, en periode med nytt nivå som «4, 5, 6», eller «other» for de andre ukene.
  - `recorded` er verdien i fasiten. For visningstekst står tallet, for eksempel 14.3 for «14,3». For en uke, en periode eller et varsel står det om den er med i fasiten (`TRUE` eller `FALSE`).
  - `recalculated` er en synlig formel som regner verdien ut på nytt, og `match` viser om de stemmer: `=E5=F5` for tekst, flagg og heltall, og `=ABS(E5-F5)<0.0005` for desimaltall.
  - `note` forklarer formelen, for eksempel hvilke uker R-10 sammenligner med.
- Rader uten `recorded` og `match` er mellomregninger. `r10_flag` viser om R-10 flagger en uke. I en lang serie står bare de flaggede ukene, og én rad viser at ingen av de andre ukene kan flagges.
- R-11 avgjøres i formler med én gjennomgang:
  - En periode med nytt nivå avgjøres i sin tredje uke, når uka er flagget og de to foregående gyldige ukene er uvanlige.
  - En flagget uke forblir uvanlig med mindre de to foregående gyldige ukene er det.
  - Hver liste med uker har en rad «other», som viser at ingen annen uke er uvanlig eller hører til et nytt nivå.
  - Varslene om uvanlige uker og nytt nivå viser til disse radene.
- Sammendraget står til høyre i arket: antall kontroller som stemmer (K1), antall kontroller (K2) og om alle stemmer (K3). Formlene har engelske funksjonsnavn i fila, og Excel viser dem på språket til programmet, for eksempel AVRUND for ROUND i norsk Excel.
- `check_log` har én rad per kontroll. Kolonnene er:
  - `date`: datoen som ISO-tekst, for eksempel «2026-11-23»;
  - `checked_by`: hvem som kontrollerte;
  - `scope`: hva kontrollen dekket;
  - `method`: hvordan kontrollen ble gjort;
  - `result`: resultatet. Den siste raden må si «N of N checks match», med N som antall kontroller i `checks`, og testene sjekker det.
- Kontrollene i `check_log`:
  1. Claude Code regnet ut hvert tilfelle på nytt med et uavhengig skript for R-1 til R-17. Formlene i `checks` ble regnet ut med avrundingen i Excel. Skriptet er ikke committet, fordi regnearket er den eneste fasiten. Ingen verdi avvek fra PRD §5.7.
  2. Brukeren Mounia-03 åpnet regnearket i Excel for Mac 16.78 23. november 2026 og lukket det uten å lagre. Excel regnet ut formlene selv, og sammendraget viste at alle 376 kontrollene stemmer.
  3. Etter BMAD Code Review ble `checks` utvidet med radene «other» og formlene for R-11. Claude Code regnet ut alle 401 kontrollene på nytt på samme måte, og ingen verdi avvek fra PRD §5.7.
  4. Mounia-03 åpnet den nye versjonen i Excel for Mac 16.78 samme dag og lukket den uten å lagre. Sammendraget viste at alle 401 kontrollene stemmer.

## Slik endres regnearket

- Ikke lagre regnearket i Excel. Excel skriver den lokale stien (`absPath`) og brukernavnet inn i fila, og testen for NFR-4 feiler da. Endre regnearket med openpyxl fra et skript, og hold `cases` og `products` fri for formler.
- Legg nye rader i `checks` til slutt i arket, og ikke sett inn eller slett rader midt i det. openpyxl flytter ikke referansene i formlene slik Excel gjør, så en formel ville da vist til feil rad.
- Etter en endring oppdateres de tilhørende radene i `checks`. Testene regner ikke ut formlene, så regnearket åpnes i Excel eller Numbers uten å lagre, og sammendraget i `checks` skal vise at alle kontrollene stemmer. Deretter får `check_log` en ny rad med dato, hvem, hva kontrollen dekket, metoden og resultatet («N of N checks match»), og `uv run pytest` skal passere.
- En forventet verdi som avviker fra PRD §5.7, regnes ut på nytt for hånd. Den siden som var feil, rettes, og en retting i PRD-en får en rad i PRD §12. Funnet føres i [QA-loggen](../docs/qa-logg.md) (AD-17, DR-9).
