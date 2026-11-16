---
name: 'Prognose'
status: final
created: '2026-11-15'
updated: '2026-11-16'
sources:
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/tilbakemelding-prd.md'
  - 'DESIGN.md'
---

# Prognose — Experience Spine

> Desktop web for one purchasing manager per company. [DESIGN.md](DESIGN.md) owns how Prognose looks; this spine owns how it works. The approved mockup is [mockups/konsept-d-kombinert.html](mockups/konsept-d-kombinert.html): Produktoversikt with «Denne uken», Produktside, and a product without a forecast. Innlogging and Samlet bestillingsoversikt have wireframes below. The spines win on any conflict with a mockup, and the known differences are listed under Open Questions and Assumptions.

## Foundation

- **Surface:** a desktop browser on an office PC or laptop (NFR-6, UJ-1). Mobile layouts, dark mode and print are not required and not designed.
- **Users:** one role per company (PRD §2.2). Prognose recommends and the user decides: nothing in the interface places an order (PRD §7).
- **Language:** Norwegian bokmål throughout, with the glossary labels from PRD §3 used verbatim and no synonyms (NFR-5).
- **Technology posture:** plain semantic HTML and CSS with the tokens in DESIGN.md, no UI library. Every function works through links and forms; scripts may only enhance (arrow keys in the list, keeping scroll positions) and draw the chart. Everything is served locally, with no web fonts and no CDN (NFR-1). The architecture fixes the framework, the chart library and the URLs; the mockup's addresses (`/produkter/`, `/produkter/10012/`) only illustrate.
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
| Vindu | number field, unit «uker» | 2–12, default 3 | with exponential smoothing: disabled, «Ikke i bruk med eksponentiell glatting.» |
| Glattingsfaktor | number field | 0,1–0,9, default 0,3 | with the moving average: disabled, «Ikke i bruk med glidende gjennomsnitt.» |
| Scenarioprosent | number field, unit «%» | 0–50, default 10 | |
| Sikkerhetsmargin | number field, unit «%» | 0–100, default 10 | |
| Uvanlige uker | radio buttons «Tas med» and «Holdes utenfor» | default tas med | also the switch below the chart |
| Sesongjustering | checkbox | off by default | only when FR-9 is built |

