# AI Portfolio Explorer Site Induction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the AI Portfolio Explorer product to yadavilli.com and extend the product framework from three phases to four (Discover · Calibrate · Decode · Activate).

**Architecture:** Hugo static site. Content pages are markdown under `content/`, the homepage and footer are hand-written Hugo templates under `layouts/`, styling is one plain CSS file at `static/css/yadavilli.css`, and diagrams are hand-authored dark-theme SVGs under `static/img/diagrams/`. Every task edits source files and verifies with a Hugo build into a scratch directory.

**Tech Stack:** Hugo v0.161.1 extended (`/opt/homebrew/bin/hugo`), plain CSS, hand-authored SVG.

**Spec:** `docs/superpowers/specs/2026-07-05-ai-portfolio-explorer-design.md`

## Global Constraints

- Product name is exactly "AI Portfolio Explorer"; URL slug is exactly `ai-portfolio-explorer`.
- Framework string is exactly "Discover · Calibrate · Decode · Activate" (U+00B7 middle dots with spaces), replacing "Calibrate · Decode · Activate" everywhere.
- No em dashes (—) anywhere in authored prose. Use commas, semicolons, or periods.
- Commit messages: plain, no AI/Claude co-author or "Generated with" trailers of any kind.
- Verify builds into a scratch directory so the tracked `public/` directory is never touched. Every shell session that runs verification commands must first run:
  ```bash
  export HUGO_OUT=/private/tmp/claude-501/-Users-yakarteek-code-personal-w-yadavilli-com/52220313-53f9-44e8-b1e6-63bb040f5bf1/scratchpad/hugo-verify
  ```
- Working directory for all commands: `/Users/yakarteek/code/personal/w/yadavilli.com`.

---

### Task 1: Product page

**Files:**
- Create: `content/products/ai-portfolio-explorer.md`

**Interfaces:**
- Produces: page at `/products/ai-portfolio-explorer/`. Every later task that links the product uses exactly this path.

- [ ] **Step 1: Create the page**

Write `content/products/ai-portfolio-explorer.md` with exactly this content:

```markdown
---
title: "AI Portfolio Explorer"
description: "Discover, prioritize, and govern your enterprise AI use-case portfolio before build spend is committed."
date: 2026-07-05
tag: "Portfolio Governance"
---

## Stop Funding AI Ideas. Start Governing a Portfolio.

**AI Portfolio Explorer** is the front door of our product suite. Enterprises do not lack AI ideas; they lack a defensible way to choose among them. AI Portfolio Explorer turns a scattered pile of use-case ideas into a scored, governed portfolio with explicit funding and kill decisions.

### What AI Portfolio Explorer Does

- **Use-Case Discovery and Inventory**: Capture AI use cases across projects and phases in one multi-tenant workspace, replacing the spreadsheets and slide decks where portfolio decisions go to die.
- **Priority Matrix and Maturity Curve**: Score every use case on sector-specific dimensions, then read the portfolio at a glance: what to fund, what to kill, what to merge, and what to revisit.
- **Semantic Graph and Playbook Audits**: Map relationships between use cases, systems, and teams to expose duplicate efforts and hidden dependencies before they become parallel budgets.
- **Claude Strategy Co-Pilot**: Interrogate your portfolio in plain language. The co-pilot drafts scoring rationales, challenges weak business cases, and surfaces portfolio gaps.
- **Enterprise Connectors**: Wire portfolio decisions into Jira, Slack, Microsoft Teams, Confluence, and ServiceNow so governance happens where delivery already lives.
- **REST API and Signed Webhooks**: A documented OpenAPI surface and HMAC-signed webhooks with retry, so the portfolio feeds downstream systems instead of becoming another silo.

### How It Fits the Pipeline

AI Portfolio Explorer represents the Discover phase of our Discover · Calibrate · Decode · Activate framework. It decides what enters the pipeline: the prioritized use-case backlog feeds directly into [BenchMark](/products/benchmark/) for infrastructure and model calibration, and the portfolio's governance cadence tracks each initiative through [DeepDive](/products/deepdive/) and [KnowHow](/products/knowhow/).

### Licensing

AI Portfolio Explorer is licensed per engagement and includes a dedicated full-stack development engineer and two operations engineers to **run portfolio onboarding, connector configuration, and governance operations**.
```

- [ ] **Step 2: Verify the build renders the page**

Run:
```bash
hugo --quiet -d "$HUGO_OUT" && test -f "$HUGO_OUT/products/ai-portfolio-explorer/index.html" && echo PAGE_OK
```
Expected: `PAGE_OK`

- [ ] **Step 3: Commit**

```bash
git add content/products/ai-portfolio-explorer.md
git commit -m "Add AI Portfolio Explorer product page"
```

---

### Task 2: Four-phase pipeline diagram

**Files:**
- Modify: `static/img/diagrams/product-pipeline.svg` (full replacement)

**Interfaces:**
- Produces: 1200x260 SVG with four cards numbered 01 DISCOVER through 04 ACTIVATE. Tasks 3 and 4 update the alt text that describes it.

