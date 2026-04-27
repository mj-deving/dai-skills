---
name: Spider
description: Low-cost high-scale web scraping and crawling via Spider.cloud API — Rust-based, fast, ~$0.48/1K pages. USE WHEN spider cloud, scale scraping, bulk scrape, bulk crawl, high volume scraping, scrape at scale, affordable crawling, spider.cloud.
---

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/Spider/`

# Spider.cloud — Low-Cost Scale Scraping

Rust-based web scraping API. Fastest option for high-volume scraping at ~$0.48 per 1,000 pages. Use when Crawl4AI is too slow or volume exceeds what self-hosted can handle.

## When to Use
- Scraping 1,000+ pages (scale)
- Need speed + reliability at low cost
- Crawl4AI too slow for the volume
- BrightData too expensive for the use case

## When NOT to Use
- <100 pages (→ Jina Reader or Crawl4AI, free)
- Anti-bot / Cloudflare bypass (→ BrightData)
- Social media platforms (→ Apify)
- Zero budget (→ Crawl4AI)

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Scale scrape, bulk crawl, spider.cloud | `Workflows/ScaleCrawl.md` |

## Prerequisites
- Spider.cloud account + API key
- Set `SPIDER_API_KEY` in `${AGENT_HOME}/.env`

## Pricing
- ~$0.48 per 1,000 pages
- Free credits on sign-up
- Open-source self-hosted option available (Rust)

## Capabilities
- JS rendering: Yes
- Markdown output: Yes
- Multi-page crawling: Yes (primary use case)
- Speed: Fastest (Rust-based)
- AI extraction: Yes
- Anti-bot: Basic
