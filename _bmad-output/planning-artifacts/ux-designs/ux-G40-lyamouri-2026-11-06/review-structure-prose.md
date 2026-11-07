# Editorial review: structure and prose (Prognose UX spines)

- **Documents:** `DESIGN.md` (SHA-256 `9daccf57292ff929…`, 2,758 words, of which 502 are YAML) and `EXPERIENCE.md` (SHA-256 `a1a4654b10ea020a…`, 3,605 words), both in this folder.
- **Lenses:** structure first, then prose. The prose pass builds on the structure findings.
- **Style guide:** Microsoft Writing Style Guide. **Reader type:** humans (architects and developers, some of them AI agents, plus the course teacher and examiner), with LLM-grade precision wherever a builder consumes a rule.
- **Date:** 2026-11-07. Word counts come from the skill's `word_metrics.py`.
- **Version note:** DESIGN.md changed during the review. The 14:35 version added seven typography tokens, `rounded.xs`, the matching Typography rows and one phrase in Shapes. These additions are approved documentation of the mockups, and no finding asks to change them.

**Purpose and audience.** These two documents exist to help architects and developers, human or AI, build Prognose's look (DESIGN.md) and behavior (EXPERIENCE.md) from one contract each. They also let the teacher and the examiner trace each design decision back to the PRD.

Every quoted "Original Text" below occurs exactly once in its file, so a fix can be applied by plain search and replace.

## Structure lens

**Model.** Both spines are Reference/Database documents: readers jump straight to a token, a component, a state or a breakpoint. The review therefore judges findability, MECE grouping and a consistent schema per item. Key Flows are also judged as linear sequences: steps in order, with the climax as the definition of done.

**Spine fit.**

- **DESIGN.md: complete.** The YAML carries all five token groups (colors, typography, rounded, spacing, components) plus name, description and status. The eight body sections each appear once, in the locked order, with nothing extra.
- **EXPERIENCE.md: complete.** All eight required sections appear in spine order. Both triggered sections, Responsive & Platform and Inspiration & Anti-patterns, sit where the BMAD examples put them. The two invented sections earn their place: Calculation display rules comes right after Component Patterns, whose Calculation line row points to it, and Open items comes last.

### DESIGN.md

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §Typography token table: 19 rows (205 words). The seven approved rows from `{typography.code}` to `{typography.card-label}` follow `{typography.chart-order}` at the end. | MOVE each of those rows directly under its base role, with no change to names or Use text. Row order: display, display-compact, headline, title, panel-title, title-large, app-title, app-title-compact, body, lede, body-app, small, caption, label, card-label, figure, chart-label, chart-order, code. | **S-D1.** Each variant now sits 9 to 13 rows from its base token, so the ramp no longer reads top-down. A builder can't see `display` and `display-compact` together, or `label` and `card-label`. Placement only. 0 words. |
| structure | §Components, Course chart row: one cell of 11 sentences (124 words) that interleaves lines, fields, markers, course symbols, labels and the mobile variant. | MOVE (regroup inside the cell, same facts): **Lines:** the history is a 2.5 px `{colors.brown}` line with 3 px dots, the week forecasts are a dashed magenta line, and the «nå» line is 1.6 px `{colors.blue}`. **Fields:** the forecast weeks sit on a `{colors.yellow}` field with a `{colors.green-screen}` scenario band. **Data-quality markers:** a stockout week is an ink × over a 45° hatch with a dotted outline, an unusual week is a white triangle with an ink outline, and a level shift is a filled ink diamond. **Course:** calculation weeks are magenta rings (r 12) numbered 1 to 3 and joined by magenta legs; the finish is a double ring labeled with `{typography.chart-order}`. **Labels:** `{typography.chart-label}`; calculation-week labels are bold `{colors.magenta-ink}`. **Mobile:** a variant under 700 px keeps the same data and symbols on a narrower canvas. | **S-D2.** This is the signature component and the densest cell in either spine. Grouping by run-in label lets a builder check each mark against Tegnforklaring. The rewrite also absorbs prose fix P-D4. "Data-quality markers" reuses the wording in Colors ("every data-quality symbol (×, △, ◆)"). +5 words. |

