---
title: 'Editorial review: prose lens on prd.md'
created: '2026-11-03'
lens: prose (bmad-review), run after the structure lens
---

# Editorial review: prose lens on prd.md

**Voice to preserve:** plain, declarative present tense; the formula lines ("Priority: X. Realizes UJ-1 …"); «» UI strings with the Norwegian decimal comma; ×, ÷ and −; "Mounia" repeated instead of pronouns inside UJ-1; the "recommends; decides" echoes; no serial comma where a list is unambiguous.

**Skipped** (cut, merged or moved by `review-structure-prd.md`): §0 first paragraph (S3), AG-3 (S12), repeated "one role per company" and FR-1 Out of Scope (S14), the FR-28 sprint-planning sentence (S14), the closing bullet after R-11, the §8.1 complexity sentence and NOTE FOR PM (S1), the NFR-2 sentence in §4.3, the FR-26 warning list (S5), DR-5's closing pointer, SM-2's verification sentence and the glossary "Stock on hand" row.

| # | Location | Problem | Fix |
|---|---|---|---|
| P1 | R-14 step 3 | "week 1, 2 and 3" next to "week number" can be read as week numbers 1 to 3; E14, E27 and E30 cannot catch it. | "for each of week 1, week 2 and week 3 of the forecast horizon, multiply the base forecast by the index of that week's week number to get its week forecast." |
| P2 | §3 Scenario, Safety margin | "plus 10%" can be read as adding 10 units; R-7 and R-8 multiply. | "increased by" / "reduced by" the scenario percentage; safety margin = "a percentage of the week-1 normal forecast, added to it". |
| P3 | FR-10 | E3 numbers listed in a different order than the labels. | "E3 gives normal 14.333, optimistic 15.767 and pessimistic 12.900." |
| P4 | FR-8, E11 b | "no moving-average forecast" suggests a fallback to exponential smoothing. | "When the moving average is the chosen method, … gets no forecast"; E11 b "so no forecast". |
| P5 | R-12 | "then" marks both a tie-breaker and the next group. | Number the three groups; "with ties sorted by product number". |
| P6 | §3 Warning, SM-3, FR-3 | Item boundaries disappear in lists whose items contain "and" or "or". | Semicolons or a serial comma in these three lists. |
| P7 | §11 | "must answer within 10 seconds before the template … is used" reads backwards. | "when the language model gives no answer within 10 seconds, the template explanation is used instead." |
| P8 | FR-15 | "not counted in any threshold" conflicts with stockout weeks counting toward the length of the sales history (R-16, E29 f) and the old-data count (FR-18). | "never uses the sales of stockout weeks"; "not counted in any valid-week threshold". |
| P9 | SM-7, §5.5, SM-C3, §1, §7, §4.1 | Synonyms for binding terms ("confidence level", "medium", "worked example", "stock figure", "seed script"). | Use the glossary terms and labels; "generator script (FR-3)". |
| P10 | DR-2, NFR-4, DR-7, §3 Calculation week | Glossary words used in a second sense ("settings", "history", "forecast calculation"). | "optional configuration"; "repository history"; "commit history"; "used to calculate the forecast". |
| P11 | FR-10 | "fixed text" contradicts the variable percentage. | "with «10 %» replaced by the actual scenario percentage". |
| P12 | FR-9 | The week forecasts "use" themselves. | "the week forecasts are seasonally adjusted, and the scenarios, suggested order quantity and weeks of cover all use them". |
| P13 | R-10 | "not flagged throughout" can read as "never flagged". | "a product with many zero-sales weeks does not get every week with sales flagged". |
| P14 | E29 e | Reads as a negation. | "the no-forecast condition is checked first". |
| P15 | FR-17 | "from the start" is ambiguous. | Remove "from the start". |
| P16 | §3 Unusual week | "break the rule" can mean "fail the test". | "A valid week that the outlier rule flags." |
| P17 | §4.9, FR-29, FR-31, §4.4 (and §4.6) | The persona name in requirement statements reads as one person's permission; other FRs name the role. | "The user can …" in requirement statements; keep Mounia in UJ-1 and in examples. **Needs the user's decision** (earlier instruction to use the name Mounia throughout). |
| P18 | §4.6, FR-21 | "the teacher's core flow" is not defined in the PRD. | "the core flow from the teacher's feedback (SM-3)"; "Realizes UJ-1 step 4 and the core flow in SM-3." |
| P19 | FR-21 table | "E1 to E2" reads as a range; unclear referents. | Use arrows ("E1 → E2: 14.333 → 13.790"); "for a test product that the setting affects … the value in the table". |
| P20 | FR-3 | Unit only implied. | "3 to 11 valid weeks … 12 to 103 valid weeks". |
| P21 | FR-27, §3 Explanation | "(with FR-28)" vague; "always labelled as AI-written text" over-broad. | "(when FR-28 is built)"; "in which case it is labelled «KI-omformulert forklaring» (FR-27)". |
| P22 | Whole document | Mixed US and British spelling. | One variety throughout. **Needs the user's decision** (the configured Microsoft guide uses US spelling; the addendum is in British spelling). |

**22 minor fixes:** §3 Week (assumption placement, "distances between weeks are counted by position"); §1 ("rules … check by hand, with settings the user can adjust"); §3 intro ("to name domain concepts"); §4.4 description (Prognose calculates, the screen shows); FR-16 ("does not add or remove this warning"); DR-5 ("Each case records …"); R-15 (notes list wording); FR-12 ("may not add up exactly to the shown result"); long sentences in FR-1, DR-9 and SM-6; DR-1 setup bullet order; §12 (split two rules); §4 intro ("Where reference examples test an FR, the FR names them"); §10 Q6 (clause order); FR-3 ("a history that reaches «høy»"; "rule test product"); NFR-3 ("the load command (DR-4)"; "a local file that `.gitignore` excludes"); FR-33 (what must be covered); SM-C1 wording; "week forecasts for weeks 1, 2 and 3"; FR-27 ("calculation area" undefined); NFR-1 ("third-party accounts"); consistency (FR-21 "value", FR-11 "the UJ-1 climax", spell out MAPE and STL); wording only (NFR-10, §4.7, §8.2, R-10, §7, FR-13).

**Summary:** 22 rows and 22 minor items; about +110 words if all are accepted. No requirement, rule, number, threshold, ID or section number changes; existing «» strings are untouched.
