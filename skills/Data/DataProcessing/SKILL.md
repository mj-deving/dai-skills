---
name: DataProcessing
description: CLI-first structured data processing — DuckDB SQL on local files, miller record transforms, xsv CSV operations, gron JSON flattening, jq/yq native patterns. USE WHEN data processing, CSV, JSON, parquet, SQL query, data transform, structured data, DuckDB, miller, xsv, aggregate, filter data, convert format, data analysis, query CSV, join files, column stats, flatten JSON, greppable JSON, format conversion, TSV, record transform, data pipeline.
---

# DataProcessing

CLI tools for structured data processing without spinning up databases.

## Tool Selection

```
SQL queries on CSV/JSON/Parquet    → DuckDB
Record-level CSV/JSON transforms   → miller (mlr)
Fast CSV slicing, stats, joins     → xsv
Flatten JSON for grep              → gron
JSON/YAML jq-style queries         → jq / yq (native, no skill needed)
```

## Availability Check

Before using any tool, verify installation:

```bash
which duckdb mlr xsv gron
```

## DuckDB — SQL on Local Files

Query CSV, JSON, and Parquet files directly with SQL. No server, no loading step.

```bash
# Query CSV directly
duckdb -c "SELECT * FROM 'data.csv' WHERE amount > 100 ORDER BY date"

# Join multiple files
duckdb -c "SELECT a.id, b.name FROM 'orders.csv' a JOIN 'customers.csv' b ON a.customer_id = b.id"

# Aggregate
duckdb -c "SELECT category, COUNT(*), AVG(price) FROM 'products.csv' GROUP BY category"

# Export to Parquet
duckdb -c "COPY (SELECT * FROM 'data.csv' WHERE active) TO 'filtered.parquet' (FORMAT PARQUET)"
```

**Best for:** Ad-hoc SQL queries, joins across files, aggregations, format conversion (CSV to Parquet).

## Miller (mlr) — Record-Level Transforms

Process CSV/JSON/TSV records with Unix-pipe-friendly commands.

```bash
# Filter rows
mlr --csv filter '$amount > 100' data.csv

# Add computed field
mlr --csv put '$total = $price * $quantity' data.csv

# Group-by stats
mlr --csv stats1 -a mean,count -f price -g category data.csv

# Format conversion
mlr --icsv --ojson cat data.csv
```

**Best for:** Row-level filtering, computed fields, group-by statistics, format conversion between CSV/JSON/TSV.

## xsv — Fast CSV Operations

Rust-based CSV toolkit for slicing, joining, and stats.

```bash
# Column stats
xsv stats data.csv

# Select columns
xsv select name,email data.csv

# Join files
xsv join id customers.csv customer_id orders.csv

# Frequency counts
xsv frequency -s category data.csv
```

**Best for:** Quick column stats, column selection, CSV joins, frequency analysis. Fastest option for large CSV files.

## gron — Greppable JSON

Flatten JSON into discrete path-value assignments for grep/sed/awk processing.

```bash
# Make JSON greppable
gron config.json | grep "database"

# Find all array paths
gron data.json | grep "\[" | sort -u

# Reverse back to JSON
gron config.json | grep "server" | gron --ungron
```

**Best for:** Exploring unfamiliar JSON structures, finding specific nested values, extracting subsets of complex JSON.

## jq / yq — Native Reference

Already available natively. Common patterns:

```bash
# jq — filter and transform JSON
cat data.json | jq '.items[] | select(.active) | {name, price}'
cat data.json | jq '[.items[] | .price] | add / length'

# yq — same syntax for YAML
yq '.services.web.ports' docker-compose.yml
```

## When NOT to Use This Skill

- **Files under 10 lines** — just read them directly
- **Data already in a running database** — query the database
- **Complex conditional logic** — write a TypeScript script
- **Real-time streaming data** — use purpose-built streaming tools
- **Simple jq/yq queries** — use them directly, no skill needed
