---
title: 'Story 1.7: Load the seed data into an empty database, with an explicit reset'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'dispatch'
baseline_commit: '16d93b77d885918d3161b69233ce2b5c6a6fe058'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `load_seed` only creates `.secret_key`. The database holds only `Company`, so the files from Story 1.6 load nowhere, nothing persists products, sales weeks or settings (FR-4), and no command can restore the demo state (DR-4).

**Approach:** Add `Product`, `SalesWeek` and `CompanySettings` with one migration, and define the FR-20 defaults and ranges once in `forecasting/settings.py`. `web/seed.py` reads and validates the seed files, and `load_seed` loads them into an empty database, or with `--reset` and a typed confirmation replaces everything in one transaction.

## Boundaries & Constraints

**Always:**
- `load_seed` order: create `.secret_key` if missing (never overwrite), then read and validate every seed file, then touch the database. A non-empty database therefore still gets its key (open point of Story 1.1).
- The files are `*.json` in `settings.SEED_DIR`, which defaults to `data/seed/`, read in name order. Tests point `SEED_DIR` at temporary folders.
- Validation runs before any write and before the reset prompt. One Norwegian `CommandError` names the file and the product, and nothing is loaded or deleted. It refuses: `schema_version` other than 1; a missing key; an empty folder; a customer number that is blank or used twice; a product number that is not 5 digits or is used twice in all the files; a `first_week` that is not an ISO week; `units_sold` that is empty, negative, not a whole number or `null` (a gap); `stockout_positions` outside 1 to N or repeated; a negative or non-integer stock; a `password_hash` that Django's `identify_hasher` does not recognize (never a plain password); and products of one company that do not end at the same ISO week (AD-8).
- The hash is stored unchanged: `Company(password=<hash>)`, never `set_password`, so Django's `must_update` stays false and a login does not rewrite it (1.6 note).
- `SalesWeek` holds product, `position` (1 to N), `iso_year`, `iso_week`, `units_sold`, `stockout`. The latest data week is derived from these and never stored. Unique: (product, position) and (company, product number). Rows are created in bulk, in a fixed number of queries.
- `CompanySettings` is one row per company (`OneToOne`) with the FR-20 fields. Its model defaults read `forecasting/settings.py`, which holds each default and range once, the method names `moving_average` and `exponential_smoothing`, and only the standard library (AD-1, AD-9). `load_seed` creates each row from the model defaults.
- Without options and with any company in the database, it stops with a Norwegian message that names `--reset`, and changes nothing (DR-4).
- `--reset` prints in Norwegian what will be deleted, and asks the user to type `nullstill`. Any other answer, or no input, changes nothing. When confirmed, one `transaction.atomic` deletes every company (with products, sales weeks and settings) and every session, then loads the seed. A failure rolls it all back. `.secret_key` is never deleted. Nothing outside the command and the README calls `--reset`.
- After this story the status table lists FR-4 as built and FR-20 as partly built (defaults and ranges), tests name FR-4, FR-20, AD-8, AD-9, AD-15 or DR-4 (D-10), and the workbook's settings are checked against the ranges in `forecasting/settings.py` (open point BH-3).

**Never:**
- No `web/queries.py`, login, view, form or template (Story 1.8, Epic 3); no forecasting rule (Epic 2); no new dependency; no change to the generator, the seed files or the workbook; no `flush`, no raw SQL, no other command or build step that runs `--reset`.
- No plain-text password, secret or local path in a message, a log or the repository.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Empty database | `load_seed` | 2 companies, 62 products, every sales week, 2 settings rows with the defaults; the stored hash equals the file's | N/A |
| Database has data | `load_seed` again | stops, names `--reset`, counts unchanged | `CommandError`, non-zero exit |
| Data, no key file | `load_seed` | `.secret_key` is created, then it stops | as above |
| Reset confirmed | settings changed, sessions present, a product deleted, `nullstill` typed | the seed state returns, no sessions, no duplicates; the counts equal the first load | N/A |
| Reset on an empty database | `--reset`, `nullstill` | loads the seed | N/A |
| Reset not confirmed | `--reset`, then `ja`, a blank line, or no input | nothing changes; sessions stay | message, no deletion |
| Broken file | wrong `schema_version`, a gap, a negative number, a plain password, products ending in different weeks, a repeated product number, or a bad week | refused with the file and the product named; nothing loaded, and with `--reset` nothing deleted or asked | `CommandError` |
| Failure while loading | an error after the delete | the transaction rolls back; the old data stays | the error is raised |

</frozen-after-approval>

## Code Map

