# Direction derivation: Prognose landing page (2026-11-06)

Working note for the BMAD UX run (design-directions creative tool), produced with Impeccable 4.8.0 `new-work` steps 1 to 4. The direction pick belongs to the user. Nothing here is a design decision yet.

## 1. What the first surface must carry

- **Mechanism (one sentence):** Prognose turns a small business's own weekly sales into one suggested order quantity per product, shows the whole calculation in a line you can check by hand, and says plainly when the number should not be trusted.
- **Audience's real scene:** Monday morning in the back office of a small Norwegian hardware store: the office PC, last week's sales, coffee, 20 minutes before the purchasing meeting (UJ-1). Second audience: the IBE160 examiner with the README open beside the browser, checking screen values against the reference spreadsheet.
- **Cultural home:** Norwegian small-business retail and the practical Nordic everyday: the hardware store floor, the week-number calendar, the stock count, the weather forecast everyone reads, road signs and maps, the order pad and the adding-machine tape.
- **What the landing page must prove in one viewport:** one number to order, how it was calculated, whether to trust it, and that you can log in right here (FR-1 makes the login page the only public page).
- **The rut (kept out of the candidate list):** the SaaS analytics landing page (navy or purple gradient hero, "AI-powered demand forecasting", a floating dashboard with a glowing line chart, three icon feature cards, logo strip, testimonials, pricing) and the ERP look (corporate blue, warehouse stock photos). Its predictable opposite is cream-paper editorial (italic display serif, hairlines, tracked mono labels) or neo-brutalist black and yellow.
- **Literal reading of the name:** "prognose" reads as the weather forecast (værprognose). At most one candidate is spent on it (candidate 3).

## 2. Grounded candidates, ordered by resonance

Each line: why it resonates and carries the mechanism; how it looks (ground and main colors, type voice, signature). Material families: calendar print (1), office paper (2, 7), public data graphics (3), physical place and material (4), public signage (5), cartography (6), planning tool (8). No family holds more than three; one operated tool (8).

1. **Ukeplanen (the week-number planner).** Norwegians plan by week number ("uke 46"), and Prognose works only in weeks: 104 weeks of history, the 12-week recent period, the three-week horizon. Looks like the year planner on the office wall: cool white sheet, a committed almanac red, black grid, giant condensed week numerals; signature: next week's cell holds the order.
2. **Lagerkortet (the visible-edge stock card file).** The pre-computer tool for exactly this job: one card per product, a colored signal rider on the visible edge for when to reorder, ruled columns ending in a balance. Looks like a grey-green steel drawer of saturated manila cards with teal ruled print, red stamps and typed figures; signature: the rider position is the weeks of cover.
3. **Værmeldingen (the meteogram).** Everyone in Norway reads a weather forecast every morning: a time axis, bars, a curve, a band of uncertainty and a clear "now". Carries forecast plus scenarios plus trust. Looks like a light sky field with white panels, bar blue and a warm forecast line, in a Norwegian media grotesk; signature: a full-width forecast band across the page. Must not borrow any weather brand.
4. **Hyllekanten (the shelf edge).** The purchasing manager walks these shelves daily: galvanized steel, clip-in label strips with article number and big figures, the yellow tag clipped on when stock is low. Looks like steel grey with safety-yellow labels and black label print; signature: the product's shelf label carries the number to order.
5. **Skiltet (road signs at night).** Norway's national sign system is a codified vocabulary, and the PRD has one too: warning (affects the label), note (does not), order soon. Looks like dark asphalt with retroreflective sign yellow, red, blue and white in sign lettering; signature: the yellow warning triangle and the blue information square carry the PRD's warnings and notes.
6. **O-kartet (the orienteering map).** Norway is an orienteering nation, and a map is read through its legend, as Prognose's chart is (NFR-7). The sales history is terrain, the calculation weeks are controls, the forecast is the course to next week. Looks like ISOM map colors (white, yellow open land, green screens, brown contours, black, blue) with the magenta course overprint; signature: the forecast drawn as a course with control circles.
7. **Regnestrimmelen (adding-machine tape and carbon order pad).** The counter's adding machine prints each sum on a roll, and the order pad keeps a carbon copy. The order calculation line is literally what the tape prints. Looks like white tape and carbon-blue ink on the pink copy, with the canary copy for adjustments; signature: the tape printing the calculation line by line.
8. **Planleggingstavla (the T-card planning board).** Stockrooms and workshops planned with racks of colored T-cards in week columns before software. One card per product, the column is when to act, the card pulls out to show details. Looks like an anodized aluminium rack with white, yellow, pink, green and blue cards; signature: the R-12 sort groups become the board's columns. Added as an eighth candidate because the user asked for ten concepts.

