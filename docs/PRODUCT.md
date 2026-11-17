# Product

<!-- impeccable:product-schema 1 -->

Sources:
- The final PRD and its addendum in `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/`. The PRD was approved on 2026-11-03 and last updated on 2026-11-17, and every change is listed in PRD §12. The PRD wins on any conflict.
- The final UX spines `DESIGN.md` (how Prognose looks) and `EXPERIENCE.md` (how it works) in `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/`, set to final on 2026-11-16 and last updated on 2026-11-17. `docs/DESIGN.md` is a symbolic link to that DESIGN.md, so Impeccable reads the approved file and no copy exists.

This file records product facts only and does not repeat the spines. It lives in `docs/` because PRD DR-2 allows only the README, a license and configuration files as loose files in the root, and Impeccable finds PRODUCT.md and DESIGN.md there. The archived design of 2026-11-06 in `_bmad-output/planning-artifacts/archive/` is not a source.

## Platform

web

## Stack

Decided in the architecture spine of 2026-11-17 (`_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/ARCHITECTURE-SPINE.md`), which owns the details and the URLs:
- one Django 5.2 LTS web application with server-rendered templates, run with uv and Python 3.13;
- PostgreSQL 18 in both run modes: locally in Docker Compose, and on Neon's free plan in the version published on Vercel, from the same code (NFR-9, DR-10);
- the forecast chart as inline SVG rendered on the server, like the approved mockup, with no chart library.

The UX assumes plain semantic HTML and CSS with no UI library. Every function works through links and forms, and scripts only enhance the page (EXPERIENCE.md, Foundation). The local app serves every asset itself, with no web fonts and no CDN, so it works offline after installation (NFR-1).

## Users

- **Primary:** the purchasing manager or inventory planner at a small business with about 10 to 50 products, who reviews forecasts and orders every week (PRD §2). The reference journey (UJ-1, EXPERIENCE.md Flow 1) is a purchasing manager at a small hardware store with about 30 products, who has 20 minutes at the office PC before the Monday purchasing meeting.
- **Jobs:**
  - decide how much to order of each product every week;
  - see at a glance which products need ordering soon;
  - have a basis for each decision that they can understand and explain;
  - know when the data behind a forecast is too thin or distorted to trust.
- **Second audience:** the IBE160 teacher and examiner. They install Prognose from the README or open the published address, log in as a test company and check each forecast against a reference example (PRD §1, SM-2, SM-9, EXPERIENCE.md Flow 2).
- **Comprehension check:** two people outside the group see the product screen of a product with the confidence label «lav». Each must explain why it has that label without reading the reason aloud (SM-10, EXPERIENCE.md Flow 3).
- **Not for (v1):**
  - large companies that need ERP or MRP planning;
  - anyone who wants to place real orders with suppliers;
  - organizations that need several roles or approval steps.

## Product Purpose

Prognose is a web application that helps the purchasing manager of a small business decide how much to order of each product next week. It runs locally from the README and as a published version on Vercel (DR-10).

It forecasts weekly demand from the company's own sales history with established, hand-checkable methods (moving average and exponential smoothing). It shows normal, optimistic and pessimistic scenarios. It turns the normal forecast into a suggested order quantity: forecast plus safety margin minus stock on hand.

Success means that for each product the user sees one number to order next week, how it was calculated and whether it can be trusted. The user leaves the session with an order quantity decided for every product (UJ-1).

## Positioning

Transparency with built-in checks. Every number comes from deterministic rules that the user can see and check by hand, with settings the user can adjust.

Prognose also says when a forecast should not be trusted:
- it leaves out stockout weeks;
- it flags unusual weeks;
- it notices a level shift;
- it gives each product a confidence label (høy, middels, lav) with a plain-language reason.

The explanation is built from fixed Norwegian templates. An optional local language model may only rephrase it, and AI never produces the numbers. Prognose recommends; the purchasing manager decides.

## Operating Context

- **Weekly ritual** (UJ-1, EXPERIENCE.md Flow 1):
  1. Log in with the customer number and password.
  2. Scan the product overview. The products with order-soon status come first, by weeks of cover, then the products without a forecast, then the rest (R-12).
  3. Open the products that need ordering, and check the confidence label, the warnings, the calculation and the explanation.
  4. Switch unusual weeks between included and excluded on the product screen. The screen says that the change applies to all products, and the base forecast and the suggested order quantity update. Then switch back.
  5. Keep or adjust the suggested quantity.
  6. Finish with the combined order overview and take it to the meeting.

  Orders are placed outside Prognose. Steps 1 to 4 are Must. Adjusting quantities and the combined order overview are Should, so in a Must-only build the list for the meeting is made outside Prognose.
