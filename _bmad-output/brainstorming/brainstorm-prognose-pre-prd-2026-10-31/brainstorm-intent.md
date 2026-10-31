---
title: Brainstorm Intent — Prognose (G40-lyamouri)
source: .memlog.md in this folder (session 2026-10-31)
input_for: bmad-prd
---

# Brainstorm Intent: Prognose

Decisions from the pre-PRD brainstorm. Builds on `brief.md` (2026-10-14) and the teacher feedback of 2026-10-06. Items marked *proposal* were suggested by the coach and not explicitly confirmed.

## 1. Core job

The purchasing manager wants to know **how much to order next week for each product**, based on past sales and expected demand, avoiding both empty shelves and overstock, with a clear basis for the decision. Priority order: a working site, good forecasts, understandable calculations, honest warnings when data is uncertain, simplicity, and finishing by the deadline.

## 2. Decisions

**Flow (weekly)**
1. After login: product overview with stock and which items need ordering soon.
2. Product screen: chart of past and expected sales, stock, safety margin, suggested order quantity, warnings and outliers.
3. Planner may adjust the suggested quantity manually.
4. Combined overview of suggested quantities (a list, not an ordering system).

**Period and data**
- Period is **week**; forecast horizon is the **next 3 weeks**.
- Synthetic data: **104 weeks** per product as the rule, plus a few test products with short history. Seasonal patterns stay in the data and chart.
- **Current stock** is a column in the synthetic data. Each week also carries a **stockout flag**.

**Order quantity**
- Covers **next week only**: `max(0, round up(forecast week 1 + safety margin − stock))`.
- Based on the **normal scenario** by default, safety margin added on top. Optimistic and pessimistic are shown as alternatives for comparison.
- Weeks 2 and 3 are for further planning and are not summed into the order.
- Shows 0 when stock covers demand. No pack sizes in v1.
- The calculation is shown on screen as a visible one-line formula.

**Data-quality rules**
- Stockout weeks are **excluded** from the calculation and the user is warned.
- Moving average uses the **last 3 valid weeks**, skipping stockout weeks. The outlier median also uses the 3 preceding valid weeks. Without this, the first normal week after a stockout is flagged as an outlier.
- Outlier rule from the brief (above 2× median of the preceding periods) stays. **3 or more consecutive high weeks** count as a possible new normal level, not as outliers: the forecast follows the increase.
- Forecast is shown only with **at least 3 valid weeks**. If the chosen moving-average window is larger than the valid weeks, show an insufficient-data message and do not compute.
- Warning if the latest valid sales data is **older than 8 weeks**.
- **Confidence badge:** low = under 12 valid weeks; medium = 12–103 valid weeks or active notes (outlier, stockout, level change); high = 104+ valid weeks and no active warnings. Every non-high badge shows a plain-language reason.

## 3. MoSCoW

**Must**
- Login with customer number and password; each business sees only its own data.
- Database with synthetic data (104 weeks, stock, stockout flag, short-history test products).
- Moving average and exponential smoothing in a separate, testable module; 3-week forecast; three scenarios; adjustable method, window, factor, scenario percentage, safety margin and outlier handling.
- Order suggestion with visible calculation.
- Product screen with chart; product overview with stock and "order soon".
- Outlier, stockout and new-level rules; confidence badge and warnings (all thresholds above).
- Template-based explanation that needs no paid API, visibly separated from calculated results.
- README with test account; tests against hand-calculated answers.
- Process and repo: documented decisions and AI use, `.env.example`, fixed location for seed data and generator script.

**Should**
- Simple seasonal adjustment that affects the forecast (cut from Must for feasibility).
- Language-model explanation when a key is available.
- Manual adjustment of the suggested order quantity.
- Combined overview of suggested quantities.
- Message that demand level has changed (the rule itself is Must).
- Scenario comparison for the order quantity; overstock note.

**Could**
- CSV export; saving manual adjustments between sessions; warning that stock will not last weeks 2–3; accuracy metric (MAPE).

**Won't (this version)**
- Pack sizes, lead time, placing actual orders, campaigns, incoming customer orders.

**Rationale for seasonality as Should.** The brief and teacher suggested including it, but it is the most demanding rule. The Must forecast is non-seasonal and the product says so. Fallback: show seasonality in the chart with a note.

## 4. Open items for the PRD or research

- Seasonal method: index per week, estimation from two years, interaction with outlier and stockout exclusion.
- "Order soon": proposal is stock coverage = stock ÷ forecast per week; not confirmed.
- Stock as-of date to trigger an "uncertain stock" warning (*proposal*).
- Outlier check in the first weeks (*proposal*: starts once 3 valid preceding weeks exist) and median 0 without a stockout flag.
- Whether manual adjustments are saved between sessions.
- Content of the template explanation, and how the optional language-model explanation falls back.
- Technology stack; final submission deadline.
