---
workflow: crawl4ai-crawl
purpose: Crawl multiple pages from a website using Crawl4AI (free, self-hosted)
---

# Crawl4AI Crawl

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Crawling website via Crawl4AI"}' > /dev/null 2>&1 &
```
-->

## When to Use
- Crawl 1-100+ pages from a website
- Free alternative to BrightData Crawl API
- When content needs to be extracted as Markdown

## Workflow Steps

### Step 1: Simple crawl (Python one-liner)
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        print(result.markdown)

asyncio.run(crawl("<url>"))
```

### Step 2: Multi-page crawl with link following
```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def crawl_site(start_url, max_pages=50):
    config = CrawlerRunConfig(
        follow_links=True,
        max_pages=max_pages,
        output_format="markdown"
    )
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=[start_url],
            config=config
        )
        for r in results:
            with open(f"extracts/{r.url.split('/')[-1] or 'index'}.md", "w") as f:
                f.write(r.markdown)
            print(f"Scraped: {r.url} ({len(r.markdown)} chars)")

asyncio.run(crawl_site("<start_url>", max_pages=50))
```

### Step 3: Save as script and run
```bash
python3 ${TMPDIR}/crawl_script.py
```

## Scale Comparison

| Pages | Crawl4AI (free) | BrightData Light | BrightData Full |
|---|---|---|---|
| 1-50 | Best choice | Works | Overkill |
| 50-500 | Good (slower) | Good | Best choice |
| 500+ | Possible but slow | — | Best choice |

## Escalation
If Crawl4AI fails (anti-bot, rate limiting):
→ BrightData Light Crawl (MCP batch, ~$0.006/page)
→ BrightData Full Crawl (API, $1.50/1K pages)
→ Spider.cloud (scale crawling, ~$0.48/1K pages)
