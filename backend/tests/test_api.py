import json

from fastapi.testclient import TestClient

from allfix.main import create_app

from conftest import reset_schema
from fakes import FakeModelClient, text, tool


def _client(script):
    reset_schema()
    fake = FakeModelClient(script)
    return TestClient(create_app(model_client_factory=lambda: fake)), fake


def _events(resp):
    out = []
    for chunk in resp.text.split("\n\n"):
        for line in chunk.splitlines():
            if line.startswith("data: "):
                out.append(json.loads(line[6:]))
    return out


def test_project_flow_and_chat_stream():
    client, fake = _client([
        ([tool("t1", "update_project", {"facts": [{"key": "average_job_value", "value": "90-140 USD",
                                                    "label": "assumption", "source": "user said"}]})], "tool_use"),
        ([text("Noted the job value.")], "end_turn"),
    ])
    with client:
        assert client.get("/api/health").json()["knowledge_entries"] == 414
        assert len(client.get("/api/stages").json()) == 7
        p = client.post("/api/projects", json={"name": "Pet grooming", "objective_type": "leads"}).json()
        assert p["stage_counts"].keys() == {str(i) for i in range(1, 8)}
        conv = client.post(f"/api/projects/{p['id']}/conversations", json={}).json()
        r = client.post(f"/api/conversations/{conv['id']}/chat", json={"message": "Average job is 90-140"})
        assert r.status_code == 200
        evs = _events(r)
        assert evs[-1]["type"] == "done"
        p2 = client.get(f"/api/projects/{p['id']}").json()
        assert p2["facts"][0]["key"] == "average_job_value"
        turns = client.get(f"/api/conversations/{conv['id']}/messages").json()
        assert [t["role"] for t in turns] == ["user", "assistant"]
        assert turns[1]["text"] == "Noted the job value."
        assert turns[1]["activity"][0]["name"] == "update_project"
        convs = client.get(f"/api/projects/{p['id']}/conversations").json()
        assert convs[0]["title"] == "Average job is 90-140"


def test_knowledge_endpoints():
    client, _ = _client([])
    with client:
        r = client.get("/api/knowledge/search", params={"q": "break-even ROAS margin"}).json()
        assert r["entries"]
        e = client.get("/api/knowledge/PLT-AUC-009").json()
        assert e["id"] == "PLT-AUC-009" and "Quality Score" in e["body"]
        assert client.get("/api/knowledge/playbooks/strategic").json()["id"] == "playbooks/strategic"
        assert client.get("/api/knowledge/NOPE-XX-001").status_code == 404


def test_chat_without_api_key_reports_setup_error():
    reset_schema()
    def broken():
        raise RuntimeError("no api key")
    client = TestClient(create_app(model_client_factory=broken))
    with client:
        p = client.post("/api/projects", json={"name": "X"}).json()
        conv = client.post(f"/api/projects/{p['id']}/conversations", json={}).json()
        evs = _events(client.post(f"/api/conversations/{conv['id']}/chat", json={"message": "hi"}))
        assert evs[0]["type"] == "error" and "ANTHROPIC_API_KEY" in evs[0]["message"]


def test_overview_lists_projects_with_needs():
    client, _ = _client([
        ([tool("t1", "save_item", {"kind": "question", "title": "What is the close rate?", "label": "unknown", "body": "-", "confidence": "low"}),
          tool("t2", "save_item", {"kind": "decision", "title": "Fix tracking first", "label": "hypothesis", "body": "-", "confidence": "medium"}),
          tool("t3", "save_item", {"kind": "forecast", "title": "10-20 leads in month 1", "label": "hypothesis",
                                   "body": "-", "confidence": "low", "data": {"review_after": "2000-01-01", "prediction": "10-20", "metric": "leads"}})], "tool_use"),
        ([text("Saved.")], "end_turn"),
    ])
    with client:
        empty = client.post("/api/projects", json={"name": "Empty", "entry_path": "ads_account"}).json()
        p = client.post("/api/projects", json={"name": "Busy", "entry_path": "new_niche"}).json()
        conv = client.post(f"/api/projects/{p['id']}/conversations", json={}).json()
        client.post(f"/api/conversations/{conv['id']}/chat", json={"message": "go"})
        cards = {c["name"]: c for c in client.get("/api/overview").json()}
        assert set(cards) == {"Empty", "Busy"}
        e = cards["Empty"]
        assert e["item_total"] == 0 and e["plan"] is None and e["file_count"] == 0
        assert [n["text"] for n in e["needs"]] == [
            "Run the account check on the report exports", "Upload the account's report exports", "Add the website address"]
        b = cards["Busy"]
        assert b["plan"] == "Fix tracking first" and b["item_total"] == 3 and b["conversation_count"] == 1
        assert [n["kind"] for n in b["needs"]] == ["check", "answer"]
        assert [n["kind"] for n in b["missing"]] == ["check", "answer"] and b["findings"] == []
        assert e["missing"] == e["needs"]
        assert client.get(f"/api/projects/{p['id']}/needs").json()["plan"] == "Fix tracking first"
        assert b["item_counts"]["question"] == 1 and b["stages_with_items"]


