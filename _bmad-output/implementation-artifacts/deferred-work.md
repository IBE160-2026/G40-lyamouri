# Deferred Work

- source_spec: none
  summary: Story 1.1, part B — record the planning phase in the process documents by starting `docs/statustabell.md` with every FR and DR-10, adding the planning-phase cases to `docs/ki-styringslogg.md` and adding the planning-phase AI defects to `docs/qa-logg.md`.
  evidence: The user split it from Story 1.1 in bmad-build's scope check on 2026-11-20, because these documents are compiled from the work log, the memlogs and the review files and can be reviewed and merged apart from the local start (part A); part B is built next on the branch `story/1-1-start-prognose-locally`, so Story 1.1 stays one pull request.

- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-start-prognose-locally-from-a-fresh-clone.md`
  summary: Consider amending AD-13 so that the phone test starts the app with `runserver --insecure <PROGNOSE_LAN_HOST>:8000` instead of `0.0.0.0:8000`, which `.env.example` now documents.
  evidence: Review pass 1 of Story 1.1 (BH-8, EC-13): `0.0.0.0` listens on every network interface, and `ALLOWED_HOSTS` checks only the Host header, which any client can set, so it is not access control; binding to the private address limits the app to the network being tested (NFR-3). The command comes from AD-13, so changing it needs the user's approval and a row in the spine's change log.

## Deferred from: code review of spec-1-1-start-prognose-locally-from-a-fresh-clone.md (2026-11-21)

- Only a manual `lsof` checks that `compose.yaml` publishes the database port on 127.0.0.1 (VG-4). A passwordless database with the image's superuser would accept connections from the network if the mapping lost its address, and no test would fail. A check of `docker compose config` fits the CI of Story 1.2, because `docker` may be missing from PATH when pytest runs.
  - Resolved 2026-11-21 in Story 1.2: `tests/test_compose.py` checks `docker compose --file compose.yaml config`, skips only without `docker` on PATH, and ran without a skip in the first CI run on PR #10 (`spec-1-2-check-every-pull-request-automatically.md`).

- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md`
  summary: Run `uv run pytest` in the Windows workflow too, so that the README's «Tester» section is checked on Windows x64.
  evidence: The Windows workflow from Story 1.3 checks only the setup; no test ran on Windows, and tests such as the mode-600 check of `.secret_key` may assume macOS or Linux. It is outside Story 1.3's criteria, which cover the setup and the start.

## Deferred from: code review of spec-1-3-confirm-the-setup-on-windows-and-without-a-network.md (2026-11-22)

- The README and the spine's Platforms row name Windows 10 22H2 and Windows 11 23H2, which are past the end of Microsoft's servicing, and Docker supports Docker Desktop only on Windows versions still in servicing. Story 4.1 checks Docker Desktop 4.99.0's requirements and proposes minimum versions; changing the platform requirement needs the user's approval. Deferred: pre-existing, because the versions come from the PRD and the spine, not from Story 1.3.

## Deferred from: code review of spec-1-4-norwegian-app-shell-and-error-pages.md (2026-11-22)

- The focus ring and the link color would fail on the navy app header (BH-12). DESIGN.md gives every focusable element a 3 px blue ring and the header no focus color, and blue on navy is about 2.4:1, under the 3:1 that WCAG 2.2 1.4.11 asks of a focus indicator. Nothing in the logged-out header can take focus yet. Story 1.8 adds «Produktoversikt» and «Logg ut» there and needs a design decision, for example a white ring in the header.
- The database connection has no connect timeout (EC-6). `env.database_config` from Story 1.1 sets none, so psycopg waits up to 130 seconds when the port answers but PostgreSQL does not, for example while the container is paused. A stopped database refuses the connection at once and gives the 503 page. Story 1.4 does not change `env.py`.

## Deferred from: code review of spec-1-5-reference-spreadsheet-as-the-answer-key.md (2026-11-23)

- The only parser of the answer key's notation («S», «S2», «none», the lists and flags) is `tests/answer_key.py`, which pytest puts on `sys.path`, so `data/generate_seed.py` cannot import it cleanly (BH-31). AD-15 and AD-17 have the generator read the same workbook, so Story 1.6 decides where the shared reader lives instead of copying the parser.
- E14's week forecasts with seasonal adjustment off, the «flat» side of the last row in FR-21's table («E14: flat → seasonal»), are not in the answer key (BH-23). The story covers only the four FR-21 variants beyond PRD §5.7, so Story 5.1, which builds FR-9, records them, for example on E30 (off).

## Deferred from: code review of spec-1-6-generate-the-synthetic-seed-data.md (2026-11-23)

- The «Denne uken» figures of Testbedrift A (4 products to order soon, 31 units, 1 without a forecast, 4 with warnings), every product's confidence label and the claim that the 21 other products are quiet are checked only by a stand-in R-8 on the last three valid weeks in `tests/test_seed_data.py` (`suggested_quantity`, `warning_shapes`) and by an uncommitted script (VG-2, AA-2, EC-13). Story 2.8 checks them with the core and removes the stand-in.
- `uv run pytest`, including `tests/test_seed_data.py`, does not run in `.github/workflows/windows-setup.yml`, and its `paths:` filter omits `data/**`, `reference/**`, `tests/**` and `.gitattributes`, so the claim that the seed files are identical on Windows is untested (VG-1, EC-12). This extends the point of Story 1.3 above: run `uv run pytest` in the Windows workflow too. A change to a workflow needs an SSH push.

## Deferred from: code review of spec-1-7-load-the-seed-data-with-an-explicit-reset.md (2026-11-23)

- `CompanySettings` stores any window, factor, percentage or method name, because the FR-20 ranges in `src/forecasting/settings.py` are used only by the tests (BH-6, EC-10). Story 3.1 builds the form that reads the ranges, and should also decide whether the model gets validators or a check constraint, so a value outside the ranges can never reach the core.
- The clone step of `.github/workflows/windows-setup.yml` expects `load_seed` to create `.secret_key` and then stop with exit code 1 and the message «Databasen har allerede data». It cannot be run on macOS, so only the pull request's Windows run shows whether PowerShell passes the output through as the step expects (BH-12, EC-13, VG-3). If the run fails on that step, fix the step; the push needs SSH.

## Deferred from: code review of spec-2-7-show-what-to-order-and-whether-to-trust-it-on-the-product-screen.md (2026-11-27)

- A `CompanySettings` row with a window, a factor, a percentage or a method outside the FR-20 ranges makes `load_company_data` raise `ValueError` from the core's `check_settings`, so every product screen of that company gives a 500 (EC-1). Nothing in the app writes such a row today (`load_seed` writes the defaults), so it is not reachable yet. Story 3.1's form must stop the value first and keep the previous one, and decide whether the model also validates, as the Story 1.7 entry above says.
