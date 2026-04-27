---
name: JinaReader
description: Free zero-setup web scraping via Jina Reader API — converts any URL to clean Markdown with JS rendering, no API key needed. USE WHEN jina reader, free scrape, quick scrape, extract webpage free, scrape without key, simple scrape, lightweight scrape, get page content.
---

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/JinaReader/`

# Jina Reader — Free Zero-Setup Web Scraper

The simplest web scraping tool available: prepend `r.jina.ai/` to any URL and get clean Markdown back. No API key, no account, no setup. Handles JavaScript-rendered pages.

## When to Use
- Quick single-page scraping without setup
- JS-rendered pages that WebFetch can't handle
- As Tier 1 before escalating to heavier tools
- Free alternative to Firecrawl for single pages

## When NOT to Use
- Multi-page crawling (→ Crawl4AI or BrightData)
- Anti-bot bypass needed (→ BrightData)
- Social media platforms (→ Apify)
- Structured data extraction / JSON output (→ Firecrawl or Crawl4AI)
- Rate: ~200 RPM limit — not for bulk scraping (→ Spider.cloud)

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Scrape URL free, quick extract, get page content | `Workflows/Scrape.md` |

## Capabilities
- JS rendering: Yes
- Markdown output: Yes
- API key: Not required
- Rate limit: ~200 requests/minute, 1M tokens/month free
- Crawling: No (single page only)
- AI extraction: No
