---
name: Prognose
description: O-kartet, the orienteering-map design language for Prognose, a local web app for weekly sales forecasts, stock and purchase planning.
status: final
sources:
  - '{planning_artifacts}/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '{planning_artifacts}/prds/prd-G40-lyamouri-2026-11-02/addendum.md'
created: '2026-11-06'
updated: '2026-11-07'
colors:
  # Light only. Dark mode is not designed (see Colors).
  paper: '#F6F8F5'
  white: '#FFFFFF'
  ink: '#141614'
  ink-2: '#4A504C'
  line: '#6B716D'
  rule: '#D5DBD4'
  brown: '#B4541A'
  brown-grid: '#E5CBB1'
  yellow: '#FFE09A'
  green-screen: '#C9E8B5'
  green-field: '#E2F1D9'
  blue: '#0A7FC0'
  blue-ink: '#005C92'
  magenta: '#C2188A'
  magenta-dark: '#9E1272'
  magenta-ink: '#930F69'
  magenta-tint: '#F8DCEE'
  trust-high: '#1E6B34'
  trust-medium: '#8A5300'
  trust-low: '#B42318'
  row-hover: '#F1F5EE'
  group-row: '#FBFCFA'
typography:
  display:
    fontFamily: 'Albert Sans'
    fontSize: 'clamp(2rem, 1.2rem + 2.4vw, 3.5rem)'
    fontWeight: '700'
    lineHeight: '1.12'
    letterSpacing: -0.02em
  headline:
    fontFamily: 'Albert Sans'
    fontSize: 'clamp(1.75rem, 1rem + 1.6vw, 2.5rem)'
    fontWeight: '600'
    lineHeight: '1.12'
    letterSpacing: -0.02em
  title:
    fontFamily: 'Albert Sans'
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  app-title:
    fontFamily: 'Albert Sans'
    fontSize: 1.875rem
    fontWeight: '700'
    lineHeight: '1.15'
    letterSpacing: -0.02em
  body:
    fontFamily: 'Albert Sans'
    fontSize: 1.0625rem
    fontWeight: '400'
    lineHeight: '1.6'
  body-app:
    fontFamily: 'Albert Sans'
    fontSize: 0.9375rem
    fontWeight: '400'
    lineHeight: '1.5'
  small:
    fontFamily: 'Albert Sans'
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: '1.5'
  caption:
    fontFamily: 'Albert Sans'
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: '1.4'
  label:
    fontFamily: 'Albert Sans'
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: '1.3'
  figure:
    fontFamily: 'Albert Sans'
    fontSize: 1rem
    fontWeight: '700'
    lineHeight: '1.2'
  chart-label:
    fontFamily: 'Albert Sans'
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1'
  chart-order:
    fontFamily: 'Albert Sans'
    fontSize: 46px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: -0.02em
  code:
    fontFamily: 'ui-monospace, SF Mono, Menlo, monospace'
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: '1.4'
  display-compact:
    fontFamily: 'Albert Sans'
    fontSize: 'clamp(2rem, 1rem + 2vw, 2.75rem)'
    fontWeight: '700'
    lineHeight: '1.12'
    letterSpacing: -0.02em
  app-title-compact:
    fontFamily: 'Albert Sans'
    fontSize: 1.625rem
    fontWeight: '700'
    lineHeight: '1.15'
    letterSpacing: -0.02em
  panel-title:
    fontFamily: 'Albert Sans'
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: '1.15'
    letterSpacing: -0.02em
  title-large:
    fontFamily: 'Albert Sans'
    fontSize: 1.375rem
    fontWeight: '700'
    lineHeight: '1.15'
    letterSpacing: -0.02em
  lede:
    fontFamily: 'Albert Sans'
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: '1.6'
  card-label:
    fontFamily: 'Albert Sans'
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: '1.3'
rounded:
  xs: 2px
  sm: 4px
  md: 6px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 32px
  gutter: 'clamp(1rem, 0.6rem + 1.2vw, 1.75rem)'
  section: 'clamp(3.5rem, 2.5rem + 3.5vw, 6.5rem)'
  rail: 248px
  side-column: 'clamp(300px, 26vw, 372px)'
