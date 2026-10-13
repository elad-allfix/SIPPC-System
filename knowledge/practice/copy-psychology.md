---
area: practice
topic: copy psychology for search ads and offers
checked: 2026-10-13
owner: research
---
# Consumer psychology behind search ad copy and offers

This file covers why searchers click (or skip) a search ad and what makes the click turn into a good customer: message match to the query and the searcher's situation, specificity and numbers, offer framing (price, free, guarantees), urgency and loss framing and their ethical and policy limits, social proof and trust, scanning behaviour on modern SERPs, differentiation, qualifying copy, and how practitioners build and test angle libraries. Evidence is graded: peer-reviewed and field studies are separated from Google-published research and from practitioner opinion. The single most important idea: **a search ad is read in a few seconds by someone who already has a need, so the winning copy is usually the one that most quickly proves fit (this is for you, in your situation, at a price/terms you accept, from someone credible), and the right success metric is qualified conversions per impression, not CTR.**

### PRC-COPY-001 · Searchers scan, they do not read: the pinball pattern and the 5-second decision
- **Claim:** On modern SERPs, users scan non-linearly ("pinball"), drawn by visual weight (images, carousels, featured snippets, bold text); SERP features got a look in 74% of cases where present, and users spent on average 5.7 seconds considering results before the first click (NN/g meta-analysis of 471 queries, 2017-2019).
- **Evidence type:** study (NN/g usability and eye-tracking, published 2019)
- **Confidence:** medium (pre-AI-Overview SERPs; no ad-specific gaze metrics reported)
- **How it works:** Attention is allocated by salience first, then by relevance cues; an ad gets a glance, and in that glance the user checks for their query words, a concrete fact, and a reason to trust.
- **When it matters / how experts use it:** Put the decisive information in the first words of H1/H2, use visual-weight assets (images, sitelinks, price cards) where eligible, and keep each headline to one idea. Expect that with AI Overviews (2024-2026) the competition for attention is harder still.
- **Exceptions and failure modes:** High-consideration B2B or legal searches may involve slower comparison reading. Data predates AI Overviews and AI Mode.
- **Signals in data:** CTR rising after adding image assets or sitelinks with no copy change (prominence effect, not message effect).
- **Sources:** [Complex search-results pages change search behavior: the pinball pattern (NN/g)](https://www.nngroup.com/articles/pinball-pattern-search-behavior/) (checked 2026-10-13)

### PRC-COPY-002 · Numbers catch the eye and signal facts
- **Claim:** Eye-tracking shows numerals attract fixations even inside text users otherwise skip, because digits look different from letters (detectable in peripheral vision) and represent facts; NN/g recommends numerals over words and exact figures for specific data, which it argues increases credibility.
- **Evidence type:** study (NN/g eye-tracking, 2007; methods summarised, sample not stated)
- **Confidence:** medium
- **How it works:** Pre-attentive pickup of digit shapes; facts reduce uncertainty, which is what a searcher is trying to do.
- **When it matters / how experts use it:** Write "24/7", "From $89", "4.8★ from 1,200 reviews" (if true and verifiable), "Same-day in 90% of jobs" rather than "fast", "affordable", "highly rated".
- **Exceptions and failure modes:** A number that is not believable or not verifiable on the page backfires and can breach the misrepresentation policy (PLT-ADS-030). A number with no reference point ("Save 15%" on an unknown base) carries little meaning.
- **Signals in data:** Ad-level tests where numeric variants win on CTR but lose on conversion rate usually indicate the number attracted the wrong people (e.g. a low "from" price).
- **Sources:** [Show numbers as numerals when writing for online readers (NN/g)](https://www.nngroup.com/articles/web-writing-show-numbers-as-numerals/) (checked 2026-10-13)

### PRC-COPY-003 · Evidence type changes clicks and conversions differently (search-ad field study)
- **Claim:** In an exploratory study of search engine ads (Haans, Raassens and van Hout, Marketing Letters 2013), ads with expert evidence and statistical evidence had higher click-through rates than causal evidence, while causal evidence (why/how the product produces the benefit) had higher conversion rates.
- **Evidence type:** study (peer-reviewed; abstract only opened; sample and setting not visible)
- **Confidence:** low-medium (single exploratory study, older SERP format)
- **How it works:** Expert and statistical claims are fast credibility cues that earn the click; causal reasoning helps the visitor commit because it resolves "will it work for me".
- **When it matters / how experts use it:** Proof angles (authority, statistics) for the headline slots; mechanism/reason-why in descriptions and on the landing page. Measure on conversions per impression, since an ad can win CTR and lose conversions.
- **Exceptions and failure modes:** One study, one advertiser context; replicate in-account before generalising.
- **Signals in data:** Diverging CTR and conversion-rate winners in ad tests.
- **Sources:** [Search engine advertisements: the impact of advertising statements on click-through and conversion rates (Marketing Letters, 2013)](https://link.springer.com/article/10.1007/s11002-013-9226-5) (checked 2026-10-13)

### PRC-COPY-004 · Message match to the query: relevance signals the searcher looks for
- **Claim:** Google bolds ad text that matches or closely matches the query, and Ad Strength checks whether keywords appear in headlines; the searcher's own words in the first headline are the fastest relevance cue.
- **Evidence type:** documented (bolding, Ad Strength keyword check); inference (user effect)
- **Confidence:** medium-high
- **How it works:** Recognition is cheaper than comprehension: a scanning user matches the shape of their query words before reading claims (consistent with PRC-COPY-001).
- **When it matters / how experts use it:** Pin 2-3 query-mirroring headlines to H1 in tightly themed ad groups. With broad match or AI Max, queries diverge from keywords, so the mirror headline may not match what was actually typed; check search terms.
- **Exceptions and failure modes:** Mirroring alone is table stakes when every competitor does it; differentiation then comes from H2/H3 and assets (PRC-COPY-015). Keyword insertion inserts the keyword, not the query.
- **Signals in data:** Low CTR in an ad group whose search terms have drifted away from its keywords.
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13); [About Ad Strength](https://support.google.com/google-ads/answer/9921843) (checked 2026-10-13); [About keyword insertion](https://support.google.com/google-ads/answer/74992) (checked 2026-10-13)

### PRC-COPY-005 · Message match to the situation, not just the keyword
- **Claim:** The same query can come from different situations (emergency vs planned, DIY-curious vs ready-to-hire, owner vs renter, consumer vs business), and the persuasive content differs by situation; copy that names the situation outperforms generic copy for that segment.
- **Evidence type:** practitioner; inference
- **Confidence:** medium
- **How it works:** Relevance is judged against the user's goal, not their words. "Burst pipe? Plumber in 60 min" speaks to a crisis; "Fixed-price bathroom refits" speaks to a planner. Situation cues in data: query modifiers ("emergency", "near me", "cost", "how to"), time of day, device, location.
- **When it matters / how experts use it:** Split ad groups or RSAs by situation where query modifiers reveal it; use ad schedules and device to infer urgency; let price-research queries see price-qualified copy.
- **Exceptions and failure modes:** Over-segmentation starves each ad of data (PLT-ADS-011). AI Max search term matching can blur the situation signal.
- **Signals in data:** Same keyword with very different conversion rates by hour or device; search terms containing "how to", "DIY", "jobs", "free" (wrong situation).
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13) (for assembly constraints); otherwise practitioner reasoning, no opened study.

### PRC-COPY-006 · Ad-to-landing-page continuity is now also a platform input
- **Claim:** Continuity between the ad's promise and the landing page matters to users (they confirm "I'm in the right place") and, since 2025, to Google directly: text customization generates ad text from the landing page and refreshes within 48 hours, Final URL expansion can choose a different page, and promoting offers not easily found on the destination violates the misrepresentation policy.
- **Evidence type:** documented (platform facts); inference (user effect)
- **Confidence:** high (platform); medium (user effect)
- **How it works:** The landing page is both the conversion surface and, under AI Max, a source of ad copy; mismatched offers create both bounce and policy risk.
- **When it matters / how experts use it:** Repeat the ad's key promise and number above the fold; keep prices and offers on the page in sync with ad text and customizers; audit AI-generated headlines against the page.
- **Exceptions and failure modes:** Final URL expansion may send traffic to pages whose copy you did not align.
- **Signals in data:** High CTR with low conversion rate on one ad but not others pointing to the same page (the ad over-promises).
- **Sources:** [About text customization in Search campaigns](https://support.google.com/google-ads/answer/11259373?hl=en) (checked 2026-10-13); [Misrepresentation policy](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### PRC-COPY-007 · Google's "messy middle" experiment: six biases that shift brand preference
- **Claim:** Google and The Behavioural Architects (2020) ran simulated purchase scenarios (310,000) with real in-market shoppers in five categories and found that applying category heuristics, power of now, social proof, scarcity, authority and power of free could move preference from a favourite brand; a fictional cereal brand with five-star reviews and 20% extra free won 28% of preference, and a fictional insurer "supercharged" on all six won 87%.
- **Evidence type:** study (Google-published, simulated choices; participants, statistics and confidence intervals not reported on the page)
- **Confidence:** low-medium (direction plausible; magnitudes are extreme-case, simulated and published by a party with an interest)
- **How it works:** At the evaluation stage shoppers use shortcuts; offering the shortcut (a spec summary, a delivery time, a rating, an expert endorsement, a free extra) reduces decision effort.
- **When it matters / how experts use it:** Use the six biases as a checklist of angle families for ads and assets (callouts for "power of now", price assets for category heuristics, seller ratings/review counts for social proof).
- **Exceptions and failure modes:** Simulated choice is not real spend; effects in real auctions where every competitor uses the same cues are likely much smaller. Scarcity and urgency are legally constrained (PRC-COPY-013).
- **Signals in data:** n/a (framework).
- **Sources:** [Navigating purchase behavior and decision-making (Think with Google, Rennie and Protheroe, July 2020)](https://business.google.com/en-all/think/consumer-insights/navigating-purchase-behavior-and-decision-making/) (checked 2026-10-13)

### PRC-COPY-008 · Specificity: concrete claims beat category claims
- **Claim:** Specific, checkable claims (time, price, quantity, guarantee terms, named credentials) carry more information and credibility than generic superlatives ("best", "quality", "affordable"), which every advertiser can say and searchers discount.
- **Evidence type:** study (NN/g on numbers and credibility; Haans et al. on statistical evidence) plus practitioner
- **Confidence:** medium
- **How it works:** Generic claims carry no signal because they are costless to make; specific claims are costly if false (policy, reviews, refunds), so they work as signals.
- **When it matters / how experts use it:** Replace each adjective with a fact: "Fast" → "Arrives in 60 min"; "Experienced" → "Since 1998, 14,000 jobs"; "Best" → "Rated 4.8 on Google (1,240 reviews)". Unverifiable superlatives also raise misrepresentation risk (PLT-ADS-030).
- **Exceptions and failure modes:** Over-precise claims that change often (prices, review counts) go stale; use customizers fed from maintained data (PLT-ADS-024).
- **Signals in data:** Generic-copy ads with average CTR and no distinct conversion profile; competitors' ads that are interchangeable with yours.
- **Sources:** [NN/g on numerals](https://www.nngroup.com/articles/web-writing-show-numbers-as-numerals/) (checked 2026-10-13); [Haans et al. 2013](https://link.springer.com/article/10.1007/s11002-013-9226-5) (checked 2026-10-13); [Misrepresentation policy](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### PRC-COPY-009 · Price precision and anchoring
- **Claim:** Precise prices are judged smaller than round prices of similar magnitude ($395,425 judged smaller than $395,000), especially under uncertainty; in real estate data, more precise list prices were associated with higher sale prices (Thomas, Simon and Kadiyali, Marketing Science 2010, five studies incl. field data).
- **Evidence type:** study (peer-reviewed; lab plus field data)
- **Confidence:** medium (robust in its domain; transfer to small service prices in ads is untested)
- **How it works:** People use numeric precision as a cue to magnitude (precise numbers feel smaller) and to the price being cost-based rather than inflated.
- **When it matters / how experts use it:** "From $89" may read cheaper than "From $90"; precise quotes ("$1,247 fixed") may feel calculated rather than padded. Anchoring logic: showing a higher reference (e.g. a premium tier in price assets) changes how a mid tier is judged; this is well established in the lab but was not re-verified for ads in this pass.
- **Exceptions and failure modes:** EU/UK rules require that "was" prices in price-reduction claims be genuine prior prices; anchors must be real. Precision effects can reverse when round numbers signal quality (premium goods) (hypothesis).
- **Signals in data:** Ad tests of price formats with matched offers.
- **Sources:** [The price precision effect: evidence from laboratory and market data (Marketing Science)](https://pubsonline.informs.org/doi/10.1287/mksc.1090.0512) (checked 2026-10-13)
- **Open questions:** No opened study tests price formats in search ad text specifically.

### PRC-COPY-010 · Putting prices in ads to qualify clicks
- **Claim:** Showing a price or price floor in ads and price assets lets users self-select before paying for the click: users who cannot afford or want something cheaper skip, so CTR may fall while conversion rate and lead quality rise.
- **Evidence type:** practitioner; inference
- **Confidence:** medium (mechanism is straightforward; magnitude varies; no opened controlled study)
- **How it works:** A price is the most decisive qualifying fact; screening before the click moves rejection from a paid visit to a free impression. Side effect: if expected CTR falls, Ad Rank and CPC can worsen, so the net result must be judged per impression.
- **When it matters / how experts use it:** Use in high-ticket services with many price shoppers, B2B with minimum order sizes, or where "cheap" searchers flood forms. Use "From $X" for honest floors; Google requires that the full cost and payment model be disclosed on the destination (dishonest pricing rule).
- **Exceptions and failure modes:** In commodity markets where the price is uncompetitive, showing it can cut volume so much that the account starves. Low "from" prices that few customers actually pay attract the wrong clicks and frustrate them.
- **Signals in data:** After adding prices: CTR down, conversion rate up, cost per qualified lead down; lead-to-sale rate is the decisive metric.
- **Sources:** [About price assets](https://support.google.com/google-ads/answer/7065415) (checked 2026-10-13); [Misrepresentation policy (dishonest pricing practices)](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### PRC-COPY-011 · "Free" is psychologically special, which is why it can degrade lead quality
- **Claim:** A zero price is not just a low price: in Shampanier, Mazar and Ariely's experiments (Marketing Science 2007), making the cheaper option free (holding the price gap constant) shifted choice disproportionately toward it, best explained by affect. Google's "messy middle" work also lists "power of free" as a decision bias.
- **Evidence type:** study (peer-reviewed lab experiments); practitioner (lead-quality implication)
- **Confidence:** high for the zero-price effect in choice; medium for its implication on lead quality
- **How it works:** "Free quote", "free consultation", "free trial" attract disproportionately more responses, including people with low intent or no budget, because the decision feels costless.
- **When it matters / how experts use it:** Use "free" where volume is the constraint and sales can filter cheaply; where sales time is expensive, add friction or qualifiers ("Free quote for jobs over $500", "Free survey for homeowners in X"), or swap "free" for a concrete low-commitment step. Always import offline outcomes so bidding does not optimize toward free-offer tyre-kickers.
- **Exceptions and failure modes:** In categories where "free estimate" is the norm, omitting it can look like a hidden fee. Lab evidence concerns choice between goods, not lead quality; the lead-quality effect is practitioner observation, not a cited study here.
- **Signals in data:** High form volume, low close rate, many leads from "free" and "cheap" search terms.
- **Sources:** [Zero as a special price: the true value of free products (Marketing Science, 2007)](https://pubsonline.informs.org/doi/10.1287/mksc.1060.0254) (checked 2026-10-13); [Think with Google: messy middle](https://business.google.com/en-all/think/consumer-insights/navigating-purchase-behavior-and-decision-making/) (checked 2026-10-13)

### PRC-COPY-012 · Risk reversal and guarantees
- **Claim:** Guarantees ("Fixed price, no surprises", "Not fixed? No fee", money-back) reduce perceived risk for first-time buyers and act as a quality signal because they are costly to offer for a bad product; they must be real and honoured, and some guarantees are prohibited outright in regulated categories.
- **Evidence type:** practitioner; documented (policy limits); study evidence not opened in this pass
- **Confidence:** medium (mechanism widely accepted; the return-policy meta-analysis (Janakiraman et al., J. Retailing 2016) could not be opened because the publisher rate-limited the request)
- **How it works:** A guarantee moves risk from buyer to seller; it matters most when quality is hard to judge before purchase (services, contractors, software).
- **When it matters / how experts use it:** Test guarantee angles against proof angles; state the terms concretely ("30-day refund", "fixed quote before work starts"). In finance, "guaranteed approval" claims are risky and guaranteeing loan modification or foreclosure prevention is explicitly prohibited.
- **Exceptions and failure modes:** Lenient guarantees can attract opportunistic buyers and returns; a guarantee that is hard to claim is deceptive (misrepresentation).
- **Signals in data:** Guarantee ads converting better with flat CTR (risk was the barrier after the click, not before).
- **Sources:** [Financial services policy](https://support.google.com/adspolicy/answer/2464998) (checked 2026-10-13); [Misrepresentation policy](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)
- **Open questions:** Effect sizes of guarantee wording in search ads specifically.

### PRC-COPY-013 · Urgency and scarcity: real deadlines work, fake ones are policy and legal risk
- **Claim:** "Power of now" and scarcity were among the biases that shifted simulated choices in Google's messy-middle work, and countdown customizers exist in RSAs; but fake urgency is a recognised dark pattern (Mathur et al. 2019 found 1,818 dark-pattern instances across ~11K shopping sites, 183 sites with deceptive practices and 22 vendors selling them), Google's misrepresentation policy bans clickbait and unavailable offers, and regulators (UK CMA 2022 online choice architecture work) treat false urgency as consumer harm.
- **Evidence type:** study (Google, Mathur et al.); documented (policy)
- **Confidence:** medium-high
- **How it works:** Deadlines reduce procrastination and make the cost of waiting salient; scarcity signals value and popularity. Fake versions exploit the same mechanism and, once noticed, destroy trust.
- **When it matters / how experts use it:** Use urgency only when true and specific (sale end date via countdown, limited appointment slots shown on the booking page, seasonal deadlines). For emergency services, urgency is the user's own state: speak to speed ("Here in 60 min") rather than manufacturing pressure.
- **Exceptions and failure modes:** Evergreen "Today only!" copy; countdowns that reset. Misrepresentation violations risk disapproval and, for repeated or serious cases, account action; only Unacceptable business practices and Coordinated deceptive practices are labelled egregious (PLT-ADS-030).
- **Signals in data:** Urgency ads that lift CTR but lift refund/cancellation rates; review complaints mentioning pressure.
- **Sources:** [Dark patterns at scale (Mathur et al., arXiv 2019)](https://arxiv.org/abs/1907.07032) (checked 2026-10-13); [Think with Google: messy middle](https://business.google.com/en-all/think/consumer-insights/navigating-purchase-behavior-and-decision-making/) (checked 2026-10-13); [Online choice architecture (UK CMA, Apr 2022)](https://www.gov.uk/government/publications/online-choice-architecture-how-digital-design-can-harm-competition-and-consumers) (checked 2026-10-13); [Misrepresentation policy](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13); [Customize RSAs: countdowns (Google Ads API)](https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads?hl=en) (checked 2026-10-13)

### PRC-COPY-014 · Loss aversion is weaker and more conditional than copywriting folklore says
- **Claim:** The "losses loom twice as large" rule is contested: loss aversion appears weak or absent for small stakes and under some risk conditions (magnitude-dependent), Gal and Rucker (2018) argue many effects are better explained by inertia, while others replicate it with predictable variation; meta-analyses (Brown et al. 2024; a 2025 re-meta-analysis arguing it is not robust) disagree. So loss-framed copy ("Stop losing money on...") is not reliably better than gain-framed copy.
- **Evidence type:** study (academic literature, reviewed via an encyclopedia summary; primary papers not opened)
- **Confidence:** low-medium
- **How it works:** Loss frames may raise attention more than they change valuation; for low-stakes purchases the asymmetry may vanish.
- **When it matters / how experts use it:** Treat loss vs gain framing as a test variable, not a rule. Loss frames may suit high-stakes, already-felt problems (damage, penalties, downtime) where the loss is concrete; avoid fear copy that exploits negative life events (prohibited, PLT-ADS-030).
- **Exceptions and failure modes:** Loss frames can read as negative or manipulative and reduce trust.
- **Signals in data:** In-account ad tests of matched loss vs gain frames.
- **Sources:** [Loss aversion (Wikipedia, criticisms section and references)](https://en.wikipedia.org/wiki/Loss_aversion) (checked 2026-10-13)
- **Open questions:** No opened search-ad experiment on loss vs gain framing.

### PRC-COPY-015 · Differentiation against neighbouring ads
- **Claim:** A search ad is judged relative to the 3-4 ads and SERP features around it; when every ad repeats the query and the same claims, the ad that adds a distinct, relevant fact (price, speed, guarantee, specialism, proof) gets the click it deserves. AI-written copy built on the same models tends to drift toward the mean, increasing sameness (executives quoted at Cannes 2026; practitioner concern).
- **Evidence type:** practitioner; inference; google-statement (Google's Sean Downey: humans own the idea, AI supplies versions)
- **Confidence:** medium
- **How it works:** Distinctiveness draws attention (isolation effect, not opened here) and gives a reason to choose; interchangeable ads compete on position alone, which means on bid.
- **When it matters / how experts use it:** Before writing, inspect the live SERP (Ad Preview tool) and Auction Insights to list competitors' claims; write the claim they cannot or do not make; avoid copying the top advertiser's angle.
- **Exceptions and failure modes:** Distinct but irrelevant claims ("Family-owned since 1952" to an emergency searcher) do not help. Competitor ads vary by auction; one SERP check is a sample.
- **Signals in data:** Auction Insights overlap with many similar competitors and flat CTR despite top positions.
- **Sources:** [Google Ads AI Max auto-upgrade: will ads all look alike? (PPC Land, 2026)](https://ppc.land/google-ads-ai-max-auto-upgrade-lands-september-1-will-ads-all-look-alike/) (checked 2026-10-13)

### PRC-COPY-016 · Social proof: reviews matter, perfect scores less so
- **Claim:** Medill Spiegel Research Center analyses (2017 onward) found products with five reviews had 270% higher purchase likelihood than those with none, with sharply diminishing returns after the first few reviews; purchase likelihood peaked at 4.0-4.7 stars and declined toward 5.0 ("too good to be true"); reviews mattered more for higher-priced items; a verified-buyer badge raised purchase odds by 15%.
- **Evidence type:** study (retail review data; methods summarised only on the opened page)
- **Confidence:** medium (e-commerce product pages, not search ads)
- **How it works:** Reviews reduce uncertainty; very high scores trigger scepticism about authenticity.
- **When it matters / how experts use it:** In ad text, review counts with ratings ("4.8★ from 1,200 Google reviews") combine social proof and specificity; seller ratings may also show automatically. For local services, a modest rating with a large count can outperform a perfect score with few reviews (hypothesis based on this data).
- **Exceptions and failure modes:** Claims must be truthful and current; fake or incentivised reviews are illegal under the US FTC rule (2024) and misleading under Google policy.
- **Signals in data:** CTR and conversion rate differences after review count crosses thresholds; competitor ads showing ratings.
- **Sources:** [How online reviews influence sales (Spiegel Research Center)](https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/) (checked 2026-10-13)

### PRC-COPY-017 · Authority and trust signals
- **Claim:** Expert and statistical evidence raised CTR in a search-ad study (Haans et al. 2013); authority bias was one of the six biases in Google's messy-middle work. Platform trust cues include verified business name and logo (PLT-ADS-022). Credentials, licences, memberships, years in business and named accreditations function as authority signals.
- **Evidence type:** study; documented (business name/logo); practitioner
- **Confidence:** medium
- **How it works:** When quality is hard to assess (services, finance, health), searchers substitute credibility cues for quality evaluation.
- **When it matters / how experts use it:** Lead with authority in high-risk categories (legal, medical, finance, home repair); claimed affiliations must be real (misrepresentation bans implying affiliations), and financial services destinations must link accreditation where affiliation is claimed.
- **Exceptions and failure modes:** Accreditation names users do not recognise carry little weight; use plain-language meaning ("Gas Safe registered").
- **Signals in data:** Authority-led RSAs winning in high-ticket ad groups but not in low-ticket ones.
- **Sources:** [Haans et al. 2013](https://link.springer.com/article/10.1007/s11002-013-9226-5) (checked 2026-10-13); [Think with Google: messy middle](https://business.google.com/en-all/think/consumer-insights/navigating-purchase-behavior-and-decision-making/) (checked 2026-10-13); [Financial services policy](https://support.google.com/adspolicy/answer/2464998) (checked 2026-10-13); [Misrepresentation policy](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### PRC-COPY-018 · Legal limits on proof: fake reviews and testimonials (US, 2024)
- **Claim:** The US FTC final rule (announced August 2024) bans fake reviews and testimonials (including AI-generated ones and fake celebrity testimonials), buying reviews conditioned on sentiment, undisclosed insider reviews, company-controlled "independent" review sites, review suppression by threats or by implying filtered reviews are representative, and buying fake social indicators; it enables civil penalties for knowing violators.
- **Evidence type:** documented (regulator)
- **Confidence:** high
- **How it works:** Social-proof claims in ads ("Rated #1", "10,000 happy customers") become legal claims that must be substantiated.
- **When it matters / how experts use it:** Only quote ratings and counts that are verifiable on a third-party platform; avoid "best-rated" unless sourced. Other jurisdictions (UK, EU) have parallel rules (not opened here).
- **Exceptions and failure modes:** Rule scope is US; enforcement relies on "knew or should have known".
- **Signals in data:** n/a
- **Sources:** [FTC announces final rule banning fake reviews and testimonials (Aug 2024)](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials) (checked 2026-10-13)

### PRC-COPY-019 · Fear appeals and negative life events
- **Claim:** Google prohibits ads that exploit negative life events (death, accidents, illness, arrests, bankruptcy) to create fear or guilt and push immediate action, and handles this under its Misrepresentation policy (only two of its sub-policies are labelled egregious; PLT-ADS-030). Copy for injury law, bail, debt, health and emergency repair must therefore focus on help and outcomes, not on dramatised fear.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The searcher is already in the negative event; copy that adds fear adds pressure without information and is policy-risky.
- **When it matters / how experts use it:** "Injured at work? Free case review with a specialist" (help, specific, verifiable) rather than "You could lose everything".
- **Exceptions and failure modes:** The line between describing a problem and exploiting it is judged by reviewers; be conservative.
- **Signals in data:** Misrepresentation disapprovals; elevated complaint rates.
- **Sources:** [Misrepresentation policy](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13)

### PRC-COPY-020 · Cognitive load: one idea per asset, shorter headlines, sentence case
- **Claim:** RSA assets are recombined in any order and scanned in seconds, so each asset should carry one idea that stands alone; in Optmyzr's 1M-ad dataset shorter headlines had higher CTR and conversion rates and sentence case beat title case on ROAS/CPA for RSAs (correlational).
- **Evidence type:** documented (assembly rules); study (Optmyzr, observational); inference
- **Confidence:** medium (rules); low-medium (case/length effects)
- **How it works:** Short headlines leave room for three headlines to display; sentence case reads like natural text consistent with the informational style Google's editorial policy demands.
- **When it matters / how experts use it:** Write 3 to 6 word headlines; avoid stacking two claims in one asset; avoid jargon or acronyms users do not search with.
- **Exceptions and failure modes:** Very short headlines can be generic; specificity beats brevity when the two conflict (PRC-COPY-008).
- **Signals in data:** Combination report dominated by two-headline combos (long headlines crowd out H3).
- **Sources:** [About responsive search ads](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13); [SEJ summary of Optmyzr 1M-ad study](https://www.searchenginejournal.com/ad-copy-tactics-backed-by-study-of-over-1-million-google-ads/527230/) (checked 2026-10-13); [Editorial policy](https://support.google.com/adspolicy/answer/6021546) (checked 2026-10-13)

### PRC-COPY-021 · Emotional vs rational appeals by intent stage
- **Claim:** Practitioners generally find that search copy works best with functional, rational content (relevance, price, speed, proof), with emotion carried by the situation (relief, reassurance, status) rather than by abstract brand feeling; emotional appeals matter more for upper-funnel and brand-building work than for search activation.
- **Evidence type:** practitioner; hypothesis (the long-term brand vs short-term activation research often cited for this, e.g. Binet and Field for the IPA, was not opened in this pass)
- **Confidence:** low-medium
- **How it works:** Searchers are mostly in evaluation or action mode; emotion is useful when it names their state ("Locked out? We'll be there in 30 min") because that is both emotional and relevant.
- **When it matters / how experts use it:** Use reassurance/relief angles for distress purchases, aspiration angles for discretionary high-ticket purchases, and rational comparisons for B2B and repeat purchases; test rather than assume.
- **Exceptions and failure modes:** Brand searchers may respond to brand-voice copy; AI Mode conversational formats may change this (unknown).
- **Signals in data:** Ad tests where emotional variants win CTR but lose conversion (curiosity clicks).
- **Sources:** No opened source supports this directly; see PRC-COPY-001 and PRC-COPY-003 for adjacent evidence.
- **Open questions:** Need a field experiment on emotional vs functional copy in search ads.

### PRC-COPY-022 · Qualifying copy that repels bad clicks
- **Claim:** Qualifiers state who the offer is not for, so unsuitable searchers do not click: prices or minimums ("From $2,500", "Min. order 500 units"), audience ("For businesses only", "Homeowners only"), location ("Serving Leeds only"), scope ("Commercial roofing, not repairs"), and commitments ("Paid consultation"). Evaluate by qualified conversions or profit per impression, not CTR.
- **Evidence type:** practitioner; inference
- **Confidence:** medium
- **How it works:** Each click costs money; moving the rejection decision to the impression is free. Because Google's prediction model may favour higher-CTR assets, qualifier headlines must be pinned or placed in a separate RSA to guarantee display (PLT-ADS-004).
- **When it matters / how experts use it:** When lead-to-sale rate is low, when many search terms are students, job seekers, DIY or cheap seekers. Complement with negative keywords; qualifiers catch what negatives cannot.
- **Exceptions and failure modes:** A strong qualifier can lower expected CTR and therefore Ad Rank, raising CPC and losing impressions; in thin markets this can cost more than it saves. Under AI Max, generated assets can omit your qualifiers unless pinned or set as a text disclaimer.
- **Signals in data:** Lead-quality feedback, conversion rate by search term, lead-to-sale rate before and after.
- **Sources:** [About responsive search ads (pinning guarantees)](https://support.google.com/google-ads/answer/7684791) (checked 2026-10-13); [About text disclaimers for Search ads](https://support.google.com/google-ads/answer/17028951) (checked 2026-10-13); [A guide to ad variations (SEL) noting filtering copy can lower CTR](https://searchengineland.com/google-ads-ad-variations-guide-442620) (checked 2026-10-13)

### PRC-COPY-023 · Angle libraries: how experienced copywriters organise and test messages
- **Claim:** Practitioners build a library of angles (pain/problem, desired outcome, proof/authority, social proof, offer/price, guarantee/risk reversal, speed/convenience, specialism/identity, objection handling) and tag each RSA asset with its angle; tests then compare angles (themed RSAs or pinned sets), not word tweaks. Practitioners recommend categorising assets (e.g. offers, brand, social proof) once asset-level conversion data became available (2025).
- **Evidence type:** practitioner
- **Confidence:** medium
- **How it works:** Angles are the units that move behaviour; wording variants within an angle usually differ too little to detect with search-ad volumes (PLT-ADS-011).
- **When it matters / how experts use it:** Build 2-3 RSAs per high-volume ad group, each led by one angle via pinned H1/H2 options, keep shared relevance headlines, and compare conversions per impression; roll winning angles across ad groups via ad variations; refresh losing angles with new hypotheses drawn from reviews, sales calls and competitor SERPs.
- **Exceptions and failure modes:** In low-volume accounts, angle tests need pooling across campaigns or long durations; asset-level metrics are confounded (PLT-ADS-010).
- **Signals in data:** Angle tags enable reporting of asset metrics by angle (directional only).
- **Sources:** [How to optimize RSAs (SEJ, Optmyzr): segmenting by message/persona](https://www.searchenginejournal.com/responsive-search-ads-testing/463538/) (checked 2026-10-13); [How to test RSAs (Adalysis): themed RSAs](https://adalysis.com/blog/how-to-test-responsive-search-ads-rsa-in-google-ads-and-microsoft-ads/) (checked 2026-10-13); [Google Ads RSA headline performance data (SEL, 2025)](https://searchengineland.com/google-ads-rsa-headline-performance-data-459541) (checked 2026-10-13)

### PRC-COPY-024 · Judging copy: the right metric and the trap of CTR
- **Claim:** Copy tests should be judged on conversions (or value, or qualified leads) per impression, which combines CTR and conversion rate; CTR alone rewards curiosity and broad appeal, and conversion rate alone rewards ads that get few clicks. Under target CPA/ROAS bidding, judge conversions within the target.
- **Evidence type:** practitioner (Optmyzr, Adalysis, SEL)
- **Confidence:** high
- **How it works:** The ad's job is to produce profitable customers from a fixed pool of impressions.
- **When it matters / how experts use it:** Use offline conversion imports so "conversion" means a qualified lead or sale; otherwise free offers and urgency copy can look like winners.
- **Exceptions and failure modes:** Per-impression metrics ignore CPC differences driven by Ad Rank changes; for a full picture, use profit per impression or an experiment comparing cost and outcomes.
- **Signals in data:** Winner flips depending on which metric is used.
- **Sources:** [How to optimize RSAs (SEJ/Optmyzr)](https://www.searchenginejournal.com/responsive-search-ads-testing/463538/) (checked 2026-10-13); [A guide to ad variations (SEL)](https://searchengineland.com/google-ads-ad-variations-guide-442620) (checked 2026-10-13)

### PRC-COPY-025 · Lab persuasion findings transfer imperfectly to auctions
- **Claim:** Most persuasion evidence (zero price, price precision, framing, messy-middle simulations) comes from lab or simulated choices with one option manipulated; in a live SERP, every competitor can use the same cues, users self-select by query, and Google's serving model chooses which assets show, so effects are diluted and context-dependent.
- **Evidence type:** inference
- **Confidence:** medium
- **How it works:** Persuasion effects are relative; when cues become universal ("Free quote" in every ad) they stop discriminating. Ad Rank and asset selection add a filter between your copy and the user.
- **When it matters / how experts use it:** Use the literature to generate test hypotheses and to avoid known-bad patterns; use in-account experiments to decide.
- **Exceptions and failure modes:** Strong, structural cues (price, free, real deadlines) tend to transfer better than subtle wording effects (hypothesis).
- **Signals in data:** Expected lift from a "proven" tactic not appearing in a controlled ad variation.
- **Sources:** [Think with Google: messy middle (caveats)](https://business.google.com/en-all/think/consumer-insights/navigating-purchase-behavior-and-decision-making/) (checked 2026-10-13); [Zero as a special price](https://pubsonline.informs.org/doi/10.1287/mksc.1060.0254) (checked 2026-10-13)

### PRC-COPY-026 · AI-generated copy changes who writes the persuasion (changed 2025-2026)
- **Claim:** With text customization in AI Max (and the Sept 2026 auto-upgrade), Google generates headlines from the landing page and serves them when predicted to beat yours; in AI Mode formats (testing from May 2026) Gemini writes tailored creative plus an independent explainer. The persuasive content of the landing page therefore becomes ad copy, and the advertiser's levers are the page, text guidelines, exclusions and disclaimers.
- **Evidence type:** documented; google-statement via press
- **Confidence:** medium-high
- **How it works:** Prediction models likely optimise toward engagement signals; persuasion levers that lower CTR (qualifiers, prices) may be under-selected by the model unless pinned or guaranteed (inference).
- **When it matters / how experts use it:** Write the landing page with the same angle discipline as ads (specific claims, real proof, qualifiers visible); set text guidelines to exclude risky claims; check that generated copy keeps qualifiers.
- **Exceptions and failure modes:** Pins may be ignored with Final URL expansion (PLT-ADS-027).
- **Signals in data:** "Google AI" assets taking a growing impression share; lead quality shifts after AI Max enablement.
- **Sources:** [About text customization in Search campaigns](https://support.google.com/google-ads/answer/11259373?hl=en) (checked 2026-10-13); [Google introduces new ad formats in AI Mode (SEJ, May 2026)](https://www.searchenginejournal.com/google-introduces-new-ad-formats-in-ai-mode/575354/) (checked 2026-10-13)

### PRC-COPY-027 · Google's own copy guidance, and how to weigh it
- **Claim:** Google advises highlighting competitive differentiators, mentioning discounts/promotions/exclusive products, using specific CTAs ("Call now for a free quote"), including best keywords in headlines, ensuring promotions appear on the landing page with a relevant final URL per ad, varying headline lengths, and testing with ad variations; it supports this with internal averages (Poor to Excellent Ad Strength ~15% more clicks and conversions) and selected case studies (e.g. Swoop +71% revenue after adding top keywords).
- **Evidence type:** google-statement (help guidance plus case studies)
- **Confidence:** medium for the advice (consistent with independent evidence on relevance and specificity); low for the quoted lifts (selected case studies, observational)
- **How it works:** The guidance aims at relevance and asset diversity, which help Google's assembly model; note that Google's example CTA uses "free quote", which optimises response volume, not necessarily lead quality (PRC-COPY-011).
- **When it matters / how experts use it:** Adopt the relevance and landing-page continuity advice by default; treat "more assets, less pinning" and "free" CTAs as hypotheses to test against qualified-lead outcomes.
- **Exceptions and failure modes:** Case studies are selected successes; no failure rate is reported.
- **Signals in data:** n/a
- **Sources:** [Create effective Search ads (Google Ads Help)](https://support.google.com/google-ads/answer/6167122) (checked 2026-10-13)

### PRC-COPY-028 · Store (seller) ratings as automatic social proof in text ads
- **Claim:** Store ratings show next to Search text ads by default when the domain has a country-level rating of at least 3.5 stars, typically from 100+ eligible reviews in the last 24 months (Google Customer Reviews, Google shopping research and about 30 partners such as Trustpilot); the visible URL domain must match. Google reports an average 2% CTR improvement (internal data). Advertisers can turn them off but not edit them; clicks on reviews are not charged.
- **Evidence type:** documented
- **Confidence:** high (requirements); low-medium (CTR claim, no methodology)
- **How it works:** A star rating adds visual weight and third-party proof in one glance, which suits scanning behaviour (PRC-COPY-001) and social-proof effects (PRC-COPY-016).
- **When it matters / how experts use it:** For e-commerce and service businesses with partner reviews, building toward the threshold is a durable advantage over competitors without stars; a rating near 3.5 may hurt more than help (inference from PRC-COPY-016), and can be switched off.
- **Exceptions and failure modes:** Ratings are per country and domain; sub-domain or third-party landing domains break eligibility. Display depends on the auction.
- **Signals in data:** Stars visible in Ad Preview; automated asset settings showing seller ratings; CTR changes when ratings start or stop showing.
- **Sources:** [About store ratings (Google Ads Help)](https://support.google.com/google-ads/answer/2375474) (checked 2026-10-13)

## Common mistakes and misleading metrics
- **CTR as the copy KPI.** It rewards curiosity, "free" and broad appeal; qualifying copy often lowers CTR while raising profit (PRC-COPY-010/022/024).
- **Treating behavioural-economics rules as laws.** Loss aversion, scarcity and anchoring are conditional; loss framing is not reliably superior (PRC-COPY-014/025).
- **Manufactured urgency and unsupported superlatives.** Policy risk (Misrepresentation, PLT-ADS-030) and legal risk outweigh short-term CTR gains (PRC-COPY-013/018).
- **"Free" offers measured on lead count.** Without offline outcomes, free offers look like winners while sales acceptance falls (PRC-COPY-011).
- **Copying the top competitor's angle.** Interchangeable ads compete only on bid (PRC-COPY-015).
- **Testing wording tweaks instead of angles.** Search volumes rarely detect small wording effects; test meaningfully different messages (PRC-COPY-023).
- **Trusting asset-level CTR/CPA as the verdict on an angle.** Selection by the serving model confounds asset metrics (PLT-ADS-010).
- **Assuming lab or Google-published simulated effects transfer at the same size.** They indicate direction, not magnitude (PRC-COPY-007/025).

## Unresolved questions
- No opened controlled field experiments on prices-in-ad-text, guarantees, or emotional vs functional copy in Google search ads; the evidence here is mostly practitioner and lab-based.
- How strongly Google's asset-selection model under-serves low-CTR qualifier assets under conversion-based bidding.
- How persuasion works in AI Mode and AI Overviews formats where Google writes or explains the ad.
- Whether eye-tracking patterns from 2017-2019 (NN/g) still hold on AI-Overview SERPs.
- Return-policy/guarantee meta-analytic evidence (Janakiraman et al. 2016) and IPA brand vs activation evidence could not be opened in this pass (publisher rate limit; fetch budget exhausted); re-check before citing.
- Size of the lead-quality penalty from "free" offers by vertical.
