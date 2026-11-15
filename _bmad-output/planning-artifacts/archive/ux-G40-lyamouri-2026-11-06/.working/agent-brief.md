# Shared brief for the ten direction agents (Prognose UX, 2026-11-06)

You build ONE design concept for Prognose: the landing page (the public entry surface, which holds the working login) as one self-contained HTML mockup, plus one concept card in Markdown. Your world is assigned in your prompt; this file holds the rules all ten agents share. Nine other agents build other worlds at the same time, and your concept must stay clearly different from theirs (section 7).

Project root: the `G40-lyamouri` folder. Paths below are relative to it. Your output folder: `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/.working/`.

## 1. Hard rules

1. **Stay inside the project folder.** Do not read, list, search or write anything outside the project folder: no home folder, no `/tmp`, no system temp, no other projects. This is the user's privacy rule.
2. **No browsers, no installs, no network.** Do not start Chrome, Edge, Safari or any headless browser, and do not try to take screenshots (a test showed Chrome writes crash data outside the project). Do not install anything (npm, pip, brew). Do not use curl, WebFetch or WebSearch. Your HTML may link Google Fonts stylesheets; only the user's browser fetches them later.
3. **No paid services or API keys**, and no image generation.
4. **Write only your own files:** your HTML, your concept card, and scratch files inside `.npm-cache/agents/<your-slug>/` (create it). Do not edit any other project file, and do not run git commands.
5. **No personal names** in the mockup. Use roles («innkjøpsansvarlig») and «Testbedrift A».
6. **No invented claims.** No customers, testimonials, user logos, press, prices, accuracy figures, hosting claims or "AI-powered" language. Demo data is synthetic and is labeled «Syntetiske data» where a visitor could mistake it for real data.
7. **Impeccable commands** run from the project root with telemetry and update checks off:
   `DO_NOT_TRACK=1 IMPECCABLE_NO_TELEMETRY=1 IMPECCABLE_NO_UPDATE_CHECK=1 .claude/skills/impeccable/scripts/impeccable <verb> ...`
   Do not run `concept-seed`, `serve-question`, `live` or `generate-image`.
8. **Budget:** build, run one self-check pass, apply the fixes in one batch, run the detector a final time, then stop. No further revision rounds.

## 2. Read before you design

1. `PRODUCT.md`: product truth.
2. `.claude/skills/impeccable/SKILL.md`: principles and modes. The landing page is **Persuade**; the app glimpse inside it is **Operate** (precision and restraint).
3. `.claude/skills/impeccable/reference/craft-floor.md`: read it immediately before you write UI. Its bans are binding.
4. `.claude/skills/impeccable/reference/mode-operate.md`, for the app-glimpse section.
5. Optional: `.claude/skills/impeccable/reference/typeset.md`, `colorize.md`, `layout.md`.
6. The PRD as needed: `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md`, especially §2.3 (journey UJ-1), §3 (glossary), §4.4 to §4.8 (screens and texts) and §6.1 (NFRs). The research reports are not needed.
7. `.working/direction-derivation.md`: how the ten worlds were derived.

## 3. Product facts the mockup must respect

- **Language:** Norwegian bokmål in all UI copy (`<html lang="nb">`). Use æ, ø and å. Decimal comma (14,3), the true minus sign − (U+2212) in calculations, a no-break space before % (10&nbsp;%), and «» quotes.
- **Binding labels (no synonyms):** Bedrift, Kundenummer, Produkt, Varenummer, Salgshistorikk, Lagerbeholdning, Uke, Siste registrerte uke, Siste 12 uker, Utsolgt uke, Gyldig uke, Uvanlig uke, Nytt nivå, Uke brukt i beregningen, Prognosemetode (Glidende gjennomsnitt, Eksponentiell glatting), Grunnprognose, De neste tre ukene, Ukeprognose, Scenario (normal, optimistisk, pessimistisk), Scenarioprosent, Sikkerhetsmargin, Foreslått bestillingsmengde, Justert bestillingsmengde, Uker dekning, Bestill snart, Samlet bestillingsoversikt, «Foreslått», «Justert av deg», Tillitsmerke (høy, middels, lav), Varsel, Merknad, Forklaring, Produktoversikt, Produktside, Prognoseutregning, Utregning av bestillingsmengde, Innstillinger.
- **Fixed strings, verbatim when shown:**
  - «Feil kundenummer eller passord.»
  - «Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong.»
  - «Scenarioene viser hva som skjer hvis salget blir 10 % høyere eller lavere. De er ikke sannsynligheter.»
  - «Tallene er avrundet for visning.»
  - «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.»
  - «Endringen gjelder alle produkter i bedriften.»
  - «Lagerbeholdningen dekker forventet behov neste uke.»
  - «Etterspørselen ser ut til å ha endret nivå.»