### EXPERIENCE.md

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §Responsive & Platform table (9 lines, 168 words). The App breakpoints (1180 px, 960 px) sit inside rows cut for the landing page. The 1024–1365 px row's App cell reads "Rail 208 px from 1180 px; mini legend hidden", the 901–1023 px row reads "Rail 208 px", and the 900 px row reads "Rail becomes a top bar at 960 px". | QUESTION: split the table into a Landing table (the current rows) and an App table with its own rows. A candidate App table follows this table; the ranges marked [confirm] are inferred and need the author. | **S-E1.** As laid out, the 901–1023 px row says "Rail 208 px", but IA › Navigation and DESIGN.md › App rail put the top bar at 960 px and below, so that row is wrong from 901 to 960 px. "From 1180 px" doesn't say which side of 1180 gets the 208 px rail; the next row implies the narrower side. The 700 px row lists the chart switch under Landing only, although the Course chart also appears on Produktside. No breakpoint or value changes. About +15 words. |
| structure | Undefined region terms. "decision strip" appears in the wireframe label, Component Patterns › Varsel and Merknad, the 1366 px row of Responsive & Platform, and Flow 1 step 3. "readout" appears in Component Patterns › Map frame and › Calculation line, the 900 px and 640 px rows of Responsive & Platform, and DESIGN.md › Layout & Spacing. | QUESTION: define each term once, for example as two IA bullets after **Breadcrumb**:<br>`- **Decision strip:** the top band of Produktside, with the suggested order quantity, the confidence label and its reason, the warnings and the calculation line. It stays above the fold at 1366 × 768 (FR-25).`<br>`- **Readout (landing page):** the block under the landing chart, with the confidence label and its reason, the safety-margin try-out, the calculation line and the settings confirmation.`<br>The wording comes from the Produktside wireframe, Flow 1 step 3 and the landing mockup; confirm it. | **S-E2.** Missing scaffolding. The decision strip carries the FR-25 above-the-fold guarantee, yet only an ASCII label defines it, and "readout" is never defined. About +60 words. |
| structure | §Information Architecture, Visual reference column: the "Landing page with login" and "Produktoversikt (dashboard)" rows say only "mockup". The links are only in the preface. | MOVE the links to where they're used. In the Landing page with login row, `mockup` → `[mockup](mockups/key-landing.html)`. In the Produktoversikt (dashboard) row, `mockup` → `[mockup](mockups/key-produktoversikt.html)`. Keep the preface list as the summary. | **S-E3.** A reader scanning IA can open the right file without going back to the preface. This also follows the BMAD rule to link visual references inline at the relevant section. 0 words. |
| structure | §Component Patterns, Map frame row (40 words), together with the 900 px row of §Responsive & Platform. | CUT the first sentence, "Holds the title bar, the map face, the side column and the sheet foot." The anatomy belongs to DESIGN.md › Components › Map frame. Keep the reading order in this row, and point the Responsive cell to it: "One column: headline, login, chart, readout, legend" → "One column, in the Map frame reading order". QUESTION: DESIGN.md › Layout & Spacing starts the same order with "title bar". Confirm which order is meant, so the surviving copy is right. | **S-E4.** The 900 px reading order appears twice in this spine and once in DESIGN.md, and the copies have already drifted apart. One source of truth fixes that. −13 words. |
| structure | §Information Architecture, the two ASCII wireframes (388 words, 11% of the document). | PRESERVE | **S-E5.** This is the largest block and the most tempting cut. It is also the only visual reference for Produktside and Samlet bestillingsoversikt, both spine-only, and it is where the decision strip's content is defined. Visual aids serve human readers. 0 words. |

**Candidate App table for S-E1.** Values come from the current table. Ranges marked [confirm] are inferred.

