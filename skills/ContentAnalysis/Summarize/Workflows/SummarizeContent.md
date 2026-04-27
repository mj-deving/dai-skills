---
workflow: summarize-content
purpose: Summarize any URL, file, or text content via AI
---

# SummarizeContent

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Summarizing content via Summarize skill"}' > /dev/null 2>&1 &
```
-->

## When to Use
- User wants a summary of a URL, article, video, or document
- User pastes text and wants it condensed
- User wants key takeaways from content

## Workflow Steps

### Step 1: Source environment
```bash
[ -f ${AGENT_HOME}/.env ] && export $(grep -v '^#' ${AGENT_HOME}/.env | xargs)
export YT_DLP_PATH=$(which yt-dlp 2>/dev/null || echo ${HOME}/.local/bin/yt-dlp)
```

### Step 2: Determine input type and flags
| Input | Extra flags |
|---|---|
| YouTube URL | `--youtube web` |
| Web URL | (none) |
| Local file | (none) |
| Stdin/text | pipe via `summarize -` |

### Step 3: Determine length
| User intent | Flag |
|---|---|
| Quick overview | `--length short` |
| Standard | (default = xl) |
| Detailed | `--length xxl` or `--length 20k` |
| Custom focus | `--prompt "Focus on..."` |

### Step 4: Determine output language
| User intent | Flag |
|---|---|
| Match source | (default = auto) |
| German | `--language de` |
| English | `--language en` |

### Step 5: Execute
```bash
summarize "<input>" [flags]
```

### Step 6: Post-process
- Structured output needed → add `--json`
- Feed to ExtractWisdom → save as .txt, then run ExtractWisdom
- Raw text needed → add `--plain`

## Model Selection
Default is `auto` (uses Claude CLI subscription). Override with:
- `--model anthropic/claude-sonnet-4-5-20250514`
- `--cli claude` (subscription, no API key)
- `--model openai/gpt-4o`
- `--model google/gemini-2.0-flash`

## Examples
```bash
# Standard summary
summarize "https://example.com/article"

# YouTube video summary in German
summarize "https://youtube.com/watch?v=..." --youtube web --language de

# Long detailed summary
summarize "https://example.com" --length xxl

# Custom prompt
summarize "https://example.com" --prompt "Extrahiere die 5 wichtigsten Geschäftsentscheidungen"

# Stdin
cat document.txt | summarize - --length medium
```
