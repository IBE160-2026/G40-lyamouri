# Digest: simple seasonal adjustment (round 1, assistant 2)

Sources read (8): fpp3 classical-decomposition; fpp3 simple-methods; fpp3 forecasting-decomposition; fpp3 missing-outliers; fpp3 complexseasonality; Hyndman blog "Seasonal periods" (2014); Hyndman blog "Forecasting with long seasonal periods" (2010); SAS/ETS "PROC FORECAST: Data Requirements" (v9.3). The five fpp3 pages count as one publisher (same book). fpp3 pages carry only "(c) 2012- OTexts", no edition number or page date, so pub_date is "undated (c 2012-)". WebFetch returns a model-written summary of each page, so quotes are as relayed by the fetch tool, not checked against raw HTML.

## Findings
| # | claim | source URL | publisher | pub_date | accessed | confidence | class |
|---|-------|-----------|-----------|----------|----------|-----------|-------|
| 1 | Classical decomposition uses seasonal period m; for odd m the trend-cycle is an m-MA, T_t = (1/m) * sum of y_(t+j) for j=-k..k with m=2k+1; for even m a 2xm-MA is used. | https://otexts.com/fpp3/classical-decomposition.html | Hyndman and Athanasopoulos, OTexts (fpp3) | undated (c 2012-) | 2026-11-01 | high | textbook |
| 2 | Additive classical decomposition (y = S + T + R): detrend with y - T; average the detrended values for each season; adjust those averages so they sum to zero; repeat the sequence for every year; remainder R = y - T - S. | https://otexts.com/fpp3/classical-decomposition.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 3 | Multiplicative classical decomposition (y = S x T x R): detrend with y / T; average the detrended ratios for each season; the book states "These seasonal indexes are then adjusted to ensure that they add to m" (so they average 1); remainder R = y / (T x S). This is the "ratio-to-moving-average" method. | https://otexts.com/fpp3/classical-decomposition.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 4 | Classical decomposition has no trend-cycle estimate for the first and last few observations (for m=12, the first and last 6), so those points give no seasonal ratios. | https://otexts.com/fpp3/classical-decomposition.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 5 | Classical decomposition assumes the seasonal component repeats identically every year, and "is not robust" to unusual values. | https://otexts.com/fpp3/classical-decomposition.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 6 | The authors say classical decomposition "is not recommended, as there are now several much better methods" (e.g. STL, X-11, SEATS), but it is the basis of many of them. | https://otexts.com/fpp3/classical-decomposition.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 7 | Seasonal naive forecast: y_hat(T+h|T) = y(T+h-m(k+1)), where m is the seasonal period and k is the integer part of (h-1)/m. In words, each forecast equals the last observed value from the same season. | https://otexts.com/fpp3/simple-methods.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 8 | Seasonal naive is one of four simple methods the book uses "as benchmarks throughout"; they "serve as benchmarks rather than the method of choice"; and "any forecasting methods we develop will be compared to these simple methods. If not [better], the new method is not worth considering." | https://otexts.com/fpp3/simple-methods.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 9 | To forecast with a decomposition, the seasonal component S and the seasonally adjusted component A are forecast separately. The seasonal component is "forecast by simply taking the last year of the estimated component" (seasonal naive). For the adjusted series "any non-seasonal forecasting method may be used" (e.g. drift, Holt, non-seasonal ARIMA). | https://otexts.com/fpp3/forecasting-decomposition.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 10 | Recombination: additive gives y = S + A, so the forecasts are summed; multiplicative gives y = S x A, so the forecasts are multiplied. The book works an example only for the additive case; the multiplicative formula is stated without a worked example. | https://otexts.com/fpp3/forecasting-decomposition.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 11 | A year is not a whole number of weeks: "365.25/7 = 52.18 on average, allowing for a leap year every fourth year", but "most functions which use ts objects require integer frequency", so weekly data is entered with frequency 52. | https://robjhyndman.com/hyndsight/seasonal-periods/ | Rob J Hyndman, Hyndsight blog | 2014-11-07 | 2026-11-01 | high (primary, author of fpp3; blog) | blog by textbook author |
| 12 | fpp3 says "Even weekly data can be challenging to forecast as there are not a whole number of weeks in a year", and that most methods in the book "are unable to deal with these seasonal complexities". Its alternatives are Fourier terms (dynamic harmonic regression), noting that for high seasonal periods this tends to over-estimate the number of terms needed, and STL, whose seasonal component is forecast with seasonal naive and whose adjusted series is forecast with ETS. | https://otexts.com/fpp3/complexseasonality.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 13 | For a seasonal period m, ETS needs m-1 parameters for the initial seasonal states, which "becomes very hard for large periods". R's ets() restricts the seasonal period to a maximum of 24. The author prefers Fourier terms with ARMA errors, or TBATS. This is a 2010 note about R software, so the cap may have changed. | https://robjhyndman.com/hyndsight/longseasonality/ | Rob J Hyndman, Hyndsight blog | 2010-09-29 | 2026-11-01 | medium (dated, software-specific) | blog by textbook author |
| 14 | SAS documentation: for seasonal (Winters) methods the minimum is the number of observations in one complete seasonal cycle, but "there should be data for several complete seasonal cycles, or the seasonal factor estimates might be poor"; for monthly seasonality "at least two years of data is recommended". | https://support.sas.com/documentation/cdl/en/etsug/63939/HTML/default/etsug_forecast_sect025.htm | SAS Institute, SAS/ETS 9.3 User's Guide | undated (v9.3, about 2011) | 2026-11-01 | medium (vendor doc, one source) | vendor doc |
| 15 | On outliers, fpp3 says "none of the methods we have considered in this book will work well if there are extreme outliers"; "simply replacing outliers without thinking about why they have occurred is a dangerous practice"; replacement is reasonable if they are errors or will not recur. | https://otexts.com/fpp3/missing-outliers.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 16 | Outlier detection in fpp3: fit STL with robust=TRUE and flag points in the remainder more than 3 IQRs from the central 50% (the author prefers 3 over the usual 1.5); set flagged values to missing, then interpolate (the book uses an ARIMA model). | https://otexts.com/fpp3/missing-outliers.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |
| 17 | On missing values, fpp3 says to consider whether missingness induces bias (systematic missingness, e.g. holiday closures, may need dummy variables). ETS() and STL() do not handle missing values. Options are to use only data after the last gap, or to estimate the gaps by fitting an ARIMA model and interpolating. | https://otexts.com/fpp3/missing-outliers.html | OTexts (fpp3) | undated | 2026-11-01 | high | textbook |

