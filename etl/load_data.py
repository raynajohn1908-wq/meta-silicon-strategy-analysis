"""
ETL: builds data/meta_silicon_strategy.db from sql/schema.sql and loads it
with ONLY the publicly disclosed figures documented in docs/DATA_SOURCES.md.

No synthetic, estimated, or interpolated numbers are inserted here. Every
row carries a `source` column. Where Meta has not disclosed a figure, the
corresponding column is left NULL rather than filled with a guess.
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "meta_silicon_strategy.db"
SCHEMA_PATH = ROOT / "sql" / "schema.sql"

# ---------------------------------------------------------------------------
# Source citations (reused across rows to keep citation text consistent)
# ---------------------------------------------------------------------------
SRC_Q2_2026_EARNINGS = "Meta Q2 2026 earnings call / report, Aug 3 2026 (via CNBC, GuruFocus coverage)"
SRC_CAPEX_GUIDANCE = "Meta Q1 2026 earnings call (capex guidance raised, Apr 2026); ceiling confirmed Meta Q2 2026 report, Aug 3 2026 (CNBC)"
SRC_LAYOFFS = "Meta workforce reduction announcement, Apr 2026 (CNBC)"
SRC_MTIA_BLOG_MAR = "Meta Engineering blog, about.fb.com, Mar 11 2026"
SRC_MTIA_BLOG_APR = "Meta Engineering blog, about.fb.com, Apr 14 2026"
SRC_CNBC_MAR11 = "CNBC, Mar 11 2026 (Meta VP of Engineering, on the record)"
SRC_TOMSHARDWARE_MAR = "Tom's Hardware, Mar 2026"
SRC_AMD_DEAL = "Meta long-term AI infrastructure agreement with AMD, ~late Feb 2026 (reported ahead of Mar 11 2026 MTIA announcement)"
SRC_DELOITTE_TECHBREW = "Deloitte estimate, cited by TechBrew, Mar 2026"

DDL = SCHEMA_PATH.read_text(encoding="utf-8")


def load(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # -- quarterly_financials ------------------------------------------------
    cur.execute(
        """
        INSERT INTO quarterly_financials (
            quarter, revenue_billion, revenue_yoy_pct, prior_year_revenue_billion,
            total_costs_yoy_pct, rd_expenses_yoy_pct,
            operating_profit_billion, operating_profit_yoy_pct,
            net_income_billion, net_income_yoy_pct, prior_year_net_income_billion,
            free_cash_flow_yoy_pct, prior_year_fcf_billion,
            report_date, source
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "Q2 2026",
            60.8, 28.0, 47.52,
            55.0, 68.0,
            18.8, -8.0,
            15.85, -14.0, 18.34,
            -91.0, 8.5,
            "2026-08-03", SRC_Q2_2026_EARNINGS,
        ),
    )

    # -- annual_guidance ------------------------------------------------------
    cur.executemany(
        """
        INSERT INTO annual_guidance (fiscal_year, metric, low_billion, high_billion, guidance_date, note, source)
        VALUES (?,?,?,?,?,?,?)
        """,
        [
            (2026, "capex", 125.0, 145.0, "2026-04-01",
             "Range raised in April 2026; ceiling of $145B confirmed on the Aug 3 2026 Q2 report", SRC_CAPEX_GUIDANCE),
            (2026, "total_expenses", 162.0, 169.0, "2026-04-01",
             "Full-year 2026 total expenses guidance", SRC_CAPEX_GUIDANCE),
        ],
    )

    # -- workforce_events -------------------------------------------------------
    cur.execute(
        """
        INSERT INTO workforce_events (event_date, jobs_cut, open_roles_removed, pct_of_workforce, stated_reason, source)
        VALUES (?,?,?,?,?,?)
        """,
        (
            "2026-04-01", 8000, 6000, 10.0,
            "Efficiency push \"to offset the other investments we're making\" (i.e., to offset AI capex)",
            SRC_LAYOFFS,
        ),
    )

    # -- mtia_chip_generations --------------------------------------------------
    cur.executemany(
        """
        INSERT INTO mtia_chip_generations (chip_name, workload_type, production_status, announced_date, notes, source)
        VALUES (?,?,?,?,?,?)
        """,
        [
            ("MTIA 300", "training (ranking/recommendation)", "in production", "2026-03-11",
             "Already in production; used for ranking/recommendation model training, not frontier LLMs",
             SRC_MTIA_BLOG_MAR),
            ("MTIA 400", "inference (GenAI)", "announced", "2026-03-11",
             "Inference-focused, primarily GenAI workloads (image/video generation from prompts); one datacenter rack holds 72 MTIA 400 chips",
             SRC_MTIA_BLOG_MAR),
            ("MTIA 450", "inference (GenAI)", "announced", "2026-03-11",
             "Inference-focused, primarily GenAI workloads", SRC_MTIA_BLOG_MAR),
            ("MTIA 500", "inference (GenAI)", "announced", "2026-03-11",
             "Inference-focused, primarily GenAI workloads", SRC_MTIA_BLOG_MAR),
        ],
    )

    # -- silicon_strategy_events (interleaved capex + silicon narrative) -------
    cur.executemany(
        """
        INSERT INTO silicon_strategy_events (event_date, event_date_sort, category, event, what_it_means, source)
        VALUES (?,?,?,?,?,?)
        """,
        [
            (
                "2023 (exact date not disclosed)", "2023-01-01", "silicon_strategy",
                "MTIA (Meta Training and Inference Accelerator) first introduced as Meta's homegrown AI chip family",
                "Meta begins building an alternative to buying 100% of its AI compute from Nvidia/AMD, starting with internal ranking/recommendation workloads.",
                SRC_MTIA_BLOG_MAR,
            ),
            (
                "April 2026", "2026-04-01", "capex_pressure",
                "2026 full-year capex guidance raised to $125B-$145B; Meta cuts 8,000 jobs (~10% of workforce) and removes 6,000 open roles",
                "Meta is simultaneously increasing AI infrastructure spend and cutting headcount elsewhere in the business, explicitly to 'offset the other investments we're making' — the labor cuts are a direct funding offset for the capex ramp, not a sign of broader retrenchment.",
                SRC_CAPEX_GUIDANCE + "; " + SRC_LAYOFFS,
            ),
            (
                "~2 weeks before Mar 11 2026 (exact date not disclosed)", "2026-02-25", "silicon_strategy",
                "Meta signs a long-term AI infrastructure agreement with AMD for additional GPU capacity",
                "Roughly two weeks before announcing its custom-silicon acceleration, Meta locks in more third-party GPU supply — evidence this is additive ('portfolio approach'), not a pivot away from GPUs.",
                SRC_AMD_DEAL + " — exact date not disclosed; timing stated only as '~2 weeks before' the Mar 11 2026 MTIA announcement",
            ),
            (
                "March 11, 2026", "2026-03-11", "silicon_strategy",
                "Meta announces acceleration to four MTIA chip generations (300/400/450/500) in two years",
                "A much faster public cadence than typical multi-year chip cycles; Meta's own stated rationale is supply diversity and price insulation versus sole reliance on Nvidia/AMD, optimized for high-volume, predictable inference TCO — not a claim that this reduces total capex.",
                SRC_MTIA_BLOG_MAR + "; " + SRC_CNBC_MAR11,
            ),
            (
                "April 14, 2026", "2026-04-14", "silicon_strategy",
                "Meta expands its silicon partnership with Broadcom to co-develop future MTIA generations (multi-generation agreement)",
                "Meta locks in a chip-design partner for multiple future MTIA generations, signaling this is a durable multi-year program rather than a one-off chip project.",
                SRC_MTIA_BLOG_APR,
            ),
            (
                "August 3, 2026", "2026-08-03", "capex_pressure",
                "Q2 2026 results: revenue +28% YoY to $60.8B, but free cash flow down ~91% YoY and net income down 14% YoY; $145B capex ceiling confirmed",
                "The capex-vs-cash-flow tension that motivated the April efficiency push has not eased by the next quarter's report — the pressure the silicon strategy is meant to address is still visibly present in the same period MTIA is scaling up.",
                SRC_Q2_2026_EARNINGS,
            ),
        ],
    )

    conn.commit()


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(DDL)
        load(conn)

        # Sanity check: every fact table row must have a non-empty source.
        for table in (
            "quarterly_financials", "annual_guidance", "workforce_events",
            "mtia_chip_generations", "silicon_strategy_events",
        ):
            n_missing = conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE source IS NULL OR TRIM(source) = ''"
            ).fetchone()[0]
            if n_missing:
                raise RuntimeError(f"{table} has {n_missing} row(s) missing a source citation")

        counts = {
            table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in (
                "quarterly_financials", "annual_guidance", "workforce_events",
                "mtia_chip_generations", "silicon_strategy_events",
            )
        }
        print(f"Loaded {DB_PATH}")
        for table, n in counts.items():
            print(f"  {table}: {n} rows")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
