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
    assert t.preamble == ["Search terms report", "October 1, 2026 - October 13, 2026"]
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


def test_more_number_formats():
    assert tables.number("CA$1,234.50") == 1234.5 and tables.number("US$12") == 12
    assert tables.number("1.234,50 €") == 1234.5 and tables.number("12,5") == 12.5
    assert tables.number("1,234,567") == 1234567 and tables.number("-3.5") == -3.5
    assert tables.number("CAD 40.00") == 40 and tables.number("garage door") is None
    assert tables.number("1.234.567") == 1234567 and tables.number("nan") is None and tables.number("inf") is None


def test_cells_with_line_breaks_are_not_glued():
    data = ('Change history\nDate & time,User,Campaign,Changes\n'
            '"Oct 1, 2026 10:00",a@b.com,Calgary,"Headline 1 changed\nfrom: Fast Repair\nto: 24/7 Repair"\n'
            '"Oct 2, 2026 11:00",a@b.com,Edmonton,Budget changed\n').encode()
    t = tables.parse(data)
    assert len(t.rows) == 2 and t.rows[0][3] == "Headline 1 changed\nfrom: Fast Repair\nto: 24/7 Repair"
    assert tables.report_type(t) == "change history"


def test_money_listed_at_several_levels_is_flagged():
    data = ("Asset report\nAsset,Level,Campaign,Clicks,Cost\n"
            "Call now,Account,,100,\"CA$1,000.00\"\n"
            "Call now,Campaign,Calgary,100,\"CA$1,000.00\"\n"
            "Free quote,Ad group,Calgary,50,CA$500.00\n"
            "Total: Account,,,150,\"CA$1,500.00\"\n").encode()
    out = tables.query(tables.parse(data))
    assert out["report_type"] == "ads and assets"
    assert out["totals_mismatch"]["Cost"] == {"rows_add_up_to": 2500.0, "file_total_says": 1500.0}
    assert "totals_warning" in out and out["totals_by_level"]["Account"]["Cost"] == 1000.0
    assert tables.query(tables.parse((EXPORTS / "search_terms_en.csv").read_bytes())).get("report_type") == "search terms"


def test_level_totals_stay_fast_and_broken_quotes_fall_back_to_text():
    import time
    rows = "".join(f"a{i},{('Account', 'Campaign', 'Ad group')[i % 3]},{i % 9},1.5\n" for i in range(5000))
    t0 = time.time()
    out = tables.query(tables.parse(("Asset,Level,Clicks,Cost\n" + rows).encode()))
    assert time.time() - t0 < 5 and set(out["totals_by_level"]) == {"Account", "Campaign", "Ad group"}
    broken = ('Name,Notes\nA,"5 ft pipe\n' + "B,ok\n" * 70000).encode()
    parsed = uploads._load({"id": "broken", "content": broken})
    assert isinstance(parsed, (str, tables.Table))
    uploads.forget("broken")


def test_large_export_is_reduced_with_a_true_account_of_what_was_kept():
    rows = ["Search terms report", "October 1, 2020 - October 13, 2026",
            "Search term\tCampaign\tImpr.\tClicks\tCost\tConversions"]
    for i in range(3000):
        cost = f"CA${i % 7 * 1.5:.2f}" if i % 3 == 0 else "CA$0.00"
        conv = "1.00" if i == 1 else "0.00"
        rows.append(f"term {i}\tCalgary\t10\t{1 if i % 3 == 0 else 0}\t{cost}\t{conv}")
    rows.append("Total: Account\t\t30000\t1000\tCA$4,498.50\t1.00")
    data = "\r\n".join(rows).encode("utf-16")
    reduced, note = tables.reduce(data, 10_000_000)
    t = tables.parse(reduced)
    # every row with cost or conversions survives; zero rows are dropped and counted
    assert len(t.rows) == 857 + 1 and note.startswith(tables.REDUCED_MARK)
    assert "100.0% of its cost and 100.0% of its conversions" in note
    assert any("Dropped 2,142 rows" in p for p in t.preamble)
    assert any("Full-file sums before reducing: cost 4,498" in p for p in t.preamble)
    assert t.footer[0][0] == "Total: Account" and t.preamble[1] == "October 1, 2020 - October 13, 2026"
    out = tables.query(t)
    assert "reduced on arrival" in out["totals_note"] and "totals_warning" not in out
    # a tight cap keeps the highest-cost rows and says what share of cost they cover
    reduced, note = tables.reduce(data, 2000)
    t = tables.parse(reduced)
    assert len(t.rows) < 858 and "highest-cost rows" in note
    assert min(tables.number(r[4]) for r in t.rows) == 9.0


