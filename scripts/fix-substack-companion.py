#!/usr/bin/env python3
"""Upload companion diagrams to Substack CDN by URL, inject image nodes."""

import os, sys, json
from urllib.parse import unquote

try:
    import requests
except ImportError:
    import subprocess; subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

SUBSTACK_URL = "https://analyticsmusings.substack.com"
BASE_URL = "https://yadavillidotcom.yakarteek.workers.dev"
SESSION_COOKIE = os.environ.get("SUBSTACK_SESSION_COOKIE", "")
POST_ID = sys.argv[1] if len(sys.argv) > 1 else "200844099"

DIAGRAMS = [
    {"file": "ai-pattern-verb-grid.svg",   "anchor": "the irreducible operation the AI performs"},
    {"file": "ai-pattern-closure-test.svg", "anchor": "only the fourth can grow the set"},
    {"file": "ai-pattern-nine-map.svg",     "anchor": "honest taxonomy is allowed to claim"},
]


def build_session(cookie_raw):
    cookie = unquote(cookie_raw)
    s = requests.Session()
    s.cookies.set("substack.sid", cookie, domain="substack.com")
    s.cookies.set("substack.sid", cookie, domain="analyticsmusings.substack.com")
    s.get("https://substack.com/sign-in?redirect=%2F&for_pub=analyticsmusings")
    return s


def upload_by_url(session, url):
    r = session.post(f"{SUBSTACK_URL}/api/v1/image", json={"image": url}, timeout=30)
    r.raise_for_status()
    d = r.json()
    return d["url"], d.get("imageWidth", 900), d.get("imageHeight", 580)


def image_node(src, w, h):
    return {"type": "paragraph", "attrs": {"textAlign": None}, "content": [{
        "type": "image",
        "attrs": {"src": src, "fullscreen": False, "imageSize": "large", "height": h,
                  "width": w, "resizeWidth": w, "bytes": None, "alt": None, "title": None,
                  "type": None, "href": None, "belowTheFold": False, "topImage": False,
                  "internalRedirect": None, "isProcessing": False, "align": "center"}}]}


def has_text(node, text):
    if isinstance(node, dict):
        if node.get("type") == "text" and text in node.get("text", ""):
            return True
        return any(has_text(c, text) for c in node.get("content", []))
    return False


if __name__ == "__main__":
    if not SESSION_COOKIE:
        print("SUBSTACK_SESSION_COOKIE not set"); sys.exit(1)
    s = build_session(SESSION_COOKIE)

    print("Uploading diagrams...")
    for d in DIAGRAMS:
        url = f"{BASE_URL}/img/diagrams/{d['file']}"
        print(f"  {d['file']} -> ", end="", flush=True)
        d["cdn"], d["w"], d["h"] = upload_by_url(s, url)
        print(d["cdn"])

    print(f"\nFetching draft {POST_ID}...")
    r = s.get(f"{SUBSTACK_URL}/api/v1/drafts/{POST_ID}", timeout=15); r.raise_for_status()
    post = r.json()
    doc = json.loads(post["draft_body"]) if isinstance(post["draft_body"], str) else post["draft_body"]

    print("Injecting image nodes...")
    new_content, done = [], set()
    for node in doc.get("content", []):
        new_content.append(node)
        for d in DIAGRAMS:
            if d["file"] not in done and has_text(node, d["anchor"]):
                new_content.append(image_node(d["cdn"], d["w"], d["h"]))
                done.add(d["file"])
                print(f"  inserted {d['file']}")
    doc["content"] = new_content

    missing = [d["file"] for d in DIAGRAMS if d["file"] not in done]
    if missing:
        print("WARNING anchors not found for:", missing)

    print(f"\nUpdating draft {POST_ID}...")
    r = s.put(f"{SUBSTACK_URL}/api/v1/drafts/{POST_ID}", json={"draft_body": json.dumps(doc)}, timeout=30)
    if r.status_code not in (200, 201):
        print(f"Update failed {r.status_code}: {r.text[:300]}"); sys.exit(1)
    print(f"Done: {SUBSTACK_URL}/p/{POST_ID}")
