---
title: 'domain research: Safety stock and order quantity'
type: 'domain'
topic: 'Safety stock and order quantity'
decision: 'Decide whether the order formula (forecast + percentage safety margin - stock, with plus/minus percent scenarios) is defensible for a small-business purchasing tool, and what standard practice says'
source: 'native run'
status: complete
preset: 'standard'
validation: 'normal'
claims_verified: 3
claims_unverified: 4
created: '2026-11-01'
updated: '2026-11-01'
---

# domain research: Safety stock and order quantity

**Decision this research serves:** Decide whether the order formula (forecast + percentage safety margin - stock, with plus/minus percent scenarios) is defensible for a small-business purchasing tool, and what standard practice says.

## Executive summary

**What the evidence says to do.** Keep the order formula, but present it as a deliberate simplification of the standard periodic-review policy, not as standard practice. State the simplifications in the PRD: review every week, zero lead time, no open orders, and a percentage margin in place of a statistical safety stock.

**Three findings that drive this.**
1. The formula "next-week forecast + safety margin - stock, never below zero" has the same structure as the textbook periodic-review order-up-to policy with a one-week review period and zero lead time [2][3][5]. Flooring the order at zero is explicit in the sources [2][5]; rounding up to pack size is described by one vendor [2].
2. No source describes a percentage-of-forecast safety margin or recommends it. The closest finding says simple "days of cover" rules are easy to communicate but "rarely optimal, because they ignore variability and service levels", and are acceptable when data is unreliable or for new products [1]. The standard alternative is safety stock = z x sigma x square root of (review period + lead time) [1][2][5].
3. No source shows a fixed plus/minus percentage as a standard way to define optimistic and pessimistic scenarios. Practitioners and textbooks build the range from forecast error [8][11]. In the one controlled study found, showing prediction intervals did not improve production decisions [12].

**Biggest caveat.** Every inventory-policy source is a vendor page or a short university tutorial (confidence medium or low); no textbook or professional-body source (for example ASCM) could be read, because the course PDFs came back as unreadable binary. The conclusions are therefore plausible but weakly evidenced.

## 1. Safety stock and the order policy

**Standard policy (periodic review, order-up-to).** At each review, order Q = max(0, S - inventory position), where S is the expected demand over the protection period (review period T plus lead time L) plus safety stock, and inventory position = on hand + on order - backorders [2][3][5]. A worked NC State example: 13 days at 20 bottles = 260, plus 40 safety stock = 300 [3]. If the position is at or above S, no order is placed [2][5]. Confidence: medium; three publishers agree, but two are vendors, and the third (NC State) states the policy without the inventory-position term.

**Safety stock.** Under independent demand, safety stock = z x sigma x sqrt(T + L), with sigma the standard deviation of demand per period and z set by the target service level [1][2][5]. The independent check found only a vendor calculator page that repeats the formula, so confidence is medium-low. One MIT lecture slide ties cycle service level to the safety factor k with SS = k x sigma and links fill rate to the loss function [7] (symbols partly lost in extraction).

**How the project formula relates (our analysis, not a sourced claim).** "Next-week forecast + safety margin - stock" equals the order-up-to formula with T = 1 week and L = 0, with the safety stock written as a percentage instead of z x sigma x sqrt(T + L), and with inventory position replaced by stock on hand. This is the same thing only if nothing is on order. If lead time is one week or more, or orders are open, the sources imply that the target must cover T + L and subtract stock on order [2][5].

**Percentage safety margins.**
- Not found in any source read. One vendor article says explicitly that it does not cover them [1].
- A days-of-cover safety rule is easy to explain but "rarely optimal" because it ignores demand variability and service levels; it can be acceptable for new products or when data is unreliable [1] (medium; vendor).
- Whether the standard deviation should come from forecast error rather than raw demand is claimed by search snippets only and was not verified.

**Rounding and minimum quantities.** One vendor article says to round order quantities up to pack sizes with documented rules (64 rounds up to 70 for cases of 10) and to model minimum order quantities explicitly, without a formula [2]. The intent document leaves pack sizes out of v1, so only "round up to whole units" is needed.

## 2. Stock coverage ("order soon")

