#!/usr/bin/env python3
"""Generate a simple monthly cost report."""

from __future__ import annotations

import csv
import datetime as dt
import pathlib


MODEL_PATH = pathlib.Path("tools/py/cost/model.csv")
OUTPUT_PATH = pathlib.Path("docs/reports/cost-report.md")


def load_metric(rows: list[dict[str, str]], name: str) -> float:
    for row in rows:
        if row["metric"] == name:
            return float(row["value"])
    raise KeyError(name)


def main() -> int:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(MODEL_PATH)

    with MODEL_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    request_cost_eur = load_metric(rows, "request_cost_eur")
    avg_requests = load_metric(rows, "session_avg_requests")
    active_users = load_metric(rows, "active_users")

    monthly_cost = active_users * avg_requests * request_cost_eur * 30

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        "# Cost Report {:%Y-%m}\n\n≈ {:.2f} EUR/Monat\n".format(
            dt.date.today(), monthly_cost
        ),
        encoding="utf-8",
    )

    print(OUTPUT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
