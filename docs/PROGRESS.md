# AllFix progress log

Kept up to date while building, so work can resume if a session ends. Newest first.

## 2026-10-13

### Windows readiness (static review by Fable; still never run on Windows)
- Fixed: native PostgreSQL installs get the allfix user and database created by setup.ps1; backups
  find pg_dump in the PostgreSQL folder, no longer corrupt Docker dumps (copied out of the
  container instead of piped through PowerShell), and don't abort on stderr notices from Task
  Scheduler; setup prefers Python 3.13/3.12 and warns when Git for Windows is missing (Claude Code
  needs it); piactl "Unknown" public IP right after connecting no longer fails the route; piactl
  runs without console windows and the monitor stops on exit; UTF-8 console output; the daily
  check runs windowless (pythonw) and logs to logs/check-accounts.log; README says to git clone.

### First eval run of the real app (11 cases, blind Fable grading)
- All 11 cases ran through the app on the subscription in about 6 minutes, with no errors.
  Answers and grading: /mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-13/.
- Result: 8 PASS, 3 PARTIAL (EV-01 Quality Score, EV-03 new niche, EV-04 competitors), 0 FAIL, no
  traps hit, no invented numbers. 23/31 critical lines under the earlier convention (the chat-only
  run scored 26/31). Single self-written grader and rubrics: a sign, not proof.
- Fixes: judge tests in the client's money; say how much data a conclusion rests on; Quality
  Score per component, never as the cause of CPC; seen / inferred / unknowable for competitors;
  follow the matching playbook's steps; clearer label definitions (owner's figures are
  assumptions, account data the user shows is observed). KB error fixed: two lines in
  measurement/tracking-attribution.md said target changes reset learning (contradicting
  PLT-BID-011).
- Re-run of the 4 weakest cases after the fixes: 10/13 critical lines (was 6/12); EV-04 now
  passes, EV-01 up from 0/3 to 2/3. Still missing: some second-order caveats (EV-01 "how to"
  queries can be emergencies, EV-11 value-based bidding). Added: forecasts in business results,
  one line about saved items. Stopped iterating here to avoid tuning to self-written rubrics.

### Supabase ready, eval runner
- Supabase project (Frankfurt, Postgres 17) now has the full AllFix schema, migrations 001-005,
  recorded in schema_migrations so the app treats them as applied. Tables are owned by `postgres`
  (the role the app connects as, so RLS does not block it); RLS with no policies closes them to
  Supabase's public API (the advisor lists this as INFO, by design). Empty: the knowledge base
  loads when the app first starts against it. To use it, put the Session pooler connection string
  in DATABASE_URL on the PC.
- `scripts/run_evals.py` runs the 11 evaluation cases through a running AllFix (throwaway project
  per case, answers to evals-out/), so the real strategist can be graded against the rubrics.
- Startup waits up to 60 s for the database and explains clearly when it can't connect.