Weeks of supply = available inventory / average weekly units sold, with a forward variant that divides by forecast weekly sales [6] (vendor, 2023). A procurement glossary defines coverage the same way and says lead time should always be shorter than coverage, with example triggers from 2 to 8 weeks that vary by product group [4] (vendor; low). The Inventory Planner article states that the metric "does not determine a purchase order on its own" [6]. No ASCM, textbook or university source for weeks of supply was found. The metric assumes constant consumption, so seasonal demand needs an adjusted calculation [4].

## 3. Scenarios, ranges and forecast error

**Prediction intervals (statistical).** A prediction interval has the form forecast +/- c x sigma_h, with c = 1.96 for 95% and 1.28 for 80% under normal errors [8]. Intervals usually widen with the horizon [8]. For SES the textbook gives sigma_h squared = sigma squared x [1 + alpha squared x (h - 1)] [9] (high from the textbook; an independent confirmation was not obtained). Bootstrapped intervals are recommended when errors are not normal [8].

**Scenarios in practice.** An S&OP practitioner article defines a base case (best guess), a worst case (a level sales is confident of reaching) and a best case, with example values 70, 100 and 140 (roughly -30% and +40%), and says the range is built from typical forecast error rather than a fixed percentage [11] (medium; one 2013 article, older than the five-year bar). A fixed plus/minus percentage appears only in a template example (plus/minus 15%) in a search snippet that was not fetched. We found no source that establishes it as a standard.

**Do ranges help decisions?** In a controlled experiment, participants choosing production quantities with asymmetric costs did not make better decisions when given 50% or 95% prediction intervals than with a point forecast, and were less responsive to cost asymmetry; a simple heuristic using 85% intervals came close to optimal [12] (medium; one lab study, abstract-level, 2010). Evidence on whether ranges help is therefore mixed to negative, and a single study.

**Accuracy measures.** MAE is easy to understand and compute [10]. MAPE is undefined if any actual value is zero, extreme near zero, and penalises over-forecasts less than under-forecasts [10] (high from the textbook; independent confirmation was not obtained). The textbook authors recommend MASE and advise against sMAPE [10]. WAPE and bias definitions reached only search snippets.

**Confidence labels for non-experts.** Vendor documentation for several planning tools reportedly shows High/Medium/Low tiers driven by history length, sales density, variability and recency, but these were seen only as search snippets, so they are leads, not findings.

## Cross-dimension insights

- **A fixed percentage does not widen with the horizon; statistical intervals do** [8][9]. With flat forecasts for weeks 1 to 3 (see the forecasting report), the scenario spread for weeks 2 and 3 would be the same as week 1. That is acceptable for an explicitly labelled what-if, but it is not a probability statement.
- **The simplifications fit one another.** Weekly review, zero lead time and a percentage margin together make the order formula hand-checkable; adding lead time or open orders would force an inventory position and a longer protection period [2][5]. The intent document already puts lead time and real orders out of scope.
- **Evidence quality is the real risk.** The same vendor family supplies the policy, the safety-stock formula and the coverage metric. If a reviewer asks for a textbook reference, the project does not yet have one.

## Recommendations

1. **Keep the formula and document it as a simplified weekly order-up-to policy** with an explicit assumptions list: weekly review, lead time zero, no open orders, stock on hand only, order at least 0, rounded up to whole units. Feeds: PRD functional requirements and README. Basis: medium for structure [2][3][5]; the simplifications are our own.
2. **Keep the percentage safety margin as an adjustable setting and call it a rule of thumb that ignores demand variability.** Do not describe it as a service-level guarantee. Add "safety stock from forecast error (z x sigma)" as a possible later improvement. Feeds: PRD and UI wording. Basis: low; one vendor statement [1].
3. **Present optimistic and pessimistic as what-if scenarios, not as confidence intervals or probabilities.** If a statistical alternative is wanted later, base it on forecast error [8]. Feeds: PRD and UI wording. Basis: low; absence of a source for fixed percentages.
4. **Define "order soon" as forward weeks of cover (stock / forecast for week 1) compared with a user-set threshold,** and say that lead time is not modelled. Feeds: PRD (product overview) and test cases. Basis: medium-low; vendor sources [4][6].
5. **If an accuracy figure is shown, use MAE, not MAPE,** because zero-sales weeks make MAPE undefined [10]. Feeds: PRD (optional). Basis: medium; single textbook source.
6. **Record "no textbook source" as a known limitation in the process documentation,** and replace vendor references with textbook references if time allows. Feeds: process and AI-use documentation. Basis: high that the gap exists.

## Open questions

