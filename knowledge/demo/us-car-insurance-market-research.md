---
area: market
topic: US car insurance search advertising, new-niche research demonstration
checked: 2026-10-13
owner: research
---
# US Car Insurance Search Advertising: Pre-Launch Market Research (Demonstration)

This document shows how an expert PPC strategist researches a new niche (US auto insurance lead generation and direct carrier search) before spending a dollar and with no account history. The single most important idea: in car insurance the price of a click is set by the bidders with the highest lifetime value and the deepest budgets (national carriers and lead marketplaces that resell one visitor to several buyers), so a new entrant cannot win by outbidding them on head terms. It wins, if at all, by finding situations, places, hours and angles where its own value per click is higher than theirs or where they are not present.

## How to read the labels

Every material claim carries one label:

- **[Verified]** I opened the source on 2026-10-13 and the claim is stated there. A verified claim can still be a company's own marketing statement; where that matters I say so.
- **[Estimate]** A third-party figure (vendor benchmark, survey) or my own calculation. The basis is shown.
- **[Hypothesis]** Plausible reasoning from verified facts, not tested. It becomes a test in section 6.
- **[Unknown]** Cannot be established without an ad account, a client, or data I could not access.
- **[Unverified background]** Something I believe from prior knowledge but could not open a source for in this session (my web search and fetch budgets ran out). Treat as needing confirmation before use.

Practitioner benchmarks are priors, not rules. Competitor bids, budgets, margins and motives are never observable; anything said about them is inference.

**Research limits in this session.** I could not render the Google Ads Transparency Center (the page loads its ad data with JavaScript and my fetch tool saw only the navigation), could not access Google Trends (blocked to automated fetch), could not open Google Keyword Planner (needs an account), could not run live search results pages, and could not open NerdWallet or the Insurance Information Institute. Competitor pages described below are their main organic pages, not necessarily the landing pages their ads point to.

---

## 1. Business framing: who could advertise, and what a click is worth to each

### 1.1 Three advertiser types

| Advertiser type | How it makes money | What it needs from a click | Examples observed |
|---|---|---|---|
| Direct carrier | Underwriting profit plus investment income on premiums, over the whole life of the policy | A bound policy from a customer it is happy to insure at its price | Progressive, GEICO, State Farm, Allstate |
| Independent or captive agency | Commission from the carrier on the premium, first year and renewals | A quote request or a phone call it can turn into a sale, from a customer at least one of its carriers will accept | Local agencies such as Blake Insurance Group (Tucson, AZ) |
| Lead-gen or comparison marketplace | Fees from carriers and agents for each referral (a click, call or lead), sometimes commission as a licensed agency | A visitor it can monetise, ideally several times over, at more than the cost of acquiring them | EverQuote, MediaAlpha (platform), The Zebra, Insurify, NerdWallet |

- **[Verified]** MediaAlpha's 2025 10-K: "We generate revenue by earning a fee for each Consumer Referral sold on our platform", payable "upon a qualifying consumer action, such as a click, call or lead". In 2025 clicks were 90.1% of transaction value, calls 4.2%, leads 5.7%. P&C insurance was $1.9 billion of $2.2 billion transaction value and 90.1% of revenue.
- **[Verified]** EverQuote's 2025 10-K: automotive insurance providers generated 91% of revenue in 2025 (89% in 2024); its two largest customers were 38% and 11% of revenue. Referrals are delivered as clicks, data or calls.
- **[Verified]** The Zebra says it earns commission from insurers with no fee to the buyer, and that its agents are licensed in all 50 states. Insurify describes itself as a licensed agency in 50 states.

**Why this matters for strategy [Hypothesis]:** the three types compete in the same auction but value the same click differently. A carrier values a click by the lifetime profit of the policy. An agency values it by lifetime commission, a fraction of premium. A marketplace values it by how many referrals it can sell from one visit. Any of the three can be the highest bidder on a given query, depending on the searcher's profile.

### 1.2 The reasoning chain for click value

The general formula every advertiser is implicitly solving:

> Maximum sensible CPC = (value of one customer) x (share of that value you are willing to spend on acquisition) x (probability a click becomes a customer)

where probability a click becomes a customer = click-to-quote-start rate x quote-start-to-completed-quote rate x completed-quote-to-sale rate.

Inputs I could source:

| Input | Figure | Label and basis |
|---|---|---|
| Average annual full-coverage premium | $2,242 per year; liability-only $1,183 | **[Estimate]** Insurify, page updated 2026-09-30, from its own quote data plus Quadrant estimates. The page itself has internal inconsistencies (it also gives $1,713 and $2,144 as averages), so treat as a range, roughly $2,100 to $2,250 for full coverage. |
| Premium of people who actually switch | Median above $3,200 | **[Verified]** J.D. Power Q1 2026 LIST figure as reported by Repairer Driven News (2026-05-14). Switchers skew to higher premiums, which matters: the people shopping are worth more than the average policy. |
| Premium uplift for risk events | Full coverage roughly +$924/yr after a speeding ticket, +$1,020/yr after an at-fault accident, +$1,404/yr after a DUI | **[Estimate]** Insurify table (same page). The page's own percentages do not reconcile with its table, so use direction and rough size only. |
| Agency commission | Independent agencies about 12-15% new business and 10-12% renewal; captive about 8-12% new and 4-10% renewal | **[Estimate, low confidence]** Firefly Agency marketing page, no methodology, not auto-specific. Real rates are in each agency's carrier contracts. |
| Annual switching rate | J.D. Power quarterly switching 4.2% (Q1 2026) and 4.5% (Q2 2026) | **[Verified]** (Repairer Driven News 2026-05-14; Insurance Edge 2026-08-10). |
| Implied average customer tenure | Roughly 5 to 6 years | **[Estimate]** My calculation: four quarters at about 4.2-4.5% gives about 17-18% of customers switching per year; 1 / 0.17 is about 5.9 years. This is crude: quarterly rates do not add exactly, switching is concentrated in a minority who switch repeatedly, and new customers acquired through price shopping probably churn faster than the average. A shopper-acquired customer's tenure is likely shorter [Hypothesis]. |
| Carrier advertising scale | Progressive advertising costs $5,133 million in 2025 vs $4,003 million in 2024 | **[Verified]** Progressive 2025 10-K, Note 1. |
| Carrier underwriting margin | Unknown per carrier. Progressive has long publicly targeted a 96 combined ratio (about 4 cents profit per premium dollar before investment income) | **[Unverified background]** not re-opened this session. |

