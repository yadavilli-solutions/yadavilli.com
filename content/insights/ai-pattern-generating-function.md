---
title: "Why These and Only These: The Generating Function Behind AI Product Patterns"
date: 2026-06-06
description: "A named list of patterns invites one question: says who? This is the answer — not a longer list, but the generating function that produces the patterns and the closure argument that bounds them."
tag: "Strategy"
---

## The List Problem

In [The AI Product Pattern Playbook](/insights/ai-product-pattern-playbook/) I named the patterns for embedding AI in a product: Copilot, Lookup, Oracle, Watchdog, Transformer, Autopilot, Persona. Seven patterns, placed on a grid.

A named list invites exactly one question, and it is the right one to ask: *says who?* Why these seven? Why not five, or twelve? What stops the next person from announcing an eighth, a ninth, a fortieth?

This is not a pedantic objection. It is the objection that destroyed the original software design pattern catalog as a closed system. The Gang of Four named twenty-three patterns in 1994. Within a decade there were pattern catalogs with hundreds of entries, because nothing in the original work explained why the number was twenty-three rather than two hundred. The patterns were *enumerated* — discovered by observation, named by taste. Enumeration has no closure. Any enumerated list is one clever counterexample away from growing, forever, with no principle to say stop.

So I am not going to defend a list. A list is indefensible by construction. I am going to defend a **generating function** — a rule that produces the patterns — and then show you the closure argument that turns "you missed one" from an unanswerable jab into a precise, falsifiable burden.

## The Crack in the Grid

Start with the inconsistency in my own framework. The Agency Shape grid has **four quadrants** — Feature, Specialist, Agent, Noise — but I placed **seven patterns** in it. Four boxes, seven things. The patterns are not the quadrants. Something finer is dividing them.

Look at the Specialist quadrant: high skill depth, low action breadth. Three patterns live there — Oracle, Watchdog, Transformer. All three have identical coordinates on the two published axes. High skill, narrow scope. So what makes them *different patterns* rather than three names for one thing?

The answer is what each one *does* with its skill:

- **Oracle** takes a question and returns a verified claim. It **answers**.
- **Watchdog** takes a stream and returns a flagged signal. It **monitors**.
- **Transformer** takes an input and returns an enriched output. It **converts**.

Answer, monitor, convert. These are not positions on the skill axis or the breadth axis. They are **operations** — distinct input-to-output types. The thing that separates patterns *within* a quadrant is a hidden third axis I never drew: the **primitive verb**, the irreducible operation the AI performs.

<img src="https://yadavilli.com/img/diagrams/ai-pattern-verb-grid.svg" alt="Three-axis grid of AI product patterns: primitive verb by skill depth by action breadth, showing filled cells and the empty high-skill generate cell" style="width:100%;max-width:900px;display:block;margin:32px auto;" />

Once you see the third axis, the patterns stop being a list. They become **cells** in a coordinate space: every pattern is a unique combination of `(verb × skill depth × action breadth)`. And a coordinate space is a thing you can *count* — and prove things about.

## The Empty Cell

Here is the first thing the coordinate view buys you, and it is the proof that this is a real method and not a story told after the fact.

If the Specialist quadrant is defined by `(high skill × low breadth × some verb)`, then the patterns in it are determined by *which verbs are viable* at high skill and low breadth. I claimed three: answer, monitor, convert. But there is an obvious fourth verb that belongs at high skill: **generate**.

Generation at *low* skill is already a pattern — that is Copilot, the autocomplete that suggests the next line and lets you accept or reject. But generation at *high* skill, in a narrow domain, with deep proprietary competence? That cell was **empty** in my original seven. Nothing filled it.

And yet the products that fill it are everywhere. The AI that drafts a complete, domain-correct contract from a brief. The system that generates a working code module from a spec. The tool that produces a finished design from a layout description. These are not Copilots — they do not suggest a fragment for you to accept; they produce a whole skilled artifact. They are not Oracles — they do not answer a question; they manufacture an object. They are a distinct pattern, and the grid *predicted the empty cell before I named the occupant*.

Call it the **Artifact Generator**: `(generate × high skill × low breadth)`. The eighth pattern. I did not find it by observing the market and adding it to a list. I found it by noticing a hole in a grid the generating function said should be full. That is the difference between enumeration and derivation. Enumeration finds patterns by looking outward at the world. Derivation finds them by looking at the structure and asking which cells the structure requires to exist.

## The Generating Function

Now state the rule precisely. A pattern is a **viable cell** in the grid `(primitive verb × skill depth × action breadth)`. Skill and breadth are binary — low or high — which buys a finite, countable grid at the cost of mid-range resolution. The verbs are the operations an AI product can perform as its core value proposition, and the working set is eight:

> **retrieve, generate, answer, monitor, transform, execute, converse, simulate**

That is `8 verbs × 2 skill × 2 breadth = 32` raw cells. Most are not viable. Four pruning rules, applied in order, cut the grid down to the patterns that actually exist:

**Rule A — Noise prune.** The entire low-skill, high-breadth row dies. Breadth without depth is the trap quadrant from the first article: an AI doing many things, none of them well. No verb survives here. *(−8 cells.)*

