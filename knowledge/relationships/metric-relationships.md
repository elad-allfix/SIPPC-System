---
area: relationships
topic: how the variables relate
checked: 2026-10-13
owner: research
---
# How the variables relate

This file is the strategist's map of how Google Ads numbers depend on each other. It has three layers, each held to a different standard of certainty:
1. **Identities**: arithmetic that is always true. These are safe to compute with.
2. **Mechanisms**: causal links that Google documents. The direction is known, but the size is not.
3. **Tendencies**: patterns from practitioners or studies. Treat them as priors to test, never as rules.

The most important idea: **almost every headline metric is a product or ratio of other metrics**, so a change in one is first decomposed into its parts (PRC-DIAG-001) before anyone looks for a cause. Most bad diagnoses come from skipping that step.

Entry IDs refer to files in `platform/`, `practice/` and `measurement/`.

---

## 1. Identities (always true, high confidence)

| Identity | Notes |
|---|---|
| Cost = Clicks × Avg CPC | |
| Clicks = Impressions × CTR | |
| Impressions = Eligible impressions × Impression share | Eligible impressions are Google's *estimate* (PLT-STR-025). |
| 1 = IS + Lost IS (budget) + Lost IS (rank) | Search IS components, per campaign (PLT-AUC-022). |
| Conversions = Clicks × Conversion rate | Conversion rate depends on which actions are counted as primary and on the attribution model. |
| CPA = Avg CPC ÷ Conversion rate | So CPA can rise with a falling CPC if the conversion rate falls faster. |
| ROAS = Conversion value ÷ Cost = (Value per conversion × Conv. rate) ÷ Avg CPC | |
| Value per click = Conversion rate × Value per conversion | Break-even CPC = Value per click × margin share you can spend. |
| Break-even ROAS = 1 ÷ Contribution margin (on the value counted) | Only when "value" is revenue and margin is measured on the same base (MEA-ECON-012/013/014; section 5). |
| Profit = Σ(true value of each conversion × margin) − Cost − other variable costs | Platform ROAS never includes returns, fees, cancellations or lead quality unless you send them in. |
| Marginal CPA ≥ Average CPA when scaling along a concave curve | Section 4; PLT-BID-030, MEA-ECON-018. |

Use: when a headline metric moves, write its identity and see which factor moved. A CPA rise is a CPC rise, a conversion-rate fall, or both. A CTR fall can come from a changed impression mix with no change in any one ad (PRC-DIAG-007).

---

## 2. Mechanisms (documented direction, unknown size)

### 2.1 The auction

```
Bid ─────────────────┐
Auction-time quality ├─► Ad Rank ─► eligible? position? ─► Impressions, Top/Abs-top share
 (exp. CTR, ad rel.,  │       │
  landing page)       │       └─► Actual CPC = minimum to beat the next Ad Rank or your threshold
Thresholds ◄─ quality ┤
Context of search ────┤
Expected asset impact ┘
```

- Ad Rank has six inputs: the bid, auction-time quality, thresholds, competitiveness, search context and the expected impact of assets (PLT-AUC-001). The visible 1–10 Quality Score is **not** an input (PLT-AUC-009). It is a historical report on exact-match searches only (PLT-AUC-010).
- Quality acts on cost in two places. It raises your Ad Rank for a given bid, and it lowers your own threshold (PLT-AUC-002). In a thin auction you pay your own threshold, so poor quality is expensive even with no competition (PLT-AUC-029).
- The price paid depends on the competitor ranked just below you and on your threshold, not on your own bid (PLT-AUC-003). Raising your bid changes your position and eligibility. It changes your price only by moving you above different competitors.
- Google adjusts pricing parameters itself, and advertisers are not told (PLT-AUC-006). So a CPC rise across the whole account with no change in Auction Insights can come from Google rather than from competitors. This is a **hypothesis to rule in or out**, never a default excuse.
- Within one account, keywords do not compete with each other. Google picks one route by precedence: an identical exact keyword first, then other keywords identical to the query, then AI relevance, then Ad Rank (PLT-AUC-025, PLT-KW-006, PLT-AUTO-003). After the September 2026 move to AI Max, broad keywords no longer get exact-like priority (PLT-KW-010).

### 2.2 The intent chain and the three quality components

The strategist reasons along the intent chain:

**Situation → Query → Results page → Ad → Click → Landing page → Action → Business value**

| Link | What breaks it | Metric that shows the break | Quality component it affects |
|---|---|---|---|
| Situation → Query | the need is real, but the words are ambiguous | search terms; query mix | none directly |
| Query → Ad | the ad answers a different intent | ad relevance status; search terms × ad group | ad relevance (PLT-AUC-012) |
| Results page → Click | competing answers (organic, AI Overview, local pack, competitors) or a weak offer | CTR adjusted for position; top/abs-top share | expected CTR (PLT-AUC-011) |
| Click → Landing page | message mismatch, speed, the page doesn't answer the query | bounce/engagement by query segment | landing page experience (PLT-AUC-013) |
| Landing page → Action | friction, trust, price, offer | conversion rate by segment | none (conversion rate is not a QS input) |
| Action → Business value | the action is not a sale (spam leads, returns, unqualified) | CRM stages; refunds; lead-to-sale rate | none, and it is invisible to the bidder unless imported (PRC-DIAG-011) |

The two links at the end are where most "great account, no money" cases live. Google's quality signals cannot see them.

### 2.3 Bidding and budgets