# Shaped like real UI exports: title, range, header, rows (one with a line break inside a cell), totals.
ASSETS = ('Asset association report\nAll time\nAsset,Level,Clicks,Cost\n'
          '"24/7 Locksmith\nWe open any lock",Campaign,10,40.00\n"24/7 Locksmith\nWe open any lock",Ad group,10,40.00\n'
          'Call us,Campaign,5,20.00\n').encode()
TERMS = ('Search terms report\nAll time\nSearch term,Campaign,Clicks,Impr.,Cost,Conversions\n'
         'garage door repair,Calgary,30,400,"CA$150.00",1.00\ngarage door repair,Edmonton,20,300,100.00,0.00\n'
         'how to fix garage door,Calgary,8,90,40.00,0.00\nlocksmith calgary,Calgary,0,12,0.00,0.00\n'
         'Total: Search terms,,58,802,290.00,1.00\nTotal: Account,,90,1200,450.00,1.00\n').encode()


def test_report_guide_and_level_note():
    t = tables.parse(ASSETS)
    assert t.rows[0][0] == "24/7 Locksmith\nWe open any lock" and len(t.rows) == 3
    out = tables.query(t)
    assert out["report"] == "Asset association report" and "never add" in out["how_to_read"]
    assert "Level" in out["level_note"]


def test_group_by_and_where():
    t = tables.parse(TERMS)
    out = tables.query(t, group_by="Search term")
    assert out["groups"][0] == {"Search term": "garage door repair", "rows": 2, "Clicks": 50, "Impr.": 700,
                                "Cost": 250, "Conversions": 1}
    out = tables.query(t, where=["Cost > 30", "Conversions = 0"], columns=["Search term"])
    assert [r["Search term"] for r in out["rows"]] == ["garage door repair", "how to fix garage door"]
    assert "totals_check" not in out and "totals_note" not in out  # filtered: no check against the Total row
    with pytest.raises(ValueError):
        tables.query(t, where=["Cost is big"])
    assert "hidden searches" in tables.query(t)["totals_note"]  # rows sum below Total: Account
    assert tables.number("Max. CPC") is None and tables.NON_ADDITIVE.search("Default max. bid")


def test_reduced_upload_is_stored_compressed_and_reads_back(monkeypatch):
    big = TERMS.split(b"Total:")[0] + b"idle term,Calgary,0,5,0.00,0.00\n" * 2000 + b"Total:" + TERMS.split(b"Total:", 1)[1]
    monkeypatch.setattr(uploads, "STORE_BYTES", 10_000)
    assert uploads.prepare("text/csv", TERMS) == ("text/csv", TERMS, None)
    mime, stored, note = uploads.prepare("text/csv", big)
    assert stored[:2] == b"\x1f\x8b" and "kept 3 of 2,004 rows" in note
    t = tables.parse(stored)
    assert len(t.rows) == 3 and [r[0] for r in t.footer] == ["Total: Search terms", "Total: Account"]
    assert tables.query(t)["totals_of_matching_rows"]["Cost"] == 290

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
        big = ("Search term,Cost\n" + "".join(f"t{i},{i % 2}\n" for i in range(200))).encode()
        uploads.STORE_BYTES, keep = 500, uploads.STORE_BYTES
        try:
            r = client.post(f"/api/projects/{p['id']}/files", params={"name": "terms.csv"}, content=big)
        finally:
            uploads.STORE_BYTES = keep
        assert r.status_code == 201 and r.json()["size_bytes"] <= 1500 and "kept" in r.json()["note"]
        client.delete(f"/api/projects/{p['id']}/files/{r.json()['id']}")
        r = client.post(f"/api/projects/{p['id']}/files", params={"name": "report.xlsx"}, content=b"x")
        assert r.status_code == 415 and "CSV" in r.json()["detail"]
        files = client.get(f"/api/projects/{p['id']}/files").json()
        assert [x["name"] for x in files] == ["jobs.csv"]
        assert client.delete(f"/api/projects/{p['id']}/files/{files[0]['id']}").status_code == 204
        assert client.get(f"/api/projects/{p['id']}/files").json() == []