## Worked example(s) / formulas

Formulas: rows 1-3 (ratio-to-MA / multiplicative classical decomposition), row 7 (seasonal naive), rows 9-10 (deseasonalise, forecast, reseasonalise).

Example, quarterly toy data (m=4, 3 years, so 2 full ratios per season). All arithmetic below is computed by assistant from the cited formulas (rows 1-3, 9-10), run once in Python to check. The data is invented for illustration. The 2x4-MA weights (1/8, 1/4, 1/4, 1/4, 1/8) are the assistant's expansion of the "2xm-MA" named in row 1, because the fetched page did not spell them out.

Data y (t=1..12): 12, 18, 30, 20 | 14, 21, 33, 22 | 16, 24, 36, 24.

Step 1, trend-cycle by 2x4-MA, T(t) = (0.5 y(t-2) + y(t-1) + y(t) + y(t+1) + 0.5 y(t+2)) / 4, available for t=3..10:
T = 20.25, 20.875, 21.625, 22.25, 22.75, 23.375, 24.125, 24.75.

Step 2, ratios y/T for t=3..10: 1.4815 (Q3), 0.9581 (Q4), 0.6474 (Q1), 0.9438 (Q2), 1.4505 (Q3), 0.9412 (Q4), 0.6632 (Q1), 0.9697 (Q2).

Step 3, average per quarter:
- Q1: (0.6474 + 0.6632) / 2 = 0.6553
- Q2: (0.9438 + 0.9697) / 2 = 0.9568
- Q3: (1.4815 + 1.4505) / 2 = 1.4660
- Q4: (0.9581 + 0.9412) / 2 = 0.9496
- Sum = 4.0277, not 4.