| Width | App |
|---|---|
| 1366 px and above | Rail 248 px. On Produktside the decision strip is above the fold |
| 1181–1365 px [confirm] | Rail 248 px [confirm]. No horizontal page scroll (NFR-6) |
| 1024–1180 px [confirm] | Rail 208 px; mini legend hidden [confirm that the legend rule starts here]. No horizontal page scroll (NFR-6) |
| 961–1023 px | Rail 208 px; the table can scroll inside its frame |
| 960 px and below | The rail becomes a top bar |
| 700 px and below [confirm] | Charts switch to their mobile variants (if this applies to Produktside too) |
| 640 px and below | Product rows become cards, the filter becomes 2 × 2, body text 16 px |

**Structure summary.** There are seven recommendations: two for DESIGN.md and five for EXPERIENCE.md, of which two are QUESTIONs and one is a PRESERVE.

- **DESIGN.md:** +5 words if all are accepted (+0.2% of 2,758).
- **EXPERIENCE.md:** about +62 words if all are accepted (+1.7% of 3,605). That is about +60 for the two definitions, an estimated +15 for the App rows, and −13 for the duplicate.

No length target was given. Nothing is lost in comprehension: the only cut removes a duplicate of DESIGN.md › Components › Map frame.

## Prose lens

**Voice, and the choices kept as they are.** Both spines use terse, declarative, present-tense US English in the form of contract rules, and their table cells are fragments. The following are deliberate choices, and no row below touches them:

- Norwegian UI strings in «…».
- Norwegian glossary labels used as names for surfaces and components (Produktoversikt, Produktside, Tegnforklaring, Varsel, Merknad, Forklaring, Bestill snart). The PRD glossary binds both languages, so "product screen", "explanation", "safety margin", "answer key" and "latest valid week" are correct as written.
- Straight quotes for rejected or English strings ("Kjøp 11 nå!", "AI-powered").
- Requirement IDs and MoSCoW markers (Should, Could) in parentheses, and `{path.to.token}` references.
- DESIGN.md's orienteering vocabulary (neatline, controls, legs, finish, overprint, map face, ground). It is the brand voice the spec allows in DESIGN.md.
- «Show the working», which is a PRODUCT.md principle name.
- The protagonist named in every Flow 1 step.
- The Flow 1 heading, which is the PRD's verbatim UJ-1 name, so its trailing period stays.
- The spine headings (Title Case, "&", spaced em dashes), which come from the BMAD template.

No structure row cuts a passage that a prose fix touches. P-D4 applies only if S-D2 is rejected.