«Lagre» applies the change to every product at once and returns to the page you came from with the confirmation message. «Avbryt» returns without changes. Number fields accept a decimal comma or a decimal point (NFR-10).

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
| Insufficient data, few weeks | fewer than 3 valid weeks | List: «Ingen prognose: færre enn 3 gyldige uker». Warning: «Produktet har [2] gyldige uker. Prognose regner ut en prognose når produktet har minst 3 gyldige uker.» | PRD FR-24; UX, FR-8 |
| Insufficient data, window | moving average with fewer calculation weeks than the window | List: «Ingen prognose: færre uker enn vinduet». Warning: «Glidende gjennomsnitt over [12] uker trenger [12] uker brukt i beregningen. Produktet har [10].» | UX, FR-8 |
| Seasonal pattern (warning, Should) | R-17 pattern not used | «Produktet har tydelig sesongvariasjon som prognosen ikke tar hensyn til.» | PRD FR-36 |
| Flat weeks 2 and 3 (note) | no seasonal adjustment | «Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong.» | PRD FR-7 |
| Seasonal adjustment not possible (note, Should) | R-14 step 4 | «Sesongjustering kunne ikke brukes for dette produktet, så ukeprognosene er regnet uten.» | UX, FR-9 |
| Overstock (note, Should) | suggestion 0 and stock above 0 | «Lagerbeholdningen dekker forventet behov neste uke.» | PRD FR-14 |
| Stock not lasting (note, Could) | FR-33 | «Lageret og bestillingen dekker ikke uke 2 og 3.» | UX, FR-33 |
| Scenario text | next to the scenarios | «Scenarioene viser hva som skjer hvis salget blir [10] % høyere eller lavere. De er ikke sannsynligheter.» | PRD FR-10 |
| Order calculation line | always, with a forecast | «Prognose [14,3] + sikkerhetsmargin [10] % ([1,4]) − lager [5] = [10,77] → foreslått bestillingsmengde [11]». When the stock covers the need: «… → foreslått bestillingsmengde 0 (lageret dekker behovet)». Then «Tallene er avrundet for visning.» | PRD FR-12 |
| Safety-margin text | below the order calculation line | «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.» | PRD FR-12 |
| Forecast calculation | always, with a forecast | «Glidende gjennomsnitt, [3] uker: ([16] + [12] + [15]) / [3] = [14,3]» or «Eksponentiell glatting, faktor [0,3]: [0,3] × [15] + [0,7] × [13,3] = [13,8]» | PRD FR-35 |
| Confidence label reason | always | «[Høy, Middels or Lav]: [deciding condition].», then any other active warnings. Examples: «Høy: minst 104 uker salgshistorikk, minst 100 gyldige uker og ingen varsler.» «Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene.» «Middels: kortere salgshistorikk enn 104 uker.» «Middels: færre enn 100 gyldige uker.» «Lav: ingen prognose, færre enn 3 gyldige uker.» «Lav: færre enn 12 gyldige uker. 1 utsolgt uke de siste 12 ukene.» | PRD FR-19 format; UX texts, R-16 |
| No decision | product without a forecast | «Prognose foreslår ingen mengde for dette produktet. Du bestemmer bestillingen selv.» | UX, FR-8 |
| Settings area | wherever settings can change | «Endringen gjelder alle produkter i bedriften.» | PRD FR-21 |
| Settings confirmation | after a change | «Innstillingen er endret: [sikkerhetsmargin] er nå [50] %.», then one line per affected value: «[Foreslått bestillingsmengde]: [11] → [17]». No difference: «[Grunnprognose]: [14,3] → [14,3] (uendret)» | PRD FR-21 format; UX `[ASSUMPTION]` for «(uendret)» |
| Value out of range | FR-20 | «[Sikkerhetsmargin] må være mellom [0] og [100] %. Den forrige verdien er beholdt.» | UX, FR-20 |
| Not a number | empty or non-numeric input | «Skriv et tall, for eksempel 10 eller 0,3. Den forrige verdien er beholdt.» | UX, NFR-10 |
| Setting not in use | FR-20 | «Ikke i bruk med eksponentiell glatting.» / «Ikke i bruk med glidende gjennomsnitt.» | UX, FR-20 |
| Adjusted quantity invalid (Should) | FR-29 | «Skriv et helt tall fra 0 og oppover.» | UX, FR-29 |
| Markings (Should) | combined order overview, cards | «Foreslått» / «Justert av deg» | PRD FR-30 |
| No products | the company has no products | «Ingen data er lastet inn. Kjør [lastekommandoen] som står i README.» with the exact command filled in | UX, FR-24 |
| No search match | search finds nothing | «Ingen produkter passer søket.» and the link «Vis alle produkter» | UX |
| Not found | NFR-10, FR-2 | «Siden finnes ikke.» and the link «Til produktoversikten» | UX |
| AI label (Should) | FR-28 rephrased text | «KI-omformulert forklaring» | PRD FR-27 |

## Component Patterns

Behavioral rules. Visual specs are in DESIGN.md (Components), with the same names.

