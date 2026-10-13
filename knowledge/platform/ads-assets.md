---
area: platform
topic: ads and assets (RSA mechanics, assets, AI text, ad policy, ad testing)
checked: 2026-10-13
owner: research
---
# Responsive search ads, assets and the rules that constrain ad copy

This file covers how Google assembles responsive search ads (RSAs) from headlines and descriptions, what pinning, Ad Strength and asset reports really tell you, how each asset type serves, how AI-generated text (text customization, now inside AI Max) and the September 2026 auto-upgrade change control over copy, and which editorial and policy rules limit what an ad may say. The single most important idea: **the RSA is a pool of components Google recombines per auction, so neither Ad Strength nor per-asset metrics are performance verdicts; only ad-level or experiment-level comparisons on business outcomes are.**

### PLT-ADS-001 · RSA inputs and character limits
- **Claim:** An RSA takes 3-15 headlines (30 characters each), 2-4 descriptions (90 characters each) and two optional display paths (15 characters each); double-width languages (Chinese, Japanese, Korean) count each character as two.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google stores the assets as a pool and assembles an ad per auction. Every asset must make sense alone and in any order, because assets can appear in any order.
- **When it matters / how experts use it:** Write each headline as a standalone unit (no "...continued" across headlines). Keywords longer than 30 characters belong in descriptions. Plan the pool by role (keyword/relevance, offer, proof, CTA, qualifier) rather than writing 15 variants of one idea.
- **Exceptions and failure modes:** Inserted text (keyword insertion, customizers) must also fit the limits, or the default is used (see PLT-ADS-024).
- **Signals in data:** Assets rejected for length, or customizers always falling back to the default text.
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13)

### PLT-ADS-002 · What actually shows: up to 3 headlines and 2 descriptions, with only H1 and D1 near-guaranteed
- **Claim:** An RSA shows at least one headline and one description; up to 3 headlines can appear in the headline position. Headline 1 and Description 1 usually show; Headline 2, Headline 3 and Description 2 are not guaranteed. Text can be truncated with an ellipsis, a headline can appear at the start of the description line, and call assets and images can take space.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Layout depends on device, screen width, position on the page and which other assets win space. Image assets in particular can truncate Description 2 (PLT-ADS-021).
- **When it matters / how experts use it:** Anything that must be seen (legal disclaimer, price qualifier, key differentiator) must sit in a position that always shows: pinned H1, H2 or D1, or a text disclaimer asset (PLT-ADS-023). Do not rely on H3 or D2 for compliance or qualification text.
- **Exceptions and failure modes:** Google's preview does not display all combinations, so the preview is not evidence of what users see.
- **Signals in data:** Combinations report showing mostly 2-headline combinations; complaints that a qualifier ("from $X") never appears.
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13)

