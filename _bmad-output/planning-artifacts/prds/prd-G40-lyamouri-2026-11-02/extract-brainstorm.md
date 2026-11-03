# Brainstorm extract for the PRD: Prognose

Sources: `_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/brainstorm-intent.md` ("intent"), the session log `.memlog.md` in the same folder ("log"), and the user's open-points list `.logs/<user>/issues.md` (Norwegian; translated here). Extracted 2026-11-02.

Refs: `[Lnn]` = log line tagged "decision by user"; `[Lnn idea]` and `[Lnn direction]` = tagged "idea by user" and "direction by user"; `(Lnn)` = any other log line (coach entries, questions, untagged). Sections 4 and 5 separate coach proposals from user decisions and show where a decision in section 3 confirms a coach proposal.

## 1. Core job statement

> "As purchasing manager I want to know how much to order of each product, based on past sales and expected demand; goal is to avoid both empty shelves and overstock, with a clear basis for purchasing decisions." [L12 idea]

What matters most, from the closing entry labelled "User's synthesis" (L81, no speaker tag): "a working website that computes good forecasts and helps plan purchasing; calculations understandable; system warns when data is uncertain; keep it simple, follow teacher requirements, finish by deadline". The intent narrows the job to "next week" (from [L60]) and turns the synthesis into a priority order that leaves out "follow teacher requirements".

## 2. Weekly flow as narrated [L31 idea]

1. After login, see the product overview with stock and which items need ordering soon.
2. Pick a product and see past sales, expected demand and the suggested order quantity.
3. Check warnings and outliers before deciding the quantity.
4. End with a combined order overview to plan purchasing efficiently.

The cycle is weekly because orders are placed weekly [L40]. Added later by the user: the planner can adjust the suggested quantity [L35], and there is no system for placing actual orders [L36]. In the agreed MoSCoW, steps 1–3 are Must, while manual adjustment and step 4 are Should. The "order soon" rule behind step 1 is still open (section 7, item 6).

## 3. Decisions by the user

- **Flow and screens**
  - Weekly flow: product overview, then product screen, then a check of warnings and outliers, then a combined order overview (section 2). [L31 idea]
  - Product screen: a clear overview with a chart of past and expected sales, current stock, safety margin and suggested order quantity. [L18 idea]
  - The calculation must be visible so the user understands the recommendation. [L19 idea]
  - The system explains any outliers and warns when the data basis is uncertain. [L20 idea]
  - The planner can manually adjust the suggested order quantity. [L35]
- **Period and data**
  - The period is the week (orders are placed weekly); the forecast horizon is the next 3 weeks. [L40]
  - Synthetic data: 104 weeks (2 years) per product as the rule, so seasonal variation can be compared between two years; plus some test products with shorter history. [L43]
  - Current stock lives as a column in the synthetic data. [L15]
  - Seasonal variation must affect the forecast calculation itself, not just the chart, through a simple adjustment that is easy to understand and check (later moved to Should [L77]). [L47]
- **Order quantity**
  - The system computes the suggested order quantity automatically. [L15]
  - It covers next week only, including safety margin and available stock; the week 2 and 3 forecasts are for further planning and are not summed into one order. [L60]
  - It is based on the normal scenario by default, with the safety margin added on top. [L63]
  - Optimistic and pessimistic are shown as alternatives so the user can compare them. [L63]
  - Never negative (shows 0 when stock covers demand); rounded up to whole units; no pack sizes in v1. [L65]
