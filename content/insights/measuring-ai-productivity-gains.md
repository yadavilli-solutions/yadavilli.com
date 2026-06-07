---
title: "From Projection to Proof: A Framework for Measuring AI Productivity Gains"
date: 2026-06-07
description: "Calling the productivity measurement problem a Luddite argument misses the point. AI can deliver real gains. Most organisations are measuring for the wrong trajectory and getting false negatives as a result. Here is what rigorous looks like."
tag: "Strategy"
---

## The Luddite Question

The previous article on career insurance and AI spending prompted a predictable response from some quarters. The argument, they said, was anti-AI. A technology skeptic's position dressed up in framework language.

It was not. Let the record be clear on this point before moving on.

The claim was not that AI cannot improve productivity. The claim was that most enterprise AI spending was not purchased as a productivity bet, and that measuring it as one produces confusion rather than insight. Those are different claims. The first is empirically contestable. The second is behaviourally observable.

Here is the more interesting question: for the fraction of AI spending that genuinely is a productivity bet, how do you know if it is working?

The answer is that almost nobody does. Not because AI productivity gains are mythological. But because most organisations are measuring for the wrong trajectory entirely.

---

## Three Things Happen When AI Augments a Role

When AI is introduced into a workflow, one of three things happens to the role it touches. These trajectories are distinct, they require different measurement instruments, and conflating them is the source of most of the "weak AI productivity evidence" that keeps appearing in the research literature.

<img src="/img/diagrams/ai-three-trajectories.svg" alt="Three trajectories of AI augmentation: Shrinkage (same work, fewer people), Profile Change (same headcount, different work), and Replacement (role eliminated) — each with different timelines and measurement requirements" style="width:100%;max-width:920px;display:block;margin:32px auto;" />

**Shrinkage.** The role exists. The work continues. Fewer people are needed to do it. AI handles the volume. Humans supervise, handle exceptions, and manage quality. Over 18 to 36 months, headcount falls through attrition or deliberate reduction. Cost per unit of output decreases. This is the trajectory that cost savings arguments actually require. It is real in specific, narrow, high-volume workflows. Contract triage. Tier-1 support deflection. Document extraction from structured inputs. The causal chain is short. The economics are auditable.

**Profile change.** The headcount stays flat. The role name stays the same. But what people spend their time on shifts materially. Routine work is automated. The time that was spent on it reallocates: toward judgment, toward exceptions, toward strategy. The lawyer who reviewed 40 contracts a week now reviews 10 complex ones and spends the rest of the time on strategy. The analyst who spent 60% of their time gathering data now spends 60% interpreting it. The engineer who wrote boilerplate now writes architecture. The job title did not change. The job did. This is Benedict Evans' accountant: still called an accountant, doing completely different work than in 1980. This is almost certainly the dominant current trajectory in knowledge work, and it produces zero signal on cost metrics.

**Replacement.** The role is eliminated. AI executes end-to-end. The human layer is minimal or absent. This is the trajectory that dominates public anxiety about AI and employment. It is also the slowest to arrive, the most visible when it does, and currently the least common. Early signals are appearing in specific job families: some junior coding roles, some paralegal functions, tier-1 contact handling in some sectors. The timeline is years, not months. And before replacement typically arrives, a prolonged period of profile change precedes it.

A fourth trajectory runs alongside all three: **role creation**. New roles emerge that did not previously exist: AI operations, governance, prompt engineering, AI-assisted workflow design. These absorb some of the displacement from shrinkage and replacement while reflecting the new skill premium that profile change produces. The net employment math is genuinely unresolved. But the measurement question is tractable, trajectory by trajectory.

---

## Why Current Measurement Gets It Wrong

The productivity measurement debate is running almost entirely on shrinkage logic. Headcount per unit of output. Cost per unit of output. Developer throughput. Lines of code. Tickets resolved. Every metric in the standard AI ROI toolkit is a shrinkage metric. It detects the signal when the same work is being done by fewer people or at lower cost.

Profile change produces no signal on these instruments. None.

A team whose work composition has fundamentally shifted, with less routine work, more judgment, and higher complexity per unit handled, will appear flat on a shrinkage metric even as a genuine transformation is underway. The productivity measurement instruments will report: weak gains. The researchers will write: AI productivity evidence is mixed. The executives will wonder if they spent the money correctly.

What actually happened is that the instrument could not see the transformation it was pointed at.

<img src="/img/diagrams/ai-measurement-mismatch.svg" alt="The Wrong Instrument Problem: a 2x2 matrix showing that applying Shrinkage metrics to a Profile Change trajectory produces a systematic false negative — which is where most organisations currently sit" style="width:100%;max-width:920px;display:block;margin:32px auto;" />

This is not a small methodological footnote. If profile change is the dominant current trajectory in knowledge work (and the structural evidence suggests it is), then the majority of AI productivity research to date is a measurement of the wrong thing against the wrong baseline. The "weak evidence" finding is not evidence that AI is failing to transform work. It is evidence that the dominant transformation is invisible to the dominant measurement approach.

The researchers are not wrong about what they measured. They are wrong about what they were trying to detect.

