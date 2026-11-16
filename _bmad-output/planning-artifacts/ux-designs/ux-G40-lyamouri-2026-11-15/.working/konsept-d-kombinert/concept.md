# Concept D – «Kombinert» (combined)

Status: concept for the user to review (2026-11-16). It combines the parts the user picked from concepts A, B and C, which stay unchanged as documentation. Updated the same day at the user's request: the chart now sits right below the order suggestion and the confidence label. Source: the updated PRD only. Mockup: [index.html](index.html).

## What comes from where

| From | The user's pick | Where it is in D |
|---|---|---|
| C | The main layout, with the product list on the left | Both screens: header bar, settings bar, the list on the left and the selected product on the right |
| C | The large forecast chart | «Hva skjer med salget?» on the product screen, with the scenario band and shape markers |
| B | Product cards | One card per product in «Bestill snart» and «Uten prognose», with the suggested order quantity in large type |
| B | Clear order suggestions | «Hva bør du bestille?» at the top of the product screen: the number at 44 px, «Behold 11 og gå videre» and «Juster mengden» |
| B | A simple workflow | «Denne uken» after login, with the three steps, and «produkt 2 av 4» with previous and next on the product screen |
| A | Detailed calculations | «Slik er tallene regnet ut»: the forecast calculation, a table of week forecasts, scenarios and order quantity per scenario, and the order calculation line |
| A | Sales data | Sales per week for the last 12 weeks, with the status of each week |
| A | Explanations | «Forklaring» at the bottom of the product screen |
| User | Blue, turquoise and green, readable and with good contrast | See Visual personality |

## Information architecture

- **Layout (C):** the list is 392 px wide, and the selected product fills the rest. The list and the right side scroll separately.
- **Product list:**
  - «Produktoversikt» has a search field with a visible label.
  - «Bestill snart» and «Uten prognose» are cards. Each card shows the name, product number, stock on hand, week-1 forecast, weeks of cover and confidence label (with the reason when it is not «høy»), plus the suggested order quantity in large type. Every FR-24 field is in the list.
  - «Øvrige produkter» are compact rows with the same fields.
  - The arrow keys step through the products, as in C.
- **After login, «Denne uken» (B):** the three steps, four figures for the week, «Start med Isskrape», and a short key to the confidence label.
- **Product screen, top to bottom:**
  1. Name, confidence label, product number, stock on hand and weeks of cover. «Produkt 2 av 4 som bør bestilles snart» with a progress bar, and previous and next.
  2. «Hva bør du bestille?» and «Kan du stole på prognosen?» side by side. The first panel holds the suggested order quantity with «Behold 11 og gå videre» and «Juster mengden». The second holds the confidence label, its reason and the active warnings.
  3. «Hva skjer med salget?»: the large chart (C), right below the two panels, with a legend, a text alternative, and the switch for unusual weeks with «Endringen gjelder alle produkter i bedriften.».
  4. «Slik er tallene regnet ut» (A): sales for the last 12 weeks, the forecast calculation, the scenario table, and the order calculation line with its fixed text (FR-12).
  5. «Forklaring» (A).
- **No forecast (FR-8, FR-24):** a dashed card in the list with «–». The product screen says «Ingen foreslått bestillingsmengde» and «Du bestemmer bestillingen selv», with the «lav» label and the insufficient-data warning.

## Visual personality

| Aspect | Choice |
|---|---|
| Colours | Canvas #EDF2F7, white panels, navy text #0E2236 (also the header bar), and secondary text #4A5B6E. Blue #1D56C4 marks actions, links, selection and the suggested order quantity. Turquoise #08727A marks the forecast line, forecast weeks and «brukt», with tints #EBF7F8 and #C5EBEE for the forecast weeks, the scenario band and «Forklaring». Green #15703F on #E2F3E8 is for «høy» and completed steps. Red #B42318 and amber #7A4B00 stay for warnings, «lav» and «middels». |
| Contrast | Every text pair is at least 4.5:1 (measured). The lowest is turquoise on its tint, at 5.2:1. Chart lines and field borders are at least 3:1. |
| Type | System UI at 15 px with tabular numerals, and 13 px for secondary text. Headings are 16, 20 and 26 px. The suggested order quantity is 44 px (28 px on the cards). Formulas use the system monospace font. |
| Shape and depth | 10 px rounded cards and panels, hairline borders, no shadows. |
| Density | Medium: denser than B, roomier than C. |
| Motion | None. |
| Trust signals | A pill with shape and word, as in C: ● Høy, ▲ Middels, ■ Lav. The chart markers match the warning icons: a hollow square for a stockout week, a triangle for an unusual week, a diamond for a level shift. |

## Choices made in D for you to check

- **The chart sits right below the order suggestion and the confidence label** (the user's change, 2026-11-16). To get it there, the order calculation line moved to the end of «Slik er tallene regnet ut», where A had it, and the switch for unusual weeks moved below the chart legend. The active warnings stay with the confidence label, because FR-25 requires them to be visible without scrolling at 1366 × 768. At that size you see the chart's heading and top without scrolling, and you scroll for the rest. Moving the warnings below the chart would lift it further, but would break FR-25.
- **Cards only where a decision is needed.** The 25 products with nothing to order are compact rows, as in B, so the list stays short.
- **Left out, because they were not picked:** the sparklines and key-figure tiles from C, and the filter chips and letter-box labels from A. The numbered question circles from B are left out too; the questions remain as headings.
- **Added in D, and easy to drop:** the key to the confidence label in «Denne uken» (written from R-16), and the progress bar for the four products to order soon.
- **Red and amber are kept for warnings.** Green means «høy», so it cannot also mark a warning.
- **PRD wording.** D uses the exact texts from FR-7, FR-10, FR-12 and FR-21. A, B and C used other wording for some of them or left them out.
- **The explanation uses only the numbers FR-27 allows.** The «Forklaring» text in A, B and C names the calculation weeks 43 to 45 and the included unusual week 42. FR-27 allows only the week numbers of weeks 1 to 3 and of the weeks left out, so D leaves those numbers out.
- **The search field has a visible label (NFR-11).** A and C had placeholder text only.
- **The frame is 1366 × 640 px**, about what a browser shows on a 1366 × 768 screen. Below 1180 px the decision panels stack, and below 900 px the list moves above the product.

## Depends on Should items

- «Behold 11 og gå videre», «Juster mengden» and «Sett mengden selv» (FR-29).
- Step 3, the combined order overview (FR-30).
- Order quantity per scenario in the scenario table (FR-13).

Without them, the product screen keeps previous and next, and the scenario table loses its last column.

## Open points

- **UJ-1 step 4 with these example numbers.** Week 42 lies outside the 3-week window, so excluding unusual weeks leaves Strøsand's forecast at 14,3. The FR-21 confirmation would then read «Grunnprognose: 14,3 → 14,3». Either the confirmation needs wording for a change with no effect, or the demo product needs an unusual week inside the window, as in E8.
- **Not drawn yet:** the login page and the combined order overview (PRD §0 asks the UX step for both), the settings form, the confirmation after a settings change (FR-21), the overstock note (FR-14), the level-shift and seasonal-pattern warnings (FR-17b, FR-36), and a real check between 800 and 1024 px.