- [ ] **Step 1: Replace the SVG**

Replace the entire content of `static/img/diagrams/product-pipeline.svg` with:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 260" width="1200" height="260" font-family="Inter, system-ui, sans-serif">
  <!-- Background -->
  <rect width="1200" height="260" fill="#09090b" rx="8" />

  <!-- Connector 1 -->
  <g stroke="#3f3f46" stroke-width="1.5" fill="none">
    <path d="M 295 130 L 325 130" />
    <polygon points="327,130 319,126 319,134" fill="#3f3f46" stroke="none" />
  </g>

  <!-- Connector 2 -->
  <g stroke="#3f3f46" stroke-width="1.5" fill="none">
    <path d="M 585 130 L 615 130" />
    <polygon points="617,130 609,126 609,134" fill="#3f3f46" stroke="none" />
  </g>

  <!-- Connector 3 -->
  <g stroke="#3f3f46" stroke-width="1.5" fill="none">
    <path d="M 875 130 L 905 130" />
    <polygon points="907,130 899,126 899,134" fill="#3f3f46" stroke="none" />
  </g>

  <!-- Card 1: Discover -->
  <g transform="translate(45, 40)">
    <rect width="240" height="180" fill="#2e1065" fill-opacity="0.25" stroke="#6d28d9" stroke-width="1" rx="6" />
    <text x="120" y="32" fill="#d8b4fe" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="1.5">01 · DISCOVER</text>
    <text x="120" y="58" fill="#e4e4e7" font-size="16" font-weight="700" text-anchor="middle">AI Portfolio Explorer</text>
    <line x1="30" y1="78" x2="210" y2="78" stroke="#6d28d9" stroke-width="0.75" />

    <!-- Details -->
    <text x="120" y="102" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Use-Case Discovery &amp; Scoring</text>
    <text x="120" y="126" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Priority Matrix &amp; Maturity Curve</text>
    <text x="120" y="150" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Portfolio Governance &amp; Connectors</text>
  </g>

  <!-- Card 2: Calibrate -->
  <g transform="translate(335, 40)">
    <rect width="240" height="180" fill="#052e16" fill-opacity="0.25" stroke="#065f46" stroke-width="1" rx="6" />
    <text x="120" y="32" fill="#6ee7b7" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="1.5">02 · CALIBRATE</text>
    <text x="120" y="58" fill="#e4e4e7" font-size="16" font-weight="700" text-anchor="middle">BenchMark</text>
    <line x1="30" y1="78" x2="210" y2="78" stroke="#065f46" stroke-width="0.75" />

    <!-- Details -->
    <text x="120" y="102" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Technology Stack Assessment</text>
    <text x="120" y="126" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Model Performance Benchmarks</text>
    <text x="120" y="150" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Infrastructure Compute Blueprints</text>
  </g>

  <!-- Card 3: Decode -->
  <g transform="translate(625, 40)">
    <rect width="240" height="180" fill="#1e1b4b" fill-opacity="0.25" stroke="#3730a3" stroke-width="1" rx="6" />
    <text x="120" y="32" fill="#a5b4fc" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="1.5">03 · DECODE</text>
    <text x="120" y="58" fill="#e4e4e7" font-size="16" font-weight="700" text-anchor="middle">DeepDive</text>
    <line x1="30" y1="78" x2="210" y2="78" stroke="#3730a3" stroke-width="0.75" />

    <!-- Details -->
    <text x="120" y="102" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Automated Code Parsing</text>
    <text x="120" y="126" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Business Rule Extraction</text>
    <text x="120" y="150" fill="#a1a1aa" font-size="11.5" text-anchor="middle">System Knowledge Graphs</text>
  </g>

  <!-- Card 4: Activate -->
  <g transform="translate(915, 40)">
    <rect width="240" height="180" fill="#451a03" fill-opacity="0.25" stroke="#78350f" stroke-width="1" rx="6" />
    <text x="120" y="32" fill="#fde047" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="1.5">04 · ACTIVATE</text>
    <text x="120" y="58" fill="#e4e4e7" font-size="16" font-weight="700" text-anchor="middle">KnowHow</text>
    <line x1="30" y1="78" x2="210" y2="78" stroke="#78350f" stroke-width="0.75" />

    <!-- Details -->
    <text x="120" y="102" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Intelligent Runbook Generation</text>
    <text x="120" y="126" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Incident Automation Procedures</text>
    <text x="120" y="150" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Operational Flow Optimization</text>
  </g>
