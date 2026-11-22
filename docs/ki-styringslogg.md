# KI-styringslogg

KI-styringsloggen oppfyller DR-5 i PRD-en. Den fører tilfeller der gruppen avklarte, avviste eller rettet det KI foreslo. Hvert tilfelle har fem felt: hva KI foreslo, hva som var feil, hva gruppen bestemte, commiten eller pull requesten, og kilden. PRD-en krever minst fem tilfeller, og minst ett for hver epic som blir bygd (D-2 i `epics.md`).

**Rutinen for KI-økter.** Brukeren godkjente rutinen 18. november 2026. Den står i `epics.md` (linje 598–604 i `d8674ad`) og gjelder for hver story:
- En Claude Code-økt for en story begynner med å nevne storyen.
- Når økten er ferdig, eksporteres samtalen med `/export` til `.logs/<bruker>/sessions/`, med storyen og datoen i filnavnet. En økt som ikke formet storyens kode, tester eller dokumenter, trenger ikke lagres.
- Før commit får eksporten den samme personvernkontrollen som alle commits. Bare treffene fjernes eller maskeres, så promptene forblir originale.
- Eksporten committes i storyens pull request, og sesjonsloggen og pull requesten lenker til den.
- Når KI-output blir avvist, rettet eller presisert, føres et tilfelle her med en gang. En feil i KI-generert kode eller tekst føres også i [QA-loggen](qa-logg.md).

**Planleggingsfasen.** Da rutinen ble innført, var ingen prompts eller KI-økter fra planleggingsfasen lagret (sesjonslogg 985, linje 102). Planleggingsfasen er derfor dokumentert av arbeidsloggen, memloggene og sesjonsloggene, slik rutinen sier (`epics.md`, linje 604 i `d8674ad`). Tilfellene fra planleggingsfasen er sammendrag med egne ord av det disse kildene beskriver, og hvert tilfelle viser til kildene med fil og linje. Ingen prompt er rekonstruert eller gjengitt som original.

