---
name: Prognose
status: final
sources:
  - '{planning_artifacts}/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '{planning_artifacts}/prds/prd-G40-lyamouri-2026-11-02/addendum.md'
created: '2026-11-06'
updated: '2026-11-07'
---

# Prognose — Experience Spine

> Desktop web first, readable on phones. The pages are server-rendered, with no client-side code except the chart. Paired with [DESIGN.md](DESIGN.md), which owns how Prognose looks; this spine owns how it works. Approved mockups: the [landing page with login](mockups/key-landing.html) and [Produktoversikt](mockups/key-produktoversikt.html). Alternate states are in an [internal design note](mockups/designnotat-tilstander.html). The spines win on any conflict with a mockup.

## Foundation

- **Form factor:** one web application in a desktop browser on a laptop or office PC, on macOS or Windows (NFR-6). Phones and narrow tablets get a readable one-column layout as a courtesy; the PRD does not require a mobile design.
- **UI system:** none. Pages are server-rendered HTML with one stylesheet of DESIGN.md tokens and a vendored Chart.js for the charts. The architecture step decides the stack (the research recommends Django + SQLite). Every interaction works through links and forms, and only the chart drawing needs client-side code.
- **Language:** Norwegian bokmål. The PRD glossary labels (PRD §3) are binding, with no synonyms, and the PRD's fixed strings appear verbatim.
- **Data:** synthetic and read-only. Only the company-wide settings and adjusted order quantities change.
- **Principle:** Prognose recommends; the user decides. The UI never presents a suggestion as an order.

## Information Architecture

| Surface | Reached from | Purpose | Visual reference |
|---|---|---|---|
| Landing page with login | The app root, and every page when logged out (FR-1) | Explain what Prognose does, show the calculation and trust signals, log in | [mockup](mockups/key-landing.html) |
| Produktoversikt (dashboard) | After login; «Produktoversikt» in the rail | Every product in R-12 order: what to order for next week, and whether to trust it (FR-24) | [mockup](mockups/key-produktoversikt.html) |
| Produktside | A product name in Produktoversikt | Everything needed to decide one product: chart, calculations, warnings, settings, explanation (FR-25, FR-35, FR-21, FR-26, FR-27) | wireframe below (spine-only) |
| Samlet bestillingsoversikt | «Samlet bestillingsoversikt» in the rail and the button in Produktoversikt | Every product's suggested or adjusted quantity for the meeting (FR-30, Should) | wireframe below (spine-only) |
| Ikke funnet | Any unknown address, or another company's product (FR-2, NFR-10) | A Norwegian «ikke funnet» message with a link to Produktoversikt | spine-only |

- **Navigation:** the app has a left rail with Produktoversikt, Samlet bestillingsoversikt, «Innstillinger i bruk», a mini legend, the company name and «Logg ut». At 960 px and below the rail becomes a top bar.
- **Breadcrumb:** Produktside shows «Produktoversikt / 10234 Treskrue 4 × 40 mm, 200 stk».
- **Decision strip:** the top band of Produktside. It holds the suggested order quantity, the confidence label and its reason, the warnings and the calculation line, and it stays above the fold at 1366 × 768 (FR-25).
- **Readout (landing page):** the block under the landing chart. It holds the confidence label and its reason, the safety-margin try-out, the calculation line and the settings confirmation.
- **Settings:** there is no settings page. Settings are changed in the settings panel on Produktside (FR-21), and the rail only shows what is in use.
- **Dialogs:** none. Every task happens inline.

### Wireframe: Produktside (1366 × 768, spine-only)

