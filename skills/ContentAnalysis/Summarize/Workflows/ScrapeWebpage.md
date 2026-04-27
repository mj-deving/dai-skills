---
workflow: scrape-webpage
purpose: Extract clean content from any webpage as Markdown
---

# ScrapeWebpage

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Scraping webpage via Summarize skill"}' > /dev/null 2>&1 &
```
-->

## When to Use
- User wants webpage content as clean Markdown
- JS-rendered page that WebFetch cannot capture
- Content extraction from articles, blogs, documentation
- As input for further processing (ExtractWisdom, Research)

## Workflow Steps

### Step 1: Source environment
```bash
[ -f ${AGENT_HOME}/.env ] && export $(grep -v '^#' ${AGENT_HOME}/.env | xargs)
```

### Step 2: Select scraping method (escalation order)

**Tier 1 — Jina Reader (fastest, free, JS-capable):**
```bash
curl -s "https://r.jina.ai/<url>"
# Or via WebFetch:
# WebFetch url="https://r.jina.ai/<url>"
```
No API key needed. Handles JS-rendered pages. Try this FIRST.

**Tier 2 — summarize extract (Readability parser):**
```bash
summarize --extract --format md "<url>"
```

**Tier 3 — summarize + Firecrawl (JS-heavy sites):**
```bash
summarize --extract --format md --firecrawl always "<url>"
```
Requires: `FIRECRAWL_API_KEY`

**Tier 4 — LLM-cleaned Markdown:**
```bash
summarize --extract --format md --markdown-mode llm "<url>"
```

### Step 3: Quality check
- Result <100 words → probably JS-rendered → try Jina Reader first, then `--firecrawl always`
- Only boilerplate → site blocks scraping → escalate to Scraping-Skill (Playwright/BrightData)
- Content OK → proceed

### Step 4: Save & further process
```bash
# Save
summarize --extract --format md "<url>" > extracts/<name>.md

# Optional: create summary
summarize "<url>" --length medium

# Optional: feed to ExtractWisdom
# cat extracts/<name>.md → ExtractWisdom pipeline
```

## When NOT to use Summarize — use Scraping-Skill instead
- Login-protected pages → Scraping-Skill (browser cookies)
- Social media profiles → Scraping-Skill (Apify actors)
- Pagination / infinite scroll → Scraping-Skill (Playwright)
- Anti-bot protection (Cloudflare) → Scraping-Skill (Bright Data)
- Structured data extraction (tables, prices) → Scraping-Skill

## Scraping Tier Decision
```
Can WebFetch handle it?
├── Yes → Use WebFetch (fastest)
└── No
    ├── Static content, just bad HTML? → summarize --extract --format md
    ├── JS-rendered SPA? → summarize --extract --firecrawl always
    ├── Anti-bot / Cloudflare? → Scraping-Skill Bright Data
    ├── Needs browser interaction? → Scraping-Skill Playwright
    └── Social media? → Scraping-Skill Apify
```
