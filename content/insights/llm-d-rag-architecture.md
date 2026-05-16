---
title: "The Architecture Gap: What AWS Recommends vs What Production RAG Actually Requires"
date: 2026-05-14
description: "Most enterprises follow AWS's getting-started docs and point everything at Bedrock. That architecture was designed for demos, not production. Here is what production RAG actually costs you - and what fixes it."
tag: "Architecture"
---

## Everyone Copies the Getting-Started Guide

There is a pattern we see repeatedly. An engineering team discovers Amazon Bedrock, follows the AWS documentation, ships something that works in a demo, and calls it a RAG implementation. API Gateway in front, Bedrock behind, S3 for documents, done.

It is not wrong. It is just the starting point masquerading as the destination.

AWS documentation is written to get you to a working result quickly. It is not written to get you to a production architecture that survives real load, real cost pressure, and real observability requirements. The gap between those two states is not a configuration change. It is a systems redesign.

The teams that hit this wall are not making amateur mistakes. They are running an architecture that was designed for proofs of concept - and discovering that at scale, that design has three compounding problems: cost, latency, and zero visibility.

<img src="https://yadavilli.com/img/diagrams/rag-architecture-comparison.svg" alt="RAG architecture comparison: copy-cat Bedrock stack vs LLM-D architect stack" style="width:100%;max-width:900px;display:block;margin:32px auto;" />

## The Three Failure Modes

**Cost.** When everything routes to a single Bedrock model, every request - simple FAQ, complex multi-hop reasoning, semantic retrieval, tool call - bills at the same rate. There is no routing intelligence. A query that could have been handled by a smaller model at 10% of the cost is indistinguishable from one that genuinely requires your most capable model. The bill grows linearly with volume, with no ceiling and no optimization surface.

**Latency.** A single model is a single bottleneck. There is no batching, no KV cache, no path selection based on request complexity. Concurrent requests queue. Simple queries wait behind complex ones. The P99 climbs as volume grows, and there is nothing to tune because there is nothing to tune against.

**Observability.** The simple stack is a black box. You know a request went in and a response came out. You do not know which retrieved chunks informed the response, why the model chose one completion over another, whether retrieval latency or inference latency dominated the round trip, or whether the context window was bloated with irrelevant content. When quality degrades, you have no signal to debug.

These three problems compound. High cost makes you reluctant to add volume. Latency makes you reluctant to add features. Lack of observability makes you reluctant to make any change at all, because you cannot tell if you made it better or worse.

## What Production RAG Actually Requires

The architecture that solves these problems has eight layers. Each one exists because a production failure mode demanded it.

**The edge layer** handles what cloud infra handles everywhere: TLS termination, rate limiting, authentication. API Gateway, WAF, Cognito. Nothing exotic, but you need it as a discrete layer so it does not bleed into your routing logic.

**LLM-D** is where the architecture diverges from the getting-started path. LLM-D is not a load balancer. It is an inference gateway that makes routing decisions based on request type, backend load, model affinity, and KV cache state. It decides whether a request goes to a GPU-backed vLLM pod, a lighter inference endpoint, or Bedrock-managed inference - without the application layer knowing which backend handled it. That routing intelligence is the single highest-leverage change in the stack. It is the layer that makes cost optimization possible without application rewrites.

**The RAG Orchestrator** on EKS handles the branching decision that the simple stack never makes: does this request need retrieval? Can it go directly to inference? Is it a tool-use or function-calling request that should bypass the inference layer entirely? Getting this wrong in either direction is expensive. Unnecessary retrieval adds latency and context bloat. Skipping retrieval on knowledge-heavy queries produces hallucination. The orchestrator is where that judgment lives as explicit, auditable logic - not as an implicit hope that the model figures it out.

**The retrieval path** hits Qdrant for vector similarity search against your document corpus. Retrieval latency frequently dominates total response time. Your embedding model, your index configuration, and your top-K selection are not academic decisions. They are the primary lever on end-to-end latency for any retrieval-augmented request.

**Context assembly** is the layer that most teams skip and most cost overruns trace back to. Retrieved chunks do not go directly into the prompt. They get ranked, deduplicated, trimmed, and assembled. Every token you add to the context window increases inference cost and latency - linearly on cost, nonlinearly on attention computation. A context assembly layer that aggressively manages prompt size pays for itself in the first week.

**vLLM** at the inference layer handles continuous batching and KV caching on EKS GPU nodes. Continuous batching means concurrent requests do not each pay full cold-start cost - they share compute across a running batch. KV caching means that for requests with shared prefixes, you are not recomputing attention from scratch. Under real concurrency, these two properties together reduce effective inference cost by a significant margin. LLM-D routes to Bedrock where managed inference is appropriate - the hybrid gives you cost control without giving up access to frontier models.

**The response layer** closes the loop with token streaming, metrics collection, and end-to-end latency tracking. This is the layer that makes the system observable. Without it, you are back to the black box.

## Where the 60-70% Cost Reduction Comes From

The Bedrock-only architecture has no optimization surface. Every request is the same request.

The architect stack creates three cost levers that compound:

The first is path selection. Simple queries route to smaller, cheaper models and skip retrieval entirely. The inference cost drops to a fraction of the premium rate. This alone accounts for a significant share of the savings on typical enterprise workloads, because the majority of production queries are not complex.

The second is context management. Controlled prompt size means you are not paying for thousands of tokens of retrieved context when a few hundred relevant ones would have produced the same answer. Token count is a direct cost input. Managing it deliberately is the most underrated cost optimization in the stack.

The third is batching efficiency. vLLM's continuous batching means the per-request cost under concurrent load is materially lower than isolated inference. The savings scale with volume.

The result, across typical enterprise workloads, is 60-70% reduction in inference spend without any quality compromise on complex tasks. The routing intelligence is what makes this possible. You are not cutting corners - you are matching the resource to the requirement.

## RAG Is an Orchestration Problem

AWS provides the right building blocks. Bedrock, EKS, API Gateway, S3, WAF - these are the correct components for a production RAG stack. The architecture gap is not a missing AWS service.

The gap is the orchestration layer: the logic that decides which component handles which request, how retrieval integrates with inference, how context gets assembled and sized, and how the whole system is observed end-to-end.

AWS documentation describes what each service does. It does not tell you how to wire them together for your specific load profile, your latency targets, your retrieval corpus size, and your cost constraints. That wiring is where most of the value lives - and most of the risk. Getting it wrong means you have a production system that is expensive to run, difficult to debug, and structurally resistant to optimization.

Getting it right means you have a system that is cheaper as volume grows, faster under load, and improvable because you can actually see what is happening.

That is not a configuration option. That is systems architecture.

---

If you are evaluating whether your current AI infrastructure can support production RAG workloads, our [BenchMark assessment](/products/benchmark/) is the right starting point. [Start with a free infrastructure assessment.](/contact/)