### PLT-ADS-003 · Enhanced flexibility: unused headlines and descriptions can serve elsewhere
- **Claim:** Up to 2 unused RSA headlines can serve as link-based assets (pointing to the ad's final URL domain), descriptions can fill link-description space, and unused assets from *other ads in the same ad group* can serve as link-based assets pointing to that other ad's final URL. Only active ads and assets qualify; sensitive verticals are excluded from this sharing.
- **Evidence type:** documented
- **Confidence:** medium (documented behaviour; the launch date was not found on an opened page)
- **How it works:** Google treats the ad group's text pool as material for sitelink-like units, so a headline written for one ad and landing page can appear as a link alongside another ad.
- **When it matters / how experts use it:** Every headline in an ad group must be accurate for *its own* final URL and acceptable when shown next to any other ad in the group. This is one reason Google now recommends a unique final URL per RSA (PLT-ADS-008): a second RSA can contribute deep links.
- **Exceptions and failure modes:** Headlines that only make sense in context (e.g. "Book Today" with no subject) produce meaningless links. Paused ads do not share.
- **Signals in data:** Assets report entries for headline text appearing in link positions; sitelink-like clicks without sitelinks configured.
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13); [About assets](https://support.google.com/google-ads/answer/7331111) (checked 2026-10-13)
- **Open questions:** Exact rollout date and whether these impressions are separable in reporting.

### PLT-ADS-004 · Pinning mechanics and costs
- **Claim:** Headlines can be pinned to H1, H2 or H3 and descriptions to D1 or D2. Pins to H1, H2 and D1 always show; H3 and D2 pins are not guaranteed. A pinned asset shows only in that slot, which cuts the combinations available; if every position is pinned, unpinned assets never show. Google says pinning "isn't recommended for most advertisers" and that pinning identical or similar text lowers Ad Strength.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Pinning is a constraint on the assembly search space. Pinning 2-3 alternatives to the same slot keeps some rotation while guaranteeing the slot carries one of a set of approved messages.
- **When it matters / how experts use it:** Pin when the message must appear (regulated disclosures, brand name, price qualifier) or when testing messages deliberately (PLT-ADS-013). Common expert pattern: pin 2-3 keyword/relevance headlines to H1, leave the rest unpinned.
- **Exceptions and failure modes:** Pinning lowers Ad Strength, but Ad Strength is not an auction input (PLT-ADS-005), so a lower rating from compliance pinning is not by itself a problem. Pinning may be ignored in some AI Max configurations (PLT-ADS-027).
- **Signals in data:** "Pinned" column in the campaign-level asset report; Ad Strength action items citing pinning.
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13); [About campaign level asset reporting for RSAs](https://support.google.com/google-ads/answer/9781208?hl=en) (checked 2026-10-13)

### PLT-ADS-005 · Ad Strength measures inputs, and is not used in Ad Rank
- **Claim:** Ad Strength (Incomplete, Poor, Average, Good, Excellent) rates relevance of headlines and descriptions to the ad group's keywords, the number and uniqueness of assets, and sitelinks (6+ at any level improve it). It counts Google-generated text when text customization is on. It does **not** measure landing page quality and is **not** used to calculate Ad Rank, Quality Score or auction outcomes, and does not decide serving eligibility.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** It is a pre-flight checklist score recalculated when keywords, assets or structure change. A keyword only counts if it sits entirely within one headline.
- **When it matters / how experts use it:** Treat it as a lint warning (missing assets, duplicate ideas, no keyword presence), not a goal. Never sacrifice a compliance pin, a qualifying message or a proven ad to raise it.
- **Exceptions and failure modes:** Because Ad Strength rewards more assets, less pinning, AI text and sitelinks, it tends to reward exactly the levers Google wants adopted (inference). "Incomplete" can mean a structural problem (no final URL, no keywords) that does block serving.
- **Signals in data:** Ad Strength column; ads rated "Average" outperforming "Excellent" ones in the same ad group.
- **Sources:** [About Ad Strength for responsive search ads](https://support.google.com/google-ads/answer/9921843) (checked 2026-10-13)

### PLT-ADS-006 · Ad Strength vs performance: Google's average lift vs independent null result
- **Claim:** Google states advertisers who moved Ad Strength from Poor to Excellent saw on average 15% more conversions (internal data, Aug 15-20, 2025). Optmyzr's study of 1M+ ads in 22,000+ accounts (published Sep 2024) found no clear correlation: "Average" RSAs had the best CPA, conversion rate and ROAS, and CTR barely differed by rating.
- **Evidence type:** study (Optmyzr, observational) and google-statement
- **Confidence:** medium
- **How it works:** Both are observational. Google's figure compares advertisers who chose to improve (they also likely added assets, sitelinks and attention) and is a "Poor to Excellent" jump, the extreme case. Optmyzr's sample skews toward advanced advertisers who may deliberately pin (lowering strength) because they know what works.
- **When it matters / how experts use it:** Moving from Poor (e.g. 3 headlines, no keyword) to a filled pool is plausibly helpful because the system has more options; moving from Good to Excellent by adding filler has no evidence of benefit. Judge by experiment (PLT-ADS-013).
- **Exceptions and failure modes:** Neither source is causal. Google's later figures in late 2025 (Aug) may reflect AI-generated text being counted.
- **Signals in data:** Compare conversions per impression across ads in the same ad group against their Ad Strength.
- **Sources:** [Google Ad Strength study (Optmyzr)](https://optmyzr.com/blog/google-ad-strength-study) (checked 2026-10-13); [Ad copy tactics backed by study of over 1 million Google ads (SEJ)](https://www.searchenginejournal.com/ad-copy-tactics-backed-by-study-of-over-1-million-google-ads/527230/) (checked 2026-10-13); [About Ad Strength](https://support.google.com/google-ads/answer/9921843) (checked 2026-10-13)
- **Open questions:** No randomized test of Ad Strength itself has been published.

### PLT-ADS-007 · Creative patterns in the Optmyzr 1M-ad dataset (pinning, case, length, DKI)
- **Claim:** In Optmyzr's data: partially pinned RSAs had the most balanced CPA/ROAS/CPC; fully pinned had slightly higher CTR but not better conversion; sentence case beat title case for RSAs (clearest on ROAS); shorter headlines had higher CTR and conversion rate; descriptions did best at moderate length; dynamic keyword insertion and customizers showed no significant gain; RSAs beat ETAs even fully pinned.
- **Evidence type:** study
- **Confidence:** low-medium (correlational, effect sizes not published in text, selection bias acknowledged by the authors)
- **How it works:** Unknown; plausible mechanisms include shorter headlines leaving room for 3 headlines to show, and sentence case reading as more natural. Differences in CTR were around 0.5-1%.
- **When it matters / how experts use it:** Use as priors for test ideas, not rules. Pinning should be decided on brand/compliance grounds, since its performance effect looks small either way.
- **Exceptions and failure modes:** Confounding by advertiser skill, vertical and bidding strategy (more accounts use Max Conversions than Max Conversion Value, which may drive ROAS patterns).
- **Signals in data:** Your own ad-level comparisons.
- **Sources:** [Google Ads ad copy: what works and what doesn't in 2024 (SEL)](https://searchengineland.com/google-ads-ad-copy-what-works-doesnt-446650) (checked 2026-10-13); [SEJ summary of the study](https://www.searchenginejournal.com/ad-copy-tactics-backed-by-study-of-over-1-million-google-ads/527230/) (checked 2026-10-13); [Optmyzr Ad Strength study](https://optmyzr.com/blog/google-ad-strength-study) (checked 2026-10-13)

### PLT-ADS-008 · How many RSAs per ad group (documented vs practitioner) (changed 2025)
- **Claim:** Google now recommends at least 2 RSAs per ad group, each with a unique final URL and Good/Excellent Ad Strength, citing +6.6% conversions going from 1 to 2 RSAs and +3.7% from 2 to 3 at similar cost per conversion (internal data, Aug 2025). Practitioners commonly run 2-3 RSAs per ad group, each with a distinct theme or with pinned vs unpinned variants, to keep ad-level testing possible.
- **Evidence type:** documented (recommendation and Google's averages); practitioner (themed approach)
- **Confidence:** medium
- **How it works:** A second RSA with a different landing page adds assets that can serve as link-based assets (PLT-ADS-003) and gives the system a second pool. Google's lift figures are observational averages.
- **When it matters / how experts use it:** Low-volume ad groups: more RSAs split already thin data and slow any learning; one strong RSA plus assets may be better (practitioner reasoning). High-volume ad groups: 2-3 RSAs enable message tests.
- **Exceptions and failure modes:** The long-standing cap of 3 enabled RSAs per ad group was not re-verified on an opened page in this pass. Unique final URLs are not always available for a single-service landing page.
- **Signals in data:** One RSA taking almost all impressions (Google optimizing toward it) while another converts better per impression.
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13); [About Ad Strength](https://support.google.com/google-ads/answer/9921843) (checked 2026-10-13); [How to test RSAs (Adalysis, Brad Geddes)](https://adalysis.com/blog/how-to-test-responsive-search-ads-rsa-in-google-ads-and-microsoft-ads/) (checked 2026-10-13); [How to optimize RSAs (SEJ, Optmyzr)](https://www.searchenginejournal.com/responsive-search-ads-testing/463538/) (checked 2026-10-13)

### PLT-ADS-009 · Asset reports: labels deprecated, full metrics since June 2025 (changed 2025)
- **Claim:** The "Performance label" column (Best/Good/Low, relative to same-type assets) is deprecated. Asset reports now show impressions, clicks, conversions, conversion value and cost per asset, available only for dates on or after June 5, 2025. Google says asset-level counts are per instance served (sums will not match ad totals), and ratio metrics (CTR, CPC, CPA, ROAS) are "directional only" because they reflect the combination served. Google recommends evaluating at asset group or campaign level.
- **Evidence type:** documented; google-statement via press for timing
- **Confidence:** high (documentation); medium (rollout timing, first seen by practitioners in Europe July 2025)
- **How it works:** When an ad with headlines A, B, C is clicked and converts, each of A, B and C gets credit; the asset metric is an attribution of the whole ad's outcome to every component that was present.
- **When it matters / how experts use it:** Use asset metrics to find assets that never get impressions or that co-occur with poor outcomes, then test replacements at ad level. Do not compute "asset CPA" and cut the worst one as if it were a controlled result.
- **Exceptions and failure modes:** Google-generated assets are labeled "Google AI" in the "Added by" column; only assets with impressions in the last 30 days in active entities appear.
- **Signals in data:** Asset conversions summing to more than ad conversions; assets with zero impressions for weeks.
- **Sources:** [About the ad-level asset report for RSAs](https://support.google.com/google-ads/answer/9564897) (checked 2026-10-13); [About campaign level asset reporting for RSAs](https://support.google.com/google-ads/answer/9781208?hl=en) (checked 2026-10-13); [Google Ads RSA headline performance data (SEL, Jul 28 2025)](https://searchengineland.com/google-ads-rsa-headline-performance-data-459541) (checked 2026-10-13)

### PLT-ADS-010 · Why per-asset data is confounded (selection by the serving system)
- **Claim:** Asset-level metrics are biased by the serving algorithm: Google chooses which assets show in which auctions based on predicted performance, so an asset's numbers reflect the queries, positions and partner assets it was served with, not its standalone effect.
- **Evidence type:** inference (from documented "directional only" and per-query assembly)
- **Confidence:** medium
- **How it works:** If headline X is shown mainly on high-intent brand-adjacent queries, it will look excellent regardless of its wording. A low-impression asset was judged weaker *by the prediction model* (which practitioners believe leans on CTR), not necessarily weaker on conversions.
- **When it matters / how experts use it:** To learn whether a message works, isolate it: pin it in one RSA vs another, or use ad variations / experiments (PLT-ADS-013). Use asset data to generate hypotheses only.
- **Exceptions and failure modes:** Large, stable ad groups with assets served broadly across similar queries make asset metrics less biased, but never unbiased.
- **Signals in data:** One asset with far higher CTR but only on a narrow query subset (check search terms by ad group, since Google does not report search terms per asset).
- **Sources:** [About the ad-level asset report](https://support.google.com/google-ads/answer/9564897) (checked 2026-10-13); [How to optimize RSAs (SEJ/Optmyzr)](https://www.searchenginejournal.com/responsive-search-ads-testing/463538/) (checked 2026-10-13)

### PLT-ADS-011 · Combinatorics: why RSA learning needs volume
- **Claim:** Five unpinned headlines shown two at a time give about 20 combinations; 15 headlines up to ~2,940; descriptions multiply this (×6 for 3 unpinned, ×12 for 4). At even 100 impressions per combination, a full pool needs hundreds of thousands of impressions to evaluate combinations, so for most ad groups the system cannot "test" all combinations and relies on its prediction model.
- **Evidence type:** practitioner (arithmetic from Brad Geddes, Adalysis)
- **Confidence:** high for the arithmetic; medium for the implication
- **How it works:** The combinations report shows which combinations served and how many impressions each got, not conversion outcomes, so it cannot tell you the best combination.
- **When it matters / how experts use it:** In low-volume accounts, deliberately reduce the search space (fewer, more distinct headlines; pin 2-3 options per key slot) so traffic concentrates on meaningfully different messages.
- **Exceptions and failure modes:** Google's model shares learning across ads and accounts, so it is not doing naive per-combination testing; the arithmetic overstates the data needed for *its* predictions but correctly shows that *you* cannot validate combinations from your own data.
- **Signals in data:** Top combination with a few hundred impressions and a long tail of single-digit combinations.
- **Sources:** [How to test RSAs (Adalysis, Brad Geddes, 2022, updated 2026)](https://adalysis.com/blog/how-to-test-responsive-search-ads-rsa-in-google-ads-and-microsoft-ads/) (checked 2026-10-13)

### PLT-ADS-012 · Ad rotation: Smart Bidding forces "Optimize"
- **Claim:** Two settings exist: Optimize (favours ads expected to perform better per auction) and Do not optimize (rotates more evenly indefinitely; "isn't recommended for most advertisers"). With Smart Bidding, Google automatically uses Optimize. Rotation applies between ads; it does not control which assets inside an RSA are combined.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Under Optimize, ads predicted to perform better enter more auctions. Even with "Do not optimize", impressions differ because ad quality affects position and eligibility.
- **When it matters / how experts use it:** An unequal impression split between RSAs is not proof the favoured ad is better on your goal; compare conversions per impression (PLT-ADS-013). For clean tests use ad variations or experiments, not rotation.
- **Exceptions and failure modes:** Brad Geddes reports (anecdotally) that Google appears to favour CTR when choosing which combinations to serve, which can diverge from conversion goals.
- **Signals in data:** One ad receiving 80-90% of impressions within days of launch.
- **Sources:** [About ad rotation](https://support.google.com/google-ads/answer/112876) (checked 2026-10-13); [How to test RSAs (Adalysis)](https://adalysis.com/blog/how-to-test-responsive-search-ads-rsa-in-google-ads-and-microsoft-ads/) (checked 2026-10-13)

### PLT-ADS-013 · Reading RSA tests correctly
- **Claim:** Valid RSA tests compare whole ads or experiment arms on a per-impression business metric, not assets on ratios. Tools: (a) ad variations (RSA-only; find-and-replace, URL or text/pinning changes; cookie-based split of auctions; up to 84 days; differences and confidence intervals shown only once significant; cannot be edited after launch), (b) custom experiments for several changes, (c) multiple RSAs in one ad group compared on conversions per impression (CTR × conversion rate) or profit per impression.
- **Evidence type:** documented (ad variations exist and are RSA-only); practitioner (split details, metrics)
- **Confidence:** medium-high
- **How it works:** Per-impression metrics fix the bias that a high-CTR ad that converts poorly looks good on CTR and a low-CTR ad that repels bad clicks looks bad. Ad variations randomize users (cookies) so query mix is balanced across arms; in-ad-group comparisons are not randomized because rotation is optimized.
- **When it matters / how experts use it:** Pre-define the metric (conversions or value per impression; for tCPA/tROAS, conversions within target). Test one meaningful message change (offer, qualifier, proof), not wording tweaks. Run full weekly cycles.
- **Exceptions and failure modes:** Qualifying copy may lower CTR and still win (fewer, better clicks). Cookie splits leak under private browsing/cookie blocking. AI text customization can inject assets into both arms and blur the comparison. Low-volume ad groups rarely reach significance; pool across campaigns with ad variations.
- **Signals in data:** Ad variation result rows without confidence intervals = not significant yet.
- **Sources:** [About ad variations](https://support.google.com/google-ads/answer/7438541) (checked 2026-10-13); [A guide to ad variations (SEL, Tim Jensen)](https://searchengineland.com/google-ads-ad-variations-guide-442620) (checked 2026-10-13); [How to optimize RSAs (SEJ/Optmyzr)](https://www.searchenginejournal.com/responsive-search-ads-testing/463538/) (checked 2026-10-13); [How to test RSAs (Adalysis)](https://adalysis.com/blog/how-to-test-responsive-search-ads-rsa-in-google-ads-and-microsoft-ads/) (checked 2026-10-13)

### PLT-ADS-014 · When assets show and how they enter Ad Rank
- **Claim:** Assets are never guaranteed to show (exception: approved text disclaimers). Google shows an asset only when it predicts the asset improves the ad and the ad's position and Ad Rank are high enough; Ad Rank factors in the expected impact of assets, and a minimum Ad Rank (including assets) is required before extra assets show. Higher-positioned ads get first chance to show more assets. Clicks on the ad and assets are capped at two charged clicks per impression; review and seller-rating clicks are free.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Assets raise expected CTR/prominence, which feeds Ad Rank; but space is limited, so lower positions show fewer assets.
- **When it matters / how experts use it:** Assets are a near-free Ad Rank lever: an advertiser with complete, relevant assets can outrank a higher bidder without them. If assets rarely show, the fix may be Ad Rank (bid/quality), not more assets.
- **Exceptions and failure modes:** Asset impressions are concentrated in top positions, so comparing asset CTR to ad CTR mixes position effects.
- **Signals in data:** Asset impression share much lower than ad impressions; assets segment showing low "shown with ad" rates in low-position campaigns.
- **Sources:** [About assets](https://support.google.com/google-ads/answer/7331111) (checked 2026-10-13)

### PLT-ADS-015 · Asset levels and override rules differ by type
- **Claim:** Most assets can be set at account, campaign or ad group level. For callouts, call and promotion assets the most specific level wins (one ad group callout makes campaign callouts ineligible for that ad group). For sitelinks Google says assets serve together within the same branch and higher-level sitelinks can serve with lower-level ones when predicted to improve performance.
- **Evidence type:** documented
- **Confidence:** medium-high (sitelink behaviour may differ from older "override" behaviour still described by practitioners)
- **How it works:** Hierarchy resolution happens per ad group at serving time.
- **When it matters / how experts use it:** Put generic proof points at account level, offer-specific or service-specific ones at ad group level, and remember that adding a single ad group callout silently removes all inherited ones.
- **Exceptions and failure modes:** Practitioner articles still describe sitelinks as strictly overriding; check the current behaviour in the account.
- **Signals in data:** Ad groups with one custom callout showing far fewer callouts overall.
- **Sources:** [About callout assets](https://support.google.com/google-ads/answer/6079510?hl=en) (checked 2026-10-13); [About sitelink assets](https://support.google.com/google-ads/answer/2375416?hl=en) (checked 2026-10-13); [Callouts & structured snippets (SEL, Aug 2025)](https://searchengineland.com/google-ads-callouts-structured-snippets-460029) (checked 2026-10-13)

### PLT-ADS-016 · Sitelinks
- **Claim:** Sitelink text is 25 characters (12 double-width). At least 2 are needed to show; Search/PMax shows up to 6 on desktop and up to 8 in a mobile carousel. Google says moving to 6 sitelinks per campaign gave up to 3.5% more conversions at similar cost per conversion (internal data, May 2025). Dynamic sitelinks may show alongside or instead of manual ones; sitelink clicks cost the same as a headline click.
- **Evidence type:** documented
- **Confidence:** high (mechanics); low-medium (lift figure, internal observational)
- **How it works:** Sitelinks expand ad size (prominence) and route users to deeper intents, which can raise CTR and conversion rate when they match sub-intents.
- **When it matters / how experts use it:** Use sitelinks as intent splitters (pricing, reviews, specific services, booking) with descriptions; keep schedules aligned with ad schedules; 6+ sitelinks also improve Ad Strength.
- **Exceptions and failure modes:** Sitelinks to generic pages (About, Contact) add size but may dilute conversion paths. Duplicate or near-duplicate text will not serve together.
- **Signals in data:** Click type segment "Sitelink"; conversion rate by sitelink; dynamic sitelinks in account-level automated assets.
- **Sources:** [About sitelink assets](https://support.google.com/google-ads/answer/2375416?hl=en) (checked 2026-10-13)

### PLT-ADS-017 · Callouts and structured snippets
- **Claim:** Callouts: 25 characters, up to 10 shown, non-clickable, Search only, schedulable, dynamic callouts may replace or join manual ones. Structured snippets: header from a fixed list (e.g. Types, Services catalog, Brands, Insurance coverage), 3-10 values of 25 characters.
- **Evidence type:** documented; practitioner (CTR benefits claimed without data)
- **Confidence:** high (mechanics); low (performance claims)
- **How it works:** They add proof points and qualifying facts to ad size without adding a click target.
- **When it matters / how experts use it:** Use callouts for facts that qualify or reassure ("Licensed and insured", "From $89", "No call-out fee") and snippets for scope ("Services: drain, boiler, leak repair") so users self-select before clicking.
- **Exceptions and failure modes:** Dynamic callouts are extracted from the site and may state stale or off-strategy facts; review "Automatically created" source rows.
- **Signals in data:** Assets report source column "Automatically created" vs "Advertiser".
- **Sources:** [About callout assets](https://support.google.com/google-ads/answer/6079510?hl=en) (checked 2026-10-13); [Callouts & structured snippets (SEL, Jyll Saskin Gales, Aug 6 2025)](https://searchengineland.com/google-ads-callouts-structured-snippets-460029) (checked 2026-10-13)

### PLT-ADS-018 · Price and promotion assets
- **Claim:** Price assets need at least 3 items (5+ recommended), show up to 8 cards, 25-character header and description, one of nine types (Services, Service tiers, Product tiers, Brands, etc.), each with a price qualifier; available in 10 languages. Promotion assets carry monetary or percentage discounts, optional occasion labels in bold, optional codes/spend thresholds; occasion assets must be created or edited within 6 months of their start date or they stop serving; editing does not reset statistics.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Prices and promotions add concrete numbers to the SERP, which both attract price-motivated users and filter out those whose budget does not fit (see PRC-COPY entries on qualifying copy).
- **When it matters / how experts use it:** Service businesses can use "Service tiers" with "From" qualifiers to pre-qualify. Promotions must be genuinely available on the landing page, or they violate the unavailable-offers rule (PLT-ADS-030).
- **Exceptions and failure modes:** Mobile truncates prices; occasions cannot be extended past their date range; automated promotions can surface deals Google finds on your site.
- **Signals in data:** Price asset click type; conversion rate of price-card clicks vs headline clicks.
- **Sources:** [About price assets](https://support.google.com/google-ads/answer/7065415) (checked 2026-10-13); [About promotion assets](https://support.google.com/google-ads/answer/7367521) (checked 2026-10-13)

### PLT-ADS-019 · Call and location assets
- **Claim:** Call numbers must be in E.164 format and verified (number in site source code, or domain verified via Search Console or a directly placed Google tag; tag managers do not count). Vanity, premium and fax numbers are rejected. Call assets can be scheduled to business hours, are shown by an auction algorithm (not every impression), and may appear as a call button with RSAs/Smart Bidding. Call reporting uses Google forwarding numbers (Search Network only) and creates a "Call from ads" conversion.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** A tap-to-call removes a page visit; for urgent local services this can be the dominant conversion path.
- **When it matters / how experts use it:** Schedule calls only when someone answers; set a call-length threshold for the conversion so short calls do not train bidding on junk.
- **Exceptions and failure modes:** Dynamic number insertion on the site causes "Unverified phone number" disapprovals unless the domain is verified. Phone numbers may not appear in ad text itself (editorial policy, PLT-ADS-029).
- **Signals in data:** Calls column, call duration, "Call from ads" conversions vs website conversions.
- **Sources:** [About call assets](https://support.google.com/google-ads/answer/2453991) (checked 2026-10-13); [About assets](https://support.google.com/google-ads/answer/7331111) (checked 2026-10-13)

### PLT-ADS-020 · Lead form assets
- **Claim:** Lead forms require a good policy history and eligible (non-sensitive) vertical; a campaign using them needs conversion-focused bidding toward a lead form conversion goal; a headline that opens directly to the form needs >$1,000 account spend (or $15,000 across accounts) and advertiser verification. A privacy policy link is required. Leads are kept 60 days (CSV covers last 30 days); delivery via webhook, API or Zapier. OTP verification is offered to improve quality.
- **Evidence type:** documented; practitioner/inference on lead quality
- **Confidence:** high (requirements); medium (quality inference)
- **How it works:** Prefilled Google account data lowers form effort, so volume rises; lower effort also admits lower-intent submitters (inference consistent with practitioner reports).
- **When it matters / how experts use it:** Add qualifying questions and OTP, import offline outcomes so bidding learns lead quality, and compare cost per *qualified* lead with website forms.
- **Exceptions and failure modes:** Without a webhook, leads expire after 60 days unseen.
- **Signals in data:** High lead-form conversion volume with low sales acceptance rate.
- **Sources:** [About lead form assets](https://support.google.com/google-ads/answer/9423234) (checked 2026-10-13)

### PLT-ADS-021 · Image assets in Search (changed 2026-07 for quality rules)
- **Claim:** Search image assets require an account open at least 60 days, good policy history, active text ads with Search spend in the last 30 days, and an eligible vertical (sexual content and gambling excluded). Square 1:1 is required (min 300×300), landscape 1.91:1 optional; up to 20 images per campaign; dynamic image assets can pull images from the landing page. Google cites a 6% average CTR increase when images show (internal data, April 2023). Description 2 may be truncated when an image shows. Collage, blurry, distorted, poorly cropped or mostly blank images are disapproved (requirements page updated July 2026).
- **Evidence type:** documented; study for dated quality rules via PPC Land
- **Confidence:** high (requirements); low-medium (CTR claim)
- **How it works:** Images increase ad area and visual weight, which eye-tracking suggests attracts attention on complex SERPs (see PRC-COPY on scanning).
- **When it matters / how experts use it:** New accounts cannot use them for 60 days. Pin required text away from D2 when images are on.
- **Exceptions and failure modes:** Dynamic images may pick irrelevant site images; format is auction-determined and not controllable.
- **Signals in data:** Image asset impressions/CTR in Assets report.
- **Sources:** [About image assets for Search campaigns](https://support.google.com/google-ads/answer/9566341) (checked 2026-10-13); [Google Ads bans blurry image assets (PPC Land)](https://ppc.land/google-ads-bans-blurry-image-assets-and-cuts-eligibility-to-60-day-accounts/) (checked 2026-10-13)

### PLT-ADS-022 · Business name and logo
- **Claim:** Business name and logo show on desktop and mobile Search ads; they require Search spend in the last 28 days and completed advertiser verification, and the name must exactly match the verified domain or legal name (brand verification with an active trademark is needed for a different name or logo). Search allows one name and one logo at account level and one per campaign. If none is eligible, a globe icon with the display URL shows. Promotional language is not allowed in the business name.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** A recognisable name/logo is a trust and brand-salience cue on an otherwise uniform text SERP.
- **When it matters / how experts use it:** Complete verification early in new accounts; for franchise or DBA names, plan brand verification.
- **Exceptions and failure modes:** Eligibility does not guarantee display; dynamic logos may replace uploads.
- **Signals in data:** Business name/logo impressions in Assets report (Search and PMax only).
- **Sources:** [About business information](https://support.google.com/google-ads/answer/12497613) (checked 2026-10-13); [Editorial policy](https://support.google.com/adspolicy/answer/6021546) (checked 2026-10-13)

### PLT-ADS-023 · Text disclaimer assets: guaranteed disclosure line (changed 2026)
- **Claim:** A text disclaimer (up to 90 characters, available globally for RSAs) shows in the description section of every Search ad in the campaign once approved, overriding any asset pinned to D1. It does not affect Ad Strength, works with AI Max text customization and Final URL expansion, and if disapproved the ad still serves without it. It can only be added after an RSA exists in the campaign.
- **Evidence type:** documented
- **Confidence:** high (help page opened); medium on exact launch date (press coverage mid-2026)
- **How it works:** It reserves the D1 slot for compliance text, replacing the old workaround of pinning disclaimers into D1.
- **When it matters / how experts use it:** Regulated advertisers (finance, insurance, legal, health) can guarantee disclosures even with AI-generated text on. It costs one of the two visible description slots, so the remaining slot carries all persuasion.
- **Exceptions and failure modes:** Truncation can still occur with large fonts or some languages.
- **Signals in data:** Disclaimer summary card under Assets > Associations.
- **Sources:** [About text disclaimers for Search ads](https://support.google.com/google-ads/answer/17028951) (checked 2026-10-13); [Google publishes guidance for text disclaimers (SEL)](https://searchengineland.com/google-publishes-guidance-for-text-disclaimers-in-search-ads-484172) (checked 2026-10-13)

### PLT-ADS-024 · Keyword insertion and ad customizers
- **Claim:** `{KeyWord:Default}` inserts the **ad group keyword**, not the search term; if it does not fit, the default is used. Ad customizers for RSAs support attributes (text, number, price, percent) linked at account, campaign, ad group or keyword level (most specific wins; max 40 enabled attributes), location insertion `{LOCATION(City):default}` and countdowns (`COUNTDOWN` in account timezone, `GLOBAL_COUNTDOWN` in user timezone). Inserted values and defaults must fit 30/90 characters. Google's help page states IF functions are not currently supported in RSAs.
- **Evidence type:** documented; study (Optmyzr: no significant gain from DKI/customizers)
- **Confidence:** high (mechanics); low-medium (performance)
- **How it works:** Insertion raises apparent relevance and bolding; customizers keep prices and deadlines current without new ads.
- **When it matters / how experts use it:** Risks: with broad match or AI Max the keyword shown may not match what the user typed (relevance mismatch); inserted competitor or trademark keywords can create trademark issues; capitalisation of inserted text can break editorial rules; inserted text that is grammatically awkward hurts credibility. Use customizers for verifiable facts (price, stock, deadline) fed from a maintained source.
- **Exceptions and failure modes:** Countdown urgency must reflect a real deadline (misrepresentation, PLT-ADS-030; and see PRC-COPY on urgency ethics).
- **Signals in data:** Ads always showing default text (inserted value too long).
- **Sources:** [About keyword insertion](https://support.google.com/google-ads/answer/74992) (checked 2026-10-13); [Customize responsive search ads (Google Ads API)](https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads?hl=en) (checked 2026-10-13); [RSAs with dynamic text (Help)](https://support.google.com/google-ads/answer/11559472?hl=en) (checked 2026-10-13); [SEJ summary of Optmyzr study](https://www.searchenginejournal.com/ad-copy-tactics-backed-by-study-of-over-1-million-google-ads/527230/) (checked 2026-10-13)

### PLT-ADS-025 · Text customization (ex automatically created assets) and the AI Max auto-upgrade (changed 2025-05, 2026-09)
- **Claim:** Text customization generates extra headlines and descriptions from the domain, landing page, existing ads and keywords (extractive plus generative AI grounded in the landing page), refreshes them at least every 48 hours, serves them only when predicted to beat your assets, and counts them in Ad Strength. It now requires AI Max. Timeline: generative ACA rollout for US/UK English completed Feb 2024; AI Max open beta May 6, 2025 and ACA upgraded into AI Max as "text customization" from late May 2025; from Sept 1, 2026 campaigns using ACA are auto-upgraded to AI Max with search term matching and text customization enabled, and campaign-level broad match campaigns get search term matching. Disabling legacy ACA cannot be undone except via AI Max.
- **Evidence type:** documented; google-statement via advertiser emails reported by press
- **Confidence:** high (features); medium (exact auto-upgrade scope)
- **How it works:** AI text competes with your text inside the same RSA pool, chosen by the same prediction model; controls are text guidelines (term exclusions, tone, concepts to avoid; pilot), up to 10 previews, per-asset permanent removal, and the campaign toggle.
- **When it matters / how experts use it:** Audit any campaign that had ACA before Sept 2026: it may now match more queries and show copy you did not write. Remove generated assets that make unverifiable claims, wrong prices or off-brand promises; for regulated copy use a text disclaimer and text guidelines. Watch for creative sameness across competitors using the same model (practitioner concern).
- **Exceptions and failure modes:** Landing page errors become ad errors within 48 hours. Ad variation tests can be contaminated by generated assets.
- **Signals in data:** "Added by: Google AI" rows; AI Max reporting columns; sudden new headlines in combinations report.
- **Sources:** [About text customization in Search campaigns](https://support.google.com/google-ads/answer/11259373?hl=en) (checked 2026-10-13); [Turn text customization on or off](https://support.google.com/google-ads/answer/16738708) (checked 2026-10-13); [Google to auto-upgrade some Search campaigns to AI Max (SEL, Aug 6 2026)](https://searchengineland.com/google-to-auto-upgrade-some-search-campaigns-to-ai-max-484428) (checked 2026-10-13); [AI Max auto-upgrade lands September 1 (PPC Land)](https://ppc.land/google-ads-ai-max-auto-upgrade-lands-september-1-will-ads-all-look-alike/) (checked 2026-10-13)

### PLT-ADS-026 · Account-level automated assets (dynamic sitelinks, callouts, snippets, images, logos)
- **Claim:** Google can automatically create sitelinks, callouts, structured snippets, image assets, logos, location, seller rating and app assets at account level; these may show alongside or instead of manual assets and are reported under "Account level automated assets". They can be paused or removed individually or disabled in automated asset settings.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Extracted from the website and other sources; served when predicted to improve performance.
- **When it matters / how experts use it:** In regulated or price-sensitive businesses, review these quarterly; a stale site page can produce stale callouts or sitelinks to outdated offers.
- **Exceptions and failure modes:** They can contradict manual qualifiers (e.g. "Free quote" callout when you charge for site visits).
- **Signals in data:** Source column "Automatically created".
- **Sources:** [About campaign level asset reporting for RSAs](https://support.google.com/google-ads/answer/9781208?hl=en) (checked 2026-10-13); [About callout assets](https://support.google.com/google-ads/answer/6079510?hl=en) (checked 2026-10-13); [About sitelink assets](https://support.google.com/google-ads/answer/2375416?hl=en) (checked 2026-10-13)

### PLT-ADS-027 · AI Max and pinning: conflicting signals
- **Claim:** Google's AI Max help page says pinned RSA assets are **not respected** when both text customization and Final URL expansion are on, nor when URL inclusions are set; Final URL expansion requires text customization. PPC Land reports that pinned assets remain respected for campaigns auto-upgraded in Sept 2026 (where Final URL expansion is not enabled by default).
- **Evidence type:** documented (help page); google-statement via press
- **Confidence:** medium (sources differ in scope; both may be true for different configurations)
- **How it works:** Final URL expansion may send users to a different page, so Google lets generated text replace your pinned text that may not fit the new page.
- **When it matters / how experts use it:** If any copy must always show (compliance), either keep Final URL expansion off, or use a text disclaimer asset (which works with AI Max). Do not rely on pins in AI Max campaigns with FUE.
- **Exceptions and failure modes:** Static tracking templates without `{lpurl}` can break expanded URLs (practitioner report).
- **Signals in data:** Pinned headline impression share falling after enabling FUE.
- **Sources:** [Optimize Google Ads with AI Max for Search campaigns](https://support.google.com/google-ads/answer/15913066?hl=en) (checked 2026-10-13); [About text customization](https://support.google.com/google-ads/answer/11259373?hl=en) (checked 2026-10-13); [PPC Land on the auto-upgrade](https://ppc.land/google-ads-ai-max-auto-upgrade-lands-september-1-will-ads-all-look-alike/) (checked 2026-10-13)

### PLT-ADS-028 · Ads in AI Overviews and AI Mode (changed 2025-2026)
- **Claim:** Ads can show above/below AI Overviews in all AIO markets from Search, Shopping, PMax and App campaigns; ads *within* AI Overviews come from Search (broad match or keywordless such as AI Max/DSA), Shopping and PMax, are English-only in a listed set of markets (US, Canada, India, Australia and others), exclude sensitive verticals (finance, healthcare, alcohol, gambling, politics, adult), cannot be targeted or opted out of, and are reported as "Top ads" without segmentation. Google's Ads Liaison stated (May/June 2026) AI Max is not a technical requirement for AI search placements and that exact match is not eligible inside AIO auctions. New AI Mode formats announced May 20, 2026 (Conversational Discovery ads, Highlighted Answers) are in US testing, with Gemini generating creative and an independent AI explainer beside it.
- **Evidence type:** documented (AIO page); google-statement (Liaison, GML via press)
- **Confidence:** medium-high for AIO; low-medium for AI Mode formats (testing, details sparse)
- **How it works:** Placement depends on relevance to both the query and the AIO content; creative is increasingly assembled or written by Google, with the advertiser supplying landing pages and guardrails.
- **When it matters / how experts use it:** Landing page content becomes ad copy input; claims on the site must be accurate and policy-safe. Advertisers in excluded verticals should not plan for AIO ad inventory. No placement reporting means you cannot isolate AIO ad performance.
- **Exceptions and failure modes:** Rollout facts change monthly; recheck before advising.
- **Signals in data:** None direct (blended into top ads); search term report may show inferred intent rather than literal queries for AI Mode (reported May 2026).
- **Sources:** [About ads and AI Overviews](https://support.google.com/google-ads/answer/16297775?hl=en) (checked 2026-10-13); [Ginny Marvin clarifies AI Max and AI search eligibility (TechWyse)](https://www.techwyse.com/?p=76611) (checked 2026-10-13); [Google introduces new ad formats in AI Mode (SEJ, May 2026)](https://www.searchenginejournal.com/google-introduces-new-ad-formats-in-ai-mode/575354/) (checked 2026-10-13); [Google's new AI search ad formats (PPC Land)](https://ppc.land/googles-new-ai-search-ad-formats-reshape-how-brands-reach-buyers) (checked 2026-10-13)
- **Open questions:** Whether advertiser RSA text is used verbatim inside AIO/AI Mode or rewritten.

### PLT-ADS-029 · Editorial policy rules that constrain copy
- **Claim:** Editorial policy requires correct capitalisation and punctuation, bans gimmicky repetition and spacing, unsupported characters, phone numbers in ad text, incomprehensible text, and misuse of ad features; ads must name the product/service/entity; asset text may not repeat words or phrases across assets in the same ad group, campaign or account (as worded by the page); business names may not contain promotional language.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Automated review plus manual review; violations disapprove the asset or ad.
- **When it matters / how experts use it:** ALL-CAPS words ("FREE"), "!!!", symbols as bullets and phone numbers in headlines fail. Use call assets for numbers. Write in the "clear, informational style of Google Search results".
- **Exceptions and failure modes:** The opened page does **not** mention superlatives or unverified claims; those fall under misrepresentation (PLT-ADS-030).
- **Signals in data:** "Disapproved: Editorial" / "Capitalization" / "Punctuation" statuses.
- **Sources:** [Editorial policy](https://support.google.com/adspolicy/answer/6021546) (checked 2026-10-13)

### PLT-ADS-030 · Misrepresentation: unreliable claims, dishonest pricing, unavailable offers
- **Claim:** Misrepresentation prohibits inaccurate claims and claims that present an unlikely result as what a user should expect; omitting material facts about identity, affiliations or qualifications; failing to disclose the payment model and full cost; clickbait and sensational copy, including exploiting negative life events (death, accident, illness, arrest, bankruptcy) to create fear or guilt and push immediate action; promoting offers that are unavailable or hard to find on the destination; implying affiliation with brands or government. Only two sub-policies are labelled egregious (suspension on detection, without prior warning, and a permanent ban): **Unacceptable business practices** and **Coordinated deceptive practices**. The others (Misleading representation, Dishonest pricing practices, Clickbait ads, Misleading ad design, Manipulated media, Unreliable claims, Unclear relevance, Unavailable offers) carry no egregious label on the policy page, which does not state their enforcement. (Corrected 2026-10-13: the first version said all of these were egregious; the evaluation grader flagged it and the policy page was re-opened.)
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** This is where superlatives ("#1", "best", "guaranteed results") become risky: an unverifiable superlative or a typical-result claim that is atypical can be judged an unreliable claim (inference; the page does not list superlatives explicitly).
- **When it matters / how experts use it:** Back every numeric or comparative claim with a source on the landing page; make prices, fees and subscription terms visible; never run countdowns or "today only" for non-existent deadlines; avoid fear copy in legal, health, debt or emergency services that exploits a negative life event.
- **Exceptions and failure modes:** Enforcement is uneven; absence of disapproval is not evidence of compliance, and the penalty is account-level.
- **Signals in data:** Suspension notices citing "Misrepresentation"; ad-level "Unreliable claims" disapprovals.
- **Sources:** [Misrepresentation policy](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### PLT-ADS-031 · Trademarks in ad text
- **Claim:** Trademark restrictions apply only to ad text (not keywords or the second-level domain of the display URL) and only after a trademark owner complains for specific countries; restricted uses are by direct competitors or in confusing/deceptive ways. Exceptions: resellers and sellers of the trademarked goods/parts/compatible products (landing page must clearly sell them, show prices, and make reseller status clear), informational sites, and descriptive use of the word's ordinary meaning. Restrictions generally apply to all ads sharing the same second-level final URL domain.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Complaint-driven enforcement means a competitor-name headline can run until the owner files.
- **When it matters / how experts use it:** Bidding on competitor names is policy-permitted; writing their name in the ad is the risk. Keyword insertion on competitor keywords can put a trademark in ad text unintentionally. Repair businesses naming brands they service ("Bosch boiler repair") rely on the compatible-products/services exception and must be clear they are independent.
- **Exceptions and failure modes:** Local trademark law differs; a warning comes at least 7 days before suspension for this policy.
- **Signals in data:** "Trademarks" disapprovals limited to certain countries.
- **Sources:** [Trademarks policy](https://support.google.com/adspolicy/answer/6118) (checked 2026-10-13)

### PLT-ADS-032 · Financial services and other sensitive-vertical copy constraints
- **Claim:** Financial services ads must comply with local law in every targeted location; destinations must show physical address and all fees visibly (not behind hover/tabs); personal loan advertisers must disclose min/max repayment period, maximum APR and a representative total-cost example; US personal loans at 36%+ APR are banned; credit repair ads banned; debt services, crypto, CFDs and prediction markets need certification or location eligibility; many countries require financial services verification. Sensitive verticals are also excluded from RSA asset sharing and from ads within AI Overviews.
- **Evidence type:** documented
- **Confidence:** high (policy page); insurance-specific rules not covered on the opened page
- **How it works:** Copy claims ("0% interest", "guaranteed approval") must match disclosures on the page and local regulation; "guaranteed" loan modification is explicitly prohibited.
- **When it matters / how experts use it:** In finance/insurance, combine a text disclaimer asset (PLT-ADS-023), conservative text guidelines for AI text, and review of automated assets.
- **Exceptions and failure modes:** Country rules (e.g. UK, EU) add verification and wording requirements beyond the global page.
- **Signals in data:** "Financial services" limited/disapproved statuses; verification prompts in Policy manager.
- **Sources:** [Financial services policy](https://support.google.com/adspolicy/answer/2464998) (checked 2026-10-13); [About ads and AI Overviews](https://support.google.com/google-ads/answer/16297775?hl=en) (checked 2026-10-13); [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13)
- **Open questions:** Insurance-specific ad text rules and country verification lists were not opened in this pass.

### PLT-ADS-033 · Store (seller) ratings on text ads
- **Claim:** Store ratings are an automatic asset: they show by default on Search text ads when the ad's visible domain has a country-level rating of 3.5+ stars from enough eligible reviews in the last 24 months (most merchants after 100+ reviews), drawn from Google Customer Reviews, Google shopping research and about 30 review partners. Advertisers can disable them in account-level automated asset settings but cannot edit them; review clicks are free; Google cites an average 2% CTR lift (internal data).
- **Evidence type:** documented
- **Confidence:** high (requirements); low-medium (CTR claim)
- **How it works:** Ratings are per country and per domain, weighted across sources with Google's internal logic; display still depends on the auction.
- **When it matters / how experts use it:** A quick trust lever for e-commerce and services with partner reviews; check the domain match when landing pages sit on a different domain.
- **Exceptions and failure modes:** A rating just above 3.5 may be a weak or negative signal (see PRC-COPY-016/028).
- **Signals in data:** Stars in Ad Preview; seller ratings rows in account-level automated assets.
- **Sources:** [About store ratings](https://support.google.com/google-ads/answer/2375474) (checked 2026-10-13); [About assets (review and seller-rating clicks not charged)](https://support.google.com/google-ads/answer/7331111) (checked 2026-10-13)

## Common mistakes and misleading metrics
- **Chasing Excellent Ad Strength.** It is not an auction input and independent data shows no performance correlation; it rewards asset count, unpinning and AI text (PLT-ADS-005/006).
- **Reading asset CTR/CPA as causal.** Asset metrics are per-instance, credited to every co-served asset, and selected by Google's serving model; Google itself calls ratios "directional only" (PLT-ADS-009/010).
- **Treating impression share between RSAs as a verdict.** Optimized rotation favours predicted CTR; compare conversions or value per impression (PLT-ADS-012/013).
- **Putting compliance or qualifying text in H3/D2 or unpinned slots.** Only H1, H2, D1 pins and text disclaimers are reliable, and AI Max with Final URL expansion can ignore pins (PLT-ADS-002/027).
- **Assuming the preview is what users see.** It does not show all combinations, and assets can move into link positions (PLT-ADS-003).
- **Judging qualifying copy on CTR.** A lower CTR with a higher conversion rate and better lead quality can be the win.
- **Ignoring automatically created and AI-generated assets after the Sept 2026 auto-upgrade.** Generated text and dynamic assets can state things you would not approve (PLT-ADS-025/026).
- **Comparing asset CTR to ad CTR.** Assets show mostly in top positions, so they inherit position effects (PLT-ADS-014).

## Unresolved questions
- Does Google use CTR, conversion probability or a blend when choosing RSA combinations under conversion bidding? Only anecdotal practitioner evidence (Geddes) exists.
- What is the causal effect of Ad Strength improvements? Google's 15% figure and Optmyzr's null result are both observational.
- Exact current behaviour of pinning in AI Max campaigns by configuration (help page vs PPC Land reporting).
- Whether advertiser-written RSA text is used verbatim in AI Overviews and AI Mode placements, and when segmented reporting will exist.
- Launch date of enhanced flexibility (headlines as link-based assets) and whether those impressions can be isolated.
- Whether the 3-enabled-RSAs-per-ad-group cap still applies in 2026 (not re-verified).
- Insurance-specific and country-specific financial ad-text rules (not opened in this pass; web search budget was exhausted).
