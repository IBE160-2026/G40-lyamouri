---
name: 'Prognose'
status: final
created: '2026-11-15'
updated: '2026-11-19'
sources:
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/tilbakemelding-prd.md'
  - 'DESIGN.md'
---

# Prognose — Experience Spine

> Responsive web for one purchasing manager per company: made for the office PC, and usable on an iPad and a phone. [DESIGN.md](DESIGN.md) owns how Prognose looks; this spine owns how it works. The approved mockup is [mockups/konsept-d-kombinert.html](mockups/konsept-d-kombinert.html): Produktoversikt with «Denne uken», Produktside, and a product without a forecast, all in the desktop layout; the narrower and touch layouts are fixed only in the spines (Responsive & Platform). Innlogging and Samlet bestillingsoversikt have wireframes below. The spines win on any conflict with a mockup, and the known differences are listed under Open Questions and Assumptions.

## Foundation

- **Surface:** a current browser on a PC or laptop, an iPad or a phone, with one responsive layout and the same functions everywhere (NFR-6). The office PC stays the main case (UJ-1). Dark mode and print are not required and not designed.
- **Users:** one role per company (PRD §2.2). Prognose recommends and the user decides: nothing in the interface places an order (PRD §7).
- **Language:** Norwegian bokmål throughout, with the glossary labels from PRD §3 used verbatim and no synonyms (NFR-5).
- **Technology posture:** plain semantic HTML and CSS with the tokens in DESIGN.md, no UI library. Every function works through links and forms; scripts may only enhance (arrow keys in the list, keeping scroll positions, sending the unusual-weeks switch, and enabling on Innstillinger the setting that the chosen method uses); the chart is SVG rendered on the server (AD-11). Everything is served locally, with no web fonts and no CDN (NFR-1). The architecture fixes the framework, how the chart is rendered and the URLs; the mockup's addresses (`/produkter/`, `/produkter/10012/`) only illustrate.
- **Accessibility target:** WCAG 2.2 AA (NFR-11); see Accessibility Floor.

## Information Architecture

| Surface | Reached from | Purpose | Visual reference |
|---|---|---|---|
| Innlogging | the app root, and every page when logged out (FR-1) | log in with customer number and password | wireframe below (spine-only) |
| Produktoversikt | after login; «Produktoversikt» in the app header | «Denne uken» beside the product list: what to order soon, in R-12 order (FR-24) | [mockup](mockups/konsept-d-kombinert.html), screen 1 |
| Produktside | a card or row in the list; «Start med …»; previous and next | decide one product: suggestion, trust, chart, calculations, explanation (FR-25, FR-35, FR-21, FR-26, FR-27) | [mockup](mockups/konsept-d-kombinert.html), screen 2 and the no-forecast state |
| Innstillinger | «Endre innstillinger» in the settings bar | change the company settings (FR-20 to FR-22) | spine-only (table below) |
| Samlet bestillingsoversikt | «Samlet bestillingsoversikt» in the app header; step 3 of the week path | every product's suggested or adjusted quantity for the meeting (FR-30, Should) | wireframe below (spine-only) |
| Ikke funnet | an unknown address, or another company's product (FR-2, NFR-10) | say that the page does not exist and link back | spine-only |
| Feilside | a database or server error, or an expired form (NFR-10) | say what went wrong and what to do next | spine-only |

- **App header** on every page: the company and the latest data week, then «Produktoversikt», «Samlet bestillingsoversikt» (only when FR-30 is built) and «Logg ut». When logged out it shows only the wordmark.
- **Settings bar** on every page after login.
- **List and product together:** on Produktoversikt and Produktside the product list stays on the left. Selecting a product changes the right side and the address, so each product has its own link, and Back works (NFR-10).
- **No modals.** Innstillinger is a page of its own and returns to the page you came from.

### Wireframe: Innlogging (spine-only)

```
┌─ App header: «Prognose» (no navigation when logged out) ─────────────────────┐
│                                                                              │
│             ┌─ Login panel (max 420 px) ─────────────────────┐               │
│             │ Logg inn                                       │               │
│             │ Prognose foreslår hvor mye du bør bestille     │               │
│             │ neste uke, og viser hvordan tallene er regnet. │               │
│             │                                                │               │
│             │ ! Feil kundenummer eller passord.              │ ← after a     │
│             │                                                │   failed try  │
│             │ Kundenummer                                    │               │
│             │ [__________________________]                   │               │
│             │ Passord                                        │               │
│             │ [__________________________]                   │               │
│             │                                                │               │
│             │ [ Logg inn ]                                   │               │
│             │                                                │               │
│             │ Innloggingen for testbedriftene står i README. │               │
│             └────────────────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Wireframe: Samlet bestillingsoversikt (spine-only, FR-30, Should)

```
┌─ App header ── Produktoversikt · [Samlet bestillingsoversikt] · Logg ut ──────┐
├─ Settings bar ───────────────────────────────────────────────────────────────┤
│ Samlet bestillingsoversikt                                                   │
│ Bestillingene for neste uke, uke 46. Prognose bestiller ingenting: ta        │
│ listen med til innkjøpsmøtet.                                                │
│                                                                              │
│ (1) Se hva som haster  (2) Gå gjennom produktene  (●3) Ta med den samlede    │
│  done                   done                        bestillingsoversikten    │
│                                                                              │
│ ┌─ Combined order table ───────────────────────────────────────────────────┐ │
│ │ Varenr.  Produkt                   Bestillingsmengde   Merking           │ │
│ │ 10007    Isskrape                                  7   Foreslått         │ │
│ │ 10012    Strøsand 25 kg            13 (foreslått 11)   [Justert av deg]  │ │
│ │ 10031    Lyspære LED E27 9 W                       9   Foreslått         │ │
│ │ 10004    Skruer 4×40 mm, 200 stk.                  4   Foreslått         │ │
│ │ 10040    Snøskuffe aluminium                       –   Uten prognose     │ │
│ │ 10001    Malertape 25 mm                           0   Foreslått         │ │
│ │ … 24 produkter til                                                       │ │
│ │ Totalt                                            33                     │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│ [ Tilbake til produktoversikten ]                                            │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Innstillinger (spine-only)

The page starts with «Endringen gjelder alle produkter i bedriften.» (FR-21) and has one field per setting (FR-20):

