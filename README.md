# Is Custom Silicon Actually Solving Meta's AI Infrastructure Cost Problem?

Meta raised its 2026 capex guidance to $125B–$145B and watched free cash flow fall ~91% year-over-year in the same quarter it confirmed that ceiling — while simultaneously accelerating its custom-silicon program (MTIA) *and* signing a new long-term GPU supply deal with AMD, rather than choosing one over the other.

This repository is a data-driven case study asking one question: **does Meta's custom-silicon strategy (MTIA) actually relieve the capex-vs-cash-flow pressure investors are watching, or is it diversifying supplier risk while total infrastructure spend keeps climbing?**

**The honest answer, from public data alone: it can't be resolved yet.** Meta has not disclosed a cost-per-query or TCO comparison between MTIA and GPU-based inference, has not broken out its 2026 capex guidance by GPU spend vs. custom-silicon spend, and has not given a timeline for whether custom silicon is meant to reduce total capex or simply change its composition. This analysis is built entirely from what Meta *has* disclosed, and names each of those gaps explicitly rather than estimating past them. The full reasoning is in [`docs/RECOMMENDATION_MEMO.md`](docs/RECOMMENDATION_MEMO.md).

## What's in this repo

| Path | What it is |
|---|---|
| `sql/schema.sql` | SQLite schema — 5 tables, every row requires a `source` column |
| `etl/load_data.py` | Loads only the real, cited figures below into `data/meta_silicon_strategy.db` |
| `sql/views.sql` | Derived views: capex-vs-revenue scale check, chronological timeline, inference "addressable share" framing |
| `etl/derived_analysis.py` | Runs the views and exports `data/derived_analysis.json` |
| `docs/RECOMMENDATION_MEMO.md` | The strategy memo — problem statement, MTIA's real scope, the open question, what to watch next, industry context |
| `exports/dashboard.html` | Single-file Chart.js dashboard: capex/FCF tension, silicon-strategy timeline, MTIA chip roadmap |

## Running it

```bash
python etl/load_data.py          # builds data/meta_silicon_strategy.db
python etl/derived_analysis.py   # applies sql/views.sql, prints + exports derived_analysis.json
```

Then open `exports/dashboard.html` directly in a browser (it loads Chart.js from a CDN; no build step, no server required).

## Data sources

Every figure used in this analysis is listed here with its source. No number in this repository is estimated, interpolated, or invented — where Meta hasn't disclosed something, that gap is stated explicitly instead.

| Figure | Value | Source |
|---|---|---|
| 2026 full-year capex guidance | $125B–$145B (ceiling confirmed Aug 3, 2026) | Meta Q1/Q2 2026 earnings calls; CNBC |
| 2026 full-year total expenses guidance | $162B–$169B | Meta Q1 2026 earnings call |
| Q2 2026 revenue | $60.8B, +28% YoY (from $47.52B) | Meta Q2 2026 earnings report, Aug 3 2026; CNBC, GuruFocus |
| Q2 2026 total costs | +55% YoY | Meta Q2 2026 earnings report |
| Q2 2026 R&D expenses | +68% YoY | Meta Q2 2026 earnings report |
| Q2 2026 operating profit | ~$18.8B, −8% YoY | Meta Q2 2026 earnings report |
| Q2 2026 net income | $15.85B, −14% YoY (from $18.34B) | Meta Q2 2026 earnings report |
| Q2 2026 free cash flow | −91% YoY (from $8.5B); absolute figure not disclosed | Meta Q2 2026 earnings report |
| April 2026 workforce reduction | 8,000 jobs cut (~10%), 6,000 open roles removed, stated to offset AI capex | CNBC, April 2026 |
| MTIA program origin | First introduced 2023 as Meta's homegrown AI chip family | Meta Engineering blog (about.fb.com), March 11 2026 |
| MTIA acceleration | 4 chip generations (300/400/450/500) in 2 years, announced March 11 2026 | Meta Engineering blog, March 11 2026; CNBC, March 11 2026 |
| MTIA 300 | In production; ranking/recommendation model training | Meta Engineering blog, March 11 2026 |
| MTIA 400/450/500 | Inference-focused, GenAI workloads; not used for frontier LLM training | Meta Engineering blog, March 11 2026; Tom's Hardware, March 2026 |
| MTIA deployment scale | "Hundreds of thousands" of chips in production inference use; 72 MTIA 400 chips per datacenter rack | Meta Engineering blog, March 11 2026 |
| Broadcom silicon partnership expansion | Multi-generation MTIA co-development agreement, announced April 14 2026 | Meta Engineering blog, April 14 2026 |
| AMD infrastructure agreement | Long-term GPU capacity deal, signed ~2 weeks before the March 11 2026 MTIA announcement (exact date not disclosed) | Reported ahead of the March 11 2026 MTIA announcement |
| Inference share of AI compute | ~2/3 of AI compute in 2026 (industry estimate, not Meta-specific) | Deloitte estimate, cited by TechBrew, March 2026 |
| Custom silicon peers | Google (TPUs since 2015), Amazon (custom chips since 2018), Microsoft (equivalent program) | Industry context, various coverage cited in the memo |

### What Meta has not disclosed (named explicitly, not estimated)

- No cost-per-query or TCO figure comparing MTIA inference to GPU-based inference.
- No breakdown of the 2026 capex guidance by GPU spend vs. MTIA/custom-silicon spend.
- No disclosed timeline for whether custom-silicon investment is expected to reduce total infrastructure capex, versus just changing its composition.

See `docs/RECOMMENDATION_MEMO.md` §3 for what internal metrics (cost-per-inference-query trend; capex split by silicon type) would be needed to close these gaps.