- **Login (FR-1):** fields «Kundenummer» and «Passord», each with a visible label, and the button «Logg inn». Add a help line such as «Innloggingen for de to testbedriftene står i README-filen.» Never show a password. Version 1 has **no** «Glemt passord?», no registration and no account creation; do not add them.
- **The principle:** Prognose recommends; the purchasing manager decides. Prognose places no orders. The explanation is built from fixed templates, and no number comes from AI (a true claim you may state).
- **Product screen (FR-25):** at 1366 × 768 the suggested order quantity, the confidence label and the active warnings are visible without scrolling. The explanation sits under the heading «Forklaring», below the calculated numbers (FR-27).
- **Chart (NFR-7, NFR-11):** stockout weeks, unusual weeks and level-shift weeks each have their own marker that differs by **shape**, not only by color, and a legend explains them. The chart has a text alternative: a short summary and a value table (for example inside `<details>`).
- **Screen size (NFR-6):** desktop browser; no horizontal page scrolling from 1024 px wide; narrower windows stay readable with nothing overlapping or cut off. No mobile design is required.
- **Horizon labels:** show the forecast horizon as «De neste tre ukene» with both the horizon number and the calendar week, for example «Uke 1 · uke 46», so the fixed FR-7 note stays understandable.

## 4. Demo content kit (synthetic; use these numbers exactly)

Every number below follows the PRD rules (R-3, R-7 to R-12, R-16). If you need more data, keep it consistent with the rules.

- **Company:** «Testbedrift A», 30 products (Syntetiske data). **Siste registrerte uke:** uke 45 (2026). **De neste tre ukene:** uke 46, 47 and 48. The order is for next week, uke 46.
- **Settings in use:** Prognosemetode glidende gjennomsnitt, 3 uker · Scenarioprosent 10 % · Sikkerhetsmargin 10 % · Uvanlige uker tatt med · Sesongjustering av.

**Hero product: 10234 «Treskrue 4 × 40 mm, 200 stk»**
- Salgshistorikk 104 uker, 102 gyldige uker. Siste 12 uker (uke 34 to 45): 13, 14, S, S, 12, 31, 14, 13, 15, 16, 12, 15 (S = utsolgt uke). Uke 39 (31 stk) is an uvanlig uke: its sammenligningsgrunnlag is 13 (median of uke 38, 35 and 34), and 31 is more than 2 × 13. For older weeks, use plausible values between 11 and 16.
- Lagerbeholdning 5.
- Prognoseutregning: «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3». Uker brukt i beregningen: uke 43, 44 og 45. Uker holdt utenfor: uke 36 og 37 (utsolgt uke).
- Ukeprognose uke 46, 47 and 48: 14,3 each, with the FR-7 note.
- Scenarier for uke 46: pessimistisk 12,9 · normal 14,3 · optimistisk 15,8.
- Utregning av bestillingsmengde: «Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → foreslått bestillingsmengde 11», followed by «Tallene er avrundet for visning.» and the safety-margin text.
- Uker dekning 0,3. Status: Bestill snart.
- Tillitsmerke middels: «Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene.»
- Varsler: 2 utsolgte uker de siste 12 ukene (uke 36 og 37); 1 uvanlig uke de siste 12 ukene (uke 39: 31 stk).
- Forklaring (template text; every number in it is also shown among the calculated numbers): «Prognosen bygger på glidende gjennomsnitt over 3 uker: uke 43, 44 og 45 med salg 16, 12 og 15. Uke 36 og 37 er holdt utenfor fordi varen var utsolgt. Uke 39 er en uvanlig uke med 31 solgte; uvanlige uker er tatt med i beregningen. Tillitsmerket er middels fordi det er 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene. Foreslått bestillingsmengde er 11: prognose 14,3 pluss sikkerhetsmargin 10 % (1,4) minus lager 5.»
- **Settings change, for a signature interaction (FR-21):** Sikkerhetsmargin 10 % → 20 % gives «Prognose 14,3 + sikkerhetsmargin 20 % (2,9) − lager 5 = 12,20 → foreslått bestillingsmengde 13» and the confirmation «Foreslått bestillingsmengde: 11 → 13», always with «Endringen gjelder alle produkter i bedriften.»
- **Order quantity per scenario (FR-13, a Should item):** optimistisk 13, pessimistisk 10. If you show it, say in the concept card that it depends on a Should item.

