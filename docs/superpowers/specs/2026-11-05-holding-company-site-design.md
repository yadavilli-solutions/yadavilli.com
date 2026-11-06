# yadavilli.com as a holding-company site

Date: 2026-11-05
Status: approved in chat, pending spec review

## Goal

Yadavilli Solutions is the legal entity. Basantra Systems (basantra.com) is the
DBA that sells products, services, and training. yadavilli.com stops being a
marketing site and becomes a three-page corporate shell: home, privacy, terms.
Everything that moved to basantra.com redirects there with a 301.

Decisions taken in chat:

- Remove services, products, case studies, Insights, and the Insights password
  Worker. Old URLs redirect.
- Visual direction: light, matching basantra.com tokens, with dark mode.
- Home page carries a contact email only. Basantra is not named on the page.
- No checkpoint commit of the in-progress rebrand; the redesign is one commit.

## Approach

Keep Hugo, Wrangler static assets, and the GitHub deploy workflow. Rewrite the
templates and CSS from scratch. Redirects live in `static/_redirects`, which
Hugo copies to `public/_redirects` and Cloudflare static assets evaluates at
the edge, so no Worker script is needed.

Rejected: hand-written HTML without Hugo (duplicates header and footer, changes
CI for no visual gain); redirecting the whole domain (conflicts with keeping a
contact page).

## Pages and URL map

| URL | Result |
|---|---|
| `/` | Home, `layouts/index.html` |
| `/privacy/` | Legal page, `layouts/_default/single.html` |
| `/terms/` | Legal page, `layouts/_default/single.html` |
| `/404.html` | Not-found page, `layouts/404.html` |
| `/sitemap.xml`, `/robots.txt` | Hugo defaults |

`static/_redirects` (all 301). Both trailing-slash and bare forms are listed
for single pages.

```
/about/                          https://basantra.com/about/
/about                           https://basantra.com/about/
/services/                       https://basantra.com/services/
/services                        https://basantra.com/services/
/products/ai-portfolio-explorer/ https://basantra.com/products/ai-portfolio-explorer/
/products/*                      https://basantra.com/products/
/products                        https://basantra.com/products/
/insights/index.xml              https://basantra.com/insights/rss.xml
/index.xml                       https://basantra.com/insights/rss.xml
/insights/*                      https://basantra.com/insights/:splat
/insights                        https://basantra.com/insights/
/case-studies/*                  https://basantra.com/
/case-studies                    https://basantra.com/
/contact/                        /
/contact                         /
```

Insights slugs are identical on basantra.com (checked four), so the splat
carries readers to the same article. BenchMark, DeepDive, and KnowHow have no
page on basantra.com, so they land on its products index. Case studies have no
equivalent and land on the basantra.com home page.

## Copy

Home page, top to bottom:

```
YADAVILLI SOLUTIONS                       (eyebrow)
A holding company.                        (h1, Newsreader; gold streak under "holding")
Yadavilli Solutions is the legal entity behind a small group of operating
businesses. It holds them; it does not trade under this name.
For legal, finance, and administrative matters: hello@yadavilli.com  (mailto)
```

Footer: `© {year} Yadavilli Solutions.` then links Privacy, Terms.

Header: Y mark (24px, currentColor) plus wordmark "Yadavilli Solutions" in
IBM Plex Sans 600, linking to `/`. Theme toggle button on the right. No nav.

404 page: "Page not found." and a link home. Hugo renders it at `/404.html`;
Cloudflare static assets serves it for missing paths when `not_found_handling`
is `404-page`.

Privacy policy rewritten to cover only: Cloudflare request logs, email sent to
hello@yadavilli.com, the theme preference stored in localStorage (not a cookie,
never sent to the server), no analytics, no third-party scripts or fonts, how to
ask for deletion. Terms rewritten to cover: the site is information only,
content ownership, no warranty, governing law line left as it is today.

## Visual

Tokens copied from basantra.com so the two sites read as one family.

```
Light (default)         Dark (prefers-color-scheme or [data-theme=dark])
--stone   #f6f5f2       #121417    page background
--surface #edebe5       #1a1d21    raised surface (toggle hover)
--ink     #16181b       #e9e7e2    text
--muted   #55585e       #a6a39c    secondary text
--line    #d6d2c8       #2d3136    hairlines
--streak  #c9a227       #c9a227    gold accent, streak only
--streak-ink #7a5e00    #d8b545    link colour, focus ring
```

Type: `--font-display` Newsreader (400, 500, 400 italic), `--font-body` IBM Plex
Sans (400, 500, 600). Scale: 0.875 / 1 / 1.15 / clamp 1.65 to 2.25 / clamp 2.25
to 3.5 rem. Body line-height 1.55.

