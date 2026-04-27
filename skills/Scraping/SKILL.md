---
name: Scraping
description: Web scraping via progressive escalation — Jina Reader, Crawl4AI, Spider.cloud, Bright Data, Apify actors, bird CLI for X/Twitter, discrawl for Discord, Katana URL discovery. USE WHEN scraping, crawl, scrape URL, Twitter scraping, Apify, bot detection, jina reader, crawl4ai, spider cloud, katana, URL discovery, bird, read tweet, search X, Discord search, Discord history, Discord messages, Discord members, Discord archive, discrawl.
---

# Scraping

Unified skill for web scraping and crawling workflows.

## Tier Decision Tree

```
Single page, quick & free     → JinaReader (r.jina.ai)
Single page, anti-bot needed  → BrightData (4-tier escalation)
URL discovery, site mapping   → Katana (fast crawl, URLs only)
Multi-page, free              → Crawl4AI (self-hosted Python)
Multi-page, at scale          → Spider.cloud (~$0.48/1K pages)
Multi-page, anti-bot          → BrightData Crawl API
Social media platforms        → Apify actors
X/Twitter                     → bird CLI
Discord servers               → discrawl (local SQLite archive)
```

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Quick scrape, free scrape, jina reader, lightweight extract | `JinaReader/SKILL.md` |
| katana, URL discovery, crawl URLs, site map, discover endpoints | See **Katana** section below |
| Crawl website free, crawl pages, crawl4ai, map site | `Crawl4AI/SKILL.md` |
| Scale scraping, bulk crawl, spider cloud, high volume | `Spider/SKILL.md` |
| Bright Data, proxy, anti-bot, CAPTCHA, progressive scraping | `BrightData/SKILL.md` |
| read tweet, search X, post tweet, reply tweet, bird, X timeline | `Bird/SKILL.md` |
| Discord search, Discord history, Discord messages, Discord members, Discord archive, discrawl | `Discord/SKILL.md` |
| Instagram, LinkedIn, TikTok, YouTube, Facebook, Google Maps, Amazon, Apify | `Apify/SKILL.md` |

## Error Fallback Chain

When a tier fails, escalate to the next tier with anti-bot capabilities:

```
JinaReader fails (empty/garbage/403)  → try Crawl4AI (has Playwright)
Crawl4AI fails (timeout/Playwright)   → try Spider.cloud (cloud-based)
Spider.cloud fails (rate limit/block)  → try BrightData (proxy rotation)
BrightData fails (all 4 tiers)        → report failure, suggest manual approach
```

For social media: Apify actor fails → check if bird CLI covers the platform (X only). No cross-platform fallback.

For Discord: discrawl is the dedicated tool — no fallback chain. If discrawl fails, check `discrawl doctor` for diagnostics.

## Katana — Fast URL Discovery

Use Katana for mapping a site's URL structure before committing to a full crawl with Spider.cloud or Crawl4AI. Faster than full crawlers when you only need URLs, not content.

```bash
# Crawl and discover URLs (depth 2)
katana -u https://example.com -d 2 -o urls.txt

# JavaScript rendering mode
katana -u https://example.com -headless -d 3

# Filter by extension (exclude images/CSS)
katana -u https://example.com -ef png,jpg,gif,css

# JSON output
katana -u https://example.com -jsonl -o results.jsonl

# Scope control (stay on domain)
katana -u https://example.com -fs "example.com" -d 5
```

**When to use:** Before Spider.cloud or Crawl4AI, when you need to map URL structure first. Also useful for discovering API endpoints, sitemaps, and hidden pages.

## Cost Overview

| Tool | Cost | Best For |
|---|---|---|
| Jina Reader | Free (1M tokens/mo) | Single pages, JS-rendered |
| Crawl4AI | Free (self-hosted) | Multi-page crawling <500 pages |
| Apify | Free tier ($5/mo) | Social media, lead gen |
| bird CLI | Free | X/Twitter |
| discrawl | Free (self-hosted) | Discord server archiving + search |
| Spider.cloud | ~$0.48/1K pages | Scale crawling 100-100K pages |
| BrightData | ~$500+/mo | Anti-bot, Cloudflare bypass |

## Examples

**Example 1:** `User: "[typical request]"` → Routes to appropriate sub-skill workflow

**Example 2:** `User: "[another request]"` → Routes to different sub-skill workflow