| Setting | Control | Values | Notes |
|---|---|---|---|
| Prognosemetode | radio buttons «Glidende gjennomsnitt» and «Eksponentiell glatting» | default glidende gjennomsnitt | |
| Vindu | number field, unit «uker» | 2–12, default 3 | with exponential smoothing: disabled, «Ikke i bruk med eksponentiell glatting.»; with the script, enabled as soon as «Glidende gjennomsnitt» is chosen, before saving |
| Glattingsfaktor | number field | 0,1–0,9, default 0,3 | with the moving average: disabled, «Ikke i bruk med glidende gjennomsnitt.»; with the script, enabled as soon as «Eksponentiell glatting» is chosen, before saving |
| Scenarioprosent | number field, unit «%» | 0–50, default 10 | |
| Sikkerhetsmargin | number field, unit «%» | 0–100, default 10 | |
| Uvanlige uker | radio buttons «Tas med» and «Holdes utenfor» | default tas med | also the switch below the chart |
| Sesongjustering | checkbox | off by default | only when FR-9 is built |

«Lagre» applies the change to every product at once and returns to the page you came from with the confirmation message. «Avbryt» returns without changes. Number fields accept a decimal comma or a decimal point (NFR-10), and a value whose extra decimals are all zero counts as that number: 10,0 is 10 and 0,30 is 0,3. The method and the setting it uses are saved together; without the script, a field that is disabled for the saved method is changed in a second save.

## Voice and Tone

Microcopy. The aesthetic posture is in DESIGN.md (Brand & Style).

| Do | Don't |
|---|---|
| «Foreslått bestillingsmengde for neste uke, uke 46» | «Smart anbefaling!» |
| «Prognose foreslår ingen mengde for dette produktet. Du bestemmer bestillingen selv.» | «Feil: prognose kunne ikke beregnes» |
| «Uke 38 og 39: utsolgt, holdt utenfor beregningen.» | «Datakvalitetsproblem oppdaget» |
| Glossary labels verbatim: «Lagerbeholdning», «Uker dekning», «Tillitsmerke», «Grunnprognose» | Synonyms: «beholdning», «dekningsgrad», «score», «basisprognose» |
| «10 %», «14,3», «−40,00» | «10%», «14.3», «-40» |
| Prognose speaks in the third person («Prognose foreslår …») and calls the user «du» | «Vi», «systemet», «KI-en» |
| Short, complete sentences that end with a full stop | Exclamation marks, emojis, urgency words beyond «Se hva som haster» |

## Message Catalogue

The copy source for every warning, note, confirmation and error (FR-25 checks each one "with its Norwegian text"). Texts in square brackets are filled from the calculation result; everything else is fixed. «PRD» means the text is fixed there, and «UX» that this spine fixes it.

