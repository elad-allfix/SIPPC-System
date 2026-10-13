# AllFix Expert Knowledge Base

This is the knowledge the AllFix strategist reasons from. It covers Google Ads platform mechanics, how experienced managers diagnose and decide, market research for new niches, websites and journeys, measurement and economics, and playbooks that tie these together.

It is **stored knowledge, not a trained model.** The strategist reads the relevant entries at the moment it needs them (by ID, keyword search or semantic search). Nothing here changes the model itself. Updating the knowledge means editing these files.

Checked: 2026-10-13. Research was done with web sources opened on that date. No real account data was used.

## Layout

| Path | What it holds | Entries |
|---|---|---|
| `SCHEMA.md` | entry format and rules (evidence type, confidence, sources, "changed" markers) | |
| `index.jsonl` | one line per entry: id, title, file, evidence type, confidence, changed flag, claim. Generated from the entry headings; Claude regenerates it after edits | 394 |
| `platform/auction-quality.md` | Ad Rank, thresholds, pricing, Quality Score, impression share, AI Overviews placement | 30 |
| `platform/keywords-matching.md` | match types, precedence, AI Max migration, search terms visibility, negatives, Keyword Planner | 33 |
| `platform/structure-targeting-budgets.md` | campaign structure, location, language, audiences, partners, budgets and pacing, impression share | 30 |
| `platform/bidding.md` | strategies, learning, conversion lag, targets vs budgets, simulators, exploration, scaling | 31 |
| `platform/ads-assets.md` | RSAs, Ad Strength, asset reporting, assets, AI text, policy limits on copy | 33 |
| `platform/automation.md` | AI Max, Performance Max, recommendations, AI Overviews / AI Mode, control patterns | 35 |
| `practice/expert-diagnosis.md` | how experts diagnose, decide and test; uncommon tactics; case studies | 40 |
| `practice/copy-psychology.md` | search ad persuasion, message match, angles, what evidence supports | 28 |
| `measurement/tracking-attribution.md` | conversion setup, attribution, enhanced conversions, Data Manager API, consent | 30 |
| `measurement/traffic-quality-economics.md` | invalid traffic, good traffic, break-even, margin, LTV, incrementality | 30 |
| `market/niche-research.md` | demand sizing, intent clustering, SERP and competitor research, regulated niches, test sizing | 28 |
| `market/website-journeys.md` | landing page review, speed, forms, trust, journey analytics, lead follow-up | 27 |
| `market/local-services.md` | Local Services Ads, Google Business Profile and the local pack, call handling, marketplaces, local policy | 19 |
| `relationships/metric-relationships.md` | identities, mechanisms, tendencies, misleading metric pairs, what is unobservable | |
| `playbooks/diagnostic.md` | backbone plus 9 symptom playbooks | |
| `playbooks/strategic.md` | 8 planning playbooks (new niche, competitors, traffic goals, intent and creative, scaling, doing nothing, measurement, local service launch) | |
| `demo/us-car-insurance-market-research.md` | one complete pre-launch market research, with every claim labelled | |
| `evals/` | 11 synthetic cases with rubrics, blind runs and graded results | |
| `research-gaps.md` | what could not be verified, source conflicts and open questions, by file | |
| `READINESS.md` | what is ready, what is uncertain, what still needs research | |

## Evidence profile (from index.jsonl)

- **Evidence type:** documented 265, study 40, practitioner 40, inference 39, Google statement 8, hypothesis 2.
- **Confidence:** high 244, medium or medium-high 129, low, low-medium or medium-low 21.
- **Recent changes:** 78 entries carry a "(changed YYYY…)" marker.

The base leans toward Google's own documentation because the shared web search budget ran out partway through every area, so practitioner sources are under-represented. `research-gaps.md` lists what is missing.

## How the strategist should use it

1. Start from the playbook for the situation. Each step names the entries behind it.
2. Pull the cited entries and check their evidence type, confidence and "changed" date before relying on them.
3. Carry the labels into the answer: verified (an entry with an opened source), estimate, hypothesis or unknown.
4. Practitioner numbers are priors. The account's own data replaces them as soon as it exists.
5. When an entry turns out to be wrong in practice, correct the entry, not just the answer.

## Maintenance

- Platform entries go stale fast: 78 entries carry a recent change marker. Re-check entries marked "changed" and anything about AI Max, AI Overviews or measurement APIs every month.
- To add an entry, follow `SCHEMA.md`, give it the next free ID in its file, then ask Claude to regenerate `index.jsonl`.