- Which textbook or professional-body source (Silver, Pyke and Thomas; Nahmias; ASCM dictionary) supports the periodic-review policy, the safety-stock formula and weeks of supply? Answer needs a readable copy; PDF extraction (for example `pdftotext`) is not installed on this machine, and installing it would let the saved MIT lecture PDFs be converted.
- Is a percentage-of-forecast safety margin used or recommended anywhere credible? Needs a search in operations-management textbooks.
- Is the standard deviation of forecast error, rather than of demand, the right input to safety stock? Only vendor snippets claim this.
- Does an independent source confirm the SES variance formula and the MAPE zero-demand problem? Both rest on the FPP3 textbook alone.

## Source appendix

All sources accessed 2026-11-01. Pages were read through a fetch tool that summarises pages, so wording is partly paraphrase.

| [n] | Claim or finding it supports | Publisher | Pub date | Accessed | Confidence |
|---|---|---|---|---|---|
| [1] | Safety stock formula, days-of-cover rule limits | [Cleverence (vendor), safety stock article](https://www.cleverence.com/articles/3pl-business/how-to-determine-and-use-safety-stock-levels-4382/) | 2026-01-16 | 2026-11-01 | medium |
| [2] | Order-up-to level, inventory position, non-negative order, rounding to pack size | [Cleverence (vendor), periodic review article](https://www.cleverence.com/articles/for-business/what-is-periodic-review-system-3279/) | 2026-04-21 | 2026-11-01 | medium |
| [3] | Periodic review restocking level, worked example | [NC State University, Supply Chain Resource Cooperative](https://scm.ncsu.edu/?p=486) | 2011-01-28 | 2026-11-01 | medium |
| [4] | Inventory coverage definition and trigger example | [Tacto Technology GmbH (vendor glossary)](https://www.tacto.ai/en/procurement-glossary-downloads/inventory-coverage) | undated | 2026-11-01 | low |
| [5] | Safety stock formula and order quantity (independent check) | [MetricGate (vendor calculator docs)](https://metricgate.com/docs/periodic-review-order-up-to-RS/) | 2026-06-10 | 2026-11-01 | medium-low |
| [6] | Weeks of supply definition, forward variant | [Inventory Planner (Sage)](https://inventory-planner.com/weeks-of-supply) | 2023-02-17 | 2026-11-01 | medium-low |
| [7] | Cycle service level and safety factor k; fill rate and loss function | [MIT OpenCourseWare, Caplice, ESD.260 lecture 12](https://ocw.mit.edu/courses/esd-260j-logistics-systems-fall-2006/bc18dd1b2543535a61f826d00a8c6e42_lect12.pdf) | 2006-10 | 2026-11-01 | medium |
| [8] | Prediction interval form, widening with horizon, bootstrap | [Hyndman and Athanasopoulos, FPP3](https://otexts.com/fpp3/prediction-intervals.html) | undated | 2026-11-01 | high |
| [9] | SES forecast variance formula | [FPP3 (SES)](https://otexts.com/fpp3/ses.html) | undated | 2026-11-01 | high (unverified independently) |
| [10] | MAE, MAPE pitfalls, MASE | [FPP3 (accuracy)](https://otexts.com/fpp3/accuracy.html) | undated | 2026-11-01 | high (unverified independently) |
| [11] | Base, worst and best case built from forecast error | [IndustryWeek, B. Johnson](https://www.industryweek.com/supply-chain/planning-forecasting/article/21961177/planning-in-an-uncertain-world-managing-performance-tradeoffs-in-sop) | 2013-09-10 | 2026-11-01 | medium |
| [12] | Prediction intervals did not improve production decisions | [Goodwin, Onkal and Thomson, European Journal of Operational Research (Northumbria record)](https://researchportal.northumbria.ac.uk/en/publications/do-forecasts-expressed-as-prediction-intervals-improve-production/) | 2010-08-16 | 2026-11-01 | medium |

## Staleness map

Textbook claims ([8], [9], [10]) have no freshness bar. Vendor practice claims ([1], [2], [4], [5], [6]) are dated 2023 to 2026 or undated; the domain research bar for practice claims is about one year, so re-check them by **2027-04-21** (the earliest is the periodic-review article of 2026-04-21 plus one year; [6] dated 2023 is already stale and should be treated as history). The 2013 and 2010 sources ([11], [12]) are older than the five-year practice bar and are used only as illustrations.
