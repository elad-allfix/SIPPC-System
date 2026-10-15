import json
import time

from fastapi.testclient import TestClient

from allfix.intelligence import stage_view
from allfix.main import create_app

from conftest import reset_schema
from fakes import FakeModelClient

VIEW = {
    "verdict": "Price and focus, not waste.",
    "kpis": [{"icon": "money", "value": "CA$1.25M", "label": "Spent, lifetime", "tone": "neutral", "evidence": "observed"},
             {"icon": "nonsense", "value": "34.5%", "label": "Hidden searches", "tone": "awful"}],
    "blocks": [
        {"type": "ad", "title": "Your ads", "icon": "ad", "url": "example.ca", "headline": "$19.99 Garage Guy",
         "highlight": "$19.99", "flags": [{"text": "Page shows $50-$100", "tone": "bad"}]},
        {"type": "page", "title": "Landing page", "icon": "page", "url": "example.ca", "heading": "Garage Door Repair",
         "score": {"value": 168, "label": "Mobile-friendly"}, "cta_after_words": 142},
        {"type": "timeline", "title": "Bids", "icon": "calendar", "steps": [{"date": "Oct 2", "label": "Halved"}]},
        {"type": "chart3d", "title": "Unknown block"},
    ],
}


def test_clean_keeps_known_shapes_only():
    v = stage_view.clean(VIEW, set())
    assert v["kpis"][1]["icon"] == "chart" and v["kpis"][1]["tone"] == "neutral"
    assert [b["type"] for b in v["blocks"]] == ["ad", "page"]  # one-step timeline and unknown type dropped
    assert v["blocks"][1]["score"]["value"] == 100
    assert stage_view.parse("Here it is:\n```json\n" + json.dumps(VIEW) + "\n```")["verdict"]


def test_view_is_written_once_and_rewritten_when_the_stage_changes():
    reset_schema()
    prompts = []

    async def writer(prompt):
        prompts.append(prompt)
        return json.dumps(VIEW), "fake-model"

    app = create_app(model_client_factory=lambda: FakeModelClient([]))
    app.state.stage_view_writer = writer
    with TestClient(app) as client:
        p = client.post("/api/projects", json={"name": "Garage doors"}).json()
        url = f"/api/projects/{p['id']}/stages/4/view"
        empty = client.get(url).json()
        assert empty["empty"] and empty["fresh"] and empty["view"] is None
        assert client.get(f"/api/projects/{p['id']}/stages/7/view").status_code == 404

        from allfix import store
        item = client.portal.call(store.create_item, p["id"], {"stage": 4, "kind": "finding", "title": "Ad promises $19.99",
                                                               "body": "", "label": "observed"})
        assert client.get(url).json()["fresh"] is False
        client.post(url)
        for _ in range(50):
            s = client.get(url).json()
            if not s["generating"]:
                break
            time.sleep(0.05)
        assert s["fresh"] and s["view"]["verdict"] == "Price and focus, not waste." and not s["error"]
        assert "Ad promises $19.99" in prompts[0] and "Website & ads" in prompts[0]
        client.post(url)  # nothing changed: no second call
        assert len(prompts) == 1
        client.patch(f"/api/items/{item['id']}", json={"status": "dropped"})
        assert client.get(url).json()["fresh"] is True  # a closed item leaves nothing to show


def test_slow_page_gives_up_and_all_changed_stages_start(monkeypatch):
    reset_schema()
    monkeypatch.setattr(stage_view, "TIMEOUT", 0.2)

    async def slow(prompt):
        import asyncio
        await asyncio.sleep(5)
        return "{}", "fake"

    app = create_app(model_client_factory=lambda: FakeModelClient([]))
    app.state.stage_view_writer = slow
    with TestClient(app) as client:
        p = client.post("/api/projects", json={"name": "Garage doors"}).json()
        from allfix import store
        for stage in (4, 5):
            client.portal.call(store.create_item, p["id"], {"stage": stage, "kind": "finding", "title": f"x{stage}",
                                                            "body": "", "label": "observed"})
        assert client.post(f"/api/projects/{p['id']}/views/refresh").json()["started"] == [4, 5]
        for _ in range(60):
            s = client.get(f"/api/projects/{p['id']}/stages/5/view").json()
            if not s["generating"]:
                break
            time.sleep(0.05)
        assert not s["generating"] and "longer than" in s["error"] and s["view"] is None