**Worked chain for each advertiser type.** Numbers below marked "assumption" are placeholders to show the arithmetic, not facts.

*Agency.* First-year commission on a $2,100-$2,250 policy at 12-15% is about $250-$340 [Estimate, calculated]. Renewal commission at 10-12% is about $210-$270 a year [Estimate]. If the customer stays 3 years in total (assumption, deliberately below the 5-6 year average because shoppers churn more), lifetime commission is roughly $670-$880 [Estimate]. If the agency is willing to spend one third of that on acquisition (assumption), its target cost per sale is roughly $220-$290. If 10% of quote requests become sales (assumption) and 8% of clicks become quote requests (assumption), each click is worth about $1.80-$2.30. Change either rate and the answer moves proportionally: at 20% close and 12% quote rate the same agency can pay about $5.30-$7.00. **The lesson is the shape, not the number:** an agency's affordable CPC is very sensitive to its close rate, which only the client can supply [Unknown].

*Carrier.* A carrier's value per customer is the margin on several years of premium plus investment income on the float, net of the risk that price-shoppers file more claims. With a switcher premium above $3,200 and multi-year tenure, the gross premium flowing from one acquired customer is in the thousands of dollars [Estimate]. The share of that the carrier can spend on acquisition depends on margin and on its current appetite for growth [Unknown]. MediaAlpha's 10-K explains the appetite mechanism: in "soft" markets carriers focus on acquiring customers; in "hard" markets "they tend to prioritize profitability over growth" [Verified]. Carriers also bid by segment: a carrier may value a clean-record homeowner with two cars far above a single young renter, and can express that through audience, location and query bidding [Hypothesis].

*Lead-gen marketplace.* Value per visitor = sum of the fees from every referral sold from that visit. On a click listing a single visitor can click several carriers, each paying [Verified that fees are per click; number of clicks per visitor Unknown]. This is why a marketplace can sometimes bid more than any single carrier for the same visitor: it is aggregating several buyers' willingness to pay [Hypothesis, but it follows directly from the verified fee model]. It also explains the "arbitrage" business: buy a search click, sell two or three onward clicks.

**What this section can and cannot establish.** It establishes the structure of value and which inputs drive it. It cannot establish an actual affordable CPC for any specific advertiser: margins, close rates, carrier contracts and tenure for that advertiser's customers are [Unknown] without a client.

---

## 2. Market and demand

### 2.1 Market structure

**[Verified]** NAIC 2025 market share report, Total Private Passenger Auto, preliminary (about 98.25% of filings received as of 2026-03-18). Industry direct premiums written: about $371.0 billion.

| Rank | Group | Share |
|---|---|---|
| 1 | State Farm | 18.64% |
| 2 | Progressive | 18.60% |
| 3 | Berkshire Hathaway (GEICO) | 11.56% |
| 4 | Allstate | 10.15% |
| 5 | USAA | 6.19% |
| 6 | Farmers | 3.57% |
| 7 | Liberty Mutual | 2.81% |
| 8 | Travelers | 1.93% |
| 9 | Auto Club Enterprises | 1.90% |
| 10 | American Family | 1.53% |