**Second chart product: 10590 «Strøsand 25 kg»** (level shift). Siste 12 uker: 19, 21, 20, 22, 21, 20, 22, 21, 22, 50, 52, 51; uke 43, 44 og 45 are a nytt nivå. Grunnprognose (50 + 52 + 51) / 3 = 51,0, lager 20, foreslått 37 («… − lager 20 = 36,10 → foreslått bestillingsmengde 37»), uker dekning 0,4. «Middels: nytt nivå de siste 12 ukene.» Warning text «Etterspørselen ser ut til å ha endret nivå.»

**Produktoversikt rows, in the R-12 order:**

| Varenummer | Produkt | Lagerbeholdning | Ukeprognose (uke 46) | Foreslått | Uker dekning | Tillitsmerke | Status |
|---|---|---|---|---|---|---|---|
| 10871 | Malertape 25 mm | 0 | 10,0 | 11 | 0,0 | høy | Bestill snart |
| 10872 | Malertape 50 mm | 0 | 20,0 | 22 | 0,0 | høy | Bestill snart |
| 10234 | Treskrue 4 × 40 mm, 200 stk | 5 | 14,3 | 11 | 0,3 | middels | Bestill snart |
| 10590 | Strøsand 25 kg | 20 | 51,0 | 37 | 0,4 | middels | Bestill snart |
| 11502 | Arbeidshansker vinter, str. L | 12 | «Ingen prognose: for lite data (2 gyldige uker)» | – | – | lav | – |
| 10110 | Spiker 75 mm, 2,5 kg | 150 | 100,0 | 0 | 1,5 | høy | «Lagerbeholdningen dekker forventet behov neste uke.» |
| 10345 | Bits PH2, 10 stk | 40 | 12,0 | 0 | 3,3 | høy | – |

The sort is order-soon products by weeks of cover (lowest first, ties by product number), then products without a forecast, then the rest by product number. Spiker's line: «Prognose 100,0 + sikkerhetsmargin 10 % (10,0) − lager 150 = −40,00 → foreslått bestillingsmengde 0 (lageret dekker behovet)». Reasons: «Høy: 104 uker med salgshistorikk, minst 100 gyldige uker og ingen aktive varsler.» and «Lav: ingen prognose (2 gyldige uker).»

**Samlet bestillingsoversikt for uke 46 (a Should item):** 10871 11 «Foreslått» · 10872 22 «Foreslått» · 10234 15 «Justert av deg» (foreslått 11) · 10590 37 «Foreslått» · 11502 10 «Justert av deg» (ingen prognose) · 10110 0 «Foreslått» · 10345 0 «Foreslått».

## 5. Page anatomy (all required)

The HTML file is the page itself, full-bleed, with no fake browser frame. Design it at 1440 px wide. It must also work at 1366 × 768 and at 1024 px wide.

