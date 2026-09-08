---
title: "Spark Declarative Pipelines: What You Own After You Adopt Them"
date: 2026-09-08
description: "An evaluation of Apache Spark 4.2.0 Declarative Pipelines, measured on a single-node OCI lab, checked against vendor documentation, with the architecture consequences for teams already running Airflow and dbt."
tag: "Architecture"
author: "Aswani Karteek Yadavilli"
---

*Aswani Karteek Yadavilli | September 2026*

---

## The short version

Open-source Spark Declarative Pipelines is a triggered batch orchestrator with incremental streaming ingestion and no incremental view refresh. That is a useful thing. It is not the thing most of the current commentary implies.

From the lab:

- Batch materialized views **fully recompute on every run**. Not on schema change, not on source change. Every run.
- Streaming tables **do process incrementally**, correctly, with offset-accurate recovery across a hard kill.
- `Trigger.AvailableNow()` is hardcoded into the only execution class that ships. No continuous mode, no interval flag, nothing in the pipeline spec to change it.

Databricks confirms the second and third points from the other direction. Their own capability comparison lists continuous mode as a Lakeflow addition rather than an SDP feature, and their engineering blog states that continuous execution and more efficient incremental processing are planned for future Spark releases. So the gaps are acknowledged, not disputed. Anyone telling you open SDP is a streaming runtime today is ahead of both the code and the vendor.

The practical read: SDP removes the orchestration code you used to write around a set of interdependent Spark jobs. It does not remove your scheduler, your CDC layer, your data quality framework, or your catalog decision.

My recommendation: pilot open SDP on one greenfield ingestion path. Do not migrate an existing Airflow and dbt estate on this release. And if you are evaluating Databricks Lakeflow specifically for incremental refresh, check your compute tier first, because on classic compute you get the same full recompute the open version gives you.

---

## What SDP actually moves

You define streaming tables, materialized views, and the flows that write into them. SDP resolves the dependency graph and orchestrates execution order and parallelism without you writing the wiring. That is accurate and it is real.

What stays outside the boundary on Apache 4.2.0 is longer than the marketing suggests, and Databricks publishes the list themselves. Their comparison of SDP against Lakeflow pipelines names five capabilities the managed version adds: AUTO CDC covering SCD Type 1 and Type 2 plus CDC from snapshot, data quality expectations, a queryable event log, update flows and `foreachBatch` sinks, and continuous mode.

Read that list as a scope statement for the open version. If your architecture assumes change data capture, declarative quality constraints, or an event log you can query for lineage and freshness, none of it is upstream. You keep whatever you use today.

Add one more item the vendor list does not cover: triggering. Something external has to invoke `spark-pipelines run`. Cron, Airflow, a Kubernetes CronJob, your choice.

So the code you delete is the DAG definition and the manual ordering of dependent transforms. On a pipeline with twenty interdependent tables that is meaningful. It is also a narrower deletion than "the framework manages orchestration and recovery" implies.

---

## What the lab measured

Setup and method are in the appendix. Everything in this section is observation from run logs, checkpoint files, and bytecode on a live instance.

### Batch materialized views recompute in full, every time

Two consecutive runs of an unchanged pipeline against unchanged source data. Run 1 completed in 19.728 seconds and wrote one Parquet part file. Run 2 completed in 19.026 seconds, deleted that part file, and wrote a new one with a fresh UUID and an mtime 26 seconds later. Same data, same plan, complete rewrite.

`TriggeredGraphExecution` issues a full refresh unconditionally. No state comparison, no source change detection, no incremental path in the open build.

**A terminology warning, because this is where readers will push back.** The Spark 4.2.0 programming guide describes a run with no refresh flags as performing a default incremental update. That phrasing is inherited from the Databricks update model, where "incremental update" names the update *mode*, the opposite of `--full-refresh`, which additionally clears streaming checkpoints and reprocesses sources from the beginning. It does not mean the materialized view is incrementally refreshed. For streaming tables, default mode is genuinely incremental and appends only new records. For batch materialized views on the open build, default mode still rewrites the table completely.

The distinction matters commercially. A reader who sees "default incremental update" in the documentation and plans compute budget around it will be wrong by the ratio of total table size to daily change volume.

### Streaming tables behave correctly and incrementally

The object storage pipeline read four JSON files from an OCI bucket over the S3 compatibility API across two runs. Run 1 committed batch 0 with `file1.json` and `file2.json`. Two new files landed. Run 2 committed batch 1 with `file3.json` and `file4.json` only; the first two are absent from the batch 1 source log entirely. Eight rows across two part files, zero duplication.

