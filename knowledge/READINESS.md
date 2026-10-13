# Readiness: what is ready, what is uncertain, what still needs research
As of 2026-10-13, after one research pass and one evaluation run.

## Ready to use
- **Platform mechanics** (auction and quality, keywords and matching, structure and budgets, bidding, ads and assets, AI Max and PMax, measurement). 393 entries (18 on local channels added 2026-10-13), two thirds backed by opened Google documentation. Dozens of entries record a 2025–2026 change, including:
  - the September 2026 move to AI Max
  - the August 2026 change in how budget-limited target campaigns behave
  - the Data Manager API path for offline import
  - removal of language targeting
  - the new budget pacing for schedules that switch off whole days
- **The relationship map**: which metric identities always hold, which mechanisms are documented, and which metric pairs mislead.
- **Diagnostic playbooks**: CPC, CTR, conversions, Quality Score, traffic quality, lead quality, false profitability, spend spikes, impression share.
- **Strategic playbooks**: new niche, competitors, traffic-only goals, intent and creative, scaling, doing nothing, measurement foundation.
- **The research method for a new niche**, shown end to end in the car insurance demonstration with every claim labelled.

Evidence that it helps: in the blind run the knowledge-base strategist met 26 of 31 critical rubric lines against 19 for the same model without it, and had no outright failures against two (`evals/results.md`). The rubrics were self-written, so treat this as a sign, not proof.

## Usable but uncertain
- **Practitioner judgement.** The web search budget ran out in every area. Experienced managers' writing (forums, independent PPC experts, Optmyzr and Search Engine Land archives) is under-represented. Entries built on inference or practitioner opinion are labelled, but there are fewer of them than there should be.
- **AI Max, broad match and PMax performance.** Published evidence is mostly ecommerce and mostly observational. Lead generation and local services have almost none. Post-migration data (after September 2026) does not exist yet.
- **AI Overviews and AI Mode.** There is no reporting split, ad formats are still changing, and pricing is unknown.
- **Persuasion and copy.** Controlled field tests in search ads are rare. Lab findings transfer imperfectly. Several entries rest on single studies.
- **Places where Google's own pages disagree**, all listed in `research-gaps.md`:
  - the learning-period wording
  - the date of the pacing change
  - the audience list minimums
  - whether pins survive in AI Max
  - the Data Manager allowlist window
- **One error has already been found and corrected** (Misrepresentation enforcement). There are probably others. Each one found in use should be fixed in the entry itself.

## Still needs research
1. **Local business channels:** covered since 2026-10-13 by `market/local-services.md` (18 entries, fact-checked by a second reviewer). Still thin: LSA lead prices by trade and city (Google publishes none), and GBP ranking factors beyond Google's own three (relevance, distance, prominence), where the evidence is vendor surveys.
2. **Vertical rules:** lawyer advertising (state bar rules), insurance state licensing and TCPA details, and healthcare and finance copy limits by country.
3. **Practitioner pass:** fill the sources the budget cut off. The list, by file, is in `research-gaps.md`.
4. **Value benchmarks:** lead marketplace and pay-per-call prices, and margins and close rates for common lead-gen verticals. These are priors for click value when a client has none.
5. **Lead-gen evidence** on AI Max and broad match, form design and lead response speed, from sources other than vendors.
6. **For the car insurance demo:** real keyword volumes and CPCs (needs a Keyword Planner account), Trends seasonality, and competitor ad copy (the Transparency Center needs a browser).
7. **Real evaluation cases:** 10–20 of Elad's past cases with known outcomes. This is the only test that can show the strategist is expert rather than well-read.

## What this is not
- **It is not a trained model.** The knowledge lives in files the strategist reads. Improving it means editing entries.
- **It is not proof of expertise.** It has passed only self-written synthetic tests.
- **It has not used any live account, client or SERP API data.**
