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

## 2026-10-13 · Run 8 (dental clinic, Ramat Gan, Hebrew prompt)
- Answer in /mnt/project-files/allfix-runs/2026-10-13-run8-dental-ramat-gan.md. Strong plan; used the medical advertising entry and the election date. Missed VAT-inclusive prices, consent for WhatsApp follow-up, patient data as sensitive data and Google's health audience limits, because it never read the Israel legal entries.
- Fixes: prompt rule to read a country's own entries (legal, language, calendar) and to check sensitive-category audience limits; new entry PLT-STR-031 (personalized advertising policy: health and other sensitive categories cannot use Customer Match or remarketing lists), from Google's policy page. Knowledge base 412 entries.
- Rerun (run 8b, /mnt/project-files/allfix-runs/2026-10-13-run8b-dental-after-fixes.md): VAT-inclusive prices, the health audience limits and WhatsApp consent now appear; patient-data handling under Amendment 13 still missing (minor, not chased).

## 2026-10-13 · Eval set extended; rubrics hidden from the strategist
- Four new evaluation cases built from runs 5-8 and their reviews: EV-12 local launch (LSA vs Search), EV-13 investor wants traffic (SaaS), EV-14 ROAS up but store revenue flat after PMax, EV-15 Israeli dental clinic in Hebrew. 15 cases in total; `scripts/run_evals.py` picks them up.
- Found and closed a blind-eval leak: the strategist's read_knowledge could read `evals/cases` (rubrics) by slug. It now reads with include_evals=False; people can still open them in the Knowledge view. New test. 82 passed, 5 skipped.
- Checked the stored agent transcripts (2,778 entries, including deleted eval projects): the strategist never read an eval document, so earlier eval scores were not contaminated.

## 2026-10-13 · Baseline for the new cases EV-12..15
- Blind run graded by Fable (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-13-new-cases/GRADING.md): EV-12, EV-13, EV-14 PASS; EV-15 PARTIAL. Critical lines 11/12; all 27 cited entry ids checked and supported; arithmetic and dates correct; no traps.
- EV-15 missed the consent rule for promotional WhatsApp follow-ups and the Sunday-Thursday week in its schedule. The country rule now says such constraints go in the plan itself, not only in saved items.
- Windows: added "Setup AllFix.cmd" and "Start AllFix.cmd" (double-click); setup.ps1 links a zip-filled folder to GitHub when its repository has no commits. Code copied to Elad's PC folder; setup not run yet.
- Recheck of EV-15 after the fix: the plan now covers consent and the "פרסומת" label for promotional WhatsApp follow-ups (MKT-ISR-003) and the Sunday-Thursday week and Shabbat (MKT-ISR-010).

## 2026-10-14 · Running on Elad's PC
- Setup ran on Windows (Python 3.14 was picked since 3.12/3.13 are not installed; all packages installed). The folder is now linked to GitHub.
- Fixes found during the run: the GitHub link needed an explicit fetch refspec; setup now signs in to Claude with the Claude Code bundled in the Agent SDK (`auth status` / `auth login`); with no usable local Postgres it asks for the Supabase Session pooler string (typed in the console, saved only in `.env`) and asks again if the connection fails; Start opens the browser only once the server answers.
- Result: AllFix runs at http://127.0.0.1:8000 on Elad's PC against Supabase; 412 knowledge entries loaded; the rail shows "Claude subscription".
- New `Update AllFix.cmd`: fetches GitHub main, lets git take over hand-copied files that already match, fast-forwards, reinstalls the backend and rebuilds the interface.

