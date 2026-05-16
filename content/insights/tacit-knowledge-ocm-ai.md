---
title: "You Ingested All Your Documents. That's Maybe 20% of What Your AI Needs to Know."
date: 2026-05-15
description: "Ingesting your documents captures the official version of how things work. Not how things actually work. The gap is tacit knowledge - and closing it is why OCM is your real AI strategy."
tag: "Strategy"
---

## The Ingestion Milestone That Isn't One

The announcement comes at some point in nearly every enterprise AI deployment: we have ingested our documents. Fifty thousand PDFs. The policy library. The SOPs. The Confluence wiki. The SharePoint drive that nobody has organized since 2018. All of it vectorized, chunked, indexed, and queryable.

The team celebrates. The leadership team sees a demo. The AI surfaces relevant policies when asked. It retrieves the right SOP for a given workflow. It answers questions about the employee handbook with appropriate citations.

Then it goes to production and starts making recommendations that are technically consistent with the documented policies but wrong in ways that immediately strike any experienced employee as wrong. The AI does not know that the documented process for client escalation is always bypassed in practice because the regional director prefers direct calls. It does not know that the compliance framework from 2021 is still in the knowledge base but was superseded by an informal guidance memo that only two people have read. It does not know that the SOP for handling exception cases was written by a committee and has never reflected what senior analysts actually do.

The documents were accurate at the time they were written. They were never an accurate picture of how the organization actually works.

## The Knowledge You Cannot Ingest

Michael Polanyi described the core problem in 1966: "we know more than we can tell." The knowledge that makes experts expert is largely not articulable. It is pattern recognition built from thousands of decisions, calibrated intuition about when to apply which rule, judgment about which details matter in which context, and a constantly updated mental model of what is true now versus what was true when the procedure was written.

None of that is in your documents. Here is what is:

What documents contain: official procedures, stated policies, finished decisions, approved frameworks, and the conclusions of decisions that were worth writing up.

What documents do not contain: the reasoning behind those decisions, the alternatives that were rejected and why, the conditions under which the procedure does not apply, the heuristics that experienced people use to navigate ambiguity, the informal workarounds that have become standard practice, the things everyone knows not to do that nobody ever wrote down, and the judgment calls that senior people make instinctively because they have seen the failure modes.

The delta between what is documented and what is known is where your most experienced people live. It is also where your liability lives, your quality lives, and your competitive advantage lives. It is the part of organizational knowledge that takes six months to a year to transfer to a new hire informally - and that you are now assuming an AI system absorbs from your SharePoint.

It does not. It cannot.

## Why This Mistake Is Structurally Predictable

The document ingestion approach feels like it solves the problem because it is visible, measurable, and completable. You can count the documents. You can track ingestion progress. You can demo the retrieval. None of those things are possible with tacit knowledge, which is why tacit knowledge does not make it into the project plan.

The result is a knowledge substrate that captures the organization's official self-description rather than its operational reality. Official self-description is useful. It is not sufficient for a system that needs to operate the way your best people operate.

The deeper problem is that document ingestion is the only knowledge transfer mechanism most AI deployments plan for. There is no second phase. Once the documents are in, the team moves on to building features, and the knowledge base settles into its permanent state as an accurate record of what the organization believed at some point in the past.

This is the ingestion fallacy: the belief that ingesting what the organization has documented is equivalent to capturing what the organization knows.

## What Tacit Knowledge Actually Looks Like

Consider a senior underwriter at an insurance company with fifteen years of experience. Her job involves applying a complex policy framework to novel situations. Her formal knowledge base - everything she could point to if asked - includes the underwriting guidelines, the risk models, the regulatory requirements, and the pricing framework.

Her actual expertise includes none of that. Any junior analyst with access to the documents has the same formal knowledge base. Her expertise is:

She knows which risk categories the models systematically underweight because of how the training data was constructed. She knows which clients tend to underreport on the dimensions that matter most and how to adjust for it. She knows the difference between a claim pattern that looks risky and one that is risky. She knows which regulatory interpretations are technically defensible but will create examination friction. She knows when the pricing model is right and when to override it.

None of that is in a document. Some of it cannot be articulated even if she tries. Some of it she does not know she knows until she encounters a situation that requires it and makes a judgment call that she could not have explained in advance.

An AI system trained on your underwriting documentation will produce outputs that are textually consistent with your policies and wrong in the ways that matter most - because the ways that matter most are exactly what the documentation does not contain.