**Rule B — Fusion at the top.** At high skill and high breadth, every *action* verb collapses into a single purchased shape. When an AI executes, transforms, retrieves, and decides across a long multi-step horizon, the user does not buy four products — they buy one: **Autopilot**, the system that turns a goal into world-changing action. The action verbs fuse. Two verbs are exempt because they are not world-changing actions: **converse** (a medium, not an act — that is Persona) and **simulate** (acting into a model, not the real world — that is Sandbox). *(High/high collapses from 8 candidate cells to 3.)*

**Rule C — Skill floor.** At low skill and low breadth, only two verbs are value-complete with essentially zero competence: **generate** (thin completion — Copilot) and **retrieve** (bare fetch — Lookup). Everything else needs skill to be worth anything. *(2 cells survive.)*

**Rule D — Specialist coupling.** At high skill and low breadth, four verbs are each a complete, distinct product: **answer** (Oracle), **monitor** (Watchdog), **transform** (Transformer), **generate** (Artifact Generator). The other verbs are breadth-incompatible here — retrieve collapses into Lookup or Oracle, execute needs breadth greater than one, converse cannot be a single turn. *(4 cells survive.)*

The arithmetic:

| Quadrant | Cells | Patterns |
|---|---|---|
| Noise (low skill, high breadth) | 0 | — |
| Feature (low skill, low breadth) | 2 | Copilot, Lookup |
| Specialist (high skill, low breadth) | 4 | Oracle, Watchdog, Transformer, Artifact Generator |
| Agent (high skill, high breadth) | 3 | Autopilot, Persona, Sandbox |

**Nine patterns.** Not nine because I counted to nine. Nine because the generating function — eight verbs through four prune rules — emits exactly nine viable cells. Change the inputs and the output changes honestly: add a verb and you may add a pattern; tighten a prune rule and you remove one. The number is a *consequence*, not a *choice*. That is the entire point.

## The Closure Test

Here is what the generating function does that a list cannot: it converts the open-ended objection "you missed a pattern" into a bounded, four-way burden. Any pattern `P` that someone proposes must land in exactly one of four buckets — and **only the fourth can grow the set.**

<img src="https://yadavilli.com/img/diagrams/ai-pattern-closure-test.svg" alt="The four-bucket closure test: a proposed pattern resolves to an existing cell, a composite, a mechanism, or a new primitive verb" style="width:100%;max-width:900px;display:block;margin:32px auto;" />

**Bucket (a) — P reduces to a named cell.** State P's coordinates. If `(verb, skill, breadth)` already exists in the grid, P is an alias, not a new pattern. *Natural-language-to-SQL* is Oracle. *Customer-service chatbot* is Persona. *Fraud detection* is Watchdog. Different marketing, same cell.

**Bucket (b) — P is a composite.** P chains named cells into a workflow. The user buys a sequence, not a primitive. *Deep Research* is Autopilot orchestrating Lookup and Oracle. *AI Negotiator* is Autopilot plus Persona plus adversarial search. Composites are real products, but they are *combinations* of patterns, not new patterns — exactly as a sentence is not a new word.

**Bucket (c) — P is a mechanism.** P lives *inside* a cell, invisible at the product surface. This is the largest bucket and the one that catches the most confusion. ReAct, Plan-and-Execute, Tree-of-Thoughts, RAG plumbing, tool-calling, memory systems, multi-agent topologies like supervisor and swarm — these are *how a cell is wired internally*, not *what the product is*. The entire HAX, PAIR, and Apple HIG guideline corpus is mechanism. So are the Sheridan and SAE **autonomy levels** — they are a quantization of the breadth axis, not new patterns. And so is the **invocation protocol** from the first article — Pull, Poll, Push, Ambient move a pattern's *effective breadth*; they are an orthogonal control surface, not a fourth pattern dimension that mints new patterns.

**Bucket (d) — P introduces a new primitive verb.** This is the *only* growth path. To add a tenth pattern you must exhibit an input-to-output operation that is not reducible to the eight verbs, grounded in the type system over the things an AI can operate on: queries, knowledge stores, data streams, world-states, and dialogue. The burden is entirely on the challenger: *name the verb, show its I/O signature differs from all eight, and show it is not a composite of them.* That is a hard, specific, falsifiable claim — not a vague "surely there are more."

## The Red Team

A closure argument you have not attacked is just a hope. So I ran nineteen adversarial attempts to break it, across three independent lenses: one attacking from frontier model capabilities, one from specialized verticals, one from novel human-AI interaction modalities. Each was instructed to name the strongest missing pattern it could and try to force it past all four buckets.

**Eighteen of nineteen attacks were absorbed** — and absorbed *correctly*, into the bucket the structure predicts. The Reasoner (a chain-of-thought model) is a mechanism inside Oracle. The Computer-Use agent is Autopilot with a screen as its tool. The Memory Companion is Persona plus a memory mechanism. The Evaluator/Judge is a mechanism. Discoverer, Negotiator, Curator, Proactive Initiator, Co-Creator, Delegate, the society-of-agents — every one reduced to a named cell, a composite, or a sub-surface mechanism. A framework that could be broken by any of these would be a list in disguise. It held.