| Message | When | Norwegian text | Source |
|---|---|---|---|
| Login error | wrong customer number or password | «Feil kundenummer eller passord.» | PRD FR-1 |
| Stockout weeks (warning) | stockout weeks in the recent period | «Uke [38 og 39]: utsolgt, holdt utenfor beregningen.» | UX, FR-15 |
| Unusual weeks (warning) | unusual weeks in the recent period | «Uke [42]: uvanlig høyt salg ([31]), tatt med i beregningen.» When excluded: «… holdt utenfor beregningen.» Several: «Uke [40 og 42]: uvanlig høyt salg ([29 og 31]), …» | UX, FR-16 |
| Level shift | a level-shift week in the recent period | In the reason (Must): «Middels: nytt nivå de siste 12 ukene.» Warning (Should): «Etterspørselen ser ut til å ha endret nivå.» | PRD FR-17, FR-17b |
| Old data (warning) | latest valid week more than 8 weeks before the latest data week | «Det har gått [9] uker siden siste gyldige uke, så prognosen bygger på gamle data.» | UX, FR-18 |
| Insufficient data, few weeks | fewer than 3 valid weeks | List: «Ingen prognose: færre enn 3 gyldige uker». Warning: «Produktet har [2] gyldige uker. Prognose regner ut en prognose når produktet har minst 3 gyldige uker.»; with one valid week «Produktet har [1] gyldig uke. Prognose regner ut en prognose når produktet har minst 3 gyldige uker.», and with none «Produktet har [0] gyldige uker. …» | PRD FR-24; UX, FR-8 |
| Insufficient data, window | moving average with fewer calculation weeks than the window | List: «Ingen prognose: færre uker enn vinduet». Warning: «Glidende gjennomsnitt over [12] uker trenger [12] uker brukt i beregningen. Produktet har [10].» | UX, FR-8 |
| Seasonal pattern (warning, Should) | R-17 pattern not used | «Produktet har tydelig sesongvariasjon som prognosen ikke tar hensyn til.» | PRD FR-36 |
| Flat weeks 2 and 3 (note) | no seasonal adjustment | «Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong.» | PRD FR-7 |
| Seasonal adjustment not possible (note, Should) | R-14 step 4 | «Sesongjustering kunne ikke brukes for dette produktet, så ukeprognosene er regnet uten.» | UX, FR-9 |
| Overstock (note, Should) | suggestion 0 and stock above 0 | «Lagerbeholdningen dekker forventet behov neste uke.» | PRD FR-14 |
| Stock not lasting (note, Could) | FR-33 | «Lageret og bestillingen dekker ikke uke 2 og 3.» | UX, FR-33 |
| Scenario text | next to the scenarios | «Scenarioene viser hva som skjer hvis salget blir [10] % høyere eller lavere. De er ikke sannsynligheter.» | PRD FR-10 |
| Order calculation line | always, with a forecast | «Prognose [14,3] + sikkerhetsmargin [10] % ([1,4]) − lager [5] = [10,77] → foreslått bestillingsmengde [11]». When the suggested quantity is 0 and the stock on hand is above 0 (the stock covers the need): «… → foreslått bestillingsmengde 0 (lageret dekker behovet)»; with no stock and no expected sales the line ends «… foreslått bestillingsmengde 0» (E23). Then «Tallene er avrundet for visning.» | PRD FR-12 |
| Safety-margin text | below the order calculation line | «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.» | PRD FR-12 |
| Forecast calculation | always, with a forecast | «Glidende gjennomsnitt, [3] uker: ([16] + [12] + [15]) / [3] = [14,3]» or «Eksponentiell glatting, faktor [0,3]: [0,3] × [15] + [0,7] × [13,3] = [13,8]» | PRD FR-35 |
| Status tag sentence | below the sales table | Explains the tags that are on the table, in this order: ««Brukt» viser de [3] ukene i glidende gjennomsnitt.» (exponential smoothing: ««Brukt» viser alle beregningsukene i eksponentiell glatting.»); «Uke [38 og 39] er utsolgte uker og er holdt utenfor beregningen.» (singular: «Uke [38] er en utsolgt uke …»); «Uke [42] er en uvanlig uke og er tatt med, fordi innstillingen er «tas med».» (plural «uvanlige uker»; with the setting off: «… er holdt utenfor, fordi innstillingen er «holdes utenfor».»); «Uke [43, 44 og 45] er nytt nivå og er alltid tatt med i beregningen.» Only the tags on the table are explained, so «Brukt» is left out when no used week is shown. Without a forecast the calculation is not mentioned: «Uke [42] er en uvanlig uke.», «Uke [43, 44 og 45] er nytt nivå.» | UX, FR-15 to FR-17 |
| Weeks left out (text) | «Prognoseutregning», when a week is left out | «Holdt utenfor: uke [38 og 39] (utsolgt).» Several kinds in one sentence, stockout weeks first and each kind in time order: «Holdt utenfor: uke [42 og 43] (utsolgt), uke [44] (uvanlig).» A list that holds a week before the last 12 weeks writes the year on every week («uke 10/2025 og 11/2025»); the first week of a new year always has it. With unusual weeks excluded and at least one unusual week left out: «[3] uker brukt i beregningen.» | UX, FR-15, FR-16, UX-DR42 |
| No sales weeks | product without a sales week | In place of the sales table: «Produktet har ingen salgsuker.» | UX, FR-8 |
| Confidence label reason | always | «[Høy, Middels or Lav]: [deciding condition].», then any other active warnings. Examples: «Høy: minst 104 uker salgshistorikk, minst 100 gyldige uker og ingen varsler.» «Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene.» «Middels: kortere salgshistorikk enn 104 uker.» «Middels: færre enn 100 gyldige uker.» «Lav: ingen prognose, færre enn 3 gyldige uker.» «Lav: ingen prognose, færre uker enn vinduet.» «Lav: færre enn 12 gyldige uker. 1 utsolgt uke de siste 12 ukene.» «Middels: gamle data, 9 uker siden siste gyldige uke.» (guard case: it cannot occur under R-15 and R-16 today, because old data means at least 9 sold-out weeks among the last 12 and the stockout phrase then comes first; the wording is fixed here so that it holds if the rules change). When several conditions for the same label apply, the first in R-16 order decides: an active warning, then a sales history shorter than 104 weeks, then fewer than 100 valid weeks. The stockout, unusual-week and level-shift warnings of the recent period are one phrase before «de siste 12 ukene», in R-15 order («2 utsolgte uker, 1 uvanlig uke og nytt nivå de siste 12 ukene»); old data is its own phrase, «gamle data, [9] uker siden siste gyldige uke», and after another warning the sentence «Gamle data, [9] uker siden siste gyldige uke.» The warning that a condition names is not repeated (insufficient data after «Lav: ingen prognose …»). | PRD FR-19 format; UX texts, R-16 |
| No decision | product without a forecast | «Prognose foreslår ingen mengde for dette produktet. Du bestemmer bestillingen selv.» | UX, FR-8 |
| Settings area | wherever settings can change | «Endringen gjelder alle produkter i bedriften.» | PRD FR-21 |
| Settings confirmation | after a change | «Innstillingen er endret: [sikkerhetsmargin] er nå [50] %.», then one line per affected value: «[Foreslått bestillingsmengde]: [11] → [17]». No difference: «[Grunnprognose]: [14,3] → [14,3] (uendret)». A change that removes or gives a forecast shows «–» for the missing value: «[Grunnprognose]: [14,3] → –» | PRD FR-21 format; UX for «(uendret)» and «–» |
| Value out of range | FR-20 | «[Sikkerhetsmargin] må være mellom [0] og [100] %. Den forrige verdien er beholdt.» | UX, FR-20 |
| Not a number | empty or non-numeric input | «Skriv et tall, for eksempel 10 eller 0,3. Den forrige verdien er beholdt.» | UX, NFR-10 |
| Setting not in use | FR-20 | «Ikke i bruk med eksponentiell glatting.» / «Ikke i bruk med glidende gjennomsnitt.» | UX, FR-20 |
| Adjusted quantity invalid (Should) | FR-29 | «Skriv et helt tall fra 0 og oppover.» | UX, FR-29 |
| Markings (Should) | combined order overview, cards | «Foreslått» / «Justert av deg»; «Uten prognose» for a product without a forecast and without an adjusted quantity | PRD FR-30 |
| No products | the company has no products | «Ingen data er lastet inn. Kjør [lastekommandoen] som står i README.» with the exact command filled in | UX, FR-24 |
| No search match | search finds nothing | «Ingen produkter passer søket.» and the link «Vis alle produkter» | UX |
| Not found | NFR-10, FR-2 | «Siden finnes ikke.» and the link «Til produktoversikten» | UX |
| Database unavailable | the database does not answer (NFR-10) | «Prognose får ikke kontakt med databasen. Prøv igjen om litt. Kjører du Prognose på din egen maskin, må databasen være startet slik README beskriver.» | UX |
| Server error | any other error, including a request the app cannot use (NFR-10) | «Noe gikk galt, og siden kunne ikke vises. Prøv igjen, eller gå til produktoversikten.» and the link «Til produktoversikten» | UX |
| Expired form | a form's security check fails (NFR-10) | «Skjemaet er utløpt. Last siden på nytt og prøv igjen.» | UX |
| AI label (Should) | FR-28 rephrased text | «KI-omformulert forklaring» | PRD FR-27 |

## Component Patterns

Behavioral rules. Visual specs are in DESIGN.md (Components), with the same names.