## OCM Is Not Change Management. It Is Knowledge Architecture.

Organizational Change Management in most AI deployments is understood as the soft work: getting people comfortable with the new tool, running training sessions, managing resistance, communicating the benefits. It is treated as the non-technical track that runs alongside the real technical work.

This framing misses what OCM actually needs to accomplish in an AI deployment. The primary function of OCM in this context is not adoption. It is knowledge extraction.

Before your AI system can operate the way your best people operate, someone has to get what your best people know out of their heads and into a form the system can use. That is an organizational problem, not a technical one. It requires structured processes, skilled facilitation, and sustained effort over time. It does not happen automatically as a byproduct of deploying a chatbot.

The organizations that are getting this right are running OCM as a knowledge architecture program. The activities look different from traditional change management:

**Knowledge mapping** identifies who knows what - not what is documented where, but which individuals carry the critical tacit knowledge for each domain. The goal is a dependency map of expertise: if this person leaves, what does the organization lose that cannot be reconstructed from existing documents?

**Structured elicitation sessions** are facilitated conversations designed to surface undocumented knowledge. Not "tell us what you know" - that produces a restatement of documented procedures. Effective elicitation uses scenario-based questioning: walk me through the last five exception cases you handled. What did you notice that made you treat them differently? What would a junior analyst have missed? The tacit knowledge surfaces in the specifics, not in the general.

**Shadow sessions** capture the undocumented steps. A skilled facilitator watches an expert work and documents the judgment calls that the expert makes without noticing - the moment they checked an additional source before making a recommendation, the way they adjusted their framing based on who was asking, the detail they noticed that flagged a routine case as non-routine. These invisible decision points are where expert performance differs from average performance, and they are never in the SOP.

**Error-as-knowledge-capture** turns every AI failure into an elicitation opportunity. When the system produces an output that an experienced person flags as wrong, the right response is not to log it as a bug and move on. It is to run a structured session: what did the system miss? What would you have known that led you to a different conclusion? What pattern is the system not recognizing? Each flagged error is a window into a piece of tacit knowledge the system does not have. Treated systematically, error logs become a knowledge extraction pipeline.

**Feedback loops** maintain the knowledge base as the organization evolves. Procedures change. Best practices shift. New failure modes get discovered. A knowledge base that reflects the organization as it was at ingestion time and not as it is now degrades in quality continuously. OCM is the organizational mechanism that keeps the knowledge substrate current - not through re-ingestion of documents, but through structured channels for surfacing and encoding what is being learned.

## The Knowledge Substrate Is a Living System

The deeper architectural point is that a knowledge substrate in an AI system is not a project deliverable. It is not something you build once, declare complete, and move on from. It is a living representation of what the organization knows, which means it requires the same ongoing maintenance that organizational knowledge itself requires.

Organizations with strong institutional knowledge invest continuously in the mechanisms that maintain it: mentorship structures, communities of practice, lessons-learned processes, knowledge transfer protocols when people leave. These mechanisms exist because everyone who has run an organization knows that institutional knowledge evaporates without active maintenance.

An AI system that depends on organizational knowledge inherits this maintenance requirement. The ingestion milestone is not the end of the knowledge problem. It is the beginning of the knowledge maintenance problem.

OCM is how you build the organizational structures and habits that keep the knowledge substrate accurate and current. Without it, you have a system that knows what your organization knew at a point in time, slowly diverging from what your organization actually knows now, with no mechanism to close the gap.

## What Gets Built Without This

The absence of a structured approach to tacit knowledge extraction produces a specific and predictable failure mode: an AI system that performs excellently on the cases that are well-documented and poorly on the cases that require judgment.

The well-documented cases are not the ones that matter most. They are the routine cases - the ones your least experienced people handle adequately. The judgment cases are the ones that differentiate expert performance from average performance. They are the cases where mistakes are expensive, where client relationships are won or lost, where compliance risk concentrates.

A system that is excellent on routine cases and unreliable on judgment cases is not a productivity multiplier. It is a liability amplifier - it scales the part of the work that needed the least help and provides no leverage on the part that needed the most.

The path out of this is not a better retrieval architecture or a more capable model. It is the organizational work of getting tacit knowledge into a form the system can use. That is OCM's job. And it is the job that most AI deployments never assign to anyone.

---

If you are designing an AI adoption program and trying to work out how to capture the institutional knowledge that makes your organization effective - not just the documents - [start with a free assessment.](/contact/)
