---
name: 'Prognose'
description: 'Visual identity for Prognose v1: a calm, cool workbench in navy, blue, turquoise and green, where the decision comes first, every number can be checked, and every warning has a shape and a word.'
status: final
created: '2026-11-15'
updated: '2026-11-16'
sources:
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/tilbakemelding-prd.md'
colors:
  canvas: '#EDF2F7'
  pane: '#F4F7FA'
  surface: '#FFFFFF'
  sunken: '#F2F6FA'
  ink: '#0E2236'
  muted: '#4A5B6E'
  border: '#D4DEE8'
  field: '#738699'
  axis: '#9AABBD'
  header: '#0E2236'
  on-header: '#FFFFFF'
  header-meta: '#BFCDDB'
  blue: '#1D56C4'
  on-blue: '#FFFFFF'
  blue-tint: '#E7EFFC'
  blue-ink: '#1B3F86'
  turquoise: '#08727A'
  turquoise-tint: '#EBF7F8'
  turquoise-border: '#BFE3E6'
  band: '#C5EBEE'
  green: '#15703F'
  green-tint: '#E2F3E8'
  amber: '#7A4B00'
  amber-tint: '#FFF1D6'
  red: '#B42318'
  red-tint: '#FDE7E4'
typography:
  wordmark:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 17px
    fontWeight: '700'
    lineHeight: '1.5'
  page-title:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 26px
    fontWeight: '700'
    lineHeight: '1.3'
  section-title:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 20px
    fontWeight: '700'
    lineHeight: '1.3'
  subsection-title:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '700'
    lineHeight: '1.3'
  card-title:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.3'
  body:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  meta:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.5'
  label:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 13px
    fontWeight: '600'
    lineHeight: '1.4'
  label-lg:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 15px
    fontWeight: '600'
    lineHeight: '1.4'
  order-number:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 44px
    fontWeight: '700'
    lineHeight: '1.1'
  order-number-card:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.15'
  order-number-row:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 18px
    fontWeight: '700'
    lineHeight: '1.15'
  week-figure:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 30px
    fontWeight: '700'
    lineHeight: '1.2'
  formula:
    fontFamily: 'ui-monospace, "SF Mono", Menlo, Consolas, monospace'
    fontSize: 13.5px
    fontWeight: '400'
    lineHeight: '1.5'
  chart-label:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.3'
  chart-caption:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif'
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.3'
rounded:
  xs: 3px
  sm: 4px
  md: 6px
  lg: 10px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 20px
  '6': 24px
  '7': 32px
  '8': 40px
  list-width: 392px
  list-width-narrow: 340px
  card-padding: 12px 14px
  panel-padding: 16px 20px 20px
  text-measure: 72ch