- `src/web/management/commands/load_seed.py` -- the secret-key code (lines 18–39) stays and runs first; the data loading is added after it.
- `src/web/models.py` -- `Company` (customer number, name, Django's password field); add `Product`, `SalesWeek`, `CompanySettings` beside it, with Norwegian `verbose_name`s like `Company`. `src/web/migrations/0001_initial.py` is the pattern; add `0002` generated by `makemigrations`.
- `src/prognose/settings.py` -- `SECRET_KEY_FILE` (line 23) is the pattern for a path setting; add `SEED_DIR` from `BASE_DIR`.
- `src/forecasting/__init__.py` -- the core's docstring; `tests/test_core_imports.py` checks that the new module imports only the standard library.
- `reference/answer_key_reader.py` -- `METHODS` (line 34), `SETTINGS` and the cases' values; the workbook-versus-ranges test uses them (`tests/test_reference_spreadsheet.py`, line 260).
- `data/README.md` -- the schema, which `web/seed.py` reads; the line that says Story 1.7 loads the files is updated. `data/generate_seed.py` has its own `validate`, `parse_week` and `end_week` for its in-memory data; `load_seed` must not import it (`data/` is no package and needs openpyxl), so `web/seed.py` has the same checks on the files.
- `tests/test_load_seed.py` -- the four secret-key tests assume no database access (`django_assert_num_queries(0)`, no `django_db`); they now need a `SEED_DIR` fixture and the database.
- `.github/workflows/windows-setup.yml` lines 64–82 -- runs `load_seed` twice against one database, the second time in a fresh clone only to create its `.secret_key`. After this story the second run stops on the loaded database.
- `README.md` (lines 34–62), `docs/statustabell.md` (FR-4, FR-20), `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md` (lines 95, 117, 122), `deferred-work.md` -- documents to update.

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/settings.py` -- FR-20 defaults, ranges and method names, once -- AD-9
- [x] `src/web/models.py`, `src/web/migrations/0002_*.py` -- `Product`, `SalesWeek`, `CompanySettings` (defaults from the core module) and the generated migration -- FR-4
- [x] `src/prognose/settings.py` -- `SEED_DIR` -- the tests need another folder
- [x] `src/web/seed.py` -- read and validate the files into plain records, raising a Norwegian `SeedError` -- AD-8, AD-15
- [x] `src/web/management/commands/load_seed.py` -- `--reset`, the confirmation, the transaction, the non-empty stop and the messages; update `help` and the module docstring -- DR-4, AD-15
- [x] `tests/test_forecasting_settings.py`, `tests/test_seed_reader.py` (with the helper `tests/seed_files.py`), `tests/test_load_seed.py` -- one test per matrix row, the counts and hashes, the defaults read from the core module, and a scan that only the command and the README mention `--reset`; the four old tests keep their claims
- [x] `tests/test_reference_spreadsheet.py` -- the workbook's settings fall inside the ranges and use the method names of `forecasting/settings.py` -- BH-3
- [x] `.github/workflows/windows-setup.yml` -- the clone step expects `load_seed` to stop after it creates the key; the push needs SSH (workflow scope) and the result shows in the pull request's run
- [ ] `README.md`, `data/README.md`, `docs/*`, `sprint-status.yaml`, `.logs/mounia-03/issues.md`, `deferred-work.md` -- how to generate and load, that a reset restores the seed state and resets the settings and adjustments (DR-1, DR-4), the new rows and checks, the story status and the open points

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given the loaded data, when the app and the database are stopped and started again, then every product, sales week and setting is unchanged (FR-4, SM-5); the user runs this check and the QA log records it.

## Implementation Notes

- 2026-11-23: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context was used as it was: the PRD and spine changes since it was compiled (E12 wording, the Windows test of Story 1.3) touch nothing here.
- Branch `story/1-7-load-the-seed-data-with-an-explicit-reset` from `16d93b7`. 66 new tests after the review, 238 in all, 1 skipped (the Docker check, because Docker is not on the PATH of this shell).
- `web/seed.py` reads and checks the files and touches no database; `load_seed` does all the writing, so only it and the migrations touch the tables (AD-7). The checks of `data/generate_seed.py` are not imported: `data/` is no package and needs openpyxl. A test reads the committed files, so the two stay in step.
- The reset prompt uses `input()`. A wrong answer or no input ends with a `CommandError` (exit code 1), as Django's own `flush` does, so a script cannot take a declined reset for a done one.
- `ordering` on `SalesWeek` was dropped after `makemigrations --check` found that a tuple differs from the list in the generated migration; queries order by `position` themselves. Ruff's RUF012 asked for tuples in `Meta`.
- Mutations applied to the code and then restored, all caught: the hash rewritten, sessions not deleted, the non-empty check removed, the confirmation check removed, the transaction removed, the key created after the data check, a changed default (the window), the end-week check removed, the hash check removed and the gap check removed. After the code review, a `--reset` added to `pyproject.toml` was caught by the widened scan.
- Run locally against the development database: `migrate`, `load_seed` (2 companies, 62 products, 5 016 sales weeks), a second `load_seed` (stops, exit code 1) and `--reset` with no input (stops, exit code 1). The restart check (FR-4, SM-5) needs Docker and was the user's: it passed on 2026-11-23 (QA log).
- The Windows job's clone step now expects `load_seed` to create the key and stop with exit code 1. It cannot be run here, so the result shows in the pull request's Windows run; the push needs SSH. Windows run 14 and CI run 34 passed on `b3b5157`, and the clone step got the message «Databasen har allerede data», so the step is verified. PR #20 was merged as `10b048a` and CI run 35 on `main` passed.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-23): Blind Hunter, run inline by the build session as in Stories 1.2 to 1.6, on the diff from `16d93b7` (82.4 kB, so at least 10 findings: min(floor(sqrt(82.4) + 1), 10) = 10). Edge Case Hunter, Verification Gap and Acceptance Auditor are skipped here, because BMAD Code Review runs them as independent subagents (D-8).

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | `schema_version` 1.0 passes as version 1, because 1.0 == 1 in Python | low | Real: `data["schema_version"] != 1` is false for 1.0, and only `bool` was excluded | patch: the type must be `int`, with a test case |
| BH-2 | No test reads the prompt of `--reset`, so «prints in Norwegian what will be deleted» is unchecked | low | Real: `typed` threw the prompt away | patch: `typed` returns the prompts, and the reset test checks that the prompt names the companies, the settings, the adjusted quantities and the word |
| BH-3 | `test_only_the_command_and_the_readme_name_the_reset` scans no README | low | Real: the name claims more than the test does | patch: renamed to `test_only_the_command_runs_the_reset`, and the status table follows |
| BH-4 | «A fixed number of queries» holds only up to the batch size of 2000 sales weeks | low | The seed has 5 016 weeks, so 3 batches; the test shows that products add no queries, which is the claim | reject: the claim is that the load does not loop over products |
| BH-5 | The model and the database accept a window of 99 or a factor of 0,0, since the ranges are not enforced | low | True now; the form and its validation come with Story 3.1 (AD-9), and the spec's Never keeps validators out | reject |
| BH-6 | `identify_hasher` accepts any hasher in `PASSWORD_HASHERS`, not only PBKDF2 | low | AD-15 asks for Django's hasher; the committed files are tested to be `pbkdf2_sha256` and to pass `check_password` | reject |
| BH-7 | `web/seed.py` and `data/generate_seed.py` check the same things twice and can drift | low | `data/` is no package and needs openpyxl, so an import is not possible; the committed files go through both in the tests | reject |
| BH-8 | The Windows clone step relies on PowerShell not stopping on the exit code 1 and the error text of `load_seed` | maybe-false | The job cannot run here; if it fails, the Windows job fails on the pull request | defer: settled by the Windows run of the pull request |
| BH-9 | «Bekreftelsen mangler» is also the message when there is no input at all | low | Cosmetic: the next sentence says that nothing is changed | reject |
| BH-10 | `Company.objects.all().delete()` loads the rows through Django's collector before it deletes them | low | About 5 000 rows of synthetic data, and the delete is the reset | reject |

BMAD Code Review (2026-11-23): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent subagents, on the working-tree diff from `16d93b7` without the spec (72.2 kB, 17 files). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor. 46 findings from the four reports: 7 medium and 39 low. 20 were patched, 2 deferred, 4 were false and 20 rejected. No finding needed a decision. The fixes are in the working tree; nothing is committed yet.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-1 | The key is created before the reset confirmation, so «ingenting er endret» is not exact | low | patch: the messages say «Ingen data er …» |
| BH-2 | `--reset` has no non-interactive path (`--noinput`) | low | reject: a flag that skips the typed confirmation would defeat DR-4 |
| BH-3 | «Empty» is only «no Company rows»; the check is outside the transaction | low | reject: products and settings cannot exist without a company (cascade) |
| BH-4 | The hash check is a prefix check, and 200 characters are accepted where the column holds 128 | medium | patch: the limit is read from the model; the prefix check stays (BH-6 of the build review) |
| BH-5 | Whole numbers above 2 147 483 647 reach the database | low | patch: the reader refuses them |
| BH-6 | The FR-20 ranges are defined but not enforced by the model | low | defer: Story 3.1 (the form), see `deferred-work.md` |
| BH-7 | `SalesWeek` has no unique ISO week, no `position` ≥ 1, no week range; migration 0002 is formatted differently | low | reject: the reader guarantees it; the migrations are excluded from Ruff by design (false for the formatting) |
| BH-8 | `CompanySettings` exists only through `load_seed`, and `create` skips `normalize_username` | low | reject: no other way to create a company exists in version 1 |
| BH-9 | The query-count test does not reach the batch size | low | reject: same as BH-4 of the build review |
| BH-10 | The `--reset` scan reads a short list of files | low | patch: every tracked file is read, except the command, the documents and the tests |
| BH-11 | The success line is printed before the commit | low | patch: it is printed after the transaction |
| BH-12 | The Windows step accepts any exit code 1 | medium | patch: the output must hold «Databasen har allerede data» (unverified until the Windows run) |
| BH-13 | README claims: `docker compose down -v` is not mentioned; no `SESSION_ENGINE` is set; DR-4 has no table row; a sentence in the status table is stale | low | patch for `down -v` and the sentence; reject the other two (the default session backend is the database, AD-10, and the table has no DR rows) |
| BH-14 | Tests copy counts and passwords; some cases are missing | low | reject: they restate what the README documents |
| EC-1 | A hash of more than 128 characters fails in the database | medium | patch: with BH-4 |
| EC-2 | Numbers above the column's maximum | low | patch: with BH-5 |
| EC-3 | `OverflowError` for a first week near 9999 | low | reject: not reachable by any seed file |
| EC-4 | `RecursionError` for deeply nested JSON | low | reject: not reachable |
| EC-5 | A customer number or name with a space first or last | low | patch: refused |
| EC-6 | Two runs at once pass the empty check | low | reject: one user per machine; the unique constraint fails loudly |
| EC-7 | `load_seed` before `migrate` gives a database error | low | reject: the README's order, and the error names the missing table |
| EC-8 | `bulk_create` may return no primary keys | false | PostgreSQL returns them (AD-14) |
| EC-9 | Other session backends are not cleared | false | AD-10 fixes the database backend |
| EC-10 | The model holds no validators | low | defer: with BH-6 |
| EC-11 | `SalesWeek` constraints | low | reject: with BH-7 |
| EC-12 | A failure on a path that is not a reset shows a traceback | low | reject: the transaction rolls back, and the error is loud |
| EC-13 | The Windows step passes for the wrong reason | medium | patch: with BH-12 |
| EC-14 | `$ErrorActionPreference` stays changed after a throw | low | reject: the step ends at the throw |
| EC-15 | The `--reset` scan is short | low | patch: with BH-10 |
| EC-16 | `prd_ranges` gives a `KeyError` when a PRD row changes | low | reject: it fails loudly, as the other PRD parsers do |
| EC-17 | Duplicate and end-week messages do not name file and product | low | patch: the files are named for a repeated customer or product number, and the products for the end weeks |
| EC-18 | The first key test no longer says «loads no data» | false | the old claim was about the old command; the key claims of the four tests are unchanged |
| EC-19 | The status table says «delvis bygd» for FR-4, not «bygd» | low | patch pending: «bygd» when the user has reported the restart check (AC 2) |
| EC-20 | «A fixed number of queries» is not literal | low | reject: with BH-9 |
| VG-1 | The reader's limits are copies of the model's | medium | patch: the limits are read from the models, with a boundary test |
| VG-2 | `--reset` can be abbreviated (`--res`) and a text scan misses it | low | reject the abbreviation (argparse's default, and nobody writes it); the scan is widened (BH-10) |
| VG-3 | Exit code 1 hides other failures in the Windows step | medium | patch: with BH-12 |
| VG-4 | The empty check is outside the transaction | low | reject: with EC-6 |
| AA-1 | FR-4 is «delvis bygd» in the table | low | with EC-19 |
| AA-2 | The documentation task is unfinished | false | planned after the review |
| AA-3 | A cross-file duplicate names neither file | low | patch: with EC-17 |
| AA-4 | A local path can leak into the message for an unreadable file | medium | patch: the error text is no longer shown, with a test |
| AA-5 | Bulk creation is not a fixed number of queries | low | reject: with BH-9 |
| AA-6 | The `--reset` scan is weaker than specified | low | patch: with BH-10 |
| AA-7 | `position` is not constrained to 1 to N in the database | low | reject: with BH-7 |
| AA-8 | An unconfirmed reset exits with code 1 | low | reject: as Django's `flush` does, so a script cannot take it for done |

**Deferred** (`deferred-work.md`): the range validation of `CompanySettings` (Story 3.1), and the Windows step, which only the pull request's Windows run can verify.

## Verification

**Commands:**
- `uv run python src/manage.py migrate` then `uv run python src/manage.py load_seed` -- expected: both companies loaded; a second `load_seed` stops with the Norwegian message.
- `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` -- expected: pass.

**Manual checks:**
- `docker compose down`, `docker compose up -d --wait`, then compare the counts of companies, products and sales weeks with those before; then try `load_seed --reset` and type `nullstill` -- expected: unchanged after the restart, and the seed state after the reset.