Recovery held under a hard kill. `SIGKILL` mid-cycle, restart, resumed from the committed offset rather than reprocessing. Underneath the declarative surface it is Structured Streaming, and it behaves like it.

The incremental story in open SDP is real, and it lives entirely on the ingestion side.

### There is no continuous execution mode

`Trigger.AvailableNow()` is hardcoded in `TriggeredGraphExecution`, and that class is the sole concrete subclass of `GraphExecution` on the 4.2.0 classpath. No `ContinuousGraphExecution` exists. The CLI accepts `--spec`, `--full-refresh`, `--full-refresh-all`, and `--refresh`; `--continuous` and `--mode continuous` both fail with an unrecognized-argument error and exit code 2. The pipeline spec YAML has no execution mode field.

Databricks lists continuous mode as a Lakeflow-only capability, which corroborates the bytecode independently.

Each invocation processes all available data in a single batch and exits. For a team expecting a long-running streaming service, this is the architectural surprise: SDP gives you streaming semantics with batch execution. Latency is a function of how often your external scheduler fires it.

### The default configuration is not idempotent

Run a pipeline twice with default settings and the second run fails with `LOCATION_ALREADY_EXISTS`. The standalone default session catalog is in-memory and starts empty each invocation, so the table definition is gone while the warehouse directory on disk is not.

The obvious fix, setting `spark.sql.catalogImplementation: hive` in the pipeline spec, is rejected with `CANNOT_MODIFY_STATIC_CONFIG`, SQLSTATE `46110`. Static configurations cannot be set from the pipeline YAML. The working fix is `spark-defaults.conf` on the cluster.

None of this is an engine defect and none of it appears on Databricks, where Unity Catalog is a given. It matters because it is the exact shape of the gap between a quickstart that works and a pipeline that runs twice, and any team evaluating open SDP will hit it in the first hour.

Two smaller constraints, worth knowing before you design:

A materialized view cannot be defined by a flow that reads a streaming relation. The error is `INVALID_FLOW_QUERY_TYPE.STREAMING_RELATION_FOR_MATERIALIZED_VIEW`, SQLSTATE `42000`. The only supported crossing from streaming to batch is through a physical table: a streaming table writes, a materialized view reads it back with `spark.table()`. Temporary views do not bridge the gap. Every stream-to-batch handoff therefore costs you a materialized table, with the storage and latency that implies.

And the `storage:` directory declared in the spec is never created for a pipeline containing only batch materialized views. It exists for streaming checkpoints and nothing else.

---

## The Databricks comparison is narrower than it looks

The obvious conclusion from the recompute finding is that Lakeflow solves it. Check the compute tier before you assume that.

Databricks documents incremental refresh as available only on serverless pipelines. Materialized views that do not run on serverless are always fully recomputed. On serverless, the Enzyme engine detects source changes and refreshes incrementally where the query supports it; where the query uses unsupported expressions, the platform falls back to a full recompute. The runtime also runs a cost analysis and picks whichever of the two is cheaper, which you can override with a refresh policy.

Three consequences for anyone building a business case:

Incremental refresh on classic compute does not exist. If your pipelines run on job clusters today, moving to Lakeflow gets you AUTO CDC, expectations, and the event log, and does nothing at all for recompute cost until you also move to serverless.

Incremental refresh is query-dependent even on serverless. The supported SQL surface is a published list, and a query outside it silently costs you a full recompute. That belongs in your evaluation as a test against your actual gold-layer SQL, not as an assumption.

The gap between open SDP and Lakeflow on classic compute is smaller than the marketing implies, and the gap on serverless is real but comes attached to serverless economics and a Unity Catalog dependency.

---

## Apache SDP against the alternatives

| | Apache SDP 4.2.0 (measured) | Lakeflow, classic compute (vendor-documented) | Lakeflow, serverless (vendor-documented) | Airflow + dbt |
|---|---|---|---|---|
| Dependency resolution | In-engine | In-engine | In-engine | External, hand-authored |
| Execution model | Single triggered batch, `Trigger.AvailableNow()` hardcoded | Triggered or continuous | Triggered or continuous | Scheduled, external |
| Batch view refresh | Full recompute every run | Always full recompute | Incremental where query supports it, cost-model selected | Incremental materializations |
| Streaming ingestion | Incremental, offset-accurate | Incremental | Incremental | Not native |
| CDC and SCD 1/2 | Not available | AUTO CDC | AUTO CDC | dbt snapshots |
| Data quality | Not available | Expectations | Expectations | dbt tests |
| Event log / lineage | Not available | Queryable event log | Queryable event log | Airflow plus dbt docs |
| Scheduler | Bring your own | Included | Included | Airflow |
| Catalog requirement | Configure persistence yourself | Unity Catalog | Unity Catalog | Warehouse-native |
| Cost model | Compute only | Per-DBU plus platform | Serverless per-DBU | Compute plus orchestration infrastructure |
| Lock-in exposure | Low | High | High | Low |

