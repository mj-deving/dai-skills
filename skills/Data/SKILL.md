---
name: Data
description: Structured data processing and economic metrics — DuckDB SQL, miller, xsv, gron, jq/yq for local files plus 68 US economic indicators from FRED, EIA, Treasury, BLS. USE WHEN data processing, CSV, JSON, parquet, SQL query, DuckDB, miller, xsv, aggregate, filter data, data analysis, GDP, inflation, unemployment, economic metrics, FRED, economic overview, US metrics.
---

# Data

Unified skill for structured data processing and economic analysis.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Data processing, CSV, JSON, parquet, SQL query, DuckDB, miller, xsv, aggregate, filter, convert format, data analysis | `DataProcessing/SKILL.md` |
| GDP, inflation, unemployment, economic metrics, gas prices, FRED, economic overview, US metrics, update data | `USMetrics/SKILL.md` |

## Examples

**Example 1: Query a CSV with SQL**
```
User: "Query this CSV to find the top 10 customers by revenue"
→ Routes to DataProcessing
→ Uses DuckDB SQL on the local file
```

**Example 2: Get current US economic state**
```
User: "How is the US economy doing?"
→ Routes to USMetrics
→ Fetches FRED/EIA/Treasury indicators, generates analysis
```

**Example 3: Process JSON data**
```
User: "Flatten this nested JSON and extract the prices"
→ Routes to DataProcessing
→ Uses gron for flattening, jq for extraction
```
