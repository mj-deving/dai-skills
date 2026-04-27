---
name: Summarize
description: Universal content extraction, summarization, web scraping, and transcription via summarize CLI (v0.11.1). USE WHEN summarize URL, extract transcript, YouTube transcript, summarize video, summarize article, batch summarize, extract slides, transcribe audio, summarize webpage, scrape website, extract markdown, web extraction, content extraction, scrape URL, podcast transcript, audio to text, video slides, OCR slides, extract content from URL.
---

## Customization

**Before executing, check for user customizations at:**
`${PAI_USER_DIR}/SKILLCUSTOMIZATIONS/Summarize/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior.

# Summarize — Universal Content Extraction & Summarization

Five capabilities in one CLI tool: **Summarize**, **Scrape**, **Transcribe**, **Extract Slides**, **Batch Process**.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Summarize URL/video/article, key takeaways from URL | `Workflows/SummarizeContent.md` |
| Extract transcript, YouTube transcript, transcribe audio/video | `Workflows/ExtractTranscript.md` |
| Scrape URL, extract webpage, get markdown from site | `Workflows/ScrapeWebpage.md` |
| Summarize multiple URLs, batch process | `Workflows/BatchProcess.md` |
| Extract slides, slides from video, OCR slides | `Workflows/SlideExtract.md` |

## Quick Decision Tree

```
User wants...
├── Summary of content → SummarizeContent
├── Raw text/transcript → ExtractTranscript
├── Webpage as Markdown → ScrapeWebpage
├── Multiple URLs processed → BatchProcess
└── Visual slides from video → SlideExtract
```

## Environment Setup

Source API keys before any summarize call:
```bash
[ -f ${AGENT_HOME}/.env ] && export $(grep -v '^#' ${AGENT_HOME}/.env | xargs)
export YT_DLP_PATH=$(which yt-dlp 2>/dev/null || echo ${HOME}/.local/bin/yt-dlp)
```

## Integration with ExtractWisdom

Summarize extracts and compresses. ExtractWisdom analyzes in depth.
Pipeline: `summarize --extract` → raw text → ExtractWisdom → structured insights.

## Scraping Tier Model

```
Tier 0: WebFetch (built-in, fastest, limited to static HTML)
Tier 1: Summarize --extract --format md (Readability + optional Firecrawl)
Tier 2: Scraping-Skill Bright Data Proxy (anti-bot bypass)
Tier 3: Scraping-Skill Playwright (full browser rendering)
Tier 4: Scraping-Skill Apify Actors (social media platforms)
```
Use Summarize for Tier 1 before escalating to heavier tools.