</svg>
```

Geometry check (do not skip): four 240-wide cards at x = 45, 335, 625, 915 with 50px gaps; connectors sit in each gap. 45 + 240 = 285, connector path 295 to 325, arrow tip 327, next card at 335. Same offsets for the other two gaps.

- [ ] **Step 2: Verify the SVG is well-formed**

Run:
```bash
xmllint --noout static/img/diagrams/product-pipeline.svg && grep -c "DISCOVER\|CALIBRATE\|DECODE\|ACTIVATE" static/img/diagrams/product-pipeline.svg
```
Expected: no xmllint output (exit 0), then `4`.

- [ ] **Step 3: Commit**

```bash
git add static/img/diagrams/product-pipeline.svg
git commit -m "Extend product pipeline diagram to four phases with Discover"
```

---

### Task 3: Framework rename and cross-links in markdown content

**Files:**
- Modify: `content/about.md:17-22`
- Modify: `content/products/benchmark.md:21`
- Modify: `content/products/deepdive.md:21`
- Modify: `content/products/knowhow.md:21`
- Modify: `content/products/_index.md:8`

**Interfaces:**
- Consumes: `/products/ai-portfolio-explorer/` from Task 1.

- [ ] **Step 1: Update `content/about.md`**

Three replacements.

Old:
```markdown
![Calibrate Decode Activate Product Pipeline](/img/diagrams/product-pipeline.svg)
```
New:
```markdown
![Discover Calibrate Decode Activate Product Pipeline](/img/diagrams/product-pipeline.svg)
```

Old:
```markdown
- **Products and Services**: We build functional software instead of delivering static presentation decks. The BenchMark, DeepDive, and KnowHow products provide licensable tooling backed by engineering teams.
```
New:
```markdown
- **Products and Services**: We build functional software instead of delivering static presentation decks. The AI Portfolio Explorer, BenchMark, DeepDive, and KnowHow products provide licensable tooling backed by engineering teams.
```

Old:
```markdown
- **Calibrate · Decode · Activate**: Our three-phase intelligence pipeline takes you from measurement to knowledge extraction to operational excellence, avoiding big-bang transformations.
```
New:
```markdown
- **Discover · Calibrate · Decode · Activate**: Our four-phase intelligence pipeline takes you from use-case discovery through measurement and knowledge extraction to operational excellence, avoiding big-bang transformations.
```

- [ ] **Step 2: Update `content/products/benchmark.md`**

Old:
```markdown
BenchMark represents the Calibrate phase of our Calibrate · Decode · Activate framework. Once your technology architecture is benchmarked, the insights feed directly into [DeepDive](/products/deepdive/) for knowledge extraction, and ultimately into [KnowHow](/products/knowhow/) for **operational runbook generation**.
```
New:
```markdown
BenchMark represents the Calibrate phase of our Discover · Calibrate · Decode · Activate framework. It takes the prioritized use-case backlog from [AI Portfolio Explorer](/products/ai-portfolio-explorer/) and grounds it in infrastructure reality. Once your technology architecture is benchmarked, the insights feed directly into [DeepDive](/products/deepdive/) for knowledge extraction, and ultimately into [KnowHow](/products/knowhow/) for **operational runbook generation**.
```

Also update the paragraph above it. Old:
```markdown
**BenchMark** is the foundation of our product suite. Before you can transform, you need to understand exactly where you stand. BenchMark provides a rigorous, data-driven assessment of your technology architecture and AI readiness.
```
New:
```markdown
**BenchMark** is the measurement foundation of our product suite. Before you can transform, you need to understand exactly where you stand. BenchMark provides a rigorous, data-driven assessment of your technology architecture and AI readiness.
```
(Reason: the Task 1 page calls AI Portfolio Explorer the front door of the suite; "the foundation" and "the front door" can coexist only if BenchMark's claim is scoped to measurement.)

- [ ] **Step 3: Update `content/products/deepdive.md`**

Old:
```markdown
DeepDive represents the Decode phase of our Calibrate · Decode · Activate framework. It takes the technology architecture assessment from [BenchMark](/products/benchmark/) to **extract the knowledge needed to power [KnowHow](/products/knowhow/) runbook generation**.
```
New:
```markdown
DeepDive represents the Decode phase of our Discover · Calibrate · Decode · Activate framework. It takes the technology architecture assessment from [BenchMark](/products/benchmark/) to **extract the knowledge needed to power [KnowHow](/products/knowhow/) runbook generation**.
```

- [ ] **Step 4: Update `content/products/knowhow.md`**

Old:
```markdown
KnowHow represents the Activate phase of our Calibrate · Decode · Activate framework. After [BenchMark](/products/benchmark/) calibrates your technology architecture and [DeepDive](/products/deepdive/) decodes your system intelligence, KnowHow **activates that knowledge into operational excellence**.
```
New:
```markdown
KnowHow represents the Activate phase of our Discover · Calibrate · Decode · Activate framework. After [AI Portfolio Explorer](/products/ai-portfolio-explorer/) selects the portfolio, [BenchMark](/products/benchmark/) calibrates your technology architecture, and [DeepDive](/products/deepdive/) decodes your system intelligence, KnowHow **activates that knowledge into operational excellence**.
```

- [ ] **Step 5: Update `content/products/_index.md`**

Old:
```markdown
![Calibrate Decode Activate Product Pipeline](/img/diagrams/product-pipeline.svg)
```
New:
```markdown
![Discover Calibrate Decode Activate Product Pipeline](/img/diagrams/product-pipeline.svg)
```

- [ ] **Step 6: Verify no stale three-phase string remains in content**

Run:
```bash
grep -rn "Calibrate · Decode · Activate" content/ | grep -v "Discover · Calibrate"
```
Expected: no output (exit 1).

Run:
```bash
hugo --quiet -d "$HUGO_OUT" && echo BUILD_OK
```
Expected: `BUILD_OK`

- [ ] **Step 7: Commit**

```bash
git add content/about.md content/products/benchmark.md content/products/deepdive.md content/products/knowhow.md content/products/_index.md
git commit -m "Rename framework to Discover-Calibrate-Decode-Activate and cross-link Explorer"
```

---

### Task 4: Homepage template and grid CSS

**Files:**
- Modify: `layouts/index.html` (hero ticker ~line 28, method section ~lines 155-192, products grid ~lines 283-320)
- Modify: `static/css/yadavilli.css:537-541, 769-774, 1485-1494`

**Interfaces:**
- Consumes: `/products/ai-portfolio-explorer/` from Task 1; diagram from Task 2.

- [ ] **Step 1: Hero ticker**

In `layouts/index.html`, the ticker track lists six items twice. Insert an AI Portfolio Explorer span before each `<span>BenchMark</span>`. Old (appears once; contains both repeats):
```html
        <span>BenchMark</span><span class="sep">·</span>
        <span>DeepDive</span><span class="sep">·</span>
        <span>KnowHow</span><span class="sep">·</span>
        <span>AI Squads</span><span class="sep">·</span>
        <span>Advisory</span><span class="sep">·</span>
        <span>Applied AI</span><span class="sep">·</span>
        <span>BenchMark</span><span class="sep">·</span>
        <span>DeepDive</span><span class="sep">·</span>
        <span>KnowHow</span><span class="sep">·</span>
        <span>AI Squads</span><span class="sep">·</span>
        <span>Advisory</span><span class="sep">·</span>
        <span>Applied AI</span>
