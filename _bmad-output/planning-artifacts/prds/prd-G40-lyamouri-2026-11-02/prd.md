---
title: 'PRD: Prognose (G40-lyamouri)'
status: final
created: '2026-11-02'
updated: '2026-11-08'
---

# PRD: Prognose (G40-lyamouri)

**Version 1 at a glance**
- **Status:** see the frontmatter. The submission deadline is 1 December 2026 (DR-6).
- **Must (§8.1):** the weekly core flow in UJ-1: log in, see the product overview, open a product, see the forecast calculation, scenarios, suggested order quantity, warnings and confidence label, change a setting and see the result change, and read the template explanation.
- **Should (§8.2):** seasonal adjustment and the seasonal-pattern warning, order quantity per scenario, the overstock note, the level-shift warning text, the optional local language model, and adjusting order quantities with the combined order overview. These items are at risk before the deadline; their order is set in sprint planning (§10, question 1).
- **Could (§8.3):** settings per product, saving adjustments and approval, CSV export, the note that stock will not last through weeks 2 and 3, and forecast accuracy (MAE).
- **Done when:** the Must scope passes SM-1 and SM-3, and SM-2 and SM-9 hold on the final commit.
- **Where it runs:** locally from the README with SQLite, and as a published version on Vercel with PostgreSQL, from the same code (DR-10).
- **Where the complexity lies:** 17 deterministic rules (15 of them in the Must scope) checked by 30 reference examples (24 of them for the Must scope), two isolated companies with saved settings, and a guarded explanation layer, not user roles or integrations.

## 0. Document Purpose

This PRD defines what version 1 of Prognose must do. It is written for the project group, the teacher and examiner of IBE160, and the next BMAD steps (UX design, architecture, epics and stories), as well as for AI-assisted implementation with Claude Code.

**Where to find what**
- §1 Vision; §2 Target user, jobs to be done and the user journey UJ-1.
- §3 Glossary: a lookup table of binding terms and their Norwegian labels.
- §4 Features with functional requirements FR-1 to FR-36, each with a priority.
- §5 Calculation rules R-1 to R-17 and reference examples E1 to E30, the answer key for the tests.
- §6 Non-functional requirements (NFR), AI guardrails (AG) and delivery requirements (DR).
- §7 Non-goals; §8 MVP scope; §9 Success metrics (SM); §10 Open questions.
- §11 Assumptions and rule sources: every `[ASSUMPTION]` tag and every project-defined rule.
- §12 Change log for changes after approval.
- `addendum.md` (same folder): technology recommendation (§2), explanation layer (§3), rejected technology and AI alternatives (§4), evidence quality (§5), rule and priority rationale (§6), changes from the Product Brief (§7) and sources (§8).

**This PRD builds on** (and does not repeat):
- Product Brief: `_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/brief.md`
- Teacher feedback on the brief: `_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/tilbakemelding-product-brief.md`
- Brainstorm decisions and MoSCoW: `_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/brainstorm-intent.md`
- Research reports A to D: `_bmad-output/planning-artifacts/research/` (forecasting methods and data rules; safety stock and order quantity; technology stack; explanations without a paid API)

The review and reconciliation reports for this PRD (`review-*.md`, `reconcile-*.md`) and the decision log (`.memlog.md`) are in the same folder as this file.

**This PRD feeds:**
- The UX step, which delivers DESIGN.md and EXPERIENCE.md, with wireframes of the login page, the product overview, the product screen and the combined order overview.
- The architecture step, which decides the technology (NFR-9; `addendum.md` §2 and §3).
- The epics and stories, which take their acceptance criteria from the FR consequences and the reference examples.

## 1. Vision

Prognose is a web application that helps the purchasing manager of a small business decide how much to order of each product next week. It forecasts weekly demand from the company's own sales history with established, hand-checkable methods, shows normal, optimistic and pessimistic scenarios, and turns the normal forecast into a suggested order quantity: forecast plus safety margin minus stock on hand. Prognose recommends; the purchasing manager decides: every suggested order quantity is advice that the purchasing manager can accept or adjust, and the final purchasing decision always stays with them.

What sets Prognose apart from a spreadsheet or a large ERP system is transparency with built-in checks. Every number comes from deterministic rules that the user can see and check by hand, with settings the user can adjust. The system also says when a forecast should not be trusted: it leaves out stockout weeks, flags unusual sales, notices when demand moves to a new level, and gives each product a confidence label with a plain-language reason. Every product gets a plain-language explanation in Norwegian, built from fixed templates; an optional AI model that runs locally can rephrase it, but AI never produces the numbers.

The first version is a course project for IBE160, module 4.1 (Forecasting and Demand Management), at Høgskolen i Molde. It runs locally and as a published version on Vercel, with synthetic data and no paid services, so an examiner can install it from the README or open the published address, log in as a test company and check each forecast against a reference example. Later versions could feed sales and operations planning (S&OP) or master production scheduling (MPS), but that is outside version 1.

## 2. Target User

The primary user is the purchasing manager or inventory planner at a small business with about 10 to 50 products, who reviews forecasts and orders every week.

### 2.1 Jobs To Be Done

- Every week, decide how much to order of each of 10 to 50 products, so shelves do not run empty and stock does not pile up.
- See at a glance which products need ordering soon.
- Have a clear basis for each purchasing decision that I can understand and explain.
- Know when the data behind a forecast is too thin or distorted to trust.

### 2.2 Non-Users (v1)

- Large companies that need ERP or MRP planning, bills of materials or production planning.
- Anyone who wants to place real orders with suppliers from the system.
- Organizations that need several roles or approval steps: v1 has one role per company.

### 2.3 Key User Journeys

- **UJ-1. Mounia plans next week's purchases before the Monday meeting.**
  - **Persona + context:** Mounia is the purchasing manager at a small hardware store with about 30 products. Mounia orders from suppliers every week and has 20 minutes before the purchasing meeting.
  - **Entry state:** Not logged in. Mounia opens Prognose in the browser on the office PC and logs in with the company's customer number and password.
  - **Path:**
    1. Mounia sees the product overview: every product with its stock on hand, weeks of cover and confidence label, and the products with order-soon status at the top.
    2. Mounia opens a product that needs ordering and sees, on the product screen, a chart of the sales history and the week forecasts for the next three weeks, the three scenarios, the stock on hand, the safety margin, the forecast calculation and the order calculation line.
    3. Before deciding, Mounia checks the warnings: two stockout weeks were left out of the calculation and one unusual week was found. Mounia then reads the explanation.
    4. To see how much the unusual week matters, Mounia switches unusual weeks from included to excluded on the product screen. The screen says that the change applies to all products, and the base forecast and the suggested order quantity update. Mounia switches back.
    5. Mounia keeps the suggested order quantity or adjusts it, and moves on to the next product.
    6. Mounia finishes with the combined order overview, where each product is marked «Foreslått» (suggested) or «Justert av deg» (adjusted by you), and takes it to the meeting.
  - **Climax:** For each product, Mounia sees one number to order next week, how it was calculated, and whether it can be trusted.
  - **Resolution:** Mounia leaves the session with an order quantity decided for every product. The orders are placed outside Prognose.
  - **Edge cases:** A product with fewer than 3 valid weeks gets no forecast, only a warning about insufficient data, so Mounia decides by hand. If the stock on hand already covers demand, the suggested order quantity is 0, and the order calculation line says why.
  - **Priority note:** Steps 1 to 4 are Must. Adjusting an order quantity (step 5) and the combined order overview with the «Foreslått» or «Justert av deg» marking (step 6) are Should. Saving adjustments between sessions and marking a product as approved are Could; without them, adjustments last for the current session only.

## 3. Glossary

The user interface and all explanations are in Norwegian; this PRD is in English. The PRD uses the English term, and the app shows the Norwegian label. Both are binding: no synonyms in either language. The code uses the English terms to name domain concepts. Where a definition summarizes a rule or a setting, the rule in §5 or the FR-20 table is authoritative.

**Company and data**

| Term | UI label (Norwegian) | Definition |
|---|---|---|
| **Company** | Bedrift | A business account, identified by a **customer number** (kundenummer) and a password. A company owns its products, sales history and settings, and sees only its own data. |
| **Product** | Produkt | An item the company buys and sells, identified by a **product number** (varenummer) and a name. Each product has a sales history and a stock on hand. A company has about 10 to 50 products. |
| **Sales history** | Salgshistorikk | Units sold per product per week. Most test products have 104 weeks; some have fewer. The number of weeks in the sales history includes stockout weeks. |
| **Stock on hand** | Lagerbeholdning | The stock of a product at the end of the latest data week (R-13). |

**Weeks**

| Term | UI label (Norwegian) | Definition |
|---|---|---|
| **Week** | Uke | The period unit for all data, forecasts and orders. `[ASSUMPTION: a calendar week identified by year and week number.]` Distances between weeks are counted by their position in the sales history, not by calendar arithmetic. |
| **Latest data week** | Siste registrerte uke | The most recent week in the company's sales history. It is the reference point for "now": week 1 of the forecast horizon is the week after it, and the old-data warning counts from it. |
| **Recent period** | Siste 12 uker | The 12 most recent weeks of the sales history, up to and including the latest data week. Stockout weeks, unusual weeks and level shifts count as active warnings only when they fall in it (R-15). |
| **Stockout week** | Utsolgt uke | A week flagged in the data as out of stock. Its sales do not show real demand. |
| **Valid week** | Gyldig uke | A week that is not a stockout week. Valid weeks are counted for the thresholds and the confidence label. |
| **Outlier rule** | Avviksregel | The rule (R-10) that decides whether a valid week is an unusual week: sales more than 2 × the baseline. |
| **Baseline** | Sammenligningsgrunnlag | The median of the 3 most recent earlier valid weeks that are not unusual weeks (R-10). |
| **Unusual week** | Uvanlig uke | A valid week that the outlier rule flags. The user chooses whether unusual weeks are included in or excluded from the calculation. An excluded unusual week still counts as a valid week. |
| **Level shift** | Nytt nivå | Three or more unusual weeks in a row, counting valid weeks only (R-11). They become level-shift weeks: a possible new normal level, always kept in the calculation and reported with a warning. |
| **Calculation week** | Uke brukt i beregningen | A valid week that is used to calculate the forecast: not an excluded unusual week. |

