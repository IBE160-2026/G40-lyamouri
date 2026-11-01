# Digest: forecasting methods (MA and SES) (round 1, assistant 1)

All sources accessed 2026-11-01. Publication dates: the pages are undated online editions (FPP3 3rd ed. is 2021; NIST e-Handbook is a living document). Textbook/handbook material, so no freshness bar. Seminal-work note: the pages were read via WebFetch (summarised by a small model), so wording is paraphrase unless in quotes.

## Findings
| # | claim | source URL | publisher | pub_date | accessed | confidence | class |
|---|---|---|---|---|---|---|---|
| 1 | SES one-step forecast in weighted-average form: yhat(T+1|T) = alpha*y_T + alpha(1-alpha)*y_(T-1) + alpha(1-alpha)^2*y_(T-2) + ..., with 0 <= alpha <= 1. | https://otexts.com/fpp3/ses.html | Hyndman and Athanasopoulos, FPP3 (OTexts) | undated (3rd ed. 2021) | 2026-11-01 | high | primary/textbook |
| 2 | SES recursive form: yhat(T+1|T) = alpha*y_T + (1-alpha)*yhat(T|T-1). Component form: forecast yhat(t+h|t) = level_t; level_t = alpha*y_t + (1-alpha)*level_(t-1). | https://otexts.com/fpp3/ses.html | FPP3 | undated | 2026-11-01 | high | primary/textbook |
| 3 | Small alpha gives more weight to distant observations, large alpha more weight to recent ones; alpha = 1 gives the naive forecast (last observation). | https://otexts.com/fpp3/ses.html | FPP3 | undated | 2026-11-01 | high | primary/textbook |
| 4 | SES forecasts are flat: yhat(T+h|T) = level_T for all h = 2, 3, ...; "all forecasts take the same value, equal to the last level component". FPP3 says this is only suitable when there is no trend or seasonality. | https://otexts.com/fpp3/ses.html | FPP3 | undated | 2026-11-01 | high | primary/textbook |
| 5 | FPP3 initialises SES with a level_0 that is estimated (not fixed), jointly with alpha, by minimising SSE = sum of (y_t - yhat(t|t-1))^2, a non-linear optimisation requiring an optimisation tool. Algeria exports example: alpha-hat = 0.84, level_0-hat = 39.5; all h=1..5 forecasts equal 22.44. | https://otexts.com/fpp3/ses.html | FPP3 | undated | 2026-11-01 | high | primary/textbook |
| 6 | NIST (single exponential smoothing): S2 = y1 (no S1); for t >= 3, S_t = alpha*y_(t-1) + (1-alpha)*S_(t-1), 0 < alpha <= 1; S_t is used as the forecast for period t (it is indexed so the smoothed value at t is built from data up to t-1). | https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc431.htm | NIST/SEMATECH e-Handbook of Statistical Methods | undated (living doc) | 2026-11-01 | high | primary/handbook |
| 7 | NIST lists three initialisation options for the first smoothed value: (a) the first observation, (b) the process target, (c) the average of the first four or five observations; and warns that the smaller alpha is, the more the initial value matters, so several methods should be tried. | https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc431.htm | NIST e-Handbook | undated | 2026-11-01 | high | primary/handbook |
| 8 | NIST chooses alpha by minimum MSE, by trial and error over a grid (start between 0.1 and 0.9, then refine) or by a non-linear optimiser (Marquardt). In its 12-point example alpha = 0.5 (MSE 16.29) beat alpha = 0.1 (MSE about 19.0). | https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc431.htm | NIST e-Handbook | undated | 2026-11-01 | high | primary/handbook |
| 9 | The NIST SES page does not discuss multi-step forecasts, trend or seasonality (limitations are only implied: dependence on initial value, no closed-form rule for alpha). | https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc431.htm | NIST e-Handbook | undated | 2026-11-01 | high | absence |
| 10 | NIST defines the moving average at period t as the mean of the most recent N values: M_t = (X_t + X_(t-1) + ... + X_(t-N+1)) / N; each new average drops the oldest value and adds the newest. Worked example with N = 3 on 12 values gives MSE 2.42 vs 3 for the plain mean. | https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc421.htm | NIST e-Handbook | undated | 2026-11-01 | high | primary/handbook |
| 11 | The NIST single-moving-average page does not cover multi-step forecasts, lag with trend, or how to choose N. | https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc421.htm | NIST e-Handbook | undated | 2026-11-01 | high | absence |
| 12 | NIST says the simple mean of all past data is only useful for forecasting when there is no trend ("The mean is not a good estimator when there are trends"); smoothing is divided into averaging and exponential smoothing methods. | https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc42.htm | NIST e-Handbook | undated | 2026-11-01 | high | primary/handbook |
| 13 | Nau (Duke): the simple moving average forecast "equals the simple average of the most recent m observations"; the window k is customarily adjusted to get the best fit (in his example the 5-term average had lowest RMSE, only slightly better than 3- and 9-term). | https://people.duke.edu/~rnau/411avg.htm | Robert Nau, Fuqua School of Business, Duke University (course notes) | undated | 2026-11-01 | medium | course notes |
| 14 | Nau: an m-term moving average has average age (m+1)/2, so a 5-term average is "about 3 periods late in responding to turning points" (lag with trend/turning points). | https://people.duke.edu/~rnau/411avg.htm | Duke course notes | undated | 2026-11-01 | medium | course notes |
| 15 | Nau: long-range forecasts from both SMA and SES are flat (horizontal line); for SMA the confidence intervals "do not get wider as the forecasting horizon increases", which he calls incorrect, whereas SES intervals widen sensibly. | https://people.duke.edu/~rnau/411avg.htm | Duke course notes | undated | 2026-11-01 | medium | course notes |
| 16 | Nau: SES alpha is chosen by minimising squared error (optimum 0.2961 in his example; examples use 0.2 to 0.5); average age of data in SES is 1/alpha (alpha = 0.2 means about 5 periods lag); alpha = 1 is a random walk, alpha near 0 approaches the mean model. | https://people.duke.edu/~rnau/411avg.htm | Duke course notes | undated | 2026-11-01 | medium | course notes |
| 17 | Nau: these models are for non-seasonal patterns and trends and need seasonal adjustment to be combined with seasonality; the page does not discuss outliers and gives no minimum sample size. He also says SES "often performs better out-of-sample than might otherwise be expected". | https://people.duke.edu/~rnau/411avg.htm | Duke course notes | undated | 2026-11-01 | medium | course notes |
| 18 | Nau: for error-based SES form, the first forecast can be set equal to the first observation (so the first error is 0). | https://people.duke.edu/~rnau/411avg.htm | Duke course notes | undated | 2026-11-01 | medium | course notes |
| 19 | FPP3 benchmark methods: mean yhat(T+h|T) = (y1+...+yT)/T; naive yhat = y_T; both give the same value for all h (constant forecasts); drift = y_T + h*(y_T - y_1)/(T-1) is not flat. FPP3 section 5.2 does not mention moving-average forecasts. | https://otexts.com/fpp3/simple-methods.html | FPP3 | undated | 2026-11-01 | high | primary/textbook |
| 20 | Hyndman: there is no fixed minimum sample size; estimation needs more observations than parameters, rules of thumb (e.g. 30 for ARIMA) are "misleading and unsubstantiated"; very short series favour models with very few parameters; use AIC as proxy for out-of-sample error when holdout is infeasible. The page gives no minimum for SES/ETS. | https://robjhyndman.com/hyndsight/short-time-series/ | Rob J Hyndman, Hyndsight blog (author of FPP3) | undated | 2026-11-01 | medium | primary author, blog |
| 21 | Croston's method applies SES separately to the non-zero demand sizes and to the intervals between non-zero demands (fable documentation, citing Croston 1972, Operational Research Quarterly 23(3), 289-303, and Shenstone and Hyndman 2005, J. Forecasting 24, 389-402). | https://rdrr.io/cran/fable/man/CROSTON.html | fable R package documentation (Hyndman group) | undated | 2026-11-01 | medium | vendor/package doc |
| 22 | Package docs give variants SBA (forecast multiplied by 1 - alpha/2) and SBJ (multiplied by 1 - alpha/(2 - alpha)); Croston's method has no underlying stochastic model, so forecast distributions are not computed. Parameter search range defaults to (0,1); no default alpha stated. | https://rdrr.io/cran/fable/man/CROSTON.html | fable documentation | undated | 2026-11-01 | medium | vendor/package doc |
| 23 | A web-search result summary (not fetched, so not relied on) attributes to Croston the observation that plain SES on intermittent data peaks right after a demand event and is lowest just before the next; treat as unverified until the Croston 1972 paper is read. | search result only (see Leads) | n/a | n/a | 2026-11-01 | low | unverified |