components:
  app-header:
    background: '{colors.header}'
    foreground: '{colors.on-header}'
    meta: '{colors.header-meta}'
    wordmark: '{typography.wordmark}'
  settings-bar:
    background: '{colors.surface}'
    border: '{colors.border}'
    label: '{colors.muted}'
    value: '{colors.ink}'
  product-list:
    background: '{colors.pane}'
    border: '{colors.border}'
    width: '{spacing.list-width}'
    width-narrow: '{spacing.list-width-narrow}'
  group-heading:
    title: '{typography.subsection-title}'
    summary: '{typography.meta}'
    summary-color: '{colors.muted}'
  product-card:
    background: '{colors.surface}'
    border: '{colors.border}'
    radius: '{rounded.lg}'
    padding: '{spacing.card-padding}'
    title: '{typography.card-title}'
    order-number: '{typography.order-number-card}'
    order-number-color: '{colors.blue}'
  product-card-selected:
    background: '{colors.blue-tint}'
    border: '{colors.blue}'
    secondary-text: '{colors.blue-ink}'
  product-card-no-forecast:
    border: '{colors.red}'
    reason: '{colors.red}'
    order-number-color: '{colors.ink}'
  product-row:
    background: '{colors.surface}'
    divider: '{colors.border}'
    order-number: '{typography.order-number-row}'
  search-field:
    background: '{colors.surface}'
    border: '{colors.field}'
    radius: '{rounded.md}'
    label: '{typography.label}'
  trust-label-hoy:
    background: '{colors.green-tint}'
    foreground: '{colors.green}'
    radius: '{rounded.full}'
    text: '{typography.label}'
  trust-label-middels:
    background: '{colors.amber-tint}'
    foreground: '{colors.amber}'
    radius: '{rounded.full}'
    text: '{typography.label}'
  trust-label-lav:
    background: '{colors.red-tint}'
    foreground: '{colors.red}'
    radius: '{rounded.full}'
    text: '{typography.label}'
  panel:
    background: '{colors.surface}'
    border: '{colors.border}'
    radius: '{rounded.lg}'
    padding: '{spacing.panel-padding}'
    title: '{typography.section-title}'
  decision-panel:
    order-number: '{typography.order-number}'
    order-number-color: '{colors.blue}'
  trust-panel:
    label: '{typography.label-lg}'
  warning-row-data:
    background: '{colors.red-tint}'
    icon: '{colors.red}'
    text: '{colors.ink}'
    radius: '{rounded.md}'
  warning-row-pattern:
    background: '{colors.amber-tint}'
    icon: '{colors.amber}'
    text: '{colors.ink}'
    radius: '{rounded.md}'
  unusual-weeks-switch:
    track-on: '{colors.blue}'
    track-off: '{colors.field}'
    knob: '{colors.surface}'
    radius: '{rounded.full}'
  forecast-chart:
    history: '{colors.ink}'
    forecast: '{colors.turquoise}'
    band: '{colors.band}'
    band-edge: '{colors.turquoise}'
    forecast-weeks: '{colors.turquoise-tint}'
    grid: '{colors.border}'
    baseline: '{colors.axis}'
    stockout-marker: '{colors.red}'
    unusual-marker: '{colors.amber}'
    level-shift-marker: '{colors.ink}'
    label: '{typography.chart-label}'
    caption: '{typography.chart-caption}'
  calculation-worksheet:
    header-text: '{colors.muted}'
    header-rule: '{colors.ink}'
    row-rule: '{colors.border}'
    text: '{typography.body-sm}'
  calculation-line:
    background: '{colors.sunken}'
    radius: '{rounded.sm}'
    text: '{typography.formula}'
  status-tag-stockout:
    background: '{colors.red-tint}'
    foreground: '{colors.red}'
    radius: '{rounded.sm}'
  status-tag-unusual:
    background: '{colors.amber-tint}'
    foreground: '{colors.amber}'
    radius: '{rounded.sm}'
  status-tag-level-shift:
    background: '{colors.canvas}'
    foreground: '{colors.ink}'
    radius: '{rounded.sm}'
  status-tag-used:
    background: '{colors.turquoise-tint}'
    foreground: '{colors.turquoise}'
    radius: '{rounded.sm}'
  explanation-panel:
    background: '{colors.turquoise-tint}'
    border: '{colors.turquoise-border}'
    text: '{colors.ink}'
  button-primary:
    background: '{colors.blue}'
    foreground: '{colors.on-blue}'
    border: '{colors.blue}'
    radius: '{rounded.md}'
  button-secondary:
    background: '{colors.surface}'
    foreground: '{colors.blue}'
    border: '{colors.blue}'
    radius: '{rounded.md}'
  week-path-step:
    circle-border: '{colors.field}'
    number: '{colors.muted}'
  week-path-step-current:
    circle: '{colors.blue}'
    number: '{colors.on-blue}'
  week-path-step-done:
    circle: '{colors.green}'
    number: '{colors.on-blue}'
  week-figure:
    number: '{typography.week-figure}'
    label: '{colors.muted}'
    rule: '{colors.border}'
  progress-segment:
    done: '{colors.green}'
    current: '{colors.blue}'
    remaining: '{colors.border}'
    radius: '{rounded.xs}'
  keyboard-key:
    background: '{colors.surface}'
    border: '{colors.field}'
    radius: '{rounded.sm}'
  confirmation-message:
    background: '{colors.blue-tint}'
    foreground: '{colors.blue-ink}'
    radius: '{rounded.md}'
  error-message:
    background: '{colors.red-tint}'
    icon: '{colors.red}'
    text: '{colors.ink}'
    radius: '{rounded.md}'
  settings-form:
    field-border: '{colors.field}'
    label: '{typography.label}'
  login-panel:
    background: '{colors.surface}'
    border: '{colors.border}'
    radius: '{rounded.lg}'
  combined-order-table:
    adjusted-quantity: '{colors.blue}'
    adjusted-marking: '{colors.blue-ink}'
    adjusted-marking-background: '{colors.blue-tint}'
  not-found-panel:
    background: '{colors.surface}'
    border: '{colors.border}'
    radius: '{rounded.lg}'
