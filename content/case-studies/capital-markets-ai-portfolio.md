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