```
┌─ App rail ─────┬─ Produktoversikt / 10234 Treskrue 4 × 40 mm, 200 stk ───────────────────────────┐
│ Prognose       │ Treskrue 4 × 40 mm, 200 stk        Varenummer 10234 · Siste registrerte uke: 45 │
│ Produktoversikt│ ┌─ Decision strip (always above the fold) ───────────────────────────────────┐ │
│ Samlet         │ │ ◎ Foreslått bestillingsmengde for uke 46: 11  ◐ Tillitsmerke: middels      │ │
│ bestillings-   │ │   Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene.             │ │
│ oversikt       │ │ △ Varsler: 2 utsolgte uker (uke 36, 37) · 1 uvanlig uke (uke 39: 31 stk)   │ │
│                │ │ Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → … 11       │ │
│ Innstillinger  │ └────────────────────────────────────────────────────────────────────────────┘ │
│ i bruk         │ ┌─ Course chart: history + De neste tre ukene ──────────┐ ┌─ Innstillinger ──┐ │
│ Tegnforklaring │ │ × △ ◆ ○ ◎ markers, «nå» line, scenario band            │ │ Prognosemetode   │ │
│                │ │ Tegnforklaring · Vis tallene i tabell                  │ │ Vindu / Faktor   │ │
│ Testbedrift A  │ └────────────────────────────────────────────────────────┘ │ Scenarioprosent  │ │
│ Logg ut        │ ┌─ Prognoseutregning ──────┐ ┌─ Scenarier ─────────────┐   │ Sikkerhetsmargin │ │
│                │ │ calculation line, weeks  │ │ strip + FR-10 sentence   │   │ Uvanlige uker    │ │
│                │ │ used, weeks left out     │ │ Uke 1–3 + FR-7 note      │   │ «Endringen …»    │ │
│                │ └──────────────────────────┘ └─────────────────────────┘   └──────────────────┘ │
│                │ Forklaring (template text below the numbers)                                     │
│                │ Juster bestillingsmengde (Should): field · «Tilbakestill til forslaget»          │
└────────────────┴──────────────────────────────────────────────────────────────────────────────────┘
```

### Wireframe: Samlet bestillingsoversikt (spine-only)

```
┌─ App rail ─┬─ Samlet bestillingsoversikt · Bestilling for uke 46 · 30 produkter ─────────────┐
│            │ Status sentence: 28 «Foreslått» · 2 «Justert av deg»                            │
│            │ Varenummer │ Produkt │ Foreslått │ Bestilling │ Merket          │                 │
│            │ 10871      │ Malertape 25 mm │ 11 │ 11 │ Foreslått                               │
│            │ 10234      │ Treskrue 4 × 40 mm │ 11 │ 15 (foreslått 11) │ Justert av deg         │
│            │ 11502      │ Arbeidshansker … │ – │ 10 (ingen prognose) │ Justert av deg         │
│            │ … rows in R-12 order; the product name opens Produktside                        │
│            │ «Prognose legger ikke inn bestillinger.» · Eksporter CSV (Could, FR-32)         │
└────────────┴─────────────────────────────────────────────────────────────────────────────────┘
```

## Voice and Tone

Microcopy rules. Brand posture lives in DESIGN.md.

| Do | Don't |
|---|---|
| «Foreslått bestillingsmengde: 11» | "Kjøp 11 nå!" or any order-placing verb |
| Show the working: «Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → foreslått bestillingsmengde 11» | A number without its calculation |
| State limits plainly: «Sikkerhetsmarginen er en enkel tommelfingerregel. …» | Hedge, hide or soften a warning (SM-C3) |
| One general login error: «Feil kundenummer eller passord.» | Say which of the two fields was wrong |
| Use the binding labels («Uker dekning», «Tillitsmerke», «Bestill snart») | Synonyms such as "dekningsgrad" or "risiko" |
| Write «uke 46» in running text, and «Uke 1 · uke 46» for the forecast horizon | Mix up horizon weeks and calendar weeks |
| «Ingen tall kommer fra KI.» | "KI-drevet", "smart" or marketing words |
| Short, complete sentences in the active voice | Exclamation marks, emoji, internal jargon |

## Component Patterns

Behavioral rules. The visual specs live in DESIGN.md Components, under the same names.

