---
title: 'technical research: Explanation without paid API'
type: 'technical'
topic: 'Explanation without paid API'
decision: 'Select how the app produces plain-language forecast explanations without a paid API, keeps AI separate from calculated numbers, and prevents invented figures'
source: 'native run'
status: complete
preset: 'standard'
validation: 'normal'
shape: 'select'
claims_verified: 0
claims_unverified: 6
created: '2026-11-01'
updated: '2026-11-01'
---

# technical research: Explanation without paid API

**Decision this research serves:** Select how the app produces plain-language forecast explanations without a paid API, keeps AI separate from calculated numbers, and prevents invented figures.

## Executive summary

**Pick: template-based explanations as the Must feature, with an optional local language model that only rephrases the template text, as a Should feature.** Runner-up: the hybrid on its own (template always runs, model rephrases). Free hosted APIs are not recommended: the only free tier with documented terms (Gemini) uses submitted content to improve Google's products, requires users to be 18 or older, and, under Google's terms, applies paid-only data terms in the EEA, Switzerland and the UK, which includes Norway (our inference; Norway is not named on the page).

**Three findings that drive this.**
1. Templates have "built-in faithfulness to input", at the cost of authoring effort and stiff wording [1]. A language model can only be trusted with numbers if the application inserts them itself and checks them: in one study of financial summaries about 5% of the numbers in model-written text were wrong, and the most common error was a real number placed in the wrong context, not an invented one [2]. A check that "every number appears in the input" would miss that error [2].
2. Structured output does not fix this. Google states that schema-valid output can still be semantically wrong [23]; the OpenAI and Ollama pages read do not say so either way [28][10]. A published pattern checks every numeric claim in the renderer, not in the model [19].
3. A local model removes keys and cost but adds a heavy install: Ollama's own quickstart example is a 7.2 GB download that needs about 8 GB of memory [6], and a smaller 3B model is about 2 GB [12]. Ollama's documentation says nothing about what happens when the server is not running [14][15].

**Biggest caveat.** The task asks for "AI explanations" and the brief says AI explains the forecasts. A pure template is not AI. If the course expects visible AI use in the app, the optional rephrasing layer is what satisfies it, and it must be demonstrable without a key. None of the recommendations was verified by an independent source, and no source measured small local models on this task.

## Requirements frame (agreed 2026-11-01)

**Hard gates:** runs without a paid API or private key; all numbers come only from deterministic calculations; works offline.
**Weighted criteria (sum 100):** no invented numbers and easy to test (30), runs without a key (25), quality of text (20), setup effort (15), testability (10).

## Candidate screen

| Candidate | Gate result |
|---|---|
| T. Template only | Passes all three gates. |
| L. Local model (Ollama) | Passes key and numbers gates only if the app inserts and checks numbers; offline is not stated explicitly in Ollama's FAQ [8] (local running is). |
| H. Free hosted API with template fallback | Fails the "no key" gate unless the fallback carries the whole app; Gemini free tier is likely unavailable for Norwegian users [22]; Groq's real free limits are unconfirmed [24]; OpenRouter free models allow 50 requests per day without buying credits [25]; Hugging Face gives free users no monthly credits [26]; Anthropic's rate-limit page describes no free tier [27]. |
| Hybrid. Template always, optional model rephrases | Passes all three gates, because the template path needs nothing. |

Cut: **H** as a primary approach. It stays in the matrix for completeness.

## Evidence per criterion

**Template.** The data-to-text literature describes templates and rule-based pipelines as having built-in faithfulness to the input, a regulated style and quick response, with the cost of new templates for every kind of message and restricted naturalness [1] (medium; a preprint survey, qualitative, with no measured error rates). Generated text can be tested deterministically with committed snapshot tests, which the Jest documentation describes for any serialisable value [5].

