# Reconciliation: research C and D against the PRD

**Inputs:** research C (`_bmad-output/planning-artifacts/research/technical-technology-stack-selection-2026-11-01/research.md`) and research D (`_bmad-output/planning-artifacts/research/technical-explanation-without-paid-api-2026-11-01/research.md`), checked on 2026-11-02 against `prd.md` and `addendum.md` in this folder.

**Status key:** R reflected; D decided otherwise on purpose; O listed as an open question; P partly reflected; M missing. G-numbers refer to §3.

## 1. Recommendations from C and D

### Report C: technology stack

| Item | Status | Location |
|---|---|---|
| C-R1: Django + SQLite (83 vs Flask 80, inside scoring uncertainty, basis medium-low) | D (deferred) | PRD §0 and NFR-9 leave the stack to the architecture step; addendum §1 and §2 carry the pick as "not decided". Correct. |
| C-R1: forecasting logic in a framework-free package; reversibility hedge | R | NFR-2, §5 intro; addendum §2 |
| Gates: no paid service or key; local embedded database; charts | R | NFR-1, FR-4, NFR-9, FR-25; the "mainstream and documented" gate is left to architecture (addendum §2) |
| Gate: password hashing with sessions | P | FR-1 (salted hashes, logout ends the session), NFR-3; hasher strength not stated (G5) |
| C-R2: every query filtered by company in one data-access layer; two-account test | R / P | FR-2 (server check on every request, "not found", A-versus-B test), NFR-3, SM-4; the layer is in addendum §2. Test scope and gating: G3 |
| OWASP: deny by default, server-side checks, random IDs are no substitute | R | FR-1 (redirect to login), FR-2; addendum §2 |
| C-R3: the group writes and tests the README setup sequence | R | DR-1, DR-4, SM-2; addendum §2 |
| C-R4: Chart.js from a pinned CDN link or a vendored file; vendor for offline use | R / P | Addendum §2: only the vendored file meets NFR-1; nothing in the PRD tests it (G2) |
| C-R5: avoid Flask-Login and FastAPI as defaults; Next.js scored lowest | R | Addendum §2, §4 |
| C-R6: record "AI-assistant fit not evidenced" as a known limitation | P | Addendum §5 points to DR-5; DR-5 does not name it (G8) |
| Caveats: single-publisher docs; 2 claims verified, 5 not; licences unchecked | R | Addendum §5 |
| Open: Django PBKDF2 iteration count; official per-company pattern | O | Addendum §5 only; acceptable while the stack is open |
| Open: Recharts with React 19; better-sqlite3 build needs | R | Addendum §4 (Next.js) |
| Open: developer reports after 6 to 12 months with Django | M | Not carried; low value |
| Re-check versions by 2026-12-01, ecosystem signals by 2027-05-01 | R | Addendum §5 |

### Report D: explanation without a paid API

| Item | Status | Location |
|---|---|---|
| Gates: no paid API or key; numbers only from deterministic rules; offline | R / P | NFR-1, AG-1, §5 intro; offline running is never tested (G2) |
| D-R1: template explanation is the Must feature; snapshot tests | R | FR-26, AG-2, §8.1 |
| D-R1: states method, inputs, calculation line, warnings and confidence label | P | FR-26 names left-out weeks and level shift but not every warning (G7) |
| D-R2: rephrasing (the hybrid) is Should, local only, off by default, needs no key | R | FR-28, AG-3, AG-5 |
| D-R2: the app inserts all numbers; the model rephrases around named placeholders | R | FR-28; placeholders and the `explain(result) -> text` seam in addendum §3 |
| D-R2: check each label and value together, not the value alone | R / P | FR-28 says so; SM-6 checks only for a "changed number" (G6) |
| Fall back to the template when the model is missing, slow or fails validation | R / P | FR-28, AG-3; a stopped server and errors inside a 200 response appear only in addendum §3 (G6) |
| Structured output does not guarantee values; schema in prompt, temperature 0 | R | Addendum §3 |
| D-R3: do not depend on a hosted free tier; optional hosted setting via `.env.example` | R / D | AG-5 and §7 exclude hosted AI entirely; addendum §3 explains why the optional setting is dropped |
| Hosted terms: Gemini content use and human review, EEA paid-only terms (Norway by inference), age 18, unstable limits | R | Addendum §3, §4, §5 (inference marked) |
| D-R4: label AI-written text and keep it apart from calculated results | R | FR-27 («KI-omformulert forklaring»), AG-4; Article 50 context in addendum §3 |
| D-R5: name the model and its licence in the README ("Built with Llama") | P | §10 Q7 and addendum §3; DR-1 does not require it (G8) |
| Caveat: a template is not AI; the course may expect a visible language model | O, but misstated | §10 Q1 and FR-28 [OPEN] are right; the Vision contradicts the caveat (§2) |
| Caveat: heavy install (1.3 to 7.5 GB; the quickstart example model needs about 8 GB of memory) | P | Addendum §3 only (G4) |
| Open: is Ollama usable fully offline; how to detect a stopped server | P | Addendum §3; not in PRD §10 (G2) |
| Open: which small model is good and fast enough on a laptop | P | §10 Q7 asks only for the model and its licence; speed is in addendum §3, §5 (G4) |
| Open: does the course require a visible language model | O | §10 Q1, with owner and timing |
| Open: is the Gemma 4 Apache 2.0 licence confirmed | O | §10 Q7, addendum §3 |
| Evidence: 0 of 6 claims verified; error rates from 2023 models | R | Addendum §5 |

