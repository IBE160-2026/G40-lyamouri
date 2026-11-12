# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G40 – G40-lyamouri |
| **PRD vurdert** | `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md` (status `final`, sist endret 2026-11-08, commit e6840f2) |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

Dette er en uvanlig sterk PRD. Den har en tydelig tese (tall som kan kontrolleres for hånd, og som sier fra når de ikke bør stoles på), regler med fasit, og en ærlig avgrensning. Risikoen ligger ikke i kvaliteten, men i størrelsen: Must-omfanget er stort for tiden som er igjen til 1. desember, og dokumentet er så langt at det blir en jobb i seg selv å holde det konsistent.

## 2. Dette fungerer godt

- **Regler og fasit.** §5 gir 17 regler (R-1 til R-17) og 30 referanseeksempler (E1–E30) med forventet resultat. Eksemplene tester også grensetilfeller, for eksempel «E5 gir 70, ikke 71» og «42 = 2 × 21, så ikke avvik» (E18a). Jeg regnet gjennom et utvalg (E2, E8, E14, E15, E16, E19, E21, E27), og de stemmer. Dette er det beste grunnlaget for testtilfeller en PRD kan gi.
- **KI under kontroll.** AG-1 til AG-6 og FR-28 sier at KI aldri lager tall, at språkmodellen er av som standard, at appen selv setter inn alle tall, og at malforklaringen vises i alle feilsituasjoner («ingen API-nøkkel, betalt tjeneste eller internett», FR-28). Kostnad, testmodus og usikre svar er dermed dekket uten at det er gjort til pynt.
- **Ærlig scope.** §7 lister bevisste utelatelser (ingen ledetid, ingen åpne ordrer, ingen trendmetode), og R-14 har en egen liste over kjente begrensninger. Sesongjustering er flyttet til Should med begrunnelse, og motmålene SM-C1–C3 hindrer at målene driver feil vei. Alle åtte `[ASSUMPTION]`-merkene står også i §11.

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet | sterk | Valg og avveininger er navngitt (Should-rekkefølge, Vercel, enkel sikkerhetsmargin). |
| Substans | sterk | Persona, regler og NFR-er er produktspesifikke og driver faktiske krav. |
| Strategisk sammenheng | sterk | Tesen «åpen, kontrollerbar og ærlig om tillit» styrer prioriteringen. |
| Testbarhet | sterk | Nesten alle Must-FR har testbare konsekvenser og E-referanser. Noen få unntak, se 4.2 og 4.4. |
| Scope og avgrensning | god | Eksplisitt, men Must er stort og Should er allerede «i fare» (§8.2). |
| Brukbarhet for neste fase | god | Glossar og ID-er er rene, men lengden og blandede prioriteringer gjør uttrekk tungt. |
| Formtilpasning | god | Passer et enbrukerverktøy med én reise. Prosesskrav (DR-5, DR-7, DR-9) fyller mye. |

## 4. Viktigste forbedringer

### 4.1 Must-omfanget er stort i forhold til fristen
- **Alvorlighet:** høy
- **Hvor:** §8.1 («All non-functional requirements, AI guardrails and delivery requirements in §6»), DR-10, §8.2 `[NOTE FOR PM]`
- **Problem og hvorfor det betyr noe:** Must omfatter 22 FR, alle 11 NFR-er, 6 AG-er og alle 10 DR-er, inkludert publisering på Vercel med PostgreSQL ved siden av lokal SQLite («samme kode», DR-10). DR-10 kom inn 2026-11-08, etter godkjenning. Samtidig er Should-delene «i fare», og det var sesongjustering briefen ba om. Når alt i §6 er Must, finnes det ingen skjøt å kutte i hvis noe sinker.
- **Forslag:** Legg til en kutt-linje i §8.1, for eksempel: «Hvis publiseringen (DR-10) ikke fungerer innen [dato], utgår SM-9, og SM-2 og SM-3 regnes som ferdige på den lokale versjonen.» Merk også hvilke DR-er som er selvpålagte prosesskrav (for eksempel «minst fem tilfeller i styringsloggen», DR-5) og hvilke som er nødvendige for at appen kan leveres.

### 4.2 Tallkontrollen i forklaringen er ikke fullt ut mekanisk
- **Alvorlighet:** medium
- **Hvor:** FR-27 («The explanation contains no number that is not also shown among the calculated numbers»), FR-28, SM-6
- **Problem og hvorfor det betyr noe:** En malforklaring inneholder naturlig nok antall beregningsuker, ukenummer og «siste 12 uker». Er de «beregnede tall på skjermen»? Uten en avgrenset mengde kan ikke testen skrives, og «etiketten som hører til et tall» (FR-28) kan ikke sjekkes.
- **Forslag:** Definer mengden: «Tillatte tall i forklaringen er verdiene i `CalculationResult` (felt: grunnprognose, scenarioer, sikkerhetsmargin, lager, bestillingsmengde, antall beregningsuker, ukenummer for utelatte uker) pluss konstantene 12 og 8 fra R-15.» La språkmodellen svare med plassholdere (`{base_forecast}`) som appen fyller inn. Testen kan da avvise svar der en plassholder mangler, er byttet eller er lagt til.

