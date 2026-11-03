---
title: 'Editorial review: structure lens on prd.md'
created: '2026-11-03'
lens: structure (bmad-review)
---

# Editorial review: structure lens on prd.md

**Purpose read:** This document exists to help the IBE160 project group, its teacher and examiner, and the BMAD and Claude Code steps that follow (UX, architecture, epics and stories) agree on exactly what version 1 of Prognose must do, and test it against rules that can be checked by hand and a fixed answer key.

**Structure model:** Strategic/Context (Pyramid), the PRD model. §3 Glossary, §5 Rules and the §6 requirement lists are also judged as Reference/Database sections (random access by ID, one consistent schema).

**Word counts are estimates** (the word-metrics script was not run). Total ≈ 12,800 words: §0 ≈ 240, §1 ≈ 260, §2 ≈ 590 (UJ-1 ≈ 430), §3 ≈ 1,200, §4 ≈ 4,100, §5 ≈ 2,800 (§5.7 ≈ 1,100), §6 ≈ 1,750 (§6.3 ≈ 1,000), §7 ≈ 270, §8 ≈ 330, §9 ≈ 580, §10 ≈ 225, §11 ≈ 400, §12 ≈ 85.

**Overall:** The section order holds up and the FR schema is mostly consistent. The main gaps are no top-down signposting (scope summary, deadline and done-gate appear only after about 10,000 words), no overview of the calculation flow, and duplicated lists that have started to drift. No renumbering is proposed.

| # | Action | Location | Recommendation | Why |
|---|---|---|---|---|
| S1 | MOVE | §8.1 complexity sentence, §8.2 NOTE FOR PM | Open the PRD with an unnumbered "Version 1 at a glance" block: status and deadline; Must = weekly core flow (→ §8.1); Should at risk (→ §8.2, §10 Q1); Could (→ §8.3); done = SM-1 and SM-3 pass and SM-2 holds. Move the complexity sentence there (it also counts Should rules and examples). | Pyramid top-down; the examiner and sprint planning need scope, deadline risk and done-gate first. Moving §8 itself would renumber §7–§10. |
| S2 | QUESTION | §5 intro | Add a "Calculation order" overview: R-1 → R-10, R-11 → R-2 → R-6 → R-14 → R-3, R-4 → R-5 → R-7 → R-8, R-9 (with R-13) → R-12 → R-15 to R-17. | Mental model before the densest section; reordering §5.1–§5.6 would renumber §5.5. |
| S3 | CONDENSE | §0 first paragraph | Keep purpose and audience as prose; turn the rest into a "Where to find what" list (§1–§12 and addendum sections); add a "This PRD feeds" list holding the UX deliverables. | The densest paragraph is the first one; the list doubles as a table of contents. |
| S4 | MERGE | §3 intro | Add: "Where a definition summarises a rule or a setting, the rule in §5 or the FR-20 table is authoritative." Optional: drop defaults and ranges from three glossary rows. | Precedence rule for duplicated values; avoids drift after approval. |
| S5 | QUESTION | FR-26 | Replace "(FR-7, FR-8, FR-15 to FR-18, FR-36)" with "(R-15)". | The list has drifted from R-15 (misses the notes from FR-9, FR-14, FR-33). |
| S6 | QUESTION | §5.7 | Add a "Rule (priority)" column. | Two-way index; shows the Must gate without cross-reading SM-1. |
| S7 | MERGE | DR-1 | Add the README items stated elsewhere: model download time (FR-28), reload resets settings and adjustments (DR-4), confirmed setup time (SM-2), unbuilt Should items with reasons (§8.2). | DR-1 becomes the one complete README checklist. |
| S8 | CONDENSE | DR-2, DR-5, DR-7 | Format as sub-bullets like DR-1; make the Definition of Done its own bullet group. | Checklists checked item by item. |
| S9 | QUESTION | §4.1–§4.9 headings | Tag every feature by core priority (§4.8 Must, §4.9 Should) and state the convention in the §4 intro, or drop the tags. | Headings mislead about mixed-priority features. |
| S10 | CONDENSE | §3 Glossary | Split into five or six short tables under unnumbered bold labels; keep every row verbatim. | Longest unbroken block; topic grouping. |
| S11 | CONDENSE | §5.7 E29 (and E11, E18) | Split into sub-rows E29 a … g. | One case per row, as the tests will be written. |
| S12 | CONDENSE | AG-3 | Point to FR-28's fallback list instead of repeating it. | One list to maintain. |
| S13 | CONDENSE | §5 source tags | Give R-10 and R-11 their own tags; turn "Known limitations of R-14" into a lead-in paragraph; decide on tags for R-13 and R-14 step 4. | The §5 intro promises a tag on every rule. |
| S14 | CUT | Repeated "one role per company"; FR-28 sentence on sprint planning | Keep §2.2 and §7; replace FR-1's Out of Scope block with "See §7"; cut the FR-28 sentence. | Five copies add nothing; FR-1 is the only FR with an Out of Scope block. |
| S15 | QUESTION | Pointers to addendum.md | Give every pointer its section (§5 intro → §4 and §6 there; NFR-9 → §2; §10 Q5 → §3; DR-5, §10 Q6, §12 → §7). Fix the stale "§10 question 4" in addendum §5 (now question 3). | Precise navigation between the two files. |
| — | PRESERVE | §11 source-status list, §6.2, UJ-1, §8, "recommends; decides" echoes, R-14 limitations | Keep. | Each serves a different reader. |

**13 minor fixes:**
1. §1: merge the two "recommends; decides" sentences (optional; the user's own principle).
2. §4.3 description: cut the NFR-2 module sentence.
3. FR-22, FR-30 and the Could FRs have no "Consequences (testable)" block, although §0 says each FR has one; add the label or qualify §0.
4. §11 heading → "Assumptions and Rule Sources".
5. DR-5's closing pointer repeats §0 and §12.
6. SM-2's verification sentence repeats §10 Q2 and DR-9.
7. Glossary "Stock on hand" restates R-13; add "(R-13)" and trim.
8. NFR-6 and FR-25 should cross-reference each other.
9. NFR-11 should cite NFR-7.
10. §8.1–§8.3 bullets could carry their feature section.
11. Turn the §9 brief-mapping paragraph into a two-column table.
12. §5.5 "Not a textbook index" could point to addendum §4.
13. §12's rule for the architecture, UX and epics documents, and §10 Q6, have no ID; DR-5 could reference them.

**Word impact if all accepted (estimate):** about −245 and +370 words, net about +125 (+1%). No ID, number or «» string changes.
