---
title: Product Brief — Prognose (G40-lyamouri)
status: final
created: 2026-09-18
updated: 2026-09-18
---

# Product Brief: Prognose

## Executive Summary

This is a web-based demand forecasting tool built for module 4.1 ("Prognoser og Demand Management") of the IBE160 course assignment "AI-støttet MRP II (incl. BOM) – Detailed Modules" at Høgskolen i Molde. Businesses log in with a customer number and password to access their own historical sales and demand data, stored in a database. The system then generates AI-based demand forecasts per period and product — expressed as optimistic, normal, and pessimistic scenarios — to support purchasing and inventory planning decisions.

The project is a solo effort (despite the repository's "group project" framing) with one explicit goal set by the course: demonstrate concrete, documented use of AI throughout the development process, not to ship a commercially viable product. Scope is deliberately bounded to the forecasting/demand-management module only — the wider MRP II assignment family (Bill of Materials (BOM), production scheduling, supplier integration) is out of scope for this brief.

Because the underlying assignment flags this module as security-relevant ("business-critical and potentially competitively sensitive data"), authentication and data storage are treated as first-class concerns even though the data itself will be synthetic.

## The Problem

Businesses that plan purchasing and inventory need a reliable read on future demand per product and period. Getting it wrong is expensive in both directions: understocking causes lost sales and expediting costs — overstocking ties up capital and warehouse space. Many smaller businesses still do this by gut feel or spreadsheet extrapolation — an approach that struggles to combine multiple weak signals (seasonality, trend, campaigns, market conditions, and incoming customer orders) into one forecast, and offers no structured way to express uncertainty (best case / worst case) or handle anomalies in the historical data (e.g., a one-off bulk order skewing the trend).

The assignment names this precisely: businesses need forecasts derived from their own historical sales and demand data, with explicit handling of forecast method, safety margin, and outliers — decisions that are usually implicit and undocumented in ad-hoc spreadsheet forecasting.

## The Solution

A web portal where a business, identified by customer number and password, logs into an account holding its own historical sales and demand data (synthetic data for this project, structured to resemble a real dataset). The system uses AI to turn that historical data — combined with season/trend signals, campaign/market data, and customer orders — into demand forecasts per product and period, presented as three scenarios: optimistic, normal, and pessimistic.

The three decision points the assignment calls out are treated as visible, adjustable controls rather than hidden model internals:
- **Forecast method** — how the forecasting approach applied to the data is chosen.
- **Safety margin** — how much buffer is layered onto the raw forecast.
- **Outlier handling** — how anomalous historical data points are detected and treated before they influence the forecast.

## Who This Serves

**Primary user:** a business's purchasing/inventory planner who logs in to review demand forecasts for their products and adjust forecast parameters (method, safety margin, outlier handling) to fit their judgment. For this project, this user is represented through a synthetic account and dataset rather than a real business relationship.

## Success Criteria

- A business can log in with customer number and password and see only its own data.
- Historical sales and demand data and account information persist correctly in a database across sessions.
- The system produces a per-product, per-period demand forecast with optimistic, normal, and pessimistic scenarios from the historical dataset.
- Forecast method, safety margin, and outlier handling are exposed as adjustable inputs, and changing them visibly changes the output.
- The development process itself demonstrates and documents concrete AI usage (per the course's own stated grading goal), independent of whether the forecasting output is production-grade.

## Scope

**In scope (module 4.1 only):**
- Business login via customer number and password.
- Database storage of business/account info and historical sales and demand data.
- A synthetic, realistic historical sales and demand dataset (no real business data available).
- AI-generated demand forecasts per product and period.
- Three-scenario output: optimistic, normal, and pessimistic.
- Adjustable decision points: forecast method, safety margin, and outlier handling.

**Out of scope:**
- BOM and other MRP II modules (production scheduling, inventory execution, etc.) — these belong to the wider assignment family but not this module.
- Real e-commerce / purchase transactions — the source assignment notes these are "not directly in the base modules."
- Supplier portal integrations.
- Real production business data.
- Enterprise-grade multi-tenant security hardening beyond what a course project reasonably demonstrates (basic authentication and data isolation only).

## Open Questions

- Forecast method itself (e.g., moving average, exponential smoothing, regression, ML/LLM-assisted) is an open technical decision — the assignment lists "prognosemetoder" as a decision point rather than prescribing one; to be resolved in architecture/design, not this brief.
- Tech stack (frontend, backend, database, AI/LLM API) — no constraint from the course; open for the next phase.
- Timeline/deadline for the course deliverable — not yet specified.
