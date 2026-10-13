"""Run the evaluation cases (knowledge/evals/cases.md) through a running AllFix server.

Each case gets a throwaway project and one strategist turn; the answer, the tools used and the
items saved are written to evals-out/<timestamp>/. Grading against the rubrics is a separate step
(a reviewer reads the answers next to cases.md), so the strategist never sees the rubric.

    python scripts/run_evals.py                  # all cases, Standard mode
    python scripts/run_evals.py EV-01 EV-09      # some cases
    python scripts/run_evals.py --deep --keep    # Deep mode; keep the eval projects

It uses the strategist for real, so each case counts against the Claude plan's usage.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "knowledge" / "evals" / "cases.md"


def parse_cases(text: str) -> dict[str, str]:
    """Case id -> what the strategist is shown (situation and question, never the rubric)."""
    cases: dict[str, str] = {}
    for m in re.finditer(r"^#{2,3} (EV-\d+) · (.+?)\n(.*?)(?=^#{2,3} |\Z)", text, re.S | re.M):
        cid, body = m.group(1), m.group(3)
        if "**Situation.**" in body:
            body = body[body.index("**Situation.**"):]
            body = body.split("**Rubric.**")[0]
            body = re.sub(r"^\*Correction after.*?$", "", body, flags=re.M)
        else:  # short cases: the situation is the evidence line, up to "Strong answer"
            body = re.sub(r"^\*\*Evidence:\*\* synthetic\.\s*", "", body.strip())
            body = body.split("Strong answer")[0]
            body = body.split("\n---")[0]
        body = body.strip()
        if "**Question.**" not in body:
            body += '\n\n"What do you think is going on, and what should we do?"'
        cases[cid] = body
    return cases


def run_case(base: str, cid: str, prompt: str, mode: str, keep: bool, out: Path) -> dict:
    with httpx.Client(base_url=base, timeout=httpx.Timeout(30, read=1800), trust_env=False) as c:
        project = c.post("/api/projects", json={"name": f"Eval {cid}", "entry_path": "ads_account",
                                                "notes": "Evaluation case, synthetic."}).json()
        conv = c.post(f"/api/projects/{project['id']}/conversations", json={"title": cid}).json()
        started = time.time()
        events = []
        with c.stream("POST", f"/api/conversations/{conv['id']}/chat",
                      json={"message": prompt, "mode": mode}) as r:
            for line in r.iter_lines():
                if line.startswith("data: "):
                    events.append(json.loads(line[6:]))
        items = c.get(f"/api/projects/{project['id']}/items").json()
        if not keep:
            c.delete(f"/api/projects/{project['id']}")
    answer = "".join(e.get("text", "") for e in events if e["type"] == "text")
    tools = [e.get("name") for e in events if e["type"] == "tool_start"]
    errors = [e for e in events if e["type"] == "error"]
    secs = round(time.time() - started)
    (out / f"{cid}.md").write_text(
        f"# {cid}\n\nMode: {mode} · {secs}s · {len(tools)} tool calls: {', '.join(tools)}\n\n"
        f"## Prompt\n\n{prompt}\n\n## Answer\n\n{answer}\n\n## Items saved ({len(items)})\n\n"
        + "\n".join(f"- {i['kind']} [{i['label']}/{i['confidence']}]: {i['title']}" for i in items)
        + ("\n\n## Errors\n\n" + json.dumps(errors, indent=1) if errors else "") + "\n",
        encoding="utf-8")
    return {"case": cid, "seconds": secs, "tools": len(tools), "items": len(items), "errors": len(errors)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="*")
    ap.add_argument("--deep", action="store_true")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--base", default="http://127.0.0.1:8000")
    ap.add_argument("--parallel", type=int, default=3)
    a = ap.parse_args()
    cases = parse_cases(CASES.read_text(encoding="utf-8"))
    chosen = {k: v for k, v in cases.items() if not a.cases or k in a.cases}
    if not chosen:
        print("no matching cases; known:", ", ".join(cases))
        return 2
    out = ROOT / "evals-out" / datetime.now().strftime("%Y%m%d-%H%M")
    out.mkdir(parents=True, exist_ok=True)
    mode = "deep" if a.deep else "standard"
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as pool:
        futures = {pool.submit(run_case, a.base, k, v, mode, a.keep, out): k for k, v in chosen.items()}
        for f in cf.as_completed(futures):
            try:
                print(json.dumps(f.result()))
            except Exception as e:  # one failed case should not stop the others
                print(json.dumps({"case": futures[f], "failed": str(e)[:300]}))
    print(f"answers in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