**Language-model risk.** The financial-summary study found numbers hallucinated in about 5% of cases (Claude 2.0 6.48%, Claude 2.1 3.97%, GPT-4 5.74%), with context mismatch the most common type (2.43%, 1.59%, 3.28%) and pure fabrication rare (0.81%, 0.79%, 0%) [2]. These are 2023-era models, so the figures are older than the three-month bar for AI claims; they show the type of error, not today's rate. The authors found GPT-4 unreliable as an automatic number checker [2]. Anthropic's guidance says that restricting the model to provided data and verifying claims "significantly reduce hallucinations" but "don't eliminate them entirely" and says to validate critical information [3].

**Guardrail pattern.** The Proof-Carrying Numbers preprint proposes that the model emits numeric spans as tokens bound to structured claims and that the renderer, not the model, verifies each one under a stated policy (exact equality, rounding, tolerance) [19] (low-medium; a single preprint). Ollama's documentation tells users to pass the JSON schema also in the prompt, set temperature to 0 and validate the parsed result with Pydantic or Zod [10]. Google's documentation says schema-valid output "can still be semantically wrong" and that values must be validated by the application [23].

**Local model.**
- No account or key is needed for local models; Ollama installs from a download page or a one-line script on macOS and Windows [6][7]; the API listens on `localhost:11434` and the generate endpoint accepts a JSON schema in `format` [8][9][10].
- Sizes: llama3.2 is 1.3 GB (1B) or 2.0 GB (3B); gemma4 e2b is 4.6 to 7.5 GB; the quickstart example model is about 7.2 GB and needs 8 GB of memory [6][12][13]. Ollama has no hardware table [8]. The library page for llama3.2 says the 3B model is strong at instruction following and summarisation [12], but no independent quality measure was found.
- Ollama ships several releases a week (v0.40.13 on 2026-10-28), so a README can only say "current version" [11].
- `GET /api/tags` lists local models, which allows a "model available?" check before calling [15]. A missing model returns 404 and mid-stream errors arrive inside a 200 response [14]. Server-not-running behaviour is not documented (it would be a connection failure at the client; inference).
- Licences: Llama 3.2 3B uses a custom community licence that requires "Built with Llama" attribution on related UI or documentation when distributing, and the model is gated on Hugging Face [16]. Google's blog of 2026-04-02 says Gemma 4 is under Apache 2.0 [18], while the older Gemma Terms of Use are a custom licence [17]; the Apache claim is not confirmed on the Ollama model page.

**Hosted free tiers.**
- Gemini: many models are free of charge, free-tier content is used to improve products, and humans may review it [20][22]. Rate-limit numbers are no longer on the public page and must be read in AI Studio [21]. In the EEA, Switzerland and the UK, paid-service data terms apply and clients made available there may use only Paid Services [22]. Users must be 18 or older [22].
- Groq's page shows Developer-plan base limits, not confirmed free limits [24]. OpenRouter: 20 requests per minute, 50 per day without purchased credits [25]. Hugging Face: no free monthly credits [26]. Anthropic's page lists no free tier [27].
- Blogs say Gemini free quotas were cut in December 2025; sources disagree and none was opened [low confidence].

## Cost and lock-in

All options are free to run locally. Hosted free tiers have changed before and can change again, and a project that depends on one needs a fallback anyway. The template path has no external dependency and no cost. A thin interface (`explain(result) -> text`) with a template implementation and an optional model implementation keeps the exit cost low.

## Verdict (weighted matrix)

Scores are 1 (poor) to 5 (strong), our judgement from the evidence above; weighted total = sum(score x weight) / 5, out of 100. Re-weight freely.

| Criterion (weight) | T. Template | L. Local model | H. Hosted free + template | Hybrid |
|---|---|---|---|---|
| No invented numbers, easy to test (30) | 5 | 2 | 2 | 4 |
| Runs without a key (25) | 5 | 4 | 3 | 5 |
| Quality of text (20) | 2 | 4 | 4 | 4 |
| Setup effort (15) | 5 | 2 | 3 | 3 |
| Testability (10) | 5 | 2 | 2 | 4 |
| **Weighted total** | **88** | **58** | **56** | **82** |

