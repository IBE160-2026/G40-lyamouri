# Deferred Work

- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-project-skeleton-running-locally-and-on-vercel.md`
  summary: Add a migration check (`python manage.py makemigrations --check --dry-run`) to the pre-pull-request checks, and let the owner confirm with `python manage.py migrate --check` that Neon has every migration after a merge.
  evidence: The architecture's pre-PR checks (DR-7) are only `test`, `ruff check` and `ruff format --check`. Under AD-16 the owner migrates Neon by hand. A model change merged without its migration, or a skipped migrate step, therefore shows up only as a 500 on the published app. `manage.py test` catches most missing migrations because it builds the test database from migrations. Adding a check changes an approved convention, so it needs an architecture decision (review finding BH-6, story 1.1).
