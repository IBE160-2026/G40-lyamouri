# Spine Pair Review — G40-lyamouri (coverage, 2026-11-16)

Pass 1 of the rubric walker in `.claude/skills/bmad-ux/references/validate.md`, run inline by the facilitator at Finalize. The Reviewer Gate's subagent lenses were not run, because the user asked for no subagents. The doc standards (`bmad-review`, structure and prose lenses) ran inline, and their eight fixes are applied.

## Overall verdict

Strong on mechanical coverage. Every user journey and success metric that touches the interface has a key flow, every token and cross-reference resolves, and every component has a visual and a behavioral spec. Two deliberate differences from the approved mockup are stated in the spines: the chart range, and possibly the size of the legend icons.

## 1. Flow coverage — strong

| Source item | Key flow | Protagonist, steps, climax, failure path |
|---|---|---|
| UJ-1 (steps 1–6, climax, edge cases) | Flow 1 | Mounia; 9 steps; climax at step 9; wrong login, no forecast, stock covers the need, Must-only build |
| SM-3 core flow | Flow 1 step 6, Flow 2 step 4 | old → new value shown (FR-21) |
| DR-1 «Prøv selv», SM-2, SM-9 | Flow 2 | Ingrid, the examiner; climax: the screen matches the hand calculation; out-of-range value, publishing cut line |
| SM-10 (teacher's feedback, point 4.5) | Flow 3 | Jonas; climax: he names the deciding condition of «lav»; revise and repeat if not |

## 2. Token completeness — strong

- DESIGN.md frontmatter: 26 colors (all valid hex), 17 typography roles, 5 radii, 13 spacing tokens, 40 component entries.
- 61 distinct token references in DESIGN.md (212 in all) and 3 in EXPERIENCE.md, all resolved against the frontmatter by script.
- Contrast is stated for every load-bearing pair (DESIGN.md, Colors). The lowest text pair is 5.2:1; turquoise on the band (4.46:1) is ruled out for text.
- Colors used only by the mockup's browser frame (`#DCE5EE`, `#E3EAF1`, `#A9B8C7`) are deliberately not tokens; the Impeccable detector reports them as three advisories.

## 3. Component coverage — strong

30 components, with identical names in DESIGN.md (Components) and EXPERIENCE.md (Component Patterns), checked by script. «Panel» had no behavioral row and got one.

## 4. State coverage — strong

| Surface | States covered |
|---|---|
| Innlogging | logged out, login failed |
| Produktoversikt | no products, no search match, nothing to order soon, product selected |
| Produktside | no forecast (two variants), suggestion 0, week-1 forecast 0, unusual weeks excluded, level shift, old data, seasonal adjustment on or not possible, seasonal pattern, settings changed (including no change), quantity adjusted, last product reviewed, language model on, focus |
| Innstillinger | invalid value, setting not in use |
| Samlet bestillingsoversikt | adjusted row, product without a forecast |
| Every page | not found, reload, Back, double submit |

Not applicable: offline (the local app needs no network, NFR-1), cold loading (server-rendered pages within 2 seconds, NFR-8), and permission states (one role per company).

## 5. Visual reference coverage — adequate

- `mockups/konsept-d-kombinert.html` is linked from DESIGN.md (Brand & Style) and from EXPERIENCE.md (the header note and the Information Architecture table), which name what it shows. Both spines say the spines win on conflict.
- Innlogging and Samlet bestillingsoversikt have wireframes in EXPERIENCE.md, as PRD §0 requires. Innstillinger and Ikke funnet are spine-only, specified in tables.
- No orphans. The concepts A to D stay in `.working/` as the audit trail and are not visual references.
- Known differences, stated under Open Questions and Assumptions in EXPERIENCE.md:
  - the mockup's chart shows 12 weeks, while FR-15 to FR-17 need a marker for every flagged week in the history;
  - the legend icons may render larger than specified.

## PRD and feedback trace

| Requirement | Where in the spines |
|---|---|
| PRD §0 wireframes (login, overview, product screen, combined order overview) | mockup (overview, product screen); EXPERIENCE.md wireframes (login, combined order overview) |
| PRD §12 open line: FR-24, the level-shift state and the explanation rule | EXPERIENCE.md: Component Patterns (Product card), State Patterns (level shift), Explanation |
| FR-1, FR-2, NFR-10 | Innlogging wireframe, Login panel, Not-found panel, Message Catalogue |
| FR-7, FR-10, FR-12, FR-35 | Calculation worksheet, Calculation Display Rules, Message Catalogue (exact PRD texts) |
| FR-8, FR-24 | Product card, State Patterns (no forecast), Message Catalogue |
| FR-13, FR-14, FR-17b, FR-36, FR-9 (Should) | Message Catalogue, State Patterns, Calculation Display Rules |
| FR-15 to FR-19, R-15, R-16 | Trust panel, Warning list, Forecast chart, Message Catalogue (warning texts the PRD leaves open) |
| FR-20 to FR-22 | Innstillinger, Unusual-weeks switch, Confirmation message |
| FR-25 (above the fold at 1366 × 768) | DESIGN.md Layout & Spacing; EXPERIENCE.md Trust panel and Responsive & Platform |
| FR-26 to FR-28 | Explanation (allowed numbers only, AI label, fallback) |
| FR-29, FR-30 | Decision panel, Combined order table, wireframe, Flow 1 |
| NFR-1, NFR-5, NFR-6, NFR-7, NFR-11 | Foundation, Voice and Tone, Responsive & Platform, Shapes, Accessibility Floor |
| Teacher's feedback 4.2 (allowed numbers) | Explanation |
| Teacher's feedback 4.4 (testable FR-24 and NFR-6) | Product card, Responsive & Platform (800 px) |
| Teacher's feedback 4.5 (SM-10) | Flow 3, the trust-label key on «Denne uken», the reason texts |
| PRD review 2026-11-15: warning texts without a copy source | Message Catalogue |

## Mechanical notes

- Both frontmatters parse as YAML, and both spines have `status: final`.
- Every relative link in both spines resolves.
- `mockups/konsept-d-kombinert.html` is byte-identical to `.working/konsept-d-kombinert/index.html`.
- Impeccable detector against the final DESIGN.md:
  - Mockup D: 0 findings, plus 3 advisories for the browser-frame colors.
  - Concepts A, B and C: findings against the new DESIGN.md, as expected, because they use their own palettes and fonts. They are kept unchanged as documentation, at the user's request.
