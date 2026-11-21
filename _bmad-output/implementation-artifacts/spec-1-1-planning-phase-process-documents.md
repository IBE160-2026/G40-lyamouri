---
title: 'Story 1.1 part B: Record the planning phase in the process documents'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_commit: 'd8674addfaf3d789699f401ebfbc861df389b5b3'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/spec-1-1-planning-phase-process-documents-sources.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The status table and the AI steering log do not exist, although every later story must update them, and the QA log wrongly says that the planning-phase defects in AI output stay in the work log (DR-5, DR-8, DR-9; Story 1.1).

**Approach:** Create `docs/statustabell.md` with every FR and DR-10, create `docs/ki-styringslogg.md` with the planning-phase cases from the work log, and record the planning-phase defects in `docs/qa-logg.md`, each entry with its source and no reconstructed prompt. The sources file holds the inventories.

## Boundaries & Constraints

**Always:**
- Norwegian, in the style of `docs/qa-logg.md`; IDs, file names and commit hashes as in the sources.
- Every entry names its source as a file with a line or section. A commit or pull request appears only where a source names one; otherwise the entry says «ikke oppgitt i kilden».
- Summaries in own words: no planning-phase prompt is reconstructed or quoted as original, and the Canvas clarification is linked, not quoted.
- A defect that the group corrected appears in both logs, the case in the AI steering log and the defect in the QA log, each linking to the other.
- The status table uses only the DR-8 statuses (bygd, delvis bygd, ikke bygd, endret); today every FR is «ikke bygd».
- Decision (the user, 2026-11-20): in the QA log each review file gets one row, with its number of findings, its most important defects and a link, while every defect from the work log gets its own row; the review files stay the detailed record.

**Never:** changes to code, tests, the README, `docs/arbeidslogg.md`, the planning artifacts, the review files or the memlogs; README links (Stories 4.1 and 4.3); running part A's tests again; cases from the sessions of 2026-11-20, because the user accepted every recommendation and their review defects are already in the QA log; personal data, e-mail addresses, local paths or secrets.

</frozen-after-approval>

## Code Map

- `_bmad-output/implementation-artifacts/spec-1-1-planning-phase-process-documents-sources.md` -- the inventories for each document (A status table, B cases, C defects), with their sources; check each entry against its source before use.
- `docs/qa-logg.md` -- the «Tidligere funn» paragraph (line 10) is wrong and is replaced; the entries are dated `##` sections, the new one goes last, and the existing ones stay unchanged.
- `docs/arbeidslogg.md`, `.logs/mounia-03/`, the memlogs and the review files -- sources only.
- `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/avklaring-publisering-2026-11-19.md` -- the reason for DR-10, to link.

## Tasks & Acceptance

**Execution:**
- [x] `docs/statustabell.md` -- create it: an introduction (DR-8; the four statuses; «ikke bygd» without a reason means not built yet; every story updates the table, Story 4.3 completes it and Story 4.4 sets the final statuses); one table with the columns Krav, Navn, Prioritet, Status, Stories, Tester and Grunn til avvik; FR-1 to FR-36 in number order with FR-17b after FR-17, then DR-10; names translated from the PRD headings; stories from section A; tests «–»; DR-10 with the priority «ikke i versjon 1» and its reason linked to the clarification -- DR-8 and Story 1.1
- [x] `docs/ki-styringslogg.md` -- create it: an introduction (DR-5; the routine for AI sessions; the planning phase is documented by the work log, the memlogs and the session logs, and no prompt is reconstructed); cases 1–26 from section B in date order, each with «Hva KI foreslo», «Hva som var feil», «Hva gruppen bestemte», «Commit eller pull request» and «Kilde», and a link to the QA-log entry for every [QA] case -- DR-5
- [x] `docs/qa-logg.md` -- replace the «Tidligere funn» paragraph with one saying that the planning-phase defects are recorded in the new entry with their sources, linking to the introduction of the AI steering log; append «2026-11-20 – Feil i KI-generert tekst og kode fra planleggingsfasen (DR-9)» with section C: the work-log defects, without behaviour that is not text or code; the four examples, with the legend-icon rule marked as not fixed in the mockup and handed to Story 2.10; and one row per review file -- DR-9