**Forecast**

| Term | UI label (Norwegian) | Definition |
|---|---|---|
| **Forecasting method** | Prognosemetode | **Moving average** (glidende gjennomsnitt; window 2 to 12 weeks, default 3) or **exponential smoothing** (eksponentiell glatting; factor 0.1 to 0.9, default 0.3). |
| **Base forecast** | Grunnprognose | The result of the forecasting method, calculated on the calculation weeks, or on their seasonally adjusted values when seasonal adjustment is on (R-14). |
| **Forecast horizon** | De neste tre ukene | The three weeks after the latest data week (week 1, week 2, week 3). |
| **Week forecast** | Ukeprognose | The forecast for one week of the forecast horizon: the base forecast, multiplied by the seasonal index of that week's week number when seasonal adjustment is on. Without seasonal adjustment, the week forecasts for weeks 1, 2 and 3 are equal. The normal scenario of a week is its week forecast, so the **week-1 normal forecast** is the week forecast for week 1. |
| **Scenario** | Scenario (normal, optimistisk, pessimistisk) | Normal = the week forecast. Optimistic = the week forecast increased by the **scenario percentage** (scenarioprosent, default 10%, range 0% to 50%). Pessimistic = the week forecast reduced by the scenario percentage, never below 0. Scenarios are what-if alternatives, not probabilities. |
| **Seasonal adjustment** | Sesongjustering | An optional calculation step (Should) that uses seasonal indices (R-14). It is a company setting, off by default. |
| **Seasonal index** | Sesongindeks | For each week number, the mean sales of that week number divided by the mean of all week-number means (R-14). |

**Ordering**

| Term | UI label (Norwegian) | Definition |
|---|---|---|
| **Safety margin** | Sikkerhetsmargin | An adjustable percentage (default 10%, range 0% to 100%) of the week-1 normal forecast, added to it when the suggested order quantity is calculated. A rule of thumb that does not account for demand variability; not a service-level guarantee. |
| **Suggested order quantity** | Foreslått bestillingsmengde | What Prognose recommends ordering for next week: week-1 normal forecast plus safety margin minus stock on hand, never below 0, rounded up to whole units (R-8). Replaces the brief's "suggested planning quantity". |
| **Adjusted order quantity** | Justert bestillingsmengde | A quantity the user sets instead of the suggested order quantity (Should). |
| **Weeks of cover** | Uker dekning | Stock on hand ÷ week-1 normal forecast, shown with one decimal. Used to sort the product overview (R-12). |
| **Order-soon status** | Bestill snart | Marks a product whose suggested order quantity is above 0, so that it comes first in the product overview (R-12). |
| **Combined order overview** | Samlet bestillingsoversikt | A list of all products with their suggested or adjusted order quantity, each marked «Foreslått» or «Justert av deg» (Should). |

**Trust signals and explanation**

| Term | UI label (Norwegian) | Definition |
|---|---|---|
| **Confidence label** | Tillitsmerke (høy, middels, lav) | A per-product label with a plain-language reason, set by R-16. |
| **Warning** | Varsel | A message about the data behind a forecast that counts as an active warning for the confidence label: stockout weeks, unusual weeks or a level shift in the recent period; old data; insufficient data; and (Should) an unadjusted seasonal pattern (R-15). |
| **Note** | Merknad | An information message that does not affect the confidence label, for example that weeks 2 and 3 repeat week 1, that seasonal adjustment could not be used, or that the stock on hand covers next week (R-15). |
| **Explanation** | Forklaring | Plain-language text about a product's forecast and suggested order quantity. Template-based (Must); optionally rephrased by a local language model (Should), in which case it is labeled «KI-omformulert forklaring» (FR-27). |

**Screens, settings and tests**

| Term | UI label (Norwegian) | Definition |
|---|---|---|
| **Product overview** | Produktoversikt | The list of all products of the company, shown after login (FR-24). |
| **Product screen** | Produktside | The page for one product (FR-25). |
| **Forecast calculation** | Prognoseutregning | The display of how the base forecast and the week forecasts were calculated, with the calculation weeks used and the weeks left out (FR-35). |
| **Order calculation line** | Utregning av bestillingsmengde | The one-line display of how the suggested order quantity was calculated (FR-12). |
| **Settings** | Innstillinger | The adjustable inputs: forecasting method, window, smoothing factor, scenario percentage, safety margin, handling of unusual weeks, and seasonal adjustment (when FR-9 is built). |
| **Reference example** | Referanseeksempel (fasit) | A hand-calculated example that serves as the answer key for tests (§5.7). |

## 4. Features

Every functional requirement (FR) has a priority: **Must** (version 1 is not done without it), **Should** (built only after the Must scope passes SM-1 and SM-3) or **Could** (only if time allows). The tag in a feature's heading is its core priority; within a feature, the Should and Could FRs follow the Must FRs. Formulas, conventions and reference examples for all calculations are in §5. Where reference examples (E-n) test an FR, the FR names them. Must and Should FRs have testable consequences; Could FRs are stated in one sentence and get their consequences when they are planned. FR numbers are stable: FR-35 and FR-36 were added during review and sit with the feature they belong to.

### 4.1 Login and Company Data (Must)

**Description:** Each company logs in with its customer number and password and works only with its own data. Version 1 has no self-registration: the generator script (FR-3) creates two test companies, whose logins are documented in the README. The data itself (products, sales history, stock on hand) comes from the seed data and cannot be edited in the app. Realizes UJ-1 (entry state).

**Functional Requirements:**

#### FR-1: Log in with customer number and password

A user can log in to their company with the customer number and password. Priority: Must. Realizes UJ-1.

**Consequences (testable):**
- A correct customer number and password open the product overview.
- A wrong customer number or password shows one general error message in Norwegian, for example «Feil kundenummer eller passord.», which does not reveal which of the two was wrong.
- Passwords are hashed with an established, well-maintained password-hashing implementation, such as the web framework's built-in password hasher or a widely used library. It uses a recognized algorithm with salt (for example PBKDF2, scrypt, Argon2 or bcrypt). A self-made hashing algorithm, plain text and fast general-purpose hashes are not allowed. No plain-text password exists in the database, the seed data or the logs.
- Every page except the login page sends a user who is not logged in to the login page. Logging out ends the session.

**Out of Scope:** see §7.

#### FR-2: Company data isolation

A logged-in company can see only its own products, sales history and stock on hand, and can see and change only its own settings and order quantities. Priority: Must.

**Consequences (testable):**
- The server checks the logged-in company on every request that reads or changes company data. Checks in the user interface alone do not count.
- A direct request for another company's product (for example by changing an identifier in the address) returns "not found" and shows none of that company's data.
- Lists, such as the product overview and the combined order overview, contain only the logged-in company's products.
- An automated test logs in as test company A, tries to read test company B's products, sales history, stock on hand and settings, and to change B's settings and order quantities, both directly and through lists. It passes only if every attempt is refused and no list shows B's data.

### 4.2 Products and Sales Data (Must)

**Description:** Prognose works only on synthetic data. A documented, repeatable generator script creates the data with known patterns, so that every calculation rule and every warning has at least one test case with a known answer. The data is stored locally and survives restarts.

**Functional Requirements:**

#### FR-3: Synthetic dataset with known patterns

The system provides a synthetic dataset for two test companies, each with 10 to 50 products. Priority: Must.

**Consequences (testable):**
- Each product has a product number, a name, a weekly sales history, a stockout flag per week and a stock on hand.
- Most products have 104 weeks of sales history. At least one product has fewer than 3 valid weeks, one has 3 to 11 valid weeks, and one has 12 to 103 valid weeks.
- The dataset contains at least one product for each of these patterns: a known trend; a known seasonal pattern without trend; stockout weeks; unusual weeks; a level shift; a long run of stockout weeks at the end of the history; stock on hand that already covers next week's demand; and a history that reaches the confidence label «høy».
- The rule test products are built from the reference-example series in §5.7 (E1 to E4, E7 to E10, E15 to E19), so that the product screen and the reference spreadsheet show the same case. For every rule test product, the reference spreadsheet holds the expected base forecast, suggested order quantity, unusual weeks and level-shift weeks, warnings, and confidence label (DR-3).
- The generator script produces identical data on every run, and both the script and its output live in documented places in the repository (DR-2).
- Each test company has a known customer number and password, documented in the README.

#### FR-4: Data stored between sessions

Products, sales history, stock on hand and settings are stored in a database: a local file when Prognose runs on the user's computer, and PostgreSQL in the published version (DR-10). Priority: Must.

**Consequences (testable):**
- After the application is stopped and started again, all data and settings are unchanged.
- Locally, the database runs as a file. No database server or online service is needed.
- The published version keeps the same data in PostgreSQL, loaded with the same load command (DR-4).

### 4.3 Forecast Calculation (Must)

