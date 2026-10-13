---
area: playbooks
topic: strategic playbooks
checked: 2026-10-13
owner: research
---
# Strategic playbooks

How the strategist plans growth. The diagnostic playbooks (`diagnostic.md`) answer "what went wrong". These answer "where should we go and how do we find out". Each playbook ends with **decision points**: results that would change the plan. A plan without them cannot learn.

Shared principles:
- **The intent cluster is the unit of strategy.** It is a group of searches with the same situation and need. Clusters are a better unit than keywords or campaigns, because value, competition, message and landing page all vary by cluster (relationships §2.2, PLT-KW-029).
- **Value before volume.** Work out what a click is worth before deciding what to pay (MEA-ECON-012, MEA-ECON-027).
- **Practitioner numbers are priors.** Benchmarks give a starting expectation, and the account's own data replaces them as soon as it exists.
- **Competitors are observed, not known.** Their ads, landing pages, offers and presence can be observed. Their bids, budgets, margins, results and motives cannot (PLT-AUC-030).
- **Tests have a hypothesis, a metric, a minimum volume and a review date** (PRC-DIAG-016–020).

---

## S1 · Entering a new niche with no history
For a worked example, see `demo/us-car-insurance-market-research.md`. Detailed methods are in `market/`.

1. **The business model first.**
   - How the client makes money and what one customer is worth: first order, repeat business and lifetime value, used conservatively (MEA-ECON-015/017).
   - Contribution margin, capacity, service area and the sales process.
   - Label the client's own numbers as their estimates.
2. **Value per click, as a formula.**

   value per click = conversion rate × close rate × value per customer × share of value you can spend

   Fill each input with a source or an explicit assumption, and show how the answer changes as the assumptions move. The output is a range plus the input that matters most, not one number (demo §1.2).
3. **Map demand into intent clusters** by customer situation and shared results page, not by word similarity (MKT-NICHE-012/013). For each cluster record:
   - the situation and need
   - the likely value
   - the likely competition
   - what the searcher needs to see
   - which page should answer it

   Sources: Keyword Planner (exact-only volume, pooled close variants, ranges; PLT-KW-025/026), search suggestions, related searches, forums and customer language. Without an account, volumes and CPCs are unknown or third-party estimates.
4. **Look at the results pages for each core cluster:**
   - who advertises, and what angles they use
   - organic and local results, and AI Overviews
   - what the page already answers for free

   This shows where an ad has to earn the click.
5. **Look at the website and the journey.** Is there a page that answers each cluster's need? Check message match, friction and trust (`market/`, PRC-COPY-004–006).
6. **Choose where to start.**
   - Prefer clusters with high intent and a clear fit, where competitors' messages fit poorly and the business has a true advantage.
   - Avoid fighting for the most generic, most contested terms first unless the value supports it.
7. **Set up measurement before spending** (MEA-CONV-030):
   - primary conversion = the real business action
   - call and form tracking
   - enhanced conversions
   - a CRM feedback path through the Data Manager API (MEA-CONV-012)
8. **Run the first test.**
   - Tight geography and high-intent clusters.
   - Phrase or exact match, or broad with a clear negative list, chosen deliberately (PLT-KW-033).
   - Bidding chosen for a zero-history account: manual CPC or Maximize clicks with a cap to learn prices, or Maximize conversions once tracking is trusted. Write down why.
   - A budget sized so the test can produce enough clicks per cluster to read the conversion rate. That size comes from the value-per-click maths, not from a benchmark.
9. **Decision points** (set before launch; kill criteria by failure type, MKT-NICHE-025; size the budget for learning, MKT-NICHE-024; break-even CPC as a range, MKT-NICHE-023):
   - What conversion rate after N clicks would show a cluster is not viable?
   - What cost per qualified lead would justify scaling?
   - What search terms would show the matching is too loose?

