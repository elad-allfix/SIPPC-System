---
area: playbooks
topic: diagnostic playbooks
checked: 2026-10-13
owner: research
---
# Diagnostic playbooks

How the strategist investigates a problem. Every playbook follows the same backbone, then adds symptom-specific branches. Playbooks describe what to check and how to reason, not fixed answers. Each step names the knowledge entries behind it, so the reasoning can be traced and corrected.

## The backbone (applies to every symptom)

1. **Restate the goal.** What does the business count as success for this campaign: profit, qualified leads, engaged traffic, or visibility? A "problem" that leaves the goal unaffected is not a problem. Example: a higher CPC at the same CPA under target bidding (PRC-DIAG-006).
2. **Is the movement real?**
   - Compare like-for-like windows: same weekdays, matured conversions, holidays aligned, and also year on year (PRC-DIAG-014).
   - Allow for conversion lag (PRC-DIAG-003, PLT-BID-014).
   - Compare against the account's own normal variance. "±10%" is a practitioner rule of thumb, not a rule (PRC-DIAG-016).
3. **Decompose before explaining.** Write the identity and find which factor moved (relationships §1, PRC-DIAG-001).
4. **Check in a fixed order**, cheapest and most common causes first (PRC-DIAG-002):
   1. Data integrity (tracking, conversion settings)
   2. Your own changes (change history and off-platform changes: site, offer, price, CRM, staff)
   3. Platform changes (Google rollouts and defaults; see the "changed" markers in `platform/`)
   4. The market (Auction Insights, demand, seasonality, news)
   5. The site and funnel, walked in person
5. **Segment to localise** by device, network, geo, hour, match type, search term, landing page, and new vs returning (PRC-DIAG-013).
6. **List the alternative explanations** that still fit the evidence, and what would separate them.
7. **Decide whether to fix, leave or test** (PRC-DIAG-016).
   - **Fix:** clear errors.
   - **Leave:** noise or learning.
   - **Test:** reversible changes with meaningful upside and enough volume to read. Set the review date and the result that would change the decision before acting.
8. **Report the answer with labels.** Mark each point as verified, observed, estimated, hypothesis or unknown, and say what is still uncertain.

Never do these:
- Change several things at once (PRC-DIAG-020).
- Change bids to fix a tracking problem.
- Tell Smart Bidding nothing about a tracking outage (data exclusions, PLT-BID-022).
- Present a competitor's motive as fact.

---

## D1 · CPC went up
1. **Does it matter?** Under tCPA or tROAS, CPC is an output. Check CPA, ROAS or value per click first (PRC-DIAG-006).
2. **Your levers:**
   - target or strategy changes, auto-applied recommendations (PLT-AUTO-028)
   - broader matching or the move to AI Max (PLT-KW-010)
   - a shift in device or geo mix
   - Performance Max overlap
3. **Mix vs price.** Is CPC stable per keyword or search term while the total rises? Then it is a mix change, not inflation.
4. **Auction.** In Auction Insights, look for new domains and rising overlap or position-above rates. Note the limits: it shows nothing below 10% impression share and excludes partners (PRC-DIAG-006, PLT-AUC-023).
5. **Quality.** Did the components worsen on high-spend exact queries? Landing page changes and new generic ads are typical causes.
6. **Thin auctions.** On niche queries a high CPC can be your own reserve price (PLT-AUC-029). Only better quality lowers it.
7. **Platform pricing.** An account-wide rise with no change in competitors and no change of your own can be Google-side (PLT-AUC-006). Record it as a hypothesis, and look for the same shift in peer accounts or forums.

Alternatives to separate: market seasonality, new competitor, your own target change, mix shift, quality loss, platform pricing.

## D2 · CTR dropped
1. Rule out dilution first: impressions up, clicks flat, and new loose queries, partner traffic or lower positions (PRC-DIAG-007).
2. Check position: top and absolute-top rates; Auction Insights position-above rate.
3. Check the results page: has the page itself changed? AI Overviews, more ads above, a local pack, or competitors with stronger offers. Look at the live page; it is observable.
4. Check the ads: asset fatigue only after 1–3 are ruled out. Look for disapproved or limited assets.
5. Decide whether the drop matters. A CTR drop with a stable or better conversion rate per impression can be healthy filtering.

## D3 · Conversions or conversion rate dropped
1. **Shape.**
   - A cliff, a drop to zero or an exact fraction points to tracking (PRC-DIAG-002).
   - A gradual slide points to market, mix or fatigue.
2. **Tracking checks:**
   - tag diagnostics, backend orders or CRM vs Ads, GA4 vs Ads divergence
   - consent changes, thank-you URL changes, site releases (see `measurement/`)
   - If tracking broke: fix it, apply a data exclusion covering the conversion delay (PLT-BID-022), and do not touch bids.
3. **Conversion lag.** Is it only the recent days? (PRC-DIAG-003)
4. **Off-platform causes:** offer or price changes, stock, forms, mobile page speed, chat widgets, CAPTCHA (PRC-DIAG-008). Segment by device and landing page, and walk the funnel yourself.
5. **Query mix:** has intent drifted toward upper-funnel queries? Check search terms and AI Max expansions (PLT-AUTO-006).
6. **Market:** is there a simultaneous move across unrelated campaigns? That suggests a market shock (PRC-DIAG-015).