**Description:** The base forecast is calculated with the forecasting method chosen in the settings, over calculation weeks only. Without seasonal adjustment (Should), the week forecasts for weeks 1, 2 and 3 are equal. Realizes UJ-1 step 2.

**Functional Requirements:**

#### FR-5: Moving average

The system calculates the moving average as the mean of the last N calculation weeks, where N is the window (2 to 12 weeks, default 3). Priority: Must.

**Consequences (testable):**
- Stockout weeks and excluded unusual weeks are skipped, and the system looks further back until it has N calculation weeks.
- Results match E1, E7, E8, E15 to E20 and E28.

#### FR-6: Exponential smoothing

The system calculates exponential smoothing over the calculation weeks in time order, with a smoothing factor from 0.1 to 0.9 (default 0.3), using the formula and start value in R-4. Priority: Must.

**Consequences (testable):**
- Stockout weeks and excluded unusual weeks are skipped, not treated as zero sales.
- Results match E2 and E17.

#### FR-7: Three-week forecast horizon

The system shows the week forecasts for week 1, week 2 and week 3 after the latest data week. Priority: Must.

**Consequences (testable):**
- Without seasonal adjustment, the week forecasts for weeks 1, 2 and 3 are equal, and the product screen shows the note «Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong.»
- Only week 1 is used for the suggested order quantity (FR-11).
- Both methods assume no trend, so a product with a steady trend gets a forecast that lags behind it (E28). This is a stated limitation (DR-1).

#### FR-8: Insufficient data

The system shows no forecast for a product without enough data, and says why. Priority: Must. Realizes the UJ-1 edge case.

**Consequences (testable):**
- A product with fewer than 3 valid weeks gets no forecast and a warning about insufficient data.
- When the moving average is the chosen method, a product with fewer calculation weeks than the window gets no forecast and a warning that names the window and the number of calculation weeks available.
- A product without a forecast has no suggested order quantity, and the user decides by hand.
- Results match E11.

#### FR-9: Seasonal adjustment

The system applies the seasonal adjustment in R-14 when the company setting «Sesongjustering» is on. Priority: Should.

**Consequences (testable):**
- The setting is off by default (FR-20).
- When it is on, the week forecasts are seasonally adjusted, and the scenarios, suggested order quantity and weeks of cover all use them (E27).
- When seasonal adjustment is not possible for a product (a week number without calculation weeks, or a week-number mean of 0), the product gets week forecasts without seasonal adjustment and a note (E25, E26).
- The cycle length is a parameter of the calculation (52 in the app), so that E14 and E25 to E27, which use a 4-week cycle, run as tests.
- With the setting off, a test confirms that the seasonal test product's week forecasts stay flat and that the note from FR-7 is shown.
- The limitations in §5.5 are stated in the README.

### 4.4 Scenarios and Suggested Order Quantity (Must)

**Description:** Prognose turns the week forecasts into three scenarios and a suggested order quantity for next week. The product screen shows exactly how the quantity was calculated and what it does not take into account. The suggested order quantity is advice: Prognose places no orders, and the user makes the final decision. Realizes UJ-1 steps 2 and 5.

**Functional Requirements:**

#### FR-10: Three scenarios

For each week of the forecast horizon, the system shows the normal, optimistic and pessimistic scenario from the week forecast and the scenario percentage (R-7). Priority: Must.

**Consequences (testable):**
- With a week forecast of 100 and a scenario percentage of 10%, the scenarios are normal 100, optimistic 110 and pessimistic 90. E3 gives normal 14.333, optimistic 15.767 and pessimistic 12.900.
- The pessimistic scenario is never below 0.
- Next to the scenarios, the product screen shows the text «Scenarioene viser hva som skjer hvis salget blir 10 % høyere eller lavere. De er ikke sannsynligheter.», with «10 %» replaced by the actual scenario percentage.

#### FR-11: Suggested order quantity

The system calculates the suggested order quantity for next week from the week-1 normal forecast, the safety margin and the stock on hand (R-8). Priority: Must. Realizes the UJ-1 climax.

**Consequences (testable):**
- Results match E4, E5, E6 and E21; E5 gives 70, not 71.
- When the stock on hand covers the week-1 normal forecast plus the safety margin, the suggested order quantity is 0, never negative.
- The result is rounded up to whole units once, at the end, after rounding to 6 decimals (R-9).
- A product without a forecast (FR-8) has no suggested order quantity.

#### FR-12: Order calculation line

The product screen shows the order calculation line: the week-1 normal forecast, the safety margin as a percentage and an amount, the stock on hand, the unrounded result and the suggested order quantity. Priority: Must.

**Consequences (testable):**
- E4 is shown as «Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → foreslått bestillingsmengde 11».
- E6 is shown as «Prognose 100,0 + sikkerhetsmargin 10 % (10,0) − lager 150 = −40,00 → foreslått bestillingsmengde 0 (lageret dekker behovet)».
- E21 is shown as «… = 0,07 → foreslått bestillingsmengde 1».
- The numbers are rounded for display (R-9), so the shown parts may not add up exactly to the shown result; the line says «Tallene er avrundet for visning.»
- Below the line, the product screen always shows the fixed text «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.»

#### FR-13: Order quantity per scenario

The product screen also shows the order quantity for the optimistic and the pessimistic scenario. Each is calculated with R-8, including the safety margin, with the scenario's week-1 value in place of the week-1 normal forecast. Priority: Should.

**Consequences (testable):**
- Results match E22.

#### FR-14: Overstock note

When the suggested order quantity is 0 and the stock on hand is above 0, the product screen and the product overview show the note «Lagerbeholdningen dekker forventet behov neste uke.» Priority: Should.

**Consequences (testable):**
- When both the week-1 normal forecast and the stock on hand are 0, no overstock note is shown (E23).

### 4.5 Data Quality, Warnings and Confidence (Must)

**Description:** Prognose tells the user when a forecast rests on weak or distorted data, and always shows which weeks were left out and why. Warnings and notes follow R-15, and the confidence label follows R-16. Realizes UJ-1 step 3.

**Functional Requirements:**

#### FR-15: Stockout weeks left out

The system never uses the sales of stockout weeks in any calculation. Priority: Must.

**Consequences (testable):**
- Stockout weeks are not valid weeks and are not counted in any valid-week threshold.
- Each stockout week has its own marker in the chart, and the product screen lists the stockout weeks left out by week number.
- A stockout week in the recent period triggers a warning (R-15).
- A product whose history contains stockout weeks gets the same forecast as the same history with those weeks removed (E7, E16, E17).

#### FR-16: Unusual weeks

The system finds unusual weeks with the outlier rule (R-10), marks them, and includes or excludes them according to the company setting. Priority: Must.

**Consequences (testable):**
- Whatever the setting, each unusual week has its own marker in the chart, different from the stockout and level-shift markers and explained in the legend.
- By default unusual weeks are included in the calculation, so no data is hidden automatically.
- When the setting excludes unusual weeks, they are not used in the calculation but still count as valid weeks.
- When unusual weeks are excluded, the product screen lists each excluded week by week number and states the number of calculation weeks used.
- Unusual weeks in the recent period trigger a warning whether they are included or excluded, so switching the setting does not add or remove this warning (R-15, R-16).
- Results match E8, E15, E18 and E19.

#### FR-17: Level shift

The system treats three or more unusual weeks in a row as a level shift (R-11), not as unusual weeks. Priority: Must for the calculation and the confidence label; Should for the dedicated warning text.

**Consequences (testable):**
- Level-shift weeks stay in the calculation whatever the unusual-week setting is.
- Detection follows the single forward pass in R-10 and R-11: two high weeks in a row are unusual weeks (E8), three are a level shift (E9), and a later spike is compared with the new level (E15). Stockout weeks in between do not break the run (E16).
- Each level-shift week has its own marker in the chart.
- A level shift in the recent period counts as an active warning for the confidence label (Must), and the label's reason names it. The dedicated warning text «Etterspørselen ser ut til å ha endret nivå.» is Should.
- `[ASSUMPTION: this simplified rule is project-defined; the research found no established simple rule. It is validated with the level-shift and seasonal test products before it is relied on (§10).]`

#### FR-18: Old-data warning

The system warns when a product's latest valid week is more than 8 weeks before the latest data week, counted by position in the sales history. Priority: Must.

**Consequences (testable):**
- Because the reference point is the latest data week, a long run of stockout weeks at the end of the history triggers the warning.
- The warning states how many weeks have passed since the latest valid week.
- Results match E12.

#### FR-19: Confidence label

Every product gets a confidence label with a plain-language reason in Norwegian, set by R-16. Priority: Must. Realizes UJ-1 step 1.

**Consequences (testable):**
- The reason names the condition that decided the label and lists the active warnings, for example «Middels: 1 uvanlig uke de siste 12 ukene.»
- Results match E29.

#### FR-36: Seasonal-pattern warning

When a product shows a seasonal pattern (R-17) that the forecast does not use, because seasonal adjustment is off or not possible, the system shows the warning «Produktet har tydelig sesongvariasjon som prognosen ikke tar hensyn til.» Priority: Should. It needs only steps 1 and 2 of R-14, so it can be built before FR-9.

**Consequences (testable):**
- The warning counts as an active warning for the confidence label (R-16).
- Results match E30.

### 4.6 Settings (Must)

**Description:** One set of settings applies to all products of a company and is saved between sessions. The user can change the settings from the product screen and see the result change at once, which is the core flow from the teacher's feedback (SM-3). Because a change affects every product, the screen always says so.

**Functional Requirements:**

#### FR-20: Company-wide settings

The company has one set of settings with these defaults and ranges. Priority: Must.