The top four hold 58.95% and the top ten about 76.9% (my sum) [Estimate, calculated from verified figures]. Progressive's page claims it is the nation's largest auto insurer based on S&P Global Q1 2026 written premium [Verified as Progressive's claim]; the NAIC full-year 2025 table has State Farm marginally ahead. Both can be true for different periods.

**Implication [Hypothesis]:** the brands with the biggest budgets are also the brands searchers already know. Brand recognition lifts click-through rate, which Google rewards in Ad Rank, so these advertisers get more for each bid dollar than an unknown entrant does.

### 2.2 Prices and the underwriting cycle in 2026

- **[Verified]** BLS CPI, August 2026: motor vehicle insurance index down 5.1% over 12 months (seasonally adjusted monthly changes: June -2.0%, July -0.3%, August -0.8%).
- **[Verified]** LexisNexis Q1 2026 (via Repairer Driven News): 35% of rate revisions were decreases, 39% increases, 26% neutral; aggregate change -1.1%. Among top 25 carriers, 42% of revisions were decreases.
- **[Estimate]** Insurify mid-2026 report (via Autobody News 2026-08-19): national full-coverage average rose 1% in H1 2026 to $2,237, with large state differences (for example Connecticut projected +15%). National CPI falling while some states rise is plausible because the measures differ.
- **[Verified]** Progressive's advertising rose about 28% in 2025 (from $4.0bn to $5.1bn).

**Interpretation [Hypothesis]:** 2026 looks like a softening market: carriers that restored profitability after 2022-2023 are cutting rates and spending more to grow. EverQuote's 10-K says carriers cut spending in 2022-2023 under rising claims and inflation and that spending has improved since, though not evenly across carriers [Verified]. For a new advertiser this means the auction is probably more expensive now than it was in 2023, and could get cheaper quickly if claims costs rise again (Autobody News notes repair parts costs are rising). Ad costs in this niche follow the insurance cycle, not just Google.

### 2.3 Shopping behaviour

- **[Verified]** J.D. Power 2026 U.S. Insurance Shopping Study (fielded January 2025 to January 2026, 12,437 customers who requested a quote): shopping fell from 57% to 53% year over year, still high historically; shoppers received an average of 3.5 quotes, the highest in the study's history; 48% of new auto policies were bought digitally, up from 36% five years earlier.
- **[Verified]** LexisNexis: 47.3% of policies in force had been shopped in the prior 12 months at end of Q1 2026, the highest since tracking began in 2020. Q1 2026 shopping growth by channel: direct +9.4%, exclusive agent +5.6%, independent agent -7.9%, non-standard -5.8%.
- **[Verified]** J.D. Power 2026 U.S. Auto Insurance Study (via Repairer Driven News 2026-06-11): 21% of consumers had a "forced cross-channel interaction"; once engaged, agents resolved 91% of cross-channel inquiries, while website follow-ups left 66% unresolved; 46% used multiple channels in the past year.

**Implications [Hypothesis]:** shoppers compare several quotes, so being one of the 3-4 quotes a person gets matters more than being the only one. Direct is the growing channel. But a meaningful minority hit a wall online and need a human, which is an opening for an agency that answers the phone.

### 2.4 Seasonality

- **[Verified]** MediaAlpha 10-K: P&C is "characterized by seasonal weakness during our fourth quarter" due to lower buyer budgets and fewer consumer referrals over the holidays, and "During our first quarter, our P&C insurance vertical typically exhibits seasonal strength."
- **[Verified]** J.D. Power monthly pattern (Q1 2026): shopping peaked in February 2026 and dropped about a point in March. Quarterly shopping was 13.6% in Q1 and 12.6% in Q2 2026.
- **[Unknown]** Search-volume seasonality by month and by cluster. Google Trends could not be accessed in this session and Keyword Planner needs an account. Both should be pulled before launch, by state.
- **[Hypothesis]** Q1 strength may relate to new-year budgets at carriers, tax-refund season and car purchases; Q4 weakness on the buyer side may mean cheaper clicks in late November and December for an advertiser whose own demand holds up. These are testable, not facts.

Note the two layers of seasonality: consumer demand (how many people search) and buyer demand (how much carriers and marketplaces want to pay). Click prices depend on both.

### 2.5 Regulation

**State licensing.** [Unverified background] Anyone who sells, solicits or negotiates insurance in a state needs a producer license there, and agencies need entity licenses; pure advertising and referral without discussing coverage terms is treated differently state by state. **[Verified as practice]** The comparison sites and agency inspected all display licensing: The Zebra ("licensed to serve customers in all 50 states"), Insurify (licensed agency in 50 states), Blake Insurance Group (shows NPN and agent license numbers). For an AllFix client, the licensing footprint defines the geography it can target: an agency licensed in three states must not buy clicks in the other 47.

**TCPA and lead consent, status as of 2026-10-13:**

- **[Verified]** The FCC's "one-to-one consent" rule (consent may name only one identified seller, closing the "lead generator loophole") was due to take effect 27 January 2025. The Eleventh Circuit vacated it in *Insurance Marketing Coalition v. FCC*, 127 F.4th 303 (11th Cir. 2025), holding the FCC exceeded its statutory authority; it also vacated the requirement that calls be "logically and topically associated" with the consent interaction (Morrison Foerster; Goodwin).
- **[Verified]** The FCC did not seek further review and issued a final rule formally removing the one-to-one provision from 47 CFR 64.1200(f) (Goodwin, 15 September 2025). The court read prior express written consent to require that consumers get "clear and unmistakable" information that calls may come from various sellers.
- **[Verified]** The separate "revoke-all" rule (47 CFR 64.1200(a)(10), from a February 2024 FCC order: once a consumer revokes consent for one type of message, the caller must stop robocalls and robotexts generally, absent an exemption) was delayed from April 2025 to April 2026, and then by an FCC order of 6 January 2026 (DA-26-12) to **31 January 2027** (Burr & Forman; Brownstein).
- **[Unverified background]** Other revocation provisions (honouring opt-outs made by any reasonable means, within 10 business days) took effect 11 April 2025. In June 2025 the US Supreme Court (*McLaughlin Chiropractic v. McKesson*) held that district courts are not bound by FCC interpretations of the TCPA, which increases legal uncertainty in both directions. Several states have their own "mini-TCPA" laws (Florida and Oklahoma are commonly cited). I could not open sources for these in this session.
- **[Verified]** EverQuote's 10-K notes TCPA fines "of up to $1,500 per violation". MediaAlpha's 10-K records a $45.0 million FTC settlement whose injunctive terms hurt its under-65 health insurance business: a reminder that regulators act on lead-gen practices even when a specific rule is vacated.
- **[Hypothesis]** Many large lead buyers kept one-to-one style consent as a contractual requirement after the rule fell, because of litigation risk and state law. This must be checked with each buyer; it changes form design and lead value.

**Google Ads policy.** **[Verified]** Google's Financial services policy requires verification "in some locations" and disclosure of physical address and fees, but the opened page does not mention insurance specifically or state whether US insurance advertisers must verify. **[Unknown]** Whether a given US insurance advertiser will be asked to complete verification; check in the account at setup.

### 2.6 Why insurance CPCs are among the highest

**[Verified]** Google's Ad Rank uses the bid, ad and landing-page quality, Ad Rank thresholds, auction competitiveness, search context and expected impact of assets; advertisers usually pay less than their maximum bid, and higher quality "can often lead to lower CPCs" (Google Ads Help).

Putting that mechanism together with the verified market facts, the reasons are [Inference, high confidence on direction]:

1. **High lifetime value.** Policies renew for years and premiums are in the thousands; one acquired customer can justify a large acquisition cost.
2. **Very large, data-rich bidders.** Progressive alone spent $5.1bn on advertising in 2025 and can model customer value by segment.
3. **Resale economics.** Marketplaces earn several fees per visitor, so they can bid above any single buyer.
4. **Commodity product with price-led switching.** Many advertisers can serve every searcher, so few queries are uncontested.
5. **Cycle.** In a soft market (2026 evidence above) carriers chase growth, adding bid pressure.

**Benchmarks and their limits.** **[Estimate]** LocaliQ/WordStream 2026 search benchmarks (updated 2026-06-01) list "Finance & Insurance" at average CPC $3.39, CTR 9.83%, conversion rate 2.64%, cost per lead $74.44. The 2024 WordStream edition (April 2023 to March 2024, about 18,000 US campaigns, medians not means) gave $3.00 CPC and $75.94 CPL. **These are not auto-insurance CPCs.** They pool banks, advisers, local agencies and others; they come only from LocaliQ/WordStream's own customers (mostly small and local businesses, a hypothesis about their client base); they are medians, which hide the expensive head terms; and they do not separate head terms from long tail. Use them as a floor for small local accounts, never as an estimate of what "car insurance quotes" costs. Real auction prices for specific keywords are **[Unknown]** until Keyword Planner is pulled in an account (and even its top-of-page bid ranges are Google's estimates, not prices).

