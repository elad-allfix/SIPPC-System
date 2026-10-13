# AllFix progress log

Kept up to date while building, so work can resume if a session ends. Newest first.

## 2026-10-13

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
