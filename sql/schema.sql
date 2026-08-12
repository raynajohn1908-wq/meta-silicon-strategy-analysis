-- Meta Silicon Strategy Analysis — data warehouse schema
-- Every fact table carries a `source` column: no row may be inserted without
-- a citation. This schema holds ONLY publicly disclosed figures — there is
-- no modeled or interpolated data at the table level. Derived calculations
-- happen in sql/views.sql, never here.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS v_capex_pct_revenue;
DROP VIEW IF EXISTS v_strategy_timeline;
DROP VIEW IF EXISTS v_addressable_share;
DROP TABLE IF EXISTS quarterly_financials;
DROP TABLE IF EXISTS annual_guidance;
DROP TABLE IF EXISTS workforce_events;
DROP TABLE IF EXISTS mtia_chip_generations;
DROP TABLE IF EXISTS silicon_strategy_events;

-- ---------------------------------------------------------------------------
-- Quarterly financial results, as reported on Meta earnings calls.
-- Only figures explicitly stated in source material are populated; a NULL
-- means Meta did not disclose an absolute value for that field (e.g. Meta
-- gave FCF as a % YoY change, not an absolute Q2 2026 dollar figure).
-- ---------------------------------------------------------------------------
CREATE TABLE quarterly_financials (
    quarter                     TEXT PRIMARY KEY,   -- e.g. 'Q2 2026'
    revenue_billion              REAL,               -- USD billions
    revenue_yoy_pct              REAL,               -- % change YoY
    prior_year_revenue_billion   REAL,               -- USD billions, prior-year comparator as stated
    total_costs_yoy_pct          REAL,               -- % change YoY
    rd_expenses_yoy_pct          REAL,               -- % change YoY
    operating_profit_billion     REAL,               -- USD billions
    operating_profit_yoy_pct     REAL,               -- % change YoY
    net_income_billion           REAL,               -- USD billions
    net_income_yoy_pct           REAL,               -- % change YoY
    prior_year_net_income_billion REAL,              -- USD billions, prior-year comparator as stated
    free_cash_flow_yoy_pct       REAL,               -- % change YoY
    prior_year_fcf_billion       REAL,               -- USD billions, prior-year comparator as stated
    report_date                  TEXT,               -- date the figures were reported
    source                       TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- Forward-looking guidance ranges given on earnings calls (not actuals).
-- ---------------------------------------------------------------------------
CREATE TABLE annual_guidance (
    id                            INTEGER PRIMARY KEY AUTOINCREMENT,
    fiscal_year                   INTEGER NOT NULL,
    metric                        TEXT NOT NULL,      -- 'capex' | 'total_expenses'
    low_billion                   REAL NOT NULL,
    high_billion                  REAL NOT NULL,
    guidance_date                 TEXT NOT NULL,       -- date this guidance was given/confirmed
    note                          TEXT,                -- e.g. 'ceiling confirmed on Q2 2026 report'
    source                        TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- Workforce actions tied to the cost-efficiency push.
-- ---------------------------------------------------------------------------
CREATE TABLE workforce_events (
    id                            INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date                    TEXT NOT NULL,
    jobs_cut                      INTEGER,
    open_roles_removed            INTEGER,
    pct_of_workforce               REAL,
    stated_reason                 TEXT,
    source                        TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- MTIA chip generation roadmap.
-- ---------------------------------------------------------------------------
CREATE TABLE mtia_chip_generations (
    chip_name                     TEXT PRIMARY KEY,   -- 'MTIA 300', 'MTIA 400', ...
    workload_type                 TEXT NOT NULL,       -- 'training (ranking/recommendation)' | 'inference (GenAI)'
    production_status             TEXT NOT NULL,       -- 'in production' | 'announced'
    announced_date                TEXT,
    notes                         TEXT,
    source                        TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- Timeline of silicon-strategy and capex-pressure events, interleaved, so
-- the sequence reads as one narrative rather than two separate stories.
-- ---------------------------------------------------------------------------
CREATE TABLE silicon_strategy_events (
    id                             INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date                     TEXT NOT NULL,       -- display text; may be approximate/partial where disclosed as such
    event_date_sort                TEXT NOT NULL,        -- ISO yyyy-mm-dd sort key only (uses earliest plausible day for partial dates); not itself a disclosed fact
    category                       TEXT NOT NULL,       -- 'capex_pressure' | 'silicon_strategy'
    event                          TEXT NOT NULL,
    what_it_means                  TEXT NOT NULL,       -- plain-language strategic interpretation
    source                         TEXT NOT NULL
);
