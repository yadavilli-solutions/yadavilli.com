#!/usr/bin/env python3
"""Post new Insights articles to Substack.

Detects newly added content/insights/*.md files in the last commit and
publishes each one directly to Substack. Requires SUBSTACK_SESSION_COOKIE
set as an environment variable (GitHub Actions secret).
"""

import os
import sys
import subprocess
import re
import json
from urllib.parse import unquote
from html.parser import HTMLParser

try:
    import frontmatter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-frontmatter", "-q"])
    import frontmatter

try:
    import markdown as md_lib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "-q"])
    import markdown as md_lib

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

SUBSTACK_URL = "https://analyticsmusings.substack.com"
SESSION_COOKIE = os.environ.get("SUBSTACK_SESSION_COOKIE", "")


# ---------------------------------------------------------------------------
# Markdown -> ProseMirror JSON
# ---------------------------------------------------------------------------

class _ProseMirrorBuilder(HTMLParser):
    """Convert HTML (from python-markdown) into a ProseMirror doc JSON."""

    def __init__(self):
        super().__init__()
        self.content = []          # top-level nodes
        self._block = None         # current block node (paragraph, heading, ...)
        self._marks = []           # active inline marks
        self._text = ""            # buffered text
        self._list_stack = []      # stack of list nodes
        self._in_li = False

    # -- helpers -------------------------------------------------------------

    def _flush(self):
        t = self._text
        self._text = ""
        if not t:
            return
        node = {"type": "text", "text": t}
        if self._marks:
            node["marks"] = [m.copy() for m in self._marks]
        self._target().setdefault("content", []).append(node)

    def _target(self):
        """Return the content list of the current innermost block."""
        if self._block is not None:
            return self._block
        if self.content:
            return self.content[-1]
        return self.content

    def _push_block(self, node):
        self._flush()
        self._block = node
        if self._list_stack:
            # inside a list item - append to the list item's content
            li = self._list_stack[-1]["_current_li"]
            li.setdefault("content", []).append(node)
        else:
            self.content.append(node)

    def _pop_block(self):
        self._flush()
        self._block = None

    def _add_mark(self, mark):
        self._flush()
        self._marks.append(mark)

    def _remove_mark(self, mark_type):
        self._flush()
        self._marks = [m for m in self._marks if m["type"] != mark_type]

    # -- tag handlers --------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "p":
            self._push_block({"type": "paragraph"})
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self._push_block({"type": "heading", "attrs": {"level": level}})
        elif tag == "blockquote":
            self._push_block({"type": "blockquote"})
        elif tag == "pre":
            self._push_block({"type": "code_block"})
        elif tag in ("ul", "ol"):
            lst = {
                "type": "bullet_list" if tag == "ul" else "ordered_list",
                "content": [],
                "_current_li": None,
            }
            self._list_stack.append(lst)
            if not self._list_stack[:-1]:
                self.content.append(lst)
            else:
                # nested list goes inside current list item paragraph
                parent_li = self._list_stack[-2]["_current_li"]
                if parent_li:
                    parent_li.setdefault("content", []).append(lst)
        elif tag == "li":
            self._flush()
            self._block = None
            para = {"type": "paragraph"}
            li_node = {"type": "list_item", "content": [para]}
            if self._list_stack:
                lst = self._list_stack[-1]
                lst["_current_li"] = li_node
                lst["content"].append(li_node)
            self._block = para
        elif tag == "strong":
            self._add_mark({"type": "strong"})
        elif tag == "em":
            self._add_mark({"type": "em"})
        elif tag == "code":
            self._add_mark({"type": "code"})
        elif tag == "a":
            href = attrs.get("href", "")
            self._add_mark({"type": "link", "attrs": {"href": href, "target": "_blank"}})
        elif tag == "hr":
            self._flush()
            self.content.append({"type": "horizontal_rule"})
        elif tag == "br":
            self._flush()
            self._target().setdefault("content", []).append({"type": "hard_break"})

    def handle_endtag(self, tag):
        if tag in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre"):
            self._pop_block()
        elif tag == "li":
            self._pop_block()
        elif tag in ("ul", "ol"):
            if self._list_stack:
                self._list_stack.pop()
        elif tag == "strong":
            self._remove_mark("strong")
        elif tag == "em":
            self._remove_mark("em")
        elif tag == "code":
            self._remove_mark("code")
        elif tag == "a":
            self._remove_mark("link")

    def handle_data(self, data):
        self._text += data

    def get_doc(self):
        self._flush()
        # strip internal tracking keys
        def clean(node):
            if isinstance(node, dict):
                return {k: clean(v) for k, v in node.items() if not k.startswith("_")}
            if isinstance(node, list):
                return [clean(i) for i in node]
            return node
        return {"type": "doc", "content": clean(self.content)}


