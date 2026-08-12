# Meta Custom Silicon Strategy Analysis

**Public-data analysis of Meta's custom silicon strategy, AI infrastructure economics, and heterogeneous compute portfolio.**

**Python · SQL · SQLite · Chart.js · Product & Strategy Analysis**

> **Key finding:** Meta's public disclosures support MTIA as a workload-optimized, cost-efficient component of a broader compute portfolio. Public data does not provide the accelerator-level TCO, silicon-spend mix, or quantified migration effort needed to calculate the full ROI of MTIA from outside the company.

[View the dashboard](exports/dashboard.html) · [Read the strategy memo](docs/RECOMMENDATION_MEMO.md) · [Review primary sources](docs/SOURCES.md)

## The product question

Meta is not choosing between custom silicon and external accelerators. Its public infrastructure strategy combines MTIA with large-scale NVIDIA and AMD deployments, while broader software and systems layers help make a heterogeneous hardware portfolio usable.

This case study asks:

**How should Meta decide which workloads run on which accelerators, and what evidence would show that its heterogeneous compute portfolio is improving infrastructure economics, flexibility, and developer velocity?**

The answer from public data is deliberately limited. **We can identify the strategic logic and the product metrics that matter, but we cannot calculate the full ROI of MTIA from outside the company.** Meta has not disclosed a comparable cost-per-query or TCO series by accelerator, a silicon-spend split, or quantified engineering migration cost across hardware.

## Product decision framework

A useful infrastructure-product decision is broader than asking whether total capex falls.

| Decision dimension | Product question |
|---|---|
| **Workload fit** | Which accelerator best matches the workload's training or inference profile, model requirements, latency target, and throughput needs? |
| **Performance / dollar** | How much useful throughput does each hardware path deliver per unit of cost? |
| **Performance / watt** | Which option uses constrained power and data-center capacity most efficiently? |
| **Software portability** | How much work is required to move a workload across hardware paths? |
| **Developer velocity** | Does the infrastructure reduce hardware-specific friction for model teams? |
| **Reliability & maturity** | Is the accelerator and software path production-ready at Meta scale? |
| **Capacity & supply** | Does the portfolio reduce dependence on a single vendor or constrained supply source? |
| **Total cost of ownership** | What is the end-to-end cost to deploy, operate, and support the workload? |

### Why software portability matters

A heterogeneous hardware strategy only creates product value if workloads can move across accelerators without excessive engineering friction. That makes model frameworks, compilers, runtimes, serving systems, and kernel optimization part of the infrastructure product decision rather than separate implementation details.

Meta's public disclosures support this framing. Its MTIA strategy emphasizes frictionless adoption through industry standards, its AMD partnership explicitly aligns silicon, systems, and software roadmaps, and its NVIDIA partnership includes co-design across hardware, networking, and software.

The product question is therefore not simply **"Is MTIA cheaper?"** It is:

**"Can Meta route each workload to the best hardware while preserving developer velocity, reliability, and performance at scale?"**

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
| `docs/RECOMMENDATION_MEMO.md` | Product and strategy memo with evidence, limitations, decision framework, and metrics to watch |
| `docs/SOURCES.md` | Primary-source ledger showing exactly what each Meta disclosure supports |
| `exports/dashboard.html` | Interactive Chart.js dashboard for financial context, portfolio evidence, MTIA roadmap, and product decision criteria |

## Reproduce the analysis

```bash
python etl/load_data.py
python etl/derived_analysis.py
```

Then open `exports/dashboard.html` in a browser. Chart.js is loaded from a CDN; no build step is required.

## Current public-data snapshot

| Figure | Value | Primary source |
|---|---|---|
| FY2026 capex guidance | **$130B-$145B**, narrowed from $125B-$145B | Meta Q2 2026 results, July 29, 2026 |
| FY2026 total-expense guidance | **$165B-$169B** | Meta Q2 2026 results, July 29, 2026 |
| Q2 2026 revenue | **$60.801B**, up 28% YoY | Meta Q2 2026 results |
| Q2 2026 costs & expenses | **$42.026B**, up 55% YoY | Meta Q2 2026 results |
| Q2 2026 R&D expense | **$21.656B**, up about 67% YoY | Meta Q2 2026 results |
| Q2 2026 operating income | **$18.775B**, down 8% YoY | Meta Q2 2026 results |
| Q2 2026 net income | **$15.848B**, down 14% YoY | Meta Q2 2026 results |
| Q2 2026 free cash flow | **$0.784B**, versus $8.549B in Q2 2025 | Meta Q2 2026 results |
| Q2 2026 capex | **$31.08B** | Meta Q2 2026 results |
| May 2026 headcount reduction | Approximately **8,000 employees impacted** | Meta Q2 2026 results |
| MTIA roadmap | Four new generations within two years | Meta, March 11, 2026 |
| MTIA 300 | In production; ranking and recommendation training | Meta, March 11, 2026 |
| MTIA 400/450/500 | Capable of all workloads; primarily targeted at GenAI inference in the near term | Meta, March 11, 2026 |
| MTIA deployment | Hundreds of thousands of chips used for inference | Meta, March 11, 2026 |

## Portfolio evidence

Meta's public disclosures show that the strategy is broader than MTIA alone:

- **NVIDIA, February 17, 2026:** multi-year infrastructure partnership supporting AI training and inference, with hardware, networking, and software co-design.
- **AMD, February 24, 2026:** up to 6GW of AMD Instinct GPU capacity and explicit alignment across silicon, systems, and software as part of a portfolio-based infrastructure strategy.
- **MTIA, March 11, 2026:** four new generations in two years, an inference-first focus, and frictionless adoption through industry standards.
- **Arm, March 24, 2026:** multiple generations of data-center CPUs designed to work alongside MTIA and improve performance density.
- **Broadcom, April 14, 2026:** multi-generation MTIA co-development, with Meta explicitly describing workload matching, performance, and total cost of ownership as decision criteria.

## What the evidence supports

Meta's public disclosures support a **portfolio approach** rather than a full replacement path for external accelerators. Custom silicon can improve workload-level economics and supplier flexibility while external accelerators continue to provide scale and capacity.

A decline in total capex is **not required** for MTIA to be successful. A better product test is whether Meta can absorb rapidly growing AI demand with better unit economics, power efficiency, portability, and operational flexibility.

## What remains undisclosed

The central ROI question cannot be solved from public disclosures because Meta has not published:

- a comparable MTIA versus external-accelerator cost-per-query or TCO time series;
- an external-accelerator versus MTIA capex split;
- quantified developer effort or migration friction across hardware;
- enough detail to isolate MTIA efficiency gains from rapidly growing AI demand and data-center expansion.

Those are not flaws to estimate around. They are the decision-relevant missing variables.

## Why this project exists

The goal is not to prove a predetermined thesis. It is to demonstrate an end-to-end product analytics workflow: source real business data, model it, identify the actual decision, define success metrics, communicate what the evidence supports, and state clearly where the data stops supporting a conclusion.

**Data current through Meta's Q2 2026 results released July 29, 2026.**