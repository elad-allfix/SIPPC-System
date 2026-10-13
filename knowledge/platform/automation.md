---
area: platform
topic: automation layer (AI Max, Performance Max, recommendations, AI surfaces)
checked: 2026-10-13
owner: research
---
# Google Ads automation layer: AI Max, Performance Max, recommendations and AI surfaces

This file covers the parts of Google Ads where Google's AI chooses queries, landing pages, ad text, channels or settings: AI Max for Search (and the DSA, auto-created-assets and broad-match-setting migrations into it), Performance Max, Demand Gen and Smart campaigns as they touch search advertisers, auto-applied recommendations and optimisation score, Gemini-based tools (Ask Advisor, AI Brief, generated assets), and ads in AI Overviews and AI Mode. The most important idea: through 2025-2026 Google moved query selection, creative and landing-page choice into its own systems and made them the default (AI Max is on by default for new Search campaigns and was switched on for legacy broad-match-setting/ACA campaigns in September 2026). The advertiser's control now comes mostly from **inputs and exclusions**: conversion goals and values, identical exact-match keywords (which still win precedence), negatives, brand and URL lists, budgets and targets, and controlled experiments. Google's published uplift numbers come from selected cohorts. Independent studies of the same features show wide variance and often higher CPA or lower ROAS on the incremental traffic.

Source-access note: research for this file hit the session's web-search and web-fetch quotas. Entries cite only pages that were actually opened. Where a relevant primary page could not be opened (account-level negative keywords, PMax final URL expansion help, Smart campaigns, Google Ads Developer Blog post of 2026-08-12), the entry says so and confidence is lowered.

---

## A. AI Max for Search campaigns