---

## Brand & Style

Prognose is a purchasing workbench for one person with 20 minutes before a Monday meeting. Its thesis, from the PRD, is that every number can be checked by hand and the app says when a forecast should not be trusted. The visual identity serves that thesis and nothing else: the decision is the largest thing on the screen, the calculation is always one scroll away, and every warning carries a shape and a word, never color alone.

The register is calm, cool and modern: navy text and a navy header bar, white panels on a pale blue-gray canvas, one blue for what you can do, one turquoise for what the forecast says, and green for what you can trust. It is denser than a consumer app and roomier than a spreadsheet. There is no decoration, no shadow, no gradient and no motion; the structure carries the hierarchy.

The design combines three concepts the user reviewed on 2026-11-15 and 2026-11-16 (concept D, «Kombinert»): the layout of concept C (product list on the left, the selected product and a large chart on the right), the product cards, clear order suggestions and simple workflow of concept B, and the worksheet calculations, sales data and explanation of concept A. The approved mockup is [mockups/konsept-d-kombinert.html](mockups/konsept-d-kombinert.html); the concepts and their rationale are in `.working/`. This spine and [EXPERIENCE.md](EXPERIENCE.md) win on any conflict with a mockup.

## Colors

Each color has one job. Contrast is measured with the WCAG 2.2 formula; every text pair is at least 4.5:1.

- **Ink (`#0E2236`)** is navy: all body text, headings, the chart's sales line and the header bar (`header`). On the header, text is white (`on-header`) and the company line is `header-meta` (`#BFCDDB`).
- **Canvas (`#EDF2F7`), pane (`#F4F7FA`) and surface (`#FFFFFF`)** are the three tonal layers: the app background, the product list, and every card and panel. `sunken` (`#F2F6FA`) sits behind formulas.
- **Muted (`#4A5B6E`)** is secondary text: labels, facts on cards, notes and fine print. On tinted backgrounds the text switches to the darker tone of that tint (`blue-ink` on `blue-tint`) or to ink, never muted gray.
- **Blue (`#1D56C4`)** is action and decision: buttons, links, the selected product, the focus ring, the switch when on, and the suggested order quantity in large type. `blue-tint` (`#E7EFFC`) marks the selected card and confirmations, with `blue-ink` (`#1B3F86`) for text on it.
- **Turquoise (`#08727A`)** is the forecast: the forecast line and its dots, the forecast week labels in the chart, the «brukt» tag in the sales table. `turquoise-tint` (`#EBF7F8`) shades the forecast weeks in the chart and the «Forklaring» panel (border `turquoise-border`, `#BFE3E6`), and `band` (`#C5EBEE`) fills the scenario band. Turquoise text is never placed on the band (4.46:1).
- **Green (`#15703F` on `#E2F3E8`)** means trust and completion: the «høy» label, completed steps and completed progress segments. It is never used for buttons or warnings.
- **Amber (`#7A4B00` on `#FFF1D6`)** marks unusual demand: «middels», unusual weeks, level shifts and seasonal patterns.
- **Red (`#B42318` on `#FDE7E4`)** marks data that cannot be trusted: «lav», stockout weeks, old data, missing forecasts and errors.
- **Border (`#D4DEE8`), field (`#738699`) and axis (`#9AABBD`)** are hairlines, form-field and switch-off borders (3:1 or more against white), and the chart's baseline.