### 4.3 Én prioritet per FR og per kapittel
- **Alvorlighet:** medium
- **Hvor:** FR-17 («Priority: Must for the calculation and the confidence label; Should for the dedicated warning text»), §4.9 «Purchase Planning (Should)» med FR-31–34 som er Could, §4.3 «(Must)» med FR-9 som er Should
- **Problem og hvorfor det betyr noe:** Epics og stories trekker prioritet fra FR-en. Et FR med to prioriteter gir enten en story som er halvt Must og halvt Should, eller uenighet om hva som er «ferdig». PRD-en er på ca. 14 000 ord (pluss 5 500 i addendum), og dette gjør uttrekk tyngre.
- **Forslag:** Del FR-17 i «FR-17 Nivåskifte i beregning og tillitsmerke (Must)» og «FR-17b Eget varsel for nivåskifte (Should)». Flytt prioritet ut av kapitteloverskriftene, eller skriv «(Should/Could)». Legg en tabell «FR → prioritet → SM» i §8.

### 4.4 Noen konsekvenser er fortsatt adjektiver
- **Alvorlighet:** lav
- **Hvor:** FR-24 («A product without a forecast shows the reason instead of a number»), NFR-6 («narrower windows stay readable»), FR-25 («all active warnings»)
- **Problem og hvorfor det betyr noe:** Disse kan ikke bli testtilfeller uten at utvikleren gjetter. FR-31–34 (Could) har ingen konsekvenser, noe PRD-en sier åpent, men FR-33 bør få dem før den eventuelt planlegges.
- **Forslag:** FR-24: «For et produkt med færre enn 3 gyldige uker viser prognosekolonnen "Ingen prognose: færre enn 3 gyldige uker", og bestillingskolonnen viser "–".» NFR-6: «Ved 800 px bredde overlapper ikke tekst, og alle kontroller kan nås med tastatur.»

### 4.5 Åpne spørsmål som egentlig er beslutninger eller oppgaver
- **Alvorlighet:** lav
- **Hvor:** §10, spørsmål 1 («Order of the Should items»), 6 («Update the Product Brief»); §9
- **Problem og hvorfor det betyr noe:** Spørsmål 1 kan avgjøres nå, og det haster når fristen er 1. desember. Spørsmål 6 er en oppgave. Samtidig måler SM-ene at beregning, isolasjon og kjørbarhet fungerer, men ikke at brukeren faktisk forstår tillitsmerket, som er tesen.
- **Forslag:** Skriv «Besluttet: rekkefølgen er FR-29/30 → FR-9/36 → FR-28» (eller en annen rekkefølge) med én setning begrunnelse. Legg til et lite mål, for eksempel «SM-10: to personer utenfor gruppen får se produktsiden og kan forklare hvorfor ett produkt har tillitsmerket "lav"».

## 5. Mekaniske funn

- FR-1 til FR-36, R-1 til R-17, E1–E30 og SM-1 til SM-9 er sammenhengende, og krysshenvisningene jeg sjekket løser seg. FR-35 og FR-36 står utenfor rekkefølge, men det er forklart.
- Alle åtte `[ASSUMPTION]`-merker finnes i §11, og motsatt.
- Mindre glossar-avvik: «latest valid week» (FR-18, R-15) er ikke definert i glossaret, og R-16 bruker «sales history» i betydningen «antall uker inkludert utsolgte».
- SM-1 «validerer» R-1 til R-17, mens R-14 og R-17 er Should. Presiser «R-1 til R-13, R-15, R-16 for Must».
- PRD-en er på engelsk med norsk UI. Glossaret håndterer det konsekvent.
- Ingen sensitive opplysninger funnet.

## 6. Før dere går videre

**Må avklares før videre arbeid (UX, arkitektur, epics)**
- Kutt-linjen i 4.1 og rekkefølgen på Should-delene (spørsmål 1). Epics bør bygges på dette.
- Definisjonen av tillatte tall i forklaringen (4.2).
- Delte prioriteter i FR-17 (4.3).

**Kan vente**
- Kildehenvisninger for lagerreglene (spørsmål 3), valg av språkmodell (spørsmål 5) og oppdatering av briefen (spørsmål 6).
- Konsekvenser for Could-FR-ene, til de planlegges.

**Oppfølging av briefen: ja.** KI-rollen er avgjort (AG-1). Scenarioer, sikkerhetsmargin og avviksregel er definert (R-7, R-8, R-10), og det finnes fasit (E1–E30). «What makes this different», visjon og primærbruker er fylt ut, og fristen står i DR-6. Sesongjustering er flyttet til Should, og kampanjer og kundeordrer er utenfor (§7). Oppdatering av selve briefen står fortsatt åpen (spørsmål 6).

## 7. Refleksjonsspørsmål

1. Mange av reglene (R-10, R-11, R-14, R-17) er «project-defined», altså deres egne valg. Hvordan avgjorde dere at en regel var god nok, og hva ville fått dere til å forkaste en regel KI-en foreslo?
2. Dere har regnet gjennom eksemplene i PRD-en (for eksempel E5, hvor avrundingsfeilen ble funnet). Hva gjør dere hvis appen og regnearket er uenige: hvem har rett, og hvordan finner dere ut hvorfor?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