- **Environment:** a desktop browser on a laptop or office PC, macOS or Windows (NFR-6).
  - The local app and its database run offline after installation (NFR-1).
  - The published version on Vercel is a shared demo on free plans (DR-10). Anyone with the logins in the README can change a test company's settings, and an explicit reset with the load command restores the seed state. The optional language model is not available there. If publishing does not work in time, the cut line in PRD §8.1 applies and the local version counts.
  - Both versions use synthetic data only, with two test companies whose logins are in the README (FR-3).
- **Examiner's scene:**
  - a fresh clone and the README setup (target at most 15 minutes, SM-2), or the published address (SM-9);
  - logging in as a test company;
  - following «Prøv selv» in the README;
  - comparing the values on screen with the reference spreadsheet (DR-1, DR-3).

  For UJ-1 step 4, «Prøv selv» uses the rule test product built from E8. Excluding its unusual weeks changes the base forecast, and the confirmation shows «Grunnprognose: 41,0 → 21,3» (FR-21, DR-1, EXPERIENCE.md Flow 1).

## Capabilities and Constraints

- **Surfaces** (EXPERIENCE.md, Information Architecture):
  - Innlogging: the app root opens it, with a short introduction. There is no separate public page, and every other page requires login (FR-1).
  - Produktoversikt.
  - Produktside.
  - Innstillinger.
  - Samlet bestillingsoversikt (Should).
  - A not-found page (NFR-10).
