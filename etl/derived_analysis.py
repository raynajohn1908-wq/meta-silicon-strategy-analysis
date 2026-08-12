"""
Applies sql/views.sql to the data warehouse and prints the three derived
analyses requested for Phase 2:
  1. Capex as a multiple of the one disclosed quarter's revenue (with the
     full-year-revenue data gap named explicitly)
  2. The chronological capex-pressure + silicon-strategy timeline
  3. The inference "addressable share" order-of-magnitude framing

Every number below traces back to a row in the base tables loaded by
etl/load_data.py, which in turn traces to a cited public source. This
script performs only arithmetic already described in sql/views.sql — it
does not introduce any new figures.
"""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "meta_silicon_strategy.db"
VIEWS_PATH = ROOT / "sql" / "views.sql"
OUT_PATH = ROOT / "data" / "derived_analysis.json"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Views are re-created fresh each run so this script can be re-executed
    # after load_data.py without leaving stale view definitions behind.
    for view in ("v_capex_pct_revenue", "v_strategy_timeline", "v_addressable_share"):
        conn.execute(f"DROP VIEW IF EXISTS {view}")
    conn.executescript(VIEWS_PATH.read_text(encoding="utf-8"))

    results = {}

    print("=" * 78)
    print("1. CAPEX AS % OF REVENUE (scale check, not a true annual ratio)")
    print("=" * 78)
    rows = [dict(r) for r in conn.execute("SELECT * FROM v_capex_pct_revenue")]
    results["capex_pct_revenue"] = rows
    for r in rows:
        print(f"  FY{r['guidance_fiscal_year']} capex guidance: "
              f"${r['fy_capex_guidance_low_billion']}B-${r['fy_capex_guidance_high_billion']}B")
        print(f"  {r['revenue_period']} revenue: ${r['quarterly_revenue_billion']}B")
        print(f"  -> capex guidance = {r['capex_low_as_multiple_of_quarterly_revenue']}x to "
              f"{r['capex_high_as_multiple_of_quarterly_revenue']}x that single quarter's revenue")
        print(f"  CAVEAT: {r['caveat']}")
    print()

    print("=" * 78)
    print("2. CHRONOLOGICAL TIMELINE (capex pressure <-> silicon strategy)")
    print("=" * 78)
    rows = [dict(r) for r in conn.execute("SELECT * FROM v_strategy_timeline")]
    results["strategy_timeline"] = rows
    for r in rows:
        tag = "[CAPEX PRESSURE]" if r["category"] == "capex_pressure" else "[SILICON STRATEGY]"
        print(f"  {r['event_date_display']:<45} {tag}")
        print(f"    {r['event']}")
        print(f"    -> {r['what_it_means']}")
    print()

    print("=" * 78)
    print("3. ADDRESSABLE SHARE (order-of-magnitude framing only)")
    print("=" * 78)
    row = dict(conn.execute("SELECT * FROM v_addressable_share").fetchone())
    results["addressable_share"] = row
    print(f"  {row['cited_industry_estimate']} (source: {row['estimate_source']})")
    print(f"  MTIA scope: {row['mtia_scope']} (source: {row['mtia_scope_source']})")
    print(f"  Conclusion: {row['conclusion']}")
    print(f"  Disclosure gap: {row['disclosure_gap']}")
    print()

    OUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote derived analysis to {OUT_PATH}")

    conn.close()


if __name__ == "__main__":
    main()
