"""Connection profiles and the verification log (Stage 01)."""

from __future__ import annotations

import json

from .. import db
from .guard import Profile, Verification

FIELDS = ("ads_customer_id", "login_customer_id", "required_country", "required_region", "vpn_profile",
          "dolphin_profile_id")


def _clean(row: dict | None) -> dict | None:
    if row is None:
        return None
    return {k: (v.isoformat() if hasattr(v, "isoformat") else str(v) if k in ("id", "project_id") else v)
            for k, v in row.items()}


async def get(project_id: str) -> dict | None:
    return _clean(await db.fetch_one("select * from connection_profiles where project_id = %s", (project_id,)))


async def upsert(project_id: str, data: dict) -> dict:
    fields = {k: (v.strip() if isinstance(v, str) else v) or None for k, v in data.items() if k in FIELDS}
    if fields.get("required_country"):
        fields["required_country"] = fields["required_country"].upper()
    if "required_country" in fields and not fields["required_country"]:
        raise ValueError("required_country can't be empty (two-letter code, e.g. US)")
    existing = await get(project_id)
    if existing is None:
        if not fields.get("required_country"):
            raise ValueError("required_country is needed (two-letter code, e.g. US)")
        cols = ", ".join(["project_id", *fields])
        vals = ", ".join(["%(project_id)s", *[f"%({k})s" for k in fields]])
        row = await db.fetch_one(f"insert into connection_profiles ({cols}) values ({vals}) returning *",
                                 {"project_id": project_id, **fields})
    else:
        sets = ", ".join(f"{k} = %({k})s" for k in fields) or "required_country = required_country"
        row = await db.fetch_one(f"update connection_profiles set {sets}, updated_at = now() "
                                 f"where project_id = %(project_id)s returning *", {"project_id": project_id, **fields})
    return _clean(row)


async def record(profile: Profile, v: Verification) -> None:
    if not profile.id:
        return
    await db.execute(
        "insert into route_checks (profile_id, ok, public_ip, country, region, checks) values (%s, %s, %s, %s, %s, %s::jsonb)",
        (profile.id, v.ok, v.public_ip, v.country, v.region, json.dumps([c.as_dict() for c in v.checks])))
    await db.execute("update connection_profiles set last_verified_at = now(), last_result = %s::jsonb where id = %s",
                     (json.dumps(v.as_dict()), profile.id))


async def record_last(guard, profile: Profile) -> None:
    """Log the guard's latest verification for this profile (used after a blocked request)."""
    last = guard._last.get(profile.id or profile.project_id)
    if last is not None:
        await record(profile, last)


async def recent_checks(project_id: str, limit: int = 10) -> list[dict]:
    rows = await db.fetch_all(
        """select rc.ok, rc.public_ip, rc.country, rc.region, rc.checks, rc.created_at from route_checks rc
           join connection_profiles cp on cp.id = rc.profile_id where cp.project_id = %s
           order by rc.created_at desc limit %s""", (project_id, limit))
    return [_clean(r) for r in rows]
