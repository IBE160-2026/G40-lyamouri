# Research extract for the PRD: forecasting (A) and safety stock / order quantity (B)

Extracted 2026-11-02 from two research reports dated 2026-11-01. Everything below comes from the reports; the one extractor note (section 7) is labelled as such.

- **Report A** (academic-lit; 4 of 8 load-bearing claims independently verified): `_bmad-output/planning-artifacts/research/academic-lit-forecasting-methods-seasonality-outliers-2026-11-01/research.md`
- **Report B** (domain; 3 claims verified, 4 unverified): `_bmad-output/planning-artifacts/research/domain-safety-stock-and-order-quantity-2026-11-01/research.md`
- **Keys:** [An] / [Bn] = source n in report A / B. A-inf / B-inf = the report's own inference or analysis, no source. A-R# / B-R# = the reports' recommendations (section 5); A-Q# / B-Q# = open questions (section 6).
- **Evidence caveat:** A rests mostly on one textbook (FPP3) or a few web pages, and several full texts could not be fetched. Every inventory-policy source in B is a vendor page or a short university tutorial; no textbook or professional-body source (e.g. ASCM) was readable. Re-check dates: A's software docs and `ets()` note by 2027-05-01, the stockout preprint [A22] by 2027-11-01; B's vendor practice claims by 2027-04-21 ([B6], 2023, is already stale).

## 1. Formulas and conventions the PRD can specify

- **Moving average (MA) of N periods:** forecast = mean of the most recent N values [A4][A5]; needs at least N values (A-inf). An m-term MA has average data age (m+1)/2 [A5]. Confidence: high for the definition (NIST source rated high); medium for data age (one source).
- **SES recursion:** level_t = alpha x y_t + (1 - alpha) x level_(t-1), with 0 <= alpha <= 1; the forecast is the latest level [A1]. alpha = 1 gives the naive forecast (last value); small alpha gives more weight to older data [A1]; average data age is 1/alpha [A5]. Confidence: high (formula); medium (data age).
- **SES indexing:** NIST (S_t uses y_(t-1)) and FPP3 (level_t uses y_t) index differently but give identical numbers; the PRD must pick one [A3][A1]. The section 7 fixture follows the FPP3 form with level_1 = y_1. Confidence: medium.
- **SES initialisation:** FPP3 estimates the initial level by optimisation, which cannot be done by hand [A1]. NIST lists hand-checkable starts: the first observation, or the average of the first four or five observations [A3]. A-R1 picks initial level = first valid observation (NIST option a). Confidence: medium.
- **alpha and window length:** no source gives a canonical default alpha. Examples use 0.2 to 0.5 [A5]; NIST starts a grid at 0.1 to 0.9 and picks alpha by minimum squared error [A3]. The brief's range 0.1 to 0.9 matches NIST's grid; the default 0.3 is consistent with example values but unsourced. Window length and alpha are usually chosen by best fit on past errors [A3][A5]. Confidence: low (default 0.3).
- **Flat multi-step forecast:** SES forecasts take the same value for every horizon h, which suits only series without trend or seasonality [A1]; long-range MA and SES forecasts are flat [A5]. Weeks 1, 2 and 3 therefore get the same number. No source discusses recursive versus flat; they coincide because the forecast equals the last level (A-inf). Confidence: high (verified; two publishers agree).
- **Standard order policy (periodic review, order-up-to):** Q = max(0, S - inventory position), where S = expected demand over review period T plus lead time L, plus safety stock, and inventory position = on hand + on order - backorders; no order when the position is at or above S [B2][B3][B5]. Worked example: 13 days x 20 bottles = 260, plus 40 safety stock = 300 [B3]. Confidence: medium (three publishers agree, two are vendors; NC State omits the inventory-position term).
- **Project order formula:** order = max(0, next-week forecast + safety margin - stock on hand), with the margin a percentage of the forecast. It equals order-up-to with T = 1 week and L = 0, a percentage in place of z x sigma x sqrt(T + L), and stock on hand in place of inventory position; that is the same only if nothing is on order (B-inf). With a lead time of one week or more, or open orders, the target must cover T + L and subtract stock on order [B2][B5]. Confidence: medium for the structure; the simplifications are B's own.
- **Non-negativity and rounding:** flooring the order at zero is explicit in the sources [B2][B5]. Rounding up to pack sizes with documented rules (64 rounds up to 70 for cases of 10) and modelling minimum order quantities explicitly (no formula given) come from one vendor [B2]. The intent document leaves pack sizes out of v1, so only "round up to whole units" is needed. Confidence: medium (floor); low (pack-size rounding, one vendor).
- **Weeks of cover ("order soon"):** weeks of supply = available inventory / average weekly units sold; the forward variant divides by forecast weekly sales [B6]. A procurement glossary defines coverage the same way, says lead time should always be shorter than coverage, and gives example triggers of 2 to 8 weeks varying by product group [B4]. The metric "does not determine a purchase order on its own" [B6] and assumes constant consumption, so seasonal demand needs an adjusted calculation [B4]. No ASCM, textbook or university source was found. B-R4: forward cover = stock / week-1 forecast, against a user-set threshold. Confidence: medium-low ([B6], vendor 2023); low ([B4]).