**Acceptance Criteria:**
- Given `docs/statustabell.md`, when it is read, then each of FR-1 to FR-36 and FR-17b appears exactly once with the PRD's priority and «ikke bygd», and DR-10 appears once with its reason.
- Given `docs/ki-styringslogg.md`, when it is read, then its introduction says how the planning phase is documented, and every case has the five fields and a source that supports it.
- Given `docs/qa-logg.md`, when it is read, then it records E5, R-10 and R-11, the CSS rule that hit the legend icons and the 640/560 px breakpoint, each with how it was found, the fix, the commit where the source names one and the source, and no paragraph says that planning-phase defects stay out of the QA log.
- Given the three files, when they are scanned, then every commit hash exists in git, every cited file exists, and they hold no local paths, e-mail addresses or secrets.

## Implementation Notes

- Decisions within the spec: priorities are written as må-ha, bør-ha and kan-ha, and the introduction maps them to Must, Should and Could; both logs cite sources by short names defined in a key table with links, with line numbers as of `d8674ad`; the cases are numbered 1–26 in date order (sources B → log: 22→1, 23→2, 24→3, 2→4, 1→5, 3→6, 4→7, 5→8, 25→9, 6→10, 7→11, 8→12, 26→13, 9→14, 10→15, 11→16, 13→17, 12→18, 14→19, 15→20, 16→21, 17→22, 18→23, 19→24, 20→25, 21→26).
- The QA entry has the four examples as `###` blocks, a table «Andre feil fra arbeidsloggen» with one row per defect (the grouped rows in section C are split, 33 rows), and a table «Gjennomgangsfilene» with 14 rows: the 12 in section C and the two archived UX review files of 2026-11-07, because example 4 comes from one of them. AL:171 and AL:439 sit in their review-file rows instead of being repeated.
- Borderline items: AL:61 (the local path) is a QA row linked to case 3; AL:35 stays out as process behaviour; the old user name is covered by the Git-identity entry. Cases 15, 21, 24 and 25 also link to their QA rows, because section C lists those defects.
- Corrections to the sources file: FR-16 and FR-17 also list Story 2.5 («FR-15 to FR-19»), FR-29 also 6.3 and 8.2, and FR-30 also 8.3, from each story's Requirements line; `review-rubric-2026-11-15.md` has 1 high, 5 medium and 6 low findings; the delete-check fix has no commit, because `d2bfad2` was committed before the deletion (S987:162–180); E5 was not found by the calculation check (Pml:43, and no source says who found it); Story 1.8 before 2.3 (AL:538) is not fixed but an open point (`issues.md`:87).
- Verification: all 38 IDs appear exactly once in the status table, with the PRD §8.5 priorities and in number order; all 25 backticked hashes resolve to commits; the privacy grep prints nothing; a script found every table row with its header's column count, every link target and every heading anchor; every cited line was printed and read against its claim; `git diff` shows only line 10 replaced and the new entry appended in `docs/qa-logg.md`.
- Review pass 1 (2026-11-21) applied P1–P16: E5, case 7 and the breakpoint now match their sources; the QA work-log table has a «Nr.» column and 33 rows, including the Product Brief additions, the Safari script and the three final-validation gaps; the row for the 29 defects names its main defects; «Gjenstår» lists all four mockup differences, §10 question 4 and E30; both logs link to the repository at `d8674ad`; the AI steering log has a «Byggefasen» section; the status table's introduction covers every deviation and the D-2 and D-3 duties, and the FR-1 row lists its three tests.
- Verification after the patches, by the parent session: all 38 IDs appear exactly once, all 25 hashes resolve to commits, the privacy grep prints nothing, and every table row, linked file and anchor checks out.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-21): Blind Hunter (BH), Edge Case Hunter (EC) and Verification Gap (VG; no gap findings, one other finding). Patches P1–P16 went back to the implementation agent.

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | E5 (example 1, case 4) and case 7 misstate who proposed what | medium | The brainstorm memlog (line 65) records the round-up rule as the user's decision, and the PRD memlog (line 43) records the 6-decimal guard as a decision the user approved while §5 was drafted, so «Kildene sier ikke hvem som foreslo regelen» is wrong; case 7 says no AI proposal exists, while the PRD memlog (line 15) shows the AI-written `extract-brainstorm.md` made the teacher's answer decide the priority | patch P1 |
| BH-2 | Example 4 and case 11 say the review found the 640 px breakpoint | low | The archived `review-structure-prose.md` (line 49) itself proposes 640 px; 560 px came from the archived mockup (`key-produktoversikt.html`, line 165) when the proposal was applied (archived UX memlog, line 43), as the QA row for that file already says | patch P2 |
| BH-3 | The impossible mockup values (Skruer 21,5, Kabelstrips 3,7) are missing | low | EXPERIENCE.md (line 347) lists them, and session log 985 (lines 59–74) shows the 18 November review corrected the demo values; same root cause as BH-6 | patch P3 (with BH-6) |
| BH-4 | «Gjenstår» names only the legend icons as open in the mockup | low | EXPERIENCE.md (line 347) lists four mockup differences that the spines govern: 12 weeks, the legend icons, two impossible values, and 3 instead of 4 products with warnings | patch P4 |
| BH-5 | Two deferred rubric findings have no outcome | medium | The PRD memlog defers four findings (line 111) and closes two (line 117); §10 question 4 was tied to Story 2.6 in the final validation (session log 985, line 57) but no source closes it, and E30 (`review-rubric-2026-11-15.md`, line 101) has no closing record | patch P5 (with EC-1) |
| BH-6 | The row for the 18 November BMAD Review names none of its 29 defects | low | No review file backs that row, while session log 985 (lines 59–74) and `epics.md` (line 2305) list them | patch P3 |
| BH-7 | AD numbers from the archived architecture are not marked | low | The 8 November QA row (AD-12) and case 13 (AD-13, AD-16) use the numbering of the archived architecture, where they are other decisions than in the current spine; only story numbers are flagged | patch P6 |
| BH-8 | The status table has no place for an unbuilt epic or an untested Windows setup | low | D-2 (`epics.md`, line 47) and D-3 (line 52) put both in the status table; the structure is Story 4.3's work (lines 1829–1832), but the introduction does not mention either duty | patch P7 (introduction only, with EC-3); the structure is rejected as Story 4.3's |
| BH-9 | The AI steering log does not say that Story 1.1 gave no case | low | It has only the planning phase, so a reader cannot tell «no case» from «not recorded» | patch P8 |
| BH-10 | Links from the AI steering log to QA rows land on the whole table | low | Every such link goes to `#andre-feil-fra-arbeidsloggen`, a table of 30 rows with several rows per date | patch P9 |
| BH-11 | The cited line numbers will drift | low | They are pinned to `d8674ad`, but the key tables link to the working-tree files, and `docs/arbeidslogg.md`, `epics.md` and `issues.md` keep changing | patch P10 (with EC-7) |
| BH-12 | Case 2 is corrected AI text without a QA row | low | The rejected additions to the Product Brief are AI-generated text, which the «Utvalget» rule covers | patch P11 |
| EC-1 | Two deferred rubric findings were never closed | medium | Same as BH-5 | patch P5 |
| EC-2 | The status table promises a reason only for unbuilt må-ha and bør-ha rows | low | DR-8 asks for «the reason for any deviation», which also covers «delvis bygd», «endret» and unbuilt kan-ha rows | patch P12 |
| EC-3 | No place to mark an unbuilt epic | low | Same as BH-8 | patch P7 |
| EC-4 | Case 23 and the row for the 29 defects do not link to each other | low | The row names the A4 check that case 23 records, against the two-way rule in the QA entry's «Kildene» | patch P13 |
| EC-5 | Case 16 has no QA row | low | The tab was closed by a script Claude wrote, and the QA entry counts other faulty Claude commands (`sed`, the delete check) as code defects | patch P14 |
| EC-6 | Defects recorded only in a session log are missing | low | Session log 985 (lines 55–58) records three gaps the final validation fixed (E20 in Story 2.2, the rule test products in 2.6, R-14 and R-17 in 5.1 and 5.2), and «Kildene» names the session logs as sources | patch P15 |
| EC-7 | Line references drift | low | Same as BH-11 | patch P10 |
| VG-O1 | The FR-1 row lists no tests, but three tests name FR-1 | low | `tests/test_company.py` (lines 15, 51 and 67) names FR-1; the row says «–» because the spec's task line said «–» for every row, and listing the three tests is a one-cell correction | patch P16 |

## Design Notes

The session export of 2026-11-20, and the links to it from the session log and the pull request, belong to the session-log step, not to this build.

Leave every change uncommitted and do not run the `sesjonslogg` skill: the user approves each commit and push, and the parent session writes the session log afterwards.

## Verification

**Commands:**
- `for id in FR-{1..36} FR-17b DR-10; do echo "$id $(grep -c "| $id |" docs/statustabell.md)"; done` -- every line ends in 1
- every hash in backticks in the three files resolves with `git cat-file -t` -- prints `commit`
- `grep -n -E '/Users/|/private/|@gmail|BEGIN [A-Z ]*PRIVATE' docs/statustabell.md docs/ki-styringslogg.md docs/qa-logg.md` -- no output

**Manual checks:**
- The three documents are in Norwegian, agree with their sources, and every table row has the same number of columns as its header.
