# Meta Custom Silicon Strategy Analysis

**Public-data analysis of Meta's custom silicon strategy, AI infrastructure economics, and heterogeneous compute portfolio.**

**Python · SQL · SQLite · Chart.js · Product & Strategy Analysis**

> **Key finding:** Meta's disclosures support MTIA as a workload-optimized, cost-efficient part of a broader silicon portfolio, but public data still does not provide the cost-per-inference, software-portability, or silicon-spend detail needed to quantify the full value of MTIA across the infrastructure stack.

[View the dashboard](exports/dashboard.html) · [Read the strategy memo](docs/RECOMMENDATION_MEMO.md)

## The product question

Meta is not choosing between custom silicon and external accelerators. It is operating a heterogeneous compute portfolio across MTIA, NVIDIA, and AMD while using software layers such as PyTorch, compilers, runtimes, and serving systems to make workloads portable across hardware.

This case study asks:

**How should Meta decide which workloads run on which accelerators, and what evidence would show that its heterogeneous compute portfolio is improving infrastructure economics, flexibility, and developer velocity?**

The answer from public data is deliberately limited: **we can identify the strategic logic and the product metrics that matter, but we cannot calculate the full ROI of MTIA from outside the company.** Meta has not disclosed a comparable cost-per-query/TCO series by accelerator, a silicon-spend split, or enough public data to quantify the engineering cost of portability across hardware.

## Product decision framework

A useful infrastructure-product decision is broader than asking whether total capex falls. The decision should consider:

| Decision dimension | Product question |
|---|---|
| **Workload fit** | Which accelerator best matches the model architecture, latency target, batch profile, and training/inference workload? |
| **Performance / dollar** | How much useful throughput does each hardware path deliver per unit of cost? |
| **Performance / watt** | Which option uses constrained power and data-center capacity most efficiently? |
| **Software portability** | How much work is required to move a workload across MTIA, NVIDIA, and AMD? |
| **Developer velocity** | Does the software stack reduce hardware-specific friction for model teams? |
| **Reliability & maturity** | Is the accelerator and software path production-ready at Meta scale? |
| **Capacity & supply** | Does the portfolio reduce dependence on a single vendor or constrained supply source? |
| **Total cost of ownership** | What is the end-to-end cost to deploy, operate, and support the workload? |

### Why software portability matters

A heterogeneous hardware strategy only creates product value if workloads can move across accelerators without excessive engineering friction. That makes the software layer—PyTorch, compiler/runtime infrastructure, serving systems, and kernel optimization—a strategic part of the compute portfolio rather than a separate implementation detail.

The product question is therefore not simply **“Is MTIA cheaper?”** It is:

**“Can Meta route each workload to the best hardware while preserving developer velocity, reliability, and performance at scale?”**

## Architecture

```text
Public company + engineering disclosures
                    ↓
               Python ETL
                    ↓
            SQLite warehouse
                    ↓
            SQL analytical views
                    ↓
            Product interpretation
                    ↓
     Dashboard + strategy recommendation
```

## What's in this repo

| Path | Purpose |
|---|---|
| `sql/schema.sql` | Five-table SQLite schema; every fact row requires a source |
| `etl/load_data.py` | Loads cited public figures into `data/meta_silicon_strategy.db` |
| `sql/views.sql` | Capex scale check, chronological strategy timeline, and workload-scope analysis |
| `etl/derived_analysis.py` | Runs analytical views and exports `data/derived_analysis.json` |
| `docs/RECOMMENDATION_MEMO.md` | Product/strategy memo: evidence, limitations, decision framework, and metrics to watch |
| `exports/dashboard.html` | Interactive Chart.js dashboard for financial context, MTIA roadmap, and product decision criteria |

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

Meta's public disclosures support a **portfolio approach** rather than a full replacement path for external accelerators. Custom silicon can improve workload-level economics and supplier flexibility while external accelerators continue to provide scale, ecosystem depth, and capacity.

That means a decline in total capex is **not required** for MTIA to be successful. A better product test is whether Meta can absorb rapidly growing AI demand with better unit economics, power efficiency, portability, and operational flexibility.

## What remains undisclosed

The central ROI question cannot be solved from public disclosures because Meta has not published:

- a comparable MTIA-vs-external-accelerator cost-per-query or TCO time series;
- a GPU/external-accelerator vs. MTIA capex split;
- public metrics for developer effort or migration friction across hardware;
- enough detail to isolate MTIA efficiency gains from rapidly growing AI demand and data-center expansion.

Those are not flaws to estimate around—they are the decision-relevant missing variables.

## Why this project exists

The goal is not to prove a predetermined thesis. It is to demonstrate an end-to-end product analytics workflow: source real business data, model it, identify the actual decision, define success metrics, communicate what the evidence supports, and state clearly where the data stops supporting a conclusion.

**Data current through Meta's Q2 2026 results released July 29, 2026.**