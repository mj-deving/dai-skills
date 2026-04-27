# PremiumSite Workflow

Full 4-phase website creation: Design Foundation → Code → Assets → Deploy. ~1-2 hours, ~$10.

## Pre-Flight: Design Principles (Mandatory)

Before any code generation, read the **Core Principles** from `${SKILLS_HOME}/FrontendDesign/SKILL.md`:
- **Design Thinking** — commit to a bold aesthetic direction (purpose, tone, constraints, differentiation)
- **Frontend Aesthetics Guidelines** — typography, color, motion, spatial composition
- **Anti-AI-Slop Rules** — forbidden patterns and required alternatives

These principles inform every phase below. The taste-skill handles CSS-level specifics; FrontendDesign handles design-level thinking.

## Phase 0: Design Foundation

### Step 0a: Brand Soul

Ask Claude to define the brand:

```
Define the Brand Soul for a website about [TOPIC].
The mood should be [USER'S DESCRIPTION or "professional and modern"].
Give me: 5 adjectives, 3 hex colors, 2 font recommendations, 1 visual metaphor.
IMPORTANT: No generic AI terms like "innovative" or "cutting-edge".
```

### Step 0b: Moodboard (Optional)

Guide the user to collect 5-10 reference images:
- **Weavy AI** — Pinterest alternative for AI-driven moodboards
- Or: collect screenshots of websites they admire

### Step 0c: Color Palette

If the user has a moodboard, use **Flux 2 Pro** to generate a cohesive palette.
Otherwise, use the hex codes from the Brand Soul.

### Step 0d: Visual Anchor

Generate one key image that sets the design language:

```
# Nano Banana 2 prompt
"[VISUAL METAPHOR from Brand Soul], studio lighting, [DARK/WHITE] background, 
professional, high quality, no text"
```

### Step 0e: Logo (Optional)

Use **Ideogram V3** with strong negative prompts:

```
Minimalist logo for [BRAND], [STYLE].
NOT: gradient, 3D, realistic, photographic, busy, complex, 
multiple colors, generic, clip art, stock-like.
```

## Phase 1: Website Code

Follow QuickSite workflow (Steps 2-4) but inject Phase 0 outputs:

```
Use this skill to design a high-end website: https://github.com/Leonxlnx/taste-skill

Design a [DESCRIPTION] website.

Brand Soul: [ADJECTIVES from Phase 0]
Color Palette: [HEX CODES from Phase 0]
Visual Metaphor: [FROM Phase 0]
Fonts: [FROM Phase 0]

Requirements:
- [FROM USER]

Style: [soft/minimalist/brutalist based on Brand Soul]
DESIGN_VARIANCE: [6-8]
MOTION_INTENSITY: [7-8]
VISUAL_DENSITY: [3-5]

Output: Single self-contained HTML file with inline CSS and JS.
Responsive. No external dependencies except Google Fonts.
```

## Phase 2: AI-Generated Assets

Hand off to `Workflows/GenerateAssets.md`.

Key decisions:
- **Hero Background:** Seedance 2.0 (loop) or Kling 3.0 (3D rotation)
- **Scroll Animation:** Kling 3.0 (exploding view / product showcase)
- **Static Images:** Nano Banana 2

## Phase 3: Integration + Deploy

### Asset Integration

```
Take [hero-video.mp4] and make it the hero background.
Apply inward masking gradient (top + bottom).
Video: autoplay, muted, loop. Compress if > 500KB.
Fallback: keep CSS gradient for non-video browsers.
```

### Scroll Animation (if applicable)

```
Take [scroll-video.mp4] and create a scroll-triggered animation.
Extract frames as optimized JPEGs, bind to scroll position.
Add text sections that reveal as user scrolls.
```

### Performance Iteration (2-4 rounds)

```
Make it faster. Compress videos. Preload scroll frames. Optimize for mobile.
```

### Mobile Optimize (3-4 rounds)

```
Mobile optimize the site.
```

### Deploy

Hand off to `Workflows/DeploySite.md`.

## Output

- Professional website with Brand Soul, AI assets, video backgrounds
- Responsive and performance-optimized
- Deployed on Netlify with live URL