1. **First viewport (a thesis, not a header):** the wordmark «Prognose» (type only, or a small authored SVG mark), a hook that lands in one line, the **working login form**, and a demonstration of the mechanism (the number to order, how it was calculated, and whether to trust it). At 1366 × 768 the login form and the demonstration are visible without scrolling.
2. **How Prognose calculates:** the forecast calculation line, the order calculation line, the scenarios with the FR-10 sentence, the FR-7 note, the rounding note and the safety-margin text.
3. **When not to trust the number:** the three confidence labels with reasons, the difference between Varsel and Merknad, and the chart with shape-coded markers, a legend and a text alternative.
4. **You decide:** «Foreslått» against «Justert av deg»; Prognose places no orders.
5. **App glimpse:** the secondary screen named in your prompt, in Operate register: real labels, demo data, the confidence labels, and at least one state variant (a product without a forecast, the overstock 0 line, or the login error «Feil kundenummer eller passord.»).
6. **Prøv selv:** five or six short steps for the examiner that follow UJ-1 (log in as Testbedrift A, open the top product, read the warnings, change a setting, read the explanation, open the combined order overview).
7. **Footer:** true context only: «Kursprosjekt i IBE160 ved Høgskolen i Molde, høsten 2026», runs locally, synthetic data, places no orders.
8. **One signature interaction**, CSS-only and keyboard operable (radio inputs with `:checked` or `:has()`, `<details>`, `:target`), for example the settings change in section 4. It must not be hover-only.

Also include a few anchor links (for example «Slik regner Prognose», «Tillit og varsler», «Prøv selv», «Logg inn») and the navigation pattern from your prompt.

## 6. Impeccable rules for this surface

### MODE RULES (persuade), verbatim from the roll

DIRECTIONS
When a catalog world's source is itself an interface language, the surface may carry its native grammar across navigation, content, controls, and states, within the platform conventions a native app keeps.

For **Persuade**, the opening must make the offer intelligible and desirable, expose a clear action, and demonstrate something only this product can prove. The action is the one the category's visitors came to take, in its working form: an airline's route-and-dates search, a clinic's open appointment slots, a store's add to cart. A decorative link pointing at it elsewhere does not count. Conversion lives inside the form's own vocabulary: a hook that lands in one line, a visible primary action, a legible reading order. A committed form that hides the offer or the action has not finished translating. For **Experience**, the work itself leads from the first viewport.

COMPS (they govern composition here too, even though no images are made)
The world may be the carrier of the page, never a picture of it: a facade, a shutter or a book can be what the page is built on, while a viewport painted whole as a facade, a book cover or a travel poster, with no working parts in it, is a picture of the world, not its website. Material coverage is wanted: the world's material is the ground and the major surfaces, its type sets the headlines, and a world reduced to an accent on a neutral template is the category default with a sticker on it. Coverage is not performance: how many regions act out the concept is limited by the depth rule in visualize.md, and the rest stay in the world's material without performing it. Both ends erase the direction: the painted poster, and the generic product page (a headline over subcopy and a button, a row of equal cards below). The dealt composition sets the skeleton, and the compositions you write for comps two and three answer to the same test: a split hero (copy on one side, the product on the other, a badge row under it) or a centred headline over a row of cards is the template whatever world paints it.

The world carries the page's parts and never absorbs them, so wherever it puts one, the page still works as a page: navigation set into a facade reads as links, copy on a shutter as set text a visitor reads, an action on a door plaque as plainly clickable, text reads against whatever sits behind it, the sections keep a steady vertical rhythm, the primary action is unmistakable, and the section below starts as a section rather than more painting. Fix a poster by making its parts work where the world put them, never by moving them into a standard layout on the world's colour: a cover that becomes copy beside a device on marigold has lost the cover.

When the world is an object, the page is that one object seen once, at one scale and from one point of view, and the object keeps its real form: a book opens to two pages on one gutter, never a third panel, and a spine that carries the navigation belongs to the book on the page, never a second book beside it. More content goes on the object's own surfaces or on the next spread below, never on extra copies or impossible folds.

### From new-work (essentials)