| Component | Where | Behavioral rules |
|---|---|---|
| App header | every page | Marks the current page. «Logg ut» ends the session and opens Innlogging (FR-1). |
| Settings bar | every page after login | Shows the settings in use: the method with its window or factor, the scenario percentage, the safety margin, unusual weeks, and seasonal adjustment once FR-9 is built. «Endre innstillinger» opens Innstillinger. |
| Product list | Produktoversikt, Produktside | All products in R-12 order: «Bestill snart» (weeks of cover, lowest first; ties by product number), «Uten prognose» (by product number `[ASSUMPTION]`), «Øvrige produkter» (by product number). Every card and row shows every FR-24 field. The list keeps its scroll position when a product is selected. |
| Group heading | product list | Names the group and sums it up: «4 produkter · 31 enheter foreslått», «1 produkt · du bestemmer selv», «25 · etter varenummer». An empty group is not shown. |
| Product card | «Bestill snart», «Uten prognose» | The whole card is one link. It shows the reason unless the label is «høy». Without a forecast, the reason replaces the week-1 forecast, and the quantity and weeks of cover show «–» (FR-24). With FR-29, an adjusted quantity is shown with «Justert av deg» in place of «Foreslått». |
| Product row | «Øvrige produkter» | The same fields as a card, on two lines; the whole row is one link. Shows the FR-14 note once it is built. |
| Search field | top of the list | Filters the list by product number or name; the groups keep their order. A plain form that works on Enter; filtering while typing is an enhancement. |
| Trust label | cards, rows, product header, trust panel | The word is always text and the shape is decoration. Its reason follows the Message Catalogue. |
| Panel | every surface | Holds one question or one task under one heading. A panel never contains another panel; inside it, structure comes from headings, tables and hairlines. |
| Decision panel | Produktside | Shows the suggested order quantity for week 1 (FR-11). With FR-29: «Behold [11] og gå videre» keeps the suggestion and opens the next product in the review sequence. «Juster mengden» opens a whole-number field with «Lagre» and «Tilbake til forslaget», and the suggestion stays visible next to the adjusted quantity. Without a forecast, «Sett mengden selv» opens the same field. Without FR-29 there are no buttons, and the previous and next links do the job. |
| Trust panel | Produktside | The label, its reason, and every active warning (R-15) whose FR is built, in R-15 order, and nothing that does not apply (FR-25). Together with the decision panel it is visible without scrolling at 1366 × 768 (FR-25). |
| Warning list | trust panel | One row per active warning, worded as in the Message Catalogue. Stockout and unusual weeks before the recent period are not warnings; the forecast calculation lists them (R-15). |
| Unusual-weeks switch | below the chart legend | Changes the company setting «Uvanlige uker» between «tas med» and «holdes utenfor» in one step (UJ-1 step 4). The page reloads with the confirmation message, and the change applies to every product (FR-21). It is a real checkbox with `role="switch"`, so Space toggles it. |
| Forecast chart | Produktside, right below the two panels | Shows the whole sales history (up to 104 weeks) and the three forecast weeks with the scenario band, so every stockout, unusual and level-shift week has its own marker (FR-15 to FR-17, FR-25). The last 12 weeks are marked «Siste 12 uker». The legend explains every marker type, whether or not this product has one. Text alternative: see Accessibility Floor. The mockup shows only the last 12 weeks. |
| Calculation worksheet | Produktside, below the chart | In order: «Salgshistorikk, siste 12 uker» (week, units sold, status); «Prognoseutregning» (FR-35, with the weeks used and every week left out, with its reason); «Ukeprognoser og scenarioer» (weeks 1–3, three scenarios, the FR-13 column once built, the FR-10 text and the FR-7 note); «Utregning av bestillingsmengde» (FR-12). |
| Calculation line | worksheet | The exact FR-12 or FR-35 format, the rounding note inside the box, and the FR-12 safety-margin text below. |
| Status tag | sales table | One tag per flagged week: «utsolgt», «uvanlig», «nytt nivå», or «brukt» for a week used in the forecast (the last N calculation weeks for the moving average; every calculation week for exponential smoothing). |
| Explanation panel | last on Produktside | The template explanation (FR-26), with only the numbers FR-27 allows (see Explanation). |
| Button | everywhere | The label says what happens. At most one primary button per panel. |
| Week path | «Denne uken» | Step 1 is current on Produktoversikt. Step 2 opens the first product in the review sequence. Step 3 opens Samlet bestillingsoversikt; without FR-30 the path has two steps. |
| Week figures | «Denne uken» | Products with order-soon status; units suggested in total (the sum of the suggested order quantities); products without a forecast; products with at least one active warning. Plain figures, not links. |
| Progress bar | Produktside header | The place in the review sequence: «produkt [2] av [4] som bør bestilles snart», then «produkt [1] av [1] uten prognose». Not shown for «Øvrige produkter». |
| Previous and next links | Produktside header | The previous and next product in R-12 order, across all groups. |
| Keyboard key | end of the list | Shows «↑ ↓ forrige og neste produkt · Enter åpner produktet». |
| Confirmation message | top of the product area | After a settings change: the new setting, and the old → new value of what it affects, as in the FR-21 table. Shown once, with `role="status"`. |
| Error message | above the field or form it concerns | `role="alert"`, and the previous value stays (FR-20, NFR-10). |
| Settings form | Innstillinger | See Information Architecture. |
| Login panel | Innlogging | Customer number and password with visible labels; Enter submits. After an error the customer number is kept and the password is cleared, and the message does not say which one was wrong (FR-1). |
| Combined order table | Samlet bestillingsoversikt (FR-30, Should) | Every product in R-12 order with its suggested or adjusted quantity and its marking; an adjusted row shows the suggestion in brackets; a total row; each product name links to its Produktside. |
| Not-found panel | unknown addresses, other companies' products | Shows no data from another company (FR-2) and links to Produktoversikt. |

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
| Suggested order quantity 0 | card, row, Produktside | «Foreslått 0» in ink; the order calculation line ends «(lageret dekker behovet)» when stock covers the need; the FR-14 note once built. |
| Week-1 forecast 0 | card, row | Weeks of cover «–», no order-soon status, no overstock note (R-12, E23). |
| Unusual weeks excluded | Produktside | The switch is off; the chart still marks them (FR-16); the warning says «holdt utenfor»; «Prognoseutregning» lists each excluded week and the number of weeks used (FR-16). |
| Level shift in the recent period | Produktside | The reason names it (FR-17); diamond markers and «nytt nivå» tags; the FR-17b warning once built. |
| Old data | Produktside | The old-data warning; the label is at most «middels» (R-16). |
| Seasonal adjustment on (Should) | Produktside | Week forecasts differ and the FR-7 note goes; the worksheet shows the indices and adjusted values (FR-35). When it cannot be used: the FR-9 note. |
| Seasonal pattern not used (Should) | Produktside | The FR-36 warning. |
| Settings changed | page you came from | Confirmation message with old → new; «(uendret)» when nothing changed `[ASSUMPTION]`. |
| Invalid setting | Innstillinger | Error message at the field; the previous value stays. |
| Quantity adjusted (Should) | card, decision panel, combined table | «Justert av deg» with the adjusted quantity; the suggestion stays visible; «Tilbake til forslaget» resets it (FR-29). The adjustment lasts for the session (FR-31 is Could). |
| Last product reviewed | Produktside | The primary button becomes «Gå til samlet bestillingsoversikt» (FR-30), or «Tilbake til produktoversikten» without it. |
| Language model on (Should) | explanation panel | «KI-omformulert forklaring» above the text; on any FR-28 failure the template text, without an error message. |
| Not found | any address | Not-found panel (FR-2, NFR-10). |
| Reload, Back, double submit | any page | The same result and no error (NFR-10). |
| Focus | every control | A 3 px outline in `{colors.blue}`, 2 px outside the element (DESIGN.md, Elevation & Depth). |

