---
title: Product Brief — Prognose (G40-lyamouri)
status: final
created: 2026-09-18
updated: 2026-10-14
---

# Product Brief: Prognose (G40-lyamouri)

## 1. Project Description

Prognose is a website for small businesses that want to estimate future demand for their products. The project covers module 4.1, "Prognoser og Demand Management" (Forecasting and Demand Management), in IBE160 at Høgskolen i Molde.

Businesses log in with a customer number and password and get access to their own historical sales data. The website calculates forecasts with established statistical methods and shows three scenarios: optimistic, normal, and pessimistic.

AI is used to explain the forecasts and to support development through BMAD and Claude Code. AI must not make up forecast numbers.

## 2. The Problem

Small businesses can run out of products or hold too much inventory because sales are hard to predict. Manual calculations can make it hard to understand sales trends and to handle unusual sales figures.

The goal is to make forecasting simpler, easier to understand, and easier to keep track of.

## 3. The Solution

The website offers:

- Login, with access only to the business's own data.
- A database of historical sales data.
- Charts of sales history and forecasts.
- Forecast calculation with moving average and exponential smoothing.
- Three scenarios: optimistic, normal, and pessimistic.
- Adjustable forecasting method, safety margin, and handling of unusual sales figures.
- AI-based explanations of the forecasts.

## 4. Calculation Rules

Proposed rules, to be validated during BMAD planning:

- **Moving average:** average of the last 3 periods, with an adjustable window from 2 to 12 periods.
- **Exponential smoothing:** adjustable factor from 0.1 to 0.9, default 0.3.
- **Forecast horizon:** 3 future periods.
- **Normal scenario:** the calculated base forecast.
- **Optimistic demand:** base forecast plus an adjustable percentage, default 10%.
- **Pessimistic demand:** base forecast minus the same percentage, never below zero.
- **Safety margin:** a separate adjustable percentage, added to the selected forecast when calculating a suggested planning quantity.
- **Unusual sales figures:** values above twice the median of the three preceding periods are flagged. The user can choose whether to include or exclude them.

The calculations must be deterministic and possible to check by hand. AI must not generate the numerical forecasts.

## 5. What Makes This Different

Prognose is meant to be simple and clear. The user can see which calculation method is used, adjust the assumptions, and understand why the forecast changes.

The solution prioritizes transparency and ease of use over advanced enterprise features.

## 6. Target Group

The main user is a purchasing manager or inventory planner at a small business with about 10–50 products. The user reviews the forecasts every week.

The project uses synthetic business accounts and sales data.

## 7. Success Criteria

- Businesses can log in and see only their own data.
- Sales data is stored between sessions.
- Forecasts can be calculated for individual products and periods.
- The three scenarios are shown clearly.
- Adjusting the settings produces visible changes in the results.
- Forecast calculations match independently checked examples.
- AI explanations are clearly separated from calculated results.
- The website can run locally with documented instructions and synthetic data.
- The use of AI during development is documented.

## 8. Scope

**In scope:** login, database, synthetic historical sales data, two statistical forecasting methods, three scenarios, adjustable settings, charts, simple historical trend and seasonal patterns in the test data, and AI explanations with an alternative that needs no paid API.

**Out of scope:** bill of materials (BOM) structures, production planning, other MRP II modules, supplier integrations, actual orders, real-time market and campaign data, incoming customer orders, advanced machine learning, and enterprise-level security solutions.

## 9. Vision

In the longer term, Prognose aims to make forecasting more accessible and easier to understand for small businesses. Any future integration with other planning functions is outside this project version.

## 10. Technical Approach and Testing

Choose a simple, documented technical solution with a local database. The forecast calculations must be testable on their own.

Use synthetic datasets with known results. The teacher must be able to run the website with a test account and a README, without paid services or private API keys.

## 11. Open Questions

- Confirm the final submission deadline.
- Choose a simple technology stack during the BMAD architecture work.
- Validate the calculation rules before implementation.
- Clarify how the AI explanations and the alternative without an API will work.