- Pick a color strategy before colors: Restrained, Committed (one saturated color carries 30 to 60% of the surface), Full palette (3 to 4 named roles) or Drenched (the surface is the color). Color commits at page scale. Light or dark comes from one sentence of physical scene, never from the category.
- Choose faces like objects from the subject's world. Do not use: Fraunces, Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk, Space Mono, IBM Plex, Inter, Roboto, Geist, DM Sans, DM Serif, Outfit, Plus Jakarta Sans, Instrument Sans. Use the face assigned in your prompt (section 7).
- Calibration: avoid the AI default looks unless your world truly is one: a warm cream ground with a serif display and a terracotta or red accent; near-black with one neon accent and glowing edges; broadsheet hairlines with an italic display serif and tracked mono labels; flat ink with black boxes, hard offset shadows and heavy condensed type.
- The first viewport is a thesis: demonstrate the mechanism at once, at the scale the form has in life. Prove, don't claim: show the subject doing its job with real demo content. Author the assets (marks, charts, labels) at full fidelity; never fill a gap with gradients, glass or generic icon tiles. Pace the scroll: vary density and quiet in one grammar, one spacing rhythm, more space above a heading than below it, and end on a real close. Give motion one authored moment, from an already-visible default.

### Craft floor (read the file; these are bans)

- No kicker or eyebrow label above a heading (a ban, never earned back). No section numbers like 01 / 02 / 03.
- No same-size icon-plus-heading-plus-text cards as the page structure, and no nested cards. Avoid the hero-metric template (big number, small label, supporting stats); the order number lives inside its calculation, never as a lone stat.
- No gradient text, no decorative glass or blur, no glow (zero-offset colored shadows), no colored `border-left` or `border-right` over 1 px on cards, list items or alerts, no hard offset shadows, no emoji or Unicode glyphs as icons (draw SVG icons in one consistent stroke), no monospace as a "technical" costume (mono only for figures and calculations, if at all).
- Theme the browser surfaces: `::selection`, `caret-color`, focus rings, `accent-color`, link underline offset, and tabular numerals (`font-variant-numeric: tabular-nums`) in all data.
- States: hover, focus, disabled, error and empty, where they apply.
- Copy: the product's own words. Controls name their action. No marketing buzzwords (sømløs, kraftig, revolusjonerende, smart, effektiviser, KI-drevet, streamline, empower and similar).

## 7. Distinctness: the ten concepts and their faces

Use only your own face(s). Do not take another concept's face, ground or signature.

| # | Concept | World | Face(s) | Ground and strategy |
|---|---|---|---|---|
| K01 | O-kartet | Orienteering map | Albert Sans | Cool map white with yellow and green fields; magenta overprint; full palette, light |
| K02 | Ukeplanen | Week-number planner | Archivo (width axis) | Cool white with a committed almanac red; light |
| K03 | Lagerkortet | Visible-edge stock card file | Libre Franklin + Courier Prime | Grey-green steel drawer with manila cards; committed, light |
| K04 | Værmeldingen | Meteogram | Schibsted Grotesk | Pale sky field with white panels; full palette, light |
| K05 | Hyllekanten | Shelf edge and labels | Chivo + Chivo Mono | Galvanized steel grey with safety-yellow labels; drenched, mid-tone |
| K06 | Skiltet | Road signs at night | Overpass | Dark asphalt with reflective sign colors; full palette, dark |
| K07 | Regnestrimmelen | Tape and carbon order pad | Doto (large numerals only) + Red Hat Text / Red Hat Mono | Pink carbon-copy paper with carbon-blue ink and white tape; drenched, light |
| K08 | Planleggingstavla | T-card planning board | Familjen Grotesk | Anodized aluminium rack with colored T-cards; full palette, light |
| K09 | Flisene | Metro tiles (catalog challenger, fused) | Commissioner | Pure black with flat tiles; one accent that is not cyan, magenta or purple; committed, dark |
| K10 | Standarden | Category standard, played straight | Hanken Grotesk | White and neutral greys with one deep green accent; restrained, light |

## 8. HTML constraints

