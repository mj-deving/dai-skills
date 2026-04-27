---
name: Crawl4AI
description: Free open-source multi-page website crawler — self-hosted Python crawler that outputs LLM-ready Markdown with JS rendering. USE WHEN crawl website free, crawl site, crawl pages free, free crawler, open source crawler, crawl4ai, crawl without cost, self-hosted crawl, map website, extract all pages.
---

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/Crawl4AI/`

# Crawl4AI — Free Self-Hosted Website Crawler

Open-source Python crawler (58K+ GitHub stars). Crawls entire websites, outputs clean Markdown, handles JavaScript. Completely free, runs locally.

## When to Use
- Crawl multiple pages of a website (free alternative to BrightData Crawl)
- Extract all pages under a URL path
- Build a sitemap + content index
- When BrightData costs are not justified

## When NOT to Use
- Single page scraping (→ Jina Reader, faster)
- Anti-bot / Cloudflare bypass needed (→ BrightData)
- Social media platforms (→ Apify)
- High-volume at scale (→ Spider.cloud)

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Crawl website, crawl all pages, map site, extract site | `Workflows/Crawl.md` |

## Prerequisites
- Python 3.12 ✅
- crawl4ai package (pip install)
- Playwright browsers (for JS rendering)

## Capabilities
- JS rendering: Yes (via Playwright)
- Markdown output: Yes (native)
- Multi-page crawling: Yes
- AI extraction: Yes (with own LLM)
- Cost: $0 (self-hosted)
- Rate limit: Only your machine's capacity