- **Must** (PRD §8.1):
  - login and company isolation (FR-1, FR-2);
  - synthetic data stored between sessions (FR-3, FR-4);
  - forecasts with the three-week horizon, and the insufficient-data case (FR-5 to FR-8);
  - scenarios, the suggested order quantity and the order calculation line (FR-10 to FR-12);
  - stockout weeks, unusual weeks, the level shift (in the calculation and the label's reason), the old-data warning and the confidence label (FR-15 to FR-19);
  - company-wide settings, changed from the product screen with an immediate before-and-after confirmation (FR-20 to FR-22);
  - the product overview, the product screen and the visible forecast calculation (FR-24, FR-25, FR-35);
  - the template explanation under «Forklaring», below the numbers, with only the numbers FR-27 allows (FR-26, FR-27).
- **Should,** in the order of PRD §8.2, started only after the Must scope passes SM-1 and SM-3:
  1. seasonal adjustment (FR-9);
  2. the seasonal-pattern warning and the level-shift warning text (FR-36, FR-17b);
  3. order quantity per scenario and the overstock note (FR-13, FR-14);
  4. adjusting order quantities (FR-29);
  5. the combined order overview (FR-30);
  6. the optional local language model, which is off by default (FR-28).
- **Could:**
  - settings per product (FR-23);
  - saving adjustments and approval (FR-31); without it, adjustments last for the session only;
  - CSV export (FR-32);
  - the note that stock will not last through weeks 2 and 3 (FR-33);
  - forecast accuracy as MAE (FR-34).
- **Binding terms:** the UI is Norwegian bokmål and uses the PRD glossary labels with no synonyms (PRD §3). Examples:
  - screens and areas: Produktoversikt, Produktside, Innstillinger, Samlet bestillingsoversikt, Forklaring;
  - forecast and ordering: Grunnprognose, Ukeprognose, Prognoseutregning, Foreslått bestillingsmengde, Utregning av bestillingsmengde, Lagerbeholdning, Uker dekning, Sikkerhetsmargin, Bestill snart;
  - trust signals: Tillitsmerke (høy, middels, lav), Varsel, Merknad, Utsolgt uke, Uvanlig uke, Nytt nivå;
  - markings: «Foreslått», «Justert av deg» and «Uten prognose».

  Fixed strings such as «Endringen gjelder alle produkter i bedriften.» and «Feil kundenummer eller passord.» appear exactly as the PRD gives them. The Message Catalogue in EXPERIENCE.md is the copy source for every warning, note, confirmation and error.
- **Numbers** (R-9, NFR-5):
  - a decimal comma, rounded half away from zero;
  - one decimal for forecasts, scenarios, weeks of cover and the margin amount;
  - two decimals for the unrounded result on the order calculation line;
  - four decimals for seasonal indices, and one for seasonally adjusted values;
  - whole numbers for order quantities and percentages.

  The order calculation line, the exponential-smoothing line and the seasonal values carry «Tallene er avrundet for visning.» (FR-12, FR-35). The UX writes «10 %» with a space and the minus sign «−», with no thousands grouping (EXPERIENCE.md, Calculation Display Rules).
- **Weeks:** a week is identified by its year and week number (PRD §3). The screen shows the year at New Year and in lists that reach before the recent period, and the explanation may name these years (FR-27, EXPERIENCE.md Calculation Display Rules).
- **Layout** (FR-25, NFR-6):
  - At 1366 × 768, the product screen shows the suggested order quantity, the confidence label and the active warnings without scrolling.
  - From 1024 px wide, the page never scrolls sideways.
  - Down to 800 px wide, no text overlaps or is cut off, and wide tables may scroll inside their own frame.
  - A mobile layout is not required.
- **Chart:**
  - It shows the whole sales history (up to 104 weeks) and the three forecast weeks with the scenarios. This is within FR-25, and the user chose it on 2026-11-16 (EXPERIENCE.md).
  - Stockout weeks, unusual weeks and level-shift weeks each have their own marker that differs by more than color, explained in a legend (FR-15 to FR-17, NFR-7).
  - It has a text alternative with a summary and a value table (NFR-11).
- **Data:** read-only in the app; only the settings and adjusted order quantities change (PRD §7). An explicit reset of the seed data resets the settings and adjustments (DR-4).

## Brand Commitments

- **Name:** Prognose. The wordmark is the name set in text, with no logo mark. The visual identity is fixed in DESIGN.md and is not repeated here: the colors, typography, shapes and components.
- **Voice:**
  - Plain, honest Norwegian that states limits openly, for example «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.» (FR-12).
  - Prognose speaks in the third person («Prognose foreslår …») and calls the user «du». It never says «vi», «systemet» or «KI-en».
  - Sentences are short and complete and end with a full stop, with no exclamation marks or emojis (EXPERIENCE.md, Voice and Tone).
  - A warning is never weakened to make the result look better (SM-C3).
- **User principle:** Prognose recommends; the purchasing manager always decides.

## Evidence on Hand

- **Reference examples:** the hand-calculated examples E1 to E30 (PRD §5.7). Once the generator script exists, there is also the synthetic seed data for two test companies (FR-3). Both may be shown as demonstration material when they are labeled as synthetic.
- **Design references:** the final spines and the approved mockup `mockups/konsept-d-kombinert.html` in the UX folder above. The mockup shows example products and figures, and the spines win on any conflict. Concepts A, B and C (in that folder's `.working/`) and the archived design of 2026-11-06 are documentation only.
- **True context that may be stated:** a course project for IBE160 at Høgskolen i Molde, autumn 2026.
- **Absent, and never to be invented:**
  - real customers or companies;
  - testimonials, user logos and press;
  - prices and accuracy benchmarks;
  - integrations;
  - hosting claims beyond the free published demo in DR-10: no uptime guarantee, custom domain or paid hosting (PRD §7).

## Product Principles

1. **Show the working.** Every number on screen can be traced to a visible calculation and checked by hand.
2. **Say when not to trust.** Warnings, notes and the confidence label are first-class information, never decoration and never softened.
3. **Recommend, never decide.** The suggested order quantity is advice, and the user's adjustment is always shown as theirs.
4. **One language, fixed terms.** Norwegian plain language with the glossary labels, using the same words on every screen and in every explanation.
5. **Small, local and free.** The local app runs offline on one machine, and the published version runs the same code on free plans. There are no paid services and no more parts than the app needs (NFR-1, NFR-9, DR-10).

## Accessibility & Inclusion

- Text contrast meets WCAG 2.2 level AA.
- Every function works with the keyboard alone, with a visible focus, and every form field has a visible label.
- Pages declare Norwegian as their language.
- The chart has a text alternative with a summary and a value table, and its markers differ by more than color (NFR-7, NFR-11).
- Down to 800 px wide, no text overlaps or is cut off, and every control can be reached with the keyboard (NFR-6).

EXPERIENCE.md (Accessibility Floor) has the behavioral details, and DESIGN.md (Colors) has the measured contrast.
