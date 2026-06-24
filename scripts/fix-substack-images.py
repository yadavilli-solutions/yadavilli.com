#!/usr/bin/env python3
"""Upload SVGs to Substack CDN via URL, inject image nodes into post body."""

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

POST_ID = sys.argv[1] if len(sys.argv) > 1 else "200830451"

DIAGRAMS = [
    {
        "file": "ai-product-shape.svg",
        "anchor": "The first framework maps AI patterns onto a 2x2",
        "width": 900, "height": 580,
    },
    {
        "file": "ai-adoption-readiness.svg",
        "anchor": "The second framework maps your organization",
        "width": 900, "height": 580,
    },
    {
        "file": "ai-invocation-protocols.svg",
        "anchor": "There is a third dimension most product teams discover late",
        "width": 900, "height": 500,
    },
]


def build_session(cookie_raw):
    cookie = unquote(cookie_raw)
    s = requests.Session()
    s.cookies.set("substack.sid", cookie, domain="substack.com")
    s.cookies.set("substack.sid", cookie, domain="analyticsmusings.substack.com")
    s.get("https://substack.com/sign-in?redirect=%2F&for_pub=analyticsmusings")
    return s


def upload_image_by_url(session, url):
    r = session.post(f"{SUBSTACK_URL}/api/v1/image", json={"image": url}, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["url"], data.get("imageWidth", 900), data.get("imageHeight", 580)


def make_image_node(src, width, height):
    return {
        "type": "paragraph",
        "attrs": {"textAlign": None},
        "content": [{
            "type": "image",
            "attrs": {
                "src": src,
                "fullscreen": False,
                "imageSize": "large",
                "height": height,
                "width": width,
                "resizeWidth": width,
                "bytes": None,
                "alt": None,
                "title": None,
                "type": None,
                "href": None,
                "belowTheFold": False,
                "topImage": False,
                "internalRedirect": None,
                "isProcessing": False,
                "align": "center",
            }
        }]
    }


def node_contains_text(node, text):
    """Recursively check if a ProseMirror node contains specific text."""
    if isinstance(node, dict):
        if node.get("type") == "text" and text in node.get("text", ""):
            return True
        for child in node.get("content", []):
            if node_contains_text(child, text):
                return True
    return False


def inject_images(doc, insertions):
    """Insert image nodes after paragraphs matching anchor text."""
    new_content = []
    for node in doc.get("content", []):
        new_content.append(node)
        for ins in insertions:
            if not ins.get("done") and node_contains_text(node, ins["anchor"]):
                new_content.append(make_image_node(ins["cdn_url"], ins["width"], ins["height"]))
                ins["done"] = True
                print(f"  Inserted image after: '{ins['anchor'][:60]}...'")
    doc["content"] = new_content
    return doc


if __name__ == "__main__":
    if not SESSION_COOKIE:
        print("SUBSTACK_SESSION_COOKIE not set"); sys.exit(1)

    session = build_session(SESSION_COOKIE)

    # Step 1: upload each SVG via URL
    print("Uploading diagrams to Substack CDN...")
    for d in DIAGRAMS:
        svg_url = f"{BASE_URL}/img/diagrams/{d['file']}"
        print(f"  {d['file']} → ", end="", flush=True)
        cdn_url, w, h = upload_image_by_url(session, svg_url)
        d["cdn_url"] = cdn_url
        d["width"] = w
        d["height"] = h
        print(cdn_url)

    # Step 2: fetch draft body
    print(f"\nFetching post {POST_ID}...")
    r = session.get(f"{SUBSTACK_URL}/api/v1/drafts/{POST_ID}", timeout=15)
    r.raise_for_status()
    post = r.json()
    body_str = post.get("draft_body", "{}")
    doc = json.loads(body_str) if isinstance(body_str, str) else body_str

    # Step 3: inject image nodes
    print("Injecting image nodes...")
    doc = inject_images(doc, DIAGRAMS)

    not_inserted = [d["file"] for d in DIAGRAMS if not d.get("done")]
    if not_inserted:
        print(f"WARNING: anchor not found for: {not_inserted}")

    # Step 4: update draft
    print(f"\nUpdating post {POST_ID}...")
    new_body = json.dumps(doc)
    r = session.put(
        f"{SUBSTACK_URL}/api/v1/drafts/{POST_ID}",
        json={"draft_body": new_body},
        timeout=30,
    )
    if r.status_code not in (200, 201):
        print(f"Update failed {r.status_code}: {r.text[:300]}")
        sys.exit(1)

    print(f"Done. View: {SUBSTACK_URL}/p/{POST_ID}")
