---
workflow: jina-scrape
purpose: Scrape a single webpage to clean Markdown via Jina Reader
---

# Jina Reader Scrape

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Scraping webpage via Jina Reader"}' > /dev/null 2>&1 &
```
-->

## Workflow Steps

### Step 1: Scrape via Jina Reader
```bash
curl -s "https://r.jina.ai/<url>"
```

Or via WebFetch tool:
```
WebFetch url="https://r.jina.ai/<url>" prompt="Extract all content"
```

### Step 2: Quality check
- Empty or error → URL may be blocked → escalate to summarize --extract or BrightData
- Content OK → use directly or save

### Step 3: Optional — save output
```bash
curl -s "https://r.jina.ai/<url>" > extracts/<name>.md
```

## Advanced Options

Jina Reader supports headers for customization:
```bash
# With specific options
curl -s "https://r.jina.ai/<url>" \
  -H "X-Return-Format: markdown" \
  -H "X-With-Links: true"
```

## Escalation Path
```
Jina Reader fails → summarize --extract --format md
  ↓ fails
summarize --extract --firecrawl always
  ↓ fails
Scraping-Skill: Playwright / BrightData
```