---

## 3. Search behaviour: intent clusters

Volumes and CPCs per cluster are **[Unknown]** in this research: Keyword Planner was not available and I found no third-party keyword data I could open and trust. Values and competition levels below are **[Hypothesis]** reasoned from the value chain in section 1 and the competitor pages in section 4. They are the things the first test is designed to check.

| Cluster | Example queries | What the searcher wants | Likely value per click | Likely competition | Natural fit |
|---|---|---|---|---|---|
| Price / quote (head) | car insurance quotes, auto insurance quote, compare car insurance | A number, fast, from several options | High (broad mix of profiles, high intent) | Extreme: every carrier and marketplace | Carriers, large marketplaces |
| Cheap / minimum coverage | cheapest car insurance, liability only insurance, state minimum car insurance | Lowest legal price; often budget-constrained | Lower per policy (liability-only around half full-coverage premium [Estimate, Insurify]), but high intent | High: non-standard carriers and marketplaces | Non-standard carriers, marketplaces, agencies with non-standard markets |
| SR-22 / after DUI / license reinstatement | sr22 insurance, insurance after dui, cheap sr22 near me | A filing so they can drive legally again; urgent; often rejected elsewhere | Premium higher (DUI adds about $1,400/yr [Estimate]), many carriers decline; value depends on finding a carrier that accepts | Medium: fewer standard carriers want them | Agencies with non-standard carrier access; specialist marketplaces |
| After accident / tickets / high-risk | insurance after accident, high risk auto insurance, insurance with bad driving record | Someone who will insure them at a bearable price | Similar to SR-22 | Medium | Agencies, non-standard carriers |
| New / young driver | car insurance for 18 year old, first time car insurance, add teen to policy | Understanding, cost, often a parent doing research | Mixed: teen added to a parent's policy is high value to the parent's carrier; standalone young driver is high premium and high risk | High on "teen" terms | Carriers (retention play), agencies |
| No prior insurance / lapse | car insurance with no prior insurance, insurance after lapse | Coverage without a penalty they fear | Medium; lapse raises price | Medium | Agencies, marketplaces |
| Non-owner | non owner car insurance | Liability cover without owning a car (often for SR-22 or borrowed cars) | Lower premium, but niche and often paired with SR-22 | Low to medium | Agencies |
| Switching / renewal shock | my car insurance went up, switch car insurance, cancel car insurance | Relief from a renewal increase | High: these are motivated switchers (median switcher premium above $3,200 [Verified, J.D. Power]) | High | Carriers and marketplaces using "switch and save" angles |
| Brand + compare | progressive vs geico, state farm quote, geico vs allstate | Validation or comparison of known brands | Brand-own queries: very high to that brand, low to others. "vs" queries: research stage | Brand owners dominate their own terms; marketplaces bid on "vs" | Brand owners; comparison publishers |
| Local agent | car insurance agent near me, insurance agency [city] | A human, local, often for complex situations or bundling | Medium to high for agencies; lower for direct carriers that do not use agents | Medium; captive agents (State Farm, Allstate, Farmers) are heavily local | Independent and captive agencies |
| Bundle | home and auto insurance bundle | Saving by combining policies; usually homeowners | Very high (multi-policy households churn less [Hypothesis]) | High | Carriers and agencies |
| Specialty vehicle or use | rideshare insurance, classic car insurance, sr22 for motorcycle | Coverage for a non-standard use | Varies; specialist products | Low to medium per niche | Specialists |
| Spanish-language | seguro de carro barato, aseguranza cerca de mi | Same intents, in Spanish; often local and phone-first | Similar to English equivalents | Unknown, possibly lower [Hypothesis] | Agencies with Spanish-speaking staff |

Notes on reading this table:

