---
area: platform
topic: keywords, search intent and query matching
checked: 2026-10-13
owner: research
---
# Keywords, search intent and query matching

This file covers how Google Ads matches search queries to keywords in 2026. It covers the three match types and close variants, broad match and AI Max (search term matching and keywordless), Google's documented rules for choosing between eligible keywords, ad groups and campaigns (including Performance Max), search terms reporting and its blind spots, negative keywords and brand lists, Keyword Planner, low search volume status, intent classification and trademark rules. The most important idea: **a keyword is no longer a literal string match. It is a signal of intent, and Google decides what that intent covers.** Even exact match matches "same meaning". In 2025-2026 AI Max matching was layered on top of exact and phrase keywords, then auto-migrated onto legacy broad-match and ACA campaigns (Sept 2026). The search terms report now hides a large share of spend and can show Google's *approximation* of a query rather than the literal one. Control has shifted from keyword selection toward exclusions (negatives, brand lists, URL rules), prioritisation design and conversion-signal quality.

---

### PLT-KW-001 · What each match type matches in 2026
- **Claim:** Exact match `[kw]` serves on searches with "the same meaning or intent" as the keyword. Phrase match `"kw"` serves on searches that "include the meaning" of the keyword, where the meaning can be implied or the search more specific. Broad match (the default, no symbols) serves on searches "related to" the keyword, including ones that don't contain its words. Each broader type captures all queries of the narrower types, plus more.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Matching is semantic, not lexical. Google's own broad match example is "low carb diet plan", which can match "carb free foods" and "how to cut carbs for beginners". Language targeting is also semantic: an English keyword "blue shoes" can serve on "zapatos azules" for a user who understands English.
- **When it matters / how experts use it:** Treat match type as a *range of intent* the advertiser accepts, not as a string filter. Exact = narrowest intent band. Phrase = intent containing the concept. Broad = related intents, steered by account signals (PLT-KW-003).
- **Exceptions and failure modes:** Practitioners who learned match types before 2018-2021 still expect literal behaviour from exact and phrase. It no longer exists (PLT-KW-002). Phrase match since 2021 has also absorbed the old broad match modifier (BMM) behaviour (PLT-KW-005).
- **Signals in data:** Search terms report rows labelled "Exact match (close variant)" or "Phrase match (close variant)" whose words differ from the keyword.
- **Sources:** [About keyword matching options](https://support.google.com/google-ads/answer/7478529?hl=en) (checked 2026-10-13)

### PLT-KW-002 · Close variants: what "exact" really includes, and you cannot opt out
- **Claim:** All keyword match types match close variants by default, with no opt-out. For exact and phrase, close variants include misspellings, singular/plural, stemming (floor/flooring), abbreviations, accents, reordered words, added or removed function words, implied words, synonyms and paraphrases, and "same search intent" (e.g. [images royalty free] may match "free copyright images").
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google's examples go well beyond spelling: [bathing suits] can match "swimming suits", and [daydream vr headset] can match "daydream headset" (vr implied). The "same search intent" category is the widest, and Google decides what counts as same intent.
- **When it matters / how experts use it:** (1) Don't build separate keywords for plurals, misspellings or word order. They are duplicates and add nothing (Google: "red car" and "car red" are treated as duplicates). (2) When two meanings must be kept apart (e.g. "cheap" vs "luxury", "repair" vs "replace"), use negatives to enforce the boundary. Exact match alone will not hold it. (3) Audit close-variant rows separately: they are where intent drift shows up first.
- **Exceptions and failure modes:** Close variants do **not** apply to negative keywords, with one exception: misspellings (PLT-KW-018). The Help page says nothing explicit about close variants for broad, since broad is already wider.
- **Signals in data:** A high share of "(close variant)" rows with different CPA or CVR from the literal match. Converting variants can be added as their own keywords to separate bids and ads.
- **Sources:** [About close variants](https://support.google.com/google-ads/answer/9342105?hl=en) (checked 2026-10-13); [About keyword matching options](https://support.google.com/google-ads/answer/7478529?hl=en) (checked 2026-10-13). The 2018 Search Engine Land article on exact "same meaning" variants could not be opened (rate-limited).

### PLT-KW-003 · Broad match signals, and why Google ties broad to Smart Bidding
- **Claim:** Broad match "may also take into account" the user's recent search activity, the content of the landing pages and assets, and the other keywords in the ad group, to understand keyword intent. Google states "It's critical to use Smart Bidding with broad match."
- **Evidence type:** documented (signals); inference (behaviour without Smart Bidding)
- **Confidence:** high for the signal list; medium for the without-Smart-Bidding implications
- **How it works:** Broad match widens *eligibility* across many queries of uneven value. Smart Bidding prices each auction with auction-time signals, so low-value expansions get low bids. Under manual CPC or Maximise Clicks, every expansion gets the same bid. Google documents no different matching logic for broad without Smart Bidding. The difference is in pricing, not in matching.
- **When it matters / how experts use it:** Broad is defensible when (a) the campaign has reliable, value-weighted conversion tracking with enough volume, (b) landing pages and ad-group keywords are tightly themed, because they steer what broad matches, and (c) negatives and brand exclusions are maintained. Ad-group keywords act as context. A tightly themed ad group of broad keywords behaves differently from a mixed one.
- **Exceptions and failure modes:** Broad under manual or click-based bidding in low-data accounts is the classic waste pattern. Broad trained on soft conversions (page views, engagement) optimises toward cheap junk. Landing pages that mention many services widen what broad matches.
- **Signals in data:** Rising share of irrelevant search terms after switching to broad. Spend shifting to queries with no conversions. Search terms that reflect user history rather than the query text (looks "unrelated").
- **Sources:** [About keyword matching options](https://support.google.com/google-ads/answer/7478529?hl=en) (checked 2026-10-13); [Your guide to broad match](https://support.google.com/google-ads/answer/12159290?hl=en) (checked 2026-10-13)
- **Open questions:** How much weight user search history gets relative to query text. Whether broad matching differs at all under non-Smart bidding. Google says it does not, but has never confirmed this explicitly.

### PLT-KW-004 · Evidence on broad vs exact vs phrase performance
- **Claim:** Large vendor datasets consistently find exact match most efficient per conversion, phrase strong (especially lead gen), and broad the biggest by spend but least efficient on average. Google claims broad match improvements of +10% for Smart Bidding users (Oct 2023–Mar 2024).
- **Evidence type:** study + google-statement
- **Confidence:** medium (direction consistent; causality weak)
- **How it works:** Optmyzr, Q1 2023, 2,637 accounts: exact beat broad on CPA in 70.8% of accounts and on ROAS in 72.5%. Broad edged ahead only on impressions and cost. Optmyzr, Feb 2026, 30,000 accounts: broad is now the largest match type by spend, and exact's spend share fell about 9.5–10 points since 2022. Exact "leads on efficiency". Phrase holds the largest non-brand share and the highest e-commerce conversion rate. In lead gen, broad loses more ground. Branded: exact and phrase near-tied on CVR (8.18% vs 8.22%).
- **When it matters / how experts use it:** Don't read "exact is more efficient" as "exact is better". Exact keywords are usually the advertiser's best-known, highest-intent terms (selection bias), and broad buys *incremental* volume at higher marginal CPA. The right question is marginal CPA/ROAS of the broad increment versus target, tested with a campaign experiment rather than a cross-sectional comparison.
- **Exceptions and failure modes:** Vendor samples skew toward advanced advertisers. Single-month snapshots. Conversion definitions vary. Google's +10% has no public methodology.
- **Signals in data:** Compare cost per incremental conversion in a broad-match experiment arm, not blended account CPA.
- **Sources:** [Optmyzr: Broad Match is Winning the Budget War (May 2026)](https://optmyzr.com/blog/google-ads-match-type-performance) (checked 2026-10-13); [Optmyzr study: broad match & bidding (Sept 2023)](https://optmyzr.com/blog/optmyzr-study-broad-match-bidding) (checked 2026-10-13); [Google: Maximize performance on Search with updates to query matching (June 2024)](https://support.google.com/google-ads/answer/15070437?hl=en) (checked 2026-10-13)

### PLT-KW-005 · Phrase match absorbed BMM, and duplicate keywords add nothing
- **Claim:** Since 2021, phrase match and legacy broad match modifier keywords are treated the same for auction preference. Keywords differing only in word order are duplicates. Duplicating a keyword across match types in one ad group is mostly redundant, because broad already covers what phrase and exact cover.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** "We don't treat phrase match and legacy BMM keywords differently in terms of preference for the auction." Among eligible keywords, "the keyword with the highest Ad Rank would be preferred", subject to the prioritisation rules in PLT-KW-006.
- **When it matters / how experts use it:** Keeping an *exact* copy of a key term is still useful because of identical-match priority (PLT-KW-006). Phrase and broad duplicates of the same term in one ad group mostly split data.
- **Exceptions and failure modes:** Legacy BMM syntax (+word) still appears in old accounts and behaves as phrase.
- **Signals in data:** The same search term appearing under several keywords. "Ad group/keyword cannibalisation" in practitioner tools.
- **Sources:** [About changes to phrase match and broad match modifier](https://support.google.com/google-ads/answer/10286719?hl=en) (checked 2026-10-13); [About keyword matching options](https://support.google.com/google-ads/answer/7478529?hl=en) (checked 2026-10-13)

### PLT-KW-006 · Google's documented prioritisation when several keywords, ad groups or campaigns are eligible
- **Claim:** Google applies a four-step order. (1) An exact-match keyword *identical* to the search term wins over all broad/phrase keywords and PMax. (2) Next, phrase or broad keywords (including AI Max) or PMax search themes *identical* to the query. (3) If none is identical, AI-based relevance (meaning of the query versus keywords, landing pages and ad group) keeps only the most relevant ad or asset groups. (4) Ad Rank breaks the tie. "Identical" includes spell-corrected queries but not plurals or synonyms.
- **Evidence type:** documented + google-statement
- **Confidence:** high
- **How it works:** A broad keyword can match the same query in two ad groups, but only the more relevant ad group enters the auction. Dynamic Search Ads, AI Max ad groups without keywords and PMax asset groups without search themes are chosen by highest Ad Rank compared with other ads in the account. Ginny Marvin (Google Ads Liaison, July 2024) adds that a Search keyword of any match type that is identical to the query beats a PMax search theme. When an identical search theme and an identical Search keyword both exist, Ad Rank decides.
- **When it matters / how experts use it:** (1) To route a high-value query to a specific ad group, landing page or bid, add it as an **exact** keyword there. This is the only deterministic routing lever left. (2) Don't expect negatives-free "funnelling" by match type alone. Relevance (step 3) can pick a different ad group than you'd intend. (3) Plurals and synonyms aren't "identical": add an exact copy of each variant that must be routed.
- **Exceptions and failure modes:** See PLT-KW-007. Prioritisation picks *which of your* keywords enters. It does not decide whether you win.
- **Signals in data:** A query served by an unexpected ad group (a check in the search terms report with the Keyword column added). An exact keyword with few impressions while its query shows under a broad keyword elsewhere, which suggests the exact keyword is ineligible (budget, status, targeting).
- **Sources:** [How Google Ads prioritizes keywords, ad groups and asset groups](https://support.google.com/google-ads/answer/7502501?hl=en) (checked 2026-10-13); [Ginny Marvin, SEJ: Guide to keyword prioritization & query matching controls (July 2024)](https://searchenginejournal.com/guide-keyword-prioritization-query-matching-controls-google-ads/522257) (checked 2026-10-13)

### PLT-KW-007 · When the prioritisation rules don't apply
- **Claim:** The preference rules can fail when: the preferred keyword has low search volume status; ads or landing pages are disapproved; campaign targeting excludes the user (location, audience, IP); the campaign is budget-limited; the inventory is Shopping (no preference rules, so a Shopping ad can show alongside your exact-match text ad); or the search is an "advanced search experience" (Lens, AI Mode, AI Overviews, autocomplete). For the last case, the reported search term is "the best approximation of the user's intent", keywords may not be automatically prioritised, and AI relevance picks the ad group. **(changed 2026-05)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** For AI-surface searches there is no literal typed query to be "identical" to, so steps 1–2 of PLT-KW-006 don't trigger.
- **When it matters / how experts use it:** A budget-capped Search campaign hands its exact-match queries to PMax or other campaigns ("Performance Max may occasionally serve on exact match terms" when Search runs out of budget). Fix budget limits on core exact-match campaigns before diagnosing cannibalisation. As AI Mode and AI Overview traffic grows, the share of queries routed by exact keywords shrinks.
- **Exceptions and failure modes:** Google does not publish how often the advanced-experience path occurs.
- **Signals in data:** Exact keyword "Limited by budget" plus the same query appearing in a PMax search terms report. Search terms that read like rewritten intents rather than typed queries.
- **Sources:** [How Google Ads prioritizes keywords, ad groups and asset groups](https://support.google.com/google-ads/answer/7502501?hl=en) (checked 2026-10-13); [About Performance Max campaigns](https://support.google.com/google-ads/answer/10724817?hl=en) (checked 2026-10-13); [SEJ: Google quietly changed how search terms are reported for some AI queries (13 May 2026)](https://www.searchenginejournal.com/google-quietly-changed-how-search-terms-are-reported-for-some-ai-queries/574803/) (checked 2026-10-13)

### PLT-KW-008 · Performance Max vs Search keywords
- **Claim:** Search campaigns with an exact-match keyword identical to the query are prioritised over PMax. PMax search themes carry the same priority as phrase and broad keywords, with Ad Rank deciding between them. For queries that are *not* identical to any keyword, PMax and Search compete through relevance and Ad Rank, so PMax can and does win non-identical queries.
- **Evidence type:** documented
- **Confidence:** high (rules); medium (how often PMax wins non-identical queries in practice)
- **How it works:** PMax asset groups without search themes are chosen by Ad Rank against the account's other ads. Search themes per asset group doubled from 25 to 50 in 2025, and a "usefulness indicator" shows whether a theme adds traffic beyond PMax's own discovery. **(changed 2025)**
- **When it matters / how experts use it:** Protect brand and core money terms with exact-match Search keywords, plus brand exclusions in PMax where you want brand traffic kept in Search. Read PMax search terms reports to find queries that should be routed with exact keywords.
- **Exceptions and failure modes:** Budget-limited Search lets PMax take exact queries (PLT-KW-007). Shopping inventory isn't subject to the rules. Marvin's AI Max launch statement ("If a user's search query matches an eligible Search keyword of any match type, that Search campaign will be prioritized over AI Max keywordless/broad match expansions and Performance Max") reads more broadly than the Help page. It most likely refers to *identical* matches, but it isn't consistent with step 3 of the Help page.
- **Signals in data:** The same terms in the Search and PMax search terms reports. A drop in Search impressions after a PMax launch on non-identical queries.
- **Sources:** [About Performance Max campaigns](https://support.google.com/google-ads/answer/10724817?hl=en) (checked 2026-10-13); [About search themes in Performance Max](https://support.google.com/google-ads/answer/14179631?hl=en) (checked 2026-10-13); [PPC Land: Google wraps up PMax feature rollouts in 2025](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13); [Search Engine Land: Google's AI Max for Search (Ginny Marvin)](https://searchengineland.com/googles-ai-max-search-ginny-marvin-455582) (checked 2026-10-13)
- **Open questions:** Whether "any match type" in Marvin's AI Max statement means identical-only.

### PLT-KW-009 · AI Max for Search: what search term matching does
- **Claim:** AI Max is a feature layer inside Search campaigns, launched in May 2025 **(changed 2025-05)**. It has three features: search term matching, text customization (formerly ACA) and final URL expansion. Search term matching combines broad match expansion with "keywordless" matching that learns from the ad group's keywords, assets and landing pages. Under AI Max, keywords effectively behave as broad. Search term matching can be switched off per ad group, which restores each keyword's own match type.
- **Evidence type:** documented + google-statement
- **Confidence:** high
- **How it works:** In the API, `Campaign.ai_max_setting.enable_ai_max` turns on search term matching only. Text customization and final URL expansion default to OPTED_OUT, and final URL expansion requires text customization. `AdGroup.ai_max_ad_group_setting.disable_search_term_matching` opts an ad group out. Controls include brand inclusions (campaign and ad group level), brand exclusions (campaign), locations of interest (ad group), URL inclusions and exclusions, and text guidelines (up to 25 term exclusions and 40 messaging restrictions). Google: when you move from the broad match setting to AI Max, "broad keywords are not treated as exact match keywords in prioritization". Add exact copies to keep identical-match priority.
- **When it matters / how experts use it:** Turn it on per campaign as an experiment, keep ad groups with exact-only intent (brand, regulated terms) opted out of search term matching, and maintain URL exclusions for pages that shouldn't receive traffic (careers, support, blog). AI Max is "not effective" when the campaign is budget-limited.
- **Exceptions and failure modes:** Tracking templates with static URLs or nonstandard {lpurl} use can 404 under final URL expansion. Marvin: "Negative keywords continue to function as they currently do", so negatives still apply, but there is no AI Max-specific negative type.
- **Signals in data:** Search terms with match type "AI Max", and a Source column showing broad-match expansion vs keywordless. The "AI Max" combined view (search term, headline, landing page). Summary rows in the keywords report. A "Selected by" column in the landing pages report.
- **Sources:** [Optimize Google Ads with AI Max for Search campaigns](https://support.google.com/google-ads/answer/15910187?hl=en) (checked 2026-10-13); [Google Ads API: Get started with AI Max for Search](https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/getting-started) (checked 2026-10-13; page updated 2026-10-01); [Search Engine Land: Google's AI Max for Search (Ginny Marvin)](https://searchengineland.com/googles-ai-max-search-ginny-marvin-455582) (checked 2026-10-13)

### PLT-KW-010 · Forced migration: the broad match setting, ACA and DSA move into AI Max (2026–2027)
- **Claim:** From 3 Aug 2026, new campaign-level broad match settings and legacy ACA can't be created in the UI, Editor or any API version. Through September 2026, existing broad-match-setting campaigns were auto-upgraded to AI Max with **search term matching on only**: text customization and final URL expansion off, pinned RSA assets still respected, brand lists preserved. ACA campaigns were upgraded with search term matching *and* text customization on. DSA automigration was moved from Sept 2026 to **February 2027**: DSA campaigns become standard ad groups with all three AI Max features on, and DSA creation ends January 2027. **(changed 2026-08/09)**
- **Evidence type:** documented + google-statement (Google email 5 Aug 2026, Developer Blog 12 Aug 2026, as reported) + practitioner reporting
- **Confidence:** high for dates and defaults (consistent across Google's announcement page, the API docs and trade press); medium for per-account detail
- **How it works:** The old broad match *setting* converted all keywords to broad and treated the campaign "as if both a broad and an exact version of every keyword exists", which kept identical-match priority. After migration that implicit exact copy no longer applies. The API deprecated `Campaign.keyword_match_type` (setting BROAD returns an error) and added read-only `broad_match_migration_date_time` and `aca_migration_date_time` (v25).
- **When it matters / how experts use it:** For any account touched in Sept 2026: (1) read the migration timestamp per campaign and split before/after comparisons by campaign, not by account month; (2) re-add exact keywords for queries that must keep routing priority; (3) review negatives and search terms weekly for the first weeks; (4) decide whether search term matching should be off in some ad groups.
- **Exceptions and failure modes:** Turning off the old broad setting before migration restores original match types, but keywords converted while it was on show as removed and must be reinstated by hand. Accounts that never used these settings are unaffected.
- **Signals in data:** Campaigns with a migration timestamp. New "AI Max" match type rows appearing in September 2026. CPA/ROAS step changes on the migration date.
- **Sources:** [Google: DSA upgrade to AI Max 2026 (Apr 2026)](https://business.google.com/us/accelerate/announcements/dsa-upgrade-to-ai-max-2026/) (checked 2026-10-13); [PPC Land: broad match campaigns face AI Max auto-upgrade (6 Aug 2026)](https://ppc.land/google-ads-broad-match-campaigns-face-ai-max-auto-upgrade-on-september-1/) (checked 2026-10-13); [PPC Land: DSA automigration delayed to Feb 2027 (13 Jun 2026)](https://ppc.land/google-delays-dsa-to-ai-max-automigration-to-february-2027/) (checked 2026-10-13); [Relevant Audience: new broad match settings blocked 3 Aug (16 Aug 2026)](https://www.relevantaudience.com/google-ads-en/google-blocks-new-broad-match-settings-ai-max-migration/) (checked 2026-10-13); [Google Ads API AI Max docs](https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/getting-started) (checked 2026-10-13)
- **Open questions:** The Google April 2026 page said DSA would upgrade in September; the June 2026 extension supersedes it. Confirm against the account's notifications.

### PLT-KW-011 · AI Max expands mainly from exact and phrase keywords, and reporting blends it in
- **Claim:** In smec's data, about 80% of AI Max impressions were attributed to exact-match keywords, 19.5% to phrase and 0.4% to broad. By July 2026, about 29% of impressions on exact-match keywords in AI Max-enabled ecommerce campaigns (EMEA, 383M impressions) were AI Max expansions rather than true exact matches, up from about 0% in early 2025. Reporting can credit AI Max traffic to exact and phrase keywords, which blends match-type performance.
- **Evidence type:** study (vendor, ecommerce, EMEA) + practitioner + google-statement
- **Confidence:** medium
- **How it works:** With search term matching on, an exact keyword acts as a seed for broad and keywordless expansion. Brad Geddes (Adalysis, Dec 2025) found the same query under an exact keyword and under AI Max, location queries routed to the wrong ad group, and "keywordless" rows with no keyword attribution. Google (Marvin) attributed some of these odd matches to Google Maps autocomplete suggestions and said "we're increasingly determining relevance by inferred intent". A Google employee claimed AI Max bids on exact/phrase keywords only when cheaper than the keyword's own auction. smec's Mike Ryan disputed this, and it is unverified.
- **When it matters / how experts use it:** Don't evaluate "exact match performance" in an AI Max campaign from keyword rows alone. Segment search terms by match type (AI Max vs exact) and Source. For true exact-only control, disable search term matching on that ad group.
- **Exceptions and failure modes:** Ecommerce-only and EMEA-only sample. Lead gen may differ. Expansion share varies with keyword hygiene and budget headroom.
- **Signals in data:** Exact keyword rows whose search terms include "AI Max" match-type entries. Exact keyword CPA worsening after AI Max is enabled.
- **Sources:** [PPC Land: Exact match loses 1 in 4 impressions to AI Max (9 Aug 2026)](https://ppc.land/exact-match-loses-1-in-4-impressions-to-ai-max-smec-finds/) (checked 2026-10-13); [SEJ: What smec's data reveals about AI Max performance (5 Mar 2026)](https://www.searchenginejournal.com/what-smecs-data-reveals-about-ai-max-performance/568866/) (checked 2026-10-13); [PPC Land: Google clarifies AI Max attribution discrepancies (Dec 2025)](https://ppc.land/google-clarifies-ai-max-attribution-discrepancies-as-advertisers-discover-search-term-reporting-anomalies/) (checked 2026-10-13)

### PLT-KW-012 · AI Max performance: Google claims vs independent data
- **Claim:** Google's uplift claims have shifted. May 2025: +14% conversions/value at similar CPA/ROAS (+27% for exact/phrase-heavy campaigns). April 2026: +7% average for the full suite vs search term matching alone (non-retail). July 2026 earnings call: +15%. Independent data is mixed. smec (250+ retail campaigns): median conversion value +13% and median CPA +16%; ROAS ranged from +42% to −35% versus baseline; only 22% of campaigns landed near target. Separately, smec (Nov 2025) found AI Max ROAS about 35% below the classic match types. Single-advertiser tests report much higher CPA.
- **Evidence type:** google-statement + study + practitioner
- **Confidence:** medium (claims documented; external validity low)
- **How it works:** Expansion buys incremental queries, which tend to have a higher marginal cost. Google's figures are averages "at similar CPA/ROAS" with undisclosed baselines.
- **When it matters / how experts use it:** Run AI Max as a campaign experiment with enough budget headroom. Google's webinar guidance (Oct 2025, reported) was at least $50/day and about 8 weeks. Judge on incremental CPA/ROAS versus target and on lead quality (offline conversions), not blended totals.
- **Exceptions and failure modes:** Engagement-type conversions make AI Max look good. Budget-limited campaigns can't expand.
- **Signals in data:** Experiment arm with higher conversions but CPA above target. AI Max rows with near-zero conversions.
- **Sources:** [SEJ: smec AI Max data (Mar 2026)](https://www.searchenginejournal.com/what-smecs-data-reveals-about-ai-max-performance/568866/) (checked 2026-10-13); [PPC Land: AI Max attribution discrepancies (Dec 2025)](https://ppc.land/google-clarifies-ai-max-attribution-discrepancies-as-advertisers-discover-search-term-reporting-anomalies/) (checked 2026-10-13); [PPC Land: smec exact match finding (Aug 2026)](https://ppc.land/exact-match-loses-1-in-4-impressions-to-ai-max-smec-finds/) (checked 2026-10-13); [Google: DSA upgrade to AI Max 2026](https://business.google.com/us/accelerate/announcements/dsa-upgrade-to-ai-max-2026/) (checked 2026-10-13)

### PLT-KW-013 · Search terms report privacy thresholds: how much is hidden
- **Claim:** Search terms without "enough query activity" are left out of the search terms report for privacy, and Google gives no numeric threshold. Since the September 2020 change (partly reversed in 2021), practitioners consistently report that 20–45% of clicks or spend sits in unreported terms, with wide variance by account and keyword. Long-tail and low-volume accounts are hidden the most.
- **Evidence type:** documented (the omission) + study/practitioner (the size)
- **Confidence:** high that a meaningful share is hidden; medium for any specific percentage
- **How it works:** Seer Interactive: spend with visible terms fell from 98.7% to 71.0% overnight on 1 Sept 2020. Matthew Umbro (5 accounts): hidden-term clicks rose from under 6% to over 30% in three accounts. Mark Meyerson (Sept 2024): about 40% of clicks and spend hidden across his agency, up to 85% on some keywords, with peers reporting 20–80%. Doctor Ads (Aug 2026, 88 accounts): the median account had 44% of clicks in the "Other search terms" row of the insights category report. That measures insights categories, not report cost. A Jan 2025 report described a "Private search term" label in PMax for terms under 50 unique searches in 90 days (unverified against Google docs).
- **When it matters / how experts use it:** Measure hidden share per campaign as (total cost − sum of visible search term cost) / total cost. Treat negatives built from visible terms as covering only the visible part. Rely on broad negatives and n-grams (PLT-KW-022) and on search term insights to cover the hidden tail. Hidden share rises with broad/AI Max and long-tail intent, so factor it into the match-type decision.
- **Exceptions and failure modes:** The percentages measure different things (clicks vs spend vs category rows) and aren't comparable. Judge Mehta (Sept 2025) declined to force Google to share query-level data, so no regulatory fix is coming.
- **Signals in data:** A large gap between campaign totals and the sum of search term rows. Hidden share jumping after enabling broad or AI Max.
- **Sources:** [About the search terms report](https://support.google.com/google-ads/answer/2472708?hl=en) (checked 2026-10-13); [PPC Land: Explaining the search terms report](https://ppc.land/search-terms-report/) (checked 2026-10-13); [Practical Ecommerce: Google Ads decreases search terms visibility (Oct 2020)](https://www.practicalecommerce.com/google-ads-decreases-search-terms-visibility) (checked 2026-10-13)

### PLT-KW-014 · Search terms may be Google's approximation, not what the user typed
- **Claim:** For searches from Lens, AI Mode, AI Overviews and autocomplete, the search term shown in reporting is "the best approximation of the user's intent", not necessarily a literal typed query. **(changed 2026-05, spotted by Anthony Higman, reported 13 May 2026)**
- **Evidence type:** documented
- **Confidence:** high (documented); low on prevalence
- **How it works:** These surfaces involve multi-turn prompts, images or partial input, so Google normalises them into a query-like string. Google hasn't said how often this happens or whether approximated rows can be told apart.
- **When it matters / how experts use it:** Treat search terms as intent evidence, not exact customer wording, especially for ad copy research, compliance review and building exact-match negatives. An exact negative on an approximated string may not block the underlying query. Prefer phrase or broad negatives on the offending concept.
- **Exceptions and failure modes:** Typed Google Search queries are still reported literally (subject to privacy thresholds and spell-correction normalisation, PLT-KW-015).
- **Signals in data:** Unusually clean, grammatical or question-like search terms. Terms that look like summaries.
- **Sources:** [How Google Ads prioritizes keywords, ad groups and asset groups](https://support.google.com/google-ads/answer/7502501?hl=en) (checked 2026-10-13); [SEJ (13 May 2026)](https://www.searchenginejournal.com/google-quietly-changed-how-search-terms-are-reported-for-some-ai-queries/574803/) (checked 2026-10-13); [Search Engine Land: query reports may not show actual user searches](https://searchengineland.com/google-says-search-query-reports-may-not-show-actual-user-searches-477393) (checked 2026-10-13)

### PLT-KW-015 · Misspelled queries are reported under the correct spelling
- **Claim:** Since June 2024, misspelled queries are reported together with the correctly spelled query. Google says this made about 9% of search terms that had been grouped under "Other" visible on average. **(changed 2024-06)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Normalisation pools low-volume misspellings into a term that clears the privacy threshold.
- **When it matters / how experts use it:** You can no longer measure misspelling traffic separately in the search terms report. Misspelling keywords are mostly pointless anyway (close variants and identical-match spell-correction cover them).
- **Exceptions and failure modes:** Brand misspellings that carry distinct intent (e.g. a competitor with a similar name) are invisible as separate rows.
- **Signals in data:** Fewer distinct misspelled rows after mid-2024.
- **Sources:** [Google: Maximize performance on Search with updates to query matching (26 Jun 2024)](https://support.google.com/google-ads/answer/15070437?hl=en) (checked 2026-10-13)

### PLT-KW-016 · Search terms insights and the PMax search terms report
- **Claim:** Search terms insights group queries into themes and subthemes from the last 56 days. Low-volume queries are rolled into subthemes or an "other queries" bucket without revealing them. PMax now has a full search terms report: announced 30 Apr 2025, in all PMax campaigns and the API by Aug 2025, in Editor 2.11 (Nov 2025). It has a source column distinguishing keywordless matches from search-theme matches. **(changed 2025)**
- **Evidence type:** documented + google-statement
- **Confidence:** medium-high (the dedicated insights Help page couldn't be opened, so details come from the main search terms report page and Google's 2025 PMax post)
- **How it works:** Insights show category-level search volume and performance where individual terms fall below the threshold, so they reach part of the hidden tail.
- **When it matters / how experts use it:** Use categories to find whole themes to exclude (negatives, brand exclusions) or to build out (exact keywords, search themes). Use the PMax report to spot Search cannibalisation and brand leakage.
- **Exceptions and failure modes:** Category labels are model-generated and can lump distinct intents together. Conversion numbers can differ from the report due to conversion lag.
- **Signals in data:** A large "Other" category share is a measure of opacity (median about 44% of clicks in one 88-account sample, PLT-KW-013).
- **Sources:** [About the search terms report](https://support.google.com/google-ads/answer/2472708?hl=en) (checked 2026-10-13); [Google: Unlock more visibility and control in Performance Max (7 Aug 2025)](https://support.google.com/google-ads/answer/16451273) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13). The search terms insights Help page (answer 11386431) could not be opened (fetch error).

### PLT-KW-017 · Reading match-type labels in the search terms report
- **Claim:** The Match type column shows Exact match, Exact match (close variant), Phrase match, Phrase match (close variant), Broad match, and since July 2025 "AI Max". The Source column for AI Max distinguishes broad-match expansion from keywordless. Dynamic Search Ads and Shopping return no keyword and show "Exact".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The label is the *match mechanism*, not the keyword's match type. An exact keyword can show AI Max rows.
- **When it matters / how experts use it:** Pivot performance by label to quantify drift. Close-variant and AI Max rows with weak CVR are candidates for negatives or for opting the ad group out of search term matching.
- **Exceptions and failure modes:** The "Exact" label on DSA and Shopping rows doesn't mean an exact keyword matched.
- **Signals in data:** Share of cost in close-variant or AI Max rows over time.
- **Sources:** [About the search terms report](https://support.google.com/google-ads/answer/2472708?hl=en) (checked 2026-10-13); [Optimize Google Ads with AI Max](https://support.google.com/google-ads/answer/15910187?hl=en) (checked 2026-10-13); [PPC Land: Explaining the search terms report](https://ppc.land/search-terms-report/) (checked 2026-10-13)

### PLT-KW-018 · How negative keyword match types behave: no close variants, but misspellings are blocked
- **Claim:** Negative broad blocks searches containing *all* its terms in any order. Negative phrase blocks the terms in that order, with extra words allowed. Negative exact blocks only the exact terms in order with no extra words. Negatives don't expand to close variants: plurals, singulars and synonyms must be added separately (negative broad "flowers" doesn't block "red flower"). Since mid-2024, negatives **do** block misspellings and account for casing. **(changed 2024-06)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google: "Negative keywords won't match to close variants or other expansions", and "Negative keywords automatically account for casing and misspellings." Example: you can exclude "all 1.5 million variations of 'YouTube' with one negative keyword." Only the first 16 words of a query are checked: a negative word in 17th position doesn't block.
- **When it matters / how experts use it:** (1) Add singular and plural forms of negatives. (2) Use negative phrase or broad on single offending words (e.g. "free", "jobs") rather than many negative exact strings. (3) Use negative exact to block one precise query while keeping longer, more qualified ones (negative [cheap plumber] blocks only that query and still allows "cheap plumber emergency"). (4) For a brand's many spellings, a single negative now suffices.
- **Exceptions and failure modes:** Display and Video negatives work as topic exclusions and may let excluded terms appear. Synonyms ("complimentary" for "free") need their own negatives. Because negatives now block misspellings, a short negative can catch a *different* word that Google treats as a misspelling. Check impact before adding very short negatives.
- **Signals in data:** Negated concepts reappearing as plurals or synonyms in search terms.
- **Sources:** [About negative keywords](https://support.google.com/google-ads/answer/2453972?hl=en) (checked 2026-10-13); [Google: query matching updates (June 2024)](https://support.google.com/google-ads/answer/15070437?hl=en) (checked 2026-10-13); [Ginny Marvin, SEJ (July 2024)](https://searchenginejournal.com/guide-keyword-prioritization-query-matching-controls-google-ads/522257) (checked 2026-10-13); [About account-level negative keywords](https://support.google.com/google-ads/answer/11396330?hl=en) (checked 2026-10-13)

### PLT-KW-019 · Negative keyword limits and scopes
- **Claim:** Up to 10,000 negatives per campaign. Negative keyword lists: up to 20 per account (and 20 per manager account), 5,000 keywords each, applied to many campaigns at once. Account-level negatives: up to 1,000 per account. For Display and Video, at most 1,000 negatives are considered.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Lists are shared objects, so editing a list changes every attached campaign. Account-level negatives sit in Admin > Account settings and apply automatically.
- **When it matters / how experts use it:** Structure scopes by blast radius: account-level for universal exclusions (jobs and careers, competitor/brand terms you never want, illegal or unsafe terms); shared lists for themes reused across some campaigns (e.g. "DIY/how-to" for service campaigns but not content campaigns); campaign or ad-group negatives for routing (sculpting queries between ad groups). A wrong account-level negative silently starves every campaign.
- **Exceptions and failure modes:** The 1,000 account-level cap is small. Large universal lists must go in shared lists.
- **Signals in data:** Impression drops right after list edits. A negative that conflicts with a positive keyword (Google flags these conflicts; practitioners also script them).
- **Sources:** [Google Ads account limits](https://support.google.com/google-ads/answer/6372658?hl=en) (checked 2026-10-13); [About negative keyword lists](https://support.google.com/google-ads/answer/2453983?hl=en) (checked 2026-10-13); [About negative keywords](https://support.google.com/google-ads/answer/2453972?hl=en) (checked 2026-10-13)

### PLT-KW-020 · Account-level negatives: which campaigns they cover
- **Claim:** Account-level negatives apply to all search and shopping inventory in Search, Performance Max, App, Shopping, Smart and Local campaigns, with broad, phrase or exact match per term. Display and YouTube placement control uses the separate "excluded content keywords" (also capped at 1,000).
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** A single list with no per-campaign opt-out.
- **When it matters / how experts use it:** The cleanest way to keep PMax off unwanted searches across all campaigns. Never put terms there that any campaign might want (e.g. own brand, if a brand campaign exists).
- **Exceptions and failure modes:** Doesn't reach Display or YouTube placements.
- **Signals in data:** Terms disappearing account-wide. Brand campaigns losing impressions after a well-meant account-level negative.
- **Sources:** [About account-level negative keywords](https://support.google.com/google-ads/answer/11396330?hl=en) (checked 2026-10-13); [Nils Rooijmans: PMax account-level negatives are here (2023, updated 2024)](https://nilsrooijmans.com/daily/performance-max-account-level-negative-keywords-are-here) (checked 2026-10-13)

### PLT-KW-021 · Negatives in Performance Max (2025 changes)
- **Claim:** PMax gained campaign-level negative keywords in early 2025. The cap rose from 100 to 10,000 per campaign (11 Mar 2025), and negative keyword lists became attachable to PMax during 2025. PMax negatives apply only to Search and Shopping inventory. The UI shows predicted impact before you commit. **(changed 2025-01 to 2025-08)**
- **Evidence type:** documented + google-statement
- **Confidence:** high
- **How it works:** The same match-type behaviour as Search negatives, set with the usual symbols. Brand exclusions stay the recommended way to block brand traffic in PMax. Retailers with feeds can set different brand exclusion rules for Search text and Shopping.
- **When it matters / how experts use it:** Before 2025, practitioners used account-level negatives or Google rep requests to control PMax queries. Now apply campaign-level negatives and shared lists directly, read the PMax search terms report, and exclude irrelevant themes.
- **Exceptions and failure modes:** No effect on Display, YouTube, Gmail, Discover or Maps placements. PPC Land reported conflicting limit figures, so treat 10,000 per campaign (Google, via SEL) as the reference.
- **Signals in data:** PMax search terms report themes that persist after negatives were added suggest they are coming through non-search inventory or through synonyms not covered.
- **Sources:** [Negative keywords in Performance Max campaigns](https://support.google.com/google-ads/answer/15726455?hl=en) (checked 2026-10-13); [Search Engine Land: Google Ads expands PMax negative keyword limits (11 Mar 2025)](https://searchengineland.com/google-ads-expands-negative-keyword-limits-pmax-453154) (checked 2026-10-13); [Google: Unlock more visibility and control in PMax (Aug 2025)](https://support.google.com/google-ads/answer/16451273) (checked 2026-10-13)

### PLT-KW-022 · Building negatives with blast-radius thinking and n-grams
- **Claim:** Experts aggregate search-term performance by 1-, 2- and 3-word n-grams to find words that waste spend across many low-volume queries, then add each as a negative at the narrowest scope and loosest match type that still blocks the waste. An account with a million search terms often has only 30,000–50,000 n-grams.
- **Evidence type:** practitioner (method) + inference (blast-radius framing)
- **Confidence:** medium
- **How it works:** A single word's cost aggregates across thousands of individually insignificant queries, which also partly offsets privacy hiding (the visible part of a pattern stands for the hidden part). Geddes's example thresholds are "Clicks > 150 and conversions = 0", sorted by cost, or high CPA with clicks > 150. These are account-dependent, not rules. "Blast radius" = the share of *converting* queries a candidate negative would also block. Before adding it, check the candidate against all converting search terms and active positive keywords.
- **When it matters / how experts use it:** Choose scope (ad group < campaign < list < account) and match type (exact < phrase < broad) by blast radius. Prefer phrase negatives on multi-word concepts, and broad on unambiguous single words ("jobs", "salary", "free" for paid services). Consider routing into a new ad group instead of negating a term with mixed intent.
- **Exceptions and failure modes:** Fractional data-driven-attribution conversions make terms look bad or good misleadingly. Words with dual meanings (e.g. "conventional" in mortgages) need context. Low-volume accounts rarely reach thresholds, so rely on semantic judgment rather than statistics.
- **Signals in data:** n-grams with high cost and zero conversions across many terms. Impression or conversion drops after negative additions, which signal blast-radius errors.
- **Sources:** [Adalysis (Brad Geddes): N-gram analysis (Apr 2025, updated Mar 2026)](https://adalysis.com/blog/n-gram-analysis-the-secret-to-scalable-search-term-management-in-google-ads/) (checked 2026-10-13); [About negative keywords](https://support.google.com/google-ads/answer/2453972?hl=en) (checked 2026-10-13)

### PLT-KW-023 · Brand lists: inclusions, exclusions and how brand matching works
- **Claim:** Brand lists are account-level lists of entities from Google's brand library, applied to campaigns. **Brand exclusions** (Search: all match types and DSA from 2024; PMax: Search and Shopping inventory) stop serving on queries "associated with" the brand, including misspellings, variants and other languages. **Brand inclusions** (Search only) restrict a campaign to queries about the listed brands. Exclusions override inclusions. Since 27 May 2025, brand inclusions are managed through AI Max, and adding a *new* brand list requires AI Max on that campaign. **(changed 2025-05)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Matching is entity-based using the newest broad match model. For example, "YouTube" matches Korean, Thai, Persian and Hebrew variants. Variants sharing a word are captured by the base name. Parent and child brands with no common word (Google, YouTube, Alphabet) need separate entries. Product names count as brands if they dominate packaging. Ad-group inclusions override campaign inclusions. Brands can be requested if they have a logo, trademark, domain, dominant product name or (for SMBs) a business name.
- **When it matters / how experts use it:** Brand campaign: broad keywords plus a brand inclusion = brand-only coverage across spellings and languages without listing every variant. Non-brand campaigns and PMax: brand exclusion of own brand to keep brand traffic in the brand campaign and stop non-brand performance being inflated by brand. Competitor exclusion where competitor traffic is unwanted.
- **Exceptions and failure modes:** "Often, but not always" captures all traffic, so it is not exhaustive. Small or local brands may not be in the library. Existing negatives matching the brand will conflict with inclusions and "may cause a reduction in performance". Inclusions cut non-brand reach in campaigns that served both.
- **Signals in data:** Brand queries in non-brand or PMax search terms reports (a missing exclusion). Brand campaign impression share drops after inclusion with leftover brand negatives.
- **Sources:** [About brand settings for Search and Performance Max](https://support.google.com/google-ads/answer/13721847?hl=en) (checked 2026-10-13); [Apply brand inclusions to Search campaigns](https://support.google.com/google-ads/answer/14453047) (checked 2026-10-13); [Google: query matching updates (June 2024)](https://support.google.com/google-ads/answer/15070437?hl=en) (checked 2026-10-13)

### PLT-KW-024 · Brand exclusion vs negative keyword: choosing the tool
- **Claim:** Use brand exclusions to block a brand *entity* across spellings, languages and product names. Use negative keywords to block specific strings precisely, or brands not in the library. Brand exclusions are coarser (entity-level, model-judged). Negatives are literal (plus misspellings) but don't cover synonyms or other languages.
- **Evidence type:** inference (from documented behaviour)
- **Confidence:** medium
- **How it works:** Follows from PLT-KW-018 and PLT-KW-023.
- **When it matters / how experts use it:** For a reseller or "brand + generic" business (e.g. "Bosch dishwasher repair"), a brand exclusion of "Bosch" would remove valuable queries. Use targeted negatives instead, or no exclusion. For own-brand separation from PMax and non-brand Search, the brand exclusion is the default.
- **Exceptions and failure modes:** An entity exclusion can catch ambiguous common-word brands (e.g. a brand named after a generic noun). Google hasn't documented how it handles generic-word brand names.
- **Signals in data:** Generic queries disappearing after a brand exclusion of a common-word brand.
- **Sources:** [About brand settings for Search and Performance Max](https://support.google.com/google-ads/answer/13721847?hl=en) (checked 2026-10-13); [About negative keywords](https://support.google.com/google-ads/answer/2453972?hl=en) (checked 2026-10-13)
- **Open questions:** How brand exclusions treat brands that are dictionary words.

### PLT-KW-025 · Keyword Planner search volume: exact-only, close variants pooled, often ranged
- **Claim:** "Avg. monthly searches" is the average searches for a keyword *and its close variants*, by default over 12 months. It is shown the same for all match types, because historical stats are exact-match only. Accounts with low spend may see only ranges (0, 1–100, 100–1K, 1K–10K, 10K–100K, 100K–1M, 1M+), a policy since 2016. Grouping of variants (plurals, abbreviations, misspellings) is inconsistent.
- **Evidence type:** documented + practitioner
- **Confidence:** high (definitions); medium (range policy details today)
- **How it works:** Pooled variants mean that summing "keyword" and "keywords" double-counts. Very low-volume or sensitive keywords aren't discoverable or forecastable.
- **When it matters / how experts use it:** Use volume to size and prioritise themes, not as a traffic promise. Never add up close-variant volumes. Long-tail volumes shown as 0 or "-" still get real traffic (see PLT-KW-028 for how the platform treats them). Combine with search terms data, which is real demand for this account.
- **Exceptions and failure modes:** Ranged data hides seasonality and order of magnitude within a bucket. Volume ignores AI Mode and Overview behaviour shifts.
- **Signals in data:** Identical volumes for singular and plural, which means they are pooled.
- **Sources:** [Keyword Planner: historical metrics vs forecasts](https://support.google.com/google-ads/answer/3022575?hl=en) (checked 2026-10-13); [Search Engine Land: Google throttling Keyword Planner data for low-spending accounts (Aug 2016)](https://searchengineland.com/google-officially-throttling-keyword-planner-data-low-spending-adwords-accounts-255795) (checked 2026-10-13); [Search Engine Land: What the heck is going on with Keyword Planner?](https://searchengineland.com/heck-going-google-keyword-planner-253062) (checked 2026-10-13)
- **Open questions:** The current spend threshold for exact rather than ranged volumes is undocumented.

### PLT-KW-026 · Keyword Planner bid ranges, competition and forecasts: what they actually mean
- **Claim:** "Top of page bid (low range)" approximates the 20th percentile, and "(high range)" the 80th percentile, of top-of-page bids advertisers historically paid for ads shown at the top, over the last 30 days. "Competition" is the number of advertisers showing on the keyword *relative to all keywords* for the location (low/medium/high), not auction price pressure. Forecasts account for bid, budget, seasonality and match type and are refreshed daily from the last 7–10 days. Historical metrics account for none of these.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Bid ranges reflect *bids that won top placement*, not CPCs paid. Actual CPC under second-price-like pricing and Smart Bidding can be lower or higher.
- **When it matters / how experts use it:** Use the high range as a rough ceiling estimate for budget feasibility (e.g. daily budget ≥ several clicks at the high range for a lead-gen niche). Expect real CPCs to differ by device, time, location and Quality Score. Re-check forecasts often, since they move with the last 7–10 days.
- **Exceptions and failure modes:** Thin-data keywords have unstable ranges. "Competition" is often misread as bid competitiveness.
- **Signals in data:** Actual avg CPC versus the planner range after launch. A large gap suggests a Quality Score or Ad Rank threshold difference.
- **Sources:** [Keyword Planner: historical metrics vs forecasts](https://support.google.com/google-ads/answer/3022575?hl=en) (checked 2026-10-13); [About Keyword Planner](https://support.google.com/google-ads/answer/7337243?hl=en) (checked 2026-10-13)

### PLT-KW-027 · Keyword discovery: ideas from URL, search term mining and planner limits
- **Claim:** Keyword Planner can generate ideas from a website URL by reading on-site content (but not hyperlink text). Very low-volume and sensitive keywords aren't discoverable. In practice the most reliable discovery source is the account's own search terms report and insights (real demand), followed by planner ideas and competitor URLs.
- **Evidence type:** documented (URL behaviour) + practitioner (prioritisation of sources)
- **Confidence:** medium
- **How it works:** A URL seed reflects how Google reads the page, which loosely previews what keywordless and AI Max matching might infer from the same landing page.
- **When it matters / how experts use it:** Mine converting search terms and promote them to exact keywords (routing and bid control). Mine non-converting n-grams for negatives. Run the planner on your own landing pages to see which themes Google associates with them. Unexpected themes show where keywordless matching may drift.
- **Exceptions and failure modes:** Planner ideas skew to head terms. Very new products show no volume.
- **Signals in data:** Converting search terms not yet present as keywords.
- **Sources:** [About Keyword Planner](https://support.google.com/google-ads/answer/7337243?hl=en) (checked 2026-10-13); [Adalysis: N-gram analysis](https://adalysis.com/blog/n-gram-analysis-the-secret-to-scalable-search-term-management-in-google-ads/) (checked 2026-10-13)

### PLT-KW-028 · Low search volume status and zero-impression pausing
- **Claim:** "Low search volume" is given to keywords with very little or no search history on Google, based on worldwide volume over the past 12 months. Such keywords are inactive and won't trigger ads, are rechecked regularly (about weekly), and reactivate automatically if volume rises "even a small amount". The status is unrelated to Quality Score, bid or ads, and doesn't harm the account. Separately, since March 2024 Google auto-pauses ad groups with zero impressions for 13 months.
- **Evidence type:** documented + practitioner
- **Confidence:** high
- **How it works:** A more general keyword (e.g. "blue bicycles") can still trigger ads for the long specific query. A low-volume exact keyword also loses identical-match priority (PLT-KW-007).
- **When it matters / how experts use it:** Don't build granular exact-only long-tail structures (SKAG-style) in niche or local markets, where many keywords will be inactive. Cover the long tail with phrase or broad parents plus negatives. Low-volume status on a core term in a small market is a hint to use a broader match type.
- **Exceptions and failure modes:** The status is global, not per-location, so a locally popular term can still pass, while a niche B2B term may be inactive everywhere.
- **Signals in data:** Many keywords with "Low search volume" status. Ad groups paused for zero impressions.
- **Sources:** [Low search volume](https://support.google.com/google-ads/answer/2616014?hl=en) (checked 2026-10-13); [How Google Ads prioritizes keywords](https://support.google.com/google-ads/answer/7502501?hl=en) (checked 2026-10-13); [Navah Hopkins, SEJ: impact of zero-impression keywords/ad groups (Apr 2024)](https://www.searchenginejournal.com/what-is-the-impact-having-zero-impression-google-ad-keywords-ad-groups/510252/) (checked 2026-10-13)

### PLT-KW-029 · Classifying search intent for keyword strategy
- **Claim:** A useful working taxonomy has two axes. *Funnel intent*: navigational (a specific site or brand), informational (learn), commercial investigation (compare, best, reviews) and transactional (buy, book, hire, price, near me, now). *Ownership*: own brand, competitor brand, generic. Add modifiers for local intent and urgency. Match type, bid target, landing page and negatives should differ by class.
- **Evidence type:** practitioner + inference; google data for local and urgency trends (dated)
- **Confidence:** medium (taxonomy is a heuristic; Google matching already uses inferred intent)
- **How it works:** Google's data (US, 2015–2017, mobile): "near me" + "can I buy/to buy" searches grew over 500%, "near me now" over 150%, and "near me today/tonight" over 900%. Users also increasingly dropped location qualifiers because the device supplies location. Google's matching infers local intent from implied context, and AI Max's "locations of interest" targets geographic intent explicitly.
- **When it matters / how experts use it:** Transactional and urgent local terms ("emergency plumber", "open now") get exact or phrase keywords, the highest bids and call-focused assets. Informational terms ("how to fix") get negatives, or a separate low-target campaign if the business sells to DIY-ers. "Near me" doesn't need to be a keyword in most cases (location targeting and implied intent cover it), but keep it if search terms show it converts differently. Separate brand, competitor and generic into different campaigns, so budgets, targets and reporting aren't blended.
- **Exceptions and failure modes:** Intent is probabilistic. "Cost of X" can be research or purchase-ready depending on the vertical. Think with Google figures are from 2015–2017 and shouldn't be cited as current growth.
- **Signals in data:** CVR by modifier n-gram ("how", "best", "near me", "price", "emergency") reveals each account's intent ladder.
- **Sources:** [Think with Google: "near me" searches (May 2018)](https://business.google.com/uk/think/marketing-strategies/near-me-searches/) (checked 2026-10-13); [AI Max for Search (locations of interest)](https://support.google.com/google-ads/answer/15910187?hl=en) (checked 2026-10-13)

### PLT-KW-030 · Trademark rules: bidding on competitor names vs using them in ads
- **Claim:** Google doesn't restrict trademarks used as **keywords**, so bidding on competitor brand names is allowed under Google policy. Google restricts trademark use in **ad text** only after a trademark owner complaint is reviewed. It restricts use by a direct competitor, or use that is confusing or misleading, unless an exception applies: authorised resellers or sales pages for the trademarked goods, informational sites about them, or descriptive use in the ordinary meaning.
- **Evidence type:** documented
- **Confidence:** high (Google policy); local law can impose more
- **How it works:** Complaints are country- and industry-specific and target specific advertisers by URL. Restrictions then apply on an ongoing basis to ads using the same second-level domain. A trademark in the display URL's second-level domain isn't restricted. Violations get a warning at least 7 days before any suspension.
- **When it matters / how experts use it:** Competitor campaigns: keywords OK, ad text should not name the competitor (it may be disapproved if they have filed a complaint, and it risks legal exposure). Write differentiation-based copy. Resellers and repairers ("Samsung TV repair") can use the brand descriptively when the landing page clearly supports that use.
- **Exceptions and failure modes:** Google policy isn't legal clearance. Some jurisdictions and courts have treated competitor-keyword bidding differently, and Google says it "abide[s] by local trademark laws". Bidding on a competitor's brand often triggers retaliation or bidding wars (practitioner observation).
- **Signals in data:** Ads "Approved (limited)" with a trademark reason. Low Quality Score and high CPC on competitor terms, which is typical because expected CTR and relevance are low (practitioner).
- **Sources:** [Google Ads policy: Trademarks](https://support.google.com/adspolicy/answer/6118?hl=en) (checked 2026-10-13)

### PLT-KW-031 · Competitor-term campaigns: what to expect
- **Claim:** Competitor-name keywords usually show low expected CTR, low Quality Score, high CPCs and low conversion rates, because most searchers want the competitor itself (navigational intent). Their value is mostly defensive or comparative and must be judged on incremental CPA, not volume.
- **Evidence type:** practitioner + inference
- **Confidence:** low-medium (widely reported; no opened dataset quantifies it)
- **How it works:** Navigational intent for another brand means few clicks and poor ad relevance. Ad Rank thresholds and Quality Score raise the price.
- **When it matters / how experts use it:** Keep competitors in their own campaign with a separate target and budget cap. Exclude competitor brands from generic broad, PMax and AI Max campaigns via brand exclusions if that traffic is unwanted. Under AI Max or PMax, competitor queries can appear without competitor keywords.
- **Exceptions and failure modes:** In fragmented local services (plumbers, locksmiths), searchers often treat a competitor's name as a generic, and conversion rates can be reasonable.
- **Signals in data:** Competitor names appearing in non-brand or PMax search terms. Competitor-campaign CPA many times the generic CPA.
- **Sources:** [About brand settings for Search and Performance Max](https://support.google.com/google-ads/answer/13721847?hl=en) (checked 2026-10-13); [Google Ads policy: Trademarks](https://support.google.com/adspolicy/answer/6118?hl=en) (checked 2026-10-13)
- **Open questions:** No independent dataset on competitor-term CPA vs generic was opened for this file.

### PLT-KW-032 · The shift toward keyword-less targeting
- **Claim:** Query targeting has been moving from keyword lists to inferred intent: DSA (landing pages) → PMax (search themes as optional signals, 25 → 50 per asset group in 2025) → AI Max keywordless matching (2025) → forced migration of legacy broad, ACA (Sept 2026) and DSA (Feb 2027) into AI Max. Advertiser spend follows: broad match is now the largest match type by spend in Optmyzr's 30,000-account sample, and exact's spend share fell about 9.5 points from 2022 to 2026. **(changed 2025-2026)**
- **Evidence type:** documented + study
- **Confidence:** high (direction)
- **How it works:** Keywordless and expansion systems learn from landing pages, assets, keywords and user context. The advertiser's inputs become *signals and boundaries* rather than targeting.
- **When it matters / how experts use it:** The strategist should invest in what steers keywordless matching: landing page content and URL exclusions, clean conversion values, negatives and brand lists, and exact keywords for must-route queries. It should treat keyword lists as one input among several.
- **Exceptions and failure modes:** Regulated, low-volume, high-ticket B2B and local niches still benefit from tight exact and phrase control, since there is little data to learn from and the cost of a wrong match is high.
- **Signals in data:** Rising share of spend in AI Max, keywordless and PMax rows.
- **Sources:** [Optmyzr (May 2026)](https://optmyzr.com/blog/google-ads-match-type-performance) (checked 2026-10-13); [Google: DSA upgrade to AI Max 2026](https://business.google.com/us/accelerate/announcements/dsa-upgrade-to-ai-max-2026/) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13)

### PLT-KW-033 · When exact still wins, when broad and AI Max work
- **Claim:** Exact (and phrase) are the better default when conversion data is thin (few conversions a month, a practitioner rule of thumb that varies widely), when conversion value is unreliable, when budget is constrained, when the market is local or niche, when the wrong match is costly or regulated, and for brand. Broad and AI Max are more likely to pay off when Smart Bidding has ample, value-weighted conversion data, budget has headroom, the landing pages are tightly themed and negatives and brand lists are maintained. Even then, keep exact keywords for priority routing of core terms.
- **Evidence type:** inference + practitioner, grounded in documented mechanisms (PLT-KW-003, -006, -009) and studies (PLT-KW-004, -012)
- **Confidence:** medium
- **How it works:** Expansion's marginal queries are less efficient on average. Only accurate auction-time bidding and enough data turn them profitable. Identical-match priority means exact keywords still route traffic deterministically, even in broad-heavy accounts.
- **When it matters / how experts use it:** A common expert structure is exact keywords for proven money terms (routing and copy control), plus phrase or broad (or AI Max) in the same theme for discovery under Smart Bidding, with negatives at the right scope and a weekly search-term and n-gram review. Promote winners to exact and negate losers. Verify every change with campaign experiments.
- **Exceptions and failure modes:** No universal conversion threshold exists. Any "30 or 50 conversions a month" rule is a heuristic, and the right volume depends on conversion lag, value variance and budget.
- **Signals in data:** Broad or AI Max increment CPA versus target in an experiment. Share of hidden spend. Proportion of non-converting expansion terms.
- **Sources:** [Your guide to broad match](https://support.google.com/google-ads/answer/12159290?hl=en) (checked 2026-10-13); [Optmyzr study (2023)](https://optmyzr.com/blog/optmyzr-study-broad-match-bidding) (checked 2026-10-13); [How Google Ads prioritizes keywords](https://support.google.com/google-ads/answer/7502501?hl=en) (checked 2026-10-13)

---

## Common mistakes and misleading metrics
- **"Exact means exact."** Since 2018–2021, exact matches same-meaning paraphrases, and under AI Max an exact keyword can seed broad and keywordless expansion (about 29% of exact impressions in one 2026 sample). Check the match-type label, not the keyword's syntax.
- **Comparing match-type CPA cross-sectionally.** Exact looks best partly because it holds the best-known terms. Use experiments and marginal CPA.
- **Keyword-level "exact performance" in AI Max campaigns** blends AI Max traffic into exact and phrase keyword rows.
- **Treating the search terms report as complete.** Often 20–45% of spend or clicks is hidden, and some AI-surface rows are approximations of intent. Negatives built from visible rows cover only part of the problem.
- **Assuming negatives catch plurals and synonyms.** They catch misspellings and casing only.
- **Account-level negatives used for "probably never" terms.** One bad entry starves brand or PMax account-wide.
- **Summing Keyword Planner volumes of variants** (they're pooled), and reading "Competition" as CPC pressure.
- **Reading top-of-page bid ranges as expected CPCs.** They are 20th and 80th percentile winning *bids* at top placement.
- **Blaming PMax cannibalisation while the Search campaign is budget-limited.** Budget-limited Search hands even exact queries to PMax.
- **Month-over-month comparisons across the Sept 2026 AI Max migration** without splitting by each campaign's migration date.
- **Brand traffic inside non-brand or PMax results** inflating "non-brand" ROAS when brand exclusions are missing.
- **Building SKAG-style exact long-tail in niche markets.** Many keywords go "Low search volume" and inactive.
- **Naming competitors in ad text** because bidding on their names is allowed. Ad text is restricted after a complaint.

## Unresolved questions
- What share of searches now goes through AI-surface paths (AI Mode, Overviews, Lens, autocomplete), where identical-match priority doesn't apply and search terms are approximated? Can approximated rows be identified?
- Does Marvin's "any match type" statement on Search vs AI Max/PMax precedence mean identical matches only? How often does PMax win non-identical queries against eligible Search keywords?
- Does AI Max expansion off an exact keyword bid only when cheaper than the keyword's own auction (Google employee claim), or simply add queries (smec reading)?
- What is the actual privacy threshold for search terms? Is the reported PMax "fewer than 50 unique searches in 90 days" label documented anywhere?
- Is the broad-match signal set (user history, landing pages, other keywords) used identically without Smart Bidding?
- How do brand exclusions handle brands named with common dictionary words?
- What is the current spend threshold for exact vs ranged Keyword Planner volumes?
- Performance of AI Max and broad in lead gen and local services (most published data is ecommerce).
- What were the post-migration (Sept 2026) effects in accounts auto-upgraded from the broad match setting? No public dataset yet.
- Pages that couldn't be opened in this pass: the Google search terms insights Help page (answer 11386431), the Google Ads API PMax search terms doc, and the 2018 SEL article on same-meaning exact close variants. Re-verify those details in a later pass.
