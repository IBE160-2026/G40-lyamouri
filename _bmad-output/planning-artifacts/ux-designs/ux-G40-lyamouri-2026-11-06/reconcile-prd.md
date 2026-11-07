# Reconciliation: PRD and addendum against the UX spines (2026-11-07)

This checks that every UX-relevant requirement in `prd.md` and `addendum.md` has a home in DESIGN.md, EXPERIENCE.md or the approved mockups. It is a coverage check, not a restatement: the requirements themselves stay in the PRD.

| Source | Where the spines cover it | Status |
|---|---|---|
| UJ-1 (steps 1 to 6, edge cases) | EXPERIENCE Key Flows, Flow 1 | covered |
| §3 glossary, binding Norwegian labels | EXPERIENCE Foundation, Voice and Tone; DESIGN Do's and Don'ts | covered |
| FR-1 login and general error, logout | Login panel; State Patterns; internal note | covered, mocked |
| FR-2 isolation (not found for other company's data) | IA «Ikke funnet»; State Patterns | covered |
| FR-7 flat horizon and the fixed note | Calculation display rules (horizon) | covered, mocked |
| FR-8 insufficient data | Calculation display rules; State Patterns | covered, mocked (overview row) |
| FR-9, FR-36 seasonal adjustment and pattern warning (Should) | State Patterns («not possible»); Varsel pattern | covered |
| FR-10 scenarios and fixed sentence | Scenario strip | covered, mocked |
| FR-11, FR-12 order quantity and calculation line | Calculation line; Calculation display rules | covered, mocked |
| FR-13 order quantity per scenario (Should) | Scenario strip | covered |
| FR-14 overstock note (Should) | State Patterns (once per group in the overview) | covered, display decision approved by the user |
| FR-15 to FR-18 stockout, unusual, level shift, old data | Course chart markers; State Patterns; Varsel and Merknad | covered, mocked |
| FR-19 confidence label with reason | Confidence label | covered, mocked |
| FR-20 to FR-22 settings, validation, not in use, saved | Segmented control; Settings confirmation; State Patterns | covered (Produktside is wireframe-only) |
| FR-24 product overview, R-12 sort, empty state | Product table; State Patterns; internal note | covered, mocked |
| FR-25 product screen, above the fold at 1366 × 768 | IA wireframe (decision strip); Responsive & Platform | covered, spine-only |
| FR-26 to FR-28 template explanation, KI label, fallback | Forklaring | covered |
| FR-29 to FR-31 adjust, combined overview, session-only adjustments | Order table; State Patterns; IA wireframe | covered, spine-only |
| FR-32 CSV export (Could) | IA wireframe (placeholder) | noted |
| FR-33, FR-34 stock through weeks 2 and 3, MAE (Could) | — | not designed; planned when the items are scheduled |
| FR-35 forecast calculation | Calculation display rules; Calculation line | covered, mocked (landing) |
| NFR-1 local assets, no CDN | DESIGN Typography; Do's and Don'ts | covered |
| NFR-5 language and number format | Voice and Tone; DESIGN Typography | covered |
| NFR-6 desktop, no horizontal scroll from 1024 px | Responsive & Platform | covered |
| NFR-7 markers differ by more than colour, legend | Course chart; Tegnforklaring | covered, mocked |
| NFR-8 2-second response | State Patterns (no skeleton) | noted |
| NFR-10 robustness (decimal comma, no stack traces, not found, resubmit) | Text field; State Patterns | covered |
| NFR-11 accessibility | Accessibility Floor; DESIGN contrast table | covered |
| AG-1, AG-4 no AI numbers, labeled AI text | Voice and Tone; Forklaring | covered |
| DR-1 README screenshots (login page, product overview, product screen) | Mockups for two of the three; product screen from the wireframe | follow-up at build |
| Addendum §2 charting (Chart.js, NFR-7 markings) | DESIGN Components (Course chart); open check at build | covered |

**Dropped qualitative ideas:** none. The product principles in PRODUCT.md («Show the working», «Say when not to trust», «Recommend, never decide») are carried by the Calculation display rules, State Patterns and Voice and Tone.
