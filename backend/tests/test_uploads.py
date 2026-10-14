from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from allfix import store
from allfix.intelligence import tables, uploads
from allfix.main import create_app
from allfix.strategist.prompt import project_brief
from allfix.strategist.tools import ToolContext, run_tool, run_tool_blocks

from conftest import reset_schema
from fakes import FakeModelClient

EXPORTS = Path(__file__).parent / "fixtures" / "exports"
PNG = (b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4"
       b"\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82")


def test_google_ads_export_preamble_totals_and_footer():
    t = tables.parse((EXPORTS / "search_terms_en.csv").read_bytes())
    assert t.preamble == ["Search terms report", '"October 1, 2026 - October 13, 2026"']
    assert t.columns[0] == "Search term" and len(t.rows) == 5
    assert [r[0] for r in t.footer] == ["Total: Search terms", "Total: Account"]
    out = tables.query(t)
    totals = out["totals_of_matching_rows"]
    # additive columns are summed, with "1,204" and "9,632.00" parsed; rates and averages are not summed
    assert totals["Clicks"] == 1249 and totals["Cost"] == 10120.7 and totals["Conversions"] == 15.04
    assert not {"CTR", "Avg. CPC", "Conv. rate", "Cost / conv."} & totals.keys()
    assert out["total_rows_in_file"][1]["Search term"] == "Total: Account"


def test_filter_sort_page_and_columns():
    t = tables.parse((EXPORTS / "search_terms_en.csv").read_bytes())
    out = tables.query(t, sort_by="cost", columns=["Search term", "Cost"], limit=2)
    assert [r["Search term"] for r in out["rows"]] == ["plumber near me, open now", "water heater replacement phoenix"]
    assert out["rows"][0].keys() == {"Search term", "Cost"}
    assert "offset=2" in out["more"]
    out = tables.query(t, contains="FREE")
    assert out["rows_matching"] == 1 and out["totals_of_matching_rows"]["Cost"] == 54.9
    # a column with "--" cells still sorts numerically, blanks last
    out = tables.query(t, sort_by="Conversions", descending=True)
    assert out["rows"][0]["Conversions"] == "12.04" and out["rows"][-1]["Conversions"].strip() == "--"
    with pytest.raises(ValueError):
        tables.query(t, sort_by="nonexistent")


def test_hebrew_utf16_tab_export():
    t = tables.parse((EXPORTS / "search_terms_he_excel.csv").read_bytes())
    assert t.delimiter == "\t" and t.columns[0] == "מונח חיפוש" and len(t.rows) == 2
    assert len(t.footer) == 1
    totals = tables.query(t)["totals_of_matching_rows"]
    assert totals["עלות"] == 462.1 and totals["קליקים"] == 43
    assert "עלות ממוצעת לקליק" not in totals and "שיעור המרה" not in totals


def test_numbers():
    assert tables.number("₪1,234.50") == 1234.5
    assert tables.number(" --") is None and tables.number("< 10%") is None
    assert tables.number("(12.5)") == -12.5 and tables.number("8.57%") == 8.57


def test_upload_check_refuses_with_a_reason():
    assert uploads.check("a.CSV", 10) == "text/csv"
    assert uploads.check("shot.jpeg", 10) == "image/jpeg"
    for name, size in (("r.xlsx", 10), ("r.pdf", 10), ("r.exe", 10), ("a.csv", 0), ("b.png", 6 * 1024 * 1024)):
        with pytest.raises(uploads.UploadRefused):
            uploads.check(name, size)


async def test_read_file_tool_and_brief(database):
    p = await store.create_project({"name": "Plumber"})
    other = await store.create_project({"name": "Other"})
    f = await store.add_file(p["id"], "search_terms_en.csv", "text/csv", (EXPORTS / "search_terms_en.csv").read_bytes())
    img = await store.add_file(p["id"], "serp.png", "image/png", PNG)
    ctx = ToolContext(project_id=p["id"], conversation_id="")

    brief = await project_brief(p["id"])
    assert "search_terms_en.csv" in brief and f["id"] in brief

    text, err = await run_tool(ctx, "read_file", {"file_id": f["id"], "sort_by": "Cost", "limit": 1})
    assert not err and "plumber near me, open now" in text and "October 1, 2026" in text
    blocks, err = await run_tool_blocks(ctx, "read_file", {"file_id": img["id"]})
    assert not err and blocks[1]["type"] == "image" and blocks[1]["mimeType"] == "image/png"

    # another project's file and a malformed id are refused, not leaked or crashed
    _, err = await run_tool(ToolContext(project_id=other["id"], conversation_id=""), "read_file", {"file_id": f["id"]})
    assert err
    _, err = await run_tool(ctx, "read_file", {"file_id": "not-a-uuid"})
    assert err


def test_upload_api():
    reset_schema()
    client = TestClient(create_app(model_client_factory=lambda: FakeModelClient([])))
    with client:
        p = client.post("/api/projects", json={"name": "Files"}).json()
        data = (EXPORTS / "jobs.csv").read_bytes()
        r = client.post(f"/api/projects/{p['id']}/files", params={"name": "jobs.csv"}, content=data)
        assert r.status_code == 201 and r.json()["size_bytes"] == len(data) and "content" not in r.json()
        r = client.post(f"/api/projects/{p['id']}/files", params={"name": "report.xlsx"}, content=b"x")
        assert r.status_code == 415 and "CSV" in r.json()["detail"]
        files = client.get(f"/api/projects/{p['id']}/files").json()
        assert [x["name"] for x in files] == ["jobs.csv"]
        assert client.delete(f"/api/projects/{p['id']}/files/{files[0]['id']}").status_code == 204
        assert client.get(f"/api/projects/{p['id']}/files").json() == []