## Worked example(s) / formulas
All numbers below are computed by assistant from the cited formula (script run in the session, python3). Data are invented illustration, not sourced: weekly units y1..y8 = 12, 15, 11, 14, 13, 16, 12, 15.

**Simple moving average, window N = 3** (formula: row 10, M_t = mean of last N values; as a forecast, the next-week forecast = M_t, flat for all horizons per rows 15):
- After week 3: (12+15+11)/3 = 12.667 (forecast for week 4)
- After week 4: (15+11+14)/3 = 13.333 (forecast week 5)
- After week 5: (11+14+13)/3 = 12.667 (forecast week 6)
- After week 6: (14+13+16)/3 = 14.333 (forecast week 7)
- After week 7: (13+16+12)/3 = 13.667 (forecast week 8)
- After week 8: (16+12+15)/3 = 14.333 -> forecast for weeks 9, 10, 11 are all 14.333 (flat).
- One-step MSE over weeks 4..8 (5 errors): 4.044.

**SES, alpha = 0.3, initial level = first observation** (formula: rows 2 and 18 with level_1 = y_1 = 12; level_t = 0.3*y_t + 0.7*level_(t-1); forecast = latest level; note this initialisation is NIST's option (a), row 7, not FPP3's optimised level_0, row 5):
- level_1 = 12.000
- level_2 = 0.3*15 + 0.7*12.000 = 12.900
- level_3 = 0.3*11 + 0.7*12.900 = 12.330
- level_4 = 0.3*14 + 0.7*12.330 = 12.831
- level_5 = 0.3*13 + 0.7*12.831 = 12.8817
- level_6 = 0.3*16 + 0.7*12.8817 = 13.8172
- level_7 = 0.3*12 + 0.7*13.8172 = 13.2720
- level_8 = 0.3*15 + 0.7*13.2720 = 13.7904 -> forecast for weeks 9, 10, 11 are all 13.790 (flat).
- One-step SSE over weeks 2..8 (7 errors) = 31.44 (MSE 4.49).
- Caveat: the MA3 MSE (5 errors) and SES MSE (7 errors) cover different weeks, so they are not directly comparable; compare over the same weeks if used in the tool.