- **Data-quality rules and thresholds**
  - Stockout periods are excluded from the forecast calculation, since their sales do not reflect real demand; the user is warned, and if too little data remains the forecast is marked uncertain. [L28]
  - Zero sales from no demand must be told apart from zero sales from a stockout (the user's worst case: a product selling 100 a week is out of stock for 4 weeks). [L51 idea]
  - The moving average skips stockout weeks and uses the last 3 valid weeks; old valid data or too short a history gives an uncertainty warning. [L54]
  - Sales that stay at a higher level for 3+ weeks are a possible new normal level, not outliers; the forecast takes the increase into account and a message says demand has changed. [L58]
  - A forecast is shown only with at least 3 valid weeks. [L68]
  - Uncertainty warning if the latest valid sales data is older than 8 weeks. [L68]
  - If the chosen moving-average window is larger than the number of valid weeks, show an insufficient-data message and do not compute with that window. [L72]
  - Warning triggers the planner would not trust: large sales outliers, seasonal variation, stockouts, missing history, uncertain stock level; the system warns and explains why. [L24 idea]
- **Confidence badge**
  - A data-confidence badge (high/medium/low) per product, with plain-language reasons. [L23]
  - Low = fewer than 12 valid weeks [L68]; medium = 12–103 valid weeks or active notes; high = 104+ valid weeks and no active warnings [L71].
- **Scope**
  - Keep it simple: no advanced inventory system. [L15]
  - No system for placing actual orders; focus stays on forecasting, demand calculation and purchase planning as in the Product Brief; CSV export is a nice-to-have if time allows. [L36]
  - Prioritise must-have vs can-wait, keeping the project realistic and in line with the Product Brief and teacher requirements and feedback. [L74 direction, L77]
  - Seasonal adjustment moves from Must to Should to keep the project feasible; the template explanation without a paid API stays Must. [L77]
  - Adjustments A, B and C are approved (section 6); the priority is a working solution by the deadline. [L80]

## 4. Coach proposals the user accepted

At the start the user delegated the session-setup choices to the coach ("use coach's proposals and the Product Brief as basis; no extra inputs", L9). That is not counted here as accepting later proposals.

- **accepted**: order quantity = forecast + safety margin − stock, so stock must be in the data (gap raised at L13; lead time became Won't) → [L15] [L60].
- **accepted**: a visible calculation (L16) → [L19 idea]. The one-line format and its example (120 + 12 − 40 = 92) are the coach's wording.
- **accepted**: a data-confidence badge with plain-language reasons (L21) → [L23]. The final levels use valid-week counts and active notes [L68] [L71], not the coach's example criteria (share of outliers, zero-sales gaps).
- **accepted**: zero sales during a stockout are not zero demand (L25) → [L28] [L51 idea].
- **accepted**: the combined overview stays a list of suggested quantities, not an ordering system (L33) → [L36].
- **accepted**: the period follows the ordering cycle, i.e. the week (L39) → [L40]; 104 weeks so seasonality can be checked against a repeat year (L41) → [L43].
- **accepted** in principle: seasonality changes the forecast through a simple adjustment (L45) → [L47]; the specific method is not confirmed (section 5).
- **accepted**: isolated spikes of 1–2 weeks are outliers, while 3+ consecutive high weeks are a new demand level shown as a note, not excluded (L57) → [L58].
- **accepted**: the order quantity is floored at 0 and rounded up to whole units (L61, L64) → [L65].
- **accepted**: "old" valid data means older than 8 weeks (suggested as "e.g. 8 weeks?" in a question, L55) → [L68]; no forecast with fewer valid weeks than the moving-average window (L66) → [L72]; the medium and high confidence definitions (L70) → [L71].
- **accepted**: the proposed MoSCoW (L76, tagged "decision by coach") with the user's changes [L77]; alignment adjustments A, B and C (L78) → [L80].
- **accepted** only as part of the agreed MoSCoW, never confirmed one by one: stockout flag per week in the data (L26; Must); overstock note when stock exceeds need (L61; Should; the user's reply at L65 left it out); warning that stock will not last weeks 2–3 (L61; Could).

## 5. Coach proposals not confirmed by the user

- **unconfirmed**: the real job is "never be blamed for an empty shelf or overstock"; the tool is hired for defensible decisions (L11).
- **unconfirmed**: a product list with a status per product (order now / ok / overstock), sorted by urgency, for the weekly review of 10–50 products (L22). The user said only "stock and which items need ordering soon" [L31 idea].
- **unconfirmed**: "order soon" = stock coverage = stock ÷ forecast per week (e.g. "stock lasts 1.4 periods"), which avoids lead time in v1 (L32; still listed as unconfirmed at L37).
- **unconfirmed**: a stock as-of date in the data, where a stale date triggers an "uncertain stock" warning (L26). The user did name "uncertain stock level" as a warning trigger [L24 idea].
- **unconfirmed**: seasonal method: divide history by a week index, forecast, multiply back (L45), applied only with enough history (e.g. 104 weeks), otherwise a non-seasonal forecast with a note (L66). The method was left to research (L48).
- **unconfirmed**: the outlier check starts only once 3 valid preceding weeks exist (L66).
- **unconfirmed**: the outlier median uses the 3 preceding valid (non-stockout) weeks, so the first normal week after a stockout is not flagged (L52). There is no direct user reply, yet the intent lists it as a decision; it is consistent with, but not stated in, the user's stockout exclusion [L28].
- **unconfirmed**: short-history products double as test cases for the low-confidence badge and the too-little-data warning (L44).
- **unconfirmed**: closing connections (L82; the log ends without a user reply): one data-quality layer feeds calculation, badge and explanations; the 4-week stockout case is the central test; structured warnings plus visible calculation make the template explanation cheap and keep AI apart from the numbers; the 104-week dataset serves as test suite, README demo and repo asset; the differentiator vs a spreadsheet is that "the system tells you when not to trust it".

## 6. MoSCoW as finally agreed

Proposed by the coach (L76); the user moved seasonal adjustment to Should and kept the template explanation as Must [L77], then approved A, B and C [L80], and did not comment on the other placements. Item wording follows the intent; italic notes are added here. These intent details are not in the log's MoSCoW entry, and the log does not show their source: "customer number and password", the list of adjustable settings, "test account", "visibly separated from calculated results", "MAPE".

- **Must**
  - Login with customer number and password; each business sees only its own data.
  - Database with synthetic data (104 weeks, stock, stockout flag, short-history test products).
  - Moving average and exponential smoothing in a separate, testable module; 3-week forecast; three scenarios; adjustable method, window, factor, scenario percentage, safety margin and outlier handling.
  - Order suggestion with visible calculation.
  - Product screen with chart; product overview with stock and "order soon".
  - Outlier, stockout and new-level rules; confidence badge and warnings (all thresholds; see section 3). — *B: the new-level calculation is Must.*
  - Template-based explanation that needs no paid API, visibly separated from calculated results. — *Kept Must by the user [L77].*
  - README with test account; tests against hand-calculated answers.
  - Process and repo: documented decisions and AI use, `.env.example`, fixed location for seed data and generator script. — *Added by A.*
- **Should**
  - Simple seasonal adjustment that affects the forecast (cut from Must for feasibility). — *Moved by the user [L77].*
  - Language-model explanation when a key is available.
  - Manual adjustment of the suggested order quantity.
  - Combined overview of suggested quantities.
  - Message that demand level has changed (the rule itself is Must). — *Split by B.*
  - Scenario comparison for the order quantity; overstock note.
- **Could**: CSV export; saving manual adjustments between sessions; warning that stock will not last weeks 2–3; accuracy metric (MAPE).
- **Won't (this version)**: pack sizes, lead time, placing actual orders, campaigns, incoming customer orders.
- **Approved adjustments** (proposed by the coach at L78, approved [L80])
  - A: process and repo items the teacher weights heavily become Must: documented decisions and AI use, `.env.example`, location of seed data and script.
  - B: the new-level rule is split: its calculation (3+ high weeks are not outliers) is Must, since otherwise the outlier rule half-excludes level shifts; the message is Should.
  - C: seasonality as Should is a justified scope cut, but the brief and teacher suggested including it, so the PRD must state the cut, keep seasonal patterns in the 104-week test data and chart, and note that the forecast is non-seasonal at Must level.
- **Why seasonality moved to Should**: the user's reason was "to keep the project feasible" [L77], with "a working solution by the deadline" as the priority [L80]. The intent adds that it is the most demanding rule, with the fallback of showing seasonality in the chart with a note. The user's earlier decision that seasonality must change the forecast itself [L47] now applies at Should level.

## 7. Open items

From intent §4 (7 items) and every unchecked line in issues.md (16 lines; none is checked). The 7 intent items repeat the first 7 issues.md lines and are merged, leaving 16 distinct items. Lines dated 2026-10-31 come from the brainstorm session, those dated 2026-11-01 from the research-for-prd session. A tag at the end names the MoSCoW level of the agreed item it affects.

- **Forecast, outlier and seasonal rules**
  - **1.** Choose the seasonal method through research: index per week, estimation from two years, interaction with the outlier and stockout rules. [intent §4; issues 2026-10-31] (Should)
  - **2.** Clarify that weeks 2 and 3 equal week 1 without seasonal adjustment: show this in the interface, or raise seasonality's priority. [issues 2026-11-01] (Must, Should)
  - **3.** Choose the SES convention (NIST vs FPP3) and its initial value, and document the thresholds (3, 8, 12, 104 weeks; alpha 0.3) as assumptions in the PRD. [issues 2026-11-01] (Must)
  - **4.** Clarify the outlier check in the first weeks (proposal: starts once 3 valid preceding weeks exist) and median 0 without a stockout flag. [intent §4; issues 2026-10-31] (Must)
  - **5.** Choose the outlier rule: keep "2 × median" with a guard against median 0, or switch to Tukey/IQR or Hampel. The intent says the brief's 2× median rule "stays", but no user decision on it is logged. [issues 2026-11-01] (Must)
- **Stock, ordering and explanation**
  - **6.** Confirm "must be ordered soon" as stock coverage (stock ÷ expected sales per week). [intent §4; issues 2026-10-31] (Must)
  - **7.** Confirm a stock as-of date (coach proposal) as the trigger for an "uncertain stock level" warning. [intent §4; issues 2026-10-31] (not in MoSCoW)
  - **8.** Clarify whether manual adjustments of the order quantity are saved between sessions. [intent §4; issues 2026-10-31] (Could)
  - **9.** Clarify the content of the template-based explanation and the fallback for the language-model explanation. [intent §4; issues 2026-10-31] (Must, Should)
  - **10.** Ask the teacher about the AI requirement: must the app show a language model, or is a template-based explanation enough? [issues 2026-11-01] (Must, Should)
- **Delivery, documents and research**
  - **11.** Choose the technology stack and set the submission deadline. [intent §4; issues 2026-10-31]
  - **12.** Define data isolation between businesses (a filter in every query, one data-layer function) and a test with two accounts, in the architecture. [issues 2026-11-01] (Must)
  - **13.** Write and test the README setup sequence (venv, installation, migration, seeding, running). [issues 2026-11-01] (Must)
  - **14.** Update the Product Brief with the decisions from the session. [issues 2026-10-31]
  - **15.** Obtain textbook sources for research report B (may require poppler), or document that they are missing. [issues 2026-11-01]
  - **16.** Optional: catch up on the semantic source check, HTML summary and language polish of the research reports. [issues 2026-11-01]
- **Also unresolved in the log, but in neither list**
  - Whether stock is one snapshot value per product (asked at L17, not answered).
  - Whether the planner can approve quantities in the combined overview (asked at L34; the user answered only on adjusting [L35] and export [L36]).

## 8. Qualitative notes: what the user kept emphasising

- Keep it simple and testable: "keep it simple, no advanced inventory system" [L15]; "simple ... easy to understand and check; stay within school-project scope" [L47]; "keep rules simple and testable" [L68]; "keep it simple" [L72] (L81).
- Calculations the user can follow, as a clear basis for purchasing decisions [L12 idea] [L19 idea] [L47] (L81).
- Warn, and explain why, whenever the data is uncertain [L20 idea] [L24 idea] [L28] [L54] [L68] (L81); the user's own worst case is a stockout read as zero demand [L51 idea].
- A realistic project that works by the deadline and follows the Product Brief and the teacher's requirements [L36] [L74 direction] [L77] [L80] (L81).
- A forecasting and purchase-planning aid, not an inventory or ordering system, where the user can compare scenarios and override the suggestion [L15] [L36] [L63] [L35].