```
New:
```html
        <span>AI Portfolio Explorer</span><span class="sep">·</span>
        <span>BenchMark</span><span class="sep">·</span>
        <span>DeepDive</span><span class="sep">·</span>
        <span>KnowHow</span><span class="sep">·</span>
        <span>AI Squads</span><span class="sep">·</span>
        <span>Advisory</span><span class="sep">·</span>
        <span>Applied AI</span><span class="sep">·</span>
        <span>AI Portfolio Explorer</span><span class="sep">·</span>
        <span>BenchMark</span><span class="sep">·</span>
        <span>DeepDive</span><span class="sep">·</span>
        <span>KnowHow</span><span class="sep">·</span>
        <span>AI Squads</span><span class="sep">·</span>
        <span>Advisory</span><span class="sep">·</span>
        <span>Applied AI</span>
```

- [ ] **Step 2: Method section header and diagram wrapper**

Old:
```html
      <h2>The <span class="gradient-text">Calibrate · Decode · Activate</span> Framework</h2>
      <p>A three-phase intelligence pipeline transitioning from measurement to knowledge extraction and operational action.</p>
```
New:
```html
      <h2>The <span class="gradient-text">Discover · Calibrate · Decode · Activate</span> Framework</h2>
      <p>A four-phase intelligence pipeline transitioning from use-case discovery to measurement, knowledge extraction, and operational action.</p>
```

Old:
```html
    <div class="pipeline-diagram fade-up" style="margin: 0 auto 3rem auto; text-align: center; max-width: 900px;">
      <img src="/img/diagrams/product-pipeline.svg" alt="Calibrate Decode Activate Product Pipeline" style="width: 100%; height: auto; border: 1px solid #1f2937; border-radius: 8px;">
    </div>
```
New:
```html
    <div class="pipeline-diagram fade-up" style="margin: 0 auto 3rem auto; text-align: center; max-width: 1200px;">
      <img src="/img/diagrams/product-pipeline.svg" alt="Discover Calibrate Decode Activate Product Pipeline" style="width: 100%; height: auto; border: 1px solid #1f2937; border-radius: 8px;">
    </div>
```

- [ ] **Step 3: Method cards, insert Discover card and renumber**

Immediately after `<div class="method-grid">`, insert this new first card:
```html
      <div class="method-card fade-up">
        <div class="method-step">01</div>
        <div class="method-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
        </div>
        <div class="method-num-line">01 · Discover</div>
        <h3>AI Portfolio Explorer</h3>
        <p>Discover and score your AI use-case portfolio with <strong>AI Portfolio Explorer</strong>. Explicit funding and kill decisions before build spend is committed.</p>
        <a href="/products/ai-portfolio-explorer/" class="method-link">Explore AI Portfolio Explorer →</a>
      </div>
