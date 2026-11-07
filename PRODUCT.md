# Product

<!-- impeccable:product-schema 1 -->

Source: the final PRD and addendum in `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/` (approved 2026-11-03). The PRD wins on any conflict. Items marked *[inferred]* were derived from the PRD without a separate interview, because the user asked on 2026-11-06 for the design work to go ahead without preference questions.

## Platform

web

## Stack

Undecided. The BMAD architecture step decides it (PRD NFR-9). The research recommends Django + SQLite with server-rendered templates and Chart.js, with Flask + SQLite as the runner-up (addendum §2). Design work must fit server-rendered HTML and CSS with little JavaScript, and every asset, including fonts and the chart library, is served locally with no CDN (NFR-1).

## Users

- **Primary:** the purchasing manager or inventory planner at a small business with about 10 to 50 products, who reviews forecasts and orders every week (PRD §2). The reference journey (UJ-1) is a purchasing manager at a small hardware store with about 30 products, who has 20 minutes at the office PC before the Monday purchasing meeting.
- **Jobs:** decide how much to order of each product every week; see at a glance which products need ordering soon; have a basis for each decision that they can understand and explain; know when the data behind a forecast is too thin or distorted to trust.
- **Second audience:** the IBE160 teacher and examiner, who install Prognose from the README, log in as a test company and check each forecast against a reference example (PRD §1, SM-2).
- **Not for (v1):** large companies that need ERP or MRP planning, anyone who wants to place real orders with suppliers, and organizations that need several roles or approval steps.

## Product Purpose

Prognose is a local web application that helps the purchasing manager of a small business decide how much to order of each product next week. It forecasts weekly demand from the company's own sales history with established, hand-checkable methods (moving average and exponential smoothing), shows normal, optimistic and pessimistic scenarios, and turns the normal forecast into a suggested order quantity: forecast plus safety margin minus stock on hand. Success means that for each product the user sees one number to order next week, how it was calculated and whether it can be trusted, and leaves the session with an order quantity decided for every product (UJ-1).

## Positioning

Transparency with built-in checks. Every number comes from deterministic rules that the user can see and check by hand, with settings the user can adjust. Prognose also says when a forecast should not be trusted: it leaves out stockout weeks, flags unusual weeks, notices a level shift, and gives each product a confidence label (høy, middels, lav) with a plain-language reason. The explanation is built from fixed Norwegian templates. An optional local language model may only rephrase it, and AI never produces the numbers. Prognose recommends; the purchasing manager decides.

## Operating Context

- **Weekly ritual:** log in with customer number and password; scan the product overview (products with order-soon status first, sorted by weeks of cover); open the products that need ordering; check the warnings and the explanation; change a setting and watch the result change; keep or adjust the suggested quantity; finish with the combined order overview and take it to the meeting. Orders are placed outside Prognose.
- **Environment:** a desktop browser on a laptop or office PC, macOS or Windows. Prognose runs locally and offline after installation, with synthetic data only and two test companies whose logins are documented in the README.
- **Examiner's scene:** a fresh clone, the README setup (target at most 15 minutes), logging in as a test company, and comparing values on screen with the reference spreadsheet.

## Capabilities and Constraints

- **Screens in the PRD:** login page, product overview, product screen and combined order overview (Should). Every page except the login page requires login (FR-1).
- **Must:** login and company isolation; forecasts with the three-week horizon, scenarios, the suggested order quantity and the order calculation line; stockout weeks, unusual weeks, level shift, the old-data warning and the confidence label; company-wide settings changed from the product screen with an immediate before-and-after confirmation; the visible forecast calculation; the template explanation under «Forklaring», below the numbers.
- **Should and Could:** seasonal adjustment, order quantity per scenario, the overstock note, the local language model, adjusting order quantities and the combined order overview; settings per product, saving adjustments and approval, CSV export and MAE.
- **Binding terms:** the UI is Norwegian bokmål and uses the PRD glossary labels with no synonyms, for example Produktoversikt, Produktside, Grunnprognose, Ukeprognose, Foreslått bestillingsmengde, Lagerbeholdning, Uker dekning, Bestill snart, Tillitsmerke (høy, middels, lav), Varsel, Merknad, Forklaring, Utsolgt uke, Uvanlig uke, Nytt nivå, Sikkerhetsmargin, Innstillinger, «Foreslått» and «Justert av deg». Fixed strings such as «Endringen gjelder alle produkter i bedriften.» and «Feil kundenummer eller passord.» appear exactly as the PRD gives them.
- **Numbers:** decimal comma; forecasts with one decimal, order quantities as whole numbers, percentages as whole numbers with «%» (R-9, NFR-5).
- **Layout:** at 1366 × 768 the product screen shows the suggested order quantity, the confidence label and the active warnings without scrolling (FR-25); no horizontal page scroll from 1024 px wide; no mobile layout required (NFR-6).
- **Chart:** stockout weeks, unusual weeks and level-shift weeks each have their own marker that differs by more than color, explained in a legend (NFR-7), and the chart has a text alternative with a summary and a value table (NFR-11).
- **Data:** read-only in the app; only the settings and adjusted order quantities change.
- **Undecided** *[inferred]*: the PRD defines no public landing page. Whether the entry surface is the login page itself with an introduction, or a separate public page (which would change FR-1), is decided with the user in the UX phase.

## Brand Commitments

- **Name:** Prognose. No logo, wordmark, colors or typefaces exist yet.
- **Voice:** plain, honest Norwegian that states limits openly, for example «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.» A warning is never weakened to make the result look better (SM-C3).
- **User principle:** Prognose recommends; the purchasing manager always decides.

## Evidence on Hand

- Synthetic seed data for two test companies and the hand-calculated reference examples E1 to E30 (PRD §5.7). They may be shown as demonstration material when they are labeled as synthetic.
- True context that may be stated: a course project for IBE160 at Høgskolen i Molde, autumn 2026.
- Absent, and never to be invented: real customers or companies, testimonials, user logos, press, prices, accuracy benchmarks, hosting or deployment claims, and integrations.

## Product Principles

1. **Show the working.** Every number on screen can be traced to a visible calculation and checked by hand.
2. **Say when not to trust.** Warnings, notes and the confidence label are first-class information, never decoration and never softened.
3. **Recommend, never decide.** The suggested order quantity is advice, and the user's adjustment is always shown as theirs.
4. **One language, fixed terms.** Norwegian plain language with the glossary labels, using the same words on every screen and in every explanation.
5. **Small and local.** Runs offline on one machine with no paid services and no more parts than the app needs.

## Accessibility & Inclusion

Text contrast meets WCAG 2.2 level AA. Every function works with the keyboard alone, with a visible focus, and every form field has a visible label. Pages declare Norwegian as their language. The chart has a text alternative with a summary and a value table, and its markers differ by more than color (NFR-7, NFR-11).
