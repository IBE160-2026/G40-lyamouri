# Spine coverage check, Pass 1 (2026-11-07)

The rubric walker's mechanical Pass 1 from `references/validate.md` ran proactively at Finalize. The checks were done by script where possible and by reading the spines otherwise. The optional multi-lens Reviewer Gate (Pass 2 judgment by separate reviewers) was not run; it is offered to the user.

| Category | Verdict | What was checked |
|---|---|---|
| 1. Flow coverage | strong | UJ-1 is a Key Flow with its verbatim PRD name, the named protagonist Mounia, numbered steps, a climax and failure paths. A second flow covers the examiner's «Prøv selv» path (DR-1, SM-2); its protagonist is a role, because the PRD names no examiner persona. |
| 2. Token completeness | strong | All 42 `{path.to.token}` references in both spines resolve. All 22 colors have hex values. The design is light-only by decision, so no light and dark pairs are expected. Contrast for every load-bearing pair is stated in DESIGN.md Colors. |
| 3. Component coverage | strong | 21 components with identical names appear in both DESIGN.md Components (visual spec) and EXPERIENCE.md Component Patterns (behavior). |
| 4. State coverage | strong | Each IA surface has its states in EXPERIENCE.md State Patterns: logged out, login error, no data, empty filter, no forecast, stock covers next week, excluded unusual weeks, level shift, old data, a setting not in use, an invalid setting, a changed setting, seasonal adjustment not possible, adjusted and invalid adjusted quantities, not found, resubmit, and fonts unavailable. There is no loading skeleton, because the pages are server-rendered within the 2-second target (NFR-8). |
| 5. Visual reference coverage | strong | `mockups/key-landing.html`, `mockups/key-produktoversikt.html` and `mockups/designnotat-tilstander.html` are linked from both spines. Produktside and Samlet bestillingsoversikt have inline wireframes and are marked spine-only. `wireframes/` and `imports/` are empty. «The spines win on any conflict» is stated in both files. |

## Low findings

- **low** Samlet bestillingsoversikt has no state row for «no data loaded». The Produktoversikt empty state applies to it too. *Fix:* name both surfaces in that row.
- **low** The status sentence in the Samlet bestillingsoversikt wireframe gives 3 «Justert av deg». The demo data has 2. *Fix:* «28 «Foreslått» · 2 «Justert av deg»».