### Phase 6 (lean) and research run 3
- Fable reviewed the Phase 6 plan first and cut it: no unattended model rounds (they would spend
  Elad's interactive Claude usage and could write to project memory unseen), no scheduled market
  sweep until manual ones prove useful, no lessons export yet.
- Built: `ads/checks.py` daily account check (deterministic, once per project per day, verified
  diffs vs the previous check, baseline checks that skip young accounts and need an expected 4+
  conversions before flagging zero), `/api/rounds/account-check` (local only), `check-accounts`
  CLI, `scripts/schedule.ps1`, Stage 07 card, forecast ledger (brief lists due forecasts; Stage 06
  counts), `update_item` can merge data. 7 new tests.
- Run 3 (emergency locksmith, Tel Aviv, Hebrew): 38 steps, 12 items, no tool errors. The agent
  tried a Write tool (refused) because the parent Claude Code session's memory settings leaked
  into it through environment variables; the strategist now gets those variables blanked, and the
  prompt says it has no file tools.
- Fable review of run 3: usefulness 7/10, rigor 7/10. Policy, call-ads and forwarding-number
  claims checked out. Misses: no forecasts saved, budget never in shekels, a "verified" label on
  an unopened page, night-hour demand handled by switching off, no English/Russian searches,
  marketplaces not compared as lead sources, bundled risk/question items.
- Fixes: save_item refuses forecasts/experiments without review_after (and prediction/metric or
  hypothesis/success_metric); calculate_economics prices a test across CPC scenarios; prompt adds
  policy check, other languages, device, demand peak vs capacity, marketplaces as lead sources,
  "observed at most" for unopened pages, screenshots request, one thing per item; due experiments
  also appear in the project state.

### Stage 01 and read-only Google Ads (Phase 5)
- Guard (`connectivity/guard.py`): PIA must report Connected (checked on every request, full check
  cached 5 min, a `piactl monitor` thread blocks on a drop); two of three IP-echo services must agree
  and match PIA's public IP; country strict, region advisory; Dolphin optional and advisory. Network
  path ignores proxies and is IPv4 only. Fable reviewed the design before building.
- `GuardedTransport` refuses any endpoint except OAuth token, listAccessibleCustomers and
  search/searchStream, then asks the guard, so mutations can't leave the machine.
- `ads/`: REST client (v25), GAQL allowlist with a 1,000-row cap, 7-query 90-day import with a plain
  summary, `ads_query` and `account_snapshot` tools, `python -m allfix ads-login` (loopback OAuth +
  PKCE, token exchange through the guard, writes the refresh token to .env).
- Stage 01 screen: profile form, Verify route checklist, read-only import, snapshot summary.
- Bug found by tests: the client passed a 10,000-row default that skipped the 1,000 cap. Fixed.
- Not verified: real PIA, Dolphin's local API path, a real Google Ads account.
- GitHub repo elad-allfix/SIPPC-System connected at 12:00; push waits on the public/private question.

### First real research run (run 1: mobile dog grooming, Austin)
- Ran end to end on the subscription (Opus 5.5, Standard): 44 steps, 5.4 min, 11 items + 6 facts
  saved. Full output: /mnt/project-files/allfix-runs/2026-10-13-run1-mobile-dog-grooming-austin.md
- Fable review: usefulness 7/10, rigor 7/10. Spot-checks of Woofie's prices, Barkbus FAQ and LSA
  eligibility held up; no invented numbers; economics arithmetic correct.
- Problems found and fixed: (1) tool budget ran out before strategy items were saved -> budget 60,
  research stops 5 calls early while saving stays open 10 past the cap, prompt says save every ~6
  calls; (2) "conversion rate matters most" was an artifact of range widths -> economics tool now
  reports uncertainty_by_input with a note; (3) prompt now covers SERP layout for local services
  (LSA, map pack, Business Profile), seasonality, owner-operated vs staffed margins, capacity,
  when to change bidding, fetch-failure handling, and a closing "This week" list.
- Environment limit: the cloud test machine's network policy blocks arbitrary websites, so
  WebFetch and audit_page cannot open pages here (search works). On Elad's PC they can.

### Website audit (Phase 4)
- `audit_page` tool: raw-HTML facts (title/H1/opening text, CTAs, tel links, forms with friction
  facts, prices, trust snippets, schema, measurement tags with ids and a visibility verdict that
  never claims tracking is missing when GTM is present, HTTP/CDN facts, notable internal links,
  JS-shell and bot-block detection, message match against intent and ad headline). SSRF guard
  checks every redirect hop. 14 offline tests with fixtures. Not yet tried on live sites (blocked
  here). Fable's design review adopted except PageSpeed (deferred) and check_site (cut).

### Subscription backend (Claude Agent SDK)
- Done: `STRATEGIST_BACKEND=subscription` (default) runs the strategist through the Claude Agent SDK
  on the user's own Claude plan. `api` keeps the original API-key loop.
- Policy (checked in Anthropic docs, 2026-10-13): a person's own Agent SDK projects draw from their
  plan's limits; offering Claude login to other users, or storing their credentials, is not allowed.
  AllFix never touches credentials (the Claude Code binary signs in through `claude login`), and the
  subscription backend refuses to serve other machines unless `ALLFIX_SINGLE_USER=true`.
- Billing guard: the agent process gets an empty `ANTHROPIC_API_KEY`; if Claude Code still reports an
  API key as its auth source, the turn stops before any model call is billed.
- Transcripts are mirrored to Postgres (`agent_transcripts`), so a conversation resumes on another
  machine or after local files are cleaned; if resume fails, a text recap seeds a new session.
- Windows: the SDK runs on its own thread with a proactor loop (subprocesses); Postgres stays on the
  main selector loop.
- Live tests (`ALLFIX_LIVE=1 pytest tests/live`): 5/5 pass in the cloud container on the subscription
  (auth source `none`, rate-limit window `five_hour`): tool call + item saved, resume after deleting
  the local transcript, API-key refusal, busy-conversation guard, Stop then continue.
- Fable review before building: accepted single-user guard, Postgres session store, source extraction,
  strict tool isolation, budget hook, per-conversation lock, usage-limit messages. Not accepted:
  moving `CLAUDE_CONFIG_DIR` to a scratch folder (it would hide the Claude login itself).

### Blockers
- GitHub: account `elad-allfix` is connected but has no repository; waiting for Elad to create
  `allfix` and install the Claude GitHub App. Code lives in /mnt/project-files/allfix-app meanwhile.
- PC: no computer linked to Elad's Claude account, so files can't be written to his folder yet.
- Not yet run on Windows.

## 2026-10-13 · Local-services knowledge
- Added `knowledge/market/local-services.md`: 18 entries (MKT-LOCAL-001..018) on Local Services Ads, Google Business Profile and the local pack, call handling and recording, lead marketplaces and local ad policy. The evaluations and run 3 (locksmith) showed the gap.
- Fable fact-checked every load-bearing claim against the cited pages: "Fit to load", minor corrections applied in the file.
- Three older entries (MEA-CONV-023, PLT-ADS-019, MKT-WEB-024) said calls count by minimum length. Each now notes the 2026-04 change: in the US and Canada "Calls from ads" are judged by AI-qualified call leads, length is a fallback (MKT-LOCAL-014).
- Knowledge base now 393 entries; README, READINESS and research-gaps updated; shared copy in /mnt/project-files/allfix-kb (index.jsonl regenerated). Tests 79 passed, 5 skipped.

## 2026-10-13 · Run 5 (new plumber, Phoenix) and fixes
- Run 5: a US plumber with no ads asks "LSA, Search or both?". Answer in /mnt/project-files/allfix-runs/2026-10-13-run5-plumber-phoenix.md. Fable: usefulness 7/10, rigor 5/10.
- Real errors: budget rows summed to $3,100-3,315 against a $3,000 cap; a bid cap above its own affordable CPC; it said LSA may not start in month 1 although plumbers get pre-badge leads; "[verified]" dropped Google's "may"; no conversion definition; tool narration in the answer.
- Fixes (general, not tuned to this case): prompt rules for one budget table that sums to the cap, bid caps at or below affordable CPC, a measurement block, hedges kept in [verified] claims, no narration; new strategic playbook S8 (local service launch); new entry MKT-LOCAL-019 (pre-badge LSA); MKT-LOCAL-001 voicemail rule corrected. Knowledge base 394 entries. Tests 79 passed, 5 skipped.
- Rerun (run 5b, /mnt/project-files/allfix-runs/2026-10-13-run5b-plumber-phoenix-after-fixes.md): budget now sums to the cap, bid cap within the affordable CPC, pre-badge correct, measurement block present. One small arithmetic slip left (LSA cost per job range); not chasing it further.

## 2026-10-13 · Run 6 (SaaS, investor wants "more traffic") and fixes
- Run 6: a 6-person PT-clinic scheduling SaaS with $6,000 over 3 months and no conversion tracking. Answer in /mnt/project-files/allfix-runs/2026-10-13-run6-saas-traffic-goal.md. Fable: usefulness 7/10, rigor 6/10. Challenging the traffic goal was right; budget summed; loss-tolerant bid caps were labelled (the run 5 rule worked).
- Gaps: kill rule (150 clicks) unreachable for two clusters at their budgets; competitor-name cluster without trademark rules; software directories not weighed as a channel; device not considered; tool narration still at the top of the answer.
- Fixes: prompt now asks for kill criteria by failure type with a per-cluster click-sufficiency check, trademark rules whenever competitor names are targeted, directories/marketplaces as competitors and channels in any category, and the buyer's device. Narration is now handled in the app itself: short text written just before a tool call is shown as a progress note in the activity list, not as the answer (UI stream, stored history, eval runner; new tests in test_render.py). Tests 81 passed, 5 skipped.
- Rerun (run 6b, /mnt/project-files/allfix-runs/2026-10-13-run6b-saas-after-fixes.md): every gap above addressed; stop rules reachable at the high CPC scenario. Stopping iteration on this case.

## 2026-10-13 · Run 7 (coffee store after a Performance Max switch) and fixes
- Run 7: Google ROAS up, Shopify revenue flat, new customers down after moving to one PMax campaign with brand and Add to cart as primary. Answer in /mnt/project-files/allfix-runs/2026-10-13-run7-coffee-pmax.md. Fable: usefulness 7/10, rigor 5/10. Causal story broadly right; Fable checked the 2026 PMax features it relied on against Google's pages (current).
- Errors: one citation (PLT-BID-031) attached to an inference; "no customer list" asserted although the user never said; a capped brand Search campaign (which hands brand queries back to PMax); engaged-view and remarketing credit not considered; three bidder-resetting changes a week apart, one scheduled before the data that decides it.
- Fixes: prompt rules on unstated account facts, on what a citation supports, and on sequencing changes with evaluation windows and a peak-season freeze; playbook D7 gains a step to split conversions by ad event type and new vs returning, plus the uncapped-brand-campaign rule.
- Rerun (run 7b, /mnt/project-files/allfix-runs/2026-10-13-run7b-coffee-pmax-after-fixes.md): every finding addressed; no narration in the answer. Stopping iteration on this case.

## 2026-10-13 · Evaluation run 3 (regression check after runs 5-7)
- All 11 cases rerun through the app; Fable graded them blind: 8 PASS, 3 PARTIAL (EV-01, EV-03, EV-04), 0 FAIL, 26/31 critical lines (first app run 23/31). Grading in /mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-13-run3/GRADING.md.
- Regression found: four answers repeated "changes reset learning". Cause: the new sequencing rule said "changes that reset bidding", and two knowledge lines (expert-diagnosis.md, PRC-DIAG alert weighing and "Stacking changes") still used the folklore. All three corrected to "recalibrate"; the prompt now says target changes do not trigger Learning (PLT-BID-011).
- EV-04 slipped because the "what we cannot see about competitors" sentence appears only by chance; the competitor rule now asks for it explicitly.
- Not done on purpose: rubric-specific playbook exceptions (dayparting, "how to fix" queries) that would tune to self-written cases.
- Recheck of EV-01, EV-04, EV-07 after the fixes (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-13-run3-recheck/): no "reset learning" claims left (EV-01 now says a target change does not reset learning, PLT-BID-011); EV-04 states what cannot be seen about competitors.

## 2026-10-13 · Israel knowledge
- Added `knowledge/market/israel-market.md`: 17 entries (MKT-ISR-001..017) on VAT-inclusive consumer prices (VAT 18% since 2025-01), the anti-spam law for SMS/email/WhatsApp follow-up, Privacy Amendment 13, Google consent rules for Israel, account setup (ILS, time zone, no prepay), Hebrew right-to-left text and keyword forms, Arabic and Russian speakers, the Sunday-Thursday week and Shabbat, the holiday and election calendar, war-time demand, WhatsApp and Waze, Zap and Yad2, Israel-specific Google policies and medical advertising law.
- Researched by a worker, then fact-checked by Fable ("Fit to load" after in-place fixes: one fine was only a notice of intent, two legal entries relabelled as secondary summaries, a weak GDP source replaced, WhatsApp-asset availability downgraded). Unverified points listed in research-gaps.md.
- Knowledge base 411 entries. Tests 81 passed, 5 skipped.