```

Then renumber the three existing cards:
- BenchMark card: `<div class="method-step">01</div>` becomes `02`; `<div class="method-num-line">01 · Calibrate</div>` becomes `02 · Calibrate`.
- DeepDive card: `02` becomes `03`; `02 · Decode` becomes `03 · Decode`.
- KnowHow card: `03` becomes `04`; `03 · Activate` becomes `04 · Activate`.

- [ ] **Step 4: Products grid, add Explorer card first**

Immediately after `<div class="products-grid">` and before the BenchMark featured card, insert:
```html
      <div class="product-card fade-up">
        <div class="product-label">Portfolio Governance</div>
        <h3>AI Portfolio Explorer</h3>
        <p>Discover, prioritize, and govern your enterprise AI use-case portfolio before build spend is committed.</p>
        <ul>
          <li>Use-case discovery &amp; inventory</li>
          <li>Priority matrix scoring</li>
          <li>Claude strategy co-pilot</li>
          <li>Enterprise connectors &amp; API</li>
        </ul>
        <a href="/products/ai-portfolio-explorer/" class="btn-ghost">Explore →</a>
      </div>
```
BenchMark keeps `product-card-featured` and its `btn-primary`.

- [ ] **Step 5: Grid CSS for four cards**

In `static/css/yadavilli.css`:

Old (line ~537):
```css
.method-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
```
New:
```css
.method-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}
```

Old (line ~769):
```css
.products-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr;
  gap: 1.5rem;
  align-items: start;
}
```
New:
```css
.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  align-items: start;
}
```

In the `@media (max-width: 1024px)` block, old:
```css
  .products-grid { grid-template-columns: 1fr 1fr; }
  .product-card-featured { grid-column: 1 / -1; }
```
New (drop the featured span so the grid stays 2x2 with four cards):
```css
  .products-grid { grid-template-columns: 1fr 1fr; }
```

Leave the 768px rules unchanged (they already collapse both grids to one column).

Caution: `.method-grid` may be used by other templates. Before committing, run:
```bash
grep -rn "method-grid" layouts/
```
If it appears outside `layouts/index.html`, check that page still lays out sensibly with two columns (it holds cards of the same type, so two columns is acceptable); note it in the commit message.

- [ ] **Step 6: Verify**

Run:
```bash
hugo --quiet -d "$HUGO_OUT" && grep -c "ai-portfolio-explorer" "$HUGO_OUT/index.html"
```
Expected: a number >= 2 (method link + product card link).

Run:
```bash
grep -c "AI Portfolio Explorer" "$HUGO_OUT/index.html"
```
Expected: a number >= 4 (two ticker entries, method card, product card).

- [ ] **Step 7: Commit**

```bash
git add layouts/index.html static/css/yadavilli.css
git commit -m "Add AI Portfolio Explorer to homepage ticker, method section, and product grid"
```

---

### Task 5: Footer link

**Files:**
- Modify: `layouts/partials/footer.html:36-41`

**Interfaces:**
- Consumes: `/products/ai-portfolio-explorer/` from Task 1.

- [ ] **Step 1: Add the link in pipeline order**

Old:
```html
        <h4>Products</h4>
        <ul>
          <li><a href="/products/benchmark/">BenchMark</a></li>
          <li><a href="/products/deepdive/">DeepDive</a></li>
          <li><a href="/products/knowhow/">KnowHow</a></li>
        </ul>
```
New:
```html
        <h4>Products</h4>
        <ul>
          <li><a href="/products/ai-portfolio-explorer/">AI Portfolio Explorer</a></li>
          <li><a href="/products/benchmark/">BenchMark</a></li>
          <li><a href="/products/deepdive/">DeepDive</a></li>
          <li><a href="/products/knowhow/">KnowHow</a></li>
        </ul>
```

- [ ] **Step 2: Verify**

Run:
```bash
hugo --quiet -d "$HUGO_OUT" && grep -c "products/ai-portfolio-explorer" "$HUGO_OUT/about/index.html"
```
Expected: a number >= 1 (footer renders on every page).

- [ ] **Step 3: Commit**

```bash
git add layouts/partials/footer.html
git commit -m "Add AI Portfolio Explorer to footer products list"
```

---

### Task 6: Case study

**Files:**
- Create: `content/case-studies/capital-markets-ai-portfolio.md`

**Interfaces:**
- Consumes: `/products/ai-portfolio-explorer/` from Task 1.

- [ ] **Step 1: Create the case study**

Write `content/case-studies/capital-markets-ai-portfolio.md` with exactly this content:

```markdown
---
title: "AI Portfolio Explorer Rationalizes AI Investment at a Capital Markets Firm"
date: 2026-07-04
description: "How portfolio-level scoring and governance turned 47 scattered AI ideas into 12 funded initiatives and a defensible kill list at a mid-size capital markets firm."
tag: "Capital Markets"
---

## The Challenge

A mid-size capital markets firm had 47 AI ideas scattered across trading, operations, compliance, and client service desks. Three desks were independently piloting near-identical document-intelligence tools. Two pilots had consumed budget for over a year with no production path and no defined conditions for shutdown. The head of technology could not answer the board's simplest question: what is the AI portfolio worth, and why these bets?

There was no inventory, no shared scoring model, and no kill criteria. Funding followed sponsor seniority, not portfolio logic.

## Our Approach