| Component | Where | Behavioral rules |
|---|---|---|
| App header | every page | Marks the current page. «Logg ut» ends the session and opens Innlogging (FR-1). |
| Settings bar | every page after login | Shows the settings in use: the method with its window or factor, the scenario percentage, the safety margin, unusual weeks, and seasonal adjustment once FR-9 is built. «Endre innstillinger» opens Innstillinger. |
| Product list | Produktoversikt, Produktside | All products in R-12 order: «Bestill snart» (weeks of cover, lowest first; ties by product number), «Uten prognose» (by product number), «Øvrige produkter» (by product number). Every card and row shows every FR-24 field. The list keeps its scroll position when a product is selected. In the one-column layout it follows the product area, with no scroll frame of its own (Responsive & Platform). |
| Group heading | product list | Names the group and sums it up: «4 produkter · 31 enheter foreslått», «1 produkt · du bestemmer selv», «25 · etter varenummer». An empty group is not shown. |
| Product card | «Bestill snart», «Uten prognose» | The whole card is one link. It shows the reason unless the label is «høy». Without a forecast, the reason replaces the week-1 forecast, and the quantity and weeks of cover show «–» (FR-24). With FR-29, an adjusted quantity is shown with «Justert av deg» in place of «Foreslått». |
| Product row | «Øvrige produkter» | The same fields as a card, on two lines; the whole row is one link. Shows the FR-14 note once it is built. |
| Search field | top of the list | Filters the list by product number or name, ignoring case; the groups keep their order. A plain form that works on Enter and always goes to Produktoversikt, also from Produktside; filtering while typing is an enhancement. The previous and next links ignore the filter. |
| Trust label | cards, rows, product header, trust panel | The word is always text and the shape is decoration. Its reason follows the Message Catalogue. |
| Panel | every surface | Holds one question or one task under one heading. A panel never contains another panel; inside it, structure comes from headings, tables and hairlines. |
| Decision panel | Produktside | Shows the suggested order quantity for week 1 (FR-11). With FR-29: «Behold [11] og gå videre» keeps the suggestion and opens the next product in the review sequence. «Juster mengden» opens a whole-number field labeled «Justert bestillingsmengde», with «Lagre» and «Tilbake til forslaget», and the suggestion stays visible next to the adjusted quantity. For a product outside the review sequence, «Behold … og gå videre» opens the next product in R-12 order. Without a forecast, «Sett mengden selv» opens the same field. Without FR-29 there are no buttons, and the previous and next links do the job. With FR-14, the overstock note stands below the suggested order quantity when it is 0 and the stock on hand is above 0. |
| Trust panel | Produktside | The label, its reason, and every active warning (R-15) whose FR is built, in R-15 order, and nothing that does not apply (FR-25). Together with the decision panel it is visible without scrolling at 1366 × 768 (FR-25). |
| Warning list | trust panel | One row per active warning, worded as in the Message Catalogue. Stockout and unusual weeks before the recent period are not warnings; the forecast calculation lists them (R-15). |
| Unusual-weeks switch | below the chart legend | Changes the company setting «Uvanlige uker» between «tas med» and «holdes utenfor» in one step (UJ-1 step 4). The page reloads with the confirmation message, and the change applies to every product (FR-21). It is a real checkbox with `role="switch"`, so Space toggles it. Without the script, the small secondary button «Lagre» next to it sends the change; the script hides the button and sends the change on toggle. |
| Forecast chart | Produktside, right below the two panels | Shows the whole sales history (up to 104 weeks) and the three forecast weeks with the scenario band, so every stockout, unusual and level-shift week has its own marker (FR-15 to FR-17, FR-25). The last 12 weeks are marked «Siste 12 uker», with no mark when the whole history lies in them. The legend explains every marker type, whether or not this product has one. Text alternative: see Accessibility Floor. On a narrow screen the chart keeps its label sizes and scrolls sideways inside its own frame, and the text alternative gives the same values (NFR-6). The mockup shows only the last 12 weeks. |
| Calculation worksheet | Produktside, below the chart | In order: «Salgshistorikk, siste 12 uker» (week, units sold, status), or «Salgshistorikk, alle ukene» for a history of 12 weeks or fewer; «Prognoseutregning» (FR-35, with the weeks used and every week left out, with its reason); «Ukeprognoser og scenarioer» (weeks 1–3, three scenarios, the FR-13 column once built, the FR-10 text and the FR-7 note, or the FR-9 note when seasonal adjustment could not be used); «Utregning av bestillingsmengde» (FR-12). A table wider than the panel scrolls inside its own frame, and calculation lines wrap between terms (NFR-6). |
| Calculation line | worksheet | The exact FR-12 or FR-35 format, the rounding note inside the box, and the FR-12 safety-margin text below. |
| Status tag | sales table | One tag per kind of flag on a week: «utsolgt», «uvanlig» (an unusual week that is taken into the calculation), «uvanlig, holdt utenfor» (one that the setting leaves out; hollow triangle and dashed border, so it differs from «uvanlig» by words and shape and not only by colour), «nytt nivå», or «brukt» for a week used in the forecast (the last N calculation weeks for the moving average; every calculation week for exponential smoothing). A week can have «brukt» beside «uvanlig» or «nytt nivå». |
| Explanation panel | last on Produktside | The template explanation (FR-26), with only the numbers FR-27 allows (see Explanation). |
| Button | everywhere | The label says what happens. At most one primary button per panel. |
| Week path | «Denne uken» | Step 1 is current on Produktoversikt. Step 2 opens the first product in the review sequence. Step 3 opens Samlet bestillingsoversikt; without FR-30 the path has two steps. |
| Week figures | «Denne uken» | Products with order-soon status; units suggested in total (the sum of the suggested order quantities); products without a forecast; products with at least one active warning. Plain figures, not links. |
| Trust legend | «Denne uken» | «Slik leser du tillitsmerket»: each trust label with its conditions, as fixed text. «Høy»: «Minst 104 uker salgshistorikk, minst 100 gyldige uker og ingen varsler.» «Middels»: «Minst ett varsel, kortere salgshistorikk enn 104 uker eller færre enn 100 gyldige uker.» «Lav»: «Ingen prognose, eller færre enn 12 gyldige uker.» The labels use the trust label component. |
| Progress bar | Produktside header | The place in the review sequence: «produkt [2] av [4] som bør bestilles snart», then «produkt [1] av [1] uten prognose». Not shown for «Øvrige produkter». |
| Previous and next links | Produktside header | The previous and next product in R-12 order, across all groups. |
| Keyboard key | end of the list | Shows «↑ ↓ forrige og neste produkt · Enter åpner produktet». Hidden on touch screens, which have no keyboard to use it with (NFR-6). |
| Confirmation message | top of the product area | After a settings change: the new setting, and the old → new value of what it affects, as in the FR-21 table. Shown once, with `role="status"`. |
| Error message | above the field or form it concerns | `role="alert"`, and the previous value stays (FR-20, NFR-10). |
| Settings form | Innstillinger | See Information Architecture. |
| Login panel | Innlogging | Customer number and password with visible labels; Enter submits. After an error the customer number is kept and the password is cleared, and the message does not say which one was wrong (FR-1). |
| Combined order table | Samlet bestillingsoversikt (FR-30, Should) | Every product in R-12 order with its suggested or adjusted quantity and its marking; an adjusted row shows the suggestion in brackets; a product without a forecast and without an adjusted quantity shows «–» and «Uten prognose» (FR-30); a total row; each product name links to its Produktside. |
| Not-found panel | unknown addresses, other companies' products, error pages | Shows no data from another company (FR-2) and links to Produktoversikt. The error pages (database unavailable, server error, expired form) use the same panel, with the first sentence of their message as the page title. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Logged out | any page | Innlogging (FR-1). |
| Login failed | Innlogging | Error message above the fields, customer number kept, password cleared. |
| No products loaded | Produktoversikt | The list shows the «No products» message; «Denne uken» is not shown (FR-24). |
| No search match | product list | «Ingen produkter passer søket.» and «Vis alle produkter». |
| Nothing to order soon | Produktoversikt | No «Bestill snart» group; the first week figure shows 0. |
| Product selected | product list | The card or row has `aria-current="page"` and the selected style. |
| No forecast: fewer than 3 valid weeks | card, row, Produktside | FR-24 in the list. On Produktside: «–» and «Ingen foreslått bestillingsmengde», the «No decision» sentence, «Lav» with its reason and warning. The chart shows the weeks that exist without a forecast region; the worksheet shows only the sales table. See the mockup's third frame. |
| No forecast: window longer than the calculation weeks | card, row, Produktside | As above, with the window texts (FR-8, E11 b). |
| Suggested order quantity 0 | card, row, Produktside | «Foreslått 0» in ink; the order calculation line ends «(lageret dekker behovet)» when stock covers the need; the FR-14 note once built, in the decision panel on Produktside and on the row in the list. |
| Week-1 forecast 0 | card, row | Weeks of cover «–», no order-soon status, no overstock note (R-12, E23). |
| Unusual weeks excluded | Produktside | The switch is off; the chart still marks them (FR-16); the warning says «holdt utenfor»; «Prognoseutregning» lists each excluded week and the number of weeks used (FR-16). |
| Level shift in the recent period | Produktside | The reason names it (FR-17); diamond markers and «nytt nivå» tags; the FR-17b warning once built. |
| Old data | Produktside | The old-data warning; the label is at most «middels» (R-16). |
| Seasonal adjustment on (Should) | Produktside | Week forecasts differ and the FR-7 note goes; the worksheet shows the indices and adjusted values (FR-35). When it cannot be used: the FR-9 note, in «Ukeprognoser og scenarioer» where the FR-7 note stands. |
| Seasonal pattern not used (Should) | Produktside | The FR-36 warning. |
| Settings changed | page you came from | Confirmation message with old → new; «(uendret)» when nothing changed. |
| Invalid setting | Innstillinger | Error message at the field; the previous value stays. |
| Quantity adjusted (Should) | card, decision panel, combined table | «Justert av deg» with the adjusted quantity; the suggestion stays visible; «Tilbake til forslaget» resets it (FR-29). The adjustment lasts for the session (FR-31 is Could). |
| Last product reviewed | Produktside | On the last product of the review sequence, and on the last product in R-12 order, the primary button becomes «Gå til samlet bestillingsoversikt» (FR-30), or «Tilbake til produktoversikten» without it. |
| Language model on (Should) | explanation panel | «KI-omformulert forklaring» above the text; on any FR-28 failure the template text, without an error message. |
| Not found | any address | Not-found panel (FR-2, NFR-10). |
| Error | any page | The not-found panel with the Database unavailable, Server error or Expired form text; no data and no technical details (NFR-10). |
| Reload, Back, double submit | any page | The same result and no error (NFR-10). |
| Focus | every control | A 3 px outline in `{colors.blue}`, 2 px outside the element; in the app header the outline is `{colors.on-header}` (DESIGN.md, Elevation & Depth). |

