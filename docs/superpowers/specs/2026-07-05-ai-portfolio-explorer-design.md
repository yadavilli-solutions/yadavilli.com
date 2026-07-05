# AI Portfolio Explorer: Site Induction Design

Date: 2026-07-05
Status: Approved

## Goal

Add the AI Portfolio Explorer product (repo: https://github.com/thedataengineer/ai-portfolio-explorer, local: `/Users/yakarteek/code/personal/2026-06-27/ai_discovery_tool`) to yadavilli.com as a first-class product, and extend the product framework from three phases to four.

## Product facts (from repo README)

AI Portfolio Explorer is a multi-tenant platform to discover, prioritize, and govern enterprise AI use cases across projects and phases. Capabilities: interactive strategy dashboard (priority matrix, maturity curve, semantic graph, playbook audits), Claude strategy co-pilot, seed/export/import, documented REST API (OpenAPI), HMAC-signed outbound webhooks with retry, connectors for Jira, Slack, Microsoft Teams, Confluence, and ServiceNow. React 19 + Vite SPA, Fastify + TypeScript API, Postgres via Drizzle, org-scoped tenancy, AES-256-GCM encrypted connector credentials.

## Decisions made

- Name on site: **AI Portfolio Explorer**. Slug: `ai-portfolio-explorer`.
- Framework becomes **Discover · Calibrate · Decode · Activate**. Explorer owns Discover, ahead of BenchMark.
- Scope: core site integration, plus one case study, plus one insight article.
- Diagram approach: hand-extend the existing `product-pipeline.svg` (not D2) to preserve the site's established diagram style.

## Changes

### 1. Framework rename (site-wide)

"Calibrate · Decode · Activate" becomes "Discover · Calibrate · Decode · Activate" everywhere it appears. Phase numbering in the diagram becomes 01 Discover, 02 Calibrate, 03 Decode, 04 Activate. Files: `content/about.md` (lines 19, 22), all four product pages, `layouts/index.html` method section.

### 2. Product page: `content/products/ai-portfolio-explorer.md`

Frontmatter: title "AI Portfolio Explorer", description (one line, discovery/prioritization/governance), date 2026-07-05, tag "Portfolio Governance".

Sections, mirroring BenchMark/DeepDive/KnowHow structure:

- Hook H2 plus intro paragraph.
- "What AI Portfolio Explorer Does": use-case discovery and inventory; priority matrix scoring; maturity curve; semantic graph; Claude strategy co-pilot; enterprise connectors (Jira, Slack, Teams, Confluence, ServiceNow); REST API and signed webhooks.
- "How It Fits the Pipeline": Discover phase; the prioritized use-case backlog feeds [BenchMark](/products/benchmark/).
- "Licensing": per engagement, dedicated full-stack development engineer and two operations engineers (same pattern as siblings).
- GitHub repo link: https://github.com/thedataengineer/ai-portfolio-explorer.

### 3. Homepage: `layouts/index.html`

- Hero ticker (both repeated span groups): add "AI Portfolio Explorer".
- Method section: add a fourth method card for Explorer before BenchMark ("Discover and govern your AI use-case portfolio..."), link to product page. Update the section copy if it names three phases.
- Products grid: add a fourth product card, label "Portfolio Governance", three feature bullets, ghost button to product page. Check grid CSS (likely 3-column); adjust to 2x2 at desktop widths and single column on mobile in `assets` CSS.

### 4. Footer: `layouts/partials/footer.html`

Add "AI Portfolio Explorer" link above BenchMark, matching pipeline order.

### 5. Diagram: `static/img/diagrams/product-pipeline.svg`

Extend from three cards to four. New first card: "01 · DISCOVER / AI Portfolio Explorer" with three or four detail lines. Renumber remaining cards 02 to 04. Widen canvas to about 1200px (consistent with recent diagram widening commits). New phase color: violet family (distinct from existing green and sibling palettes), same dark card idiom (#09090b background, card fill-opacity 0.25, 1px stroke, rounded corners).

### 6. Cross-links on sibling product pages

- `benchmark.md`: pipeline section now says BenchMark takes the prioritized use-case backlog from [AI Portfolio Explorer](/products/ai-portfolio-explorer/) and represents the Calibrate phase of the four-phase framework.
- `deepdive.md`, `knowhow.md`: framework name update only.
- `products/_index.md`: description already generic; verify diagram alt text says four phases.

### 7. Case study: `content/case-studies/capital-markets-ai-portfolio.md`

Tag "Capital Markets". Grounded in the product's real capital-markets seed pack (16 pre-scored use cases). Narrative: a capital markets firm with 40+ scattered AI ideas, duplicate pilots across desks, no kill criteria. Explorer deployment: inventoried 47 use cases, scored them on the sector's dimensions, priority matrix separated fund/kill/merge (funded 12, killed 9, merged 8 duplicates into 4, remainder held in a scored backlog), governance cadence wired through Jira and ServiceNow connectors, webhook-driven portfolio reviews. Funded winners entered BenchMark. Results section with concrete numbers. Challenge / Our Approach / The Results format matching existing case studies.

### 8. Insight article: `content/insights/ai-use-case-lottery.md`

Tag "Strategy". Thesis: enterprises fund AI use cases like lottery tickets; executive enthusiasm substitutes for portfolio discipline. Argument arc: how use cases actually get selected today; what a portfolio discipline requires (discovery, explicit scoring dimensions, kill criteria, governance cadence); why the kill decision is the hard part; what changes when the portfolio is governed. One new diagram: 2x2 priority matrix SVG in the site's diagram style, saved to `static/img/diagrams/`. Cross-link to the product page. Site voice, no em dashes.

### 9. Verification

- `hugo` build completes clean.
- Preview server: homepage renders 4-card grid and method section without layout breakage at desktop and mobile widths; footer shows four products; pipeline diagram renders four phases; all new internal links resolve; case study and insight pages render.

## Out of scope

- Substack posting of the insight article (user-run process, after merge).
- Product screenshots on the product page (no sibling page has them).
- Any changes to the ai-portfolio-explorer repo itself.
