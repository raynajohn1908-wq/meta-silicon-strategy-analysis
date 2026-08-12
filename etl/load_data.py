"""Build the sourced SQLite dataset for the Meta custom-silicon case study."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "meta_silicon_strategy.db"
SCHEMA_PATH = ROOT / "sql" / "schema.sql"

SRC_Q2 = "Meta Platforms Q2 2026 Results, July 29 2026"
SRC_MTIA = "Meta Newsroom, Expanding Meta's Custom Silicon to Power Our AI Workloads, Mar 11 2026"
SRC_AMD = "Meta Newsroom, Meta and AMD Partner for Longterm AI Infrastructure Agreement, Feb 24 2026"
SRC_BROADCOM = "Meta Newsroom, Meta Partners With Broadcom to Co-Develop Custom AI Silicon, Apr 14 2026"


def load(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO quarterly_financials (
            quarter, revenue_billion, revenue_yoy_pct, prior_year_revenue_billion,
            costs_billion, costs_yoy_pct, rd_expenses_billion, rd_expenses_yoy_pct,
            operating_income_billion, operating_income_yoy_pct,
            net_income_billion, net_income_yoy_pct, prior_year_net_income_billion,
            free_cash_flow_billion, prior_year_fcf_billion, capex_billion,
            report_date, source
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "Q2 2026", 60.801, 28.0, 47.516,
            42.026, 55.0, 21.656, 67.0,
            18.775, -8.0,
            15.848, -14.0, 18.337,
            0.784, 8.505, 31.08,
            "2026-07-29", SRC_Q2,
        ),
    )

    cur.executemany(
        """
        INSERT INTO annual_guidance
        (fiscal_year, metric, low_billion, high_billion, guidance_date, note, source)
        VALUES (?,?,?,?,?,?,?)
        """,
        [
            (2026, "capex", 130.0, 145.0, "2026-07-29",
             "Narrowed from prior outlook of $125B-$145B", SRC_Q2),
            (2026, "total_expenses", 165.0, 169.0, "2026-07-29",
             "Lower end raised to reflect Q2 legal charges", SRC_Q2),
        ],
    )

    cur.execute(
        """
        INSERT INTO workforce_events
        (event_date, employees_impacted, stated_context, source)
        VALUES (?,?,?,?)
        """,
        (
            "2026-05-01", 8000,
            "Meta's Q2 release says approximately 8,000 employees were impacted by the May 2026 headcount reduction; Q2 included $1.18B of related severance expense.",
            SRC_Q2,
        ),
    )

    cur.executemany(
        """
        INSERT INTO mtia_chip_generations
        (chip_name, near_term_use, capability, production_status, announced_date, notes, source)
        VALUES (?,?,?,?,?,?,?)
        """,
        [
            ("MTIA 300", "ranking and recommendation training", "specialized production workload", "in production", "2026-03-11",
             "Meta says MTIA 300 is already in production.", SRC_MTIA),
            ("MTIA 400", "primarily GenAI inference", "capable of all workloads", "developing/deploying", "2026-03-11",
             "Part of Meta's inference-first near-term roadmap.", SRC_MTIA),
            ("MTIA 450", "primarily GenAI inference", "capable of all workloads", "developing/deploying", "2026-03-11",
             "Part of Meta's inference-first near-term roadmap.", SRC_MTIA),
            ("MTIA 500", "primarily GenAI inference", "capable of all workloads", "developing/deploying", "2026-03-11",
             "Part of Meta's inference-first near-term roadmap into 2027.", SRC_MTIA),
        ],
    )

    cur.executemany(
        """
        INSERT INTO silicon_strategy_events
        (event_date, event_date_sort, category, event, what_it_means, source)
        VALUES (?,?,?,?,?,?)
        """,
        [
            ("2023", "2023-01-01", "silicon_strategy",
             "Meta develops the MTIA custom-silicon family",
             "Meta begins building workload-specific accelerators as part of its internal AI infrastructure stack.", SRC_MTIA),
            ("February 24, 2026", "2026-02-24", "silicon_strategy",
             "Meta announces long-term AMD AI infrastructure agreement",
             "External accelerators remain part of the scaling plan; custom silicon is complementary, not a clean replacement path.", SRC_AMD),
            ("March 11, 2026", "2026-03-11", "silicon_strategy",
             "Meta announces four new MTIA generations within two years",
             "The roadmap emphasizes rapid iteration and an inference-first deployment strategy while keeping broader workload capability.", SRC_MTIA),
            ("April 14, 2026", "2026-04-14", "silicon_strategy",
             "Meta expands Broadcom partnership across multiple MTIA generations",
             "The custom-silicon program is a sustained multi-generation infrastructure strategy.", SRC_BROADCOM),
            ("May 2026", "2026-05-01", "cost_context",
             "Approximately 8,000 employees impacted by headcount reduction",
             "Q2 later included $1.18B of related severance expense; this is cost context, not evidence that MTIA caused the reduction.", SRC_Q2),
            ("July 29, 2026", "2026-07-29", "financial_context",
             "Q2 results: $60.801B revenue, $784M FCF, $31.08B quarterly capex; FY capex guidance $130B-$145B",
             "Meta is simultaneously growing revenue and funding a very large AI infrastructure buildout, making workload-level efficiency economically important.", SRC_Q2),
        ],
    )

    conn.commit()


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        load(conn)
        for table in (
            "quarterly_financials", "annual_guidance", "workforce_events",
            "mtia_chip_generations", "silicon_strategy_events",
        ):
            missing = conn.execute(
                f"SELECT COUNT(*) FROM {table} WHERE source IS NULL OR TRIM(source) = ''"
            ).fetchone()[0]
            if missing:
                raise RuntimeError(f"{table} has {missing} row(s) without a source")
        print(f"Loaded {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
