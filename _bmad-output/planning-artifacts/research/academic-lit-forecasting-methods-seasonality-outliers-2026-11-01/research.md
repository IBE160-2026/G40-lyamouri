---
title: 'academic-lit research: Forecasting methods, seasonality, outliers and stockouts'
type: 'academic-lit'
topic: 'Forecasting methods, seasonality, outliers and stockouts'
decision: 'Choose forecast, seasonal-adjustment and outlier/stockout rules for a weekly small-business demand forecaster so the PRD can specify hand-checkable calculations'
source: 'native run'
status: complete
preset: 'standard'
validation: 'normal'
claims_verified: 4
claims_unverified: 4
created: '2026-11-01'
updated: '2026-11-01'
---

# academic-lit research: Forecasting methods, seasonality, outliers and stockouts

**Decision this research serves:** Choose forecast, seasonal-adjustment and outlier/stockout rules for a weekly small-business demand forecaster so the PRD can specify hand-checkable calculations.

## Executive summary

**What the evidence says to do.** Specify moving average and simple exponential smoothing (SES) exactly as textbooks define them, and say in the PRD that both give a flat forecast. Treat the outlier rule, the stockout rule, the level-shift rule and every numeric threshold as project-defined design decisions, because the research found no established rule for them.

**Three findings that drive this.**
1. Moving average and SES are well documented, hand-checkable, and give the same forecast for every future week [1][5]. With a flat forecast, weeks 2 and 3 equal week 1 unless a seasonal adjustment is applied. The Must version of the product therefore cannot show different numbers for weeks 2 and 3.
2. Seasonal adjustment by seasonal indices is a standard approach [7][8], but the textbook authors do not recommend classical decomposition [7], and with 104 weeks of history there is only one raw ratio per week of the year (our inference). This supports keeping seasonality as Should.
3. The brief's outlier rule ("above 2 times the median of the three preceding periods") is not a documented rule. Established alternatives exist: Tukey fences at 1.5 or 3 times the interquartile range [21] and the Hampel filter [14][15]. Stockout-censored demand is a recognised concept [18][22], but no source gives a simple rule for stockout weeks, a moving average over valid weeks, or a three-week level shift.

**Biggest caveat.** Most claims rest on one textbook (Hyndman and Athanasopoulos, FPP3) or on a handful of web pages. Independent confirmation was possible for 4 of 8 load-bearing claims; the other 4 are flagged `unverified`. Several full-text sources could not be fetched.

## 1. Moving average and simple exponential smoothing

**Definitions.**
- Moving average of N periods: the mean of the most recent N values [4][5]. SES: level_t = alpha x y_t + (1 - alpha) x level_(t-1), with 0 <= alpha <= 1; the forecast is the latest level [1].
- Small alpha gives more weight to older data; alpha = 1 gives the naive forecast (last value) [1]. The average age of data in SES is 1/alpha; an m-term moving average has average age (m+1)/2 [5] (medium, one source).

**Flat multi-step forecasts (verified, high).** FPP3 states that SES forecasts take the same value for every horizon h, and that this is only suitable without trend or seasonality [1]. Nau (Duke) says long-range forecasts of both the simple moving average and SES are flat [5]. Two publishers agree. No source discusses "recursive versus flat" for these methods; they coincide because the forecast equals the last level (our inference).

**Hand-checkable conventions.**
- NIST and FPP3 index SES differently (NIST: S_t uses y_(t-1); FPP3: level_t uses y_t) [3][1]. The numbers are identical; the PRD must pick one.
- FPP3 estimates the initial level by optimisation, which cannot be done by hand [1]. NIST lists hand-checkable starts: the first observation, or the average of the first four or five observations [3].
- No source gives a canonical default alpha. Examples use 0.2 to 0.5 [5]; NIST starts a grid at 0.1 to 0.9 and picks alpha by minimum squared error [3]. The brief's range 0.1 to 0.9 matches NIST's grid; the default 0.3 is consistent with example values but not sourced (confidence: low).
- Window length and alpha are usually chosen by best fit on past errors [3][5].

**Minimum history.** Hyndman says there is no fixed minimum sample size and warns against unsubstantiated rules of thumb [6]. A moving average of N periods needs at least N values (our inference). The thresholds in the brief (3 valid weeks, 12 weeks for low confidence) are design choices.