| Setting | Default | Allowed values |
|---|---|---|
| Forecasting method | Moving average | Moving average or exponential smoothing |
| Window (moving average) | 3 weeks | 2 to 12 weeks |
| Smoothing factor (exponential smoothing) | 0.3 | 0.1 to 0.9 |
| Scenario percentage | 10% | 0% to 50% |
| Safety margin | 10% | 0% to 100% |
| Unusual weeks | Included | Included or excluded |
| Seasonal adjustment | Off | On or off (only when FR-9 is built) |

**Consequences (testable):**
- A value outside the allowed range is refused with a Norwegian message, and the previous value stays.
- A setting that does not apply to the chosen forecasting method (the window under exponential smoothing, or the smoothing factor under the moving average) is shown as not in use.

#### FR-21: Changes apply to all products at once

A change to the settings takes effect immediately for every product of the company and can be made from the product screen. Priority: Must. Realizes UJ-1 step 4 and the core flow in SM-3.

**Consequences (testable):**
- The settings area always shows the text «Endringen gjelder alle produkter i bedriften.»
- After a change, the screen confirms the change in Norwegian and shows the previous and the new affected value, for example «Grunnprognose: 14,3 → 13,8».
- After a change, the affected value updates on the product screen. A test changes each setting for a test product that the setting affects and checks that the value in the table changes:

| Setting changed | Value that changes | Example |
|---|---|---|
| Forecasting method | Base forecast | E1 → E2: 14.333 → 13.790 |
| Window | Base forecast (moving average) | E1 with window 4 instead of 3 |
| Smoothing factor | Base forecast (exponential smoothing) | E2 with factor 0.5 instead of 0.3 |
| Scenario percentage | Optimistic and pessimistic scenario | E3 with 20% instead of 10% |
| Safety margin | Suggested order quantity | E4 with 50% instead of 10% |
| Unusual weeks | Base forecast of a product with unusual weeks | E8: 41.0 → 21.333 |
| Seasonal adjustment (Should) | Week forecasts of the seasonal test product | E14: flat → seasonal |

#### FR-22: Settings saved between sessions

The settings are saved per company. Priority: Must.

**Consequences (testable):**
- The settings are the same after logging out and in again, or after a restart.

#### FR-23: Settings per product

A product can have its own settings that override the company settings. Priority: Could.

### 4.7 Product Overview and Product Screen (Must)

**Description:** The product overview shows where to start; the product screen shows everything needed to decide the order for one product, including how the numbers were calculated. Realizes UJ-1 steps 1 to 4.

**Functional Requirements:**

#### FR-24: Product overview

After login, the system shows the product overview: all products of the company with product number, name, stock on hand, week-1 normal forecast, suggested order quantity, weeks of cover, confidence label and order-soon status. Priority: Must. Realizes UJ-1 step 1.

**Consequences (testable):**
- The products are sorted by R-12 (E13, E24).
- A product without a forecast shows the reason instead of a number.
- When the company has no products, the overview says in Norwegian that no data is loaded and names the load command from the README.

#### FR-25: Product screen

For one product, the system shows a chart and the decision details. Priority: Must. Realizes UJ-1 steps 2 to 4.

**Consequences (testable):**
- The chart shows the sales history and the week forecasts with the three scenarios for the forecast horizon.
- Stockout weeks, unusual weeks and level-shift weeks each have their own marker, which differs by more than color (NFR-7), and a legend explains them.
- The screen shows the stock on hand, the safety margin, the forecast calculation (FR-35), the order calculation line (FR-12), all active warnings and notes, the confidence label with its reason, and the explanation (FR-26).
- On a 1366 × 768 screen, the suggested order quantity, the confidence label and the active warnings are visible without scrolling (see also NFR-6).
- The settings can be changed from the screen (FR-21).

#### FR-35: Forecast calculation

The product screen shows how the base forecast and the week forecasts were calculated, so that they can be checked by hand. Priority: Must.

**Consequences (testable):**
- For the moving average, one line with the values used, for example «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3» (E1), and the week numbers of the calculation weeks used.
- For exponential smoothing, the last update, for example «Eksponentiell glatting, faktor 0,3: 0,3 × 15 + 0,7 × 13,3 = 13,8» (E2), and a table of all calculation weeks with their sales and level.
- A list of the weeks left out and why (stockout week or excluded unusual week).
- With seasonal adjustment on (Should), the seasonal indices and adjusted values used, and the week forecasts for weeks 1 to 3 (E14).
- Numbers are rounded for display by R-9, and the values match the reference examples.

### 4.8 Explanation (Must)

**Description:** Every product screen has a plain-language explanation in Norwegian. The version 1 explanation is built from templates, so it never contains a number that the calculation did not produce. An optional local language model can make the text read more naturally, under strict checks. Realizes UJ-1 step 3.

**Functional Requirements:**

#### FR-26: Template explanation in Norwegian

The system writes an explanation from the calculation result only. Priority: Must.

**Consequences (testable):**
- The explanation covers the forecasting method and settings used, the number of calculation weeks, which weeks were left out and why, every active warning and note (R-15), the confidence label and its reason, and the order calculation line.
- The same calculation result always gives the same text, and snapshot tests cover each template.
- Every number in the explanation comes from the calculation result.

#### FR-27: Explanation kept apart from calculated numbers

The explanation is shown in its own area under the heading «Forklaring», below the calculated numbers. Priority: Must.

**Consequences (testable):**
- The explanation contains no number that is not also shown among the calculated numbers on the product screen.
- Text produced or rephrased by a language model is labeled «KI-omformulert forklaring» (when FR-28 is built).

#### FR-28: Optional local language model

When switched on, a language model running locally rephrases the template explanation in Norwegian. Priority: Should.

**Consequences (testable):**
- The feature is off by default. It is switched on in the local configuration listed in `.env.example`, not in the company settings. It needs no API key, paid service or internet connection, and no hosted AI service is used (AG-5).
- The application inserts every number itself; the model only rephrases the text around them.
- The application rejects the rephrased text if any number, or the label attached to a number, differs from the template explanation.
- The template explanation is shown instead, without an error for the user, when the model server is not running, the model is missing, no answer arrives within 10 seconds `[ASSUMPTION]`, the response contains an error, or the text is rejected.
- The README names the model used and its license obligations (DR-1).
- The model is never part of the basic setup (SM-2): the README describes it as a separate, optional step with its download size and expected time, and the app runs fully without it.

### 4.9 Purchase Planning (Should)

**Description:** The user can override a suggested order quantity and collect all decisions in one list before the purchasing meeting. Prognose recommends; the user decides, and no order is ever placed from the system. Realizes UJ-1 steps 5 and 6.

**Functional Requirements:**

#### FR-29: Adjust an order quantity

The user can replace the suggested order quantity with an adjusted order quantity. Priority: Should. Realizes UJ-1 step 5.

**Consequences (testable):**
- The adjusted order quantity must be a whole number of 0 or more; other input is refused with a Norwegian message.
- The suggested order quantity stays visible next to the adjusted one, and the user can reset it to the suggested order quantity.
- Example: Mounia changes a suggested order quantity of 70 to 80; the product is then marked «Justert av deg».

#### FR-30: Combined order overview

The system shows the combined order overview. Priority: Should. Realizes UJ-1 step 6.

**Consequences (testable):**
- Every product of the company appears with its suggested or adjusted order quantity, marked «Foreslått» or «Justert av deg».

#### FR-31: Save adjustments and mark products as approved

Adjusted order quantities are saved between sessions, and the user can mark a product as approved. Priority: Could.

#### FR-32: Export the combined order overview

The combined order overview can be exported as a CSV file. Priority: Could.

#### FR-33: Stock not lasting through weeks 2 and 3

The system shows a note when the stock on hand plus the suggested order quantity is less than the sum of the week forecasts for weeks 1, 2 and 3, that is, when it will not last through weeks 2 and 3. Priority: Could.

#### FR-34: Forecast accuracy

The product screen shows the mean absolute error (MAE) of past one-week forecasts. The mean absolute percentage error (MAPE) is not used, because weeks with zero sales make it undefined. Priority: Could.

## 5. Calculation Rules and Reference Examples

All calculations are deterministic: the same data and settings always give the same result. The rules live in one module that does not depend on the user interface or the database, so that each rule can be unit tested against the reference examples in §5.7 (NFR-2). The group recalculates every reference example by hand or in a spreadsheet before implementation; those examples are the answer key (fasit) for the tests (DR-3).

Each rule is tagged with its source status: **sourced** (backed by the research reports), **partly supported**, or **project-defined** (a simplified choice made for this project, listed in §11). The rationale behind each rule, including the alternatives considered, is in `addendum.md` (§6 there); the research reports are in `_bmad-output/planning-artifacts/research/`.

**Calculation order.** For each product, the rules apply in this order:
1. Valid weeks (R-1).
2. Unusual weeks and level shifts (R-10, R-11).
3. Calculation weeks (R-2) and minimum data (R-6).
4. Base forecast (R-3 or R-4), on seasonally adjusted values when seasonal adjustment is on (R-14).
5. Week forecasts (R-5; R-14 step 3 when seasonal adjustment is on).
6. Scenarios (R-7).
7. Suggested order quantity (R-8, R-9), with the stock on hand from R-13.
8. Order-soon status and sorting (R-12).
9. Warnings, notes and the confidence label (R-15 to R-17).

### 5.1 Which Weeks Are Used

- **R-1 Valid weeks** *(partly supported)*. All weeks of the sales history except stockout weeks.
- **R-2 Calculation weeks** *(project-defined)*. The valid weeks in time order, minus unusual weeks when the setting excludes them. Level-shift weeks are always calculation weeks.

