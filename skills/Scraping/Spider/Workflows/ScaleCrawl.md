---
workflow: spider-scale-crawl
purpose: High-volume web crawling via Spider.cloud API
---

# Spider.cloud Scale Crawl

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Scale crawling via Spider.cloud"}' > /dev/null 2>&1 &
```
-->

## Prerequisites
```bash
# API key must be set
export SPIDER_API_KEY=$(grep SPIDER_API_KEY ${AGENT_HOME}/.env | cut -d= -f2)
```

## Workflow Steps

### Step 1: Single page scrape
```bash
curl -s -X POST "https://api.spider.cloud/scrape" \
  -H "Authorization: Bearer $SPIDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "<url>", "return_format": "markdown"}'
```

### Step 2: Multi-page crawl
```bash
curl -s -X POST "https://api.spider.cloud/crawl" \
  -H "Authorization: Bearer $SPIDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<start_url>",
    "limit": 100,
    "return_format": "markdown"
  }'
```

### Step 3: Save results
Process JSON response, save each page as separate Markdown file in `extracts/`.

## Cost Estimation
| Pages | Approx. Cost |
|---|---|
| 100 | ~$0.05 |
| 1,000 | ~$0.48 |
| 10,000 | ~$4.80 |
| 100,000 | ~$48.00 |

## Decision: Spider vs. Alternatives

```
<100 pages + free    → Crawl4AI (self-hosted)
<100 pages + fast    → Jina Reader
100-10K pages        → Spider.cloud (best price/performance)
10K+ pages           → Spider.cloud or BrightData Full Crawl
Anti-bot needed      → BrightData (only option)
```