- **Smart Bidding** sets a bid for each auction from a predicted conversion rate or value (PLT-BID-003). Its quality is limited by the conversion signal it is given. If you send the wrong event, it optimises toward the wrong event (PRC-DIAG-011).
- **Target and budget** play different roles. The target sets efficiency; the budget caps volume (PLT-BID-008). **(changed 2026-08)** A budget-limited tCPA or tROAS campaign now converges *toward* its target instead of beating it (PLT-BID-007), so a stale lax target now spends money that it used not to.
- **Maximize conversions or value with no target** spends the whole budget by design. "Budget-limited" status is expected for these strategies and is not a signal (PLT-BID-004).
- **Conversion lag**: recent days always show full cost and incomplete conversions (PLT-BID-014, PRC-DIAG-003). Read results by conversion time, or wait out the lag, before judging a change.
- **Lost IS (budget)** says impressions were missed. It does **not** say those impressions would convert at the current CPA (PLT-STR-024).
- **Lost IS (rank)** under target bidding is often the bidder choosing to skip expensive auctions, not a failure (PLT-STR-026).
- **(changed 2026)** Ad schedules that switch off whole days now pace toward 30.4× the daily budget per month. A day-limited campaign can spend up to about twice what it used to (PLT-STR-021).

### 2.4 Matching and query mix

- A match type sets the *pool* of possible queries. Smart Bidding sets what is paid in each one. Broad match combined with value-based bidding behaves very differently from broad match with Maximize clicks (PLT-KW-003, PLT-KW-033).
- A changed query mix moves CTR, conversion rate and QS together, even when no ad or page changed. Always check the search terms before blaming creative (PRC-DIAG-007, PRC-DIAG-008).
- Hidden search terms (roughly 20–45% of clicks or spend in practitioner and study samples; PLT-KW-013) and approximated search terms (PLT-KW-014) cap how much of the query mix can be known.

---

## 3. Tendencies (priors, test before relying)

| Tendency | Evidence | When it fails |
|---|---|---|
| Higher quality usually means lower CPC for the same position | Google says it "can often" lower CPCs; the "QS 10 = 50% off" tables are an artefact of the old formula, not a measurement (PLT-AUC-017) | thin auctions; aggressive competitors; position goals |
| Higher CTR raises expected CTR and helps Ad Rank | documented mechanism; size unknown; CTR alone is a weak quality metric (MEA-ECON-019, PRC-COPY-024) | when the clicks are the wrong audience. Cost per *useful* visit can rise (EV-02) |
| Brand search is cheap and converts well, but much of it would happen anyway | Haus: significant lift 82% of the time for brands with strong competition, 35% with low competition (PRC-DIAG-025) | depends on whether competitors bid on your brand |
| AI Max adds volume at worse efficiency | independent studies with high variance; Google reports better outcomes (PLT-AUTO-007/008) | varies by vertical; little lead-gen evidence |
| Scaling spend lowers marginal return | economic logic plus Google's simulator curves (PLT-BID-030) | when demand is growing, or when a structural fix opens new demand |
| Experiments called at 80% confidence produce false winners | Google's default threshold (PRC-DIAG-018) | long, high-volume tests |

---

## 4. Diminishing returns and the scaling question

Each extra unit of spend buys conversions at a **marginal** CPA that is usually above the average. The question "should we double the budget?" is answered with:
1. The marginal return, from the bid or budget simulator (a 7-day look-back estimate; PLT-BID-028), from past step changes, or from a test.
2. Whether there is headroom: lost IS (budget) together with exact-match IS on the core queries (PLT-STR-028).
3. Whether the business can absorb the volume (capacity, stock, sales follow-up; PRC-DIAG-029).

The average ROAS being above break-even does not show that the next dollar is above break-even.

---

## 5. Misleading pairs: metrics that move together for the wrong reason

| Looks like | Could actually be | How to tell |
|---|---|---|
| CTR up, good | the ad now attracts a different, cheaper-intent audience | search terms; engagement and lead quality by segment (EV-02) |
| CPC down, good | lower-quality inventory (partners, broad expansion, cheap informational queries) | segment by network, match type and search term (EV-05) |
| ROAS up, good | value inflation: tax or shipping in value, secondary actions counted as primary, duplicates; or more brand traffic | reconcile with backend orders; split brand from non-brand (PRC-DIAG-012, PRC-DIAG-038) |
| Conversions up, good | a lead-form change brings in low-quality leads; a new conversion action was added | lead-to-sale rate; conversion action breakdown (EV-11) |
| Conversion rate down, bad | conversion lag; a tracking break; a mix shift toward a new, upper-funnel segment | conversions by conversion time; tag checks; segment (EV-09) |
| QS low, bad | broad reach or a niche with little exact-match data; QS is a diagnostic | look at the components on high-spend exact queries only (PRC-DIAG-022) |
| Lost IS (rank) high, bad | target bidding deliberately skipping expensive auctions | compare marginal CPA against the target |
| Impression share down, bad | demand grew (the denominator went up) | impressions trend vs IS trend (PRC-DIAG-010) |

---

## 6. What cannot be observed, so the strategist reasons around it

- Competitors' bids, budgets, margins, quality and motives. Auction Insights shows overlap and position rates only (PLT-AUC-023, PLT-AUC-030).
- Google's internal pricing parameters and the real-time quality estimates (PLT-AUC-006, PLT-AUC-009).
- Hidden search terms, and the real wording of searches made through AI surfaces (PLT-KW-013, PLT-KW-014).
- Placement inside AI Overviews or AI Mode, which has no separate reporting (PLT-AUTO-032).
- Incrementality: whether a conversion would have happened anyway. This needs a holdout or geo test (PRC-DIAG-027, MEA-ECON-025).
- Modelled and cross-device conversions inside the "Conversions" column, which cannot be audited one by one (MEA-CONV-018, MEA-CONV-026).

When a conclusion depends on one of these, the strategist labels it as a hypothesis and names the test that would settle it.