## Interaction Primitives

- **Links and forms.** Every action is a link or a form submission, so everything works without scripts (Foundation).
- **Keyboard.** Tab follows the reading order: header, settings bar, list, product. In the list, ↑ and ↓ move between products and Enter opens one (an enhancement; Tab and Enter always work). Space toggles the switch. There are no shortcuts without a visible hint.
- **Mouse.** Click anywhere on a card or row. Nothing depends on hover, and there is no drag.
- **Review sequence.** «Bestill snart», then «Uten prognose» (R-12 groups 1 and 2). «Behold … og gå videre» moves through it; previous and next cover every product.
- **Settings.** The switch below the chart changes unusual weeks in one step; Innstillinger changes the rest. Every change applies to every product at once and ends with the confirmation message (FR-21).
- **Banned:** modals, popovers, tooltips as the only home of information, auto-refresh, animation, infinite scroll, drag, hover-only controls, and color-only signals.

## Calculation Display Rules

| What | Rule |
|---|---|
| Rounding | As R-9 (display rounding). |
| Number format | Decimal comma; «%» after a space («10 %»); the minus sign «−»; no thousands grouping. |
| Rounding note | «Tallene er avrundet for visning.» inside the order calculation line (FR-12), and also below the exponential-smoothing line and the seasonal table, where shown inputs can differ from a hand check `[ASSUMPTION]`. |
| Moving average | The FR-35 line, then «Uker brukt: uke 43, 44 og 45.» and «Holdt utenfor: uke 38 og 39 (utsolgt).». With unusual weeks excluded, each excluded week is listed and «[3] uker brukt i beregningen» is stated (FR-16). |
| Exponential smoothing | The FR-35 line for the last update, and a table of every calculation week with its sales and level in its own scroll frame (FR-35). |
| Seasonal adjustment (Should) | The indices (four decimals) and adjusted values (one decimal) for the weeks used and for weeks 1–3, and the week forecasts (FR-35, E14) `[ASSUMPTION]` for the decimals. |
| Week labels | Horizon columns read «Uke 1 · uke 46». Chart axes use week numbers; the first week of a new year carries its year («1/2027»), and lists that reach before the recent period show the year («uke 10/2025») `[ASSUMPTION]`. |
| Weeks left out | Every stockout week and excluded unusual week in the history, with its reason, in «Prognoseutregning»; the recent ones are also warnings (R-15). |
| Missing values | «–» for the suggested order quantity and weeks of cover without a forecast (FR-24), and for weeks of cover when the week-1 forecast is 0 (E23). |
| Order quantity per scenario (Should) | A «Bestillingsmengde» column in the scenario table, calculated from week 1 (FR-13, E22). |

