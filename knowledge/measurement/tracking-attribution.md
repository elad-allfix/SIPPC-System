---
area: measurement
topic: conversion tracking and attribution
checked: 2026-10-13
owner: research
---
# Conversion tracking and attribution in Google Ads

This file covers how Google Ads decides what counts as a conversion, how much credit it assigns, when it reports it, and how the setup changed in 2025-2026: enhanced conversions became one setting, offline imports moved to the Data Manager API, and consent mode became the only control over Ads cookies collected through GA4. The most important idea: **Smart Bidding optimizes toward exactly what the "Conversions" column contains.** That is the primary actions in the goals the campaign uses, credited by the action's attribution model, dated by click, and including modelled conversions. Any mistake in that column becomes a bidding mistake. So the strategist audits the conversion setup before it reads any CPA or ROAS.

### MEA-CONV-001 · Bidding uses only primary actions in goals the campaign actually uses
- **Claim:** A conversion action affects bidding only if it is set to Primary *and* belongs to a goal that the campaign uses. One exception: every action inside a custom goal is biddable, primary or secondary. "Conversions" and "Conv. value" contain only these actions. "All conv." also contains secondary actions and primary actions that the campaign does not use.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Actions are grouped into standard goals by category (Purchase, Submit lead form, Contact, etc.). A campaign optimizes toward the account-default goals or toward goals selected for that campaign. Secondary actions are "observe only". According to Google, primary actions that a campaign does not use "may still enhance predictions", which is an opaque statement.
- **When it matters / how experts use it:** This is the first audit step whenever performance looks odd. Check which goals each campaign uses and which actions in them are primary. Compare the "Conversions" and "All conv." columns: a large gap means the account tracks a lot it does not bid on, which is fine. A small "Conversions" count can mean the action the business cares about is secondary by mistake.
- **Exceptions and failure modes:** A primary action inside a goal that no campaign uses changes nothing. A custom goal makes secondary actions biddable, which surprises people. Changing conversion goals or primary actions changes what the bidder optimises and triggers recalibration; a CPA/ROAS target change does not trigger Learning status, per Google (PLT-BID-011).
- **Signals in data:** Campaign status "Misconfigured" or "No recent conversions" while All conv. is healthy. Conversions appear in All conv. but not in Conversions. Bid strategy reports name a different conversion set than expected.
- **Sources:** [About conversion goals](https://support.google.com/google-ads/answer/10995103) (checked 2026-10-13); [About primary and secondary conversion actions](https://support.google.com/google-ads/answer/11461796) (checked 2026-10-13)

### MEA-CONV-002 · Account-default goals, campaign-specific goals and custom goals
- **Claim:** Account-default goals apply to every new campaign. Google recommends making only one stage of a funnel the default, for example Purchase and not also Add to cart. A campaign can override the default with campaign-specific goals. Custom goals mix actions across categories, but a campaign can bid toward only one custom goal, and Google calls them advanced and "generally not recommended".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Goal selection is the switch that decides which conversion stream a campaign's bid model learns from. If several funnel stages are default goals, the campaign optimizes toward their sum, and a cheap upper-funnel action can dominate.
- **When it matters / how experts use it:** Use campaign-specific goals when campaigns have different jobs: a brand campaign on purchases, a lead campaign on qualified leads, or a prospecting campaign on a stage further up the funnel when volume is too thin. Practitioners often keep micro-conversions (scroll, page view, add to cart) secondary so they can watch them without bidding on them.
- **Exceptions and failure modes:** A custom goal must include every action you want bidding to target, because a campaign takes only one. When a new action is added to an account-default goal, every campaign that uses that goal starts optimizing to it immediately.
- **Signals in data:** CPA falls while revenue does not move after someone adds an "Add to cart" or "Begin checkout" action as primary. Different campaigns report very different conversion mixes.
- **Sources:** [About conversion goals](https://support.google.com/google-ads/answer/10995103) (checked 2026-10-13)

### MEA-CONV-003 · Count setting: "One" vs "Every", and why it is not deduplication
- **Claim:** "Every" counts each conversion after an ad interaction. "One" counts at most one conversion per action per ad click. Google recommends Every for purchases and One for leads. The defaults are Every for website, in-app actions, Analytics transactions and import actions, and One for calls from ads, calls to website numbers, Analytics goals and app installs. A change applies only to future conversions.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Counting is per click and per action. One click that produces 2 sales (Every) and 2 leads (One) counts as 3. "Repeat rate" equals the Every count divided by the One count. If attribution is set to "Paid and organic channels" in GA4, the count setting is managed in GA4.
- **When it matters / how experts use it:** A lead action left on Every rewards bidding for people who submit the same form several times, including spam bots. Use One for leads. For purchases, use Every *plus* a transaction ID (see MEA-CONV-020); One would undercount real repeat purchases.
- **Exceptions and failure modes:** iOS clicks carrying GBRAID/WBRAID cannot be matched to a single click. Uploads with these IDs to a conversion action set to One are rejected, so practitioners switch such actions to Every and accept some double counting of leads (practitioner source, see MEA-CONV-016). Count does not deduplicate the same order fired twice from different clicks.
- **Signals in data:** Conversions for a lead action exceed CRM lead count for the same period. Repeat rate well above 1 on a lead action.
- **Sources:** [About conversion counting options](https://support.google.com/google-ads/answer/3438531) (checked 2026-10-13); [Able CDP: One-per-click braid error](https://www.ablecdp.com/q/google-ads-one-per-click-braid-error) (checked 2026-10-13)

### MEA-CONV-004 · Conversion windows: click-through, engaged-view and view-through
- **Claim:** The click-through window defaults to 30 days and can be set from 1 to 90 days, depending on the source. The engaged-view window defaults to 3 days, and the view-through window to 1 day. Changes are not retroactive. Conversions after the window are never recorded, and Smart Bidding optimizes to whatever window you choose.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The window caps how long after the interaction a conversion can be credited. Google Ads cookies expire 90 days after a click, while GA4 cookies can last up to 2 years. This is one reason GA4 shows conversions that Ads does not.
- **When it matters / how experts use it:** Match the window to the real purchase cycle, using the Path / time lag reports and CRM time-to-close. A window much shorter than the cycle hides real conversions from bidding. A long window (90 days) increases conversion lag, so recent days look worse for longer (MEA-CONV-008). Google recommends at least 7 days.
- **Exceptions and failure modes:** Imported GA4 key events may have windows managed in GA4 (the "Paid and organic channels" setting). Time lag reports are capped at the window length, so they cannot show conversions that the window cuts off.
- **Signals in data:** CRM shows many deals closing more than 30 days after the first click, but Ads conversions stay flat. A step change in volume on the date someone changed the window.
- **Sources:** [About conversion windows](https://support.google.com/google-ads/answer/3123169) (checked 2026-10-13); [Create conversions from Google Analytics events](https://support.google.com/google-ads/answer/2375435?hl=en) (checked 2026-10-13)

### MEA-CONV-005 · Engaged-view conversions are inside the "Conversions" column
- **Claim:** An engaged view means 10 seconds watched of a skippable in-stream ad (or the whole ad if it is shorter), 5 seconds of an in-feed or Shorts ad (or a CTA click), or a completed rewarded ad or 5 seconds after the skip point on a GDN video ad. Engaged-view conversions count in "Conversions" and "All conv.", and engaged views count in "Interactions". Video, App, Display, Demand Gen and Performance Max are eligible.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** No click is needed. If the viewer converts inside the engaged-view window (3 days by default for web), the conversion is credited. For offline conversions and enhanced conversions for leads, uploads must happen within 14 days of the conversion for engaged-view credit, even when the window is longer.
- **When it matters / how experts use it:** In Performance Max and Demand Gen, part of the reported conversions may come from people who watched and did not click. Segment by "Ad event type" to split click-through from engaged-view. Treat engaged-view credit as weaker evidence of causality than click credit, and judge it through lift tests (see MEA-ECON on incrementality).
- **Exceptions and failure modes:** Default windows differ for apps (1-2 days). Older advice that defines an engaged view as 30 seconds is outdated: the 10-second definition for skippable in-stream ads dates from about 2021 (PPC Land, Feb 2021).
- **Signals in data:** Performance Max conversions far exceed the clicks you would expect at the observed conversion rate. The Ad event type segment shows a large engaged-view share.
- **Sources:** [About Engaged-view conversions](https://support.google.com/google-ads/answer/10048752?hl=en) (checked 2026-10-13); [PPC Land: engaged-view conversions standard for video campaigns](https://ppc.land/google-ads-introduces-engaged-view-conversions-as-standard-attribution-for-all-video-campaigns) (checked 2026-10-13)

### MEA-CONV-006 · Attribution models available in 2026: data-driven, last click, external
- **Claim:** Data-driven attribution (DDA) is the default for most conversion actions. Last click and external attribution remain. First click, linear, time decay and position-based were retired: selection was removed in June 2023, and actions still using them were moved to DDA in September 2023. All conversion actions are eligible for DDA regardless of volume. Google *recommends* at least 200 conversions and 2,000 ad interactions in 30 days.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** DDA spreads fractional credit across Google ad interactions (Search including Shopping, YouTube, Display, Demand Gen) using the account's own path data. Supported types are website, store visit and Google Analytics conversions. With little data Google says DDA still runs, but "identifies patterns" less precisely. In some cases it gives the same result as last click.
- **When it matters / how experts use it:** The 200/2,000 figures are recommendations, not eligibility gates. Older (pre-2021) advice about DDA minimums of 3,000 interactions and 300 conversions is obsolete. DDA only reallocates credit *among Google ad touchpoints*. It is not cross-channel and not a measure of incrementality.
- **Exceptions and failure modes:** In low-volume accounts, DDA output is close to an opaque heuristic. Do not read keyword-level fractional credit as precise. Offline uploads with external attribution data must use an action set to the external model.
- **Signals in data:** Fractional conversion counts (decimals). Upper-funnel or generic keywords get more credit than under last click.
- **Sources:** [About data-driven attribution](https://support.google.com/google-ads/answer/6394265) (checked 2026-10-13); [First click, linear, time decay and position-based models are going away](https://support.google.com/google-ads/answer/13427716) (checked 2026-10-13); [About attribution models](https://support.google.com/google-ads/answer/6259715) (checked 2026-10-13)

### MEA-CONV-007 · What an attribution model change does to reported numbers and to bidding
- **Claim:** A model change applies to the chosen action *going forward* in "Conversions" and "All conv.". The "(current model)" columns show history as if the new model had always applied. Credit moves between campaigns, keywords and networks, so tCPA and tROAS targets must be rescaled per campaign, or bidding will over- or under-spend.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google's example: brand and generic CPAs under last click were $5 and $20, and under DDA they became about $6.67 and $10. With unchanged targets, the account underbids brand and overbids generic. Google's method: compare "Cost / conv." with "Cost / conv. (current model)" per campaign and move each target by the same percentage. Do the same for ROAS. Leave out the most recent ~14 days because of lag.
- **When it matters / how experts use it:** Before and after any model switch, and whenever someone compares periods that span a switch. Period-over-period comparisons across a model change are not like-for-like unless they use current-model columns.
- **Exceptions and failure modes:** Manual bidding is unaffected until a person acts on the new numbers. Current-model columns include only primary actions and include cross-device conversions.
- **Signals in data:** Decimals appear suddenly in conversion counts. Brand CPA rises and generic CPA falls on a specific date. The Change history shows an attribution edit.
- **Sources:** [Best practices for managing attribution model changes](https://support.google.com/google-ads/answer/9203352?hl=en) (checked 2026-10-13); [About attribution models](https://support.google.com/google-ads/answer/6259715) (checked 2026-10-13)

### MEA-CONV-008 · Conversion lag: standard columns are dated by click, so recent days always look worse
- **Claim:** Standard Google Ads conversion columns credit conversions to the **date of the ad click**, so spend and conversions line up. The "(by conv. time)" columns, added October 2019, credit them to the date the conversion happened. As a result, the most recent days under-report conversions until the lag has passed.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** A click on Monday that converts on Friday is added to *Monday's* row on Friday. Imported offline conversions are also reported under the original click date (Google Ads API docs). GA4 reports conversions on the date they occurred.
- **When it matters / how experts use it:** Never judge the last N days, where N is roughly the typical time to convert, by standard CPA or ROAS. Read "Avg. days to conversion" and the time lag report, and exclude that window. Use the by-conv.-time columns to reconcile with sales or CRM for a calendar month. Do not divide them by spend for CPA, because spend stays on click dates.
- **Exceptions and failure modes:** Short-lag e-commerce (same session) shows little effect. B2B lead-to-sale imports can lag weeks, so last month's ROAS keeps rising for weeks after month end.
- **Signals in data:** Every weekly report shows a "drop" in the latest week that fills in later. Month-end ROAS is restated upward a few weeks later.
- **Sources:** [About "by conversion time" columns](https://support.google.com/google-ads/answer/9549009?hl=en) (checked 2026-10-13); [Google Ads API: upload click conversions](https://developers.google.com/google-ads/api/docs/conversions/upload-clicks) (checked 2026-10-13); [Create conversions from Google Analytics events](https://support.google.com/google-ads/answer/2375435?hl=en) (checked 2026-10-13)

### MEA-CONV-009 · Data freshness: delays differ by attribution model and source
- **Claim:** Google Ads tag conversions take about 3 hours to appear under last click and about 15 hours under other models. GA-imported goals and transactions take about 12 hours under last click and about 24 hours otherwise. Google's discrepancy page says conversion reporting can lag 15-48 hours, especially for non-last-click models.
- **Evidence type:** documented
- **Confidence:** medium (the freshness page does not name GA4 explicitly; the figures may come from the UA era)
- **How it works:** DDA has to compute path credit in batch, so its data arrives later than last click. Imports add their own processing time.
- **When it matters / how experts use it:** Intraday and "yesterday" decisions, automated rules and scripts that pause on zero conversions, and alerts for broken tracking. Do not alert on zero conversions for "today" in a DDA account.
- **Exceptions and failure modes:** Offline imports can lag much more, because they depend on how often the advertiser uploads.
- **Signals in data:** Yesterday's numbers grow over the next day. Scripts flag false "no conversion" anomalies.
- **Sources:** [About data freshness](https://support.google.com/google-ads/answer/2544985?hl=en) (checked 2026-10-13); [Fix missing data and discrepancies](https://support.google.com/google-ads/answer/2404039) (checked 2026-10-13)

### MEA-CONV-010 · Enhanced conversions: mechanism, and the 2026 single toggle
- **Claim:** Enhanced conversions send normalized, SHA-256-hashed first-party data (email, phone, name, address) with the conversion. Google matches it to Google accounts that were signed in when the user engaged with the ad, which recovers conversions that cookies missed. **(changed 2026-04)** Google Ads accepts user-provided data from website tags, Data Manager and API connections *at the same time*. **(changed 2026-06)** Enhanced conversions for web and for leads are merged into one on/off setting with no choice of implementation method. Existing users were migrated automatically.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Before hashing, data is normalized: trim, lowercase, E.164 phone format, and for gmail/googlemail addresses, periods removed. Matching happens on Google's side. Turning the feature on requires accepting the Google Ads Data Processing Terms. It can be enabled at account or action level, and a single action can opt out. There is an optional setting that lets Google build "conversion-based customer lists" from this data.
- **When it matters / how experts use it:** It recovers conversions lost to cookie loss, cross-device journeys and Safari restrictions. Practitioners expect a modest uplift, not a step change. Because several sources are now accepted, a tag and a CRM upload can both supply user data, which gives redundancy.
- **Exceptions and failure modes:** User data cannot be sent when `ad_user_data` consent is denied (MEA-CONV-018). Data that is badly formatted or hashed twice silently fails to match. The setting "Customer data use" has to be accepted again on new accounts.
- **Signals in data:** The enhanced conversions diagnostics show match and coverage rates. A conversion uplift appears gradually after activation and does not show in historical data.
- **Sources:** [About enhanced conversions](https://support.google.com/google-ads/answer/9888656?hl=en) (checked 2026-10-13); [Updates to your enhanced conversions settings](https://support.google.com/google-ads/answer/16884284?hl=en) (checked 2026-10-13); [PPC Land: enhanced conversions collapse into a single toggle](https://ppc.land/google-ads-finally-collapses-enhanced-conversions-into-a-single-toggle/) (checked 2026-10-13)

### MEA-CONV-011 · Enhanced conversions for leads are the recommended form of offline conversion import
- **Claim:** Google recommends moving from classic GCLID-only offline conversion import (OCI) to enhanced conversions for leads. These send hashed user data, plus GCLID where available, for offline outcomes such as qualified leads and closed sales. Google states a *median* 10% increase in conversions for advertisers who combine first-party data with GCLIDs, compared with standard offline import.
- **Evidence type:** documented (mechanism); google-statement (the 10% median)
- **Confidence:** high (mechanism); medium (uplift figure is Google's own, with no methodology given)
- **How it works:** At form submission, the tag captures hashed user data and the click ID. Later, the CRM uploads the outcome with the same hashed email or phone, and Google joins the two. GCLID is still recommended, and it is required when no tag collects user data. Google says the feature supports engaged-view and cross-device conversions, which GCLID-only import cannot.
- **When it matters / how experts use it:** Lead generation where the form fill is not the business outcome. Import stages such as qualified lead, opportunity and won deal (with deal value) as separate actions. Bid on the deepest stage that still has enough volume, and keep the others secondary. This is the main defence against bidding on spam leads (see MEA-ECON on form spam).
- **Exceptions and failure modes:** A CRM must store the click ID or user data from the original submission. Uploading too late misses windows: engaged-view credit needs upload within 14 days, and the conversion window caps the rest. Leads captured offline with no web touchpoint cannot match.
- **Signals in data:** Imported "qualified lead" counts are far lower than "form submit", which is expected. Match rate diagnostics in Data Manager / the enhanced conversions for leads diagnostics report.
- **Sources:** [About offline conversion imports](https://support.google.com/google-ads/answer/2998031?hl=en) (checked 2026-10-13); [Your guide to upgrading offline conversion imports](https://support.google.com/google-ads/answer/15479486?hl=en) (checked 2026-10-13); [About Engaged-view conversions](https://support.google.com/google-ads/answer/10048752?hl=en) (checked 2026-10-13)

### MEA-CONV-012 · Data Manager API replaces the Google Ads API for offline conversion import (changed 2026-06)
- **Claim:** Verified. On 15 June 2026 the Google Ads API stopped accepting *new adopters* of offline conversion imports, including enhanced conversions for leads, through `ConversionUploadService.UploadClickConversions`. Access is allowlisted by developer token. Existing adopters may keep using it during migration. Google calls the Data Manager API (launched 9 Dec 2025) "the primary API for importing offline conversions". Requests that are not allowlisted fail with `CUSTOMER_NOT_ALLOWLISTED_FOR_THIS_FEATURE`.
- **Evidence type:** documented
- **Confidence:** high (the change); medium (the exact allowlist window: the developer blog says no imports Dec 2025 to May 2026, while the Help Center says tokens with no requests Jan to June 2026)
- **How it works:** Google announced the change on the Google Ads Developer Blog on 15 May 2026. The Help Center describes uploads as "blocked in the Google Ads API" from 15 June 2026, and existing users get "legacy access". The Data Manager UI and API also serve Customer Match, which moved earlier (Google Ads API Customer Match uploads stopped 1 April 2026, per PPC Land).
- **When it matters / how experts use it:** Any new CRM-to-Ads integration in 2026 must be built on the Data Manager API, Data Manager UI connectors, or a partner. Audit integrations built before June 2026 for legacy-access dependence, because the blog frames continued Google Ads API use as transitional.
- **Exceptions and failure modes:** PPC Land notes that blocked uploads can fail *silently* from the advertiser's point of view if the integration does not handle the error code. The blog post does not say whether call conversion imports and adjustments are covered.
- **Signals in data:** Offline conversion actions stop receiving data after mid-June 2026. Upload diagnostics show allowlist errors. A newly built Zapier or custom script never shows imports.
- **Sources:** [Google Ads Developer Blog: Changes to offline click conversion import support](https://ads-developers.googleblog.com/2026/05/changes-to-offline-click-conversion.html) (checked 2026-10-13); [PPC Land: Google blocks new offline conversion imports via Ads API from June 15](https://ppc.land/google-blocks-new-offline-conversion-imports-via-ads-api-from-june-15/) (checked 2026-10-13); [Updates to your enhanced conversions settings](https://support.google.com/google-ads/answer/16884284?hl=en) (checked 2026-10-13)
- **Open questions:** Whether there is an end date for legacy Google Ads API access. How call conversion imports and conversion adjustments are treated.

### MEA-CONV-013 · Data Manager API behaves differently: whole-request rejection, new auth, no developer token
- **Claim:** The Data Manager API has no `partial_failure`: it rejects the *entire request* if any field fails validation. It uses OAuth with the `datamanager` scope and needs no developer token. Click IDs map to `ad_identifiers.gclid/gbraid/wbraid` and `order_id` maps to `transaction_id`. Consent can be set as a request-level default and overridden per event. Processing is asynchronous, and results are checked through diagnostics by `request_id`.
- **Evidence type:** documented (field mapping guide); study/press (limits from PPC Land)
- **Confidence:** high (mapping); medium (quota numbers)
- **How it works:** Per PPC Land, limits are 100,000 requests/day and 300/minute per Cloud project, and up to 2,000 conversion events per request. Some Ads API fields have no equivalent: `conversion_environment`, `external_attribution_data`, and `mobile_id`/`third_party_user_id` user identifiers.
- **When it matters / how experts use it:** One malformed row (for example a bad timestamp) can drop a whole batch of good conversions. Validate rows before sending and send smaller batches. Monitor diagnostics, not just HTTP success. External attribution workflows need a rethink.
- **Exceptions and failure modes:** Integrations ported mechanically from the Ads API, which relied on partial failure, will lose data in bulk.
- **Signals in data:** Whole days of imports missing rather than a few rows. Diagnostics errors per request_id.
- **Sources:** [Data Manager API: field mappings from Google Ads API](https://developers.google.com/data-manager/api/devguides/events/google-ads/offline/upgrade/field-mappings) (checked 2026-10-13); [PPC Land: Google blocks new offline conversion imports via Ads API](https://ppc.land/google-blocks-new-offline-conversion-imports-via-ads-api-from-june-15/) (checked 2026-10-13)

### MEA-CONV-014 · Offline import data rules that silently drop or misattribute conversions
- **Claim:** For click conversion uploads: the timestamp must include a timezone offset, and conversions report under the original click's date. Order IDs deduplicate conversions and must be reused for later adjustments, and a duplicate order ID in one batch means those rows are not processed. Custom variables cannot be combined with GBRAID/WBRAID or with user-provided data; Google treats such rows as invalid and drops them. Omitting the consent field "may make conversions unattributable".
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** These are validation rules applied on Google's side. An offset in the wrong timezone can move the conversion before the click, which makes it invalid, or shift it out of the window.
- **When it matters / how experts use it:** These rules belong on the QA checklist for any CRM integration. Store the click time and the lead time in UTC with an offset. Keep the CRM deal ID as the order ID so value can be restated later, for example after refunds or a deal that grows.
- **Exceptions and failure modes:** In the Data Manager API, where there is no partial failure, one bad row rejects the batch (MEA-CONV-013).
- **Signals in data:** Upload summary shows "processed" much lower than "sent". Imported conversions appear on unexpected dates.
- **Sources:** [Google Ads API: upload click conversions](https://developers.google.com/google-ads/api/docs/conversions/upload-clicks) (checked 2026-10-13)

### MEA-CONV-015 · GCLID, GBRAID and WBRAID: what each is and where it applies
- **Claim:** Auto-tagging appends GCLID to the landing URL, and the Google tag / conversion linker stores it in a first-party cookie (`_gcl_aw`). After Apple's App Tracking Transparency (ATT, April 2021), GCLID is not sent for iOS 14+ traffic from some Google apps. In its place, WBRAID (web conversions, March 2021) and GBRAID (app conversions, May 2021) carry aggregated, non-click-unique identifiers that work together with conversion modelling.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Braid identifiers are not unique to one click, so Google cannot apply one-per-click logic to them (Able CDP explanation, consistent with the upload error). Per Google, GBRAID is for Search, Shopping, Display and Performance Max only, and offline import with it may need allowlisting. **(changed 2025-10)** Per PPC Land, the Google Ads API allows GCLID and GBRAID in the same upload from 3 October 2025.
- **When it matters / how experts use it:** Lead forms should capture all three parameters into hidden fields, not only gclid. iOS-heavy audiences (consumer, US) lose more click-level matching, so expect more modelled conversions.
- **Exceptions and failure modes:** Custom variables are not supported with braid identifiers. Conversion actions set to "One" reject braid uploads.
- **Signals in data:** CRM records with wbraid/gbraid but no gclid, concentrated on iOS. Lower offline match rates on iOS.
- **Sources:** [Updates to iOS 14 campaign measurement](https://support.google.com/google-ads/answer/10417364?hl=en) (checked 2026-10-13); [About auto-tagging](https://support.google.com/google-ads/answer/3095550?hl=en) (checked 2026-10-13); [PPC Land: Safari is quietly killing your GCLID](https://ppc.land/safari-is-quietly-killing-your-gclid-and-here-is-the-fix/) (checked 2026-10-13)

### MEA-CONV-016 · What breaks click IDs: redirects, parameter-hostile servers, forms, cross-domain, Safari
- **Claim:** GCLID is lost when (a) a redirect drops query parameters before the final landing page, (b) the server rejects arbitrary URL parameters, (c) forms, booking engines or third-party domains do not carry the ID forward, (d) consent denies `ad_storage` with `ads_data_redaction` on, which redacts click IDs, or (e) Safari strips it. Safari stripping is documented in Private Browsing and in links from Mail and Messages, and in all browsing if the user turns on Advanced Tracking and Fingerprinting Protection for "All Browsing". Practitioner tests (Sep 2025, Apr 2026) found GCLID *not* stripped in regular iOS 26 browsing by default. GBRAID/WBRAID were not stripped in these tests.
- **Evidence type:** documented (a, b, d); practitioner (Safari scope)
- **Confidence:** high (a, b, d); medium (Safari: tests reported on social media, no controlled study; the agency blog WITHIN contradicts itself)
- **How it works:** Conversion attribution needs the click ID or a matchable user identity at conversion time. Losing both turns a paid conversion into "unattributed", which modelling recovers only partly.
- **When it matters / how experts use it:** Test by clicking a live ad (or using a `?gclid=test` URL) and following the ID through every redirect, form and domain hop to the CRM record. Mitigations: enhanced conversions, server-side tagging and Google tag gateway (first-party serving). A community "Restore GCLID" GTM template copies the click ID through a custom URL suffix parameter. That works, but Apple may close it, and it must respect consent.
- **Exceptions and failure modes:** App campaigns ignore auto-tagging. UTM-only setups do not give Ads click IDs. Some shorteners and QR-style redirects strip queries.
- **Signals in data:** Ads clicks far exceed GA4 sessions with a gclid. Conversions drop on iOS Safari specifically. CRM leads show a "google / cpc" source but an empty gclid.
- **Sources:** [About auto-tagging](https://support.google.com/google-ads/answer/3095550?hl=en) (checked 2026-10-13); [Consent mode overview (developers)](https://developers.google.com/tag-platform/security/concepts/consent-mode) (checked 2026-10-13); [PPC Land: iOS 26 testing reveals mixed impact](https://ppc.land/ios-26-testing-reveals-mixed-impact-on-google-ads-tracking-parameters/) (checked 2026-10-13); [PPC Land: Safari is quietly killing your GCLID](https://ppc.land/safari-is-quietly-killing-your-gclid-and-here-is-the-fix/) (checked 2026-10-13); [WITHIN: iOS 26 Link Tracking Protection](https://www.within.co/blog/ios-26/) (checked 2026-10-13)
- **Open questions:** What share of real Safari traffic has "All Browsing" protection enabled. Whether Apple will make it the default.

### MEA-CONV-017 · Consent mode: basic vs advanced, and what each denied signal removes
- **Claim:** In *basic* consent mode, Google tags are blocked until the user consents, and nothing (not even the consent state) is sent on denial, so modelling falls back to a general model. In *advanced* mode, tags load with denied defaults and send cookieless pings, which allows advertiser-specific modelling. Effects of each denial: `ad_storage` denied means no ad cookies are read or written, and IPs are truncated. `ad_user_data` denied disables user data for ads, *including user_id and enhanced conversions*. `ad_personalization` denied disables remarketing. `ads_data_redaction` also redacts click IDs.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Pings carry a timestamp, user agent, referrer, consent state, whether a GCLID was present in the URL, and a random per-page number. They carry no identifiers. Google's models use them to estimate the share of unconsented conversions.
- **When it matters / how experts use it:** In the EEA, UK and Switzerland, where a meaningful share of users decline consent (rates vary widely by site, banner design and country; no reliable benchmark was opened this session), consent mode decides how many conversions bidding sees. Advanced mode generally recovers more, but it is a legal decision for the advertiser, not a tracking tweak.
- **Exceptions and failure modes:** A consent banner that fires its update *after* the conversion tag drops the conversion. Tag Assistant should show the default (denied) consent before any tag fires and the update after acceptance.
- **Signals in data:** The Google Ads consent mode status, which shows "implemented" but "modeling not active" when below thresholds. Conversion drops when a consent management platform (CMP) is launched.
- **Sources:** [Consent mode overview (developers)](https://developers.google.com/tag-platform/security/concepts/consent-mode) (checked 2026-10-13); [About consent mode (Google Ads Help)](https://support.google.com/google-ads/answer/10000067?hl=en) (checked 2026-10-13); [Verify consent mode implementation (GA Help)](https://support.google.com/analytics/answer/14218557?hl=en) (checked 2026-10-13)

### MEA-CONV-018 · Consent mode conversion modelling in Google Ads: thresholds and where modelled conversions go
- **Claim:** Modelling activates after **700 ad clicks over 7 days per country and domain grouping**, followed by a training period. Modelled conversions (and values) are added to the standard "Conversions" column at the same granularity as observed ones, and they feed Smart Bidding. Google says consented users typically convert 2-5x more often than unconsented users, and its models aim to *minimize over-prediction*, so some real conversions stay unaccounted for.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google uses observed conversion rates among consented users and cookieless pings to estimate conversions among unconsented clicks, and calibrates per advertiser when pings exist. Google's worked example: a 50% consent rate caused a 19% conversion drop, and modelling recovered part of it, an 18% conversion-rate uplift. Uplift reporting appears after at least 7 full days and is shown for 4 weeks after modelling starts.
- **When it matters / how experts use it:** Small EEA accounts below 700 clicks/week per country/domain get *no* modelling, so their reported conversions are structurally low. Lower tCPA, or raise tROAS expectations, accordingly. Do not compare EEA and non-EEA CPAs directly.
- **Exceptions and failure modes:** There is no column that separates modelled from observed conversions in campaign reports, so per-row modelled share cannot be audited. Modelling stops if eligibility lapses.
- **Signals in data:** Conversion counts in the EEA rise gradually after consent mode launch. Ads conversions exceed GA4 key events or CRM for the same period.
- **Sources:** [About consent mode modeling (Google Ads)](https://support.google.com/google-ads/answer/10548233?hl=en) (checked 2026-10-13); [Verify consent mode implementation (GA Help)](https://support.google.com/analytics/answer/14218557?hl=en) (checked 2026-10-13)

### MEA-CONV-019 · EEA consent requirements, and the June 2026 shift of ads-data control to consent mode
- **Claim:** Since March 2024, advertisers must collect consent from EEA end users and pass it to Google via consent mode v2 (`ad_user_data`, `ad_personalization`) to keep measurement, personalization and remarketing for EEA traffic. This also applies to UK firms advertising into the EEA. **(changed 2026-06)** From 15 June 2026, Google Ads consent mode, not GA4's Google Signals setting, is the single control over Google Ads cookies and IDs collected through the GA tag and SDK. Google Signals now only controls linking GA data to signed-in users for GA behavioural reporting. Google says ads-personalization control (via `ad_personalization`) and encrypted IP sharing to linked Ads accounts will follow later in 2026.
- **Evidence type:** documented (GA Help 17016975); google-statement via press (2024 enforcement)
- **Confidence:** high (June 2026 change); medium (2024 details reported by SEJ, which quotes Google's help text)
- **How it works:** With consent signals missing for EEA traffic, Google limits ad personalization and remarketing. With `ad_storage` granted, GA4-linked data can now feed Ads even when Signals is off (per Simo Ahava, as reported by PPC Land).
- **When it matters / how experts use it:** Any EEA account audit: check that the CMP is certified, that defaults fire before tags, and that `ad_user_data` is passed (or enhanced conversions do nothing). After June 2026, turning Signals off in GA4 no longer stops Ads data collection. Privacy reviews must look at consent mode.
- **Exceptions and failure modes:** Consent rules differ by jurisdiction. This is not legal advice.
- **Signals in data:** EEA remarketing lists stop growing. Enhanced conversions coverage near zero in EEA countries.
- **Sources:** [GA Help: consolidating data controls (Google Signals change)](https://support.google.com/analytics/answer/17016975?hl=en) (checked 2026-10-13); [PPC Land: Google strips Analytics of ad data authority in June 2026](https://ppc.land/google-strips-analytics-of-ad-data-authority-in-june-2026-consent-overhaul/) (checked 2026-10-13); [SEJ: Consent mode v2 key details](https://www.searchenginejournal.com/consent-mode-v2-google-shares-shares-key-details-for-advertisers/508623/) (checked 2026-10-13)

### MEA-CONV-020 · Duplicate and inflated conversions: causes and the transaction-ID defence
- **Claim:** Common causes of inflation: the same event tracked twice as primary (Ads tag *and* GA4-imported key event in the same goal), thank-you page reloads or revisits, "Every" counting on leads, static or placeholder transaction IDs, and spam or bot form fills. Google deduplicates conversions that share a transaction ID *within the same conversion action*. It does not deduplicate view-through conversions, and `GG_`-prefixed IDs mean the tag sent none.
- **Evidence type:** documented (transaction ID behaviour); inference/practitioner (cause list)
- **Confidence:** high
- **How it works:** A static ID (for example "thank_you") makes Google keep only the first instance, which causes massive *under*counting. A missing ID allows duplicates. Dedup does not work across actions, so two actions for one purchase both count if both are primary in the campaign's goals.
- **When it matters / how experts use it:** Before any bid or target change, compare conversions with real orders or leads for the same dates (by conv. time). Keep one primary source per business event, and put the other one (usually the GA4 import) as secondary. Use server-generated order IDs, and the same ID in any backend upload so tag and import deduplicate.
- **Exceptions and failure modes:** Google says reports can occasionally show more conversions than clicks, which is legitimate when a converting click was later judged invalid (MEA-ECON-001), or with engaged-view and modelled conversions.
- **Signals in data:** Conversions above orders. A conversion rate jump on a tag-change date. A "Google tag is missing transaction ID" diagnostic. Value per conversion halves (sign of a duplicated low-value event).
- **Sources:** [Use a transaction ID to minimize duplicate conversions](https://support.google.com/google-ads/answer/6386790?hl=en) (checked 2026-10-13); [About primary and secondary conversion actions](https://support.google.com/google-ads/answer/11461796) (checked 2026-10-13)

### MEA-CONV-021 · GA4-imported conversions vs native Google Ads conversions
- **Claim:** Native Google Ads tag conversions and GA4 key events imported into Ads differ in five ways. (1) Ads reports by click date, while GA4 reports by event date. (2) GA4 counts conversions from all channels, while Ads counts only those credited to Google Ads. If the GA4 setting "channels that can receive credit" is "Paid and organic", organic and other channels can take credit, and Ads receives fewer. (3) Cookie and window lengths differ: Ads cookies last 90 days and windows 1-90 days, while GA4 cookies last up to 2 years and lookback windows are 30, 60 or 90 days. (4) GA4 imports arrive up to about 24 hours later. (5) Actions created from GA4 default to *secondary*, and their window and count may be managed in GA4.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** GA4's reporting attribution model (DDA or paid-and-organic last click) changes retroactively in GA4 reports. The "channels that can receive credit" setting applies only going forward and takes days to reach Ads. GA4 rule-based models (first click, linear, time decay, position) have been unavailable since November 2023.
- **When it matters / how experts use it:** Many practitioners bid on the native Ads tag, which is faster and has a Google-ads-only scope with enhanced conversions, and keep the GA4 import secondary as a cross-check. GA4 import can be preferable when GA4 already holds server-side or enriched events, or when there is a single source of truth policy. Either way, *one* primary per business event.
- **Exceptions and failure modes:** App conversions always use Google paid channels. Analytics events can be filtered out by invalid click detection. Historical data before the import is not backfilled.
- **Signals in data:** GA4 shows more conversions than Ads for long-cycle products (longer cookies). Ads shows more than GA4 when GA4 consent or ad blockers bite harder, or with modelled conversions.
- **Sources:** [Create conversions from Google Analytics events in Google Ads](https://support.google.com/google-ads/answer/2375435?hl=en) (checked 2026-10-13); [GA4 attribution settings](https://support.google.com/analytics/answer/10597962?hl=en) (checked 2026-10-13)

### MEA-CONV-022 · Data exclusions: telling Smart Bidding to ignore broken conversion data
- **Claim:** Data exclusions (Tools > Adjustments > Exclusions) tell Smart Bidding to ignore clicks, and their conversions, from a date range with broken tracking, site outages or failed uploads. They work in both directions: missing conversions and inflated ones. They do *not* change reported conversions, they apply only to conversion-based Smart Bidding on Search, Display, Shopping and Performance Max, and they are not available for Hotel campaigns.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Exclusions are dated by *click*. Extend the start date back by the conversion delay and cover at least 90% of affected clicks. Google's example: an issue on 15-18 Oct with a 5-day delay means excluding 10-18 Oct. Future exclusions (planned maintenance) take effect within about a day.
- **When it matters / how experts use it:** Apply as soon as the break is found. Do not remove an exclusion once applied, and do not backfill data, because that disturbs bidding. If backfill is needed for reporting, wait at least 5 days after the exclusion. Expect fluctuation for a few days, or for 1-2 conversion cycles if a week or more was excluded. Adjust targets and budgets temporarily.
- **Exceptions and failure modes:** Frequent or long exclusions degrade bidding. For gradual degradation (slowly declining match rate) there is no clean date range. Exclusions do not fix reporting for stakeholders.
- **Signals in data:** Abrupt conversion-rate cliff or spike with stable traffic. Tag diagnostics flag "no recent conversions". Upload job failures.
- **Sources:** [About data exclusions](https://support.google.com/google-ads/answer/10370710?hl=en) (checked 2026-10-13); [Use data exclusions for conversion data outages](https://support.google.com/google-ads/answer/10276486?hl=en) (checked 2026-10-13)

### MEA-CONV-023 · Call conversions: five types with very different evidential strength
- **Claim:** Google offers (1) calls from ads (call assets or call-only ads, through a Google forwarding number, counted when the call lasts at least a minimum length you set), (2) calls to a forwarding number on your website after an ad click (website call conversion), (3) clicks on a phone number on the mobile site (the click only, not the call), (4) clicks on call ads and assets, where Google *estimates* whether a meaningful call followed, and (5) imported call conversions from your own system. **(changed 2026-04)** In the US and Canada, "Calls from ads" are judged by AI-qualified call leads from the call recording, and the minimum length is only a fallback (MKT-LOCAL-014).
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Forwarding numbers exist in 30 countries. A website forwarding number keeps routing for 60 days after the user's last call. If the user writes it down, the first call connects only within about 30 minutes, or up to about 2 hours in some markets. The website snippet tracks one number per page by default. GTM is not recommended with dynamic number insertion (DNI) or third-party call tracking.
- **When it matters / how experts use it:** For service businesses, phone calls are often the main conversion. Prefer duration-qualified calls (2) or imported qualified calls (5) for bidding over tap-to-call clicks (3) and estimated call clicks (4), which inflate easily. Set the minimum duration from the actual business: how long a real enquiry takes versus a wrong number or spam.
- **Exceptions and failure modes:** Outside the 30 countries, ad call tracking falls back to (3), (4) or third-party tools. Phone-tree systems with early media can report missed calls. Display call assets cannot use forwarding numbers.
- **Signals in data:** Call conversions far exceed calls logged by staff. Many calls just above the minimum duration. Tap-to-call clicks with no call log.
- **Sources:** [About phone call conversion tracking](https://support.google.com/google-ads/answer/6100664?hl=en) (checked 2026-10-13); [Google forwarding number](https://support.google.com/google-ads/answer/2382961?hl=en) (checked 2026-10-13); [Track calls to a phone number on your website](https://support.google.com/google-ads/answer/6095883?hl=en) (checked 2026-10-13)

### MEA-CONV-024 · Conversion value rules change the value bidding sees, so reported value is not revenue
- **Claim:** Conversion value rules can add to, multiply or set the conversion value based on conditions such as location, device and audience (for example new vs existing customers). Value-based bidding then optimizes on the adjusted value, and the adjusted value appears in conversion value columns. Reported "Conv. value" therefore includes business-weighting adjustments and is not raw revenue.
- **Evidence type:** inference (from prior knowledge of the feature; the Help page could not be opened this session)
- **Confidence:** medium
- **How it works:** Rules apply at conversion time, before bidding and reporting. They encode values the tag cannot see: higher LTV in a region, lower value on a device with more returns, a new-customer premium.
- **When it matters / how experts use it:** Use rules to steer tROAS toward profitable segments without re-tagging. When reconciling "Conv. value" with finance, remove rule adjustments first. Practitioners document each rule's justification and review it quarterly.
- **Exceptions and failure modes:** Arbitrary multipliers can make ROAS look good while revenue is flat. Stacked rules are hard to audit.
- **Signals in data:** Conv. value / revenue ratio is not 1 even with correct tags. ROAS jumps on the date a rule was created.
- **Sources:** Help page (answer/10391326) not reachable during this session; claim from prior knowledge, verify before relying on details.
- **Open questions:** Exact supported campaign types and rule conditions in 2026, and whether a segment or column isolates rule adjustments.

### MEA-CONV-025 · Reconciling Ads, GA4 and CRM: expected gaps vs real problems
- **Claim:** Some gaps between Ads, GA4 and CRM are structural and expected. Ads counts clicks (several per session possible) and filters invalid clicks, which GA4 still records as sessions. A click that leaves before the page loads is in Ads with no GA4 session. Dates differ (click date vs event date). Scope differs (Google Ads-only vs cross-channel). Ads adds modelled and engaged-view conversions. Windows and cookies differ. Only gaps larger than these explain, or gaps that change suddenly, signal a problem.
- **Evidence type:** documented (individual causes); inference (the reconciliation method)
- **Confidence:** high (causes); medium (method)
- **How it works:** Reconcile on a shared basis. Use calendar month by conversion time (Ads "by conv. time" columns, GA4 event date, CRM created date). Use primary actions only. Compare one business event across systems, and record the ratio each month. A stable ratio is acceptable, and a moving ratio is the alarm.
- **When it matters / how experts use it:** Monthly reporting to clients, and before trusting CPA targets. The CRM is the ground truth for outcomes. GA4 is the cross-channel referee. Ads is the bidding signal. Use the CRM-to-Ads ratio to set targets: if Ads reports 1.2x the CRM's paid leads, set tCPA 1.2x tighter than the CRM-based CPA.
- **Exceptions and failure modes:** Offline-heavy businesses (phone, in-store) cannot reconcile without call and store imports. Different time zones between systems shift day boundaries.
- **Signals in data:** Ratio drift after a site release, a CMP change or a form change. Sudden divergence on one device or browser (Safari).
- **Sources:** [Fix missing data and discrepancies](https://support.google.com/google-ads/answer/2404039) (checked 2026-10-13); [Create conversions from Google Analytics events](https://support.google.com/google-ads/answer/2375435?hl=en) (checked 2026-10-13); [About "by conversion time" columns](https://support.google.com/google-ads/answer/9549009?hl=en) (checked 2026-10-13)

### MEA-CONV-026 · Cross-device and modelled conversions are part of "Conversions" and cannot be audited row by row
- **Claim:** Google Ads "Conversions" mixes observed conversions with conversions inferred from three sources: cross-device conversions (included by default, for example in current-model columns), consent-mode modelled conversions, and iOS/braid modelling. These cannot be separated in standard campaign reports.
- **Evidence type:** documented (inclusion); inference (non-separability, from the absence of a column in the docs opened)
- **Confidence:** medium
- **How it works:** Google links signed-in users across devices and uses enhanced conversion matches, then models what it cannot observe and adds it to the totals with no flag.
- **When it matters / how experts use it:** Expect Ads to report more than the CRM can tie to gclids. Use the ratio approach in MEA-CONV-025, and incrementality tests (MEA-ECON on lift), rather than trying to audit each conversion.
- **Exceptions and failure modes:** In small or new accounts below modelling thresholds, the totals are mostly observed.
- **Signals in data:** The "conversions > clicks" anomaly at keyword level. A gap between Ads and gclid-matched CRM records that grows with iOS share or EEA share.
- **Sources:** [About attribution models](https://support.google.com/google-ads/answer/6259715) (checked 2026-10-13); [About consent mode modeling](https://support.google.com/google-ads/answer/10548233?hl=en) (checked 2026-10-13); [Updates to iOS 14 campaign measurement](https://support.google.com/google-ads/answer/10417364?hl=en) (checked 2026-10-13)

### MEA-CONV-027 · GA4 behavioural modelling has separate, higher thresholds and only fills user and session metrics
- **Claim:** GA4 behavioural modelling needs consent mode on all pages, at least 1,000 events/day with `analytics_storage` denied for 7+ days, and at least 1,000 daily consented users on 7 of the previous 28 days. Even then, eligibility is not guaranteed. It models users and sessions (shown only with "Blended" reporting identity), not event counts. It is unavailable in audiences, explorations of several kinds, BigQuery export and predictive metrics.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The model starts on the date of eligibility, with no backfill, and stops if eligibility lapses.
- **When it matters / how experts use it:** Most small advertisers will *not* get GA4 behavioural modelling, so GA4 sessions and users in the EEA are under-counted relative to Ads clicks. Do not read the click-to-session gap there as bot traffic without checking the consent rate.
- **Exceptions and failure modes:** BigQuery-based analyses never include modelled data, so they will always differ from GA4 UI reports.
- **Signals in data:** The reporting identity setting. A sudden rise in users on the eligibility date.
- **Sources:** [GA4 behavioral modeling for consent mode](https://support.google.com/analytics/answer/11161109?hl=en) (checked 2026-10-13)

### MEA-CONV-028 · Learning periods and target resets after conversion setup changes
- **Claim:** **(corrected 2026-10)** Smart Bidding recalibrates after a strategy, setting or composition change, and conversion-goal changes alter what it optimises. Google states that changing a CPA or ROAS target does not trigger "Learning" status or reset what was learned (PLT-BID-011); the old "any change resets learning" reading is folklore. Any conversion setup change that alters the "Conversions" stream (new primary action, model switch, counting change, value rules) therefore changes what the bidder optimizes, and should be made deliberately, together with target rescaling.
- **Evidence type:** documented (learning phase); inference (bundling advice)
- **Confidence:** medium
- **How it works:** The bid model's predicted conversion rates and values are trained on the conversion stream. Change the stream and past predictions are miscalibrated until enough new data arrives, roughly 1-3 conversion cycles in practitioner experience.
- **When it matters / how experts use it:** Batch measurement changes, avoid stacking them with budget changes, annotate dates, and judge only after lag plus learning.
- **Exceptions and failure modes:** Low-volume campaigns may never stabilize. Treat the 7-14 days as Google's typical figure, not a guarantee.
- **Signals in data:** The bid strategy status shows "Learning". CPA is volatile after a goal edit.
- **Sources:** [About conversion goals](https://support.google.com/google-ads/answer/10995103) (checked 2026-10-13); [About primary and secondary conversion actions](https://support.google.com/google-ads/answer/11461796) (checked 2026-10-13)

### MEA-CONV-029 · The "by conv. time" view is for reconciliation, standard columns for efficiency
- **Claim:** Use standard (click-date) columns for CPA, ROAS and bid evaluation, because cost and conversions share a date basis. Use "(by conv. time)" columns to match sales or CRM records in a calendar period. Mixing the two, for example by-conv-time conversions divided by click-date spend, produces an efficiency number that is wrong whenever spend or lag changes.
- **Evidence type:** documented (definitions); inference (usage rule)
- **Confidence:** high
- **How it works:** In a period of rising spend, by-conv-time conversions lag the spend and CPA looks worse. In a falling period it looks better.
- **When it matters / how experts use it:** Monthly client reporting, budget pacing, and promotions with sharp spend changes.
- **Exceptions and failure modes:** With near-zero lag both views agree.
- **Signals in data:** Month-over-month CPA moves in opposite directions depending on the column set used.
- **Sources:** [About "by conversion time" columns](https://support.google.com/google-ads/answer/9549009?hl=en) (checked 2026-10-13)

### MEA-CONV-030 · Recommended baseline conversion architecture (synthesis)
- **Claim:** A defensible baseline: one primary action per business outcome, using native Ads tag or Data Manager upload. Transaction IDs on purchases, "One" counting on leads. Enhanced conversions on with consent passed. Click IDs (gclid, wbraid, gbraid) captured into CRM, and deeper funnel stages imported (qualified, won) with value. GA4 key events imported as secondary for cross-checks. Windows matched to the sales cycle. DDA unless a reason exists. Data exclusions ready for incidents. A monthly reconciliation ratio against the CRM.
- **Evidence type:** inference (from documented mechanisms in MEA-CONV-001 to 029)
- **Confidence:** medium
- **How it works:** Each element closes a known failure: double counting, spam leads, cookie loss, lag misreads, or bidding on the wrong outcome.
- **When it matters / how experts use it:** Use as a checklist for a new account audit. Deviations are fine when justified, for example GA4 as the primary source for server-side enriched events, or last click for very sparse actions where DDA adds noise.
- **Exceptions and failure modes:** Very small accounts may lack volume for deep-funnel bidding. Use the shallower action as primary and the deeper one for reporting and value rules.
- **Signals in data:** n/a (audit framework).
- **Sources:** See the entries above (all checked 2026-10-13).

## Common mistakes and misleading metrics
- **Reading the last 7-30 days of CPA or ROAS as final.** Click-date reporting plus lag makes recent periods look worse (MEA-CONV-008). Account for "Avg. days to conversion".
- **Two primaries for one event.** The Ads tag plus the GA4 import, or a purchase plus a "thank you page view" action, double the Conversions column and train bidding on an inflated CVR (MEA-CONV-020).
- **Micro-conversions as primary.** Add to cart, scroll or time-on-site as primary makes CPA look excellent while sales stay flat (MEA-CONV-002).
- **Comparing periods across a model, window or count change** without current-model columns (MEA-CONV-007).
- **Treating the 200 conversions / 2,000 interactions figure as a DDA eligibility rule.** It is a recommendation (MEA-CONV-006).
- **Assuming "Conversions" = observed conversions.** It includes modelled, cross-device and engaged-view conversions (MEA-CONV-005, 018, 026).
- **Treating "Conv. value" as revenue** when value rules or modelled values apply (MEA-CONV-024).
- **Fixing a tracking outage by backfilling** instead of using data exclusions (MEA-CONV-022).
- **Building a new CRM upload on the Google Ads API in 2026.** It will be rejected for new adopters (MEA-CONV-012).
- **Assuming iOS Safari strips gclid everywhere, or nowhere.** It depends on mode and settings (MEA-CONV-016).
- **Tap-to-call clicks counted as calls** (MEA-CONV-023).

## Unresolved questions
- The exact allowlist window for legacy Google Ads API offline import (blog: Dec 2025 to May 2026; Help: Jan to June 2026), and whether legacy access has an end date.
- Whether conversion adjustments, call conversion imports and store sales via the Google Ads API fall under the June 2026 restriction.
- The size of the modelled share inside "Conversions" for a given account. Google exposes uplift only for 4 weeks after modelling starts.
- The real-world share of Safari users with Advanced Tracking and Fingerprinting Protection set to "All Browsing", and Apple's next step.
- The 2026 conversion value rule specifics (Help page not reachable this session).
- Whether "primary actions not used for optimization may still enhance predictions" means they influence bids in practice. Google gives no detail.
- Whether the GA Help "data freshness" figures (about 12-24 h for imports) still hold for GA4 key events in 2026.
