---
title: 'Sprint Plan: Prognose (G40-lyamouri)'
status: final
created: '2026-11-19'
updated: '2026-11-19'
deadline: '2026-12-08 23:59'
sources:
  - '_bmad-output/planning-artifacts/epics.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md'
companions:
  - 'sprint-status.yaml'
---

# Sprint Plan: Prognose (G40-lyamouri)

`sprint-status.yaml` tracks the status of each story. This plan holds what that file cannot: the milestone dates, the test dates, the order and the fallback order, which DR-6 and the planning constraints in `epics.md` leave to sprint planning. The user approved it on 2026-11-19.

## Basis

- **Deadline:** 8 December 2026 at 23:59 (DR-6).
- **Capacity:** one person, about 5 to 6 hours a day, weekends included.
- **Scope:** all 27 Must stories are planned. Should stories start only after M4, and Could stories (Epic 8) are not planned.
- **Fixed dates:** the Windows x64 PC is available on 2026-11-25 and 2026-12-07, and the two people for SM-10 on 2026-12-03 and 2026-12-04.
- **Readiness:** the implementation-readiness check of 2026-11-19 gave CONCERNS. The milestones are set here. The text findings were fixed, with rows in the change logs of `epics.md`, the architecture spine and the PRD, and the note on Story 1.8 is an open point in `.logs/mounia-03/issues.md`.

## Milestones

| Milestone | Date | Done when |
|---|---|---|
| M0 | Fri 2026-11-20 | This plan, `sprint-status.yaml`, the readiness fixes and the new deadline are merged into `main` |
| M1 | Tue 2026-11-24 | Epic 1 except Story 1.3 (7 stories), with the first test on the real iPhone 13 in Story 1.8 |
| M2 | Mon 2026-11-30 | Epic 2 (12 stories); SM-1 passes with all 24 Must reference examples |
| M3 | Wed 2026-12-02 | Epic 3 (3 stories); SM-3 passes, so the Must scope has passed its gate (DR-6, SM-C2) |
| M4 | Fri 2026-12-04 | Stories 4.1 to 4.3, with SM-10 on 2026-12-03 and 2026-12-04; the Must scope can be submitted |
| M5 | Sun 2026-12-06 | A buffer for Must stories; otherwise Should stories in the PRD §8.2 order. No new feature starts after this day |
| M6 | Mon 2026-12-07 to Tue 2026-12-08 | Story 4.4 on the final commit on 2026-12-07. 2026-12-08 is the buffer for fixes and the submission by 23:59; a fix after the final check makes a new final version, which is checked again before the submission |

## Test Dates

| Test | Story | Date |
|---|---|---|
| Real iPhone 13 over the local network (NFR-6, AD-13) | 1.8, 4.4 | By 2026-11-24, and on the final commit on 2026-12-07 |
| Windows x64 setup and offline start (SM-2, D-3) | 1.3 | 2026-11-25, after M1, so that it also covers the login |
| Impeccable finish review | 4.2 | 2026-12-03 |
| SM-10 with two people outside the group | 4.2 | 2026-12-03, after SM-3 has passed; 2026-12-04 for a second round if the first fails and the texts are fixed |
| Setup time on macOS, from the clone to logged in (SM-2) | 4.1, 4.4 | 2026-12-03 to 2026-12-04, and on the final commit on 2026-12-07 |
| Windows x64 setup on the final commit (SM-2, D-3) | 4.4 | 2026-12-07 |
| The manual checklist (NFR-6, NFR-7, NFR-8, NFR-11, SM-2 offline) and the privacy scan of the whole history (NFR-4, DR-9) | 4.4 | 2026-12-07 |

The Windows x64 PC is available only on these two days. A fix after the test on 2026-11-25 is checked again on macOS at once, and on Windows on 2026-12-07.

**Fixes after the final check.** Every fix after the final check on 2026-12-07 makes a new final version, and the checks of Story 4.4 run again on that version before the submission. The Windows x64 PC is not available after 2026-12-07, so the QA log then records which commit the Windows check ran on (D-3).

## Order

1. Epic 1: Stories 1.1, 1.2, 1.4, 1.5, 1.6, 1.7 and 1.8. Story 1.5 may be built alongside Stories 1.1 to 1.4 and is done before Story 1.6. Story 1.3 runs on 2026-11-25 and blocks no other story.
2. Epic 2: Stories 2.1 to 2.12.
3. Epic 3: Stories 3.1 to 3.3.
4. Stories 4.1, 4.2 and 4.3.
5. Should, only once M4 is reached: Stories 5.1, 5.2, 6.1, 6.2, 6.3 and 7.1 (PRD §8.2). The work can stop after any of them with nothing half built.
6. Could (Epic 8): not planned; the stories stay in the backlog.
7. Story 4.4, always last, on the final commit.

`sprint-status.yaml` lists the stories by epic, so Story 4.4 comes before Epic 5 there. The order above wins, so the story is named when `bmad-build` starts. Retrospectives are optional and not planned.

## Fallback Order

If the work is more than one day behind at M1, M2 or M3, the remaining Must stories are built in this order, 2026-12-05 and 2026-12-06 are used for Must stories, and no Should story is built (`epics.md`, Planning constraints):

1. The stories that SM-1, SM-2, SM-3 and DR-1 need: 1.1 to 1.8, 2.1 to 2.9, 3.1, 3.2 and 4.1.
2. Story 4.2 (SM-10, which the teacher tied to the PRD's thesis), and Stories 2.12 (SM-6) and 4.3 (SM-8), two success criteria of the Product Brief.
3. Stories 2.10 (the chart), 3.3 (the switch below the chart) and 2.11 («Denne uken», the review sequence and search).
4. Story 4.4, last; it is never cut.

A Must story that is not built is marked as not built, with the reason, in the status table and the README (DR-8). No priority changes. SM-10 runs only after SM-3 has passed (PRD SM-10), and the two people are available only on 2026-12-03 and 2026-12-04, so M3 must hold.

## Change Log

Every change to this plan is recorded here with the date, the reason and the commit.

| Date | Change | Reason | Commit |
|---|---|---|---|
| 2026-11-19 | Plan created: milestones M0 to M6, test dates, order and fallback order. | Sprint planning with the user on 2026-11-19, after the implementation-readiness check and the new deadline of 8 December 2026 at 23:59. | not committed yet |