## Explanation

- **Place:** its own panel titled «Forklaring», last on Produktside, below every calculated number (FR-27).
- **Content, in order (FR-26):** the method and settings; the number of calculation weeks and the week forecasts; the weeks left out and why; every active warning and note; the order calculation; the weeks of cover; the confidence label and its reason; the scenarios.
- **Numbers:** only the ones FR-27 allows. Templates therefore leave out sales figures, years, and the week numbers of calculation weeks, included unusual weeks and level-shift weeks. Example for Strøsand 25 kg, as in the mockup: «Prognosen bruker glidende gjennomsnitt over de 3 siste ukene brukt i beregningen. Det gir 14,3 per uke for uke 46, 47 og 48. Uke 38 og 39 er holdt utenfor fordi varen var utsolgt. Det er 1 uvanlig uke de siste 12 ukene, og uvanlige uker tas med i beregningen. Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong. Med 10 % sikkerhetsmargin (1,4) og 5 på lager blir utregningen 10,77, og Prognose foreslår å bestille 11. Lageret dekker 0,3 uker. Tillitsmerket er middels fordi det er 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene. Scenarioene viser 15,8 hvis salget blir 10 % høyere, og 12,9 hvis det blir 10 % lavere.»
- **Language model (FR-28, Should):** rephrased text carries «KI-omformulert forklaring». On any failure the template text is shown without an error. The published version always shows the template text (DR-10).

## Accessibility Floor

Behavioral; visual contrast is in DESIGN.md (Colors).

- WCAG 2.2 AA on every surface, and pages declare `lang="nb"` (NFR-11).
- Every function works with the keyboard alone, with the visible focus ring (NFR-11). On Produktside the first focusable element is a skip link «Gå til produktet». The product list and the product area are labeled scroll regions («Produkter», «Valgt produkt») that keyboard users can scroll.
- Every field has a visible label, the search field included (NFR-11).
- Headings: one `h1` per page (the product name, «Denne uken», the page title); panels use `h2`, worksheet subsections and list groups use `h3`.
- The selected product has `aria-current="page"`. Trust labels are text; their shapes are hidden from screen readers.
- **Chart text alternative (NFR-11):** the chart has a title and a short summary (weeks shown, stockout, unusual and level-shift weeks, forecast and scenario range). Its plotted values are in the worksheet's tables, plus a disclosure «Tabell med alle ukene i grafen» with every plotted week. Markers differ by shape, and the legend names each one (NFR-7).
- Confirmations use `role="status"`, errors `role="alert"`, and field errors are linked to their field with `aria-describedby`.
- No timing, no motion, and no content that appears only on hover.
- Down to 800 px wide, no text overlaps or is cut off, and every control is reachable (NFR-6).

## Responsive & Platform

| Width | Behavior |
|---|---|
| ≥ 1181 px | The list (`{spacing.list-width}`) beside the product; the decision panel and the trust panel side by side, with the chart below them. |
| 901–1180 px | The list narrows to `{spacing.list-width-narrow}`; the two panels stack, decision first. |
| ≤ 900 px | One column: the list on top (at most 420 px high, scrolling on its own), the product below. Tables scroll inside their own frame. |
| 1024 px and wider | No horizontal page scrolling (NFR-6). |
| 1366 × 768 | The suggested order quantity, the confidence label and the active warnings are visible without scrolling (FR-25); the chart starts right below them. |

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
2. Produktoversikt opens with «Denne uken»: 4 products to order soon, 31 units suggested, 1 product without a forecast, 3 with warnings. The list shows «Bestill snart» first, lowest weeks of cover first (UJ-1 step 1).
3. She selects «Start med Isskrape», keeps the suggested 7 and moves on to Strøsand 25 kg.
4. Without scrolling she sees «11», «Middels» and the two warnings; the chart right below shows the gap in weeks 38–39 and the peak in week 42 (UJ-1 steps 2–3).
5. She scrolls to «Slik er tallene regnet ut»: (16 + 12 + 15) / 3 = 14,3, and the order calculation line ends at 11. She reads «Forklaring» (UJ-1 step 3).
6. She switches unusual weeks off below the chart. The confirmation shows «Grunnprognose: 14,3 → 14,3 (uendret)», because week 42 is outside the 3-week window, and says the change applies to all products. She switches back (UJ-1 step 4).
7. She chooses «Behold 11 og gå videre», or «Juster mengden» and 13 (FR-29), and continues through the list (UJ-1 step 5).
8. After the last product she opens Samlet bestillingsoversikt, where every product is marked «Foreslått» or «Justert av deg» (UJ-1 step 6, FR-30).
9. **Climax:** for every product she has one number for next week, how it was calculated, and whether to trust it, on one list she takes to the meeting.

