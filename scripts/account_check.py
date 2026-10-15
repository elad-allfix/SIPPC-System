"""Run the Account check on a project's uploaded report exports, through a running AllFix server.

Same as the Account check button: one Deep-mode turn that reads every attached export and gives
a verdict, the 3 numbers that matter and the top 5 actions. Read-only for Google Ads; it adds a
conversation and saved items to the project, as the button does.

    python scripts/account_check.py "Garage doors"            # project name contains this text
    python scripts/account_check.py "Garage doors" --standard # Standard mode instead of Deep
    python scripts/account_check.py "Garage doors" --growth   # the growth plan instead of the check

It uses the strategist for real, so it counts against the Claude plan's usage.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date

import httpx

# Keep in step with ACCOUNT_CHECK in frontend/src/components/Chat.tsx.
ACCOUNT_CHECK = ("Account check: read every attached report. First say what each file covers (report type, "
                 "date range, its own totals) and whether conversion tracking can be trusted. Then give one verdict line, "
                 "the 3 numbers that matter most, and the top 5 actions in order. Mark each number as observed from a file or estimated.")

GROWTH_PLAN = ("Growth plan: build or update this project's growth plan from every attached report, aimed at more "
               "qualified clicks at the lowest cost per click. Find keyword gaps with keyword_gaps, then cover all six "
               "parts (keywords to add, searches to cut or bid down, bids and budgets, settings, ads, website) and "
               "save each move with its plan_part. Say whether conversions can be trusted and, if not, which proxies "
               "you judge by.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", help="text the project's name contains")
    ap.add_argument("--standard", action="store_true", help="Standard mode instead of Deep")
    ap.add_argument("--growth", action="store_true", help="build the growth plan instead of the account check")
    ap.add_argument("--base", default="http://127.0.0.1:8000")
    a = ap.parse_args()
    with httpx.Client(base_url=a.base, timeout=httpx.Timeout(30, read=3600), trust_env=False) as c:
        try:
            projects = c.get("/api/projects").json()
        except httpx.ConnectError:
            print(f"AllFix is not running at {a.base}. Start it, then run this again.")
            return 1
        found = [p for p in projects if a.project.lower() in p["name"].lower()]
        if len(found) != 1:
            print(f"Need exactly one project whose name contains {a.project!r}; found {[p['name'] for p in found]}")
            return 1
        p = found[0]
        files = c.get(f"/api/projects/{p['id']}/files").json()
        if not files:
            print(f"{p['name']} has no uploaded exports.")
            return 1
        mode = "standard" if a.standard else "deep"
        conv = c.post(f"/api/projects/{p['id']}/conversations",
                      json={"title": f"{'Growth plan' if a.growth else 'Account check'} ({mode}, {date.today().isoformat()})"}).json()
        message = "\n".join([GROWTH_PLAN if a.growth else ACCOUNT_CHECK] + [f"[Attached: {f['name']} (file {f['id']})]" for f in files])
        print(f"{p['name']}: {len(files)} files, {mode} mode, conversation {conv['id']}. This can take 10+ minutes.", flush=True)
        started, text, tools, errors = time.time(), "", 0, []
        with c.stream("POST", f"/api/conversations/{conv['id']}/chat", json={"message": message, "mode": mode}) as r:
            for line in r.iter_lines():
                if not line.startswith("data: "):
                    continue
                e = json.loads(line[6:])
                if e["type"] == "tool_start":
                    tools += 1
                    text = ""
                elif e["type"] == "text":
                    text += e.get("text", "")
                elif e["type"] == "error":
                    errors.append(e.get("message"))
        print(f"Finished in {round(time.time() - started)}s with {tools} tool calls and {len(errors)} errors {errors or ''}")
        print("\n" + text.strip())
        print(f"\nOpen the project in AllFix to see the conversation and saved items.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
