---
title: "The Architecture Gap: What AWS Recommends vs What Production RAG Actually Requires"
date: 2026-05-14
description: "Most enterprises follow AWS's getting-started docs and point everything at Bedrock. Here's why that's costing them — and what production RAG actually requires."
tag: "Architecture"
---

## The Copy-Cat Problem

AWS documentation is excellent for getting started. The problem is that "getting started" and "production-ready" are different destinations — and the path between them isn't a config option.

Most enterprises that come to us have followed the path of least resistance: API Gateway → Bedrock. It works. It ships. It demos beautifully. Then the bills arrive, the latency climbs, and the team realizes they have zero visibility into what's actually happening between the request and the response.

They're not doing anything wrong. They're running an architecture that was designed for proofs of concept, not production workloads. The gap is real, it compounds at scale, and the good news is it's well-understood — if you know what to look for.

<div class="diagram-embed">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Header ─────────────────────────────────────────── */
.header { text-align: center; margin-bottom: 28px; }
.eyebrow {
  font-size: 10px; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase; color: #06b6d4; margin-bottom: 10px;
}

/* ── Copy-cat strip ──────────────────────────────────── */
.before {
  max-width: 880px; margin: 0 auto 10px;
  background: #0e0810; border: 1px solid #2e1620;
  border-radius: 10px; padding: 14px 18px;
}
.section-pill {
  font-size: 9px; font-weight: 700; letter-spacing: .12em;
  text-transform: uppercase; padding: 3px 9px;
  border-radius: 20px; display: inline-block; margin-bottom: 12px;
}
.pill-bad  { background: #3a1a22; color: #d06060; }
.pill-good { background: #0c3030; color: #10b981; }

.cc-row { display: flex; align-items: center; gap: 0; }
.cc-box {
  flex: 1; background: #1a0e14; border: 1px solid #3a2028;
  border-radius: 7px; padding: 9px 10px; text-align: center;
}
.cc-box .t { font-size: 12px; font-weight: 600; color: #c4a0a0; }
.cc-box .s { font-size: 10px; color: #7a5a5a; margin-top: 2px; }
.cc-box.hero { flex: 2.5; background: #1e0c14; border-color: #5a2030; }
.cc-box.hero .t { color: #e07070; font-size: 13px; }
.cc-arr { color: #4a2530; font-size: 18px; padding: 0 7px; flex-shrink: 0; }
.cc-note {
  font-size: 11px; color: #7a5060; font-style: italic;
  margin-top: 10px; padding-top: 8px; border-top: 1px solid #2a1520; line-height: 1.5;
}

/* ── VS divider ──────────────────────────────────────── */
.vs {
  max-width: 880px; margin: 0 auto;
  display: flex; align-items: center; gap: 14px; padding: 10px 0;
}
.vs-line { flex: 1; border-top: 1px solid #1e2630; }
.vs-badge {
  font-size: 11px; font-weight: 700; color: #4a5560;
  border: 1px solid #2a3040; background: #0a0f18;
  border-radius: 20px; padding: 4px 12px; letter-spacing: .04em;
}

/* ── Architect section ───────────────────────────────── */
.after {
  max-width: 880px; margin: 0 auto;
  background: #050e10; border: 1px solid #0c3030;
  border-radius: 10px; padding: 16px 18px 18px;
}

/* Top row: steps 1-4 */
.row { display: flex; align-items: stretch; margin-bottom: 8px; }
.step {
  flex: 1; border-radius: 8px; padding: 11px 12px; position: relative;
}
.step-arr {
  display: flex; align-items: center; justify-content: center;
  color: #1e3040; font-size: 18px; padding: 0 5px; flex-shrink: 0;
}
.n { font-size: 9px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; margin-bottom: 5px; opacity: .75; }
.t { font-size: 12px; font-weight: 700; margin-bottom: 3px; line-height: 1.3; }
.s { font-size: 10px; line-height: 1.4; opacity: .7; }
.ann {
  font-size: 10px; font-style: italic; color: #3a5868;
  border-left: 2px solid #0d3040; padding-left: 7px;
  margin-top: 7px; line-height: 1.45;
}

/* Step colors */
.s1 { background: #0c1620; border: 1px solid #172840; }
.s1 .n { color: #7a8eb0; } .s1 .t { color: #a0b4ce; }

.s2 { background: #0a1420; border: 1px solid #142840; }
.s2 .n { color: #6a80a8; } .s2 .t { color: #8aaace; }

.s3 { background: #051616; border: 1px solid #0a3838; }
.s3 .n { color: #06b6d4; } .s3 .t { color: #06b6d4; } .s3 .ann { border-color: #0c4040; }

.s4 { background: #071610; border: 1px solid #0e3828; }
.s4 .n { color: #10b981; } .s4 .t { color: #10b981; } .s4 .ann { border-color: #103830; }

/* Route label */
.route-label {
  text-align: center; font-size: 10px; color: #2e4050;
  letter-spacing: .06em; font-style: italic; margin-bottom: 7px;
}

/* Branch: 5a / 5b / 5c */
.branches {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 8px; margin-bottom: 8px;
}
.b5a { background: #060c20; border: 1px solid #0e2550; }
.b5a .n { color: #4a80c0; } .b5a .t { color: #6aaae0; } .b5a .ann { border-color: #0e2850; }

.b5b { background: #050c18; border: 1px solid #0c2640; }
.b5b .n { color: #3a90b8; } .b5b .t { color: #5ab0d8; } .b5b .ann { border-color: #0c2840; }

.b5c { background: #0c0c18; border: 1px solid #1e1e40; }
.b5c .n { color: #7070b8; } .b5c .t { color: #9090d8; } .b5c .ann { border-color: #1e2040; }

/* Down arrow */
.down { text-align: center; color: #1a3040; font-size: 18px; margin: 5px 0; }

/* Bottom row: 6-7-8 */
.s6 { background: #060e18; border: 1px solid #0e2840; }
.s6 .n { color: #5a7a98; } .s6 .t { color: #8aaabe; } .s6 .ann { border-color: #0e2840; }

.s7 { flex: 1.8; background: #040e08; border: 1px solid #0a3020; }
.s7 .n { color: #10b981; } .s7 .t { color: #10b981; } .s7 .ann { border-color: #103820; }

.s8 { background: #0c1018; border: 1px solid #1a2030; }
.s8 .n { color: #8b95a5; } .s8 .t { color: #a0aab8; }

/* ── Comparison grid ─────────────────────────────────── */
.grid {
  max-width: 880px; margin: 12px auto 0;
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px;
}
.gc {
  background: #08111a; border: 1px solid #122030;
  border-radius: 8px; padding: 11px 12px;
}
.gc-label { font-size: 10px; font-weight: 700; color: #c4ccd6; margin-bottom: 7px; }
.gc-bad  { font-size: 10px; color: #905050; line-height: 1.4; padding-left: 10px; position: relative; }
.gc-good { font-size: 10px; color: #10b981;  line-height: 1.4; padding-left: 10px; position: relative; margin-top: 5px; }
.gc-bad::before  { content: '–'; position: absolute; left: 0; color: #904040; }
.gc-good::before { content: '+'; position: absolute; left: 0; color: #10b981; }

/* ── Insight bar ─────────────────────────────────────── */
.insight {
  max-width: 880px; margin: 12px auto 0;
  background: #06101e; border: 1px solid #102840;
  border-radius: 10px; padding: 15px 22px; text-align: center;
}
.insight p { font-size: 13px; color: #8b95a5; line-height: 1.7; }
.insight strong { color: #06b6d4; }
</style>

<!-- BEFORE -->
<div class="before">
  <span class="section-pill pill-bad">The Copy-Cat Stack — point everything at Bedrock</span>
  <div class="cc-row">
    <div class="cc-box"><div class="t">Client</div><div class="s">Web · APIs · Agents</div></div>
    <div class="cc-arr">→</div>
    <div class="cc-box"><div class="t">API Gateway</div><div class="s">Basic routing</div></div>
    <div class="cc-arr">→</div>
    <div class="cc-box hero"><div class="t">Amazon Bedrock</div><div class="s">One model · Every request · Same premium rate</div></div>
    <div class="cc-arr">→</div>
    <div class="cc-box"><div class="t">Response</div><div class="s">Hopefully correct</div></div>
  </div>
  <div class="cc-note">Simple query, complex reasoning, or knowledge retrieval — everything bills at your largest model's rate with zero routing intelligence, no retrieval, and a single point of latency.</div>
</div>

<div class="vs"><div class="vs-line"></div><div class="vs-badge">vs the architect path</div><div class="vs-line"></div></div>

<!-- AFTER -->
<div class="after">
  <span class="section-pill pill-good">The Architect Stack — LLM-D + vLLM on EKS</span>

  <!-- Top row: 1–4 -->
  <div class="row">
    <div class="step s1">
      <div class="n">1 · Clients</div>
      <div class="t">Web Apps · AI Agents · APIs</div>
      <div class="s">All request types enter here</div>
    </div>
    <div class="step-arr">→</div>
    <div class="step s2">
      <div class="n">2 · Edge (AWS)</div>
      <div class="t">API GW + WAF + Cognito</div>
      <div class="s">TLS termination · Rate limiting · Authentication</div>
    </div>
    <div class="step-arr">→</div>
    <div class="step s3">
      <div class="n">3 · LLM-D Gateway</div>
      <div class="t">Intelligent Routing</div>
      <div class="s">Request routing · Load balancing · Policy enforcement · Rate limits</div>
      <div class="ann">LLM-D decides routing, not just load balancing — routes to optimal backend based on request type</div>
    </div>
    <div class="step-arr">→</div>
    <div class="step s4">
      <div class="n">4 · RAG Orchestrator (EKS)</div>
      <div class="t">Request Parsing · Prompt Building · Tool Decision Logic</div>
      <div class="s">Decides: retrieve? call tools? direct to LLM?</div>
      <div class="ann">Decides: retrieve? call tools? or direct LLM?</div>
    </div>
  </div>

  <!-- Routing label -->
  <div class="route-label">↓ &nbsp; routes to right path per request type &nbsp; ↓</div>

  <!-- Branches: 5a / 5b / 5c -->
  <div class="branches">
    <div class="step b5a">
      <div class="n">5a · Retrieval Layer</div>
      <div class="t">Qdrant (self-hosted or EKS) or Managed alternative</div>
      <div class="s">Embedding lookup · Top-K retrieval · Amazon S3 document store</div>
      <div class="ann">Retrieval latency often dominates total response time</div>
    </div>
    <div class="step b5b">
      <div class="n">5b · Direct LLM Path</div>
      <div class="t">Simple Queries — Skip Retrieval</div>
      <div class="s">Cheaper · Faster · Right-sized for low-complexity requests</div>
      <div class="ann">Bigger context ≠ better answers. Context size ↑ → latency ↑ and cost ↑</div>
    </div>
    <div class="step b5c">
      <div class="n">5c · Tool Path</div>
      <div class="t">Function Calls · Orchestration</div>
      <div class="s">Agentic workflows · API integrations · External tool use</div>
      <div class="ann">Tool-use routes through orchestrator, bypasses inference layer</div>
    </div>
  </div>

  <!-- Down arrow -->
  <div class="down">↓</div>

  <!-- Bottom row: 6-7-8 -->
  <div class="row">
    <div class="step s6">
      <div class="n">6 · Context Assembly</div>
      <div class="t">Retrieved Chunks · Prompt Construction</div>
      <div class="s">Token expansion · Reranking · Context optimization</div>
      <div class="ann">Context size ↑ = latency ↑ and cost ↑ — managed here</div>
    </div>
    <div class="step-arr">→</div>
    <div class="step s7">
      <div class="n">7 · Hybrid LLM Inference</div>
      <div class="t">vLLM on EKS GPU Nodes · Amazon Bedrock (managed)</div>
      <div class="s">Continuous batching · KV cache on GPU pods · Hybrid model routing via LLM-D · API-based inference</div>
      <div class="ann">Hybrid inference = flexibility + cost control. Right model per complexity.</div>
    </div>
    <div class="step-arr">→</div>
    <div class="step s8">
      <div class="n">8 · Response + Streaming</div>
      <div class="t">Token Streaming · Formatting</div>
      <div class="s">Optional caching · Metrics &amp; signals · End-to-end latency tracking</div>
    </div>
  </div>

</div>

<!-- Key differences -->
<div class="grid">
  <div class="gc">
    <div class="gc-label">Cost</div>
    <div class="gc-bad">Premium rate, every call</div>
    <div class="gc-good">Right model per complexity — 60–70% savings</div>
  </div>
  <div class="gc">
    <div class="gc-label">Knowledge</div>
    <div class="gc-bad">Stale training data or hallucination</div>
    <div class="gc-good">Live semantic retrieval via Qdrant + S3</div>
  </div>
  <div class="gc">
    <div class="gc-label">Latency</div>
    <div class="gc-bad">Single model bottleneck, no batching</div>
    <div class="gc-good">Continuous batching + KV cache + path selection</div>
  </div>
  <div class="gc">
    <div class="gc-label">Scale</div>
    <div class="gc-bad">Vendor-managed only, no GPU control</div>
    <div class="gc-good">Each EKS layer scales independently</div>
  </div>
  <div class="gc">
    <div class="gc-label">Control</div>
    <div class="gc-bad">Black box — no observability per layer</div>
    <div class="gc-good">Observable, tunable, and measurable end-to-end</div>
  </div>
</div>

<div class="insight">
  <p><strong>RAG on AWS = Orchestration + Retrieval + Inference.</strong> RAG is a systems problem, not a prompt problem. The gap isn't a config option — it's systems knowledge. AWS docs describe the components. An architect knows how to wire them for your load, your data, and your cost targets.</p>
</div>

</div>

## The 8 Layers Production RAG Actually Requires

The architect stack isn't complicated for its own sake. Every layer exists because production workloads exposed a failure mode that the simple path couldn't handle.

**LLM-D** sits at layer three — not as a dumb load balancer, but as an intelligent inference gateway that routes requests to the optimal backend based on load, model affinity, and KV cache state. It decides whether a request goes to a heavyweight GPU pod, a lighter inference endpoint, or Bedrock-managed inference — without the application needing to know which backend handles it. That backend-routing intelligence alone improves throughput and reduces cold-path latency significantly.

The **RAG Orchestrator** on EKS is where the branching logic lives. It reads the incoming request and makes a call: does this need retrieval? Can it go direct to the LLM? Is this a tool-use or function-calling request that should bypass inference altogether? Getting this wrong in either direction is expensive — unnecessary retrieval adds latency; skipping retrieval on knowledge-heavy queries produces hallucination.

The retrieval path hits **Qdrant** for vector similarity search against your document corpus in S3. Retrieval latency frequently dominates total response time — which means your embedding model choice, index configuration, and top-K selection aren't academic decisions.

Context assembly at layer six is where retrieved chunks get ranked, trimmed, and assembled into the final prompt. Bigger context is not better. Every token you add to the context window increases both inference cost and latency — linearly on cost, nonlinearly on attention. Reranking and context optimization here pay for themselves immediately.

**vLLM** at layer seven handles inference on EKS GPU nodes with **continuous batching** and a **KV cache** that dramatically improves throughput under concurrent load. LLM-D routes to Bedrock for managed inference when appropriate. The hybrid model gives you cost control, GPU flexibility, and the option to run open-weight models where proprietary ones aren't warranted.

Layer eight closes the loop: streaming responses, token-level metrics, and end-to-end latency tracking you can actually act on.

## Where the Cost Goes

The Bedrock-only pattern bills every request at your largest model's rate. A simple FAQ lookup, a complex multi-hop reasoning chain, and a retrieval-augmented response with fifty retrieved chunks all hit the same meter.

The architect stack disaggregates this. Simple queries route to smaller, cheaper models and skip retrieval entirely — the inference cost drops to a fraction. Retrieval-augmented queries use context assembly to keep prompt size controlled, which directly reduces token count. GPU-batched inference on vLLM means concurrent requests don't each pay full cold-start cost.

The result is 60–70% reduction in inference spend on typical enterprise workloads — without any compromise on output quality for complex tasks. The savings come from routing intelligence, not model downgrading.

None of this happens automatically. It requires knowing where to cut, what to route where, and how to instrument the system to verify the decisions are working.

## RAG Is a Systems Problem

AWS provides excellent building blocks. Bedrock, EKS, API Gateway, S3 — these are the right components for a production RAG stack. The architecture gap isn't a missing AWS service.

The gap is the **orchestration layer**: the logic that decides which component handles which request, how retrieval integrates with inference, how context is assembled and sized, and how the whole system is observed end-to-end. AWS documentation describes what each service does. It doesn't tell you how to wire them together for your load profile, your latency targets, and your cost constraints.

That's not a configuration option. That's an architect.

---

If you're evaluating whether your current AI infrastructure can support production RAG workloads, our [BenchMark assessment](/products/benchmark/) is the right starting point. [Start with a free infrastructure assessment.](/contact/)