**Worked examples for tests** (invented data; arithmetic computed by the research assistant from the cited formulas, so treat as test fixtures to re-verify, not as sourced results). Weekly units y1..y8 = 12, 15, 11, 14, 13, 16, 12, 15.
- Moving average, N = 3: forecasts after weeks 3 to 8 are 12.667, 13.333, 12.667, 14.333, 13.667, 14.333. The forecast for weeks 9, 10 and 11 is 14.333 each.
- SES, alpha = 0.3, level_1 = y_1 = 12: levels are 12.000, 12.900, 12.330, 12.831, 12.882, 13.817, 13.272, 13.790. The forecast for weeks 9, 10 and 11 is 13.790 each.

**Intermittent demand.** Croston's method smooths demand sizes and intervals between demands separately [23]. The research did not retrieve its equations, so it is out of scope for v1 and is noted only as the standard route for many zero weeks.

## 2. Simple seasonal adjustment

**Standard approach.** Estimate seasonal indices by ratio-to-moving-average (multiplicative classical decomposition): divide each value by a centred moving average, average the ratios per season, and adjust the indices so they add to m (average 1) [7]. For weekly data the centred average is a 2x52 moving average, which loses 26 weeks at each end [7]. Forecast the seasonally adjusted series with any non-seasonal method, then multiply the forecast by the seasonal index [8]. Confidence: medium; a second source on the normalisation step and on the three-step method could not be read (V1, V2 unverified).

**Warnings from the sources.**
- The FPP3 authors write that classical decomposition "is not recommended, as there are now several much better methods", and that it assumes a seasonal pattern that repeats identically and is not robust to unusual values [7].
- Seasonal naive (forecast = the value from the same week last year) is the recognised benchmark any seasonal method should beat [2]. It is the simplest possible seasonal baseline and is trivial to check by hand.
- A year has 52.18 weeks, so weekly seasonality is not an integer period [10]; FPP3 notes most methods cannot handle this [9]. Fourier terms or STL are the textbook alternatives [9], but they are not hand-checkable.
- Exponential smoothing with seasonal terms (Holt-Winters/ETS) needs m-1 initial seasonal parameters, and R's `ets()` capped the period at 24 in a 2010 note that may be stale [11].
- SAS recommends data for several complete seasonal cycles, and at least two years for monthly seasonality [12] (medium, one vendor source). No source gives a number of cycles for weekly data.

**Consequence for 104 weeks (our inference, not a sourced claim).** After the 2x52 moving average there is one raw ratio per week of the year, so each weekly index is a single noisy value and one promotion or stockout week passes straight into it. Smoothing the indices or grouping weeks (for example four-week blocks) are untested ideas, not recommendations from any source.

## 3. Outliers, stockouts and level shifts

**Outlier rules that are established.**
- Tukey fences: inner fences at 1.5 x IQR beyond the quartiles ("mild"), outer fences at 3 x IQR ("extreme") [21] (verified, high). FPP3 applies them to the remainder of a robust STL fit, not to raw sales, and prefers 3 x IQR [13].
- Hampel identifier: flag a value outside the rolling median +/- 3 x 1.4826 x MAD [14][15] (two publishers agree; medium-high).
- FPP3 warns that replacing outliers without understanding why they occurred is "a dangerous practice"; replacing is reasonable if they are errors or will not recur [13].

**The brief's rule is not established.** No source describes "above 2 times the median of the three preceding periods". It is a short-window variant of a rolling-median rule. Its zero-median weakness follows from its own definition (our derivation): if the three preceding values are 0, the limit is 0 and every positive value is flagged. No source read documents this for Hampel either [14], although the Hampel rule fails the same way when MAD = 0.

**Stockouts and censored demand.**
- When stock runs out, recorded sales understate true demand: "censored demand" [18][22] (verified for the definition).
- Stockouts are generally handled as missing data, but one 2025 paper argues they are missing not at random, so ordinary imputation is inadequate, and notes that common benchmarks record stockouts as zero sales without a flag [22] (medium; one preprint).
- A 2012 survey of "unconstraining" methods exists and lists five approaches, but only its abstract was readable and it concerns airline revenue management [19].
- No source states that excluding stockout weeks from the history is the recommended simple treatment. Excluding them is consistent with "treat as missing" [22], with FPP3's options for missing values (use only data after the last gap, or interpolate) [13], and with the project's stockout flag. It is a design decision with partial support.
- FPP3 notes that ETS and STL in R cannot take missing values, while benchmark methods can [13]. This describes one R package, not the app's stack.

**Moving average over the last N valid weeks.** No source states this rule; it is the project's own. The documentation for statsmodels exposes a `missing='drop'` option for exponential smoothing but does not say what a gap does to the fit [20].