## 2. Rules that research shows are project-defined (no source)

Report A's summary: treat the outlier rule, the stockout rule, the level-shift rule and every numeric threshold as project-defined design decisions, because the research found no established rule for them. Report B adds the margin, the scenarios and the order-formula simplifications.

| # | Rule | What the research found | What the report recommends |
|---|---|---|---|
| 1 | Outlier: a value above 2 x the median of the three preceding periods | Not described by any source; a short-window variant of a rolling-median rule. If the three preceding values are 0, the limit is 0 and every positive value is flagged (A-inf). | A-R3: keep only as a documented project-defined rule with an explicit zero-median guard (e.g. do not flag when the median is 0, or require a minimum floor), or switch to Tukey 1.5 x IQR or Hampel and accept that those also need a zero guard. Basis: low-medium. |
| 2 | Exclude stockout weeks from the history | No source states that exclusion is the recommended simple treatment. It is consistent with "treat as missing" [A22], with FPP3's missing-value options [A13] and with the project's stockout flag: partial support. | A-R4: keep excluding, call it a design decision with partial support, and keep the stockout flag in the seed data. Basis: medium. |
| 3 | Moving average over the last N valid weeks | No source; the project's own rule. statsmodels exposes `missing='drop'` for exponential smoothing but does not say what a gap does to the fit [A20]. | No dedicated recommendation; left as open question A-Q3 (last N valid weeks versus shrinking the window). |
| 4 | Level shift: three or more consecutive high weeks | No source gives a simple rule. A level shift is a recognised outlier type separate from a one-off outlier [A16] (unverified); CUSUM detects small persistent shifts but is heavier than a counting rule [A17]. | A-R5: keep as a project-defined rule with a dedicated test series; it must be tested with synthetic data. Basis: low. |
| 5 | Numeric thresholds: 3 valid weeks, 8 weeks old, 12 weeks low confidence, 104 weeks high confidence, alpha default 0.3 | No basis found for any of them. Hyndman says there is no fixed minimum sample size and warns against unsubstantiated rules of thumb [A6]. Only the alpha range 0.1 to 0.9 matches a source (NIST's grid [A3]). | A-R6: record every threshold as an assumption in the PRD and README. Basis: low. |
| 6 | Safety margin as a percentage of the forecast | Not found in any source read; one vendor article says explicitly that it does not cover them [B1]. Closest finding: days-of-cover rules are easy to communicate but "rarely optimal, because they ignore variability and service levels", acceptable when data is unreliable or for new products [B1]. | B-R2: keep as an adjustable setting called a rule of thumb that ignores demand variability, never a service-level guarantee; name z x sigma safety stock as a possible later improvement. Basis: low. |
| 7 | Optimistic / pessimistic as a fixed plus/minus percent | No source shows it as a standard way to define scenarios; plus/minus 15% appears only in an unfetched template snippet. Practitioners and textbooks build the range from forecast error [B8][B11]. | B-R3: present as what-if scenarios, not confidence intervals or probabilities; base any later statistical alternative on forecast error [B8]. Basis: low. |
| 8 | Order-formula simplifications: weekly review, lead time zero, no open orders, stock on hand instead of inventory position, whole-unit rounding | The structure matches order-up-to [B2][B3][B5] (the floor at zero is sourced); the simplifications are B's own. | B-R1: document the formula as a simplified weekly order-up-to policy with an explicit assumptions list. Basis: medium for structure. |

## 3. Established alternatives the reports name

**Outliers and level shifts**
- **Tukey fences:** inner fences at 1.5 x IQR beyond the quartiles ("mild"), outer at 3 x IQR ("extreme") [A21]. FPP3 applies them to the remainder of a robust STL fit, not to raw sales, and prefers 3 x IQR [A13]. Confidence: high (verified).
- **Hampel identifier:** flag a value outside rolling median +/- 3 x 1.4826 x MAD [A14][A15] (default k = 3 [A15]). Fails the same way as the brief's rule when MAD = 0 (A-inf). Confidence: medium-high (two publishers agree).
- **Outlier replacement:** FPP3 calls replacing outliers without understanding why they occurred "a dangerous practice"; replacing is reasonable if they are errors or will not recur [A13]. Confidence: high (textbook).
- **Level shift versus outlier:** time-series outlier detection treats a level shift (LS) as a separate type from an additive outlier (AO) and a temporary change (TC) [A16] (medium; software docs, unverified). CUSUM charts detect small persistent mean shifts [A17] (medium).

**Stockouts, missing data and intermittent demand**
- **Censored demand:** when stock runs out, recorded sales understate true demand [A18][A22] (verified for the definition). Stockouts are generally handled as missing data, but a 2025 preprint argues they are missing not at random, so ordinary imputation is inadequate [A22] (medium; one preprint).
- **FPP3 missing-value options:** use only data after the last gap, or interpolate [A13]. In R, ETS and STL cannot take missing values while benchmark methods can [A13] (one R package, not the app's stack).
- **Unconstraining:** a 2012 survey lists five approaches, but only its abstract was readable and it concerns airline revenue management [A19] (medium).
- **Croston's method:** smooths demand sizes and intervals between demands separately; the standard route for many zero weeks; equations not retrieved, so out of scope for v1 [A23] (medium).

**Seasonality (A-R2 keeps seasonal adjustment as Should)**
- **Ratio-to-moving-average indices** (multiplicative classical decomposition): divide each value by a centred moving average (2x52 for weekly data, losing 26 weeks at each end), average the ratios per season, adjust the indices to add to m (average 1); forecast the adjusted series with any non-seasonal method, then multiply by the index [A7][A8]. Confidence: medium (normalisation step and three-step method unverified).
- **FPP3 warning:** classical decomposition "is not recommended, as there are now several much better methods"; it assumes a pattern that repeats identically and is not robust to unusual values [A7] (high).
- **Seasonal naive** (forecast = same week last year): the recognised benchmark any seasonal method should beat; trivial to check by hand [A2] (high).
- **Weekly specifics:** 52.18 weeks per year [A10]; most methods cannot handle a non-integer period; Fourier terms or STL are the alternatives but are not hand-checkable [A9] (high). Holt-Winters/ETS needs m-1 initial seasonal parameters; R's `ets()` capped the period at 24 in a 2010 note that may be stale [A11] (medium). SAS recommends several complete cycles, at least two years for monthly seasonality [A12] (medium); no source gives a cycle count for weekly data.

**Safety stock, ranges and accuracy**
- **Statistical safety stock:** SS = z x sigma x sqrt(T + L), sigma = standard deviation of demand per period, z set by the target service level [B1][B2][B5] (medium-low; the independent check found only a vendor calculator). An MIT slide ties cycle service level to safety factor k with SS = k x sigma and links fill rate to the loss function [B7] (medium; symbols partly lost). Sigma from forecast error rather than raw demand: search snippets only, unverified.
- **Prediction intervals:** forecast +/- c x sigma_h, c = 1.96 (95%) or 1.28 (80%) under normal errors; intervals usually widen with the horizon; bootstrap when errors are not normal [B8] (high). For SES, sigma_h^2 = sigma^2 x [1 + alpha^2 x (h - 1)] [B9] (high from the textbook; not independently confirmed).
- **Scenarios in practice:** base case (best guess), worst case (a level sales is confident of reaching) and best case, e.g. 70, 100 and 140 (roughly -30% and +40%), with the range built from typical forecast error, not a fixed percentage [B11] (medium; 2013, illustration only).
- **Do ranges help?** In one controlled study, 50% or 95% prediction intervals did not improve production decisions over a point forecast and made participants less responsive to cost asymmetry; a simple heuristic using 85% intervals came close to optimal [B12] (medium; one lab study, abstract-level, 2010). Evidence is mixed to negative.
- **MAE versus MAPE:** MAE is easy to understand and compute; MAPE is undefined if any actual value is zero, extreme near zero, and penalises over-forecasts less than under-forecasts; FPP3 recommends MASE and advises against sMAPE [B10] (high from the textbook; not independently confirmed). WAPE and bias reached only search snippets.
- **Confidence tiers:** vendor planning tools reportedly show High/Medium/Low tiers driven by history length, sales density, variability and recency (search snippets only: leads, not findings; B section 3).

## 4. Cross-cutting insights

1. **Weeks 2 and 3 equal week 1 without seasonal adjustment** (A; flatness verified, high). The order uses week 1 and weeks 2 and 3 are for planning, so planning ahead shows no new information and the Must version cannot show different numbers for weeks 2 and 3. A's options: raise seasonal adjustment, or say plainly in the UI that weeks 2 and 3 repeat week 1 until seasonality is added. A-R2 keeps seasonal adjustment as Should.
2. **A percentage spread does not widen with the horizon; statistical intervals do** [B8][B9]. With flat forecasts the scenario spread for weeks 2 and 3 is the same as for week 1: acceptable for an explicitly labelled what-if, but not a probability statement (B).
3. **Zero weeks break two rules at once** (A). A zero median breaks the outlier rule (Hampel fails the same way when MAD = 0), and a run of stockout zeros breaks the moving average if the flag is missing. One data design fixes both: a stockout flag in the data and a guard for a zero median. Zero-sales weeks also make MAPE undefined [B10], and common benchmarks record stockouts as zero sales without a flag [A22].
4. **Exclusion rules and seasonal indices interact** (A-inf). With 104 weeks and a 2x52 moving average there is one raw ratio per week of the year, so one promotion or stockout week passes straight into its index, and excluding a stockout or outlier week removes that week's only ratio. Settle exclusion before specifying seasonality. Smoothing the indices or grouping weeks (e.g. four-week blocks) are untested ideas, not source recommendations.
5. **The simplifications fit one another** (B). Weekly review, zero lead time and a percentage margin together keep the order formula hand-checkable; adding lead time or open orders would force an inventory position and a longer protection period [B2][B5]. The intent document already puts lead time and real orders out of scope.
6. **Hand-checkability narrows the method choice** (A). The optimised initial level [A1] and Fourier terms or STL [A9] cannot be checked by hand; NIST's starting values [A3] and seasonal naive [A2] can.
7. **Evidence quality is the real risk** (A, B). The same vendor family supplies B's policy, safety-stock formula and coverage metric, so the project has no textbook reference yet; A confirmed only 4 of 8 load-bearing claims independently; the SES variance formula and the MAPE zero-demand problem rest on FPP3 alone.

## 5. All recommendations (12)

| # | Recommendation | Feeds | Basis |
|---|---|---|---|
| A-R1 | Define MA and SES with the section 1 formulas: flat for weeks 1 to 3, recursive form for SES, initial level = first valid observation (NIST option a). | PRD functional requirements; test cases | Verified, high for flatness; medium for conventions |
| A-R2 | Keep seasonal adjustment as Should. If specified later: ratio-to-moving-average indices normalised to average 1, compared against seasonal naive, with a decision on the single-ratio problem. | PRD scope | Medium; verification of the normalisation step failed |
| A-R3 | Keep the brief's outlier rule only if documented as project-defined with an explicit zero-median guard (e.g. do not flag when the median is 0, or require a minimum floor), or switch to Tukey 1.5 x IQR or Hampel and accept that those also need a zero guard. | PRD data-quality requirements | Low-medium; the rule has no source |
| A-R4 | Keep excluding stockout weeks and call it a design decision with partial support; keep the stockout flag in the seed data. | PRD; test dataset | Medium |
| A-R5 | Keep "three or more consecutive high weeks" as a project-defined rule and give it a dedicated test series. | PRD; test dataset | Low; no source |
| A-R6 | Record every threshold (3 valid weeks, 8 weeks old, 12 weeks low confidence, 104 weeks high confidence, alpha default 0.3) as an assumption. | PRD assumptions; README | Low |
| B-R1 | Keep the order formula, documented as a simplified weekly order-up-to policy with an explicit assumptions list: weekly review, lead time zero, no open orders, stock on hand only, order at least 0, rounded up to whole units. | PRD functional requirements; README | Medium for structure [B2][B3][B5]; the simplifications are B's own |
| B-R2 | Keep the percentage safety margin as an adjustable setting and call it a rule of thumb that ignores demand variability; do not describe it as a service-level guarantee; add "safety stock from forecast error (z x sigma)" as a possible later improvement. | PRD; UI wording | Low; one vendor statement [B1] |
| B-R3 | Present optimistic and pessimistic as what-if scenarios, not confidence intervals or probabilities; if a statistical alternative is wanted later, base it on forecast error [B8]. | PRD; UI wording | Low; absence of a source for fixed percentages |
| B-R4 | Define "order soon" as forward weeks of cover (stock / forecast for week 1) compared with a user-set threshold, and say that lead time is not modelled. | PRD (product overview); test cases | Medium-low; vendor sources [B4][B6] |
| B-R5 | If an accuracy figure is shown, use MAE, not MAPE, because zero-sales weeks make MAPE undefined [B10]. | PRD (optional) | Medium; single textbook source |
| B-R6 | Record "no textbook source" as a known limitation in the process documentation, and replace vendor references with textbook references if time allows. | Process and AI-use documentation | High that the gap exists |

## 6. Open questions (9)

- **A-Q1:** What is the established, simple rule for treating stockout weeks in history, and which of the five unconstraining approaches is simplest? Needs a full-text read of the 2012 survey [A19] or an inventory textbook.
- **A-Q2:** Does the seasonal index need smoothing with 104 weeks, and by how much? Needs a source on weekly indices with two years of data.
- **A-Q3:** How should a moving average skip gaps (last N valid weeks versus shrinking the window)? No source found.
- **A-Q4:** What is a source-backed simple level-shift rule? Needs the Chen and Liu paper or a textbook on intervention detection.
- **A-Q5:** Do MAPE and related measures break with zero demand, as FPP3 states? Not independently confirmed (same gap as B-Q4).
- **B-Q1:** Which textbook or professional-body source (Silver, Pyke and Thomas; Nahmias; ASCM dictionary) supports the periodic-review policy, the safety-stock formula and weeks of supply? Needs a readable copy; the saved MIT lecture PDFs could not be converted to text.
- **B-Q2:** Is a percentage-of-forecast safety margin used or recommended anywhere credible? Needs a search in operations-management textbooks.
- **B-Q3:** Is the standard deviation of forecast error, rather than of demand, the right input to safety stock? Only vendor snippets claim this.
- **B-Q4:** Does an independent source confirm the SES variance formula [B9] and the MAPE zero-demand problem [B10]? Both rest on FPP3 alone.

## 7. Worked test fixtures in report A (section 1)

Invented data. The arithmetic was computed by the research assistant from the formulas cited in report A section 1, so these are test fixtures to re-verify, not sourced results.

- **Input:** weekly units y1..y8 = 12, 15, 11, 14, 13, 16, 12, 15.
- **Moving average, N = 3:** forecasts after weeks 3 to 8 are 12.667, 13.333, 12.667, 14.333, 13.667, 14.333. The forecast for weeks 9, 10 and 11 is 14.333 each.
- **SES, alpha = 0.3, level_1 = y_1 = 12:** levels are 12.000, 12.900, 12.330, 12.831, 12.882, 13.817, 13.272, 13.790. The forecast for weeks 9, 10 and 11 is 13.790 each.
- **Precision:** values are shown to three decimals; report A states no rounding or tolerance convention for tests.
- **Not covered:** report A gives no fixture for the outlier, stockout, level-shift or seasonal rules (A-R4 and A-R5 call for seed and dedicated test data). Report B has illustrative numbers only (260 + 40 = 300 [B3]; 64 rounds up to 70 for cases of 10 [B2]; 70/100/140 [B11]).
- **Extractor note (not a research claim):** a hand recomputation during extraction matched every value above; this does not replace re-verification in tests.

## 8. Wording guidance for the UI and PRD

- **Order formula:** present it as a deliberate simplification of the standard periodic-review policy, not as standard practice, and state the simplifications: review every week, zero lead time, no open orders, a percentage margin in place of a statistical safety stock (B summary; B-R1).
- **Safety margin:** call it a rule of thumb that ignores demand variability; do not describe it as a service-level guarantee (B-R2).
- **Scenarios:** optimistic and pessimistic are what-if scenarios, not confidence intervals or probabilities; the fixed spread is the same for weeks 1 to 3 and is not a probability statement (B-R3; B cross-insight).
- **Weeks 2 and 3:** the PRD says both methods give a flat forecast; the UI says plainly that weeks 2 and 3 repeat week 1 until seasonality is added (A summary; A cross-insight).
- **"Order soon":** say that lead time is not modelled (B-R4); the metric "does not determine a purchase order on its own" [B6] and assumes constant consumption [B4].
- **Data-quality rules:** call stockout exclusion "a design decision with partial support" (A-R4); label the outlier rule, the level-shift rule and every threshold as project-defined assumptions, not established methods (A-R3, A-R5, A-R6).
- **Outliers:** FPP3 calls replacing outliers without understanding why they occurred "a dangerous practice"; replacing is reasonable if they are errors or will not recur [A13].
- **Accuracy:** if shown, use and label MAE; MAPE is undefined with zero-sales weeks (B-R5; [B10]).
- **Confidence labels:** the 12-week (low) and 104-week (high) thresholds are assumptions (A-R6); vendor High/Medium/Low tiers are leads from snippets only (B section 3).
- **Evidence:** record "no textbook source" for the inventory policy as a known limitation in the process documentation (B-R6).