- **Situational clusters are where the formula in 1.2 diverges between advertisers.** A standard carrier that will decline most SR-22 drivers has low value for those clicks. An agency with a non-standard carrier appointment may have high value. Divergent value is where a smaller advertiser can win an auction [Hypothesis].
- **"Cheap" does not mean low value.** It means price-sensitive and probably shorter tenure. Whether it is worth buying depends on the advertiser's carriers [Unknown].
- **Informational queries** (what is full coverage, how much is car insurance) are research stage; they suit content and remarketing more than direct lead buying [Practitioner prior].

---

## 4. Results-page and competitor reality

### 4.1 What could and could not be inspected

- **Not inspected:** live Google results pages (no search-results tool), ad copy in the Google Ads Transparency Center (page is JavaScript-rendered; my fetch returned only navigation), NerdWallet (page would not load for the fetch tool). A strategist with a browser should open the Transparency Center for progressive.com, geico.com, thezebra.com, insurify.com, everquote.com and two or three local agencies in the target state, filter to United States and Search, and record ad text, final URLs and how long ads have run.
- **Inspected [Verified, 2026-10-13]:** organic pages of Progressive (auto page), GEICO (auto page), The Zebra (home), EverQuote (home), Insurify (home), and a local agency (Blake Insurance Group, Tucson AZ, online auto quote page). These may differ from ad landing pages.
- **Never observable:** competitors' bids, budgets, target costs, margins, impression share, conversion rates, or why they bid as they do. Auction Insights (inside an account) will later show overlap and outranking rates for queries the client also enters, but still not bids.

### 4.2 What competitors say, and the angle behind it

| Competitor | Headline offer (verified wording or close paraphrase) | Angles |
|---|---|---|
| Progressive | "Join over 37 million drivers who trust the nation's largest auto insurer" (footnoted to S&P Global Q1 2026). "Drivers save an average of $975 when they switch" (footnoted: survey of new customers who saved, June 2025 to May 2026). Separate averages for switchers from Allstate ($1,019), GEICO ($759) and State Farm ($792). Bundle $1,099; Snapshot $328; "Name Your Price". ZIP field, "Get a quote", 24/7 phone line. Notes "Prices vary based on how you buy." | Scale and trust; price anchor with a specific dollar figure; competitor-specific switching savings; bundle; budget-first tool; omnichannel (online, phone, agent) |
| GEICO | "Get a personalized quote in minutes"; "Drivers who switch to GEICO can save over $900 a year" (no footnote visible to my fetch); ZIP field; bundle, DriveEasy, discounts; app; "For nine decades". Some figures rendered as "0" because they load by script; this is a tool limitation, not GEICO's error. | Speed; price anchor; heritage; app and self-service |
| The Zebra | "Instantly Compare Insurance Quotes"; works with "100+ companies"; "Over 74 million quotes"; "No junk mail. No spam calls. Free quotes."; licensed agents in 50 states; no specific savings figure. Estimator asks age range first, then ZIP. | Comparison breadth; anti-spam reassurance; licensed human help |
| EverQuote | "The fast, free, and easy way to shop for insurance"; "5 mins"; "$591" average savings reported by users (self-reported, no method); "30+ licensed carriers compared on every quote"; ZIP field. Consent wording was not visible on the fetched home page. | Speed; ease; modest savings anchor; marketplace breadth |
| Insurify | "Compare Car Insurance Quotes in Real Time & Save"; "2 minutes"; "$1,100 average potential savings" (footnoted: initial quotes of 151,494 customers, "do not reflect typical results"); "spam-free. We only call when you ask us to"; no phone number required since 2024; AI policy upload; Trustpilot 4.7. Inconsistent carrier counts (120+ vs 500+). | Real-time comparison; large savings anchor; privacy; AI features; review volume |
| Blake Insurance Group (local agency) | "Compare Car Insurance in Minutes, Real Discounts, Local Rates & 'Near Me' Options"; licensed agents who work for the customer, not one carrier; phone number in header, hero, "Text or Call" button and footer; NPN shown; "No Spam"; state "near me" sections (AZ, TX, FL, OH, NC). | Local and human; independence (multiple carriers); phone-first; licensing as trust |

### 4.3 Patterns and gaps

- **Everyone anchors on price** with a dollar savings figure ($591 to $1,100). Savings claims are self-selected averages (only people who saved) and the footnotes say so [Verified]. A new entrant cannot credibly beat these numbers and should not try [Hypothesis].
- **Everyone promises speed** ("minutes", "2 minutes", "5 mins").
- **Comparison sites now advertise against spam.** The Zebra, Insurify and the local agency all promise no spam calls or no selling data. This tells us the category's reputation for lead resale is a real consumer fear [Hypothesis, strongly suggested by the convergence].
- **Big brands bury the human.** Progressive and GEICO show phone numbers and agent finders, but lead with self-service. Given J.D. Power's finding that 21% hit a forced channel switch and agents resolve 91% of such inquiries once engaged [Verified], "talk to a licensed person now" is an under-used lead angle for an agency [Hypothesis].
- **Situational help is mostly absent from the headline offers.** None of the inspected main pages lead with SR-22, lapse, non-owner or high-risk situations. Carriers have SR-22 content deeper in their sites [Unverified background; the Progressive SR-22 page did not load].

---

## 5. Website and user journey

### 5.1 What a winning landing page must do, by cluster [Hypothesis, built from section 3 and 4 evidence]

