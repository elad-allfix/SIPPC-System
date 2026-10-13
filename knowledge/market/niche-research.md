---
area: market
topic: niche research without account data
checked: 2026-10-13
owner: research
---
# Researching a new niche with no campaign, site or conversion data

How to size demand, estimate cost, map customer situations, read competitors, check regulatory constraints and decide whether a niche is economically testable before any Google Ads data exists. The single most important idea: every pre-launch number (search volume, forecasts, bid ranges, competitor "signals") is a coarse, biased estimate. Use it as a **range for scenario planning**, triangulate it from independent sources, and design the first test to replace the estimates with real data quickly and cheaply, with kill criteria written down before spending.

### MKT-NICHE-001 · Keyword Planner "avg. monthly searches" is a grouped, rounded, 12-month average
- **Claim:** Keyword Planner's average monthly searches is the average number of searches for a keyword *and its close variants* over 12 months (by default), shown for exact-match keywords only and rounded. It is an order-of-magnitude topic signal, not a per-keyword count.
- **Evidence type:** documented (definition); study (accuracy)
- **Confidence:** high (definition); medium (size of error)
- **How it works:** Google groups close variants (plurals, reorderings, misspellings) under one figure, so several "different" keywords can show the identical number; summing them double-counts. The 12-month average hides seasonality (Ahrefs' example: a term that swung from 2.3M to 374k within months). Ahrefs' comparison against Search Console impressions found Keyword Planner "roughly accurate" in about 45% of cases and that it overestimated about 54% of the time (2021 study). Upgrow's 16-month GKP vs GSC comparison (~33k keywords) also found large errors in both directions, with grouping causing some terms to be overstated many times over, and ~7% of keywords with real impressions showing zero in GKP.
- **When it matters / how experts use it:** Use to rank *clusters* of intent against each other and to get an order of magnitude for a market (is this a 500-search or a 50,000-search niche in this geography?). De-duplicate grouped variants before summing. Look at the monthly breakdown, not the average, for seasonal niches.
- **Exceptions and failure modes:** Both accuracy studies come from SEO tool vendors/agencies comparing against GSC impressions, which only count when a page is shown in organic results, so "truth" is itself imperfect; Upgrow's write-up contains internally inconsistent figures. Long-tail, numbered, medical and technical queries are where zeros and misses cluster. Local queries were more often overstated in Upgrow's data.
- **Signals in data:** Multiple keyword ideas with the identical volume; very round numbers; a keyword shown as "0" or "-" that autocomplete clearly suggests; after launch, Search terms report volume far below planner numbers.
- **Sources:** [About Keyword Planner forecasts – Google Ads Help](https://support.google.com/google-ads/answer/3022575) (checked 2026-10-13); [Keyword Search Volume: 5 Things You Need to Know – Ahrefs](https://ahrefs.com/blog/keyword-search-volume/) (checked 2026-10-13); [How accurate is the keyword search volume in Ahrefs – Ahrefs Help](https://help.ahrefs.com/ahrefs-terminology/keywords-explorer/how-accurate-is-the-keyword-search-volume-in-ahrefs) (checked 2026-10-13); [Google keyword tools data study – Upgrow](https://www.upgrow.io/google-keyword-tools-data-study/) (checked 2026-10-13)
- **Open questions:** Whether 2025-2026 grouping changes (AI Mode and longer conversational queries) have widened the gap between planner volume and auction-eligible queries.

### MKT-NICHE-002 · Volume buckets for low-spend or new accounts: work with orders of magnitude
- **Claim:** Accounts with little or no spend may see search volume as wide buckets (e.g. 1-100, 100-1K, 1K-10K, 10K-100K) rather than point estimates. A brand-new AllFix client account is likely to be in this situation.
- **Evidence type:** google-statement (2016, reported by press); practitioner
- **Confidence:** medium (the policy was announced in 2016; current Help pages we opened do not describe it, so the exact thresholds today are unverified)
- **How it works:** Google said "most" advertisers see normal data while lower-spending accounts "could see limited data". The buckets are 10x wide, so a bucket alone cannot distinguish a viable niche from a marginal one.
- **When it matters / how experts use it:** Treat the bucket as a prior, not an answer. Narrow it with (a) the forecast tool, which still returns modelled impressions/clicks, (b) Google Trends ratios against an anchor term whose volume is known (MKT-NICHE-007), (c) a third-party tool (MKT-NICHE-009), and (d) a small paid test, which is the only real measurement. Plan budgets for both ends of the bucket.
- **Exceptions and failure modes:** Practitioners commonly report that running any modest spend unlocks fuller data; this is an observation, not a documented threshold. Access via the API or agency MCC accounts may differ.
- **Signals in data:** Volume column showing ranges; identical ranges for very different keywords.
- **Sources:** [Google officially throttling Keyword Planner data for low-spending AdWords accounts – Search Engine Land](https://searchengineland.com/google-officially-throttling-keyword-planner-data-low-spending-adwords-accounts-255795) (checked 2026-10-13)
- **Open questions:** Current spend threshold (undocumented) and whether it is per account or per payments profile.

### MKT-NICHE-003 · Keyword Planner forecasts are bid-, budget- and quality-conditioned models
- **Claim:** Forecasts estimate impressions, clicks and cost from historical search data, and explicitly factor in your bid, budget, seasonality and *historical ad quality*; historical search volume does not. Overlap between similar or broad match keywords is modelled. A forecast is a conditional scenario, not a promise.
- **Evidence type:** documented
- **Confidence:** high (what goes in); low (accuracy for a new advertiser)
- **How it works:** Google models how many auctions you would enter and win at the stated bid/budget. For a new account there is no ad-quality history, so the model must assume something generic; real quality (ad relevance, landing page) will move results up or down. Overlapping terms are de-duplicated ("Keyword Planner tries to predict how traffic will be divided between the overlapping terms").
- **When it matters / how experts use it:** Run the forecast at two or three bid levels (e.g. near the low and high top-of-page ranges) to see the slope of clicks vs cost: if doubling the bid barely increases clicks, the market is thin. Use the forecast's clicks at the planned budget to size the test (MKT-NICHE-024), and expect real results to deviate.
- **Exceptions and failure modes:** Forecasts assume the keyword list you entered; real broad match and AI-driven matching will trigger different queries. Smart bidding behaviour, ad schedule and audience exclusions are not fully represented. Forecasts cannot see your conversion rate.
- **Signals in data:** After launch, compare forecast clicks/CPC to actual in the first 2-4 weeks; large gaps in impressions point to volume or eligibility, gaps in CPC point to competition or quality.
- **Sources:** [About Keyword Planner forecasts – Google Ads Help](https://support.google.com/google-ads/answer/3022575) (checked 2026-10-13)

### MKT-NICHE-004 · Top-of-page bid ranges are 20th/80th percentile historical bids, not CPC
- **Claim:** "Top of page bid (low range)" approximates the 20th percentile and "(high range)" the 80th percentile of what advertisers have historically paid/bid to appear at the top of the page for that keyword, over the last 30 days, for the selected location and network. They are not the average CPC you will pay and not a ceiling.
- **Evidence type:** documented (definitions); inference (relation to actual CPC)
- **Confidence:** high (definition); medium (how actual CPC relates)
- **How it works:** In the Google Ads auction you normally pay what is needed to keep your position, so actual CPC is often below the bid you set; the separate in-account "top of page bid estimate" is described as depending on Quality Score and competition, with a very high estimate suggesting poor Quality Score. For a new advertiser without quality history, the cost to reach top positions can sit at or above the high range; for a strong, relevant advertiser it may be lower. Twenty percent of top-of-page bids were below the low figure, so that is not a floor either.
- **When it matters / how experts use it:** Use the low/high range to build CPC *scenarios* (pessimistic = high range, optimistic = low range or mid-point) for the break-even calculation (MKT-NICHE-023). A wide spread between low and high indicates heterogeneous competitors (some bidding aggressively, some cheaply) or volatility.
- **Exceptions and failure modes:** 30-day window distorts seasonal niches; "top of page" is not absolute top; aggressive automated bidders can push actual CPCs above the range during peaks; low-volume keywords may have no bid data at all. Do not compare ranges across countries without currency and network checks.
- **Signals in data:** After launch, average CPC vs the planner range by keyword theme; Auction insights "top of page rate" vs CPC.
- **Sources:** [About Keyword Planner forecasts – Google Ads Help](https://support.google.com/google-ads/answer/3022575) (checked 2026-10-13); [Top of page bid estimate: Definition – Google Ads Help](https://support.google.com/google-ads/answer/6292661) (checked 2026-10-13)
- **Open questions:** Whether the percentile ranges include automated (Smart Bidding) auction-time bids, which have no fixed max CPC.

### MKT-NICHE-005 · "Competition" in Keyword Planner measures advertiser density, not cost or difficulty
- **Claim:** The Competition column (low/medium/high, plus a 0-100 index) reflects the number of advertisers that showed on a keyword relative to all keywords on Google, for the chosen location and network. It is not a measure of CPC, SEO difficulty or commercial value.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Counts advertiser presence, not bid intensity. A keyword can have "high" competition with modest CPCs (many small bidders) or "low" competition with high CPCs (few deep-pocketed bidders in a lucrative niche).
- **When it matters / how experts use it:** Use it as a hint about commercial intent (many advertisers usually means someone monetises the query). Do not discard "low competition" terms; they can be overlooked opportunities or simply non-commercial. Always pair with bid ranges and a live SERP check.
- **Exceptions and failure modes:** Informational queries with no ads can show "low" while being worthless for leads; local niches may show "low" nationally but be crowded in one city.
- **Signals in data:** Competition "high" with low bid ranges suggests many cheap or automated bidders; "low" with high bids suggests a few high-value players.
- **Sources:** [About Keyword Planner forecasts – Google Ads Help](https://support.google.com/google-ads/answer/3022575) (checked 2026-10-13)

### MKT-NICHE-006 · Google Trends is a sampled, normalised relative index
- **Claim:** Trends values are scaled 0-100 relative to the share of all searches in that place and time range, computed from a sample, with repeated searches by the same person in a short period removed, low-volume terms shown as 0, and searches made by Google's own products (including AI Mode and AI Overviews) filtered out. It shows direction, seasonality and geography, not absolute volume.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Because values are normalised to total searches in each region, a small region can score higher than a big one. Each query you run is re-scaled, so numbers from separate web queries are not comparable (the alpha Trends API, opened to applicants in 2025-07, returns consistently scaled values across requests). Google warns of noise on low-interest queries and that one-off spikes "should not be interpreted as real search activity".
- **When it matters / how experts use it:** Seasonality (when to launch and budget peaks), geographic prioritisation (which regions over-index), comparing synonyms (which wording users actually prefer), and spotting structural decline or growth over 5 years.
- **Exceptions and failure modes:** Niche local terms often return all zeros; categories ("topics") and literal search terms behave differently; a rising trend may be news-driven and non-commercial.
- **Signals in data:** Jagged series with zeros means sampling noise; use longer windows or broader terms.
- **Sources:** [FAQ about Google Trends data – Google Trends Help](https://support.google.com/trends/answer/4365533) (checked 2026-10-13); [Google Trends – PPC Land](https://ppc.land/google-trends/) (checked 2026-10-13)
- **Open questions:** Since AI Mode searches are excluded, Trends may understate total demand for question-style queries **(changed: exclusion date not documented)**.

### MKT-NICHE-007 · Calibrating Trends with an anchor keyword to fill gaps
- **Claim:** You can convert Trends ratios into approximate volumes by comparing an unknown term against an "anchor" term whose volume you trust (from Keyword Planner monthly data or your own impression data) in the same Trends query.
- **Evidence type:** inference (from documented normalisation)
- **Confidence:** medium-low
- **How it works:** Within one Trends query, all terms share the same scale, so the ratio of their values approximates the ratio of their search shares. Multiply the anchor's volume by the ratio.
- **When it matters / how experts use it:** When the planner shows buckets or zeros for the niche terms, or to estimate a city's share of national demand. Choose an anchor of similar magnitude (ratios near 1:1 to 1:10) to avoid rounding to 0-1.
- **Exceptions and failure modes:** Sampling noise, rounding to integers, different handling of close variants vs Keyword Planner grouping, and Trends' exclusion of repeat searches all bias the ratio. Treat the result as ±50% or worse.
- **Signals in data:** Unstable ratios when re-running the same query on different days means the terms are too small.
- **Sources:** [FAQ about Google Trends data – Google Trends Help](https://support.google.com/trends/answer/4365533) (checked 2026-10-13)

### MKT-NICHE-008 · Autocomplete and People Also Ask show phrasing, not demand size
- **Claim:** Autocomplete predictions reflect real searches but are not a ranking of popularity: Google says they don't "simply display the most common queries" and should not be compared to Trends. They are shaped by language, location, freshness and the user's own past searches, and filtered by policy. People Also Ask boxes are undocumented as a demand measure.
- **Evidence type:** documented (autocomplete); practitioner (PAA use)
- **Confidence:** high (autocomplete); low (PAA as a signal)
- **How it works:** Prediction systems weigh many signals besides frequency; manual and automated removals delete whole classes of predictions (e.g. health-hazard, disparaging terms).
- **When it matters / how experts use it:** Discover the language customers use, modifiers (cost, near me, emergency, reviews, "vs"), problem statements and objections, to seed keyword lists, ad copy and FAQ content. Run in a clean browser in the target location.
- **Exceptions and failure modes:** Personalisation contaminates results; sensitive verticals (health, finance) may have suppressed predictions; absence of a prediction does not mean absence of demand.
- **Signals in data:** Predictions differing by location/device indicates local phrasing to mirror.
- **Sources:** [How Google autocomplete predictions work – Google Search Help](https://support.google.com/websearch/answer/7368877) (checked 2026-10-13)

### MKT-NICHE-009 · Third-party volume tools: useful for ungrouping, but vendor-measured accuracy
- **Claim:** Tools like Ahrefs or Semrush blend Keyword Planner data with clickstream, Trends and other sources to estimate per-keyword volume. Ahrefs reports its estimates are "roughly accurate" for ~60% of keywords vs ~45% for Keyword Planner, measured against Search Console impressions. Expect large errors on any single keyword.
- **Evidence type:** study (vendor self-assessment)
- **Confidence:** low-medium
- **How it works:** They try to split Google's grouped variants and smooth with panel data; Ahrefs states "Only Google has access to the exact data" and aims to be "directionally accurate".
- **When it matters / how experts use it:** Use to split grouped variants, see monthly history without spending, and see organic competitors. Triangulate: if planner, Trends ratios and a third-party tool agree within the same order of magnitude, confidence rises.
- **Exceptions and failure modes:** Vendor studies grade their own homework; clickstream panels under-represent some countries, devices and B2B audiences; small local niches are least accurate.
- **Signals in data:** Tools disagreeing by more than 3-5x on the same term means none should be trusted for that term.
- **Sources:** [How accurate is the keyword search volume in Ahrefs – Ahrefs Help](https://help.ahrefs.com/ahrefs-terminology/keywords-explorer/how-accurate-is-the-keyword-search-volume-in-ahrefs) (checked 2026-10-13); [Keyword Search Volume – Ahrefs](https://ahrefs.com/blog/keyword-search-volume/) (checked 2026-10-13)

### MKT-NICHE-010 · From searches to paid clicks: the demand funnel
- **Claim:** Searches are not available clicks. Paid clicks ≈ eligible searches × impression share you can afford × ad CTR, and only a fraction of searches in a cluster have commercial intent. Many searches end without any click.
- **Evidence type:** inference; study (zero-click statistic)
- **Confidence:** medium
- **How it works:** Ahrefs cites research that roughly two-thirds of Google searches in 2020 ended without a click; ad eligibility further depends on matching, budget, rank and location targeting. New advertisers rarely win a high share of auctions at first.
- **When it matters / how experts use it:** Turn volume into a click range before computing leads: e.g. 1,000 searches/month × 20-60% impression share × 3-8% CTR gives 6-48 clicks, which changes whether the niche can feed even one campaign. The ranges are scenario inputs, not benchmarks.
- **Exceptions and failure modes:** Strong broad match/AI Max expansion can find more queries than the planner listed; branded or navigational queries in the list inflate the estimate.
- **Signals in data:** Low impressions with "Limited by budget" vs low impressions with "eligible" status tell volume from budget problems after launch.
- **Sources:** [Keyword Search Volume – Ahrefs](https://ahrefs.com/blog/keyword-search-volume/) (checked 2026-10-13)

### MKT-NICHE-011 · Microsoft Advertising Keyword Planner: a second, independent estimate
- **Claim:** Microsoft Advertising's Keyword Planner returns 12-month average search counts, competition, suggested bids and historical average CPC, and its traffic estimates are returned as a **minimum and maximum** (a range), aggregated across devices unless filtered.
- **Evidence type:** documented (API guide)
- **Confidence:** medium (the end-user help page could not be opened; the API guide describes the same data)
- **How it works:** Same underlying data as the UI; results vary "significantly depending on the respective filter criteria".
- **When it matters / how experts use it:** A second opinion on relative demand and CPC levels, and an estimate of the Microsoft opportunity itself (often older/desktop-heavy audiences in some markets). Do not assume Bing volume or CPC ratios transfer to Google.
- **Exceptions and failure modes:** Smaller sample means more zeros in niche terms. The page does not explain how competition or the min/max are computed.
- **Signals in data:** Large differences in the ranking of themes between Google and Microsoft planners deserve a SERP check before trusting either.
- **Sources:** [Keyword Ideas and Traffic Estimates – Microsoft Advertising API docs](https://learn.microsoft.com/en-us/advertising/guides/keyword-ideas-traffic-estimates?view=bingads-13) (checked 2026-10-13); help page help.ads.microsoft.com/apex/index/3/en/56696 returned "not found" on 2026-10-13.

### MKT-NICHE-012 · Map demand by customer situation (jobs-to-be-done), not by keyword list
- **Claim:** In a new niche, list the situations that cause someone to search (urgent breakdown, planned purchase, comparison, compliance deadline, price shock, DIY attempt failed) and the progress they want; each situation implies different queries, urgency, conversion type (call vs form), value and landing page.
- **Evidence type:** practitioner; inference
- **Confidence:** medium
- **How it works:** Jobs-to-be-done frames purchases as "hiring" a product to make progress in a specific circumstance; in search, the circumstance shows up as modifiers (emergency, near me, cost, best, how to, vs, for [audience]). Situations are more stable than keywords and survive broad/AI matching.
- **When it matters / how experts use it:** Build a situation × intent table; for each row note example queries (from autocomplete, planner ideas, reviews), likely conversion action, value tier and whether the business can serve it (hours, area, licence). Prioritise situations with urgency + ability to serve. Use it to write negative themes (DIY, jobs, free, definitions) before launch.
- **Exceptions and failure modes:** Situations guessed at a desk can be wrong; validate with client interviews, call recordings and competitor reviews. Over-segmentation creates campaigns too thin to learn.
- **Signals in data:** After launch, search terms and call reasons that do not fit any situation reveal gaps.
- **Sources:** [Know Your Customers' "Jobs to Be Done" – Christensen et al., Harvard Business Review, 2016-09](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done) (checked 2026-10-13) ("the circumstances in which customers try to do them are more critical than any buyer characteristics"); [How Google autocomplete predictions work – Google Search Help](https://support.google.com/websearch/answer/7368877) (checked 2026-10-13) (as a phrasing source)
- **Open questions:** No controlled study links JTBD-based account structures to better paid search results.

### MKT-NICHE-013 · Intent clustering: group by shared SERP and landing page, not by word similarity
- **Claim:** Keywords belong in the same cluster when the same answer (same landing page, same offer) serves them, which is best checked by whether the live SERP shows similar ads and results. Keyword Planner's "refine keywords" groups by theme/brand/category and is a starting point only.
- **Evidence type:** practitioner; documented (planner grouping feature)
- **Confidence:** medium
- **How it works:** Google's systems interpret meaning, so words that look similar can carry different intent ("roof repair" vs "roof repair course"), while different words share intent ("boiler not working" vs "boiler repair"). SERP overlap is a proxy for Google's own interpretation.
- **When it matters / how experts use it:** Defines ad groups/asset groups and landing pages; one cluster per distinct promise. Tag each cluster: commercial, informational, navigational, local, job-seeker, DIY.
- **Exceptions and failure modes:** SERPs change with location, device and time; organic overlap ≠ paid behaviour; tools that automate SERP-overlap clustering differ in thresholds.
- **Signals in data:** After launch, ad groups whose search terms overlap heavily should be merged; ones with mixed intent show split conversion rates.
- **Sources:** [Use Keyword Planner – Google Ads Help](https://support.google.com/google-ads/answer/7337243) (checked 2026-10-13)

### MKT-NICHE-014 · Live SERP review: sample by location, device and time, and don't click competitor ads
- **Claim:** A single search from the office is not representative. Ads vary by user location, device, time and auction; organic results are personalised. A legitimate review samples the core queries several times, from target locations, on mobile and desktop, and records ad count, advertisers, offers, extensions/assets, map pack and AI features.
- **Evidence type:** inference; practitioner
- **Confidence:** medium
- **How it works:** Every query runs a fresh auction; budget-limited competitors appear intermittently. Clicking competitors' ads costs them money and is invalid traffic in Google's definition (intentional clicks by people with no interest, "such as competitors").
- **When it matters / how experts use it:** Decide whether paid space is crowded (4 top ads + LSAs + shopping) or empty (an opportunity or a signal of no money in the niche). Note whether AI Overviews push ads down. Use Google's ad preview tool or a location-set incognito session; record screenshots with timestamp.
- **Exceptions and failure modes:** Seeing no ads on a few checks does not prove no one bids; ads shown to you may be skewed by your own search history.
- **Signals in data:** Same advertisers appearing across all checks suggests sustained budgets; rotating advertisers suggests budget-capped or testing players.
- **Sources:** [About invalid traffic – Google Ads Help](https://support.google.com/google-ads/answer/11182074) (checked 2026-10-13)

### MKT-NICHE-015 · Ads Transparency Center: what it shows and what it never shows
- **Claim:** The Ads Transparency Center is a searchable repository of advertisers and the ads they served on Google surfaces (Search, Display, YouTube, Gmail), filterable by date and location, showing advertiser name, verified/unverified badge, payer, location, ad format and the last date an ad ran. For some regions (notably EEA) it adds targeting information, recipient counts and topic labels. It does not show spend (outside political ads), keywords, bids, CTR, conversions or landing-page performance.
- **Evidence type:** documented; google-statement
- **Confidence:** high (what it shows); medium (EU extras vary)
- **How it works:** Google built it from verification data; ad previews are renderings of creative, not the query that triggered them.
- **When it matters / how experts use it:** Collect competitors' messaging themes, offers, formats (are they on YouTube? Display?), geographic focus and roughly how long creatives have been running. Search by domain as well as legal name; payer and advertiser names can differ (agencies, resellers).
- **Exceptions and failure modes:** Responsive search ads may appear as asset combinations that never served together; absence of a competitor may mean a different legal name; the volume of ads shown says nothing about budget.
- **Signals in data:** Many recent creative variants suggests active testing or an agency; one stale ad suggests a set-and-forget account (weakly).
- **Sources:** [Ads transparency – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/13733850) (checked 2026-10-13); [Announcing the launch of the new Ads Transparency Center – Google blog, 2023-03-29](https://blog.google/technology/ads/announcing-the-launch-of-the-new-ads-transparency-center/) (checked 2026-10-13); [A deep dive into the Google Ads Transparency Center – PPC Land](https://ppc.land/a-deep-dive-into-the-google-ads-transparency-center/) (checked 2026-10-13)
- **Open questions:** Retention period and data lag for non-political ads: PPC Land reports 48-72h lag and ~365-day retention, but no Google page we opened confirms this.

### MKT-NICHE-016 · Interpreting competitor ads: longevity is weak evidence, disappearance is ambiguous
- **Claim:** "This ad has run for a year, so it must work" is an over-claim. Long-running ads may be unmonitored, the only ad in an ad group, a brand campaign, or protected by a large budget. Ads disappear for many reasons unrelated to performance: budget exhaustion, seasonality, policy disapproval, account suspension, agency change, test ending, or a switch to Performance Max/AI-generated assets.
- **Evidence type:** inference (from schema rule 2: competitor bids, budgets, margins and motives are not observable)
- **Confidence:** high (that longevity alone is weak evidence)
- **How it works:** You observe survival, not outcome. Survival correlates with "not obviously failing *for that advertiser's economics and attention level*" at best.
- **When it matters / how experts use it:** Treat persistent themes across *several independent* competitors as a stronger signal than one long-running ad. Use competitor messaging as hypotheses to test, never as proof. State in client reports: "observed", "inferred", "unknown".
- **Exceptions and failure modes:** Large, well-run advertisers with known testing cultures give somewhat stronger signals, but you still cannot see their margins (a loss-leader ad can be rational for them and fatal for you).
- **Signals in data:** Same claim/offer across 3+ competitors = market norm (table stakes); unique claim = possible differentiator or untested idea.
- **Sources:** [Ads transparency – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/13733850) (checked 2026-10-13)

### MKT-NICHE-017 · Competitor landing page and offer teardown: record observables in a fixed grid
- **Claim:** A structured teardown of 5-10 competitors' landing pages (from live ads, not home pages) reveals the market's offer norms: price disclosure, guarantees, response-time promises, CTA type (call/form/booking/quote), form length, financing, trust proofs, and service area. These are observable; their conversion rates are not.
- **Evidence type:** practitioner; inference
- **Confidence:** medium
- **How it works:** Searchers compare multiple ads; your page is judged against what they just saw. Matching table stakes avoids disqualification; differentiation needs at least one credible, provable advantage.
- **When it matters / how experts use it:** Set the client's minimum offer, choose the conversion action (calls where competitors all push calls may signal urgency), and find gaps (no one shows prices; no one offers evening slots).
- **Exceptions and failure modes:** Visiting through ad clicks costs competitors money; use the displayed URL or organic route. Copying offers the business cannot fulfil creates misrepresentation and refund risk.
- **Signals in data:** Homogeneous offers across competitors suggest a commoditised niche where CPCs will be driven by bid competition, not quality.
- **Sources:** [Misrepresentation – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13) (limits on what offers may claim)

### MKT-NICHE-018 · Mine competitor reviews for customer language and switching reasons
- **Claim:** Public reviews (Google Business Profiles, marketplaces, Trustpilot) of competitors are a low-cost source of real customer situations, objections and decisive factors, in customers' own words.
- **Evidence type:** practitioner
- **Confidence:** medium
- **How it works:** Negative reviews reveal failure points (no-shows, hidden fees, slow response) that a challenger can address in ads and landing pages; positive reviews reveal what buyers value enough to mention.
- **When it matters / how experts use it:** Extract recurring phrases into ad copy hypotheses and FAQ; quantify themes (e.g. "price" mentioned in 30% of 1-star reviews) to choose positioning.
- **Exceptions and failure modes:** Review samples are self-selected and may include fake or incentivised reviews; avoid claims comparing yourself to named competitors that you cannot substantiate (unreliable claims risk).
- **Signals in data:** Repeated complaints about response time point to speed as a differentiator (see MKT-WEB lead handling entries).
- **Sources:** practitioner heuristic; no single study opened. Policy limit: [Misrepresentation – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### MKT-NICHE-019 · Offer and positioning analysis must survive the "unreliable claims" policy
- **Claim:** Positioning statements in ads and pages must be provable. Google's Misrepresentation policy prohibits "inaccurate claims or claims that entice the user with an improbable result (even if this result is possible) as the likely outcome", and Dishonest pricing practices covers failure to disclose the full cost or creating a misleading impression of cost.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Misrepresentation subcategories include unacceptable business practices, misleading representation, dishonest pricing, clickbait ads, misleading ad design, manipulated media, unreliable claims, unclear relevance and unavailable offers.
- **When it matters / how experts use it:** When copying aggressive competitor claims ("guaranteed approval", "save 70%", "cheapest in town"), check substantiation; express best-case outcomes as such. Price "from" claims must be available to a real share of customers.
- **Exceptions and failure modes:** Competitors running such claims does not mean they are allowed; enforcement is uneven, and a disapproval or account suspension on a new account is costly.
- **Signals in data:** Disapprovals for "Unreliable claims" or "Misrepresentation"; account-level suspension for "Unacceptable business practices".
- **Sources:** [Misrepresentation – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### MKT-NICHE-020 · Financial services: country-by-country verification before launch
- **Claim:** Google requires financial services verification to advertise financial services in specific countries, typically requiring the type of service, licence/authorisation and regulator registration number, submitted per country. Enforcement began in the UK (2021-09), Australia/Singapore/Taiwan (2022-08-30), Brazil/France/Germany/India/Indonesia/Portugal/Spain (2023-01-24), Italy/Türkiye (2023-11-01), Ireland/New Zealand/South Korea/Thailand (2024-11-07), Malaysia (2026-04-14), and a further EU/EEA batch including Austria, Belgium, Denmark, Finland, Hungary, Iceland, Liechtenstein, Luxembourg, Netherlands, Norway and Sweden from 2026-07-23 **(changed 2026-07)**. The United States is not on the list we opened.
- **Evidence type:** documented; press (expansion detail)
- **Confidence:** high (list as of the check date); medium (whether all remaining EEA countries are now covered)
- **How it works:** Verification is checked against official registries; regulators differ by country (e.g. BaFin, ACPR/ORIAS, IVASS, IRDAI). Unverified advertisers have their financial services ads restricted rather than the whole account; there is a 30-day window after enforcement starts (per PPC Land). Separately, the Financial products and services policy requires visible disclosures (physical address, fees) and, for personal loans, minimum/maximum repayment period, max APR and a representative example; personal loans must have repayment of 61+ days and in the US APR must be below 36%.
- **When it matters / how experts use it:** Before scoping any finance or insurance niche, confirm the client holds the right licence in every target country and can pass verification; if they are a lead generator/broker, check whether their own authorisation (not the end lender's) qualifies. Build the timeline (days to weeks) into launch.
- **Exceptions and failure modes:** Affiliates and comparison sites without their own authorisation may not be verifiable; policy wording changes often; country lists here can go stale.
- **Signals in data:** Ads "Eligible (limited)" or disapproved for "Financial services verification"; ads serving only in some countries.
- **Sources:** [Financial services verification: relevant regulators and enforcement dates – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/12390454?hl=en-GB) (checked 2026-10-13); [Financial products and services – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/2464998) (checked 2026-10-13); [Google expands financial ad verification to 24 EU and EEA countries – PPC Land, 2026-06-28](https://ppc.land/google-expands-financial-ad-verification-to-24-eu-and-eea-countries/) (checked 2026-10-13)
- **Open questions:** PPC Land lists Sweden both as new and already enrolled; the exact set of the 24 new countries was not fully named in the article.

### MKT-NICHE-021 · Insurance: Google policy plus insurance advertising law (US example)
- **Claim:** Insurance falls under Google's financial services rules (and verification where required), but the stricter constraints usually come from insurance regulators. In the US, the NAIC model regulation on accident and sickness insurance advertising (adopted in varying forms by states) treats web and email material as advertising, makes the insurer responsible for all ads including those made by others, requires lead-generating devices to disclose that an agent may contact the person, and bans or restricts words such as "no medical examination required", "low cost", "only", "unlimited", "comprehensive" when they overstate.
- **Evidence type:** documented (model regulation text); inference (applicability to a given state)
- **Confidence:** medium (model law ≠ enacted law in every state)
- **How it works:** "Invitations to inquire" may not mention cost and must refer to an agent/company for details; "invitations to contract" must disclose exclusions and limitations. Testimonials must be genuine and paid endorsements labelled. Licensing may not be implied beyond the states where the insurer is licensed.
- **When it matters / how experts use it:** Ask the client for licence numbers and states/countries of licence; restrict location targeting to licensed jurisdictions; route ad copy through their compliance team; avoid price-led headlines for health products unless the regulation allows.
- **Exceptions and failure modes:** Property/casualty and life have different rules; non-US markets have their own regimes (e.g. EU insurance distribution rules) which this entry does not cover.
- **Signals in data:** Competitor ads in the niche that never mention price may reflect regulation, not strategy.
- **Sources:** [NAIC Model Regulation 040: Advertisements of Accident and Sickness Insurance](https://content.naic.org/sites/default/files/model-law-040.pdf) (checked 2026-10-13); [Financial services verification: regulators – Google](https://support.google.com/adspolicy/answer/12390454?hl=en-GB) (checked 2026-10-13)
- **Open questions:** Which states have adopted which version; how Medicare TPMO rules interact with Google's own health insurance restrictions (not researched).

### MKT-NICHE-022 · Lead-gen consent rules in US insurance: FCC one-to-one vacated, CMS one-to-one still applies to Medicare
- **Claim:** The FCC's "one-to-one consent" rule (one named seller per consent) was vacated by the Eleventh Circuit in *Insurance Marketing Coalition v. FCC* days before its 2025-01-27 effective date **(changed 2025-01)**. Separately, CMS's contract-year 2025 rule requires Medicare third-party marketing organisations (TPMOs) to get prior express written consent, separately for each TPMO, before sharing beneficiary data, and commentators reported it still stood after the FCC ruling.
- **Evidence type:** documented (CMS fact sheet); practitioner/legal commentary
- **Confidence:** medium (legal status can change; this is not legal advice)
- **How it works:** Lead forms that sell leads to multiple buyers depend on the consent language captured at submission; regulated programs (Medicare) can impose stricter rules than general telemarketing law.
- **When it matters / how experts use it:** For any niche whose lead value depends on reselling or calling leads (insurance, solar, debt, home services), check the consent text on the form and who may call. The economics of a niche can collapse if leads cannot legally be shared.
- **Exceptions and failure modes:** State mini-TCPA laws, carrier messaging rules and future rulemaking may re-impose stricter consent; outside the US, GDPR/ePrivacy regimes apply.
- **Signals in data:** Lead buyers rejecting leads for consent defects; high complaint rates on follow-up calls.
- **Sources:** [Contract Year 2025 MA and Part D final rule fact sheet – CMS](https://www.cms.gov/newsroom/fact-sheets/contract-year-2025-medicare-advantage-and-part-d-final-rule-cms-4205-f) (checked 2026-10-13); [Eleventh Circuit vacates FCC's TCPA one-to-one consent rule – Morrison Foerster, 2025-01-30](https://www.mofo.com/resources/insights/250130-eleventh-circuit-vacates-fcc-s-tcpa-one-to-one-consent-rule) (checked 2026-10-13); [Even with FCC 1:1 gone, the CMS 1:1 rule is still standing – TCPAWorld, 2025-03-11](https://tcpaworld.com/2025/03/11/even-with-fcc-11-gone-the-cms-11-rule-is-still-standing/) (checked 2026-10-13)
- **Open questions:** Status of the CMS provision in 2026 rulemaking was not verified.

### MKT-NICHE-023 · Break-even CPC as a range, not a point
- **Claim:** Break-even CPC = (landing page conversion rate) × (lead-to-customer rate) × (gross profit per customer, or the value the client will pay per lead). With no data, compute it as a range using pessimistic and optimistic assumptions, and compare to the top-of-page bid range.
- **Evidence type:** inference (arithmetic)
- **Confidence:** high (formula); low (inputs before launch)
- **How it works:** Example: CVR 5-12%, close rate 20-40%, profit per job $300 → break-even CPC $3.00-$14.40. If the planner's high range for core terms is $25, the niche fails even in the optimistic case unless lifetime value or upsell changes the profit figure. Use a target margin (e.g. spend no more than 50-70% of break-even) because of fixed costs, wasted clicks and attribution gaps.
- **When it matters / how experts use it:** Go/no-go and channel choice before launch; tells you which input (CVR, close rate, value) most needs validating. Use the client's historical close rate from other channels where available.
- **Exceptions and failure modes:** Industry conversion-rate benchmarks are averages across very different advertisers and should be a sanity check, not an input; lifetime value claims from clients are often optimistic; lead value from marketplaces (MKT-NICHE-026) reflects their economics, not the client's.
- **Signals in data:** After launch, recompute with actual CVR at the cluster level; the biggest gap usually sits in lead-to-customer rate, which needs CRM feedback.
- **Sources:** [About Keyword Planner forecasts – Google Ads Help](https://support.google.com/google-ads/answer/3022575) (checked 2026-10-13) (bid range inputs)

### MKT-NICHE-024 · Size test budgets for learning: the "rule of three"
- **Claim:** A test budget should buy enough clicks to distinguish "viable" from "not viable", not to optimise. With zero conversions in n clicks, the 95% upper confidence bound on conversion rate is about 3/n (statistical "rule of three"); so to rule out a 5% conversion rate you need roughly 60 clicks with zero conversions, and to estimate a CVR with useful precision you need many more.
- **Evidence type:** inference (standard statistics)
- **Confidence:** high (the statistic); medium (its application to messy ad data)
- **How it works:** Budget ≈ required clicks × expected CPC (use the high range). Example: break-even requires CVR ≥ 4%; to be ~95% sure CVR is below 4% after zero conversions you need ~75 clicks; at $6 CPC that is ~$450 per tested cluster. To see whether CVR is around 8% rather than 4%, you typically need 15-30 conversions in the comparison, i.e. several hundred clicks.
- **When it matters / how experts use it:** Decide how many clusters to test at once (fewer, better-funded tests), how long the test runs given the forecast's daily clicks, and when to stop. Practitioner advice that Smart Bidding needs a minimum monthly conversion count is a heuristic, not a rule; for niche tests, start with manual/maximise clicks with caps or tightly controlled bidding.
- **Exceptions and failure modes:** Conversion tracking errors invalidate all of this (check tracking first); lead quality, not count, may be the real failure; seasonality and day-of-week effects in a 2-week test.
- **Signals in data:** Zero conversions after the planned click count = kill or rework; 1-3 conversions = ambiguous, extend only if cost per lead is plausibly near target.
- **Sources:** inference from standard binomial statistics; no external page opened for the rule of three during this research.

### MKT-NICHE-025 · Write kill criteria before launch, by failure type
- **Claim:** Kill or pivot criteria should be pre-registered and separated by failure type: (1) no demand (impressions far below forecast while eligible and not budget-limited), (2) unaffordable traffic (CPC persistently above the pessimistic break-even), (3) no conversion (zero or near-zero conversions after the planned clicks), (4) poor lead quality (close rate below threshold after enough leads).
- **Evidence type:** practitioner; inference
- **Confidence:** medium
- **How it works:** Each failure type has a different fix: volume → broaden geography/match types or abandon; cost → narrow to high-intent long tail, improve quality, or change offer; conversion → page/offer/tracking; quality → targeting, negatives, form questions.
- **When it matters / how experts use it:** Prevents sunk-cost continuation and premature killing. Agree with the client in writing what spend they risk to learn, and what result continues/changes/stops the test.
- **Exceptions and failure modes:** Killing on CPA in the first days (high variance); ignoring that the first week of a new account may have higher CPCs; attributing failure to the niche when tracking or call handling is broken.
- **Signals in data:** Impression share lost to budget vs rank; search terms quality; conversions without matching CRM records.
- **Sources:** practitioner heuristic synthesised from MKT-NICHE-003/023/024; no single source.

### MKT-NICHE-026 · Lead marketplaces and pay-per-call prices as value benchmarks (with caution)
- **Claim:** What lead marketplaces, pay-per-call networks or Local Services Ads charge per lead in a niche is evidence that some buyers find leads worth at least that much, and is a useful upper reference for a client's willingness to pay. It is not the client's value per lead.
- **Evidence type:** inference; hypothesis (no marketplace pricing pages were opened in this research)
- **Confidence:** low
- **How it works:** Marketplaces price for their own margin and often sell shared (non-exclusive) leads; pay-per-call prices depend on call duration thresholds and exclusivity.
- **When it matters / how experts use it:** If marketplace leads are cheaper than your projected cost per lead from search, the client may prefer buying leads; if a client already buys leads at $X with a known close rate, that is the best pre-launch estimate of value.
- **Exceptions and failure modes:** Shared vs exclusive, quality filters, refund policies and qualification differ, so prices are not comparable to own-site leads.
- **Signals in data:** Client's existing lead purchases and close rates in CRM.
- **Sources:** none opened (fetch budget exhausted); treat as hypothesis to be verified.
- **Open questions:** Current per-lead pricing by category for Google Local Services Ads, Angi, Thumbtack and pay-per-call networks.

### MKT-NICHE-027 · Traffic objectives: define "good traffic" before buying it
- **Claim:** When the objective is traffic (awareness, content, audience building), define good traffic with behavioural criteria measured in analytics: engaged sessions (GA4: >10 seconds, or a key event, or 2+ page views), scroll or key interactions, return visits, and later conversions, segmented by campaign/placement. Cheap clicks with low engagement are often accidental, bot or low-intent traffic.
- **Evidence type:** documented (GA4 definition, Google invalid traffic); study (vendor IVT data)
- **Confidence:** medium
- **How it works:** Google filters invalid traffic and credits what it detects, including accidental clicks from poor placements, but filtering is not complete. A June 2026 report from an IVT-detection vendor (Lunio, 64M clicks, Q3 2025-Q1 2026) found invalid-traffic rates of ~4-5% on Search and 3-7% on Display; the vendor sells detection, so treat as indicative.
- **When it matters / how experts use it:** Set per-placement or per-channel thresholds (e.g. engagement rate, cost per engaged session) and exclude placements that fail; avoid optimising to "clicks" alone on Display/Demand Gen/PMax without engagement checks.
- **Exceptions and failure modes:** GA4's 10-second default can be gamed by slow pages or auto-refresh; consent banners can hide engaged sessions; engagement ≠ purchase intent.
- **Signals in data:** Very high CTR with very low engagement rate; traffic concentrated in apps or one geography; sessions without scroll or interaction.
- **Sources:** [About engagement rate and bounce rate – Google Analytics Help](https://support.google.com/analytics/answer/12195621) (checked 2026-10-13); [About invalid traffic – Google Ads Help](https://support.google.com/google-ads/answer/11182074) (checked 2026-10-13); [LinkedIn drives the most bot clicks per ad dollar – PPC Land, 2026-06-13](https://ppc.land/linkedin-drives-the-most-bot-clicks-per-ad-dollar-new-report-finds/) (checked 2026-10-13)

### MKT-NICHE-028 · Sites made mainly for ads / arbitrage: the correct Google Ads policy names
- **Claim:** For advertisers, Google Ads prohibits destinations made mainly to show ads under **Destination requirements → "Insufficient original content"**: pages with more ads than original content (traffic routed via "arbitrage"), scraped/mirrored/templated content, bridge/doorway pages, parked or "coming soon" pages, and incomprehensible pages. **"Valuable inventory"** is the name of an AdSense (publisher) policy from 2016 about ad-to-content balance, not the Google Ads advertiser policy. **"Unreliable claims"** is a subcategory of the Misrepresentation policy.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Destination requirements also cover destinations not working, mismatched, not crawlable, not accessible in the targeted location, poor destination experience, and unverified/unacceptable phone numbers. "Abusing the ad network" separately covers gaining "an unfair traffic advantage" and circumventing systems.
- **When it matters / how experts use it:** If a client wants traffic campaigns to monetise a content site with display ads, check the destination's ad density and original content before launch; refuse pure arbitrage set-ups. Use exact policy names when diagnosing disapprovals.
- **Exceptions and failure modes:** Content sites with moderate ads and substantial original content are allowed; thresholds are not published.
- **Signals in data:** Disapproval reason "Destination requirements (Insufficient original content)"; account suspension for circumventing systems in repeat cases.
- **Sources:** [Insufficient original content – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/16427718) (checked 2026-10-13); [Destination requirements – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6368661) (checked 2026-10-13); [Misrepresentation – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13); [Abusing the ad network – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6020954) (checked 2026-10-13); [Google removes AdSense 3-ads-per-page limit – MarTech](https://martech.org/google-removes-adsense-3-ads-per-page-limit-focuses-content-ad-balance/) (checked 2026-10-13)
- **Open questions:** The date "Insufficient original content" became a named sub-policy (its Help article ID suggests a recent page) was not found.

## Common mistakes and misleading metrics
- Summing Keyword Planner volumes across close variants (double counting grouped volume) and treating a 12-month average as next month's demand.
- Reading "Competition: High" as "expensive" or "hard to rank"; it measures advertiser count.
- Using the top-of-page high range as a maximum CPC or the low range as a floor; both are percentiles of historical bids.
- Treating forecasts as targets; they assume generic ad quality and your keyword list, not real matching.
- Comparing Trends values across separate queries or reading Trends as volume; Trends now also excludes AI Mode searches.
- Calling a competitor ad "proven" because it has run for months; inferring competitor budgets from ad counts in the Transparency Center.
- Clicking competitor ads during research (invalid traffic, and it distorts their data and costs money).
- Using industry-average conversion rates as inputs for break-even instead of scenario ranges.
- Killing tests on CPA after a handful of clicks, or continuing because "Smart Bidding needs time" with no pre-set stopping rule.
- Buying "cheap traffic" and celebrating CTR/CPC while engagement rate and conversions are near zero.
- Assuming a regulated niche can launch on a new account in days; verification and licensing checks take time per country.

## Unresolved questions
- Current spend threshold at which Keyword Planner shows exact volumes rather than buckets (undocumented since 2016).
- How AI Mode, AI Overviews and conversational queries change the relationship between planner volume and ad-eligible auctions in 2026.
- Ads Transparency Center data lag and retention for non-political ads (only secondary sources).
- Whether Keyword Planner bid ranges include Smart Bidding auction-time bids.
- Current per-lead prices in lead marketplaces and pay-per-call networks by category (not researched because the fetch budget ran out).
- Status of the CMS TPMO one-to-one consent provision in 2026, and state adoption of insurance advertising model rules.
- No independent (non-vendor) accuracy study of third-party keyword volume tools was found.
