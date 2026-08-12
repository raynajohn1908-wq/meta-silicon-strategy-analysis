-- Meta Silicon Strategy Analysis: sourced public-data schema

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS v_capex_scale_check;
DROP VIEW IF EXISTS v_strategy_timeline;
DROP VIEW IF EXISTS v_workload_scope;
DROP TABLE IF EXISTS quarterly_financials;
DROP TABLE IF EXISTS annual_guidance;
DROP TABLE IF EXISTS workforce_events;
DROP TABLE IF EXISTS mtia_chip_generations;
DROP TABLE IF EXISTS silicon_strategy_events;

CREATE TABLE quarterly_financials (
    quarter                       TEXT PRIMARY KEY,
    revenue_billion               REAL,
    revenue_yoy_pct               REAL,
    prior_year_revenue_billion    REAL,
    costs_billion                 REAL,
    costs_yoy_pct                 REAL,
    rd_expenses_billion           REAL,
    rd_expenses_yoy_pct           REAL,
    operating_income_billion      REAL,
    operating_income_yoy_pct      REAL,
    net_income_billion            REAL,
    net_income_yoy_pct            REAL,
    prior_year_net_income_billion REAL,
    free_cash_flow_billion        REAL,
    prior_year_fcf_billion        REAL,
    capex_billion                 REAL,
    report_date                   TEXT,
    source                        TEXT NOT NULL
);

CREATE TABLE annual_guidance (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    fiscal_year    INTEGER NOT NULL,
    metric         TEXT NOT NULL,
    low_billion    REAL NOT NULL,
    high_billion   REAL NOT NULL,
    guidance_date  TEXT NOT NULL,
    note           TEXT,
    source         TEXT NOT NULL
);

CREATE TABLE workforce_events (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date          TEXT NOT NULL,
    employees_impacted INTEGER,
    stated_context      TEXT,
    source              TEXT NOT NULL
);

CREATE TABLE mtia_chip_generations (
    chip_name          TEXT PRIMARY KEY,
    near_term_use      TEXT NOT NULL,
    capability         TEXT,
    production_status  TEXT NOT NULL,
    announced_date     TEXT,
    notes              TEXT,
    source             TEXT NOT NULL
);

CREATE TABLE silicon_strategy_events (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date       TEXT NOT NULL,
    event_date_sort  TEXT NOT NULL,
    category         TEXT NOT NULL,
    event            TEXT NOT NULL,
    what_it_means    TEXT NOT NULL,
    source           TEXT NOT NULL
);