## Interaction Primitives

- **Links and forms.** Every action is a link or a form submission, so everything works without scripts (Foundation).
- **Keyboard.** Tab follows the order of the page: header, settings bar, list, product, also in the one-column layout, where the product area is shown above the list; on Produktside the skip link «Gå til produktet» comes first (Accessibility Floor). In the list, ↑ and ↓ move between products and Enter opens one (an enhancement; Tab and Enter always work). Space toggles the switch. There are no shortcuts without a visible hint.
- **Mouse and touch.** Click or tap anywhere on a card or row. Nothing depends on hover, nothing is dragged, and a swipe only scrolls the page or a scroll frame. On touch screens every control has a target of at least 44 × 44 px, and form fields use 16 px text so that the phone does not zoom in when a field is selected (NFR-6).
- **Review sequence.** «Bestill snart», then «Uten prognose» (R-12 groups 1 and 2). «Behold … og gå videre» moves through it; previous and next cover every product.
- **Settings.** The switch below the chart changes unusual weeks in one step; Innstillinger changes the rest. Every change applies to every product at once and ends with the confirmation message (FR-21).
- **Banned:** modals, popovers, tooltips as the only home of information, auto-refresh, animation, infinite scroll, drag, hover-only controls, and color-only signals.

## Calculation Display Rules