### 5.2 Base Forecast and Week Forecasts

- **R-3 Moving average** *(sourced; skipping weeks is project-defined)*. Base forecast = the sum of the last N calculation weeks divided by N, where N is the window. Requires at least N calculation weeks.
- **R-4 Exponential smoothing** *(sourced; skipping weeks is project-defined)*. The level of the first calculation week is its sales. For each later calculation week, in time order: level = α × sales that week + (1 − α) × previous level, where α is the smoothing factor. Weeks that are not calculation weeks are skipped and do not count as zero (E17). Base forecast = the last level. The default α of 0.3 comes from the Product Brief.
- **R-5 Week forecasts** *(sourced)*. Without seasonal adjustment, the week forecasts for weeks 1, 2 and 3 all equal the base forecast, because both methods give a flat forecast. Both methods assume no trend, so they lag behind a steady trend (E28). Only seasonal adjustment (R-14, Should) can make the week forecasts differ.
- **R-6 Minimum data** *(project-defined)*. A forecast is made only when the product has at least 3 valid weeks and enough calculation weeks: at least N for the moving average, and at least 1 for exponential smoothing.

### 5.3 Scenarios and Suggested Order Quantity

- **R-7 Scenarios** *(project-defined: a fixed percentage, not a statistical interval)*. With week forecast F and scenario percentage s: optimistic = F × (1 + s); pessimistic = the larger of 0 and F × (1 − s).
- **R-8 Suggested order quantity** *(partly supported: a simplified weekly order-up-to policy; the percentage margin is project-defined)*. With week-1 normal forecast F1, safety margin m and stock on hand S: suggested order quantity = the larger of 0 and (F1 × (1 + m) − S, rounded up to a whole unit). The rule assumes weekly review, no lead time, no orders already on the way, and stock on hand as the only stock; the margin is a rule of thumb that does not account for demand variability.
- **R-9 Rounding and display** *(project-defined)*. Calculations use full precision. Before rounding up in R-8, the value is rounded to 6 decimals, so that a computer result such as 70.00000000000001 becomes 70 and not 71 (E5). Displayed numbers are rounded half away from zero (E20): forecasts, scenarios, weeks of cover and the margin amount with one decimal; the unrounded result on the order calculation line with two decimals; order quantities and percentages as whole numbers. The Norwegian decimal comma is used.

### 5.4 Unusual Weeks and Level Shift

- **R-10 Outlier rule** *(project-defined; the threshold comes from the Product Brief, and the research found no source for it)*. The valid weeks are checked one at a time, in time order, in a single pass. For each valid week, the baseline is the median of the 3 most recent earlier valid weeks that are not unusual weeks; level-shift weeks are included. If there are fewer than 3 such weeks, the week is not checked, but it still enters later baselines (E19). If the baseline is 0, the week is not an unusual week, so a product with many zero-sales weeks does not get every week with sales flagged (E10). Otherwise the week is an unusual week when its sales are more than 2 × the baseline; exactly 2 × is not (E18). Only high sales are flagged.
- **R-11 Level shift** *(project-defined)*. In the same pass, when a week becomes an unusual week and the two previous valid weeks are also unusual weeks, the three weeks become level-shift weeks at once (E9). Level-shift weeks are not unusual weeks, are always calculation weeks, and count in later baselines, so later weeks are compared with the new level (E15). Stockout weeks between them do not break the run (E16). One or two unusual weeks in a row stay unusual weeks (E8).

### 5.5 Order-Soon Status, Stock on Hand and Seasonal Adjustment

- **R-12 Order-soon status** *(project-defined)*. A product has order-soon status when its suggested order quantity is above 0, that is, when the stock on hand does not cover the week-1 normal forecast plus the safety margin. When the week-1 normal forecast is 0, weeks of cover is shown as «–» and there is no order-soon status (E23). The product overview is sorted in three groups:
  1. the products with order-soon status, by weeks of cover, lowest first, with ties sorted by product number (E24);
  2. the products without a forecast `[ASSUMPTION]`, so they are not forgotten;
  3. the other products, by product number.
- **R-13 Stock on hand** *(project-defined)*. One value per product: the stock at the end of the latest data week.
- **R-14 Seasonal adjustment** *(Should; steps 1, 2 and 4 are project-defined, step 3 is sourced)*. Used only when the setting «Sesongjustering» is on.
  1. For each week number (1 to the cycle length, which is 52 in the app), take the mean of the sales in that week number's calculation weeks.
  2. Seasonal index = that mean ÷ the mean of all week-number means. The indices are kept at full precision and average exactly 1.
  3. Divide each calculation week's sales by the index of its week number, and calculate the base forecast on these adjusted values with the chosen forecasting method. Then, for each of week 1, week 2 and week 3 of the forecast horizon, multiply the base forecast by the index of that week's week number to get its week forecast.
  4. If any week number has no calculation week, or any week-number mean is 0, seasonal adjustment is not used for the product: its week forecasts are calculated without it, and a note is shown (E25, E26).

  The cycle length is a parameter, so that the reference examples can use a 4-week cycle (E14, E25 to E27, E30). `[ASSUMPTION: the data uses week numbers 1 to 52; a week 53 would use the index of week 52.]`

**Known limitations of R-14.** These are stated in the README and the process documentation:
- **No trend.** The method ignores trend. If sales rise from one year to the next, the second year's weeks pull the indices, and trend is mistaken for season. The seasonal test product is therefore made without trend, and products with a strong trend may get distorted indices.
- **Few values per week number.** With 104 weeks, each index rests on at most two values. One stockout week or unusual week in a given week number moves that index strongly.
- **Seasonal peaks can look like unusual weeks.** The outlier rule (R-10) compares each week with the three weeks before it, so a seasonal peak can be flagged as an unusual week. Because unusual weeks are included by default, the forecast is not changed by this, but a peak in the recent period triggers a warning and lowers the confidence label to «middels».
- **Long seasonal peaks can become a level shift.** A peak that stays above 2 × the baseline for three weeks or more becomes a level shift, so the seasonal test product can show level-shift markers every season.
- **Excluded spikes can switch seasonal adjustment off.** With unusual weeks excluded, a spike flagged in the same week number in both years leaves that week number without calculation weeks, and step 4 then switches seasonal adjustment off for the product.
- **Not a textbook index, and no benchmark.** The research found no source for the simple index in steps 1 and 2. The textbook alternatives, which handle trend better but are much harder to check by hand, are described in `addendum.md` (§6 there). To keep the scope small, the result is not compared with the seasonal naive benchmark.

### 5.6 Warnings, Notes and Confidence Label

- **R-15 Warnings and notes** *(project-defined)*. These are the active warnings, each counted by R-16:
  1. Stockout weeks in the recent period (FR-15).
  2. Unusual weeks in the recent period, whether included or excluded (FR-16).
  3. A level shift with at least one level-shift week in the recent period (FR-17).
  4. Old data: the latest valid week is more than 8 weeks before the latest data week, counted by position in the sales history (FR-18).
  5. Insufficient data: the product has no forecast (FR-8).
  6. (Should) An unadjusted seasonal pattern (R-17, FR-36).

  Stockout weeks and unusual weeks before the recent period are still listed on the product screen, but they are not active warnings. The notes, which do not affect the label, are: weeks 2 and 3 repeat week 1 (FR-7); seasonal adjustment could not be used (FR-9); the stock on hand covers next week (FR-14); and the stock will not last through weeks 2 and 3 (FR-33).
- **R-16 Confidence label** *(project-defined thresholds)*. The conditions are checked in this order, and the first one that applies sets the label:
  1. The product has no forecast, or fewer than 12 valid weeks: **lav**.
  2. The product has an active warning, fewer than 104 weeks in its sales history, or fewer than 100 valid weeks: **middels**.
  3. Otherwise (at least 104 weeks in the sales history, at least 100 valid weeks, and no active warning): **høy**.

  The reason names the deciding condition and lists the active warnings (E29).
- **R-17 Seasonal-pattern check** *(Should; project-defined thresholds)*. For a product where R-14 steps 1 and 2 can be calculated (every week number has a calculation week and no week-number mean is 0), the product has a seasonal pattern when any seasonal index is 1.3 or more, or 0.7 or less `[ASSUMPTION]`. When seasonal adjustment is off or not used for the product, this is an active warning (E30).

### 5.7 Reference Examples (answer key)

Sales history for E1 to E4: 12, 15, 11, 14, 13, 16, 12, 15 (weeks 1 to 8, no stockout weeks, no unusual weeks). "S" marks a stockout week. Every result below was recomputed independently during review. The "Rule (priority)" column shows what each example tests; the Must examples form the Must gate in SM-1.