---

## The Protocol: Identify Trajectory First

The pre-step that almost nobody takes is asking which trajectory a given workflow is on before selecting a measurement instrument. The right question is not: is AI making us more productive? The right question is: which trajectory is this workflow on, and am I using the instrument that can detect that trajectory's signal?

<img src="/img/diagrams/ai-measurement-protocol.svg" alt="Matched Measurement Protocol: three trajectories — Shrinkage, Profile Change, Replacement — each with the right measurement instrument, detection signal, and timeline" style="width:100%;max-width:920px;display:block;margin:32px auto;" />

**Measuring Shrinkage correctly** requires: a pre-deployment baseline of at least eight weeks, a fully-loaded cost stack on both sides (license fees plus AI operations headcount plus governance overhead, not just the license price), a defined unit of output that is locked before deployment, and a control group. Without a control group, you cannot separate AI impact from economic conditions, process changes, team composition, or the Hawthorne effect. Before/after comparisons with no control produce a positive signal for almost any intervention. They are not measurement.

The cost stack point deserves emphasis. A tool that saves £200,000 in labour costs but requires £80,000 in licenses, £90,000 in AI operations headcount, and £40,000 in governance overhead is a £10,000 loss. Most ROI calculations count only the licence. This is not an accounting error. It is a motivated omission.

**Measuring Profile Change correctly** requires an entirely different instrument. Time allocation studies (structured sampling of how people spend their time, before and after deployment) are the primary tool. The signal to track is not cost. It is the distribution of task types: what fraction of time goes to routine work versus judgment work, and how does that distribution change over 12 to 24 months? Secondary signals: the complexity of work being handled (are people taking on harder problems?), the skills premium in the labour market for roles that have undergone profile change, and the quality of high-judgment output compared to pre-AI baseline.

Profile change also carries a risk that shrinkage does not. If AI automates the routine work that used to build expertise (the contracts a junior lawyer reviewed that built their pattern recognition, the code a junior engineer wrote that built their debugging instincts), the team gains short-term efficiency and loses long-term judgment. The Friction Doctrine article covers this in detail. The measurement instrument for profile change must track not just what work is being done but whether the capability to do hard work is being maintained. Time allocation studies need a quality dimension, not just a volume dimension.

**Measuring Replacement correctly** operates on a different time horizon entirely. Three to seven years. The signals are external as much as internal: job posting volume in the relevant role family, organisation chart headcount in the target role over time, the ratio of AI-generated output to human-generated output in the workflow. This is the measurement that most organisations are not running because the timeline exceeds the budget cycle. Which is why replacement often arrives as a surprise rather than a tracked trend.

---

## The Scope Problem Nobody Accounts For

Across all three trajectories, there is a confound that invalidates most AI productivity claims even when the measurement instrument is correctly matched: scope expansion.

When AI reduces the cost of a task, organisations do not typically take the savings as savings. They take them as capacity. The team that used to handle 100 contracts a month can now handle 140. The developer who shipped two features a sprint now ships three. From the organisation's perspective, this looks like productivity. From a cost-savings perspective, it is nothing of the sort. The cost per unit fell, but so did the price per unit of new scope. The organisation is doing more work at the same total cost, not the same work at lower total cost.

This is the Jevons paradox applied to knowledge work: make a resource cheaper, people consume more of it. The productivity gain is real. The cost savings are not.

The measurement implication: any AI productivity claim must specify whether it is measuring efficiency gains (same output, lower cost) or throughput gains (more output, same cost). Both are valuable. Neither is the other. Most current claims slide between them depending on which looks more impressive.

---

## What Rigorous Measurement Actually Produces

An organisation that runs this protocol correctly (identifies trajectory, chooses the right instrument, captures pre-deployment baseline, controls for scope expansion, runs long enough to separate signal from Hawthorne effect) produces something that almost no organisation currently has: an attributed, quality-adjusted, trajectory-matched signal on whether AI is delivering in their specific workflows.

Not a vendor projection. Not a developer satisfaction survey. Not a post-hoc narrative constructed to justify a renewal. An actual reading.

That reading will almost certainly show three things simultaneously. In some workflows, specifically the high-volume, low-variance, short-causal-chain ones, genuine shrinkage is occurring and costs are falling. In most knowledge work workflows, profile change is happening at a pace that shrinkage metrics cannot see. In a small but growing set of roles, early replacement signals are present that the organisation should be tracking if only to plan transitions thoughtfully.

The organisations that build this measurement infrastructure will make compounding decisions. They will know where to invest more, where to stop, and where to reskill ahead of the transition rather than behind it. The organisations that continue to rely on vendor ROI projections and developer satisfaction surveys will continue to debate whether AI is "really" working, while the transformation they cannot see continues regardless.

The productivity measurement problem is not a reason to be sceptical of AI. It is an argument for being rigorous about it. Those are not the same thing. The Luddite has no interest in better measurement. The person asking for better measurement wants to know what is actually working, so they can do more of it.

---

If you are building the measurement infrastructure to track AI's actual impact on your workforce, [start with a free assessment.](/contact/)