## Leads worth chasing (named entities, contradictions, opened questions)
- Index convention contradiction to flag for the spec: NIST writes S_t = alpha*y_(t-1) + (1-alpha)*S_(t-1) (S_t is the forecast for t), FPP3 and Nau write level_t = alpha*y_t + (1-alpha)*level_(t-1) with forecast for t+1 = level_t. Same numbers, different indexing; the spec should pick one.
- Initialisation difference: FPP3 estimates level_0 by optimisation (not hand-checkable); NIST gives hand-checkable options (first value, average of first 4-5). For a hand-checkable tool NIST's options fit better.
- Recursive vs flat multi-step: no source found that discusses "recursive" multi-step for SES/MA; because forecast = last level, recursive and flat coincide (my inference, not a sourced claim). A source stating this explicitly would be worth finding (e.g. FPP3 section on ETS forecasting, or Hyndman et al. 2008 "Forecasting with Exponential Smoothing").
- Primary sources not yet read: Brown (1959/1963) and Holt (1957) for SES origin; Croston (1972); Shenstone and Hyndman (2005); Syntetos and Boylan (2005) on bias correction and on when to use Croston (ADI and CV2 classification); Hyndman and Koehler (2006) MASE as an accuracy measure robust to zeros.
- Outlier sensitivity of MA/SES and robust variants (e.g. median-based, winsorising, tsclean): not covered by the pages read.
- Typical default alpha: only examples seen (0.1-0.5 range in Nau, 0.1-0.9 grid in NIST); no source stating a canonical default such as 0.2 or 0.3.

## Not found / could not verify
- A source stating a recommended or typical default alpha (only example values and optimisation by MSE were found).
- A source for choosing the moving-average window other than "pick by best fit" (Nau); no rule linking window to demand frequency.
- Minimum history for MA (logically needs at least N observations; this is an inference, no source) and for SES (Hyndman says no fixed minimum, depends on parameters vs observations; nothing SES-specific).
- Behaviour of SES/MA on very short series beyond the general guidance in row 20.
- Recursive vs flat multi-step discussion for MA/SES (see Leads).
- Outlier sensitivity of both methods (Nau page does not discuss; NIST pages do not discuss).
- Croston forecast equation (size smoothed / interval smoothed), default alpha and initialisation: the Hyndman forecast-package page (pkg.robjhyndman.com/forecast/reference/croston.html) returned empty and the rdrr.io forecast man page returned 404; fable page does not give the equation. Only the high-level description (row 21-22) is evidenced.
- Source budget: 8 distinct sources read (FPP3 ses, FPP3 simple-methods, NIST pmc431, pmc421, pmc42, Nau Duke, Hyndman blog, fable CROSTON doc); two Croston fetches failed.