We deployed [AI Portfolio Explorer](/products/ai-portfolio-explorer/) as the single system of record for the firm's AI portfolio:

1. **Inventory**: Captured all 47 use cases in one workspace, seeded from the platform's capital-markets content pack and enriched through structured working sessions with each desk.

2. **Score**: Applied sector-specific dimensions (revenue impact, regulatory exposure, data readiness, execution complexity) to every use case. Scoring arguments happened in the open, against written criteria, with the Claude strategy co-pilot drafting rationales for the investment committee.

3. **Decide**: The priority matrix and maturity curve separated the portfolio into explicit decisions: 12 funded, 9 killed, 8 near-duplicates merged into 4 platform bets, and the remainder placed in a scored backlog with revisit dates.

4. **Govern**: Jira and ServiceNow connectors pushed every funding decision into delivery queues, and signed webhooks kept downstream systems current. Quarterly portfolio reviews now run from the dashboard instead of a month of slide assembly. The funded initiatives entered BenchMark for infrastructure calibration.

## The Results

- **47 ideas, 12 funded initiatives**: Each with an owner, a written scoring rationale, and pre-agreed kill criteria.
- **9 zombie pilots terminated**: Including the two year-old pilots, releasing engineers and budget within one quarter.
- **~30% of AI budget reallocated**: From duplicated and unviable pilots to the funded portfolio.
- **Governance cadence established**: Quarterly portfolio reviews compressed from weeks of preparation to a two-hour dashboard session.
```

- [ ] **Step 2: Verify**

Run:
```bash
hugo --quiet -d "$HUGO_OUT" && test -f "$HUGO_OUT/case-studies/capital-markets-ai-portfolio/index.html" && echo PAGE_OK
```
Expected: `PAGE_OK`

- [ ] **Step 3: Commit**

```bash
git add content/case-studies/capital-markets-ai-portfolio.md
git commit -m "Add capital markets AI portfolio case study"
```

---

### Task 7: Priority matrix diagram for the insight article

**Files:**
- Create: `static/img/diagrams/ai-portfolio-priority-matrix.svg`

**Interfaces:**
- Produces: diagram embedded by Task 8 at `/img/diagrams/ai-portfolio-priority-matrix.svg`.

- [ ] **Step 1: Create the SVG**

Write `static/img/diagrams/ai-portfolio-priority-matrix.svg` with exactly this content:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 660" width="1200" height="660" font-family="Inter, system-ui, sans-serif">
  <!-- Background -->
  <rect width="1200" height="660" fill="#09090b" rx="8" />

  <!-- Title -->
  <text x="600" y="46" fill="#e4e4e7" font-size="18" font-weight="700" text-anchor="middle">The Portfolio Selection Grid</text>
  <text x="600" y="70" fill="#71717a" font-size="12" text-anchor="middle">Every use case gets a quadrant and a decision. No side doors.</text>

  <!-- Quadrant: Incubate (high value, low feasibility) -->
  <g transform="translate(150, 100)">
    <rect width="440" height="220" fill="#2e1065" fill-opacity="0.25" stroke="#6d28d9" stroke-width="1" rx="6" />
    <text x="220" y="40" fill="#d8b4fe" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="1.5">INCUBATE</text>
    <text x="220" y="70" fill="#e4e4e7" font-size="13" text-anchor="middle">High value, not yet feasible</text>
    <text x="220" y="100" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Fund the readiness gap, not the build:</text>
    <text x="220" y="122" fill="#a1a1aa" font-size="11.5" text-anchor="middle">data quality, platform, skills</text>
    <text x="220" y="152" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Re-score on a set date</text>
  </g>

  <!-- Quadrant: Fund (high value, high feasibility) -->
  <g transform="translate(610, 100)">
    <rect width="440" height="220" fill="#052e16" fill-opacity="0.25" stroke="#065f46" stroke-width="1" rx="6" />
    <text x="220" y="40" fill="#6ee7b7" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="1.5">FUND</text>
    <text x="220" y="70" fill="#e4e4e7" font-size="13" text-anchor="middle">High value, high feasibility</text>
    <text x="220" y="100" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Assign an owner and a budget</text>
    <text x="220" y="122" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Write kill criteria before the first sprint</text>
    <text x="220" y="152" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Enter the delivery pipeline</text>
  </g>

  <!-- Quadrant: Kill (low value, low feasibility) -->
  <g transform="translate(150, 340)">
    <rect width="440" height="220" fill="#450a0a" fill-opacity="0.25" stroke="#7f1d1d" stroke-width="1" rx="6" />
    <text x="220" y="40" fill="#fca5a5" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="1.5">KILL</text>
    <text x="220" y="70" fill="#e4e4e7" font-size="13" text-anchor="middle">Low value, low feasibility</text>
    <text x="220" y="100" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Terminate now, in writing</text>
    <text x="220" y="122" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Release the budget and the engineers</text>
    <text x="220" y="152" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Record why, so it stays dead</text>
  </g>

  <!-- Quadrant: Merge or defer (low value, high feasibility) -->
  <g transform="translate(610, 340)">
    <rect width="440" height="220" fill="#451a03" fill-opacity="0.25" stroke="#78350f" stroke-width="1" rx="6" />
    <text x="220" y="40" fill="#fde047" font-size="13" font-weight="700" text-anchor="middle" letter-spacing="1.5">MERGE OR DEFER</text>
    <text x="220" y="70" fill="#e4e4e7" font-size="13" text-anchor="middle">Feasible, but thin value alone</text>
    <text x="220" y="100" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Fold duplicates into one platform bet</text>
    <text x="220" y="122" fill="#a1a1aa" font-size="11.5" text-anchor="middle">Park the rest in a scored backlog</text>
    <text x="220" y="152" fill="#a1a1aa" font-size="11.5" text-anchor="middle">No standing teams, no standing budget</text>
  </g>

  <!-- Y axis -->
  <g stroke="#3f3f46" stroke-width="1.5" fill="none">
    <path d="M 120 560 L 120 100" />
    <polygon points="120,96 116,104 124,104" fill="#3f3f46" stroke="none" />
  </g>
  <text x="112" y="330" fill="#71717a" font-size="12" font-weight="700" letter-spacing="1.5" text-anchor="middle" transform="rotate(-90 112 330)">VALUE</text>

  <!-- X axis -->
  <g stroke="#3f3f46" stroke-width="1.5" fill="none">
    <path d="M 150 590 L 1050 590" />
    <polygon points="1054,590 1046,586 1046,594" fill="#3f3f46" stroke="none" />
  </g>
  <text x="600" y="622" fill="#71717a" font-size="12" font-weight="700" letter-spacing="1.5" text-anchor="middle">FEASIBILITY</text>
</svg>
```