Step 4, normalise so the indices add to m=4 (multiply each by 4 / 4.0277 = 0.99312):
S = Q1 0.6508, Q2 0.9502, Q3 1.4559, Q4 0.9431. Sum = 4.0000, mean = 1.

Step 5, deseasonalise: A(t) = y(t) / S(season). The last four are Q1 16/0.6508 = 24.59, Q2 24/0.9502 = 25.26, Q3 36/1.4559 = 24.73, Q4 24/0.9431 = 25.45. These are what a moving average or SES is run on.

Step 6, reseasonalise: forecast for next Q1 = (non-seasonal forecast of A) x 0.6508. For example, if the SES or moving-average forecast of A is about 25.0, the Q1 forecast is 25.0 x 0.6508 = 16.3. The 25.0 is an illustrative figure, not computed from a cited rule.

Simpler variant, "indices from averages" (no moving average): index_q = (mean of season q) / (grand mean). On the same data the grand mean is 22.5 and the indices are 0.622, 0.933, 1.467, 0.978. They average 1 automatically. This variant is NOT in the fetched sources. It is the assistant's own simplification and ignores trend. Compare it with the ratio-to-MA values 0.651, 0.950, 1.456, 0.943: the trend (12 rising to 24 in the Q1 values) biases the plain-average indices.

For weekly data the same steps apply with m=52 (even, so a 2x52-MA, which loses 26 weeks at each end). With 104 weeks that leaves 52 usable ratios, so exactly one ratio per week-of-year. This is the assistant's deduction from rows 1, 4 and 11, not a quoted statement.

## Leads worth chasing
- Minitab Winters' method documentation (surfaced only in search snippet, not read): reportedly suggests about 4-5 full seasonal cycles for reasonable seasonal indices. This conflicts in spirit with SAS's "at least 2 years". Unverified until read.
- Texas A&M AFPC course notes "03 cycles" (afpc.tamu.edu/courses/622/2022/resources/03_cycles.pdf): ratio-to-MA / cycles teaching notes, not read.
- Hyndman and Athanasopoulos fpp3 ETS chapter (https://otexts.com/fpp3/ets.html) and the STL chapter (https://otexts.com/fpp3/stl.html): not read; would give the Holt-Winters/ETS(A,A,A) equations and STL robustness.
- NIST e-Handbook, section 6.4.4.2 (seasonal decomposition / seasonal subseries plot): not read.
- Original: Makridakis, Wheelwright and Hyndman, "Forecasting: Methods and Applications" (ratio-to-moving-average indices); Winters (1960), "Forecasting sales by exponentially weighted moving averages", Management Science.
- Current fpp3 and Hyndman material on whether ETS in the current R package still caps seasonality at 24 (the 2010 blog may be stale).
- Practical option: if 52 indices from 1-2 observations each look too noisy, aggregate (e.g. to monthly or 4-week indices) or smooth the weekly indices. No source in this round says this; it is a hypothesis only.

## Not found / could not verify
- No fetched source gives a specific risk statement about "only 2 cycles" for weekly data. Only SAS gives a general rule (several cycles; at least 2 years for monthly). The risk below is an inference, not a sourced claim: with 104 weeks and a 2x52-MA losing 26 weeks at each end, there is only 1 raw ratio per week-of-year (see worked example, last paragraph), so each weekly index is a single noisy value and one outlier or promotion week passes straight into it. (Without the MA, a plain-average variant would have 2 values per week.) Fpp3 row 5 (not robust to unusual values) and row 14 (poor estimates with too few cycles) are consistent with this.
- No source in this round states how many cycles are "reliable" for weekly data specifically.
- No fetched source describes exactly how a missing period or outlier shifts a seasonal index within classical decomposition. The fpp3 outlier/missing page does not discuss decomposition effects (it covers detection by robust STL and interpolation). The only sourced claims are rows 4, 5, 15-17.
- Holt-Winters equations and ETS(A,A,A) were not read directly. Only the m-1 initial seasonal state parameter count (row 13) and the m<=24 software cap are evidenced.
- "Seasonal indices from simple averages" as a textbook method is not evidenced by a fetched source; it appears above only as an assistant-derived variant.
- NIST e-Handbook not read (budget).
