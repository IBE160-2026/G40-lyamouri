# Concept A – «Arket» (the sheet)

Status: concept for the user to choose from (2026-11-15). Source: the updated PRD only. Mockup: [index.html](index.html).

## Idea

Prognose works as a calm, checkable worksheet. The thesis it serves is "every number can be checked by hand".

## Information architecture

- **Product overview:** one dense table with the R-12 groups as table sections (Bestill snart, Uten prognose, Øvrige produkter). It has filter chips that set GET parameters, a search field, and the settings in use at the top right. About 30 products fit on one screen at 1366 × 768.
- **Product screen:** a numbered worksheet that reads top to bottom.
  1. Weeks used in the calculation, as a table with status tags.
  2. Prognoseutregning.
  3. Week forecasts and scenarios, as a table.
  4. Utregning av bestillingsmengde.
  5. «Forklaring».
- **Side column:** the confidence label with its reason, the warnings, a small chart, and the settings in use with «Endre innstillinger».
- **No forecast (FR-24):** the forecast cell shows the reason, and the order quantity and weeks-of-cover cells show «–».

## Visual personality

| Aspect | Choice |
|---|---|
| Colours | Near-monochrome: paper #FAFAF7, ink #1F2328, muted #57606A. One teal accent (#0B6E69) for links and «Bestill snart». Warning red #B42318; «middels» uses #7A4B00 on #FFF4DC. |
| Type | System UI at 13.5 px with tabular numerals. Formulas use the system monospace font. |
| Shape and depth | Square corners, hairline rules, no shadows. |
| Density | High. |
| Motion | None. |
| Trust signals | A letter box (H, M or L) plus the word, so colour never carries the meaning alone. |

## Strengths

- It is the easiest concept to check by hand.
- It shows the most products at once.
- It is plain and robust, and quick to build.

## Trade-offs

- It looks the most like a spreadsheet, the very thing the PRD positions Prognose against.
- It is less inviting for a first-time user or examiner.
- The chart is secondary.

## Elements you could take

- The table overview with group sections.
- The numbered worksheet on the product screen.
- Tabular numerals and formulas in monospace.
- The letter-box trust labels.
- The settings in use shown on every page.