**Level shift versus outlier.**
- Time-series outlier detection treats a level shift as a separate type from a one-off additive outlier or a temporary change [16] (software documentation; independent confirmation unavailable, V5 unverified).
- CUSUM charts detect small persistent shifts in the mean [17], but they are heavier than a counting rule.
- No source gives a simple "three or more consecutive high weeks" rule. It is the project's own rule and must be tested with synthetic data.

## Cross-dimension insights

- **Flat forecasts make weeks 2 and 3 identical to week 1.** The intent document uses week 1 for the order and weeks 2 and 3 for planning. Without a seasonal adjustment, planning ahead shows no new information. This is a reason to either raise seasonal adjustment or to say plainly in the UI that weeks 2 and 3 repeat week 1 until seasonality is added.
- **Exclusion rules and seasonal indices interact.** Each weekly index rests on one ratio. Excluding a stockout week or an outlier week removes that week's only ratio. This must be settled before seasonality is specified.
- **Zero weeks break two rules at once.** A median of zero breaks the outlier rule, and a run of stockout zeros breaks the moving average if the flag is missing. Both are fixed by the same data design: a stockout flag in the data and a guard for a zero median.

## Recommendations

1. **Define both methods in the PRD with the formulas above, flat for weeks 1 to 3, recursive form for SES, initial level = first valid observation (NIST option a).** Feeds: PRD functional requirements and test cases. Basis: verified, high for flatness; medium for conventions.
2. **Keep seasonal adjustment as Should.** If specified later, use ratio-to-moving-average indices normalised to average 1, compare against seasonal naive, and decide how to handle the single-ratio problem. Feeds: PRD scope. Basis: medium; verification of the normalisation step failed.
3. **Keep the brief's outlier rule only if it is documented as a project-defined rule** with an explicit guard for a zero median (for example: do not flag when the median is 0, or require a minimum floor), or switch to Tukey 1.5 x IQR or Hampel and accept that those also need a zero guard. Feeds: PRD data-quality requirements. Basis: low-medium; the rule has no source.
4. **Keep excluding stockout weeks, and call it a design decision with partial support.** Keep the stockout flag in the seed data. Feeds: PRD and test dataset. Basis: medium.
5. **Keep the "three or more consecutive high weeks" rule as a project-defined rule** and give it a dedicated test series. Feeds: PRD and test dataset. Basis: low; no source.
6. **Record every threshold (3 valid weeks, 8 weeks old, 12 weeks low confidence, 104 weeks high confidence, alpha default 0.3) as an assumption** in the PRD. The research found no basis for any of them. Feeds: PRD assumptions and README. Basis: low.

## Open questions

- What is the established, simple rule for treating stockout weeks in history, and which of the five unconstraining approaches is the simplest? A full-text read of the 2012 survey [19], or an inventory textbook, would answer it.
- Does the seasonal index need smoothing with 104 weeks, and by how much? Needs a source on weekly indices with two years of data.
- How should a moving average skip gaps (last N valid weeks versus shrinking the window)? No source found.
- What is a source-backed simple level-shift rule? Needs the Chen and Liu paper or a textbook on intervention detection.
- Do MAPE and related measures break with zero demand, as FPP3 states? Confirmation by an independent source was not obtained (see the lagerstyring report).

## Source appendix

All sources accessed 2026-11-01. Pages were read through a fetch tool that summarises the page, so wording is partly paraphrase.