## S2 · Competitor and angle analysis
1. **Collect what is observable:**
   - ads on the live results page for each cluster, plus Ads Transparency Center where it renders
   - landing pages, offers, guarantees, prices, proof, calls to action
   - Auction Insights: overlap, position above and outranking share, only above 10% impression share (PLT-AUC-023)
2. **Map each competitor angle to the motivation it serves:**
   - price
   - speed
   - risk removal
   - proof of outcome
   - choice or comparison
   - expertise
   - locality
   - identity or language
3. **Find the gaps:**
   - motivations no one serves for a given cluster
   - claims everyone makes, which therefore do not differentiate (PRC-COPY-015)
   - situations the generic ads ignore (PRC-COPY-005)
4. **Match the gaps to true advantages of the business.** An angle the business cannot truthfully claim is a policy and legal risk (PLT-ADS-029/030, PRC-COPY-018), not a strategy.
5. **Do not infer success from presence.** An advertiser that keeps running an ad is not proof it is profitable. Persistence is weak evidence of something working for them, labelled as such.
6. **Competitor-brand bidding** is a separate decision. Expect confusion clicks and low expected CTR (PRC-DIAG-026, PLT-KW-030/031), and check trademark rules for ad text.

## S3 · Traffic-only objectives
1. **Define good traffic** with the client, in observable terms (MEA-ECON-010):
   - the right geography and audience
   - engaged sessions (GA4 definition, MEA-ECON-007)
   - depth (pages, scroll, time with limits; MEA-ECON-008)
   - meaningful micro-actions (outbound clicks to partners, sign-ups, downloads)
2. **Track those as conversions,** secondary first. Make them primary only if the bidder should optimise toward them. Then watch for proxy-gaming (MEA-ECON-029).
3. **Judge on cost per good visit,** not CPC or CTR. Cheap clicks that miss the definition are not cheap (EV-05).
4. **Guard the traffic:**
   - tight matching and negatives
   - location option set to "Presence" where the audience is local
   - search partners and Display expansion reviewed by segment (MEA-ECON-006, PLT-STR-018/019)
   - watch the gap between clicks and sessions (MEA-ECON-011)
5. **If the real goal is downstream** (sales elsewhere, hotel nights, brand), say what cannot be measured and propose a geo or time test if the client needs to know (MEA-ECON-025).

## S4 · Winning through intent matching and creative strategy
1. **Split each contested market into clusters** by situation, urgency, audience (who is searching for whom), price sensitivity, language and stage.
2. **For each cluster, write the searcher's question.** The ad should answer it in the first headline, and the landing page should continue the same answer (PRC-COPY-004–006).
3. **Build an angle library** per cluster (PRC-COPY-023):
   - specific claims, not category claims (PRC-COPY-008)
   - numbers where they are true (PRC-COPY-002)
   - risk reversal (PRC-COPY-012)
   - proof (PRC-COPY-016/017)
   - qualifying copy where bad clicks are expensive (PRC-COPY-010/022)
4. **Test angles across whole ads or experiment arms.** Per-asset metrics are confounded by serving (PLT-ADS-010/013). Judge on cost per valuable action, not CTR (PRC-COPY-024).
5. **Mind automation.** AI-written text and Final URL expansion can override the message you designed (PLT-ADS-025/027, PLT-AUTO-004). Decide deliberately whether to allow them per campaign, and use text disclaimer assets for wording that must appear (PLT-ADS-023).
6. **Use timing** where demand has a calendar (test dates, seasons, events): concentrate budget where intent peaks. Label any timing effect as a hypothesis until the account's own data shows it.

