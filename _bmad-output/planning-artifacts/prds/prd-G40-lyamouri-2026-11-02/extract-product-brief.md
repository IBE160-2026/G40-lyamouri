# Product Brief extract for PRD: Prognose

Source: `_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/brief.md` (front matter: `status: final`, created 2026-09-18, updated 2026-10-14). Extracted 2026-11-02. [§n] = brief section number. Text in quotes is verbatim. Nothing is added beyond the brief, except the observations in section 11.

## 1. Product in one paragraph
Prognose is "a website for small businesses that want to estimate future demand for their products" [§1]. Businesses log in with a customer number and password, see only their own historical sales data, and get forecasts calculated "with established statistical methods" (moving average and exponential smoothing). The forecasts are shown as three scenarios: optimistic, normal and pessimistic [§1, §3]. It is for a purchasing manager or inventory planner at a small business with about 10–50 products, who reviews the forecasts every week [§6]. Why: small businesses "can run out of products or hold too much inventory because sales are hard to predict" [§2]. AI explains the forecasts but "must not make up forecast numbers" [§1]. Context: a course project covering module 4.1, "Prognoser og Demand Management" (Forecasting and Demand Management), in IBE160 at Høgskolen i Molde [§1].

## 2. Problem statement
- "Small businesses can run out of products or hold too much inventory because sales are hard to predict." [§2]
- "Manual calculations can make it hard to understand sales trends and to handle unusual sales figures." [§2]
- "The goal is to make forecasting simpler, easier to understand, and easier to keep track of." [§2]

## 3. Users and usage context
- **Who:** "The main user is a purchasing manager or inventory planner at a small business" [§6].
- **Company size:** "small business". It is described only by product count; no headcount or revenue is stated [§1, §6].
- **Product count:** "about 10–50 products" [§6].
- **Review frequency:** "The user reviews the forecasts every week." [§6]
- **Access:** businesses log in with "a customer number and password" and get access to "their own historical sales data" [§1].
- **Data used:** historical sales data in a database [§3]; "The project uses synthetic business accounts and sales data." [§6]; "simple historical trend and seasonal patterns in the test data" [§8]; "synthetic datasets with known results" [§10].
- **Evaluator:** "The teacher must be able to run the website with a test account and a README" [§10].

## 4. Capabilities stated in the brief
**Product**
- C1. Login with customer number and password, "with access only to the business's own data" [§1, §3, §7].
- C2. "A database of historical sales data" [§3]; "Sales data is stored between sessions" [§7]; local database [§10].
- C3. "Charts of sales history and forecasts." [§3]
- C4. "Forecast calculation with moving average and exponential smoothing." [§1, §3]
- C5. Forecasts "for individual products and periods" [§7].
- C6. Three scenarios (optimistic, normal, pessimistic), "shown clearly" [§1, §3, §7].
- C7. "Adjustable forecasting method, safety margin, and handling of unusual sales figures" [§3]. The moving-average window, smoothing factor and scenario percentage are also adjustable [§4]. "Adjusting the settings produces visible changes in the results" [§7].
- C8. Suggested planning quantity: the safety margin is "added to the selected forecast" [§4].
- C9. Unusual sales figures are flagged (rule R8); "The user can choose whether to include or exclude them." [§4]
- C10. "The user can see which calculation method is used, adjust the assumptions, and understand why the forecast changes." [§5]
- C11. "AI-based explanations of the forecasts" [§3], "clearly separated from calculated results" [§7].
- C12. An alternative to the AI explanations "that needs no paid API" [§8].

**Delivery / project**
- C13. "synthetic business accounts and sales data" [§6]; "synthetic datasets with known results" [§10].
- C14. "The website can run locally with documented instructions and synthetic data" [§7]; a test account and a README, "without paid services or private API keys" [§10].
- C15. "The forecast calculations must be testable on their own." [§10]
- C16. "The use of AI during development is documented." [§7]; AI supports development "through BMAD and Claude Code" [§1].

## 5. Calculation rules (verbatim, §4)
The brief introduces them as "Proposed rules, to be validated during BMAD planning:"
- R1. Moving average: "average of the last 3 periods, with an adjustable window from 2 to 12 periods."
- R2. Exponential smoothing: "adjustable factor from 0.1 to 0.9, default 0.3."
- R3. Forecast horizon: "3 future periods."
- R4. Normal scenario: "the calculated base forecast."
- R5. Optimistic demand: "base forecast plus an adjustable percentage, default 10%."
- R6. Pessimistic demand: "base forecast minus the same percentage, never below zero."
- R7. Safety margin: "a separate adjustable percentage, added to the selected forecast when calculating a suggested planning quantity."
- R8. Unusual sales figures: "values above twice the median of the three preceding periods are flagged. The user can choose whether to include or exclude them."

Determinism and AI: "The calculations must be deterministic and possible to check by hand. AI must not generate the numerical forecasts." [§4] Related: "AI must not make up forecast numbers." [§1]; "Forecast calculations match independently checked examples." and "AI explanations are clearly separated from calculated results." [§7]

## 6. Success criteria (verbatim, §7)
- Businesses can log in and see only their own data.
- Sales data is stored between sessions.
- Forecasts can be calculated for individual products and periods.
- The three scenarios are shown clearly.
- Adjusting the settings produces visible changes in the results.
- Forecast calculations match independently checked examples.
- AI explanations are clearly separated from calculated results.
- The website can run locally with documented instructions and synthetic data.
- The use of AI during development is documented.