- [ ] **Step 2: Verify**

Run:
```bash
xmllint --noout static/img/diagrams/ai-portfolio-priority-matrix.svg && echo SVG_OK
```
Expected: `SVG_OK`

- [ ] **Step 3: Commit**

```bash
git add static/img/diagrams/ai-portfolio-priority-matrix.svg
git commit -m "Add portfolio priority matrix diagram"
```

---

### Task 8: Insight article

**Files:**
- Create: `content/insights/ai-use-case-lottery.md`

**Interfaces:**
- Consumes: `/products/ai-portfolio-explorer/` from Task 1; diagram from Task 7.

- [ ] **Step 1: Create the article**

Write `content/insights/ai-use-case-lottery.md` with exactly this content:

```markdown
---
title: "The Use-Case Lottery"
date: 2026-07-05
description: "Enterprises do not have an AI idea shortage. They have a selection problem. Most AI portfolios are stacks of lottery tickets bought by whoever pitched loudest, and the fix is portfolio governance, not more pilots."
tag: "Strategy"
---

## How AI Use Cases Get Selected Today

Walk into any large enterprise and ask for the list of AI initiatives. You will get a spreadsheet, assembled last quarter for a steering committee, already stale. It will contain somewhere between twenty and eighty rows. Ask a second question, "why these?", and the answers fall into three buckets: an executive sponsored it, a vendor demoed it, or a team was already experimenting and got grandfathered in.

None of those are selection criteria. They are acquisition stories. Nobody chose the portfolio. It accumulated, one sponsored ticket at a time.

This is the use-case lottery. Every business unit buys a ticket, funding flows to the tickets held by the best-connected sponsors, and the organization waits to see which ones pay out. Lottery economics follow. A few wins get amplified in internal communications, the losses persist quietly as zombie pilots, and nobody can say what the portfolio as a whole is worth, because it was never constructed as a portfolio.

<img src="/img/diagrams/ai-portfolio-priority-matrix.svg" alt="The Portfolio Selection Grid: a 2x2 matrix of value against feasibility, with quadrants for Fund, Incubate, Merge or Defer, and Kill, each carrying an explicit decision" style="width:100%;max-width:1200px;display:block;margin:32px auto;" />

## The Missing Discipline Is Selection, Not Execution

The standard diagnosis for weak AI results is execution: not enough talent, immature platforms, poor data. Execution problems are real, but they sit downstream of a selection problem that rarely gets named. If the use case should never have been funded, no amount of engineering rescues it.

A selection discipline has four parts, and most enterprises have none of them.

**A single inventory.** Use cases live in one system with owners, status, and scores, not in per-department slide decks. If assembling the full list takes a week of email, there is no inventory.

**Explicit scoring dimensions.** Value and feasibility, decomposed into dimensions that fit the sector: revenue impact, regulatory exposure, data readiness, execution complexity. The specific dimensions matter less than the fact that they are written down, applied to every candidate, and argued about in the open.

**Kill criteria set at funding time.** Every funded use case gets the conditions under which it dies, decided before the first sprint. Without pre-committed kill criteria, every review becomes a negotiation with a sponsor defending sunk cost.

**A governance cadence.** The portfolio gets re-scored and re-decided on a schedule, quarterly at minimum. New candidates enter through the same scoring gate, not through a side door labeled executive sponsorship.

## The Kill Decision Is the Product

Funding decisions are easy; enthusiasm does that work for free. The value of portfolio governance concentrates in the kills and the merges.

Killing a pilot releases budget, engineers, and the scarcest resource in any transformation: organizational attention. Merging three near-identical document-intelligence pilots into one platform bet removes two future migration projects before they exist. These are the compounding moves, and they only happen when the whole portfolio is visible in one place and the kill criteria were agreed before politics could form around each initiative.

There is a simple test of whether your organization governs its AI portfolio. Name the last AI initiative you killed on schedule, by pre-agreed criteria, without a sponsor fight. If there is no answer, the portfolio governs you.

## What Changes Under Governance

Selection discipline changes the questions leadership asks. "Which pilots look promising?" becomes "what is the portfolio worth, what did we kill this quarter, and what did the kills release?" Budget conversations move from defending line items to rebalancing a scored portfolio. The board question that terrifies technology leaders, "why these bets?", gets a written answer that predates the meeting.

It also changes what engineering receives. A funded use case arrives with an owner, a scoring rationale, and kill criteria, which means delivery teams inherit clarity instead of a sponsor's enthusiasm. Selection feeds calibration: the funded backlog is the input to infrastructure assessment, not an afterthought discovered mid-build.

This is the problem [AI Portfolio Explorer](/products/ai-portfolio-explorer/) exists to solve: a single inventory, sector-specific scoring, a priority matrix that makes fund, kill, and merge decisions legible, and connectors that push those decisions into Jira, ServiceNow, and the systems where delivery already happens. It is the Discover phase of our Discover · Calibrate · Decode · Activate pipeline. Nothing enters engineering until it has survived selection.

The lottery is comfortable because tickets are cheap and nobody audits the drawer they sit in. Governance is uncomfortable because every quarter it makes someone's project die in public. That discomfort is the point. It is what a portfolio costs, and it is far cheaper than the alternative: fifty tickets, three winners, and no idea which drawer the losses are in.
```

