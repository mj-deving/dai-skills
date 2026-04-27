# GenerateAssets Workflow

Generate AI images and videos for website hero sections and scroll animations.

## Step 1: Determine Asset Needs

Ask the user:
1. What kind of website is this for?
2. Hero background: ambient/loop (→ Seedance) or 3D product/rotation (→ Kling)?
3. Scroll animation needed? (exploding view, product showcase)
4. Color scheme: dark or light background?

## Step 2: Generate Images (Nano Banana 2)

**Platform:** Google Gemini API or key.ai

Let Claude Code generate the image prompts:

```
Generate 3 Nano-Banana-2 prompts for hero images that match a [DESCRIPTION] website.
Style: [dark/light], [BRAND SOUL adjectives if available].
Each prompt should produce a different angle/composition.
Include "no text" and "[white/dark] background" in each.
```

**Direct prompts if generating manually:**

```
# Abstract Tech Hero (Dark)
"Abstract 3D geometric shapes floating in space, dark background, 
[ACCENT COLOR] glow, depth of field, cinematic lighting, no text"

# Product/Object Hero (White)
"Photorealistic 3D render of [OBJECT], studio lighting, 
white background, professional product photography, no text"

# Scene Hero
"Cinematic [SCENE DESCRIPTION], professional lighting, 
depth of field, high quality, no text"
```

## Step 3: Generate Videos

### Option A: Seedance 2.0 (Loops — Hero Backgrounds)

**Platform:** fal.ai API (`bytedance/seedance-2.0/image-to-video`)

**Loop Trick (CRITICAL):**
1. Take the Nano Banana image from Step 2
2. The script automatically sends it as BOTH first AND last frame
3. This creates a seamless loop with no visible cut

**Automated (recommended):**
```bash
python Projekt-Factory/Scripts/seedance-video.py \
  --image hero-image.jpg \
  --prompt "Slow cinematic camera movement through the scene, particles floating, subtle glow pulsing" \
  --duration 10 --aspect 16:9 \
  -o hero-bg.mp4
```

**Manual fallback:** Use dreamina.capcut.com — upload image as first frame AND last frame.

**Settings:** 5-10 seconds, 16:9, 720p
**Cost:** ~$1.50-3.00 per video via fal.ai

### Option B: Kling 3.0 (3D — Scroll Animations)

**Platform:** klingai.com/dev or fal.ai

**Prompt templates:**
```
# Rotating Product
"High-quality 3D render style video of [OBJECT] slowly rotating 360 degrees, 
[white/dark] background, studio lighting, product photography"

# Exploding View
"High quality exploding view animation of [OBJECT], components 
separating in all directions, [white/dark] background, no text"
```

**Settings:** 5 seconds, 16:9, 1080p

### Decision Guide

| Use Case | Model | Why |
|---|---|---|
| Hero background (ambient, looping) | **Seedance 2.0** | Seamless loop trick |
| Product showcase (rotation) | **Kling 3.0** | Better 3D quality |
| Scroll animation (exploding view) | **Kling 3.0** | Frame-by-frame extraction |
| Architecture / interior scene | **Seedance 2.0** | Organic movement |

## Step 4: Download and Prepare

1. Download the best video (generate 2-3 variants, pick best)
2. Rename clearly: `hero-bg.mp4`, `scroll-explode.mp4`
3. Place in the website project directory

## Step 5: Integration Prompts

Provide these to the user for their Claude Code session:

**Hero Video:**
```
Take hero-bg.mp4 and make it the hero section background.
Autoplay, muted, loop. Apply inward masking gradient (top + bottom)
so the video fades into the page background. Compress if > 500KB.
```

**Scroll Animation:**
```
Take scroll-explode.mp4 and create a scroll-triggered animation.
Extract frames as optimized JPEGs, bind each to scroll position.
Add text overlays that appear between key frames.
```

## Cost Estimate

| Component | Cost |
|---|---|
| Nano Banana 2 (3 images) | $0.12-0.45 |
| Seedance 2.0 via fal.ai (2-3 videos) | $3-9 |
| Kling 3.0 (2-3 videos) | $3-5 |
| **Total assets** | **$6-15** |

## Automation

The Seedance pipeline is automated via `Projekt-Factory/Scripts/seedance-video.py`:

```bash
# Requires FAL_KEY env var (fal.ai API key)
# Loop video (hero background)
python seedance-video.py --image hero.jpg --prompt "..." -o hero-bg.mp4

# Text-to-video (no image)
python seedance-video.py --prompt "Abstract shapes floating" -o abstract.mp4

# Fast mode (cheaper)
python seedance-video.py --image hero.jpg --prompt "..." --fast -o hero-bg.mp4
```