## 2026-10-14 · Attach exports and screenshots
- Gap: the strategist asked users for search-term exports and phone screenshots, but the app had no way to receive files; the Ads API importer is the only account path.
- Fable reviewed the design before building: cut to CSV/TSV + images (no Excel or PDF yet), keep files in Postgres so backups carry them, return the export's preamble (date range) and its own Total rows so a filtered or top-N export is detectable, don't resend old screenshots every turn, test against export-shaped fixtures. Its premise that the strategist had never produced real answers was out of date (runs 1-8 exist); the design advice was applied.
- Built: migration 006 (`project_files`), upload/list/delete API (raw body), paperclip and paste-a-screenshot in the chat, files listed in the project brief, `read_file` tool (filter, sort, columns, paging, totals of additive columns only, Google Ads preamble and Total rows, UTF-16 Excel CSV, Hebrew headers, "--" as empty; images returned as image blocks). API backend drops screenshots from earlier turns. Tests 89 passed, 5 skipped.
- Live check (subscription backend): first run caught a missing import in the subscription tool bridge (the strategist reported the failure honestly instead of guessing). After the fix it read both files: named the off-topic broad term taking 95% of spend, the $621 gap between the rows and the export's account total, and the competitor offers in the screenshot; it asked what the conversions were before recommending a block.

## 2026-10-14 · Reading real account exports
- Prompted by 11 real Google Ads exports from Elad (about 1M rows, 2020-2026; they stay on his PC). Analysis: /mnt/project-files/allfix-runs/account-check-2026-10-14.md; tracking plan: tracking-plan-2026-10-14.md.
- Big files: uploads up to 200 MB. A table over 20 MB is reduced on arrival: rows with no cost and no conversions are dropped (their impressions and clicks are counted), then the highest-cost rows are kept if still too big. Change history keeps its first rows. The stored file's preamble says what was kept, the share of cost and conversions it covers, and the full-file sums; the original Total rows stay. A 244 MB UTF-16 search terms file reduces in about 12 s.
- Reading fixes: the CSV is parsed as a whole, so cells with line breaks (ad text, change history) are no longer glued together; CA$/US$/A$ and ISO codes, 1.234,50 and 1.234.567 parse as money; nan/inf are rejected; a broken quote falls back to plain text instead of crashing.
- Totals: when nothing is filtered, row sums are compared with the file's own Total row. A mismatch is flagged as totals_warning (e.g. an asset report listing the same money at account, campaign and ad group level summed to 2.57M vs 1.25M); for search terms a lower sum is explained as hidden searches; reports with a Level column also get totals per level. Report type (search terms, keywords, ads and assets, ad groups, campaigns, change history, conversion actions, auction insights; English and Hebrew) is recognised.
- Prompt: account reviews go tracking, waste, quality, structure, bidding history, and never add up files with different date ranges.
- Interface: an "Account check" button next to the paperclip uploads several exports and asks for what each covers, whether tracking can be trusted, one verdict, 3 numbers and the top 5 actions. A reduction note shows under the box.
- Reviews: Fable before (per-type shrink rules, full-file sums, separating level duplication from shrinkage, date ranges, dropping a duplicate checklist) and after (a slow per-level loop, csv errors, nan, byte-accurate size cap, lower upload limit), all applied. Tests 96 passed, 5 skipped.
- Live check (subscription): an account check on two synthetic files read both, reported each file's type, dates and totals, caught that the files did not reconcile (different campaigns, 10x spend, the Total row) and put tracking first.
- Known limit: a lone "1.000" reads as one, since English and Hebrew Google Ads exports use dot decimals.