### DESIGN.md

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| prose | There is one family, **Albert Sans** (SIL Open Font License), with weights 400, 500, 600 and 700. | There is one brand typeface, **Albert Sans** (SIL Open Font License), with weights 400, 500, 600 and 700. | **P-D1.** The approved `{typography.code}` token uses the system monospace, so "one family" is no longer true. "Brand" matches that row's "not a brand face". Typography intro. |
| prose | The landing page (Persuade) carries the full map sheet<br>The app screens (Operate) take only four things from the world: | The landing page (Impeccable's Persuade mode) carries the full map sheet<br>The app screens (Operate mode) take only four contributions from the map: | **P-D2.** "Persuade", "Operate" and "the world" are Impeccable process terms that a builder or examiner can't decode. "Four contributions" ties this sentence to the Do's and Don'ts row "the four contributions in the app". Brand & Style ¶2. |
| prose | - **No horizontal scroll from 1024 px** (NFR-6). The breakpoints are in EXPERIENCE.md. | - **No horizontal scroll from 1024 px upward** (NFR-6). The full breakpoint table is in EXPERIENCE.md, Responsive & Platform. | **P-D3.** DESIGN.md states several breakpoints itself (760 px high, 900 px, 960 px, 700 px, 640 px), so the old pointer misleads. "Upward" restores NFR-6's "from 1024 pixels wide upwards". Layout & Spacing. |
| prose | Markers: stockout weeks are ink × over a 45° hatch with a dotted outline. An unusual week is a white triangle with an ink outline. A level shift is a filled ink diamond.<br>Labels use `{typography.chart-label}`, and the calculation weeks are bold `{colors.magenta-ink}`. | Markers: a stockout week is an ink × over a 45° hatch with a dotted outline, an unusual week is a white triangle with an ink outline, and a level shift is a filled ink diamond.<br>Labels use `{typography.chart-label}`, and calculation-week labels are bold `{colors.magenta-ink}`. | **P-D4.** Apply only if S-D2 is rejected, because S-D2 already contains both fixes. Parallel definitions make the scope of "Markers:" clear. "The calculation weeks are bold" clashes with "Calculation weeks are magenta rings" and seems to mean their labels; confirm. Components › Course chart. |
| prose | Inputs, buttons, calculation lines and the settings switch use `{rounded.sm}`. | Consider: "Inputs, buttons, calculation lines and the segmented control use `{rounded.sm}`."? | **P-D5.** No component is named "settings switch". If it means the Segmented control (the landing safety-margin try-out is one), use that name so the radius lands on the right component. Shapes › Corners. |
| prose | Use magenta for decoration, headings or charts other than the course<br>or use ruled paper as a table | Consider: "Use magenta for decoration, headings or chart marks other than the course"?<br>Consider: "or style a table as ruled paper"? | **P-D6.** There is only one chart, so "charts other than the course" reads oddly, and "chart marks" matches Tegnforklaring. "Use ruled paper as a table" is unclear; confirm the intent before rewording it. Do's and Don'ts, rows 1 and 8. |
| prose | Red appears nowhere else except the login error. | Elsewhere, red appears only in the login error. | **P-D7.** This removes the doubled "nowhere else except". Also consider whether the sentence should cover the Text field error state. Components › Text field gives that state a `{colors.trust-low}` border, and EXPERIENCE.md uses text fields for settings and adjusted quantities, so the two lines can read as conflicting. Colors › Confidence colors. |

### EXPERIENCE.md

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| prose | In the overview it is shown once for the whole group. | In Produktoversikt it is shown once for the whole group. | **P-E1.** "The overview" could also mean Samlet bestillingsoversikt, and the glossary allows no synonyms for surface names. State Patterns › Stock covers next week. |
| prose | A Norwegian «not found» message with a link to Produktoversikt | Consider: "A Norwegian «ikke funnet» message with a link to Produktoversikt", which matches State Patterns › Not found? | **P-E2.** Everywhere else, «…» marks a verbatim Norwegian string, so an English gloss inside guillemets could ship as UI text. IA › Ikke funnet. |
| prose | the customer number kept and the password cleared. See the internal note. | the customer number kept and the password cleared. See [the internal note](mockups/designnotat-tilstander.html). | **P-E3.** "The internal note" has no antecedent in State Patterns, so a reader who jumps straight to this row needs the link. State Patterns › Login error. |
| prose | **Charts:** each chart has a short summary (`<title>` and `<desc>`) and a value table. | **Charts:** each chart has a short summary (`<title>` and `<desc>`) and a data table. | **P-E4.** The component is the Data table toggle, and the Course chart row says "the data table". "Value table" is a third name for the same thing. Accessibility Floor. |
| prose | **Motion:** respect `prefers-reduced-motion`. The one motion (the course drawing in) is skipped. | **Motion:** respect `prefers-reduced-motion`. When reduced motion is requested, the one motion (the course drawing in) is skipped. | **P-E5.** As written, the animation reads as always skipped, because the condition is only implied. Accessibility Floor. |
| prose | Diamond markers. With the Should text: «Etterspørselen ser ut til å ha endret nivå.» (FR-17). | Diamond markers. The text «Etterspørselen ser ut til å ha endret nivå.» is added when that Should item is built (FR-17). | **P-E6.** "With the Should text" is compressed. The revision reuses the Scenario strip row's own phrasing and leaves the Norwegian string unchanged. State Patterns › Level shift. |
| prose | A post form with Kundenummer and Passord.<br>Post, redirect, get: reloading or going back repeats nothing (NFR-10). | A POST form with Kundenummer and Passord.<br>Post/Redirect/Get: reloading or going back repeats nothing (NFR-10). | **P-E7.** HTTP methods are capitalized, as "GET" already is elsewhere. Post/Redirect/Get is the pattern's standard name, so a builder can look it up. Component Patterns › Login panel; State Patterns › Resubmit or back. |
| prose | drag and drop (the data is read-only, and nothing may suggest that dragging changes an order);<br>dialogs for settings;<br>auto-refresh and infinite scroll;<br>confirmations that disappear on a timer;<br>any action that places an order. | The same five items with no end punctuation: drop the four semicolons and the final period. | **P-E8.** Microsoft style puts no semicolons or conjunctions at the end of list items, and fragments take no end punctuation. Interaction Primitives › Banned. |
| prose | **Lifted from the orienteering map (ISOM):**<br>**Lifted from the declined catalog challengers:** | **Lifted from the orienteering map (ISOM, the International Specification for Orienteering Maps):**<br>Consider: "**Lifted from the declined catalog challengers (alternative design concepts, named in parentheses):**"? | **P-E9.** Spell out an unfamiliar acronym on first use. "Catalog challengers" is design-process jargon, and the names in parentheses (drum machine, drawcord cape and so on) only make sense once that is explained. Inspiration & Anti-patterns. |
| prose | - Where `PRODUCT.md` and this DESIGN.md live for Impeccable during the build (DR-2) is decided with the repository layout in the architecture step.<br>run on the real build (direction contract, FINISH line). | - The architecture step decides, together with the repository layout, where `PRODUCT.md` and DESIGN.md live for Impeccable during the build (DR-2).<br>run on the real build, as the FINISH line of the direction contract requires (surface briefs in `.impeccable/surfaces/`). | **P-E10.** "This DESIGN.md" is wrong inside EXPERIENCE.md, and the long subject clause is passive. The bare parenthetical names terms that are defined only in the surface briefs. Open items. |
| prose | Closed by default and opened with the keyboard. | Consider: "Closed by default and keyboard operable."? | **P-E11.** As written, it can read as keyboard-only. "Keyboard operable" is the Segmented control row's term. Component Patterns › Data table toggle. |

### Both documents

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| prose | A mobile variant under 700 px (DESIGN.md › Course chart)<br>Under 640 px each row becomes a bordered card (DESIGN.md › Product table)<br>Under 640 px each row is a card. (EXPERIENCE.md › Product table)<br>the product cards under 640 px keep the reading order (EXPERIENCE.md › Accessibility Floor)<br>On phones the filter becomes a 2 × 2 grid. (DESIGN.md › Segmented control)<br>(framed on phones) (DESIGN.md › Login panel) | Consider one boundary form, the one the breakpoint table uses:<br>A mobile variant at 700 px and below<br>At 640 px and below each row becomes a bordered card<br>At 640 px and below each row is a card.<br>the product cards at 640 px and below keep the reading order<br>At 640 px and below the filter becomes a 2 × 2 grid.<br>For the login panel, name the width that "on phones" means. | **P-B1.** "Under 640 px" excludes 640, while "640 px and below" includes it, so builders would write different media queries from the two spines. "On phones" names no width at all. All breakpoint values stay. The approved Typography rows that say "on phones" are not flagged here. |
| prose | in magenta-ink 600 (DESIGN.md › Data table toggle)<br>a visible 3 px magenta-ink focus ring (EXPERIENCE.md › Accessibility Floor)<br>The values are 1.375 rem 700, and Normal is on (DESIGN.md › Scenario strip)<br>«Prognose» in Albert Sans 700, beside (DESIGN.md › Wordmark) | in `{colors.magenta-ink}` 600<br>a visible 3 px `{colors.magenta-ink}` focus ring<br>Consider: "The values are in `{typography.title-large}`, and Normal is on"?<br>Consider: "«Prognose» in `{typography.title-large}`, beside"? | **P-B2.** A token name written as a plain word doesn't resolve as a reference, and EXPERIENCE.md should use `{path.to.token}`. The approved `{typography.title-large}` row covers "the wordmark and the scenario values", so pointing these older Components rows at it keeps one source. The values are identical. |
| prose | is the shell colour:<br>a black centre dot<br>in the trust colour (<br>Neither has a coloured side border.<br>apart by colour alone<br>**Status beyond colour:** status never relies on colour.<br>so they survive greyscale | is the shell color:<br>a black center dot<br>in the trust color (<br>Neither has a colored side border.<br>apart by color alone<br>**Status beyond color:** status never relies on color.<br>so they survive grayscale | **P-B3.** The spines are in US English (Colors, labeled, behavioral) and the style guide is Microsoft. Seven passages still use British spelling: DESIGN.md Colors › Vegetation green, Components › Wordmark, › Confidence label and › Varsel and Merknad, and Do's and Don'ts row 2; EXPERIENCE.md Accessibility Floor, and Inspiration & Anti-patterns. |
| prose | type, palette, density, and one signature move (DESIGN.md › Brand & Style ¶2) | Decide the series-comma rule. Microsoft style puts a comma before the final "and" or "or" in every series. The spines omit it in about 48 short series and use it in about 8 long ones. To follow Microsoft, add it throughout. If omitting it is deliberate (the PRD does the same), keep that and make this short series match: "type, palette, density and one signature move". | **P-B4.** Low comprehension impact. It is listed because the configured guide conflicts with a consistent house habit. |

**DESIGN.md: 7 further minor fixes.**

1. "- **Product screen.** At 1366 × 768" → "- **Produktside.** At 1366 × 768". Both names are binding; this one matches EXPERIENCE.md's surface names.
2. "Nothing is decorative that a reader could mistake for data." → "No decoration could be mistaken for data."
3. "a 1200 px wrap" → Consider: "a container at most 1200 px wide"? (Only if 1200 px is a maximum.)
4. "The numbers 1 to 3 in the calculation steps are course controls and state the calculation order." → "The numbers 1 to 3 in the calculation steps are not section numbers: they are course controls that state the calculation order."
5. "A list of 26 × 18 px symbols" → "The legend: a list of 26 × 18 px symbols". This ties the body's word "legend" to Tegnforklaring.
6. "half for middels" → "half-filled for middels".
7. In Brand & Style ¶4 and the EXPERIENCE.md preface, replace the raw file paths used as link text with descriptive text, for example "[landing page mockup](mockups/key-landing.html)". Microsoft style asks for descriptive link text.

**EXPERIENCE.md: 6 further minor fixes.**

1. "is shown struck and labeled as not in use" → "is shown struck through and labeled as not in use".
2. "the old and new value, and the affected value" → "the old and new values, and the affected value".
3. "(role alert)" → "(`role="alert"`)".
4. "Behind each one Mounia saw how it was calculated" → "Behind each one, Mounia has seen how it was calculated".
5. "checks the new quantity against the rule." → Consider naming the rule, for example "against the order rule (R-8)"?
6. "which owns how it looks" → "which owns how Prognose looks".

**Prose count:** 22 rows (7 for DESIGN.md, 11 for EXPERIENCE.md, 4 for both) plus 13 minor fixes.

**Not flagged on purpose:**

- The mockup paragraph and the "spines win on any conflict" sentence appear in both files. Each spine is read on its own, and the coverage check states the rule in both on purpose.
- Do's and Don'ts and the EXPERIENCE.md preface recap rules from the body. These summaries help human readers.
- The approved typography tokens, `rounded.xs` and the Shapes focus-ring phrase. S-D1 only moves rows and leaves their text untouched.

**Outside these lenses (not an editorial finding):** Accessibility Floor gives each chart `<title>` and `<desc>`, which are SVG elements, but Foundation draws the charts with Chart.js, which renders to a canvas. That is for the architecture step to settle.