## 2. Misrepresentations

1. **Vision overstates AI (medium).** PRD §1 says "AI explains the result in plain language", and the §9 brief mapping links "AI explanations" to SM-6. The Must explanation is a template (FR-26, AG-2), and report D's biggest caveat is that a template is not AI: version 1 has AI in the app only if FR-28 (Should, open in §10 Q1) is built.
2. **Glossary "Explanation" (low).** "always labelled as AI-written text" can be read as covering template text too, and "AI-written" differs from the UI label «KI-omformulert forklaring» (FR-27), which the glossary does not list although its terms are binding.
3. **§0 wording (low).** "Technology choices ... live in `addendum.md`" can be read as a choice already made; the addendum holds an undecided recommendation. NFR-9 and addendum §1 state it correctly.

Otherwise the PRD and addendum restate C and D accurately. Both matrices, the Flask-wins re-weighting (the addendum's testability-15 note is right: 83 against 81), the error-rate ranges, model sizes, hosted limits, versions and re-check dates match the reports, and the stack is correctly left undecided.

## 3. Gaps

No high-severity gaps.

| # | Severity | Gap | Suggested fix |
|---|---|---|---|
| G1 | medium | §1 and the §9 mapping promise AI explanations that the Must scope does not deliver (§2, item 1). | Reword §1: the explanation is plain Norwegian from fixed templates; an optional local model may rephrase it; neither produces numbers. In §9, note that the AI part depends on FR-28 and §10 Q1. |
| G2 | medium | Offline running is required (NFR-1, FR-28) but never verified: SM-2 checks only "without paid services or keys". A CDN chart script (C-R4's first option) would break it unnoticed, and Ollama's offline use is undocumented (a report D open question) and absent from §10. | NFR-1 or SM-2: after install, the SM-3 flow passes with the network off, and front-end libraries are served locally at pinned versions. Add the offline question to §10 Q7; DR-1 states whether the optional model works offline. |
| G3 | medium | The isolation test is narrower than C-R2 and not gated. FR-2's test names products, sales history and settings, not list views (report C: per-record checks do not partition lists, as Flask's index shows) or the order quantities FR-2 itself lists. SM-4 is secondary and outside the DR-6 and SM-C2 gate, though report C makes isolation a hard gate. | FR-2: company A's product overview (and later the combined order overview and CSV export) shows none of B's products, and adjusted order quantities are tested once built. Add SM-4 to the DR-6 and SM-C2 gate, or make it primary. |
| G4 | medium | §10 Q1 does not say what follows if FR-28 becomes Must: a model download of 1.3 to 7.5 GB, with the quickstart example needing about 8 GB of memory (against SM-2's 15-minute target and NFR-8's "ordinary laptop"), unmeasured speed against NFR-8's 2 seconds, and whether it stays off by default. | Add these consequences to Q1; add "good and fast enough on an ordinary laptop" to Q7; state whether NFR-8 applies with the model on. |
| G5 | low | "Salted hashes" (FR-1, NFR-3) would accept a fast salted hash, while every candidate in report C uses a dedicated password hasher (PBKDF2, scrypt, Argon2 or bcrypt); the work-factor question is open only in addendum §5. FR-3's "identical data on every run" can conflict with salted hashes. | FR-1: use the framework's or a maintained library's password hasher, never a self-written one; confirm the work factor in architecture. FR-3 and DR-4: hash the README test passwords at load time and leave hashes out of the determinism check. |
| G6 | low | FR-28's fallback does not name a stopped server or an error inside a 200 response [D14]; addendum §3 assumes it covers them. SM-6 checks only a "changed number", not swapped labels (the commonest error in [D2]) or added and dropped numbers. | FR-28: fall back on any runtime error; accept only output with exactly the template's numbers, each with its label. SM-6: add swapped-label and dropped-number cases. |
| G7 | low | FR-26 leaves out the old-data warning, included unusual weeks and the no-forecast case, while D-R1 asks for the warnings. | FR-26: cover every active warning (FR-8, FR-15 to FR-18). |
| G8 | low | D-R5 and C-R6 live only in the addendum: DR-1 does not require the model name and licence (Llama 3.2 needs "Built with Llama" when distributed), and DR-5 does not name the unevidenced AI-assistant fit. | Add the model and its licence to DR-1, and the C-R6 limitation to DR-5. |
| G9 | low | Signed sessions need a local secret (inference from report C's signed session cookie). NFR-3 bars committed secrets, and DR-1 does not say how the examiner gets one. | DR-1 and NFR-3: setup creates the secret locally, so the examiner needs no key. |
| G10 | low | FR-28 says "when switched on", but the switch is not a setting in FR-20, and only DR-1 and `.env.example` hint at where it lives. | State that the switch is local configuration listed in `.env.example`, not a company setting. |
