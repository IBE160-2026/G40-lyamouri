---
title: 'Editorial review: structure lens on addendum.md'
created: '2026-11-03'
lens: structure (bmad-review)
---

# Editorial review: structure lens on addendum.md

**Purpose and audience:** helps the people and agents running the architecture, UX and epics steps find the technical detail, research figures, rejected alternatives and reasons behind the PRD, without reopening research reports A to D.

**Structure model:** Strategic/Context (Pyramid), with Reference/Database traits (readers arrive from PRD pointers).

**Order and grouping:** technology first (§2, §3) suits the architecture step; ending with the change record and sources (§7, §8) is right. The two sections moved in from the PRD were added at the end rather than worked in: rule material is split between §4 and §6, reasons for priorities are spread over §3, §4 and §6, §1 still describes the document before the move, one pointer goes to the wrong section and four have become ambiguous. All recommendations keep the numbers §1 to §8.

**Word counts (estimates):** about 5,000 words: §1 ~165, §2 ~970, §3 ~1,270, §4 ~1,190, §5 ~625, §6 ~430, §7 ~320, §8 ~70.

| # | Action | Location | Recommendation | Why |
|---|---|---|---|---|
| A1 | MOVE (re-point) | §1 "Citation keys" | Point to §8 (Sources), not §6. Optionally define the -Q keys (open questions) and the convention "a bare § is this addendum; a PRD section is written 'PRD §n'". | Sources moved from §6 to §8; the citation key now sends readers to Rule Rationale. |
| A2 | MERGE | §4 rule bullets and §6 entries for R-1, R-4, R-10, R-12 | Merge into §6, one entry per rule in rule order (R-1, R-4, R-7, R-8, R-10/R-11 with Croston, R-12, R-14, R-16, FR-34), each with: why the PRD has the rule, alternatives considered and why not, the tests (E-n). Keep one copy of each fact and every citation (keep the fuller version where copies differ). §4 keeps FastAPI, Next.js and hosted AI, plus a line pointing to §6. | The PRD sends readers to §6 for alternatives, but some are only in §4; four rules are covered twice and the copies already differ. |
| A3 | MOVE (re-point) | Bare § numbers meaning PRD sections (§3, §4, §1) | Write "PRD §7", "PRD §5.5", "PRD §0", "PRD §10". | A bare §7 now reads as this addendum's §7. |
| A4 | MOVE and expand | §1 description and §7 "Moved from the PRD" line | Update §1 to list every PRD pointer into the addendum (§2, §3, §6, §7), note that §6 and §7 were moved in on 2026-11-03, and add a short "Where to look" list per downstream step. | §1 was written before the move. |
| A5 | MOVE | §3 FR-28 priority sentence; §4 "Deliberately set to Could" paragraph | Move both into §6 as "Priority decisions"; retitle §6 "Rule and priority rationale" in sentence case, keeping the number. | Priority reasons in one place; the Could items were not rejected. |
| A6 | QUESTION (re-point) | §5 "PRD §10 question 4 records this gap (B-R6)" | Change to question 3. | The PRD's open questions were renumbered. |
| A7 | MOVE | Bold paragraph labels in §2 and §3 | Turn them into unnumbered ### subheadings (Recommendation, Runner-up, Company isolation, Further notes, Template approach, Optional local model, Model candidates, Why hosted free tiers are not used). | §2 and §3 are about 45% of the document but have no internal headings. |
| A8 | MOVE | Start of §2 | Put the recommendation first, with the note that the 3-point margin is inside the scoring uncertainty and that the architecture step decides. | Pyramid: recommendation before detail. |
| A9 | QUESTION | Section order §4, §5, §6 | Keep the current order (swapping §5 and §6 would break PRD pointers). | Renumbering risk. |
| — | PRESERVE | §1 "No new requirements" and "Nothing is decided here"; §4 "Hosted AI APIs" (re-point §7 only); §7 placement and its overlap with §6 | Keep. | Each serves a purpose. |

**2 minor fixes:** a pointer from "Versions as of 2026-11-01" in §2 to the re-check date in §5; "why: §6" pointers on the "Outlier rule" and "Season" bullets in §7.

**Length if all accepted (estimate):** about −85 and +150 words, net about +65 (+1.3%). No renumbering.