The column that surprises people is the third one from the left. Lakeflow on classic compute shares the open version's recompute behavior.

---

## What I would tell three different teams

**Already on Databricks, on classic compute.** Lakeflow SDP is worth adopting for AUTO CDC and expectations, both of which you are hand-rolling today. Do not build the business case on refresh cost, because incremental refresh will not apply to you until you move to serverless. Price that migration separately.

**Running Airflow and dbt at scale.** Stay. dbt already gives you incremental materializations, tests, and lineage; open SDP gives you none of the three and takes back full recomputes on your gold layer. The orchestration code SDP deletes is not worth rebuilding those. Revisit when incremental processing lands upstream, which Databricks has signaled is on the roadmap without committing to a release.

**Greenfield, streaming-heavy ingestion.** This is where open SDP earns its place today. The streaming side is solid, recovery works, and dependency resolution genuinely removes wiring code. Keep aggregations thin, expect to schedule externally, and design the stream-to-batch boundary around materialized physical tables from day one.

---

## Pilot shape

Two engineers, six weeks, one ingestion path. [ASSUMPTION: sizing is from comparable pipeline evaluations, not from this lab.]

Weeks one and two: one real source landing into streaming tables, external scheduler wired, catalog persistence configured properly. Weeks three and four: the aggregation layer, with recompute cost measured against your actual volumes rather than estimated. Weeks five and six: failure drills, including a hard kill mid-run and a backfill.

Expand if the full recompute cost stays inside budget and external scheduling does not reintroduce the coordination logic SDP was supposed to remove. Stop if either fails. Both are measurable inside six weeks, which is the reason to run a pilot instead of an opinion.

---

## Appendix: method and limits

**Environment.** Apache Spark 4.2.0, PySpark from pip, OpenJDK 17.0.20, Python 3.10, Ubuntu 22.04.5, single node. OCI `VM.Standard.E5.Flex`, AMD EPYC 9J14, x86_64. The lab was designed for `VM.Standard.A1.Flex` on Ampere; A1 capacity was exhausted across all availability domains in `us-chicago-1`, which forced the pivot to x86 and off the Always Free tier. Plan for that if you reproduce this.

**Object storage.** OCI Object Storage through the S3 compatibility API with the `s3a` connector. Required jars: `hadoop-aws-3.5.0.jar`, `bundle-2.35.4.jar` (AWS SDK v2), and `analyticsaccelerator-s3-1.3.1.jar`. They must sit in PySpark's `site-packages/pyspark/jars/` directory, not `$SPARK_HOME/jars/`, because a pip-installed PySpark resolves its classpath from site-packages. That cost more time than any other setup step.

**Verification.** The no-continuous-mode finding was checked three independent ways (CLI argument surface, bytecode inspection of the shipped jar, and the programming guide), plus a falsification attempt against the CLI, and it agrees with Databricks' published capability comparison. The full-recompute finding rests on part-file UUIDs, mtimes, and run timings across two runs.

**Not tested, and therefore not claimed.** Delta or Iceberg as the sink; behavior at meaningful data volume; multi-node clusters; Spark Connect execution mode; anything about Lakeflow beyond published documentation. The full-recompute measurement was taken against a plain Parquet warehouse under a Hive catalog. Whether a table-format layer changes it is open, and it is the first thing I would test next, because it is what enterprise readers are running.

**Reproducibility.** Every version pinned and recorded, every state-changing command logged, every finding traced to a log line. Where a finding was inference rather than observation, it is labeled. One earlier finding was contradicted by later evidence and the correction is recorded rather than edited away.

**Sources.** Apache Spark 4.2.0 Declarative Pipelines programming guide. Databricks documentation on pipeline refresh semantics, incremental refresh for materialized views, and the SDP versus Lakeflow capability comparison. Databricks engineering blog on declarative pipelines. SPARK-51727.
