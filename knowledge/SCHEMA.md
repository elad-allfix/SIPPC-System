# AllFix Expert Knowledge Base: entry schema

Every knowledge file is Markdown. A file covers one topic and contains numbered **entries**. Each entry is self-contained so the strategist can retrieve it alone (by ID, by grep, or by embedding search).

## File header

```
---
area: platform | practice | market | measurement | playbooks | relationships
topic: <short topic name>
checked: 2026-10-13
owner: research
---
# <Topic title>
<2-4 sentence overview: what this file covers and the single most important idea in it>
```

## Entry format

```
### <ID> · <short title>
- **Claim:** one or two sentences, the knowledge itself.
- **Evidence type:** documented (official Google/platform docs) | google-statement (Google rep, blog, forum answer) | study (named dataset / vendor study, observational) | practitioner (heuristic from experienced managers) | inference (our reasoning from documented facts) | hypothesis (plausible, unverified)
- **Confidence:** high | medium | low
- **How it works:** the mechanism, as far as known.
- **When it matters / how experts use it:** decisions this changes.
- **Exceptions and failure modes:** when it does not hold, counterexamples.
- **Signals in data:** what you would see in an account, SERP or analytics that indicates this is in play.
- **Sources:** [title](url) (checked YYYY-MM-DD); at least one opened page for documented/study claims.
- **Open questions:** what we still do not know (omit if none).
```

IDs: `<AREA>-<TOPIC>-<NNN>`, e.g. `PLT-AUC-001` (platform/auction), `PRC-DIAG-004` (practice/diagnosis), `MKT-NICHE-002`, `MEA-CONV-007`.

## Rules

1. Never present a practitioner number (e.g. "30 conversions a month") as a platform rule. Put it in `practitioner`, give the range seen, and say when it fails.
2. Separate what is observable from what is inferred. Competitor bids, budgets, margins and motives are never observable.
3. Every documented claim needs an opened source page and a checked date. If a page could not be opened, say so and lower confidence.
4. Prefer mechanisms over tips: say *why*, so the strategist can reason about new situations.
5. Mark anything that changed in 2025-2026 with **(changed YYYY-MM)** so stale advice can be spotted.
6. Keep entries short and specific. Research quality over volume.
