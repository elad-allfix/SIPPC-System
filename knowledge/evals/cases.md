---
area: evals
topic: evaluation cases
checked: 2026-10-13
owner: research
---
# AllFix evaluation cases

Every case below is **synthetic**: the numbers were written by Claude to create a realistic situation, not taken from a real account. They test whether the strategist reasons well; they do not prove it is expert. Passing them shows only that the knowledge base and reasoning cover the situations we thought of. The real test is Elad's own past cases with known outcomes (see "What these cases cannot show" at the end).

Each case has: the situation and data, the question asked, a rubric (what a strong answer must contain), and traps (what a weak answer would do). Results of running the cases are in `results.md`.

Rubric scoring per case: each rubric line is met / partly / missed. A case passes only if every line marked **(critical)** is met and no trap is hit.

---

## EV-01 · High CPC with weak Quality Score
**Evidence:** synthetic.

**Situation.** Local emergency plumber, one city, Search only. Campaign "Plumbing - General", phrase and broad match, Maximize Conversions, no target. Last 30 days:

| Keyword | QS | Exp. CTR | Ad relevance | LP experience | Avg CPC | Clicks | Conv |
|---|---|---|---|---|---|---|---|
| plumber | 2 | Below avg | Average | Below avg | $38.10 | 210 | 9 |
| emergency plumber | 3 | Average | Below avg | Below avg | $44.70 | 160 | 14 |
| water heater repair | 1 | Below avg | Below avg | Below avg | $29.40 | 90 | 2 |
| blocked drain | 6 | Average | Average | Average | $21.80 | 70 | 6 |