**Kildene.** Linjenumrene gjelder filene i commit `d8674ad`, og de siterte linjene leses i [repoet ved `d8674ad` på GitHub](https://github.com/IBE160-2026/G40-lyamouri/tree/d8674ad). Lenkene i tabellen under går til filene slik de er nå, og de kan ha endret seg. En commit eller pull request står bare der en kilde nevner den; ellers står det «ikke oppgitt i kilden». Kortnavnene viser til disse filene:

| Kortnavn | Fil |
|---|---|
| arbeidsloggen | [`docs/arbeidslogg.md`](arbeidslogg.md) |
| sesjonslogg 985–997 | Fila i [`.logs/mounia-03/`](../.logs/mounia-03/) som begynner med nummeret, for eksempel `997-2026-11-03-18-34-13-prd-prognose.md` |
| brief-memloggen | [`_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/.memlog.md`](../_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/.memlog.md) |
| brainstorm-memloggen | [`_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/.memlog.md`](../_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/.memlog.md) |
| PRD-memloggen | [`_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/.memlog.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/.memlog.md) |
| den arkiverte UX-memloggen og de arkiverte UX-filene | `.memlog.md`, `mockups/key-produktoversikt.html` og `review-structure-prose.md` i [`_bmad-output/planning-artifacts/archive/ux-G40-lyamouri-2026-11-06/`](../_bmad-output/planning-artifacts/archive/ux-G40-lyamouri-2026-11-06/), UX-en fra 6.–7. november |
| UX-memloggen | [`_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/.memlog.md`](../_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/.memlog.md) |
| arkitektur-memloggen | [`_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/.memlog.md`](../_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/.memlog.md) |
| PRD-en | [`_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md) |
| `extract-brainstorm.md`, `reconcile-brainstorm.md`, `review-calculations.md` og `review-sensorveiledning.md` | Sammendraget av brainstormingen og gjennomgangene av PRD-en i [`_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/`](../_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/) |
| `epics.md` | [`_bmad-output/planning-artifacts/epics.md`](../_bmad-output/planning-artifacts/epics.md) |
| mockupen | [`_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/mockups/konsept-d-kombinert.html`](../_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/mockups/konsept-d-kombinert.html) |

## Planleggingsfasen

Planleggingsfasen ga 26 tilfeller fra 14. oktober til 18. november 2026, og de står i datorekkefølge. Når et tilfelle også er en feil i KI-generert tekst eller kode, lenker det til feilen i QA-loggen.

### 1. Hoppede steg i BMAD for Product Brief (14. oktober 2026)

- **Hva KI foreslo:** Claude oppdaterte Product Brief med `bmad-product-brief` på rask vei, uten å tilby den veiledede arbeidsmåten, og hoppet i første runde over flere steg i workflowen, blant annet memloggen og sluttstegene.
- **Hva som var feil:** BMAD ble ikke fulgt slik workflowen beskriver. Avviket kom fram da brukeren kontrollerte at BMAD faktisk ble brukt.
- **Hva gruppen bestemte:** Stegene som manglet, ble fullført, blant annet memloggen og sluttstegene.
- **Commit eller pull request:** `5c4fb17` (arbeidsloggen, linje 41).
- **Kilde:** arbeidsloggen, linje 34–35; brief-memloggen, linje 16 og 21–22.

### 2. KI-tilleggene i Product Brief ble avvist (14. oktober 2026)

- **Hva KI foreslo:** Det første utkastet av briefen hadde egne tillegg og forslag fra KI, blant annet fire åpne punkter om trend og sesong, avviksregelen, periodelengden og S&OP/MPS, og et addendum.
- **Hva som var feil:** Briefen skulle bare følge brukerens reviderte tekst.
- **Hva gruppen bestemte:** Brukeren avviste tilleggene. `brief.md` ble skrevet om som en direkte oversettelse til engelsk av brukerens tekst, med de samme 11 seksjonene, og addendumet ble slettet.
- **Commit eller pull request:** `5c4fb17` (arbeidsloggen, linje 41).
- **Kilde:** arbeidsloggen, linje 36–37; brief-memloggen, linje 17–20, 22 og 24–26.
- **QA-loggen:** [rad 1](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 3. Lokal filsti og en fast personvernregel (1. november 2026)

- **Hva KI foreslo:** En fil som skulle committes etter researchen med `bmad-deep-recon`, inneholdt en lokal filsti.
- **Hva som var feil:** En lokal filsti hører ikke hjemme i en fil som pushes til GitHub.
- **Hva gruppen bestemte:** Stien ble fjernet før commit. Brukeren innførte også en fast personvernregel: Claude Code skal bare arbeide i prosjektmappen, og personopplysninger, lokale filstier og hemmeligheter skal ikke komme med til GitHub.
- **Commit eller pull request:** `a55da02` og `f46a88b`, som ble committet etter rettingen (arbeidsloggen, linje 62).
- **Kilde:** arbeidsloggen, linje 59 og 61–63.
- **QA-loggen:** [rad 2](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 4. Avrundingen i E5 (2.–3. november 2026)

- **Hva KI foreslo:** I brainstormingen foreslo KI-veilederen å runde bestillingsmengden opp til hele enheter, og brukeren bestemte det (brainstorm-memloggen, linje 61 og 65). Det KI-skrevne sammendraget av brainstormingen førte regelen videre til PRD-arbeidet (`extract-brainstorm.md`, linje 40).
- **Hva som var feil:** En datamaskin regner 100 × 1,1 − 40 til 70,00000000000001, så en ren oppoverrunding gir E5 bestillingsmengden 71 i stedet for 70. Ingen kilde sier hvem som oppdaget dette.
- **Hva gruppen bestemte:** Da beregningsreglene i PRD §5 ble skrevet, ble det lagt til at verdien rundes til 6 desimaler før den rundes opp, og brukeren godkjente det (PRD-memloggen, linje 43). Regelen er nå R-9, og E5 tester den. Avstemmingen mot brainstormingen viser byttet (`reconcile-brainstorm.md`, linje 29).
- **Commit eller pull request:** `4ada86d`, det første PRD-utkastet (arbeidsloggen, linje 74).
- **Kilde:** arbeidsloggen, linje 72; sesjonslogg 997, linje 19; brainstorm-memloggen, linje 61 og 65; `extract-brainstorm.md`, linje 40; PRD-memloggen, linje 43; `reconcile-brainstorm.md`, linje 29; `review-calculations.md`, linje 15; PRD-en, linje 612 og 671.
- **QA-loggen:** [eksempel 1](qa-logg.md#eksempel-1-avrundingen-i-e5). E5 står i begge loggene fordi DR-5 (PRD-en, linje 761) og story 1.1 (`epics.md`, linje 754) nevner den.

### 5. Prognosekonflikten i R-10 og R-11 (2.–3. november 2026)

- **Hva KI foreslo:** PRD-utkastet beskrev reglene for uvanlige uker (R-10) og nytt nivå (R-11), men sa ikke i hvilken rekkefølge ukene skulle behandles.
- **Hva som var feil:** Den uavhengige beregningskontrollen viste at de samme salgstallene kunne gi grunnprognosen 51,0 eller 70,333 (funn F1, kritisk).
- **Hva gruppen bestemte:** Brukeren godkjente rettingen: ukene behandles i tidsrekkefølge i én gjennomgang, og tre uvanlige uker på rad blir nytt nivå med en gang, så senere uker sammenlignes med det nye nivået. E15 tester regelen.
- **Commit eller pull request:** `4ada86d` (arbeidsloggen, linje 74; PRD-memloggen, linje 89). Den ferdige PRD-en er `d938baa` (arbeidsloggen, linje 74).
- **Kilde:** arbeidsloggen, linje 72; sesjonslogg 997, linje 19; PRD-memloggen, linje 66 og 74–75; `review-calculations.md`, linje 30; PRD-en, linje 616–617 og 682.
- **QA-loggen:** [eksempel 2](qa-logg.md#eksempel-2-prognosekonflikten-i-r-10-og-r-11).

### 6. Oppsettsmålet på 10 minutter (2.–3. november 2026)

- **Hva KI foreslo:** Kontrollen av PRD-en mot sensorveiledningen, som en subagent gjorde, foreslo å stramme oppsettsmålet i SM-2 fra 15 til 10 minutter.
- **Hva som var feil:** Brukeren ville beholde 15 minutter. Kildene oppgir ingen grunn.
- **Hva gruppen bestemte:** Brukeren avviste forslaget og beholdt 15 minutter. Prøven på en ren maskin gjentas på siste commit.
- **Commit eller pull request:** `4ada86d` (PRD-memloggen, linje 89).
- **Kilde:** arbeidsloggen, linje 72; PRD-memloggen, linje 77 og 79; `review-sensorveiledning.md`, linje 97 og 142.

### 7. Språkmodellen uten lærerens svar (2.–3. november 2026)

- **Hva KI foreslo:** Det KI-skrevne sammendraget av brainstormingen gjorde spørsmålet til læreren om appen må vise en språkmodell, til det åpne punktet som avgjorde om forklaringen med språkmodell ble må-ha eller bør-ha (PRD-memloggen, linje 15; `extract-brainstorm.md`, linje 133). Etter gjennomgangene var planen å spørre læreren før arkitekturen (PRD-memloggen, linje 69).
- **Hva som var feil:** Den valgfrie språkmodellen ble da avhengig av et svar fra læreren. Kildene gir ingen annen grunn.
- **Hva gruppen bestemte:** Brukeren bestemte at den valgfrie lokale språkmodellen (FR-28) ikke skal avhenge av lærerens svar. Den er bør-ha og aldri en del av grunnoppsettet.
- **Commit eller pull request:** `4ada86d` (PRD-memloggen, linje 89).
- **Kilde:** arbeidsloggen, linje 72; PRD-memloggen, linje 15, 69, 81 og 86; `extract-brainstorm.md`, linje 133.

### 8. Ti parallelle agenter (6. november 2026)

- **Hva KI foreslo:** Ti designkonsepter fra ti subagenter som skulle kjøre parallelt.
- **Hva som var feil:** Brukskvoten ble brukt opp to ganger før agentene hadde laget noe design, så ingen av konseptene ble ferdige.
- **Hva gruppen bestemte:** Brukeren stoppet planen og ba om at agentene ikke ble startet på nytt. I stedet skulle Claude lage ett gjennomarbeidet design, ta designbeslutningene og vise resultatet før detaljeringen.
- **Commit eller pull request:** `23a7589`, der designet ble committet 7. november (sesjonslogg 996, linje 191). Arbeidsloggen sier at ingenting var committet 6. november (linje 88).
- **Kilde:** arbeidsloggen, linje 84–85; sesjonslogg 996, linje 6 og 11.

### 9. Fem forbedringer av skissene (7. november 2026)

- **Hva KI foreslo:** Designforslaget «O-kartet» fra 6. november, med landingssiden og produktoversikten som HTML-skisser.
- **Hva som var feil:** Brukeren så skissene i nettleseren og ville ha fem forbedringer: en mye mindre varseltrekant, en kortere landingsside uten gjentakelser, en tydeligere innlogging, interne designnotater adskilt fra sidene brukerne ser, og bedre tilpasning til mobil.
- **Hva gruppen bestemte:** Alle fem ble gjort. Farger, grafer, hovedstruktur og designretning skulle beholdes, og det skulle ikke komme nye funksjoner. Varseltrekanten er tilfelle 10.
- **Commit eller pull request:** `23a7589` (sesjonslogg 996, linje 191).
- **Kilde:** arbeidsloggen, linje 86 og 94–107; sesjonslogg 996, linje 50–57.

### 10. Den store varseltrekanten (7. november 2026)

- **Hva KI foreslo:** CSS-koden i skissene fra 6. november.
- **Hva som var feil:** En regel for grafen traff også varselikonet, så trekanten ble like bred som grafen.
- **Hva gruppen bestemte:** Brukeren ba om en mye mindre trekant. Regelen gjelder nå bare grafen, og ikonene er 16 px.
- **Commit eller pull request:** `23a7589` (sesjonslogg 996, linje 191).
- **Kilde:** arbeidsloggen, linje 95 og 102; sesjonslogg 996, linje 65; den arkiverte UX-memloggen, linje 35.
- **QA-loggen:** [rad 3](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 11. Feil bruddpunkt og grafbeskrivelse (7. november 2026)

- **Hva KI foreslo:** UX-dokumentene `DESIGN.md` og `EXPERIENCE.md`, som Claude skrev da UX-fasen ble fullført.
- **Hva som var feil:** Forslaget fra gjennomgangen av struktur og språk til en egen tabell for appen satte filteret på mobil til 2 × 2 ved 640 px, med verdier fra den gjeldende tabellen. Skissen gjør det ved 560 px, og det kom fram da forslaget ble tatt inn. Bare arbeidsloggen sier at gjennomgangen fant feilen i bruddpunktet. Gjennomgangen fant derimot at beskrivelsen av grafen ikke passet med Chart.js.
- **Hva gruppen bestemte:** Begge ble rettet i dokumentene, med filteret ved 560 px som i skissen, uten å endre designet.
- **Commit eller pull request:** `23a7589` (sesjonslogg 996, linje 191).
- **Kilde:** arbeidsloggen, linje 115 og 120–122; den arkiverte UX-memloggen, linje 43; den arkiverte `review-structure-prose.md`, linje 39, 49 og 138; den arkiverte `key-produktoversikt.html`, linje 165.
- **QA-loggen:** [eksempel 4](qa-logg.md#eksempel-4-feil-bruddpunkt-og-grafbeskrivelse).

### 12. Django 6.1 eller 5.2 LTS (8. november 2026)

- **Hva KI foreslo:** Claude foreslo den nyeste versjonen, Django 6.1.
- **Hva som var feil:** Brukeren ville ha stabilitet fram mot fristen, og 6.1 er ikke langtidsversjonen.
- **Hva gruppen bestemte:** Langtidsversjonen Django 5.2 med Python 3.13.
- **Commit eller pull request:** `29dd679` (sesjonslogg 995, linje 46).
- **Kilde:** arbeidsloggen, linje 132 og 137; sesjonslogg 995, linje 19, 30 og 37.

### 13. Vercel som publiseringsløsning (8. november 2026)

- **Hva KI foreslo:** Etter sjekken av Vercel gjorde arkitekturen lokal kjøring til standard og publisering på Vercel valgfri etter må-ha (AD-13 i den arkiverte arkitekturen fra 8. november).
- **Hva som var feil:** Brukeren ville at Vercel skulle være publiseringsløsningen, ikke bare et valg.
- **Hva gruppen bestemte:** Vercel ble publiseringsløsningen. PRD-en fikk DR-10 og SM-9, og arkitekturen fra 8. november, som nå er arkivert, fikk AD-16. Beslutningen ble omgjort 19. november etter lærerens avklaring, og publisering er ikke med i versjon 1 (DR-10 i [statustabellen](statustabell.md)).
- **Commit eller pull request:** `21cd020` (sesjonslogg 995, linje 118). Omgjøringen er i `ea06f01` (PR #5) (PRD-en, linje 978).
- **Kilde:** arbeidsloggen, linje 138–139 og 511–518; sesjonslogg 995, linje 59 og 79–88.

### 14. Addendumet i kravlisten for epics (8. november 2026)

- **Hva KI foreslo:** Kravlisten og storyene i det første utkastet av `epics.md`.
- **Hva som var feil:** Fire punkter fra addendumet og PRD §10 manglet i kravlisten. Sluttvalideringen fant også to stories i epic 1 som viste til senere stories, og et manglende kriterium for passordhashing (FR-1).
- **Hva gruppen bestemte:** Brukeren ba Claude sjekke at addendumet var dekket. Punktene ble lagt til uten nye funksjoner, og henvisningene og kriteriet ble rettet. Disse epics ble arkivert 16. november.
- **Commit eller pull request:** `f74665b` (sesjonslogg 994, linje 20).
- **Kilde:** arbeidsloggen, linje 147 og 326; sesjonslogg 994, linje 15 og 18.
- **QA-loggen:** [rad 4 og 5](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 15. FR-24 etter tilbakemeldingen (15. november 2026)

- **Hva KI foreslo:** I oppdateringen etter lærerens tilbakemelding lot Claude FR-24 følge det godkjente UX-designet, der årsaken står over tre kolonner, i stedet for lærerens eksempel.
- **Hva som var feil:** FR-24 oppfylte da ikke lærerens funksjonelle krav.
- **Hva gruppen bestemte:** FR-24 skal oppfylle lærerens krav: prognosekolonnen viser årsaken, og bestillingskolonnen og uker dekning viser «–». UX-en skulle tilpasses senere.
- **Commit eller pull request:** `47a8857` (arbeidsloggen, linje 174), flettet til `main` gjennom PR #2 (arbeidsloggen, linje 366).
- **Kilde:** arbeidsloggen, linje 172; PRD-memloggen, linje 104, 111 og 115; sesjonslogg 990, linje 29.
- **QA-loggen:** [rad 7](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 16. Safari-fanene (15.–16. november 2026)

- **Hva KI foreslo:** Et skript fra Claude styrte Safari og lukket en av brukerens faner.
- **Hva som var feil:** Skriptet grep inn i brukerens egne faner.
- **Hva gruppen bestemte:** Claude skal bare åpne filer med `open -a Safari`, og ikke styre faner eller vinduer.
- **Commit eller pull request:** ikke oppgitt i kilden.
- **Kilde:** arbeidsloggen, linje 193; UX-memloggen, linje 15; sesjonslogg 988, linje 44.
- **QA-loggen:** [rad 8](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 17. Grafen høyere opp (15.–16. november 2026)

- **Hva KI foreslo:** Konsept D, der grafen sto under panelene for bestillingsforslag og tillit. Da brukeren ba om å flytte grafen høyere, forklarte Claude at varslene må bli stående over grafen, fordi FR-25 krever at de er synlige uten å rulle på en skjerm på 1366 × 768.
- **Hva som var feil:** Grafen sto lenger ned på produktsiden enn brukeren ville.
- **Hva gruppen bestemte:** Grafen ble flyttet et stykke opp, og varslene ble stående over den. Utregningslinjen for bestillingsmengden ble flyttet til slutten av «Slik er tallene regnet ut», så ved 1366 × 768 starter grafen omtrent 70 px høyere enn før.
- **Commit eller pull request:** `5db2fe7` (arbeidsloggen, linje 211).
- **Kilde:** arbeidsloggen, linje 191 og 195; UX-memloggen, linje 19–20; sesjonslogg 988, linje 98 og 111–115.

### 18. Den store bryteren (15.–16. november 2026)

- **Hva KI foreslo:** CSS-koden i konsept D, der regelen `.chart svg{width:100%}` gjør grafen like bred som panelet.
- **Hva som var feil:** Da bryteren for uvanlige uker ble flyttet inn i grafpanelet, traff regelen også bryteren, så den ble like bred som panelet. Det er samme type feil som varseltrekanten 7. november (tilfelle 10).
- **Hva gruppen bestemte:** Brukeren ba om normal størrelse på bryteren. Én ny CSS-linje gir den igjen 40 × 22 px, og en kontrollsum viste at ingenting annet i fila var endret. Regelen treffer også symbolene i tegnforklaringen. De ble stående etter brukerens beskjed, og story 2.10 krever at regelen ikke treffer dem i appen.
- **Commit eller pull request:** `5db2fe7` (arbeidsloggen, linje 211).
- **Kilde:** arbeidsloggen, linje 191 og 194; UX-memloggen, linje 21–22; sesjonslogg 988, linje 117; mockupen, linje 182–183; `epics.md`, linje 1444.
- **QA-loggen:** [rad 9](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen», om bryteren, og [eksempel 3](qa-logg.md#eksempel-3-css-regelen-som-traff-tegnforklaringen), om symbolene i tegnforklaringen.

### 19. PostgreSQL i begge kjøremodusene (17. november 2026)

- **Hva KI foreslo:** SQLite lokalt og PostgreSQL bare på Vercel, slik PRD-en sa.
- **Hva som var feil:** Etter brukerens vurdering var det mer langsiktig å bruke PostgreSQL i begge kjøremodusene.
- **Hva gruppen bestemte:** PostgreSQL er et krav i begge kjøremodusene. Claude skulle undersøke konsekvensene for PRD-en før noe ble endret, og PRD-en, addendumet og UX-en ble deretter oppdatert.
- **Commit eller pull request:** `1441c40` og `c76d6cd` (arbeidsloggen, linje 441), flettet til `main` gjennom PR #3 (arbeidsloggen, linje 495–503).
- **Kilde:** arbeidsloggen, linje 422 og 431–437; arkitektur-memloggen, linje 9 og 35.

### 20. Ingen automatisk sletting (17. november 2026)

- **Hva KI foreslo:** Anbefaling P6: byggesteget på Vercel skulle kjøre migreringer og laste seed-data automatisk. En av avklaringene sa at `load_seed` sletter alle økter når dataene lastes på nytt.
- **Hva som var feil:** Automatiske steg kunne slette eller overskrive brukerdata.
- **Hva gruppen bestemte:** P6 ble godkjent med et forbehold: ingenting skal slette eller overskrive brukerdata automatisk. Byggesteget migrerer bare når endringene bare legger til, `load_seed` laster bare inn i en tom database, og bare en tilbakestilling som brukeren bekrefter, sletter data. DR-4 og DR-10 i PRD-en ble endret.
- **Commit eller pull request:** `1441c40` (arbeidsloggen, linje 441).
- **Kilde:** arbeidsloggen, linje 423–426; arkitektur-memloggen, linje 28, 33 og 52–54.

### 21. Docker-oppsettet bekreftet og ny port (17. november 2026)

- **Hva KI foreslo:** Lokal PostgreSQL med Docker Compose på porten 54320.
- **Hva som var feil:** Løsningen var ikke kjørt på noen maskin, og porten 54320 kan være reservert på Windows.
- **Hva gruppen bestemte:** Brukeren ville ha Docker-løsningen bekreftet før godkjenningen. Claude skilte mellom det som var dokumentert, målt og ikke testet, porten ble endret til 15432, og PostgreSQL ble testet på Mac etter at Docker Desktop var installert. Testen står i [QA-loggen](qa-logg.md#2026-11-17--test-av-lokal-postgresql-med-docker-compose-sm-2-nfr-1-nfr-8).
- **Commit eller pull request:** `1441c40` (arbeidsloggen, linje 441).
- **Kilde:** arbeidsloggen, linje 427–429; arkitektur-memloggen, linje 39, 43–47 og 50.
- **QA-loggen:** [rad 21](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 22. Epic 2 slått sammen (18. november 2026)

- **Hva KI foreslo:** 15 stories i epic 2.
- **Hva som var feil:** Så mange stories ville gi mange pull requests.
- **Hva gruppen bestemte:** Tre par stories ble slått sammen for å få færre pull requests, og alle akseptansekriteriene og testene ble beholdt.
- **Commit eller pull request:** `9dee8b1` (arbeidsloggen, linje 492), flettet til `main` gjennom PR #3 (arbeidsloggen, linje 495–503).
- **Kilde:** arbeidsloggen, linje 475; `epics.md`, linje 631; sesjonslogg 985, linje 33.

### 23. NFR-8 kontrollert mot kildene (18. november 2026)

- **Hva KI foreslo:** Funn A4 fra BMAD Review gjaldt unntaket fra NFR-8 når den valgfrie språkmodellen er slått på, og kravet kunne bli endret.
- **Hva som var feil:** Ingen endring trengtes. FR-28 setter selv tidsgrensen på 10 sekunder, og addendum §3 gjør forholdet til NFR-8 til et arkitekturvalg.
- **Hva gruppen bestemte:** Brukeren ba Claude kontrollere unntaket mot PRD-en og addendumet før kravet eventuelt ble endret. NFR-8 ble beholdt uendret, og D-7 i `epics.md` viser til kildene.
- **Commit eller pull request:** `9dee8b1` (arbeidsloggen, linje 492).
- **Kilde:** arbeidsloggen, linje 476; sesjonslogg 985, linje 60 og 77; `epics.md`, linje 77–83.
- **QA-loggen:** [rad 24](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 24. GitHub Issues og funn A5 (18. november 2026)

- **Hva KI foreslo:** Claude vurderte GitHub Issues (funn A5) ut fra sammendraget av sensorveiledningen i `review-sensorveiledning.md`, fordi Claude ikke hadde hele sensorveiledningen.
- **Hva som var feil:** Merknaden om GitHub Issues i reglene for alle stories bygde på et sammendrag, ikke på den originale sensorveiledningen.
- **Hva gruppen bestemte:** Brukeren limte inn hele sensorveiledningen. Merknaden viser nå til originalen, som godtar «issues eller tilsvarende», og `issues.md` er fortsatt prosjektets liste over feil og åpne punkter.
- **Commit eller pull request:** `9dee8b1` (`epics.md`, linje 2308).
- **Kilde:** arbeidsloggen, linje 457–459 og 477; sesjonslogg 985, linje 78, 101 og 105; `epics.md`, linje 2308.
- **QA-loggen:** [rad 25](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 25. Ikke «godkjent» uten dokumentasjon (18. november 2026)

- **Hva KI foreslo:** Claude foreslo å lenke til lærerens godkjenning av avgrensningen.
- **Hva som var feil:** Ingen kilde dokumenterte en slik godkjenning. Lærerens tilbakemelding 6. oktober er en vurdering av avgrensningen, og godkjenningen 14. oktober var brukerens egen godkjenning av briefen.
- **Hva gruppen bestemte:** Ingenting skal påstås godkjent uten dokumentasjon. Story 4.1 krever at README-en gjengir tilbakemeldingen med dens egne ord og ikke kaller den en godkjenning.
- **Commit eller pull request:** `9dee8b1` (`epics.md`, linje 2311).
- **Kilde:** arbeidsloggen, linje 478; sesjonslogg 985, linje 115; `epics.md`, linje 2311.
- **QA-loggen:** [rad 26](qa-logg.md#andre-feil-fra-arbeidsloggen) under «Andre feil fra arbeidsloggen».

### 26. Mobil og iPad (18. november 2026)

- **Hva KI foreslo:** Claude anbefalte at README-en skulle si at appen bare er laget for PC.
- **Hva som var feil:** Brukeren ville at nettsiden også skal fungere på mobil og iPad.
- **Hva gruppen bestemte:** Nettsiden skal også fungere på mobil og iPad. Claude vurderte først NFR-6, PRD-en, UX-en og arkitekturen uten å endre noe. Deretter ble NFR-6 oppdatert i PRD-en, `EXPERIENCE.md`, `DESIGN.md` og `epics.md`, blant annet med minste bredde 320 px og trykkflater på minst 44 × 44 px. Arkitekturen ble ikke endret.
- **Commit eller pull request:** `9dee8b1` (`epics.md`, linje 2312).
- **Kilde:** arbeidsloggen, linje 466–473 og 479; sesjonslogg 985, linje 116–125; `epics.md`, linje 2312.

## Byggefasen

**Story 1.1.** Story 1.1 ga to tilfeller, 27 og 28. Ellers godtok brukeren hver anbefaling fra Claude i øktene 20. og 21. november 2026. Feilene som reviewene fant i KI-generert kode og tekst, står i QA-loggen, for [del A](qa-logg.md#2026-11-20--feil-i-ki-generert-kode-og-tekst-fra-reviewen-av-story-11-del-a-dr-9), [del B](qa-logg.md#2026-11-21--feil-i-ki-generert-tekst-fra-reviewen-av-story-11-del-b-dr-9) og [BMAD Code Review](qa-logg.md#2026-11-21--feil-i-ki-generert-kode-og-tekst-fra-bmad-code-review-av-story-11-dr-9).

### 27. Regelen om CI og story 1.1 (21. november 2026)

- **Hva KI foreslo:** Reglene som Claude skrev i `epics.md`, og AD-17 i arkitekturspinen, krevde at CI passerer før hver story flettes. Den samme planen la CI i story 1.2, etter story 1.1. Claude fant motsigelsen da brukeren ba om en sjekk, og foreslo unntaket D-9.
- **Hva som var feil:** Story 1.1 kunne aldri oppfylle regelen.
- **Hva gruppen bestemte:** Brukeren godkjente D-9: story 1.1 flettes når testene og Ruff passerer lokalt på siste commit, og den første CI-kjøringen kommer med story 1.2.
- **Commit eller pull request:** `fa237e7` og `5268fe0` (PR #8).
- **Kilde:** D-9 i `epics.md`; [sesjonsloggen for story 1.1](../.logs/mounia-03/983-2026-11-20-18-35-44-story-1-1-lokal-oppstart.md).
- **QA-loggen:** [motsigelsen i planen om CI](qa-logg.md#2026-11-21--motsigelse-i-planen-om-ci-før-story-12-dr-7-dr-9).

### 28. Beslutningene i BMAD Code Review av story 1.1 (21. november 2026)

- **Hva KI foreslo:** Fire KI-granskere i `bmad-code-review` fant 34 funn, og Claude foreslo en vurdering og en beslutning for hvert av dem.
- **Hva som var feil:** Ikke alle funnene skulle følges. 11 lå utenfor storyen etter spesifikasjonen, var lite sannsynlige med en retting som ville gitt mer kode, krevde en endring i spesifikasjonen eller var vurdert før. Tre krevde et valg som bare brukeren kunne ta.
- **Hva gruppen bestemte:** Brukeren godkjente vurderingene: 21 funn ble rettet, 2 utsatt og 11 avvist. Brukeren valgte selv en test for `.gitignore`, som var avvist i del A, beslutningen D-10 om hvilke ID-er testene nevner, og en advarsel om `DATABASE_URL` i stedet for et nytt navn på variabelen.
- **Commit eller pull request:** PR #8.
- **Kilde:** «Review Findings» i [spesifikasjonen for story 1.1 del A](../_bmad-output/implementation-artifacts/spec-1-1-start-prognose-locally-from-a-fresh-clone.md); kommentaren i PR #8; [sesjonsloggen for story 1.1](../.logs/mounia-03/983-2026-11-20-18-35-44-story-1-1-lokal-oppstart.md).
- **QA-loggen:** [feilene fra BMAD Code Review](qa-logg.md#2026-11-21--feil-i-ki-generert-kode-og-tekst-fra-bmad-code-review-av-story-11-dr-9).

**Story 1.2.** Story 1.2 ga tilfelle 29. Ellers godtok brukeren hver anbefaling fra Claude i øktene 21. og 22. november 2026. Feilene som reviewene fant i KI-generert kode og tekst, står i QA-loggen, under [reviewene av story 1.2](qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-reviewene-av-story-12-dr-9).

### 29. Beslutningene i reviewene av story 1.2 (22. november 2026)

- **Hva KI foreslo:** Claude skrev CI-workflowen og testene for story 1.2. Importtesten godtok hele standardbiblioteket, og alle kjøringer på `main` delte én kø. Reviewen i `bmad-build` og fire KI-granskere i `bmad-code-review` fant til sammen 45 funn, og Claude foreslo en vurdering og en beslutning for hvert av dem.
- **Hva som var feil:** Importtesten slapp gjennom database- og nettverksmodulene i standardbiblioteket, selv om AD-1 holder dem utenfor kjernen, og køen kunne avbryte en kjøring på `main`. Ikke alle funnene skulle følges: 10 var lite sannsynlige med en retting som ville gitt mer kode, var vurdert før, eller var feil.
- **Hva gruppen bestemte:** Brukeren valgte at importtesten også avviser database- og nettverksmodulene i standardbiblioteket, og at hver kjøring utenfor en pull request får sin egen gruppe. Brukeren godkjente resten av vurderingene: i BMAD Code Review ble 12 funn rettet og 3 avvist, og i `bmad-build` ble 7 avvist.
- **Commit eller pull request:** `e24727e` og PR #10.
- **Kilde:** «Review Triage Log» og «Review Findings» i [spesifikasjonen for story 1.2](../_bmad-output/implementation-artifacts/spec-1-2-check-every-pull-request-automatically.md); kommentaren i PR #10.
- **QA-loggen:** [feilene fra reviewene av story 1.2](qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-reviewene-av-story-12-dr-9).

**Story 1.3.** Story 1.3 ga tilfelle 30. Ellers godtok brukeren hver anbefaling fra Claude i økten 22. november 2026. Feilene som reviewene fant i KI-generert kode og tekst, står i QA-loggen, under [reviewene av story 1.3](qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-reviewene-av-story-13-dr-9).

### 30. Windows-testen og reviewene av story 1.3 (22. november 2026)

- **Hva KI foreslo:** README som Claude skrev i story 1.1, nevnte ikke at Terminal kan mangle `docker`, og testskriptet for den første testen uten nett sjekket ikke at Docker Desktop var avsluttet. Da ingenting kunne installeres på jobb-PC-en, foreslo Claude å føre begrensningen og legge til en delvis test i GitHub Actions. Fire KI-granskere i `bmad-code-review` fant 46 funn, og Claude foreslo en vurdering og en beslutning for hvert av dem.
- **Hva som var feil:** Den som fulgte README på macOS, fikk `command not found: docker`. Den første testen viste ikke en kald start av Docker Desktop uten nett, men README sa at oppstarten uten nett var testet. Windows-workflowen hadde svakheter, og QA-loggen førte en kjøring av en eldre versjon av den. Ikke alle funnene skulle følges: 2 ble avvist, og 1 ble utsatt, fordi det gjelder et plattformkrav fra før story 1.3.
- **Hva gruppen bestemte:** Brukeren valgte å føre begrensningen og den delvise testen i GitHub Actions i stedet for å installere noe på jobb-PC-en, og å teste den ferdige nettsiden i en nettleser på Windows i story 4.4. I BMAD Code Review valgte brukeren å kjøre testen uten nett på macOS på nytt med Docker Desktop helt avsluttet, og at Windows-testen også kjører når koden endres. Brukeren godkjente resten: 19 punkter ble rettet, 1 utsatt og 2 avvist.
- **Commit eller pull request:** `0eaea95`, `fedaef2` og PR #12.
- **Kilde:** «Implementation Notes» og «Review Triage Log» i [spesifikasjonen for story 1.3](../_bmad-output/implementation-artifacts/spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md); kommentaren i PR #12; [sesjonsloggen for story 1.3](../.logs/mounia-03/981-2026-11-22-09-53-00-story-1-3-windows-og-uten-nett.md).
- **QA-loggen:** [oppsettet på Windows](qa-logg.md#2026-11-22--oppsettet-på-windows-story-13-sm-2-nfr-1-dr-1-d-3) og [feilene fra reviewene av story 1.3](qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-reviewene-av-story-13-dr-9).

**Story 1.4.** Story 1.4 ga tilfelle 31 og 32. Ellers godtok brukeren hver anbefaling fra Claude i økten 22. november 2026. Feilene som byggingen og reviewene fant i KI-generert kode og tekst, står i QA-loggen, under [byggingen og reviewene av story 1.4](qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-byggingen-og-reviewene-av-story-14-dr-9).

### 31. 503-siden og den ytterste mellomvaren (22. november 2026)

- **Hva KI foreslo:** AD-12 i arkitekturspinen, som Claude skrev og rettet etter BMAD-reviewen 18. november, sier at 503-håndteringen sitter i den ytterste mellomvaren, slik at en databasefeil fra hvor som helst, også fra annen mellomvare, gir 503-siden. Story 1.4 i `epics.md` har det samme kravet.
- **Hva som var feil:** Django gjør om et unntak til et svar i laget der det oppstår, så den ytterste mellomvaren ser aldri unntaket fra lagene innenfor. En `try/except` rundt resten av forespørselen, som er den vanlige måten å lese regelen på, ville aldri slått til, og en stoppet database ville gitt 500-siden i stedet for 503.
- **Hva gruppen bestemte:** Claude fant feilen da story 1.4 ble planlagt, ved å lese koden i Django 5.2.19. Claude foreslo at Djangos signal `got_request_exception` merker forespørselen mens unntaket håndteres, og at den ytterste mellomvaren deretter viser 503-siden. Kravet og spinen er uendret, fordi håndteringen fortsatt sitter i den ytterste mellomvaren. Brukeren godkjente spesifikasjonen med denne løsningen.
- **Commit eller pull request:** `9ae95fc` og PR #14.
- **Kilde:** «Design Notes» og «Implementation Notes» i [spesifikasjonen for story 1.4](../_bmad-output/implementation-artifacts/spec-1-4-norwegian-app-shell-and-error-pages.md).
- **QA-loggen:** [feilene fra byggingen og reviewene av story 1.4](qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-byggingen-og-reviewene-av-story-14-dr-9).

### 32. Beslutningene i reviewene av story 1.4 (22. november 2026)

- **Hva KI foreslo:** Claude skrev stilarket, malene, mellomvaren, loggoppsettet og testene for story 1.4. Blind Hunter i `bmad-build` fant 10 funn, og fire KI-granskere i `bmad-code-review` fant 35. Claude foreslo en vurdering og en beslutning for hvert av dem.
- **Hva som var feil:** Med DEBUG på kunne 503-siden bli sendt som ren tekst. Flere tester var for snevre: de slapp gjennom en token som ble overstyrt, flere måter å fjerne fokusringen på og en database-URL som begynner med `postgres://`. Dokumentene viste til åpne punkter som ikke var ført, og bare til pull requesten, ikke til commiten. Ikke alle funnene skulle følges: 8 i `bmad-build` og 9 i BMAD Code Review ble avvist, og 2 ble utsatt, fordi de kommer fra designet og fra story 1.1.
- **Hva gruppen bestemte:** Brukeren valgte å beholde berøringsreglene for skjermer der berøring er hovedinngangen. Brukeren sjekket også fokusringen og versjonene av Safari og macOS for hånd i stedet for å la QA-loggen stå som den var. Brukeren godkjente resten: alle 15 rettingene fra BMAD Code Review.
- **Commit eller pull request:** `5063f67` og PR #14.
- **Kilde:** «Review Triage Log» og «Review Findings» i [spesifikasjonen for story 1.4](../_bmad-output/implementation-artifacts/spec-1-4-norwegian-app-shell-and-error-pages.md); kommentaren i PR #14.
- **QA-loggen:** [feilene fra byggingen og reviewene av story 1.4](qa-logg.md#2026-11-22--feil-i-ki-generert-kode-og-tekst-fra-byggingen-og-reviewene-av-story-14-dr-9).

Hver epic som bygges, skal gi minst ett tilfelle (D-2 i `epics.md`, linje 45–47).