### PLT-AUTO-001 · AI Max is a settings layer on a Search campaign, not a campaign type
- **Claim:** AI Max for Search is a bundle of switches on a standard Search campaign: **search term matching** (ad-group level, on by default when AI Max is enabled) and **asset optimisation**, which covers **text customization** (formerly automatically created assets) and **final URL expansion** (both campaign level). Each part can be turned off separately. **(changed 2025-05; default-on for new Search campaigns by 2026-06)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google calls AI Max "a continuous optimization layer for your Search campaigns." It keeps the campaign/ad group/keyword structure and adds query expansion and generated creative on top. Turning AI Max off disables its brand and URL controls. Turning it back on "will re-enable those settings just as they originally were set." Google launched it in open beta in late May 2025. In June 2026 the Ads Liaison said AI Max is now the default for **new** Search campaigns, citing faster time to first conversion in tests.
- **When it matters / how experts use it:** Check the AI Max state of every Search campaign during an audit. Since mid-2026 a new campaign can have it on without anyone deciding to. Treat the three components as separate decisions: many practitioners enable search term matching in a test while keeping final URL expansion off for regulated or single-offer sites.
- **Exceptions and failure modes:** Google says AI Max "won't be effective if campaigns are limited by budget" and shows an alert when they are. Full capability needs conversion- or value-based bidding (see PLT-AUTO-002).
- **Signals in data:** "AI Max" in the campaign settings panel. "AI Max" match type rows in the search terms report. "Google AI" in the asset report's "Added by" column. "Total: AI Max ..." rows in the keywords report.
- **Sources:** [Optimize Google Ads with AI Max for Search campaigns (how it works)](https://support.google.com/google-ads/answer/15910187) (checked 2026-10-13); [AI Max overview](https://support.google.com/google-ads/answer/15910366) (checked 2026-10-13); [Google blog: AI Max for Search campaigns, 2025-05-06](https://blog.google/products/ads-commerce/google-ai-max-for-search-campaigns/) (checked 2026-10-13); [SEL: Google delays DSA migration, 2026-06-12](https://searchengineland.com/google-delays-dynamic-search-ads-migration-to-ai-max-480049) (checked 2026-10-13)

### PLT-AUTO-002 · Search term matching = AI broad match on your keywords + keywordless matching from your site and assets; it needs Smart Bidding
- **Claim:** Search term matching adds two kinds of traffic. **AI Max broad match** expands your existing keywords, including exact and phrase, to broad-style matching. **Keywordless** matching uses landing-page and asset content, like DSA. It does not work with Manual CPC.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The API labels the sources `AI_MAX_BROAD_MATCH` (expanded from your keywords) and `AI_MAX_KEYWORDLESS` (from website content or landing pages). The UI shows them as the keyword-report rows "Total: AI Max expanded matches" and "Total: AI Max landing page matches". The FAQ says "The Search Term Matching feature in AI Max will not work with manual CPC bidding," and full capability requires "a conversion or conversion value-based bidding strategy." The Ads Liaison has described search term matching as extending broad-match-style behaviour to phrase and exact keywords.
- **When it matters / how experts use it:** Turning AI Max on effectively converts a tightly controlled exact/phrase campaign into a broad-match campaign. Judge it the way you would judge a broad match rollout: is conversion tracking strong enough, and are the conversion values truthful? Use the two keyword-report rows to see which mechanism drives the volume. Keywordless traffic depends heavily on site content, so thin, outdated or ambiguous pages produce poor matches.
- **Exceptions and failure modes:** Because matching follows the site content, a site that ranks for informational topics (blogs, guides) can pull research-stage queries. Search term matching can be switched off per ad group, which lets you protect an exact-only "core" ad group.
- **Signals in data:** Search terms with match type "AI Max". A large "landing page matches" row means the site, not the keywords, is driving matching. Blog or support URLs in the landing pages report with "Selected by" = AI Max.
- **Sources:** [AI Max FAQ](https://support.google.com/google-ads/answer/15913066) (checked 2026-10-13); [Google Ads API: AI Max reporting](https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/ai-max-reporting) (checked 2026-10-13); [About reporting in AI Max](https://support.google.com/google-ads/answer/16470459) (checked 2026-10-13); [TechWyse summary of Ginny Marvin PPC Chat Q&A, 2026-06-11](https://www.techwyse.com/?p=76611) (checked 2026-10-13)

### PLT-AUTO-003 · Keyword precedence: identical exact match still wins, but leaving the broad-match setting changes how broad keywords rank
- **Claim:** Google serves a query in this order: (1) an **exact match keyword identical to the query** (after spell correction) beats everything, including PMax. (2) **Identical** phrase or broad keywords, including AI Max, and identical PMax **search themes** share the next tier. (3) AI-judged ad group relevance. (4) Ad Rank breaks ties. When a campaign moves from the campaign-level broad match setting to AI Max, its broad keywords **lose exact-match-equivalent priority**. **(changed 2026-09 for migrated campaigns)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Under the old campaign-level broad match setting, a broad keyword identical to the query got exact-tier priority. The AI Max help page says broad keywords are no longer treated as exact in prioritisation after the switch. To keep the previous behaviour, add exact-match copies. Converting broad keywords to exact match removes their historical statistics. If no keyword is identical to the query, "the campaign with the higher Ad Rank will serve" across Search, AI Max and PMax. Search keywords also lose to PMax if they are ineligible: the campaign is budget-limited, the keyword has low search volume, all creatives or landing pages are disapproved, or targeting requirements aren't met.
- **When it matters / how experts use it:** The "exact match fortress" pattern: put the queries you most want to control (brand, top converters) as exact keywords in well-funded campaigns, so they win precedence over AI Max expansion and PMax. Keep those campaigns out of "Limited by budget". Otherwise PMax can take the traffic legitimately.
- **Exceptions and failure modes:** Precedence applies only to **identical** queries. Close variants and longer queries fall through to relevance and Ad Rank. For ads **inside** AI Overviews, exact match is not eligible, so an exact keyword does not block a broad keyword from serving there (see PLT-AUTO-030).
- **Signals in data:** After the September 2026 migration, top queries shift from a broad keyword's row to another ad group or to PMax. Search term overlap between Search and PMax. "Limited by budget" on the campaign that should own a term.
- **Sources:** [About keyword matching options (prioritization)](https://support.google.com/google-ads/answer/7478529) (checked 2026-10-13); [How Performance Max interacts with other campaigns](https://support.google.com/google-ads/answer/13810170) (checked 2026-10-13); [AI Max how it works](https://support.google.com/google-ads/answer/15910187) (checked 2026-10-13)

### PLT-AUTO-004 · Text customization and final URL expansion rewrite ads and landing pages and override pinning
- **Claim:** Text customization generates headlines and descriptions from your landing pages, ads and keywords. Final URL expansion (FUE) can send a click to a different page on your domain. FUE **requires** text customization, and **pins are not respected** when FUE picks a different URL or URL inclusions are used.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** AI Max identifies marketing messages on your URLs that fit the query, writes assets to complement your ads, and sends the composed ad "as a candidate into auction." Generated assets cannot be created or edited directly, only removed. They show as "Google AI" in the asset report's "Added by" column. In the UI they can only be removed one at a time; bulk removal works through Editor or the API. Turning text customization off marks generated assets "Removed" and also turns FUE off. Dynamic landing pages can 404 if tracking templates don't use `{lpurl}` correctly. Google says to verify that dynamic landing pages work before enabling.
- **When it matters / how experts use it:** These are the riskiest components for compliance-bound advertisers (finance, health, legal), single-offer lead-gen pages, and sites with stale or off-strategy pages. Experts set URL exclusions before enabling (careers, blog, support, legal, out-of-stock or legacy pages) and review the "Expanded final URL assets" tab weekly at first. In April 2026 Google announced **text disclaimers** for regulated industries: guaranteed disclosure text even with FUE.
- **Exceptions and failure modes:** Pinning of legal or required copy silently stops working when FUE is on. Generated claims can conflict with the actual offer, prices or policy. Offline-conversion setups that rely on static landing-page parameters can break.
- **Signals in data:** "Selected by" = AI Max rows in the landing pages report. Spikes in 404s or bounces on unexpected URLs in analytics. Generated headlines with claims you never wrote.
- **Sources:** [AI Max FAQ](https://support.google.com/google-ads/answer/15913066) (checked 2026-10-13); [AI Max how it works](https://support.google.com/google-ads/answer/15910187) (checked 2026-10-13); [About reporting in AI Max](https://support.google.com/google-ads/answer/16470459) (checked 2026-10-13); [PPC Land: AI Brief and text disclaimers, 2026-05-03](https://ppc.land/ai-brief-google-lets-advertisers-steer-ai-max-in-plain-language/) (checked 2026-10-13); [Choice OMG AI Max auto-upgrade dossier, 2026-08-26](https://choice.marketing/research/google-ai-max-auto-upgrade/) (checked 2026-10-13)

### PLT-AUTO-005 · AI Max controls and the level each one lives at
- **Claim:** AI Max has these controls: **brand inclusions** (campaign and ad group), **brand exclusions** (campaign only), **URL inclusions** (ad group), **URL exclusions** (campaign), **locations of interest** (ad group, geographic intent even for keywordless matches), and negative keywords, which "will be respected even with AI Max turned on." **(changed 2025-05)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The API enforces the levels. Negative brand lists attached to an ad group fail with `ONLY_INCLUSION_BRAND_LIST_ALLOWED_FOR_AD_GROUPS`. Attaching a brand list to a non-AI-Max Search campaign fails with `CANNOT_ATTACH_BRAND_LIST_TO_NON_QUALIFIED_SEARCH_CAMPAIGN`. Negative webpage criteria in standard ad groups are campaign level only. URL exclusions can use URL, page title, page content, custom label or category conditions. Brand exclusions take priority over brand inclusions. Turning AI Max off makes the system ignore URL inclusions and exclusions.
- **When it matters / how experts use it:** Brand inclusions on a brand campaign let it run broad or AI Max while serving only on brand-associated queries. Brand exclusions on a non-brand campaign keep it from re-buying your own brand. Competitor-brand exclusions matter because one smec-cited account saw 69% of AI Max Search impressions on competitor brand terms (see PLT-AUTO-008).
- **Exceptions and failure modes:** Brand lists are only as good as Google's brand entity. Generic-word brands may be under- or over-captured, and Google says the general brand "will often, but not always" capture variants. Locations of interest data is aggregated at country level by default in the API.
- **Signals in data:** Competitor names in AI Max search terms. Your own brand queries appearing in a non-brand AI Max campaign. Location interest report rows.
- **Sources:** [AI Max how it works](https://support.google.com/google-ads/answer/15910187) (checked 2026-10-13); [AI Max FAQ](https://support.google.com/google-ads/answer/15913066) (checked 2026-10-13); [Google Ads API: AI Max reporting](https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/ai-max-reporting) (checked 2026-10-13); [About brand settings for Search and PMax](https://support.google.com/google-ads/answer/13721847) (checked 2026-10-13)

### PLT-AUTO-006 · AI Max reporting: where it shows, and the traps
- **Claim:** AI Max reporting appears in four places. (1) The search terms report has a match type "AI Max", a source column, and views including "Search terms and ad combinations" (search term + headline + landing page). Since mid-2026 the default is the landing-page view. (2) The keywords report has two total rows, "AI Max expanded matches" and "AI Max landing page matches". (3) The landing pages report has a "Selected by" column. (4) The asset report has an "Expanded final URL assets" tab and "Google AI" in "Added by". **(changed 2025-05; docs revised 2026-06-23)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Google warns that filtering on match type = "AI Max" "may show lower numbers" because the filter excludes "Other search terms," the queries hidden by privacy thresholds. The API docs say: "Never sum metrics from these two views." The `ai_max_search_term_ad_combination_view` must not be used for reconciliation, and expanded-landing-page rows carry no asset reference.
- **When it matters / how experts use it:** Measure AI Max's contribution from the keywords-report totals and from campaign-level experiments, not by adding up search-term rows. Use the combination view to judge relevance: query, generated headline and chosen URL together. Practitioner scripts, such as Wenner's on SEL, compute overlap between AI Max queries and existing keywords and compare conversion share with spend share.
- **Exceptions and failure modes:** Totals and filtered views won't reconcile. Low-volume terms disappear into "Other". Travel campaigns add feed-based "Booking Links" traffic that has no keyword.
- **Signals in data:** AI Max share of campaign cost compared with its share of conversions. A high share of AI Max spend on queries already covered by your keywords (overlap) suggests reshuffling rather than new demand.
- **Sources:** [About reporting in AI Max](https://support.google.com/google-ads/answer/16470459) (checked 2026-10-13); [Google Ads API: AI Max reporting](https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/ai-max-reporting) (checked 2026-10-13); [PPC Land: Google rewrites AI Max reporting docs, 2026-06-26](https://ppc.land/google-quietly-rewrites-ai-max-reporting-docs-dsa-deadline-moves-to-2027/) (checked 2026-10-13); [SEL: AI Max early case studies and script, 2025-09-30](https://searchengineland.com/ai-max-early-case-studies-analysis-script-462706) (checked 2026-10-13)

### PLT-AUTO-007 · Google's claimed AI Max results, and what the cohort definitions hide
- **Claim:** Google claims advertisers "typically see 14% more conversions or conversion value at a similar CPA/ROAS." For campaigns still mostly on exact and phrase, it claims 27%. In 2026 it added a claim of +7% for the full suite compared with search term matching alone. All three figures are Google internal data for **non-Retail** advertisers.
- **Evidence type:** google-statement
- **Confidence:** medium (that Google said it: high; that it applies to a given account: low)
- **How it works:** The 27% cohort is campaigns where more than 70% of conversions came from exact or phrase keywords. These have the most untapped query space, so the largest relative gains are expected there. "Similar CPA/ROAS" is measured at campaign level, so marginal CPA on the added conversions is not reported. Named case studies: L'Oréal (2x conversion rate, -31% cost per conversion) and MyConnect (+16% leads at -13% CPA).
- **When it matters / how experts use it:** Treat these figures as a prior that needs testing, not as a forecast. Retail is explicitly excluded. Running Google's 50/50 AI Max experiment on your own account is the only valid way to estimate the effect.
- **Exceptions and failure modes:** Survivorship and selection effects: case studies are chosen, and campaigns that already used broad match have less headroom. Conversions counted can include low-value or soft conversions if goals are set loosely.
- **Signals in data:** If experiment results show more conversions at a higher CPA, you are seeing the marginal-cost effect the averages hide.
- **Sources:** [Google blog: AI Max launch, 2025-05-06](https://blog.google/products/ads-commerce/google-ai-max-for-search-campaigns/) (checked 2026-10-13); [AI Max overview](https://support.google.com/google-ads/answer/15910366) (checked 2026-10-13); [Google blog: DSA upgrade to AI Max, 2026-04-15, updated 2026-06-11](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/) (checked 2026-10-13)

### PLT-AUTO-008 · Independent AI Max evidence: more volume, often worse efficiency, high variance
- **Claim:** Independent analyses disagree with Google's "similar CPA" framing. smec (Mike Ryan, 250+ campaigns) found median **revenue +13% and median CPA +16%**, with ROAS ranging from +42% to -35%; he called enabling AI Max "a coin toss" for efficiency. In retail, AI Max traffic ran at about **35% lower ROAS** than other match types and was only about 5% of spend in the campaigns using it. One practitioner's four-month test put AI Max CPA about 90% above phrase match.
- **Evidence type:** study (smec), practitioner (Mantica, Wenner)
- **Confidence:** medium
- **How it works:** The incremental queries are by construction the ones your keywords didn't cover, often longer, more informational, or competitor queries, so their marginal conversion rate is lower. smec also reported broad match cannibalisation (up to 63% of the time), competitor brand hijacking (69% of Search impressions in one account) and Search Partner Network waste (one campaign at 0.07% conversion rate vs 3.04% on Google Search). Wenner's three accounts found 69-81% of AI Max queries were new. Fashion e-commerce benefited, while B2B SaaS was the worst match type because it caught informational queries.
- **When it matters / how experts use it:** Approve AI Max when the business values incremental volume above the current efficiency target: growth goals, headroom on tROAS, long-tail catalogues. Resist it when the CPA ceiling is hard. Put the AI Max-only CPA next to the blended CPA.
- **Exceptions and failure modes:** Most of these studies are not randomised (match-type comparisons inside a campaign are confounded by query mix), samples are small or retail-only, and several were published as social posts. Results from 2025 may not reflect later model updates.
- **Signals in data:** CPA on AI Max match-type rows compared with exact and phrase rows. Competitor-name queries. Search partner segment performance.
- **Sources:** [SEL: AI Max increases revenue 13% but drives higher CPA (smec), 2026-03-05](https://searchengineland.com/google-ai-max-revenue-higher-cpa-study-470928) (checked 2026-10-13); [PPC Land: Independent tests show AI Max underperforms, 2025-11-08](https://ppc.land/independent-tests-show-ai-max-underperforms-traditional-match-types/) (checked 2026-10-13); [SEL: AI Max early case studies (Wenner), 2025-09-30](https://searchengineland.com/ai-max-early-case-studies-analysis-script-462706) (checked 2026-10-13)
- **Open questions:** No published randomised (experiment-based) multi-account AI Max study was found. Whether the 2026 model and AI Brief change the efficiency gap is unknown.

### PLT-AUTO-009 · When AI Max tends to help and when it tends to hurt
- **Claim:** AI Max tends to help where (a) the conversion signal is strong and value-weighted, (b) the site has many specific, high-quality pages (catalogues, locations, services), and (c) the existing keyword set is narrow. It tends to hurt where (a) lead-gen conversions are form fills with no quality feedback, (b) conversion volume is thin, (c) the vertical is regulated or copy-sensitive, or (d) the site has heavy informational content.
- **Evidence type:** inference (from documented mechanics) + practitioner
- **Confidence:** medium
- **How it works:** Keywordless matching follows site content, and broad expansion follows the bidding model's predicted conversion probability. If the conversion action counts any form fill, the model optimises toward cheap, low-quality leads. Wenner's B2B SaaS case found informational traffic pushing CPA above target. Thin data gives the bidder little to separate good expansion from bad. FUE and text customization create compliance exposure, which is why Google added text disclaimers (announced 2026-04-30). Ads inside AI Overviews are also withheld from sensitive verticals (finance, healthcare and others).
- **When it matters / how experts use it:** In lead gen, import offline qualified-lead or sale conversions (or set values by lead stage) before enabling, and consider enabling search term matching only. With thin data, run AI Max on the account's highest-volume campaign or skip it. In regulated verticals, keep FUE off and use URL inclusions only.
- **Exceptions and failure modes:** Some lead-gen accounts report wins (MyConnect, per Google). Practitioner minimum-conversion thresholds vary widely, and none is a Google rule.
- **Signals in data:** Lead-to-sale rate falls after enabling while platform CPA looks fine. AI Max search terms that start with "how", "what" or "free". Disapprovals or legal complaints about generated copy.
- **Sources:** [SEL: AI Max early case studies, 2025-09-30](https://searchengineland.com/ai-max-early-case-studies-analysis-script-462706) (checked 2026-10-13); [About ads and AI Overviews](https://support.google.com/google-ads/answer/16297775) (checked 2026-10-13); [PPC Land: AI Brief and text disclaimers](https://ppc.land/ai-brief-google-lets-advertisers-steer-ai-max-in-plain-language/) (checked 2026-10-13); [Google blog: AI Max launch](https://blog.google/products/ads-commerce/google-ai-max-for-search-campaigns/) (checked 2026-10-13)

### PLT-AUTO-010 · Testing AI Max: built-in experiments, ramp-up and negatives
- **Claim:** Google offers a one-click AI Max experiment, a 50/50 split of the base campaign against an AI Max treatment arm. Search term matching or asset optimisation can be enabled or disabled per ad group in the treatment. Google advises waiting **at least 2 weeks** after enabling before changes such as adding negatives, and using negatives "sparingly."
- **Evidence type:** documented (experiment, 2 weeks) + practitioner (cadence)
- **Confidence:** high (documented parts), medium (practitioner parts)
- **How it works:** The experiment splits traffic within the same campaign, so comparing the arms isolates the AI Max effect better than before/after or match-type comparisons. Wenner suggests watching daily in month one and acting if performance keeps worsening after about 3 weeks.
- **When it matters / how experts use it:** Run the experiment before accepting a forced migration. Pre-define the success metric (marginal CPA or ROAS, or profit, not raw conversions). Block obviously irrelevant spend (competitor brands if unwanted, careers/support pages) immediately rather than waiting 2 weeks. Google's "wait" advice protects learning, not your budget.
- **Exceptions and failure modes:** Low-volume campaigns rarely reach significance in a 50/50 split. Shared budgets and portfolio strategies can contaminate arms.
- **Signals in data:** Experiment scorecard confidence intervals. Different query mixes between arms.
- **Sources:** [AI Max FAQ](https://support.google.com/google-ads/answer/15913066) (checked 2026-10-13); [About reporting in AI Max](https://support.google.com/google-ads/answer/16470459) (checked 2026-10-13); [SEL: AI Max early case studies](https://searchengineland.com/ai-max-early-case-studies-analysis-script-462706) (checked 2026-10-13)

### PLT-AUTO-011 · September 2026 auto-upgrade: legacy broad-match-setting and auto-created-asset campaigns became AI Max
- **Claim:** Search campaigns still using the **campaign-level broad match setting** or **automatically created assets (ACA)** were converted in place to AI Max during September 2026. Creating those legacy configurations was blocked from 2026-08-03. **(changed 2026-09)**
- **Evidence type:** google-statement (Google blog) + secondary (dossier summarising Google Developer Blog 2026-08-12; that post itself could not be opened)
- **Confidence:** medium-high
- **How it works:** As reported in the dossier from Google's developer post, broad-match-setting campaigns got AI Max with search term matching on, text customization off and FUE off. ACA campaigns got search term matching and text customization on, with FUE off. Google's blog confirms that broad-match-setting campaigns get search term matching and ACA campaigns get search term matching plus text customization. API fields `campaign.aca_migration_date_time` and `campaign.broad_match_migration_date_time` mark migrated campaigns. Advertisers were emailed on 2026-08-05 (trade press). After conversion, each component can still be switched off.
- **When it matters / how experts use it:** Any account that had broad match setting or ACA on before September 2026 now has AI Max search term matching on, which means keywordless matching it didn't have before. Re-audit search terms, add exact copies of priority broad keywords (see PLT-AUTO-003), and check brand and URL controls.
- **Exceptions and failure modes:** Campaigns in both cohorts: Google's public table does not say which text-customization default applies. Google has not committed to keeping opt-outs available indefinitely.
- **Signals in data:** Change history around September 2026. Migration timestamps in the API. A step change in query count or CPA in September 2026.
- **Sources:** [Google blog: DSA upgrade to AI Max (updated 2026-06-11)](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/) (checked 2026-10-13); [Choice OMG AI Max auto-upgrade dossier, 2026-08-26](https://choice.marketing/research/google-ai-max-auto-upgrade/) (checked 2026-10-13)
- **Open questions:** Exact behaviour for Manual CPC campaigns in the broad-match cohort (search term matching requires Smart Bidding). The developer post could not be opened.

### PLT-AUTO-012 · DSA sunset: creation ends January 2027, auto-migration to AI Max February 2027
- **Claim:** Google announced on 2026-04-15 that Dynamic Search Ads would be retired into AI Max, originally with auto-upgrade in September 2026. On 2026-06-11 it **delayed DSA auto-migration to February 2027** and restored new-DSA creation from 2026-06-15. New DSA creation ends in January 2027, a reminder comes around 2027-01-15, and remaining DSA campaigns migrate during February 2027. **(changed 2026-04, 2026-06)**
- **Evidence type:** documented / google-statement
- **Confidence:** high
- **How it works:** Dynamic ad groups convert to standard ad groups with search term matching, text customization and FUE all on. Legacy URL (page-feed/webpage) controls are preserved and history stays in the same ad groups. Ginny Marvin said the delay responded to feedback: "you need more time." Google calls AI Max "an evolution of DSA and Performance Max with Final URL expansion" that uses "a superset" of their asset-generation technology.
- **When it matters / how experts use it:** Plan DSA migration as a deliberate experiment before February 2027 rather than accepting defaults. Specifically, decide whether text customization and FUE should stay on, since DSA advertisers effectively already had dynamic URLs. PMG warns that AI Max is not a complete catch-all replacement, so keyword coverage of high-value queries should be built out.
- **Exceptions and failure modes:** DSA "search terms from Dynamic Search Ads" views remain until migration. Note that the AI Overviews help page still lists DSA as an eligible keywordless option.
- **Signals in data:** Banners in the account (from September 2026). DSA ad groups still present.
- **Sources:** [Google blog: DSA upgrade to AI Max](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/) (checked 2026-10-13); [SEL: Google delays DSA migration, 2026-06-12](https://searchengineland.com/google-delays-dynamic-search-ads-migration-to-ai-max-480049) (checked 2026-10-13); [PPC Land: DSA deadline moves to 2027](https://ppc.land/google-quietly-rewrites-ai-max-reporting-docs-dsa-deadline-moves-to-2027/) (checked 2026-10-13); [PMG: DSA deprecation, 2026-05-05](https://www.pmg.com/insights-and-news/google-to-deprecate-dynamic-search-ads-campaigns-requiring-shift-to-ai-max) (checked 2026-10-13); [AI Max FAQ](https://support.google.com/google-ads/answer/15913066) (checked 2026-10-13)

### PLT-AUTO-013 · AI Brief: natural-language steering of AI Max (soft guidance, not hard filters)
- **Claim:** Announced on 2026-04-30, AI Brief is a Gemini interface inside AI Max for Search where advertisers write **messaging guidelines** (content limits for generated copy), **matching guidelines** (search priorities) and **audience guidelines**, and preview sample assets and searches. It is rolling out to English AI Max campaigns first, with PMax and AI Max for Shopping later. Existing text guidelines migrate into it. **(changed 2026-04/05)**
- **Evidence type:** google-statement (via trade press) + practitioner interpretation
- **Confidence:** medium
- **How it works:** Matching guidelines are described as a **soft priority** the system weighs, not a hard filter. Messaging guidelines constrain generated copy. Brainlabs calls it the top release of 2026 because it links how well a brand describes its customers to how the campaign performs.
- **When it matters / how experts use it:** Use AI Brief for things that are hard to express as keywords (tone, banned claims, priority segments). Keep **hard** exclusions in negatives and brand and URL lists, because a soft priority does not stop spend.
- **Exceptions and failure modes:** It is not documented how closely previews predict live behaviour. Availability outside English was uncertain at announcement.
- **Signals in data:** Changes in the AI Max query mix after editing the brief. Generated assets that still violate the brief show its limits.
- **Sources:** [PPC Land: AI Brief, 2026-05-03](https://ppc.land/ai-brief-google-lets-advertisers-steer-ai-max-in-plain-language/) (checked 2026-10-13); [Brainlabs: GML 2026, 2026-05-20](https://www.brainlabsdigital.com/google-marketing-live-2026/) (checked 2026-10-13); [Google Marketing Live 2026 hub](https://business.google.com/us/accelerate/googlemarketinglive/) (checked 2026-10-13)
- **Open questions:** Whether AI Brief is generally available in all English accounts as of October 2026, and in which other languages.

### PLT-AUTO-014 · AI Max for Shopping overlaps Performance Max, and Google has given no rule for choosing
- **Claim:** In 2026 Google extended AI Max to standard Shopping campaigns (beta, one-click toggle) with FUE, text customization and reach into longer conversational queries. It reports via the landing pages ("Automatically selected" in "Selected by"), asset and search terms reports. **(changed 2026-04/05)**
- **Evidence type:** documented + practitioner
- **Confidence:** medium
- **How it works:** The help page says exact match Search keywords take priority, so it advises adding negatives only when needed and judging success at account level. Brainlabs notes Google has given no guidance on choosing between AI Max for Shopping and PMax.
- **When it matters / how experts use it:** Retailers running Standard Shopping for control now face the same expansion choice. Test it with a holdout or experiment rather than switching on account-wide.
- **Exceptions and failure modes:** Shopping campaign priority interactions with PMax are not described on the PMax interaction page.
- **Signals in data:** Text ads and expanded URLs appearing from a Shopping campaign. Search terms with conversational phrasing.
- **Sources:** [About reporting in AI Max for Shopping](https://support.google.com/google-ads/answer/17091676) (checked 2026-10-13); [Brainlabs: GML 2026](https://www.brainlabsdigital.com/google-marketing-live-2026/) (checked 2026-10-13)

---

## B. Performance Max

### PLT-AUTO-015 · How PMax chooses channels: one budget, predicted-value allocation, diagnostics that look like "lower priority"
- **Claim:** PMax spends one budget across Search, Shopping, YouTube, Display, Discover, Gmail, Maps and Search partners. It prioritises channels its models predict will meet the bid goal, so a channel with no listed problems may simply get **lower priority**. Missing assets or feeds make channels ineligible or limited.
- **Evidence type:** documented (diagnostics and priority wording) + inference (allocation logic)
- **Confidence:** medium-high
- **How it works:** The channel performance report's diagnostics list statuses (Not eligible, Eligible (Limited), Eligible, Missing required assets) and causes (policy issues, feed issues, missing network-specific assets such as video, FUE, budget). Google says a channel with no issues may be deprioritised because PMax favours higher-ROI channels. PMax and Demand Gen "interact based on normal auction dynamics."
- **When it matters / how experts use it:** If PMax spends on Display or Video without results, check whether the conversion goal rewards view-through or engaged-view events, and whether missing video assets push Google to auto-generate them. Feed quality determines Shopping eligibility.
- **Exceptions and failure modes:** "ROI" is judged on the conversions you report, so a soft or duplicated conversion action drives spend toward channels that produce that action cheaply.
- **Signals in data:** Channel cost share compared with conversion-value share. Engaged-view conversions concentrated in YouTube. "Missing required assets" diagnostics.
- **Sources:** [About the channel performance report](https://support.google.com/google-ads/answer/16260130) (checked 2026-10-13); [How PMax interacts with other campaigns](https://support.google.com/google-ads/answer/13810170) (checked 2026-10-13)

### PLT-AUTO-016 · Channel performance report (2025): what it shows and doesn't
- **Claim:** Announced on 2025-04-30 and rolled out through 2025, the PMax channel performance report breaks out impressions, clicks, conversions, value and **cost** by channel (Search, Display, YouTube, Discover, Maps, Gmail, Search partners). It has an "ads using product data" segment for Shopping-type ads. Data is available for dates after **2025-06-06**. **(changed 2025-04/06)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** The report uses each conversion action's own attribution model. Store-level offline conversions are summed in totals, not split by channel. Merchant Center feed formats on Gmail and product video ads on YouTube and Discover are not yet included in the product-data segment. AI Overviews are not a separate channel. In January 2026 Google added network segmentation to **placement** reports.
- **When it matters / how experts use it:** Use it to find spend leaking to channels that don't drive value and to decide whether to split out Search, for example by moving top PMax search terms into exact-match Search (PLT-AUTO-019). Pre-June-2025 periods cannot be compared.
- **Exceptions and failure modes:** There are still no channel-level bid or budget controls in PMax. The report diagnoses but does not steer.
- **Signals in data:** Search partners' share of spend. Video channel cost with zero click conversions.
- **Sources:** [About the channel performance report](https://support.google.com/google-ads/answer/16260130) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts, 2025-08-07](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13); [Google: PMax steering and reporting updates 2026, 2026-01-09](https://business.google.com/us/accelerate/resources/articles/new-performance-max-steering-and-reporting-updates-coming-in-2026/) (checked 2026-10-13)

### PLT-AUTO-017 · PMax search terms report and campaign-level negatives (2025)
- **Claim:** During 2025 PMax gained a full **search terms report** (UI and API), **campaign-level negative keywords** (rollout from January 2025, with the limit raised to 10,000 around March 2025), and in August 2025 **shared negative keyword lists** applicable to PMax. Negatives apply to Search and Shopping inventory. **(changed 2025-01 to 2025-08)**
- **Evidence type:** documented + trade press (dates)
- **Confidence:** high (features), medium (exact dates and limits: the PPC Land timeline gives 10,000 per campaign while its body text gives 5,000 per list and 20 lists, so the figures conflict)
- **How it works:** Before 2025, PMax negatives needed account-level lists or a Google rep. Now normal negative-keyword hygiene applies. Search themes and exclusions coexist ("Exclusions and negative keywords still apply").
- **When it matters / how experts use it:** Run the same search-term review for PMax as for Search. Add a shared "junk" list (jobs, free, DIY, competitor names if unwanted) across Search and PMax. Exclude brand from PMax via brand exclusions (PLT-AUTO-018) rather than hundreds of negatives.
- **Exceptions and failure modes:** Negatives don't affect Display, YouTube or Gmail placements. Those need placement or content exclusions. Over-negation can starve PMax and push it toward non-search channels.
- **Signals in data:** Search terms in PMax that overlap your Search keywords. A shift of spend to video or display after heavy negation.
- **Sources:** [Unlock more visibility and control in PMax, 2025-08-07](https://support.google.com/google-ads/answer/16451273) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13); [Use search themes with PMax](https://support.google.com/google-ads/answer/14767319) (checked 2026-10-13)
- **Open questions:** Current account-level negative keyword limits and scope: the help page could not be opened in this session.

### PLT-AUTO-018 · Brand exclusions and inclusions: scope across Search, PMax and Shopping
- **Claim:** Brand **exclusions** work in Search (all match types and DSA, from 2024-06) and in PMax, where they cover **Search and Shopping inventory**. In 2025, feed retailers gained format-specific exclusions (text ads vs Shopping ads). Brand **inclusions** apply only in Search, with broad match or AI Max, and restrict serving to brand-associated queries. Exclusions beat inclusions. **(changed 2024-06, 2025)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Brand lists are built on Google's brand entities (logo, trademark, domain, product name or business name). They cover misspellings, variants and other languages. From 2024-06, one negative keyword also covers misspelled variants: Google's example is "YouTube" covering about 1.5M misspellings. Google warns brand settings "limit the reach of a campaign and performance may decrease."
- **When it matters / how experts use it:** The standard pattern is a brand Search campaign (exact plus brand-inclusion broad or AI Max), with brand exclusions on PMax and non-brand AI Max so they don't claim cheap brand conversions. Feed retailers who want branded Shopping ads in PMax but not branded text ads can use the format-specific option.
- **Exceptions and failure modes:** Brands that are generic words. Reseller brands (e.g., a retailer selling brand X wants brand-X queries). New or local brands Google doesn't have as entities.
- **Signals in data:** Own-brand queries in PMax search terms. A falling blended CPA in PMax alongside falling brand-campaign volume points to brand cannibalisation.
- **Sources:** [About brand settings for Search and PMax](https://support.google.com/google-ads/answer/13721847) (checked 2026-10-13); [Maximize performance on Search with updates to query matching, 2024-06-26](https://support.google.com/google-ads/answer/15070437) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13)

### PLT-AUTO-019 · PMax vs Search in practice: overlap is common, and Search usually converts better on shared terms
- **Claim:** In Brad Geddes's analysis of 3,300+ non-retail PMax campaigns (about 1.2M terms), 45% of PMax search terms could also trigger Search, and 67% of PMax campaigns overlapped Search keywords on at least one term. On overlapping terms, PMax won impressions 61% of the time, but **Search had the higher conversion rate about 84% of the time** and higher conversion value about 85% of the time.
- **Evidence type:** study (vendor, disclosed conflict of interest)
- **Confidence:** medium
- **How it works:** Overlap happens because precedence only protects **identical** exact matches (PLT-AUTO-003). Everything else is Ad Rank, where PMax can bid using cross-channel signals.
- **When it matters / how experts use it:** Mine PMax search terms. Add proven converters as exact keywords in Search (ensuring budget so they stay eligible). Use PMax for incremental reach rather than letting it absorb search demand.
- **Exceptions and failure modes:** Retail was excluded. The 2024 data predates PMax campaign-level negatives and AI Max. A higher Search conversion rate on a term may partly reflect audience differences rather than campaign superiority.
- **Signals in data:** The same query appearing in both PMax and Search reports. PMax conversion rate on those terms below Search's.
- **Sources:** [SEL: PMax vs Search overlap data (Geddes), 2024-12-03](https://searchengineland.com/performance-max-vs-search-campaigns-overlap-data-448788) (checked 2026-10-13); [About keyword matching options](https://support.google.com/google-ads/answer/7478529) (checked 2026-10-13)

### PLT-AUTO-020 · Search themes are additive hints with phrase/broad priority, not targeting
- **Claim:** PMax search themes (up to **50 per asset group**, doubled from 25 in 2025) are "optional and additive" to what PMax predicts. They do not restrict serving. They share phrase/broad-tier priority with Search keywords, and an identical theme can beat a non-identical phrase keyword. **(changed 2025)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Themes guide PMax toward query spaces it may not infer from assets, URLs or the feed. Google advises against near-synonyms ("car"/"automobile"), which reach the same people.
- **When it matters / how experts use it:** Use themes to seed new product lines or a new site with little history. Do not expect them to keep PMax off unrelated queries: negatives and brand exclusions do that.
- **Exceptions and failure modes:** A theme identical to a query your Search campaign covers only with a phrase keyword can send that query to PMax.
- **Signals in data:** Search term insights showing the theme as source. Queries moving from a Search phrase keyword to PMax after adding a theme.
- **Sources:** [Use search themes with PMax](https://support.google.com/google-ads/answer/14767319) (checked 2026-10-13); [About keyword matching options](https://support.google.com/google-ads/answer/7478529) (checked 2026-10-13); [PMax visibility and control](https://support.google.com/google-ads/answer/16451273) (checked 2026-10-13)

### PLT-AUTO-021 · Audience signals are hints; audience exclusions (2026) are the hard control
- **Claim:** PMax audience signals are optional "audience suggestions". "Performance Max may show ads to relevant audiences outside of your signals." In 2026 Google added **first-party (customer list) audience exclusions** in PMax, which are a real restriction. **(changed 2026-01)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Signals seed the model, mostly early in learning. Exclusions remove users. Other 2025-2026 hard controls: device targeting and age exclusions (generally available 2025), gender targeting (beta 2025), budget report, and audience demographic reporting (2026).
- **When it matters / how experts use it:** Don't read signal-audience performance as "who PMax targeted". To stop paying for existing customers, use customer-list exclusions or new-customer goals (PLT-AUTO-022), not signals.
- **Exceptions and failure modes:** Customer-list match rates limit how well exclusions work. Small lists may not meet size thresholds (practitioner experience; thresholds not checked here).
- **Signals in data:** Audience reporting showing most conversions outside signal segments. A high returning-customer share in conversions.
- **Sources:** [About audience signals for PMax](https://support.google.com/google-ads/answer/14530785) (checked 2026-10-13); [Google: PMax steering and reporting updates 2026](https://business.google.com/us/accelerate/resources/articles/new-performance-max-steering-and-reporting-updates-coming-in-2026/) (checked 2026-10-13); [PMax visibility and control](https://support.google.com/google-ads/answer/16451273) (checked 2026-10-13)

### PLT-AUTO-022 · New customer acquisition goals change what PMax and Search optimise for
- **Claim:** Customer acquisition has three modes. **New Customer Value** bids more for new customers and needs a Purchase goal (Search, PMax, Shopping, Demand Gen). **High Value New Customer** (PMax and Search, out of beta in 2025) adds a tier for high-value prospects. **New Customer Only** bids only for new customers and also suits lead gen. Existing customers are defined by advertiser first-party data (customer lists, tags). Since 2025 Google estimates new-vs-returning status for previously "unknown" conversions. **(changed 2025)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** In value modes, Google adds the new-customer value you set to conversions it classifies as new, so value-based bidding pursues them. Classification depends on list and tag coverage, plus Google's estimates where data is missing.
- **When it matters / how experts use it:** Use it where returning customers would buy anyway, which is typical with PMax brand capture. Set the new-customer value from real first-order contribution or LTV, not arbitrarily. Check that reported "new" share is plausible against the CRM.
- **Exceptions and failure modes:** With stale customer lists or no new-customer tag parameter, existing customers get classified as new, so you pay a premium for retention. New Customer Only can starve volume.
- **Signals in data:** The new-vs-returning segment in conversions. Conversion value inflated by acquisition values (watch reported ROAS).
- **Sources:** [About customer lifecycle goals](https://support.google.com/google-ads/answer/12080169) (checked 2026-10-13); [PMax visibility and control](https://support.google.com/google-ads/answer/16451273) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13)

### PLT-AUTO-023 · Final URL expansion, URL rules and feed-only PMax
- **Claim:** PMax can send traffic to URLs other than the asset group's final URL (final URL expansion). In 2025 Google finished reporting on FUE assets (removable) and added "URL contains" rules for feed campaigns. A **feed-only** PMax (product feed with minimal or no creative assets) concentrates spend on product-data formats, but Google can still auto-generate assets.
- **Evidence type:** documented (FUE asset reporting, URL rules) + practitioner/inference (feed-only behaviour)
- **Confidence:** medium (FUE), low (feed-only)
- **How it works:** FUE in PMax uses the same technology family that AI Max extends. "Missing required or network-specific assets" diagnostics show where lack of assets limits channels. Feed-only setups rely on that limitation to keep PMax in Shopping-like inventory. Practitioners use this as a semi-Shopping campaign with PMax bidding signals.
- **When it matters / how experts use it:** Turn FUE off, or add URL exclusions, for lead gen and for sites with pages that shouldn't receive paid traffic. Retailers who want Shopping-like PMax use feed-only asset groups and watch the channel report to confirm.
- **Exceptions and failure modes:** Google can auto-create text, image or video assets unless asset automation is controlled, so feed-only is not a guaranteed channel restriction. Dynamic remarketing on Display is still part of "ads using product data".
- **Signals in data:** The channel report shows non-product-data spend in a feed-only campaign. The "Expanded final URL assets" tab.
- **Sources:** [PMax visibility and control](https://support.google.com/google-ads/answer/16451273) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13); [About the channel performance report](https://support.google.com/google-ads/answer/16260130) (checked 2026-10-13)
- **Open questions:** The current PMax FUE help page and the asset-automation opt-out settings were not opened in this session. Verify the exact controls before advising.

### PLT-AUTO-024 · PMax creative automation: brand guidelines and generated assets
- **Claim:** Since 2025-01-20, new UI-created PMax campaigns require **brand guidelines** (business name, logo, colours, fonts). Rollout to all UI campaigns completed on 2025-07-14, with auto-migration by 2025-10-30. PMax can generate text and image assets, and AI image editing expanded in 2025. From 2026-07-01, Google's terms state advertisers have a "continued obligation to review, approve or remove" automatically generated campaigns and assets, and that inputs to conversational tools "can be used across various Google Ads features." **(changed 2025-01, 2025-07, 2026-07)**
- **Evidence type:** documented / trade press
- **Confidence:** medium-high
- **How it works:** Generated assets compete in the same asset rotation as yours. Responsibility for their content sits with the advertiser under the terms.
- **When it matters / how experts use it:** Review generated assets weekly in regulated verticals. Remove generated assets that make claims you can't support. Treat the terms change as a compliance item (who approves generated copy).
- **Exceptions and failure modes:** Bulk removal of generated text in AI Max needs Editor or the API. Generated imagery can misrepresent products.
- **Signals in data:** "Google AI" or "Automatically created" in "Added by". Disapprovals on generated assets.
- **Sources:** [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13); [PPC Land: Google Ads tells advertisers how inputs will be used from July 2026](https://ppc.land/google-ads-tells-advertisers-how-their-inputs-will-be-used-starting-july-2026/) (checked 2026-10-13); [About reporting in AI Max](https://support.google.com/google-ads/answer/16470459) (checked 2026-10-13)

---

## C. Demand Gen and Smart campaigns (search-advertiser view)

### PLT-AUTO-025 · Demand Gen matters to search advertisers mainly through auction overlap and 2026 measurement features
- **Claim:** Demand Gen and PMax "interact based on normal auction dynamics" (higher Ad Rank wins). GML 2026 added features relevant to a search-led account: Demand Gen on **Google Maps**, **view-through conversion optimisation** (opt-in), **Demand Gen uplift experiments**, **AI-assisted Demand Gen creation from existing PMax campaigns**, and campaign-type attribution. **(changed 2026-05)**
- **Evidence type:** documented (interaction) + google-statement (GML 2026 list)
- **Confidence:** medium
- **How it works:** Demand Gen targets audiences on YouTube, Discover, Gmail (and now Maps), not search queries, so it does not compete with Search keywords directly. It competes with PMax's non-search inventory.
- **When it matters / how experts use it:** For search advertisers it is a demand-creation layer. Judge it with uplift experiments or brand-search lift, not last-click CPA. VTC optimisation inflates platform-reported conversions unless incrementality is tested.
- **Exceptions and failure modes:** Auto-building Demand Gen from PMax copies PMax's assumptions, including weak conversion goals.
- **Signals in data:** Branded search volume after Demand Gen flights. View-through share of conversions.
- **Sources:** [How PMax interacts with other campaigns](https://support.google.com/google-ads/answer/13810170) (checked 2026-10-13); [GML 2026 hub](https://business.google.com/us/accelerate/googlemarketinglive/) (checked 2026-10-13); [Brainlabs: GML 2026](https://www.brainlabsdigital.com/google-marketing-live-2026/) (checked 2026-10-13)

### PLT-AUTO-026 · Smart campaigns: the lowest-control tier (brief)
- **Claim:** Smart campaigns are Google's simplified campaign type for small businesses. They use keyword themes and automated bidding and creative, and give far less query, negative, bidding and reporting control than Search with AI Max. For a strategist, existing Smart campaigns are usually a migration candidate once conversion tracking exists.
- **Evidence type:** inference (no Smart-campaign help page could be opened in this session)
- **Confidence:** low
- **How it works:** Not re-verified this session.
- **When it matters / how experts use it:** Identify Smart campaigns in audits. Plan migration to Search (optionally with AI Max) or PMax when the business can measure conversions, keeping a short overlap period.
- **Exceptions and failure modes:** Very small budgets with no tracking may perform acceptably as Smart campaigns.
- **Signals in data:** Campaign type "Smart". Keyword themes instead of keywords.
- **Sources:** none opened this session (verify before use).
- **Open questions:** Whether Google announced any Smart-campaign sunset or migration in 2025-2026.

---

## D. Recommendations, optimisation score and auto-apply

### PLT-AUTO-027 · Optimisation score measures adoption of Google's recommendations, not performance
- **Claim:** Optimisation score (0-100%) is "an estimate of how well your Google Ads account is set to perform." It is computed from the estimated impact of available recommendations, and **100% can be reached by applying or dismissing all recommendations**. It "is not used by your Quality Score." Google Partner status requires a manager-account score of **at least 70%**.
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Each open recommendation subtracts its estimated uplift. Dismissing it removes the deduction. Dismissed recommendations can return. Because Partner status depends on the score, agencies have an incentive to keep it high, which can be done by dismissing rather than applying.
- **When it matters / how experts use it:** Never treat a higher score as better performance. Read recommendations as hypotheses (keyword, bidding, asset ideas), apply the ones that fit, and dismiss the rest with reasons. Explain to clients why a low score is not a problem.
- **Exceptions and failure modes:** Some recommendations are genuinely useful (conversion tracking upgrades, fixing disapprovals, budget-limited high performers). Ignoring all of them is also a mistake.
- **Signals in data:** A score that jumps without any performance change (dismissals). Recommendations that push broad match, budget increases or higher targets.
- **Sources:** [About optimization score](https://support.google.com/google-ads/answer/9061546) (checked 2026-10-13); [Google Partners requirements](https://support.google.com/google-ads/answer/9702452) (checked 2026-10-13)

### PLT-AUTO-028 · Auto-applied recommendations: what can change silently, and how experts lock them down
- **Claim:** Auto-apply can change keywords (add broad match keywords, add keywords, remove "redundant" or "non-serving" keywords), reach (search partners, targeting expansion, Display expansion), bidding (switch strategies, adjust tCPA or tROAS targets), ads (improve RSAs, optimised rotation) and add DSA. It works at account level only and never raises budgets. On **2026-01-26**, "Add responsive search ads" stopped auto-creating new RSAs. **(changed 2026-01)**
- **Evidence type:** documented
- **Confidence:** high
- **How it works:** Once on, the recommendations "apply regularly". You can review the queue on the Recommendations page and look back via History and Change History.
- **When it matters / how experts use it:** The common expert default is all auto-apply off, with a manual weekly review. Exceptions some practitioners allow are low-risk hygiene items (removing conflicting negatives). Unexplained changes in match types, targets or partner settings should prompt a Change History check for "Recommendations" as the source.
- **Exceptions and failure modes:** Bid-target adjustments can quietly loosen efficiency. "Remove redundant keywords" can delete exact keywords that protect precedence (PLT-AUTO-003).
- **Signals in data:** Change History entries made by recommendations. New broad keywords nobody added. Search partners switched on.
- **Sources:** [About auto-apply recommendations](https://support.google.com/google-ads/answer/10279006) (checked 2026-10-13)

---

## E. Gemini tools in the Ads UI

### PLT-AUTO-029 · Ads Advisor became Ask Advisor and can now change settings with approval
- **Claim:** Google launched **Ads Advisor** (Gemini agent) to English accounts in late 2025 (announced 2025-11-12). At GML 2026 (2026-05-20) it became **Ask Advisor**, spanning Ads, Analytics, DV360 and Merchant Center. By September 2026 the Ads version could pause and rename campaigns, change budgets and locations, appeal disapprovals and update final URLs, "with your approval." It is in beta and not available in MCC accounts. **(changed 2025-11, 2026-05, 2026-09)**
- **Evidence type:** documented + trade press
- **Confidence:** high
- **How it works:** It answers questions from account data, generates reports and charts, suggests keywords and assets, and saves "business context". Google's own disclaimers say responses may be inaccurate. Billing, identity and policy outcomes must be verified in the account itself.
- **When it matters / how experts use it:** Useful for quick diagnostics and policy fixes. Its suggestions come from the same system that writes recommendations, so they carry the same bias toward expansion and should be checked like any recommendation. Under the July 2026 terms, inputs given to conversational tools may be used across Google Ads features.
- **Exceptions and failure modes:** No MCC support limits agency use. Changes it makes appear in Change History and need review.
- **Signals in data:** Change History entries from Ask Advisor sessions.
- **Sources:** [Ask Advisor in Google Ads (beta)](https://support.google.com/google-ads/answer/16574983) (checked 2026-10-13); [PPC Land: Ads and Analytics Advisors, 2025-11-12](https://ppc.land/google-launches-ads-and-analytics-advisors-for-all-english-accounts/) (checked 2026-10-13); [PPC Land: Ask Advisor, 2026-05-20](https://ppc.land/googles-ask-advisor-unifies-ads-analytics-and-commerce-in-one-ai-agent/) (checked 2026-10-13); [PPC News Feed: Ask Advisor actions, 2026-09-22](https://ppcnewsfeed.com/ppc-news/2026-09/google-ask-advisor-can-now-pause-campaigns-change-budgets-and-appeal-ads/) (checked 2026-10-13); [PPC Land: input-use terms, July 2026](https://ppc.land/google-ads-tells-advertisers-how-their-inputs-will-be-used-starting-july-2026/) (checked 2026-10-13)

---

## F. Ads in AI Overviews and AI Mode

### PLT-AUTO-030 · Ads inside AI Overviews need broad match or keywordless targeting; exact and phrase can only serve above or below
- **Claim:** Text and Shopping ads from Search, Shopping and PMax campaigns can show **within** AI Overviews, but only via **broad match or keywordless** targeting (AI Max, PMax, Shopping, DSA). Exact match can trigger ads **above or below** an AI Overview, not within it. In-AIO ads run in English only, in the markets the help page lists: US, Australia, Canada, India, Indonesia, Kenya, Malaysia, New Zealand, Nigeria, Pakistan, Philippines and Singapore. Ads above or below AI Overviews can serve in all 200+ AIO markets. Ads in sensitive verticals (finance, healthcare, alcohol, gambling, politics, adult) don't show in AI Overviews. There is **no opt-out and no direct targeting**. **(changed 2025-05: US desktop; later 2025: more countries)**
- **Evidence type:** documented + google-statement (Ads Liaison)
- **Confidence:** high
- **How it works:** Placement considers both the query and the AI Overview content, and uses the normal auction. An ad serves within or above/below, not both, in one auction. Ginny Marvin said AI Max is not required: plain broad match qualifies. Because exact match doesn't compete in the within-AIO auction, an exact keyword does not prevent a broad keyword from serving there.
- **When it matters / how experts use it:** Exact-only accounts are structurally absent from in-AIO placements. Whether that matters depends on whether those placements are incremental for you, which you cannot see (PLT-AUTO-032). Regulated verticals get no in-AIO exposure regardless.
- **Exceptions and failure modes:** The country list is from the help page as of this check and may expand.
- **Signals in data:** None directly (reported as Top ads). Indirectly: changes in broad-match top-of-page impressions after AIO expansions.
- **Sources:** [About ads and AI Overviews](https://support.google.com/google-ads/answer/16297775) (checked 2026-10-13); [TechWyse: Ginny Marvin PPC Chat Q&A, 2026-06-11](https://www.techwyse.com/?p=76611) (checked 2026-10-13); [SEL: ads in AI Overviews to desktop, 2025-05-21](https://searchengineland.com/google-ads-ai-overviews-ai-mode-desktop-455733) (checked 2026-10-13)

### PLT-AUTO-031 · Ads in AI Mode: tests since 2025 and new Gemini-built formats from GML 2026
- **Claim:** Google began testing ads in AI Mode in May 2025, eligible from PMax, Shopping and broad-match Search (including AI Max). At GML 2026 (2026-05-20) it announced **Conversational Discovery ads** and **Highlighted Answers** in AI Mode (testing), where Gemini builds creative and adds an "independent AI explainer". It also announced **AI-powered Shopping ads** and **Business Agent for Leads** (a Gemini brand agent replacing a lead form; US open beta; automotive, education and real estate first), plus a **Direct Offers** pilot (launched 2026-01). **(changed 2025-05, 2026-05)**
- **Evidence type:** google-statement + trade press
- **Confidence:** medium
- **How it works:** Google tells advertisers to build a "strong foundation" with AI Max for Search, AI Max for Shopping and PMax. Trade press reports these as practical eligibility requirements. In a healthcare AI Mode test, the first phase excluded ads with pinned assets or text disclaimers. In these formats Google generates part of the message seen next to your ad.
- **When it matters / how experts use it:** Advertisers who keep AI Max off or stay exact-only are opting out of these surfaces by default. Weigh that against control and compliance. For lead gen, Business Agent for Leads moves qualification into a Gemini chat, so lead-quality measurement becomes essential.
- **Exceptions and failure modes:** No advertiser performance data has been published. Google's only stat (75% of people report faster decisions with AI Mode) is a self-reported user survey.
- **Signals in data:** None separable (see PLT-AUTO-032).
- **Sources:** [Google blog: A new generation of ads for the AI era of Search, 2026-05-20](https://blog.google/products/ads-commerce/a-new-generation-of-ads-for-the-ai-era-of-search/) (checked 2026-10-13); [Google blog: AI brand discovery, 2025-05-21](https://blog.google/products/ads-commerce/google-search-ai-brand-discovery/) (checked 2026-10-13); [Browser Media: ads in AI Mode, 2026-06-11](https://browsermedia.agency/blog/ads-in-ai-mode-and-gml-2026-highlights/) (checked 2026-10-13); [Brainlabs: GML 2026](https://www.brainlabsdigital.com/google-marketing-live-2026/) (checked 2026-10-13)
- **Open questions:** Which AI Mode formats are live (not test) as of October 2026, and in which countries.

### PLT-AUTO-032 · There is no segmented reporting for AI Overviews or AI Mode ad placements
- **Claim:** Ads in AI Overviews are reported as **Top ads**, and Google says "segmented reporting for AI Search placements is not yet available." As of the June 2026 Liaison Q&A, advertisers should not expect granular placement data soon.
- **Evidence type:** documented + google-statement
- **Confidence:** high
- **How it works:** AIO and AI Mode impressions and clicks are mixed into top-of-page metrics. The channel performance report has no AI Overviews channel.
- **When it matters / how experts use it:** Any claim about how AIO or AI Mode ads perform for an account is inference. Practitioners use proxies: SERP sampling of their own head terms, shifts in broad-match versus exact-match top-of-page CTR, and before/after comparisons around rollout dates (weak evidence).
- **Exceptions and failure modes:** Proxy methods are confounded by seasonality and auction changes.
- **Signals in data:** Changes in top-of-page rate or CTR for broad/AI Max terms with no account change.
- **Sources:** [About ads and AI Overviews](https://support.google.com/google-ads/answer/16297775) (checked 2026-10-13); [TechWyse: Ginny Marvin PPC Chat Q&A](https://www.techwyse.com/?p=76611) (checked 2026-10-13); [About the channel performance report](https://support.google.com/google-ads/answer/16260130) (checked 2026-10-13)

---

## G. Strategic implications: what the advertiser still controls

### PLT-AUTO-033 · The advertiser's control surface is now inputs, constraints and tests
- **Claim:** With query selection, creative and landing pages automated, the advertiser's levers are: (1) **conversion goals and values** (what the bidder maximises), (2) **budgets and targets**, (3) **identical exact keywords** (precedence), (4) **exclusions** (negatives, brand lists, URL exclusions, audience exclusions, placement exclusions), (5) **creative and landing-page inputs** (the site content keywordless matching reads), (6) **component toggles** (search term matching per ad group, text customization, FUE), and (7) **experiments**.
- **Evidence type:** inference (synthesis of documented mechanics above)
- **Confidence:** medium-high
- **How it works:** Every automated component optimises toward the conversion signal within the constraints given. Bad signals (soft conversions, unvalued leads, duplicate counting) are amplified, not corrected. Google's own docs tie AI Max effectiveness to budget availability and value-based bidding.
- **When it matters / how experts use it:** The first diagnostic question for any automated campaign is "what conversion is it optimising toward, and is that conversion worth what the target implies?" before looking at queries or creative.
- **Exceptions and failure modes:** Some decisions are not controllable: AIO or AI Mode placement, Gemini-written explainers next to ads, channel allocation inside PMax, and the soft (non-binding) effect of signals, search themes and AI Brief matching guidelines.
- **Signals in data:** Platform conversions rising while CRM revenue is flat means the signal is wrong, not the automation.
- **Sources:** [AI Max how it works](https://support.google.com/google-ads/answer/15910187) (checked 2026-10-13); [AI Max FAQ](https://support.google.com/google-ads/answer/15913066) (checked 2026-10-13); [About keyword matching options](https://support.google.com/google-ads/answer/7478529) (checked 2026-10-13); [About audience signals](https://support.google.com/google-ads/answer/14530785) (checked 2026-10-13)

### PLT-AUTO-034 · How experienced managers keep control: common patterns (not universal rules)
- **Claim:** Recurring patterns among practitioners: separate brand from non-brand (brand campaign with exact plus brand inclusions; brand exclusions on PMax and non-brand AI Max); exact-match coverage of proven converters in well-funded campaigns; shared negative lists across Search and PMax; URL exclusions before FUE; test AI Max with Google's 50/50 experiment and judge on marginal CPA, ROAS or profit; auto-apply off; import offline or qualified conversions before broad expansion in lead gen.
- **Evidence type:** practitioner (supported by documented mechanics)
- **Confidence:** medium
- **How it works:** Each pattern uses a documented lever: precedence, brand lists, negatives, URL exclusions, experiments or conversion goals. Its value depends on the account's data volume and goals.
- **When it matters / how experts use it:** Use these patterns as default hypotheses in audits.
- **Exceptions and failure modes:** Over-segmentation thins data per campaign and can hurt Smart Bidding. Very small accounts may do better consolidated. Brand exclusion from PMax can lower PMax-reported efficiency without changing total profit, so judge at account level.
- **Signals in data:** Fragmented campaigns each with few conversions per month. Brand share of PMax conversions.
- **Sources:** [SEL: PMax vs Search overlap (Geddes)](https://searchengineland.com/performance-max-vs-search-campaigns-overlap-data-448788) (checked 2026-10-13); [SEL: AI Max early case studies](https://searchengineland.com/ai-max-early-case-studies-analysis-script-462706) (checked 2026-10-13); [PMG: DSA deprecation](https://www.pmg.com/insights-and-news/google-to-deprecate-dynamic-search-ads-campaigns-requiring-shift-to-ai-max) (checked 2026-10-13); [About brand settings](https://support.google.com/google-ads/answer/13721847) (checked 2026-10-13)

### PLT-AUTO-035 · Defaults are drifting toward "on": assume automation is enabled unless verified
- **Claim:** Since 2025 Google has repeatedly made automation the default or forced it: brand guidelines required in PMax (2025), AI Max default for new Search campaigns (by 2026-06), forced AI Max conversion of broad-match-setting and ACA campaigns (2026-09), DSA conversion (2027-02), and terms placing review duty for generated assets on advertisers (2026-07). **(changed 2025-2027)**
- **Evidence type:** inference from documented dated changes
- **Confidence:** high
- **How it works:** Each migration preserves the advertiser's ability to switch components off, but the starting state is "on". Inaction therefore means expansion.
- **When it matters / how experts use it:** AllFix should check each automation toggle at every audit and after every Google migration date. Don't assume last quarter's settings still hold.
- **Exceptions and failure modes:** Google has reversed or delayed timelines before (DSA delay, restoring DSA creation), so dates should be re-checked.
- **Signals in data:** Changes in Change History attributed to Google or system migrations. API migration timestamp fields.
- **Sources:** [Google blog: DSA upgrade to AI Max](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/) (checked 2026-10-13); [SEL: Google delays DSA migration](https://searchengineland.com/google-delays-dynamic-search-ads-migration-to-ai-max-480049) (checked 2026-10-13); [PPC Land: PMax 2025 rollouts](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) (checked 2026-10-13); [PPC Land: input-use terms](https://ppc.land/google-ads-tells-advertisers-how-their-inputs-will-be-used-starting-july-2026/) (checked 2026-10-13)

---

## Timeline of Google automation changes 2024-2026

| Date | Change | Source |
|---|---|---|
| 2024-06-26 | Brand exclusions extended to all match types and DSA. Negatives and search terms cover misspellings. Brand-inclusion recommendation for broad match. | [Query matching updates](https://support.google.com/google-ads/answer/15070437) |
| 2024-12-03 | Geddes/Adalysis study: 45% of PMax terms overlap Search | [SEL](https://searchengineland.com/performance-max-vs-search-campaigns-overlap-data-448788) |
| 2025-01 | PMax campaign-level negative keywords begin rolling out. Brand guidelines required for new UI PMax campaigns (2025-01-20). | [PPC Land](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) |
| 2025-03-11 | PMax negative keyword limit raised (10,000 reported; figures conflict) | [PPC Land](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) |
| 2025-04-30 | PMax channel performance reporting and fuller search terms announced (data from 2025-06-06) | [Channel report help](https://support.google.com/google-ads/answer/16260130) |
| 2025-05-06 | AI Max for Search announced. Global beta from late May 2025. | [Google blog](https://blog.google/products/ads-commerce/google-ai-max-for-search-campaigns/) |
| 2025-05-21 | Ads in AI Overviews expand to US desktop. Ads in AI Mode testing begins. | [Google blog](https://blog.google/products/ads-commerce/google-search-ai-brand-discovery/) |
| 2025-07-14 | PMax brand guidelines rollout complete (auto-migration by 2025-10-30) | [PPC Land](https://ppc.land/google-wraps-up-performance-max-feature-rollouts-in-2025/) |
| 2025-08-07 | PMax shared negative lists, 50 search themes, full search terms reporting, device and age targeting GA, new-customer "unknown" estimation | [PMax visibility and control](https://support.google.com/google-ads/answer/16451273) |
| 2025-11-12 | Ads Advisor and Analytics Advisor rolling out to English accounts | [PPC Land](https://ppc.land/google-launches-ads-and-analytics-advisors-for-all-english-accounts/) |
| 2026-01-09 | PMax: first-party audience exclusions, budget report, audience reporting, network segmentation in placements | [Google](https://business.google.com/us/accelerate/resources/articles/new-performance-max-steering-and-reporting-updates-coming-in-2026/) |
| 2026-01-26 | Auto-apply stops creating new RSAs | [Auto-apply help](https://support.google.com/google-ads/answer/10279006) |
| 2026-04-15 | DSA retirement into AI Max announced. ACA and broad-match-setting auto-upgrade set for 2026-09. | [Google blog](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/) |
| 2026-04-30 | AI Brief, AI Max for Shopping, Search campaigns for Travel, and text disclaimers announced | [PPC Land](https://ppc.land/ai-brief-google-lets-advertisers-steer-ai-max-in-plain-language/) |
| 2026-05-20 | GML 2026: Ask Advisor, AI Mode ad formats (Conversational Discovery, Highlighted Answers), Business Agent for Leads, AI-powered Shopping ads | [Google blog](https://blog.google/products/ads-commerce/a-new-generation-of-ads-for-the-ai-era-of-search/) |
| 2026-06-11/12 | DSA auto-migration delayed to 2027-02. DSA creation restored from 2026-06-15. AI Max default for new Search campaigns (Liaison). | [SEL](https://searchengineland.com/google-delays-dynamic-search-ads-migration-to-ai-max-480049) |
| 2026-06-23 | AI Max reporting docs revised: landing-page view default, "Other search terms" caveat | [PPC Land](https://ppc.land/google-quietly-rewrites-ai-max-reporting-docs-dsa-deadline-moves-to-2027/) |
| 2026-07-01 | New Google Ads terms: input use across features, advertiser duty to review generated assets | [PPC Land](https://ppc.land/google-ads-tells-advertisers-how-their-inputs-will-be-used-starting-july-2026/) |
| 2026-08-03 | Creation of new broad-match-setting and ACA configurations blocked (per dossier summarising Google developer post) | [Choice OMG](https://choice.marketing/research/google-ai-max-auto-upgrade/) |
| 2026-09-01 to 09-30 | Broad-match-setting and ACA campaigns auto-converted to AI Max | [Google blog](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/) |
| 2026-09 (reported 09-22) | Ask Advisor can pause campaigns, change budgets and locations, appeal ads, update URLs (with approval) | [Ask Advisor help](https://support.google.com/google-ads/answer/16574983) |
| 2027-01 (scheduled) | New DSA creation ends. Reminder about 2027-01-15. | [SEL](https://searchengineland.com/google-delays-dynamic-search-ads-migration-to-ai-max-480049) |
| 2027-02 (scheduled) | Remaining DSA campaigns auto-migrated to AI Max | [Google blog](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/) |

## Common mistakes and misleading metrics

- **Treating Google's "+14% conversions at similar CPA" as a forecast.** It is a non-retail average from Google's selected cohort, measured at campaign level. Independent data shows median CPA rising (smec +16%) and retail ROAS falling. Use your own 50/50 experiment (PLT-AUTO-007/008/010).
- **Summing AI Max search-term rows or filtering on match type "AI Max" to size its contribution.** That undercounts because "Other search terms" is excluded, and the API docs forbid summing views. Use the keywords-report totals and experiments (PLT-AUTO-006).
- **Reading optimisation score as a performance score.** It reaches 100% by dismissing everything, isn't used by Quality Score, and is tied to agency Partner status (PLT-AUTO-027).
- **Assuming audience signals or search themes restrict PMax.** They are additive hints. Only exclusions restrict (PLT-AUTO-020/021).
- **Assuming exact match protects a term everywhere.** It wins only for identical queries, only when the campaign is eligible (not budget-limited), and doesn't compete for in-AIO placements (PLT-AUTO-003/030).
- **Keeping pinned legal copy and assuming it shows.** Pins are ignored when FUE chooses another URL (PLT-AUTO-004).
- **Blended PMax ROAS including brand and returning customers.** It overstates incremental value. Use brand exclusions, new-customer reporting, or holdouts (PLT-AUTO-018/022).
- **Assuming last quarter's settings still hold.** Migrations in September 2026 and February 2027 flip defaults (PLT-AUTO-011/012/035).
- **Attributing performance changes to "AI Overviews".** There is no segmented reporting, so any such claim is inference (PLT-AUTO-032).
- **Counting soft lead-gen conversions as success after enabling AI Max.** Expansion optimises toward whatever is counted. Check lead-to-sale rates (PLT-AUTO-009).

## Unresolved questions

1. No randomised, multi-account AI Max study (experiment-arm based) has been published. Existing independent evidence is observational, small, or retail-only. What is the true marginal CPA of AI Max traffic by vertical?
2. Exact September 2026 migration behaviour for Manual CPC campaigns in the broad-match-setting cohort, and for campaigns in both cohorts. The Google developer post (2026-08-12) could not be opened.
3. Does AI Brief's "matching guidelines" measurably change query mix, and how closely do previews match live serving? Is it generally available beyond English as of October 2026?
4. How should advertisers choose between AI Max for Shopping and PMax for retail? No Google guidance has been found.
5. Which AI Mode ad formats are live (not testing) as of October 2026, in which markets, and will any segmented reporting arrive?
6. Current limits and scope of account-level negative keywords and PMax asset-automation opt-outs: help pages not opened this session.
7. Smart campaigns: any 2025-2026 deprecation or migration plan. Not verified this session.
8. Whether forced AI Max defaults change auction pressure (more advertisers bidding broad on the same long-tail queries), which would raise CPCs for exact-only advertisers. Hypothesis, untested.
