"""Files the user uploads for the strategist: report exports (CSV/TSV/TXT) and screenshots."""

from __future__ import annotations

from collections import OrderedDict
from pathlib import PurePath
from typing import Any

from . import tables

MAX_BYTES = 10 * 1024 * 1024
MAX_IMAGE_BYTES = 5 * 1024 * 1024  # the model's own limit per image
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
               ".gif": "image/gif"}
TABLE_TYPES = {".csv": "text/csv", ".tsv": "text/tab-separated-values", ".txt": "text/plain"}
ACCEPT = ", ".join(sorted(IMAGE_TYPES | TABLE_TYPES))
TEXT_PAGE = 20000

_parsed: OrderedDict[str, tables.Table | str] = OrderedDict()  # file id -> parsed table or plain text


class UploadRefused(ValueError):
    pass


def check(name: str, size: int) -> str:
    """The stored type for an upload, or UploadRefused with a reason the user can act on."""
    ext = PurePath(name).suffix.lower()
    if ext in (".xlsx", ".xls"):
        raise UploadRefused("Excel files are not read yet. In Google Ads choose Download > CSV, "
                            "or in Excel use Save as > CSV UTF-8.")
    if ext == ".pdf":
        raise UploadRefused("PDFs are not read yet. Upload a screenshot (PNG/JPG) or a CSV instead.")
    mime = IMAGE_TYPES.get(ext) or TABLE_TYPES.get(ext)
    if mime is None:
        raise UploadRefused(f"Unsupported file type. Upload one of: {ACCEPT}.")
    if size == 0:
        raise UploadRefused("The file is empty.")
    limit = MAX_IMAGE_BYTES if mime.startswith("image/") else MAX_BYTES
    if size > limit:
        raise UploadRefused(f"The file is larger than {limit // (1024 * 1024)} MB.")
    return mime


def _load(f: dict) -> tables.Table | str:
    key = f["id"]
    if key in _parsed:
        _parsed.move_to_end(key)
        return _parsed[key]
    try:
        parsed: tables.Table | str = tables.parse(f["content"])
    except ValueError:
        parsed = tables.decode(f["content"])
    _parsed[key] = parsed
    while len(_parsed) > 8:
        _parsed.popitem(last=False)
    return parsed


def forget(file_id: str) -> None:
    _parsed.pop(file_id, None)


def read(f: dict, args: dict) -> Any:
    from ..strategist.tools import ToolImage
    about = {"file": f["name"], "uploaded": f["created_at"],
             "label": "observed: user-supplied file; it may be filtered, partial or edited"}
    if f["mime"].startswith("image/"):
        return ToolImage(f["mime"], f["content"], about)
    parsed = _load(f)
    if isinstance(parsed, str):
        start = max(0, int(args.get("offset") or 0))
        out = {**about, "text": parsed[start:start + TEXT_PAGE], "characters": len(parsed)}
        if start + TEXT_PAGE < len(parsed):
            out["more"] = f"pass offset={start + TEXT_PAGE} for the next part"
        return out
    return {**about, **tables.query(parsed, args.get("contains"), args.get("sort_by"),
                                    args.get("descending", True), args.get("offset") or 0,
                                    args.get("limit") or 50, args.get("columns"))}