- One self-contained `.html` file with inline `<style>`. **No JavaScript.** No external images; draw charts, marks and icons as inline SVG.
- Google Fonts: one `<link>` (with preconnect) for your assigned faces and only the weights you use, `display=swap`, and a fallback stack.
- `<!doctype html>`, `<html lang="nb">`, `<meta charset="utf-8">`, the viewport meta, and `<title>Prognose · <concept name> (designkonsept)</title>`.
- Layout: fluid grids (`minmax`, `clamp`), no fixed widths over 1024 px without wrapping, no horizontal page scroll from 1024 px, and a single column below about 900 px.
- Accessibility: WCAG 2.2 AA contrast for all text (4.5:1 body, 3:1 large text and UI components); visible, themed focus styles; a visible `<label>` for every input; heading levels in order; the chart SVG with `role="img"`, a `<title>` or `aria-label`, and the table alternative; `prefers-reduced-motion` respected; content visible by default.
- In `<style>`, one comment block lists the palette (hex values and roles). Do **not** put the direction contract or concept rationale in the HTML (no comments, hidden DOM or data attributes): it is development-only and lives in the concept card.

## 9. Verification without a browser

1. **Contrast:** write a small python3 script in `.npm-cache/agents/<slug>/` that computes the WCAG ratio for every text and background pair you use, and fix any failure.
2. **Detector:** `DO_NOT_TRACK=1 IMPECCABLE_NO_TELEMETRY=1 IMPECCABLE_NO_UPDATE_CHECK=1 .claude/skills/impeccable/scripts/impeccable detect --json --no-design-system <your html>` (exit 2 means findings). Fix what is real. When a finding is a deliberate exception you can justify, keep it, say why in the card, and add no ignore config. (`--no-design-system` is needed because DESIGN.md is still empty on purpose.)
3. **Self-review against the code:** walk the page anatomy and the craft floor; reason through widths at 1024, 1366 and 1440 px for overflow; check that the HTML is well-formed, the `<label>` `for` attributes match, the anchors resolve, and the radio-group interaction works by keyboard.
4. Then one batch of fixes and a final detector run. Stop there.

## 10. Concept card template (English; Norwegian UI terms quoted)

Write it as `direction-NN-<slug>.md` beside your HTML, with these sections in this order:

```
# KNN · <Name> (<short English gloss>)

**Kind:** <assigned | pick | grounded, position n | challenger (catalog id), verdict | canon> · **Mockup:** direction-NN-<slug>.html

## Design direction
Two or three sentences: the world, the thesis, why it fits Prognose.

## Color palette
Color strategy and the light or dark scene sentence, then a table: token | hex | role | contrast against its background.

## Typography
Faces (Google Fonts, license), roles (display, headings, body, figures), the size scale, numerals, and the note that the app self-hosts the fonts (NFR-1).

## Layout
Landing page: the first viewport at 1440 × 900, what fits at 1366 × 768, the section sequence, the grid, and behavior at 1024 px.
App: how the identity carries into the product overview and product screen, density, and what is above the fold.

## Navigation
Landing navigation, and the in-app pattern: where Produktoversikt, Samlet bestillingsoversikt, the company name and «Logg ut» live, how a product screen is opened and left, and the keyboard path.

## Rationale
Why it serves the purchasing manager and the examiner, with PRD references (for example FR-1, FR-12, FR-19, FR-21, FR-24, FR-25, FR-27, NFR-6, NFR-7, NFR-11).

## Signature interaction
What it is, how the mockup does it without JavaScript, and how the app would do it (a server round trip in Django).

## Implementation realism
Django templates, CSS and a vendored Chart.js: what is easy and what is hard, an effort estimate (small, medium or large), the chart markers through Chart.js `pointStyle` (for example `rect`, `crossRot`, `triangle`, `rectRot`), the fonts to self-host, and confirmation that no other JavaScript is needed.

## Direction contract (development only; never copied into HTML)
THESIS · OWN-WORLD · STORY · FIRST VIEWPORT · FORM (the form, its position on the ordered list or its catalog id, and `seed:aedd9cea56b9908b`) · FINISH: "unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance"

## Impeccable checks
Detector findings before and after (rule ids), the remaining findings with reasons, the craft-floor self-check, and the lowest contrast ratio with its pair.

## Honest risks
Two to four bullets.
```

## 11. What to return to the parent

Return only a compact summary of about 200 words: the two file paths; one line on the personality; the first viewport and the secondary screen depicted; 5 to 7 palette hex values with roles; the faces; the detector result (findings before and after, remaining); the lowest contrast ratio; the main risks; and anything you could not do. Do not paste HTML.