One ad group, one RSA with headlines "Trusted Local Plumbers", "Family Owned Since 1998", "Call Today". All traffic goes to the homepage, which loads in about 6 s on mobile (owner's claim) and leads with a company history video. Search terms include "plumber salary", "plumbing school", "how to fix water heater".

**Question.** "Our CPCs are crazy. How do we bring them down?"

*Correction after run 1 (2026-10-13):* the first version showed QS 4, 5 and 3 for the first three keywords, which do not match their component ratings under the reverse-engineered formula (PLT-AUC-014). The strategist run with the knowledge base caught this. Scores corrected to 2, 3 and 1; run 1 used the old values.

**Rubric.**
1. **(critical)** Explains that QS is a diagnostic summary, not an auction input; the auction uses real-time quality estimates, so "raise QS to 10" is not the goal. Fixing the underlying relevance, expected CTR and landing page is.
2. **(critical)** Reads the three components separately and maps each to a cause: ad relevance (one generic RSA serving all themes), landing page (homepage, slow, video, no service-specific content), expected CTR (generic copy, irrelevant queries).
3. **(critical)** Checks search terms first: job seekers and DIY queries waste spend and depress CTR. Proposes negatives (salary, school, how to, DIY) with the caveat that "how to fix" queries can occasionally become emergency calls.
4. Restructures by intent theme (emergency, water heater, drains) with matching ads and landing pages, rather than splitting keywords for its own sake.
5. Considers alternative explanations for high CPC that QS will not fix: competitive local market, Maximize Conversions with no target bidding up, emergency intent being genuinely expensive, competitors using call ads, LSAs taking top space.
6. Evaluates on cost per lead or booked job, not CPC. Notes that "emergency plumber" has the best conversion rate despite the highest CPC.
7. States uncertainty: 30 days and 31 conversions is little data; component labels are coarse; mobile speed is the owner's claim and should be measured.

**Traps.** Promising a specific CPC reduction. Recommending pausing "emergency plumber" because it is the most expensive. Treating QS as a KPI to maximise. Recommending exact-match-only as the cure without checking search terms.

---

## EV-02 · Strong CTR but poor traffic quality
**Evidence:** synthetic.

**Situation.** B2B SaaS (inventory software for mid-size retailers, plans from $400/month). Campaign launched 6 weeks ago with a new ad: headline "Free Inventory Tool - Try Now". CTR rose from 4.1% to 11.8%. Clicks tripled. Demo bookings: 22 in the 6 weeks before, 19 in the 6 weeks after. GA4 shows engagement rate falling from 61% to 34%. Search terms now include "free inventory spreadsheet", "inventory template excel", "simple stock tracker app".

**Question.** "CTR is amazing, why aren't leads growing?"

**Rubric.**
1. **(critical)** Identifies that "Free" changed who clicks: the ad now attracts a different audience (free-seekers, small shops) whose intent does not match a $400/month product. High CTR is a measure of attention, not of fit.
2. **(critical)** Uses search terms and post-click behaviour to show the shift; does not rely on CTR or conversion rate alone.
3. Lists alternatives: seasonality, a landing page change, tracking change, broad match expansion, competitor change, sales follow-up slowdown. Asks which changed at the same time.
4. Recommends qualifying copy (price signal, "for retailers with 5+ locations", "book a demo"), negatives for free/template/excel terms, and judging by qualified demos or pipeline, not CTR.
5. Notes the trade-off: qualifying copy will lower CTR and may raise CPC through expected CTR; that is acceptable if cost per qualified demo falls.
6. States uncertainty: 22 vs 19 demos is within noise; the main evidence is the composition change, not the demo count.

**Traps.** Celebrating CTR. Recommending more budget because CTR is high. Concluding the landing page is the only problem.

---

## EV-03 · New niche with no history
**Evidence:** synthetic setup; market facts should come from real research.

**Situation.** A client wants to launch Google Ads for a new mobile pet grooming service in two suburbs of a US city. No website yet, no ad account, no CRM. Budget "around $3,000 a month". Average job $90-$140 (client's estimate). They can handle about 40 jobs a week at full capacity, currently about 15.

**Question.** "Where do we start and what should we expect?"

**Rubric.**
1. **(critical)** Starts from the business: margin per job, repeat rate (grooming is recurring, so lifetime value matters more than first job), capacity, service radius. Labels the client's numbers as their estimates.
2. **(critical)** Researches demand and competition before structure: intent clusters ("mobile dog groomer near me", "dog grooming at home", breed-specific, "cat grooming"), local pack and LSAs presence, competitor angles. Says which facts came from research and which are unknown without Keyword Planner or a test.
3. **(critical)** Gives no invented CPC or conversion-rate prediction; gives a reasoning range with sources or labels it as an assumption, and defines what the first weeks must learn.
4. Considers non-Search channels that matter for local services (Google Business Profile, LSAs if eligible) and that the website must exist and convert before spend.
5. Proposes a learning plan: tight geography, high-intent clusters first, call and form tracking from day one, a decision point after a defined amount of data, and what results would change the plan.
6. Notes the capacity ceiling: at ~25 spare jobs a week, scaling beyond capacity is waste.

**Traps.** Recommending PMax or broad match with Smart Bidding from day one with zero conversion history, without discussing the trade-off. Quoting a benchmark CPC as a prediction. Ignoring repeat value.

---

## EV-04 · Competitors using different angles
**Evidence:** synthetic.

**Situation.** Personal injury law firm, one metro. Top-of-page competitors' ads (as captured from the results page): Competitor A: "No Win No Fee - Free Consultation". Competitor B: "$2.1 Billion Recovered for Clients". Competitor C: "Injured? Get Paid Fast - Call 24/7". Competitor D (lead-gen site): "Compare Top-Rated Lawyers Near You". Our ad: "Experienced Injury Lawyers - Call Now". Our CTR 3.2%, impression share 38%, lost IS (rank) 51%.

**Question.** "How do we beat them?"

**Rubric.**
1. **(critical)** Separates what is observable (their ad text, landing pages, presence) from what is not (their bids, budgets, results, whether their angle works for them).
2. **(critical)** Maps each angle to the searcher motivation it targets (risk removal, proof of outcome, speed and money, choice and comparison) and notes that our ad has no distinct angle: "experienced" is a claim every firm makes.
3. Recommends finding an angle grounded in a true differentiator of the firm (case type specialism, language, response time, specific results), and testing angles by intent cluster rather than copying the loudest competitor.
4. Addresses lost IS (rank) 51%: the problem is Ad Rank, i.e. bid and quality. Better angle helps expected CTR and ad relevance; bid is also a lever; both are costly in PI law.
5. Mentions legal advertising rules (state bar rules on claims like results and "specialist") as a constraint on copy.
6. Gives a test design and what result would count as a win (qualified signed cases, not CTR).

**Traps.** Claiming to know competitors' budgets or that "Competitor B is winning". Copying an angle the firm cannot truthfully claim. Recommending outbidding everyone.

---

## EV-05 · Campaign with no conversion objective
**Evidence:** synthetic.

**Situation.** A regional tourism board runs a Search campaign whose goal is visits to its "Things to do" guide, to support hotel occupancy in shoulder season. No bookings happen on their site. Current setup: Maximize Clicks, broad match, $8,000/month. 41,000 clicks/month at $0.19 average CPC. Average engagement time 9 seconds; 71% of clicks from one display-like search partner pattern; top search terms include "free games", "things to do when bored".

**Question.** "Our CPC is so low, the campaign is doing great, right?"

**Rubric.**
1. **(critical)** Accepts that a traffic objective is legitimate and does not demand purchase conversions. Defines "good traffic" for this goal: visitors in or planning travel to the region, engaging with the guide, clicking to partner hotels or events.
2. **(critical)** Identifies that the current traffic is mostly not that: irrelevant queries, search partner pattern, 9-second engagement. Cheap clicks that do not reach the goal are not cheap.
3. Proposes measurable proxies: engaged sessions, scroll or time thresholds, outbound clicks to hotels, newsletter or guide downloads, and optionally setting these as secondary conversions to inform bidding.
4. Recommends tightening match types and queries, location intent (people searching about the region), reviewing search partners, and comparing cost per engaged visit.
5. States what cannot be measured (incremental hotel nights) and suggests a geo or time-based test if the board wants to know that.

**Traps.** Insisting the campaign needs purchase tracking to be valid. Praising the low CPC. Optimising CTR.

---

## EV-06 · Looks profitable but is not
**Evidence:** synthetic.

**Situation.** E-commerce store, kitchen appliances. Google Ads reports ROAS 4.2 (conversion value / cost) on $60,000/month spend. Conversion value includes tax and shipping. Product margin after COGS averages 22%. Return rate on the best-selling SKU (a $900 espresso machine, 38% of revenue) is 17%. Payment fees 3%. 46% of conversions are from brand search. The conversion action counts "Add to cart" as a primary conversion alongside "Purchase".

**Question.** "ROAS is 4.2, should we double the budget?"

**Rubric.**
1. **(critical)** Spots the measurement problems: Add to cart counted as primary (inflates conversions and value or changes bidding), value includes tax and shipping, no returns adjustment.
2. **(critical)** Computes break-even ROAS from stated margin: at 22% margin, break-even is roughly 1 / 0.22 = 4.5 before fees and returns, so 4.2 on inflated value is likely below break-even. Shows the arithmetic and labels inputs.
3. **(critical)** Questions incrementality of brand search (46% of conversions): many would have bought anyway. Recommends separating brand and non-brand economics.
4. Recommends fixing conversion settings, passing net value (or profit) where possible, and a holdout or geo test for incrementality before scaling.
5. Notes that doubling budget usually lowers marginal ROAS (diminishing returns); the decision should use marginal, not average, return.

**Traps.** Saying yes to doubling. Accepting platform ROAS as profit. Ignoring returns.

---

## EV-07 · Conflicting keyword, ad and landing page signals
**Evidence:** synthetic.

**Situation.** Home security company. Ad group "Wireless Security Cameras". Keywords include "wireless security camera" and broad "home security". Ads promise "Professional Installation - 24/7 Monitoring From $29/mo". Landing page is a product page for a $199 DIY camera kit with no monitoring plan mentioned. Search terms: 40% "wireless camera" product queries, 30% "home security system" service queries, 20% "best security camera reddit", 10% brand names of competitors. Conversion rate 1.1%; average across account 3.4%.

**Question.** "This ad group converts badly. Is it the page?"

**Rubric.**
1. **(critical)** Identifies three different promises in one chain: product shoppers (DIY camera), service shoppers (monitored system) and researchers. The ad speaks to service, the page sells a product. Every link mismatches some of the traffic.
2. **(critical)** Splits by intent: product ad group to the kit page with product copy; service ad group to a monitoring plan page; research queries either to comparison content or excluded; competitor terms judged separately.
3. Considers alternatives: the price (from $29/mo vs $199) is confusing; the page may be fine for product searchers; check conversion by search-term segment before blaming the page.
4. Recommends measuring each segment after the split rather than a single verdict.

**Traps.** Answering "yes, redesign the page" without addressing the query and ad mismatch. Treating the ad group as one population.

---

## EV-08 · Beating competitors through intent matching and creative strategy
**Evidence:** synthetic.

**Situation.** Online tutoring company for US high school students (SAT and AP prep). Large competitors dominate "SAT prep" with big brands and high bids. The client cannot outbid them. Budget $15,000/month. They have strong results with students who start 3 months before the test, and offer Spanish-speaking tutors.

**Question.** "We can't outspend them. How do we win?"

**Rubric.**
1. **(critical)** Breaks the market into intent clusters (by test date, by score goal, by subject, by parent vs student searcher, by language, by price sensitivity, by urgency) and finds clusters where the big competitors' generic message fits poorly.
2. **(critical)** Builds creative around true differentiators matched to clusters (bilingual parents, "test in 12 weeks" plans, specific AP subjects), with matching landing pages.
3. Uses timing: test-date calendar seasonality, dayparting for parent searches, and budget concentration where intent is strongest. Labels these as hypotheses to test.
4. Notes what we cannot know: competitors' budgets and whether their generic campaigns are profitable.
5. Defines success by cost per enrolled student and lifetime value, with a test plan.

**Traps.** "Bid on competitor brand names" as the main strategy without discussing cost, QS and trademark limits. Recommending a generic "better ads" answer. Claiming certainty that the niche is underserved.

---

## Additional cases

### EV-09 · Conversion drop that is really a tracking break
**Evidence:** synthetic. Conversions fell 70% overnight on all campaigns; clicks, CTR and CPC unchanged; GA4 sessions unchanged; site deploy happened that day. Strong answer: suspects tracking first (tag removed, consent mode change, thank-you page URL change), verifies with tag diagnostics and backend orders before touching bids; warns that Smart Bidding will react to false data and suggests data exclusions.

### EV-10 · When to do nothing
**Evidence:** synthetic. A tROAS campaign's ROAS fell from 5.1 to 4.3 over 4 days after a target change from 450% to 400%. Strong answer: expects a short learning and conversion-lag effect, checks conversion lag, does not revert or change again within days, sets a review date, and explains that frequent changes make results impossible to read and give the bidder a moving target. It must not claim that every edit "resets learning": Google states a target change does not trigger Learning status (see PLT-BID entries). Since August 2026, budget-limited tCPA/tROAS campaigns drift toward the target rather than beating it, so a fall toward a newly lowered target can be the bidder doing what it was told.

### EV-11 · Lead volume up, sales down
**Evidence:** synthetic. Solar installer switched form to 2 fields, leads up 80%, sales flat, sales team complains. Strong answer: lead quality not lead count; import qualified-lead and sale stages (via the Data Manager API path, since new Google Ads API offline click import adopters are closed since 2026-06-15); consider value-based bidding on qualified stages; consider adding a qualifying field.

---

## What these cases cannot show

- They were written by the same system that will be graded on them, so they test coverage of known situations, not judgement in unknown ones.
- They have no real outcomes: a "correct" answer here is a well-reasoned one, not one proven to have made money.
- The next step is a set of 10-20 of Elad's real past cases (anonymised), each with what was done and what happened, graded blind against the strategist's answer.
