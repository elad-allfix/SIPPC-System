---
area: practice
topic: expert diagnosis and decision craft
checked: 2026-10-13
owner: research
---
# How exceptional campaign managers investigate and decide

This file covers four things: how experienced PPC managers diagnose performance changes (order of checks, metric decomposition, segmentation, separating market shifts from account changes), how they decide whether to test, change or leave something alone (including the mechanics and statistical limits of Google Ads experiments), when common advice fails, and which less common tactics hold up against evidence. It ends with case studies that include numbers. The most important idea is to **establish that the data is true before explaining it**. Broken or inflated conversion tracking, conversion lag and mix shifts cause more "performance changes" than auction dynamics do. After that, decompose the headline metric into its drivers and check whether the change came from you (change history), the market (auction insights, demand) or the website. Only then act, and change one thing at a time.

Evidence note: the search and fetch budget for this research session ran out before Microsoft Ads import documentation, Reddit or PPCChat mirrors beyond one recap, and the Lost IS definitions page could be opened. Entries that rely on those are marked inference or hypothesis and carry lower confidence.

---

## A. Investigation methods

### PRC-DIAG-001 · Decompose the headline metric before looking for causes
- **Claim:** Experts do not look for causes of "CPA went up" directly. They break the metric into drivers (conversions = impressions × CTR × CVR, and CPA = CPC ÷ CVR) and follow whichever branch moved, down to campaign, ad group, keyword, device, network and geo.
- **Evidence type:** practitioner (consistent across independent writers), with inference for the arithmetic.
- **Confidence:** high
- **How it works:** Each driver has a different set of possible causes. CPC is driven by the auction and by your bids. CTR is driven by ads, the SERP and the impression mix. CVR is driven by the site, the offer, tracking and query intent. Impressions are driven by demand, impression share and targeting. Identifying which driver moved removes most hypotheses. Search Engine Land's four-level "metrics tree" (Wenner, 2024) runs from top-level KPIs, to CTR/CVR/CPC/clicks, to impression share and QS components, to segments. An Optmyzr-authored piece on SEL describes the same tree and adds a bottom-up method: export entity-level data for the bad period and a normal period, join them, compute deltas and sort by absolute change. This exposes good and bad changes that cancel out in averages.
- **When it matters / how experts use it:** Use it first for any reported "performance drop". If CPA rose 30% because CPC rose 30% while CVR held, investigate the auction, bids and match-type mix, not the landing page. If CPC held and CVR fell, investigate the site, tracking and the query mix.
- **Exceptions and failure modes:** Ratios mislead when volumes are small. Mix shifts can make every segment improve while the total worsens (Simpson's paradox), for example when spend moves toward a weaker device. The bottom-up method needs minimum-volume filters, or noise dominates the sorted list.
- **Signals in data:** One driver moves while the others stay flat. Large offsetting deltas in the bottom-up join.
- **Sources:** [How to recover from Google Ads performance drops (SEL, Wenner)](https://searchengineland.com/google-ads-performance-drops-recover-444357) (checked 2026-10-13); [How to check why PPC performance changed (SEL, sponsored by Optmyzr)](https://searchengineland.com/how-to-check-why-ppc-performance-changed-316778) (checked 2026-10-13)

### PRC-DIAG-002 · Order of checks: data integrity, then your own changes, then market, then site
- **Claim:** Practitioners converge on this order: (1) verify that conversion tracking and data are intact, (2) read change history and other internal changes (site releases, offer or price changes), (3) check the market (auction insights, demand, seasonality, news), (4) inspect the landing page and funnel in person. The shape of the change tells you where to start. A cliff to zero almost always means tracking. A gradual slide points to market, mix or fatigue.
- **Evidence type:** practitioner
- **Confidence:** high (that this order is common practice). Medium that it is optimal in every case.
- **How it works:** Internal causes are the most frequent and the cheapest to rule out. Tabeling (SEL) names removed tags and conversion events after site releases as "the most common self-inflicted wound". In a PPCChat recap (Sept 2026), Julie Bacchini checks conversion tags first, then campaign data, change history, CPC spikes, auction insights and landing pages. Menachem Ani (SEL) notes that a complete drop to zero conversions points to tracking much more clearly than a 20% fall does. He also compares the start date of the decline with client-side changes such as new offers, sales-flow changes and price increases.
- **When it matters / how experts use it:** Use it for the first 30 minutes of any investigation. Before touching bids, confirm that conversions still fire (Tag Assistant, a test conversion, GA4/CRM cross-check) and that nobody changed anything.
- **Exceptions and failure modes:** When spend is running away (hacked account, budget typo), stop the bleeding before diagnosing. Market shocks (war, inflation, a competitor's promotion) can be the first-order cause, and checking internal causes first only delays the answer slightly. Change history may not show everything (see PRC-DIAG-004).
- **Signals in data:** Conversions fall to zero or by a round fraction (for example exactly half, which suggests one of two tags died). Clicks are stable while conversions vanish. GA4 and Ads diverge suddenly.
- **Sources:** [PPCChat: when you're doing everything right and performance still sucks (Karooya recap)](https://www.karooya.com/blog/ppcchat-when-youre-doing-everything-right-performance-still-sucks/) (checked 2026-10-13); [What to do when performance tanks in PPC (SEL, Tabeling)](https://searchengineland.com/?p=432558) (checked 2026-10-13); [PPC diagnostics: low conversions (SEL, Ani)](https://searchengineland.com/ppc-diagnostics-low-conversions-450710) (checked 2026-10-13)

### PRC-DIAG-003 · Conversion lag makes recent periods look worse; read conversions by click date with care
- **Claim:** Google Ads attributes conversions in the standard columns to the date of the click, not the date of the conversion. Conversions can arrive up to 90 days after the click, depending on the conversion window. As a result, the most recent days always look under-converted while their cost is complete. Experts judge recent performance only after the typical lag has passed, or they use "(by conv. time)" columns.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google Help says the primary columns are "calculated based on the time of the click", and that "All conv. (by conv. time)" reports by when the conversion happened. For lag analysis, Google advises setting the date range to end at least 30 days ago and segmenting by "Days to conversion". For Smart Bidding, hovering over conversion columns shows the average delay.
- **When it matters / how experts use it:** Never compare "last 7 days" with "previous 7 days" for a business with multi-day lag. Compare periods that are equally mature, or exclude the last N days, where N is about the 80–90th percentile of days to conversion. Lead-gen and B2B accounts with offline imports can lag by weeks.
- **Exceptions and failure modes:** In e-commerce with same-session purchases, lag is small and the effect is minor. The "by conv. time" columns fix the timing but break the link between conversions and the cost that produced them.
- **Signals in data:** CPA spikes in the last few days that "heal" as days pass. The bid strategy report shows a conversion-delay shaded zone.
- **Sources:** [Understand your conversion tracking data (Google Ads Help)](https://support.google.com/google-ads/answer/6270625?hl=en) (checked 2026-10-13); [Find out how long it takes for your customers to convert (Google Ads Help)](https://support.google.com/google-ads/answer/6239119?hl=en) (checked 2026-10-13)

### PRC-DIAG-004 · Change history is necessary but incomplete; annotate everything else
- **Claim:** Change history covers 2 years and shows who changed what, including API and third-party tool changes and some Google-system entries. Google says some account-level changes, and changes made by Google representatives during consultations, may not appear. Website, offer, CRM and tracking changes never appear. Experts therefore keep an external change log or annotations.
- **Evidence type:** documented (limits); practitioner (annotation habit)
- **Confidence:** high
- **How it works:** Filter change history by date, change type and campaign around the inflection date. Entries labelled "Google Ads API" or a tool name reveal scripts and tools. Auto-applied recommendations should be audited separately on the Recommendations page; the Optmyzr CPC-spike article lists auto-applied bid, match-type and keyword changes as a CPC-spike cause. The Help page does not say whether auto-applied recommendations always show in change history (unverified). PPCChat participants keep weekly landing-page screenshots and annotate site releases. Tabeling recommends a buddy-system QA before launches and individual logins so changes can be traced.
- **When it matters / how experts use it:** Use it whenever a metric breaks on a specific date. Match the inflection date to change-history entries, deploys, promotions and platform announcements.
- **Exceptions and failure modes:** Bulk edits affecting more than 2,000 entities show truncated details. Inferring cause from timing alone is weak when several changes coincide, which is another reason for one change at a time (PRC-DIAG-020).
- **Signals in data:** A step change in a metric on the same day as a logged change. "Google Ads system" or unknown-user entries.
- **Sources:** [About change history (Google Ads Help)](https://support.google.com/google-ads/answer/19888) (checked 2026-10-13); [Why your Google Ads CPC spiked overnight (Optmyzr)](https://www.optmyzr.com/blog/google-ads-cpc-spike-causes-prevention/) (checked 2026-10-13); [PPCChat recap](https://www.karooya.com/blog/ppcchat-when-youre-doing-everything-right-performance-still-sucks/) (checked 2026-10-13)

### PRC-DIAG-005 · Google's "Explanations" can shortcut diagnosis, within strict limits
- **Claim:** Explanations, shown in time-comparison mode, lists the most likely causes of changes in cost, clicks, impressions, conversions or value. Causes can be bidding, budget, conversion settings or delay, rejection rate, assets and eligibility, targeting, learning, auction competition and search interest, and day-of-week effects. They only appear for equal-length, contiguous periods within the last 90 days that exclude today, and only for metrics tied to the campaign's bid strategy.
- **Evidence type:** documented
- **Confidence:** high for the mechanics; medium for its diagnostic accuracy (not independently validated).
- **How it works:** Under Max Conversions, only cost and conversions are explained. Under Manual or Enhanced CPC Search, impressions, clicks, cost, conversions and value are explained. (changed, date unknown: the 2019 Help page said Explanations covered only manual and enhanced CPC Search. The current page lists Search, PMax, Demand Gen, Display, Video and App.)
- **When it matters / how experts use it:** Use it as a hypothesis generator after the data-integrity check, not as a verdict. It is useful for pointing quickly at shared-budget reallocation or bid strategy target changes.
- **Exceptions and failure modes:** It only shows for "significant" changes. It cannot see off-platform causes (site, CRM, offer). It cannot compare non-adjacent periods such as year-over-year.
- **Signals in data:** The "See explanations" link in comparison mode.
- **Sources:** [About explanations (Google Ads Help)](https://support.google.com/google-ads/answer/9000655?hl=en) (checked 2026-10-13); [Understand performance changes with explanations (older Help page)](https://support.google.com/google-ads/answer/9569021?hl=en) (checked 2026-10-13)

### PRC-DIAG-006 · Diagnosing a CPC increase: is it you, the auction, or quality, and does it even matter?
- **Claim:** A CPC rise has three families of causes. (1) Your own levers: higher targets, a bid strategy change, a broader match-type or query mix, device or geo mix, Performance Max and Search overlap. (2) Auction pressure: new entrants, rising overlap or position-above rates, seasonal crowding. (3) Lower ad quality or landing-page relevance. Under tCPA or tROAS, CPC is an output. A higher CPC at a stable or better CPA or ROAS is not a problem.
- **Evidence type:** practitioner + documented (auction insights definitions)
- **Confidence:** medium-high
- **How it works:** Check change history for target and strategy changes first. Then compare auction insights across the two periods for new domains and changes in overlap rate, position-above rate and outranking share. Then split CPC by match type, search term, device and network to find mix shifts. Optmyzr gives an example in which 72 new competitors appeared and a long-time rival doubled its share. Auction insights only reports competitors when you have at least 10% impression share, and it excludes search partners.
- **When it matters / how experts use it:** If CPC rose but CPA held, leave it alone or reconsider whether the higher-CPC traffic is incremental. If a competitor is the cause, decide whether to match (position effects matter mostly on brand terms, PRC-DIAG-024/025) or retreat to cheaper long-tail and off-peak inventory.
- **Exceptions and failure modes:** Auction insights shows that competitors appeared, not what they bid; competitor bids and budgets are unobservable. An average CPC rise can be pure mix with no single keyword's CPC changing. When Enhanced CPC was retired (Optmyzr says March 2025; not verified against Google's own announcement), migrated campaigns could have used stale targets (changed 2025-03).
- **Signals in data:** New domains in auction insights. Rising position-above rate. CPC stable per keyword while the total rises (mix). A CPC jump on the date of a target change.
- **Sources:** [Why your Google Ads CPC spiked overnight (Optmyzr, Mod)](https://www.optmyzr.com/blog/google-ads-cpc-spike-causes-prevention/) (checked 2026-10-13); [Auction insights (Google Ads Help)](https://support.google.com/google-ads/answer/2579754?hl=en) (checked 2026-10-13)

### PRC-DIAG-007 · Diagnosing a CTR drop: rule out impression-mix dilution before blaming the ads
- **Claim:** Most account-level CTR drops are mix effects: more impressions in low-CTR places (new broad keywords, close variants, lower positions, search partners, PMax text placements) rather than worse ads. Experts segment CTR by keyword, search term, network and top-of-page rate before rewriting ads.
- **Evidence type:** inference (from documented metric definitions) + practitioner
- **Confidence:** medium
- **How it works:** CTR = clicks ÷ impressions. A large influx of marginal impressions lowers the ratio even when every existing ad performs the same. The Optmyzr method flags entities with four consecutive weekly CTR declines above an impression floor, which separates slow fatigue from step changes. A drop in top-of-page rate or absolute-top rate in auction insights points to rank loss.
- **When it matters / how experts use it:** If CTR fell but clicks and conversions did not, the "problem" may be extra free impressions. Do nothing. If CTR fell on stable keywords at a stable top-of-page rate, look at the SERP (new competitors, AI Overviews, Shopping units) and at assets.
- **Exceptions and failure modes:** Expected CTR feeds Quality Score and ad rank, so persistent real CTR declines can raise CPC. Pre-qualifying copy (for example price in the ad, PRC-DIAG-031) lowers CTR on purpose.
- **Signals in data:** Impressions up and CTR down with clicks flat. Search-term report full of new loosely related queries. Network segment shows partner impressions growing.
- **Sources:** [How to check why PPC performance changed (SEL/Optmyzr)](https://searchengineland.com/how-to-check-why-ppc-performance-changed-316778) (checked 2026-10-13); [Auction insights (Google Ads Help)](https://support.google.com/google-ads/answer/2579754?hl=en) (checked 2026-10-13)

### PRC-DIAG-008 · Conversion-rate drop with stable traffic: site, offer, tracking or query mix
- **Claim:** When clicks and CPC hold but CVR falls, the cause is usually off-platform (site release, form or checkout break, price or offer change, stock-outs, slow mobile pages), a tracking change, or a shift in query intent. Device and landing-page segmentation usually isolates it.
- **Evidence type:** practitioner
- **Confidence:** medium-high
- **How it works:** Wenner's worked example: conversions fell with CTR stable. CVR was the culprit, the landing-page experience rating had dropped, and the fall was concentrated on mobile, so the problem was a mobile landing page. He also recommends walking the customer journey personally, at least twice, through to a completed checkout. Ani adds price increases and sales-flow changes on the client side. Tabeling adds CAPTCHA changes, chatbots and banners added by developers.
- **When it matters / how experts use it:** Ask the client "what changed on your side?" before optimising the ads. Segment CVR by device, landing page, new vs returning visitors, and search term.
- **Exceptions and failure modes:** External demand quality can fall too. Tabeling cites a client whose CVR fell 15% year over year in connection with the war in Ukraine. Conversion lag mimics a CVR drop in recent data (PRC-DIAG-003).
- **Signals in data:** The CVR drop is concentrated on one device or landing page. GA4 shows rising form-start-to-submit abandonment. Landing-page experience falls to "Below average".
- **Sources:** [SEL, Wenner](https://searchengineland.com/google-ads-performance-drops-recover-444357) (checked 2026-10-13); [SEL, Ani](https://searchengineland.com/ppc-diagnostics-low-conversions-450710) (checked 2026-10-13); [SEL, Tabeling](https://searchengineland.com/?p=432558) (checked 2026-10-13)

### PRC-DIAG-009 · Sudden spend spike: documented overdelivery vs real problems
- **Claim:** A campaign can legitimately spend up to 2× its average daily budget on a given day. Monthly spend is capped at about 30.4× the average daily budget, and served cost above the limits is not billed. A spike above that pattern points to a budget or bid change, a new broad or PMax expansion, a script or rule, a hacked account, or traffic anomalies.
- **Evidence type:** documented (limits); practitioner (other causes)
- **Confidence:** high
- **How it works:** Check whether the month is within 30.4× before alarming anyone. Then read change history for budget or target edits (Tabeling: daily budget accidentally switched to lifetime). Then look at search terms, placements, networks and hour-of-day. Tabeling reports a hack that "blew through a $100,000 budget before the workday started". He also reports an undisclosed holiday spend spike that triggered an account suspension and about $150k of lost sales, so warn Google of planned spikes.
- **When it matters / how experts use it:** Set campaign-level spend and CPC alerts (Optmyzr advises campaign- or keyword-level alerts so local spikes are not averaged away). Use 2FA and individual logins.
- **Exceptions and failure modes:** Mid-month budget changes reset the 30.4× arithmetic. Shared budgets can move spend between campaigns without any change to the shared budget amount.
- **Signals in data:** Daily cost above 2× average. Unknown users in change history. Spend concentrated in unusual hours or placements.
- **Sources:** [Budget overdelivery (Google Ads Help)](https://support.google.com/google-ads/answer/2375423?hl=en) (checked 2026-10-13); [SEL, Tabeling](https://searchengineland.com/?p=432558) (checked 2026-10-13); [Optmyzr CPC spike](https://www.optmyzr.com/blog/google-ads-cpc-spike-causes-prevention/) (checked 2026-10-13)

### PRC-DIAG-010 · Impression-share loss: separate demand change from competitiveness change
- **Claim:** Impressions = eligible impressions × impression share. If impressions fell while impression share held, demand (or eligibility) shrank. If impression share fell, you lost auctions. Lost IS (budget) and lost IS (rank) then split the cause. Impression share is an estimate that already excludes auctions you could only win with an implausibly large bid increase, and it excludes search partners.
- **Evidence type:** documented (definitions) + inference (the decomposition)
- **Confidence:** high
- **How it works:** Google estimates eligible impressions using targeting, approval and quality, including "quality for you and other participants". The Help page gives an example: auctions needing a 1,000% bid increase are excluded. Auction insights hides data below 10% impression share. On a profitable campaign, budget-lost IS is the cheapest lever. Rank-lost IS calls for bids or quality, and it may be rational to accept it.
- **When it matters / how experts use it:** Before telling a client "we're losing to competitors", check that impression share actually fell. Pair it with Google Trends or Keyword Planner volume (Wenner's "market" area).
- **Exceptions and failure modes:** Chasing impression share as a goal often buys expensive marginal impressions (PRC-DIAG-024). Under Smart Bidding, rank-lost IS can be the algorithm deliberately skipping unprofitable auctions. Small fluctuations are noise (Google says so explicitly).
- **Signals in data:** Impressions and IS moving together (competitiveness) vs impressions moving with IS flat (demand). Budget-lost IS above 0 on a campaign beating its target.
- **Sources:** [About impression share (Google Ads Help)](https://support.google.com/google-ads/answer/2497703?hl=en) (checked 2026-10-13); [Auction insights (Google Ads Help)](https://support.google.com/google-ads/answer/2579754?hl=en) (checked 2026-10-13); [SEL, Wenner](https://searchengineland.com/google-ads-performance-drops-recover-444357) (checked 2026-10-13)
- **Open questions:** The Lost IS (rank) and (budget) definitions page was not opened in this session.

### PRC-DIAG-011 · Lead-quality collapse: the bidder is optimising to the wrong event
- **Claim:** When reported leads hold or rise but sales say quality collapsed, the usual mechanism is that Smart Bidding or PMax is optimising toward form fills, including bots and junk, and finds cheaper inventory that produces them. The fix is to change what counts as a conversion, not to tweak bids.
- **Evidence type:** practitioner (mechanism widely reported) + documented (lead form options)
- **Confidence:** medium-high
- **How it works:** A guest piece on SEL describes a "feedback loop of doom". Bot submissions fire the conversion tag, Google treats them as successes, and it seeks more traffic like them. The fixes it lists: block bots before the tag fires (invisible reCAPTCHA or honeypot), import offline conversions from the CRM, value leads by stage, count calls only above about 60 seconds, turn off URL expansion and location expansion for local businesses, and move to PMax only once quality signals exist. Google's lead form assets offer "More volume" (fewer steps; may include "people who are less interested") and "More qualified" (more steps, fewer but more interested leads).
- **When it matters / how experts use it:** Ask for CRM outcomes by campaign, network and search term before diagnosing. Segment leads by network (search partners, Display and PMax placements) and by hour. Junk often clusters at night or on specific placements (anecdote).
- **Exceptions and failure modes:** Offline imports need volume and a short enough lag. Too few qualified events starve the bidder. A mixed approach (primary = qualified lead, with a modest value for raw leads) is common practitioner advice, but its parameters are untested here.
- **Signals in data:** Rising lead volume with falling cost per lead while the CRM close rate falls. Spikes in Display/partner or PMax non-search conversions. Duplicate or gibberish submissions.
- **Sources:** [Why Performance Max for lead generation often fails (SEL)](https://searchengineland.com/why-performance-max-lead-generation-fails-make-it-work-393038) (checked 2026-10-13); [Use lead forms in campaigns (Google Ads Help)](https://support.google.com/google-ads/answer/16726829) (checked 2026-10-13)

### PRC-DIAG-012 · The "profitable-looking" campaign that loses money: reconcile value before believing ROAS
- **Claim:** Platform ROAS can be inflated by double-counted micro-conversions, secondary goals set as primary, offline imports at pre-close value, stale value rules, gross rather than net order values, duplicate tags, and brand or returning-customer traffic that would have converted anyway. Reconciling with CRM or order data and stripping brand often turns "profitable" into loss-making.
- **Evidence type:** practitioner + study (incrementality vendor data)
- **Confidence:** medium-high (mechanisms); low for the size ranges.
- **How it works:** Sarah Stemen (SEJ, Aug 2026) says these distortions stack to an estimated 20–40% value inflation (practitioner estimate). Her example: Ads reports $400k of value against $270k of matching revenue, so a reported 380% ROAS is really 310% and the target should be reset. Uebergang's PMax "brand leak" audit (PPC Hero, Aug 2026) computes brand share of cost vs brand share of value, then the return on non-brand spend alone, which he argues is the only figure a target should be set against. ROAS also has to be compared with breakeven ROAS (1 ÷ gross margin) after returns, which no platform metric does.
- **When it matters / how experts use it:** Run this on any inherited account and any campaign "beating target". Check conversion actions (one to three revenue-linked primaries), counting settings, attribution, duplicate firing, a 90-day value-to-revenue reconciliation and a GA4 cross-check.
- **Exceptions and failure modes:** Data-driven attribution and GA4 are imperfect too. Reconciliation needs matching IDs (gclid or order ID). Some brand spend is defensive and worthwhile (PRC-DIAG-025).
- **Signals in data:** "All conv." far above "Conversions". Conversion count above order count. Brand-term share of PMax value much higher than its share of cost. Reported value above recognized revenue.
- **Sources:** [The PPC clean-up: value inflation (SEJ, Stemen)](https://www.searchenginejournal.com/the-ppc-clean-up-how-to-audit-and-fix-value-inflation-in-google-ads/583009/) (checked 2026-10-13); [The Performance Max brand leak audit (PPC Hero, Uebergang)](https://ppchero.com/?p=31522) (checked 2026-10-13); [Understand your conversion tracking data (Google Ads Help)](https://support.google.com/google-ads/answer/6270625?hl=en) (checked 2026-10-13)

### PRC-DIAG-013 · Segmentation tricks that find hidden causes
- **Claim:** The segments that most often reveal a hidden cause are device, network (Google search vs search partners vs PMax channel/ad format), geo, hour and day, match type and search term, new vs returning (audience observation), and landing page. Each corresponds to a different cause family.
- **Evidence type:** practitioner + documented (segment availability)
- **Confidence:** medium-high
- **How it works:** Device isolates mobile site problems (Wenner, Optmyzr examples). Network isolates partner traffic, which is excluded from impression share and auction insights, so a shift into partners stays invisible there. PMax search terms segmented by ad format separate Shopping from text (Uebergang). Audience segments added in Observation mode do not change reach and let you compare returning visitors with new users. Hour-of-day isolates bot or call-coverage problems.
- **When it matters / how experts use it:** When the account-level change does not appear in any single campaign, cut by these dimensions and compare both periods, for example with a pivot table.
- **Exceptions and failure modes:** Too many cuts on small data produce false positives (multiple comparisons). Under Smart Bidding, manual bid adjustments are not supported. Only a -100% device adjustment is possible, and for tCPA a device adjustment modifies the CPA target. A segment finding therefore needs a structural fix (separate campaign, exclusion, schedule, conversion definition) rather than a bid modifier.
- **Signals in data:** One segment's share of spend shifts between periods. One segment's CVR diverges.
- **Sources:** [SEL/Optmyzr](https://searchengineland.com/how-to-check-why-ppc-performance-changed-316778) (checked 2026-10-13); [Targeting vs Observation (Google Ads Help)](https://support.google.com/google-ads/answer/7365594?hl=en) (checked 2026-10-13); [PPC Hero, Uebergang](https://ppchero.com/?p=31522) (checked 2026-10-13); [Auction insights help](https://support.google.com/google-ads/answer/2579754?hl=en) (checked 2026-10-13); [About bid adjustments (Google Ads Help)](https://support.google.com/google-ads/answer/2732132?hl=en) (checked 2026-10-13)

### PRC-DIAG-014 · Like-for-like comparison windows
- **Claim:** Compare periods with the same weekday mix, equal conversion maturity, and matching holidays and promotions. Check both previous-period and year-over-year. A drop that appears in previous-period but not in year-over-year is usually seasonality.
- **Evidence type:** practitioner + documented (Explanations requires equal contiguous periods)
- **Confidence:** medium-high
- **How it works:** Day-of-week effects are strong in most accounts, and Explanations lists them explicitly as a cause. Moving holidays (Easter, Black Friday week) shift year-over-year comparisons. Conversion lag biases the most recent window (PRC-DIAG-003). Ani's ABA-therapy example: a predictable slow period from Thanksgiving to New Year, during which he avoids overbidding and raises budgets before peak season.
- **When it matters / how experts use it:** In every client report and every "did my change work?" check.
- **Exceptions and failure modes:** Year-over-year is useless when the account structure, tracking or business changed in between. Then use previous period plus a market benchmark (Trends, auction insights).
- **Signals in data:** The weekly pattern repeats. The year-over-year line tracks this year's shape.
- **Sources:** [About explanations](https://support.google.com/google-ads/answer/9000655?hl=en) (checked 2026-10-13); [SEL, Ani](https://searchengineland.com/ppc-diagnostics-low-conversions-450710) (checked 2026-10-13)

### PRC-DIAG-015 · Separating market shocks from account problems, and telling Smart Bidding about them
- **Claim:** External events (inflation, war, news, trade disputes, local events) move CPC and CVR with no account change. Experts confirm this by finding the move across many campaigns and keywords at once, with no change-history trigger, often across peer accounts too. Google provides two narrow tools to stop Smart Bidding from learning the wrong lesson: seasonality adjustments (for short, expected CVR shifts of 1–7 days, poor beyond 14) and data exclusions (for conversion-tracking outages).
- **Evidence type:** documented (tools) + practitioner (cases)
- **Confidence:** high (tools); medium (case attributions)
- **How it works:** Tabeling cites a 40% CPC decrease tied to inflation and CPI readings, and a 15% year-over-year CVR drop linked to the Ukraine war (anecdote; the causal link is the author's interpretation). Data exclusions apply to click dates, so the window has to extend back by the conversion delay. Google's example: an outage on Oct 15–18 with a 5-day delay means excluding Oct 10–18, covering at least 90% of affected clicks. Do not remove an exclusion once applied, do not use exclusions frequently, and do not backfill. Seasonality adjustments are unnecessary for routine seasonality, which Smart Bidding already models.
- **When it matters / how experts use it:** Use seasonality adjustments for flash sales. Use data exclusions immediately after a tracking break is fixed. For market shocks, usually wait rather than react, unless margins are breached.
- **Exceptions and failure modes:** Running a seasonality adjustment for a promotion that underperforms makes the bidder overspend. Exclusions covering a week or more can cause 1–2 conversion cycles of fluctuation.
- **Signals in data:** Simultaneous movement across unrelated campaigns. Peers report the same thing in forums. No triggering entries in change history.
- **Sources:** [Seasonality adjustments (Google Ads Help)](https://support.google.com/google-ads/answer/10369906?hl=en) (checked 2026-10-13); [Data exclusions (Google Ads Help)](https://support.google.com/google-ads/answer/10276486?hl=en) (checked 2026-10-13); [SEL, Tabeling](https://searchengineland.com/?p=432558) (checked 2026-10-13)

---

## B. Decision craft

### PRC-DIAG-016 · Decide whether to leave it, fix it, or test it
- **Claim:** Strong managers sort every observation into one of three buckets. **Fix now:** broken tracking, disapprovals, runaway spend, obvious errors. **Leave alone:** movement within normal variance, or a campaign in learning. **Test:** an uncertain, reversible change with meaningful upside and enough volume to read. Changing things "to justify your existence" is a recognised anti-pattern.
- **Evidence type:** practitioner
- **Confidence:** medium-high
- **How it works:** Ani's rule of thumb: avoid major changes during a dip of up to about 7 days, and treat roughly ±10% fluctuation as normal. That is a practitioner heuristic; the right band depends on volume, so compute the account's own week-to-week variance. PPCChat participants suggest waiting a day or two before changing anything unless budgets are high. Lawrence Chasse: "If it is not broken, don't fix it"; "Don't change things just to justify your existence." Chris Kostecki: "Decide on strategy periodically, optimize performance regularly, monitor spend daily."
- **When it matters / how experts use it:** On every alert. Weigh the cost of waiting (spend at risk per day) against the cost of acting on noise (the bidder recalibrates, and you lose the ability to attribute what happened; MEA-CONV-028).
- **Exceptions and failure modes:** A fixed ±10% band is too tight for low-volume campaigns (10 conversions per week varies by ±30% from Poisson noise alone) and too loose for very large ones.
- **Signals in data:** Change within the historical weekly range. Learning status active.
- **Sources:** [SEL, Ani](https://searchengineland.com/ppc-diagnostics-low-conversions-450710) (checked 2026-10-13); [PPCChat recap](https://www.karooya.com/blog/ppcchat-when-youre-doing-everything-right-performance-still-sucks/) (checked 2026-10-13)

### PRC-DIAG-017 · Google Ads custom experiments: mechanics
- **Claim:** Custom experiments split a campaign's traffic and budget, 50% recommended, between the original (control) and a treatment. On Search they use either a cookie-based split (each user sees one arm; recommended) or a search-based split (per query; faster significance, but users can see both arms). Display always uses cookies. You can schedule up to 5 experiments per campaign but run only one at a time. At the end, you apply the treatment to the original or convert it to a new campaign.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Custom experiments are supported for Search, Display, Video and Hotel. Shopping and App are not supported (App has its own asset experiments). For audience-list cookie splits, Google recommends at least 10,000 users. Schedule a future start so ads clear review before the test begins.
- **When it matters / how experts use it:** Use them to test bid strategies, match-type changes, landing pages and settings where a before/after comparison would be confounded by seasonality.
- **Exceptions and failure modes:** A search-based split leaks users between arms, which matters for remarketing and frequency effects. A 50/50 split halves each arm's data, which slows Smart Bidding learning in both arms.
- **Signals in data:** The experiment's scorecard; treatment and control spend should track the split percentage.
- **Sources:** [About custom experiments (Google Ads Help)](https://support.google.com/google-ads/answer/6261395?hl=en) (checked 2026-10-13)

### PRC-DIAG-018 · Experiments' statistical limits: the 80% default and short windows
- **Claim:** Google's experiment scorecard uses an **80% confidence interval by default** (adjustable). It marks significant results with a blue asterisk and recommends running 2–3 weeks. At 80% confidence, a meaningful share of "winners" will be noise, especially when several metrics are checked or results are read repeatedly. With conversion lag and the learning period, the first week or more of a bid-strategy test is contaminated.
- **Evidence type:** documented (defaults) + inference (false-positive implications) + practitioner
- **Confidence:** high (defaults); medium (the practical implications)
- **How it works:** An 80% interval means roughly 1 in 5 null effects would look "different" on a given metric. Checking cost, conversions, CPA and value multiplies that. Rémi Kerhoas (SEL) argues that significance shows a difference, not durability. He gives an example: at a 5% CVR with 7,000 weekly visitors, a lift to 6.5% can be detected in under 8 days, which is shorter than a full customer journey. Tests have to run long enough for cohorts to finish converting, which is especially hard in B2B. Haus's brand-search findings also use an 80%-probability threshold, which is less strict than the conventional 95%.
- **When it matters / how experts use it:** Set the confidence level to 95% for consequential decisions. Pre-register the primary metric (usually profit, CPA or ROAS) and a fixed duration that covers learning plus lag. Discard the learning-period days. Require practical as well as statistical significance.
- **Exceptions and failure modes:** In low-volume accounts, a 95% threshold may never be reached. Use longer tests, larger effect hypotheses, or decide under explicit uncertainty. A/A test practice is discussed by practitioners, but no credible A/A results were opened in this session.
- **Signals in data:** "No clear winner" after 3 weeks means the effect is smaller than detectable. A winner whose interval nearly touches zero.
- **Sources:** [Monitor your experiments (Google Ads Help)](https://support.google.com/google-ads/answer/6318747?hl=en) (checked 2026-10-13); [A/B testing mistakes in PPC (SEL, Kerhoas)](https://searchengineland.com/a-b-testing-mistakes-ppc-436695) (checked 2026-10-13); [Haus: when is branded search worth it](https://www.haus.io/blog/when-is-branded-search-worth-the-investment) (checked 2026-10-13)

### PRC-DIAG-019 · Ad variations: for one change across many campaigns
- **Claim:** Ad variations test a single text change (for example a headline swap) across RSAs account-wide, in specific campaigns or in a custom scope, with a chosen traffic percentage. Google positions them for one change at scale, and custom experiments for several changes at smaller scale.
- **Evidence type:** documented
- **Confidence:** high (mechanics); low (statistical rigor, since the Help page does not describe significance reporting).
- **How it works:** You define the change, scope, split and end date. Results compare modified ads with originals, and winners can be applied by replacing existing ads or adding new ones.
- **When it matters / how experts use it:** Test a sitewide offer, price mention or CTA by pooling volume across low-traffic ad groups that could never reach significance alone.
- **Exceptions and failure modes:** RSA asset combinations and Google's serving choices confound text tests, and CTR wins may not be CVR wins. Judge on conversions per impression, not CTR. That is a long-standing practitioner position (associated with Martin Roettgerding and others); his slides could not be opened this session.
- **Signals in data:** The variation report's conversion and CTR differences, with their intervals.
- **Sources:** [About ad variations (Google Ads Help)](https://support.google.com/google-ads/answer/7438541?hl=en) (checked 2026-10-13)

### PRC-DIAG-020 · One change at a time, and give the bidder time to learn
- **Claim:** Bid strategy changes, target changes, and adding or removing campaigns, ad groups or keywords from a strategy all trigger a learning period. Learning typically takes 1–2 conversion cycles, and Google says the algorithm keeps learning after the status clears. Stacking changes makes outcomes unattributable and keeps the bidder recalibrating.
- **Evidence type:** documented (learning triggers) + practitioner (staging cadence)
- **Confidence:** high (triggers); medium (cadence)
- **How it works:** Learning-period length depends on conversion volume, conversion-cycle length and strategy type; Manual CPC has none. A secondary source (TechWyse, Sept 2026) reports Google's docs now say calibration can take "up to around 50 conversion events or three conversion cycles" (changed 2026-09; Google's exact wording not verified). Stemen's practitioner cadence: move tROAS or tCPA by 15–20% every 5–7 days, then hold at least 2 weeks before the next change.
- **When it matters / how experts use it:** Space changes and log each one. Make target changes in steps rather than jumps. Do not judge a strategy switch until at least one or two full conversion cycles plus lag have passed.
- **Exceptions and failure modes:** If something is broken (tracking, a catastrophic target typo), fix it immediately whatever the learning status. In very high-volume accounts, learning completes fast and staging can be quicker.
- **Signals in data:** Status "Learning (strategy change / composition change)". Volatile CPA for 1–2 weeks after a change.
- **Sources:** [Duration of the learning period (Google Ads Help)](https://support.google.com/google-ads/answer/13020501) (checked 2026-10-13); [Google Ads updates Smart Bidding documentation with 50-conversion benchmark (TechWyse)](https://www.techwyse.com/news/platform-updates/google-ads-smart-bidding-learning-period-50-conversions) (checked 2026-10-13); [SEJ, Stemen](https://www.searchenginejournal.com/the-ppc-clean-up-how-to-audit-and-fix-value-inflation-in-google-ads/583009/) (checked 2026-10-13)

### PRC-DIAG-021 · When "always use exact" and "broad always wastes money" are wrong
- **Claim:** Neither holds universally. Across 2,637 accounts that used both match types (Optmyzr, Q1 2023), exact won on CPA in about 71% of accounts, but broad won in about 27%. In the 2026 study (30,000 accounts, Feb 2026), exact leads efficiency on average, phrase has the highest CVR in e-commerce, and phrase dominates lead gen. Broad does best where Smart Bidding has rich signals (conversion value, strong volume) and negatives are maintained.
- **Evidence type:** study (vendor, observational)
- **Confidence:** medium
- **How it works:** Broad adds query discovery, and Smart Bidding can price each query. Without good conversion signals it buys loosely related queries at full price. Exact keywords are usually the proven winners, which is selection bias, so within-account comparisons flatter exact.
- **When it matters / how experts use it:** Test broad through a custom experiment when the account has strong, clean conversion signals (especially value-based) and budget headroom. Keep exact or phrase for high-value core terms and for brand, where the 2026 data favours exact.
- **Exceptions and failure modes:** In lead gen without quality feedback, broad degrades more (2026 study). Low-volume accounts fall within the 71%. The studies are correlational and come from an automation vendor whose users are more advanced than average.
- **Signals in data:** Broad's search terms include many converting queries absent from the exact list = discovery value. Broad's terms mostly duplicate exact ones at higher CPC = cannibalisation.
- **Sources:** [Optmyzr study: broad match and bidding (Hopkins, 2023)](https://optmyzr.com/blog/optmyzr-study-broad-match-bidding) (checked 2026-10-13); [Google Ads match type performance (Vallaeys, 2026)](https://www.optmyzr.com/blog/google-ads-match-type-performance/) (checked 2026-10-13)

### PRC-DIAG-022 · "Quality Score must be high" confuses a diagnostic with the target
- **Claim:** Google says "Quality Score is not an input in the ad auction". It is a diagnostic: a 1–10 aggregate of expected CTR, ad relevance and landing-page experience, each compared with other advertisers shown on the same search over 90 days. Underlying real-time quality does affect ad rank and CPC, but chasing the displayed number can destroy profit.
- **Evidence type:** documented + study
- **Confidence:** high
- **How it works:** Improve the components where they reveal a real problem, such as a "Below average" landing-page experience on a high-spend keyword. Ghose & Yang (NYU, 2009) found that a one-unit rise in landing-page quality score was associated with up to 22.5% higher conversion rates and lower CPC. That is observational, from one retailer.
- **When it matters / how experts use it:** Prioritise quality work by spend × component gap, not by the lowest QS. Accept low QS on competitor terms and loosely relevant but profitable terms.
- **Exceptions and failure modes:** Copy that maximises CTR (curiosity bait, no price) can raise expected CTR while cutting CVR. A low QS on a profitable keyword is fine. QS is undefined or meaningless for low-volume keywords and absent in PMax.
- **Signals in data:** QS components by keyword weighted by cost. CPC vs QS within an ad group.
- **Sources:** [About Quality Score (Google Ads Help)](https://support.google.com/google-ads/answer/6167118?hl=en) (checked 2026-10-13); [NYU Stern: top positions not always most profitable (Ghose & Yang)](https://www.stern.nyu.edu/experience-stern/news/uat_024897) (checked 2026-10-13)

### PRC-DIAG-023 · "Consolidate everything" fails when segments differ in value, objective, geography or funnel stage
- **Claim:** Consolidation helps Smart Bidding by pooling conversions. Practitioners suggest about 30 or more conversions a month per campaign as a working level, which is a practitioner figure, not a platform rule. Over-consolidation hurts when merged segments differ in margin, objective (lead vs sale), strategic geography or funnel intent, and mixing brand with non-brand muddies signals.
- **Evidence type:** practitioner
- **Confidence:** medium
- **How it works:** Stemen (SEJ, Oct 2026): 60 monthly conversions split across 12 campaigns leaves about 5 each, too few for reliable bidding. Merging high- and low-margin products pushes the bidder to an average target that underserves both. Her test: if a split changes strategy, budget or creative experience, keep it separate. If it only relabels identical journeys, consolidate.
- **When it matters / how experts use it:** When restructuring inherited SKAG or device-split accounts, and when deciding whether to split brand or high-margin lines into their own campaigns with their own targets.
- **Exceptions and failure modes:** Very high-volume accounts can afford granular splits. Portfolio strategies and shared budgets partly get around the trade-off.
- **Signals in data:** Many campaigns under about 10–30 conversions a month with volatile CPA. Merged campaigns where one product line takes all the spend.
- **Sources:** [Why legacy PPC account structures are sabotaging Smart Bidding (SEJ, Stemen)](https://searchenginejournal.com/why-legacy-ppc-account-structures-are-sabotaging-your-smart-bidding-strategy/588832) (checked 2026-10-13)

### PRC-DIAG-024 · "Raise bids to get top position" is usually wrong outside brand defence
- **Claim:** For the same ad, conversion rate barely changes with position: less than 5% variation across positions in Google's 2009 analysis. Higher positions mainly buy more clicks at a higher marginal CPC. Ghose & Yang found profits were often lower at the top than in middle positions. The exception is brand terms, where position has strong causal effects on who captures the click (PRC-DIAG-025).
- **Evidence type:** study (old: 2009, pre-2019 SERP layout)
- **Confidence:** medium (direction robust; magnitudes dated)
- **How it works:** The marginal clicks gained by moving up cost the full incremental CPC on all clicks, not just the extra ones. Profit is maximised where marginal cost per click equals marginal value per click, which is usually below the top. Smart Bidding approximates this per auction.
- **When it matters / how experts use it:** Push back on clients who want "#1 always". Use target impression share (absolute top) only for brand defence or deliberate visibility goals, with a max CPC cap.
- **Exceptions and failure modes:** Today's SERPs (AI Overviews, Shopping units, only 4 top ads) may make lower positions much less visible than in 2009, so the position-to-CTR curve may be steeper now. Not re-measured publicly in sources opened here.
- **Signals in data:** Absolute-top impression rate rising with CPA rising faster than conversions. Absolute top vs other segments in the "Top vs Other" report.
- **Sources:** [Conversion rates don't vary much with ad position (Inside AdWords, 2009)](https://adwords.googleblog.com/2009/08/conversion-rates-dont-vary-much-with-ad.html?m=0) (checked 2026-10-13); [NYU Stern, Ghose & Yang](https://www.stern.nyu.edu/experience-stern/news/uat_024897) (checked 2026-10-13)

### PRC-DIAG-025 · "Never bid on brand" and "always bid on brand" are both wrong; it depends on the competition in the auction
- **Claim:** Brand-ad incrementality ranges from near zero to strongly positive, depending mainly on whether competitors, resellers or marketplaces would take the click. The eBay field experiment found "no measurable short-term benefits" from brand ads. Bing experiments (Simonov, Nosko, Rao) found only a 1–4% click lift with no competitors present, but competitors capture 18–42% of brand-search clicks when the brand does not advertise. Haus's test data found significant lift for 82% of brands facing high competition vs 35% facing low competition.
- **Evidence type:** study (academic field experiments + vendor geo tests)
- **Confidence:** high (that it is conditional); medium (specific magnitudes for any given brand)
- **How it works:** When you rank first organically and no one else bids, your ad mostly takes clicks you would have got for free. Google's 2012 research found only 50% of ad clicks were incremental when the advertiser's organic result was rank 1, versus 96% at organic rank 5 or below (and 89% across all pause studies, 2011). When rivals bid, your absence hands them the top slot, and position effects divert traffic. Haus also found brand-search lift 1.7× higher among new customers, and that brand ads can shift sales from Amazon to DTC (−1.9% Amazon, +3.1% DTC on average).
- **When it matters / how experts use it:** Check auction insights on brand campaigns. Haus's "high competition" means 3 or more competitors with more than 50% combined impression share. Check the organic SERP, marketplace and reseller presence, and Search Console brand clicks. Defend at a bid level justified by incremental ROAS, not "position 1 at any price". Separate existing customers.
- **Exceptions and failure modes:** Google's 89% and 50% figures are Google-authored and from 2011–12. eBay is an exceptionally strong brand. Haus tests are short (median 14 days), use an 80% threshold, and come from a vendor.
- **Signals in data:** Competitors appearing in brand auction insights. Brand CPCs rising. Brand ROAS "too good" (likely non-incremental).
- **Sources:** [Consumer heterogeneity and paid search effectiveness (NBER, Blake/Nosko/Tadelis)](https://www.nber.org/papers/w20171) (checked 2026-10-13); [Competition and crowd-out for brand keywords (IDEAS abstract, Simonov/Nosko/Rao)](https://ideas.repec.org/a/inm/ormksc/v37y2018i2p200-215.html) (checked 2026-10-13); [Incremental clicks impact of search advertising (Google Research, 2011)](https://research.google/pubs/incremental-clicks-impact-of-search-advertising/) (checked 2026-10-13); [Impact of organic ranking on ad click incrementality (Google Research blog, 2012)](https://www.research.google/blog/impact-of-organic-ranking-on-ad-click-incrementality/) (checked 2026-10-13); [When is branded search worth the investment? (Haus, 2025)](https://www.haus.io/blog/when-is-branded-search-worth-the-investment) (checked 2026-10-13)

---

## C. Less common strategies and overlooked opportunities

### PRC-DIAG-026 · Competitor conquesting: expect many "confusion clicks"; it works best for credible alternatives
- **Claim:** In Bing randomized experiments (Simonov & Hill), 46% of users who clicked a competitor's ad on a brand query returned to Bing within 30 seconds, versus 3.5–6% for the brand's own link. That points to confused or mismatched clicks. More relevant competitors earned more clicks with fewer quick returns. A Chicago Booth summary of the Simonov/Nosko/Rao work says a smaller brand can capture about 20% of a rival's traffic by taking the top paid slot on its name.
- **Evidence type:** study (platform-run randomized experiments)
- **Confidence:** medium-high
- **How it works:** Searchers on a brand query mostly want that brand. Only those open to alternatives convert. Conquest ads therefore pay high CPCs (low relevance, low QS) for a small qualified slice.
- **When it matters / how experts use it:** Conquest when you are a credible substitute (cheaper, better rated, switching offer). Use explicit comparison copy and landing pages. Judge on downstream conversions and profit, not CTR. Cap bids, and expect retaliation (the rival bidding on your brand raises your brand CPC).
- **Exceptions and failure modes:** Trademark policy limits using rival names in ad text in many regions (not researched here). Conquesting a much stronger brand mostly buys bounces.
- **Signals in data:** Very low CVR, a high quick-bounce rate in analytics, below-average expected CTR and ad relevance on conquest terms.
- **Sources:** [Competitive advertising on brand search: traffic stealing and customer selection (Microsoft Research, Simonov & Hill)](https://www.microsoft.com/en-us/research/?p=627741) (checked 2026-10-13); [Why smaller brands beat their big rivals on search ads (Chicago Booth Review)](https://www.chicagobooth.edu/review/why-smaller-brands-beat-their-big-rivals-on-search-ads) (checked 2026-10-13)

### PRC-DIAG-027 · Measuring brand defence: geo holdouts with omnichannel outcomes
- **Claim:** The credible way to value brand search is a geo holdout: brand ads paused in a random share of regions (often 30–50%) for at least 2 weeks. The outcome should be total business (DTC plus marketplace plus retail), not platform conversions. Pausing everywhere and watching totals is confounded by seasonality.
- **Evidence type:** study (vendor case studies) + practitioner
- **Confidence:** medium
- **How it works:** Orthofeet (Haus, 70/30 split, 2 weeks): +1.36% DTC lift, but Amazon fell 2.7% in treatment regions, so omnichannel lift was only 0.26% at an iROAS below $1. Amazon bid on "Orthofeet" in the holdout regions, which the authors read as a margin-defence argument. Bose paused brand search in about half of US markets in 2025 (results not published). Uebergang suggests a cheaper proxy: compare Search Console brand clicks with paid brand clicks. Flat total brand search with rising paid brand clicks suggests cannibalisation.
- **When it matters / how experts use it:** For brands spending heavily on brand terms, or where clients question brand spend. Fix the measurement window in advance.
- **Exceptions and failure modes:** Small brands lack the volume for geo tests. Two-week tests miss delayed effects (Haus: just under 10% further lift appeared in post-treatment windows). Vendor case studies lack confidence intervals.
- **Signals in data:** Brand impression share near 100% with no competitors in auction insights is the strongest case for a test.
- **Sources:** [The Amazon curveball in Orthofeet's brand search test (Haus)](https://www.haus.io/customer/orthofeet) (checked 2026-10-13); [Bose pauses ads to find out (ContentGrip)](https://contentgrip.com/bose-tests-paid-search) (checked 2026-10-13); [PPC Hero, Uebergang](https://ppchero.com/?p=31522) (checked 2026-10-13); [Haus, branded search](https://www.haus.io/blog/when-is-branded-search-worth-the-investment) (checked 2026-10-13)

### PRC-DIAG-028 · PMax brand leak: measure the brand share, then decide; exclusion is not always right
- **Claim:** PMax tends to collect warm, branded, bottom-funnel traffic that inflates its reported ROAS and can subsidise weak non-brand spend. Experts measure brand share of PMax cost and value from search terms (regex-classified), then test exclusion. Haus geo tests found excluding brand produced 24% more incremental revenue on average and 19–60% lower new-customer CAC. Excluding won in only 50% of experiments, though, and brands with AOV above $238 did better including brand.
- **Evidence type:** study (vendor geo tests) + practitioner
- **Confidence:** medium
- **How it works:** Nils Rooijmans' script charts brand vs non-brand share of PMax over time. His example showed the brand share jumping when Google auto-added assets and falling when they were removed. Uebergang notes the search terms report covers only Search and Shopping, not Display, YouTube or Discover. Caraway (Haus) counterexample: PMax including brand produced 1.95× the total revenue and 1.75× the new-customer revenue of PMax excluding brand, though the platform overstated PMax-with-brand by 33%.
- **When it matters / how experts use it:** Use it whenever PMax ROAS looks far better than Search non-brand. Launch a dedicated brand campaign before applying brand exclusions. Measure total account outcomes over at least 4 weeks.
- **Exceptions and failure modes:** Where competitors bid on your brand, PMax's brand coverage may be doing real defence. The results depend on KPI (new customers vs revenue) and AOV.
- **Signals in data:** Brand share of PMax value far above its share of cost. PMax ROAS falls sharply after a brand exclusion while account revenue holds, which means it was taking credit.
- **Sources:** [PMax experiments: including vs excluding branded search terms (Haus, 2024)](https://www.haus.io/blog/pmax-experiments-including-excluding-branded-search-terms) (checked 2026-10-13); [PMax brand traffic analyzer script (Nils Rooijmans)](https://nilsrooijmans.com/daily/google-ads-script-pmax-brand-traffic-analyzer) (checked 2026-10-13); [PPC Hero, Uebergang](https://ppchero.com/?p=31522) (checked 2026-10-13)

### PRC-DIAG-029 · Schedule ads to the business's capacity, not only to conversion data
- **Claim:** For call- and appointment-driven businesses, the value of a click depends on whether someone can answer or act on it. Practitioners schedule call assets and call-heavy campaigns to staffed hours, and judge after-hours performance on booked or answered outcomes rather than raw calls or forms.
- **Evidence type:** practitioner / inference (mechanism partly documented)
- **Confidence:** low-medium (no opened quantitative case)
- **How it works:** An unanswered call can still register as a conversion if the conversion is defined by any call. Bidding then rewards hours that produce no business. Counting only calls above a duration threshold (the SEL PMax lead-gen piece suggests 60 seconds) partly corrects this. Capacity limits (a fully booked plumber) also mean extra leads have zero marginal value, so reduce spend rather than chase volume.
- **When it matters / how experts use it:** Local services, legal and medical. Ask the client about staffing hours, missed-call rate and booking capacity before designing the schedule.
- **Exceptions and failure modes:** Forms submitted after hours can convert well if followed up quickly. Under Smart Bidding, ad-schedule *bid adjustments* are not used, but ads "strictly follow" the ad schedule itself. Smart Bidding already uses day-of-week and time-of-day as signals, but it cannot see staffing or capacity, so use schedule exclusions or tighter conversion definitions (documented).
- **Signals in data:** The hour-of-day segment shows call conversions outside staffed hours. Call reports with short or unanswered calls cluster at night or weekends.
- **Sources:** [Why Performance Max for lead generation often fails (SEL)](https://searchengineland.com/why-performance-max-lead-generation-fails-make-it-work-393038) (checked 2026-10-13); [About bid adjustments (Google Ads Help)](https://support.google.com/google-ads/answer/2732132?hl=en) (checked 2026-10-13); [About Smart Bidding signals (Google Ads Help)](https://support.google.com/google-ads/answer/7065882?hl=en) (checked 2026-10-13)
- **Open questions:** No published, numbers-backed case was found in the time available.

### PRC-DIAG-030 · Calls and lead forms: call ads are being retired; choose between friction and volume deliberately
- **Claim:** New call ads (call-only) can no longer be created as of February 2026, and existing call ads stop serving in February 2027. Google directs advertisers to call assets on RSAs **(changed 2026-02)**. For lead form assets, "More volume" (fewer steps) vs "More qualified" (more steps) is an explicit quality-volume dial.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Call assets keep a website click path alongside the phone number, so the call-vs-click mix is now partly decided by Google and the user. Lead forms reduce friction, which raises volume and, per Google's own description, may lower intent.
- **When it matters / how experts use it:** Migrate call-only campaigns before February 2027. Track call duration and quality. Start lead forms on "More qualified" when sales capacity is the constraint, and on "More volume" when the backend can filter.
- **Exceptions and failure modes:** The relative performance of lead forms vs landing pages varies by niche. No credible numbers were opened this session.
- **Signals in data:** Call ads disappearing from reports. Lead-form leads with low contact rates.
- **Sources:** [About call ads (Google Ads Help)](https://support.google.com/google-ads/answer/6341403?hl=en) (checked 2026-10-13); [Use lead forms in campaigns (Google Ads Help)](https://support.google.com/google-ads/answer/16726829) (checked 2026-10-13)

### PRC-DIAG-031 · Putting price in ads to filter unqualified clicks
- **Claim:** Practitioners often report that showing price ("from $X", "plans start at $Y/mo") in ad text or price assets lowers CTR but raises CVR and lead quality, because price-sensitive or mismatched searchers self-select out before paying for a click.
- **Evidence type:** hypothesis / practitioner (anecdotal; no controlled public study opened)
- **Confidence:** low
- **How it works:** It is a pre-click filter, much like stating minimums ("projects from $10k") in B2B. Lower expected CTR can slightly worsen ad rank, so the net effect depends on how much wasted click spend is removed.
- **When it matters / how experts use it:** Use it for high-ticket or premium offers where cheap-seekers waste budget, and for businesses with minimum order sizes. Test with ad variations (PRC-DIAG-019), judged on conversions or qualified leads per impression, not CTR.
- **Exceptions and failure modes:** When you are the low-price option, price raises CTR and volume. When competitors show lower prices, it can drain all traffic.
- **Signals in data:** High CTR with poor lead quality and many "too expensive" disqualifications in the CRM.
- **Sources:** No opened source this session. Treat this as a hypothesis to test.

### PRC-DIAG-032 · Geo-tiering and tight local radii
- **Claim:** Geography often hides very different economics (close rate, ticket size, competition, travel cost). Practitioners split strategically different regions into separate campaigns or tiers with their own targets and budgets. For local services, they turn off location expansion and use about a 30–45 minute drive radius.
- **Evidence type:** practitioner
- **Confidence:** medium-low
- **How it works:** A single tCPA across geos lets the bidder spend where conversions are cheapest, not most profitable. Separating tiers lets the targets reflect value. Stemen lists "strategic geography" (dedicated budgets, localisation) as a valid reason not to consolidate. The SEL PMax lead-gen piece recommends turning off location expansion and the drive-time radius for local businesses.
- **When it matters / how experts use it:** Service-area businesses, multi-location brands, and national advertisers with regional margin differences. The default location option is "Presence or Interest", which also reaches people who have only shown interest in the area. For local services that need the customer on-site, consider "Presence" and check user-location reports for leakage.
- **Exceptions and failure modes:** Splitting too finely starves Smart Bidding of data (PRC-DIAG-023). With value-based bidding and accurate lead values by geo, a single campaign can handle tiers.
- **Signals in data:** Geo report with conversions from outside the service area. CPA or close-rate differences above about 2× between regions.
- **Sources:** [SEJ, Stemen (structures)](https://searchenginejournal.com/why-legacy-ppc-account-structures-are-sabotaging-your-smart-bidding-strategy/588832) (checked 2026-10-13); [SEL PMax lead gen](https://searchengineland.com/why-performance-max-lead-generation-fails-make-it-work-393038) (checked 2026-10-13); [Location targeting options (Google Ads Help)](https://support.google.com/google-ads/answer/1722038?hl=en) (checked 2026-10-13)

### PRC-DIAG-033 · Audience layering on Search (RLSA): observe first; separate existing customers when they distort targets
- **Claim:** Audience segments added in Observation mode do not change reach. They give segment-level reporting and act as Smart Bidding signals. When returning or existing customers convert far better, mixing them into one target inflates bids for new-customer traffic or hides weak acquisition. Haus advises putting existing customers in their own brand campaign, and found brand-search lift 1.7× higher for new customers.
- **Evidence type:** documented (Observation) + study (Haus)
- **Confidence:** medium
- **How it works:** Use Observation to compare segments. Use Targeting (narrowing) only for dedicated RLSA campaigns, for example bidding on broad generic terms only for past visitors, where the generic term is unprofitable for strangers. That last tactic is classic practitioner advice and not re-verified with data this session.
- **When it matters / how experts use it:** Use it in any account with a large returning-customer base, and for subscription or repeat-purchase businesses where new-customer acquisition is the real goal.
- **Exceptions and failure modes:** List-size and privacy thresholds limit small advertisers. Third-party cookie and consent changes shrink lists.
- **Signals in data:** CVR by audience segment differs several-fold. Customer-match or remarketing lists dominate conversions.
- **Sources:** [Targeting vs Observation (Google Ads Help)](https://support.google.com/google-ads/answer/7365594?hl=en) (checked 2026-10-13); [Haus, branded search](https://www.haus.io/blog/when-is-branded-search-worth-the-investment) (checked 2026-10-13)

### PRC-DIAG-034 · Microsoft Ads import: cheap incremental volume, but imported settings need auditing
- **Claim:** Practitioners commonly import Google campaigns into Microsoft Advertising as a low-effort way to add incremental volume. The common pitfalls they report are carried-over settings that do not fit Microsoft's audience and network: partner network defaults, bid strategies needing more conversion volume than Microsoft provides, and location or ad-schedule settings, plus scheduled re-imports overwriting manual Microsoft edits.
- **Evidence type:** hypothesis (practitioner lore; Microsoft documentation could not be opened this session)
- **Confidence:** low
- **How it works:** Microsoft volume is typically a fraction of Google's, so Smart Bidding signals are thinner. Syndicated or partner traffic quality differs.
- **When it matters / how experts use it:** When a Google account is capped by demand rather than budget. Audit network, location and bid settings after import, and decide whether scheduled imports may overwrite Microsoft-specific changes.
- **Exceptions and failure modes:** Not verified. Do not cite as fact.
- **Signals in data:** Microsoft CPA very different from Google's on the same keywords. High partner-network share.
- **Sources:** None opened (fetch budget exhausted). Research again before relying on it.

### PRC-DIAG-035 · Search partners and PMax channels are blind spots in standard diagnostics
- **Claim:** Impression share and auction insights exclude search partners, and the PMax search terms report excludes Display, YouTube and Discover. Spend that shifts into these surfaces can drive a CPA or lead-quality change that standard IS and auction diagnostics will not show.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Search partners "aren't split into top and others" and are excluded from IS. PMax auction insights cover Search and Shopping only.
- **When it matters / how experts use it:** When CPA or lead quality changes with no visible change in auction insights, segment by network (Search campaigns) and use channel-level PMax reporting and placement data.
- **Exceptions and failure modes:** Partner traffic is sometimes good. Judge on downstream quality, not on principle.
- **Signals in data:** Network segment shows a rising partner share. PMax spend rising in non-search channels.
- **Sources:** [Auction insights (Google Ads Help)](https://support.google.com/google-ads/answer/2579754?hl=en) (checked 2026-10-13); [About impression share](https://support.google.com/google-ads/answer/2497703?hl=en) (checked 2026-10-13); [PPC Hero, Uebergang](https://ppchero.com/?p=31522) (checked 2026-10-13)

---

## D. Case studies with numbers

### PRC-DIAG-036 · Case: three brand-search holdouts lead a brand to switch brand search off (Haus)
- **Claim:** Situation: a brand spending heavily on Google brand search wanted to know whether it drove incremental activations. Investigation: three 2-week GeoLift holdouts: US slow season (70/30), US peak season (70/30), and new launch markets (60/40). Result: about 1% lift at a "highly inefficient" CPA in the slow season, and no lift at peak or in new markets. Action: brand search turned off and budget moved to other channels. Caveat: a vendor case study with no disclosed CPA, spend or confidence intervals, and short tests. This brand apparently had little competitor pressure. Contrast PRC-DIAG-025.
- **Evidence type:** study (vendor case study)
- **Confidence:** medium-low
- **How it works:** No competitor capture plus strong organic rank leaves brand ads with little to add.
- **When it matters / how experts use it:** As a template for test design: test in more than one season and include new markets.
- **Exceptions and failure modes:** Brands with competitors or resellers on their terms would likely see a different result.
- **Signals in data:** Brand auction insights with few or no competitors.
- **Sources:** [A series of three incrementality tests prove brand search to be ineffective (Haus)](https://haus.io/case-study/a-series-of-3-incrementality-tests-prove-brand-search-to-be-ineffective) (checked 2026-10-13)

### PRC-DIAG-037 · Case: Orthofeet brand test, where measuring only DTC would have given a false positive
- **Claim:** Situation: a footwear brand selling via Shopify and Amazon. Investigation: a 2-week geo test, brand search on in 70% of US regions and paused in 30%. Result: DTC +1.36% at an iROAS above $1, Amazon −2.7%, omnichannel +0.26% at an iROAS below $1. Interpretation: Amazon bid on the brand in the holdout regions, so brand search protects DTC margin and customer relationships rather than total sales. Caveat: single short test, no intervals, vendor-published, mechanism inferred.
- **Evidence type:** study (vendor case study)
- **Confidence:** medium-low
- **How it works:** Channel substitution. Paid brand ads move buyers between your own channels.
- **When it matters / how experts use it:** Always include marketplace and retail outcomes when testing brand or upper-funnel search. Value the DTC shift by margin difference.
- **Exceptions and failure modes:** Brands without marketplace presence will not see this effect.
- **Signals in data:** Amazon or marketplace advertisers in brand auction insights.
- **Sources:** [The Amazon curveball in Orthofeet's brand search test (Haus)](https://www.haus.io/customer/orthofeet) (checked 2026-10-13)

### PRC-DIAG-038 · Case: value reconciliation turns 380% ROAS into 310% (illustrative audit)
- **Claim:** Situation: an account bidding on tROAS with stacked conversion actions. Investigation: 90-day reconciliation of Ads conversion value against CRM or order revenue by conversion action. Result: $400k reported vs $270k recognized, and a true blended ROAS of 310% vs a reported 380%. Action: remove double counting, demote micro-conversions to secondary, then reset the target in steps of 15–20% every 5–7 days and hold 2 weeks. Caveat: presented as an example in a practitioner article, not a documented client case with before/after outcomes.
- **Evidence type:** practitioner (illustrative)
- **Confidence:** medium-low (numbers); high (that the method is sound)
- **How it works:** Smart Bidding "optimizes toward whatever value you feed it", so inflated values raise bids on traffic that is not actually profitable.
- **When it matters / how experts use it:** Run it as a standard first step on account takeover.
- **Exceptions and failure modes:** Lagging CRM revenue (long sales cycles) can make reconciliation look worse than reality. Match on cohorts.
- **Signals in data:** Reported value consistently above booked revenue.
- **Sources:** [SEJ, Stemen](https://www.searchenginejournal.com/the-ppc-clean-up-how-to-audit-and-fix-value-inflation-in-google-ads/583009/) (checked 2026-10-13)

### PRC-DIAG-039 · Case: brand ads at eBay, with no measurable short-term benefit
- **Claim:** Situation: eBay was spending on brand-keyword ads. Investigation: large-scale field experiments switching ads off. Result: brand ads had "no measurable short-term benefits", and on non-brand terms most spend went to frequent users whose purchases the ads did not change, so average returns were negative. Only new and infrequent users responded. Caveat: eBay is an outlier brand with dominant organic presence (a secondary source reports that about 99.5% of traffic was retained via organic links). The results are short-term.
- **Evidence type:** study (peer-reviewed field experiment)
- **Confidence:** high (for eBay-like conditions)
- **How it works:** Where organic rank is high and searchers are loyal, paid clicks substitute for organic ones.
- **When it matters / how experts use it:** As the canonical evidence that platform ROAS overstates incrementality, especially for returning and loyal customers. It motivates new-vs-returning segmentation.
- **Exceptions and failure modes:** Smaller brands with competitor pressure (PRC-DIAG-025/037).
- **Signals in data:** Very high brand ROAS, mostly returning customers.
- **Sources:** [Consumer heterogeneity and paid search effectiveness (NBER)](https://www.nber.org/papers/w20171) (checked 2026-10-13); [ContentGrip (secondary, the 99.5% figure)](https://contentgrip.com/bose-tests-paid-search) (checked 2026-10-13)

### PRC-DIAG-040 · Case: external shocks and operational incidents from one agency's book (Tabeling)
- **Claim:** Four anecdotes with numbers from one agency head. (1) A hacked account spent $100,000 overnight. (2) An undisclosed holiday spend spike triggered an account suspension and about $150,000 of lost sales. (3) A client's CPC fell 40% in connection with inflation and CPI moves. (4) A client's CVR fell 15% year over year, linked to the war in Ukraine. Investigation pattern: change history, then development changes, then competitors, then seasonality, then external events. Caveat: anecdotes. The causal links in (3) and (4) are the author's interpretation.
- **Evidence type:** practitioner (anecdote)
- **Confidence:** medium (that such events happen); low (causal attributions)
- **How it works:** Security and policy incidents are a real operational risk. Macro shocks move auctions without account changes.
- **When it matters / how experts use it:** Security hygiene (2FA, individual logins). Pre-warn Google reps about planned spend surges. Do not "optimise" in response to macro moves you cannot control.
- **Exceptions and failure modes:** n/a
- **Signals in data:** Overnight spend with no human changes. Account-wide CPC or CVR moves with no change-history triggers.
- **Sources:** [What to do when performance tanks in PPC (SEL, Tabeling)](https://searchengineland.com/?p=432558) (checked 2026-10-13)

---

## Common mistakes and misleading metrics

- **Judging the last 7 days.** Conversions are reported on the click date, so recent periods are always under-converted (PRC-DIAG-003).
- **Diagnosing before verifying tracking.** A fall to zero, or by an exact fraction, means a tag problem, not a market one (PRC-DIAG-002).
- **Treating platform ROAS or CPA as profit.** Inflated values, micro-conversions, view-throughs in "All conv.", gross revenue, and non-incremental brand or returning-customer conversions all flatter it (PRC-DIAG-012, 025).
- **Reading average CPC or CTR as if the traffic mix were constant.** Mix shifts (new broad terms, partners, devices) move averages with no change in any individual unit (PRC-DIAG-001, 007).
- **Chasing Quality Score, impression share or absolute-top position as goals.** They are diagnostics or means, not profit (PRC-DIAG-010, 022, 024).
- **Over-trusting experiment "winners".** The default 80% confidence, multiple metrics, peeking, and learning-period contamination all inflate false positives (PRC-DIAG-018).
- **Stacking changes.** Several simultaneous edits make the bidder recalibrate on a mix of causes and make attribution impossible (PRC-DIAG-020). Target changes alone do not trigger Learning (PLT-BID-011).
- **Optimising to form fills in lead gen.** The bidder finds junk efficiently (PRC-DIAG-011).
- **Year-over-year comparisons across structural changes,** and windows with mismatched weekdays or holidays (PRC-DIAG-014).
- **Assuming auction insights shows everything.** It excludes search partners, hides competitors below 10% impression share, reveals nothing about bids, and covers only Search and Shopping in PMax (PRC-DIAG-006, 035).
- **Testing brand incrementality on DTC only,** which ignores marketplace substitution (PRC-DIAG-037).
- **Applying vendor-study averages to one account.** Broad beat exact in about 27% of accounts. Excluding brand from PMax won only 50% of the time (PRC-DIAG-021, 028).

## Unresolved questions

- How large is the experiment false-positive rate in practice? No credible public A/A test results for Google Ads experiments were opened. Roettgerding's ad-testing critique could not be loaded.
- Does today's SERP (AI Overviews, more Shopping units, 4-ad cap) make position effects on CVR or CTR larger than the 2009 data showed? No recent public re-measurement was found.
- What is the exact current Google wording on the learning period ("up to around 50 conversion events or three conversion cycles")? It was seen only via a secondary source (Sept 2026).
- Do auto-applied recommendations reliably appear in change history? The Help page is silent.
- Microsoft Ads import pitfalls and the Lost IS (budget/rank) definitions page were not verified this session (budget exhausted). Research these next.
- Price-in-ad filtering (PRC-DIAG-031) and capacity-based scheduling (PRC-DIAG-029) lack numbers-backed public cases.
- Brand incrementality evidence is dominated by Google-authored (2011–12), academic (Bing, eBay) and vendor (Haus) sources. Independent, recent, small-advertiser evidence is scarce.
- r/PPC threads were not reachable in this session, so community counterexamples are under-represented.