## 3. The roll

`impeccable concept-seed --scope direction --mode persuade` was run against the catalog API with telemetry off (the API is told not to record the roll). Seed reference: `seed:aedd9cea56b9908b` (candidate count 7). It assigned candidate 6 (O-kartet) as the direction to build, so Impeccable's pick card is candidate 1 (Ukeplanen). It dealt six catalog challengers.

## 4. Challengers: fused, weighed, verdict

Weighed against the assigned direction on audience identification and product clarity only.

| Challenger (catalog id) | Fused with Prognose | Verdict | Discipline kept and raised into O-kartet |
|---|---|---|---|
| Drum-machine step row (`signals-instruments-drum-machine-step-row`) | Weeks as step keys: lit = calculation week, dark = stockout, accent = unusual; the chase light is "now" | Declined: weak identification; clearer only for one mechanic | Every week is its own addressable step and "now" is always marked; the 104-week history never wraps, it scales as one unbroken row |
| Darkroom exposure record (`operate-b-exposure-record-zone-sheets`) | Data-quality states as hatch and line style; cross-hatch for conflicting signals | Declined: low identification; its jargon costs product clarity (strongest of the declined, adoptable on request) | States without color: excluded and not-in-use states are drawn as line style and hatch, so every state survives greyscale (NFR-7) |
| Chromatophore skin (`reefs-bioluminescent-nocturnal-chromatophore-skin-language`) | Signals drawn onto one living surface | Declined: loses both axes; GPU shaders do not fit a server-rendered app | Signals are drawn on the terrain at the week they happened, not only pinned on as badges |
| Drawcord cape (`textiles-weave-drape-fashion-drawcord-transforming-cape`) | One pull reshapes the whole: one setting changes every product | Declined: loses both axes | One control visibly reshapes the whole field (FR-21: «Endringen gjelder alle produkter i bedriften.») |
| City-pop airbrush sleeve (`pop-culture-shelf-city-pop-airbrush`) | Everything hangs on one horizon line | Declined: loses both axes; gradient text is a detector finding | One vertical "nå" line at the latest data week runs through the page: history to its left, forecast to its right |
| Metro typographic tiles (`digital-design-canon-metro-typographic-tiles`) | Products as flat status tiles, giant numerals as interface, pivot headers as navigation | **Competitive:** holds product clarity (glanceable number and urgency); does not beat the map on identification | Full alternate (K09). Its native cyan-on-black accent is a detector tell and must be replaced |

## 5. The ten concepts handed to the subagents

| # | Concept | Kind | Landing world | Secondary screen |
|---|---|---|---|---|
| K01 | O-kartet | Assigned by the roll, raised by five declined challengers | Orienteering map | Produktside |
| K02 | Ukeplanen | Impeccable's pick (top of the ordered list) | Week-number planner | Samlet bestillingsoversikt |
| K03 | Lagerkortet | Grounded, position 2 | Stock card file | Produktoversikt |
| K04 | Værmeldingen | Grounded, position 3 (literal reading) | Meteogram | Produktoversikt |
| K05 | Hyllekanten | Grounded, position 4 | Shelf edge and labels | Produktoversikt |
| K06 | Skiltet | Grounded, position 5 | Road signs at night | Produktside |
| K07 | Regnestrimmelen | Grounded, position 7 | Tape and carbon order pad | Samlet bestillingsoversikt |
| K08 | Planleggingstavla | Grounded, position 8 (added for ten) | T-card board | Produktoversikt |
| K09 | Flisene | Catalog challenger, competitive | Metro tiles, fused | Produktoversikt |
| K10 | Standarden | Standing exit: the category standard, played straight | High-craft B2B SaaS | Produktside |

## 6. Deviations from the Impeccable flow, and why

- **Ten full cards instead of a small hand.** Impeccable sizes the hand by the verdicts; the user explicitly asked for ten clearly different concepts, and "the brief wins". The extra cards are the user's own grounded candidates (kind `grounded`). No declined challenger was promoted to fill a slot.
- **No decision page.** `serve-question` starts a local server and waits for an immediate pick. The user wants to review all ten in their own time and choose later, so a static comparison page replaces it. The choice is recorded when the user makes it.
- **Code-led, no comps.** No image generation is available, and paid image APIs are excluded. Each card carries a full HTML sketch instead.
- **No browser screenshots.** A headless Chrome test crashed and its crash reporter reached for a folder outside the project, so browser rendering was dropped under the privacy rule. Checks rely on the detector (static scan), computed contrast ratios and code review.
- **Finish review and documentation come after the pick.** Impeccable's finish reviewer and documenter run on the chosen direction's build, not on exploration sketches.
