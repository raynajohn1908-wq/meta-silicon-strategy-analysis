-- Derived analysis views. Every value here is computed directly from rows
-- in the base tables (which are themselves 100% sourced, real, disclosed
-- figures) using simple arithmetic — division, subtraction, ordering. No
-- view invents, estimates, or interpolates a number that Meta has not
-- disclosed. Where a computation would require an undisclosed input (e.g.
-- full-year 2026 revenue, or a training/inference spend split), the view
-- either omits it or labels the result explicitly as an order-of-magnitude
-- framing rather than a precise figure.

-- ---------------------------------------------------------------------------
-- v_capex_pct_revenue
--
-- IMPORTANT LIMITATION (named explicitly, not glossed over): Meta reports
-- capex guidance as a FULL-YEAR 2026 figure, but as of this analysis only
-- Q2 2026 quarterly revenue has been disclosed (2026 is still in progress;
-- Q3/Q4 have not been reported). There is no disclosed full-year 2026
-- revenue actual to divide the full-year capex guidance by. Rather than
-- inventing an annualized revenue estimate (which the source data forbids),
-- this view expresses capex guidance as a multiple of the one disclosed
-- quarterly revenue figure, clearly labeled as such. Treat this as a scale
-- check, not a true annual capex/revenue ratio.
-- ---------------------------------------------------------------------------
CREATE VIEW v_capex_pct_revenue AS
SELECT
    qf.quarter                                                       AS revenue_period,
    qf.revenue_billion                                                AS quarterly_revenue_billion,
    ag.fiscal_year                                                    AS guidance_fiscal_year,
    ag.low_billion                                                    AS fy_capex_guidance_low_billion,
    ag.high_billion                                                   AS fy_capex_guidance_high_billion,
    ROUND(ag.low_billion  / qf.revenue_billion, 2)                    AS capex_low_as_multiple_of_quarterly_revenue,
    ROUND(ag.high_billion / qf.revenue_billion, 2)                    AS capex_high_as_multiple_of_quarterly_revenue,
    'Full-year 2026 revenue not yet disclosed (2026 in progress); capex guidance is a FY figure compared here against a single quarter''s revenue, not annual revenue. Not a true annual capex/revenue ratio.' AS caveat,
    qf.source                                                          AS revenue_source,
    ag.source                                                          AS capex_guidance_source
FROM annual_guidance ag
JOIN quarterly_financials qf ON qf.quarter = 'Q2 2026'
WHERE ag.metric = 'capex';

-- ---------------------------------------------------------------------------
-- v_strategy_timeline
--
-- Interleaves capex-pressure events and silicon-strategy events in
-- chronological order (via event_date_sort) so the sequence reads as one
-- narrative: guidance raised -> layoffs -> AMD deal -> MTIA acceleration ->
-- Broadcom expansion -> Q2 results confirming the pressure hasn't eased.
-- ---------------------------------------------------------------------------
CREATE VIEW v_strategy_timeline AS
SELECT
    event_date_sort,
    event_date          AS event_date_display,
    category,
    event,
    what_it_means,
    source
FROM silicon_strategy_events
ORDER BY event_date_sort;

-- ---------------------------------------------------------------------------
-- v_addressable_share
--
-- Order-of-magnitude framing only — NOT a precise estimate. Deloitte
-- (cited by TechBrew, Mar 2026) puts inference at roughly two-thirds of AI
-- compute in 2026. MTIA's disclosed scope is inference-only (MTIA 400/450/
-- 500); training stays on GPUs, including MTIA 300's ranking/recommendation
-- training which is not a frontier-LLM workload. So at most ~2/3 of AI
-- compute is even theoretically addressable by Meta's custom silicon
-- program today — the other ~1/3 (frontier-LLM training) is out of scope
-- for MTIA regardless of how well the chips perform. Meta has NOT disclosed
-- its own training/inference compute split, or a dollar spend split by
-- silicon type, so this cannot be converted into a capex dollar figure.
-- ---------------------------------------------------------------------------
CREATE VIEW v_addressable_share AS
SELECT
    'Order-of-magnitude framing, not a precise estimate' AS framing_type,
    'Inference ~ two-thirds of AI compute in 2026'         AS cited_industry_estimate,
    'Deloitte estimate, cited by TechBrew, Mar 2026'        AS estimate_source,
    'MTIA 400/450/500 target inference (GenAI) workloads only; frontier LLM training remains GPU-bound' AS mtia_scope,
    'Meta Engineering blog, about.fb.com, Mar 11 2026'      AS mtia_scope_source,
    'At most ~2/3 of AI compute is theoretically addressable by custom silicon today; the remaining ~1/3 (frontier-LLM training) is out of MTIA''s disclosed scope regardless of chip performance' AS conclusion,
    'Meta has not disclosed its own training/inference compute split or a capex dollar split by silicon type -- this framing cannot be converted into a dollar figure' AS disclosure_gap;