## 2026-10-14 · Reading real full-history exports (parallel session on Elad's PC)
- Elad shared 11 full-history UI exports from his own account (kept on his PC only). Running the reader over them found: line breaks inside cells were lost (asset and change-history text glued together), "CA$" amounts did not parse (time series cost missing), sums across repeated levels were taken at face value (asset report rows add up to CA$2.57M against CA$1.25M spend), and four files were over the 10 MB upload limit (search terms 113 MB).
- Fixed: csv reads the whole text so cells keep their line breaks; currency prefixes and ISO codes parse; bids and Quality Score columns are never summed; read_file warns when rows differ from the file's first Total row or sit at several Levels; known Google Ads reports come with how_to_read; new where (number filters) and group_by (sums per value).
- Big files: uploads up to 250 MB; tables over 10 MB are condensed (rows with no cost, clicks or conversions left out, a note in the preamble) and gzip-stored. On the real files: search terms 113 MB -> 1.7 MB (79,571 of 692,048 rows, totals equal the file's own), change history 21 MB -> 1.2 MB, ad report 19 MB -> 0.2 MB. The prompt says to state a tracking gap once, then judge by cost, clicks, intent, quality and structure.
- DB-backed tests could not run on the PC (no local Postgres); the 71 others pass.
- Merged with the entry above into one version: kept the 20 MB reduce (with cost/conversion shares and full-file sums), Total-row checks and the Account check button; added this session's how_to_read, where, group_by, bid/quality columns never summed, gzip storage and the "say the tracking gap once" rule. A Level note replaces the first-Total-row warning.

## 2026-10-14 · Ignition entrance and setup
- New front door (Elad picked "Ignition" of five mockups): full-screen AllFix wordmark with three amber orbits on a canvas and one Enter button, shown once per browser tab session. Enter opens the app, or setup when there are no projects.
- The new-project pop-up is replaced by four full-screen questions (business, starting point with website when needed, market, goal with optional words); Enter key moves on. NewProject.tsx removed.

## 2026-10-14 · Orbit interface
- Elad picked "Orbit" from several mockups: a dark graphite frame (top bar, numbered seven-step path) holding light rounded sheets (chat, stage panel), the Sora typeface, amber only for the current step and focus, ink-black primary buttons. One fixed look; the light/dark toggle is gone.
- Fewer words by request: short stage names (Connection, Business, Market, ...); the answer comes first, with tool steps, reasoning, sources and the model line folded behind "Details" (only the last three steps show while working); findings show an evidence dot and title, labels in plain words (Checked, Seen, Estimate, To test, Assumed) and a small evidence bar per stage; Claude status is one dot in the top bar.

## 2026-10-14 · Hands-off updates on the PC
- Elad asked not to be asked to close, update and restart AllFix. With `ALLFIX_AUTO_UPDATE=1` (set by run.ps1) the server checks GitHub every 10 minutes; when a fast-forward update exists and no answer is being written, it stops with exit code 75 and run.ps1 updates (git, backend packages, interface build) and starts it again. A version that fails to apply is recorded in logs/update-blocked.txt so it doesn't restart in a loop. Start AllFix.cmd also just opens the browser if AllFix is already running. Tests 91 passed, 5 skipped.
- Not done: starting AllFix automatically at Windows sign-in (a Startup-folder shortcut). It was blocked as an unrequested persistent change; it needs Elad's explicit go-ahead.

## 2026-10-14 · Evaluation run 4 (all 15 cases) and a self-check
- Full run after today's changes, graded blind by Fable (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-14/GRADING.md): 13 PASS, 2 PARTIAL (EV-01, EV-03), 0 FAIL; critical lines 28/31 for EV-01..11 (run 3: 26/31) and 12/12 for EV-12..15 (11/12). The "resets learning" folklore is gone. Attachment requests are sensible (one paperclip mention per answer).
- Regressions found: prose contradicting its own table (EV-01), a stop rule the budget could not reach and a wrong [verified] label (EV-15), lost "what we cannot know" lines (EV-08, EV-13), an unlabelled cap above the affordable CPC (EV-12).
- Fix: a "Before you send" self-check in the prompt (text matches tables and tool results, sums, caps, reachable stop rules, exact [verified] labels, data limits where they change the conclusion) and, for new niches, structure and budgets only after demand and results-page research.
- Recheck of 8 cases (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-14-recheck/GRADING.md): every regression above fixed; all sums, caps and arithmetic correct; 53 cited ids exist. Verdicts unchanged (6 PASS, EV-01 and EV-03 PARTIAL); all-lines 37/9/0 vs 33/12/1. Answers 12% longer, substantive. The data-limits line was showing up as boilerplate in 5 of 8 answers, so it is now asked for only where it changes the conclusion (not rerun).
- Still open on purpose: EV-01's "how to fix" caveat and similar case-specific items; adding them would tune the strategist to self-written cases.

## 2026-10-14 · Navigation and first projects in Elad's AllFix
- Elad: the Dashboard said there were no projects and would not open; he wants Back on every page.
- Dashboard always opens; with no projects it shows an empty state with New project. Back on the entrance choice screen, on every setup question (the first goes back to where setup was opened), and an arrow plus the logo in the top bar return to the entrance. Library closes back to chat. Checked by clicking through in a browser.
- His Supabase had 0 projects: every earlier run used a throwaway local database. The 13 Oct test runs (6) and the 14 Oct account check are being imported as projects from the saved run logs (answers verbatim, items from the logs; data fields cut short in the logs are kept as text). Projects are named "(test run)"; the account project notes that the raw CSVs stay on his PC.


## 2026-10-14 · Projects page
- Elad: Dashboard should open a page with all projects, each showing its main details and what it needs; then he dropped the two-button choice screen: Enter goes straight there, with New project on that page.
- `GET /api/overview` (store.overview, no model call): per project the entry path, goal, place, conversations with messages, files, saved items, stages holding items, last activity (latest of project, conversation, file, item), latest open decision as "Current plan", and up to 4 needs (with a total): missing setup first (first conversation or account check, exports, website), then verified/observed website issues and one risk, due forecasts/experiments, open questions. Nothing is invented: "Nothing saved yet" when a project is empty. `store.is_due` is now shared with the strategist's brief (also skips scored forecasts and bad dates).
- Navigation: entrance → projects → project. The top-bar arrow goes one level up, the logo and "All projects" in the switcher go to the projects page, a reload in a project stays in it. Fable reviewed it; fixed: load errors no longer look like "No projects yet", due logic matched the strategist's, counts include closed items, lighter queries, "+N more inside". Not done: browser Back button between levels.
- Next: the fix round from the 7-layer audit (/mnt/project-files/allfix-audit/audit-2026-10-14.md), in its order.

## 2026-10-14 · Audit fix round 1 (7-layer audit by Fable)
- Audit: /mnt/project-files/allfix-audit/audit-2026-10-14.md. Elad approved the order and the database repairs ("go").
- Stages: Connection (1) and Control (7) hold no items; items asked for stage 1 go to Business (2), for 7 to their kind's stage (store.item_stage, on create and update). Stage 1 lists any items it has. Control now shows what the project needs (same logic as the projects page, `GET /projects/{id}/needs`), open actions (opportunities and decisions) and stage counts; the API-only daily check shows only when a connection profile exists. Ads-account projects open on Website & ads, whose empty state says to run Account check. Account check runs in Deep mode.
- Business: calculate_economics saves its inputs as facts (segment-keyed, labelled, assumption by default) and never overwrites a fact the user gave; when its inputs differ from such a fact it returns `conflicts` and asks for a rerun. Fact keys are canonical (business_model, conversion_definition, the economics input names). Stage 2 has a Correct button that quotes the exact key.
- Prompt: know the business model (company, agency, lead network) and the conversion definition first, without stalling the account review; a change to a live setting must rest on observed before/after metrics, a max CPC is a cap, and an affordable range that spans the observed CPC cannot decide; "Other search terms" is hidden, not waste (also in REPORT_GUIDE); recommended actions and open questions are saved as items as they are decided, closed when done. SAVE_ALLOWANCE 10 -> 20, research margin stays 5.
- Data repair in Elad's Supabase: 21 cut-short test-run item bodies made readable (whole fields kept, forecast metric/prediction/review date restored where the log had them; one forecast now due 16 Oct); 45 title-only items say where the reasoning is; Canada: two stage-1 tracking findings to stage 2, three account findings to stage 4, the hidden-searches item renamed with a note, and a note on the bid finding (avg CPC paid after the change CA$3.22, range too wide to call). The original item bodies are not recoverable (the run logs cut them).
- Fable reviewed the round; its 8 notes are applied. New eval EV-16 (bid reversal on assumed economics, business model, hidden terms).
- Note: the Supabase MCP tool hangs on any SQL text containing a semicolon inside a string; use one statement per call and chr(59).

## 2026-10-14 · Projects page in the Ignition style
- Elad picked style 2 "Ignition" from the three mockups (artifact 1dXCCuQ4F5gKRvTsEifWno). The projects page is now all dark with the entrance's orbits behind it: one line naming the project that needs him first (real projects before test runs, then the most severe need: fix, risk, do, check, answer) with that need underneath, three numbers (projects, fix or risk, your answers) and New project; that project's card glows; each card shows its place, a Test tag for test runs, the open-needs count, the 7-stage track, its single most urgent need, the other needs as chips, and the plan.

## 2026-10-14 · Eval check of the fix round, prompt tightened
- Ran EV-01, 03, 08, 12, 13, 15 and the new EV-16 (standard and Deep), graded blind by Fable: 18/20 critical lines, 6 pass, 2 partial (EV-03, EV-13). Grading: /mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-14-audit-fixes/GRADING.md.
- What the new rules fixed: no live bid reversal on assumed economics, business model asked first, hidden search terms not called waste.
- Regressions found and addressed in the prompt: a stop rule above a manual-bid cap (unreachable) is now checked before sending; affordable CPCs print their economics inputs; [verified] only for sources opened in the conversation, unexplained thresholds labelled a rule of thumb or dropped; at most five actions saved, one question per item, no list of saved items in the answer.
- Re-run of EV-08, 12, 13 on the new prompt, graded blind by Fable (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-14-prompt-recheck/GRADING.md): EV-13 back to PASS (stop rules reachable), EV-08 PASS with no [verified] on unopened pages, every affordable CPC recomputes from its printed inputs, answers no longer list saved items. EV-12 slipped to PARTIAL (a $20 cap above its mid affordable CPC not labelled as a loss-tolerant test, one lead-cost input appearing from nowhere). Still open: some unlabelled thresholds.
- Questions were still saved in bundles despite the prompt, so save_item now refuses a question item holding more than one question (code check, tested).

## 2026-10-14 · Niche run 9: personal injury law firm, Houston (Deep)
- Two turns in Deep mode on a synthetic 3-lawyer firm ($15k/month, $9k fee per car case, 1 in 8 callers sign). Answer and saved items: /mnt/project-files/allfix-runs/2026-10-14-run9-personal-injury-houston-deep.md. Fable reviewed it as a legal-PPC manager: /mnt/project-files/allfix-runs/2026-10-14-run9-review.md.
- Verdict: direction right (LSA first, no English head terms at this budget, intake before spend, Spanish test); B- on advice, C on rigour. Problems: an LSA stop rule above its own max bid, car-case break-even applied to the truck test, agency CPCs labelled observed and the top of a 4x spread used as the figure, client statements labelled verified, no review/Business Profile programme for LSA rank, Texas bar filing half answered, stale items after turn 2, ~1,100-word answers.
- Fixes: prompt (owner statements are [assumption, owner says]; agency and search-summary figures are [estimate] at most and show their spread; stop rules respect LSA and manual caps, fit their budget line and use their own segment's economics; stale items updated when a later turn changes the plan; LSA plans include the Business Profile and reviews and start when verification allows; regulated professions check their bar's rules; about 600 words). Knowledge: new market/legal-services.md with Texas Rules 7.04 and 7.05 (10-day filing, $100 per ad, homepage not exempt, contingent-fee copy not on the exempt list), from the rule text and the State Bar page. 414 entries.
- Re-run 9b on the fixed version (/mnt/project-files/allfix-runs/2026-10-14-run9b-personal-injury-houston-after-fixes.md), compared by Fable (appended to the review): advice B- to B+, rigour C to B-. Labels fixed, turn-2 stop rules reachable in their own units, $790/truck rules gone, LSA bid anchored to its economics, reviews and Business Profile in week 1, Keyword Planner gate before Search. Still open: answers ~1,050 words (the 600-word prompt rule did not hold; a code-level length check is the next lever if it persists), the Texas entries were not used (prompt now says search the knowledge base for the profession and state before the web), one bundled question passed the check (widened to would/should/could/did/has/have), turn 1 kept a dead LSA rule, a few stale items. Page fetching was refused by this test environment's proxy, so web figures came from search summaries.
- `scripts/account_check.py "<project name text>"` runs the Account check (Deep by default) on a project's uploaded exports through the running AllFix, the same as the button, and prints the answer. On the PC: `.venv\Scripts\python.exe scripts\account_check.py "Garage doors"`. Tested end to end on a throwaway project.

## 2026-10-15 · Deep falls back when Fable's limit is reached
- The Canada account check in Deep mode on Elad's PC stopped at once: Claude Code answered "You've reached your Fable limit" as a synthetic assistant message (model "<synthetic>"), which AllFix stored as the answer. Now a Deep turn refused that way before any output is re-run on the standard model, with a notice on the turn ("Deep mode's model has reached its limit... this answer uses the standard model"), and the plan-limit error is held back in Deep mode until that decides. Tests added; 107 pass.
- Learning: a due forecast can now be scored straight from the ledger ("Record what happened": what actually happened plus hit / partial / miss / unscorable), without a strategist turn. `POST /api/items/{id}/outcome` stores data.outcome (scored_by user) and closes the item (hit → confirmed, miss → refuted, partial or unscorable → done); it then drops out of the project's needs. Changing an item now also moves the project's timestamp, so the stage list reloads after a status change or a score. Tested in the API and in the browser.
- Deep mode now defaults to Opus 5.5 at maximum effort (Elad, 2026-10-15: "please use Opus 5.5"; his PC already ran that way after Fable was refused there). The fallback to the standard model stays for anyone who sets MODEL_DEEP to a model their plan refuses.
- Length: the 600-word rule in the system prompt did not hold, so every turn's project brief now ends with a short length reminder (verdict, key numbers, actions, what is needed; detail in saved items; no source list unless asked). Run 9c on the Houston law firm case (Opus 5.5 Deep, /mnt/project-files/allfix-runs/2026-10-15-run9c-personal-injury-houston-opus-deep.md): answers 948 and 974 words (were ~1,050), with stop rules reachable within their budgets and the Texas entries used (MKT-LEGAL-001/002). Shorter, not yet 600; left there for now, since the content is dense and each section is used.
- Canada project data (Elad's answers, 2026-10-15): business_model = sells the calls (owner says); busy_season = October to February (estimate); the two answered questions closed, the job-value question dropped, two plain questions added (pay per call, minimum call length).
- Learning: the forecast ledger now lists the next forecasts coming up for review with their dates (so a project shows what will be checked before anything is due; Canada has two, Nov 30 and Dec 15). Scoring a forecast as a miss or partial opens the chat with a prefilled question asking what it teaches, so the strategist records the lesson. Tested in the browser (due 1 → scored miss → 0 due, prompt prefilled, no page errors).
- Run 10 (Opus 5.5 Deep), new niche matching Elad's own model: selling garage door repair calls in Calgary, CA$4,000 test (/mnt/project-files/allfix-runs/2026-10-15-run10-garage-door-calls-calgary-deep.md). Fable review 6/10 (/mnt/project-files/allfix-runs/2026-10-15-run10-review.md): arithmetic, labels and the Canada verification answer all correct; misses were Google's call-forwarding policy (never mentioned for a call reseller), the Nov–Jan peak the test runs into, and a Keyword Planner gate checked against the best case. Fixes: new KB entry MKT-LOCAL-020 (lead and call resellers: policy risk first), prompt rules for resellers' policy risk, season bias of a test window with a spike reserve, and go/no-go gates against the mid case; call-only retirement date corrected to January 2026 (PRC-DIAG-030). KB 415 entries. Answers still 1,049 and 900 words.
- Run 10b (same case after the fixes, /mnt/project-files/allfix-runs/2026-10-15-run10b-garage-door-calls-calgary-after-fixes.md): the answer now opens with "Policy comes first" (call-forwarding policy quoted and linked, MKT-LOCAL-020), keeps a CA$1,000 cold-snap reserve, gates Keyword Planner against the mid case, notes that cold snaps may flatter November, and adds a pause rule on any policy warning. Lengths 1,012 and 1,017 words.
- Answer length: the length reminder now gives a cut order (background the user knows, assumption lists, extra scenario tables, repeated points). Run 10c (/mnt/project-files/allfix-runs/2026-10-15-run10c-garage-door-calls-calgary-length.md): 835 and 860 words (10b: 1,012 and 1,017), with the policy risk, season bias, mid-case price check and reachable stop rules all kept.
- Full eval re-run after today's changes (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-15-after-run10/GRADING.md, Fable blind): 12 PASS, 4 PARTIAL, 0 FAIL; critical lines 33/37; every cited KB id exists and every economics figure reproduces. Regression: the shorter answers dropped second-tier content (EV-13, EV-14 PASS → PARTIAL). Fixes: before/after figures get every fitting explanation with the report that tests it; plans whose success is a later stage (qualified call, booked job) name the measurement chain; the length rule never cuts those two; research that doesn't need the city comes first when the city is unknown; KB riders for emergency "how to fix" negatives (PLT-KW-022) and the Israeli Shabbat schedule (MKT-ISR-011). Seven affected cases re-run (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-15-recheck/), grading pending.
- Recheck of the seven affected cases (/mnt/project-files/allfix-kb/evals/runs/app-run-2026-10-15-recheck/GRADING.md, Fable blind): 5 PASS, 2 PARTIAL (morning: 3 / 4), critical 17/19 (was 15/19); EV-13 and EV-14 back to PASS, no padding from the new rules, +4.6% words of restored substance. Still failing for six runs: EV-01 "how to fix" caveat (the rider sat outside the entry's claim, which retrieval shows; now moved into the claims of PLT-KW-022 and PLT-KW-029) and EV-03 research before structure. Smaller slips: EV-14 presumes a tROAS again, EV-05 adds an AI Max check that doesn't apply.
- EV-01's six-run miss fixed with a reasoning rule: before negating a group of searches or calling it waste, check whether it converted; in emergency trades "how to fix" searches sometimes become calls (PLT-KW-022). Re-run EV-01 now says "Before blocking 'how to fix water heater', check whether any of it turned into calls"; EV-09 unchanged in shape.
- Traffic without conversion data (Elad's question, 2026-10-15): new keyword_gaps tool (intelligence/gaps.py) finds searches in an uploaded search terms report that bring clicks but are not keywords, merged across campaigns, and the words no keyword covers; read_file's where now takes exact text ('Added/Excluded = None'). New prompt section "Growing qualified traffic without conversion data": qualified clicks at the lowest CPC, proxies until tracking works, then keywords to add, cut, bids and budgets, leaking settings, ads and website. Tested (115 passed).
- Growth plan for every project (Elad, 2026-10-15): every account review, niche research and plan now ends with a growth plan aimed at qualified clicks at the lowest CPC, in six parts saved as stage-5 opportunities with data.plan_part (keywords_add, keywords_cut, bids_budgets, settings, ads, website); the objective changes the emphasis, not whether the plan exists. `GET /api/projects/{id}/growth-plan` returns the parts and which are missing; the project brief tells the strategist what is missing. `scripts/account_check.py "<project>" --growth` builds it on a project's uploaded exports.
