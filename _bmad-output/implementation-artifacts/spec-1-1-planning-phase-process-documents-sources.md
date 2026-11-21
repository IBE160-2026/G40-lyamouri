# Sources for Story 1.1 part B

Compiled on 2026-11-20 from three read-only investigations, for [spec-1-1-planning-phase-process-documents.md](spec-1-1-planning-phase-process-documents.md). Every commit hash below exists in git. Check each entry against its cited source before using it, and leave out or correct anything the source does not support.

**Keys.** AL = `docs/arbeidslogg.md`. QA = `docs/qa-logg.md`. S9nn = `.logs/mounia-03/9nn-*.md`. PRD = `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md`. EP = `_bmad-output/planning-artifacts/epics.md`. Memlogs under `_bmad-output/planning-artifacts/`: Bml = `briefs/brief-G40-lyamouri-2026-09-18/.memlog.md`, Pml = `prds/prd-G40-lyamouri-2026-11-02/.memlog.md`, Uml = `ux-designs/ux-G40-lyamouri-2026-11-15/.memlog.md`, Aml = `architecture/architecture-G40-lyamouri-2026-11-17/.memlog.md`. RS = `prds/prd-G40-lyamouri-2026-11-02/review-sensorveiledning.md`.

## A. Status table (DR-8)

- **DR-8 (PRD:771):** one table lists every FR and DR-10, with its priority, its status at submission (built, partly built, not built or changed), its stories and tests, and the reason for any deviation. The README links it in Stories 4.1 and 4.3 (EP:1762, EP:1829–1832). Story 1.1 asks only for every FR and DR-10 with its priority and status (EP:749). Every story updates the table (EP:589). Story 4.3 completes the columns, and Story 4.4 sets the final statuses with reasons (EP:1879–1881). An unbuilt Must story keeps its priority and gets a reason (EP:379).
- **DR-10 (PRD:773):** not in version 1. Publishing on Vercel with Neon, and Story 1.9, were removed after the teacher's clarification on Canvas on 2026-11-19 (D-1 at EP:32–43; AD-16 in the architecture spine). `prds/prd-G40-lyamouri-2026-11-02/avklaring-publisering-2026-11-19.md` summarises the clarification and is not a verbatim quote. DR-10 has no Must, Should or Could (PRD:804).
- **Current state:** no FR is built or partly built on the branch. `web.Company` and the Compose database are groundwork for FR-1 and FR-4, which Stories 1.8 and 1.7 build.
- **FRs** (PRD heading line · priority · main story first, then the others): 37 in all, with 24 Must, 8 Should and 5 Could. The PRD's order is not numeric, so the table uses number order.
  - FR-1 Log in with customer number and password · L172 · Must · 1.8
  - FR-2 Company data isolation · L184 · Must · 1.8 (2.7, 2.8, 2.11, 3.1, 3.3, 6.2, 6.3, 8.2, 8.3)
  - FR-3 Synthetic dataset with known patterns · L200 · Must · 1.6 (1.5, 2.6)
  - FR-4 Data stored between sessions · L212 · Must · 1.7
  - FR-5 Moving average · L226 · Must · 2.2
  - FR-6 Exponential smoothing · L234 · Must · 2.2
  - FR-7 Three-week forecast horizon · L242 · Must · 2.4 (2.5, 2.9)
  - FR-8 Insufficient data · L251 · Must · 2.2 (2.5, 2.7)
  - FR-9 Seasonal adjustment · L261 · Should · 5.1
  - FR-10 Three scenarios · L279 · Must · 2.4 (2.9)
  - FR-11 Suggested order quantity · L288 · Must · 2.4 (2.7)
  - FR-12 Order calculation line · L298 · Must · 2.4 (2.9)
  - FR-13 Order quantity per scenario · L309 · Should · 6.1
  - FR-14 Overstock note · L316 · Should · 6.1
  - FR-15 Stockout weeks left out · L329 · Must · 2.1 (2.5, 2.9, 2.10)
  - FR-16 Unusual weeks · L339 · Must · 2.1 (2.2, 2.9, 2.10; the switch in 3.3)
  - FR-17 Level shift · L351 · Must · 2.1 (2.2, 2.10, 5.2)
  - FR-17b Level-shift warning text · L379 · Should · 5.2
  - FR-18 Old-data warning · L362 · Must · 2.5
  - FR-19 Confidence label · L371 · Must · 2.5 (2.7, 4.2, 5.2)
  - FR-20 Company-wide settings · L401 · Must · 3.1 (5.1, 8.1)
  - FR-21 Changes apply to all products at once · L419 · Must · 3.2 (1.5, 3.3, 5.1, 8.1)
  - FR-22 Settings saved between sessions · L438 · Must · 3.1
  - FR-23 Settings per product · L445 · Could · 8.1
  - FR-24 Product overview · L455 · Must · 2.8 (1.8 gives the first list; 2.6, 2.11)
  - FR-25 Product screen · L464 · Must · 2.7 (2.10, 4.2, 5.2; settings from the screen in 3.2, 3.3)
  - FR-26 Template explanation in Norwegian · L493 · Must · 2.12 (5.1, 5.2, 6.1, 8.4)
  - FR-27 Explanation kept apart from calculated numbers · L502 · Must · 2.12 (5.1, 5.2, 6.1, 7.1, 8.4, 8.5)
  - FR-28 Optional local language model · L524 · Should · 7.1
  - FR-29 Adjust an order quantity · L546 · Should · 6.2
  - FR-30 Combined order overview · L555 · Should · 6.3
  - FR-31 Save adjustments and mark products as approved · L563 · Could · 8.2
  - FR-32 Export the combined order overview · L567 · Could · 8.3
  - FR-33 Stock not lasting through weeks 2 and 3 · L571 · Could · 8.4
  - FR-34 Forecast accuracy · L575 · Could · 8.5
  - FR-35 Forecast calculation · L476 · Must · 2.9 (5.1)
  - FR-36 Seasonal-pattern warning · L387 · Should · 5.2