## 7. Scope (verbatim, §8)
**In scope:** "login, database, synthetic historical sales data, two statistical forecasting methods, three scenarios, adjustable settings, charts, simple historical trend and seasonal patterns in the test data, and AI explanations with an alternative that needs no paid API."

**Out of scope:** "bill of materials (BOM) structures, production planning, other MRP II modules, supplier integrations, actual orders, real-time market and campaign data, incoming customer orders, advanced machine learning, and enterprise-level security solutions."

Also: "Any future integration with other planning functions is outside this project version." [§9]

## 8. Differentiation and vision
- "Prognose is meant to be simple and clear. The user can see which calculation method is used, adjust the assumptions, and understand why the forecast changes." [§5]
- "The solution prioritizes transparency and ease of use over advanced enterprise features." [§5]
- Vision: "In the longer term, Prognose aims to make forecasting more accessible and easier to understand for small businesses." [§9]

## 9. Technical approach and testing constraints
- "Choose a simple, documented technical solution with a local database." [§10]
- "The forecast calculations must be testable on their own." [§10]
- "Use synthetic datasets with known results." [§10]
- "The teacher must be able to run the website with a test account and a README, without paid services or private API keys." [§10]
- The product is a website [§1]. The stack is not chosen yet: "Choose a simple technology stack during the BMAD architecture work." [§11]
- The calculations must be "deterministic and possible to check by hand" [§4] and must match "independently checked examples" [§7].
- The AI explanations need "an alternative that needs no paid API" [§8]. AI supports development "through BMAD and Claude Code" [§1], and its use is to be documented [§7].

## 10. Open questions (verbatim, §11)
- Confirm the final submission deadline.
- Choose a simple technology stack during the BMAD architecture work.
- Validate the calculation rules before implementation.
- Clarify how the AI explanations and the alternative without an API will work.

## 11. Ambiguities and gaps inside the brief
- O1 (observation): The front matter says `status: final`, yet §4 calls the rules "Proposed rules, to be validated during BMAD planning", and §11 still lists "Validate the calculation rules before implementation."
- O2 (observation): "Period" is never defined (week, month or other), although R1, R3 and R8 are all expressed in periods. The only time unit in the brief is the weekly review [§6].
- O3 (observation): R1–R8 do not fully fix the numbers that must be "possible to check by hand" [§4]. They give no starting value for exponential smoothing, do not say how the 3-period horizon is produced for either method, and give no rounding rule for percentage results.
- O4 (observation): Defaults and ranges are uneven. The moving-average default (3) is implied but not labelled "default". The scenario percentage has a default (10%) but no range. The safety margin has neither. No default forecasting method is named [§3, §4].
- O5 (observation): "the selected forecast" [R7] could mean the selected scenario, the selected method, or both. The brief does not say whether the quantity is per period or for the whole horizon. The suggested planning quantity appears only in §4, not in §3, §7 or §8.
- O6 (observation): R8 flags only values "above" twice the median, so low outliers are not covered. It does not cover the first periods, which lack three preceding periods, and does not say what "exclude" means for the moving-average window or the smoothing. No minimum history length is given, although the window goes up to 12 periods.
- O7 (observation): The brief does not describe how sales data gets into the system (entry, import or editing). It mentions only a database, storage "between sessions" and synthetic data [§3, §6, §7]. Whether user settings persist is not stated.
- O8 (observation): §8 puts "simple historical trend and seasonal patterns in the test data" in scope, but §4 has no rule for trend or seasonality. It is unclear whether the forecasts should reflect them.
- O9 (observation): The AI wording varies: "must not make up forecast numbers" [§1] vs. "must not generate the numerical forecasts" [§4], and "no paid API" [§8] vs. "without an API" [§11] vs. "without paid services or private API keys" [§10]. Whether explanations may quote calculated numbers is not stated.
- O10 (observation): The required security level is undefined. §7 requires that businesses "see only their own data", while §8 puts "enterprise-level security solutions" out of scope.
- O11 (observation): The success criteria are qualitative ("shown clearly", "visible changes", "clearly separated"). "Independently checked examples" has no stated number or tolerance [§7].
- O12 (observation): "individual products and periods" [§7] does not say what choosing a period means. No multi-product overview is mentioned, although about 10–50 products are reviewed every week [§6].
- O13 (observation): Terms vary: "Normal scenario" vs. "Optimistic demand"/"Pessimistic demand", and "base forecast" vs. "calculated base forecast" vs. "selected forecast" [§4].

## 12. Qualitative notes
- Simplicity dominates: "simple"/"simpler" appears in §2, §5, §8, §10 and §11, and the brief "prioritizes transparency and ease of use over advanced enterprise features" [§5].
- Numerical integrity is a hard rule ("must") in §1 and §4 and a success criterion in §7. AI only explains; the numbers come from the deterministic calculations.
- Understandability recurs as a goal ("understand" in §2, §5 and §9): show the method, let the user change assumptions, and show why the forecast changes.
- Reproducibility for an academic evaluator: local run, README, test account, synthetic data, and no paid services or private keys [§7, §10].
- Documentation is a deliverable in itself ("documented" twice in §7 and once in §10), including the use of AI during development.
- The tone is plain, concise and deliberately modest: nine out-of-scope items [§8], a small vision that excludes future integration [§9], and rules framed as "Proposed" and "to be validated" [§4].