Layout: header, main, footer in a column with `min-height: 100dvh` so the footer
sits at the bottom on short pages. Text column `max-width: 40rem`, left-aligned,
gutter 16px below 768px and 24px above. Radius 4px. No background texture, no
scroll reveal, no marquee, no counters, no icons beyond the Y mark and the two
theme glyphs.

Dark mode: `prefers-color-scheme: dark` applies the dark tokens unless
`data-theme="light"` is set; `data-theme="dark"` forces dark. An inline script
in `<head>` reads `localStorage.theme` before first paint. The toggle button
flips the attribute and stores the choice. Same pattern as basantra.com.

## Files

New or rewritten:

- `layouts/_default/baseof.html` – document shell, header, footer, theme script
- `layouts/index.html` – home
- `layouts/_default/single.html` – legal pages (eyebrow, h1, prose)
- `layouts/404.html`
- `layouts/partials/head.html` – meta, OG, JSON-LD Organization, icons, fonts
- `layouts/partials/header.html`, `layouts/partials/footer.html`
- `assets/css/site.css` – one file, about 250 lines
- `assets/js/theme.js` – toggle only
- `static/_redirects`
- `static/fonts/` – six woff2 files from Fontsource (newsreader latin 400,
  500, 400 italic; ibm-plex-sans latin 400, 500, 600)
- `static/img/brand/logo-mark.svg` – Y mark with `fill="currentColor"`
- `static/img/favicon.svg`, `favicon.ico`, `favicon-16x16.png`,
  `favicon-32x32.png`, `apple-touch-icon.png`, `android-chrome-192x192.png`,
  `android-chrome-512x512.png`, `og-default.png` – regenerated in the new palette
- `scripts/generate-brand-assets.py` – trimmed to the favicon set and OG card
- `content/_index.md`, `content/privacy.md`, `content/terms.md`

Deleted:

- `content/about.md`, `content/services.md`, `content/contact.md`,
  `content/case-studies/`, `content/insights/`, `content/products/`
- `layouts/_default/about.html`, `contact.html`, `list.html`, `services.html`,
  `layouts/home.rss.xml`, `layouts/partials/icon.html`
- `assets/icons/`, `assets/css/yadavilli.css`, `assets/js/yadavilli.js`
- `static/img/diagrams/`, `static/img/logos/`, `static/img/hero.webp`,
  `static/img/brand/logo-horizontal-*.svg`, `logo-mark-{black,white,color}.svg`,
  `logo-cover.png`, `logo-profile.png`, `static/fonts/geist*`
- `worker/`
- `scripts/post-to-substack.py`, `fix-substack-*.py`, `update-substack-partone.py`,
  `generate-logo.py`, `recolor-images.py`
- `themes/blowfish/` (vendored, never referenced by config)
- `docs/AI-Embedding-Design-Patterns.docx`, `.pdf`,
  `docs/ai-embedding-pattern-catalog.md` (Insights source material)
- `archetypes/default.md`

Config:

- `config/_default/hugo.toml`: title "Yadavilli Solutions", description
  "Yadavilli Solutions is a holding company.", remove `[menu]`, disable RSS and
  taxonomies (`disableKinds = ["taxonomy", "term", "RSS"]`).
- `wrangler.jsonc`: remove `main`, `assets.run_worker_first`,
  `compatibility_flags`; add `assets.not_found_handling = "404-page"`.
- `.github/workflows/deploy.yml`: remove the uv install and Substack steps,
  `fetch-depth`, and the `--exclude "insights/*"` on the S3 sync.
- `static/site.webmanifest`: name, colours.

Untouched: `infra/` (AWS Terraform for a different domain), `baseURL`
(still the workers.dev host; canonical tags follow it), `.hugo_version`.

## Verification

1. `hugo --minify` builds with no warnings; `public/` contains exactly
   `index.html`, `privacy/`, `terms/`, `404.html`, `_redirects`, `sitemap.xml`,
   `robots.txt`, `site.webmanifest`, `fonts/`, `img/`, fingerprinted css and js.
2. `npx wrangler dev` serves the build; `curl -I` on each redirect source returns
   301 with the expected `Location`; `/nope` returns 404 with the 404 page body.
3. Browser: home, privacy, terms at 375px and 1280px, light and dark, toggle
   persists across reload, console clean, every internal link resolves.
4. No request leaves the origin (fonts self-hosted, no analytics).

## Commit

One commit, message "Rebuild yadavilli.com as a holding-company site", no
attribution trailers. Not pushed.