| Cluster | Page must do | Avoid |
|---|---|---|
| Price / quote head terms | Start the quote above the fold with one field (ZIP), state the time it takes honestly, show carriers or a credible price range, show licensing and privacy promise | Long copy before the form; a generic home page |
| Cheap / minimum | Explain the state minimum in one line for the visitor's state, show that liability-only is available, give the fastest path to a price | Implying a specific price you cannot honour |
| SR-22 / DUI / high-risk | Say plainly "we can file your SR-22" and in which states; explain what happens next and how fast the filing reaches the state; offer a phone call immediately; reassure that being declined elsewhere is normal | Pages that look like the standard funnel; any shaming tone |
| Switching / renewal shock | Acknowledge the increase; ask for current premium and renewal date; promise a side-by-side comparison | Vague "save money" with no mechanism |
| Local agent | Name the city or area, show real people with licence numbers, office hours, address, reviews, click-to-call | Stock photos; national-sounding copy |
| Bundle | Ask "own or rent?" early; show which carriers bundle; set expectation that a home quote needs more data | A form that ignores the home side |
| Spanish | Full Spanish page and Spanish-speaking phone line during stated hours | Machine-translated page with an English-only phone line |

### 5.2 Friction points in quote forms [Hypothesis unless marked]

- **Length.** A full auto quote needs drivers, dates of birth, vehicles (often VIN), garaging address, driving history, prior insurance and coverage choices [Verified: Blake's "have ready" list]. Each extra screen loses people. Progressive-style progressive disclosure (ZIP first) is the norm.
- **Phone number and consent.** Asking for a phone number early, with consent language for several sellers, raises fear of spam calls. Insurify removed the phone requirement in 2024 [Verified as its claim]. For an agency the trade-off is real: the phone is its best closing tool, so the test is whether asking later (after showing value) yields more completed quotes.
- **Credit and licence-number anxiety.** Blake addresses "does quoting affect my credit" in an FAQ [Verified]; this is a known concern worth answering on the page.
- **Bridge pages.** Lead-gen sites often send a visitor through to carrier listings. For an advertiser buying clicks, every extra hop leaks people.
- **Channel break.** If the visitor cannot finish online and has to call, the call must be answered. A page that promotes the phone outside staffed hours wastes the click.

### 5.3 Message match

The query, the ad and the first screen of the page should say the same thing. "sr22 insurance [state]" should land on "SR-22 filing in [state], filed today" with a phone number, not on a generic quote form. This affects conversion directly and affects Ad Rank through landing-page experience [Verified that landing-page quality is an Ad Rank input; size of effect Unknown].

---

## 6. Strategy

The strategy depends on which advertiser type the client is. I write it for the most likely AllFix client, a **small or mid-size independent agency or a small lead-gen operator**, and note where a carrier would differ.

### 6.1 Where a new entrant could realistically win [Hypothesis]

1. **Situations where its value per click is higher than the giants'.** SR-22, DUI, lapse, non-owner, high-risk, newly licensed adults, drivers new to the US. Standard carriers value many of these searchers less; an agency with non-standard carrier appointments values them more. The win condition is that the client can actually place these drivers, which only the client can confirm [Unknown].
2. **"A licensed human, now".** Competitors lead with self-service and anti-spam promises. An agency can lead with "talk to a licensed agent in [state] now, we will not sell your number", run call-focused ads during staffed hours, and rely on the J.D. Power evidence that agents resolve channel-break inquiries [Verified evidence, Hypothesis for ad effect].
3. **Geography.** Target only states where the client is licensed and has competitive carriers, and within those, areas where it has an office or reviews. LexisNexis shows shopping growth differs sharply by state (New York, California, Wyoming, Louisiana at or above 10% in Q1 2026) [Verified], and Insurify shows price changes differ by state [Estimate]. Rising-price states produce renewal-shock searchers.
4. **Dayparting.** If the conversion that matters is a conversation, buy clicks mainly when calls are answered. Off-hours clicks can still be bought if the form path converts, but they should be valued lower until data shows otherwise.
5. **Spanish-language search** if the client has Spanish-speaking licensed staff. Competition is unknown and possibly thinner [Hypothesis].
6. **Seasonal timing.** If MediaAlpha's Q4 buyer weakness reflects lower bidding [Verified that it is weaker for them; effect on CPC Unknown], Q4 could be a cheaper window for an advertiser whose own demand holds up.

### 6.2 Where it should not compete (at first)

- **Head terms nationally** ("car insurance", "car insurance quotes", "cheap car insurance" on broad match across all states). These are where the five reasons in 2.6 apply most strongly, and a new account with no history has no quality or data advantage [Inference].
- **Competitor brand terms** ("geico quote"). The searcher wants that brand; conversion is likely poor; trademark rules restrict ad text [Unverified background on the specific trademark policy wording].
- **States outside the licensing footprint**, without exception (legal, not strategic).
- **Display and search-partner traffic** in the first test, until the core search signal is clean [Practitioner prior].

For a **carrier** the picture flips: head terms and brand defence are core, and the job is segment-level bidding using its own customer-value model. For a **lead-gen marketplace** the job is buying where the resale value per visitor exceeds the click price, which requires its buyer price tables [Unknown].

### 6.3 First-test plan

**Step 0: measure before spending (no budget).**
- Pull Keyword Planner for the target state(s) for each cluster in section 3: volumes and top-of-page bid ranges, monthly over 24 months for seasonality. Record as Google estimates, dated.
- Pull Google Trends by state for the head term and two or three situational terms.
- Open the Ads Transparency Center for the competitors in 4.2 and for local agencies in the target cities.
- Get from the client: licensed states, carrier appointments (especially non-standard), staffed phone hours and languages, current close rate on inbound calls and forms, average commission per policy, and how they will report sales back (CRM or spreadsheet). Without the close rate and the sale feedback, the test can only measure leads, not value.

**Step 1: calculate the affordable CPC (budget as reasoning, not a number).** Using the chain in 1.2 with the client's real commission, close rate and an assumed quote rate, compute the maximum CPC for each cluster. Compare to Keyword Planner's bid ranges. Clusters where the affordable CPC is well below the low end of Google's range are dropped before launch. Clusters where it sits inside or above the range go into the test.

**Step 2: size the test budget from the decision you need to make.** The question for each cluster is "does it produce sales at an acceptable cost?". To answer that you need enough leads to see a close rate, not just a click-through rate. So:

> Test budget per cluster = (number of leads needed to judge it) x (expected cost per lead), where expected cost per lead = expected CPC / expected click-to-lead rate.

The number of leads needed is a practitioner judgement, commonly a few dozen per cluster before reading conversion-to-sale, and it fails when close rates are low (you then need more) [Practitioner prior, not a platform rule]. If that budget is unaffordable across all clusters, test fewer clusters, not all of them thinly. Start with two or three: one situational (for example SR-22 or high-risk), one local-agent cluster, and one switching or cheap-coverage cluster as a control that is likely more expensive.

**Step 3: structure.** Separate campaigns per cluster (so budgets and bids can differ), exact and phrase match first, tight geography, schedule set to staffed hours plus a lower-bid off-hours test, call assets and a call-focused variant for the situational clusters, dedicated landing page per cluster. Track form submissions and calls of a minimum length as conversions, and plan offline conversion import for sales so bidding can later learn from sales rather than leads.

**Hypotheses the first test checks, and what would change the plan:**

| # | Hypothesis | Measured by | Result that changes the plan |
|---|---|---|---|
| H1 | Situational clusters (SR-22, high-risk) cost less per sale than head terms for this client | Cost per sale by cluster, after enough sales to compare | If situational sales cost the same or more, or the client cannot place these drivers, drop them and move to local/switching |
| H2 | Calls close at a higher rate than forms | Close rate by lead source | If forms close as well, extend hours with form-first ads; if calls dominate, cut off-hours spend |
| H3 | "Licensed human, no resale" outperforms a price-anchor message | Ad CTR and lead-to-sale rate, A/B by ad and page | If price anchor wins, the client is competing on price after all and needs more competitive carriers |
| H4 | Actual CPCs are within the affordable range computed in Step 1 | Average CPC vs affordable CPC | If CPCs are well above, narrow geography and queries further or stop; no bidding strategy fixes negative unit economics |
| H5 | Asking for a phone number later in the form increases completed quotes without lowering close rate | Completion and close rates, page variant test | If close rate falls, return the phone field |
| H6 | Off-hours clicks are worth less | Cost per sale by hour | If equal, remove the schedule restriction |

**What would stop the test early:** lead quality the client rejects (wrong state, no car, invalid numbers) above a level agreed in advance; signs of invalid traffic; any compliance concern with consent wording.

### 6.4 Traffic-only variant

If the objective were traffic rather than leads (for example a publisher monetising with ads or affiliate links, or a brand wanting awareness), "good traffic" must still be defined by what it leads to, or the account will optimise towards cheap, useless clicks:

- **For a publisher:** good traffic is traffic whose revenue per visit exceeds its cost per click. Define it with revenue per session (ad RPM or affiliate earnings), not sessions. Clusters with informational intent (how much is car insurance in [state], what does SR-22 mean) may suit this.
- **For awareness or content:** define a quality visit with observable behaviour: engaged session (time and scroll), visit to a second page, quote-tool start, return visit within 30 days, from the target states, on search (not partner or display) inventory. Exclude bot-like patterns (zero-second sessions, data-centre locations).
- **What to avoid:** maximise-clicks bidding with no quality guardrail tends to buy the cheapest clicks available, which in insurance are often low intent or out of footprint [Practitioner prior].
- **Still unknown:** the value of a visit that does not convert, which is a business decision the client has to make.

---

## 7. Risks, honest uncertainty, and what needs account data or a client

### 7.1 Risks

- **Compliance.** TCPA and state telemarketing law for any calls or texts that follow a lead; the revoke-all rule now due 31 January 2027 [Verified]; buyer contracts may impose stricter consent than law [Hypothesis]; state licensing for anyone discussing coverage [Unverified background]. A lawyer, not the strategist, signs off consent wording.
- **Google policy.** Possible financial-services verification and disclosure requirements; status for US insurance not confirmed [Unknown].
- **Cycle risk.** Click prices follow carrier appetite. If claims costs rise and carriers pull back as in 2022-2023 [Verified], lead prices and click prices can move quickly, changing both sides of a lead-gen business.
- **Buyer concentration.** Even EverQuote gets 38% of revenue from one customer [Verified]. A small lead seller is more exposed.
- **Lead quality and invalid traffic.** High-value verticals attract fraud; unknown scale for this client.
- **Measurement gap.** The sale happens offline, days later. Without sales fed back, bidding optimises to leads, which can drift towards cheap, low-quality leads [Practitioner prior].
- **Claims you cannot make.** Competitors' savings claims rest on their own customer surveys. A new advertiser without that data should not quote savings figures.

### 7.2 What this research could not establish

| Question | Why unknown | What resolves it |
|---|---|---|
| Real CPCs and volumes by cluster and state | No Keyword Planner access; benchmarks are pooled and not auto-specific | Keyword Planner in an account, then live test data |
| Monthly search seasonality | Google Trends blocked to automated access | Trends and Keyword Planner monthly data |
| Competitor ad copy, final URLs, longevity | Transparency Center is script-rendered | Manual browser review |
| Competitors' bids, budgets, margins, motives | Never observable | Nothing; Auction Insights shows overlap only |
| Client's affordable CPC | Needs commission, close rate, tenure | Client data, then sales feedback |
| Whether the client can place high-risk drivers | Depends on carrier appointments | Client |
| Consent rules each buyer requires | Contract-specific | Buyer contracts, counsel |
| Status of state mini-TCPA laws, April 2025 revocation provisions, McLaughlin effect | Could not open sources this session | Counsel or a follow-up research pass |
| Whether "licensed human" beats price anchoring | Untested | H3 in the first test |

---

## 8. Sources (all checked 2026-10-13 unless noted)

Opened in this session:

1. NAIC, 2025 Market Share Reports, Property and Casualty (Total Private Passenger Auto table): https://content.naic.org/sites/default/files/research-actuarial-property-casualty-market-share.pdf
2. Repairer Driven News, "State Farm, Progressive hold 37% of auto insurance market share, NAIC data shows" (2026-03-31): https://www.repairerdrivennews.com/2026/03/31/state-farm-progressive-hold-37-of-auto-insurance-market-share-naic-data-shows/
3. Morrison Foerster, "Eleventh Circuit Vacates FCC's TCPA One-to-One Consent Rule": https://www.mofo.com/resources/insights/250130-eleventh-circuit-vacates-fcc-s-tcpa-one-to-one-consent-rule
4. Goodwin, "The FCC Issues Final Rule Formally Eliminating the One-to-One Consent Requirement" (2025-09-15): https://www.goodwinlaw.com/en/insights/blogs/2025/09/the-fcc-issues-final-rule-formally-eliminating-the-one-to-one-consent-requirement
5. Burr & Forman, "The FCC Delays Effective Date of TCPA Revoke-All Rule Until January 31, 2027": https://www.burr.com/telephone-consumer-protection-act/the-fcc-delays-effective-date-of-tcpa-revoke-all-rule-until-january-31-2027
6. Brownstein, "FCC Extends Compliance Deadline for 'Revoke All' Rule": https://www.bhfs.com/insight/fcc-extends-compliance-deadline-for-revoke-all-rule/
7. MediaAlpha, Form 10-K for FY2025: https://www.sec.gov/Archives/edgar/data/1818383/000181838326000049/max-20251231.htm
8. EverQuote, Form 10-K for FY2025: https://www.sec.gov/Archives/edgar/data/1640428/000119312526066957/ever-20251231.htm
9. Progressive, Form 10-K for FY2025 (Note 1, advertising costs): https://www.sec.gov/Archives/edgar/data/80661/000008066126000086/pgr-20251231_d2.htm
10. J.D. Power, 2026 U.S. Insurance Shopping Study press release (2026-06-04): https://www.jdpower.com/business/press-releases/2026-us-insurance-shopping-study/ and PDF: https://www.jdpower.com/sites/default/files/file/2026-06-02/2026033%20U.S.%20Insurance%20Shopping%20Study.pdf
11. Repairer Driven News, "LexisNexis, J.D. Power report upward insurance shopping and switching trends" (2026-05-14): https://www.repairerdrivennews.com/2026/05/14/lexisnexis-j-d-power-report-upward-insurance-shopping-and-switching-trends/
12. Repairer Driven News, "Consumers less satisfied if forced to switch channels during auto insurance inquiry" (2026-06-11): https://www.repairerdrivennews.com/2026/06/11/consumers-less-satisfied-if-forced-to-switch-channels-during-auto-insurance-inquiry/
13. Insurance Edge, "Latest Quarterly Trends in Focus for J.D. Power" (2026-08-10): https://insurance-edge.net/2026/08/10/latest-quarterly-trends-in-focus-for-j-d-power/
14. US Bureau of Labor Statistics, CPI Table 2, August 2026: https://www.bls.gov/news.release/cpi.t02.htm
15. Autobody News, "Insurance price index falls nationally as state rate filings climb, parts costs rise" (2026-08-19): https://www.autobodynews.com/news/insurance-price-index-falls-nationally-as-state-rate-filings-climb-parts-costs-rise
16. Insurify, "Average Cost of Car Insurance" (updated 2026-09-30): https://www.insurify.com/car-insurance/average-car-insurance-cost/
17. Firefly Agency, "Insurance agency producer commission splits" (marketing page, no methodology): https://www.fireflyagency.com/learn/insurance-agency-producer-commission-splits/
18. LocaliQ, "Search Advertising Benchmarks" (2026 edition, updated 2026-06-01): https://localiq.com/blog/search-advertising-benchmarks/
19. WordStream, "Google Ads Benchmarks 2024" PDF: https://www.wordstream.com/wp-content/uploads/2024/05/ws-guide-google-ads-benchmarks-2024.pdf
20. Google Ads Help, "About Ad Rank": https://support.google.com/google-ads/answer/1722122
21. Google Advertising Policies Help, "Financial services": https://support.google.com/adspolicy/answer/2464998
22. Progressive auto insurance page: https://www.progressive.com/auto/
23. GEICO auto insurance page: https://www.geico.com/auto-insurance/
24. The Zebra home page: https://www.thezebra.com/
25. EverQuote home page: https://www.everquote.com/
26. Insurify home page: https://insurify.com/
27. Blake Insurance Group, online auto quote page: https://blakeinsurancegroup.com/online-auto-quote/

Attempted but not opened (claims depending on them are labelled Unknown or Unverified background):

- Google Ads Transparency Center (https://adstransparency.google.com/), rendered without ad data.
- Google Trends (robots disallowed).
- NerdWallet car insurance pages, Insurance Information Institute SR-22 page, Progressive SR-22 page, Texas DPS SR-22 page, US Supreme Court opinion in McLaughlin Chiropractic v. McKesson, CompliancePoint revoke-all article: fetch errors or session budget exhausted.
- Bankrate car insurance rates page redirected to the Bankrate home page.
