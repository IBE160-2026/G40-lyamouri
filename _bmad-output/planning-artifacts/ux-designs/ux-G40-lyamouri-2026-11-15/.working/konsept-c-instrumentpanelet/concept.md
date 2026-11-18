# Concept C – «Instrumentpanelet» (the instrument panel)

Status: concept for the user to choose from (2026-11-15). Source: the updated PRD only. Mockup: [index.html](index.html).

## Idea

Prognose works as an analyst's instrument panel: seeing comes before reading. The product list and the selected product share one screen, so Mounia steps through every product without losing the overview (UJ-1 step 5).

## Information architecture

- **Layout:** master and detail on one page, below a settings bar that shows the settings in use and «Endre innstillinger – gjelder alle produkter».
- **Left, the product list:** the R-12 groups. Each row shows the name, product number, weeks of cover, trust label, a 12-week sparkline and the number to order. The arrow keys step through the products, which also gives keyboard-only use (NFR-11).
- **Right, the selected product:**
  - Four key figures: stock on hand, week-1 forecast, suggested order quantity (highlighted) and weeks of cover.
  - A large line chart with the scenario band and markers that differ by shape (NFR-7): stockout is a hollow square, an unusual week a triangle, a level shift a diamond. A text alternative goes with it (NFR-11).
  - «Slik er tallene regnet ut»: the forecast calculation, the order calculation line and the scenario table.
  - «Tillit og varsler», and then «Forklaring».
- **No forecast (FR-24):** the list row shows «ingen prognose» and «–». The forecast figure carries the reason, and the order quantity and weeks of cover show «–».

## Visual personality

| Aspect | Choice |
|---|---|
| Colours | Cool, high-contrast: canvas #F1F5F9, text #0F172A, blue accent #1D4ED8, scenario band #BFDBFE. Status pills: green #166534 on #DCFCE7, amber #92400E on #FEF3C7, red #B42318 on #FEE4E2. |
| Header | A dark header bar. |
| Type | System UI at 14 px with tabular numerals. The key figures are 22 px. |
| Shape and depth | Compact panels with 6 px radii and thin borders. |
| Density | High, and visual. |
| Motion | Only selection and hover highlights are implied. |
| Trust signals | Pill plus shape (●, ▲ or ■) plus word. |

## Strengths

- It is the fastest way to work through all products.
- The shape of the demand, with its peaks and gaps, is visible at a glance, in the list and in the chart.
- It works well with the keyboard.

## Trade-offs

- It is the most visually complex.
- It depends most on good charts and their accessible text alternatives.
- The fixed list column takes width at 1024 px and below. NFR-6 requires readability down to 800 px, so the list must collapse there.
- It can overwhelm a first-time user.

## Elements you could take

- The master-and-detail layout with arrow-key navigation.
- Sparklines in the list.
- The key-figure tiles.
- The large chart with the scenario band and shape markers.
- The settings bar at the top.
- «Slik er tallene regnet ut» as one compact card.
