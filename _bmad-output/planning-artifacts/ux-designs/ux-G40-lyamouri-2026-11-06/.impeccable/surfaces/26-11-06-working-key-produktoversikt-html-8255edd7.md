---
version: 1
slug: "26-11-06-working-key-produktoversikt-html-8255edd7"
primary_target: "_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/.working/key-produktoversikt.html"
related_targets: []
---

# Surface brief: Produktoversikt (dashboard)

- **Scope and mode:** the product overview shown after login (FR-24, UJ-1 step 1). Mode: Operate.
- **Task:** in the weekly review, see which products need ordering for uke 46, their suggested quantities and whether to trust them, then open a product.
- **Information and states:** 30 products in the R-12 groups (Bestill snart, Uten prognose, the rest), the FR-24 columns, confidence reasons for middels and lav, the overstock note, the reason shown instead of a number, and the empty state.
- **World contribution:** type, palette, density and one signature move only. Navigation and controls are standard web components.
- **Signature move:** the order quantity for Bestill snart sits in the magenta finish circle, and data quality and trust use the legend's symbols, explained in the rail.
- **Unresolved:** a per-row versus per-group overstock note (FR-14), search and sorting beyond R-12, dark mode.

## Direction contract

THESIS: A working product overview first. The map world enters only as type, palette, density and the legend's symbols. It refuses the KPI-card dashboard of hero numbers, sparklines and rings.

OWN-WORLD: The same tokens as the landing page: map-white ground, a pale green rail as the shell color, magenta reserved for action and Bestill snart, black symbols, the trust colors (green, ochre, red, always with a shape and a word), Albert Sans with tabular figures, and hairline rules.

STORY: Mounia scans the four Bestill snart rows first, reads each number and its trust, notices the product without a forecast, and opens the top product.

FIRST VIEWPORT: A left rail with navigation, the company and Logg ut. A header with the week context and one status sentence. A filter row. A table with the Bestill snart group first, all four rows visible at 1366 × 768, then Uten prognose and the remaining products.

FORM: Operate surface inside the O-kartet world; seed:aedd9cea56b9908b.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
