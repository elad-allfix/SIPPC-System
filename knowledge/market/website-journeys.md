---
area: market
topic: website and post-click journey diagnosis
checked: 2026-10-13
owner: research
---
# Diagnosing websites and user journeys after the ad click

How to judge what happens between the ad click and a sale: landing page continuity, speed, mobile usability, forms, trust, pricing, analytics instrumentation, tracking reliability and the business's handling of leads and calls. The single most important idea: **verify measurement and lead handling before redesigning pages**. A broken tag, duplicated thank-you page, or unanswered phone can make a good page look bad (or a bad page look good), and most published "conversion lift" numbers are case studies or vendor data that only tell you what to test, not what will happen.

### MKT-WEB-001 · The first five minutes: an expert landing-page review protocol
- **Claim:** An experienced reviewer checks, in order: (1) does tracking work (submit a test lead; see it in Google Ads/GA4 and the CRM), (2) does the page answer the query that triggered the ad in the first screen (message match), (3) mobile load and usability on a real phone over cellular, (4) the conversion path (form/call) end to end, (5) trust and price disclosure, (6) what happens after submission (confirmation, follow-up speed).
- **Evidence type:** practitioner; inference (ordering by the cost of being wrong)
- **Confidence:** medium
- **How it works:** Measurement failures invalidate every other conclusion; continuity and mobile issues affect most visitors; trust/price issues affect consideration; post-submission issues affect revenue but not on-site metrics.
- **When it matters / how experts use it:** Use as the default checklist for a new client; record each finding as observed / inferred / needs data. Review from the actual final URL of a top ad (with parameters), not the home page.
- **Exceptions and failure modes:** A five-minute review finds obvious defects, not the best variant; anything beyond defects needs data (MKT-WEB-027).
- **Signals in data:** Clicks with few sessions (tracking or redirect loss); sessions with near-zero engagement; leads in Ads not in CRM.
- **Sources:** synthesis of MKT-WEB-002 to MKT-WEB-026; [How Google Ads tracks website conversions – Google Ads Help](https://support.google.com/google-ads/answer/7521212) (checked 2026-10-13)

### MKT-WEB-002 · Message match: the first screen should continue the query and the ad
- **Claim:** Google describes higher-rated landing pages as having "text that relates to a person's search terms" and being "clear and useful" and "well organized". In practice, the headline and first screen should repeat the searcher's problem/service and the ad's promise (offer, price, location, speed) so the visitor recognises they are in the right place.
- **Evidence type:** documented (Google's definition); practitioner (continuity heuristic)
- **Confidence:** medium-high
- **How it works:** Visitors scan for confirmation of the "scent" that made them click; a mismatch (generic home page, different offer, different location) creates doubt and back-clicks. For Google, landing page relevance feeds the landing page experience assessment.
- **When it matters / how experts use it:** Map each ad group/intent cluster to a page whose H1 and first-screen copy reflect it; if the ad mentions a price, guarantee or "same day", the page must show it above the fold. Dynamic text on pages should not create absurd or non-compliant headlines.
- **Exceptions and failure modes:** Over-literal matching (keyword-stuffed H1) can harm readability; with broad match/AI Max the triggering queries vary, so match the intent cluster rather than every keyword.
- **Signals in data:** Low engagement rate and quick backs on one ad group's landing page but not others; "Below average" landing page experience in keyword diagnostics.
- **Sources:** [Landing page experience: Definition – Google Ads Help](https://support.google.com/google-ads/answer/1659694) (checked 2026-10-13)

### MKT-WEB-003 · Attention concentrates in the first screens (desktop eye-tracking evidence)
- **Claim:** In NN/g's 2018 eye-tracking study (120 participants, 130,000+ fixations, 1920×1080 desktop screens), 57% of viewing time was above the fold and 74% within the first two screenfuls; in 2010 it was 80% above the fold.
- **Evidence type:** study
- **Confidence:** medium (desktop, lab tasks; not specific to ad landing pages)
- **How it works:** People decide quickly whether to invest in scrolling based on what the first screen promises; attention decays down the page.
- **When it matters / how experts use it:** Put the value proposition, proof and primary CTA in the first screen; long pages are fine if the top earns the scroll. On mobile the first screen is smaller, so prioritise ruthlessly.
- **Exceptions and failure modes:** The analysis ignores page length (short pages inflate the top share); mobile behaviour was not measured; motivated, high-consideration visitors read deeper.
- **Signals in data:** Clarity or GA4 scroll depth showing most visitors never reach the form; CTA clicks concentrated in the hero.
- **Sources:** [Scrolling and Attention – Nielsen Norman Group, 2018-04-15](https://www.nngroup.com/articles/scrolling-and-attention/) (checked 2026-10-13)

### MKT-WEB-004 · Landing page quality in Google Ads: diagnostic score vs auction input
- **Claim:** Quality Score (with landing page experience as one of three components) "is not an input in the ad auction" and is "a diagnostic tool". Ad Rank, however, uses "the quality of your ads and landing page" at auction time, together with bid, thresholds, competitiveness, search context and expected asset impact.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google's real-time quality assessment influences position and price; the 1-10 Quality Score is a summarised, historical view of that assessment for exact-match-like traffic.
- **When it matters / how experts use it:** Treat "Below average" landing page experience as a pointer to relevance/usability issues, not a metric to optimise directly. Improvements can lower CPCs and improve position because they affect auction-time quality.
- **Exceptions and failure modes:** QS components are often blank or "-" for low-volume keywords; changing pages for QS alone without user benefit rarely helps.
- **Signals in data:** Landing page experience "Below average" across many keywords pointing to one URL.
- **Sources:** [About Quality Score for Search campaigns – Google Ads Help](https://support.google.com/google-ads/answer/6167118) (checked 2026-10-13); [About Ad Rank – Google Ads Help](https://support.google.com/google-ads/answer/1752122) (checked 2026-10-13); [Landing page experience: Definition – Google Ads Help](https://support.google.com/google-ads/answer/1659694) (checked 2026-10-13)

### MKT-WEB-005 · Core Web Vitals: what is documented for SEO vs for Google Ads
- **Claim:** For Search (organic), Google states Core Web Vitals "are used by our ranking systems" but good scores do not guarantee ranking, and relevant content can still rank with sub-par page experience. "Good" thresholds: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at the 75th percentile of page loads, mobile and desktop separately. The Google Ads Help pages we opened on Quality Score and landing page experience do **not** mention Core Web Vitals.
- **Evidence type:** documented (SEO and thresholds); inference (Ads relation)
- **Confidence:** high (SEO statements); low (any direct CWV → Ads quality link)
- **How it works:** For Ads, speed plausibly matters through user behaviour (abandonment before the page renders, lower conversion) and Google's general landing page usability assessment, but there is no documented use of CWV metrics in Ad Rank.
- **When it matters / how experts use it:** Do not promise clients "better Quality Score from CWV". Justify speed work by conversion and abandonment evidence on their own site (clicks vs sessions gap, mobile vs desktop conversion gap).
- **Exceptions and failure modes:** Passing CWV with a slow server redirect chain or heavy consent banner still loses impatient visitors; a page can fail CWV and convert well when intent is high.
- **Signals in data:** Large gap between Google Ads clicks and GA4 sessions on mobile; poor field LCP/INP in PageSpeed Insights.
- **Sources:** [Understanding page experience in Google Search results – Google Search Central (updated 2026-09-22)](https://developers.google.com/search/docs/appearance/page-experience) (checked 2026-10-13); [Web Vitals – web.dev](https://web.dev/articles/vitals) (checked 2026-10-13); [Landing page experience: Definition – Google Ads Help](https://support.google.com/google-ads/answer/1659694) (checked 2026-10-13)
- **Open questions:** Google's separate article "Understanding landing page experience" (which historically mentioned load time) could not be opened during this research.

### MKT-WEB-006 · Speed-to-conversion evidence is case-study grade
- **Claim:** Published links between faster pages and more conversions are mostly company-reported case studies (e.g. Vodafone Italy: 31% LCP improvement linked to 8% more sales; Redbus: TTI halved linked to 80-100% higher mobile conversion), correlational and often bundled with other changes. Widely quoted Think with Google mobile-speed statistics are no longer available at their original URL (redirects to a generic hub as of 2026-10-13).
- **Evidence type:** study (self-reported case studies)
- **Confidence:** medium (direction); low (size of effect for any given site)
- **How it works:** Slow rendering increases abandonment before the page is seen and adds friction to interaction (forms, buttons).
- **When it matters / how experts use it:** Use these as reasons to test, not forecasts. Prioritise speed when the mobile clicks-to-sessions gap is large or field LCP/INP is poor; estimate value from the client's own data.
- **Exceptions and failure modes:** Cite stats with their source and date; avoid the "53% abandon after 3 seconds" figure unless you can open the original (it dates to 2016-2017 Google data).
- **Signals in data:** Sessions per click falling on slow mobile networks; conversion rate gap by device.
- **Sources:** [Business impact of Core Web Vitals – web.dev case studies (last updated 2021-09-01)](https://web.dev/case-studies/vitals-business-impact) (checked 2026-10-13); thinkwithgoogle.com mobile page speed benchmarks page (redirected to business.google.com/en-all/think/ on 2026-10-13, original content not available)

### MKT-WEB-007 · Measure speed with field data at the 75th percentile, on mobile
- **Claim:** Google's guidance is to assess Core Web Vitals at the 75th percentile of real page loads, segmented by device; "only field measurement can accurately capture the complete picture". Lab tests (Lighthouse) are for debugging.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Real users have slower devices and networks than developers; the 75th percentile captures the slow tail that drives abandonment.
- **When it matters / how experts use it:** Check PageSpeed Insights field data for the landing URL (or origin), then test on a mid-range phone over 4G with the consent banner and tag manager active, because the real paid visitor sees those.
- **Exceptions and failure modes:** Low-traffic landing pages often lack field data (inference: public field datasets need enough visits), so origin-level or lab data are the fallback; ad parameters and A/B tools can make paid traffic slower than organic.
- **Signals in data:** Lab score "good" but field "poor"; desktop fine, mobile poor.
- **Sources:** [Web Vitals – web.dev](https://web.dev/articles/vitals) (checked 2026-10-13)

### MKT-WEB-008 · Mobile is the default visitor; check inputs and keyboards on a real phone
- **Claim:** In Unbounce's 2024 benchmark data (41k landing pages, 464M visitors) 83% of visits were mobile while desktop converted about 8% better on average. Baymard found that 54% of mobile sites failed to invoke optimised touch keyboards for phone, ZIP or card fields (older data).
- **Evidence type:** study (vendor datasets)
- **Confidence:** medium
- **How it works:** Mobile users face small targets, the wrong keyboard, autocorrect/auto-capitalisation on email fields, and sticky elements covering CTAs; each adds friction.
- **When it matters / how experts use it:** Test the form on a phone: correct `type`/`inputmode` for phone/email/postcode, tap-to-call link on the number, CTA reachable without zooming, no interstitials hiding content. For urgent services, a visible call button often matters more than form polish.
- **Exceptions and failure modes:** Financial services and SaaS did not follow the mobile/desktop pattern in Unbounce's data; device mix depends on campaign settings.
- **Signals in data:** Mobile conversion rate far below desktop for the same page and intent; dead clicks on phone numbers that are not links.
- **Sources:** [Conversion Benchmark Report – Unbounce](https://unbounce.com/conversion-benchmark-report/) (checked 2026-10-13); [Mobile touch keyboards – Baymard Institute](https://baymard.com/blog/mobile-touch-keyboards) (checked 2026-10-13)

### MKT-WEB-009 · Form length: fewer fields usually help, but the effect depends on field type and lead quality
- **Claim:** NN/g recommends removing every field that can be derived, collected later, or dropped. HubSpot's analysis of 40,000+ customer landing pages found conversion fell only slightly as fields increased, with multiple text areas and drop-downs having the strongest negative association. Baymard's checkout research found the average checkout has 11.3 fields while most need only 8.
- **Evidence type:** study; practitioner
- **Confidence:** medium (direction); low (any universal "ideal number")
- **How it works:** Each field adds effort and perceived risk (phone, address), but some fields pre-qualify and set expectations. Removing qualifying fields can raise lead volume while lowering lead quality and sales efficiency.
- **When it matters / how experts use it:** Classify every field as needed now / later / never. Keep fields that the sales team actually uses to route or qualify; measure qualified leads or sales per click, not form submissions, when testing.
- **Exceptions and failure modes:** HubSpot's data is observational (forms differ in many ways); Baymard's figures are e-commerce checkout, not lead forms; high-value B2B or finance leads may tolerate long forms.
- **Signals in data:** Field-level drop-off (form analytics) concentrated on one field (often phone or free-text); rising junk leads after shortening.
- **Sources:** [Website Forms Usability: Top 10 Recommendations – NN/g, 2016](https://www.nngroup.com/articles/web-form-design/) (checked 2026-10-13); [Which types of form fields lower landing page conversions – HubSpot](https://blog.hubspot.com/blog/tabid/6307/bid/6746/Which-Types-of-Form-Fields-Lower-Landing-Page-Conversions.aspx) (checked 2026-10-13); [Checkout flow average form fields – Baymard Institute, 2024-06-26](https://baymard.com/blog/checkout-flow-average-form-fields) (checked 2026-10-13)

### MKT-WEB-010 · Multi-step forms: plausible mechanism, weak public evidence
- **Claim:** Multi-step lead forms (easy, low-threat questions first; contact details last; progress indicator) are often reported to raise conversions, but the best-known evidence (Venture Harbour: 0.96% → 8.1%, 11% → 46%) comes from a company that sells a multi-step form builder, without sample sizes, controls or significance tests.
- **Evidence type:** practitioner; study (vendor, uncontrolled)
- **Confidence:** low-medium
- **How it works:** Claimed mechanisms: lower perceived effort at the start, commitment/endowed-progress effects, and conditional logic that makes questions relevant.
- **When it matters / how experts use it:** Worth an A/B test when the form has many qualifying questions (quotes, insurance, finance) or high field-level abandonment. Measure qualified leads, not step-1 starts.
- **Exceptions and failure modes:** Extra steps add load time and can hide the total effort, causing late abandonment; partial-entry capture of contact details without consent can breach privacy law.
- **Signals in data:** Step-level drop-off in GA4 funnel (MKT-WEB-017); many starts, few completions.
- **Sources:** [Multi-step lead forms – Venture Harbour (2016, updated 2026-04-04)](https://ventureharbour.com/multi-step-lead-forms-get-300-conversions/) (checked 2026-10-13)

### MKT-WEB-011 · Form mechanics that reliably reduce errors
- **Claim:** NN/g's form guidance: labels close to (above) fields, avoid placeholder text as labels, single-column layout, mark optional fields explicitly (and minimise them), explain input requirements before submission, and make errors highly visible and specific while preserving the user's input.
- **Evidence type:** study (usability research synthesis)
- **Confidence:** high (as usability guidance)
- **How it works:** These reduce scanning confusion, memory load (placeholder disappears when typing) and failed submissions.
- **When it matters / how experts use it:** Use as a defect checklist during review; fix before A/B testing larger changes, since they rarely hurt.
- **Exceptions and failure modes:** Short related fields (city/state/ZIP) can share a row; very short forms may not benefit measurably.
- **Signals in data:** Repeated submit clicks (rage clicks) on the submit button; error events firing in analytics.
- **Sources:** [Website Forms Usability: Top 10 Recommendations – NN/g, 2016](https://www.nngroup.com/articles/web-form-design/) (checked 2026-10-13)

### MKT-WEB-012 · Plain, short copy correlates with higher landing page conversion (except finance)
- **Claim:** Unbounce's 2024 dataset found negative correlations between conversion rate and difficult words (-24.3%), reading time (-19.4%) and word count (-18.6%); pages at a 5th-7th grade reading level converted at 11.1% vs 5.3% for professional-level writing. Financial services was an exception.
- **Evidence type:** study (vendor, observational)
- **Confidence:** medium-low (correlation, unknown controls)
- **How it works:** Plain language lowers cognitive load for scanning mobile visitors; the finance exception suggests that complexity can signal credibility where stakes are high.
- **When it matters / how experts use it:** Rewrite jargon-heavy hero sections and CTAs; keep regulated disclosures intact.
- **Exceptions and failure modes:** Simple pages may also be simpler offers (confounding); median landing page conversion of 6.6% across industries is a context figure, not a target.
- **Signals in data:** High scroll and time on page with low conversion can mean people are hunting for an answer in long copy.
- **Sources:** [Conversion Benchmark Report – Unbounce](https://unbounce.com/conversion-benchmark-report/) (checked 2026-10-13)

### MKT-WEB-013 · Trust signals: design quality, upfront disclosure, completeness, external proof
- **Claim:** NN/g identifies four trust communicators: design quality, upfront disclosure (contact details, base costs, fees, policies), comprehensive and current content, and connection to the rest of the web. In their studies users trusted external reviews more than on-site testimonials, which they viewed sceptically.
- **Evidence type:** study (qualitative usability research)
- **Confidence:** medium-high
- **How it works:** Visitors from ads have no prior relationship; small defects (a typo) and missing basics (no address, no rates) trigger doubt.
- **When it matters / how experts use it:** Check for: real business name, address and phone; licence/accreditation numbers where relevant (and required in finance, MKT-NICHE-020); reviews linked to third-party profiles; photos of real staff/work; recent dates. Prefer verifiable proof over badges.
- **Exceptions and failure modes:** Fake or unverifiable badges damage trust and can breach misrepresentation policies; too many logos clutter the first screen.
- **Signals in data:** Visitors clicking "about", "reviews" or external review links before converting; quick backs.
- **Sources:** [Trustworthiness in web design: 4 credibility factors – NN/g, 2016](https://www.nngroup.com/articles/trustworthy-design/) (checked 2026-10-13)

### MKT-WEB-014 · Pricing transparency: disclosure helps trust; hidden costs carry policy risk
- **Claim:** In NN/g research users ruled out a service provider that did not list rates. Google's Misrepresentation policy prohibits failing to "clearly and conspicuously disclose the payment model or full expense" and pricing that creates a misleading impression; the Financial products policy requires fees and a physical address to be visible.
- **Evidence type:** documented (policy); study (qualitative)
- **Confidence:** high (policy); medium (conversion effect)
- **How it works:** Price is a qualifying filter: showing a range or "from" price deters poor-fit leads and reassures good-fit ones.
- **When it matters / how experts use it:** If exact prices vary, show ranges, typical jobs, or a pricing explanation; ensure any price in ads is on the page. Measure lead quality, since disclosure may reduce lead volume while raising close rate.
- **Exceptions and failure modes:** Businesses with highly variable quotes or competitive concerns may resist; regulated insurance ads may restrict cost language (MKT-NICHE-021).
- **Signals in data:** Many leads asking "how much?" and not proceeding; sales reporting price shock.
- **Sources:** [Trustworthiness in web design – NN/g](https://www.nngroup.com/articles/trustworthy-design/) (checked 2026-10-13); [Misrepresentation – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6020955) (checked 2026-10-13); [Financial products and services – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/2464998) (checked 2026-10-13)

### MKT-WEB-015 · Navigation and distractions on landing pages: reduce exits, keep trust routes
- **Claim:** Practitioners commonly remove global navigation, unrelated links and competing CTAs from paid landing pages to focus visitors on one action. This is a heuristic: some visitors need trust routes (about, reviews, service area, pricing) before converting.
- **Evidence type:** practitioner
- **Confidence:** medium-low
- **How it works:** Each extra link is a potential exit; but removing all context can reduce trust (MKT-WEB-013). Google's landing page guidance favours pages that are useful and "well organized".
- **When it matters / how experts use it:** Keep one primary CTA (and call for urgent services); put trust content on the page (reviews, FAQs, pricing) so visitors need not leave. Test a navigation-light version against the existing page rather than assuming.
- **Exceptions and failure modes:** Complex B2B or e-commerce journeys may need navigation; home-page traffic from brand queries behaves differently.
- **Signals in data:** GA4 path or "next action" showing many visitors leaving to blog/careers pages; Clarity heatmaps with clicks on nav items.
- **Sources:** [Landing page experience: Definition – Google Ads Help](https://support.google.com/google-ads/answer/1659694) (checked 2026-10-13); practitioner heuristic otherwise.

### MKT-WEB-016 · Technical destination checks that block ads or lose data
- **Claim:** Google's Destination requirements disallow destinations that are not working, mismatched with the display domain, not crawlable by AdsBot, not accessible in the targeted location, or with poor destination experience; phone numbers in assets must be verified. For measurement, auto-tagging must be on and redirects/click trackers must preserve the GCLID; tags should not fire from iFrames.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Geo-blocking, bot protection that blocks AdsBot, HTTP errors and redirect chains stripping parameters break eligibility or attribution.
- **When it matters / how experts use it:** Before launch, click the final URL with a test parameter from a target-location device and confirm the parameter survives to the conversion page; check that firewall/CDN rules allow AdsBot.
- **Exceptions and failure modes:** Consent banners that block all tags until interaction (basic consent mode) reduce observed data but are not policy violations.
- **Signals in data:** Disapprovals "Destination not working/not crawlable"; GA4 sessions from paid traffic labelled as direct/organic (lost GCLID).
- **Sources:** [Destination requirements – Google Advertising Policies Help](https://support.google.com/adspolicy/answer/6368661) (checked 2026-10-13); [How Google Ads tracks website conversions – Google Ads Help](https://support.google.com/google-ads/answer/7521212) (checked 2026-10-13)

### MKT-WEB-017 · GA4 funnel exploration for lead journeys
- **Claim:** GA4 funnel explorations support up to 10 steps defined by events or dimensions (not metrics), open or closed funnels, "directly followed" vs "indirectly followed" steps, elapsed time, breakdowns, next action and trended views, with up to 4 segments.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Define steps such as landing page view → form start → form step 2 → submit → thank-you; segment by device, campaign or landing page to locate drop-off.
- **When it matters / how experts use it:** Requires instrumenting form_start/step events (GA4's automatic form interaction events are not reliable for multi-step or JS forms; inference from common implementations). Use closed funnels for paid landing pages to isolate entrants.
- **Exceptions and failure modes:** Breakdowns attribute users to the first breakdown value only; "(no next action)" is not always drop-off; consent and thresholds reduce counts; small samples swing wildly.
- **Signals in data:** One step losing most users on mobile only (layout bug); long elapsed time at a step (confusing field).
- **Sources:** [Funnel exploration – Google Analytics Help](https://support.google.com/analytics/answer/9327974) (checked 2026-10-13)

### MKT-WEB-018 · Engagement rate as a landing page smoke alarm, not a goal
- **Claim:** GA4 counts an engaged session if it lasts longer than 10 seconds (default), has a key event, or has 2+ page/screen views; bounce rate is the share of sessions not engaged. Very low engagement from paid traffic flags mismatch, slow load, bots or accidental clicks.
- **Evidence type:** documented
- **Confidence:** high (definition); medium (diagnostic use)
- **How it works:** Compare engagement rate by campaign, device and landing page; paid search traffic with intent should engage more than display.
- **When it matters / how experts use it:** Triage which pages or placements to inspect in recordings; not a success metric for lead-gen.
- **Exceptions and failure modes:** Single-page sites with a click-to-call can look "unengaged" when the user called within 10 seconds; consent denial removes sessions.
- **Signals in data:** Engagement rate far below the site average for one campaign; display placements with near-zero engagement.
- **Sources:** [About engagement rate and bounce rate – Google Analytics Help](https://support.google.com/analytics/answer/12195621) (checked 2026-10-13)

### MKT-WEB-019 · Clarity behavioural flags: rage clicks, dead clicks, excessive scrolling, quick backs
- **Claim:** Microsoft Clarity flags rage clicks (rapid repeated clicks in one area), dead clicks (clicks with no visible response), excessive scrolling (more than the expected average) and quick backs (leaving and returning quickly). Microsoft frames these as indicators of possible frustration, broken elements or poor relevance, not confirmed causes.
- **Evidence type:** documented
- **Confidence:** high (definitions); medium (interpretation)
- **How it works:** Filter recordings by these flags and by paid-traffic UTMs to watch real sessions; heatmaps show where people click that is not clickable.
- **When it matters / how experts use it:** Fast way to find broken buttons, non-link phone numbers, images people expect to be clickable, and confusing form validation. Watch 10-20 sessions per issue before concluding.
- **Exceptions and failure modes:** Thresholds are not published; "excessive scrolling" can be normal on long pages; recordings are a biased sample when consent is required.
- **Signals in data:** Dead clicks on a price table or phone number; rage clicks on the submit button (validation failure).
- **Sources:** [Semantic metrics (rage clicks, dead clicks…) – Microsoft Clarity docs](https://learn.microsoft.com/en-us/clarity/insights/semantic-metrics) (checked 2026-10-13)

### MKT-WEB-020 · Clarity consent enforcement for EEA, UK and Switzerland (changed 2025-10)
- **Claim:** From 2025-10-31 Clarity enforces consent signals for visits from the EEA, UK and Switzerland when the project requires consent **(changed 2025-10)**. Without consent it runs in no-consent mode: no cookies, a unique ID per page view, so sessions are not linked across pages.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Sites pass consent via `clarity('consentv2', {ad_Storage, analytics_Storage})`.
- **When it matters / how experts use it:** European clients' recordings and funnels will under-represent visitors who decline cookies and break multi-page journeys; interpret heatmaps as a consenting-user sample.
- **Exceptions and failure modes:** Misconfigured consent integration can silently drop most sessions.
- **Signals in data:** Sudden fall in Clarity sessions in Europe around 2025-11; single-page sessions dominating.
- **Sources:** [Clarity Consent API v2 – Microsoft Clarity docs](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-consent-api-v2) (checked 2026-10-13)

### MKT-WEB-021 · Consent mode changes what Google Ads and GA4 observe
- **Claim:** Consent mode passes users' consent state to Google tags. In basic mode tags are blocked until consent (nothing sent if declined; a general model fills gaps); in advanced mode tags load with consent denied and send cookieless pings, enabling an advertiser-specific conversion model. Modelling needs a minimum data threshold and at least 7 full days before uplift is reported.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Observed conversions fall when users decline; modelled conversions may be added in Ads reporting where thresholds are met.
- **When it matters / how experts use it:** When comparing Ads conversions to CRM leads, account for consent losses and modelling; low-traffic European accounts may not qualify for modelling and will look worse than they are.
- **Exceptions and failure modes:** Banners that load late or block the Google tag entirely; mismatched defaults by region.
- **Signals in data:** Ads conversions well below CRM leads in consent regions; GA4 sessions far below Ads clicks.
- **Sources:** [About consent mode – Google Ads Help](https://support.google.com/google-ads/answer/10000067) (checked 2026-10-13)

### MKT-WEB-022 · Tag firing checks before judging any page
- **Claim:** Google recommends verifying tags with Tag Assistant, avoiding conflicting gtag.js and Google Tag Manager installations, keeping auto-tagging on, preserving GCLID through redirects, using the domain linker across domains, and not firing tags in iFrames; status changes can take up to 48 hours.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Double installations cause duplicate events; iFrame forms (third-party schedulers, embedded forms) often fire on another domain; lost GCLIDs break attribution.
- **When it matters / how experts use it:** Submit a test lead from a paid click (with gclid), confirm one conversion in Tag Assistant, the event in GA4 DebugView, and the record in the CRM. Repeat on mobile and with consent declined.
- **Exceptions and failure modes:** Testing from an internal IP excluded in GA4; ad blockers on the tester's browser giving false negatives.
- **Signals in data:** Conversion action "Unverified/Inactive"; conversions ≈ 2× leads; conversions only on desktop.
- **Sources:** [How Google Ads tracks website conversions – Google Ads Help](https://support.google.com/google-ads/answer/7521212) (checked 2026-10-13)

### MKT-WEB-023 · Thank-you page duplication and conversion counting for leads
- **Claim:** Reloading or returning to a confirmation page can fire the tag again; Google Ads de-duplicates conversions sharing the same transaction ID within a conversion action (static IDs cause under-counting). For lead generation Google suggests counting "One" conversion per ad click; for sales, "Every".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Without a unique ID, bookmarked thank-you pages, back-button visits and multiple tabs inflate leads; "One" caps per click but does not catch duplicates across different clicks.
- **When it matters / how experts use it:** Pass a unique lead ID as transaction ID; fire on a confirmed server response, not page view where possible; make the thank-you page unreachable without submission (noindex, no menu links).
- **Exceptions and failure modes:** Transaction IDs do not de-duplicate view-through conversions; "One" may undercount genuine repeat leads for multiple services.
- **Signals in data:** Thank-you page views > form submissions; organic traffic to the thank-you page; conversion spikes without CRM leads.
- **Sources:** [Use a transaction ID to minimize duplicate conversions – Google Ads Help](https://support.google.com/google-ads/answer/6386790) (checked 2026-10-13); [About conversion counting options – Google Ads Help](https://support.google.com/google-ads/answer/3438531) (checked 2026-10-13)

### MKT-WEB-024 · Calls are part of the journey: track them and check they are answered
- **Claim:** Website call tracking with Google forwarding numbers replaces the business number dynamically and counts calls longer than a minimum length you set as conversions, attributing them to keywords and ads; limitations include only one number per page with the default tag, verification problems with third-party dynamic number insertion, and country availability.
- **Evidence type:** documented; practitioner (call handling)
- **Confidence:** high (tracking); medium (handling advice)
- **How it works:** For urgent services many visitors call instead of submitting forms; untracked calls make pages look like they fail, and unanswered calls waste paid demand.
- **When it matters / how experts use it:** Set call-length thresholds that match a real enquiry; review call recordings or outcomes where legal; test-call during and outside business hours; align ad schedules with staffing; consider call-only periods.
- **Exceptions and failure modes:** Short calls can still be valuable (booking confirmations); long calls can be spam or existing customers.
- **Signals in data:** Many short calls, missed-call logs, calls outside opening hours.
- **Sources:** [Set up tracking calls to a phone number on a website – Google Ads Help](https://support.google.com/google-ads/answer/6095883) (checked 2026-10-13)

### MKT-WEB-025 · Speed to lead: response time matters, but the famous multipliers are old
- **Claim:** The widely cited findings (contacting web leads within 5 minutes vs 30 minutes: ~100x odds of contact, ~21x odds of qualifying) come from the Oldroyd/InsideSales Lead Response Management study (publicised 2011; study period and sample not verified) and the 2011 HBR article "The Short Life of Online Sales Leads" (co-authored by InsideSales' founder). More recent data are mostly vendor mystery-shopping studies (e.g. a 2026 dealership study of 53 dealers: average first response >9 hours, ~13% within 5 minutes, nearly one-third never responded in five days).
- **Evidence type:** study (dated, vendor-involved, observational)
- **Confidence:** medium (direction: faster is better); low (exact multipliers today)
- **How it works:** Interest decays quickly; prospects often submit to several competitors and buy from the first credible responder.
- **When it matters / how experts use it:** Mystery-shop the client (submit a test lead, call after hours) before blaming ads; set response-time targets and auto-acknowledgement; measure contact rate and time-to-first-contact in the CRM.
- **Exceptions and failure modes:** Low-urgency, high-consideration purchases may not need minutes; aggressive instant calling can breach consent rules (MKT-NICHE-022).
- **Signals in data:** Low lead-to-contact rate or median time-to-first-contact measured in hours in the CRM; conversion quality complaints concentrated on weekend leads.
- **Sources:** [The Short Life of Online Sales Leads – HBR, 2011-03](https://hbr.org/2011/03/the-short-life-of-online-sales-leads) (checked 2026-10-13; only the introduction was accessible); [Increase your sales effectiveness by 21x in 25 minutes – Electronics Cooling, 2011](https://www.electronics-cooling.com/2011/06/increase-your-sales-effectiveness-by-21x-in-25-minutes/) (checked 2026-10-13); [The five-minute lead response stat – LeadSigma](https://leadsigma.com/resources/blog/five-minute-lead-response-stat) (checked 2026-10-13); [State of speed to lead – Callingly](https://callingly.com/blog/state-of-speed-to-lead) (checked 2026-10-13)
- **Open questions:** No independent, recent, controlled study of response time vs close rate in home services or insurance was found.

### MKT-WEB-026 · Close the loop: send lead outcomes back to Google Ads (changed 2026-06)
- **Claim:** Enhanced conversions for leads captures hashed user-provided data (email recommended; phone in E.164) from forms via the Google tag, then matches later uploaded offline outcomes (qualified lead, sale) to ad clicks, improving measurement and bidding. From 2026-06-15 offline conversion imports and enhanced-conversions-for-leads uploads move to the Data Manager API and are blocked in the Google Ads API **(changed 2026-06)**.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Form-fill conversions measure volume; outcome uploads let bidding learn which clicks produced revenue, which matters when lead quality varies by keyword or placement.
- **When it matters / how experts use it:** Once a test shows viability, set up qualified-lead and sale conversions and optimise toward them; requires auto-tagging, form interaction collection, accepted customer data terms and a CRM that stores GCLID/lead ID.
- **Exceptions and failure modes:** Low outcome volume and long sales cycles limit learning; integrations built on the old API path need migration.
- **Signals in data:** Many form conversions but few CRM-qualified leads; bidding favouring cheap, low-quality placements.
- **Sources:** [About enhanced conversions for leads – Google Ads Help](https://support.google.com/google-ads/answer/11021502) (checked 2026-10-13)

### MKT-WEB-027 · Prioritise fixes by traffic × drop-off × confidence × effort
- **Claim:** Rank fixes by expected lost conversions = visitors reaching the step × drop-off attributable to the problem × confidence that the fix helps, divided by effort. Measurement and lead-handling defects come first because they affect every decision; then defects on high-traffic mobile templates; then experiments.
- **Evidence type:** inference; practitioner (PIE/ICE-style scoring)
- **Confidence:** medium
- **How it works:** A 10% improvement on a step that 5,000 paid visitors reach beats a 50% improvement on a page with 100 visitors; certain defects (broken button) have high confidence, opinions (colour, imagery) low.
- **When it matters / how experts use it:** Use GA4 funnels and Ads landing page reports to size each step; confirm causes with recordings (MKT-WEB-019) before redesigning; small sites rarely have enough traffic to A/B test, so ship defect fixes and monitor.
- **Exceptions and failure modes:** Scores are subjective; downstream quality (sales) may move opposite to form conversion rate.
- **Signals in data:** Steps with the largest absolute user loss; device- or browser-specific drops.
- **Sources:** [Funnel exploration – Google Analytics Help](https://support.google.com/analytics/answer/9327974) (checked 2026-10-13); prioritisation formula is our inference.

## Common mistakes and misleading metrics
- Judging a landing page before verifying the tag, thank-you page de-duplication and CRM match; conversions inflated by reloads look like a "great page".
- Treating Quality Score's landing page component as a KPI, or promising that Core Web Vitals work will raise Quality Score (not documented).
- Quoting old or unavailable speed statistics (e.g. "53% abandon after 3 s") and vendor case studies as forecasts.
- Optimising form submission rate after cutting qualifying fields while lead quality falls.
- Reading bounce/engagement rate as success for call-driven pages (a quick call looks like a bounce).
- Taking the Unbounce 6.6% median or any "industry average" conversion rate as a target.
- Assuming Clarity recordings or GA4 funnels represent all visitors in consent-required regions.
- Blaming ads for poor results when leads are not called back for hours or calls go unanswered.
- Testing on a fast office desktop instead of a mid-range phone on cellular with the consent banner active.

## Unresolved questions
- Whether Google Ads' landing page assessment uses any speed or Core Web Vitals signal directly (Google's "Understanding landing page experience" article could not be opened).
- Independent, controlled evidence on multi-step forms vs single-step for lead quality (not only volume).
- Current, independent speed-to-lead evidence outside automotive and B2B, especially for home services and insurance.
- How much of observed conversion loss in EEA/UK accounts is recovered by consent-mode modelling for small advertisers.
- Practical field-count thresholds for high-value lead forms (finance, insurance) where qualification is required.