| Pair | Ratio | Where |
|---|---|---|
| ink on surface / canvas | 16.1:1 / 14.3:1 | all body text |
| muted on surface / canvas / pane | 7.0:1 / 6.2:1 / 6.5:1 | secondary text |
| on-header / header-meta on header | 16.1:1 / 10.0:1 | header bar |
| blue on surface; on-blue on blue | 6.6:1; 6.6:1 | links, secondary and primary buttons, order numbers |
| blue on blue-tint; blue-ink on blue-tint | 5.7:1; 8.6:1 | selected card, confirmation |
| turquoise on surface / turquoise-tint | 5.7:1 / 5.2:1 | forecast text, «brukt» |
| green on green-tint | 5.3:1 | «høy» |
| amber on amber-tint | 6.6:1 | «middels», «uvanlig» |
| red on red-tint / surface | 5.6:1 / 6.6:1 | «lav», «utsolgt», errors |
| field on surface | 3.8:1 | field borders, switch off (non-text, 3:1) |

Light mode only. Dark mode is not designed, and the PRD does not require it.

## Typography

One family: the system UI stack (`system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif`), so the app needs no web font and works offline (NFR-1). Formulas use the system monospace stack (`formula`). All numbers use tabular numerals (`font-variant-numeric: tabular-nums`) so that columns line up.

| Role | Token | Use |
|---|---|---|
| Page title | `{typography.page-title}` | product name, «Denne uken», page headings |
| Section title | `{typography.section-title}` | panel headings («Hva bør du bestille?», «Forklaring») and «Produktoversikt» |
| Subsection title | `{typography.subsection-title}` | group headings in the list, worksheet subsections |
| Card title | `{typography.card-title}` | product names on cards |
| Body | `{typography.body}` | running text, reasons, explanation |
| Body small | `{typography.body-sm}` | settings bar, product meta line, warnings, tables, switch text |
| Meta | `{typography.meta}` | facts on cards, notes, fine print, legend |
| Label | `{typography.label}` | trust labels, field labels, «Foreslått», keyboard keys |
| Label large | `{typography.label-lg}` | the trust label in the product header and trust panel |
| Order number | `{typography.order-number}` | the suggested order quantity on the product screen |
| Order number, card / row | `{typography.order-number-card}` / `{typography.order-number-row}` | the quantity on cards and compact rows |
| Week figure | `{typography.week-figure}` | the four figures on «Denne uken» |
| Formula | `{typography.formula}` | forecast calculation and order calculation line |
| Chart label / caption | `{typography.chart-label}` / `{typography.chart-caption}` | axes and markers / scenario captions and region labels |

Rules: no text below 12 px (chart labels only), and no UI text below 13 px. No letter-spacing and no uppercase labels. Headings have more space above than below. Paragraphs stop at `{spacing.text-measure}`.

## Layout & Spacing

Spacing scale: `{spacing.1}` 4 · `{spacing.2}` 8 · `{spacing.3}` 12 · `{spacing.4}` 16 · `{spacing.5}` 20 · `{spacing.6}` 24 · `{spacing.7}` 32 · `{spacing.8}` 40 px. Tight pairs (label and value, icon and word) use 4–8 px, items in a list 8 px, panels 16 px apart, and sections 24–40 px.

The app shell, top to bottom: the app header, the settings bar, and the work area. The work area has two columns, each scrolling separately: the product list at `{spacing.list-width}` on the left and the selected product filling the rest, with 16 px top and 24 px side padding.

On the product screen, the decision panel and the trust panel sit side by side in two equal columns, and the forecast chart spans the full width right below them. The calculation worksheet and the explanation follow at full width.

