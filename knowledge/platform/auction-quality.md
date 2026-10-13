---
area: platform
topic: auction mechanics and quality
checked: 2026-10-13
owner: research
---
# Google Ads auction mechanics and quality (Search)

How the Search ad auction decides who shows, where, and at what price: Ad Rank and its inputs, Ad Rank thresholds and reserve prices, how actual CPC is set, auction-time quality versus the 1-10 Quality Score diagnostic, position and impression-share metrics, Auction Insights, own-account keyword prioritisation, and 2024-2026 changes (top-ads redefinition, bottom-of-page double serving, ads in AI Overviews / AI Mode, court findings on pricing "knobs"). The single most important idea: **the visible Quality Score is not used in the auction; auction-time quality, context-dependent thresholds and undisclosed pricing parameters are**, so QS is a coarse diagnostic for *where* quality is weak, never a pricing formula or a KPI to optimise.

---

### PLT-AUC-001 · Ad Rank has six documented inputs and is computed per auction, per ad location
- **Claim:** Ad Rank decides whether an ad is eligible and where it ranks. Google lists six inputs: bid, ad and landing-page quality (auction-time), Ad Rank thresholds, auction competitiveness, context of the search, and expected impact of assets and other formats. A separate auction runs for each ad location (e.g. top ads vs bottom ads), and Ad Rank is calculated for eligibility and again for ranking.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google does not publish a formula or the weights. "Context" is listed as search terms, location, device, time of search, other ads and results on the page, and user signals. Because thresholds and context differ per query, the same keyword with the same bid and ad can have a different Ad Rank in every auction.
- **When it matters / how experts use it:** Diagnose position or volume problems against all six inputs, not just "bid and QS". If volume drops while bids and QS are unchanged, look at context (device or geo mix, SERP layout, AI Overviews) and competitiveness before rewriting ads.
- **Exceptions and failure modes:** The older formula "Ad Rank = max CPC × QS" (pre-2013) is obsolete. Using it to predict outcomes gives wrong answers (see PLT-AUC-017).
- **Signals in data:** Search lost IS (rank) moving without bid or QS changes. Segment by device, time or geo to show rank loss concentrated in one context.
- **Sources:** [About Ad Rank](https://support.google.com/google-ads/answer/1722122) (checked 2026-10-13); [How the Google Ads auction works](https://support.google.com/google-ads/answer/6366577) (checked 2026-10-13)

### PLT-AUC-002 · Ad Rank thresholds are dynamic per auction; low quality raises your own threshold
- **Claim:** Thresholds are the minimum Ad Rank needed to show at all, and separately to show in a given position (higher for top ads). They are set per auction based on ad quality ("lower quality ads have higher thresholds"), ad position, user signals and attributes (e.g. country, device), and the nature of the search (topic and intent).
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google's example contrasts wedding-related queries with basket-weaving queries. Thresholds rise with commercial value and sensitivity of the topic. Since 2017, thresholds also account for query meaning: news-like queries get higher thresholds, so fewer ads show. For some query categories bids "may carry a larger weight in Ad Rank than in the past", Google said at the time (**changed 2017-05**).
- **When it matters / how experts use it:** A thin niche with no competitors can still be expensive, because the advertiser pays the threshold rather than a rival's price. A low-quality ad pays a quality penalty through a higher threshold even when it faces no competition. Quality work therefore lowers the price floor as well as improving rank against rivals.
- **Exceptions and failure modes:** Thresholds are not visible. They can only be inferred from CPC behaviour when competition is known to be thin. The 2017 change meant some advertisers saw higher CPCs with unchanged QS, so a CPC rise is not proof that quality fell.
- **Signals in data:** High CPCs on keywords where Auction Insights shows few or no competitors. CPC differences by device or country for the same keyword and ad. Top-of-page CPC well above all-positions CPC.
- **Sources:** [About Ad Rank thresholds](https://support.google.com/google-ads/answer/7634668) (checked 2026-10-13); [Search Engine Land: changes to AdWords Ad Rank thresholds, May 2017](https://searchengineland.com/adwords-ad-rank-changes-bid-query-meaning-275000) (checked 2026-10-13)

### PLT-AUC-003 · Actual CPC is the minimum needed to clear the threshold and beat the Ad Rank directly below
- **Claim:** Google documents that you pay "only the minimum needed" to clear the relevant Ad Rank threshold and to beat the Ad Rank of the competitor immediately below. With nobody below, you pay the reserve price: the threshold rounded up to the minimum billable unit, such as the next cent in the US. Under manual bidding you are never charged more than your max CPC.
- **Evidence type:** documented
- **Confidence:** high (for the stated rule); medium (as a complete description, see PLT-AUC-004 and PLT-AUC-006)
- **How it works:** Google's worked example: five advertisers have Ad Ranks of 80, 50, 30, 10 and 5. The top-ads threshold is 40 and the threshold below results is 8, with up to 4 top slots.
  - 80 shows at top and pays just enough to beat 50.
  - 50 shows at top and pays just enough to clear 40, the top threshold, because 30 is below that threshold.
  - 30 shows below results and pays just enough to beat 10.
  - 10 shows below results and pays just enough to clear 8.
  - 5 is below every threshold and does not show.

  The price is expressed in Ad Rank units and converted to money by your own quality. Google does not publish that conversion.
- **When it matters / how experts use it:** CPC is set mostly by the advertiser *below* you and by the threshold, not by your own bid. Raising a bid often changes CPC less than expected until it moves you into a different position or auction (for example from bottom to top, where the threshold is higher). Expect step changes in CPC when crossing into top placement.
- **Exceptions and failure modes:** Actual CPC can exceed max CPC with automated bidding. Under manual bidding with bid adjustments, the adjusted bid is the cap. The ECPC exception has been retired for Search (PLT-AUC-024). Asset clicks are billed (PLT-AUC-008).
- **Signals in data:** Avg. CPC well below max CPC under manual bidding. A sharp CPC rise coinciding with a jump in Impr. (Top) %.
- **Sources:** [Actual cost-per-click (CPC): Definition](https://support.google.com/google-ads/answer/6297) (checked 2026-10-13); [About Ad Rank thresholds](https://support.google.com/google-ads/answer/7634668) (checked 2026-10-13); [Google Ads blog 2009: Introduction to the ad auction (Hal Varian)](https://adwords.googleblog.com/2009/03/introduction-to-ad-auction.html) (checked 2026-10-13)

### PLT-AUC-004 · The auction is "generalised-second-price-like", not a pure second-price auction
- **Claim:** Google's documentation never calls the auction "second-price". The pricing rule (pay the next Ad Rank or the threshold) resembles a generalised second-price (GSP) auction weighted by quality. Several documented and court-reported features break pure second-price logic: thresholds that depend on your own quality, an explicit statement that the higher-ranked ad "may pay more" as the Ad Rank gap grows, probabilistic winning, and adjustable pricing parameters revealed in the US antitrust case.
- **Evidence type:** inference (from documented rules plus court-reported facts)
- **Confidence:** medium
- **How it works:** In a pure GSP auction the winner's price does not depend on how far ahead of second place it is. Google's own competitiveness text says that "as the gap in ad rank between two advertisers' ads grows, the higher-ranking ad will be more likely to win but may also pay more" for that certainty. So price and placement have a stochastic element tied to the gap. This is consistent with the randomised GSP ("rGSP") reported at trial (PLT-AUC-006).
- **When it matters / how experts use it:** Do not model CPC as "competitor's bid + 1 cent". Treat CPC as a noisy function of bid, quality and competition. Evaluate bid changes on aggregate outcomes over enough auctions, not on single-day CPC moves.
- **Exceptions and failure modes:** The simple "pay the next Ad Rank" rule is still a useful first approximation for reasoning about direction: better quality or weaker competition below you means a lower price.
- **Signals in data:** CPC variance at a constant bid and stable competitor set. Position "flips" against the same competitor visible in Auction Insights position-above rate, even when you usually outrank them.
- **Sources:** [About Ad Rank](https://support.google.com/google-ads/answer/1722122) (checked 2026-10-13); [Actual CPC: Definition](https://support.google.com/google-ads/answer/6297) (checked 2026-10-13); [SE Roundtable: Google raised ad prices to hit revenue goals](https://www.seroundtable.com/google-raised-ad-prices-to-hit-revenue-goals-36073.html) (checked 2026-10-13)
- **Open questions:** How much of the "gap" pricing is rGSP versus other parameters is not public.

### PLT-AUC-005 · Auction competitiveness: winning is probabilistic, and competitors further down still affect price
- **Claim:** Ads with similar Ad Rank have "similar chances" of winning a position, so winning is not deterministic. Google also says competitors further down the page influence the price paid.
- **Evidence type:** documented
- **Confidence:** high (as a statement); low (for magnitudes)
- **How it works:** No mechanism is published. The court record describes rGSP, under which the higher-ranked ad can be swapped with the runner-up in some auctions; Google's VP Jerry Dischler testified "we flip them" (PLT-AUC-006).
- **When it matters / how experts use it:** Small bid or quality edges over a near-equal competitor buy only a slightly higher probability of the better slot. Expect a share of auctions in which a near-equal competitor sits above you even when you "should" outrank them. Large, durable gaps (much better relevance or much higher value per click) are what give you consistent top placement.
- **Exceptions and failure modes:** In thin auctions the threshold dominates price, not competitors.
- **Signals in data:** Auction Insights for one competitor shows outranking share and position-above rate that are both material (for example 60% and 30%) rather than near 100% / 0%.
- **Sources:** [How the Google Ads auction works](https://support.google.com/google-ads/answer/6366577) (checked 2026-10-13); [Actual CPC: Definition](https://support.google.com/google-ads/answer/6297) (checked 2026-10-13)

### PLT-AUC-006 · US antitrust record: Google tunes text-ad prices with "pricing knobs" (format pricing, squashing, rGSP) without notice
- **Claim:** In *US v. Google* (search), the court found in August 2024 that Google charged supra-competitive prices for general search text ads. It found Google raised prices incrementally so that advertisers would read increases as ordinary "noise", and that many advertisers "do not even realize that Google is responsible for the changes in price". Trial evidence describes three knobs:
  - **Format pricing (launched 2017 as "Project Momiji", per DOJ):** asset/format effects raise the runner-up's effective Ad Rank, raising the winner's price.
  - **Squashing:** adjusts how pCTR differences translate into rank and price, raising the top bidder's price.
  - **rGSP (2019):** a randomised generalised second-price auction that can swap first and second place or multiply the runner-up's score.

  Reported per-change magnitudes: 5% to 15% price increases (court remedies opinion, as reported). The DOJ claimed rGSP added about 10% to revenue and Momiji about 15% to winners' prices. The September 2025 remedies decision requires Google to report changes to its Search Text Ads auction monthly to plaintiffs and a Technical Committee; one law-firm summary says material auction changes must also be disclosed publicly (**changed 2025-09**). Google is appealing.
- **Evidence type:** google-statement (sworn testimony) plus court findings as reported by trade press; DOJ figures are plaintiff argument
- **Confidence:** high that the knobs existed and were used without notice; medium on exact mechanics and magnitudes (court documents not opened directly); low on current settings
- **How it works:** Each knob mostly works by inflating the score of the ad *below* the winner, which sets the winner's CPC without any change in bids, quality or competitor behaviour. The DOJ slides quote a 2017 Google document describing the ranking system as "a simple algorithm consisting of bid, three quality signals, and some (mostly) hand tuned parameters".
- **When it matters / how experts use it:**
  - When CPCs rise 5-15% account-wide, across unrelated accounts and verticals, with no change in Auction Insights, suspect platform-side pricing changes before blaming your own quality or a new competitor.
  - Do not promise clients CPC reductions from QS work.
  - Re-baseline CPC benchmarks when Google discloses auction changes (watch for remedy-driven disclosures from 2025-2026).
- **Exceptions and failure modes:** The findings cover general search text ads, not Shopping or PMax pricing. The record is mostly 2012-2020; current parameter values are unknown. Sponsored law-firm articles add claims (e.g. "15-30% of eligible spend") that are not court findings.
- **Signals in data:** A step change in CPC across many accounts on the same date. Rising CPC with flat or improving QS, flat Auction Insights and stable conversion rates.
- **Sources:** [Search Engine Journal: Google quietly raised ad prices, court orders more transparency (2025-09-03)](https://www.searchenginejournal.com/google-quietly-raised-ad-prices-court-orders-more-transparency/555190/) (checked 2026-10-13); [Search Engine Land: How Google harms search advertisers in 20 slides (DOJ closing deck)](https://searchengineland.com/doj-google-search-ad-price-manipulation-440207) (checked 2026-10-13); [The Current: what the Google search ruling means for advertisers (2024-08-06)](https://www.thecurrent.com/advertisers-google-search-ruling) (checked 2026-10-13); [SE Roundtable: Dischler testimony on revenue-driven auction tweaks](https://www.seroundtable.com/google-raised-ad-prices-to-hit-revenue-goals-36073.html) (checked 2026-10-13); [SEJ sponsored post (Silver Arbitration): ruling and advertisers, 2026-10-07; describes format pricing 2012-2019, squashing 2014+, rGSP 2019+](https://searchenginejournal.com/google-search-antitrust-ruling-silverarbitration-spa/591591) (checked 2026-10-13; sponsored, treat with caution)
- **Open questions:** Whether the monthly auction-change reports will become public. Whether the appeal changes the remedy. Current rGSP and squashing parameters. The primary opinion texts were not opened, so wording comes from press quotes.

### PLT-AUC-007 · "Expected impact of assets and formats" is an Ad Rank input, and assets need minimum Ad Rank to show
- **Claim:** Since October 2013, Google's estimate of how assets (sitelinks, callouts, call and so on) will improve an ad's performance feeds Ad Rank, so two ads with the same bid and quality can rank differently. Assets themselves show only if the ad's Ad Rank, including assets, clears a minimum. Higher positions get first pick of the limited asset space.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:**
  - Google estimates incremental CTR from each eligible asset combination and picks the combination predicted to perform best, within position constraints. Assets cannot buy a lower ad a combination with more expected CTR than a higher ad.
  - Clicks on assets are billed like headline clicks, capped at two clicks per impression. Clicks on review and seller-rating annotations are free.
  - Google states that adding assets is often a cheaper route to more clicks than moving up a position.
  - Google warned in 2013 that CPCs could rise for some advertisers, because competitors' assets now raise the Ad Rank you must beat. This is the same mechanism the DOJ called "format pricing" (PLT-AUC-006).
- **When it matters / how experts use it:** Fill all relevant asset types (sitelinks, callouts, structured snippets, image, call, location where relevant) as a cheap Ad Rank lever before raising bids. Check that assets actually serve. An asset that never serves usually means Ad Rank is too low for that position, not that the asset is bad.
- **Exceptions and failure modes:** More assets do not always help. Google only shows assets predicted to improve performance, and space shrinks in lower positions and on mobile. Account-level automated assets can serve unless opted out.
- **Signals in data:** Asset report impressions low relative to ad impressions. Asset impressions concentrated in "Top" segment.
- **Sources:** [About assets (Google Ads Help)](https://support.google.com/google-ads/answer/7331111) (checked 2026-10-13); [Search Engine Watch: Google rolls out AdWords Ad Rank algorithm update (Oct 2013)](https://www.searchenginewatch.com/2013/10/23/google-rolls-out-adwords-ad-rank-algorithm-update/) (checked 2026-10-13); [Search Engine Land: Ad Rank study after the 2013 formula change (The Search Agency, ~3,500 campaigns)](https://searchengineland.com/google-ad-rank-study-how-the-new-formula-is-impacting-adwords-performance-178736) (checked 2026-10-13)

### PLT-AUC-008 · Asset clicks cost money and are capped at two charged clicks per impression
- **Claim:** There is no cost to add assets. Clicks on them are charged as normal clicks, but Google charges no more than two clicks per impression across the ad and its assets. Seller-rating and review clicks are not charged.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Covered by the billing rules in the assets documentation.
- **When it matters / how experts use it:** Sitelinks pointing to low-intent pages (careers, about us) spend money on non-converting clicks. Point sitelinks at commercial pages and judge assets on conversions per impression, not on CTR alone.
- **Exceptions and failure modes:** Asset-level conversion attribution is limited. Judge assets with ad-group-level tests rather than per-asset CTR.
- **Signals in data:** Assets report: high-CTR sitelinks with poor downstream conversion rate in landing-page reports.
- **Sources:** [About assets](https://support.google.com/google-ads/answer/7331111) (checked 2026-10-13)

### PLT-AUC-009 · The 1-10 Quality Score is not used in the auction; auction-time quality is
- **Claim:** Google states that "Quality Score is not an input in the ad auction" and is "not used at auction time to determine Ad Rank". It is an aggregated, historical, keyword-level diagnostic. Real-time evaluations of the same three components (expected CTR, ad relevance, landing-page experience) *are* used at auction time, together with factors QS does not capture: device, location, time of day, the actual query and assets.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Auction-time quality is a per-auction prediction for the actual search term, device and context. QS is a summary computed for searches that exactly match the keyword (PLT-AUC-010), rated against other advertisers over 90 days. Google calls QS a "diagnostic tool… not a key performance indicator", likening it to a car's engine warning light, and says it should not be "optimized or aggregated".
- **When it matters / how experts use it:**
  - Use QS components to locate weak ads or landing pages, never as a target.
  - For broad match and AI Max, most auctions are not exact matches of the keyword, so QS can be weakly related to the quality you actually face.
  - A keyword with QS 4 can be your most profitable one. Bid and budget decisions follow conversion economics, not QS.
- **Exceptions and failure modes:** Shopping and PMax have no QS, but Google says offer quality and relevance still affect eligibility and impression share.
- **Signals in data:** QS stable while CPC or position moves, or the reverse. The auction-time picture shows up only in outcome metrics (CPC, IS, top rate).
- **Sources:** [About Quality Score (definition)](https://support.google.com/google-ads/answer/140351) (checked 2026-10-13); [About Quality Score for Search campaigns](https://support.google.com/google-ads/answer/6167118) (checked 2026-10-13); [Using Quality Score to guide optimizations](https://support.google.com/google-ads/answer/6167123) (checked 2026-10-13); [Auction insights / impression share notes](https://support.google.com/google-ads/answer/2579754) (checked 2026-10-13)

### PLT-AUC-010 · How visible QS is computed: exact-match searches, 90-day peer comparison, inherited across match types
- **Claim:** QS and its component statuses are based on historical impressions for searches that *exactly* match the keyword. Each component is rated "above average / average / below average" relative to other advertisers whose ads showed for the exact same search over the last 90 days. Changing match type does not change QS. A broad keyword can show a QS with no impressions of its own if an identical exact keyword in the same ad group had impressions in the last 90 days. Paused keywords keep their last scores.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Because the comparison is relative to other advertisers, your QS can fall when competitors improve, with no change on your side (inference). Because it is exact-search based, broad and phrase traffic quality is largely invisible in QS.
- **When it matters / how experts use it:**
  - Don't expect QS to move after rewriting ads for broad-match traffic.
  - Don't switch match types to "fix" QS.
  - Read component changes with a lag: 90-day windows make QS slow to react to fixes and slow to reveal breakage.
- **Exceptions and failure modes:** Low-volume keywords may show "-" (PLT-AUC-015). Keyword text drives QS, so two keywords served by the same ad and page can differ.
- **Signals in data:** Identical QS on a broad keyword and its exact twin in the same ad group. QS unchanged weeks after an obvious landing-page fix.
- **Sources:** [About Quality Score for Search campaigns](https://support.google.com/google-ads/answer/6167118) (checked 2026-10-13); [Ad relevance status](https://support.google.com/google-ads/answer/1659752) (checked 2026-10-13); [Expected CTR](https://support.google.com/google-ads/answer/1659696) (checked 2026-10-13)

### PLT-AUC-011 · Expected CTR is position- and format-normalised and pooled across advertisers; it is not your CTR column
- **Claim:** Expected CTR estimates the likelihood of a click "irrespective of your ad's position, assets, and other ad formats". It uses past keyword performance adjusted for position, assumes the search term matches the keyword exactly, and considers performance within your account and across other advertisers. Device type and the actual search term are considered only at auction time.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Normalising removes the advantage of being at absolute top or having many assets. A below-average expected CTR means the creative or offer underperforms *at equal prominence*. A keyword can have high QS with low expected CTR, or the reverse.
- **When it matters / how experts use it:**
  - Raw CTR is inflated by position, so a high CTR from absolute-top placement does not imply good expected CTR.
  - To fix a below-average status, improve the offer and specificity of headlines for the keyword's exact intent. Bids won't fix it.
  - Expected CTR and landing-page experience appear to carry more weight in visible QS than ad relevance (PLT-AUC-014).
- **Exceptions and failure modes:** Brand keywords and navigational queries have naturally high CTR. Generic informational keywords have low CTR for any advertiser. Status is relative to others on the same search, so a structurally low-CTR query isn't penalised per se.
- **Signals in data:** CTR high but expected CTR "Below average" usually means position-driven CTR. CTR low but status "Average" usually means a low-CTR query type.
- **Sources:** [Expected clickthrough rate: definition](https://support.google.com/google-ads/answer/1659696) (checked 2026-10-13)

### PLT-AUC-012 · Ad relevance measures intent match between keyword/search and ad text
- **Claim:** Ad relevance is "how closely your ad matches the intent behind a user's search", rated against advertisers on the exact same search over 90 days. Google's suggested fixes are matching ad language more directly to search terms and splitting ad groups with many unrelated keywords.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** This is a semantic match of keyword and query to ad text. It is usually the easiest component to move: put the keyword's core concept in headlines, or regroup keywords so one RSA can be specific.
- **When it matters / how experts use it:** A "Below average" ad relevance on many keywords in an ad group usually signals that the ad group is too broad thematically. Restructure or add keyword insertion or ad customisers before rewriting everything.
- **Exceptions and failure modes:** Ad relevance carries the smallest weight in reverse-engineered QS (PLT-AUC-014), so fixing it alone moves QS by about 1-2 points at most. Over-tight ad groups (one keyword each) fragment data that Smart Bidding and RSA testing need.
- **Signals in data:** Mixed relevance statuses within one ad group. Keywords whose head term never appears in any headline.
- **Sources:** [Ad relevance status](https://support.google.com/google-ads/answer/1659752) (checked 2026-10-13); [Quality Score page, ad relevance guidance](https://support.google.com/google-ads/answer/6167130) (checked 2026-10-13)

### PLT-AUC-013 · Landing-page experience: relevance and usefulness, assessed partly by crawlers; your conversion rate is not an input
- **Claim:** Landing-page experience estimates how relevant and useful the page is to people who click. Google says highly rated pages are well organised and have text matching the search, that crawler information may be used to assess ad quality, and that conversion rate can be a proxy for the advertiser but "doesn't impact your landing page status".
- **Evidence type:** documented
- **Confidence:** high (for what is stated); low (for the detailed factor list)
- **How it works:** Google's current help pages give only high-level criteria: consistent messaging from ad to page, giving people what they searched for, and clarity. Older Google guidance on transparency, navigability and mobile speed exists, but the pages opened here do not enumerate those factors.
- **When it matters / how experts use it:** Landing-page experience is the most heavily weighted component in reverse-engineered visible QS, along with expected CTR (PLT-AUC-014). It is also the component AI Max and PMax text customisation and final-URL expansion read. Fix it by:
  - sending each theme to a matching page
  - making the page crawlable (no blocking of Google's crawlers, no interstitial walls)
  - putting the query's answer above the fold.
- **Exceptions and failure modes:** A page that converts well can still rate "Below average" (for example a thin lead-gen page), and the reverse. Pages blocked from crawling, or with frequent errors, can rate poorly or be disapproved (inference from the crawler statement).
- **Signals in data:** "Below average" landing-page experience concentrated on one final URL across many keywords. The status flips after a site redesign or robots/CDN change.
- **Sources:** [Landing page experience: definition](https://support.google.com/google-ads/answer/1659694) (checked 2026-10-13); [About Quality Score for Search campaigns](https://support.google.com/google-ads/answer/6167118) (checked 2026-10-13); [Quality Score component guidance](https://support.google.com/google-ads/answer/6167130) (checked 2026-10-13)
- **Open questions:** Whether mobile speed is still a direct factor. The detailed criteria page (answer/2404197) did not return those details when opened.

### PLT-AUC-014 · Visible QS appears to be 1 + points per component, with expected CTR and landing page weighted more than ad relevance
- **Claim:** Brad Geddes (Adalysis) reverse-engineered visible QS from API data on component statuses: QS ≈ 1 + LPE + AdRel + eCTR, rounded.

  | Status | Landing page experience | Ad relevance | Expected CTR |
  |---|---|---|---|
  | Above average | 3.5 | 2 | 3.5 |
  | Average | 1.75 | 1 | 1.75 |
  | Below average | 0 | 0 | 0 |

  A 10 therefore requires all three components above average.
- **Evidence type:** study (vendor reverse-engineering; sample size not stated; not confirmed by Google)
- **Confidence:** medium
- **How it works:** Worked example from the source: LPE average (1.75) + AdRel above average (2) + eCTR average (1.75) = 1 + 5.5 = 6.5, displayed as 7. Raising LPE or eCTR to above average adds 1.75, giving 8.25, displayed as 8. Adalysis's 2026 page still describes the same additive structure.
- **When it matters / how experts use it:** To prioritise QS diagnostics, a below-average expected CTR or landing-page status costs about 1.75-3.5 points each; ad relevance costs at most 2. Fixing ad relevance alone rarely moves QS much.
- **Exceptions and failure modes:** This describes the *visible* score only. Auction-time weights are unknown and may differ by query. Google could change the mapping without notice.
- **Signals in data:** Every QS in an account can be reproduced from its three statuses with this table. If not, the mapping has changed.
- **Sources:** [Search Engine Land: Reverse-engineering AdWords Quality Score factors (Brad Geddes)](https://searchengineland.com/?p=244192) (checked 2026-10-13); [Adalysis: Quality Score formula explained (modified 2026-03-26)](https://adalysis.com/quality-score/) (checked 2026-10-13)

### PLT-AUC-015 · QS "-" (null) means not enough exact-match searches, not low quality
- **Claim:** A "-" in the QS column means there aren't enough searches that exactly match the keyword to determine a score. Historical QS columns also report no value when impression and click data are insufficient.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** QS is computed from exact-search history (PLT-AUC-010). Long-tail and phrase or broad keywords whose exact form is rarely searched never accumulate enough data. Google suggests higher-volume keywords or broader match types.
- **When it matters / how experts use it:**
  - Exclude null QS from any quality analysis; don't impute a score.
  - In broad-match and AI Max accounts a large share of spend can sit on null-QS keywords. Judge their quality through search-term-level CTR, conversion rate and CPC instead.
- **Exceptions and failure modes:** Treating null as zero, or as "low", in a weighted average distorts account QS badly.
- **Signals in data:** Many "-" rows on keywords with impressions, where the impressions come from non-identical search terms.
- **Sources:** [About Quality Score for Search campaigns](https://support.google.com/google-ads/answer/6167118) (checked 2026-10-13); [Search Engine Land: historical Quality Score reporting](https://searchengineland.com/google-adwords-quality-score-reporting-improvements-275010) (checked 2026-10-13)

### PLT-AUC-016 · Historical QS columns report the last known daily value in the date range
- **Claim:** Four columns, "Qual. Score (hist.)", "Landing page exper. (hist.)", "Ad relevance (hist.)" and "Exp. CTR (hist.)", show the last known score within the selected date range. Segmenting by day shows end-of-day scores. Data go back to January 2016. The plain "Quality Score" column always shows the *current* score regardless of date range.
- **Evidence type:** documented (via Google announcement as reported) plus Google Help mention of the hist. columns
- **Confidence:** high
- **How it works:** Values are daily snapshots, not averages over the period.
- **When it matters / how experts use it:**
  - To check whether a change helped or hurt, segment the historical columns by day around the change date.
  - Experts track impression-weighted QS weekly (by script or tool) to catch breakage. A falling trend matters more than the absolute level; Aaron Levy: "If quality score is trending down, something new is broken."
- **Exceptions and failure modes:** Comparing the current "Quality Score" column to a past date range is a common error. Use the hist. columns.
- **Signals in data:** A step drop on a specific day that coincides with a landing-page deployment or an ad change.
- **Sources:** [Search Engine Land: Google AdWords historical Quality Score data](https://searchengineland.com/google-adwords-quality-score-reporting-improvements-275010) (checked 2026-10-13); [Ad relevance status (hist. column)](https://support.google.com/google-ads/answer/1659752) (checked 2026-10-13); [Optmyzr: Does Quality Score still matter in 2026?](https://www.optmyzr.com/blog/google-ads-quality-score/) (checked 2026-10-13)

### PLT-AUC-017 · The "QS 10 = 50% discount / QS 1 = +400-600%" tables are artefacts of an obsolete formula
- **Claim:** The widely shared CPC discount tables derive from Craig Danuloff's 2009 table (QS 10 = 30% discount vs QS 7; QS 1 = +600%), revised by WordStream in 2013 to a "neutral" QS of 5 (QS 10 ≈ -50%, QS 6 ≈ -17%). They follow mechanically from the old formula "CPC = Ad Rank of advertiser below ÷ your QS + $0.01", not from measured auction data. Google's current documentation says only that higher-quality ads "can often lead to lower CPCs" and gives no mapping.
- **Evidence type:** practitioner (tables); documented (Google's non-quantified statement); inference (that tables are formula-derived)
- **Confidence:** high that the tables are not a platform rule; medium on their derivation (the WordStream article does not state its method; the inverse-ratio pattern matches the formula)
- **How it works:** Illustrative example (constructed, using the obsolete formula). The advertiser below has bid $2 × QS 5 = Ad Rank 10.
  - With QS 10 you pay 10/10 + $0.01 = $1.01.
  - With QS 5 you pay 10/5 + $0.01 = $2.01.

  The "50% discount" is built into the formula by construction. In the real auction, thresholds that depend on quality, context, asset impact, competitiveness, rGSP and squashing (PLT-AUC-002, PLT-AUC-006) break this proportionality. QS is not even the input; auction-time quality is.
- **When it matters / how experts use it:** Never forecast savings from QS changes with these tables. Do expect directional benefit: better auction-time quality lowers both thresholds and the price needed to beat the next ad. Validate with experiments (ad or landing-page A/B tests via Experiments) measuring CPC *and* conversion rate.
- **Exceptions and failure modes:** WordStream's separate empirical finding (CPA about 16% lower per QS point above 5, from about $100M of client spend; Portent found 22%) is observational. High-QS keywords are disproportionately brand or high-intent terms with naturally low CPA, so causality is confounded.
- **Signals in data:** Raising QS from 6 to 8 with no material CPC change is common and consistent with the above.
- **Sources:** [WordStream: Quality Score and cost per conversion (Larry Kim, 2013)](https://www.wordstream.com/blog/ws/2013/07/16/quality-score-cost-per-conversion) (checked 2026-10-13); [About Ad Rank](https://support.google.com/google-ads/answer/1722122) (checked 2026-10-13); [About Quality Score (definition)](https://support.google.com/google-ads/answer/140351) (checked 2026-10-13)

### PLT-AUC-018 · When to work on quality vs bids: an expert decision rule
- **Claim:** Quality work is worth prioritising when rank, not budget, limits volume *and* quality signals are weak on the traffic that matters. It is a red herring when the account meets efficiency targets, when low QS reflects broad reach or low-volume exact forms, or when rank-lost IS is small.
- **Evidence type:** practitioner (Optmyzr 2026 roundup: Aaron Levy, Jyll Saskin Gales; Ginny Marvin "fundamentals are still fundamental") plus inference from documented mechanisms
- **Confidence:** medium
- **How it works:** Quality improves Ad Rank at no marginal cost per click, while bids raise Ad Rank at a cost. Rank-lost impression share combines low bids, low quality and thresholds (PLT-AUC-022). Decision sequence:
  1. Is Search lost IS (rank) or lost top IS (rank) material on converting themes?
  2. Are components "Below average" there (expected CTR or landing page first, PLT-AUC-014)?
  3. Fix those. If components are already average or above, raise bids or targets instead.
- **When it matters / how experts use it:** Saskin Gales treats 7 as very good and 6 as fine. Levy says don't make changes "solely for QS purposes at the expense of ROAS/ROI". These are judgement calls, not thresholds.
- **Exceptions and failure modes:**
  - Brand campaigns usually already have high quality, so bid or competitor dynamics dominate.
  - In PMax, AI Max or broad-match accounts, conversion-data quality and landing-page content matter more than keyword QS.
  - Regulated verticals may have structurally lower expected CTR and higher thresholds that ad tweaks can't fix.
- **Signals in data:** High rank-lost IS plus "Below average" components points to quality work. High rank-lost IS with "Above average" components points to bids or value. Low rank-lost IS means neither is the constraint (check budget or demand).
- **Sources:** [Optmyzr: Does Quality Score still matter in 2026? (2026-03-02)](https://www.optmyzr.com/blog/google-ads-quality-score/) (checked 2026-10-13); [Using Quality Score to guide optimizations](https://support.google.com/google-ads/answer/6167123) (checked 2026-10-13)

### PLT-AUC-019 · Top and absolute-top metrics: definitions, counting rules, and why they can fall as bids rise
- **Claim:** There are two families of metrics.
  - **Rates** (share of *your impressions* that were in a position): Impr. (Top) % = impressions among top ads ÷ your impressions; Impr. (Abs. Top) % = impressions as the first top ad ÷ your impressions.
  - **Shares** (share of the *eligible* top impressions you won): Search top IS = top impressions ÷ estimated eligible top impressions; Search abs. top IS = absolute-top impressions ÷ eligible top impressions. Lost top / lost abs. top IS are split into (rank) and (budget).

  The rates count at most one impression per advertiser per search. Google advises against using the rates as bid targets because they "may decrease as bids increase".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Higher bids let you enter more, and more competitive, auctions where you land in a worse location. Your impression mix shifts, so the *rate* falls while absolute top impressions and top IS rise. Shares use an eligible-impressions denominator, so they are the bid-targetable metrics (Target impression share bidding uses them).
- **When it matters / how experts use it:** Use top IS or abs. top IS (and their lost-rank and lost-budget splits) for competitive or brand-defence goals. Use the rates only to understand where your impressions land. Search partners are excluded, since they don't distinguish top from other.
- **Exceptions and failure modes:** Reading a falling Impr. (Top) % after a bid increase as "the bid increase failed" is a mistake (see PLT-AUC-020 for the 2024 definitional change). Since April 2025, bottom-of-page impressions from advertisers also in top ads change the mix (PLT-AUC-026).
- **Signals in data:** After a bid increase: impressions up, Impr. (Top) % down, Search top IS up. This is consistent with entering new auctions.
- **Sources:** [About top and absolute top metrics](https://support.google.com/google-ads/answer/7501826) (checked 2026-10-13); [Get impression share data](https://support.google.com/google-ads/answer/7103314) (checked 2026-10-13)

### PLT-AUC-020 · "Top ads" no longer always means above organic results (changed 2024-03)
- **Claim:** Google redefined top ads as "adjacent to the top organic search results… generally above" them, but they "may show below the top organic results on certain queries". Placement is dynamic. Google told Search Engine Land this was a "definitional change" that does not alter how metrics are calculated.
- **Evidence type:** documented plus google-statement
- **Confidence:** high
- **How it works:** Testing began in mid-2023 on mobile. The Ads Liaison confirmed the placement as permanent on 2024-03-28. Observed placements include mixed in between organic results and directly below featured snippets. Practitioners described these as rare in mid-2024.
- **When it matters / how experts use it:** An "absolute top" or "top" impression may sit below organic content, so Impr. (Top) % no longer guarantees above-the-fold visibility. Don't promise clients "position 1 above organic" based on these metrics. Auction Insights help text still describes top of page as "above the unpaid search results", an inconsistency in Google's own documentation.
- **Exceptions and failure modes:** Placement depends on query and SERP features. AI Overviews add a further layer (PLT-AUC-027).
- **Signals in data:** CTR on "Top" impressions falling without a change in Top %. Manual SERP checks showing ads interleaved with organic results.
- **Sources:** [Top ads: definition](https://support.google.com/google-ads/answer/14662643) (checked 2026-10-13); [Search Engine Land: Google changes definition of top ads](https://searchengineland.com/google-changes-definition-top-ads-438803) (checked 2026-10-13); [Search Engine Journal: Google ads now mixed in with organic results (2024-05-29)](https://www.searchenginejournal.com/google-ads-now-being-mixed-in-with-organic-results/516940/) (checked 2026-10-13); [Auction insights](https://support.google.com/google-ads/answer/2579754) (checked 2026-10-13)

### PLT-AUC-021 · Average position was removed in September 2019; there is no ordinal position metric now
- **Claim:** Google removed average position starting the week of 2019-09-30. Rules, custom columns, filters and saved reports using it were disabled, and the {adposition} ValueTrack parameter returns an empty string. Search top and absolute-top metrics replace it.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Average position measured order relative to other ads, not page location. Position 1 could be at the bottom of the page when there were no top ads. The replacement metrics describe page location.
- **When it matters / how experts use it:** Legacy scripts, rules and client reports that reference average position or {adposition} silently break or return blanks. Rebuild "position" reporting on top and abs. top IS and rates.
- **Exceptions and failure modes:** Third-party "rank tracking" tools that scrape SERPs measure something different (one location and device, no personalisation).
- **Signals in data:** Empty adposition values in landing-page URLs. Old dashboards with null position fields.
- **Sources:** [Average position sunset begins the week of September 30th](https://support.google.com/google-ads/answer/9439546?hl=en) (checked 2026-10-13); [About top and absolute top metrics](https://support.google.com/google-ads/answer/7501826) (checked 2026-10-13)

### PLT-AUC-022 · Impression share and "lost to rank": an estimate whose rank component bundles bid, quality and thresholds
- **Claim:** Impression share = impressions ÷ *estimated* eligible impressions, where eligibility depends on targeting, approval status and quality. Search lost IS (rank) is the percentage of time ads weren't shown "due to poor Ad Rank". Lost IS (rank) is not shown on the Ad groups tab if the budget ran out at any point in the range.
- **Evidence type:** documented (definitions); inference (decomposition)
- **Confidence:** high (definitions); medium (interpretation)
- **How it works:** Since Ad Rank includes bid, quality, thresholds, context and assets (PLT-AUC-001), "lost to rank" cannot tell you which lever is short. The denominator is Google's estimate, and it changes when Google adds inventory such as bottom-ad double serving or AI Overview placements, so IS can fall with no competitive change.
- **When it matters / how experts use it:** Pair lost IS (rank) with QS components and CPC trends to decide between quality and bids (PLT-AUC-018). Use lost IS (budget) to judge whether more budget would buy more volume at similar efficiency.
- **Exceptions and failure modes:** IS is a poor goal for non-brand terms. Chasing 100% IS buys the most marginal auctions at the highest prices.
- **Signals in data:** IS drops on a date with no competitor or bid change, while impressions are stable or rising. This suggests the denominator grew.
- **Sources:** [About impression share](https://support.google.com/google-ads/answer/2497703) (checked 2026-10-13); [Get impression share data](https://support.google.com/google-ads/answer/7103314) (checked 2026-10-13); [Auction insights (eligibility depends on quality)](https://support.google.com/google-ads/answer/2579754) (checked 2026-10-13)

### PLT-AUC-023 · Auction Insights: what each metric means and what it cannot tell you
- **Claim:** Search Auction Insights reports six metrics: impression share, overlap rate, position above rate, top of page rate, absolute top of page rate and outranking share.
  - **Overlap rate:** how often the other advertiser showed when you showed.
  - **Position above rate:** how often they showed above you when both showed.
  - **Outranking share:** how often you ranked higher or showed when they didn't.

  Limits:
  - No insights are shown below 10% impression share; keywords and ad groups need a minimum activity level.
  - Search partners are excluded.
  - PMax is available at campaign level only and is segmented by channel.
  - A competitor's IS is computed over *their* eligible auctions that overlap yours, so it differs from what they see.
  - "google.com" can appear for Google-hosted landing pages (Business Profile, Sites).
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Competitors are grouped by display domain. You see shares and rates only, never bids, budgets, Quality Scores or targeting.
- **When it matters / how experts use it:** Use it to identify who entered or left, and whether a CPC rise coincides with a competitor's overlap or position-above rate rising. Infer competitor budget limits cautiously: a competitor whose IS drops late in the day *may* be budget-capped, but this is inference, never observation. Since April 2025, overlap and IS can shift because the same advertiser can appear in both top and bottom blocks (PLT-AUC-026).
- **Exceptions and failure modes:** Low-volume ad groups have no report. Account-level views mix branded and non-branded auctions, so segment by campaign.
- **Signals in data:** New domain with rising overlap and position-above rate plus your CPC rising suggests competitive pressure. CPC rising with a flat Auction Insights picture suggests thresholds, pricing or mix changes (PLT-AUC-006).
- **Sources:** [About Auction insights](https://support.google.com/google-ads/answer/2579754) (checked 2026-10-13)

### PLT-AUC-024 · Smart Bidding sets a bid per auction; that bid still enters Ad Rank alongside quality (changed 2025-03 for ECPC)
- **Claim:** Smart Bidding uses "auction-time bidding": it sets a bid for every query and auction from signals including device, location and location intent, time, remarketing lists, language, browser, OS and the actual query. Under automated bidding, actual CPC can exceed a max CPC. ECPC can no longer be chosen for new Search and Display campaigns (October 2024); remaining ECPC campaigns migrated to Manual CPC from March 2025.
- **Evidence type:** documented (bidding behaviour); inference (interaction with Ad Rank)
- **Confidence:** high (documented parts); medium (interaction)
- **How it works:** Google does not document a separate auction for Smart Bidding. The documented Ad Rank inputs still apply, so the automated bid replaces the manual max CPC as the bid input. Inference: higher auction-time quality lets the same tCPA or tROAS bid win more auctions or pay less per click. Quality improvements therefore show up as more conversion volume at target, not as a visible QS-to-CPC change.
- **When it matters / how experts use it:**
  - Under tCPA or tROAS, judge quality fixes by conversion volume and CPA at constant target, not by CPC.
  - Remember that auction-time bids use signals that manual bids can't; manual bid adjustments are largely ignored except device -100%. This last point is practitioner knowledge, not confirmed on the pages opened.
  - Maximize Clicks and Target IS accept a max CPC limit (widely known; the Target IS help page could not be opened in this session).
- **Exceptions and failure modes:** Smart Bidding bids high on auctions it predicts will convert, which can raise average CPC while improving CPA. A rising CPC under Smart Bidding is not by itself a quality problem.
- **Signals in data:** Avg. CPC above any cap you would have set manually. CPC dispersion by device or hour larger than under manual bidding.
- **Sources:** [About Smart Bidding](https://support.google.com/google-ads/answer/7065882) (checked 2026-10-13); [About automated bidding](https://support.google.com/google-ads/answer/2979071) (checked 2026-10-13); [Actual CPC: Definition](https://support.google.com/google-ads/answer/6297) (checked 2026-10-13); [Bidding / ECPC page](https://support.google.com/google-ads/answer/2464964) (checked 2026-10-13); [PPC Land: Google to sunset ECPC by March 2025](https://ppc.land/google-to-sunset-enhanced-cpc-for-search-and-display-ads-by-march-2025/) (checked 2026-10-13)
- **Open questions:** Whether Smart Bidding's predicted conversion rate feeds Ad Rank directly (beyond via the bid) is not documented.

### PLT-AUC-025 · Within one account, keywords don't compete: Google picks one keyword per search by a documented priority order
- **Claim:** Multiple eligible keywords from the same account matching one search don't bid against each other. Google selects one, in this order:
  1. An exact-match keyword identical to the search term (spelling-corrected counts; plurals and synonyms do not).
  2. An identical phrase or broad keyword, AI Max keyword, or PMax search theme.
  3. For non-identical matches, the most relevant ad groups or asset groups.
  4. Ad Rank as tiebreaker.

  Dynamic Search Ads, keywordless AI Max and PMax without search themes compete by Ad Rank. These rules do *not* govern searches from Lens, AI Mode, AI Overviews or autocomplete, where AI relevance selects (**changed 2021-09**, updated with AI Max/PMax).
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** This is deduplication before the auction, so only one ad per advertiser enters a given location's auction. Duplicate keywords across campaigns do not raise your own CPC through self-bidding. They do split data and can route traffic to an unintended campaign (wrong budget, bid strategy or landing page).
- **When it matters / how experts use it:**
  - To force routing, use identical exact keywords. Relevance and Ad Rank decide everything else.
  - Expected keywords sometimes fail to trigger because of low search volume status, disapprovals, targeting exclusions or a limited budget.
  - DSA upgrades to AI Max in September 2026, so DSA-style traffic will follow AI Max rules (**changed 2026-09**, per PPC Land).
- **Exceptions and failure modes:** Separate accounts of the same business are governed by the unfair advantage policy (one ad per auction location), not this logic. Exact-match keywords cannot serve *within* AI Overviews, so they don't block broad from that placement (PLT-AUC-027).
- **Signals in data:** The search terms report shows a query served by a broad keyword even though an exact twin exists. Check eligibility, budget and targeting of the exact.
- **Sources:** [How Google Ads chooses keywords when several match (Google Ads Help)](https://support.google.com/adwords/answer/7502501?hl=en) (checked 2026-10-13); [How the Google Ads auction works](https://support.google.com/google-ads/answer/6366577) (checked 2026-10-13); [Search Engine Land: identical phrase and broad keywords now preferred (2021-09-23)](https://searchengineland.com/google-ads-phrase-and-broad-match-keywords-that-are-identical-to-a-query-are-now-preferred-374673) (checked 2026-10-13); [PPC Land: GML backstage (DSA to AI Max Sept 2026)](https://ppc.land/google-gml-backstage-product-leaders-on-gemini-ai-max-and-measurement/) (checked 2026-10-13)

### PLT-AUC-026 · Same advertiser can now appear in both top and bottom ad blocks (changed 2025-04)
- **Claim:** Since April 2025, advertisers that appear in top ads can also enter the separate bottom-ads auction on the same page. Previously an advertiser was generally limited to one location per page. Within one location the one-ad-per-advertiser rule still applies. Google says advertisers "never bid against themselves", that the top-ads auction is unchanged, and that ad load is unchanged. It reported about 14% more bottom-ad conversions in January-March 2025 tests.
- **Evidence type:** documented plus practitioner commentary
- **Confidence:** high (the change); low (its effect on costs)
- **How it works:** Separate auctions per location (PLT-AUC-001) make this possible. The ad shown at the bottom can differ from the one at top.
- **When it matters / how experts use it:**
  - Segment by "Top vs. other" to see bottom-of-page volume.
  - Expect more impressions with lower blended CTR.
  - Impression share can fall because the eligible pool grew.
  - Auction Insights overlap changes may reflect double serving rather than new competition.
  - Judge on cost per qualified conversion.
- **Exceptions and failure modes:** Practitioners argue the change favours large budgets, and small advertisers may face more competition for bottom slots. That is opinion; there are no published cost data.
- **Signals in data:** "Other" impressions rising from early 2025 for brand and high-intent queries. Blended CTR down while conversions are flat or up.
- **Sources:** [Improving Search ads relevance lower down the page (Google Ads Help, 2025-04-21)](https://support.google.com/google-ads/answer/16206862) (checked 2026-10-13); [Search Engine Land: Google's double-serving dilemma (2025-11-06, opinion)](https://searchengineland.com/google-double-serving-dilemma-who-wins-464233) (checked 2026-10-13)

### PLT-AUC-027 · Ads in AI Overviews and AI Mode use the existing auction; "within" placements need broad match or keywordless targeting (changed 2025-2026)
- **Claim:** Ads can show above, below or within AI Overviews. They serve via "the existing auction ranking system and signals", considering both the query and the AI Overview content. Rules:
  - Within-AIO placement is English-only, in about a dozen markets including the US, and limited to text and Shopping ads from Search, Shopping and PMax.
  - Sensitive verticals are excluded: adult, alcohol, gambling, finance, healthcare, politics and more.
  - You can't target or opt out.
  - These ads are reported as top ads, with no segmentation.

  Ginny Marvin (May 2026) said exact and broad can serve above or below; only broad or keywordless can serve within. An ad can't appear both within and above or below in the same auction. AI Max is "not a technical requirement" for AI search. However, the new AI Mode formats announced at GML 2026 (Conversational Discovery ads, Highlighted Answers, with Gemini-written creative and an independent "explainer") are reported to require AI Max for Search or PMax with text customisation.
- **Evidence type:** documented (AIO help page); google-statement (Ads Liaison, reported); google-statement (GML blog, PPC Land report)
- **Confidence:** high (AIO rules); medium (AI Mode format eligibility)
- **How it works:** Exact match isn't eligible for within-AIO placement, so it doesn't compete there and doesn't block your broad keyword. Ad selection for AI Mode is driven by Gemini relevance to the full response, and the keyword prioritisation rules don't apply (PLT-AUC-025).
- **When it matters / how experts use it:**
  - Accounts on exact or phrase only are absent from within-AIO and new AI Mode inventory. Test broad or AI Max in a controlled experiment if that inventory matters to the vertical.
  - Because reporting merges these impressions into "Top", a shift in Top CTR or conversion rate may be AIO-driven and is unattributable.
- **Exceptions and failure modes:** Excluded verticals (finance, health and others) get no within-AIO ads, so do not plan around it there. Google says there is no separate auction for these placements, but whether pricing or thresholds differ is undisclosed.
- **Signals in data:** The search terms report shows long conversational queries. Top impressions rising on long-tail queries with lower CTR.
- **Sources:** [About ads and AI Overviews (Google Ads Help)](https://support.google.com/google-ads/answer/16297775?hl=en) (checked 2026-10-13); [TechWyse: Ginny Marvin clarifies AI Max and AI search eligibility (2026-06-11)](https://www.techwyse.com/?p=76611) (checked 2026-10-13); [Google blog: A new generation of ads for the AI era of Search (2026-05-20)](https://blog.google/products/ads-commerce/a-new-generation-of-ads-for-the-ai-era-of-search/) (checked 2026-10-13); [PPC Land: GML backstage (2026-05-28)](https://ppc.land/google-gml-backstage-product-leaders-on-gemini-ai-max-and-measurement/) (checked 2026-10-13)
- **Open questions:** How CPC is set for Gemini-generated ad formats. Whether thresholds for AI placements differ. When segmented reporting will arrive.

### PLT-AUC-028 · Ad Strength is not an auction input
- **Claim:** Google states that Ad Strength "isn't used to calculate Ad Rank, Quality Score, or auction wins" and doesn't directly influence serving eligibility. It is creation-time feedback.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Ad Strength scores asset variety and keyword inclusion in RSAs. It is a proxy for the system's ability to test combinations, not a performance measure.
- **When it matters / how experts use it:** Don't sacrifice compliance pinning or proven messaging just to raise Ad Strength. Judge RSAs on conversion metrics and expected-CTR status. Indirect effects exist: more varied assets can raise predicted CTR at auction time.
- **Exceptions and failure modes:** Some automated recommendations and auto-applied changes are framed around Ad Strength. Review them before accepting.
- **Signals in data:** "Poor" Ad Strength ads outperforming "Excellent" ones in the same ad group is common and not a contradiction.
- **Sources:** [About Ad Strength for responsive search ads](https://support.google.com/google-ads/answer/9921843) (checked 2026-10-13)

### PLT-AUC-029 · Thin auctions can be expensive: the reserve price is quality-dependent
- **Claim:** With no competitor below (or none clearing the threshold), you pay the reserve price: your threshold rounded up to the minimum billable unit. Because low-quality ads face higher thresholds, a low-quality ad "could be relatively expensive, even when no ads show immediately below it".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Price = f(threshold), and the threshold depends on your quality, position, user signals and query nature (PLT-AUC-002).
- **When it matters / how experts use it:** In niche or local B2B markets with few competitors, quality (landing-page relevance, expected CTR) is the main CPC lever because there is no competitor price to undercut. Bidding lower does not reduce CPC below the reserve price. It only makes you miss the threshold.
- **Exceptions and failure modes:** Top-ad thresholds are higher, so in a thin market, staying out of the top (lower bids) can sharply cut CPC at some CTR cost. Test it.
- **Signals in data:** Auction Insights shows few or no rivals, yet CPC is stable and high and drops only when quality components improve.
- **Sources:** [About Ad Rank thresholds](https://support.google.com/google-ads/answer/7634668) (checked 2026-10-13); [Actual CPC: Definition](https://support.google.com/google-ads/answer/6297) (checked 2026-10-13)

### PLT-AUC-030 · Observable vs inferable in the auction
- **Claim:**
  - **Observable:** your own bids, CPC, QS and components, IS and lost IS, top and abs. top rates and shares, Auction Insights shares, asset serving, search terms.
  - **Never observable:** competitors' bids, budgets, QS, targeting, margins; the threshold values; auction-time quality; Google's pricing parameters.
- **Evidence type:** inference (from documented reporting scope)
- **Confidence:** high
- **How it works:** Every competitor or threshold explanation is a hypothesis to be tested with experiments (bid, ad or landing-page splits) or natural experiments (dated changes).
- **When it matters / how experts use it:** State causal claims about CPC changes with explicit uncertainty: "consistent with a new competitor (overlap +20 points), cannot exclude platform pricing change".
- **Exceptions and failure modes:** Third-party SERP tools estimate competitor spend and copy. They are useful for copy and offer intelligence, unreliable for bids.
- **Signals in data:** Not applicable.
- **Sources:** [About Auction insights](https://support.google.com/google-ads/answer/2579754) (checked 2026-10-13); [About Ad Rank thresholds](https://support.google.com/google-ads/answer/7634668) (checked 2026-10-13)

---

## Common mistakes and misleading metrics
- **Treating QS as a KPI or auction input.** Google says it is neither (PLT-AUC-009). Optimising for QS can hurt ROAS, for example by adding keyword-stuffed headlines or pausing profitable low-QS keywords.
- **Using QS discount tables to forecast savings.** They are artefacts of an obsolete formula (PLT-AUC-017).
- **Account-level averages of QS that include nulls or are unweighted.** Google says not to aggregate. If you must, weight by impressions and exclude "-".
- **Comparing the current "Quality Score" column to a historical date range.** Use the (hist.) columns, segmented by day (PLT-AUC-016).
- **Expecting broad or phrase traffic quality to show in QS.** QS reflects exact-match searches only (PLT-AUC-010).
- **Reading raw CTR as expected CTR.** Raw CTR is position- and asset-inflated (PLT-AUC-011).
- **Targeting Impr. (Top) % or Impr. (Abs. Top) % with bids.** These rates can fall as bids rise. Use top or abs. top IS (PLT-AUC-019).
- **Assuming "top" means above all organic results.** Not true since 2024 (PLT-AUC-020). AI Overview ads are also lumped into Top (PLT-AUC-027).
- **Reading a falling impression share as lost competitiveness.** The eligible pool (denominator) grows with new inventory: bottom double serving (2025), AIO placements, query expansion (PLT-AUC-022, PLT-AUC-026).
- **Blaming CPC rises on competitors or your own quality without checking for platform-wide shifts.** Google has raised prices in 5-15% increments without notice (PLT-AUC-006).
- **Thinking duplicate keywords across campaigns bid against each other.** They don't, but they do misroute traffic (PLT-AUC-025).
- **Treating Ad Strength as a ranking factor** (PLT-AUC-028).
- **Treating rising average CPC under Smart Bidding as a quality problem.** Judge CPA or ROAS at target (PLT-AUC-024).
- **Using average position or {adposition} in scripts, rules or URLs.** Both are dead since 2019 (PLT-AUC-021).

## Unresolved questions
- How CPC is computed for Gemini-generated AI Mode formats (Conversational Discovery, Highlighted Answers), and whether thresholds for AI Overview placements differ from standard top ads. Google says "existing auction", but pricing is undisclosed.
- Whether the September 2025 remedy's monthly auction-change reports will be public, and whether Google's appeal alters them. Current settings of rGSP, squashing and format pricing are unknown. The primary court opinions were not opened here; findings come from press quotes.
- Whether Smart Bidding's predicted conversion value affects Ad Rank beyond the bid it produces.
- Google's current criteria list for landing-page experience (mobile speed, transparency, navigation). Help pages opened here give only high-level wording.
- Whether the reverse-engineered QS weights (PLT-AUC-014) still hold in 2026 at scale. They need re-validation on a current API pull.
- How much search inventory now flows through non-keyword selection (AI Mode, AIO within, Lens, autocomplete), where keyword prioritisation rules don't apply. There is no segmented reporting yet.
- The magnitude of CPC effects from bottom-of-page double serving (2025). There are no independent studies with cost data yet.
- Research note: web search and fetch budgets were exhausted during this session. Target impression share help (answer/9298564) and the primary court opinions could not be opened, and practitioner sources such as Kirk Williams, Navah Hopkins, Nils Rooijmans and r/PPC were not reached for this file.
