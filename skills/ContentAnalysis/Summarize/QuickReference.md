# Summarize CLI — Quick Reference

> `summarize` v0.11.1 — https://github.com/steipete/summarize

## Core Commands

```bash
# Summarize
summarize "<url>"                                    # AI summary (default: xl)
summarize "<url>" --length short                     # Quick summary
summarize "<url>" --length 20k                       # Long summary
summarize "<url>" --prompt "Extract 5 key decisions" # Custom focus
summarize "<url>" --language de                      # German output

# Extract (no LLM, raw content)
summarize "<url>" --extract                          # Raw text
summarize "<url>" --extract --format md              # Markdown
summarize "<url>" --extract --format md --markdown-mode llm  # LLM-cleaned MD

# YouTube
summarize "<yt-url>" --youtube web                   # Summary via subtitles
summarize "<yt-url>" --extract --youtube web         # Raw transcript
summarize "<yt-url>" --extract --youtube yt-dlp      # Via audio download
summarize "<yt-url>" --extract --timestamps          # With timestamps

# Audio/Video transcription
summarize "<file.mp3>" --extract                     # Transcribe audio
summarize "<file.mp3>"                               # Transcribe + summarize

# Web scraping
summarize "<url>" --extract --format md              # Standard scraping
summarize "<url>" --extract --firecrawl always       # JS-rendered pages

# Slides
summarize "<yt-url>" --slides                        # Summary + slides
summarize "<yt-url>" --slides --slides-ocr           # Slides + OCR
summarize "<yt-url>" --slides --extract              # Transcript + slides

# Stdin
cat file.txt | summarize -                           # Summarize stdin
pbpaste | summarize -                                # Summarize clipboard
```

## Flags Reference

### Input/Source
| Flag | Values | Default | Description |
|---|---|---|---|
| `--youtube` | auto, web, yt-dlp, no-auto, apify | auto | YouTube transcript source |
| `--transcriber` | auto, whisper, parakeet, canary | auto | Audio transcription backend |
| `--video-mode` | auto, transcript, understand | auto | Video handling mode |

### Output Control
| Flag | Values | Default | Description |
|---|---|---|---|
| `--extract` | (boolean) | false | Raw content, no LLM summary |
| `--format` | md, text | text (md in extract mode) | Content format |
| `--markdown-mode` | off, auto, llm, readability | readability | Markdown conversion method |
| `--length` | short/medium/long/xl/xxl or number | xl | Summary length |
| `--language` | auto, en, de, ... | auto | Output language |
| `--max-output-tokens` | number (e.g. 2k) | provider default | Hard token cap |
| `--max-extract-characters` | number | unlimited | Extract character limit |
| `--json` | (boolean) | false | Structured JSON output |
| `--plain` | (boolean) | false | No ANSI rendering |
| `--timestamps` | (boolean) | false | Include timestamps |

### LLM Control
| Flag | Values | Default | Description |
|---|---|---|---|
| `--model` | auto, provider/model | auto | LLM model selection |
| `--cli` | claude, gemini, codex, agent | (none) | Use CLI provider |
| `--prompt` | text | (built-in) | Override summary prompt |
| `--prompt-file` | path | (none) | Prompt from file |
| `--force-summary` | (boolean) | false | Force LLM even on short content |

### Web Scraping
| Flag | Values | Default | Description |
|---|---|---|---|
| `--firecrawl` | off, auto, always | auto | Firecrawl for JS pages |
| `--preprocess` | off, auto, always | auto | Input preprocessing |

### Slides
| Flag | Values | Default | Description |
|---|---|---|---|
| `--slides` | (boolean/value) | false | Extract slides from video |
| `--slides-ocr` | (boolean) | false | OCR on slides (needs tesseract) |
| `--slides-max` | number | 6 | Max slides to extract |
| `--slides-dir` | path | ./slides | Output directory |
| `--slides-scene-threshold` | 0.1-1.0 | 0.3 | Scene change sensitivity |
| `--slides-min-duration` | seconds | 2 | Min time between slides |
| `--slides-debug` | (boolean) | false | Show paths instead of inline |

### Caching & Performance
| Flag | Values | Default | Description |
|---|---|---|---|
| `--no-cache` | (boolean) | false | Bypass LLM cache |
| `--no-media-cache` | (boolean) | false | Bypass media cache |
| `--timeout` | duration (30s, 2m) | 2m | Fetch/LLM timeout |
| `--retries` | number | 1 | LLM retry attempts |
| `--cache-stats` | (boolean) | false | Show cache stats |
| `--clear-cache` | (boolean) | false | Delete cache DB |

### Debug
| Flag | Description |
|---|---|
| `--verbose` / `--debug` | Detailed progress |
| `--metrics detailed` | Full metrics output |
| `--stream on/off` | Control LLM streaming |
| `--no-color` | Disable ANSI colors |
| `--theme` | aurora, ember, moss, mono |

## Environment Variables

### Transcription (priority order)
```bash
GROQ_API_KEY=gsk_...           # Groq Whisper (fastest, free)
OPENAI_API_KEY=sk-...          # OpenAI Whisper
FAL_KEY=...                    # FAL AI Whisper
# Local whisper: ${HOME}/.local/bin/whisper (CPU fallback)
```

### LLM Providers
```bash
ANTHROPIC_API_KEY=...          # Claude models
OPENAI_API_KEY=sk-...          # GPT models
GEMINI_API_KEY=...             # Gemini models
XAI_API_KEY=...                # Grok models
OPENROUTER_API_KEY=...         # OpenRouter (any model)
```

### Web Scraping
```bash
FIRECRAWL_API_KEY=...          # Firecrawl for JS pages
```

### YouTube
```bash
YT_DLP_PATH=${HOME}/.local/bin/yt-dlp  # yt-dlp binary
APIFY_API_TOKEN=...                       # Apify fallback
```

### CLI Providers
```bash
CLAUDE_PATH=...                # Claude CLI binary
CODEX_PATH=...                 # Codex CLI binary
GEMINI_PATH=...                # Gemini CLI binary
```

### Preferences
```bash
SUMMARIZE_MODEL=...            # Default model override
SUMMARIZE_THEME=aurora         # CLI theme
SUMMARIZE_TRANSCRIBER=auto     # Default transcriber
```

## Model Identifiers

```
# CLI providers (subscription-based, no API key)
cli/claude/sonnet
cli/claude/opus

# API providers
anthropic/claude-sonnet-4-5-20250514
openai/gpt-4o
openai/gpt-5-mini
google/gemini-2.0-flash
xai/grok-3
zai/z1-mini

# OpenRouter
openrouter/<author>/<slug>
```

## Installed Infrastructure

| Component | Path | Version |
|---|---|---|
| summarize | `$(which summarize)` | v0.11.1 |
| yt-dlp | `${HOME}/.local/bin/yt-dlp` | 2026.03.13 |
| whisper | `${HOME}/.local/bin/whisper` | openai-whisper 20250625 |
| ffmpeg | `/bin/ffmpeg` | 6.1.1 |
| tesseract | not installed | needed for --slides-ocr |