| # | Rule (priority) | Input and settings | Expected result |
|---|---|---|---|
| E1 | R-3 (Must) | Moving average, window 3 | (16 + 12 + 15) / 3 = 14.333 (shown as 14,3) |
| E2 | R-4 (Must) | Exponential smoothing, α = 0.3 | Levels 12, 12.9, 12.33, 12.831, 12.8817, 13.8172, 13.272, 13.7904; base forecast 13.790 (shown as 13,8) |
| E3 | R-7 (Must) | E1 with scenario percentage 10% | Optimistic 15.767, normal 14.333, pessimistic 12.900 |
| E4 | R-8, R-9 (Must) | E1 with safety margin 10% and stock on hand 5 | 14.333 × 1.1 − 5 = 10.767, rounded up to 11 |
| E5 | R-8, R-9 (Must) | Week-1 normal forecast 100, safety margin 10%, stock on hand 40 | 70 (not 71; tests R-9) |
| E6 | R-8 (Must) | Week-1 normal forecast 100, safety margin 10%, stock on hand 150 | 0 (the stock on hand covers the need) |
| E7 | R-1 to R-3 (Must) | Sales 20, 22, S, S, 21, 23; moving average, window 3 | 4 valid weeks; base forecast (22 + 21 + 23) / 3 = 22.0 |
| E8 | R-2, R-10 (Must) | Sales 20, 22, 21, 50, 52, 21 | Weeks 4 and 5 are unusual weeks. Moving average 3 with unusual weeks included: (50 + 52 + 21) / 3 = 41.0; excluded: (22 + 21 + 21) / 3 = 21.333 |
| E9 | R-11 (Must) | Sales 20, 22, 21, 50, 52, 51 | Weeks 4 to 6 are a level shift, kept whatever the setting: moving average 3 = 51.0 |
| E10 | R-10 (Must) | Sales 0, 0, 0, 5 | Baseline 0, so week 4 is not an unusual week |
| E11 a | R-6 (Must) | Sales 30, S, 25 (2 valid weeks) | No forecast; warning about insufficient data; confidence label «lav» (E29 e) |
| E11 b | R-6 (Must) | 12 valid weeks, of which 2 are unusual weeks excluded by the setting; moving average, window 12 | 10 calculation weeks, so no forecast; the warning names window 12 and 10 calculation weeks; confidence label «lav» (E29 e) |
| E12 | R-15 (Must) | Latest data week at position 104; latest valid week at position 95, then at position 96 | 9 weeks: old-data warning. 8 weeks: no warning |
| E13 | R-12 (Must) | Stock on hand 5 and week-1 normal forecast 14.333 (E4); stock on hand 150 and week-1 normal forecast 100 (E6) | First: weeks of cover 0.349 (shown as 0,3), order-soon status. Second: weeks of cover 1.5 (shown as 1,5), no order-soon status |
| E14 | R-14 (Should) | Seasonal adjustment, with a 4-week cycle instead of 52 to keep it short. Year 1: 10, 20, 30, 20. Year 2: 12, 18, 30, 22. Moving average, window 3 | Week-number means 11, 19, 30, 21; their mean 20.25; indices 0.5432, 0.9383, 1.4815, 1.0370 (kept at full precision). Adjusted last three weeks 19.184, 20.250, 21.214; base forecast 20.216. Week forecasts for weeks 1 to 3: 10.982, 18.968, 29.950 |
| E15 | R-10, R-11 (Must) | Sales 20, 22, 21, 50, 52, 51, 110, 50; moving average, window 3 | Weeks 4 to 6 are a level shift; week 7 is an unusual week (baseline 51, and 110 > 102); week 8 is normal. Unusual weeks included: (51 + 110 + 50) / 3 = 70.333; excluded: (52 + 51 + 50) / 3 = 51.0 |
| E16 | R-1, R-11 (Must) | Sales 20, 22, 21, S, S, 50, S, 52, 51; moving average, window 3 | 6 valid weeks, 3 stockout weeks left out. Weeks 6, 8 and 9 are a level shift; base forecast 51.0 with either setting |
| E17 | R-4 (Must) | Sales 20, 22, S, S, 21, 23; exponential smoothing, α = 0.3 | Levels 20, 20.6, 20.72, 21.404; base forecast 21.404 (16.256 if the stockout weeks were wrongly counted as zero) |
| E18 a | R-10 (Must) | Sales 20, 22, 21, 42; moving average, window 3 | 42 = 2 × 21, so not an unusual week; base forecast 28.333 |
| E18 b | R-10 (Must) | Sales 20, 22, 21, 43; moving average, window 3 | 43 is an unusual week; included 28.667, excluded 21.0 |
| E19 | R-10 (Must) | Sales 40, 10, 10, S, S, 25, 10; moving average, window 3 | Weeks 1 to 3 are not checked but enter the baseline. Week 6: baseline 10, so 25 is an unusual week. Included: (10 + 25 + 10) / 3 = 15.0; excluded: (10 + 10 + 10) / 3 = 10.0 |
| E20 | R-9 (Must) | Sales 10, 10, 10, 11; moving average, window 4 | 10.25, shown as 10,3 (half away from zero) |
| E21 | R-8, R-9 (Must) | Sales 27, 27, 28; moving average, window 3; safety margin 10%; stock on hand 30 | Week-1 normal forecast 27.333; 27.333 × 1.1 − 30 = 0.067, rounded up to 1. The order calculation line shows «= 0,07 → foreslått bestillingsmengde 1» |
| E22 | R-8 with FR-13 (Should) | E4 inputs with scenario percentage 10% | Optimistic: 15.767 × 1.1 − 5 = 12.343, rounded up to 13. Pessimistic: 12.9 × 1.1 − 5 = 9.19, rounded up to 10 |
| E23 | R-12 (Must) | Sales 0, 0, 0; stock on hand 0; moving average, window 3 | Base forecast and scenarios 0; suggested order quantity 0; weeks of cover «–»; no order-soon status; no overstock note |
| E24 | R-12 (Must) | Product A: stock on hand 0, week-1 normal forecast 10. Product B: stock on hand 0, week-1 normal forecast 20. Safety margin 10% | Suggested order quantities 11 and 22; both have weeks of cover 0.0, so they are sorted by product number |
| E25 | R-14 step 4 (Should) | 4-week cycle. Year 1: 0, 20, 30, 20. Year 2: 0, 18, 30, 22. Seasonal adjustment on; moving average, window 3 | The mean of week number 1 is 0, so seasonal adjustment is not used; a note is shown; the week forecasts are (18 + 30 + 22) / 3 = 23.333 |
| E26 | R-14 step 4 (Should) | 4-week cycle. Year 1: 10, S, 30, 20. Year 2: 12, S, 30, 22. Seasonal adjustment on; moving average, window 3 | Week number 2 has no calculation week, so seasonal adjustment is not used; a note is shown; the week forecasts are (12 + 30 + 22) / 3 = 21.333 |
| E27 | R-14, R-7, R-8 (Should) | E14 with seasonal adjustment on, scenario percentage 10%, safety margin 10%, stock on hand 5 | Week 1: normal 10.982, optimistic 12.080, pessimistic 9.883. Suggested order quantity: 10.982 × 1.1 − 5 = 7.080, rounded up to 8. Weeks of cover 0.455 (shown as 0,5). Using the base forecast 20.216 instead would wrongly give 18 |
| E28 | R-5 (Must) | Sales 10, 12, 14, 16, 18, 20; moving average, window 3 | Base forecast 18.0, while the trend would continue to 22: the forecast lags behind the trend, with no warning (a stated limitation) |
| E29 a | R-16 (Must) | E7 | «lav» (4 valid weeks; the stockout warning is also listed) |
| E29 b | R-16 (Must) | 12 valid weeks, no active warning | «middels» (fewer than 104 weeks of sales history) |
| E29 c | R-16 (Must) | 104 weeks of sales history, all valid, one unusual week 50 weeks before the latest data week, nothing else | «høy» |
| E29 d | R-16 (Must) | As E29 c, but the unusual week is in the recent period | «middels» (1 unusual week in the recent period) |
| E29 e | R-16 (Must) | E11 b | «lav» (the no-forecast condition is checked first) |
| E29 f | R-16 (Must) | 104 weeks of sales history with 3 stockout weeks, all before the recent period (101 valid weeks), nothing else | «høy» |
| E29 g | R-16 (Must) | As E29 f, but with 5 such stockout weeks (99 valid weeks) | «middels» (fewer than 100 valid weeks) |
| E30 | R-17 (Should) | E14 data with seasonal adjustment off, then on | Indices 0.5432 and 1.4815 are outside 0.7 to 1.3, so the product has a seasonal pattern. Off: seasonal-pattern warning, label at most «middels». On: no seasonal-pattern warning |

## 6. Quality, AI Guardrails and Delivery

### 6.1 Cross-Cutting Non-Functional Requirements

