---
area: measurement
topic: traffic quality and business economics
checked: 2026-10-13
owner: research
---
# Traffic quality, business economics and misleading metrics

This file covers three things: how to judge whether paid traffic is real and useful (invalid clicks, bots, form spam, search partners, GA4 engagement, Clarity behaviour signals), how to turn ad metrics into business economics (break-even CPC, contribution margin, POAS, CAC, payback, LTV, lead funnels, marginal returns), and which metrics mislead (CTR, micro-conversion CVR, brand ROAS, view-through, platform over-attribution). The single most important idea: **platform-reported return is an average, attributed number. Business decisions need marginal, incremental, margin-based numbers.** The strategist's job is to build the bridge between the two and to say how wide the uncertainty is.

### MEA-ECON-001 · Google filters invalid clicks before billing, and they never appear in campaign metrics
- **Claim:** Google defines invalid clicks as clicks that do not reflect genuine interest: accidental clicks, automated (bot or software) traffic, and manual clicks meant to inflate costs or publisher revenue. Google's automated systems filter them out of campaign metrics and billing. The "Invalid clicks" column, and "Invalid interactions" in reports, shows how many were removed.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Automated filters (machine learning) run in real time. A Traffic Quality team investigates manually and builds new filters. Google says the Media Rating Council (MRC) accredits its invalid traffic defences for specific services and metrics. Because filtered clicks are removed, reports can occasionally show more conversions than clicks: a converting click later judged invalid is removed, but the conversion stays.
- **When it matters / how experts use it:** Add the Invalid clicks column to campaign views. A rising invalid click *rate* (invalid ÷ (valid + invalid)) on a campaign, placement type or network points to where attacks or junk inventory are. The filtered clicks cost nothing. The real risk is invalid clicks that slip *through* the filters.
- **Exceptions and failure modes:** GA4 and server logs still record sessions from clicks that Ads filtered, so GA4 can show "paid" sessions that were never billed.
- **Signals in data:** Invalid click share spikes. Conversions exceed clicks at keyword or ad-group level. GA4 google/cpc sessions exceed billed clicks.
- **Sources:** [About invalid traffic](https://support.google.com/google-ads/answer/42995?hl=en) (checked 2026-10-13); [How Google protects against invalid traffic](https://support.google.com/google-ads/answer/11182074?hl=en) (checked 2026-10-13); [Google Ad Traffic Quality](https://www.google.com/ads/adtrafficquality/) (checked 2026-10-13); [Fix missing data and discrepancies](https://support.google.com/google-ads/answer/2404039) (checked 2026-10-13)

### MEA-ECON-002 · Invalid activity credits arrive later and do not restate campaign metrics
- **Claim:** If Google finds invalid traffic after a billing cycle closes, it issues credits "where appropriate and possible". They show as "Invalid activity" adjustments on the Billing Summary. Campaign metrics are *not* changed retroactively. Adjusted clicks, cost and conversion rate are visible only in the Invalid Activity Credit Report ("Credited clicks").
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Offline analysis catches patterns that real-time filters miss, and the money is returned through billing, not through reporting.
- **When it matters / how experts use it:** Finance reconciliation: actual cost = campaign cost minus invalid activity credits. Historic CPCs and CPAs in the UI are slightly overstated for credited periods.
- **Exceptions and failure modes:** Credits are not guaranteed for every invalid click, and Google does not explain decisions.
- **Signals in data:** Billing adjustments lines. A gap between UI cost and invoice amount.
- **Sources:** [How Google protects against invalid traffic](https://support.google.com/google-ads/answer/11182074?hl=en) (checked 2026-10-13)

### MEA-ECON-003 · Requesting an invalid click investigation: what evidence Google needs
- **Claim:** Advertisers can submit the Click Quality Form for activity in the past 60 days. Google asks for the customer ID, exact dates, campaign and ad group, suspicious keywords, server logs with IPs, device data and **GCLIDs**, and, for lead problems, a spreadsheet of each lead's GCLID with your assessment. Specialists review it manually, typically over several business days, and will not confirm whether individual clicks were judged valid.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** GCLIDs let Google join your evidence to its click records. IP addresses alone are weak because NAT (shared IPs) means one IP can serve many devices.
- **When it matters / how experts use it:** Log GCLIDs server-side and in the CRM all the time (also needed for offline import), so you can file evidence within the 60-day limit. Collect evidence before asking for credits.
- **Exceptions and failure modes:** Anecdotes ("a competitor is clicking") without click-level evidence rarely produce credits.
- **Signals in data:** Repeated leads with the same fake details tied to distinct GCLIDs. Bursts of clicks from one geography outside the targeting intent.
- **Sources:** [How Google protects against invalid traffic](https://support.google.com/google-ads/answer/11182074?hl=en) (checked 2026-10-13)

### MEA-ECON-004 · Click fraud claims vs evidence: treat vendor fraud rates as hypotheses
- **Claim:** Third-party "click fraud" vendors often publish high invalid traffic rates for paid search. These figures come from the vendors' own classifiers, which have their own incentives, and they are not independently validated. Google filters pre-billing and credits later, and it does not publish independent fraud rates. The defensible stance: measure *your* account's evidence (lead validity, GCLID-level behaviour, invalid click share trend) rather than adopting industry fraud percentages.
- **Evidence type:** inference (from documented Google process and the absence of independent audits among the sources opened)
- **Confidence:** medium
- **How it works:** Fraud tools flag clicks by IP, device fingerprint and behaviour. Many flagged clicks may already be filtered by Google (and not billed), and some flags are false positives, for example corporate NAT, VPNs and repeat research visits.
- **When it matters / how experts use it:** When a client wants to buy a fraud tool or blames "bots" for poor results, first check: invalid click column trend, lead validity rate from the CRM, geographic and search partner splits, and session behaviour (MEA-ECON-008 to 011). Use IP exclusions only for clear, stable offenders.
- **Exceptions and failure modes:** Display, Performance Max and partner inventory carry more invalid traffic risk than Google Search. High-CPC local services (locksmiths, legal) attract competitor and lead-gen abuse, so real issues exist there.
- **Signals in data:** Low-quality leads concentrated in a network, placement or hour. A traffic pattern that does not change with bids.
- **Sources:** [How Google protects against invalid traffic](https://support.google.com/google-ads/answer/11182074?hl=en) (checked 2026-10-13); [Google Ad Traffic Quality](https://www.google.com/ads/adtrafficquality/) (checked 2026-10-13)
- **Open questions:** No independent, audited estimate of residual (billed) invalid traffic on Google Search was found.

### MEA-ECON-005 · Bots and form spam poison Smart Bidding unless lead quality is fed back
- **Claim:** Spam form submissions that fire a conversion tag are, to Smart Bidding, indistinguishable from real leads. Bidding then learns to buy more of the traffic that produces them, often on Display, Performance Max or partner inventory. Google's own guidance for lead quality is safeguards such as reCAPTCHA and server-side validation, plus lead-focused goals. The structural fix is to bid on imported *qualified* leads (MEA-CONV-011).
- **Evidence type:** documented (Google's safeguards); inference (feedback-loop mechanism); practitioner (common pattern)
- **Confidence:** medium-high
- **How it works:** Value-based or CPA bidding maximizes the cheapest conversions. Bots convert cheaply, so a self-reinforcing loop forms.
- **When it matters / how experts use it:** Any lead-gen account where conversion volume rises and sales do not. Add honeypot fields, server-side validation and CAPTCHA. Fire the conversion only after validation. Use "One" counting. Import qualified status and value, and move the raw "form submit" action to secondary once the qualified action has volume.
- **Exceptions and failure modes:** Aggressive CAPTCHA reduces real conversion rate. Some spam is human (lead farms) and passes CAPTCHA.
- **Signals in data:** CPA falls while the CRM qualified rate falls. Leads with gibberish names or duplicated phone numbers. Spikes at odd hours. Conversion share shifting to Performance Max or Display placements.
- **Sources:** [How Google protects against invalid traffic](https://support.google.com/google-ads/answer/11182074?hl=en) (checked 2026-10-13); [Your guide to upgrading offline conversion imports](https://support.google.com/google-ads/answer/15479486?hl=en) (checked 2026-10-13)

### MEA-ECON-006 · Search partners: thin documentation, so judge by segment data, not reputation
- **Claim:** The Search Network includes "hundreds" of non-Google sites plus YouTube search results and watch pages. Partners must follow Google policies, but Google says "violations can occasionally happen". Google's partner page offers little on placement transparency, so partner quality must be judged from the account's own Network segment data.
- **Evidence type:** documented (definition); practitioner (quality varies)
- **Confidence:** medium
- **How it works:** Partner inventory has a different user context and click intent from Google.com. Smart Bidding sets bids by predicted conversion rate, so conversion-based bidding partly prices in partner quality, *if* the conversion signal is clean.
- **When it matters / how experts use it:** Segment by Network (with search partners) and compare CPA, *qualified-lead rate* and engagement. Practitioners often switch partners off for lead-gen with spam problems and keep them where conversion quality holds up. There is no universal rule.
- **Exceptions and failure modes:** When conversions are spammy, Smart Bidding over-values partners (MEA-ECON-005). Reported partner CPA can look cheap while CRM quality is poor.
- **Signals in data:** Partner CTR far above or below Google search. Partner conversions with low CRM qualification. High quick-back or low engagement for partner sessions (if distinguishable).
- **Sources:** [Search partners definition (Google Ads Help)](https://support.google.com/google-ads/answer/2616017?hl=en) (checked 2026-10-13)
- **Open questions:** Current (2026) placement-level reporting for search partners, and any recent changes to parked domain policy. Not verified this session.

### MEA-ECON-007 · GA4 engaged session and engagement rate: exact definitions
- **Claim:** A GA4 engaged session lasts more than 10 seconds, has a key event, or has 2+ page or screen views. `first_visit`, `first_open` and `session_start` do not count even if marked as key events. Engagement rate = engaged sessions ÷ sessions, and bounce rate is its inverse. The engaged-session timer (default 10 seconds) can be adjusted in the web data stream settings. Google's page states no allowed range; practitioners commonly cite a 60-second maximum (not verified). Session timeout defaults to 30 minutes.
- **Evidence type:** documented
- **Confidence:** high (definition); medium (timer range)
- **How it works:** Engagement time is accumulated from the page being visible/in focus (GA4 user_engagement mechanics, from prior knowledge). The threshold is an OR of three cheap conditions, so it is a low bar.
- **When it matters / how experts use it:** Engagement rate is useful as a *relative* measure: campaign vs campaign, partner vs Google, before vs after a landing page change. It is weak as an absolute quality score. Raise the timer (for example to 30 seconds) on content-heavy sites to make "engaged" more demanding, and annotate the change.
- **Exceptions and failure modes:** Key events count toward engagement, so a micro key event that fires on load (or a scroll event marked key) makes nearly every session engaged. Single-page apps without virtual page views look less engaged.
- **Signals in data:** Engagement rate near 100% (key event misconfiguration). A sudden engagement change on a configuration date.
- **Sources:** [GA4 engagement rate and bounce rate](https://support.google.com/analytics/answer/12195621?hl=en) (checked 2026-10-13); [GA4 adjust session timeout / engaged session timer](https://support.google.com/analytics/answer/12131703?hl=en) (checked 2026-10-13)

### MEA-ECON-008 · Limits of GA4 engagement as a traffic quality test
- **Claim:** GA4 engagement misses or distorts quality in five ways. (1) Sessions from clicks that Ads filtered as invalid still appear in GA4. (2) Without behavioural modelling, users who deny consent are invisible or only cookieless, and modelled data appears only under Blended identity. (3) Modern bots can scroll and wait past 10 seconds. (4) A long engaged time can mean confusion, not interest. (5) Event counts are never modelled.
- **Evidence type:** documented (1, 2, 5); inference (3, 4)
- **Confidence:** medium
- **How it works:** Engagement is a behavioural proxy, not a validity test. It does not prove a human or intent.
- **When it matters / how experts use it:** Combine it with outcome data: leads that qualify, revenue. Combine it with friction signals (Clarity, MEA-ECON-009) and with click-to-session ratios (MEA-ECON-011). Never optimize Smart Bidding to "engaged session" as a primary conversion without a validity check, because the bidder will find the cheapest traffic that satisfies the definition.
- **Exceptions and failure modes:** For traffic-only objectives, engagement may be the best available proxy. Mitigate by tightening the definition.
- **Signals in data:** Campaigns with high engagement but zero downstream outcomes over a meaningful sample.
- **Sources:** [GA4 behavioral modeling for consent mode](https://support.google.com/analytics/answer/11161109?hl=en) (checked 2026-10-13); [Fix missing data and discrepancies](https://support.google.com/google-ads/answer/2404039) (checked 2026-10-13); [GA4 engagement rate and bounce rate](https://support.google.com/analytics/answer/12195621?hl=en) (checked 2026-10-13)

### MEA-ECON-009 · Microsoft Clarity friction signals: rage clicks, dead clicks, quick backs, excessive scrolling
- **Claim:** Clarity flags **rage clicks** (rapid repeated clicks in a small area), **dead clicks** (no visible response or navigation within a "reasonable" time), **quick backs** (leaving to a page and returning faster than the page's dwell-time threshold), **excessive scrolling** (more vertical scrolling than the expected average), and JavaScript and click errors. Clarity does not publish numeric thresholds.
- **Evidence type:** documented
- **Confidence:** high (definitions); low (any absolute benchmark)
- **How it works:** These are heuristic, page-relative behavioural flags. Their value is in comparison (segment vs segment, before vs after a change) and in session recordings that show *why*.
- **When it matters / how experts use it:** Filter Clarity sessions by UTM or gclid presence to see paid-traffic friction. High quick backs on paid landings suggest a message mismatch between ad and page. Dead clicks on non-links suggest UI problems that depress conversion rate, which shows up as "bad traffic" when the real problem is the page.
- **Exceptions and failure modes:** Rage clicks also occur on slow-loading pages or carousels, and on legitimately repeated controls (quantity buttons). Thresholds may change, so compare within the same time period. Clarity's Bot Detection setting is admittedly incomplete (advanced bots can evade it). Recordings are capped at 100,000 sessions per project per day and kept 30 days. The GA integration adds a session-scoped "Clarity Playback URL" dimension, which lets you jump from a GA paid-traffic segment to recordings.
- **Signals in data:** Paid sessions with higher quick-back or dead-click share than organic. JavaScript errors concentrated on one browser.
- **Sources:** [Microsoft Clarity semantic metrics](https://learn.microsoft.com/en-us/clarity/insights/semantic-metrics) (checked 2026-10-13); [Microsoft Clarity FAQ](https://learn.microsoft.com/en-us/clarity/faq) (checked 2026-10-13)

### MEA-ECON-010 · Defining "good traffic" when the objective is traffic only
- **Claim:** When a campaign's stated objective is traffic, with no conversion, "good traffic" needs an explicit composite definition agreed up front. For example: cost per engaged session (with a tightened engagement timer), the share of sessions from target geographies and devices, a low quick-back and dead-click share, new-user share if acquisition is the goal, scroll or content-consumption events, and a click-to-session ratio near the account norm. Clicks or CTR alone reward accidental and low-intent traffic.
- **Evidence type:** inference (from documented metric definitions)
- **Confidence:** medium
- **How it works:** Each component removes one failure mode. Engagement removes instant bounces, geography removes off-target serving, Clarity flags remove frustrated visits, and the click-to-session ratio removes non-loading and bot clicks.
- **When it matters / how experts use it:** Awareness campaigns, content sites monetized by ads, or a "maximize clicks" setup. Track the composite as the KPI, and avoid bidding to raw clicks on Display or partner inventory without exclusions.
- **Exceptions and failure modes:** A traffic objective is often a proxy that the business has not examined. Ask what the traffic is *for*. If a downstream outcome exists (newsletter, return visits), measure that.
- **Signals in data:** Maximize-clicks campaigns drifting to very low CPCs on Display apps or partner inventory with near-zero engagement.
- **Sources:** [GA4 engagement rate and bounce rate](https://support.google.com/analytics/answer/12195621?hl=en) (checked 2026-10-13); [Microsoft Clarity semantic metrics](https://learn.microsoft.com/en-us/clarity/insights/semantic-metrics) (checked 2026-10-13)

### MEA-ECON-011 · The click-to-session gap is a quality and tracking signal
- **Claim:** Ads clicks normally exceed GA4 sessions somewhat. Google documents three reasons: multiple clicks in one session count once in GA, users who leave before the page loads give a click but no session, and consent or blockers reduce GA collection. Invalid clicks push the other way, because filtered in Ads they still appear in GA. A *change* in the ratio, or a ratio far from the account's norm in one segment, suggests slow pages, bot traffic, broken tags or redirect loss.
- **Evidence type:** documented (causes); inference (diagnostic use)
- **Confidence:** medium
- **How it works:** The two systems count different things: billed clicks vs sessions with a fired tag. Each break in the chain from click to page to tag to consent widens the gap.
- **When it matters / how experts use it:** Track the ratio weekly per campaign and network. A sudden rise on mobile points to slow landing pages. A rise on one placement or partner points to junk traffic. A rise everywhere on one date points to a tag or consent change.
- **Exceptions and failure modes:** In the EEA without behavioural modelling, large gaps are normal (consent).
- **Signals in data:** The ratio itself, by device, network and country.
- **Sources:** [Fix missing data and discrepancies](https://support.google.com/google-ads/answer/2404039) (checked 2026-10-13); [GA4 behavioral modeling for consent mode](https://support.google.com/analytics/answer/11161109?hl=en) (checked 2026-10-13)

### MEA-ECON-012 · Break-even CPC from conversion rate, value and contribution margin
- **Claim:** Break-even CPC = conversion rate × average order value × contribution margin %. Equivalently, value per click × margin. For lead generation: break-even CPC = click-to-lead rate × qualified-lead rate × close rate × contribution per sale.
- **Evidence type:** inference (arithmetic)
- **Confidence:** high (formula); the inputs are uncertain
- **How it works:** Example: CVR 3%, AOV €80, contribution margin 35% gives €0.84 break-even CPC. A target CPC must sit below that by the profit the business wants per click.
- **When it matters / how experts use it:** Sanity-check keyword viability before launch, using Keyword Planner CPC ranges against break-even. Set tCPA (break-even CPA = AOV × margin) or tROAS (MEA-ECON-014).
- **Exceptions and failure modes:** It uses *average* conversion rate, but the marginal click converts worse (MEA-ECON-019). It ignores LTV (MEA-ECON-017) and assisted value. Conversion-rate estimates from small samples are noisy: 3 conversions in 100 clicks has a wide interval.
- **Signals in data:** Keywords whose actual CPC exceeds break-even while the account's average ROAS looks fine.
- **Sources:** None needed (arithmetic); inputs come from the account and finance.

### MEA-ECON-013 · Contribution margin, not revenue or gross margin, is the right value base
- **Claim:** Contribution margin per order = revenue − COGS − variable costs per order (shipping, payment fees, packaging, pick and pack, expected returns and refunds, marketplace fees). Using gross margin, or revenue, overstates what each conversion is worth to the business.
- **Evidence type:** inference (standard managerial accounting)
- **Confidence:** high
- **How it works:** Ad spend is a variable acquisition cost. The question "is this click worth buying?" depends on cash left after the order's own variable costs.
- **When it matters / how experts use it:** Ask finance for contribution margin by category. Return rates matter a lot in fashion. Free-shipping thresholds change margin by basket size.
- **Exceptions and failure modes:** Fixed costs are excluded deliberately. Do not allocate rent to the ROAS target, but the business still needs total contribution to cover fixed costs.
- **Signals in data:** High-revenue categories with high return rates that look great on ROAS and poor in finance.
- **Sources:** None (accounting definition).

### MEA-ECON-014 · ROAS vs POAS, and break-even ROAS = 1 ÷ margin
- **Claim:** Break-even ROAS (revenue ÷ ad cost) = 1 ÷ contribution margin %. A 25% margin needs 4.0 ROAS (400%) just to break even. POAS (profit on ad spend) uses contribution profit as the conversion value, so break-even POAS = 1.0. Passing profit instead of revenue makes tROAS bidding optimize toward profit directly.
- **Evidence type:** inference (arithmetic); practitioner (POAS implementation)
- **Confidence:** high (math); medium (implementation benefits)
- **How it works:** With mixed margins across products, revenue-ROAS bidding favours high-price, low-margin items. Profit-based values re-rank the same clicks.
- **When it matters / how experts use it:** E-commerce with margin dispersion. Implementation is via server-side or GTM computation of profit per order, a conversion value rule, or Data Manager uploads. Keep a revenue action as secondary for reporting continuity.
- **Exceptions and failure modes:** Profit values reveal margins to the ad platform (a confidentiality decision). Profit data must account for returns, which arrive later; use adjustments. Very low profit values make tROAS targets hard to interpret for stakeholders.
- **Signals in data:** ROAS above target while finance reports losses. Top-selling products by revenue with low or negative contribution.
- **Sources:** None opened for POAS practitioner material this session (search budget exhausted); arithmetic is self-evident.

### MEA-ECON-015 · CAC, payback period and why first-order ROAS can be "too strict" or "too loose"
- **Claim:** CAC = acquisition spend ÷ new customers acquired (not total conversions). Payback period = CAC ÷ monthly contribution per customer. Subscription and repeat-purchase businesses can rationally accept first-order losses if the payback is within their cash constraints. One-off-purchase businesses cannot.
- **Evidence type:** inference (standard unit economics)
- **Confidence:** high (definitions)
- **How it works:** Google Ads conversions include returning customers, so cost per conversion is lower than true CAC. A new-customer split, via customer lists, new customer acquisition goals or CRM matching, is needed.
- **When it matters / how experts use it:** Setting targets for subscription, SaaS and DTC replenishment businesses. Agree the maximum payback (for example 3, 6 or 12 months) with finance. Then derive the allowable CAC and convert it to a tCPA on new customers.
- **Exceptions and failure modes:** Brand search conversions are mostly existing customers, which makes CAC look tiny (MEA-ECON-021).
- **Signals in data:** Share of conversions from returning customers (CRM match). Payback cohorts lengthening as spend scales.
- **Sources:** None (definitions).

### MEA-ECON-016 · Lead-to-sale funnels: value per lead and the qualified-lead rate
- **Claim:** Value per lead = qualified-lead rate × close rate × average contribution per sale. Platform CPA on raw leads is meaningless without the qualified rate, which commonly differs a lot by campaign, keyword theme, network and device.
- **Evidence type:** inference (arithmetic); practitioner (variation by segment)
- **Confidence:** high (formula); medium (variation claim)
- **How it works:** A €40 CPA lead with 10% qualification costs €400 per qualified lead. A €80 CPA lead with 40% qualification costs €200.
- **When it matters / how experts use it:** Import funnel stages as offline conversions (MEA-CONV-011) with values (expected value at lead stage, actual value at won stage). Compute cost per qualified lead by segment monthly. Bid on the deepest stage with enough volume.
- **Exceptions and failure modes:** Long sales cycles delay ground truth by months. Use leading stages with *calibrated* expected values and revisit the calibration quarterly. Sales-team qualification can be inconsistent.
- **Signals in data:** CPA improving while the cost per qualified lead or per sale worsens. Strong qualified-rate differences between search terms.
- **Sources:** [About offline conversion imports](https://support.google.com/google-ads/answer/2998031?hl=en) (checked 2026-10-13)

### MEA-ECON-017 · LTV is a forecast with wide error bars, so use it conservatively
- **Claim:** Customer lifetime value (LTV) used for bidding or CAC limits is a forecast. It is based on cohort retention and margin, should be discounted for time and risk, and is usually estimated from immature cohorts. Over-estimating LTV is a common way to justify unprofitable acquisition.
- **Evidence type:** inference
- **Confidence:** high (principle)
- **How it works:** LTV = Σ (expected contribution in period t × retention to t) ÷ (1 + discount rate)^t. Early cohorts extrapolated forward often assume retention curves flatten more than they do. Paid-acquired customers may retain differently from organic ones.
- **When it matters / how experts use it:** Use a horizon-limited LTV (for example 12-month contribution) rather than an open-ended one. Use paid-cohort retention where possible. Express the target as a range, and test with tighter targets first. Pass a new-customer premium through value rules or new customer acquisition goals only with a documented basis.
- **Exceptions and failure modes:** Mature subscription businesses with years of cohort data can use longer horizons.
- **Signals in data:** Cohort revenue curves for paid-acquired customers falling below the LTV assumption. Rising CAC as spend scales with no retention gain.
- **Sources:** None (finance principle).

### MEA-ECON-018 · Marginal vs average returns: the last euro earns less than the average euro
- **Claim:** Account or campaign ROAS is an *average*. The return on the next increment of spend (marginal ROAS) is lower, often much lower, because auctions get more expensive and less-intent queries come in as spend rises. Scaling decisions should use marginal estimates: bid simulators, incremental budget tests, or experiment splits.
- **Evidence type:** inference (diminishing returns); study (eBay: average returns hide segment differences, and frequent users absorb most spend with no behaviour change)
- **Confidence:** high (direction); the size is specific to each account
- **How it works:** Example: €10k at 5.0 ROAS → €15k at 4.2 ROAS means the extra €5k produced €13k, a marginal ROAS of 2.6. That is below break-even at a 30% margin (3.33) even though the average is "above target".
- **When it matters / how experts use it:** Budget increases, tROAS relaxations and "scale what works" requests. Compute marginal ROAS between budget steps. Treat Google's simulators as model estimates.
- **Exceptions and failure modes:** Under-funded campaigns that are "Limited by budget" with impression share lost to budget can have near-constant marginal returns over a range.
- **Signals in data:** Falling ROAS as spend rises. CPC inflation. A rising share of broad and loosely matched search terms.
- **Sources:** [Blake, Nosko, Tadelis: Consumer heterogeneity and paid search effectiveness (NBER w20171)](https://www.nber.org/papers/w20171) (checked 2026-10-13)

### MEA-ECON-019 · CTR is a weak quality metric on its own
- **Claim:** CTR rises with brand terms, top positions, larger ad formats and assets, and curiosity-bait copy. None of these mean buyer intent. High CTR with low conversion or qualification can mean misleading copy or broad query matching. Low CTR on generic queries can be normal.
- **Evidence type:** inference; practitioner
- **Confidence:** medium
- **How it works:** CTR = clicks ÷ impressions. Both terms depend on position, SERP layout and query mix, not only on relevance.
- **When it matters / how experts use it:** Compare CTR only within a like-for-like query set and position. Use it to diagnose ad relevance (an input to expected-CTR components), not as an outcome.
- **Exceptions and failure modes:** In traffic-objective campaigns, CTR matters more, but still needs the quality composite (MEA-ECON-010).
- **Signals in data:** CTR up and CVR down after a copy change. Brand campaigns dominating account CTR.
- **Sources:** None opened specifically; reasoning from metric definitions.

### MEA-ECON-020 · Conversion rate inflated by micro-conversions
- **Claim:** When micro-conversions (page views, scrolls, add-to-cart, clicks on email or phone links) are primary, or are included in the KPI, conversion rate and CPA describe *those* actions, not business outcomes. Such numbers can improve while sales fall.
- **Evidence type:** documented (column composition); inference (misreading)
- **Confidence:** high
- **How it works:** "Conversions" includes every primary action in the used goals (MEA-CONV-001). Cheap, frequent actions dominate the count.
- **When it matters / how experts use it:** Always report CPA and CVR per conversion action (segment by Conversion action), and use "All conv." for micro-actions. Stakeholder dashboards should show the business-outcome action separately.
- **Exceptions and failure modes:** Very low-volume accounts may deliberately bid to a mid-funnel action. Document the proxy and validate it against sales.
- **Signals in data:** Conversions per click above 20-30% on non-brand search for a typical business. This rule-of-thumb threshold is a practitioner red flag, not a rule.
- **Sources:** [About primary and secondary conversion actions](https://support.google.com/google-ads/answer/11461796) (checked 2026-10-13)

### MEA-ECON-021 · Brand search ROAS is mostly non-incremental, except when competitors are present
- **Claim:** Brand campaigns show the highest platform ROAS in most accounts, but the causal effect varies a lot. In eBay's field experiments, brand keyword ads had "no measurable short-term benefits". Bing experiments across thousands of brands (Simonov, Nosko & Rao, 2018) found brand ads add only about 1-4% clicks when no competitors bid. When competitors bid and the brand does not, competitors capture about 18-42% of the brand's clicks. So defensive brand bidding can have strongly positive ROI.
- **Evidence type:** study
- **Confidence:** high (that brand ROAS overstates incrementality); medium (size for any given advertiser)
- **How it works:** Searchers who type a brand name mostly intend to visit it, and organic results capture them if the ad is absent, *unless* competitor ads or other SERP features intercept them. Incrementality therefore depends on competitive pressure on the brand SERP, the organic listing's strength, and SERP layout.
- **When it matters / how experts use it:** Never use blended ROAS that includes brand to justify non-brand spend. Report brand separately. Estimate brand incrementality with a geo or time holdout, observing total (paid + organic) brand clicks and conversions, and check the Auction insights competitor presence first.
- **Exceptions and failure modes:** Weak organic listings (new brands, retailers outranking the brand, ambiguous brand names) make brand ads more incremental. Studies predate AI Overviews and the 2024-2026 SERP changes.
- **Signals in data:** Brand ROAS 10x+ non-brand. Auction insights showing competitors on brand terms. Organic brand clicks rising when paid brand is paused (Search Console).
- **Sources:** [Blake, Nosko, Tadelis (NBER w20171)](https://www.nber.org/papers/w20171) (checked 2026-10-13); [Simonov, Nosko, Rao: Competition and crowd-out for brand keywords in sponsored search (Marketing Science 2018)](https://pubsonline.informs.org/doi/10.1287/mksc.2017.1065) (checked 2026-10-13)

### MEA-ECON-022 · Google's "Search Ads Pause" studies: 89% incremental *clicks*, about 50% when you rank #1 organically
- **Claim:** Google meta-analyses of 400+ pause studies (2011) found that on average 89% of paid clicks are incremental, meaning they are not replaced by organic clicks when ads pause. A follow-up of 390 studies found that when the advertiser holds the #1 organic position, about 50% of ad clicks are incremental. With no organic listing, essentially 100% are.
- **Evidence type:** study (Google research, observational and modelled)
- **Confidence:** medium
- **How it works:** Organic click volume observed during pauses is fed into a model that predicts clicks from spend and organic impressions.
- **When it matters / how experts use it:** These are *click* incrementality estimates, not conversion or profit incrementality, and averages across verticals. They support "paid search is largely incremental for non-brand" and "brand with a strong #1 organic listing is about half incremental at best". Pair them with MEA-ECON-021.
- **Exceptions and failure modes:** The data dates from 2011 with an older SERP layout. The authors are Google employees with an interest in the result. Conversion incrementality on brand can be lower than click incrementality, because people who would have clicked organically convert anyway.
- **Signals in data:** n/a (benchmark).
- **Sources:** [Google Research: Incremental clicks impact of search advertising](https://research.google/pubs/incremental-clicks-impact-of-search-advertising/) (checked 2026-10-13); [Google Research: Impact of ranking of organic search results on the incrementality of search ads](https://research.google/pubs/impact-of-ranking-of-organic-search-results-on-the-incrementality-of-search-ads/) (checked 2026-10-13)

### MEA-ECON-023 · View-through and engaged-view conversions are correlational credit
- **Claim:** View-through conversions (1-day default window, counted when an impression was served and the user converted with no click) and engaged-view conversions (a 10-second or 5-second video watch) assign credit for exposure. Exposure targeting selects people likely to convert anyway, so these numbers overstate causal impact unless validated by lift tests.
- **Evidence type:** documented (definitions, windows); inference (selection bias); study (eBay shows the general gap between correlational and causal returns)
- **Confidence:** medium-high
- **How it works:** Remarketing and Performance Max audience signals put impressions in front of existing intenders, and a cheap impression precedes a purchase that was already planned. Transaction IDs do not deduplicate view-through conversions.
- **When it matters / how experts use it:** Evaluate Display, YouTube, Demand Gen and Performance Max with lift tests or geo experiments. Discount view-based credit in finance views. Segment "Ad event type" to see the click-through share.
- **Exceptions and failure modes:** Genuine upper-funnel effects exist. The point is that the platform metric cannot tell you their size.
- **Signals in data:** A high share of engaged-view or view-through conversions in Performance Max or Demand Gen. Conversions concentrated in remarketing audiences.
- **Sources:** [About conversion windows](https://support.google.com/google-ads/answer/3123169) (checked 2026-10-13); [About Engaged-view conversions](https://support.google.com/google-ads/answer/10048752?hl=en) (checked 2026-10-13); [Use a transaction ID](https://support.google.com/google-ads/answer/6386790?hl=en) (checked 2026-10-13); [NBER w20171](https://www.nber.org/papers/w20171) (checked 2026-10-13)

### MEA-ECON-024 · Platform over-attribution: the sum of platform conversions exceeds reality
- **Claim:** Each ad platform attributes conversions using its own touchpoints, windows and modelling. Google Ads DDA shares credit only among Google ads, and it adds modelled, cross-device and engaged-view conversions. Summing Google, Meta, Microsoft and others therefore routinely exceeds actual orders. GA4 cross-channel attribution and the CRM are the de-duplicating references.
- **Evidence type:** documented (Google's scope and modelling); inference (summation problem)
- **Confidence:** high
- **How it works:** No platform subtracts credit claimed by others. Each is incentivized and designed to show its own contribution.
- **When it matters / how experts use it:** Multi-channel advertisers. Report "platform-claimed" vs "deduplicated (GA4/CRM)" vs "incremental (tests)" as three separate tiers, and budget on the lowest tier you trust.
- **Exceptions and failure modes:** GA4 also under-credits upper-funnel channels and loses unconsented users. No single number is "true".
- **Signals in data:** Sum of platform conversions ÷ CRM orders > 1.2-1.5 (practitioner heuristic for when over-claiming is severe; it varies by channel mix).
- **Sources:** [About data-driven attribution](https://support.google.com/google-ads/answer/6394265) (checked 2026-10-13); [About consent mode modeling](https://support.google.com/google-ads/answer/10548233?hl=en) (checked 2026-10-13); [GA4 attribution settings](https://support.google.com/analytics/answer/10597962?hl=en) (checked 2026-10-13)

### MEA-ECON-025 · Incrementality tests: Google Conversion Lift and geo experiments
- **Claim:** Google's Conversion Lift splits audiences into treatment and control, by user or by geography, and reports incremental conversions, incremental value, iCPA and iROAS. Geo-based lift supports offline data. Google's Help page says it "isn't available for all accounts" and directs advertisers to their Google representative. Independent geo holdouts (turning campaigns off in matched regions) are the self-serve alternative.
- **Evidence type:** documented
- **Confidence:** high (feature); medium (availability in 2026, where reports of lower thresholds could not be verified this session)
- **How it works:** Randomized or quasi-randomized exposure removes selection bias, so the difference between groups estimates causal effect.
- **When it matters / how experts use it:** Before scaling Performance Max, Demand Gen, YouTube or brand. To calibrate platform ROAS into an "incrementality factor" (iROAS ÷ platform ROAS) applied in finance reporting until the next test.
- **Exceptions and failure modes:** Small budgets give wide confidence intervals and inconclusive results. Short tests miss lagged effects. Geo spillover (people commuting between regions) and seasonality bias geo tests.
- **Signals in data:** n/a (method).
- **Sources:** [About Conversion Lift](https://support.google.com/google-ads/answer/12003020?hl=en) (checked 2026-10-13)
- **Open questions:** 2025-2026 changes to Conversion Lift eligibility and minimum spend for Search and Performance Max (not verified).

### MEA-ECON-026 · The metrics bridge: platform → analytics → CRM → finance
- **Claim:** Experts reconcile through a fixed chain. They write down each layer's unit, date basis and scope, and convert platform numbers into finance numbers with explicit, periodically recalibrated factors:
  1. **Ads:** clicks, cost and conversions by click date, Google-only, including modelled conversions.
  2. **Analytics:** sessions and key events by event date, cross-channel, consent-limited.
  3. **CRM:** leads, qualified leads, deals and customers by created or closed date.
  4. **Finance:** revenue, contribution and cash, after returns and credits.
- **Evidence type:** inference (built from documented differences: MEA-CONV-021, 025; MEA-ECON-002, 011)
- **Confidence:** medium
- **How it works:** Bridge factors: Ads conversions → CRM-matched conversions (match ratio), CRM leads → qualified → won (funnel rates), revenue → contribution (margin), platform-claimed → incremental (lift factor), and invoice cost = UI cost − invalid activity credits. Each factor is tracked monthly, and its drift is itself a diagnostic.
- **When it matters / how experts use it:** Target setting: derive the tCPA or tROAS from finance's allowable CAC through the factors. Client reporting: show all layers. Diagnosis: find which factor moved.
- **Exceptions and failure modes:** Factors estimated from small samples are noisy, so use rolling 3-month windows. Factors change after tracking changes (consent mode launch, enhanced conversions) and must be re-baselined.
- **Signals in data:** A factor jumps on a known change date (a tracking artifact) vs drifts gradually (a real business change).
- **Sources:** [Fix missing data and discrepancies](https://support.google.com/google-ads/answer/2404039) (checked 2026-10-13); [About "by conversion time" columns](https://support.google.com/google-ads/answer/9549009?hl=en) (checked 2026-10-13); [How Google protects against invalid traffic](https://support.google.com/google-ads/answer/11182074?hl=en) (checked 2026-10-13)

### MEA-ECON-027 · Value per click as the unifying efficiency metric
- **Claim:** Value per click (conversion value ÷ clicks, or contribution ÷ clicks) combines conversion rate and order value into the number that should be compared with CPC. Value per click minus CPC is profit per click, and profit per click × clicks is the total that should be maximized. ROAS or CPA targets are only proxies for that.
- **Evidence type:** inference
- **Confidence:** high
- **How it works:** Maximizing ROAS shrinks volume toward the most efficient clicks, and maximizing volume ignores efficiency. Profit = Σ(value/click − CPC) is maximized where marginal value per click equals marginal CPC.
- **When it matters / how experts use it:** Explaining to clients why a lower ROAS at higher spend can mean more profit, *if* the marginal ROAS stays above break-even (MEA-ECON-018). Choosing between tROAS levels with simulator outputs.
- **Exceptions and failure modes:** Cash-constrained businesses may prefer efficiency over total profit.
- **Signals in data:** The "Conv. value / click" column vs "Avg. CPC" by segment.
- **Sources:** None (arithmetic).

### MEA-ECON-028 · Modelled and consent-recovered conversions in economic reporting
- **Claim:** Since "Conversions" and "Conv. value" include consent-mode modelled conversions, cross-device and braid modelling, Google Ads value will normally exceed what finance can tie to specific orders. This is by design. Finance-facing ROAS should use CRM or finance revenue with a documented attribution rule, and Ads ROAS stays the bidding signal.
- **Evidence type:** documented (inclusion); inference (reporting rule)
- **Confidence:** high
- **How it works:** Modelled conversions estimate real but unobservable conversions. Google designs them to avoid over-prediction, so the "excess" is not necessarily wrong. It is simply not order-traceable.
- **When it matters / how experts use it:** EEA accounts, iOS-heavy audiences, and any client who asks "why don't the numbers match?".
- **Exceptions and failure modes:** Below modelling thresholds there is little modelled data.
- **Signals in data:** Ads conversions ÷ gclid-matched CRM orders stable at above 1.
- **Sources:** [About consent mode modeling](https://support.google.com/google-ads/answer/10548233?hl=en) (checked 2026-10-13)

### MEA-ECON-029 · Bidding to a proxy metric invites the system to game the proxy
- **Claim:** Smart Bidding optimizes whatever it is given. Make engaged sessions, page views, form starts or tap-to-call clicks primary, and the system will find the cheapest inventory that produces them. That inventory includes accidental, low-intent or automated traffic. The more automated the campaign type (Performance Max, Display), the stronger this effect.
- **Evidence type:** inference (from documented bidding mechanics); practitioner (widely reported pattern)
- **Confidence:** medium
- **How it works:** This is Goodhart's law applied to ML bidding: the conversion definition is the objective function.
- **When it matters / how experts use it:** Choose the deepest reliable outcome as the objective. When a proxy is unavoidable, harden it (validated leads, longer engagement thresholds, value rules) and monitor downstream quality.
- **Exceptions and failure modes:** Search campaigns with tight keyword sets are less exposed than inventory-rich campaign types.
- **Signals in data:** Conversion volume rises sharply after adding a proxy action, while downstream outcomes stay flat. Placements shift toward apps and partners.
- **Sources:** [About conversion goals](https://support.google.com/google-ads/answer/10995103) (checked 2026-10-13)

### MEA-ECON-030 · Uncertainty must be reported with every economic estimate
- **Claim:** Conversion rate, qualified rate, LTV and incrementality factors are all estimates with sampling error. For small numbers of conversions, intervals are wide (for example, 5 conversions out of 200 clicks gives a 95% interval of roughly 0.8% to 5.7%). Decisions such as pausing a keyword or changing a target should reflect the interval, not the point estimate.
- **Evidence type:** inference (binomial statistics)
- **Confidence:** high
- **How it works:** With a Wilson or exact interval, 5/200 = 2.5% (CI about 1.1% to 5.7% Wilson; about 0.8% to 5.7% exact). So a break-even CPC estimated from it ranges about 5-fold.
- **When it matters / how experts use it:** Low-volume accounts, keyword-level decisions, and A/B landing page tests. Pool data (longer periods, keyword themes), or wait for more data before acting.
- **Exceptions and failure modes:** Large-volume campaigns have tight intervals, and there bias (attribution, tracking) dominates sampling error.
- **Signals in data:** Keywords "with zero conversions" after a number of clicks still consistent with the account conversion rate.
- **Sources:** None (statistics).

## Common mistakes and misleading metrics
- **Blended ROAS including brand** used to justify non-brand or Performance Max spend (MEA-ECON-021, 022).
- **ROAS targets set without margin.** A "good" 300% ROAS loses money at a 25% margin (MEA-ECON-014).
- **Average ROAS as the scaling argument** instead of marginal ROAS (MEA-ECON-018).
- **CPA on raw leads** without qualified-lead rate. Spam and junk lower CPA (MEA-ECON-005, 016).
- **CTR as the success metric** (MEA-ECON-019).
- **Micro-conversions in the conversion rate** (MEA-ECON-020).
- **Engagement rate read as human validity.** Bots and misconfigured key events pass it (MEA-ECON-007, 008).
- **Vendor click fraud percentages taken as fact** without account-level evidence (MEA-ECON-004).
- **Summing platform conversions** across channels (MEA-ECON-024).
- **Treating view-through and engaged-view credit as causal** (MEA-ECON-023).
- **Using UI cost for finance** while ignoring invalid activity credits (MEA-ECON-002).
- **LTV assumptions from immature cohorts** used to justify loss-making CAC (MEA-ECON-017).
- **Point estimates on tiny samples** (MEA-ECON-030).

## Unresolved questions
- An independent, audited estimate of residual (billed) invalid traffic on Google Search vs Search Partners vs Performance Max. None found.
- Search partner placement transparency and quality controls as of 2026 (not verified this session).
- Conversion Lift availability and minimum spend for Search and Performance Max in 2025-2026. Practitioner reports of lower thresholds were not verified.
- How AI Overviews and AI Mode (2024-2026) change brand-search incrementality relative to the 2011-2018 studies.
- Exact Clarity thresholds for rage clicks, dead clicks and quick backs. Clarity documents a Bot Detection setting, but not its method or accuracy.
- The GA4 engaged-session timer's allowed range. Google's page states only the 10-second default; the 60-second maximum is practitioner lore.
- No opened practitioner source on POAS adoption outcomes. Benefits vs revenue-based tROAS remain unquantified.