Reference size: 1366 × 640 px of browser content, which is what a 1366 × 768 screen shows. At that size the suggested order quantity, the confidence label and the active warnings are above the fold (FR-25), and the chart's heading and top edge are visible without scrolling.

Narrower windows: at 1180 px and below the list narrows to `{spacing.list-width-narrow}` and the two decision panels stack. At 900 px and below the layout is one column, with the list on top (at most 420 px high, scrolling on its own) and the product below. Wide tables scroll inside their own frame. The breakpoints and the 800 px floor are in EXPERIENCE.md (Responsive & Platform).

## Elevation & Depth

Flat. Depth comes from the three tonal layers (canvas, pane, surface) and 1 px `border` hairlines, never from shadows. The header bar is the only dark surface. Selection is shown by `blue-tint` fill plus a 2 px blue border; focus by a 3 px blue outline 2 px outside the element. Nothing floats: there are no modals, popovers or sticky overlays.

## Shapes

`{rounded.lg}` (10 px) for cards, panels and the browser frame of mockups; `{rounded.md}` (6 px) for buttons, fields, warning rows and messages; `{rounded.sm}` (4 px) for status tags, the calculation line and keyboard keys; `{rounded.xs}` (3 px) for progress segments; `{rounded.full}` for trust labels and the switch.

Shapes also carry meaning, so that color is never the only signal (NFR-7):

| Meaning | Shape |
|---|---|
| Høy / Middels / Lav | filled circle / filled triangle / filled square, always with the word |
| Stockout week | hollow square (white fill, red outline) |
| Unusual week | filled amber triangle |
| Level shift | filled ink diamond |
| Old data, insufficient data, seasonal pattern, error | ring with «!» in the row's color |

## Components

Visual specs. Behavior is in EXPERIENCE.md (Component Patterns). Names match across both spines.

