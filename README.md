# Meta Custom Silicon Strategy Analysis

**Public-data strategy analysis of whether Meta's MTIA custom silicon can materially improve AI infrastructure economics while the company continues scaling third-party accelerators.**

**Python · SQL · SQLite · Chart.js · Financial & Strategy Analysis**

> **Key finding:** Meta's disclosures support MTIA as a workload-optimized, cost-efficient part of a broader silicon portfolio, but public data still does not provide the cost-per-inference or GPU-vs-custom-silicon spending detail needed to quantify how much MTIA reduces total infrastructure cost.

[View the dashboard](exports/dashboard.html) · [Read the strategy memo](docs/RECOMMENDATION_MEMO.md)

## The question

Meta is simultaneously accelerating its custom-silicon roadmap and expanding external compute capacity. At the same time, its 2026 capital-expenditure guidance remains exceptionally large.

This case study asks:

**Is MTIA beginning to relieve Meta's AI infrastructure cost pressure, or is it primarily improving workload efficiency and supplier diversification while total infrastructure investment continues to rise?**

The answer from public data is deliberately limited: **we can identify the strategic logic and the metrics that matter, but we cannot yet calculate MTIA's net savings.** Meta has not disclosed a comparable cost-per-query/TCO series for MTIA versus external accelerators or a capex split by silicon type.

## Architecture

```text
Public company disclosures + Meta engineering disclosures
                         ↓
                    Python ETL
                         ↓
                 SQLite warehouse
                         ↓
                 SQL analytical views
                         ↓
                 Derived analysis
                         ↓
        Interactive dashboard + strategy memo
```

## What's in this repo

| Path | Purpose |
|---|---|
| `sql/schema.sql` | Five-table SQLite schema; every fact row requires a source |
| `etl/load_data.py` | Loads cited public figures into `data/meta_silicon_strategy.db` |
| `sql/views.sql` | Capex scale check, chronological strategy timeline, and workload-scope framing |
| `etl/derived_analysis.py` | Runs analytical views and exports `data/derived_analysis.json` |
| `docs/RECOMMENDATION_MEMO.md` | Strategy memo: evidence, limitations, interpretation, and decision-relevant metrics |
| `exports/dashboard.html` | Interactive Chart.js dashboard for the financial tension, silicon timeline, and MTIA roadmap |

## Reproduce the analysis

```bash
python etl/load_data.py
python etl/derived_analysis.py
```

Then open `exports/dashboard.html` in a browser. Chart.js is loaded from a CDN; no build step is required.

## Current public-data snapshot

| Figure | Value | Primary source |
|---|---|---|
| FY2026 capex guidance | **$130B–$145B**, narrowed from $125B–$145B | Meta Q2 2026 results, July 29, 2026 |
| FY2026 total-expense guidance | **$165B–$169B** | Meta Q2 2026 results, July 29, 2026 |
| Q2 2026 revenue | **$60.801B**, +28% YoY | Meta Q2 2026 results |
| Q2 2026 costs & expenses | **$42.026B**, +55% YoY | Meta Q2 2026 results |
| Q2 2026 R&D expense | **$21.656B**, +67% YoY | Meta Q2 2026 results |
| Q2 2026 operating income | **$18.775B**, −8% YoY | Meta Q2 2026 results |
| Q2 2026 net income | **$15.848B**, −14% YoY | Meta Q2 2026 results |
| Q2 2026 free cash flow | **$0.784B**, down ~91% from $8.505B | Meta Q2 2026 results |
| Q2 2026 capex | **$31.08B** | Meta Q2 2026 results |
| May 2026 headcount reduction | Approximately **8,000 employees impacted** | Meta Q2 2026 results |
| MTIA roadmap | Four new generations within two years | Meta, March 11, 2026 |
| MTIA 300 | In production; ranking/recommendation training | Meta, March 11, 2026 |
| MTIA 400/450/500 | Capable of all workloads; primarily targeted at GenAI inference in the near term | Meta, March 11, 2026 |
| MTIA deployment | Hundreds of thousands of chips used for inference | Meta, March 11, 2026 |
| Broadcom partnership | Multi-generation MTIA co-development agreement | Meta, April 14, 2026 |

## What the evidence supports

Meta explicitly describes MTIA as part of a **portfolio approach** to AI infrastructure rather than a full replacement for external accelerators. Its newer MTIA generations are designed around an inference-first strategy, while remaining capable of supporting additional workloads. Meta also says its custom full-stack approach improves compute and cost efficiency for intended workloads.

That supports a strong operational thesis: **custom silicon can improve workload-level economics and reduce dependence on any single external silicon supplier.** It does **not** prove that total company infrastructure spending will decline, because Meta is simultaneously adding data-center capacity and external compute.

## What remains undisclosed

The central ROI question cannot be solved from public disclosures because Meta has not published:

- a comparable MTIA-vs-external-accelerator cost-per-query or TCO time series;
- a GPU/external-accelerator vs. MTIA capex split;
- enough detail to isolate savings from MTIA from the effects of rapidly growing AI demand and data-center expansion.

Those are not flaws to estimate around—they are the decision-relevant missing variables.

## Why this project exists

The goal is not to prove a predetermined thesis. It is to demonstrate an end-to-end analytics workflow: source real business data, model it, analyze it, communicate what the evidence supports, and state clearly where the data stops supporting a conclusion.

**Data current through Meta's Q2 2026 results released July 29, 2026.**