| What | Rule |
|---|---|
| Rounding | As R-9 (display rounding). |
| Number format | Decimal comma; «%» after a space («10 %»); the minus sign «−»; no thousands grouping. |
| Rounding note | «Tallene er avrundet for visning.» inside the order calculation line (FR-12), and also below the exponential-smoothing line and the seasonal values (FR-35). |
| Moving average | The FR-35 line, then «Uker brukt: uke 43, 44 og 45.» and «Holdt utenfor: uke 38 og 39 (utsolgt).». With unusual weeks excluded, each excluded week is listed, as «Holdt utenfor: uke 38 og 39 (utsolgt), uke 42 (uvanlig).», and «[3] uker brukt i beregningen.» is stated (FR-16). |
| Exponential smoothing | The FR-35 line for the last update, and a table of every calculation week with its sales and level in its own scroll frame (FR-35). |
| Seasonal adjustment (Should) | The indices (four decimals) and adjusted values (one decimal) for the weeks used and for weeks 1–3, and the week forecasts (FR-35, E14); the decimals follow R-9. |
| Week labels | Horizon columns read «Uke 1 · uke 46». Chart axes use week numbers; the first week of a new year carries its year («1/2027»), and lists that reach before the recent period show the year («uke 10/2025»). The explanation may name these years (FR-27). |
| Weeks left out | Every stockout week and excluded unusual week in the history, with its reason, in «Prognoseutregning»; the recent ones are also warnings (R-15). |
| Missing values | «–» for the suggested order quantity and weeks of cover without a forecast (FR-24), and for weeks of cover when the week-1 forecast is 0 (E23). |
| Order quantity per scenario (Should) | A «Bestillingsmengde» column in the scenario table, calculated from week 1 (FR-13, E22). |

## Explanation

- **Place:** its own panel titled «Forklaring», last on Produktside, below every calculated number (FR-27).
- **Content, in order (FR-26):** the method and settings; the number of calculation weeks and the week forecasts; the weeks left out and why; every active warning and note; the order calculation; the weeks of cover; the confidence label and its reason; the scenarios.
- **Numbers:** only the ones FR-27 allows. Templates therefore leave out sales figures and the week numbers of calculation weeks, included unusual weeks and level-shift weeks. A year appears only next to a week left out or a horizon week that lies in another year than the latest data week (FR-27). Example for Strøsand 25 kg, as in the mockup: «Prognosen bruker glidende gjennomsnitt over de 3 siste ukene brukt i beregningen. Det gir 14,3 per uke for uke 46, 47 og 48. Uke 38 og 39 er holdt utenfor fordi varen var utsolgt. Det er 1 uvanlig uke de siste 12 ukene, og uvanlige uker tas med i beregningen. Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong. Med 10 % sikkerhetsmargin (1,4) og 5 på lager blir utregningen 10,77, og Prognose foreslår å bestille 11. Lageret dekker 0,3 uker. Tillitsmerket er middels fordi det er 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene. Scenarioene viser 15,8 hvis salget blir 10 % høyere, og 12,9 hvis det blir 10 % lavere.»
- **Language model (FR-28, Should):** rephrased text carries «KI-omformulert forklaring». On any failure the template text is shown without an error.
## Accessibility Floor

Behavioral; visual contrast is in DESIGN.md (Colors).

- WCAG 2.2 AA on every surface, and pages declare `lang="nb"` (NFR-11).
- Every function works with the keyboard alone, with the visible focus ring (NFR-11). On Produktside the first focusable element is a skip link «Gå til produktet». The product list and the product area are labeled regions («Produkter», «Valgt produkt»); where they scroll on their own, keyboard users can scroll them. In the one-column layout the product area is shown above the list while the HTML order stays the same, so the skip link stays the first focusable element on Produktside.
- Every field has a visible label, the search field included (NFR-11).
- Headings: one `h1` per page (the product name, «Denne uken», the page title); panels use `h2`, worksheet subsections and list groups use `h3`.
- The selected product has `aria-current="page"`. Trust labels are text; their shapes are hidden from screen readers.
- **Chart text alternative (NFR-11):** the chart has a title and a short summary (weeks shown, stockout, unusual and level-shift weeks, forecast and scenario range). Its plotted values are in the worksheet's tables, plus a disclosure «Tabell med alle ukene i grafen» with every plotted week. Markers differ by shape, and the legend names each one (NFR-7).
- Confirmations use `role="status"`, errors `role="alert"`, and field errors are linked to their field with `aria-describedby`.
- No timing, no motion, and no content that appears only on hover.
- From 320 px wide, the page does not scroll sideways, no text overlaps or is cut off, and every control is reachable with the keyboard and by touch (NFR-6). Only wide tables and the chart scroll sideways, inside their own frame.

## Responsive & Platform

| Width | Behavior |
|---|---|
| ≥ 1181 px | The list (`{spacing.list-width}`) beside the product; the decision panel and the trust panel side by side, with the chart below them. |
| 901–1180 px | The list narrows to `{spacing.list-width-narrow}`; the two panels stack, decision first. |
| ≤ 900 px | One column, also on an iPad held upright and on a phone: the product area first (the product on Produktside, «Denne uken» on Produktoversikt), then the product list. Neither has a scroll frame of its own; the page scrolls, and the previous and next links move between products. |
| 320 px and wider | No horizontal page scrolling, nothing overlaps or is cut off, and every control is reachable with the keyboard and by touch (NFR-6). Only wide tables and the chart scroll sideways, inside their own frame, and the chart keeps its label sizes; calculation lines wrap between terms. The app header and the settings bar wrap onto more lines. |
| 1366 × 768 | The suggested order quantity, the confidence label and the active warnings are visible without scrolling (FR-25); the chart starts right below them. |
| Smaller screens | The suggested order quantity, the confidence label and the active warnings come first in the product area, right after the product header (NFR-6). |
| Touch screens | Every control has a target of at least 44 × 44 px, form fields use 16 px text, and the keyboard hint is hidden (NFR-6). |
| Test sizes | 1366 × 768 (PC); 820 × 1180 and 1180 × 820 (iPad); 390 × 844 (iPhone 13); 360 × 800 (Android); and 320 px wide. 1366 × 768 is tested in the desktop browsers. The iPhone 13 is also tested on the real phone over the local network; the iPad and Android sizes and 320 px only in the browser's responsive view. The QA log and the README keep the two kinds of test apart (NFR-6). |

## Inspiration & Anti-patterns