def test_is_due():
    from datetime import date
    from allfix.store import is_due
    t = date(2026, 10, 14)
    f = lambda **d: {"kind": "forecast", "status": "open", "data": d}  # noqa: E731
    assert is_due(f(review_after="2026-10-14"), t)
    assert not is_due(f(review_after="2026-10-15"), t)
    assert not is_due(f(review_after="2026-10-01", outcome={"verdict": "hit"}), t)
    assert not is_due(f(review_after="not a date"), t) and not is_due(f(), t)
    assert is_due({"kind": "experiment", "status": "open", "data": {"review_after": "20261001"}}, t)
    assert not is_due({**f(review_after="2026-10-01"), "status": "done"}, t)


def test_economics_inputs_become_facts_and_stage_one_items_move():
    client, _ = _client([
        ([tool("t1", "update_project", {"facts": [{"key": "value_per_customer (garage doors)", "value": "400 CAD",
                                                    "label": "observed", "source": "owner"}]}),
          tool("t2", "calculate_economics", {"conversion_rate": [0.04, 0.12], "value_per_customer": [250, 600],
                                             "contribution_margin": 0.5, "segment": "garage doors", "currency": "CAD",
                                             "labels": {"contribution_margin": "estimate"}}),
          tool("t3", "save_item", {"kind": "finding", "stage": 1, "title": "Calls not tracked", "body": "-",
                                   "label": "observed", "confidence": "high"})], "tool_use"),
        ([text("Done.")], "end_turn"),
    ])
    with client:
        p = client.post("/api/projects", json={"name": "Doors"}).json()
        conv = client.post(f"/api/projects/{p['id']}/conversations", json={}).json()
        client.post(f"/api/conversations/{conv['id']}/chat", json={"message": "go"})
        facts = {f["key"]: f for f in client.get(f"/api/projects/{p['id']}").json()["facts"]}
        assert facts["value_per_customer (garage doors)"]["value"] == "400 CAD"   # the owner's figure stays
        assert facts["conversion_rate (garage doors)"] == {**facts["conversion_rate (garage doors)"],
                                                           "value": "4%-12%", "label": "assumption"}
        assert facts["contribution_margin (garage doors)"]["label"] == "estimate"
        items = client.get(f"/api/projects/{p['id']}/items").json()
        assert [(i["title"], i["stage"]) for i in items] == [("Calls not tracked", 2)]


def test_lessons_endpoint_lists_project_and_shared():
    client, _ = _client([
        ([tool("t1", "record_lesson", {"what_was_wrong": "A", "correction": "B"}),
          tool("t2", "record_lesson", {"what_was_wrong": "C", "correction": "D", "shared": True})], "tool_use"),
        ([text("Noted.")], "end_turn"),
    ])
    with client:
        p = client.post("/api/projects", json={"name": "L"}).json()
        other = client.post("/api/projects", json={"name": "M"}).json()
        conv = client.post(f"/api/projects/{p['id']}/conversations", json={}).json()
        client.post(f"/api/conversations/{conv['id']}/chat", json={"message": "go"})
        assert {l["correction"] for l in client.get(f"/api/projects/{p['id']}/lessons").json()} == {"B", "D"}
        assert [l["correction"] for l in client.get(f"/api/projects/{other['id']}/lessons").json()] == ["D"]