## B. AI steering cases (DR-5)

- **DR-5 (PRD:761):** at least five cases, at least one per epic, where the group clarified, rejected or corrected AI output. Each records what the AI proposed, what was wrong, what the group decided, and the commit or pull request. The planning phase gives the first entries, for example E5 and R-10/R-11.
- **Routine for AI sessions (EP:598–604):** a corrected defect in AI output also goes into the QA log. No original planning-phase prompt is saved (S985:102), so no prompt may be reconstructed: the work log, the memlogs and the session logs are the record (EP:604). No process document states this yet. README, QA and AL §1 and §4 say nothing about it.
- **Cases** (date · title · AI proposed → what was wrong → what the group decided · commit · source). [QA] means the defect also goes into section C.
  1. 2.–3.11 · Prognosekonflikt R-10/R-11 · the rules gave 51,0 or 70,333 → one pass in time order · `4ada86d`, `d938baa` · AL:72; Pml:66, 75 [QA]
  2. 2.–3.11 · Avrunding i E5 · a float was rounded up from 70 to 71 → round to 6 decimals first (R-9) · `4ada86d` · AL:72; Pml:43 [QA]
  3. 2.–3.11 · Oppsettsmål på 10 minutter · a review agent proposed 10 minutes → 15 minutes kept, with no reason recorded · `4ada86d` · AL:72; RS:97, 142; Pml:79
  4. 2.–3.11 · Språkmodellen uten lærerens svar · FR-28 waited on the teacher's answer → made independent of it; the source names no explicit AI proposal · `4ada86d` · AL:72; Pml:69, 81
  5. 6.11 · Ti parallelle agenter stoppet · the quota ran out twice → no restart; one design, shown before it was worked out in detail · `23a7589` (named only in S996:191; AL:88 says nothing was committed then) · AL:84–85
  6. 7.11 · Den store varseltrekanten · a CSS rule for the chart also hit the icon → fixed · `23a7589` · AL:102; S996:65 [QA]
  7. 7.11 · Feil bruddpunkt og grafbeskrivelse · 640 px instead of 560 px, and a chart description that did not fit Chart.js → fixed in the documents · `23a7589` · AL:122 [QA]
  8. 8.11 · Django 6.1 eller 5.2 LTS · Django 6.1 proposed → the LTS version 5.2, for stability up to the deadline · `29dd679` · AL:137; S995:19, 46
  9. 8.11 · Addendumet i epics · a check the group asked for found four missing items and two forward references → fixed · `f74665b` · AL:147; S994:15–20 [mostly QA]
  10. 15.11 · FR-24 etter lærerens krav · Claude kept the UX layout instead of the teacher's example → the forecast column shows the reason, and the order column «–» · `47a8857`, PR #2 · AL:172; Pml:111, 115
  11. 15.–16.11 · Safari-faner · a script from Claude closed a tab → only `open -a Safari` from then on · no commit · AL:193; Uml:15; S988:44
  12. 15.–16.11 · Den store bryteren · `.chart svg` also hit the switch and the legend icons → one CSS line for the switch · `5db2fe7` · AL:194; Uml:21–22 [QA]
  13. 15.–16.11 · Grafen høyere opp · the group asked for it; Claude cited FR-25 → moved about 70 px only · `5db2fe7` · AL:191, 195; Uml:19–20
  14. 17.11 · PostgreSQL i begge kjøremodusene · SQLite locally, as the PRD said → PostgreSQL in both, with the consequences checked first · `1441c40`, `c76d6cd`, PR #3 · AL:422; Aml:9, 35
  15. 17.11 · Ingen automatisk sletting · automatic migration and seed → additive migrations only, seed only into an empty database, deletion only after a confirmed reset (DR-4) · `1441c40` · AL:423–426; Aml:28, 33, 52–53
  16. 17.11 · Docker bekreftet før godkjenning · port 54320 → the group asked for proof, and Claude separated documented, measured and untested claims; the port became 15432 · `1441c40` · AL:427; Aml:39, 43–46
  17. 18.11 · Epic 2 slått sammen · 15 stories → three pairs merged, with every criterion and test kept · `9dee8b1`, PR #3 · AL:475; EP:631
  18. 18.11 · NFR-8 kontrollert før endring · review finding A4 → checked first and kept unchanged (D-7) · `9dee8b1` · AL:476; S985:60
  19. 18.11 · Issues (A5) · judged from the summary of the examiner guidelines → corrected from the full guidelines · `9dee8b1` · AL:477; S985:101; EP:2308
  20. 18.11 · Ikke «godkjent» uten belegg · a link to «lærerens godkjenning av avgrensningen» → nothing is called approved without documentation · `9dee8b1` · AL:478; EP:2311
  21. 18.11 · Mobil og iPad · the README said PC only → NFR-6 widened · `9dee8b1` · AL:479; EP:2312
  22. 14.10 · Hoppede BMAD-steg · a fast path skipped the memlog and the closing steps → checked and completed · `5c4fb17` · AL:35; Bml:16, 21–22
  23. 14.10 · KI-tillegg i Product Brief avvist · four open gaps and other additions → the brief follows only the group's text, and the addendum was deleted · `5c4fb17` · AL:36–37; Bml:17–20, 24–26
  24. 1.11 · Personvernregel · a local path in a file → removed, and a standing rule set · `a55da02` · AL:61, 63
  25. 7.11 · Fem forbedringer av skissene · five fixes, with the design direction kept · `23a7589` · AL:94–101; S996:50–57
  26. 8.11 · Vercel som løsning · AD-13 made publishing optional → mandatory; reversed on 2026-11-19 · `21cd020` · AL:139; S995:59, 118