**One attack broke it.** The **Simulator** — an interactive generative world-model. The Genie-style learned world you can move through. The digital twin you drive with what-if actions. The physics or economy simulator that accepts your action and returns a coherent, navigable, causally consistent next world-state, into which you act again. Its I/O signature is `(world-state × action) → re-enterable next-world-state`, and that signature is carried by none of the seven prior verbs. It is not **generate**: the output is non-terminal and consistency-constrained, not a finished artifact. It is not **execute**: the world is modeled and reversible, not the irreversible real one. It is not **transform**: it is a sustained, branchable dynamical rollout, not a one-shot type conversion. It is a genuinely new primitive verb — **simulate** — and by the framework's *own* fourth bucket, it legitimately grows the grid.

So I added it. The verb **simulate** and its pattern **Sandbox**: `(simulate × high skill × high breadth)`, the interactive model you act *into*. It sits in the Agent quadrant beside Autopilot and Persona, exempt from the fusion rule for the same reason Persona is — you are not changing the real world, so it does not collapse into Autopilot. The seventh-to-ninth pattern was not invented to round out a story. It was forced by an adversary who found the one verb the eight-verb set was missing.

This is the signature of a real structure rather than a rationalization. A framework that absorbed *everything* would be unfalsifiable, and an unfalsifiable framework is worthless — it explains nothing because it forbids nothing. This one absorbed eighteen attacks and *grew on the nineteenth*, and it grew only where a type-theoretically irreducible verb provably appeared. It is closed everywhere except where a new verb forces it open, which is exactly as much closure as an honest taxonomy is allowed to claim.

<img src="https://yadavilli.com/img/diagrams/ai-pattern-nine-map.svg" alt="The final nine-pattern map: Copilot, Lookup, Oracle, Watchdog, Transformer, Artifact Generator, Autopilot, Persona, Sandbox, with Actuator flagged as a contested tenth" style="width:100%;max-width:900px;display:block;margin:32px auto;" />

## Where It Is Soft

The fastest way to lose a rigor argument is to oversell it. Three places where this one is genuinely contestable, stated plainly so you can defend the parts that hold and concede the parts that do not.

**The verb set is reasoned, not proven.** Everything downstream of the eight verbs is rigorous; the eight verbs themselves are asserted from a five-type I/O system, not proven minimal or complete. A critic can argue that **answer** decomposes into retrieve-plus-generate, pushing toward seven verbs, or that **decide** is irreducible, pushing toward nine. Both are defensible. The foundation is a reasoned choice, and the whole edifice inherits exactly that much uncertainty.

**The fusion rule is asymmetric.** Rule B collapses every action verb at high/high into Autopilot while exempting converse and simulate. The exemption rests on a judgment — "is this the same product the user buys?" — and that judgment is contestable at the margin. A different analyst could fuse differently and get eight patterns, or ten.

**Actuator is the live falsification target.** There is one pruned cell I did not silently bury: `(execute × high skill × low breadth)` — a single, irreversible, high-stakes action. One trade. One surgical incision. One kilohertz flight-control loop. I folded it into Autopilot's high/high cell on the argument that it is "an Autopilot with a breadth of one." A controls engineer or a roboticist will reasonably reject that — to them, a flight-control loop is not a degenerate workflow, it is its own pattern with its own failure model. This is where Rule D does the most work for the least independent justification, and it is the cell most likely to become a contested **tenth** pattern, **Actuator**. I flag it rather than defend it, because flagging the weakest joint is what makes the strong joints credible.

## The Defense

The point of all this is not to win the argument that there are exactly nine patterns. The point is to change what kind of argument it is.

If patterns are a list, "you missed one" is a coin flip and the list owner has no defense but assertion. If patterns are a generating function, "you missed one" becomes a specific, bounded burden: *name an irreducible I/O verb that is not retrieve, generate, answer, monitor, transform, execute, converse, or simulate — and show that it is not a composite of them and not an implementation mechanism beneath them.* That is a claim someone can actually win or lose. Most of the time they will find that their candidate is an alias, a composite, or a mechanism, and the conversation ends cleanly. Occasionally — as with simulate — they will find a real verb, and the framework will grow by exactly one cell, honestly, the way it is supposed to.

So when someone tells you there are more than nine AI product patterns, do not argue about the number. Say this:

> "These are not patterns I picked. They are the cells that survive a generating function — primitive I/O verb times skill depth times action breadth, minus four pruning rules. So 'you missed one' is not an opinion fight. Name an irreducible verb that is not one of the eight, and show it is not a composite or a mechanism. We red-teamed this nineteen ways. Eighteen attacks reduced to existing cells. The one that did not forced a new verb — interactive world-models, `simulate` — so we added it and the count went to nine. It is closed everywhere except where a new verb provably appears. That is the only kind of closure an honest taxonomy gets to have."

---

*The nine patterns, their definitions, and the maturity model for deploying them are in [The AI Product Pattern Playbook](/insights/ai-product-pattern-playbook/). If you want to know which pattern your product needs — and whether your organization can sustain it — [start with a conversation.](/contact/)*
