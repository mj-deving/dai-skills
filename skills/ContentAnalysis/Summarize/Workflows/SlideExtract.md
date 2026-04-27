---
workflow: slide-extract
purpose: Extract visual slides from YouTube videos with optional OCR
---

# SlideExtract

<!-- ## Voice Notification
```bash
curl -s -X POST http://localhost:8888/notify -H "Content-Type: application/json" \
  -d '{"message": "Extracting slides via Summarize skill"}' > /dev/null 2>&1 &
```
-->

## When to Use
- User wants presentation slides from a video
- Lecture/conference videos with visual content
- OCR from whiteboard recordings or screencasts
- Extracting key frames from tutorials
- User wants to see what's visually shown in a video without watching it

## Workflow Steps

### Step 1: Source environment
```bash
[ -f ${AGENT_HOME}/.env ] && export $(grep -v '^#' ${AGENT_HOME}/.env | xargs)
export YT_DLP_PATH=$(which yt-dlp 2>/dev/null || echo ${HOME}/.local/bin/yt-dlp)
```

### Step 2: Assess video type and choose settings

**Critical:** Slide extraction quality depends heavily on the video format. Choose settings accordingly:

| Video Type | Recommended Settings | Why |
|---|---|---|
| **Screencast / Tutorial** | `--slides-max 12 --slides-scene-threshold 0.3` | Many visual changes, default works well |
| **Presentation / Lecture** | `--slides-max 15 --slides-scene-threshold 0.3 --slides-min-duration 10` | Slides stay long, avoid duplicates |
| **Talking Head + Grafiken** | `--slides-max 8 --slides-scene-threshold 0.5 --slides-min-duration 5` | Filter out identical presenter frames |
| **Whiteboard / Handwriting** | `--slides-max 10 --slides-scene-threshold 0.4 --slides-ocr` | OCR extracts handwritten text |
| **Demo / Live Coding** | `--slides-max 20 --slides-scene-threshold 0.2 --slides-min-duration 3` | Fast changes, capture more |

### Step 3: Execute extraction

**Standard — Summary + inline slides:**
```bash
summarize "<yt-url>" --slides --slides-max 8 \
  --slides-scene-threshold 0.5 --slides-min-duration 5 \
  --slides-dir ./slides --youtube web
```

**With OCR (German + English):**
```bash
summarize "<yt-url>" --slides --slides-ocr --slides-max 10 \
  --slides-dir ./slides --youtube web
```

**Full transcript interleaved with slides:**
```bash
summarize "<yt-url>" --slides --extract --slides-max 12 \
  --slides-dir ./slides --youtube web
```

**Slides-only mode (no summary):**
```bash
summarize slides "<yt-url>" --render auto --slides-max 10
```

### Step 4: Verify results
- Check `--slides-dir` for extracted PNG files
- Naming: `slide_NNNN_TIMEs.png` (e.g. `slide_0003_211.80s.png`)
- Review slide images: `Read` tool on each PNG
- If too many identical frames → increase `--slides-scene-threshold`
- If missing key visuals → decrease threshold or increase `--slides-max`

### Step 5: Optional post-processing

**OCR on individual slides (if --slides-ocr wasn't used):**
```bash
tesseract <slide.png> <output> -l deu+eng
```

**AI enhancement of extracted slides (Gemini Flash Image):**
```python
import base64, json, requests
API_KEY = "$(grep GEMINI_API_KEY ${AGENT_HOME}/.env | cut -d= -f2)"
with open("slide.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
payload = {
    "contents": [{"parts": [
        {"inlineData": {"mimeType": "image/png", "data": img_b64}},
        {"text": "Clean up: remove reflections, sharpen text, white background. Keep content unchanged."}
    ]}],
    "generationConfig": {"responseModalities": ["image", "text"]}
}
resp = requests.post(url, json=payload, timeout=60).json()
for part in resp["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        with open("slide_enhanced.png", "wb") as f:
            f.write(base64.b64decode(part["inlineData"]["data"]))
```

**Convert to Mermaid diagram (for flowcharts/process diagrams):**
1. OCR the slide: `tesseract slide.png output -l deu`
2. Read OCR output and build Mermaid syntax
3. Render: `npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.png`

## Best Practice Notes (from testing)

### What works well
- **Screencast/tutorial videos** produce the best slides — every visual change is captured
- **OCR (tesseract)** reads printed text well, handwriting moderately
- **Gemini Flash Image** can clean up whiteboard photos (reduce glare, sharpen text)
- **Interleaved mode** (`--slides --extract`) gives the richest output: transcript + visuals together

### What doesn't work well
- **Talking Head videos** produce mostly identical presenter frames — the scene detection triggers on minor lighting/gesture changes, not content changes
- **Default threshold (0.3)** is too sensitive for talking head format — produces many near-duplicate frames
- **Very short videos (<2 min)** may not have enough scene changes

### Recommended defaults by use case

**Quick slide grab (most videos):**
```bash
summarize "<url>" --slides --slides-max 8 --slides-scene-threshold 0.5 --slides-min-duration 5 --youtube web
```

**Maximum detail (screencasts, tutorials):**
```bash
summarize "<url>" --slides --slides-ocr --slides-max 15 --slides-scene-threshold 0.3 --youtube web
```

**Whiteboard/handwritten content:**
```bash
summarize "<url>" --slides --slides-ocr --slides-max 10 --slides-scene-threshold 0.4 --slides-min-duration 3 --youtube web
```

### Talking Head videos — special handling
Most DigitalXShift-style videos are talking head with occasional graphic inserts. For these:
1. Use high threshold (`0.5`) + high min-duration (`5s`) to only capture actual visual changes
2. Expect 2-4 useful slides per 10 minutes (graphic inserts, text overlays)
3. The **transcript** is more valuable than slides for these videos — use `ExtractTranscript` instead
4. If the video shows n8n workflows or screen recordings, lower threshold to `0.3`

### Output organization
- Slides saved to: `slides/youtube-<VIDEO_ID>/slide_NNNN_TIMEs.png`
- Include `--slides-dir` to control output location
- For batch processing: each video gets its own subdirectory automatically

## Tuning Parameters Reference

| Parameter | Default | Range | Effect |
|---|---|---|---|
| `--slides-max` | 6 | 1-50 | Hard cap on number of slides |
| `--slides-scene-threshold` | 0.3 | 0.1-1.0 | Higher = fewer slides, less sensitive |
| `--slides-min-duration` | 2 | 1-60 | Minimum seconds between captures |
| `--slides-dir` | ./slides | any path | Output directory for slide images |
| `--slides-ocr` | false | — | Run tesseract OCR on each slide |
| `--slides-debug` | false | — | Show file paths instead of inline |

## Prerequisites
- `tesseract` ✅ installed (v5.3.4 + deu language pack)
- `yt-dlp` ✅ installed (`${HOME}/.local/bin/yt-dlp` v2026.03.13)
- `ffmpeg` ✅ installed (v6.1.1)
- `GEMINI_API_KEY` ✅ in `${AGENT_HOME}/.env` (for AI image enhancement)
