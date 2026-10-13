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
        assert client.get("/api/health").json()["knowledge_entries"] == 411
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