**The pick:** T (88) for the Must feature. **Runner-up:** the hybrid (82), which wins if text quality or a visible AI feature matters more than certainty, for example if the weight on quality rises from 20 to about 40 while the no-invented-numbers weight falls. The gap between T and the hybrid is small relative to our scoring uncertainty, so treat them as the Must and Should of one design rather than rivals.

**Strongest argument against the pick.** A template is not AI, and the brief and the teacher feedback describe AI explanations. A pure template reads stiffly and takes authoring effort for every message type [1].

**Cheapest reversibility hedge.** Define one function `explain(result) -> text` and a numeric validator. Ship the template implementation first. Add the model implementation behind a setting and make the app fall back to the template whenever the model is missing, slow or fails validation.

## Recommendations

1. **Make the template explanation the Must feature.** It states the method, the inputs, the calculation line, warnings and the confidence label in fixed sentences. Feeds: PRD functional requirements and README. Basis: medium [1][5].
2. **Make the model rephrasing a Should feature, local only, off by default.** The application inserts all numbers; the model rephrases text around named placeholders; the application rejects any output whose numbers or placeholders differ from the input (check the label and value together, not just the value). Feeds: PRD and architecture. Basis: low-medium; the pattern is a single preprint [19] and Ollama's own tips [10].
3. **Do not depend on a hosted free tier.** If the group wants one, make it a separate optional setting with a `.env.example`, and expect it to be unavailable in the EEA under Gemini's terms [22]. Feeds: architecture and README. Basis: medium (official terms).
4. **Label AI-written text in the UI and keep it visually apart from calculated results.** The EU Article 50 transparency duties apply from 2 August 2026 to AI text published on matters of public interest, with an exception for human editorial review [4]. They probably do not apply to a school project; the labelling is still good practice and supports the brief's success criterion. Feeds: UX. Basis: medium.
5. **Document the model choice and its licence in the README if it is used:** a 2 GB model such as Llama 3.2 3B with "Built with Llama" attribution [16], or Gemma 4 under Apache 2.0 once confirmed on the model page. Feeds: README and process documentation. Basis: medium for Llama, low for Gemma.

## Open questions

- Which small model gives acceptable short explanations on an ordinary laptop, and how fast is it? No source measured this.
- Is Ollama usable fully offline, and how should the app detect that the server is not running? Neither is documented.
- Does the course expect an AI feature that visibly uses a language model? Ask the teacher; it decides whether the optional layer is a Should or a Must.
- Is the Gemma 4 Apache 2.0 licence confirmed on the official model card?
- Do Anthropic, Gemini or Ollama structured-output docs state that valid structure does not guarantee valid values? Only Google's does.

## Source appendix

All sources accessed 2026-11-01.