| [n] | Claim or finding it supports | Publisher | Pub date | Accessed | Confidence |
|---|---|---|---|---|---|
| [1] | SES formulas, flat forecast, initial level by optimisation | [Hyndman and Athanasopoulos, FPP3 (SES)](https://otexts.com/fpp3/ses.html) | undated (3rd ed. 2021) | 2026-11-01 | high |
| [2] | Seasonal naive formula and benchmark role | [FPP3 (simple methods)](https://otexts.com/fpp3/simple-methods.html) | undated | 2026-11-01 | high |
| [3] | NIST SES indexing, initial values, alpha by minimum error | [NIST/SEMATECH e-Handbook, 6.4.3.1](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc431.htm) | undated | 2026-11-01 | high |
| [4] | Moving average definition | [NIST/SEMATECH e-Handbook, 6.4.2.1](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc421.htm) | undated | 2026-11-01 | high |
| [5] | Moving average lag, alpha examples, flat long-range forecasts | [Robert Nau, Duke University course notes](https://people.duke.edu/~rnau/411avg.htm) | undated | 2026-11-01 | medium |
| [6] | No fixed minimum sample size | [Rob J. Hyndman, Hyndsight blog](https://robjhyndman.com/hyndsight/short-time-series/) | undated | 2026-11-01 | medium |
| [7] | Ratio-to-moving-average, indices sum to m, not recommended, not robust | [FPP3 (classical decomposition)](https://otexts.com/fpp3/classical-decomposition.html) | undated | 2026-11-01 | high |
| [8] | Forecast the adjusted series, recombine | [FPP3 (forecasting with decomposition)](https://otexts.com/fpp3/forecasting-decomposition.html) | undated | 2026-11-01 | high |
| [9] | Weekly data challenges, Fourier terms, STL | [FPP3 (complex seasonality)](https://otexts.com/fpp3/complexseasonality.html) | undated | 2026-11-01 | high |
| [10] | 52.18 weeks per year | [Rob J. Hyndman, Hyndsight blog](https://robjhyndman.com/hyndsight/seasonal-periods/) | 2014-11-07 | 2026-11-01 | high |
| [11] | ETS seasonal period cap of 24 (R, 2010) | [Rob J. Hyndman, Hyndsight blog](https://robjhyndman.com/hyndsight/longseasonality/) | 2010-09-29 | 2026-11-01 | medium (possibly stale) |
| [12] | Several seasonal cycles recommended | [SAS Institute, SAS/ETS 9.3 User's Guide](https://support.sas.com/documentation/cdl/en/etsug/63939/HTML/default/etsug_forecast_sect025.htm) | about 2011 | 2026-11-01 | medium |
| [13] | Outlier replacement, 3 x IQR on STL remainder, missing-value options | [FPP3 (missing values and outliers)](https://otexts.com/fpp3/missing-outliers.html) | undated | 2026-11-01 | high |
| [14] | Hampel identifier, 3 x 1.4826 x MAD | [SAS, The DO Loop blog](https://blogs.sas.com/content/iml/2021/06/01/hampel-filter-robust-outliers.html) | 2021-06-01 | 2026-11-01 | medium |
| [15] | hampel_anomalies defaults, k = 3 | [Rob J. Hyndman, R package weird](https://pkg.robjhyndman.com/weird/reference/hampel_anomalies.html) | undated | 2026-11-01 | high |
| [16] | Outlier types AO, LS, TC; critical value defaults | [CRAN tsoutliers documentation (rdrr.io mirror)](https://rdrr.io/cran/tsoutliers/man/tso.html) | 2024-05-29 | 2026-11-01 | medium |
| [17] | CUSUM for small persistent shifts | [NIST/SEMATECH e-Handbook, 6.3.2.3](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm) | undated | 2026-11-01 | medium |
| [18] | Definition of censored demand | [Lancaster University STOR-i blog](https://www.lancaster.ac.uk/stor-i-student-sites/tessa-wilkie/2020/03/23/censored-demand/) | 2020-03-23 | 2026-11-01 | medium |
| [19] | Unconstraining survey exists (abstract only) | [Guo, Xiao, Li, Advances in Operations Research (Crossref record)](https://api.crossref.org/works/10.1155/2012/270910) | 2012 | 2026-11-01 | medium |
| [20] | statsmodels `missing` option | [statsmodels documentation](https://www.statsmodels.org/stable/generated/statsmodels.tsa.holtwinters.ExponentialSmoothing.html) | version 0.15.0 docs | 2026-11-01 | medium |
| [21] | Inner and outer fences at 1.5 and 3 x IQR | [NIST/SEMATECH e-Handbook, 7.1.6](https://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm) | undated | 2026-11-01 | high |
| [22] | Stockouts understate demand; missing not at random | [Wang et al., arXiv 2505.16319 (preprint)](https://arxiv.org/html/2505.16319v3) | v3 2026-06-09 | 2026-11-01 | medium |
| [23] | Croston's method description | [fable R package documentation](https://rdrr.io/cran/fable/man/CROSTON.html) | undated | 2026-11-01 | medium |

## Staleness map

Textbook and handbook claims have no freshness bar (seminal work). Claims that age: software documentation ([16], [20]; re-check within 6 months, earliest **2027-05-01**), the preprint on stockouts [22] (state-of-the-art claim, 12 months, **2027-11-01**) and the possibly outdated `ets()` cap [11] (check against the current package within 6 months, **2027-05-01**). Earliest re-check: **2027-05-01**.