Failure paths: a wrong login shows «Feil kundenummer eller passord.». A product without a forecast shows «Du bestemmer bestillingen selv», and with FR-29 she sets the quantity herself. When the stock covers the need, the line ends «(lageret dekker behovet)». In a Must-only build, steps 7–8 use the previous and next links, and the meeting list stays outside Prognose.

### Flow 2 — The examiner checks a forecast by hand

Ingrid, the course examiner, on her own laptop, with the README and the reference spreadsheet open.

1. Ingrid follows «Prøv selv» in the README (DR-1) and opens the local app or the published address (DR-10). She logs in as Testbedrift A.
2. In Produktoversikt she picks a rule test product named in the README table, for example Strøsand 25 kg (E1, E4).
3. On Produktside she compares «Slik er tallene regnet ut» with the spreadsheet: the weekly sales, «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3» and the order calculation line «… = 10,77 → foreslått bestillingsmengde 11».
4. She opens «Endre innstillinger», sets the safety margin to 50 % and saves. Back on the product, the confirmation shows «Foreslått bestillingsmengde: 11 → 17» (SM-3).
5. **Climax:** the screen matches her hand calculation and the spreadsheet, and the change shows its previous and new value.
6. She sets the safety margin back to 10 %.

Failure paths: a value outside the range, for example 150, shows «Sikkerhetsmargin må være mellom 0 og 100 %. Den forrige verdien er beholdt.». If publishing hit the cut line (PRD §8.1), the README says so and Ingrid uses the local app.

### Flow 3 — SM-10. Someone outside the group explains «lav»

Jonas, a fellow student outside the group, is shown Prognose for the first time.

1. Jonas sees Produktside for Snøskuffe aluminium: «Lav» and «Ingen foreslått bestillingsmengde».
2. The trust panel says «Lav: ingen prognose, færre enn 3 gyldige uker.» and «Produktet har 2 gyldige uker. Prognose regner ut en prognose når produktet har minst 3 gyldige uker.».
3. **Climax:** asked why the label is «lav», Jonas answers without reading aloud: "it has too few weeks of sales to make a forecast". He names the deciding condition, which is what SM-10 checks (R-16).
4. The check is recorded in the QA log (DR-9).

Failure path: if Jonas cannot explain the label, the reason texts in the Message Catalogue are revised and the check is repeated, while there is still time to fix it (SM-10).

## Open Questions and Assumptions

- `[ASSUMPTION]` «Uten prognose» is sorted by product number; R-12 gives no order inside that group.
- `[ASSUMPTION]` A settings change that does not alter a value is confirmed with «(uendret)».
- `[ASSUMPTION]` In Samlet bestillingsoversikt, a product without a forecast and without an adjusted quantity shows «–» and «Uten prognose», because FR-30 names only «Foreslått» and «Justert av deg». The table uses the R-12 order of Produktoversikt.
- `[ASSUMPTION]` The rounding note also appears below the exponential-smoothing line and the seasonal table; seasonal indices have four decimals and adjusted values one.
- `[ASSUMPTION]` Weeks show their year at New Year and in lists that reach before the recent period.
- **Open for the PRD:** FR-27 allows week numbers but not years, so the explanation cannot say which year a left-out week from an earlier year belongs to.
- **Open for the dataset (FR-3, DR-3):** in the example numbers, week 42 lies outside Strøsand's 3-week window, so UJ-1 step 4 changes nothing for that product. A demo product with an unusual week inside the window, as in E8, would show the effect.
- **Mockup differences (the spine wins):** the mockup's chart shows only the last 12 weeks; the chart shows the whole sales history. The legend icons in the mockup may render larger than 14 and 24 px, because the chart's `width: 100%` rule also matches them.

## Change Log

The spine pair (DESIGN.md and EXPERIENCE.md) was set to `final` on 2026-11-16. Every later change to either file is recorded here with the date, the reason and the commit, as PRD §12 and DR-5 require.

| Date | Change | Reason | Commit |
|---|---|---|---|
