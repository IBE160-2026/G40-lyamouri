# Concept B – «Innkjøpsmøtet» (the purchasing meeting)

Status: concept for the user to choose from (2026-11-15). Source: the updated PRD only. Mockup: [index.html](index.html).

## Idea

Prognose works as a coach for the 20 minutes before the Monday purchasing meeting (UJ-1). It leads Mounia from "what is urgent" to a combined order to bring to the meeting.

## Information architecture

- **Overview, «Denne uken»:**
  - A three-step path: Se hva som haster → Gå gjennom produktene → Ta med samlet bestilling til møtet. The last step is FR-30, which is Should.
  - Four summary tiles: products to order soon, units suggested in total, products without a forecast, and products with warnings.
  - Cards for the R-12 groups. Each card shows the one number to order in large type, its stock and weeks of cover, and its trust label with the reason.
  - The products with no order suggested fall into a compact list.
- **Product screen:** three numbered plain-language questions.
  1. «Hva skjer med salget?»: the chart and the forecast calculation.
  2. «Kan du stole på prognosen?»: the trust label, the reason and the warnings, plus the unusual-weeks switch with «Endringen gjelder alle produkter».
  3. «Hva bør du bestille?»: the big number, the order calculation line, the scenarios, and «Behold» or «Juster» (FR-29, which is Should).

  After the three questions come «Forklaring» and links to the previous and next product.
- **No forecast (FR-24):** a dashed card with «Bestill –», «uker dekning –» and the reason. The product screen says «Du bestemmer bestillingen selv».

## Visual personality

| Aspect | Choice |
|---|---|
| Colours | Pale sage canvas #EEF2EC (changed from cream on 2026-11-15 after the Impeccable check) and text #2B2A28. The warmth comes from the ochre action colour #9A5B00 and the green ok colour #2F6B3A. Warning red #B42318, and «middels» in #7A4B00 on #FFF1D6. |
| Type | System UI at 16 px. Card titles are 20 px, section headings 24 px and page titles 32 px; the order number is 34 to 48 px. |
| Shape and depth | 12 px rounded cards with a soft shadow. |
| Density | Generous spacing, so density is low to medium. |
| Motion | One calm step transition between products is implied. |
| Trust signals | Shape plus word: circle for høy, triangle for middels, hollow square for lav. |

## Strengths

- It is the easiest concept to follow, for Mounia and for an examiner trying it for the first time.
- It reads as UJ-1 itself, from overview to meeting.
- The decision is always the biggest thing on the screen.

## Trade-offs

- It is the least dense: 30 products need scrolling.
- The guided steps can feel slow for a user who already knows the tool.
- Several elements depend on Should items (FR-29, FR-30).

## Elements you could take

- The «Denne uken» summary tiles.
- The three-step path to the meeting.
- The card with the large order number.
- The product screen organised as three questions.
- The plain-language tone.
- The unusual-weeks switch placed next to the warnings.