- [ ] **Step 2: Verify the page builds and the banned-pattern scan passes**

Run:
```bash
hugo --quiet -d "$HUGO_OUT" && test -f "$HUGO_OUT/insights/ai-use-case-lottery/index.html" && echo PAGE_OK
```
Expected: `PAGE_OK`

Run (em-dash scan across everything this plan created or touched):
```bash
grep -rn "—" content/insights/ai-use-case-lottery.md content/case-studies/capital-markets-ai-portfolio.md content/products/ai-portfolio-explorer.md content/about.md content/products/benchmark.md content/products/deepdive.md content/products/knowhow.md
```
Expected: no output (exit 1).

- [ ] **Step 3: Commit**

```bash
git add content/insights/ai-use-case-lottery.md
git commit -m "Add use-case lottery insight article"
```

---

### Task 9: Full-site verification

**Files:**
- No new files. Verification only; fix regressions in the files above if found.

- [ ] **Step 1: Clean build**

Run:
```bash
hugo -d "$HUGO_OUT" 2>&1 | tail -5
```
Expected: the Hugo build summary table with no WARN or ERROR lines.

- [ ] **Step 2: Link integrity for every new internal reference**

Run:
```bash
for p in products/ai-portfolio-explorer products/benchmark products/deepdive products/knowhow case-studies/capital-markets-ai-portfolio insights/ai-use-case-lottery; do test -f "$HUGO_OUT/$p/index.html" && echo "OK $p" || echo "MISSING $p"; done
```
Expected: six `OK` lines, zero `MISSING`.

- [ ] **Step 3: Rendered-output checks**

Run:
```bash
grep -c "AI Portfolio Explorer" "$HUGO_OUT/index.html"
grep -c "products/ai-portfolio-explorer" "$HUGO_OUT/products/benchmark/index.html"
grep -o "Discover · Calibrate · Decode · Activate" "$HUGO_OUT/about/index.html" | head -1
```
Expected: a number >= 4; a number >= 1 (footer plus cross-link); the framework string echoed once.

- [ ] **Step 4: Visual check in the preview server**

Start the Hugo dev server via the preview tooling (create `.claude/launch.json` with `{"version": "0.0.1", "configurations": [{"name": "hugo", "runtimeExecutable": "hugo", "runtimeArgs": ["server", "--port", "1313"], "port": 1313}]}` if absent). Then:

1. Homepage at desktop width: method grid shows 4 cards in 2x2, products grid shows 4 cards in 2x2, pipeline diagram shows four phases, ticker includes AI Portfolio Explorer.
2. Resize to mobile (375px): both grids collapse to one column, no horizontal overflow.
3. Footer on any page lists four products.
4. Product page, case study, and insight article render with correct titles and images.
5. Screenshot the homepage method + products sections and the new product page as proof.

- [ ] **Step 5: Final commit if verification produced fixes**

If steps 1 through 4 forced edits, commit them:
```bash
git add -A && git commit -m "Fix verification findings for AI Portfolio Explorer induction"
```
If nothing changed, skip.