def test_user_scores_a_due_forecast_without_the_strategist():
    client, _ = _client([
        ([tool("t1", "save_item", {"kind": "forecast", "title": "10-20 leads in month 1", "label": "hypothesis",
                                   "body": "-", "confidence": "low",
                                   "data": {"review_after": "2000-01-01", "prediction": "10-20", "metric": "leads"}}),
          tool("t2", "save_item", {"kind": "finding", "title": "Display wastes money", "label": "observed",
                                   "body": "-", "confidence": "high"})], "tool_use"),
        ([text("Saved.")], "end_turn"),
    ])
    with client:
        p = client.post("/api/projects", json={"name": "S"}).json()
        conv = client.post(f"/api/projects/{p['id']}/conversations", json={}).json()
        client.post(f"/api/conversations/{conv['id']}/chat", json={"message": "go"})
        items = {i["kind"]: i for i in client.get(f"/api/projects/{p['id']}/items").json()}
        assert any(n["kind"] == "check" for n in client.get(f"/api/projects/{p['id']}/needs").json()["needs"])
        r = client.post(f"/api/items/{items['forecast']['id']}/outcome", json={"actual": "14 leads", "verdict": "hit"})
        assert r.status_code == 200 and r.json()["status"] == "confirmed"
        assert r.json()["data"]["outcome"]["actual"] == "14 leads" and r.json()["data"]["prediction"] == "10-20"
        assert not any(n["kind"] == "check" for n in client.get(f"/api/projects/{p['id']}/needs").json()["needs"])
        assert client.post(f"/api/items/{items['finding']['id']}/outcome", json={"actual": "x", "verdict": "hit"}).status_code == 400
        assert client.post(f"/api/items/{items['forecast']['id']}/outcome", json={"actual": "x", "verdict": "maybe"}).status_code == 422


def test_overview_findings_put_firm_and_confident_first():
    items = [
        ("finding", "Likely: brand moved into PMax", "hypothesis", "high"),
        ("finding", "Tracking misses most calls", "observed", "high"),
        ("website_issue", "Ad price not on the page", "observed", "medium"),
        ("risk", "Health ads limits", "verified", "medium"),
        ("opportunity", "Not a finding", "observed", "high"),
    ]
    client, _ = _client([
        ([tool(f"t{i}", "save_item", {"kind": k, "title": t, "label": lab, "body": "-", "confidence": conf})
          for i, (k, t, lab, conf) in enumerate(items)], "tool_use"),
        ([text("Saved.")], "end_turn"),
    ])
    with client:
        p = client.post("/api/projects", json={"name": "F", "entry_path": "new_niche"}).json()
        conv = client.post(f"/api/projects/{p['id']}/conversations", json={}).json()
        client.post(f"/api/conversations/{conv['id']}/chat", json={"message": "go"})
        card = client.get(f"/api/projects/{p['id']}/needs").json()
        assert [f["text"] for f in card["findings"]] == [
            "Tracking misses most calls", "Ad price not on the page", "Health ads limits", "Likely: brand moved into PMax"]
        assert [f["firm"] for f in card["findings"]] == [True, True, True, False]


def test_recycle_bin_hides_restores_and_deletes_forever():
    client, _ = _client([])
    with client:
        p = client.post("/api/projects", json={"name": "Old", "entry_path": "new_niche"}).json()
        client.delete(f"/api/projects/{p['id']}")  # not in the bin: nothing happens
        assert [c["name"] for c in client.get("/api/overview").json()] == ["Old"]
        assert client.post(f"/api/projects/{p['id']}/trash").status_code == 204
        assert client.get("/api/overview").json() == [] and client.get("/api/projects").json() == []
        assert [t["name"] for t in client.get("/api/trash").json()] == ["Old"]
        assert client.post(f"/api/projects/{p['id']}/restore").status_code == 204
        assert [c["name"] for c in client.get("/api/overview").json()] == ["Old"]
        client.post(f"/api/projects/{p['id']}/trash")
        assert client.delete(f"/api/projects/{p['id']}").status_code == 204
        assert client.get("/api/trash").json() == [] and client.get(f"/api/projects/{p['id']}").status_code == 404