- **App header** — `header` bar, 10 px × 20 px padding. Left: the wordmark «Prognose» (`{typography.wordmark}`, white) and the company with the latest data week (`{typography.body-sm}`, `header-meta`). Right: the navigation links in white, 14 px; the current page has weight 600 and a 2 px white underline. No logo mark, and no turquoise or blue text on navy.
- **Settings bar** — white strip with a bottom hairline, 8 px × 20 px. «Innstillinger i bruk:» in muted, the values in ink at weight 600, then a small secondary button «Endre innstillinger» and the sentence «Endringen gjelder alle produkter i bedriften.» in `{typography.meta}` muted, pushed to the right. Wraps to two lines when narrow.
- **Product list** — `pane` background with a right hairline, padding 16 / 12 / 24 px. «Produktoversikt» in `{typography.section-title}` with the product count in meta; then the search field, the groups, and the keyboard hint.
- **Group heading** — the group name in `{typography.subsection-title}`, its summary («4 produkter · 31 enheter foreslått») in meta muted, right-aligned on the same line; 24 px above, 8 px below.
- **Product card** — white, 1 px border, `{rounded.lg}`, `{spacing.card-padding}`, 8 px apart. Top left: the name (`{typography.card-title}`) and «Varenr. 10012» (meta muted). Top right: «Foreslått» (meta muted) over the suggested order quantity (`{typography.order-number-card}`, blue). Then a facts line in meta: «Lager», «Ukeprognose uke 1» and «Uker dekning» in muted with their values in ink 600. Last: the trust label and, unless it is «høy», the reason in meta muted. *Selected:* `blue-tint` fill, 2 px blue border, secondary text in `blue-ink`. *No forecast:* 2 px dashed red border, the reason in red 600 where the forecast would be, «–» in ink for the quantity and the weeks of cover. When a card is both selected and without a forecast, selection wins (solid blue border); the red reason stays.
- **Product row** — the compact form for «Øvrige produkter»: rows inside one white bordered box (`{rounded.lg}`), separated by hairlines, 10 px × 14 px. Name in 15 px 600; one meta line with product number, stock, week-1 forecast and weeks of cover; «Foreslått» over the quantity in `{typography.order-number-row}` ink (0 is not an order, so no blue); the trust label below.
- **Search field** — visible label «Søk i produktene» (`{typography.label}`), then a white input with a 1 px `field` border, `{rounded.md}`, 7 px × 10 px, 14 px text.
- **Trust label** — a pill (`{rounded.full}`, 2 px × 10 px with 8 px before the icon), `{typography.label}`, a 12 px shape icon in the text color and the word: «Høy» green, «Middels» amber, «Lav» red, each on its tint. The large variant (`{typography.label-lg}`, 14 px icon) appears next to the product name and in the trust panel.
- **Panel** — white, 1 px border, `{rounded.lg}`, `{spacing.panel-padding}`, 16 px apart; heading in `{typography.section-title}`.
- **Decision panel** — a panel titled «Hva bør du bestille?». The suggested order quantity in `{typography.order-number}` blue, with «Foreslått bestillingsmengde for neste uke, uke 46» in 16 px 600 on the same baseline. The buttons sit at the bottom of the panel: primary «Behold 11 og gå videre», secondary «Juster mengden». Without a forecast, the number is «–» in ink, with «Ingen foreslått bestillingsmengde».
- **Trust panel** — a panel titled «Kan du stole på prognosen?», the same height as the decision panel: the large trust label, the reason in body, then the warning list.
- **Warning list** — rows with 8 px × 10 px padding, `{rounded.md}`, 8 px apart, 14 px ink text and a 16 px icon. Data problems (stockout weeks, old data, insufficient data) use `red-tint`; demand patterns (unusual weeks, level shift, seasonal pattern) use `amber-tint`. Icons follow Shapes.
- **Unusual-weeks switch** — below the chart legend, after a hairline with 12 px above. A 40 × 22 px track (`{rounded.full}`) with a 16 px white knob: blue with the knob on the right when unusual weeks are included, `field` gray with the knob on the left when they are excluded. Beside it, 14 px text: the state in bold («Uvanlige uker tas med.»), what switching does, and «Endringen gjelder alle produkter i bedriften.». Only the chart itself is full width; the switch keeps its 40 × 22 px size.
- **Forecast chart** — a panel titled «Hva skjer med salget?» with a one-line subtitle in body-small muted, then the chart at full width (aspect about 3:1) and the legend.
  - Sales: an ink line, 2.5 px, with 4.5 px dots where weeks are at least 12 px apart.
  - Stockout weeks: the line breaks, a 1.5 px dashed ink connector bridges the gap, and each week gets a 12 px hollow red square at its sales value.
  - Unusual weeks: an amber triangle about 20 × 17 px on the point, with its sales value in 12 px ink.
  - Level-shift weeks: a 14 px ink diamond.
  - Forecast: the three forecast weeks sit on a `turquoise-tint` area labeled «De neste tre ukene» (13 px ink), with a 3 px turquoise line and dots, joined to the last sales week by a 2 px dashed turquoise line.
  - Scenarios: the band in `band` with 1.5 px dashed turquoise edges, and the captions «Optimistisk», «Normal» (bold) and «Pessimistisk» with values in `{typography.chart-caption}` ink.
  - Recent period: a dashed `border` line where the last 12 weeks begin, labeled «Siste 12 uker» in chart-label muted.
  - Axes: gridlines in `border`, baseline in `axis`, labels in `{typography.chart-label}` muted, and the forecast week numbers in turquoise 700.
  - Legend: 13 px ink items, each with its 14 px marker (24 px for lines and the band).
