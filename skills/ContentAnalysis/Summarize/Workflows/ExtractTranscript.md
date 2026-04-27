---
workflow: extract-transcript
purpose: Extract transcript from YouTube video or audio/video file
---

# ExtractTranscript

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Extracting transcript via Summarize skill"}' > /dev/null 2>&1 &
```
-->

## When to Use
- User wants YouTube video transcript
- User wants audio/video file transcription
- User wants raw text from media for further processing

## Workflow Steps

### Step 1: Source environment
```bash
[ -f ${AGENT_HOME}/.env ] && export $(grep -v '^#' ${AGENT_HOME}/.env | xargs)
export YT_DLP_PATH=$(which yt-dlp 2>/dev/null || echo ${HOME}/.local/bin/yt-dlp)
```

### Step 2: Determine source type
- YouTube URL → Step 3
- Local audio/video file → Step 4
- Web URL with embedded video → try Step 3 approach

### Step 3: YouTube Transcript (Fallback-Kette)

**Attempt 1 — Web subtitles (fastest, no setup):**
```bash
summarize --extract --youtube web "<url>"
```
Check result: <50 words or YouTube boilerplate → Attempt 2

**Attempt 2 — yt-dlp mode:**
```bash
summarize --extract --youtube yt-dlp "<url>"
```
Empty result → Attempt 3

**Attempt 3 — Manual audio download + local Whisper:**
```bash
# Download audio
${HOME}/.local/bin/yt-dlp -x --audio-format mp3 --audio-quality 5 \
  -o "${TMPDIR}/%(id)s.%(ext)s" "<url>"

# Transcribe via summarize (uses Groq if GROQ_API_KEY set)
summarize --extract "${TMPDIR}/<id>.mp3"

# Final fallback: local Whisper (CPU, always available, slower)
${HOME}/.local/bin/whisper "${TMPDIR}/<id>.mp3" \
  --model base --language de --output_format txt --output_dir ${TMPDIR}/
```

### Step 4: Local audio/video transcription
```bash
# Via summarize (auto-selects best backend)
summarize --extract "<filepath>"

# Direct local Whisper
${HOME}/.local/bin/whisper "<filepath>" \
  --model base --language de --output_format txt --output_dir .
```

### Step 5: Optional formatting
```bash
# Clean markdown from raw transcript
summarize "<transcript.txt>" --extract --format md --markdown-mode llm
```

### Step 6: Save output
- Save to `extracts/<descriptive-name>.txt`
- For YouTube: use `<num>_<video-id>.txt` naming

## Transcription Backends (priority order)
1. Groq Whisper (`GROQ_API_KEY`) — fastest, free tier, VPN may block
2. OpenAI Whisper (`OPENAI_API_KEY`) — fast, paid
3. FAL Whisper (`FAL_KEY`) — fast
4. Local Whisper (`${HOME}/.local/bin/whisper`) — slow (CPU), always works
5. Parakeet/Canary ONNX (`summarize transcriber setup`) — medium speed

## Tips
- Use `--timestamps` to include timestamps in transcript
- Use `run_in_background: true` for long transcriptions
- For batch YouTube: use BatchProcess workflow instead
- YouTube video titles via: `curl -s "https://noembed.com/embed?url=<url>" | grep -o '"title":"[^"]*"'`
