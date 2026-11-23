---
title: 'Story 1.6: Generate the synthetic seed data'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'dispatch'
baseline_commit: '1610325cf1f4631523e4b5ffc5ae57616284a906'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `data/` holds nothing. Stories 1.7 and 1.8, Epic 2's tests and the examiner have no test companies, and the rule test products exist only inside the reference spreadsheet (FR-3, AD-15).

**Approach:** `data/generate_seed.py` writes `data/seed/testbedrift-a.json` and `testbedrift-b.json`, one file per company, identical on every run. The rule test products and Strøsand 25 kg take series and stock from `reference/reference-examples.xlsx` through one shared reader; all other products come from compact product specs in the script. `data/README.md` documents the schema, the products and the patterns, and the root README gives the two logins.

## Boundaries & Constraints

**Always:**
- Schema version 1, per company: `customer_number`, `name`, `password_hash`, `products`. Per product: `product_number` (5 digits, text), `name`, `first_week` («2026-W45» form), `units_sold` (whole numbers, oldest first), `stockout_positions` (1-based, as in the workbook), `stock_on_hand`. The latest data week is not stored; it is `first_week` plus the length, and every product of a company ends at the same week (AD-8): A ends 2026-W45 (UX-DR46), B ends 2026-W44, so the two companies show different weeks.
- Output is identical on every platform: integer arithmetic only, no clock, no `random`, no floating-point functions. Noise comes from SHA-256 of the product number and the position. The files are UTF-8, with LF line endings, fixed key order and a final newline.
- Passwords: Django's `PBKDF2PasswordHasher`, a fixed salt per company and Django 5.2's default iteration count, so a login does not rewrite the hash. Plain passwords stand only in the generator and the README (the README must give them); the seed files hold the hash only (NFR-3). Customer numbers 1001 (A) and 1002 (B); passwords `testbedrift-a` and `testbedrift-b`.
- Testbedrift A, a hardware store with 30 products, 5-digit numbers 10001–10043: Isskrape (10007, stock 2, 3-week sum 24), Strøsand 25 kg (10012, from the workbook), Lyspære LED E27 9 W (10031, stock 12, sum 56), Skruer 4×40 mm, 200 stk. (10004, stock 20, a level shift in the last 12 weeks, sum 64), Snøskuffe aluminium (10040, 2 valid weeks, stock 6), Malertape 25 mm (10001, stock 40, sum 28), Kabelstrips 200 mm (10002, stock 25, sum 20), Tetningslist 6 m (10019, shorter than 104 weeks, stock 14, sum 9) and the E8 product (stock 50, from the workbook). Every other number is 10020 or higher. The 21 other products are stable, with no stockout, unusual or level-shift week and enough stock to cover the need.
- Testbedrift B holds the other rule test products (E1, E7, E9, E10, E15, E16, E18 a, E18 b, E19) and pattern products: a known trend, a seasonal pattern without trend, stockout weeks, unusual weeks in the recent period, a level shift, a long run of stockout weeks at the end, stock that covers next week, a history for «høy», a product with fewer than 3 valid weeks and one with 3 to 11. Numbers 20001 and up. Each company has 10 to 50 products, most with 104 weeks, and at least one with fewer than 3 valid weeks, one with 3 to 11 and one with 12 to 103.
- Verified before the files are committed, by an independent script in the scratchpad (R-1 to R-16, not committed): «Denne uken» for A gives 4 products to order soon, 31 units, 1 without a forecast and 4 with warnings; Isskrape 7, Strøsand 11, Lyspære 9 and Skruer 4; Skruer's week-1 forecast is 21,3 and Kabelstrips' weeks of cover 3,8; no other product of A has an active warning; every pattern product shows its pattern and no product has an unintended unusual week, level shift or stockout.
- The shared reader of the workbook is `reference/answer_key_reader.py`, beside the workbook (the user's decision of 2026-11-23, BH-31). The generator and the tests add `reference/` to the import path; the PRD and mockup parsers stay in `tests/answer_key.py`.
- Tests name FR-3, AD-15, AD-8, NFR-3, NFR-4 or UX-DR46 (D-10), read the files with no database, and compare the rule test products with the workbook.

**Never:**
- No `load_seed` change, model, migration or database access (Story 1.7); no forecasting code in the repository (Epic 2); no change to the workbook; no new dependency.
- No plain-text password, real name, local path or personal data in any seed file (NFR-3, NFR-4).
- No copy of the workbook's notation parser in the generator, and no import of `tests/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Repeat run | the generator runs twice | both runs write byte-identical files | N/A |
| Committed files | a file differs from a fresh run | the test fails and says to run the generator | N/A |
| Workbook changed | a rule test product's series or stock differs in the workbook | the file differs from the committed one, and the sync test fails | N/A |
| Rule product missing | a mapped product has no row in the workbook | the generator stops and names the product | non-zero exit, nothing written |
| Broken run | a product's weeks do not end at the company's latest week, or a number is not 5 digits or is used twice | the generator stops before writing | non-zero exit, nothing written |
| Plain password | a seed file holds `testbedrift-a` or `testbedrift-b` | the NFR-3 test fails | N/A |
| Hash check | each stored hash with its README password | Django's `check_password` accepts it, and `must_update` is false | N/A |
| Local path | a seed file holds `/Users/`, `/home/` or a drive path | the NFR-4 test fails | N/A |

</frozen-after-approval>

## Code Map

- `tests/answer_key.py` -- lines 16–294 are the workbook reader (`Week`, `Row`, `parse_sales`, `parse_value`, `read_rows`, `read_typed`, `cases`, `products` and their constants); lines 296–448 parse the PRD and the mockup and stay in the tests. `WORKBOOK` is read when a function is called, which tests patch.
- `tests/test_reference_spreadsheet.py` -- imports `answer_key`, uses both halves (56 uses) and patches `answer_key.WORKBOOK`; it follows the moved names.
- `pyproject.toml` -- `pythonpath = ["src"]`; the folder of the reader is added. openpyxl 3.1.5 is a dev dependency, which `uv sync --locked` installs.
- `reference/README.md` -- documents the notation and says «Fra story 1.6 leser seed-generatoren også seriene»; add the reader's place.
- `src/web/models.py` -- `Company` with `customer_number` (max 20) and `name`; `load_seed.py` loads nothing yet. Neither is touched.
- `tests/test_app_shell.py` lines 16–22 -- how a test reads a planning document by its real path.
- The mockup `konsept-d-kombinert.html` (lines 255–345) and `EXPERIENCE.md` (Flow 1 and 3) -- the numbers, names, stocks and figures of A's demo products.
- `docs/statustabell.md` (FR-3 row), `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `README.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md` (lines 116 and 117), `deferred-work.md` -- documents to update.

## Tasks & Acceptance

**Execution:**
- [x] Scratchpad, not committed -- an independent R-1 to R-16 check of both seed files (the figures in Boundaries); finds a wrong tail or stock before the files are committed.
- [x] `reference/answer_key_reader.py` -- move the workbook reading out of `tests/answer_key.py`; the PRD parsers stay; update the imports and the path.
- [x] `data/generate_seed.py` -- product specs, series by integer arithmetic with hash noise, the workbook products, hashes, validation and writing.
- [x] `data/seed/testbedrift-a.json`, `testbedrift-b.json` -- generated and committed.
- [x] `data/README.md` -- in Norwegian: the schema, how to run the generator, every product with its number, the pattern or E-n it shows (FR-3, SM-7), and that Story 1.7 loads the files.
- [x] `tests/test_seed_data.py` -- one test per matrix row, plus the counts, the history ranges, the disjoint numbers and the patterns.
- [x] `README.md`, `reference/README.md`, `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md`, `deferred-work.md` -- the logins and the generator command, the reader, the FR-3 row, the checks and any difference, the work log, the story status and the open points.

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass.
- Given the generator run twice, when the files are compared, then they are identical and equal the committed files.
- Given each company, when its products are counted, then the ranges, the patterns, A's «Denne uken» figures and the rule test products agree with the sections above.

## Review Findings

BMAD Code Review of PR #18 (2026-11-23): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent subagents, on the diff from `main` to `1dff8db` without the seed JSON and the spec. 42 findings: 9 medium and 33 low, none high. 26 patches, 5 decisions and 11 rejected. The fixes are in `ecbf55d`.

The user's decisions (2026-11-23):
1. Windows (EC-12, VG-1): soften the text in `data/README.md` (tested on macOS and Linux only) and extend the deferred point about `pytest` in the Windows job; no workflow change.
2. «Denne uken» (EC-13, VG-2, AA-2, BH-7): add a test that computes R-8 on the last three valid weeks and compares with the mockup's quantities, totals and the four warnings; story 2.8 replaces it with the core and checks the labels.
3. Apply all patches P1–P9.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-1 | Seed JSON files left out of the diff | low | reject — left out to save tokens; the files are reproduced by running the generator, and the diff said where they were |
| BH-2 | Seasonal peak is in ISO week 27 and the trough in week 1, not 26 and 52 | low | patch |
| BH-3 | A workbook product that no company places is dropped silently | medium | patch |
| BH-4 | `validate` skips names, customer numbers, empty series and the schema's exact keys | low | patch — prefix, types and the `first_week` format rejected: derived from date arithmetic, and the committed files are tested |
| BH-5 | The salt comment says «128 bits of entropy»; iterations are not pinned | low | patch — comment fixed; pinning the iterations rejected (Django's default is chosen in the spec, and the hash test is the tripwire) |
| BH-6 | The privacy scan reads the base64 hash | low | patch |
| BH-7 | The mockup test never checks the suggested quantity or the totals | medium | patch — new «Denne uken» test (decision 2); the labels are deferred to story 2.8 |
| BH-8 | The mockup parser is fragile | low | reject — fails loudly |
| BH-9 | Pattern checks are ad hoc, and the cover threshold is undefined | low | patch — the threshold is now in `data/README.md`; the approximations stay (the core comes in Epic 2) |
| BH-10 | Trend and season exist only in Testbedrift B, unexplained | low | patch |
| BH-11 | The status table lists too few tests | low | patch |
| BH-12 | The LF test only reads `.gitattributes` text | low | patch — now uses `git check-attr` |
| BH-13 | `main` catches only `ValueError` | low | reject — any other error is loud and writes nothing |
| BH-14 | The two files are written one after the other | low | patch |
| BH-15 | The logins carry no «demo only» note | low | patch |
| EC-1 | Raw traceback for a missing workbook | low | reject — same as BH-13 |
| EC-2 | A workbook product row without company, sales or stock gives a `KeyError` | medium | patch — with BH-3 |
| EC-3 | Two workbook rows with the same product silently keep the last | medium | patch — with BH-3 |
| EC-4 | `validate` accepts repeated names and customer numbers | low | patch — with BH-4 |
| EC-5 | `dumps` regex rewrites list-like text inside strings | low | reject — the names are fixed, and a fix is more than a direct correction |
| EC-6 | A failure on the second file leaves a half-written pair | low | patch — with BH-14 |
| EC-7 | `mockup_products` gives a `TypeError` when «Foreslått» is missing | low | reject — fails loudly |
| EC-8 | `mockup_products` drops a malformed product silently | low | reject — the count of 8 catches it |
| EC-9 | `pattern_table` reads rows past the next heading | low | patch |
| EC-10 | The cover pattern passes a product with no valid weeks | low | patch |
| EC-11 | The privacy regex can match inside the hash | low | patch — with BH-6 |
| EC-12 | The Windows claim is tested only on Linux | medium | decision — decision 1: soften the text and defer |
| EC-13 | «Denne uken» claim has no committed test | medium | decision — decision 2: test added; the core in story 2.8 |
| VG-1 | No test of the byte-for-byte claim runs on Windows | medium | decision — decision 1 (with EC-12) |
| VG-2 | Suggested quantities, labels and totals are not asserted | medium | decision — decision 2; the labels deferred to story 2.8 |
| VG-3 | Skruer and 20014 fall back to 9 in the middle of the new level | low | patch |
| VG-4 | «Long ago» stockouts of 20012 are not checked | low | reject — the text is more precise than the approximation, with no harm |
| VG-5 | 20015 has 10 stockout weeks, the test needs 9 | low | reject — same |
| VG-6 | Several `validate` and `series_of` branches have no test | low | patch |
| AA-1 | The documentation task is not done | low | reject — not a defect: planned after the review, and done in the documentation commit |
| AA-2 | «Denne uken» for A is not checked by a committed test | medium | decision — decision 2 |
| AA-3 | `data/README.md` does not list every product | low | patch |
| AA-4 | `validate` does not compare the end week with the configured latest week | low | patch — with BH-4 |
| AA-5 | The test counts in the Implementation Notes are off | low | patch |
| AA-6 | The odd week among Skruer's new-level weeks | low | patch — same as VG-3 |
| AA-7 | `.gitattributes` is outside the spec | low | reject — a logged addition from BH-3 of the build review, with a test |
| AA-8 | The phone-number pattern can match inside the hash | low | patch — same as BH-6 |

**Deferred** (`deferred-work.md`): the core-based check of «Denne uken», the labels and the 21 quiet products (story 2.8); `pytest` and the seed tests in the Windows job.

## Implementation Notes

- 2026-11-23: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context was used as it was, as in Stories 1.4 and 1.5: the spine and PRD changes since it was compiled touch nothing here.
- The reader: the workbook half of `tests/answer_key.py` moved to `reference/answer_key_reader.py` (the user chose `reference/`); the PRD and mockup parsers stayed, and `mockup_products()` is new. `WORKBOOK` now points at the file beside the reader. `pyproject.toml` puts `reference` and `data` on pytest's path, and the generator adds `reference/` to `sys.path` when it runs as a script. The 151 earlier tests passed unchanged in behaviour after the move.
- The generator writes 30 products for A and 32 for B. Strøsand 25 kg (10012) and the E8 product (10025) are in A and the nine other rule test products (20001–20009) in B, each placed in the company the workbook names; the generator checks that.
- The independent R-1 to R-16 script in the scratchpad (not committed) found that A's «Denne uken» gives 4 products to order soon (Isskrape 7, Strøsand 11, Lyspære 9, Skruer 4: 31 units), 1 without a forecast and 4 with warnings, that no other A product has a warning, that every one of the 11 workbook products gets the expected base forecast, order quantity, unusual weeks, level-shift weeks, warnings and label, and that no product has an unintended unusual week, level shift or stockout. Skruer's forecast is 21,3 and Kabelstrips' cover 3,75 (3,8).
- Found by the tests, not by the build: the first salt, «prognoseSeedA» (13 letters), has about 77 bits of entropy, and Django's `must_update` asks for 128, so the first login would have rewritten the hash with a random salt and the fixed salt would not hold. The salts now have 24 letters (QA log). The first level-shift proxy in the pattern test also ignored that R-10 leaves out earlier unusual weeks from the baseline, so it missed Skruer; it now uses the baseline before the first of the three weeks.
- 17 tests in `tests/test_seed_data.py` at the first commit, 168 in all. Nine mutations, each applied to the committed files or the README and then restored, were all caught: a changed stock, a plain password, a local path, a wrong pattern product, a removed pattern row, a wrong README password, a changed hash, CRLF line endings and a dropped week.
- After the review (`ecbf55d`): 21 test functions in the file and 173 tests in all. «Denne uken» for A (4 products, 31 units, 1 without a forecast, 4 with warnings) is checked by a stand-in R-8 in `tests/test_seed_data.py`; the core and the labels are checked in story 2.8.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-23): Blind Hunter, run inline by the build session as in Stories 1.2 to 1.5, on the diff from `1610325` (130.4 kB, so at least 10 findings: min(floor(sqrt(130.4) + 1), 10) = 10). Edge Case Hunter and Verification Gap were skipped here, because BMAD Code Review runs them as independent subagents on the pull request (D-8).

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | `patches` and `tail` index the week list with a negative index when they reach past the history, so an edit silently lands on the wrong week | low | Real: `weeks[count - 1 - from_end]` wraps for `from_end >= count`; no current product does it | patch: both raise ValueError |
| BH-2 | `validate` does not refuse a negative stock on hand | low | Real gap in the schema check; no current product has one | patch: refused, with a test |
| BH-3 | Git for Windows with `core.autocrlf` checks the seed files out with CRLF, so the byte-for-byte test fails for an examiner who runs `uv run pytest` on Windows | medium | Real: the repository has no `.gitattributes`, and the test compares bytes | patch: `.gitattributes` with `data/seed/*.json text eol=lf` and a test that reads it |
| BH-4 | The error message says «Frøfilene», which is not the project's word for seed files | low | The project says «seed» (`load_seed`, «seed-generatoren») | patch: «Seed-filene» |
| BH-5 | `build_companies` imports the reader inside the function with no reason given | low | Real: a reader of the file would move it to the top | patch: a comment says the folder is on the path under pytest but not when the file runs as a script |
| BH-6 | `RECENT_WEEKS` is defined in the generator and never used | low | Real: found by search, and Ruff does not flag module constants | patch: deleted |
| BH-7 | A Django release that raises the default iteration count makes `must_update` true, so the hash test fails | low | Intended: it is the tripwire, and `data/README.md` says to run the generator again | reject |
| BH-8 | The pattern tests are proxies of R-10 and R-11, not the rules | low | True, and by design: the core of Epic 2 does not exist, so the independent script in the scratchpad ran the rules, and the open point for story 2.8 moves the check into the tests | reject |
| BH-9 | `mockup_products` and the README table parsers break when the markup or the table changes | low | They fail loudly with a named product or pattern, like the PRD parsers in Story 1.5 | reject |
| BH-10 | `data` on pytest's path could shadow another module | false | Its only module is `generate_seed`, and no other code has that name | reject |

## Design Notes

The generator's weekly series: `units = (level × (100 + noise) + 50) // 100`, with `noise` in −20…+20 from the hash and `level` from the product's shape (flat, a trend of fixed steps, a triangular seasonal profile, a tail forced to the mockup's sums). A flat product with a level of 8 or more gives at most a ratio of 1,5 between a week and its baseline, so R-10 never flags it; the scratchpad check confirms this for every product.

## Verification

**Commands:**
- `uv run python data/generate_seed.py` twice, then `git status` -- expected: no change after the second run.
- `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` -- expected: pass.
