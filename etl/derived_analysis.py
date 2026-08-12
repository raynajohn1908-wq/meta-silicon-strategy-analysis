"""Run sourced analytical views and export the results as JSON."""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "meta_silicon_strategy.db"
VIEWS_PATH = ROOT / "sql" / "views.sql"
OUT_PATH = ROOT / "data" / "derived_analysis.json"


def rows(conn, query):
    return [dict(r) for r in conn.execute(query)]


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    for view in ("v_capex_scale_check", "v_strategy_timeline", "v_workload_scope"):
        conn.execute(f"DROP VIEW IF EXISTS {view}")
    conn.executescript(VIEWS_PATH.read_text(encoding="utf-8"))

    results = {
        "capex_scale_check": rows(conn, "SELECT * FROM v_capex_scale_check"),
        "strategy_timeline": rows(conn, "SELECT * FROM v_strategy_timeline"),
        "workload_scope": rows(conn, "SELECT * FROM v_workload_scope"),
    }

    OUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")

    scale = results["capex_scale_check"][0]
    print("Q2 2026 financial scale check")
    print(f"  Revenue: ${scale['quarterly_revenue_billion']}B")
    print(f"  Capex:   ${scale['quarterly_capex_billion']}B")
    print(f"  Capex / revenue: {scale['quarterly_capex_as_share_of_revenue']:.1%}")
    print(f"  FY2026 capex guidance: ${scale['fy_capex_guidance_low_billion']}B-${scale['fy_capex_guidance_high_billion']}B")
    print()
    print("MTIA workload scope")
    for item in results["workload_scope"]:
        print(f"  {item['chip_name']}: {item['near_term_use']} | {item['capability']} | {item['production_status']}")
    print(f"\nWrote {OUT_PATH}")

    conn.close()


if __name__ == "__main__":
    main()
