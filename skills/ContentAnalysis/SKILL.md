---
name: ContentAnalysis
description: Content extraction and analysis — wisdom extraction, summarization, web scraping, transcription, slide extraction, YouTube to ebook, and AI builders digest. USE WHEN extract wisdom, content analysis, summarize URL, extract transcript, YouTube transcript, batch summarize, scrape website, newspaper4k, youtube to ebook, channel digest, AI builders digest, follow builders.
---

# ContentAnalysis

Unified skill for content extraction and analysis workflows.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Extract wisdom, content analysis, insight report, analyze content | `ExtractWisdom/SKILL.md` |
| Summarize URL/video/article, extract transcript, transcribe audio, scrape webpage, batch summarize, extract slides | `Summarize/SKILL.md` |
| YouTube to ebook, YouTube channels to EPUB, video to article, transcript to ebook | `YouTubeToEbook/SKILL.md` |
| newspaper4k, local extraction, article text, offline scrape | See **newspaper4k** section below |
| AI builders digest, AI industry insights, builder updates, /ai, follow builders | `FollowBuilders/SKILL.md` |

## newspaper4k — Local Article Extraction

Local-first article extraction using newspaper4k. No API keys, no external services, automatic boilerplate removal. Use when Jina Reader is unavailable or you want offline extraction.

**When to use:** Local/offline extraction needed, no API keys available, quick article text grab, boilerplate removal from news sites.

### Full extraction (title, authors, date, text)

```python
# Via pipx run (no global install needed)
pipx run --spec newspaper4k python3 -c "
from newspaper import Article
url = 'https://example.com/article'
article = Article(url)
article.download()
article.parse()
print(f'Title: {article.title}')
print(f'Authors: {article.authors}')
print(f'Date: {article.publish_date}')
print(f'Text: {article.text[:500]}')
"
```

### One-liner for quick text extraction

```bash
pipx run --spec newspaper4k python3 -c "from newspaper import Article; a = Article('URL'); a.download(); a.parse(); print(a.text)"
```

### Key advantages

- Runs locally, no API keys required
- Automatic boilerplate/ad removal
- Extracts metadata (authors, publish date, top image)
- Works offline once article HTML is cached
- No rate limits or token quotas

## Examples

**Example 1:** `User: "[typical request]"` → Routes to appropriate sub-skill workflow

**Example 2:** `User: "[another request]"` → Routes to different sub-skill workflow