components:
  button-primary:
    backgroundColor: '{colors.magenta}'
    textColor: '{colors.white}'
    typography: '{typography.label}'
    rounded: '{rounded.sm}'
    height: 46px
    padding: '0 20px'
  button-primary-hover:
    backgroundColor: '{colors.magenta-dark}'
  button-secondary:
    backgroundColor: '{colors.white}'
    textColor: '{colors.ink}'
    typography: '{typography.label}'
    rounded: '{rounded.sm}'
    height: 40px
    padding: '0 16px'
  button-secondary-hover:
    backgroundColor: '{colors.green-field}'
  text-field:
    backgroundColor: '{colors.white}'
    textColor: '{colors.ink}'
    typography: '{typography.body}'
    rounded: '{rounded.sm}'
    height: 46px
    padding: '0 12px'
  login-panel:
    backgroundColor: '{colors.green-field}'
    textColor: '{colors.ink}'
    padding: '20px 24px'
  app-rail:
    backgroundColor: '{colors.green-field}'
    textColor: '{colors.ink}'
    width: '{spacing.rail}'
  nav-item-active:
    backgroundColor: '{colors.white}'
    textColor: '{colors.ink}'
    rounded: '{rounded.md}'
  segmented-control-selected:
    backgroundColor: '{colors.ink}'
    textColor: '{colors.white}'
  calculation-line:
    backgroundColor: '{colors.paper}'
    textColor: '{colors.ink}'
    rounded: '{rounded.sm}'
    padding: '13px 14px'
  order-figure:
    textColor: '{colors.magenta-ink}'
    typography: '{typography.figure}'
  confidence-label-high:
    textColor: '{colors.trust-high}'
    typography: '{typography.label}'
  confidence-label-medium:
    textColor: '{colors.trust-medium}'
    typography: '{typography.label}'
  confidence-label-low:
    textColor: '{colors.trust-low}'
    typography: '{typography.label}'
  note:
    textColor: '{colors.blue-ink}'
    typography: '{typography.small}'
  warning:
    textColor: '{colors.ink}'
    typography: '{typography.small}'
  panel:
    backgroundColor: '{colors.white}'
    textColor: '{colors.ink}'
  product-table:
    backgroundColor: '{colors.white}'
    textColor: '{colors.ink}'
    typography: '{typography.body-app}'
    rounded: '{rounded.md}'
  product-table-group-row:
    backgroundColor: '{colors.group-row}'
  product-table-row-hover:
    backgroundColor: '{colors.row-hover}'
  status-sentence:
    backgroundColor: '{colors.white}'
    textColor: '{colors.ink}'
    rounded: '{rounded.md}'
  tag-adjusted:
    textColor: '{colors.magenta-ink}'
    typography: '{typography.caption}'
---

## Brand & Style

Prognose is drawn as an **orienteering map** (O-kartet). A purchasing manager reads a product's sales the way an orienteer reads terrain, through a legend they can trust. The sales history is the terrain, the weeks used in the calculation are the controls, the forecast is the course to next week, and the finish is the number to order. The map grammar is a working information system, not ornament. Every symbol on a chart is explained in a legend, and the magenta overprint marks the course and the action only.

