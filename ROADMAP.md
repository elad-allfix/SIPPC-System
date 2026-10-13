# AllFix roadmap

Each phase ends with something that can actually be used. A phase counts as done only when its acceptance check passes against the real system.

| Phase | Builds | Acceptance check |
|---|---|---|
| 1. Foundation | Backend, database and migrations, knowledge base loaded into Postgres, projects and conversations, the seven-stage interface with chat and stage panel, local setup scripts (Windows and Linux) | Create a project, see the seven stages, search the knowledge base from the interface, and survive a restart with data intact |
| 2. Working strategist | Streaming tool loop, Opus 5.5 / Fable 5.1 modes, knowledge tools, project memory tools, economics tool, web research | With a real API key, the strategist answers a diagnostic question citing knowledge entries, saves an item, and remembers it in a new conversation |
| 3. New-niche research end to end | Research plan for `new_niche` projects; intent clusters, competitors, economics and opportunities saved per stage; follow-up questions; decisions saved | A real niche researched from an empty project produces sourced, labelled findings in stages 03 and 05 that Elad judges useful |
| 4. Website intelligence | `audit_page` tool, website journey checks, stage 04 view | The strategist audits a real site and ties issues to search intent and ads |
| 5. Secure connectivity + Google Ads read-only | Connection profiles, the fail-closed guard (PIA and Dolphin), Google Ads API read access (GAQL), account import into stage 02/04, Keyword Planner | On Elad's PC, an unverified route blocks every account call, and a verified one imports a real account the strategist can diagnose |
| 6. Ongoing intelligence | Scheduled rounds (daily account check, weekly market sweep), forecast reviews, lessons feeding back into the knowledge base | A scheduled round runs unattended and leaves a reviewed summary |

Further capabilities are added only when real use shows they are needed.

## Status (2026-10-13)

| Phase | State | What was checked |
|---|---|---|
| 1. Foundation | Built and tested | 23 backend tests pass; a fresh clone sets up with `scripts/setup.sh` and serves the app; interface smoke-tested in a browser (create project, chat stream, stage panel, reload keeps data, dark theme, knowledge search). The schema was dry-run on the Supabase database (Postgres 17) and rolled back. `setup.ps1` and `backup.ps1` have not been run on Windows yet. |
| 2. Working strategist | Built, plumbing tested, not yet run against the real model | Tool loop, persistence, interrupted turns, errors and refusals are tested with a scripted model. The real client passes SDK validation and reaches the API (rejected only for the missing key). Answer quality is unverified until an `ANTHROPIC_API_KEY` is set. |
| 3. New-niche research | Research procedure written into the strategist prompt; not yet run | Needs the API key, then one real niche researched and judged by Elad. |
| 4–6 | Not started | |
