# Generated data artifacts

This directory is populated by the reproducible pipeline.

Run:

```bash
python etl/load_data.py
python etl/derived_analysis.py
```

The commands generate:

- `meta_silicon_strategy.db` — SQLite warehouse built from sourced public figures.
- `derived_analysis.json` — JSON export of the analytical SQL views.

Generated artifacts are intentionally not committed so stale outputs cannot drift from the source code and cited public data.