| Component | Use | Behavioral rules |
|---|---|---|
| Wordmark | Landing title bar, app rail, footer | Links to the top of the landing page, or to Produktoversikt when logged in. |
| Map frame | Landing first viewport | At 900 px and below it becomes one column in this reading order: title bar, headline, login, chart, readout, legend, sheet foot. |
| Button | Everywhere | Primary is used only for the main action of a surface (log in, save an adjustment). Secondary is for navigation-like actions. Ghost is for «Logg ut». Each button names its action. |
| Login panel | Landing | A POST form with Kundenummer and Passord. A wrong pair reloads the page with one general error (FR-1) and keeps the customer number. Success opens Produktoversikt. The «Logg inn» button in the title bar and the skip link jump to the panel and outline it. |
| Text field | Login, settings, adjusted quantity | Always has a visible label. Numeric fields accept a decimal comma or a point (NFR-10). Invalid input shows a Norwegian message under the field and keeps the previous value. |
| Course chart | Landing, Produktside | Shows the sales history, the week forecasts and the scenario band (FR-25). Calculation weeks are circled, and weeks left out carry their marker (FR-15 to FR-17). It redraws after a settings change. The chart is never the only carrier of a number: every value is also in the data table. |
| Tegnforklaring | Beside every chart | Lists every mark that can appear, including marks absent for this product, so the legend stays stable. |
| Data table toggle | Under every chart | Closed by default and keyboard operable. It is the chart's text alternative, one row per week (NFR-11). |
| Calculation line | Produktside, landing readout | Formats follow the Calculation display rules below. It updates after every settings change. |
| Confidence label | Produktoversikt, Produktside | Always shows the reason. The reason names the deciding condition and lists the active warnings (FR-19). It changes only when the data or the settings change. |
| Varsel and Merknad | Produktside decision strip and lists | A Varsel affects the confidence label; a Merknad does not (R-15). Both name weeks by number. |
| Segmented control | Settings, Produktoversikt filter | Radio buttons behind joined labels, keyboard operable. In the app a settings choice is a POST, and a filter choice is a GET parameter (`?vis=bestill`). |
| Settings confirmation | Produktside settings panel | After each change, one line names the setting, the old and new values, and the affected value, for example «Grunnprognose: 14,3 → 13,8» (FR-21). It stays until the next change. «Endringen gjelder alle produkter i bedriften.» is always visible in the panel. |
| Scenario strip | Produktside, landing | Shows week 1's three scenarios with the FR-10 sentence. The order quantity per scenario (FR-13) is added when that Should item is built. |
| Calculation steps | Landing | A static explanation in three steps (forecast, scenarios, order), with no interaction. |
| App rail | Every app page | The current page is marked with `aria-current`. «Innstillinger i bruk» is read-only and states where settings are changed. «Logg ut» ends the session (FR-1). |
| Status sentence | Produktoversikt, Samlet bestillingsoversikt | Plain counts that match the groups or tags below, never KPI tiles. |
| Product table | Produktoversikt | Rows in the R-12 groups: Bestill snart (by uker dekning, then varenummer), Uten prognose, then the rest by varenummer. A product without a forecast shows its reason across the three number columns (FR-24). The product name opens Produktside. At 640 px and below each row is a card. |
| Order table | Samlet bestillingsoversikt, landing example | Each product shows «Foreslått» or «Justert av deg» (FR-30). An adjusted row also shows the suggestion. Adjustments last for the session unless FR-31 is built, and the page says so. |
| Forklaring | Produktside | Template text below the numbers, under the heading «Forklaring». It contains only numbers that are also shown above (FR-26, FR-27). When FR-28 is on, the rephrased text is labeled «KI-omformulert forklaring», and any failure falls back silently to the template. |
| Empty state | Produktoversikt, filters | States why the surface is empty and offers one way forward: the README load command (FR-24), or «Vis alle produkter». |

## Calculation display rules

These are product-specific rules. The PRD rules decide every value (R-1 to R-17).

- **Order calculation line (FR-12):** «Prognose {F1} + sikkerhetsmargin {m} % ({margin amount}) − lager {S} = {raw, 2 decimals} → foreslått bestillingsmengde {Q}». When the raw value is negative, add «(lageret dekker behovet)». Below it, always show «Tallene er avrundet for visning.» and the margin caveat.
- **Forecast calculation (FR-35):**
  - Moving average: «Glidende gjennomsnitt, {N} uker: (a + b + c) / N = {F}», then the calculation weeks by number.
  - Exponential smoothing: the last update line plus a table of every calculation week with its sales and level.
  - In both cases, list the weeks left out with their reason (utsolgt uke, or an excluded uvanlig uke).
