---
area: platform
topic: structure, targeting, networks and budgets (Search)
checked: 2026-10-13
owner: research
---
# Search campaign structure, targeting, networks and budgets

This file covers how a Search campaign is built and constrained: campaign and ad group structure, location, language, device, schedule and audience settings, network choices (Search Partners, Display expansion), budgets and pacing, and impression share diagnostics. The single most important idea: **a campaign is a container for settings that cannot vary inside it (budget, networks, locations, schedule, bid strategy and target)**. Split campaigns only when one of those has to differ, and otherwise let query-level Smart Bidding work on pooled data. Several settings changed in 2025-2026 and older advice will be wrong about them: language targeting was removed from Search (Sept 2026), budget pacing for day-of-week schedules changed (rolled out from March 2026, general date June 1, 2026), campaign total budgets were added, Search Partner placement reporting arrived (Aug 2025), and audience minimums dropped to 100 users.

---

## A. Structure

### PLT-STR-001 · A campaign is the unit of settings; split only when a setting must differ
- **Claim:** Budget, networks, locations, ad schedule, bid strategy and target are set at the campaign level, so a new campaign is justified when one of these has to differ. Ad groups exist to group keywords, ads and landing pages around one theme.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google's help says a campaign "consists of a collection of ad groups" and that campaign-level choices cover spending limits, networks, locations and other top-level settings. Its example: if shirts and pants need different budgets, create two campaigns. If ads share a budget and locations, one campaign is enough. Google also suggests separate campaigns for high-performing cities so that bids and budgets can be raised there.
- **When it matters / how experts use it:** Before adding a campaign, write down which campaign-level setting will differ. If none does (same budget pool, geo, target, schedule, network), use an ad group instead. Typical valid reasons are a different CPA/ROAS target (margin or lead value differs), a budget that must be protected (brand), a geo with different economics, a different network policy, or a different schedule. Google also warns that reorganizing later "wipes out" accumulated data, so the structure should be decided before scaling.
- **Exceptions and failure modes:** Portfolio bid strategies can share one target across campaigns, so a campaign split does not always fragment bidding. Reporting needs (for example client-level P&L by product line) can justify a split even when settings are identical, but that split costs budget flexibility.
- **Signals in data:** Several campaigns with identical settings and targets, each budget-limited while siblings underspend, means the split is fragmenting budget for no reason.
- **Sources:** [Organize your account with ad groups](https://support.google.com/google-ads/answer/6372655) (checked 2026-10-13); [Refine your location targeting](https://support.google.com/google-ads/answer/2404184) (checked 2026-10-13)

### PLT-STR-002 · Smart Bidding learns at query level across the account, which weakens the case for fine segmentation
- **Claim:** Smart Bidding sets bids per auction from signals including the actual query, device, physical location, location intent, time, remarketing list membership, browser, OS, language and Search Partner placement. It can use data from all campaigns, and Google says there is no need to segment by match type to help it optimize.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google says "Smart Bidding can optimize based on data from all of your campaigns", so even new campaigns benefit. Its 2021 bidding guide says algorithms "aren't limited by where a keyword lives in your account structure" and that stacking manual adjustments "doesn't account for the interacting effects" of signals. Splitting a campaign by device, hour or city to bid differently mostly duplicates what auction-time bidding already does.
- **When it matters / how experts use it:** Do not create device, geo-city or daypart campaigns only to bid differently. Split when the business needs a different target, budget or message. For evaluation Google recommends windows with at least 30 conversions (50 for Target ROAS). That is an evaluation guide, not an eligibility rule.
- **Exceptions and failure modes:** Shared learning does not mean shared targets. One tCPA across lines with very different lead values over-bids on low-value lines and under-bids on high-value ones. Fix this with conversion values or separate targets, not by consolidating blindly. Query-level learning also cannot overcome bad conversion data.
- **Signals in data:** Many small campaigns each with fewer than ~30 conversions per evaluation window and volatile CPA, or bid strategies stuck in "Learning" after frequent composition changes (adding or removing campaigns or keywords triggers learning).
- **Sources:** [About Smart Bidding](https://support.google.com/google-ads/answer/7065882?hl=en) (checked 2026-10-13); [Setting Smarter Search Bids, Google 2021 PDF](https://services.google.com/fh/files/misc/setting_smarter_search_bids_2021.pdf) (checked 2026-10-13); [Bid strategy statuses](https://support.google.com/google-ads/answer/6263057) (checked 2026-10-13)

### PLT-STR-003 · Consolidation vs segmentation: there is no proven universal "winning" structure
- **Claim:** Google's consolidation guidance (often called "Hagakure" in agency decks, and "Power Pack" for its AI-campaign bundle) is best treated as one strong default. Practitioner data finds no single structure that wins across accounts. Consolidation helps mainly where data or budget is fragmented.
- **Evidence type:** practitioner (plus inference)
- **Confidence:** medium
- **How it works:** Consolidation pools conversions, so bidding and ad rotation see more data, and budget moves automatically to where the auctions are. Segmentation buys control: separate targets, budgets, reporting, ad copy and landing pages. Optmyzr's 2023 within-account study (about 2,600 accounts) found exact match beat broad on CPA in about 71% of accounts but not all, and the author said there is no conclusive winning structure. Match-type-split campaigns often lost impression share to rank and budget, and consolidation was suggested as the mitigation.
- **When it matters / how experts use it:** Start consolidated by theme and economics. Split when (a) targets differ materially, (b) one part must have guaranteed budget (brand, a hero product), (c) geos differ in economics or legal rules, (d) intent stage differs enough to need different landing pages or offers, or (e) a split is needed to run a clean experiment. Re-merge when a segment cannot reach evaluation volume.
- **Exceptions and failure modes:** Over-consolidation hides losers inside averages: one campaign with a blended tROAS can spend heavily on a low-margin category. Google's public Hagakure/Power Pack materials could not be opened in this session, so their specific thresholds (such as impressions per ad group per week) are **not verified** here and must not be quoted as rules.
- **Signals in data:** Consolidation candidates: many campaigns budget-limited while siblings underspend, ad groups with few impressions per week, and identical targets across campaigns. Segmentation candidates: a single campaign whose segment-level CPA/ROAS spread (by category or geo) is wide and stable over time.
- **Sources:** [Optmyzr study: broad match and bidding (Navah Hopkins, 2023, updated 2026)](https://www.optmyzr.com/blog/optmyzr-study-broad-match-bidding/) (checked 2026-10-13); [About Smart Bidding](https://support.google.com/google-ads/answer/7065882?hl=en) (checked 2026-10-13)
- **Open questions:** Google's current official consolidation thresholds; whether any independent study isolates the structure effect from the effect of bid strategy and match type.

### PLT-STR-004 · Ad groups are themes; overlapping ad groups do not bid against each other, and Google picks among them
- **Claim:** Only one keyword or ad group from the account can enter an auction for a given query. Google picks it by preferring an exact keyword identical to the query, then phrase or broad keywords identical to the query, then AI-based relevance (query meaning against the ad group's keywords and landing pages), and finally the highest Ad Rank.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** "Identical" includes spell corrections but not plurals or synonyms. Where no keyword is identical, "only the most relevant ad and asset groups are considered". DSA, keywordless AI Max ad groups and PMax asset groups without search themes compete on Ad Rank. Targeting exclusions, budget restriction, disapprovals and low search volume can stop the preferred ad group from serving. For Lens, AI Mode, AI Overviews and autocomplete searches, keywords "may not automatically be prioritized."
- **When it matters / how experts use it:** Build ad groups so that each has one clear meaning, with keywords, ads and the landing page all agreeing. That makes the relevance step select the intended ad group. Use exact keywords identical to high-value queries to force routing (for example brand terms into the brand campaign). Read the search terms report by ad group to confirm routing.
- **Exceptions and failure modes:** A budget-limited campaign may not trigger its preferred keyword, so traffic leaks to another campaign. Single-keyword ad groups (SKAGs) no longer guarantee control, because close variants and AI relevance cross ad group lines.
- **Signals in data:** The same search term showing in several ad groups or campaigns. Brand queries appearing in non-brand or PMax campaigns. A "low search volume" status on the keyword you expected to win.
- **Sources:** [About how Google chooses keywords and ad groups (AI-based prioritization)](https://support.google.com/google-ads/answer/2756257?hl=en) (checked 2026-10-13); [Organize your account with ad groups](https://support.google.com/google-ads/answer/6372655) (checked 2026-10-13)

### PLT-STR-005 · Brand vs non-brand is the most defensible split
- **Claim:** Brand and non-brand queries usually differ by an order of magnitude in conversion rate and CPC and in how incremental they are. Putting them in one campaign under one target distorts both budget allocation and the bid target.
- **Evidence type:** inference (from documented campaign-level budget and target mechanics) plus practitioner consensus
- **Confidence:** medium-high
- **How it works:** Under one tCPA or tROAS, cheap brand conversions lower the blended CPA, so bidding can over-bid on expensive non-brand auctions while still "hitting target". The reverse is also possible: non-brand demand can use up the budget brand needs. Brand conversions are also often non-incremental (the user would have arrived organically), so judging blended efficiency overstates paid search value.
- **When it matters / how experts use it:** Run brand in its own campaign, with its own budget (rarely limited) and its own target or a Target impression share strategy. Exclude brand terms from non-brand campaigns using negatives or brand exclusions where available. Report non-brand CPA and ROAS separately. Test brand incrementality with holdouts where spend is material.
- **Exceptions and failure modes:** For very small accounts with almost no brand searches, a separate campaign adds little. Some generic queries include the brand implicitly (for example navigational queries for a product name), so classification needs a maintained term list.
- **Signals in data:** Blended CPA improves while non-brand CPA worsens. Brand impression share falling with lost IS (budget) above zero. Brand terms in non-brand search term reports.
- **Sources:** [About how Google chooses keywords and ad groups](https://support.google.com/google-ads/answer/2756257?hl=en) (checked 2026-10-13); [Organize your account with ad groups](https://support.google.com/google-ads/answer/6372655) (checked 2026-10-13)
- **Open questions:** Typical brand incrementality ranges by vertical (belongs in measurement files).

---

## B. Location and language

### PLT-STR-006 · Location option defaults: "Presence or interest" is the default, exclusions are presence-only, and old values are blocked
- **Claim:** The positive location option defaults to "Presence or interest" (people likely in, or regularly in, the area, plus people showing interest in it). "Presence" restricts to people likely in, or regularly in, the area. Exclusions apply only on presence. The old "Search interest" positive option and the "Presence or interest" negative option can no longer be set for Search.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Interest is inferred from search terms, recent presence and related content viewed. In the API, setting `positive_geo_target_type = SEARCH_INTEREST` or `negative_geo_target_type = PRESENCE_OR_INTEREST` on Search returns `SETTING_VALUE_NOT_COMPATIBLE_WITH_CAMPAIGN`. Google says most campaigns lose impressions when they switch to Presence. **(changed 2025-04)** Google's SPN announcements page says an April 2025 geo enhancement made area-of-interest and area-of-presence matching "better match advertiser expectations" and "eliminates scenarios of undesired spend caused by clicks from unexpected user locations".
- **When it matters / how experts use it:** Local service businesses (plumber, clinic, store-visit retail) usually set Presence, because a person searching "plumber Leeds" from London is rarely a customer. Travel, real estate, education and relocation services benefit from interest. Google cites +5% conversions for Travel, Real Estate and Education advertisers who switched to Presence or interest (internal data, 2022 window, not independently verified).
- **Exceptions and failure modes:** "Regularly present" still includes commuters and frequent visitors under Presence. Presence does not equal "physically there right now". Google says accuracy is best effort and "100% accuracy is not guaranteed".
- **Signals in data:** Matched-locations report showing conversions or clicks from outside the service area. Calls or leads from out-of-area customers.
- **Sources:** [About advanced location options](https://support.google.com/google-ads/answer/1722038) (checked 2026-10-13); [Target ads to geographic locations](https://support.google.com/google-ads/answer/1722043) (checked 2026-10-13); [Search Partner Network announcements (geo enhancement April 2025)](https://support.google.com/google-ads/answer/16286960) (checked 2026-10-13)

### PLT-STR-007 · How Google decides where a user is: signals, best effort, and "unspecified" traffic
- **Claim:** Location targeting uses "a variety of signals, including users' settings, devices, and behavior on our platform". IP address is one signal. When the IP cannot be resolved and the query shows no location interest, traffic appears as an unspecified area.
- **Evidence type:** documented (signals, unspecified areas); inference (VPN behaviour)
- **Confidence:** medium
- **How it works:** Device location (where permitted), Google account settings, past behaviour and IP are combined into a likely location. Google does not document the weighting.
- **When it matters / how experts use it:** Out-of-area clicks are expected, not a bug. Judge them by their share and conversion quality, not by their existence. For compliance-critical geo restrictions (gambling, pharmacy, licensing), add exclusions and on-site geo checks rather than relying on ad targeting alone.
- **Exceptions and failure modes:** **VPN users (inference, not documented):** a VPN changes the IP signal. If other signals (signed-in account location, device GPS) are weak, the user may be geolocated to the VPN exit country. Expect some leakage into and out of targeted areas from VPN, corporate proxies and carrier NAT. Google publishes no rate.
- **Signals in data:** Clicks from cities at VPN or data-centre hubs. Unexplained spikes in unspecified locations. Matched-location cities far outside the radius.
- **Sources:** [Target ads to geographic locations](https://support.google.com/google-ads/answer/1722043) (checked 2026-10-13); [About measuring geographic performance](https://support.google.com/google-ads/answer/2453994) (checked 2026-10-13)
- **Open questions:** Whether Google discounts or flags known VPN or proxy IPs for targeting (not documented).

### PLT-STR-008 · Location reports: targeted vs matched locations, and the distance report
- **Claim:** The Locations report has a "Targeted locations" view (performance by the locations you targeted) and a "Matched locations" view (performance by where ads matched, which "could be users' physical locations or locations of interest"). The distance report (requires location assets) measures from the location that triggered the ad to your nearest business location.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** "Most specific location" is the finest location used for matching. It can be a physical location or an interest location. The distance report can show distances beyond your radius because the trigger can be an interest location.
- **When it matters / how experts use it:** Use matched locations to decide exclusions and whether to switch to Presence. Use the distance report to set a radius (for example, conversion rate drops sharply beyond 5 miles). Under Smart Bidding, location bid adjustments do nothing (PLT-STR-012), so act through exclusions, separate campaigns with different targets, or budgets.
- **Exceptions and failure modes:** Report totals can differ from analytics and billing. Google says to use Billing reports for spend. Low-volume cities produce noisy conversion rates, so aggregate before excluding.
- **Signals in data:** A high share of matched locations that are interest-only. Distance buckets beyond the radius with real conversions (which argues for widening the radius).
- **Sources:** [About measuring geographic performance](https://support.google.com/google-ads/answer/2453994) (checked 2026-10-13)

### PLT-STR-009 · Radius, location groups and exclusions
- **Claim:** The minimum radius is 1 km, and very small radii can make ads show intermittently or not at all. Location groups can be built from places of interest, business locations (location assets) or tiered demographics. Exclusions are presence-based, and "locations of interest" cannot be used for areas excluded at campaign level.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Radius targets are checked against the user's estimated location, which is itself imprecise (PLT-STR-007). For a small radius, location uncertainty is comparable to the radius, so eligibility flickers. Google recommends targeting a country and excluding regions when you want "most of a country".
- **When it matters / how experts use it:** For local businesses, use a radius that matches realistic travel or service distance, not the smallest possible one. For multi-location businesses, use location groups based on business locations. When one campaign spans several stores, each needs its own budget control. Overlapping targets inside one campaign are fine. For location bid adjustments the most specific location wins (manual bidding only).
- **Exceptions and failure modes:** A small radius in a low-population area can starve the campaign of volume, which then shows as "low search volume" or very low impressions. Location target limits per campaign exist (see the limits page linked from Google's help, not opened here).
- **Signals in data:** Impressions near zero despite eligible keywords. The distance report concentrated at the radius edge.
- **Sources:** [Target ads to geographic locations](https://support.google.com/google-ads/answer/1722043) (checked 2026-10-13)

### PLT-STR-010 · Language targeting removed from Search campaigns (late September 2026)
- **Claim:** **(changed 2026-09)** The campaign-level language setting no longer applies to Search or AI Max for Search campaigns, nor to Google Search inventory inside PMax. Search ads "automatically match based on the language of your ads", using the query language, user language settings and preferences. AI-based ad group prioritization picks the best-matching language when several are eligible.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** API: adding or updating `CampaignCriterion.language` on Search campaigns returns `ContextError.OPERATION_NOT_PERMITTED_FOR_CONTEXT`. Existing criteria are still returned in queries but are not used for targeting. PMax keeps language targeting for YouTube, Display, Discover and Gmail. Shopping ads are unaffected. Google says no action is required.
- **When it matters / how experts use it:** The language of the ad and the landing page is now the targeting control. Campaigns split by language keep working, but the split is no longer enforced: an English-language query can be served from the Spanish campaign if that ad wins. Check that every ad and asset (including AI-generated assets) is in the intended language. Google confirmed that an auto-generated French ad could serve on an English query. Monitor search terms and matched locations after the change.
- **Exceptions and failure modes:** Brand queries that look the same across languages give little language signal. Regulated advertisers needing proof of equitable delivery by language (for example English/Spanish insurance) have no new language report. Google's API deprecation and sunset page did not mention this change when opened. The source is the Ads Developer Blog (Aug 13, 2026).
- **Signals in data:** After late September 2026, language-split campaigns showing search terms in the "wrong" language. Shifts in spend between language campaigns without any setting change.
- **Sources:** [Ads Developer Blog: Changes to language targeting in Google Ads (Aug 13, 2026)](https://ads-developers.googleblog.com/2026/08/google-ads-language-targeting-changes.html) (checked 2026-10-13); [About language targeting](https://support.google.com/google-ads/answer/1722078?hl=en-GB) (checked 2026-10-13); [SEL: Google Ads is removing language targeting from Search campaigns](https://searchengineland.com/google-ads-is-removing-language-targeting-from-search-campaigns-484831) (checked 2026-10-13); [SEJ: Google Ads is retiring language targeting in Search campaigns](https://www.searchenginejournal.com/google-is-removing-language-targeting-from-search-campaigns/585592/) (checked 2026-10-13)
- **Open questions:** Exact rollout completion date. Whether any language-level reporting will be added.

### PLT-STR-011 · Smart Bidding already bids by location; geo splits are for targets, budgets, messaging or law
- **Claim:** Smart Bidding uses physical location (down to city) and location intent as auction-time signals even when targeting is set at a broader level. Separate geo campaigns are therefore needed only when the target, budget, ad copy, landing page or legal constraints differ by geo.
- **Evidence type:** documented (signals) plus inference (structure implication)
- **Confidence:** medium-high
- **How it works:** Location is one of the signals in the bid. Location bid adjustments are ignored by tCPA, tROAS, Maximize conversions and Maximize conversion value. Geo economics (different margins, closing rates or lead values by region) are not visible to bidding unless they are encoded as conversion values or separate targets.
- **When it matters / how experts use it:** Use geo splits for (a) countries with different currencies, margins or legal rules, (b) regions with materially different lead value or capacity (for example a service area at capacity), and (c) region-specific offers or landing pages. Otherwise keep geos together and let bidding use the signal.
- **Exceptions and failure modes:** When conversion volume is low, the city-level signal is thin and bidding may not learn real geo differences. Value rules or separate targets then help more than they would in a high-volume account.
- **Signals in data:** Large, stable CPA or ROAS differences by region inside one campaign that do not shrink over 4 to 8 weeks suggest bidding cannot see the economics, so split or use value rules.
- **Sources:** [About Smart Bidding](https://support.google.com/google-ads/answer/7065882?hl=en) (checked 2026-10-13); [Setting Smarter Search Bids (PDF)](https://services.google.com/fh/files/misc/setting_smarter_search_bids_2021.pdf) (checked 2026-10-13); [About bid adjustments](https://support.google.com/google-ads/answer/2732132?hl=en) (checked 2026-10-13)

---

## C. Devices, schedule, audiences

### PLT-STR-012 · Which bid adjustments Smart Bidding respects
- **Claim:** Under Target ROAS, Maximize conversions, Maximize conversion value and Target impression share, only a **-100% device adjustment** applies. Under Target CPA, device adjustments apply "as a target adjustment" (they change the CPA target for that device, not the bid). Location, ad schedule, audience, call and demographic adjustments are ignored by all of these. Maximize clicks respects all adjustment types.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Device adjustments range from -100% to +900%. Multiple adjustments multiply, except that device and location adjustments do not stack within their own type (the ad group device adjustment replaces the campaign one unless the campaign is at -100%, and the most specific location wins). The combined total is capped at +900% and floored at -90%.
- **When it matters / how experts use it:** Set -100% on a device only for structural reasons, such as a form that does not work on mobile, a desktop-only B2B product, or call-only ads. Use a tCPA device adjustment to accept a higher CPA on a device whose conversions are worth more (for example mobile calls with a higher close rate). Do not expect audience or schedule adjustments to do anything under Smart Bidding. Remove them to avoid misleading future readers.
- **Exceptions and failure modes:** Manual CPC and Maximize clicks still use all adjustments. Excluding a device removes its data from bidding for that campaign.
- **Signals in data:** Audience or schedule bid adjustments present in a Smart Bidding campaign: they have no effect, which suggests the account history was managed manually. Device CPA gaps persisting under tCPA without a target adjustment.
- **Sources:** [About bid adjustments](https://support.google.com/google-ads/answer/2732132?hl=en) (checked 2026-10-13)

### PLT-STR-013 · Ad schedule is a hard on/off control; under Smart Bidding it is not a bid lever
- **Claim:** By default ads are eligible all day. Ad schedules restrict when ads can show. Schedule bid adjustments are ignored by Smart Bidding, which already uses the user's local weekday and time as a signal. **(changed 2026-03/06)** Day-of-week schedules now change how the daily budget paces (PLT-STR-021).
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** A schedule removes eligibility outside the chosen windows. Time-of-day value differences are learned by Smart Bidding from conversion data.
- **When it matters / how experts use it:** Use schedules for hard constraints, such as call-only or call-heavy campaigns outside staffed hours, regulated hours, or a business that cannot fulfil at certain times. Under manual or Maximize clicks bidding, schedule adjustments still work. When a schedule switches off whole days, recalculate the daily budget for the new pacing rules.
- **Exceptions and failure modes:** Cutting nights or weekends from evidence of low *last-click* conversion rate can remove early-funnel research clicks that convert later. Check conversions by click time rather than conversion time and allow for conversion lag. Schedules run in the account time zone. Google's ad scheduling page does not state this explicitly, so it is not verified here.
- **Signals in data:** Calls missed outside office hours (call reports). Weekend-off schedules plus spend that jumped after March to June 2026.
- **Sources:** [About ad scheduling](https://support.google.com/google-ads/answer/2404244?hl=en) (checked 2026-10-13); [About bid adjustments](https://support.google.com/google-ads/answer/2732132?hl=en) (checked 2026-10-13); [About Smart Bidding](https://support.google.com/google-ads/answer/7065882?hl=en) (checked 2026-10-13)

### PLT-STR-014 · Audiences on Search: Observation vs Targeting
- **Claim:** "Observation" adds an audience for reporting (and bid adjustments under manual bidding) without restricting reach. "Targeting" restricts serving to that audience. Google recommends Observation for Search. First-party segments added under Observation "will be used as signals for Smart Bidding".
- **Evidence type:** documented (Observation, Smart Bidding signal); practitioner (Targeting use cases on Search)
- **Confidence:** medium-high
- **How it works:** Under Observation, reporting is produced only where the audience overlaps your keywords' traffic. Under Targeting (Microsoft calls it "Target and bid"), ads show only to users who are both searching your keywords and in the audience.
- **When it matters / how experts use it:** Use Observation to see how remarketing, Customer Match and in-market segments perform within keyword traffic. Use Targeting for RLSA-only campaigns, meaning broader or more expensive keywords bid only for past visitors or customers. Use exclusions (for example existing customers on acquisition campaigns) to reduce wasted spend. This applies under Smart Bidding too, because exclusions restrict eligibility rather than adjust bids.
- **Exceptions and failure modes:** The current Google help page lists only Observation for Search audiences, while practitioners (SEJ, July 2025) still describe Targeting for remarketing and Customer Match on Search. The UI availability of Targeting for each segment type on Search was **not verified** in this session. In-market and affinity segments as Targeting on Search shrink reach a lot and are rarely worth it.
- **Signals in data:** Audience report on a Search campaign showing remarketing segments with much higher conversion rate: a candidate for an RLSA-only broad-keyword campaign. Very low impressions on a Targeting-mode campaign means the list is too small.
- **Sources:** [About targeting and observation settings](https://support.google.com/google-ads/answer/7365594?hl=en) (checked 2026-10-13); [SEJ: PPC audience strategy, targeting vs observation (Brooke Osmundson, 2025-07-30)](https://www.searchenginejournal.com/ppc-audience-strategy-targeting-vs-observation/430438/) (checked 2026-10-13); [Data segments for Search ads (RLSA)](https://support.google.com/google-ads/answer/2701222?hl=en) (checked 2026-10-13)

### PLT-STR-015 · Audience list minimums dropped to 100 active users; membership up to 540 days
- **Claim:** **(changed 2025-12)** Search, Display and YouTube segments need a minimum of 100 active visitors or users in the last 30 days, and customer lists have the same eligibility. Customer lists uploaded or refreshed before Feb 1, 2024 still need 1,000 matched users. Search membership defaults to 30 days, with a maximum of 540.
- **Evidence type:** documented (current help page) plus google-statement/press for timing
- **Confidence:** medium-high (thresholds); medium (dates)
- **How it works:** Lists fill within seconds of a tagged visit, but a new list can take 48 to 72 hours to fully populate. Each visit resets the membership clock. Segments unused for 540 days close automatically. Accounts that do not meet Customer Match requirements can use customer lists only in Observation and for exclusions.
- **When it matters / how experts use it:** Small local businesses can now use RLSA and Customer Match on Search (previously search lists needed 1,000). Use longer durations (90 to 540 days) for long-cycle or B2B purchases, and shorter durations for high-urgency services.
- **Exceptions and failure modes:** Help pages conflict: the RLSA page still says a segment needs "1,000 cookies" for Search. The current requirements page says 100. Press dates also conflict: Search Engine Roundtable and Search Engine Land dated the Search and YouTube change December 2025, while PPC Land's summary places related changes in 2024. A 100-user list gives Smart Bidding very little signal, so treat small-list results as noise.
- **Signals in data:** A list marked "too small to serve" on Search despite having more than 100 users: check whether it is an old customer list (pre-Feb 2024, which still needs 1,000).
- **Sources:** [How your data segments work](https://support.google.com/google-ads/answer/2472738) (checked 2026-10-13); [About your data segment compatibility](https://support.google.com/google-ads/answer/7476585) (checked 2026-10-13); [SER: Google Ads lowers active visitors lists to 100 for Search & YouTube (2025-12-24)](https://www.seroundtable.com/google-ads-lowers-customer-lists-40648.html) (checked 2026-10-13); [SEL: Google lowers audience size limits across Ads (2025-12-24)](https://searchengineland.com/google-lowers-audience-size-limits-across-ads-466816) (checked 2026-10-13); [PPC Land: thresholds to 100 users](https://ppc.land/google-slashes-audience-targeting-thresholds-to-100-users-across-all-networks/) (checked 2026-10-13); [Data segments for Search ads](https://support.google.com/google-ads/answer/2701222?hl=en) (checked 2026-10-13)
- **Open questions:** Status of similar segments (Google retired them in 2023 per widely reported coverage, but no page was opened this session) and whether any lookalike replacement applies to Search.

---

## D. Networks

### PLT-STR-016 · Google Search Partners: what it is and how it behaves
- **Claim:** Search Partners are non-Google sites and apps (site search, directories, product pages, YouTube search results and Watch pages) that show Google Search ads. They are included by default in new Search campaigns, can be switched off only for the whole campaign, and their CTR "doesn't impact your Quality Score on Google".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Partners can customize ad placement, size and style. Billing is per click. Smart Bidding treats "Search partner" as a bidding signal. For manual bids, Smart Pricing lowers bids on partner traffic. **(changed 2025-02)** Google enhanced Smart Bidding for SPN. **(changed 2026-02)** Parked domains stopped being an SPN surface from Feb 10, 2026. **(changed 2025-04)** A pre-screen brand-safety solution launched, with curated exclusion lists from DoubleVerify, IAS and Zefr.
- **When it matters / how experts use it:** Decide per campaign. Keep partners on where Smart Bidding has enough data and partner CPA or ROAS is within target. Turn them off where budget is limited and Google Search alone can absorb the budget, or where partner lead quality is poor (spam forms).
- **Exceptions and failure modes:** Google's own help page on the Search Network still says Google "doesn't provide information detailing the website where your ad was shown" outside PMax, which is out of date since August 2025. Auto-applied recommendations can switch partners back on.
- **Signals in data:** Segment by Network (with search partners). Partner CTR is typically much lower (expected, and not a quality signal on its own). Partner conversions with poor offline quality.
- **Sources:** [About the Google Search Network](https://support.google.com/google-ads/answer/1722047?hl=en) (checked 2026-10-13); [Search partners: definition](https://support.google.com/google-ads/answer/2616017) (checked 2026-10-13); [Search Partner Network announcements](https://support.google.com/google-ads/answer/16286960) (checked 2026-10-13); [About Smart Bidding](https://support.google.com/google-ads/answer/7065882?hl=en) (checked 2026-10-13)

### PLT-STR-017 · Search Partner placement transparency (2024-2026)
- **Claim:** **(changed 2025-08)** Search, Shopping and App campaigns now have full Search Partner placement reporting: site-level impressions (no clicks, cost or conversions per site) in Report editor > When and where ads showed > Content suitability. API: `detail_content_suitability_placement_view` and `group_content_suitability_placement_view`. A placement appears only if it had at least 5 impressions or any clicks, video views or conversions in the range.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** History: after Adalytics' November 2023 report alleging partner ads on objectionable and sanctioned-country sites, Google let PMax advertisers opt out of partners (Dec 2023) and gave PMax impression-level placement data from March 4, 2024. Search campaigns followed in August 2025. **(changed 2026-01)** PMax channel reporting shows an SPN split. **(changed 2026-04)** An Invalid Activity Credit report adds "Adjusted cost/clicks" for Search and PMax.
- **When it matters / how experts use it:** Use the report to find low-quality or brand-unsafe domains and exclude them (placement exclusions or pre-screen lists). Because the report is impressions only, judge partner value from network-level CPA or ROAS, not from the domain list.
- **Exceptions and failure modes:** The threshold filtering means the list is not exhaustive. There is still no per-site cost or conversion data, so you cannot calculate per-site CPA. How site exclusions apply to Search Partners (as opposed to Display placements) is described only indirectly in the pages opened; verify in the UI.
- **Signals in data:** Many impressions on app or parked-style domains. Partner spend share rising while partner conversion quality falls.
- **Sources:** [About Search Partner Network full placement reporting](https://support.google.com/google-ads/answer/17078188?hl=en) (checked 2026-10-13); [Search Partner Network announcements](https://support.google.com/google-ads/answer/16286960) (checked 2026-10-13); [PPC Land: full placement reporting for SPN (2025-08-20)](https://ppc.land/google-enables-full-placement-reporting-for-search-partner-network/) (checked 2026-10-13); [SEJ: SPN placement visibility (2025-08-20)](https://www.searchenginejournal.com/google-quietly-announces-search-partner-network-placement-visibility/554294/) (checked 2026-10-13); [eMarketer: Adalytics forced Google to give search advertisers more transparency (2024-02-27)](https://www.emarketer.com/content/adalytics-forced-google-give-search-advertisers-more-transparency) (checked 2026-10-13)

### PLT-STR-018 · Search Partner performance: highly account-dependent, judge by CPA/ROAS per campaign
- **Claim:** Partner performance varies widely across accounts. Opteo's analysis of about 10,000 accounts (2021) found median partner CPA about 7% higher than Google Search, with long tails in both directions. Google claims (Dec 2025) that advertisers with partner spend of at least 5% in unconstrained campaigns typically see about 11% more conversions (volume Smart Bidding) or about 7% more conversion value (value Smart Bidding).
- **Evidence type:** study (Opteo, vendor, observational) plus google-statement plus practitioner (Adalysis)
- **Confidence:** medium
- **How it works:** Partner inventory adds incremental auctions, often at lower CPC but lower intent. Smart Bidding prices them as a signal but does not always hit target there. Adalysis (Brad Geddes) reported cases where partner CPA was 17 times Google Search CPA, and others where partners beat Search.
- **When it matters / how experts use it:** Compare partner CPA or ROAS with both the target and Google Search CPA over a window with enough conversions. Do not use CTR or conversion rate as the decision metric. Opteo's rule: exclude only if partner CPA is worse than both the target and Search CPA, given enough clicks (minClicks ≈ expected conversions / conversion rate). Small budget-limited accounts can reasonably turn partners off by default so budget goes to Google Search.
- **Exceptions and failure modes:** Google's uplift claim is conditional ("unconstrained" campaigns) and comes from Google, not an independent source. The Opteo data predates parked-domain removal and the 2025 bidding changes. Lead-gen spam can make partner CPA look good while lead quality is poor, so use offline or qualified conversions.
- **Signals in data:** Partner CPA far above target with meaningful spend. Partner leads with high junk rates in the CRM.
- **Sources:** [Opteo: excluding search partner sites (2021)](https://opteo.com/blog/excluding-search-partners-in-opteo) (checked 2026-10-13); [Adalysis: how to evaluate search partners (Geddes, 2023, updated 2024)](https://adalysis.com/blog/how-to-evaluate-search-partners-on-google-ads-microsoft-ads/) (checked 2026-10-13); [Search Partner Network announcements](https://support.google.com/google-ads/answer/16286960) (checked 2026-10-13)

### PLT-STR-019 · Display expansion inside Search campaigns
- **Claim:** Checking "Display Network" in a Search campaign lets Google show ads on Display inventory when it predicts unused Search budget, after an exploration period, and stop if it cannot match Search cost per conversion. Google claims up to 15% more conversions at similar CPA (about 14% more value for value strategies). It does not apply to shared budgets or campaign experiments.
- **Evidence type:** documented (mechanism, Google claims)
- **Confidence:** medium (claims are Google's own)
- **How it works:** Ads are generated from the Search ads, with contextual targeting based on keywords. The overall campaign budget cap is respected, and for full-spend strategies "the majority of the budget will typically still be reserved for Search".
- **When it matters / how experts use it:** Practitioner default is off for Search campaigns (inference: it mixes Display traffic into Search metrics, impression share and search-intent reporting, and Display conversions often skew view-adjacent or low intent). If testing, use a separate campaign or experiment and judge on qualified conversions. Google's own note says experiments are excluded, so test with before/after or separate campaigns.
- **Exceptions and failure modes:** **(changed 2026-05)** Google is retiring standalone Display campaigns into Demand Gen (migration tool from June 2026, through 2027). Whether Display expansion on Search is affected was not stated in the sources opened.
- **Signals in data:** A "Display Network" row when segmenting a Search campaign by network. Clicks with very low CPC and lower conversion rate.
- **Sources:** [About Display Expansion on Search campaigns](https://support.google.com/google-ads/answer/7193800?hl=en) (checked 2026-10-13); [SEJ: Google is retiring standalone Display campaigns in favor of Demand Gen (2026-05-26)](https://www.searchenginejournal.com/google-is-retiring-standalone-display-campaigns-in-favor-of-demand-gen/575889/) (checked 2026-10-13)

---

## E. Budgets

### PLT-STR-020 · Average daily budget: 2x daily ceiling, 30.4x monthly charging limit
- **Claim:** The daily budget is an *average*. On any day a campaign may spend up to 2x it (for most campaigns), and in a calendar month you are not charged more than 30.4x it. Served cost can exceed the limits, but overdelivery is credited, so billed cost never does.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google shifts spend toward days "when you're more likely to get clicks and conversions." Billed vs served cost can be checked in the Report editor "Billed cost" report. When the budget is changed mid-month, the monthly limit becomes spend to date plus the new daily budget × remaining days.
- **When it matters / how experts use it:** Plan monthly spend as daily budget × 30.4, not × days remaining. Daily spend at 2x is normal, not a bug. To cap a hard monthly total, use campaign total budgets (new campaigns), account budgets (billing), or scripts.
- **Exceptions and failure modes:** "For most campaigns": the exceptions are not listed on the page. Frequent budget edits reset the monthly calculation and make pacing look erratic.
- **Signals in data:** Daily cost above budget on high-demand days, with lower spend on others. Served cost above billed cost (credits).
- **Sources:** [About average daily budgets](https://support.google.com/google-ads/answer/6385083) (checked 2026-10-13); [About overdelivery and your average daily budget](https://support.google.com/google-ads/answer/1704443?hl=en) (checked 2026-10-13); [Changes to budget pacing for Ad Scheduling](https://support.google.com/google-ads/answer/16913225) (checked 2026-10-13)

### PLT-STR-021 · 2026 change: campaigns that switch off days via ad schedule now pace toward the full 30.4x monthly limit
- **Claim:** **(changed 2026-03, general 2026-06)** For campaigns whose ad schedule turns off whole days of the week, pacing now "attempts to spend up to 30.4 times the average daily budget per month, regardless of ad schedule usage". Google says hour-of-day schedules are not affected. Maximum spend = (daily budget × 2) × active days if 15 or fewer active days per month; daily budget × 30.4 if 16 or more.
- **Evidence type:** documented plus google-statement
- **Confidence:** high (mechanism); medium (rollout dates)
- **How it works:** Before the change, pacing roughly matched active days (weekend-only, $100/day ≈ $800 per month). Now the same campaign can spend $200 on each of about 8 days ≈ $1,600. Google's help examples: 20 active days with a $2,000 goal now needs a daily budget of about $66, not $100. The 2x daily cap and 30.4x monthly cap are unchanged, and ads never run on switched-off days. Shared budgets follow the same behaviour.
- **When it matters / how experts use it:** For every campaign with day-off schedules, recalculate: daily budget = monthly goal / 30.4 (16 or more active days) or monthly goal / (2 × active days) (15 or fewer). Google advises against automated rules that pause campaigns on certain days.
- **Exceptions and failure modes:** Dates conflict across sources. Google's email and Ginny Marvin (reported Feb 20, 2026) said the rollout began March 1, 2026 for a first wave of notified accounts. Google's help page and SEL (Apr 22, 2026) give June 1, 2026. Treat accounts as possibly changed from March and certainly from June 2026. One commenter quoted by PPC Land called it "a showstopper for shared budgets", and Google gave no specific shared-budget guidance at that point (the help page now says shared budgets follow the same behaviour).
- **Signals in data:** Month-over-month spend jump (up to about 2x) in day-limited campaigns from March or June 2026 with no budget edits. Daily spend at or near 2x budget on every active day.
- **Sources:** [Changes to Google Ads budget pacing for Ad Scheduling](https://support.google.com/google-ads/answer/16913225) (checked 2026-10-13); [SER: budget pacing for ad scheduling updated (2026-02-20)](https://www.seroundtable.com/google-ads-budget-pacing-for-ad-scheduling-updated-40966.html) (checked 2026-10-13); [SEL: Google to change budget pacing for campaigns using ad scheduling](https://searchengineland.com/google-to-change-budget-pacing-for-campaigns-using-ad-scheduling-470214) (checked 2026-10-13); [SEL: Google changes budget pacing rules for scheduled campaigns (2026-04-22)](https://searchengineland.com/google-changes-budget-pacing-rules-for-scheduled-campaigns-475107) (checked 2026-10-13); [PPC Land: what the March 1 change actually does](https://ppc.land/google-ads-budget-pacing-with-ad-scheduling-what-the-march-1-change-actually-does/) (checked 2026-10-13); [About ad scheduling](https://support.google.com/google-ads/answer/2404244?hl=en) (checked 2026-10-13)

### PLT-STR-022 · Campaign total budgets (date-bound budgets) for Search
- **Claim:** **(changed 2026)** New Search campaigns can use a campaign total budget: one amount over a fixed period of 3 to 90 days, paced daily toward the total with no daily cap, and never charged above the total. The type cannot be changed after creation, and existing daily-budget campaigns cannot switch.
- **Evidence type:** documented plus google-statement
- **Confidence:** high
- **How it works:** The system "adjusts spending daily to attempt to spend the total budget in the remaining days." Search supports tROAS, Maximize conversion value, tCPA, Maximize conversions, Maximize clicks, Target impression share and Manual CPC. The end date can be extended. Frequent edits "can lead to uneven spend". A restrictive tCPA or tROAS can still leave budget unspent. Google (GML, May 2026) says these launched "earlier this year" for Search, Shopping and PMax, and claims a 66% average reduction in manual budget adjustments. Google also announced upcoming "demand-led pacing" for Search and Shopping that moves spend toward peak days within monthly and daily limits (no date given).
- **When it matters / how experts use it:** Use for promotions, events and fixed flights (for example a 2-week sale) where the total matters more than daily evenness. Pair with a volume strategy if full spend is the goal.
- **Exceptions and failure modes:** Because there is no daily cap, spend can be very front- or back-loaded. Interaction with shared budgets and ad schedules is not documented on the page. Availability may still vary by account (not verified per account).
- **Signals in data:** Uneven daily spend inside the flight. Unspent remainder at the end under strict targets.
- **Sources:** [About campaign total budgets](https://support.google.com/google-ads/answer/10486938?hl=en) (checked 2026-10-13); [Google Marketing Live 2026: bidding and budgeting news](https://blog.google/products/ads-commerce/bidding-budgeting-google-marketing-live-2026/) (checked 2026-10-13)

### PLT-STR-023 · Shared budgets: pooling and its traps
- **Claim:** A shared budget pools one daily amount across campaigns. Maximize-type strategies in a shared budget with other strategies show as "Misconfigured", and Google wants all campaigns in a shared budget on the same portfolio strategy. Switching campaigns into a shared budget mid-day restarts serving "as though the campaigns have spent $0".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Adding a campaign adds its budget to the pool. Allocation across campaigns is not documented. In practice the campaign that wins more auctions consumes more (inference). Display expansion's spare-budget logic does not apply to shared budgets. The 2026 schedule-pacing change applies to shared budgets too.
- **When it matters / how experts use it:** Use shared budgets only for campaigns with similar economics and priority (for example several non-brand campaigns with the same target, ideally under one portfolio strategy). Never share a budget between brand and non-brand, or between a campaign you must protect and one with unlimited demand.
- **Exceptions and failure modes:** One high-volume campaign can starve the others. The mid-day switch reset can allow up to a double day of spend.
- **Signals in data:** Unequal spend shares in a shared budget, with the strategic campaign at low impression share. A "Misconfigured" bid strategy status.
- **Sources:** [Manage a shared budget across campaigns](https://support.google.com/google-ads/answer/2517512) (checked 2026-10-13); [Bid strategy statuses](https://support.google.com/google-ads/answer/6263057) (checked 2026-10-13); [About Display Expansion on Search campaigns](https://support.google.com/google-ads/answer/7193800?hl=en) (checked 2026-10-13); [Changes to budget pacing for Ad Scheduling](https://support.google.com/google-ads/answer/16913225) (checked 2026-10-13)

### PLT-STR-024 · Budget-limited status and what raising budget actually buys
- **Claim:** "Limited: Budget constrained" means budget is stopping the strategy from bidding up enough to meet goals. Lost IS (budget) measures the share of eligible impressions missed because budget ran out. Neither metric says the missing traffic would convert at the current CPA.
- **Evidence type:** documented (definitions) plus practitioner/inference (interpretation)
- **Confidence:** medium-high
- **How it works:** When budget binds, Google throttles serving across the day. With Maximize conversions or value, the strategy spends the whole budget and picks the auctions it believes are best, so marginal budget buys auctions it valued lower. Practitioners warn that "extra budget mostly buys more of the same traffic". Check whether its marginal CPA is profitable.
- **When it matters / how experts use it:** If lost IS (budget) is high and the campaign is under target CPA, raising budget is the first lever. If it is at or over target, consider a tighter target (tCPA or tROAS) instead, which makes bidding skip lower-value auctions, or narrow keywords or geo. Small accounts that are budget-limited should cut low-yield inventory (partners, broad expansions) before adding campaigns.
- **Exceptions and failure modes:** A budget-limited campaign may not trigger its preferred keyword, so traffic leaks to other campaigns (PLT-STR-004). Budget-constrained status under target-based strategies can coexist with rank loss.
- **Signals in data:** Lost IS (budget) above about 10 to 20% plus a status showing "Limited" (practitioner range, not a rule). Spend that ends at the same hour each day (intraday exhaustion).
- **Sources:** [Bid strategy statuses](https://support.google.com/google-ads/answer/6263057) (checked 2026-10-13); [About impression share](https://support.google.com/google-ads/answer/7103314?hl=en) (checked 2026-10-13); [Relevant Audience: impression share guide (2026-10-11)](https://www.relevantaudience.com/google-ads-en/google-ads-impression-share-guide/) (checked 2026-10-13)

---

## F. Impression share

### PLT-STR-025 · Search impression share: an estimate against an estimated denominator
- **Claim:** Search IS = impressions / estimated eligible impressions. "Eligible impressions are estimated using many factors, including targeting settings, approval statuses, and quality." Metrics update within 1 to 2 days, and IS is not aggregated across campaign types.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The denominator is the set of auctions you were *eligible* for, not every search containing your keywords. Expanding keywords or geo can raise impressions while IS falls, because the denominator grew. Lost IS (budget) is available at campaign level only. Lost IS (rank) is hidden at ad group level if the budget ran out in the period. Search Partners are not included in IS (practitioner guide; consistent with Google's IS being "on the Search Network" for Google).
- **When it matters / how experts use it:** Use IS for headroom questions ("could we get more of this demand?"), and always alongside the split between lost to budget and lost to rank. Compare IS trends within a stable setup only, because changes in targeting change the denominator. Do not trust the last 1 to 2 days.
- **Exceptions and failure modes:** The API reports values below 10% as 0.0999 and lost IS above 90% as 0.9001 (stated by a practitioner guide; the API field page could not be read here). Treat these as bounds. Auction insights show no rows below 10% IS.
- **Signals in data:** IS falls after a broad-match or geo expansion while impressions rise, which is a denominator effect, not lost competitiveness.
- **Sources:** [About impression share](https://support.google.com/google-ads/answer/7103314?hl=en) (checked 2026-10-13); [Impression share: definition](https://support.google.com/google-ads/answer/2497703?hl=en) (checked 2026-10-13); [Relevant Audience: impression share guide](https://www.relevantaudience.com/google-ads-en/google-ads-impression-share-guide/) (checked 2026-10-13)

### PLT-STR-026 · Lost IS (rank) is about Ad Rank, including quality and thresholds, and can be intentional
- **Claim:** Search lost IS (rank) is the share of eligible impressions missed because of insufficient Ad Rank. Ad Rank combines bid, ad quality, thresholds and context, so rank loss is not only a bid problem. Under target-based Smart Bidding, rank loss is often the strategy deliberately skipping expensive auctions.
- **Evidence type:** documented (definition); inference/practitioner (interpretation)
- **Confidence:** medium-high
- **How it works:** If tCPA or tROAS predicts an auction cannot meet target, it bids low or not at all, and that auction counts as lost to rank. Raising the target (or loosening it) reduces rank loss. Improving ad relevance, expected CTR and landing page also reduces it for the same cost.
- **When it matters / how experts use it:** High rank loss plus on-target CPA means volume is available at a higher CPA. Decide by marginal economics. High rank loss plus off-target CPA points to quality or relevance problems. Check ad relevance and landing pages before raising bids.
- **Exceptions and failure modes:** Rank loss does not show who you lost to or why. Auction insights shows overlap with visible competitors, not their bids or budgets (unobservable).
- **Signals in data:** Lost IS (rank) rising right after a target was tightened is expected. Rising without any setting change suggests competition or quality decline.
- **Sources:** [About impression share](https://support.google.com/google-ads/answer/7103314?hl=en) (checked 2026-10-13); [Relevant Audience: impression share guide](https://www.relevantaudience.com/google-ads-en/google-ads-impression-share-guide/) (checked 2026-10-13)

### PLT-STR-027 · Top and absolute top IS vs Impr. (Top)% and (Abs. Top)%
- **Claim:** Search top IS = impressions in the top ads location / estimated eligible top impressions. Abs. top IS = impressions as the first top ad / estimated eligible top impressions. Impr. (Top)% and Impr. (Abs. Top)% are shares of *your own* impressions that were top or absolute top. **(changed 2024-03)** "Top ads" are now defined as adjacent to the top organic results: usually above them, but they can appear below for some queries.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The IS versions measure share of opportunity. The Impr.% versions measure position mix of what you won, and these can fall when bids rise, because you start entering more competitive auctions where you rank lower. The 2024 definition change did not change calculations, according to Google.
- **When it matters / how experts use it:** Use top or abs top IS (not Impr.%) for brand defence goals and Target impression share settings. A brand campaign with abs top IS well below 90% and high rank loss suggests competitor conquesting or a quality problem.
- **Exceptions and failure modes:** Because "top" can now be below organic results, a high top IS no longer guarantees above-the-fold visibility. AI Overviews and AI Mode placements complicate "position" further (out of scope here).
- **Signals in data:** Impr. (Top)% falls while top IS rises, which means you are winning more top auctions in harder SERPs.
- **Sources:** [About top and absolute top metrics (2018 announcement page)](https://support.google.com/google-ads/answer/9140484?hl=en-GB) (checked 2026-10-13); [Updates to top ads definition](https://support.google.com/google-ads/answer/14660113?hl=en) (checked 2026-10-13); [SEJ: Google updates definition of top ads (2024-03-28)](https://searchenginejournal.com/google-updates-definition-of-top-ads-in-search-results/512530) (checked 2026-10-13)

### PLT-STR-028 · Exact match IS: headroom on core queries vs broad expansion
- **Claim:** Search exact match IS is the IS on searches that exactly match your keywords or close variants, regardless of the keyword's match type. It is not available for Shopping.
- **Evidence type:** documented (definition); practitioner (use)
- **Confidence:** medium-high
- **How it works:** It isolates competitiveness on the core queries from the large, diluted denominator broad match creates.
- **When it matters / how experts use it:** If overall IS is low but exact match IS is high, the "loss" is in broad-match expansion queries, which may be low value. Review search terms rather than raising budget or bids. If exact match IS is low, you are losing the core demand, so fix budget, rank or quality first.
- **Exceptions and failure modes:** Close variants make "exact" broader than literal. It is still an estimate with the same freshness limits as other IS metrics.
- **Signals in data:** A large gap between Search IS and exact match IS after switching to broad match.
- **Sources:** [About impression share](https://support.google.com/google-ads/answer/7103314?hl=en) (checked 2026-10-13); [Relevant Audience: impression share guide](https://www.relevantaudience.com/google-ads-en/google-ads-impression-share-guide/) (checked 2026-10-13)

### PLT-STR-029 · Impression share reporting limits that change interpretation
- **Claim:** Budget-lost metrics exist only at campaign level. Since June 2022, saved reports that combine Lost IS (budget) with ad group, keyword or ad group label segments drop that column. IS values are per campaign type, and history goes back to Oct 2012 for Search.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Budget is a campaign property, so ad group or keyword attribution of budget loss is not meaningful. Rank loss can be read at lower levels unless the budget ran out.
- **When it matters / how experts use it:** Diagnose budget at campaign level and rank or quality at ad group and keyword level. When an ad group shows no rank-loss number, check whether the campaign hit budget in the range.
- **Exceptions and failure modes:** Averages over long ranges hide intraday exhaustion. Use hour-of-day spend to see when budget ran out.
- **Signals in data:** Missing columns in custom reports. Blank rank loss at ad group level.
- **Sources:** [About impression share](https://support.google.com/google-ads/answer/7103314?hl=en) (checked 2026-10-13)

### PLT-STR-030 · Structure-level diagnostic: map each symptom to the setting that controls it
- **Claim:** Most structure and targeting problems show up as one of a few patterns. Each maps to a specific campaign-level control: budget (lost IS budget, "Budget constrained"), Ad Rank or target (lost IS rank), geo (matched locations), network (segment by network), routing (search terms in the wrong campaign), and schedule pacing (spend jumps on day-limited campaigns after March to June 2026).
- **Evidence type:** inference (from the documented mechanics above)
- **Confidence:** medium
- **How it works:** Each setting operates at a specific level (campaign: budget, geo, network, schedule, strategy; ad group: theme, routing via relevance; account: audiences as signals). A symptom is usually fixed at the level of the setting that causes it.
- **When it matters / how experts use it:** Before restructuring, check (1) segment by network, (2) the matched-locations report, (3) the lost IS split, (4) bid strategy status, (5) search terms by campaign and ad group, and (6) schedules plus the 2026 pacing change. Restructure only if the fix needs a setting to differ (PLT-STR-001).
- **Exceptions and failure modes:** Conversion-tracking errors look like structure problems. Rule them out first (measurement files).
- **Signals in data:** As listed.
- **Sources:** Derived from PLT-STR-001 to 029 sources (all checked 2026-10-13).

---

## Common mistakes and misleading metrics

- **Splitting campaigns by device, hour or city to "bid differently" under Smart Bidding.** Bidding already uses those signals, and location, schedule and audience adjustments are ignored (PLT-STR-012). Splits should reflect differences in targets, budgets, messages or legal rules.
- **Treating Google's consolidation thresholds or practitioner rules (for example "30 conversions per month per campaign") as platform rules.** Google's 30 or 50 conversions is an *evaluation* guide. Eligibility does not depend on it.
- **Leaving audience or schedule bid adjustments on Smart Bidding campaigns and assuming they work.**
- **Planning monthly spend as daily budget × days remaining.** Plan at 30.4x. For day-limited schedules after March to June 2026, use the new formula (PLT-STR-021).
- **Reading "Presence or interest" out-of-area clicks as fraud, or Presence as "physically there now".**
- **Language-split campaigns after September 2026:** the setting no longer enforces anything. Ad and landing page language does.
- **Judging Search Partners by CTR or conversion rate.** Use CPA or ROAS per campaign. The SPN placement report has impressions only, so it cannot show which site is "bad" by cost.
- **Chasing impression share as a goal.** IS denominators change with targeting, rank loss can be the bidding strategy's deliberate choice, and extra budget buys marginal auctions. Impr.(Top)% can fall while you are winning more.
- **Assuming "top" means above organic.** Since March 2024 top ads can appear below the top organic results.
- **Comparing IS across campaign types or summing it.** It is not aggregated.
- **Putting brand and non-brand in one shared budget or under one target.**
- **Moving campaigns into a shared budget mid-day** (spend counter resets).
- **Trusting help pages that contradict each other:** the RLSA page still says 1,000 cookies, the Search Network page still says no partner site data. Prefer the newest dedicated page.

## Unresolved questions

1. The exact rollout timing of the ad-schedule pacing change per account (first wave March 1 vs general June 1, 2026), and whether hour-only schedules are truly unaffected in practice.
2. How language matching performs after the September 2026 removal: whether wrong-language serving increases measurably, and whether Google will add language reporting for regulated advertisers.
3. Current official Google structure thresholds (Hagakure / Power Pack documents could not be opened), and independent evidence isolating structure effects from bidding and match-type effects.
4. How Google allocates spend among campaigns inside a shared budget, and how campaign total budgets interact with shared budgets and ad schedules.
5. Whether Display expansion on Search survives the Display-to-Demand Gen migration (2026-2027).
6. Whether Search campaigns still offer audience "Targeting" mode for all first-party segment types (the help page lists only Observation for Search), and the status of similar or lookalike segments on Search.
7. How VPN and proxy traffic is geolocated, and its share of out-of-area clicks.
8. Independent (non-Google) post-2025 data on Search Partner performance after parked-domain removal and the Smart Bidding upgrades.
9. Timing and mechanics of Google's announced "demand-led pacing" for Search budgets (GML 2026, no date).
10. The API boundary values for IS (0.0999 / 0.9001) were not verified on the API field page in this session.