- **NFR-1 Local and free to run.** The application and every Must feature run on one computer without paid services, API keys or third-party accounts. After installation, the local app runs without an internet connection: all assets, including the chart library, are served locally and not from a content delivery network. The README covers macOS and Windows. The published version (DR-10) uses only free plans; only the group member who publishes it needs accounts there, and users and the examiner need nothing but a browser.
- **NFR-2 Correct, testable calculations.** All rules in §5 live in one calculation module with no dependency on the user interface or the database. Automated unit tests check every rule and every reference example that applies to the features built (SM-1), and all tests run with one documented command that needs nothing beyond the README's installation steps; the README shows the expected result.
- **NFR-3 Security.** Passwords are hashed with an established, secure implementation as described in FR-1, never a self-made algorithm. The logged-in company is checked on the server on every request (FR-2). The secret used to sign sessions is created automatically by the load command (DR-4) when it is missing, stored in a local file that `.gitignore` excludes (DR-2), and never committed; setup needs no manual file editing. In the published version, the secret is an environment variable on Vercel instead. The repository contains no secrets; optional configuration is listed in `.env.example`.
- **NFR-4 Privacy.** Only synthetic data is used: no real company, customer or personal data. Files in the repository contain no personal data and no local file paths. Saved AI sessions are cleaned of personal data and local paths before they are committed, and before submission the group scans the whole repository history for secrets, personal data and local paths and records the result in the QA log (DR-9).
- **NFR-5 Language and number format.** All screens, messages, warnings, notes and explanations are in Norwegian `[ASSUMPTION: bokmål]`. Numbers use a decimal comma; percentages are whole numbers with «%».
- **NFR-6 Platform and screen size.** Prognose runs in a desktop browser on a laptop or PC, because the user plans at an office PC (UJ-1). The README names at least one current browser per operating system that the group has tested. From 1024 pixels wide upwards there is no horizontal page scrolling; narrower windows stay readable, without overlapping or cut-off content. FR-25 sets what must be visible without scrolling at 1366 × 768. A mobile layout is not required.
- **NFR-7 Readable markings.** In the chart, stockout weeks, unusual weeks and level-shift weeks differ by more than color alone (for example by shape or pattern), and a legend explains them.
- **NFR-8 Responsiveness.** `[ASSUMPTION]` With 50 products of 104 weeks each, the product overview and the product screen open within 2 seconds on an ordinary laptop, and results update within 2 seconds after a settings change. The target applies to the local app. In the published version, the first request after a quiet period may take longer, because the free plans start the server and the database on demand.
- **NFR-9 Simple architecture.** One web application with one database and no more parts than the app needs: SQLite when the app runs locally, and PostgreSQL in the published version (DR-10). The technology is decided in the architecture step; the research recommendation and its rationale are in `addendum.md` (§2 there).
- **NFR-10 Robustness.** Numeric fields accept a decimal comma or a decimal point. Empty or non-numeric input is refused with a Norwegian message, and the previous value stays. No address or input shows a stack trace or a debug page; an unknown address shows a "not found" page in Norwegian with a link to the product overview. Submitting the same change twice, reloading a page or going back gives the same result without errors.
- **NFR-11 Basic accessibility.** Text contrast meets WCAG 2.2 level AA. Every function works with the keyboard alone, with a visible focus. Every form field has a visible label. Pages declare Norwegian as their language. The chart has a text alternative: a short summary and a table with the plotted values; its markings follow NFR-7.

### 6.2 AI Guardrails

- **AG-1 No numbers from AI.** Forecasts, scenarios, order quantities, weeks of cover, warnings, notes and confidence labels come only from the rules in §5.
- **AG-2 Explanation without a language model.** The Must explanation is template-based and needs no language model (FR-26).
- **AG-3 Optional local model under control.** The optional language model runs locally, is off by default, only rephrases, and falls back to the template explanation in every case that FR-28 lists.
- **AG-4 Labeled AI text.** Text written or rephrased by a language model is labeled and kept apart from the calculated numbers (FR-27).
- **AG-5 No external AI services.** Version 1 sends no data to external AI services.
- **AG-6 AI in development is documented.** How BMAD and Claude Code were used to plan and build Prognose is documented (DR-5).

### 6.3 Delivery and Repository Requirements

- **DR-1 README.** The README covers:
  - What Prognose does and who it is for, with screenshots of at least the login page, the product overview and the product screen (Must). A screen recording of UJ-1 steps 1 to 4, at most 2 minutes long, is optional.
  - Prerequisites with minimum versions.
  - Setup on macOS and Windows, tested by the group from a fresh clone: exact commands to copy into macOS Terminal and Windows PowerShell, including activating the virtual environment; how the session secret is created (NFR-3); and fixes for the most likely setup errors. Once SM-2 is confirmed, the README states the setup time.
  - The customer numbers and passwords of the two test companies, how to generate and load the synthetic data, and that reloading the data resets the settings and adjustments (DR-4).
  - The address of the published version, and for the group the steps to publish it and to load the seed data into its database (DR-10).
  - A «Prøv selv» (try it yourself) section of 5 to 10 steps that follows UJ-1, and a table of the test products naming the rule, warning or confidence label each one shows and its reference example (E-n).
  - How to run the tests, with the expected result (NFR-2), and the browsers tested (NFR-6).
  - How to switch on the optional language model as a separate step: which model is used, its download size and expected download time, its license obligations, and what happens without it (FR-28).
  - An overview of the folders and links to the planning and process documents: this PRD, the architecture, the epics and stories, the decision logs, the AI steering log (DR-5), the QA log (DR-9) and the status table (DR-8).
  - The known limitations: the trend lag (FR-7), the limitations of R-14, the assumptions behind the suggested order quantity (R-8), and the project-defined rules.
  - Any Should item that was not built, with the reason (§8.2, DR-8).
- **DR-2 Repository layout.**
  - The synthetic data, its generator script, the reference spreadsheet, the documentation, the saved AI sessions and the planning artifacts each have a documented place. The concrete folders are fixed in the architecture step.
  - The README explains every top-level folder, including the BMAD and Claude Code folders. The root holds no loose files other than the README, a license and configuration files.
  - A `.gitignore` keeps out the virtual environment, caches, test and coverage output, the local database file, `.env`, the session-secret file, and operating-system and editor files. The generated seed data is versioned; the database is not.
  - `.env.example` lists optional configuration, and no secrets are committed.
  - One formatter and one linter, chosen in the architecture step, run with a documented command and pass on the submitted commit. Dependencies are pinned to exact versions in one file.
- **DR-3 Reference spreadsheet.** The group stores a spreadsheet in the repository with the hand-calculated reference examples E1 to E30 and the expected results for every rule test product (FR-3). The automated tests use the same inputs and expected results, so the examiner can compare the two.
- **DR-4 Seed data.** The deterministic generator script (FR-3) creates the data, and one documented command loads it. Running the load command again resets the database to the seed state without duplicates or errors; the README says that this also resets the settings and adjustments.
- **DR-5 Process documentation, AI use and traceability.**
  - Decisions are recorded with their rationale (BMAD logs and session logs).
  - The prompts and AI sessions for each story are saved in the documented folder (DR-2), cleaned as NFR-4 requires.
  - An AI steering log records at least five cases, at least one per epic, where the group clarified, rejected or corrected AI output. Each case records what the AI proposed, what was wrong, what the group decided, and the commit or pull request. The planning phase already gives its first entries, for example the rounding error found in E5 and the processing order of R-10 and R-11.
  - Every story names the FR-n it implements, every test names the FR-n or E-n it verifies, and every commit names its story, so that each FR can be traced from this PRD to code and tests.
  - The change-log rule in §12 also applies to the architecture, UX and epics documents, and the Product Brief is updated after approval (§10, question 6).
- **DR-6 Deadline.** The submission deadline is 1 December 2026, and the work is planned backwards from it. Milestone dates and the order of the Should items are set in sprint planning. Should and Could items start only after the Must scope passes SM-1 and SM-3 (§9).
- **DR-7 Workflow.**
  - Each story is built on its own branch and merged through a pull request that names the story and its FR-n and says what was tested; review comments stay in the pull request.
  - Defects and open points are tracked as issues.
  - Commits are small and pushed as the work happens, so that the commit history covers the whole build period.
  - **Definition of Done.** A story is done when its tests and the linter pass; it has no commented-out, unused or duplicated code; the status table and the affected documents are updated; and its pull request has been reviewed.
- **DR-8 Status table.** One table lists every FR with its priority, its status at submission (built, partly built, not built or changed), its stories and tests, and the reason for any deviation. The README links it.
- **DR-9 QA log.** Every defect in AI-generated code or text that a test, the reference spreadsheet, a review or a manual test finds is recorded with how it was found, the fix and the commit or pull request. A manual test checklist for NFR-6, NFR-7, NFR-8, NFR-11, SM-2 (including the offline start) and SM-9 is run on the final commit and recorded with date, operating system, browser and result.
- **DR-10 Publishing.** Prognose is published on Vercel from the `main` branch, with the same code as the local app.
  - The published version uses a PostgreSQL database. Vercel and the database run on free plans, with no paid services.
  - The examiner can open the address, log in as a test company and see the product overview without installing anything (SM-9).
  - It holds only the synthetic seed data and is a shared demo: anyone with the logins in the README can change a test company's settings, and the load command restores the seed state (DR-4).
  - Debug pages are off, and secrets are environment variables on Vercel, never in the repository (NFR-3, NFR-10).
  - The optional local language model (FR-28) is not available there; the template explanation is shown.

## 7. Non-Goals (Explicit)

