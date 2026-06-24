#!/usr/bin/env python3
"""Update the already-published part-one Substack post to the 9-pattern version.

Re-converts the reconciled markdown, re-uploads the changed diagrams, injects
image nodes, and re-publishes WITHOUT sending email (send=false).
"""

import importlib.util, os, sys, json
from urllib.parse import unquote
import requests, frontmatter

HERE = os.path.dirname(os.path.abspath(__file__))

# reuse md_to_prosemirror from the hyphenated module file
spec = importlib.util.spec_from_file_location("p2s", os.path.join(HERE, "post-to-substack.py"))
p2s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p2s)
md_to_prosemirror = p2s.md_to_prosemirror

SUBSTACK_URL = "https://analyticsmusings.substack.com"
BASE_URL = "https://yadavillidotcom.yakarteek.workers.dev"
SESSION_COOKIE = os.environ.get("SUBSTACK_SESSION_COOKIE", "")
POST_ID = "200830451"
MD = os.path.join(HERE, "..", "content", "insights", "ai-product-pattern-playbook.md")

DIAGRAMS = [
    {"file": "ai-product-shape.svg",        "anchor": "maps AI patterns onto a 2x2"},
    {"file": "ai-adoption-readiness.svg",   "anchor": "which patterns you can credibly execute"},
    {"file": "ai-invocation-protocols.svg", "anchor": "without changing the capability you built"},
]


def build_session(cookie_raw):
    cookie = unquote(cookie_raw)
    s = requests.Session()
    s.cookies.set("substack.sid", cookie, domain="substack.com")
    s.cookies.set("substack.sid", cookie, domain="analyticsmusings.substack.com")
    s.get("https://substack.com/sign-in?redirect=%2F&for_pub=analyticsmusings")
    return s


def upload_by_url(s, url):
    r = s.post(f"{SUBSTACK_URL}/api/v1/image", json={"image": url}, timeout=30)
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

    # 1. convert reconciled markdown to ProseMirror
    post_md = frontmatter.load(MD)
    body = md_to_prosemirror(post_md.content)
    doc = json.loads(body)

    # 2. upload changed diagrams
    print("Uploading diagrams...")
    for d in DIAGRAMS:
        url = f"{BASE_URL}/img/diagrams/{d['file']}"
        print(f"  {d['file']} -> ", end="", flush=True)
        d["cdn"], d["w"], d["h"] = upload_by_url(s, url)
        print(d["cdn"])

    # 3. inject image nodes at anchors
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
        print("WARNING anchors not found:", missing)

    # 4. update draft body
    print(f"\nUpdating draft {POST_ID}...")
    r = s.put(f"{SUBSTACK_URL}/api/v1/drafts/{POST_ID}",
              json={"draft_body": json.dumps(doc)}, timeout=30)
    if r.status_code not in (200, 201):
        print(f"Draft update failed {r.status_code}: {r.text[:300]}"); sys.exit(1)
    print("  draft updated")

    # 5. re-publish WITHOUT sending email
    print("Re-publishing (send=false, no email)...")
    r = s.post(f"{SUBSTACK_URL}/api/v1/drafts/{POST_ID}/publish",
               json={"send": False, "share_automatically": False}, timeout=30)
    if r.status_code not in (200, 201):
        print(f"Publish-sync failed {r.status_code}: {r.text[:300]}")
        print("Draft body was updated; you may need to hit 'Publish'/'Save' once in the Substack UI.")
        sys.exit(1)
    print(f"Done: {SUBSTACK_URL}/p/{POST_ID}")
