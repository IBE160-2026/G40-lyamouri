---
title: 'Editorial review: prose lens on addendum.md'
created: '2026-11-03'
lens: prose (bmad-review), run after the structure lens
---

# Editorial review: prose lens on addendum.md

**Style to keep:** plain, declarative technical English; bold run-in labels; British spelling; no serial comma (as in the PRD); ISO dates; citation keys; «» for Norwegian UI labels. The Microsoft Writing Style Guide would use US spelling and the serial comma, but changing only the addendum would make it differ from the PRD, so neither is flagged (P2 is the one place where the missing comma changes the meaning).

**Scope:** text that the structure findings (`review-structure-addendum.md`) propose to merge or move was skipped; fixes that fall in merged text follow it (P4, P19).

| # | Location | Original | Revised | Why |
|---|---|---|---|---|
| P1 | §2 Charting | "A line chart is the getting-started example with a different chart type [C22]." | "The getting-started example is a bar chart, and a line chart is the same code with a different chart type [C22]." | Follows report C; the current wording misstates the source. |
| P2 | §3 Error behaviour | "send all of these cases, a timeout and a rejected text to the template explanation, without an error … so the timeout, and how it fits NFR-8's 2-second target, are architecture choices." | "send all of these cases, as well as a timeout and a rejected text, to the template explanation without an error … so the timeout and how it fits NFR-8's 2-second target are architecture choices." | Without a serial comma the two further cases read as a second name for "these cases". |
| P3 | §3 Model's role | "It may not supply, compute or change … It may not replace …" | "It must not supply, compute or change … It must not replace …" | "May not" can mean "might not"; a prohibition needs "must not". |
| P4 | §5 Inferences | Mixed "that" clauses and noun phrases; "one-ratio-per-week problem"; "MAD" undefined. | Parallel noun phrases; "the problem of one ratio per week number"; "median absolute deviation (MAD)". | Parallel list; precise term; MAD usually means mean absolute deviation in forecasting. |
| P5 | §2 Recommended and reversibility hedge | "forecasting logic", "forecasting package", "calculation module" | "calculation module" throughout | One component, the PRD's term (NFR-2). |
| P6 | §3, §5, §6 | "the calculation line"; "method"; "MAPE zero-demand problem"; "Warnings about … count only"; "«Høy»" | "the order calculation line"; "forecasting method"; "the MAPE problem with zero-sales weeks"; "… count as active warnings only"; "The label «høy»" | Glossary terms; sales and demand kept apart. |
| P7 | §2 Company isolation | "It is usually enforced like this:" / "C-R2 turns this into …" | "Company isolation is usually enforced like this:" / "C-R2 turns OWASP's guidance into …" | Unclear "it" and "this". |
| P8 | §2 Libraries to avoid | "For FastAPI as the default and for Next.js, see §4." | "For why FastAPI should not be the default and why Next.js is rejected, see §4." | Reads like a pointer to the case for FastAPI. |
| P9 | §6 Seasonal adjustment as Should | "suggested season … and the user first wanted …" | "suggested seasonal adjustment … and the group first wanted …" (check the noun; use it also in R-16 and the moved FR-28 sentence) | In the PRD, "the user" is the purchasing manager persona. |
| P10 | §3 Versions and offline use | "It says … it works offline … the docs do not confirm" | "The documentation says … Ollama works offline … it does not confirm" | Two different referents for "it", and "docs" next to "documentation". |
| P11 | §3 Terms in the EEA | "(inference: Norway is not named)" | "(inference, because the terms do not name Norway)" | Elsewhere the words after "inference:" are the inferred claim. |
| P12 | §3 Unstable limits | "none was opened (low confidence)" | "none of them was opened during the research (low confidence)" | Says what was not opened. |
| P13 | §5, §3 | "The guardrail pattern"; "a numeric validator" | "The proof-carrying numbers pattern behind D-R2"; "a number checker" | One name per thing. |
| P14 | §7 Exponential smoothing | "were fixed" | "were defined" | "Fixed" reads as "corrected". |
| P15 | §3 Report D weights | "… easy to test 30, runs without a key 25 …" | "… easy to test (30), runs without a key (25) …" | Shows where each criterion ends. |
| P16 | §2 Report C terms | "gates"; "basis medium-low"; "vendored"; totals without scale | "hard gates (pass/fail requirements)"; "evidence basis medium-low"; "a pinned link to a content delivery network (CDN) or a vendored file (a copy kept in the repository)"; "out of 100" | Undefined terms for readers who have not opened report C. |
| P17 | §2 Charting | "how Chart.js draws the markings that differ by more than colour, or the legend, that NFR-7 asks for" | "how Chart.js draws the legend and the markings that differ by more than colour, both of which NFR-7 asks for" | Competing "that" clauses. |
| P18 | §7 Settings and Season | "a default of 10% (0% to 100%)"; "made Should, with stated limitations, plus a seasonal-pattern warning" | "a default of 10% and a range of 0% to 100%"; "specified as a simple index with stated limitations and made Should, and a seasonal-pattern warning was added" | Parallel wording; the warning is not part of the priority change. |
| P19 | §7 Outlier rule (and the merged §6 R-10/R-11 entry) | "2 × the median of the three preceding periods" / "2 × the median of the last 3 weeks" | "twice the median of the three preceding periods" in both places | Quotes the brief word for word ("values above twice the median of the three preceding periods are flagged"). |
| P20 | §8 Sources | "A, forecasting methods, seasonality and outliers: …" | "A (forecasting methods, seasonality and outliers): …" (same for B, C, D) | Reads as a list of four items. |
| P21 | §3 Labelling | "the EU Article 50 transparency duties"; "a school project" | Consider "the transparency duties in Article 50 of the EU AI Act" (only if [D4] confirms the act); "a course project" | Avoids confusion with the treaty article; the PRD's term. |
| P22 | §3 | "That matches the case where FR-28 becomes Must." | Consider "That would be the case if FR-28 became Must." | FR-28 stays Should. |
| P23 | §6 intro | "without losing the professional content" | Consider "without losing the subject-matter detail" | A literal translation of «faglig innhold». |

**14 further minor fixes** (not expanded): placement of "only" (three places), a sentence that starts with "5.2", criterion names, "docs" next to "documentation", and small parallel-structure points in §5.

**Summary:** 23 rows; about +70 words (+1.4%) if all are accepted. Nothing is cut.