| [n] | Claim or finding it supports | Publisher | Pub date | Accessed | Confidence |
|---|---|---|---|---|---|
| [1] | Template strengths and weaknesses, neural hallucination problems | [Osuji et al., data-to-text survey (arXiv 2402.08496)](https://ar5iv.labs.arxiv.org/html/2402.08496) | 2024-02 | 2026-11-01 | medium |
| [2] | About 5% of numbers wrong in LLM financial summaries; context mismatch most common | [Cao et al. (arXiv 2404.06162)](https://ar5iv.labs.arxiv.org/html/2404.06162) | 2024-04 | 2026-11-01 | medium (older models) |
| [3] | Restricting to provided data reduces but does not eliminate hallucination | [Anthropic documentation](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) | undated | 2026-11-01 | medium |
| [4] | EU Article 50 labelling obligations and code of practice | [European Commission](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) | 2026 | 2026-11-01 | medium |
| [5] | Deterministic snapshot tests for generated text | [Jest documentation](https://jestjs.io/docs/snapshot-testing) | undated | 2026-11-01 | high |
| [6] | Install, no key, 7.2 GB example model | [Ollama quickstart](https://docs.ollama.com/quickstart) | undated | 2026-11-01 | high |
| [7] | Scripted installs for macOS and Windows | [Ollama on GitHub](https://github.com/ollama/ollama) | undated | 2026-11-01 | high |
| [8] | Local API port, privacy, cloud toggle, memory behaviour | [Ollama FAQ](https://docs.ollama.com/faq) | undated | 2026-11-01 | high |
| [9] | Generate endpoint parameters | [Ollama API reference](https://docs.ollama.com/api/generate) | undated | 2026-11-01 | high |
| [10] | Structured output via JSON schema, validation tips | [Ollama documentation](https://docs.ollama.com/capabilities/structured-outputs) | undated | 2026-11-01 | high |
| [11] | Release cadence | [Ollama releases](https://github.com/ollama/ollama/releases) | 2026-10-28 | 2026-11-01 | high |
| [12] | Llama 3.2 sizes and summary claim | [Ollama library: llama3.2](https://ollama.com/library/llama3.2) | undated | 2026-11-01 | high |
| [13] | Gemma 4 sizes | [Ollama library: gemma4](https://ollama.com/library/gemma4) | undated | 2026-11-01 | high |
| [14] | Error codes, mid-stream errors | [Ollama errors](https://docs.ollama.com/api/errors) | undated | 2026-11-01 | high |
| [15] | `GET /api/tags` lists local models | [Ollama API (GitHub)](https://github.com/ollama/ollama/blob/main/docs/api.md) | undated | 2026-11-01 | high |
| [16] | Llama 3.2 community licence terms | [Meta via Hugging Face](https://huggingface.co/meta-llama/Llama-3.2-3B) | 2024-09-25 | 2026-11-01 | medium |
| [17] | Gemma Terms of Use (older models) | [Google](https://ai.google.dev/gemma/terms) | 2026-04-01 | 2026-11-01 | high |
| [18] | Gemma 4 under Apache 2.0 | [Google Open Source Blog](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html) | 2026-04-02 | 2026-11-01 | medium |
| [19] | Proof-Carrying Numbers verification pattern | [Solatorio, arXiv 2509.06902](https://arxiv.org/abs/2509.06902) | 2025-09-08 | 2026-11-01 | low-medium |
| [20] | Gemini free-tier models and data handling | [Google, Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) | 2026-10-30 | 2026-11-01 | high |
| [21] | Gemini rate limits are shown only in AI Studio | [Google, Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) | 2026-10-28 | 2026-11-01 | high |
| [22] | Gemini terms: content use, EEA/UK/Switzerland, age 18 | [Google, Gemini API terms](https://ai.google.dev/gemini-api/terms) | 2026-04-28 | 2026-11-01 | high |
| [23] | Schema-valid output can still be wrong | [Google, Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output) | 2026-10-21 | 2026-11-01 | high |
| [24] | Groq limits (Developer-plan base figures) | [Groq documentation](https://console.groq.com/docs/rate-limits) | undated | 2026-11-01 | medium |
| [25] | OpenRouter free-model limits | [OpenRouter documentation](https://openrouter.ai/docs/api-reference/limits) | undated | 2026-11-01 | medium |
| [26] | Hugging Face has no free monthly credits | [Hugging Face documentation](https://huggingface.co/docs/inference-providers/pricing) | undated | 2026-11-01 | high |
| [27] | Anthropic rate limits and tiers, no free tier listed | [Anthropic documentation](https://platform.claude.com/docs/en/api/rate-limits) | undated | 2026-11-01 | high |
| [28] | OpenAI structured outputs and refusals | [OpenAI documentation](https://developers.openai.com/api/docs/guides/structured-outputs) | undated | 2026-11-01 | high |

## Staleness map

This is a selection report on a fast-moving topic: **re-check it before acting on it after 2027-05-01 (two quarters)**. The fastest-ageing claims are hosted-tier terms and limits ([20] to [22], [24] to [27]; re-check within 3 months, by **2027-02-01**), Ollama version and model sizes ([11] to [13]; 1 month, by **2026-12-01**), and the study figures on number errors [2] (AI-adjacent, 3 months; already older than the bar). Earliest re-check: **2026-12-01**.
