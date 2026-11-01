# Digest: safety stock and order policy (round 2) (round 2, assistant 1)

Status: weak result. Only one source yielded verifiable text, and only a few lines of it. The PDFs (MIT OCW, edX, arXiv) came back as compressed binary through WebFetch. I extracted raw text from one of them with a crude local script. Two fetches failed, one with a 404 and one with a TLS error. The tool budget was overrun by one call (16 versus 15) in a last attempt to read the arXiv PDF. That attempt produced nothing usable.

## Findings
| # | claim | source URL | publisher | pub_date | accessed | confidence | class |
|---|-------|-----------|-----------|----------|----------|------------|-------|
| 1 | In Caplice's "Safety Stock Logic" slide, cycle service level (labelled P1) maps to the safety factor k, with P[stockout] = 1 - CSL and safety stock SS = k x sigma (sigma symbol lost in extraction; Eqn 7.20). The slide is an equation diagram, not a prose definition. | https://ocw.mit.edu/courses/esd-260j-logistics-systems-fall-2006/bc18dd1b2543535a61f826d00a8c6e42_lect12.pdf | MIT OCW (Chris Caplice, MIT CTL), ESD.260 Lecture 12 "Inventory Management, More Probabilistic Demand" | Oct 2006 | 2026-11-01 | medium (symbols partly lost in extraction) | lecture slides |
| 2 | The same slide ties item fill rate (IFR, labelled P2) to the loss function G(k) = (1 - IFR) x Q / sigma (Eqn 7.23). So cycle service level and fill rate are different service objectives linked to k in different ways, and the slides state "Any inputted objective implies all others". | same as #1 | same as #1 | Oct 2006 | 2026-11-01 | medium | lecture slides |
| 3 | The Caplice slide above is a (s,Q) continuous-review example. Its extracted text contained nothing on (R,S), sqrt(R+L), forecast-error sigma, percentage safety stock, inventory position, rounding or non-negativity. | same as #1 | same as #1 | Oct 2006 | 2026-11-01 | medium | observation |
| 4 | A paper titled "Accuracy Is Not Service: A Decision-Aware Benchmark for Intermittent-Demand Forecasting" (Chin, Cheng, Gunawan; arXiv:2609.13840v1, metadata date 2026-09-15) exists. It is relevant to the topic, but I could not read its body, so no claim from it is made here. | https://arxiv.org/pdf/2609.13840 | arXiv (preprint, not peer reviewed) | 2026-09 (metadata) | 2026-11-01 | low | pointer only |

## Worked example(s) / formulas
None verified. Do not use search-engine summaries as evidence for the standard formulas (see Leads).

## Leads worth chasing (UNVERIFIED: surfaced only by the search tool's summaries, never read by me)
- MIT 15.762J inventory notes (Graves-style, "Inventory Buildup Diagrams"): https://dspace.mit.edu/bitstream/handle/1721.1/71720/15-762j-spring-2005/contents/lecture-notes/inventory_notes.pdf. WebFetch returned 404 for it. The search summary says it treats base-stock policies as a special case of periodic review. It is the best candidate for Q3. Retry it via ocw.mit.edu or the 15.762J Spring 2011 pages, or download it and run a real PDF extractor (poppler is not installed here).
- Caplice ESD.260 Lecture 11 (periodic review (R,S): "Order S - IP every R time periods", per the search summary only): https://ocw.mit.edu/courses/esd-260j-logistics-systems-fall-2006/8b53c45fd26ffff706d815131e8d177e_lect11.pdf. It is compressed binary like lect12, so use a local PDF-to-text tool.
- MITx CTL.SC1x Key Concept Week 7 Lesson 1 (periodic review (R,S), safety factor k): https://courses.edx.org/asset-v1:MITx+CTL.SC1x_1+2T2015+type@asset+block/KeyConcept_Week7Lesson1.pdf. It is compressed binary.
- Prak, Teunter, Syntetos (2017, European Journal of Operational Research), via the search summary: the standard sigma x sqrt(L) scaling understates safety stock because forecast errors across lead-time periods are positively correlated. The relevant page is https://orca.cardiff.ac.uk/id/eprint/92130/. I did not read the abstract. If confirmed, this bears on Q1 and is a real academic caveat to sigma x sqrt(R+L).
- Arias-Vargas et al. 2017, "Impact on safety stock due to the use of the standard deviation of forecast errors" (Costa Rica). The repository fetch failed with a TLS error: https://repositoriotec.tec.ac.cr/items/9cac67f1-8010-4e68-b646-50f10071c681. It is relevant to Q1 (forecast error versus demand sigma).
- Practitioner pages (vendor or blog, so low quality) on forecast-error sigma: Demand Planning "Error Measure for Safety Stocks: MAPE vs RMSE" (https://demandplanning.net/?p=4662, truncated on fetch) and Lokad (https://www.lokad.com/calculate-safety-stocks-with-sales-forecasting/).
- A smenet.org or SME article and a frepple business-rules page were surfaced for fixed-percentage or days-of-cover rules (Q2). The percentage rule is described there as simple but blind to per-item variability. Not read, so not usable as a citation. Candidates: https://frepple.com/docs/current/examples/distribution/business-rules.php and https://store.smenet.org/20slp36/435.
- Weeks of supply (Q5): only vendor glossaries surfaced (racklify, Cogsy, Hyperbots, Inventory Planner). None was read. The ASCM dictionary entry was not found by search; try ascm.org directly (it may be paywalled or JS-rendered). Textbook candidates are still Silver-Pyke-Thomas, Nahmias and Chopra-Meindl.
- Open-source dpaste-free alternative: install poppler (`brew install poppler`) so WebFetch-saved PDFs under ~/.claude/projects/.../tool-results can be converted with pdftotext. That would unlock all the MIT lecture PDFs.

## Not found / could not verify
- Q1: no read source defines the cycle service level versus fill rate in prose. Only the equation-level link in rows 1-2. Nothing read on whether sigma should be forecast-error sigma.
- Q2: no credible source read that describes percentage-of-forecast safety stock, its limits, or any recommendation for small businesses. The only mention is an unread search summary.
- Q3: no read source states inventory position = on hand + on order - backorders. None states that with zero lead time and weekly review the order-up-to level reduces to review-period demand plus safety stock.
- Q4: nothing read on rounding up to pack size or on never ordering a negative quantity in (R,S) descriptions.
- Q5: no ASCM, textbook or university source for weeks of supply or weeks of cover as a metric or reorder trigger.
- Failures: the dspace inventory_notes.pdf returned 404. The edX PDF, the lect12 PDF (partly recovered with a local script) and the arXiv PDF returned compressed binary. The demandplanning.net article was truncated. The repositoriosiidca.csuca.org fetch had a TLS error. The ESD.260 lect11 and 15.762J pages were never fetched.
- Budget: sources read to any useful degree: 1 (lect12, partially). Tool calls: 16 versus the 15 allowed.