- **From concept C «Instrumentpanelet»:** the list and the selected product on one screen, the settings bar, the large chart with shape markers, and arrow-key stepping.
- **From concept B «Innkjøpsmøtet»:** product cards with the quantity in large type, the plain-language panel questions, the three-step week path, «Behold og gå videre», and the switch for unusual weeks.
- **From concept A «Arket»:** the worksheet that reads like a hand calculation, the weekly sales table with status tags, monospace formulas and the explanation.
- **Not picked (left out):** sparklines in the list and key-figure tiles (C); filter chips and letter-box labels (A); numbered question circles (B).
- **Rejected by the PRD:** excluding unusual weeks by default (FR-16), color-only markers (NFR-7), numbers produced by AI (AG-1), and placing orders (PRD §7).
- **Rejected for this register:** shadows, gradients, cream backgrounds, side stripes on cards, and celebratory feedback.

## Key Flows

### Flow 1 — UJ-1. Mounia plans next week's purchases before the Monday meeting

Mounia, purchasing manager at a small hardware store with about 30 products, has 20 minutes before the meeting, at the office PC.

1. Mounia opens Prognose and logs in with the company's customer number and password (Innlogging).
2. Produktoversikt opens with «Denne uken»: 4 products to order soon, 31 units suggested, 1 product without a forecast, 4 with warnings (Strøsand 25 kg, Skruer, Snøskuffe aluminium and the E8 demo product). The list shows «Bestill snart» first, lowest weeks of cover first (UJ-1 step 1).
3. She selects «Start med Isskrape», keeps the suggested 7 and moves on to Strøsand 25 kg.
4. Without scrolling she sees «11», «Middels» and the two warnings; the chart right below shows the gap in weeks 38–39 and the peak in week 42 (UJ-1 steps 2–3).
5. She scrolls to «Slik er tallene regnet ut»: (16 + 12 + 15) / 3 = 14,3, and the order calculation line ends at 11. She reads «Forklaring» (UJ-1 step 3).
6. To see how much unusual weeks matter, she opens the demo product built from E8 (DR-1), whose two unusual weeks are among the 3 weeks used, and switches unusual weeks off below the chart. The confirmation shows «Grunnprognose: 41,0 → 21,3» and says the change applies to all products. She switches back (UJ-1 step 4). On Strøsand 25 kg the same switch would show «Grunnprognose: 14,3 → 14,3 (uendret)», because week 42 lies outside the 3-week window.
7. She chooses «Behold 11 og gå videre», or «Juster mengden» and 13 (FR-29), and continues through the list (UJ-1 step 5).
8. After the last product she opens Samlet bestillingsoversikt, where every product is marked «Foreslått» or «Justert av deg», and the product without a forecast «Uten prognose» (UJ-1 step 6, FR-30).
9. **Climax:** for every product she has one number for next week, how it was calculated, and whether to trust it, on one list she takes to the meeting.

Failure paths: a wrong login shows «Feil kundenummer eller passord.». A product without a forecast shows «Du bestemmer bestillingen selv», and with FR-29 she sets the quantity herself. When the stock covers the need, the line ends «(lageret dekker behovet)». In a Must-only build, steps 7–8 use the previous and next links, and the meeting list stays outside Prognose.

### Flow 2 — The examiner checks a forecast by hand

Ingrid, the course examiner, on her own laptop, with the README and the reference spreadsheet open.

1. Ingrid follows «Prøv selv» in the README (DR-1) and opens the local app. She logs in as Testbedrift A.
2. In Produktoversikt she picks a rule test product named in the README table, for example Strøsand 25 kg (E1, E4).
3. On Produktside she compares «Slik er tallene regnet ut» with the spreadsheet: the weekly sales, «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3» and the order calculation line «… = 10,77 → foreslått bestillingsmengde 11».
4. She opens «Endre innstillinger», sets the safety margin to 50 % and saves. Back on the product, the confirmation shows «Foreslått bestillingsmengde: 11 → 17» (SM-3).
5. **Climax:** the screen matches her hand calculation and the spreadsheet, and the change shows its previous and new value.
6. She sets the safety margin back to 10 %.

Failure paths: a value outside the range, for example 150, shows «Sikkerhetsmargin må være mellom 0 og 100 %. Den forrige verdien er beholdt.». If the local database is not started, every page shows the database message, and the README says how to start it.

### Flow 3 — SM-10. Someone outside the group explains «lav»

Jonas, a fellow student outside the group, is shown Prognose for the first time.

1. Jonas sees Produktside for Snøskuffe aluminium: «Lav» and «Ingen foreslått bestillingsmengde».
2. The trust panel says «Lav: ingen prognose, færre enn 3 gyldige uker.» and «Produktet har 2 gyldige uker. Prognose regner ut en prognose når produktet har minst 3 gyldige uker.».
3. **Climax:** asked why the label is «lav», Jonas answers without reading aloud: "it has too few weeks of sales to make a forecast". He names the deciding condition, which is what SM-10 checks (R-16).
4. The check is recorded in the QA log (DR-9).

Failure path: if Jonas cannot explain the label, the reason texts in the Message Catalogue are revised and the check is repeated, while there is still time to fix it (SM-10).

## Open Questions and Assumptions

No open questions remain. On 2026-11-16 the user approved the five assumptions that stood here, and the PRD was updated the same day:
- «Uten prognose» is sorted by product number (R-12).
- A settings change that does not alter a value is confirmed with «(uendret)» (Message Catalogue).
- In Samlet bestillingsoversikt, a product without a forecast and without an adjusted quantity shows «–» and «Uten prognose», in R-12 order (FR-30).
- The rounding note also appears below the exponential-smoothing line and the seasonal values; seasonal indices have four decimals and adjusted values one (FR-35, R-9).
- Weeks show their year at New Year and in lists that reach before the recent period, and the explanation may name these years (FR-27).

The user also decided that the demo for UJ-1 step 4 uses the rule test product built from E8 (DR-1, Flow 1), and that the chart shows the whole sales history.

**Mockup differences (the spine wins):** the mockup's chart shows only the last 12 weeks, while the chart shows the whole sales history. The legend icons in the mockup may render larger than 14 and 24 px, because the chart's `width: 100%` rule also matches them. Two mockup values cannot occur under the rules: Skruer's week-1 forecast of 21,5, because a 3-week moving average of whole units gives 21,3 or 21,7 (the seed uses 21,3, and the suggestion 4 and the weeks of cover 0,9 stay), and Kabelstrips' weeks of cover of 3,7, because 25 ÷ 6,667 gives 3,8 under R-9. The mockup's «Denne uken» counts 3 products with warnings; with the E8 demo product in Testbedrift A it is 4 (Flow 1).

