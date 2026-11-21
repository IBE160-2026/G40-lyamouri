# Deferred Work

- source_spec: none
  summary: Story 1.1, part B — record the planning phase in the process documents by starting `docs/statustabell.md` with every FR and DR-10, adding the planning-phase cases to `docs/ki-styringslogg.md` and adding the planning-phase AI defects to `docs/qa-logg.md`.
  evidence: The user split it from Story 1.1 in bmad-build's scope check on 2026-11-20, because these documents are compiled from the work log, the memlogs and the review files and can be reviewed and merged apart from the local start (part A); part B is built next on the branch `story/1-1-start-prognose-locally`, so Story 1.1 stays one pull request.

- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-start-prognose-locally-from-a-fresh-clone.md`
  summary: Consider amending AD-13 so that the phone test starts the app with `runserver --insecure <PROGNOSE_LAN_HOST>:8000` instead of `0.0.0.0:8000`, which `.env.example` now documents.
  evidence: Review pass 1 of Story 1.1 (BH-8, EC-13): `0.0.0.0` listens on every network interface, and `ALLOWED_HOSTS` checks only the Host header, which any client can set, so it is not access control; binding to the private address limits the app to the network being tested (NFR-3). The command comes from AD-13, so changing it needs the user's approval and a row in the spine's change log.

## Deferred from: code review of spec-1-1-start-prognose-locally-from-a-fresh-clone.md (2026-11-21)

- Only a manual `lsof` checks that `compose.yaml` publishes the database port on 127.0.0.1 (VG-4). A passwordless database with the image's superuser would accept connections from the network if the mapping lost its address, and no test would fail. A check of `docker compose config` fits the CI of Story 1.2, because `docker` may be missing from PATH when pytest runs.
