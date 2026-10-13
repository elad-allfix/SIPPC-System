# AllFix progress log

Kept up to date while building, so work can resume if a session ends. Newest first.

## 2026-10-13

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