- **Horizon (FR-7):** «De neste tre ukene» shows «Uke 1 · uke 46» to «Uke 3 · uke 48». The fixed note appears whenever the three week forecasts are equal.
- **No forecast (FR-8):** no number, no order quantity, a warning that names the reason (and the window when that applies), and «Du bestemmer bestillingen selv.»
- **Rounding (R-9):** forecasts, scenarios, uker dekning and the margin amount get one decimal. The raw order result gets two decimals. Quantities and percentages are whole numbers. Use a decimal comma.
- **Uker dekning (R-12):** when the week-1 forecast is 0, show «–».

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Logged out | Any app page | Redirect to the landing page (FR-1). |
| Login error | Landing | The panel reloads with «Feil kundenummer eller passord.» (`role="alert"`), the customer number kept and the password cleared. See [the internal note](mockups/designnotat-tilstander.html). |
| No data loaded | Produktoversikt, Samlet bestillingsoversikt | Empty state with the README load command (FR-24). |
| Filter without hits | Produktoversikt | Empty state with «Vis alle produkter». |
| Product without forecast | Produktoversikt, Produktside | The reason replaces the numbers. Tillitsmerke lav. No order quantity (FR-8). |
| Stock covers next week | Produktoversikt, Produktside | Quantity 0 and «Lagerbeholdningen dekker forventet behov neste uke.» (FR-14, Should). In Produktoversikt it is shown once for the whole group. |
| Unusual weeks excluded | Produktside | The excluded weeks are listed by number, with the count of calculation weeks used (FR-16). The chart keeps their markers. |
| Level shift | Produktside | Diamond markers. The text «Etterspørselen ser ut til å ha endret nivå.» is added when that Should item is built (FR-17). |
| Old data | Produktside | A warning with the number of weeks since the latest valid week (FR-18). |
| Setting not in use | Settings panel | The window under exponential smoothing, or the factor under moving average, is shown struck through and labeled as not in use (FR-20). |
| Invalid setting | Settings panel | A Norwegian message under the field. The previous value stays (FR-20, NFR-10). |
| Setting changed | Produktside | The settings confirmation line. All values on the page update (FR-21). |
| Seasonal adjustment not possible | Produktside | A Merknad that says why. The week forecasts are shown without adjustment (FR-9, Should). |
| Adjusted quantity | Produktside, Samlet bestillingsoversikt | «Justert av deg», with the suggestion beside it and «Tilbakestill til forslaget» (FR-29, Should). |
| Invalid adjusted quantity | Produktside | «Skriv et helt tall som er 0 eller mer.» The previous value stays (FR-29). |
| Not found | Any | A Norwegian «ikke funnet» page with a link to Produktoversikt (NFR-10). Another company's product gives the same page (FR-2). |
| Resubmit or back | Any form | Post/Redirect/Get: reloading or going back repeats nothing (NFR-10). |
| Fonts unavailable | Any | The system fallback stack. The layout holds. |

## Interaction Primitives

- **Input:** mouse and keyboard, with standard links, buttons, radio groups, inputs and `<details>`. Every function is reachable by Tab in reading order. A skip link leads to the login on the landing page and to the content in the app.
- **Server round trips:** every settings change and adjustment is a POST followed by a redirect to the same page with the confirmation (Post/Redirect/Get). Filters are GET links. The pages work without client-side code; Chart.js only draws the charts.
- **Touch:** touch targets are at least 44 px on coarse pointers. Nothing depends on hover.
- **Banned:**
  - drag and drop (the data is read-only, and nothing may suggest that dragging changes an order)
  - dialogs for settings
  - auto-refresh and infinite scroll
  - confirmations that disappear on a timer
  - any action that places an order

## Accessibility Floor

Behavioral rules. Visual contrast lives in DESIGN.md.

- WCAG 2.2 AA on every surface (NFR-11).
- **Page basics:** pages declare `lang="nb"`, and every field has a visible label.
- **Focus:** a visible 3 px `{colors.magenta-ink}` focus ring on every interactive element. The tab order follows the reading order.
- **Charts:** each chart has a short text summary and a data table. In the mockups the summary is the SVG `<title>` and `<desc>`. Chart.js draws on a canvas, so in the app the summary is a caption or an `aria-label` on the canvas, and the data table carries the values. The markers differ by shape and are explained in Tegnforklaring (NFR-7).
- **Status beyond color:** status never relies on color. Confidence labels pair a shape with a word, and Bestill snart pairs the finish symbol with visually hidden text.
- **Announcements:** the login error is announced as an alert (`role="alert"`) and the settings confirmation as a status (`role="status"`).
- **Motion:** respect `prefers-reduced-motion`. When reduced motion is requested, the one motion (the course drawing in) is skipped.
- **Small screens:** at 640 px and below the product cards keep the reading order. The app should keep table semantics on that layout, for example with ARIA roles.

## Responsive & Platform

**Landing page**

| Width | Behavior |
|---|---|
| 901 px and above | The map sheet with its side column (300 to 372 px). At 1366 × 768 the login, the chart and the calculation line are in the first viewport. |
| 1100 px and below | The calculation steps, the trust section, «Du bestemmer» and «Prøv selv» stack into one column. |
| 900 px and below | One column, in the Map frame reading order (see Component Patterns). |
| 760 px and below | The section links are hidden; the «Logg inn» button stays. |
| 700 px and below | Both charts switch to their mobile variants. |
| 640 px and below | The readout becomes one column, with tighter padding. |

On short desktop screens (760 px high and below) the headline and chart shrink, so the first viewport keeps the login, the chart and the calculation line.

**App**