- Prognose does not place orders or send anything to suppliers, and it does not make the purchasing decision: it recommends, and the user decides.
- No editing of products, sales history or stock on hand in the app: that data comes from the seed data. Only the settings and adjusted order quantities can be changed.
- No ERP or MRP II functions: no bills of materials, production planning, master production scheduling or S&OP in version 1.
- No supplier integrations, campaign or market data, or incoming customer orders: each new signal would need its own rules and test data.
- No import of real company data; version 1 uses the synthetic seed data only.
- No hosted AI services, no AI-generated numbers and no advanced machine learning.
- No paid hosting, custom domain or uptime guarantee: the published version runs on free plans (DR-10).
- No trend method (such as Holt's linear method) and no seasonal naive benchmark; the trend lag is a stated limitation.
- No flagging of unusually low sales: weeks with low sales are never unusual weeks (R-10). Stockout weeks are handled by the stockout flag.
- No lead time, open orders, pack sizes, minimum order quantities or statistical safety stock (z × σ); the safety margin is a simple percentage.
- No warning about the age of the stock-on-hand figure, because the stock on hand always refers to the latest data week.
- No self-registration, password reset, several users or roles per company, or enterprise-level security.
- No mobile app.

## 8. MVP Scope

### 8.1 In Scope (Must)

- Login and company data isolation: FR-1, FR-2 (§4.1).
- Synthetic data stored in the database: FR-3, FR-4 (§4.2).
- Forecast calculation and insufficient data: FR-5 to FR-8 (§4.3).
- Scenarios, suggested order quantity and the order calculation line: FR-10 to FR-12 (§4.4).
- Stockout weeks, unusual weeks, level shift (calculation and label), old-data warning and confidence label: FR-15 to FR-19 (§4.5).
- Company-wide settings: FR-20 to FR-22 (§4.6).
- Product overview, product screen and forecast calculation: FR-24, FR-25, FR-35 (§4.7).
- Template explanation, kept apart from the numbers: FR-26, FR-27 (§4.8).
- Publishing on Vercel: DR-10 (§6.3).
- All non-functional requirements, AI guardrails and delivery requirements in §6.

### 8.2 Should (after the Must scope passes SM-1 and SM-3)

- Seasonal adjustment and the seasonal-pattern warning: FR-9, FR-36 (§4.3, §4.5).
- Order quantity per scenario and overstock note: FR-13, FR-14 (§4.4).
- Level-shift warning text: FR-17, warning part (§4.5).
- Optional local language model: FR-28 (§4.8).
- Adjusting order quantities and the combined order overview: FR-29, FR-30 (§4.9).

Seasonal adjustment was suggested in the Product Brief and by the teacher, and was moved to Should to protect the core flow before the deadline; the rationale is in `addendum.md` (§6 there). Until FR-9 and FR-36 are built, the week forecasts are flat (FR-7 note), and a product with a seasonal pattern gets no warning. Any Should item that is not built is listed with its reason in the status table (DR-8) and the README.

`[NOTE FOR PM]` With the deadline on 1 December 2026, the Should items are at risk. Their order is decided in sprint planning (§10).

### 8.3 Could (only if time allows)

- Settings per product: FR-23 (§4.6).
- Saving adjustments and marking products as approved: FR-31 (§4.9).
- CSV export: FR-32 (§4.9).
- Note that stock will not last through weeks 2 and 3: FR-33 (§4.9).
- Forecast accuracy (MAE): FR-34 (§4.9).

### 8.4 Out of Scope

Everything in §7.

## 9. Success Metrics

**Primary**
- **SM-1 Correct calculations.** For the Must scope, 100% of the reference examples for Must rules pass as automated tests and match the reference spreadsheet (DR-3): E1 to E13, E15 to E21, E23, E24, E28 and E29. When FR-9, FR-13 and FR-36 are built, E14, E22, E25 to E27 and E30 must pass too. Validates FR-5 to FR-13, FR-15 to FR-19, FR-35, FR-36 and rules R-1 to R-17.
- **SM-2 Runnable by the examiner.** From a fresh clone, following only the README, a person can log in as a test company and see the product overview on macOS and on Windows, without paid services or keys; after installation, the app also starts and works with the network switched off. Target: at most 15 minutes from clone to logged in, to be confirmed by testing (§10, question 2; DR-9). Validates NFR-1, DR-1, DR-4.
- **SM-3 Core flow works.** Log in; select a product; see the sales history, forecast calculation and scenarios; change the forecasting method, safety margin or unusual-week setting; and see the affected value change (FR-21). At least one automated test runs this flow through the web application. Validates FR-1, FR-10, FR-20, FR-21, FR-24, FR-25, FR-35.

**Secondary**
- **SM-4 Isolation.** The two-account isolation test passes, including lists. Validates FR-2.
- **SM-5 Persistence.** Data and settings are unchanged after a restart. Validates FR-4, FR-22.
- **SM-6 Explanation integrity.** Every number in every template explanation comes from the calculation result. With the optional language model, rephrased text is never accepted if it changes a number or attaches a number to a different label. Validates FR-26 to FR-28.
- **SM-7 Rule coverage.** Every warning and every confidence label, including «høy», is triggered by at least one test product in the dataset. Validates FR-3, FR-15 to FR-19.
- **SM-8 Traceable process.** Decisions and the use of AI during development are documented, the AI steering log has at least five cases linked to commits or pull requests, every story was merged through a reviewed pull request, and the status table traces every FR to the stories and tests that implement and verify it. Validates DR-5, DR-7, DR-8, DR-9.
- **SM-9 Published version works.** On the published address, a person can log in as each test company, see the product overview, and run the core flow in SM-3 by hand. Checked after the first deployment and on the final commit (DR-9). Validates DR-10, FR-4.

**Counter-metrics (do not optimize)**
- **SM-C1 Forecast accuracy.** Accuracy is not pursued through more complex models at the cost of rules that can be checked by hand. Counterbalances SM-1.
- **SM-C2 Feature count.** No Should or Could item is started before the Must scope passes SM-1 and SM-3. Counterbalances scope growth.
- **SM-C3 Share of «høy» confidence labels.** A high share of products with the confidence label «høy» is not a goal; warnings are never weakened to make the labels look better. Counterbalances SM-7.

**Mapping to the Product Brief's success criteria (§7 of the brief)**

| Success criterion in the brief | Success metric |
|---|---|
| Businesses can log in and see only their own data | SM-4 |
| Sales data is stored between sessions | SM-5 |
| Forecasts can be calculated for individual products | SM-1, SM-3 |
| The three scenarios are shown clearly | SM-3 |
| Changing the settings changes the results | SM-3 |
| Calculations match independently checked examples | SM-1 |
| AI explanations are separated from calculated results | SM-6 |
| The app runs locally with documented instructions and synthetic data | SM-2 |
| The use of AI during development is documented | SM-8 |

## 10. Open Questions

1. **Order of the Should items.** Which Should items come first in the time left before 1 December 2026 (seasonal adjustment and the seasonal-pattern warning, optional language model, adjusting order quantities)? Decided in sprint planning, together with the milestone dates.
2. **Setup time.** Is the 15-minute setup target (SM-2), including the offline check, met on clean macOS and Windows machines? Answered by testing before the README is final, and again on the final commit.
3. **Sources for the inventory rules.** The research found only vendor sources and one short university tutorial for the order-up-to policy, and no source for a percentage safety margin. Textbook references are added if found; otherwise the gap is stated in the process documentation.
4. **Project-defined rules.** Do R-10, R-11, R-14 and R-17 behave as expected on the test products? Pass criterion: for every rule test product, the app's results equal the expected results in the reference spreadsheet (DR-3).
5. **Local model choice.** If FR-28 is built, which small model is used, and what does its license require? Candidates are in `addendum.md` (§3 there).
6. **Update the Product Brief.** After this PRD is approved, the Product Brief is updated with the changes listed in `addendum.md` (§7 there), so that the repository history shows how the plan developed. Owner: the group.

## 11. Assumptions and Rule Sources

**Inline assumptions**
- §3 Week: a calendar week identified by year and week number.
- FR-17 / R-11: the level-shift rule is project-defined and validated with test products.
- FR-28: when the language model gives no answer within 10 seconds, the template explanation is used instead.
- R-12: products without a forecast are listed right after the products with order-soon status.
- R-14: the data uses week numbers 1 to 52; a week 53 would use the index of week 52.
- R-17: a seasonal pattern is an index of 1.3 or more, or 0.7 or less.
- NFR-5: the Norwegian is bokmål.
- NFR-8: pages open, and results update, within 2 seconds with 50 products of 104 weeks.

**Rules and thresholds by source status**
- **Sourced:** the moving-average and exponential-smoothing formulas and the start value (R-3, R-4); flat week forecasts and the trend lag (R-5); the deseasonalize, forecast and reseasonalize step (R-14 step 3).
- **Partly supported:** leaving stockout weeks out (R-1); the order rule as a simplified weekly order-up-to policy (R-8).
- **Project-defined** (from the Product Brief or decided in planning; each is covered by reference examples or test products):
  - Skipping weeks that are not calculation weeks (R-2 to R-4).
  - Minimum 3 valid weeks for a forecast (R-6).
  - Scenarios as a fixed plus or minus percentage (R-7), and the safety margin as a percentage of the forecast (R-8): simple rules of thumb, not statistical methods.
  - Rounding to 6 decimals before rounding up, and the display rounding (R-9).
  - The outlier rule, more than 2 × the baseline (R-10; threshold from the brief), and the level shift of 3 or more unusual weeks in a row (R-11).
  - The order-soon trigger and the sort order (R-12), and one stock-on-hand value per product (R-13).
  - The simple seasonal index (R-14 steps 1, 2 and 4), with the limitations in §5.5.
  - The recent period of 12 weeks, the old-data warning after 8 weeks, and the confidence thresholds: 12 valid weeks for «middels», and 104 weeks of sales history with at least 100 valid weeks for «høy» (R-15, R-16).
  - The seasonal-pattern thresholds of 0.7 and 1.3 (R-17).
  - Defaults and ranges: window 3 (2 to 12) and smoothing factor 0.3 (0.1 to 0.9) from the brief; scenario percentage 10% from the brief, with the range 0% to 50%; safety margin 10% (0% to 100%); unusual weeks included; seasonal adjustment off.

## 12. Change Log

This PRD was approved and set to final on 2026-11-03. Every change to a requirement, priority, rule or reference example after that date is recorded here, with the date, the reason, and the commit or pull request. The architecture, UX and epics documents follow the same rule. Changes made before approval, including the changes from the Product Brief, are listed in `addendum.md` (§7 there).

| Date | Change | Reason | Commit or pull request |
|---|---|---|---|
| 2026-11-08 | Vercel is the publishing solution. New DR-10 and SM-9; updated FR-4, NFR-1, NFR-3, NFR-8, NFR-9, DR-1, DR-9, §1, §7, §8.1 and the summary at the top. The local app keeps SQLite, and the published version uses PostgreSQL. | The group chose Vercel for publishing. The technical choices are in the architecture spine (AD-13, AD-15, AD-16). | Not committed yet |
