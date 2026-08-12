-- Derived analytical views built only from sourced base-table values.

CREATE VIEW v_capex_scale_check AS
SELECT
    qf.quarter AS revenue_period,
    qf.revenue_billion AS quarterly_revenue_billion,
    qf.capex_billion AS quarterly_capex_billion,
    ROUND(qf.capex_billion / qf.revenue_billion, 3) AS quarterly_capex_as_share_of_revenue,
    ag.low_billion AS fy_capex_guidance_low_billion,
    ag.high_billion AS fy_capex_guidance_high_billion,
    qf.source AS quarterly_source,
    ag.source AS guidance_source
FROM quarterly_financials qf
JOIN annual_guidance ag ON ag.metric = 'capex'
WHERE qf.quarter = 'Q2 2026';

CREATE VIEW v_strategy_timeline AS
SELECT
    event_date_sort,
    event_date AS event_date_display,
    category,
    event,
    what_it_means,
    source
FROM silicon_strategy_events
ORDER BY event_date_sort;

CREATE VIEW v_workload_scope AS
SELECT
    chip_name,
    near_term_use,
    capability,
    production_status,
    notes,
    source
FROM mtia_chip_generations
ORDER BY
    CASE chip_name
        WHEN 'MTIA 300' THEN 300
        WHEN 'MTIA 400' THEN 400
        WHEN 'MTIA 450' THEN 450
        WHEN 'MTIA 500' THEN 500
        ELSE 999
    END;
