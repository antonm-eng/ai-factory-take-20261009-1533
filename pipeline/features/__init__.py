"""Step 3: build churn features from the validated batch."""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

FEATURES_DIR = Path(__file__).parent
FEATURE_SETS = ["recharge", "usage"]


def build_features(conn: sqlite3.Connection, run_ts: datetime) -> dict:
    params = {
        "run_ts": run_ts.strftime("%Y-%m-%d %H:%M:%S"),
        "window_start": (run_ts - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
    }
    counts = {}
    for name in FEATURE_SETS:
        sql = (FEATURES_DIR / f"{name}.sql").read_text()
        conn.execute(f"DROP TABLE IF EXISTS features_{name}")
        conn.execute(f"CREATE TABLE features_{name} AS {sql}", params)
        counts[name] = conn.execute(f"SELECT COUNT(*) FROM features_{name}").fetchone()[0]
    return counts