def md_to_prosemirror(content: str) -> str:
    """Convert markdown string to a JSON-stringified ProseMirror doc."""
    # Strip diagram embeds - Substack can't render custom CSS
    content = re.sub(r'<div class="diagram-embed">.*?</div>', '', content, flags=re.DOTALL)
    # Strip trailing CTA links that reference internal Hugo paths
    content = re.sub(r'\[.*?\]\(/.*?\)', '', content)
    html = md_lib.markdown(content, extensions=["extra", "nl2br", "sane_lists"])
    builder = _ProseMirrorBuilder()
    builder.feed(html)
    return json.dumps(builder.get_doc())


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def get_new_insight_files():
    """Return insight markdown files added in the last commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", "HEAD~1", "HEAD"],
        capture_output=True, text=True
    )
    files = result.stdout.strip().split("\n")
    return [
        f for f in files
        if f.startswith("content/insights/")
        and f.endswith(".md")
        and "_index" not in f
    ]


# ---------------------------------------------------------------------------
# Substack API
# ---------------------------------------------------------------------------

def build_session(cookie_raw: str) -> requests.Session:
    cookie = unquote(cookie_raw)
    session = requests.Session()
    session.cookies.set("substack.sid", cookie, domain="substack.com")
    session.cookies.set("substack.sid", cookie, domain="analyticsmusings.substack.com")
    session.get("https://substack.com/sign-in?redirect=%2F&for_pub=analyticsmusings")
    return session


def get_user_id(session: requests.Session) -> int:
    profile = session.get("https://substack.com/api/v1/user/profile/self").json()
    return int(profile["id"])


def publish(session: requests.Session, user_id: int, md_file: str) -> bool:
    post = frontmatter.load(md_file)
    title = post.metadata.get("title", "")
    subtitle = post.metadata.get("description", "")
    body = md_to_prosemirror(post.content)

    # Create draft
    resp = session.post(
        f"{SUBSTACK_URL}/api/v1/drafts",
        json={
            "draft_title": title,
            "draft_subtitle": subtitle,
            "draft_body": body,
            "type": "newsletter",
            "audience": "everyone",
            "draft_bylines": [{"id": user_id, "is_guest": False}],
        },
        timeout=30,
    )

    if resp.status_code not in (200, 201):
        print(f"Failed to create '{title}' ({resp.status_code}): {resp.text[:300]}")
        return False

    draft_id = resp.json().get("id")

    # Publish immediately
    pub = session.post(
        f"{SUBSTACK_URL}/api/v1/drafts/{draft_id}/publish",
        json={"send": True, "share_automatically": False},
        timeout=30,
    )

    if pub.status_code in (200, 201):
        slug = resp.json().get("slug") or draft_id
        print(f"Published: {title}")
        print(f"  URL: {SUBSTACK_URL}/p/{slug}")
        return True
    else:
        print(f"Draft created but publish failed ({pub.status_code}): {pub.text[:300]}")
        return False


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not SESSION_COOKIE:
        print("SUBSTACK_SESSION_COOKIE is not set - skipping Substack sync")
        sys.exit(0)

    files = sys.argv[1:] if len(sys.argv) > 1 else get_new_insight_files()

    if not files:
        print("No new Insights articles detected in this commit")
        sys.exit(0)

    print(f"Publishing {len(files)} article(s) to Substack...")

    session = build_session(SESSION_COOKIE)
    user_id = get_user_id(session)

    results = [publish(session, user_id, f) for f in files]
    if not all(results):
        sys.exit(1)