## Change Log

The spine pair (DESIGN.md and EXPERIENCE.md) was set to `final` on 2026-11-16. Every later change to either file is recorded here with the date, the reason and the commit, as PRD §12 and DR-5 require.

| Date | Change | Reason | Commit |
|---|---|---|---|
| 2026-11-16 | The five assumptions became decisions. «Uten prognose» added to the markings and the combined order table. Flow 1 uses the E8 demo product for unusual weeks. The explanation may name years (FR-27). DESIGN.md: the «Uten prognose» marking in red. | The user's decisions before the architecture; the PRD was updated the same day (R-9, R-12, FR-27, FR-30, FR-35, DR-1). | `5373e7b` |
| 2026-11-17 | Error pages for an unavailable database, a server error and an expired form: a Feilside surface in the Information Architecture, three Message Catalogue rows, the not-found panel for every error page, an Error state, and a failure path in Flow 2. DESIGN.md: the not-found panel also serves the error pages. | PostgreSQL now runs locally as a server, so a stopped database is a new failure, and NFR-10 needs Norwegian error pages (architecture step; PRD §12, 2026-11-17). | `1441c40` |
| 2026-11-18 | Innstillinger: with the script, the setting that the chosen method uses is enabled before saving; without it, a field disabled for the saved method is changed in a second save. The unusual-weeks switch gets the small secondary button «Lagre» when scripts are off, and the script hides it. The Foundation line names both enhancements. DESIGN.md is unchanged, because the button is its small secondary button. | The user's decisions when approving Epic 3 in `epics.md` (D-4 and D-5), with AD-11 in the architecture spine amended the same day. | `9dee8b1` |
| 2026-11-18 | Produktside: the FR-14 overstock note stands in the decision panel, below the suggested order quantity (the Decision panel row and the state «Suggested order quantity 0»). | The spines did not say where the note stands on Produktside; the user approved the placement when approving Epic 6 in `epics.md` (D-6). | `9dee8b1` |
| 2026-11-18 | Fixes from the BMAD review: the Foundation line follows AD-11 (the chart is rendered on the server, with no chart library); the Trust legend for «Slik leser du tillitsmerket»; the field label «Justert bestillingsmengde» and «Behold … og gå videre» outside the review sequence; search always goes to Produktoversikt, ignores case and leaves the previous and next links alone; the reason when the window prevents a forecast, and which condition comes first; «–» in the confirmation when a forecast is removed or given; where the FR-9 note stands; short histories in the sales table and the chart; zero decimals in number fields; Flow 1 counts 4 products with warnings; three more mockup differences. DESIGN.md: a suggested order quantity of 0 is ink in the decision panel. | The review of `epics.md`, the architecture spine and this spine found contradictions and gaps; the user approved fixing all 29 findings (A1–A14 and E1–E15). | `9dee8b1` |
| 2026-11-18 | Responsive design for PC, iPad and phone (NFR-6): the intro and the Surface line; one column at 900 px and below, with the product area first and the list below it and no scroll frames of their own; no horizontal page scrolling from 320 px; touch targets of at least 44 × 44 px, 16 px text in form fields and the keyboard hint hidden on touch screens; the chart keeps its label sizes and scrolls inside its own frame, and calculation lines wrap between terms; the keyboard order and the skip link; the test sizes, with tests on a real device kept apart from the browser's responsive view. DESIGN.md follows in Layout & Spacing, the app header, the settings bar, the search field, the forecast chart, the calculation line, the button, the keyboard key and Do's and Don'ts. No function added. | The user's decision of 2026-11-18 and the updated NFR-6 in the PRD; the user has an iPhone 13 for tests on a real device. | `9dee8b1` |
| 2026-11-19 | Publishing removed from version 1: the Explanation section no longer names a published version, the iPhone 13 is tested on the real phone over the local network (Responsive & Platform), and Flow 2 uses only the local app. DESIGN.md needs no change. | The teacher's clarification on Canvas on 2026-11-19, as reported by the user, and the updated DR-10 in the PRD. | `ea06f01` (PR #5) |
| 2026-11-23 | The focus ring in the app header is white (`{colors.on-header}`), 3 px and 2 px outside the element, like the blue one elsewhere. DESIGN.md: the Elevation & Depth rule names the exception. | Story 1.8 puts «Produktoversikt» and «Logg ut» in the navy header, and the blue ring there gives about 2.4:1, under the 3:1 of WCAG 2.2 1.4.11 (BH-12 of the code review of Story 1.4). The user chose the white ring on 2026-11-23. | `a078c90` (Story 1.8) |
| 2026-11-27 | Confidence label reason: the phrase for old data («gamle data, [9] uker siden siste gyldige uke», and as a sentence after another warning), and how several recent-period warnings are joined before «de siste 12 ukene». | Story 2.5 writes the reasons, and the catalogue had a phrase for a level shift but none for old data. The user chose option A on 2026-11-27 and approved changing the catalogue. | `e74a814` (Story 2.5) |
| 2026-11-27 | The old-data phrase in the confidence reason is marked as a guard case that cannot occur under today's rules. Insufficient data, few weeks: the singular «Produktet har [1] gyldig uke.» and the zero case. | The BMAD Code Review of Story 2.5 found that the stand-alone old-data phrase is unreachable (BH-1) and that the singular is not in the catalogue (AA-5). The user decided on 2026-11-27 to mark the phrase as a guard case and to add the singular. | `e74a814` (Story 2.5) |
| 2026-11-28 | Message Catalogue: the status tag «uvanlig, holdt utenfor» beside «uvanlig»; the sentence below the sales table; the list of weeks left out with several kinds and the year rule; «[3] uker brukt i beregningen.»; the empty sales table; and «(lageret dekker behovet)» only when the stock is above 0. The Moving average row names the combined list. | Story 2.9 shows the worksheet and the catalogue fixed only the stockout example. The user approved the wording of the list and the count, the year rule and the six clarifications on 2026-11-28, and asked that an unusual week that is used be clearly told from one that is held out. | hash følger (Story 2.9) |