The landing page (Impeccable's Persuade mode) carries the full map sheet: a framed neatline, a title bar, a map face with the course chart, and a margin column with the login and the legend. The app screens (Operate mode) take only four contributions from the map: type, palette, density and one signature move. That move puts the order quantity in a magenta finish circle and draws data quality and trust in the legend's symbols. Navigation, tables, inputs and buttons stay standard web components.

The tone is calm, precise, Norwegian and honest about limits. No decoration could be mistaken for data.

Approved mockups (2026-11-07): the [landing page with login](mockups/key-landing.html) and [Produktoversikt](mockups/key-produktoversikt.html). Alternate states are in an [internal design note](mockups/designnotat-tilstander.html) that is not shown to users. The spines win on any conflict with a mockup.

## Colors

**Light only.** Prognose is used at an office PC in daylight, so dark mode is not designed. No `-dark` tokens exist; adding them is a future decision.

- **Map white, `{colors.paper}`:** the page ground, a cool white, never cream.
- **White, `{colors.white}`:** panels, tables, inputs and the map sheet itself.
- **Black, `{colors.ink}`:** all body text and every data-quality symbol (×, △, ◆). **`{colors.ink-2}`** is for secondary text. **`{colors.line}`** is for input borders and chart axes. **`{colors.rule}`** is for hairline rules.
- **Contour brown, `{colors.brown}`:** the sales-history line. **`{colors.brown-grid}`** is for gridlines every 5 units, like contour lines.
- **Open-land yellow, `{colors.yellow}`:** the field behind the three forecast weeks. It is never used for text or buttons.
- **Vegetation green:** **`{colors.green-screen}`** is the scenario band and the «Normal» cell. **`{colors.green-field}`** is the shell color: the app rail, the login panel and the «Prøv selv» band.
- **North-line blue, `{colors.blue}`:** the «nå» line only. **`{colors.blue-ink}`** is the text color of Merknad.
- **Course magenta, `{colors.magenta}`:** the course, calculation-week circles, the finish circle, Bestill snart and the primary button. **`{colors.magenta-dark}`** is button hover. **`{colors.magenta-ink}`** is magenta text and the focus ring. **`{colors.magenta-tint}`** is text selection.
- **Confidence colors, always with a shape and a word:** **`{colors.trust-high}`** for høy, **`{colors.trust-medium}`** for middels, **`{colors.trust-low}`** for lav. Elsewhere, red appears only in error states: the login error and invalid input in a text field.

**Contrast (WCAG 2.2 AA, checked by script):**

| Pair | Ratio | Use |
|---|---|---|
| `ink` on `paper` / `white` | 17.0 / 18.2 | body text |
| `ink-2` on `paper` / `white` / `green-field` | 7.7 / 8.3 / 7.0 | secondary text |
| `white` on `magenta` | 5.5 | primary button label |
| `magenta-ink` on `paper` / `white` / `yellow` | 7.8 / 8.4 / 6.5 | magenta text, focus ring |
| `blue-ink` on `paper` | 6.7 | Merknad |
| `trust-high` / `trust-medium` / `trust-low` on `white` | 6.6 / 6.3 / 6.6 | confidence labels |
| `line` on `white` | 5.0 | input borders (3:1 needed) |
| `brown` / `magenta` / `blue` on `paper` | 4.7 / 5.2 / 4.1 | chart lines (3:1 needed) |

## Typography

There is one brand typeface, **Albert Sans** (SIL Open Font License), with weights 400, 500, 600 and 700. The app self-hosts the WOFF2 files and links no font CDN (NFR-1). The fallback stack is Avenir Next, Segoe UI, system-ui, sans-serif.

| Token | Use |
|---|---|
| `{typography.display}` | the landing headline only |
| `{typography.display-compact}` | the landing headline on short desktop screens (760 px high and below) |
| `{typography.headline}` | landing section headings |
| `{typography.title}` | panel and card headings |
| `{typography.panel-title}` | the «Logg inn» heading in the login panel |
| `{typography.title-large}` | the wordmark and the scenario values |
| `{typography.app-title}` | the page title in the app («Produktoversikt») |
| `{typography.app-title-compact}` | the app page title on phones |
| `{typography.body}` | landing body text |
| `{typography.lede}` | the landing lede and section introductions |
| `{typography.body-app}` | app body text and table cells |
| `{typography.small}` | notes, warnings, help text |
| `{typography.caption}` | captions, group descriptions, the reason under a confidence label |
| `{typography.label}` | form labels, buttons, confidence labels |
| `{typography.card-label}` | value labels in product cards on phones |
| `{typography.figure}` | the order quantity in tables |
| `{typography.chart-label}` | chart axes and labels |
| `{typography.chart-order}` | the order number at the chart's finish |
| `{typography.code}` | commands and code only, such as the README load command in an empty state. It is the system monospace, not a brand face. |

Rules:
- **Figures:** all figures use tabular lining numerals (`font-variant-numeric: tabular-nums lining-nums`), a decimal comma, the true minus sign − and a no-break space before %.
- **Text size:** body text never goes below 13 px, and no functional text goes below 11 px.
- **Headings:** headings use balanced wrapping. No label sits above a heading (no kickers or eyebrows), and there are no section numbers. The numbers 1 to 3 in the calculation steps are not section numbers: they are course controls that state the calculation order.

## Layout & Spacing

**Spacing:** the base scale is 4, 8, 12, 16, 24 and 32 px (`{spacing.1}` to `{spacing.6}`). Sections are separated by `{spacing.section}` and columns by `{spacing.gutter}`. Headings always have more space above than below.

**Landing page:**
- **Desktop.** The map sheet fills the first viewport. It is a two-column grid: the map face is fluid, and the side column is `{spacing.side-column}` with the login and the legend. Below the sheet, the content sits in a container at most 1200 px wide, with side gutters of at least 16 px.
- **Short desktop screens.** At 760 px height and below, the headline and chart shrink so that the login, the chart and the calculation line fit at 1366 × 768.
- **900 px and below.** The sheet becomes one column in this order: title bar, headline, login, chart, readout, legend, sheet foot.

**App:**
- **Desktop.** The rail is `{spacing.rail}` on the left, and the work area is fluid with 24 to 32 px padding.
- **Produktside.** At 1366 × 768 the suggested order quantity, the confidence label and the active warnings are visible without scrolling (FR-25).
- **No horizontal scroll from 1024 px upward** (NFR-6). The full breakpoint table is in EXPERIENCE.md, Responsive & Platform.

## Elevation & Depth

The map is flat print. There are no shadows, glows or glass. Depth comes from frames: the 1.5 px `{colors.ink}` neatline around the map sheet, 1 px `{colors.ink}` borders on panels and tables, and `{colors.rule}` hairlines inside them. Surfaces separate by tone (`{colors.paper}` against `{colors.white}`, `{colors.green-field}` for the shell). The only inset effect is the double ring of the finish symbol.

## Shapes

- **Corners:** crisp. The focus ring uses `{rounded.xs}`. Inputs, buttons, calculation lines and the segmented control use `{rounded.sm}`. App tables, the status sentence and nav items use `{rounded.md}`. Panels on the landing page are square, like map frames.
- **Circles:** reserved for map symbols. These are the calculation-week control (one ring), the finish (two rings), the course-control numbers and the confidence dots.
- **Icons:** drawn SVG in one stroke weight (1.8 px at 16 to 18 px). Unicode glyphs and emoji are never used as icons.

## Components

| Component | Visual spec |
|---|---|
| Wordmark | «Prognose» in `{typography.title-large}`, beside a magenta control circle with a course leg and a black center dot (an authored SVG). |
| Map frame | The landing page's first viewport: a 1.5 px ink neatline with corner ticks, a title bar ruled below, a map face, a side column ruled left, and a sheet foot ruled above. |
| Button | Primary: `button-primary` (magenta, white label, 46 px). Secondary: `button-secondary` (white, 1.5 px ink border), used for «Logg inn» in the title bar and for «Samlet bestillingsoversikt». Ghost: a 36 px outline, used for «Logg ut». |
| Login panel | `login-panel`: a pale green block at the top of the side column (framed at 900 px and below), holding a «Logg inn» heading, one instruction line, two fields, a full-width primary button and a help line. It is outlined 3 px in `{colors.magenta-ink}` when it is the anchor target. |
| Text field | `text-field`: a white field with a 1.5 px `{colors.line}` border that turns `{colors.ink}` on hover. A visible label sits above it. In the error state the border is `{colors.trust-low}`. |
| Course chart | **Lines:** the history is a 2.5 px `{colors.brown}` line with 3 px dots, the week forecasts are a dashed magenta line, and the «nå» line is 1.6 px `{colors.blue}`. **Fields:** the forecast weeks sit on a `{colors.yellow}` field with a `{colors.green-screen}` scenario band. **Data-quality markers:** a stockout week is an ink × over a 45° hatch with a dotted outline, an unusual week is a white triangle with an ink outline, and a level shift is a filled ink diamond. **Course:** calculation weeks are magenta rings (r 12) numbered 1 to 3 and joined by magenta legs, and the finish is a double ring labeled with `{typography.chart-order}`. **Labels:** `{typography.chart-label}`; calculation-week labels are bold `{colors.magenta-ink}`. **Mobile:** a variant at 700 px and below keeps the same data and symbols on a narrower canvas. |
| Tegnforklaring | The legend: a list of 26 × 18 px symbols with short labels, one per chart mark, in `{typography.small}`. |
| Data table toggle | A `<details>` with the summary «Vis tallene i tabell» in `{colors.magenta-ink}` 600. It opens a white table with one row per week. |
| Calculation line | `calculation-line`: paper ground, hairline border, tabular figures, the result in bold `{colors.magenta-ink}`. The rounding note and the margin caveat sit below it in `{typography.small}`. |
| Confidence label | A 12 to 16 px dot (filled for høy, half-filled for middels, empty for lav) and the word, in the trust color (`confidence-label-*`). The reason follows in `{typography.caption}` `{colors.ink-2}`. |
| Varsel and Merknad | Varsel: an ink triangle with «!» at 16 px plus the text (`warning`). Merknad: a `{colors.blue-ink}` square with «i» at 16 px plus the text (`note`). Neither has a colored side border. |
| Segmented control | Joined options with a 1.5 px `{colors.line}` border. The selected option is `segmented-control-selected`. At 560 px and below the filter becomes a 2 × 2 grid. |
| Settings confirmation | One line in `{colors.magenta-ink}` 600: «… endret fra … til … Foreslått bestillingsmengde: 11 → 13». |
| Scenario strip | Three joined cells (Pessimistisk, Normal, Optimistisk). The values are in `{typography.title-large}`, and Normal is on `{colors.green-screen}`. |
| Calculation steps | Three panels on the landing page with a magenta course line running through the gaps between them. Each heading starts with a control circle; the last is a double ring. |
| App rail | `app-rail`: pale green, a 1 px ink rule on the right, sticky, holding the wordmark, the nav (active item `nav-item-active` with a magenta icon), «Innstillinger i bruk», a mini legend and the account block. It becomes a top bar at 960 px and below. |
| Status sentence | `status-sentence`: one bordered line that combines the finish symbol, the counts and plain words, with no KPI tiles. |
| Product table | `product-table`: white, a 1 px ink frame, a header rule in ink, `{colors.rule}` row lines, group rows on `{colors.group-row}`, row hover `{colors.row-hover}`, and numeric columns right-aligned. The order quantity for Bestill snart is in `order-figure` with the finish symbol. At 640 px and below each row becomes a bordered card whose values are labeled from `data-label`. |
| Order table | A white table with a caption. The quantity is right-aligned in bold, an adjusted value shows «foreslått 11» below it, and the tags are «Foreslått» (ink) and «Justert av deg» (`tag-adjusted` with a pencil icon). |
| Forklaring | A heading «Forklaring» and plain paragraphs below the calculated numbers, at most 62 characters per line. The label «KI-omformulert forklaring» appears in `{typography.caption}` when FR-28 is on. |
| Empty state | A white bordered block with a heading, one or two sentences in `{colors.ink-2}` and one link or command. |

## Do's and Don'ts

| Do | Don't |
|---|---|
| Keep `{colors.magenta}` for the course, the order to place and the primary action | Use magenta for decoration, headings or chart marks other than the course |
| Explain every chart mark in a legend and make each mark differ by shape (NFR-7) | Tell stockout, unusual and level-shift weeks apart by color alone |
| Show the number inside its calculation | Show a lone big-number KPI tile, sparklines or progress rings |
| Use frames and hairlines for depth | Add shadows, glows, glass, gradients or gradient text |
| Draw icons as SVG in one stroke | Use emoji or Unicode symbols as icons |
| Use the binding Norwegian labels exactly | Use synonyms or English labels in the UI |
| Self-host Albert Sans and Chart.js | Load fonts or scripts from a CDN in the app |
| Keep the map grammar to the landing page and the four contributions in the app | Turn app screens into map pictures or style tables as ruled ledger paper |
