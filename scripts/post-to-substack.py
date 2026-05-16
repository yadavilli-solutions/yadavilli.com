#!/usr/bin/env python3
"""Post new Insights articles to Substack as drafts.

Detects newly added content/insights/*.md files in the last commit and
creates a draft in Substack for each one. Requires SUBSTACK_SESSION_COOKIE
set as an environment variable (GitHub Actions secret).
"""

import os
import sys
import subprocess
import re
from urllib.parse import unquote

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


def build_session(cookie_raw):
    """Build an authenticated requests session."""
    cookie = unquote(cookie_raw)
    session = requests.Session()
    session.cookies.set("substack.sid", cookie, domain="substack.com")
    session.cookies.set("substack.sid", cookie, domain="analyticsmusings.substack.com")
    # Sign in to the publication context
    session.get("https://substack.com/sign-in?redirect=%2F&for_pub=analyticsmusings")
    return session


def get_user_id(session):
    """Fetch the authenticated user's ID."""
    profile = session.get("https://substack.com/api/v1/user/profile/self").json()
    return profile["id"]


def md_to_html(content):
    """Convert markdown to clean HTML."""
    # Strip inline HTML blocks (diagram embeds etc) - Substack cant render custom CSS
    content = re.sub(r'<div class="diagram-embed">.*?</div>', '', content, flags=re.DOTALL)
    html = md_lib.markdown(content, extensions=["extra", "nl2br", "sane_lists"])
    return html


def post_to_substack(session, user_id, md_file):
    post = frontmatter.load(md_file)

    title = post.metadata.get("title", "")
    subtitle = post.metadata.get("description", "")
    body_html = md_to_html(post.content)

    resp = session.post(
        f"{SUBSTACK_URL}/api/v1/drafts",
        json={
            "draft_title": title,
            "draft_subtitle": subtitle,
            "draft_body": body_html,
            "type": "newsletter",
            "audience": "everyone",
            "draft_bylines": [{"id": user_id, "is_guest": False}],
        },
        timeout=30,
    )

    if resp.status_code in (200, 201):
        data = resp.json()
        draft_id = data.get("id", "unknown")
        print(f"Draft created (id={draft_id}): {title}")
        print(f"  Preview: {SUBSTACK_URL}/publish/post/{draft_id}")
        return True
    else:
        print(f"Failed to post '{title}' ({resp.status_code}): {resp.text[:300]}")
        return False


if __name__ == "__main__":
    if not SESSION_COOKIE:
        print("SUBSTACK_SESSION_COOKIE is not set - skipping Substack sync")
        sys.exit(0)

    # Allow passing specific files as args (for manual runs)
    files = sys.argv[1:] if len(sys.argv) > 1 else get_new_insight_files()

    if not files:
        print("No new Insights articles detected in this commit")
        sys.exit(0)

    print(f"Posting {len(files)} article(s) to Substack...")

    session = build_session(SESSION_COOKIE)
    user_id = get_user_id(session)

    results = [post_to_substack(session, user_id, f) for f in files]
    if not all(results):
        sys.exit(1)