## D4 · Low Quality Score
1. Remember that QS is a diagnostic, not the target (PLT-AUC-009, PRC-DIAG-022). Look only at keywords that carry spend and have meaningful exact-match volume (PLT-AUC-010).
2. Read the three components separately and map each one to a link in the intent chain (relationships §2.2):
   - **Ad relevance below average:** the ad group mixes intents, or the ads don't speak to the query. Split by theme; mirror the query's language.
   - **Expected CTR below average:** weak offer or angle, the wrong audience, or an irrelevant query share (the query mix weakens the keyword's CTR history).
   - **Landing page below average:** message mismatch, slow mobile page, the page doesn't answer the query (PLT-AUC-013).
3. Check search terms first, because irrelevant queries depress CTR and relevance.
4. Decide whether to act at all. Work on quality is worth it when rank, not budget, limits volume and the weak signals sit on traffic that matters (PLT-AUC-018).

## D5 · Good-looking traffic that does nothing (traffic quality)
1. Define good traffic for the goal (see `measurement/`). For traffic objectives this means engagement and actions that indicate the right audience.
2. Segment by network (search partners, Display expansion), placement, match type, search term, geo (matched vs targeted locations, PLT-STR-008) and hour.
3. Look for patterns of low-quality or invalid traffic:
   - very short sessions
   - one placement or partner dominating
   - spikes at odd hours
   - "presence or interest" location settings pulling in out-of-area users (PLT-STR-006)
4. Check whether the ad is attracting the wrong audience. A "free", "cheap" or curiosity angle raises CTR among people who will never buy (EV-02).
5. Actions:
   - negatives and n-gram cleanup (PLT-KW-022)
   - location option set to "Presence"
   - review partners and Display expansion
   - qualifying copy
   - move bidding to a better signal (engaged-session conversions, or lead stages)

## D6 · Leads up, sales down (lead quality)
1. The usual mechanism: the bidder is optimising toward form fills, including junk (PRC-DIAG-011).
2. Measure the lead-to-qualified and lead-to-sale rates by campaign, keyword, search term and network. Look for bots: gibberish, duplicates, odd hours.
3. Fixes, in order:
   1. Block bots before the conversion tag fires.
   2. Import qualified or sale stages from the CRM. New offline click import goes through the Data Manager API, because the Google Ads API stopped accepting new adopters on 2026-06-15.
   3. Value leads by stage.
   4. Count only calls above a minimum duration.
   5. Add friction where volume is cheap and junk is high (PRC-DIAG-030).
4. Remember that changing conversion goals or values recalibrates the bidder (PLT-BID-031). Plan for a learning window.

## D7 · Looks profitable, isn't (false profitability)
1. **Reconcile value with the backend**, looking for:
   - tax and shipping counted in value
   - secondary actions counted as primary
   - duplicates
   - pre-close offline values
   - stale value rules
   - returns and cancellations

   Practitioner estimates put inflation at 20–40% in audited accounts (PRC-DIAG-012, PRC-DIAG-038). That is a prior, not a constant.
2. **Compute break-even ROAS** on a margin consistent with the value counted. Include fees and returns.
3. **Split brand from non-brand**, and for PMax measure the brand share of value vs cost. Judge non-brand on its own (PRC-DIAG-028). A brand Search campaign meant to take brand queries back from PMax must not be budget-limited, or PMax serves them again (PLT-KW-007/008).
4. **Split by how the conversion was credited.** Segment PMax and Demand Gen conversions by ad event type (click vs engaged-view or view-through) and by new vs returning customer. Remarketing to existing customers and engaged-view credit from YouTube and Display can raise reported value while backend revenue stays flat (MEA-CONV-005, PLT-AUTO-015). Do this before blaming brand alone, and check whether a gap between platform and backend existed before the change. Check PMax negatives and brand exclusions (PLT-AUTO-017).
5. **Question incrementality.** Would these conversions have happened anyway? This needs a holdout or geo test (PRC-DIAG-027, PRC-DIAG-036/037/039).
6. **Judge scaling on marginal return**, not average return (relationships §4).

## D8 · Spend spike
1. Is it within the documented limits? Up to 2× daily budget on a given day, and no more than 30.4× in a month. Since 2026, campaigns that switch off whole days in their schedule pace toward the full monthly amount (PLT-STR-020/021, PRC-DIAG-009).
2. If not: check change history (budget type, targets, unknown users), new expansion (AI Max, PMax), scripts, and signs of a compromised account.

## D9 · Impression share fell
1. Did impressions fall with IS flat? Then demand fell. Did IS fall? Then you lost auctions (PRC-DIAG-010).
2. Split the loss into budget and rank.
   - **Budget loss on a profitable campaign** is the cheapest lever.
   - **Rank loss under target bidding** may be the bidder rationally skipping expensive auctions (PLT-STR-026).
3. Check exact-match IS on the core queries to find real headroom (PLT-STR-028).