- **Leave out:** concept D (AL:185) and the conditional approvals of 16.11 (AL:224–225) are choices, not corrections. AL:52 is too vague.
- **Duplicates:** several cases are mentioned twice in AL, and each counts as one case: 132/137 (case 8), 420/423 (15), 455/476 (18), 466/479 (21), 191/194–195 (12 and 13) and 36/37 (23). AL:457 overlaps case 19.

## C. Planning-phase defects in AI-generated text and code (DR-9)

- **QA:10 is wrong.** It says these defects stay in AL's «Kvalitetssikring» bullets. The four examples in Story 1.1 (EP:754) are «Eksempel på styring av KI» bullets, and the QA log records none of them.
- **Defects in the work log** (date · defect · how found · fix · commit · source):
  - 2.–3.11 · R-10 and R-11 could give 51,0 or 70,333 · calculation check · one pass in time order · `4ada86d`, `d938baa` (S997:22) · AL:72
  - 2.–3.11 · 70 rounded up to 71 in E5 · calculation check · R-9 rounds to 6 decimals first · `4ada86d` · AL:72
  - 7.11 · a chart rule made the warning triangle as wide as the chart · the user · the rule applies to the chart only · `23a7589` (S996:65, 191) · AL:102
  - 7.11 · breakpoint 640 px instead of 560 px, and a chart description that did not fit Chart.js · review · the documents fixed · `23a7589` · AL:122
  - 8.11 · four requirements missing and two forward references in epics.md · check · fixed · `f74665b` · AL:147 (and an FR-1 criterion, S994:18)
  - 8.11 · Story 1.1 had no source for the session secret · clarity check · fixed · `425d818` (S993:22) · AL:153
  - 15.11 · 10 deviations in the PRD update · consistency review · fixed · `47a8857` · AL:171
  - 15.11 · FR-24 followed the UX design instead of the teacher's requirement · the user · changed · `47a8857` · AL:172
  - 15.–16.11 · `.chart svg` made the switch full width · the user · one CSS line · `5db2fe7` · AL:194
  - 15.–16.11 · concepts A–C used week numbers that FR-27 forbade, and the mockup showed only 12 weeks · Claude · concept D and the spines follow the PRD · `5db2fe7` · AL:196, 201
  - 16.11 · a check script reported «ingen funn» without reading the files · Claude · run again · `5373e7b` (S988:152) · AL:235
  - 16.11 · «för» instead of «for» in a fixed text · Claude · fixed · `e549c78` · AL:256
  - 16.11 · `.gitignore` lacked `.secret_key` and `db.sqlite3`, and a wrong date in the archive README · review · fixed · `d67211c` · AL:287, 289
  - 16.11 · the archive README said every sprint date had passed · check · fixed · `652f747` (S987:130) · AL:336
  - 16.11 · a `sed` command failed on macOS · the run · Python instead · no commit · AL:353
  - 16.11 · a wrongly written safety check in a delete command · it stopped before deleting · a new check · `d2bfad2` · AL:384
  - 17.11 · the archived architecture was out of date and contradicted itself; port 54320; outdated claims; 12 holes · Claude, the final check and an inline review · a new spine, port 15432 · `1441c40` · AL:405–410, 427, 437, 439
  - 18.11 · 29 defects (A1–A14, E1–E15); A5 built on a summary; an undocumented «godkjenning»; 1366 × 768 and NFR-2 · BMAD Review, the user, the final check · fixed · `9dee8b1` · AL:456, 477–478, 486
  - 19.11 · `PRODUCT.md` said the app is for PC only · check · fixed · `ea06f01` (PR #5) · AL:520
  - 19.11 · leftovers from publishing (AD-16), `uv sync` against `--locked`, Story 1.8 before 2.3, and the deadline 2026-12-01 · Implementation Readiness · fixed · `67694f7` (PR #6) · AL:535–538, 551
  - **Behaviour, not text or code, so leave it out of the QA log:** the Chrome test wrote outside the project (AL:87); the PostgreSQL test outside Docker, stopped by the permission system (AL:430).
  - **Borderline:** AL:35, AL:61 (`a55da02`), and the old user name in S987:118–120 (`3f6d417`). QA:27 already covers the user name.
- **The four examples Story 1.1 names:**
  - **E5:** AL:72; S997:19; Pml:43, where the rule was set while §5 was drafted, before the reviews; `prds/prd-G40-lyamouri-2026-11-02/reconcile-brainstorm.md:29`, where the brainstorm rounded straight up. The fix is R-9 (PRD:612) and E5 (PRD:671), in `4ada86d`. No source says who found it.
  - **R-10 and R-11:** AL:72; S997:19; `review-calculations.md:30` (F1, critical) and :74 (M1); `review-rubric.md:101–105`, which gives 71,0 for the other reading. The fix is in Pml:74–75, E15 (PRD:682) and `addendum.md:189`, in `4ada86d`.
  - **The legend icons:** the rule is in `ux-designs/ux-G40-lyamouri-2026-11-15/mockups/konsept-d-kombinert.html:182`. Sources: S988:117; Uml:21–22; `review-coverage.md:49, 98`; EXPERIENCE.md:347; DESIGN.md:476; EP:492 and EP:1444 (Story 2.10). AL names only the switch (AL:194) and the similar triangle (AL:102). The switch was fixed in the mockup (:183, `5db2fe7`). The icons were left as they were at the user's instruction, and the rule moved to the spines (`5db2fe7`) and to Story 2.10 (`9dee8b1`). **The icons are still not fixed in the mockup.**
  - **The breakpoint:** AL:122 is the only source outside the archive; S996:77 shows the mockup rule («under 640 px»). The fix is in `23a7589`.
- **Review files** (findings · defects · whether fixes and commits are recorded · most important defects). Every file is in `prds/prd-G40-lyamouri-2026-11-02/` unless named otherwise. None names a commit. «About n» is the investigator's count of contradictions, wrong results and wrong claims; the other findings are gaps or style.
  - `review-calculations.md` · 19 findings and 16 missing examples · about 9 defects · fixes not recorded · F1 (processing order), F2 (a product both «lav» and «middels»), F4 (0/0 in R-14)
  - `review-rubric.md` · 21 findings (3 high, 11 medium, 7 low) · about 10 · not recorded · the Must gate includes E14; two readings of the level shift; the FR-12 line sums to 20, not 21
  - `review-consistency.md` · 38 findings (1, 12, 25) · about 20 · not recorded · PR-1, IC-3, IC-2
  - `review-sensorveiledning.md` · 29 findings (8, 16, 5) · 1 defect (1.7, wrong addendum references) · its Outcome section lists the fixes
  - `review-structure-prd.md` · 15 findings and 13 minor · about 3 (S5, S15) · not recorded
  - `review-prose-prd.md` · 22 findings and 22 minor · about 5 (P3, P8, P11) · not recorded
  - `review-structure-addendum.md` · 9 findings and 2 minor · about 3 (A1, A6) · not recorded
  - `review-prose-addendum.md` · 23 findings and 14 minor · about 4 (P1 misstates its source, P19 misquotes) · not recorded
  - `review-consistency-2026-11-15.md` · 10 findings (0, 3, 7) and 11 downstream · all 10 · fixed in `47a8857` (AL:171) · C-2, C-1, C-3
  - `review-rubric-2026-11-15.md` · 12 findings (1, 6, 5) · about 7 · not recorded · the FR-27 allowed numbers; FR-28 misses swapped placeholders; downstream documents contradict it
  - `ux-designs/ux-G40-lyamouri-2026-11-15/review-coverage.md` · no numbered findings · 1 gap fixed (:27), 2 mockup defects kept · the «eight fixes» (:3) are not listed
  - `architecture/architecture-G40-lyamouri-2026-11-17/reviews/review-inline.md` · 12 findings (8 holes, 4 gaps), each with its fix · `1441c40` only through AL:441 · hole 6 (the secret file in the deployment), hole 7 (an open redirect), hole 3 (no company filter)
- **Already in QA, so do not repeat:** the Git-identity entry (QA:27 covers the old user name) and the review findings from Story 1.1 part A (`93c9147`).