| Width | Behavior |
|---|---|
| 1181 px and above | Rail 248 px with the mini legend. On Produktside the decision strip is above the fold at 1366 × 768. |
| 961–1180 px | Rail 208 px; mini legend hidden. No horizontal page scroll from 1024 px (NFR-6). Below 1024 px the product table scrolls inside its frame. |
| 960 px and below | The rail becomes a top bar. «Innstillinger i bruk» and the mini legend are hidden, and the table scrolls inside its frame. |
| 700 px and below | The Produktside chart switches to its mobile variant. |
| 640 px and below | Product rows become cards, body text is 16 px, and the account line shows only «Logg ut». |
| 560 px and below | The filter becomes a 2 × 2 grid. |

## Inspiration & Anti-patterns

- **Lifted from the orienteering map (ISOM, the International Specification for Orienteering Maps):** the legend as the contract for every mark, the magenta course overprint, map-frame composition, and states drawn by line style and hatch so they survive grayscale.
- **Lifted from the declined catalog challengers (alternative design concepts from Impeccable's catalog, named in parentheses):** every week is its own step and «nå» is always marked (drum machine); one control visibly reshapes the whole (drawcord cape); signals are drawn where they happened (chromatophore skin); everything hangs on the «nå» line (city-pop sleeve).
- **Rejected:**
  - The SaaS hero with a floating dashboard, three icon cards, logos and testimonials. There is nothing true to fill them with.
  - KPI-card dashboards. They hide the calculation.
  - "AI-powered" framing. AI produces no numbers (AG-1).
  - A board with draggable cards. The data is read-only.
  - A separate settings page. Settings belong next to their effect (FR-21).

## Key Flows

### Flow 1 — UJ-1. Mounia plans next week's purchases before the Monday meeting.

Mounia, purchasing manager at a small hardware store with about 30 products, has 20 minutes at the office PC before the purchasing meeting.

1. Mounia opens Prognose. The landing page shows the map sheet, and Mounia logs in with the customer number and password.
2. Produktoversikt opens. The status sentence says 4 products should be ordered for uke 46. Bestill snart is first, sorted by uker dekning.
3. Mounia opens Treskrue 4 × 40 mm. The decision strip shows the number to order, the confidence label with its reason, the warnings and the calculation line without scrolling.
4. Mounia reads the warnings (2 utsolgte uker, 1 uvanlig uke), checks the course chart and the data table, and reads the Forklaring.
5. Mounia switches «Uvanlige uker» to «holdt utenfor». The settings confirmation names the change, the page says it applies to all products, and the values update. Mounia switches back.
6. Mounia keeps the suggestion, or adjusts it (Should) and sees «Justert av deg» with the suggestion beside it. Mounia returns to Produktoversikt and moves on.
7. **Climax:** in Samlet bestillingsoversikt (Should), every product shows one number for uke 46, marked «Foreslått» or «Justert av deg». Behind each one, Mounia has seen how it was calculated and whether it can be trusted. Mounia takes the list to the meeting; the orders are placed outside Prognose.

Failure paths:
- **Wrong login:** one general error, and Mounia tries again.
- **Product without a forecast:** the reason replaces the number, and Mounia decides by hand.
- **Stock covers the need:** quantity 0, with «(lageret dekker behovet)».
- **Invalid setting:** a message, and the previous value stays.

### Flow 2 — The examiner follows «Prøv selv» (DR-1, SM-2)

The IBE160 examiner has installed Prognose from the README and has the reference spreadsheet open beside the browser.

1. On the landing page the examiner reads «Prøv selv» and logs in as Testbedrift A with the login from the README.
2. The examiner opens Treskrue 4 × 40 mm and compares the calculation line and the forecast calculation with reference examples E1 and E4.
3. The examiner opens «Vis tallene i tabell» and checks the weeks used and the weeks left out against the spreadsheet.
4. The examiner changes the safety margin and checks the new quantity against the order rule (R-8).
5. **Climax:** every number on screen matches the answer key, and the examiner can trace each one through the calculation line, the forecast calculation and the explanation.

Failure path: the data is not loaded, so Produktoversikt shows the empty state with the README load command.

## Open items (non-blocking)

- Dark mode is not designed (DESIGN.md Colors).
- The README load command in the empty state is set in the architecture step.
- Produktside and Samlet bestillingsoversikt have wireframes only. HTML mockups can be added in an update if wanted.
- The Impeccable finish review and design documentation run on the real build, as the FINISH line of the direction contract requires (surface briefs in `.impeccable/surfaces/`).
- The architecture step decides, together with the repository layout, where `PRODUCT.md` and DESIGN.md live for Impeccable during the build (DR-2). It also confirms the canvas summary for the Chart.js charts.
- In the approved Produktoversikt mockup, the table between 961 and 1023 px wide is clipped rather than scrollable. This spine wins: the build lets the table scroll inside its frame there.
