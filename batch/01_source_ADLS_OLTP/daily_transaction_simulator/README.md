# AtliQ Commerce — Daily Order Simulator

This script generates a few fresh OLTP orders so your nightly OLTP → OLAP pipeline always has new data to ingest. Each run creates new orders, items, and payments with updated timestamps, making your incremental ADF pipeline behave like a real production system.

---

## Setup

1. Go to the `atliq_simulator/` folder.
2. Create a `.env` file next to the script:

```
AZ_SQL_SERVER=example.database.windows.net
AZ_SQL_DB=example
AZ_SQL_USER=example
AZ_SQL_PASSWORD=your_password
```

> Tip: Commit `.env.example`, not your real `.env`.

3. Install dependencies:

```
pip install -r requirements.txt
```

(Requires ODBC Driver 18 for SQL Server.)

---

## Run the simulator

```
python daily_order_simulator.py --orders 8
```

Change the number as needed:

```
python daily_order_simulator.py --orders 15
```

Each run inserts new rows into the OLTP database. Your ADF pipeline will pick up only rows with a newer `updated_at`.
