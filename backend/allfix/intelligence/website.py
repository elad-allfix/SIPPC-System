"""Landing page audit: fetch one page and report what is observably on it.

Everything returned is an observation of the HTML AllFix received, not a judgement.
The strategist interprets it against search intent. Limits are stated in the result:
pages that build their content with JavaScript, block bots, or vary by visitor can
look different to a real searcher.
"""

from __future__ import annotations

import asyncio
import ipaddress
import json
import re
import socket
import time
from urllib.parse import urljoin, urlparse

import httpx
from selectolax.lexbor import LexborHTMLParser as HTMLParser

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/130.0 Safari/537.36 AllFix-audit/1.0")
MAX_BYTES = 3_000_000
TIMEOUT = 15.0

PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?\(?\b[2-9]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b|\+\d{1,3}[\s.-]?\d[\d\s.-]{6,14}\d")
PRICE_RE = re.compile(r"(?:[$€£₪]\s?\d[\d,]*(?:\.\d{2})?(?:\s?(?:-|–|to)\s?[$€£₪]?\s?\d[\d,]*(?:\.\d{2})?)?"
                      r"|\b\d[\d,]*(?:\.\d{2})?\s?(?:USD|EUR|GBP|ILS|dollars)\b)")
TRUST_PATTERNS = {
    "reviews_or_ratings": r"\b(reviews?|rated|stars?|testimonials?|★)\b",
    "guarantee": r"\b(guarantee[ds]?|money[- ]back|satisfaction)\b",
    "licensed_insured": r"\b(licensed|insured|bonded|certified|accredited)\b",
    "years_in_business": r"\b(since\s+(19|20)\d{2}|\d+\+?\s+years?)\b",
    "awards_or_press": r"\b(award|as seen (on|in)|featured in|best of)\b",
}
TRACKING_PATTERNS = {
    "google_tag_gtag": r"googletagmanager\.com/gtag/js|gtag\(",
    "google_tag_manager": r"googletagmanager\.com/gtm\.js",
    "google_ads_conversion": r"send_to['\"]?\s*:\s*['\"]AW-\d+/[\w-]+",
    "consent_mode": r"gtag\(\s*['\"]consent['\"]",
    "meta_pixel": r"connect\.facebook\.net/[^\"']*fbevents\.js|fbq\(",
    "microsoft_uet": r"bat\.bing\.com",
    "microsoft_clarity": r"clarity\.ms",
    "hotjar": r"static\.hotjar\.com|hjid",
    "call_tracking": r"callrail|calltrackingmetrics|whatconverts|invoca|marchex|ringba|dni\.js",
    "cookie_banner": r"cookiebot|onetrust|cookieyes|termly|iubenda|usercentrics|osano",
}
TAG_IDS = {"gtm": r"\bGTM-[A-Z0-9]{4,10}\b", "google_ads": r"\bAW-\d{6,12}\b", "ga4": r"\bG-[A-Z0-9]{6,12}\b"}
CAPTCHA_RE = re.compile(r"g-recaptcha|recaptcha/api|hcaptcha|cf-turnstile", re.I)
FORM_VENDORS = {"hubspot": "hsforms|hubspot", "typeform": "typeform", "jotform": "jotform", "gravity_forms": "gform_",
                "wpforms": "wpforms", "calendly": "calendly", "acuity": "acuityscheduling", "square": "squareup",
                "google_forms": "docs.google.com/forms"}
LINK_KINDS = {"service": r"service|grooming|repair|install|treatment|product", "contact": r"contact|book|schedule|appointment",
              "pricing": r"pric|cost|rates|packages|fees", "about": r"about|team|reviews|testimonial", "location": r"location|area|cities|near"}
CTA_WORDS = re.compile(r"\b(call|book|schedule|get|request|quote|start|contact|buy|order|sign up|reserve|"
                       r"free|estimate|appointment|claim|try)\b", re.I)


class AuditError(Exception):
    pass


def _proxied(scheme: str) -> bool:
    import urllib.request
    return bool(urllib.request.getproxies().get(scheme))


def _check_target(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.hostname
    if parsed.scheme not in ("http", "https") or not host:
        raise AuditError("only public http(s) URLs can be audited")
    if host == "localhost" or host.endswith((".local", ".internal", ".localhost")):
        raise AuditError("that address is private or local; only public sites can be audited")
    try:
        literal = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        literal = None
    if literal is not None:
        addresses = [literal]
    else:
        try:
            addresses = [ipaddress.ip_address(i[4][0]) for i in socket.getaddrinfo(host, None)]
        except socket.gaierror as e:
            # Behind an outbound proxy the machine may not resolve names itself; the proxy
            # connects, so local addresses on this machine are out of its reach anyway.
            if _proxied(parsed.scheme):
                return parsed.geturl()
            raise AuditError(f"could not resolve {host}") from e
    if any(not ip.is_global for ip in addresses):
        raise AuditError("that address is private or local; only public sites can be audited")
    return parsed.geturl()


BLOCK_MARKERS = {
    "cloudflare": r"cf-chl|challenge-platform|Attention Required! \| Cloudflare|Just a moment\.\.\.",
    "akamai": r"Access Denied.*akamai|Reference&#32;#",
    "perimeterx": r"px-captcha|_pxCaptcha",
    "datadome": r"datadome",
    "captcha": r"g-recaptcha|hcaptcha|cf-turnstile",
}


_transport: httpx.AsyncBaseTransport | None = None  # tests substitute a mock transport


async def fetch(url: str) -> dict:
    url = await asyncio.to_thread(_check_target, url)
    started = time.perf_counter()
    hops: list[str] = []
    async with httpx.AsyncClient(follow_redirects=False, timeout=TIMEOUT, transport=_transport,
                                 headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.8"}) as client:
        current = url
        for _ in range(8):
            # Every hop is checked before connecting, so a redirect can't reach a private address.
            await asyncio.to_thread(_check_target, current)
            async with client.stream("GET", current) as resp:
                if resp.is_redirect and resp.headers.get("location"):
                    hops.append(current)
                    current = urljoin(current, resp.headers["location"])
                    continue
                chunks, size = [], 0
                async for chunk in resp.aiter_bytes():
                    size += len(chunk)
                    chunks.append(chunk)
                    if size > MAX_BYTES:
                        break
                body = b"".join(chunks)
                h = resp.headers
                return {
                    "requested_url": url,
                    "final_url": current,
                    "status": resp.status_code,
                    "redirects": hops,
                    "seconds_to_download": round(time.perf_counter() - started, 2),
                    "bytes": size,
                    "truncated": size > MAX_BYTES,
                    "content_type": h.get("content-type", ""),
                    "http": {
                        "version": resp.http_version,
                        "server": h.get("server"),
                        "cdn_hint": next((v for k, v in (("cf-ray", "cloudflare"), ("x-vercel-id", "vercel"),
                                                         ("x-amz-cf-id", "cloudfront"), ("x-fastly-request-id", "fastly"),
                                                         ("x-served-by", "fastly"), ("x-wix-request-id", "wix"),
                                                         ("x-shopify-stage", "shopify")) if k in h), None),
                        "cache_control": h.get("cache-control"),
                        "cookies_set": len(resp.headers.get_list("set-cookie")),
                    },
                    "html": body.decode(resp.encoding or "utf-8", errors="replace"),
                }
    raise AuditError("too many redirects")


def _text(node) -> str:
    return re.sub(r"\s+", " ", node.text(separator=" ", strip=True)).strip() if node else ""


def analyse(html: str, base_url: str, intent: str | None = None, ad_headline: str | None = None) -> dict:
    tree = HTMLParser(html)
    raw_html = html
    for tag in tree.css("script, style, noscript, template, svg"):
        if tag.tag == "script" and (tag.attributes.get("type") or "") == "application/ld+json":
            continue
        tag.decompose()

    def meta(name: str) -> str | None:
        n = tree.css_first(f'meta[name="{name}"]') or tree.css_first(f'meta[property="{name}"]')
        return (n.attributes.get("content") or "").strip() if n else None

    canonical = tree.css_first('link[rel="canonical"]')
    body = tree.body
    schema_types: list[str] = []
    for jl in HTMLParser(raw_html).css('script[type="application/ld+json"]'):
        try:
            data = json.loads(jl.text() or "null")
        except ValueError:
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            d = stack.pop()
            if isinstance(d, dict):
                t = d.get("@type")
                if isinstance(t, str):
                    schema_types.append(t)
                elif isinstance(t, list):
                    schema_types += [x for x in t if isinstance(x, str)]
                stack += [v for v in d.values() if isinstance(v, (dict, list))]
            elif isinstance(d, list):
                stack += d
    for jl in tree.css('script[type="application/ld+json"]'):
        jl.decompose()

    text = _text(body)
    words = len(text.split())
    h1 = [_text(n) for n in tree.css("h1")][:5]
    h2 = [_text(n) for n in tree.css("h2")][:15]

    tel_links = sorted({(a.attributes.get("href") or "")[4:].strip() for a in tree.css('a[href^="tel:"]')} - {""})
    phones_in_text = sorted({m.group(0).strip() for m in PHONE_RE.finditer(text)})[:10]

    forms = []
    for f in tree.css("form")[:10]:
        fields = []
        for inp in f.css("input, select, textarea"):
            itype = (inp.attributes.get("type") or inp.tag).lower()
            if itype in ("hidden", "submit", "button", "image", "reset"):
                continue
            fields.append({"name": inp.attributes.get("name") or inp.attributes.get("id") or "",
                           "type": itype, "required": "required" in inp.attributes})
        submit = f.css_first('button, input[type="submit"]')
        action = f.attributes.get("action") or ""
        names = " ".join(f"{x['name']} {x['type']}".lower() for x in fields)
        forms.append({"fields": len(fields), "required": sum(1 for x in fields if x["required"]),
                      "asks_phone": "tel" in names or "phone" in names,
                      "asks_email": "email" in names,
                      "action_host": urlparse(urljoin(base_url, action)).hostname if action else None,
                      "field_list": fields[:15],
                      "submit_text": (_text(submit) or (submit.attributes.get("value") if submit else "") or "")[:60]})
    iframes = [i.attributes.get("src") or "" for i in tree.css("iframe")]
    form_vendors = sorted({v for v, p in FORM_VENDORS.items() if re.search(p, raw_html, re.I)})

    ctas = []
    for n in tree.css("a, button"):
        t = _text(n)
        if t and len(t) <= 60 and CTA_WORDS.search(t) and t not in ctas:
            ctas.append(t)
    first_cta_at_word = None
    if ctas:
        idx = text.find(ctas[0])
        first_cta_at_word = len(text[:idx].split()) if idx >= 0 else None

    trust = {}
    for k, p in TRUST_PATTERNS.items():
        m = re.search(p, text, re.I)
        trust[k] = {"pattern_match": bool(m),
                    "snippet": text[max(0, m.start() - 60): m.end() + 60] if m else None}
    tracking = {k: bool(re.search(p, raw_html, re.I)) for k, p in TRACKING_PATTERNS.items()}
    ids = {k: sorted(set(re.findall(p, raw_html)))[:5] for k, p in TAG_IDS.items()}
    gtm = tracking["google_tag_manager"] or bool(ids["gtm"])
    measurement = {
        "tags_seen": [k for k, v in tracking.items() if v],
        "ids": ids,
        "visibility": ("gtm_present_cannot_inspect" if gtm else
                       "observed" if any(tracking.values()) else "not_observed_static"),
        "note": ("Google Tag Manager is present: most tags (including Google Ads conversions) may load "
                 "through it and cannot be seen here. Do not conclude tracking is missing." if gtm else
                 "Only tags written into the HTML are visible here."),
    }
    prices = sorted({m.group(0).strip() for m in PRICE_RE.finditer(text)})[:15]
    imgs = tree.css("img")
    host = urlparse(base_url).hostname or ""
    internal: dict[str, str] = {}
    for a in tree.css("a[href]"):
        u = urljoin(base_url, a.attributes.get("href") or "").split("#")[0]
        if urlparse(u).hostname == host and u not in internal:
            internal[u] = _text(a)[:60]
    link_list = []
    for u, anchor in list(internal.items())[:200]:
        kinds = [k for k, p in LINK_KINDS.items() if re.search(p, f"{u} {anchor}", re.I)]
        if kinds:
            link_list.append({"url": u, "text": anchor, "looks_like": kinds})

    out = {
        "title": _text(tree.css_first("title")),
        "meta_description": meta("description"),
        "canonical": canonical.attributes.get("href") if canonical else None,
        "robots_meta": meta("robots"),
        "has_mobile_viewport": bool(meta("viewport")),
        "language": (tree.css_first("html").attributes.get("lang") if tree.css_first("html") else None),
        "h1": h1,
        "h2": h2,
        "word_count": words,
        "opening_text": text[:1500],
        "phone_links": tel_links,
        "phone_numbers_in_text": phones_in_text,
        "forms": forms,
        "calls_to_action": ctas[:15],
        "first_cta_after_words": first_cta_at_word,
        "prices_mentioned": prices,
        "schema_types": sorted(set(schema_types)),
        "trust_signals": trust,
        "measurement": measurement,
        "captcha": bool(CAPTCHA_RE.search(raw_html)),
        "form_vendors": form_vendors,
        "iframes": [i for i in iframes if i][:10],
        "images": len(imgs),
        "images_missing_alt": sum(1 for i in imgs if not (i.attributes.get("alt") or "").strip()),
        "scripts": len(HTMLParser(raw_html).css("script[src]")),
        "internal_links": len(internal),
        "notable_internal_links": link_list[:30],
        "looks_javascript_rendered": words < 80 and len(raw_html) > 20_000,
    }
    low_title, low_h1, low_text = (out["title"] or "").lower(), " ".join(h1).lower(), text.lower()
    if intent:
        terms = [t for t in re.findall(r"[a-z0-9]+", intent.lower()) if len(t) > 2]
        out["intent_terms"] = {t: {"title": t in low_title, "h1": t in low_h1, "first_300_chars": t in low_text[:300],
                                   "body_mentions": low_text.count(t)} for t in terms[:12]}
    if ad_headline:
        phrase = ad_headline.lower().strip()
        words_ = [w for w in re.findall(r"[a-z0-9]+", phrase) if len(w) > 2]
        found = [w for w in words_ if w in low_text[:1500]]
        out["ad_message_match"] = {"exact_in_title": phrase in low_title, "exact_in_h1": phrase in low_h1,
                                   "exact_in_opening_text": phrase in low_text[:1500],
                                   "headline_words_in_opening_text": f"{len(found)}/{len(words_)}",
                                   "missing_words": [w for w in words_ if w not in found]}
    return out


LIMITS = ("Observed in the raw HTML AllFix downloaded, without running JavaScript, from a data-centre "
          "connection. Content added by scripts, A/B tests, geo or device variations, and tags that load "
          "through Tag Manager are not visible. 'Not found' means not seen in this HTML, not proof of absence.")


async def audit_page(url: str, intent: str | None = None, ad_headline: str | None = None) -> dict:
    try:
        page = await fetch(url)
    except AuditError as e:
        return {"url": url, "error": str(e)}
    except httpx.HTTPError as e:
        return {"url": url, "error": f"could not fetch the page: {type(e).__name__}: {str(e)[:200]}"}
    html = page.pop("html")
    result = {**page}
    if "html" not in page["content_type"] and "<html" not in html[:2000].lower():
        result["error"] = f"not an HTML page ({page['content_type'] or 'unknown type'})"
        return result
    vendor = next((v for v, p in BLOCK_MARKERS.items() if v != "captcha" and re.search(p, html[:50000], re.I)), None)
    if page["status"] in (401, 403, 429, 503) or (vendor and len(html) < 40000):
        result["blocked"] = True
        result["block_vendor"] = vendor
        result["note"] = ("The site answered with a block or challenge page instead of its content, so it was "
                          "not audited. A real visitor may see the normal page.")
        return result
    if page["status"] >= 400:
        result["note"] = f"The server returned status {page['status']}."
    result.update(analyse(html, page["final_url"], intent, ad_headline))
    result["https"] = page["final_url"].startswith("https://")
    result["limits"] = LIMITS
    return result