## S5 · Scaling a campaign that works
1. **Confirm it works on trusted value:** reconciled with the backend, brand split out, and ideally incrementality checked (D7).
2. **Find the headroom:** lost IS (budget), exact-match IS on the core clusters, new clusters, new geography (PLT-STR-024/028).
3. **Estimate the marginal return** from simulators (7-day look-back, PLT-BID-028), past step changes or a test. Scale while the *marginal* return stays above the business threshold (MEA-ECON-018).
4. **Scale in steps.** Each step should be readable after the conversion lag. Since August 2026, budget-limited tCPA and tROAS campaigns converge toward their targets, so set targets deliberately (PLT-BID-007/008).
5. **Check capacity** (staff, stock, delivery) before every step.

## S6 · When to do nothing
1. The movement is within the account's normal variance, or inside the conversion-lag window (PRC-DIAG-003/016).
2. The bidder is adjusting to a change made less than 1–2 conversion cycles ago (PLT-BID-017).
3. A test has not reached its planned volume.
4. The proposed change would mainly "show activity" (PRC-DIAG-016).

In each case, say so explicitly, give the next review date, and say what result would trigger action. Doing nothing is a recommendation and is logged like one.

## S7 · Measurement foundation (before any optimisation is trusted)
1. Primary conversions match the business goal. Secondary actions are not primary (MEA-CONV-001/002).
2. Count settings, windows and attribution model are chosen on purpose (MEA-CONV-003/004/006).
3. Duplicates are defended with transaction IDs (MEA-CONV-020).
4. Enhanced conversions are on, and consent mode is set correctly for the regions served (MEA-CONV-010/017/019).
5. Lead businesses have an offline feedback loop through the Data Manager API, with validation monitoring, because whole requests are rejected if any field fails (MEA-CONV-012/013/014).
6. A reconciliation routine runs: platform, then analytics, then CRM, then finance (MEA-CONV-025, MEA-ECON-026).

## S8 · Launching a local service business (calls and bookings from nearby customers)
Use with S1. Read the entries named in each step; search hits alone miss steps.
1. **Eligibility per channel.** Check LSA at g.co/localservices for the real category and postcode, and record the result (MKT-LOCAL-003). Say whether pre-badge leads apply to this category (MKT-LOCAL-019), check the category's ad policy (MKT-LOCAL-015), and note the migration of LSA into pay-per-lead Performance Max (MKT-LOCAL-006).
2. **Phone handling first.** Name who answers during every hour the ads and listings run. Set hours to staffed hours everywhere (GBP, LSA, call assets, ad schedule), because LSA charges missed calls and missed calls can hurt ranking (MKT-LOCAL-001, MKT-LOCAL-002, MKT-LOCAL-017, PRC-DIAG-029).
3. **Business Profile.** Use the real name, a hidden address for service-area businesses, accurate services and hours, photos, and a policy-safe review routine (MKT-LOCAL-009, MKT-LOCAL-012). LSA reviews and badges now live here (MKT-LOCAL-004).
4. **Channel split by economics.** Pay-per-lead (LSA) suits low tickets. Search suits clusters whose value per click covers realistic CPCs. Compare channels and marketplaces on cost per booked job, not cost per lead (MKT-LOCAL-007, MKT-LOCAL-016).
5. **Budget table.** One table whose rows sum to the cap in the case where every channel runs from day 1. The forecast uses the same spend. Bid caps stay at or below the affordable CPC from the economics, or are labelled as a loss-tolerant learning test.
6. **Measurement.** Define the call conversion for the country (duration, or AI-qualified calls in the US/Canada, MKT-LOCAL-014, MEA-CONV-023), keep LSA leads and Search calls separate and deduplicated in the owner's job log, and plan booked-job import (MEA-CONV-012). Express bidding-switch triggers in qualified calls or booked jobs.
7. **Targeting.** Service area by drive time and job value, "Presence" targeting, the same area on GBP, LSA and ads (MKT-LOCAL-018, PLT-STR-006). Link the Business Profile for location assets (MKT-LOCAL-013).

**Decision points:** cost per booked job by channel against the affordable figure; answer rate below about 90%; LSA leads disputed or out of area; Search clusters that never book after their planned click volume.