- **Calculation worksheet** — a panel titled «Slik er tallene regnet ut» with subsections in `{typography.subsection-title}`: «Salgshistorikk, siste 12 uker», «Prognoseutregning», «Ukeprognoser og scenarioer» and «Utregning av bestillingsmengde». Tables: 14 px, a header row in 13 px muted with a 1 px ink rule below, hairlines between rows, numbers right-aligned, first column left-aligned. In the scenario table the normal row is bold and its order quantity is blue.
- **Calculation line** — a `sunken` box, `{rounded.sm}`, 8 px × 10 px, in `{typography.formula}`. «Tallene er avrundet for visning.» sits on its own line inside the box in 13 px muted system UI. The FR-12 sentence about the safety margin follows below the box in meta muted.
- **Status tag** — in the sales table: `{rounded.sm}`, 1 px × 6 px, 13 px, with a 10 px icon. «utsolgt» red on red-tint (hollow square), «uvanlig» amber on amber-tint (triangle), «nytt nivå» ink on canvas (diamond), «brukt» turquoise on turquoise-tint (no icon).
- **Explanation panel** — a panel on `turquoise-tint` with a `turquoise-border` border, titled «Forklaring», body text in ink only, at most `{spacing.text-measure}`. When a language model has rephrased it, «KI-omformulert forklaring» appears above the text in `{typography.label}` ink.
- **Button** — `{rounded.md}`, 8 px × 14 px, weight 600, 1 px blue border. Primary: blue fill, white text. Secondary: white fill, blue text. The small variant (5 px × 10 px, 14 px) is used in the settings bar. Text only, no icon-only buttons.
- **Week path** — three steps in a row: a 30 px circle with the number (2 px `field` border, muted number), the step title in 16 px 600 ink and a line of meta muted. Current step: blue circle, white number. Done step: green circle, white number.
- **Week figures** — four figures in a row between two hairlines with 16 px padding, no boxes: the number in `{typography.week-figure}` ink, the label below in 14 px muted.
- **Progress bar** — four 28 × 6 px segments, `{rounded.xs}`, 4 px apart: green for done, blue for the current product, `border` for the rest; always followed by its text («produkt 2 av 4 som bør bestilles snart»).
- **Previous and next links** — plain blue links with arrows («← Isskrape», «Lyspære LED E27 9 W →»), right-aligned in the product header.
- **Keyboard key** — 13 px, 0 × 6 px, white with a 1 px `field` border, `{rounded.sm}`.
- **Confirmation message** — `blue-tint` with `blue-ink` text, `{rounded.md}`, 8 px × 12 px, at the top of the product area. (Spine-only.)
- **Error message** — a `red-tint` row with the red «!» ring and ink text, `{rounded.md}`, placed above the fields it concerns. (Spine-only.)
- **Settings form** — a panel with one field per setting: visible label (`{typography.label}`), number fields like the search field with the unit after them, radio buttons for the method and for unusual weeks, and «Lagre» (primary) and «Avbryt» (secondary). (Spine-only.)
- **Login panel** — one panel, at most 420 px wide, centered on the canvas below the header bar without navigation. It holds the page title «Logg inn», fields with visible labels and a primary «Logg inn» button. (Spine-only; wireframe in EXPERIENCE.md.)
- **Combined order table** — a panel with the worksheet's table style. An adjusted quantity is blue, and its marking «Justert av deg» is a `blue-tint` tag in `blue-ink`; «Foreslått» is plain muted text. The total row is bold. (Spine-only; wireframe in EXPERIENCE.md.)
- **Not-found panel** — a panel with the page title «Siden finnes ikke» and a link back to «Produktoversikt». (Spine-only.)

## Do's and Don'ts

| Do | Don't |
|---|---|
| Make the suggested order quantity the largest number on the screen | Give the chart, a figure or a heading more weight than the decision |
| Pair every trust label and marker with a shape and a word | Signal anything with color alone |
| Keep blue for actions and the decision, turquoise for the forecast, green for trust | Use green for buttons, or red and amber for decoration |
| Show every formula in monospace with the rounding note | Hide a calculation behind a tooltip or a hover |
| Use the three tonal layers and hairlines for depth | Add shadows, gradients, glows or side stripes on cards |
| Keep UI text at 13 px or more and paragraphs within 72 characters | Use uppercase labels, letter-spacing or text below 12 px |
| Keep the switch, icons and markers at their own sizes | Let a rule meant for the chart (`width: 100%`) reach other SVGs |
| Use system fonts and inline assets only | Load web fonts or anything from a CDN (NFR-1) |
