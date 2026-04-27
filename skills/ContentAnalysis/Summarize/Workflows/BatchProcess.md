---
workflow: batch-process
purpose: Process multiple URLs in parallel with summarize
---

# BatchProcess

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Batch processing URLs via Summarize skill"}' > /dev/null 2>&1 &
```
-->

## When to Use
- User provides multiple URLs to summarize/extract
- Bulk processing of YouTube playlists
- Analyzing multiple articles/sources in parallel

## Workflow Steps

### Step 1: Source environment
```bash
[ -f ${AGENT_HOME}/.env ] && export $(grep -v '^#' ${AGENT_HOME}/.env | xargs)
export YT_DLP_PATH=$(which yt-dlp 2>/dev/null || echo ${HOME}/.local/bin/yt-dlp)
```

### Step 2: Parse input
- Extract all URLs from user message
- Assign sequential IDs (01, 02, ...)
- For YouTube: get titles via noembed API
  ```bash
  curl -s "https://noembed.com/embed?url=<yt-url>" | grep -o '"title":"[^"]*"' | cut -d'"' -f4
  ```

### Step 3: Parallel extraction (max 7 concurrent)
```bash
mkdir -p extracts
for url in $URLS; do
  id=$(echo "$url" | grep -oP '[?&]v=\K[^&]+' || basename "$url")
  summarize --extract --youtube web "$url" > "extracts/${num}_${id}.txt" 2>&1 &
done
wait
```

Use `run_in_background: true` for the batch command.

### Step 4: Check failures and retry
```bash
for f in extracts/*.txt; do
  words=$(wc -w < "$f")
  [ "$words" -lt 50 ] && echo "FAILED: $f ($words words)"
done
```
Retry failed ones via yt-dlp fallback or manual Whisper pipeline.

### Step 5: Parallel summarization
```bash
for url in $URLS; do
  summarize "$url" --youtube web > "extracts/sum_${num}.txt" 2>&1 &
done
wait
```

### Step 6: Build combined document
- Create Markdown document with all summaries
- Table of contents with video titles + links
- Per-video: title, URL, summary, key takeaways
- Links to raw extract files
- Cross-cutting analysis section

## Performance Tips
- Max 7 parallel summarize processes (avoid API rate limits)
- Use `--youtube web` first (fastest), only fall back when needed
- For audio transcription: run sequentially (CPU-bound)
- Use `run_in_background: true` for long-running batches
